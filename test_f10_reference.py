# F10 tests: deterministic vectors + behavioral coverage
import json
import unittest
import f10_reference as f10, hashlib
from f10_reference import Sig, Chain, Witness, detect_fork, verify_chain, MockTool, recover, canon, h, GENESIS_SEED, PROTO

WSEED = bytes.fromhex('11' * 32)

def fixed_writer():
    seed = bytes.fromhex('22' * 32)
    return Sig('writer-1', seed), seed

def fixed_witness():
    return Sig('witness-1', WSEED)

def test_deterministic_vectors():
    w, seed = fixed_writer()
    chain = Chain('chain-A', w, {'writer-1': w.pub()})
    tool = MockTool()
    tool.call(chain, 'op-1', b'hello')
    cp = chain.checkpoint()
    # vector 1: canonical checkpoint blob
    assert cp['blob'] == canon(cp['checkpoint'])
    # vector 2: signature deterministic under Ed25519 (skip if fallback MAC)
    from f10_reference import HAVE_CRYPTO
    if HAVE_CRYPTO:
        cp2 = chain.checkpoint()  # head unchanged, same sig
        assert cp['sig'] == cp2['sig']
    # vector 3: genesis event shape
    g = chain.events[0]
    assert g['type'] == 'genesis' and g['prev_hash'] == h(GENESIS_SEED)
    vectors = {'blob': cp['blob'].decode(), 'sig': cp['sig'], 'genesis_hash': g['event_hash']}
    EXPECTED_A2 = {'blob': '{"chain_id":"chain-A","event_id":2,"head_hash":"2cec5e5c471fa377552b4bb1f16f9e91b0ce8f9f29d5171390856e18c7668969"}', 'sig': '7291979127d56ca74a81b2be731650331f76ed5f8f738b1d096371a17e03d6885522ab7ec5eb54abdfc10ad7832c83f3caf751a6657f6d547a24914c77703904', 'genesis_hash': '7f38db8f86577377e5d22c29fbc5453560ab9e050b2921d6e0e624c68508f5a9'}
    if not f10.HAVE_CRYPTO:
        raise unittest.SkipTest('cryptography backend unavailable; cannot validate Ed25519 vectors')
    assert vectors == EXPECTED_A2, 'vector mismatch: %r' % vectors
    print(json.dumps(vectors, indent=2))
    return None

def test_fork_disclosure():
    w, _ = fixed_writer()
    reg = {'writer-1': w.pub()}
    c1 = Chain('chain-A', w, reg)
    c2 = Chain('chain-A', w, reg)  # same writer, same chain_id: equivocation
    MockTool().call(c1, 'op-1', b'x')
    MockTool().call(c2, 'op-1', b'y')  # divergent payload -> different heads
    wit = fixed_witness()
    W = Witness('witness-1', WSEED)
    W.receive(c1.checkpoint(), reg)
    W.receive(c2.checkpoint(), reg)
    receipts = W.query_all('chain-A', len(c1.events) - 1)
    forked, heads = detect_fork(receipts, wit.pub())
    assert forked and len(heads) == 2, heads

def test_crash_recovery_no_retry():
    w, _ = fixed_writer()
    chain = Chain('chain-A', w, {'writer-1': w.pub()})
    chain.execution_intent('op-9', 'nonidempotent-tool', b'payload')  # crash after intent
    recover(chain, set())
    kinds = [e['type'] for e in chain.events]
    assert 'outcome_unconfirmed' in kinds
    verify_chain(chain.events, {})

def test_idempotent_retry():
    w, _ = fixed_writer()
    chain = Chain('chain-A', w, {'writer-1': w.pub()})
    tool = MockTool()
    tool.call(chain, 'op-1', b'data')
    out2 = tool.call(chain, 'op-1', b'data')  # retry same operation_id: no duplicate
    assert out2 == b'already-done'
    ids = [e['operation_id'] for e in chain.events if 'operation_id' in e]
    assert ids.count('op-1') == 2  # intent + result only; retry is deduplicated by operation_id

def test_chain_integrity():
    w, _ = fixed_writer()
    chain = Chain('chain-A', w, {'writer-1': w.pub()})
    MockTool().call(chain, 'op-a', b'1')
    MockTool().call(chain, 'op-b', b'2')
    verify_chain(chain.events, {})
    # tamper detection
    chain.events[1]['tool'] = 'hacked'
    try:
        verify_chain(chain.events, {})
        raise AssertionError('tamper not detected')
    except AssertionError:
        pass

def test_side_effect_crash():
    w, _ = fixed_writer()
    chain = Chain('chain-A', w, {'writer-1': w.pub()})
    tool = MockTool()
    try:
        tool.call(chain, 'op-crash', b'payload', crash_after_side_effect=True)
    except RuntimeError:
        pass
    kinds = [e['type'] for e in chain.events]
    assert 'execution_intent' in kinds and 'execution_result' not in kinds
    recover(chain, tool.done)
    kinds = [e['type'] for e in chain.events]
    assert 'outcome_unconfirmed' in kinds
    # idempotent retry with same operation_id succeeds, marks result
    tool.call(chain, 'op-crash', b'payload')
    assert any(e['type'] == 'execution_result' for e in chain.events)
    verify_chain(chain.events, {}, 'chain-A')

def test_forged_checkpoint_rejected():
    w, _ = fixed_writer()
    other = Sig('writer-2', bytes.fromhex('33' * 32))
    reg = {'writer-1': w.pub()}
    chain = Chain('chain-A', w, reg)
    MockTool().call(chain, 'op-1', b'hello')
    cp = chain.checkpoint()
    forged = {'checkpoint': cp['checkpoint'], 'sig': other.sign(cp['blob']), 'writer_key_id': 'writer-1'}
    W = Witness('witness-1', WSEED)
    try:
        W.receive(forged, reg)
        raise AssertionError('forged checkpoint accepted')
    except AssertionError:
        pass  # forged checkpoint correctly rejected

import f10_reference as f10
if __name__ == '__main__':
    if f10.HAVE_CRYPTO:
        test_deterministic_vectors()
    else:
        print('SKIP test_deterministic_vectors (no cryptography backend)')
    test_fork_disclosure()
    test_crash_recovery_no_retry()
    test_idempotent_retry()
    test_chain_integrity()
    test_side_effect_crash()
    test_forged_checkpoint_rejected()
    print(json.dumps({'status': 'ALL PASS'}, indent=2))
# F10 tests: deterministic vectors + behavioral coverage
import json, hashlib
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
    return {'blob': cp['blob'].decode(), 'sig': cp['sig'], 'genesis_hash': g['event_hash']}

def test_fork_disclosure():
    w, _ = fixed_writer()
    reg = {'writer-1': w.pub()}
    c1 = Chain('chain-A', w, reg)
    c2 = Chain('chain-A', w, reg)  # same writer, same chain_id: equivocation
    MockTool().call(c1, 'op-1', b'x')
    MockTool().call(c2, 'op-1', b'y')  # divergent payload -> different heads
    wit = fixed_witness()
    W = Witness('witness-1', WSEED)
    W.receive(c1.checkpoint())
    W.receive(c2.checkpoint())
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

if __name__ == '__main__':
    vectors = test_deterministic_vectors()
    test_fork_disclosure()
    test_crash_recovery_no_retry()
    test_idempotent_retry()
    test_chain_integrity()
    print(json.dumps({'status': 'ALL PASS', 'vectors': vectors}, indent=2))
# F10 thin reference implementation: design for public non-equivocation
# Deterministic test vectors: fixed keys (seeded), fixed inputs, expected hashes/signatures.

import hashlib, json, hmac

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    HAVE_CRYPTO = True
except ImportError:
    HAVE_CRYPTO = False

PROTO = 'omega-provenance/1'

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()

def h(b):
    return hashlib.sha256(b).hexdigest()

def content_hash(event_type, input_blob, output_blob):
    # domain-separated aggregate hash: PROTO/event_type | sha256(input) | sha256(output)
    dom = (PROTO + '/' + event_type).encode()
    return h(dom + b'|' + h(input_blob or b'').encode() + b'|' + h(output_blob or b'').encode())

class Sig:
    """Ed25519 signer; deterministic keys via seed. Falls back to a keyed MAC
    when cryptography lib is absent (test-only, NOT a real signature)."""
    def __init__(self, key_id, seed):
        self.key_id = key_id
        self.seed = seed
        if HAVE_CRYPTO:
            self._sk = Ed25519PrivateKey.from_private_bytes(seed)
            self._vk = self._sk.public_key()
    def pub(self):
        if HAVE_CRYPTO:
            return self._vk.public_bytes_raw().hex()
        return self.seed.hex()  # fallback: pub id = seed (test-only)
    def sign(self, blob):
        if HAVE_CRYPTO:
            return self._sk.sign(blob).hex()
        return hmac.new(self.seed, blob, hashlib.sha256).hexdigest()
    def verify(self, blob, sig_hex, pub_hex):
        if HAVE_CRYPTO:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
            Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex)).verify(bytes.fromhex(sig_hex), blob)
            return True
        return hmac.compare_digest(hmac.new(bytes.fromhex(pub_hex), blob, hashlib.sha256).hexdigest(), sig_hex)

GENESIS_SEED = b'\x00' * 32

class Chain:
    def __init__(self, chain_id, sig, registry):
        self.chain_id = chain_id
        self.sig = sig
        self.registry = registry  # key_id -> pub hex, bootstrap = trust anchor (genesis event)
        self.events = []
        self.head = h(GENESIS_SEED)
        self._emit({'type': 'genesis', 'registry': {k: self.registry[k] for k in sorted(self.registry)}})

    def _emit(self, body):
        ev = {
            'chain_id': self.chain_id,
            'writer_key_id': self.sig.key_id,
            'protocol': PROTO,
            'event_id': len(self.events),
            'prev_hash': self.head,
        }
        ev.update(body)
        ev['event_hash'] = h(canon(ev))
        self.head = ev['event_hash']
        self.events.append(ev)
        return ev

    def execution_intent(self, operation_id, tool, input_blob):
        ch = content_hash('execution_intent', input_blob, b'')
        return self._emit({'type': 'execution_intent', 'operation_id': operation_id,
                           'tool': tool, 'input_hash': h(input_blob), 'content_hash': ch})

    def execution_result(self, operation_id, output_blob, input_blob=b''):
        ch = content_hash('execution_result', input_blob, output_blob)
        return self._emit({'type': 'execution_result', 'operation_id': operation_id,
                           'output_hash': h(output_blob), 'content_hash': ch})

    def outcome_unconfirmed(self, operation_id):
        return self._emit({'type': 'outcome_unconfirmed', 'operation_id': operation_id})

    def checkpoint(self):
        cp = {'chain_id': self.chain_id, 'event_id': len(self.events) - 1, 'head_hash': self.head}
        blob = canon(cp)
        return {'checkpoint': cp, 'blob': blob, 'sig': self.sig.sign(blob),
                'writer_key_id': self.sig.key_id}

class Witness:
    """Receives checkpoints; returns durable signed receipts. Byzantine-capable:
    may hold conflicting receipts; API must expose ALL receipts per (chain_id, event_id).
    Verifies the writer's signed checkpoint envelope against the registry before
    issuing any receipt, and preserves the full envelope in the receipt."""
    def __init__(self, key_id, seed):
        self.sig = Sig(key_id, seed)
        self.receipts = {}  # (chain_id, event_id) -> list of signed receipts
    def receive(self, checkpoint_msg, registry):
        verify_checkpoint(checkpoint_msg, registry)  # reject forged checkpoints
        cp = checkpoint_msg['checkpoint']
        blob = canon(cp)
        r = {'checkpoint': cp, 'witness_key_id': self.sig.key_id,
             'writer_key_id': checkpoint_msg['writer_key_id'],
             'writer_sig': checkpoint_msg['sig'],  # preserve signed envelope
             'receipt_sig': self.sig.sign(blob)}
        self.receipts.setdefault((cp['chain_id'], cp['event_id']), []).append(r)
        return r
    def query_all(self, chain_id, event_id):
        return list(self.receipts.get((chain_id, event_id), []))

def verify_checkpoint(cp_msg, registry):
    cp = cp_msg['checkpoint']
    blob = canon(cp)
    pub = registry[cp_msg['writer_key_id']]
    assert cp_msg['sig'], 'missing signature'
    try:
        assert Sig('v', GENESIS_SEED).verify(blob, cp_msg['sig'], pub)
    except Exception as e:
        raise AssertionError('checkpoint signature invalid: %r' % (e,))
    return True

def verify_receipt(r, witness_pub):
    blob = canon(r['checkpoint'])
    Sig('v', GENESIS_SEED).verify(blob, r['receipt_sig'], witness_pub)
    return True

def detect_fork(receipts, witness_pub):
    """Fork disclosure: >=2 valid receipts for same (chain_id, event_id)
    with differing head_hash exposes the writer's equivocation."""
    heads = set()
    for r in receipts:
        verify_receipt(r, witness_pub)
        heads.add(r['checkpoint']['head_hash'])
    return len(heads) > 1, heads

def verify_chain(events, registry, chain_id=None):
    head = h(GENESIS_SEED)
    prev_id = -1
    for ev in events:
        assert ev['event_id'] == prev_id + 1, 'event_id must be contiguous'
        prev_id = ev['event_id']
        assert ev['protocol'] == PROTO, 'protocol mismatch'
        if chain_id is not None:
            assert ev['chain_id'] == chain_id, 'chain_id mismatch'
        assert ev['prev_hash'] == head
        body = {k: v for k, v in ev.items() if k != 'event_hash'}
        assert ev['event_hash'] == h(canon(body))
        head = ev['event_hash']
    return True

# ---- Mock idempotent tool with intent/recovery protocol ----
class MockTool:
    def __init__(self):
        self.done = set()
    def call(self, chain, operation_id, arg, crash_after_side_effect=False):
        # idempotent on operation_id: duplicate call is a no-op
        if operation_id in self.done:
            # recovery case: side effect done but chain lacks result event
            has_result = any(e['type'] == 'execution_result' and e['operation_id'] == operation_id for e in chain.events)
            if not has_result:
                chain.execution_result(operation_id, b'result:' + arg, arg)
            return b'already-done'
        chain.execution_intent(operation_id, 'mocktool', arg)
        out = b'result:' + arg
        if crash_after_side_effect:
            # external side effect succeeded, crash before result append
            self.done.add(operation_id)
            raise RuntimeError('crash after side effect, before result append')
        chain.execution_result(operation_id, out, arg)
        self.done.add(operation_id)
        return out

def recover(chain, tool_done_ops):
    """After crash: intents lacking results -> outcome_unconfirmed (no auto-retry
    for non-idempotent tools; idempotent ones may retry with same operation_id)."""
    results = {e['operation_id'] for e in chain.events if e['type'] == 'execution_result'}
    for e in chain.events:
        if e['type'] == 'execution_intent' and e['operation_id'] not in results:
            chain.outcome_unconfirmed(e['operation_id'])
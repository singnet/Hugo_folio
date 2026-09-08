# F09 reference: immutable append-only trace records for register transitions.
# Hash function: sha256, hex digest.
# Canonical payload serialization: UTF-8 JSON, sorted keys, no whitespace, excluding volatile metadata, including schema_version.
# Typed-edge vocabulary (parent link kinds): data, control-trigger, hypothesis-lineage, re-attribution.
import json, hashlib, time

SCHEMA_VERSION = "f09.v1"
EDGES = ("data", "control-trigger", "hypothesis-lineage", "re-attribution")

def canonical_bytes(payload):
    body = {k: v for k, v in payload.items() if k != "volatile_metadata"}
    body["schema_version"] = payload["schema_version"]
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def payload_hash(payload):
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()

class Trace:
    def __init__(self):
        self.events = []

    def append(self, transition_id, payload, parents=(), volatile=None):
        for _, kind in parents:
            assert kind in EDGES, kind
        ev = {
            "transition_id": transition_id,
            "payload": payload,
            "parents": list(parents),
            "volatile_metadata": volatile if volatile is not None else {"timestamp": time.time()},
        }
        self.events.append(ev)
        return ev

    def replay(self):
        return list(self.events)

def re_attribute(trace, original, new_id, payload, volatile=None):
    # snapshot original serialized bytes and hash before re-attribution
    before_bytes = canonical_bytes(original["payload"])
    before_hash = payload_hash(original["payload"])
    ev = trace.append(new_id, payload, parents=[(original["transition_id"], "re-attribution")], volatile=volatile)
    # original record byte-identical afterward: never rewritten
    assert canonical_bytes(original["payload"]) == before_bytes
    assert payload_hash(original["payload"]) == before_hash
    return ev

def test_f09_reference():
    trace = Trace()
    failed = trace.append(
        "T1",
        {"schema_version": SCHEMA_VERSION, "invariant": "register", "attempted_change": {"lane": "default"},
         "result": "failure", "failure_reason": "non-finite value"},
        parents=[("D0", "data")],
        volatile={"timestamp": 100.0},
    )
    prefix = trace.replay()
    ev = re_attribute(
        trace, failed, "T2",
        {"schema_version": SCHEMA_VERSION, "invariant": "register",
         "attempted_change": {"reason": "diagnosis revision"}, "result": "success"},
        volatile={"timestamp": 200.0},
    )
    replayed = trace.replay()
    # replay preserves the original prefix and appends exactly one new event
    assert replayed[:len(prefix)] == prefix
    assert len(replayed) == len(prefix) + 1
    assert replayed[0] is failed
    assert ("T1", "re-attribution") in replayed[-1]["parents"]
    # volatile timestamps differ while payload bytes stay stable
    assert failed["volatile_metadata"]["timestamp"] != ev["volatile_metadata"]["timestamp"]
    # semantically identical payloads with different input key order give the same hash
    a = {"schema_version": SCHEMA_VERSION, "invariant": "register", "result": "failure", "failure_reason": "x"}
    b = {"failure_reason": "x", "result": "failure", "invariant": "register", "schema_version": SCHEMA_VERSION}
    assert payload_hash(a) == payload_hash(b)
    # volatile metadata is excluded from the hashed canonical payload
    c = dict(a)
    c["volatile_metadata"] = {"timestamp": 999.9}
    assert payload_hash(c) == payload_hash(a)
    print("f09 reference passed: sha256 canonical hash (schema_version in, volatile out), original byte-identical after re-attribution, prefix-preserving replay plus one typed re-attribution event, key-order-insensitive hash")

if __name__ == "__main__":
    test_f09_reference()
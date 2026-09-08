# F09 v3: frozen, immutable, append-only trace records.
# Hash: sha256 hex. Canonical payload: UTF-8 JSON, sorted keys, no whitespace,
# excluding volatile metadata, including schema_version.
# Typed edges: data, control-trigger, hypothesis-lineage, re-attribution.
# Trace guarding: __slots__ plus __setattr__/__delattr__ that always reject,
# so the backing binding cannot be replaced or removed via normal Python
# assignment, including the mangled _Trace__events name. The only internal
# mutation path is append(), which uses object.__setattr__ under the guard.
import json, hashlib, time
from types import MappingProxyType

SCHEMA_VERSION = "f09.v3"
EDGES = ("data", "control-trigger", "hypothesis-lineage", "re-attribution")

def freeze(obj):
    if isinstance(obj, (dict, MappingProxyType)):
        return MappingProxyType(dict((k, freeze(v)) for k, v in obj.items()))
    if isinstance(obj, (list, tuple)):
        return tuple(freeze(v) for v in obj)
    return obj

def plain(obj):
    if isinstance(obj, (dict, MappingProxyType)):
        return dict((k, plain(v)) for k, v in obj.items())
    if isinstance(obj, tuple):
        return [plain(v) for v in obj]
    return obj

def canonical_bytes(payload):
    body = dict((k, v) for k, v in payload.items() if k != "volatile_metadata")
    return json.dumps(plain(body), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def payload_hash(payload):
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()

class Trace:
    __slots__ = ("__events",)

    def __init__(self):
        object.__setattr__(self, "_Trace__events", ())

    def __setattr__(self, name, value):
        raise AttributeError("Trace attributes are read-only")

    def __delattr__(self, name):
        raise AttributeError("Trace attributes cannot be deleted")

    @property
    def _events(self):
        return self.__events

    @property
    def events(self):
        return self.__events

    def append(self, transition_id, payload, parents=(), volatile=None):
        for p in parents:
            assert p[1] in EDGES, p[1]
        ev = freeze({
            "transition_id": transition_id,
            "payload": payload,
            "parents": list(parents),
            "volatile_metadata": volatile if volatile is not None else {"timestamp": time.time()},
        })
        object.__setattr__(self, "_Trace__events", self.__events + (ev,))
        return ev

    def replay(self):
        return self.events

def re_attribute(trace, original, new_id, payload, volatile=None):
    before_bytes = canonical_bytes(original["payload"])
    before_hash = payload_hash(original["payload"])
    ev = trace.append(new_id, payload, parents=[(original["transition_id"], "re-attribution")], volatile=volatile)
    assert canonical_bytes(original["payload"]) == before_bytes
    assert payload_hash(original["payload"]) == before_hash
    return ev

def expect_rejected(fn):
    try:
        fn()
    except (TypeError, AttributeError):
        return True
    raise AssertionError("mutation was not rejected")

def test_f09_frozen_successor():
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
    assert replayed[:len(prefix)] == prefix
    assert len(replayed) == len(prefix) + 1
    assert replayed[0] is failed
    assert ("T1", "re-attribution") in replayed[-1]["parents"]
    assert failed["volatile_metadata"]["timestamp"] != ev["volatile_metadata"]["timestamp"]
    a = {"schema_version": SCHEMA_VERSION, "invariant": "register", "result": "failure", "failure_reason": "x"}
    b = {"failure_reason": "x", "result": "failure", "invariant": "register", "schema_version": SCHEMA_VERSION}
    assert payload_hash(a) == payload_hash(b)
    c = dict(a)
    c["volatile_metadata"] = {"timestamp": 999.9}
    assert payload_hash(c) == payload_hash(a)

    stored_bytes = canonical_bytes(failed["payload"])
    stored_hash = payload_hash(failed["payload"])
    expect_rejected(lambda: failed["payload"].__setitem__("result", "tampered"))
    expect_rejected(lambda: failed["payload"]["attempted_change"].__setitem__("lane", "x"))
    expect_rejected(lambda: failed["payload"].__delitem__("failure_reason"))
    expect_rejected(lambda: failed["parents"].append(("X", "data")))
    events = trace.events
    expect_rejected(lambda: events.__setitem__(0, None))
    expect_rejected(lambda: events.__delitem__(0))
    expect_rejected(lambda: trace.events.append("T3"))
    expect_rejected(lambda: trace._events.append("T4"))
    # guarded binding: replacement and deletion rejected, including the mangled name
    expect_rejected(lambda: setattr(trace, "_Trace__events", ()))
    expect_rejected(lambda: setattr(trace, "_Trace__events", None))
    expect_rejected(lambda: delattr(trace, "_Trace__events"))
    expect_rejected(lambda: setattr(trace, "events", ()))
    expect_rejected(lambda: setattr(trace, "_events", ()))
    expect_rejected(lambda: setattr(trace, "anything", 1))
    assert len(trace.replay()) == len(replayed)
    assert trace.replay() == replayed
    assert canonical_bytes(failed["payload"]) == stored_bytes
    assert payload_hash(failed["payload"]) == stored_hash
    print("f09 v3 passed: guarded __setattr__/slots design, mangled binding replacement and deletion rejected, replay length and hashes intact; schema_version in, volatile out, prefix-preserving replay, key-order-insensitive sha256 all hold")

if __name__ == "__main__":
    test_f09_frozen_successor()

from f10_reference import Sig, Chain, Witness
from f10_receipts import GossipClient, gossip_merge

def test_adversarial_fork():
    writer = Sig("writer", b"W" * 32)
    registry = {"writer": writer.pub()}
    wA = Witness("wA", b"A" * 32)
    wB = Witness("wB", b"B" * 32)
    pubs = {"wA": wA.sig.pub(), "wB": wB.sig.pub()}
    roster = [(wA, pubs["wA"]), (wB, pubs["wB"])]
    # equivocating writer: two chains with same chain_id, same event_id, different heads
    chA = Chain("chain-R", writer, registry)
    chA.execution_intent("op1", "set", b"x")
    cpA = chA.checkpoint()
    chB = Chain("chain-R", writer, registry)
    chB.execution_intent("op2", "set", b"y")
    cpB = chB.checkpoint()
    # initially both witnesses only see cpA
    wA.receive(cpA, registry)
    wB.receive(cpA, registry)
    c1 = GossipClient("c1")
    c1.collect("chain-R", cpA["checkpoint"]["event_id"], roster, registry)
    r1 = c1.conflict_report("chain-R", cpA["checkpoint"]["event_id"], pubs, registry)
    assert r1["status"] == "NO_CONFLICT_OBSERVED", r1
    assert "not a claim none exists" in r1["note"]
    # witness A later reveals conflicting receipt cpB
    wA.receive(cpB, registry)
    assert len(wA.query_all("chain-R", cpA["checkpoint"]["event_id"])) == 2
    c2 = GossipClient("c2")
    c2.collect("chain-R", cpA["checkpoint"]["event_id"], roster, registry)
    r2 = c2.conflict_report("chain-R", cpA["checkpoint"]["event_id"], pubs, registry)
    assert r2["status"] == "FORK_EVIDENCE", r2
    assert len(r2["heads"]) == 2, r2
    # gossip merge: single-view client + full-view client -> durable fork evidence
    merged = gossip_merge(c1, c2)
    r3 = merged.conflict_report("chain-R", cpA["checkpoint"]["event_id"], pubs, registry)
    assert r3["status"] == "FORK_EVIDENCE", r3
    # single-view report never claims "no conflict exists"
    assert "no conflict exists" not in r1["note"]
    print("adversarial A/B fork test: PASS")

if __name__ == "__main__":
    test_adversarial_fork()
    print("ALL PASS")
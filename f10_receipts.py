from f10_reference import Sig, Chain, Witness, verify_receipt, canon

class GossipClient:
    """Collects receipts from roster witnesses per (chain_id, event_id),
    merges via gossip, reports conflict evidence without claiming completeness."""
    def __init__(self, client_id):
        self.client_id = client_id
        self.receipts = {}   # (chain_id, event_id) -> list of receipts
        self.assurance = {}  # (chain_id, event_id) -> witness_key_id -> ok/absent
    def collect(self, chain_id, event_id, roster):
        for w, pub in roster:
            rs = w.query_all(chain_id, event_id)
            status = "ok" if rs else "absent"
            self.assurance.setdefault((chain_id, event_id), {})[w.sig.key_id] = status
            if rs:
                for r in rs:
                    verify_receipt(r, pub)
                self.merge(rs)
    def merge(self, receipts):
        for r in receipts:
            cp = r["checkpoint"]
            k = (cp["chain_id"], cp["event_id"])
            bucket = self.receipts.setdefault(k, [])
            if not any(canon(x) == canon(r) for x in bucket):
                bucket.append(r)
    def conflict_report(self, chain_id, event_id, witness_pubs):
        """Returns report; NEVER claims absence of conflict elsewhere."""
        rs = self.receipts.get((chain_id, event_id), [])
        for r in rs:
            verify_receipt(r, witness_pubs[r["witness_key_id"]])
        heads = set(r["checkpoint"]["head_hash"] for r in rs)
        absent = sorted(k for k, a in self.assurance.get((chain_id, event_id), {}).items() if a == "absent")
        if len(heads) > 1:
            return {"status": "FORK_EVIDENCE", "heads": sorted(heads), "receipts": rs}
        return {"status": "NO_CONFLICT_OBSERVED", "heads": sorted(heads), "absent_witnesses": absent,
                "note": "no conflict observed; not a claim none exists"}

def gossip_merge(a, b):
    """Merge two clients' receipt sets: durable fork evidence."""
    for k, rs in b.receipts.items():
        a.merge(rs)
    for k, m in b.assurance.items():
        a.assurance.setdefault(k, {}).update(m)
    return a
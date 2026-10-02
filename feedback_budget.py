# rev9: interactive feedback protocol/budget module
# Per approved rev9_open_items_proposal.md:
# - Q = 10 evaluator queries per episode (raw J only)
# - Diagnostics: raw J plus one gradient-free scalar (loss delta vs previous query)
# - Duplicate queries count against budget but return no new info

Q_DEFAULT = 10
Q_REDUCED = 5  # for higher-dimensionality feedback tasks e.g. fm_kernel_loss

class FeedbackBudget:
    def __init__(self, q=Q_DEFAULT, dup_tolerance=1e-9):
        self.q = q
        self.dup_tolerance = dup_tolerance
        self.used = 0
        self.prev_j = None
        self.seen_queries = []

    def remaining(self):
        return max(0, self.q - self.used)

    def submit(self, query, j_value):
        # returns dict with raw J and scalar delta, or None if exhausted/duplicate
        if self.used >= self.q:
            return None
        self.used += 1
        delta = None
        if not self._is_duplicate(query):
            self.seen_queries.append(query)
            if self.prev_j is not None:
                delta = self.prev_j - j_value  # improvement vs previous query
            self.prev_j = j_value
            return {"j": j_value, "delta": delta, "duplicate": False}
        # duplicate: budget consumed, no new information
        return {"j": None, "delta": None, "duplicate": True}

    def _is_duplicate(self, query):
        return any(abs(query - s) <= self.dup_tolerance for s in self.seen_queries)

def main():
    # Wire-up to evaluator/oracle at episode start; ledger records per-query cost.
    raise NotImplementedError

if __name__ == "__main__":
    main()
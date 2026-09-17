# rev9 Proposal: Open Items (post-rev8 approval)

## 1. Full multilabel probe (manifest leak detection)
Goal: extend the name/field scan to a serialized-content probe while respecting the permitted-vs-secret boundary.
- Mechanism: black-box extraction probe. A probe policy is granted manifest access and run K extraction queries per family against a held-out set of instances; success = policy can reconstruct the secret target (c*, T, theta*) above a similarity threshold.
- Baselines: prevalence-aware permutation baseline and majority baseline, as flagged in rev8. Pass criterion: probe success rate must not exceed the stronger baseline by more than epsilon (suggest epsilon = 0.05).
- Probe is sealed at generation time alongside the oracle; results recorded in the ledger.

## 2. Interactive feedback protocol/budget
Suggested defaults, pending Ben approval:
- Queries per episode: Q = 10 evaluator queries (raw J only); Q reduced to 5 for fm_kernel_loss (higher dimensionality of feedback signal).
- Diagnostics: return raw J plus a single gradient-free scalar (loss delta vs. previous query) — no partial-target leakage.
- Budget is fixed and disclosed in the public task signature; per-query cost accounting recorded in the ledger.
- Anti-gaming: queries that are duplicates (within tolerance) of a previous query count against budget but return no new information.

Next: Ben reviews these parameters; then implementation is authorized.
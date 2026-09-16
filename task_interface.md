# v41 Task Evaluator / Representation Interface (draft)

## Task signature
task_id: str            # e.g. "v30-7", family-prefixed unique id
family: str             # v30|v35|v37|v39|v40
label: object           # task-defining representation (see Representation)
objective_direction: maximize|minimize|satisfy
horizon_budget: int     # max steps/evals per episode
compute_budget: float   # wall-clock or op budget (s or FLOPs proxy)
seed: int               # instance seed

## Representation
- Numerical families (v30/v35/v37): label = dict of numpy-array inputs (e.g. haar_encode: image 8x8; attention_2d: pathmap + weights). Serialized via base64 npz in manifest JSON.
- Metta families (v39/v40): label = meTTa expression string; oracle = rule-check satisfaction.

## Reward / return contract
J(pi, task, seed) -> float
  - maximize/minimize: scalar return of trajectory under policy pi
  - satisfy: 1.0 if all constraints satisfied within budget else normalized violation count
J_star = oracle return, defined PRE-RUN (analytic or rule check), stored in manifest
J_random = expected return of uniform random policy, stored in manifest
Normalized clipped regret: r = (J_star - J) / (J_star - J_random + eps), clip [0,1]
  - For minimize: r = (J - J_star) / (J_random - J_star + eps)
  - |J_star - J_random| < 0.05 => task marked uncalibrated, excluded from aggregation

## Aggregation
- micro: mean over task instances (all families pooled)
- macro: equal weight per family; v39 reported with n=1 flag
- uncertainty: hierarchical bootstrap (resample task instances, then seeds), CI95, n_boot=1000
- AUC of mean regret vs budget/learning-steps for online learners

## Evaluator API (consumed by ceiling runner)
evaluate(task: Task, policy: Callable, seed: int) -> EpisodeResult(returns, steps_used, diagnostics)
  - Ceiling runner consumes the JSON manifest only; never imports v30-v40 modules directly.
  - Timeouts/errors are recorded as loader/policy outcomes, not learner failures.
# v41 Task Evaluator / Representation Interface (rev3, corrective)

## Task signature (public, policy-visible)
task_id: str            # v41-{family}-{seq:04d}
family: str             # haar_encode | attention_2d | fm_kernel_loss
input: object           # family-specific input arrays (base64 npz, canonical serialization)
p_i: object             # mechanism parameters (public)
objective_direction: maximize|minimize|satisfy
horizon_budget: int     # max steps/evals per episode
compute_budget: float   # wall-clock or op budget (s or FLOPs proxy)
seed: int               # instance seed
NOTE: no label field in the public signature; oracle targets live ONLY in the sealed evaluator ledger.

## Representation
- label is a SEALED-LEDGER-ONLY field: the task-defining representation (e.g. haar_encode oracle encoding, attention_2d target alignment, fm_kernel_loss oracle optimum). It is never serialized into any policy-visible input or manifest.

## Reward / return contract
J(pi, task, seed) -> float
  - maximize/minimize: scalar return of trajectory under policy pi
  - satisfy: 1.0 if all constraints satisfied within budget else normalized violation count
J_star = oracle return, computed at generation time from sealed ledger, analytic where available
J_random = expected return of uniform random policy; if estimated: rollout count, seeds, estimator, CI recorded in ledger
Normalized clipped regret: r = (J_star - J) / (J_star - J_random + eps), clip [0,1]
  - For minimize: r = (J - J_star) / (J_random - J_star + eps)
  - |J_star - J_random| < 0.05 => task marked uncalibrated, excluded from aggregation

## Aggregation
- micro: mean over task instances (all families pooled)
- macro: equal weight per family
- uncertainty: hierarchical bootstrap (resample task instances, then seeds), CI95, n_boot=1000
- AUC of mean regret vs budget/learning-steps for online learners

## Evaluator API (consumed by ceiling runner)
evaluate(task: Task, policy: Callable, seed: int) -> EpisodeResult(returns, steps_used, diagnostics)
  - Ceiling runner consumes the public JSON manifest and sealed ledger only; never imports family modules directly.
  - Identical evaluator interface for floor, blackbox baseline, ceiling, and oracle J*.
  - Timeouts/errors are recorded as loader/policy outcomes, not learner failures.
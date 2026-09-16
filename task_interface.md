# v41 Task Evaluator / Representation Interface (rev4, corrective)

## Task signature (public, policy-visible)
task_id: str            # v41-{family}-{seq:04d}
family: str             # haar_encode | attention_2d | fm_kernel_loss
input: object           # family-specific input arrays (base64 npz, canonical serialization)
p_i: object             # mechanism parameters (public)
objective_direction: maximize|minimize|satisfy
horizon_budget: int     # max steps/evals per episode
compute_budget: float   # wall-clock or op budget (s or FLOPs proxy)
seed: int               # instance seed
NOTE: no label field in the public signature; oracle targets live ONLY in the sealed ledger.

## Trusted evaluator service vs policy/runner boundary (BLOCKER FIX)
- A TRUSTED EVALUATOR SERVICE reads the sealed ledger and computes J, J_star, J_random. It is the only component with ledger access.
- The POLICY and the RUNNER receive only the public manifest and evaluator responses (scalar returns, diagnostics). They never read the ledger via file reads, imports, or serialization.
- Runner: orchestrates episodes, enforces budgets, records outcomes; delegates all reward computation to the evaluator service.

## Per-family action/output schema (public)
- haar_encode: policy outputs a coefficient vector (float array, fixed dim per instance); evaluator returns reconstruction/regret via sealed oracle encoding.
- attention_2d: policy outputs a full attention weight matrix W (nonneg row-stochastic, fixed shape per instance); evaluator scores alignment against sealed target matrix.
- fm_kernel_loss: policy outputs kernel/parameter vector (float array, box-constrained per instance); evaluator evaluates kernel loss at sealed oracle optimum calibration.

All outputs validated for shape/type by the evaluator service; malformed output is recorded as a policy outcome.

## Reward / return contract
J(pi, task, seed) -> float
  - maximize/minimize: scalar return of trajectory under policy pi
  - satisfy: 1.0 if all constraints satisfied within budget else normalized violation count
J_star = oracle return, computed at generation time by evaluator service, analytic where available
J_random = expected return of uniform random policy; if estimated: rollout count, seeds, estimator, CI recorded in ledger
Normalized clipped regret: r = (J_star - J) / (J_star - J_random + eps), clip [0,1]
  - For minimize: r = (J - J_star) / (J_random - J_star + eps)
  - |J_star - J_random| < 0.05 => task marked uncalibrated, excluded from aggregation

## Aggregation
- micro: mean over task instances (all families pooled)
- macro: equal weight per family
- uncertainty: hierarchical bootstrap (resample task instances, then seeds), CI95, n_boot=1000
- AUC of mean regret vs budget/learning-steps for online learners

## Evaluator API (consumed by runner)
evaluate(task: Task, policy_output: object, seed: int) -> EpisodeResult(returns, steps_used, diagnostics)
  - Runner passes public manifest + policy output to the trusted evaluator service; never imports family modules or the ledger directly.
  - Identical evaluator interface for floor, blackbox baseline, ceiling, and oracle J*.
  - Timeouts/errors recorded as policy outcomes, not learner failures.
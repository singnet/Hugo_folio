# v41 Eval Rev2 Spec (rev8, corrective)

## Canonical return convention (all families)
Every family reports a single scalar return J, always maximized. Regret derived only from J: r_raw = (J* - J)/(J* - J_random + eps), clip [0,1] presentation-only; aggregation uses unclipped values.

## Exact reward semantics (mathematical)
- haar_encode: input X in R^{n x d}. Policy outputs c in box [lo, hi]^k. J = -(1/k) sum_j (c_j - c*_j)^2, c* sealed oracle Haar encoding. J* = 0.
- attention_2d: input tokens H in R^{n x d}. Policy outputs W in R^{n x n}, nonnegative row-stochastic. Canonical target: T is defined as the row-normalized target matrix, computed once at generation time; the oracle is defined solely against this canonical row-stochastic T. J = -||W - T||_F^2 / n^2. Unique maximizer W = T; J* = 0.
- fm_kernel_loss: canonical return J = -L(theta), L(theta) = (1/m) sum_i max(0, 1 - y_i f_theta(x_i)) + lambda ||theta||^2, theta in box B. Always maximize J; all regret math uses J only. J* = -L(theta*) at sealed oracle optimum theta*.
- satisfy: J = 1.0 if all constraints hold within budget else 1 - (violations/total_constraints), bounded [0,1].
- Exact random policy per family: haar_encode: uniform iid in [lo, hi]^k; attention_2d: uniform row-stochastic (Dirichlet(1,...,1) per row); fm_kernel_loss: uniform iid in box B. J_random = expectation over at least 100 seeded rollouts, estimator + CI recorded in ledger.
- If |J* - J_random| < 0.05 the instance is uncalibrated, excluded from aggregation (micro and macro).

## Malformed-output anti-gaming (fixed pre-generation formula)
- Shape/type-invalid outputs and timeouts receive a fixed worst-case return computed at generation time, before any policy runs: J_worst = 2*J_random - J* - 2*eps. Regret then equals (J* - J_worst)/(J* - J_random + eps) = (2(J* - J_random) + 2*eps)/(J* - J_random + eps) = 2 exactly, consistent with the documented denominator. This depends only on sealed generation-time quantities, never on observed policy results. Malformed outputs are aggregated with J_worst, never excluded. A policy cannot evade aggregation by failing.

## Permitted-vs-secret boundary and p_i status
- p_i is an intended public mechanism: fully specifies instance mechanics; only the sealed oracle target (c*, T, theta*) is hidden and must be learned from evaluator responses.
- Sealed ledger only (trusted evaluator service access): oracle label, c*, T, theta*, J* values, oracle instances.
- Policy-visible: public task signature, p_i, per-family action/output schema, evaluator responses (raw J, diagnostics).
- Trusted evaluator service computes all rewards; policy and runner never access the ledger.

## Manifest scan
- Scan task JSON manifests for serialized fields: label, target, encoding, optimum, policy-positive.oracle. Checked at generation, post-edit, pre-publish; any hit blocks publication.
- Name/field scan only; full multilabel probe remains an open item for Ben design review.

## Open items for Ben design review
- Full multilabel probe (permitted-p_i control, prevalence-aware permutation and majority baselines).
- Interactive feedback protocol/budget (queries per episode, diagnostics returned) - design decision required before implementation.
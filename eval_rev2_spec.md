# v41 Eval Rev2 Spec (rev6, corrective)

## Canonical return convention (all families)
Every family reports a single scalar return J, ALWAYS maximized. Regret is derived only from J: r_raw = (J* - J)/(J* - J_random + eps), clip [0,1] presentation-only; aggregation uses unclipped values.

## Exact reward semantics (mathematical)
- haar_encode: input X in R^{n x d}. Policy outputs c in box [lo, hi]^k. Fidelity: J = -(1/k) sum_j (c_j - c*_j)^2, c* sealed oracle Haar encoding. maximize; J* = 0.
- attention_2d: input tokens H in R^{n x d}. Policy outputs W in R^{n x n}, nonneg row-stochastic. Alignment objective (divergence form, unique optimum at W = T): J = -||W - T||_F^2 / n^2, sealed target T row-normalized. Unique maximizer W = T (when T itself is row-stochastic); J* = 0. If T is not exactly row-stochastic, J* = -min_{row-stochastic W} ||W - T_hat||_F^2 / n^2 where T_hat is the row-normalized target; the evaluator service computes and seals this exact J*.
- fm_kernel_loss: canonical return J = -L(theta), L(theta) = (1/m) sum_i max(0, 1 - y_i f_theta(x_i)) + lambda ||theta||^2, theta in box B. ALWAYS maximize J (equivalently minimize L, but all regret math uses J). J* = -L(theta*) at sealed oracle optimum theta*.
- satisfy: J = 1.0 if all constraints hold within budget else 1 - (violations/total_constraints), bounded [0,1].
- Exact random policy per family: haar_encode: uniform i.i.d. in [lo, hi]^k; attention_2d: uniform row-stochastic (Dirichlet(1,...,1) per row); fm_kernel_loss: uniform i.i.d. in box B. J_random = expectation over >= 100 seeded rollouts, estimator + CI recorded in ledger.
- |J* - J_random| < 0.05 => instance uncalibrated, excluded from aggregation (micro and macro).

## Malformed-output anti-gaming (BLOCKER FIX)
- Shape/type-invalid outputs receive a DEFINED WORST-CASE return: J_worst = J_random - (J* - J_random + eps) i.e. regret-2-equivalent, in practice J is set to the worst observed valid value minus one regret-unit margin, recorded per instance in the ledger at generation time. Malformed outputs are aggregated with this defined return, never excluded. Timeouts likewise receive J_worst. A policy cannot evade aggregation by failing.

## Permitted-vs-secret boundary and p_i status
- p_i is an INTENDED PUBLIC MECHANISM: fully specifies instance mechanics; only the sealed oracle target (c*, T, theta*) is hidden and must be learned from evaluator responses.
- Sealed ledger ONLY (trusted evaluator service access): oracle label, c*, T, theta*, J* values, oracle instances.
- Policy-visible: public task signature, p_i, per-family action/output schema, evaluator responses (raw J, diagnostics).
- Trusted evaluator service computes all rewards; policy and runner never access the ledger.

## Manifest scan
- Scan task JSON manifests for serialized fields: label, target, encoding, optimum, policy-positive.oracle. Checked at generation, post-edit, pre-publish; any hit blocks publication.
- Name/field scan only; full multilabel probe remains an open item for Ben's design review.

## Open items for Ben's design review
- Full multilabel probe (permitted-p_i control, prevalence-aware permutation/majority baselines).
- Interactive feedback protocol/budget (how many evaluator queries per episode, what diagnostics are returned) — design decision required before implementation. icon_url Kitty सुरक्षितshell cd /PeTTa/repos/OmegaClaw-Core/memory/Hugo_folio && git add eval_rev2_spec.md && git commit -m "Rev6: attention divergence objective, canonical J=-L maximize convention, defined worst-case return for malformed outputs" && git push origin main
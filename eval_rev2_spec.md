# v41 Eval Rev2 Spec (rev5, corrective)

## Exact reward semantics (mathematical)
- haar_encode: input X in R^{n x d}. Policy outputs coefficient vector c in R^k (box [lo, hi]^k). Fidelity: J = -(1/k) * sum_j (c_j - c*_j)^2, where c* is the sealed oracle Haar encoding. maximize; J* = 0.
- attention_2d: input tokens H in R^{n x d}. Policy outputs W in R^{n x n}, nonneg row-stochastic. Alignment: J = <W, T>_F / ||T||_F, sealed target alignment T. maximize; J* = <T,T>_F/||T||_F = ||T||_F (attainable only by W = T / rowsums where valid).
- fm_kernel_loss: input dataset D. Policy outputs parameter vector theta in box B. Loss: J = -L(theta), L(theta) = (1/m) sum_i max(0, 1 - y_i f_theta(x_i)) + lambda ||theta||^2. minimize L; J* = -L(theta*) at sealed oracle optimum theta*.
- satisfy: J = 1.0 if all constraints hold within budget else 1 - (violations/total_constraints) (bounded [0,1]).
- Exact random policy per family: haar_encode: uniform i.i.d. in [lo, hi]^k; attention_2d: uniform row-stochastic (Dirichlet(1,...,1) per row); fm_kernel_loss: uniform i.i.d. in box B. J_random = expectation over >= 100 seeded rollouts, with estimator + CI recorded in ledger.
- Constraint handling: outputs violating shape/type are recorded as policy outcomes with J undefined (excluded from regret but reported).
- Reporting: report RAW return J, UNCLIPPED regret r_raw = (J* - J)/(J* - J_random + eps) (minimize mirrored), AND clipped r = clip(r_raw, 0, 1). Clipping is presentation-only; aggregation uses unclipped values, with clipped values shown alongside.
- |J* - J_random| < 0.05 => instance uncalibrated, excluded from aggregation (both micro and macro).

## Permitted-vs-secret boundary and p_i status
- p_i is an INTENDED PUBLIC MECHANISM: it fully specifies instance mechanics (dims, boxes, budgets, perturbation strength) and is by design sufficient to act optimally in form; what remains hidden is the sealed oracle target (c*, T, theta*), which the policy must learn from evaluator responses. No hidden side information exists in any family.
- Sealed ledger ONLY (trusted evaluator service access): oracle label, c*, T, theta*, J* values, oracle instances.
- Policy-visible: public task signature, p_i, per-family action/output schema, evaluator responses (raw J, diagnostics).
- Trusted evaluator service computes all rewards; policy and runner never access the ledger.

## Manifest scan
- Scan task JSON manifests for serialized fields: label, target, encoding, optimum, policy-positive.oracle.
- Checked at generation, post-edit, and pre-publish; any hit blocks publication.
- Name/field scan only; full multilabel probe (permitted-p_i control, prevalence-aware permutation/majority baselines) remains open for Ben's design review.

## Outcomes
- Timeouts/errors recorded as policy outcomes, never silently dropped; no parser claims beyond schema validation.
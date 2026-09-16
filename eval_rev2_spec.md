# v41 Eval Rev2 Spec (rev4, corrective)

## Exact reward semantics
- J_star and J_random computed at generation time by the trusted evaluator service; audit trail (values, seeds, estimator, CI) recorded.
- Normalized clipped regret: r = (J_star - J) / (J_star - J_random + eps), clip [0,1]; for minimize: r = (J - J_star) / (J_random - J_star + eps).
- |J_star - J_random| < 0.05 => instance marked uncalibrated, excluded from aggregation.

## Permitted-vs-secret boundary
- Sealed ledger ONLY (evaluator service access): oracle label, target encoding, J_star values, family-specific oracle instances.
- Policy-visible: task signature (task_id, family, input, p_i, objective_direction, horizon_budget, compute_budget, seed), per-family action/output schema, and evaluator responses.
- Trusted evaluator service computes all rewards; policy and runner never access the ledger.

## Manifest scan (renamed; was mislabeled multilabel leak audit)
- Scan task JSON manifests for serialized fields: label, target, encoding, optimum, policy-positive.oracle.
- Checked at generation, post-edit, and pre-publish; any hit blocks publication.
- NOTE: this is a name/field scan only. The full multilabel probe (permitted-p_i control and prevalence-aware permutation/majority baselines) is NOT yet specified and remains an open item pending Ben's design review.

## Outcomes
- Timeouts/errors recorded as policy outcomes, never silently dropped. Parser-specific claims removed: no v41 policy parsing is required beyond schema validation of outputs.

## Safeguards inherited from rev3/4
- Exact reward semantics and normalization as above.
- Sealed ledger boundary enforced at generation and evaluation, with the trusted evaluator service as sole ledger reader.
- Manifest scan on every emitted artifact.
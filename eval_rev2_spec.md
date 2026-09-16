# v41 Eval Rev2 Spec (rev3, corrective)

## Exact reward semantics
- J_star and J_random computed at generation time from the sealed ledger; audit trail (values, seeds, estimator, CI) recorded.
- Normalized clipped regret: r = (J_star - J) / (J_star - J_random + eps), clip [0,1]; for minimize: r = (J - J_star) / (J_random - J_star + eps).
- Elastic instances excluded if |J_star - J_random| < 0.05 => marked uncalibrated, excluded from aggregation.

## Permitted-vs-secret boundary
- Sealed ledger ONLY: oracle label, target encoding, J_star values, family-specific oracle instances.
- Policy-visible: task signature (task_id, family, input, p_i, objective_direction, horizon_budget, compute_budget, seed) and the evaluator API.
- No policy may access the ledger via file reads, imports, or serialization.

## Multilabel leak audit
- Scan task JSON manifests for serialized fields: label, target, encoding, optimum, policy-positive.oracle.
- Checked at generation, post-edit, and pre-publish; any hit blocks publication.

## Parser rules
- Policies must parse only the public manifest schema; malformed input => recorded as loader outcome, not learner failure.
- Timeouts/errors recorded as loader/policy outcomes, never silently dropped.

## Safeguards inherited from rev3/4
- Exact reward semantics and normalization as above.
- Sealed ledger boundary enforced at generation and evaluation.
- Multilabel leak audit on every emitted artifact.
- Parser rules for all policy-adapter loaders.
# v41 Difficulty Calibration Plan (rev2, corrective — proposal-only, pending review)

Status: PROPOSAL ONLY (draft per Protomega verification of 92dfa28). Not an implementation authorization; awaiting Ben's design review.

Goal: hard-but-tractable test problems that discriminate strong ML learners from weak baselines.

## Families under proposal (v41)
1. haar_encode: learn a Haar-basis encoding matching a sealed oracle encoding c*.
2. attention_2d: 2D attention alignment against a sealed target matrix T.
3. fm_kernel_loss: optimize a kernel-loss objective with sealed oracle optimum theta*.

All v30/v35/v37/v39/v40 framings (lifecycle, resource-bounded, adversarial composition, quarantine, cutset) are WITHDRAWN and superseded by v41.

## Calibration protocol
1. Baseline floor: random, nearest-neighbor, simple gradient learner — should clearly fail (regret near 1).
2. Strong ceiling: modern RL/meta-learner — should partially succeed (regret meaningfully below 1).
3. Iterate constraints (dimensionality, horizon/compute budgets, perturbation strength) until sweet spot.
4. Exclude uncalibrated instances: |J_star - J_random| < 0.05.

## Safeguards (per eval_rev2_spec.md rev5)
- Exact mathematical reward semantics per family, with RAW returns and UNCLIPPED regret reported alongside clipped (presentation-only) regret; aggregation uses unclipped values.
- Sealed ledger boundary: trusted evaluator service is sole ledger reader; policy/runner see only public manifest + evaluator responses. p_i is an intended public mechanism.
- Manifest scan (name/field scan only) on every emitted artifact; full multilabel probe remains an open item for Ben's design review.
- Loader outcomes: timeouts/errors and shape-invalid outputs recorded as policy outcomes, never silently dropped; no parser claims beyond schema validation.

Next steps: Ben's design review of the proposal; baselines only after approval. Rev5/eval-rev2 spec updating; rev4 stands until push.
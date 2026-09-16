# v41 Difficulty Calibration Plan (rev2, corrective — proposal-only, pending review)

Status: PROPOSAL ONLY. v41 families and evaluator design are new; nothing here is approved until reviewers (Ben, Protomega) sign off.

Goal: hard-but-tractable test problems that discriminate strong ML learners from weak baselines.

## Families under proposal (v41)
1. haar_encode: learn a Haar-basis encoding that matches a sealed oracle encoding.
2. attention_2d: 2D attention alignment against a sealed target alignment matrix.
3. fm_kernel_loss: optimize a kernel-loss objective with a sealed oracle optimum.

All v30/v35/v37/v39/v40 framings (lifecycle, resource-bounded, adversarial composition, quarantine, cutset) are WITHDRAWN and superseded by v41.

## Calibration protocol
1. Baseline floor: random, nearest-neighbor, simple gradient learner — should clearly fail (regret near 1).
2. Strong ceiling: modern RL/meta-learner — should partially succeed (regret meaningfully below 1).
3. Iterate constraints (dimensionality, horizon/compute budgets, perturbation strength) until sweet spot.
4. Exclude uncalibrated instances: |J_star - J_random| < 0.05.

## Safeguards (inherited rev3/4)
- Exact reward semantics and normalized clipped regret per eval_rev2_spec.md.
- Sealed ledger boundary and multilabel leak audit per eval_rev2_spec.md.
- Parser rules: loader errors recorded, never silently dropped.

Next steps: run baselines once evaluator scaffolding is approved. Rev5/eval-rev2 paused; rev4 stands.
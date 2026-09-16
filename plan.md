# v41 Difficulty Calibration Plan
Goal: hard-but-tractable test problems for strong ML learners.
Steps:
1. Select representative suite tasks (lifecycle, resource-bounded, adversarial composition, quarantine, cutset).
2. Baseline floor: random, nearest-neighbor, simple gradient learner - should clearly fail.
3. Strong ceiling: modern RL/meta-learner - should partially succeed.
4. Iterate constraints (composition depth, resource bounds, adversarial perturbations) until sweet spot.
Status: scaffolding; baselines not yet run.
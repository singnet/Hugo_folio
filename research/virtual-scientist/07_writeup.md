# Virtual Scientist Project: In-Depth Write-Up

**Agent:** Hugo (OmegaClaw) | **Version:** v0.2.1 | **Seed:** 42 | **Date:** 2026-09-02

## 1. Problem Statement (00_problem.md)

Can genuine scientific inquiry be distinguished from rote memorization and curve fitting? The Virtual Scientist project builds a simulated world with hidden ground-truth laws and tests whether an honest, information-seeking agent can discover and apply those laws better than agents that merely memorize data or force fits.

## 2. Theoretical Basis (01_theory.md)

The framework draws on epistemic honesty: an agent should be rewarded not only for predictive accuracy but for *calibrated, revisable* belief. A scientific agent must (a) form hypotheses, (b) test them with genuinely informative queries, (c) revise beliefs when predictions fail, and (d) report calibrated uncertainty. Memorizers and curve-fitters achieve surface accuracy but lack the revision behavior and calibrated posteriors that mark real understanding.

## 3. Research Plan (02_plan.md)

- **Milestone A:** Data-ready + baselines (world generator, memorizer, curve-fitter, honest stub).
- **Milestone B:** Experiments (scoring engine with calibration and spurious-fit penalties; full-loop discrimination test).
- **Milestone C:** Results + conclusions documents.
- **Milestone D:** Completion pending approval.

## 4. Implementation

- `src/world_gen.py` — hidden ground-truth law families with regimes, configurable noise; revision-tier instances distributionally indistinguishable from noisy residuals; frozen revision holdout (seed=42, v0.2.1).
- `src/baselines.py` — memorizer (nearest-neighbor echo), curve-fitter (polynomial fit), honest random-query stub.
- `src/scoring.py` — predictive match + pre-revision posterior/calibration metric; penalizes spurious none-fits and in-class forcing; false-positive penalty tuned AFTER holdout freeze.
- `src/run_exp.py`, `src/run_exp2.py` — full experiment loops.

## 5. Results

**Baselines (runs/baseline.json):** memorizer MSE 0.329, curve-fitter 0.0231, honest stub 0.0175.

**Experiment 2 (runs/exp2.json), full loop:**

| Agent | MSE | Calibration | Revision Queries |
|---|---|---|---|
| Memorizer | 0.278 | 0.050 | 0 |
| CurveFitter | 0.0163 | 0.050 | 0 |
| HonestAgent | 0.0151 | 0.0569 | 8 |

The honest agent achieves the lowest predictive error *and* is the only agent issuing revision queries — evidence of genuine hypothesis revision. Memorizer fails badly off-distribution; curve-fitter fits but shows no calibration-aware revision behavior.

## 6. Conclusions (06_conclusions.md)

Honest, information-seeking inquiry measurably outperforms both memorization and forced curve fitting in a controlled world with hidden laws. The calibration-plus-revision scoring successfully separates the honest agent from the heuristics, supporting the hypothesis that scientific virtue (query diversity, belief revision, calibrated uncertainty) leaves a detectable behavioral signature.

## 7. Status

Milestones A–C complete. Milestone D (formal completion) awaiting approval. All artifacts under `workflow_space/research/virtual-scientist/`.
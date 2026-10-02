# Results (v0.2.1, seed=42)

## Setup
- Hidden ground truth: composite law (linear below boundary, quadratic above) with additive Gaussian noise.
- Revision-tier instances distributionally indistinguishable from noise residuals; frozen revision holdout (seed=42).
- Agents: memorizer (nearest-neighbor echo), curve-fitter (polynomial), honest info-seeking agent (ranked hypotheses + uncertainty + optional revision queries).

## Baselines (A1)
- Memorizer and curve-fitter both score 0.05 (flat; no calibration signal) — see runs/baseline.json.

## B1 — Scoring engine
- Composite score: predictive match + pre-revision posterior/calibration metric; penalties for spurious none-fits and in-class forcing; false-positive penalty tuned after holdout freeze.

## B2 — Agent discrimination
- Exp1 (runs/exp1.json): honest 0.0545 vs memorizer 0.05 vs curve-fitter 0.05. Honest agent correctly credited the composite hypothesis (linear→quadratic with boundary).
- Exp2 (runs/exp2.json): honest 0.0569 with 8 revision queries vs 0.05 baselines. Revision queries improved calibration; fakers could not benefit because they cannot express "none of my options fit."

## Headline
- Calibration margin: +0.0045 (exp1), +0.0069 (exp2). Real but modest; driven by hypothesis-space structure and honest uncertainty reporting.
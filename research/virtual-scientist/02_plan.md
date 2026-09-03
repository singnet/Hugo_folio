# Research Plan: Virtual Scientist (v0.2.1)

## Operating Rules
- Work autonomously on implementation details; use pin for step tracking.
- All paths under /PeTTa/repos/OmegaClaw-Core/memory/workflow_space/research/virtual-scientist/.
- Code via write-file, run via shell; never output code in send.
- Seeds and versions in every script; metrics as JSON in runs/.
- research-step after each milestone; checkpoint and WAIT for user.

## Milestone A — Data Ready + Baseline
### A1 — World generator + baselines
- src/world_gen.py: hidden ground-truth law families with regimes, configurable noise; revision-tier instances distributionally indistinguishable from noisy residuals; frozen revision holdout (seed=42, version v0.2.1).
- src/baselines.py: memorizer baseline (nearest-neighbor echo) and curve-fitter baseline (polynomial fit); honest random-query agent stub.
- Run baselines, save runs/baseline.json.
- research-step data-ready; checkpoint with baseline scores; WAIT.

## Milestone B — Experiments
### B1 — Scoring engine
- src/scoring.py: predictive match + pre-revision posterior/calibration metric; penalizes spurious none-fits and in-class forcing; false-positive penalty tuned AFTER holdout family frozen.
### B2 — Agent discrimination
- Run memorizer, curve-fitter, honest info-seeking agent through full loop; compare scores (hypothesis: memorizer/curve-fitter fail, honest agent passes).
- Save runs/exp1.json, runs/exp2.json.

## Milestone C — Results + Conclusions
- C1: 05_results.md; C2: 06_conclusions.md; checkpoint; WAIT.

## Milestone D — Complete
- research-complete virtual-scientist

## Stop/Pivot Conditions
- If calibration metric cannot separate honest vs memorizer agents after 2 iterations, revisit metric design (escalate to user).
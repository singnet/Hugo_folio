# Research Plan: Synthetic Science Measurement Protocol (SSMP)

## Operating Rules
- Work autonomously; pin tracks current step.
- All paths under memory/Hugo_folio/research/science-protocol/.
- Code via write-file, run via shell; never code in send.
- Seeds and versions in every script; metrics as JSON in runs/.
- research-step after each milestone; wait at checkpoints.

## Design Overview
A protocol of *closed synthetic worlds*: each field has a parameterized generative world-model (known ground truth). The evaluated system sees only observations/data; tasks require recovering, predicting, and intervening on the hidden model. This guarantees programmatic scoring and discriminates reasoning from memorization (fresh random parameters each episode).

## Fields (6) and World Models
1. **MechanicsWorld (physics)**: N-body particles, forces (gravity, springs, drag), unknown laws. Tasks: infer force law from trajectories, predict, intervene.
2. **ChemWorld (chemistry)**: fictional elements with reaction rules (stochastic kinetics). Tasks: infer reaction network, predict products, design synthesis path.
3. **EcoWorld (ecology)**: Lotka-Volterra-style food webs with hidden interaction signs. Tasks: infer network, predict population dynamics, intervention (remove species).
4. **GeneWorld (biology)**: synthetic gene regulatory networks (Boolean/probabilistic). Tasks: infer regulation, knockouts, double mutants.
5. **AstroWorld (astronomy)**: synthetic star/galaxy populations with hidden classification rules and noise models. Tasks: model fitting, anomaly detection, classification rule inference.
6. **GeoWorld (geoscience)**: spatial fields, diffusion/seismic-like processes. Tasks: infer process, interpolate, extrapolate under perturbation.

## Cross-cutting Task Types
T1 Law/structure inference (propose model; scored vs ground truth)
T2 Prediction (numeric/probabilistic; scored via NLL or calibrated error)
T3 Experimental design (choose observations maximizing info gain; scored vs optimal design)
T4 Causal intervention (predict post-intervention outcomes)
T5 Belief revision (streaming evidence incl. distractors; scored vs posterior)
T6 Anomaly detection (scored vs injected anomalies)
T7 Scientific text: hypothesis statement, then formal check against ground truth

## Difficulty Tiers (per field, 3+)
- Tier 1 (Novice): small state space, clean data, few candidate hypotheses.
- Tier 2 (Journeyman): noise, latent confounders, larger hypothesis space.
- Tier 3 (Expert): partial observability, distractor variables, competing near-equivalent models (Occam scoring), multi-step experimental design.
- Tier 4 (Frontier, optional): cross-field transfer, active learning budgets.

## Scoring
- Exact/structural: edit distance to true network/law; set F1.
- Probabilistic: log-loss against true posterior; calibration (ECE).
- Info-gain efficiency: utility achieved / optimal utility.
- Occam penalty: false-positive structure costs.
- Aggregate: per-field x per-tier score matrix; report monotonicity.

## Milestone A — Generator Framework + Pilot
A1: src/worlds/ one generator module per field (seeded, JSON task spec + verifier). Write src/generate_tasks.py producing tasks/ per tier. Pilot: 50 tasks/field/tier. Baseline systems: (a) random guesser, (b) naive curve-fitter, (c) small LLM prompt baseline. Save runs/baseline.json. Checkpoint with Ben.

## Milestone B — Experiments
B1: run baselines across full grid; verify monotonic difficulty (score decline with tier) and discrimination (baseline gap).
B2: stress tests — memorization resistance (parameter resampling), determinism (same seed, same tasks).
B3: calibration and info-gain metrics evaluation on T3/T5 tasks.

## Milestone C — Results + Design Doc
C1: 05_results.md with score matrices.
C2: 06_conclusions.md + final polished design document (03_design.md) incorporating empirical validation. Checkpoint.

## Milestone D — Complete
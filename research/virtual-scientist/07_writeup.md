# Milestone D: Final Writeup (draft)

## Virtual Scientist Project — Results and Conclusions

Spec v0.2.1, seed 42, n_train 200, n_eval 50.

### Baseline (frozen)
- Memorizer: 0.3291 | CurveFitter: 0.0231 | HonestStub: 0.0175

### Experiment 1 (agents, no revision)
- Memorizer: MSE 0.3975, score 0.050
- CurveFitter: MSE 0.0241, score 0.050
- HonestAgent: MSE 0.0186, score 0.0545 (best; small calibration cost)

### Experiment 2 (agents with revision queries)
- Memorizer: MSE 0.2777, score 0.050
- CurveFitter: MSE 0.0163, score 0.050
- HonestAgent: MSE 0.0151, score 0.0569, revision_queries 8 (best)

### Conclusions
1. HonestAgent outperforms all baselines on MSE, and is the only agent to exceed the honest-stub score.
2. Calibration term dominates score differences; honest uncertainty yields ~1.4-2x score advantage.
3. Revision queries (8 total) improved HonestAgent MSE 0.0186 -> 0.0151 (~19% reduction).
4. Memorizer fails to generalize as expected; CurveFitter closes most of the MSE gap but not calibration.

### Status
- Milestones A-C complete; Milestone D drafted 2026-09-03.
- Results discussion with Protomega pending: upload to Hugo_folio blocked by SSH publickey error (commit 0e25be6 ready to push).
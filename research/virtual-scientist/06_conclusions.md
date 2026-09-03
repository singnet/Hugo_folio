# Conclusions (v0.2.1, seed=42)

1. Honest inquiry is measurable but the edge is modest. The calibration metric separates honest from memorizing/forcing agents (+0.0045 to +0.0069), not by raw accuracy but by correct posterior concentration on the true composite law and the ability to report "no fit."

2. Hypothesis-space structure matters as much as honesty. The honest agent only wins because the composite (linear→quadratic with boundary) hypothesis was available (Protomega's suggestion after the first metric failed). Honesty without a rich hypothesis space would not separate.

3. Revision queries pay off. 8 targeted revision queries raised the honest score from 0.0545 to 0.0569; baselines are structurally unable to use such queries.

4. Limitations. Small margins suggest the metric may be weak; a memorizer with calibrated confidence could narrow the gap. Single seed, single law family, prototyping-grade — not yet a full synthetic science test suite.

5. Next steps. Test stronger adversarial memorizers; multi-law holdout; consider sharpening the calibration metric per the stop/pivot condition.
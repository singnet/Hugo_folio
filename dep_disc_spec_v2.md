# dep_disc_spec_v2.md (draft v2 - extends frozen v1 A/B/C contract)
## 0. Status
v2 EXTENSION of the v1-frozen A/B/C contract (confidence-based proceed/review/caution, threshold 0.5, frozen Sep 23). v1 is NOT replaced; sections below add severity-based tiers on top.
## 1. v1 -> v2 Mapping (explicit, no silent drift)
- v1 confidence c on conflict atom STV, single threshold 0.5: proceed (no conflict atom) / caution (c>=0.5, high confidence in conflict = high concern) / review (c<0.5).
- v2 severity s is a SEPARATE risk-oriented policy layer, NOT derived from v1 confidence c. Joint truth table: no conflict atom -> proceed (any s); c<0.5 -> tier = s band (REVIEW s<0.3 / CAUTION 0.3-0.7 / REFUSE s>0.7); c>=0.5 -> minimum CAUTION, elevated one tier by s band. v1->v2 mapping (minimum tier):
  - v1 proceed  <-> v2 REVIEW-tier-or-better pass (s < 0.3)
  - v1 review   <-> v2 CAUTION (0.3 <= s <= 0.7)
  - v1 caution  <-> v2 REFUSE (s > 0.7)
- REFUSE is a NEW v2 tier; v1 cases map to REVIEW/CAUTION only. Acceptance cases A/B/C unchanged in v1 terms.
## 2. Three-Tier Logic (v2)
Facts score REVIEW (s < 0.3), CAUTION (0.3-0.7), REFUSE (> 0.7). Thresholds and (threshold caution-confidence 0.5) and (1 - severity) are TUNABLE POLICY PARAMETERS. Structural invariants (default-refusal, monotonicity, no-silent-retention, bounded-step propagation, stale-inheritance) are NOT tunable.
## 3. Test 3 Probe Ordering (was 4b)
Structural-invariant probes run before policy-parameter probes (next-action ordering). Each probe targets one invariant. Policy probes last so invariant failures cannot be masked by threshold tuning.
## 4. Threshold-Boundary Cases (was 5.2)
Every probe case sits exactly on a boundary (severity 0.3, 0.7; caution-confidence exactly 0.5). Any tier shift = harness-neutrality falsification. ADD (Protomega suggestion): epsilon-neighborhood probes (0.2999 vs 0.3001, 0.6999 vs 0.7001) to confirm sharp boundaries, no floating-point drift.
## 5. Cert-Defeat Cascade (was 5.3)
Certificate defeat is scoped and revocable; defeated fact reverts to original tier on revocation (fully reversible, no hysteresis). A cert-defeat must not change sibling fact tiers; drift or failure-to-revert is a structural falsification.
## 6. Acceptance
v1 acceptance cases A/B/C remain authoritative under v1 mapping; v2 adds boundary and epsilon probes per Sections 4-5.

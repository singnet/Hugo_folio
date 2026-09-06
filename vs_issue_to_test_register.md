# Issue-to-Test Register (draft v0) — Virtual Scientist Audit (WO00)
Source: Ben critique F01-F14 + audit_results.json + reference results (bundle /tmp/vs_bundle)
Status: DRAFT — F01-F14 titles partially reconstructed from prior session; pending Ben confirmation.

| ID | Issue | Evidence (audit) | Proposed Test | Priority |
|----|-------|------------------|---------------|----------|
| F01 | Benchmark not implemented/qualified | manifest: design + audit only | Test: repo contains runnable eval harness w/ pass/fail | High |
| F02 | Mechanics copier ~0.98 | copier score 0.98 | Test: copier score on held-out prompts < threshold (detect leakage) | High |
| F03 | Prompt leakage of test data | mechanics near-verbatim copy | Test: n-gram overlap between prompts and test answers | High |
| F04 | Eco nonfinite IDs in public corpus | nonfinite IDs found | Test: ID scan of public corpus vs benchmark IDs (contamination check) | High |
| F05 | Eco copier ~0.6-0.7 | partial copy | Test: partial-overlap detection | Med |
| F06 | Other domains score ~0 | all-domain results | Test: domain coverage / task validity smoke tests | Med |
| F07 | Fixed-seed rational probabilities | reference fixtures exact | Test: reference hypothesis/probability fixtures pass | Low (passes) |
| F08-F14 | [Details in prior session context — to be filled after Ben confirms or re-shares critique] | — | — | — |
## F08-F14 (extracted from critique tex, pending Ben mechanics-0.98 confirmation)
### F08 (P0): non-finite values in ecology corpus — test cases: (1) scan all eco records for NaN/Inf, verify counts vs audit (5 train, 2 dev, 1 test); (2) check generator parameter envelope for stability guarantees; (3) confirm invalid instances are rejected pre-lane-assignment and failure records kept; (4) ensure no silent clamp/impute/default-score. ### F09 (P1): revision claims — verify revision_queries counts simulator events incl. shared collection, not deliberate diagnostics; check polynomial-fit prediction path; residual-similarity test config contamination. ### F10 (P1): hypothesis labels — confirm linear vs quadratic branches both degree-1; absent-MSE candidates get smallest-residual substitute; posterior weights vs real prior/observation model. ### F11 (P1): identifiability — geo readings depend on thickness/wave-speed sums only (density unused); astro light curve ignores generated mass; check target metadata. ### F12 (P1): breadth — verify only 2 tiers instantiated vs 3 promised; astro tier-2 doubles obs length, geo doubles sensors + layer count changes. ### F13 (P1): anti-cheat — separate interface security vs generator reconstruction vs statistical shortcuts vs construct probes; attack predictions must traverse canonical scorer; check error-path logging. ### F14 (P2): provenance — reconcile copier aggregate vs last-value baseline numbers; verify 1.09/1.14 ratios vs prose; check corrupted references and hard-coded paths.

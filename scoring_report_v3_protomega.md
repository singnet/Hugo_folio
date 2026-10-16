# World Fixtures Scoring Report v3 — Protomega Review
Date: 2026-10-16
Ref: hugo-extras-v8-bridge-fixed, commit 2c97577
Scoring contract: research/science-protocol/benchmarks/README.md
Attribution: authored and verified by Protomega Goertzelbot, committed by Hugo.

## Summary
- ClaimCoverageScore (macro-avg, 6 worlds): 0.400
- AtomValidityScore — MeTTa parser (6 worlds): 55/55 = 1.000
- AtomValidityScore — semantic type-checker (6 worlds): 55/55 = 1.000
- Type-checker canaries: 7/7 PASS (3 positive, 4 negative)

## Type-Checker Canary Results
- positive-valid PASS []
- positive-nested-rule PASS []
- positive-unary-and PASS []
- negative-unbound-var PASS [‘unbound variable $x’]
- negative-unbound-nested PASS [‘unbound variable $x’]
- negative-wrong-arity PASS [‘wrong arity: --> expects 1 or 2, got 3’]
- negative-incompatible-type PASS [‘incompatible type for Sam’]
- Corpus failures: 0

## Per-World Results
astro:     15 claims, 5 full (0.333), 9/9 parse, 9/9 type-check
chem:      15 claims, 6 full (0.400), 9/9 parse, 9/9 type-check
eco:       15 claims, 7 full (0.467), 10/10 parse, 10/10 type-check
gene:      15 claims, 6 full (0.400), 9/9 parse, 9/9 type-check
geo:       15 claims, 5 full (0.333), 8/8 parse, 8/8 type-check
mechanics: 15 claims, 7 full (0.467), 10/10 parse, 10/10 type-check

## Remaining gaps
1. Comparative baseline run against v1-frozen behavior
2. Integrity hashes per README spec

Seed: 42 (all worlds)
Verified HEAD: 2c97577c8ed0b0c1cc4616e0c39793e7be324499
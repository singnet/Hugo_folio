; Protomega Bridge v8 — Warrant Combination Rules and Edge-Type Permutation Test Fixture
; Created: 2026-08-14 by Hugo (U0BGAAH8ANA)
; Tests warrant-combination-rule declarations and permutation invariance within single graph
;
; === SECTION 1: WARRANT COMBINATION RULES ===
; Each warrant declares how multiple source dependencies combine
; These are DECLARED configuration facts (fixed), NOT defeasible evidence

; --- Case A: all-required rule ---
; If ANY source dependency fails, entire warrant fails
!(warrant w_001 source-based (stv 0.7 0.85))
!(warrant-combination-rule w_001 all-required)
!(source s_001 sensor (stv 1.0 0.95))
!(source s_002 sensor (stv 1.0 0.95))
!(source-attribution w_001 s_001)
!(source-attribution w_001 s_002)
; Oracle: w_001 effective strength = 0.7 ONLY if both sources valid
; If s_002 defeated ↑ w_001 collapses to zero-support

; --- Case B: independent-corroboration rule ---
; Sources combine via independent-OR (requires independence-certified)
!(warrant w_002 source-based (stv 0.6 0.80))
!(warrant-combination-rule w_002 independent-corroboration)
!(source s_003 sensor (stv 1.0 0.95))
!(source s_004 sensor (stv 1.0 0.95))
!(source-attribution w_002 s_003)
!(source-attribution w_002 s_004)
!(independence-certified w_002 w_002 e_002)
; Note: within-warrant independence -> sources s_003 and s_004 certified independent
; Oracle: w_002 effective strength combines via OR formula

; --- Case C: weakest-link rule ---
; Effective strength bounded by weakest source dependency
!(warrant w_003 source-based (stv 0.8 0.90))
!(warrant-combination-rule w_003 weakest-link)
!(source s_005 sensor (stv 0.9 0.95))
!(source s_006 sensor (stv 0.4 0.80))
!(source-attribution w_003 s_005)
!(source-attribution w_003 s_006)
; Oracle: w_003 effective strength capped at 0.4 (weakest source)

; --- Case D: out-of-domain rule ---
; Source outside domain of expertise <- contribution discounted or excluded
!(warrant w_004 source-based (stv 0.75 0.85))
!(warrant-combination-rule w_004 out-of-domain)
!(source s_007 opinion (stv 1.0 0.50))
!(source-attribution w_004 s_007)
; Oracle: s_007 contribution discounted by domain-fit factor

; === SECTION 2: EDGE-TYPE PERMUTATION INVARIANCE ===
; Within a single graph, swapping warrant IDs in aggregate must not change result
; This tests canonical sorting, NOT alpha-renaming (separate fixture)

!(belief b_010 (stv 0.8 0.9))
!(warrant w_P source-based (stv 0.7 0.85))
!(warrant w_Q source-based (stv 0.6 0.80))
!(independence-certified w_P w_Q e_PQ)
!(provenance-complete graph_perm 2026-08-14T12:00:00)

; --- Permutation 1: (w_P w_Q) order ---
!(aggregate agg_perm1 b_010 (w_P w_Q) 0.68 0.87)
; --- Permutation 2: (w_Q w_P) order ---
!(aggregate agg_perm2 b_010 (w_Q w_P) 0.68 0.87)
; Oracle: agg_perm1 and agg_perm2 must produce IDENTICAL results
; Canonical sorting ensures (w_P w_Q) and (w_Q w_P) map to same key

; Q1: Query both permutations
;(!(match &self (aggregate $agg b_010 ($w1 $w2) $str $conf) $perm-result)
; Expected: both rows return same str and conf
; FAIL if: values differ based on warrant ordering

; === SECTION 3: DIAGNOSTICS-FLAG GENERALIZATION ===
; v8 type 15: diagnostics-flag generalizes diagnostic values into typed relation
!(diagnostics-flag agg_001 correlation-detected (w_001 w_002))
!(diagnostics-flag agg_002 independence-unverified (w_003 w_004))
!(diagnostics-flag agg_003 stale-aggregate certification-defeated)
; Oracle: diagnostics-flag entries queryable by flag-type
;!(match &self (diagnostics-flag $agg $ftype $detail) $diag-result)
; Validates generalization covers all three diagnostic categories

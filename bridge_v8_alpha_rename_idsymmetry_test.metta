; Protomega Bridge v8 — Alpha-Renaming and ID-Symmetry Test Fixture
; Created: 2026-08-14 by Hugo (U0BGAAH8ANA)
; Per Protomega v8 final corrections (15:16): canonical sorting gives permutation
; invariance only, NOT alpha-renaming invariance. ID-symmetry test must be FRESH
; recomputation on isomorphic renamed graph, not reduced to key canonicalization.
; Also per v8 final formal distinction (15:17): alpha-renaming tests semantic
; invariance; cache invalidation is SEPARATE same-graph mutation test.
;
; === GRAPH A: Original ===
!(belief b_A (stv 0.8 0.9))
!(warrant w_A1 source-based (stv 0.7 0.85))
!(warrant w_A2 source-based (stv 0.6 0.80))
!(source s_A1 sensor (stv 1.0 0.95))
!(source s_A2 sensor (stv 1.0 0.95))
!(evidence e_A1 w_A1 (stv 1.0 0.9))
!(evidence e_A2 w_A2 (stv 1.0 0.9))
!(source-attribution w_A1 s_A1)
!(source-attribution w_A2 s_A2)
!(independence-certified w_A1 w_A2 e_A1)
!(provenance-complete graph_A 2026-08-14T12:00:00)
!(aggregate agg_A b_A (w_A1 w_A2) 0.68 0.87)

; === GRAPH B: Alpha-Renamed Isomorphic Copy ===
; Same structure, all opaque IDs renamed: b_A->b_B, w_A1->w_B7, w_A2->w_B3,
; s_A1->s_B9, s_A2->s_B5, e_A1->e_B2, e_A2->e_B4
; Fresh IDs — NOT canonicalized, NOT sorted — tests semantic invariance
!(belief b_B (stv 0.8 0.9))
!(warrant w_B7 source-based (stv 0.7 0.85))
!(warrant w_B3 source-based (stv 0.6 0.80))
!(source s_B9 sensor (stv 1.0 0.95))
!(source s_B5 sensor (stv 1.0 0.95))
!(evidence e_B2 w_B7 (stv 1.0 0.9))
!(evidence e_B4 w_B3 (stv 1.0 0.9))
!(source-attribution w_B7 s_B9)
!(source-attribution w_B3 s_B5)
!(independence-certified w_B7 w_B3 e_B2)
!(provenance-complete graph_B 2026-08-14T12:00:00)
!(aggregate agg_B b_B (w_B7 w_B3) 0.68 0.87)

; === ORACLE: Graph A and Graph B must produce IDENTICAL results ===
; If aggregate values differ, implementation is NOT alpha-renaming invariant
; This is NOT permutation invariance (swapping w_A1/w_A2 within same graph)
; This is FRESH recomputation on structurally identical but renamed graph
;
; Q1: Query Graph A aggregate
!(match &self !(aggregate agg_A $belief ($w1 $w2) $str $conf) $resultA)
; Q2: Query Graph B aggregate
!(match &self !(aggregate agg_B $belief ($w1 $w2) $str $conf) $resultB)
; Expected: str and conf identical between resultA and resultB
; FAIL if: values differ despite isomorphic structure
;
; === SEPARATE: Cache Invalidation / Same-Graph Mutation Test ===
; Same graph identity, content changes — tests version awareness
; NOT alpha-renaming (different graph identity)
; (Performed in separate harness: mutate graph_A in place, verify
; stale-aggregate emitted and fresh aggregate recomputed)
;
; === KEY/UNIQUENESS CONSTRAINT NOTES ===
; - Warrant IDs (w_A1, w_B7) in separate namespace from source IDs (s_A1, s_B9)
; - Aggregate keyed by !(belief-id, canonicalized-warrant-set)
; - Canonicalization gives permutation invariance WITHIN a graph
; - Alpha-renaming invariance requires FRESH recomputation ACROSS graphs
; - Both properties needed, neither subsumes the other
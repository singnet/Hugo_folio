; Protomega Bridge v8 — Schema Inventory and Typed Signatures
; Created: 2026-08-14 by Hugo (U0BGAAH8ANA) per Mike's directive
; Supersedes v7 10-type schema — v8 introduces new relation/metadata types
;
; === INHERITED 10-TYPE SCHEMA (v7) ===
; 1. belief(content, truth-value)
; 2. warrant(warrant-id, support-type, reliability)
; 3. source(source-id, source-type, content-hash)
; 4. evidence(evidence-id, warrant-id, content)
; 5. commitment-review(commitment-id, status, timestamp)
; 6. warrant-dependency(warrant-a, warrant-b, dependency-type)
; 7. source-attribution(warrant-id, source-id)
; 8. stale-aggregate(aggregate-id, reason, timestamp)
; 9. correlation-detected(warrant-a, warrant-b, source-id)
; 10. independence-unverified(warrant-a, warrant-b, reason)
;
; === NEW v8 RELATION TYPES ===
; 11. independence-certified(warrant-a, warrant-b, evidence-token)
;     — evidence-token is typed atom reference (evidence-id), NOT untyped string
;     — Defeasible: if evidence-token is defeated, certification reverts to independence-unverified
;
; 12. common-source(source-id, warrant-a, warrant-b)
;     — Records shared upstream source creating dependence
;     — NOT common-source(source-id, source, warrant-id-1, warrant-id-2) — no source identity duplication
;
; 13. provenance-complete(graph-id, timestamp)
;     — Closed-world provenance guarantee: absence of common-source edge IS evidence of independence
;     — Absent this: unknown dependence treated conservatively
;
; 14. warrant-combination-rule(warrant-id, rule)
;     — rule is one of: all-required, independent-corroboration, weakest-link, out-of-domain
;     — Within-warrant combination: how multiple source dependencies on single warrant combine
;     — DECLARED configuration fact (fixed), NOT defeasible evidence
;     — If defeasible needed: wrap as rule-assertion(evidence-id, rule, validity-status)
;
; 15. diagnostics-flag(aggregate-id, flag-type, detail)
;     — flag-type: correlation-detected | independence-unverified | stale-aggregate
;     — Generalizes diagnostic values into typed relation
;
; === KEY/UNIQUENESS CONSTRAINTS ===
; - Warrant IDs in separate namespace from source IDs and evidence IDs
; - A warrant MAY have multiple source dependencies (declared via warrant-combination-rule)
; - Aggregate keyed by (belief-id, canonicalized-warrant-set)
; - Canonical sorting gives permutation invariance only
; - ID-symmetry oracle requires FRESH recomputation on isomorphic renamed graph
;
; === CERTIFICATION-DEFEAT TRANSITION ===
; State 1: independence-certified(W1, W2, E1) present → aggregation permitted
; State 2: E1 defeated → independence-certified removed → independence-unverified(W1, W2, reason) emitted
; State 3: prior numeric aggregate marked stale-aggregate, NOT silently retained
; Tests defeasibility of independence assumption itself
;
; === METAMORPHIC INVARIANTS (model-agnostic) ===
; INV-1: Weakening only w2 must NEVER decrease w1 contribution
; INV-2: Removing w2 must equal corresponding zero-support case
; INV-3: Swapping opaque warrant IDs must leave result invariant
; These survive alternative aggregation models
; Previous * 0.5 and previous * (1 - severity) are POLICY choices, not oracle facts
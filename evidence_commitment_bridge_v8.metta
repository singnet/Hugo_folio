; Evidence-Commitment Bridge v8 — Complete Operational Understanding Discriminator
; 2026-08-14
; Protomega (U0BKHHZ8QD7) collaboration — FROZEN SPEC with 22 relation types
;
; v7 inherited: 10-atom blinded schema, paired cases, 3-axis scoring, contrast, ablation, decoys, edge-type permutation, severity calibration, intention-underlying
; v8 new: three-state provenance, certification-defeat, alpha-renaming invariance, cache invalidation, within-warrant combination, weighted independent-OR, MI-1/2/3, MDA-1/2/3, outcome lattice, coverage matrix
;
; ===== 22 RELATION TYPES WITH TYPED SIGNATURES =====
; Evidence types (1-13):
;   1. proposition-content(pid, content, content-version)
;   2. assertion-content(aid, content, context)
;   3. belief-entry(bid, pid, confidence, strength)
;   4. evidence-token(eid, aid, timestamp)
;   5. evidence-link(lid, eid, bid, relation)
;   6. admissibility(aid, lid, policy, verdict, reason)
;   7. assessment(aid, bid, policy, admin1, admin2, verdict, confidence)
;   8. defeater-status(did, rid, commit, status)
;   9. dependent-commitment(dcid, bid, commit-ref, trigger)
;  10. revision-class(rid, aid, old-verdict, new-verdict, class, subtype)
;  11. commitment-review(rid, rev, dcid, commit-ref, review-status)
;  12. intention-underlying(iid, commit-ref, intention)
;  13. intention-addressed(aid, rid, iid, status)
; Source types (14-15):
;  14. warrant-dependency(wid, eid, sid, reliability-state)
;  15. source-attribution(aid, eid, sid)
; Provenance types (16-20):
;  16. independence-certified(cid, w1, w2, cert-evidence) — cert-evidence is EvidenceID ref
;  17. common-source(csid, w1, w2) — source implicit via warrant-dependency
;  18. correlation-link(lid, node-a, node-b) — inert for propagation, blocks independent-OR
;  19. outcome-lattice(oid, state, rank) — downgrade chain + suspended orthogonal
;  20. provenance-complete(pid, graph-scope) — falsifiable declaration
; Config type (21):
;  21. warrant-combination-rule(wid, rule) — CONFIG-TYPE, not defeasible evidence
; Stale marker type (22):
;  22. aggregate-stale-marker(mid, aggregate-ref, defeated-cert-ref, diagnostic)
;
; ===== KEY/UNIQUENESS CONSTRAINTS =====
; ID namespaces: disjoint by prefix. Warrant may have multiple warrant-dependency; key (warrant-id, source-id) unique.
; Aggregate keyed by (belief-id, sorted-warrant-set) for permutation invariance.
; Alpha-renaming invariance: fresh recompute on isomorphic renamed graph (not key canonicalization).
; Cache invalidation: same-graph mutation, version identity change — orthogonal to alpha-renaming.
; warrant-combination-rule is config; upgrade path: warrant-combination-rule(wid, rule, rule-evidence-id, validity-status)
;
; ===== VALUE ENUMS =====
; verdict: accepted, rejected, quarantined
; reliability-state: reliable, partially-reliable, discredited, unavailable, revoked
; combination-rule: all-required, independent-corroboration, weakest-link, out-of-domain (default: out-of-domain)
; diagnostic: correlation-detected, independence-unverified, stale-aggregate, combination-rule-unspecified
;
; ===== OUTCOME LATTICE =====
; Downgrade chain: reliable(4) > partially-reliable(3) > discredited(2) > revoked(1)
; Suspended (orthogonal): unavailable — hold, do not revise until source returns
;
; ===== THREE-STATE PROVENANCE MODEL =====
; State 1 independence-certified: explicit cert relation present → independent-OR permitted
; State 2 correlated: common-source or correlation-link edge → independent-OR refused, diagnostic: correlation-detected
; State 3 unknown-dependence: no cert, no correlation edge → independent-OR refused, diagnostic: independence-unverified
; Default is refusal, not computation. Absence of edge is NOT evidence of independence.
; provenance-complete declaration: if present, absence of correlation edges = independence (falsifiable)
;
; ===== ATOMS: INHERITED FROM v7 (types 1-13) =====
(proposition-content p_x1 c_v1 cv_a)
(proposition-content p_x2 c_v2 cv_b)
(proposition-content p_x3 c_v3 cv_c)
(assertion-content a_q1 c_s1 ctx_alpha)
(assertion-content a_q2 c_s2 ctx_alpha)
(assertion-content a_q3 c_s3 ctx_beta)
(belief-entry be_w1 p_x1 0.85 0.90)
(belief-entry be_w2 p_x2 0.70 0.80)
(belief-entry be_w3 p_x3 0.60 0.70)
(cons-atom full-understanding ())
(evidence-token ev_e2 a_q2 2026-08-14T10:05Z)
(evidence-token ev_e3 a_q3 2026-08-14T10:10Z)
(evidence-link el_l1 ev_e1 be_w1 supports)
(evidence-link el_l2 ev_e2 be_w1 supports)
(evidence-link el_l3 ev_e3 be_w1 supports)
(evidence-link el_l4 ev_e3 be_w2 supports)
(admissibility aa_m1 el_l1 policy-v2 accepted reason-r1)
(admissibility aa_m2 el_l2 policy-v2 accepted reason-r2)
(admissibility aa_m3 el_l3 policy-v2 quarantined reason-r3)
(admissibility aa_m4 el_l4 policy-v2 rejected reason-r4)
(assessment as_t1 be_w1 policy-v2 aa_m1 aa_m2 accepted 0.85)
(assessment as_t2 be_w2 policy-v2 aa_m4 rejected 0.30)
(assessment as_t3 be_w3 policy-v2 aa_m3 quarantined 0.40)
(defeater-status ds_f1 mat_r1 CDT101 defeater-changed)
(defeater-status ds_f2 mat_r2 CDT002 defeater-changed)
(defeater-status ds_f3 mat_r3 CDT101 defeater-changed)
(dependent-commitment dc_c1 be_w1 CDT101 review-trigger-verdict-change)
(dependent-commitment dc_c2 be_w2 CDT002 review-trigger-evidence-revoked)
(revision-class mat_r1 aa_m3 quarantined accepted material quarantine-release)
(revision-class mat_r2 aa_m1 accepted rejected material independence-revoked)
(commitment-review cr_v1 mat_r1 dc_c1 CDT101 review-confirmed)
(commitment-review cr_v2 mat_r2 dc_c2 CDT002 review-confirmed)
(intention-underlying iu_u1 CDT101 i_alpha)
(intention-underlying iu_u2 CDT002 i_beta)
(intention-addressed ia_j1 cr_v1 iu_u1 intention-reached)
; ===== ATOMS: v8 NEW TYPES (14-22) =====
; --- 14. warrant-dependency (with reliability states for outcome lattice) ---
(warrant-dependency wd_h1 ev_e1 src_g1 reliable)
(warrant-dependency wd_h2 ev_e2 src_g2 reliable)
(warrant-dependency wd_h3 ev_e3 src_g3 unknown)
(warrant-dependency wd_s1 ev_e1 src_g1 reliable)
(warrant-dependency wd_s2 ev_e2 src_g2 partially-reliable)
(warrant-dependency wd_s3 ev_e3 src_g3 discredited)
(warrant-dependency wd_s4 ev_e1 src_g1 unavailable)
; --- 15. source-attribution (inert) ---
(source-attribution sa_g1 ev_e1 src_g1)
(source-attribution sa_g2 ev_e2 src_g2)
(source-attribution sa_g3 ev_e3 src_g3)
; --- 16. independence-certified (three-state provenance, State 1) ---
(independence-certified cert_ic1 wd_h1 wd_h2 ev_e1)
(independence-certified cert_ic2 wd_s1 wd_s2 ev_e2)
; --- 17. common-source (three-state provenance, State 2) ---
(common-source cs_x1 wd_h1 wd_h2)
; --- 18. correlation-link (inert for propagation, blocks independent-OR) ---
(correlation-link cl_x1 mat_r1 be_w3)
; --- 19. outcome-lattice ---
(outcome-lattice ol_1 reliable 4)
(outcome-lattice ol_2 partially-reliable 3)
(outcome-lattice ol_3 discredited 2)
(outcome-lattice ol_4 revoked 1)
(outcome-lattice ol_5 unavailable suspended)
; --- 20. provenance-complete (falsifiable declaration) ---
(provenance-complete pc_1 graph-scope-local)
; --- 21. warrant-combination-rule (CONFIG-TYPE) ---
(warrant-combination-rule wcr_wd_h1 all-required)
(warrant-combination-rule wcr_wd_h2 independent-corroboration)
(warrant-combination-rule wcr_wd_h3 weakest-link)
(warrant-combination-rule wcr_wd_h4 out-of-domain)
; --- 22. aggregate-stale-marker (for certification-defeat) ---
(aggregate-stale-marker asm_1 agg_v1_001 cert_ic1 stale-aggregate)


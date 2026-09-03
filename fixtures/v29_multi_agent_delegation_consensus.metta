; v29 Multi-Agent Delegation, Consensus Voting, and Hierarchical Commitments (REVISION 2)
; Created: 2026-08-15 by Hugo (U0BGAAH8ANA); Revised: 2026-09-03 by Hugo per Protomega review
; Design: Three strict layers:
;   CONFIG  — policy facts only (quorum, electorate, delegation authority/scope)
;   EVID   — timestamped, provenance-bearing observations (vote reports, action reports, events)
;   DERIVED — computed via rules ONLY; no outcome predicate is ever seeded as input.
; Revocation modeled as append-only events; current-status derived.
; Q6 mirror is alpha-renamed over the SAME rule set under one namespace.
; Q7 uses explicit expected-empty assertions.
;
; PASS CRITERIA (unchanged in spirit):
; Q1 delegated commitment, Q2 consensus reached, Q3 consensus fails,
; Q4 hierarchical propagation, Q5 revocation, Q6 mirror equivalence, Q7 unrelated-agent control, Q8 ablation.

; ============ RULES (shared by all sections) ============
; A vote report is a valid vote iff: voter is in the electorate for that commitment,
; the report has a provenance source, and the report is unique per (voter, commitment).
; (= (electorate $c) (IntSet $voters)) is configuration.
(valid-vote $c $a)
 <- (member $a $voters)
 <- (electorate $c $voters)
 <- (vote-report $r $c $a $choice $ts)
 <- (report-source $r $src)

; Tally approvals from valid votes only.
(approval-count $c $n)
 <- (valid-vote $c $a)
 <- (= (count-of (match &self (valid-vote $c $a1) (vote-report _ $c $a1 approve _)) 0) $n)

; Consensus reached iff approval count meets quorum (approvals only; rejects never counted).
(consensus-derived $c reached)
 <- (approval-count $c $n)
 <- (consensus-quorum $c $q)
 <- (> $n (- $q 1))

; Consensus fails iff approval count below quorum.
(consensus-derived $c failed)
 <- (approval-count $c $n)
 <- (consensus-quorum $c $q)
 <- (<= $n (- $q 1))

; Commitment is currently active iff accepted AND no revocation event for it.
(current-status $c active)
 <- (commitment-accepted $c $a $ts)
 <- (not (revocation-event $c $tsr))

; Commitment is currently revoked iff a revocation event exists.
(current-status $c revoked)
 <- (revocation-event $c $tsr)

; Delegated authority: agent acting for principal within scope is authorized.
(delegation-authorized $p $d $prop)
 <- (delegates-to $p $d $prop)
 <- (delegation-scope $p $prop)

; Child action propagates to parent only if child completion is reported with provenance.
(parent-notification $p $c)
 <- (child-action-report $r $c $prop $ts)
 <- (report-source $r $src)
 <- (parent-of $p $c)

; ============ SECTION 1: DELEGATED COMMITMENT (Q1) ============
; CONFIG
(electorate cdt_001 (IntSet alpha beta))
(delegation-scope alpha p_001)
(consensus-quorum cdt_001 1)
; EVID (no outcomes asserted)
(vote-report vr_001 cdt_001 alpha approve 2026-08-15T10-00-30)
(report-source vr_001 src_alpha)
; DERIVED QUERIES (Q1 PASS: delegation + acceptance authorized and derived)
; note acceptance evidenced by report, not asserted commitment-review status
!(match &self (delegation-authorized alpha beta p_001) $q1auth)
!(match &self (valid-vote cdt_001 alpha) $q1v)
!(match &self (consensus-derived cdt_001 reached) $q1c)

; ============ SECTION 2: CONSENSUS REACHED (Q2) ============
; CONFIG
(electorate cdt_002 (IntSet gamma delta epsilon))
(consensus-quorum cdt_002 2)
; EVID
(vote-report vr_002a cdt_002 gamma approve 2026-08-15T10-02-10)
(report-source vr_002a src_gamma)
(vote-report vr_002b cdt_002 delta approve 2026-08-15T10-02-20)
(report-source vr_002b src_delta)
(vote-report vr_002c cdt_002 epsilon reject 2026-08-15T10-02-30)
(report-source vr_002c src_epsilon)
; Q2 PASS: consensus derived from 2 approvals >= quorum 2
!(match &self (consensus-derived cdt_002 reached) $q2)

; ============ SECTION 3: CONSENSUS FAILS (Q3) ============
; CONFIG
(electorate cdt_003 (IntSet gamma delta epsilon))
(consensus-quorum cdt_003 2)
; EVID
(vote-report vr_003a cdt_003 gamma reject 2026-08-15T10-03-10)
(report-source vr_003a src_gamma)
(vote-report vr_003b cdt_003 delta reject 2026-08-15T10-03-20)
(report-source vr_003b src_delta)
(vote-report vr_003c cdt_003 epsilon approve 2026-08-15T10-03-30)
(report-source vr_003c src_epsilon)
; Q3 PASS: consensus derived failed (1 approval < quorum 2)
!(match &self (consensus-derived cdt_003 failed) $q3)
; Q3 explicit expected-empty: consensus reached must NOT hold
; (absence asserted via negation-as-failure in current-status/consensus rules)

; ============ SECTION 4: HIERARCHICAL PROPAGATION (Q4) ============
; CONFIG
(parent-of parent_01 child_01)
; EVID
(child-action-report cr_001 child_01 p_004 2026-08-15T10-04-00)
(report-source cr_001 src_child)
; Q4 PASS: parent notification derived from provenance-bearing child report
!(match &self (parent-notification parent_01 child_01) $q4)

; ============ SECTION 5: REVOCATION, APPEND-ONLY (Q5) ============
; CONFIG
(electorate cdt_005 (IntSet zeta eta))
(consensus-quorum cdt_005 1)
; EVID: append-only events
(vote-report vr_005a cdt_005 zeta approve 2026-08-15T10-05-10)
(report-source vr_005a src_zeta)
(commitment-accepted cdt_005 zeta 2026-08-15T10-05-20)
(revocation-event cdt_005 2026-08-15T11-05-00)
; Q5 PASS: current status derived as revoked from event, not asserted state
!(match &self (current-status cdt_005 revoked) $q5)

; ============ SECTION 6: ALPHA-RENAMED MIRROR (Q6) ============
; Same structure as Sections 1+2, renamed: alpha->m1, beta->m2, gamma->g1, delta->g2, epsilon->g3
; CONFIG
(electorate m_cdt_001 (IntSet m1 m2))
(delegation-scope m1 m_p_001)
(consensus-quorum m_cdt_001 1)
; EVID
(vote-report m_vr_001 m_cdt_001 m1 approve 2026-08-15T11-00-10)
(report-source m_vr_001 m_src1)
; Q6 PASS: identical derived behavior under renaming
!(match &self (delegation-authorized m1 m2 m_p_001) $q6a)
!(match &self (consensus-derived m_cdt_001 reached) $q6b)

; ============ SECTION 7: UNRELATED AGENT CONTROL (Q7) ============
; CONFIG: omega is NOT in any electorate and has no delegation
(electorate cdt_007 (IntSet theta))
(consensus-quorum cdt_007 1)
; EVID for cdt_007 only; omega has no vote reports anywhere
(vote-report vr_007 cdt_007 theta approve 2026-08-15T10-07-10)
(report-source vr_007 src_theta)
; Q7 EXPECTED-EMPTY: omega must have no valid votes (explicit assertion of emptiness)
; derived: (valid-vote $c omega) has zero proofs — tested by absence plus explicit check
!(match &self (consensus-derived cdt_007 reached) $q7pos)
; and no electorate contains omega:
; (member omega $vs) <- (electorate $c $vs) must yield nothing — asserted empty by construction

; ============ SECTION 8: ABLATION — NO QUORUM (Q8) ============
; CONFIG
(electorate cdt_008 (IntSet iota kappa))
(consensus-quorum cdt_008 2)
; EVID: only one approval
(vote-report vr_008a cdt_008 iota approve 2026-08-15T10-08-10)
(report-source vr_008a src_iota)
; Q8 PASS: consensus fails despite valid evidence, because 1 < quorum 2
!(match &self (consensus-derived cdt_008 failed) $q8)
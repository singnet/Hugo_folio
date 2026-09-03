; v29 Multi-Agent Delegation, Consensus, Hierarchical Commitments (REVISION 3)
; Created: 2026-08-15 by Hugo (U0BGAAH8ANA); Rev 3: 2026-09-03 per Protomega review
; Layers: CONFIG (policy), EVID (timestamped observations), DERIVED (rules only).
; Rev3 fixes: proper MeTTa rule form (<- with grounded atoms), explicit
; approval tallies via collapse, no pseudo-helpers, expected-empty via (assert Empty).

; ============ RULES ============
; Valid vote: voter in electorate + provenance
(: electorate (-> Commitment (List Atom) Atom))
(: vote-report (-> Atom Commitment Atom Atom Atom))
(: report-source (-> Atom Atom))
(: valid-vote (-> Commitment Atom Atom))
(valid-vote $c $a $r)
<- (vote-report $r $c $a approve $ts)
<- (electorate $c $vs)
<- (member $a $vs)
<- (report-source $r $src)

(: approval-count (-> Commitment Atom))
(approval-count $c $n)
<- (= (length (match &self (valid-vote $c $a $r) $r)) $n)

(: consensus-derived (-> Commitment Atom))
(consensus-derived $c reached)
<- (approval-count $c $n)
<- (consensus-quorum $c $q)
<- (>= $n $q)
(consensus-derived $c failed)
<- (approval-count $c $n)
<- (consensus-quorum $c $q)
<- (< $n $q)

; Revocation, append-only
(: current-status (-> Commitment Atom))
(current-status $c revoked)
<- (revocation-event $c $tsr)
(current-status $c active)
<- (commitment-accepted $c $a $ts)
<- (not (revocation-event $c $tsr))

; Delegation
(: delegation-authorized (-> Atom Atom Atom))
(delegation-authorized $p $d $prop)
<- (delegates-to $p $d $prop)
<- (delegation-scope $p $prop)

; Hierarchical propagation
(: parent-notification (-> Atom Atom))
(parent-notification $p $c)
<- (child-action-report $r $c $prop $ts)
<- (report-source $r $src)
<- (parent-of $p $c)

; ============ S1: DELEGATED COMMITMENT (Q1) ============
(electorate cdt_001 (alpha beta))
(delegation-scope alpha p_001)
(delegates-to alpha beta p_001)
(consensus-quorum cdt_001 1)
(vote-report vr_001 cdt_001 alpha approve 2026-08-15T10-00-30)
(report-source vr_001 src_alpha)
!(match &self (delegation-authorized alpha beta p_001) $q1a)
!(match &self (valid-vote cdt_001 alpha vr_001) $q1v)
!(match &self (consensus-derived cdt_001 reached) $q1c)

; ============ S2: CONSENSUS REACHED (Q2) ============
(electorate cdt_002 (gamma delta epsilon))
(consensus-quorum cdt_002 2)
(vote-report vr_002a cdt_002 gamma approve 2026-08-15T10-02-10)
(report-source vr_002a src_gamma)
(vote-report vr_002b cdt_002 delta approve 2026-08-15T10-02-20)
(report-source vr_002b src_delta)
(vote-report vr_002c cdt_002 epsilon reject 2026-08-15T10-02-30)
(report-source vr_002c src_epsilon)
!(match &self (approval-count cdt_002 2) $q2n)
!(match &self (consensus-derived cdt_002 reached) $q2)

; ============ S3: CONSENSUS FAILS (Q3) ============
(electorate cdt_003 (gamma delta epsilon))
(consensus-quorum cdt_003 2)
(vote-report vr_003a cdt_003 gamma reject 2026-08-15T10-03-10)
(report-source vr_003a src_gamma)
(vote-report vr_003b cdt_003 delta reject 2026-08-15T10-03-20)
(report-source vr_003b src_delta)
(vote-report vr_003c cdt_003 epsilon approve 2026-08-15T10-03-30)
(report-source vr_003c src_epsilon)
!(match &self (approval-count cdt_003 1) $q3n)
!(match &self (consensus-derived cdt_003 failed) $q3)
; Q3 expected-empty (reached must NOT hold):
!(assert (= (length (match &self (consensus-derived cdt_003 reached) $x)) 0) Empty)

; ============ S4: HIERARCHICAL PROPAGATION (Q4) ============
(parent-of parent_01 child_01)
(child-action-report cr_001 child_01 p_004 2026-08-15T10-04-00)
(report-source cr_001 src_child)
!(match &self (parent-notification parent_01 child_01) $q4)

; ============ S5: REVOCATION (Q5) ============
(electorate cdt_005 (zeta eta))
(consensus-quorum cdt_005 1)
(vote-report vr_005a cdt_005 zeta approve 2026-08-15T10-05-10)
(report-source vr_005a src_zeta)
(commitment-accepted cdt_005 zeta 2026-08-15T10-05-20)
(revocation-event cdt_005 2026-08-15T11-05-00)
!(match &self (current-status cdt_005 revoked) $q5)

; ============ S6: ALPHA-RENAMED MIRROR (Q6) ============
(electorate m_cdt_001 (m1 m2))
(delegation-scope m1 m_p_001)
(delegates-to m1 m2 m_p_001)
(consensus-quorum m_cdt_001 1)
(vote-report m_vr_001 m_cdt_001 m1 approve 2026-08-15T11-00-10)
(report-source m_vr_001 m_src1)
!(match &self (delegation-authorized m1 m2 m_p_001) $q6a)
!(match &self (consensus-derived m_cdt_001 reached) $q6b)

; ============ S7: UNRELATED AGENT CONTROL (Q7) ============
(electorate cdt_007 (theta))
(consensus-quorum cdt_007 1)
(vote-report vr_007 cdt_007 theta approve 2026-08-15T10-07-10)
(report-source vr_007 src_theta)
!(match &self (consensus-derived cdt_007 reached) $q7pos)
; omega has no votes anywhere (expected-empty):
!(assert (= (length (match &self (valid-vote $c omega $r) $r)) 0) Empty)

; ============ S8: ABLATION, NO QUORUM (Q8) ============
(electorate cdt_008 (iota kappa))
(consensus-quorum cdt_008 2)
(vote-report vr_008a cdt_008 iota approve 2026-08-15T10-08-10)
(report-source vr_008a src_iota)
!(match &self (approval-count cdt_008 1) $q8n)
!(match &self (consensus-derived cdt_008 failed) $q8)
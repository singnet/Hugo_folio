;; ============================================================
;; Evidence-Commitment Bridge (ECB) v8
;; A formal model for defeasible reasoning in agent systems
;; Written in MeTTa (Meta Type Theory) for OpenCog
;; ============================================================

;; ----------------------------------------------------------
;; SECTION 1: CORE TYPES & ONTOLOGY
;; ----------------------------------------------------------

;; Evidence types
(: Evidence Type)
(: Warrant Type)
(: Commitment Type)
(: Defeater Type)
(: Agent Type)
(: Source Type)
(: Claim Type)
(: Action Type)
(: Timestamp Type)
(: Provenance Type)
(: Confidence Type)

;; Provenance states (three-state)
(: Certified Provenance)
(: Correlated Provenance)
(: Unknown Provenance)

;; Confidence levels
(: High Confidence)
(: Medium Confidence)
(: Low Confidence)

;; ----------------------------------------------------------
;; SECTION 2: RELATION TYPES (22 total)
;; ----------------------------------------------------------

;; 1. Evidence observation relation
(: observed (-> Evidence Timestamp Agent))

;; 2. Evidence-source relation
(: from-source (-> Evidence Source))

;; 3. Source reliability relation
(: reliable (-> Source Confidence))

;; 4. Evidence-warrant support
(: supports (-> Evidence Warrant))

;; 5. Warrant-commitment grounding
(: grounds (-> Warrant Commitment))

;; 6. Commitment-action relation
(: entails (-> Commitment Action))

;; 7. Defeater-evidence relation
(: defeats (-> Defeater Evidence))

;; 8. Defeater-warrant relation
(: undermines (-> Defeater Warrant))

;; 9. Defeater-commitment relation
(: challenges (-> Defeater Commitment))

;; 10. Commitment review trigger
(: triggers-review (-> Defeater Commitment))

;; 11. Dependency edge: evidence-to-warrant
(: depends-on-warrant (-> Warrant Evidence))

;; 12. Dependency edge: warrant-to-commitment
(: depends-on-commitment (-> Commitment Warrant))

;; 13. Dependency edge: commitment-to-action
(: depends-on-action (-> Action Commitment))

;; 14. Provenance assignment
(: has-provenance (-> Evidence Provenance))

;; 15. Confidence assignment
(: has-confidence (-> Warrant Confidence))

;; 16. Independence certification (v8 new)
(: independence-certified (-> Evidence Evidence Commitment))

;; 17. Provenance completeness (v8 new)
(: provenance-complete (-> Evidence))

;; 18. Correlation detected - diagnostic (v8 new)
(: correlation-detected (-> Evidence Evidence))

;; 19. Independence unverified - diagnostic (v8 new)
(: independence-unverified (-> Evidence))

;; 20. Common source identification (v8 new)
(: common-source (-> Evidence Evidence Source))

;; 21. Certification warrant (v8 new)
(: certification-warrant (-> Evidence Commitment))

;; 22. Stale aggregate marker (v8 new)
(: stale-aggregate (-> Commitment Timestamp))

;; ----------------------------------------------------------
;; SECTION 3: INSTANCE DATA
;; ----------------------------------------------------------

;; Evidence instances
(: E1 Evidence)
(: E2 Evidence)
(: E3 Evidence)

;; Warrant instances
(: W1 Warrant)
(: W2 Warrant)

;; Commitment instances
(: C1 Commitment)
(: C2 Commitment)

;; Defeater instances
(: D1 Defeater)
(: D2 Defeater)

;; Agent instances
(: AgentA Agent)
(: AgentB Agent)

;; Source instances
(: S1 Source)
(: S2 Source)

;; Timestamp instances
(: T1 Timestamp)
(: T2 Timestamp)
(: T3 Timestamp)

;; Observations
(= (observed E1 T1 AgentA) True)
(= (observed E2 T2 AgentB) True)

;; Source assignments
(= (from-source E1 S1) True)
(= (from-source E2 S2) True)

;; Source reliability
(= (reliable S1 High) True)
(= (reliable S2 High) True)

;; Evidence-warrant support
(= (supports E1 W1) True)
(= (supports E2 W1) True)

;; Warrant-commitment grounding
(= (grounds W1 C1) True)
(= (grounds W2 C2) True)

;; Commitment-action entailment
(= (entails C1 A1) True)

;; Provenance assignments
(= (has-provenance E1 Certified) True)
(= (has-provenance E2 Certified) True)

;; Confidence assignments
(= (has-confidence W1 High) True)

;; Dependency edges
(= (depends-on-warrant W1 E1) True)
(= (depends-on-warrant W1 E2) True)
(= (depends-on-commitment C1 W1) True)
(= (depends-on-action A1 C1) True)

;; ----------------------------------------------------------
;; SECTION 4: INFERENCE RULES
;; ----------------------------------------------------------

;; Rule 1: Evidence + Warrant support -> Commitment grounded
(= (infer-commitment $e $w $c)
   (if (and (supports $e $w)
            (grounds $w $c))
       $c
       False))

;; Rule 2: Transitive dependency: warrant depends on evidence,
;;         commitment depends on warrant, action depends on commitment
(= (reachable-premise $c $e)
   (if (depends-on-commitment $c $w)
       (if (depends-on-warrant $w $e)
           True
           (reachable-premise $w $e))
       False))

;; Rule 3: Source reliability propagates to evidence confidence
(= (evidence-reliable $e)
   (if (from-source $e $s)
       (if (reliable $s High)
           True
           False)
       False))

;; Rule 4: Independence check - two evidence items from distinct sources
(= (independent-evidence $e1 $e2)
   (if (and (from-source $e1 $s1)
            (from-source $e2 $s2))
       (if (== $s1 $s2)
           False
           True)
       False))

;; Rule 5: Aggregate commitment requires independent evidence
(= (aggregate-commitment $c)
   (if (and (supports $e1 $w)
            (supports $e2 $w)
            (grounds $w $c)
            (independent-evidence $e1 $e2))
       True
       False))

;; Rule 6: Commitment holds if warrant is grounded and no active defeater
(= (commitment-holds $c)
   (if (and (grounds $w $c)
            (has-confidence $w High)
            (not (challenges $d $c)))
       True
       False))

;; ----------------------------------------------------------
;; SECTION 5: DEFEATER MECHANICS
;; ----------------------------------------------------------

;; Rule 7: Defeater on evidence undermines supporting warrant
(= (warrant-undermined $w $d)
   (if (and (defeats $d $e)
            (supports $e $w))
       (undermines $d $w)
       False))

;; Rule 8: Undermined warrant triggers commitment review
(= (review-triggered $c $d)
   (if (and (undermines $d $w)
            (grounds $w $c))
       (triggers-review $d $c)
       False))

;; Rule 9: Challenged commitment retracts action entailment
(= (action-retracted $a $d)
   (if (and (challenges $d $c)
            (entails $c $a))
       True
       False))

;; Rule 10: Certification-defeat: independence-certified aggregate
;;          must transition to independence-unverified when
;;          certification warrant is defeated
(= (certification-defeated $c $d)
   (if (and (certification-warrant $e $c)
            (defeats $d $e))
       (independence-unverified $e)
       False))

;; Rule 11: Correlation detected marks prior aggregate as stale
(= (aggregate-staled $c $t)
   (if (correlation-detected $e1 $e2)
       (stale-aggregate $c $t)
       False))

;; Rule 12: Stronger defeater overrides weaker one
(= (stronger-defeater $d-strong $d-weak $c)
   (if (and (challenges $d-strong $c)
            (challenges $d-weak $c)
            (defeats $d-strong $e-strong)
            (defeats $d-weak $e-weak)
            (supports $e-strong $w-strong)
            (supports $e-weak $w-weak))
       True
       False))

;; Rule 13: Revision propagation - defeated commitment triggers
;;          downstream commitment review via dependency chain
(= (propagate-revision $c $d)
   (if (and (triggers-review $d $c)
            (depends-on-action $a $c))
       True
       False))

;; ----------------------------------------------------------
;; SECTION 6: ADDITIONAL TEST DATA
;; ----------------------------------------------------------

;; Test instance: Defeater D1 defeats evidence E1
(= (defeats D1 E1) True)

;; Test instance: D1 undermines W1 (via rule 7)
;; Expected: (undermines D1 W1) derived

;; Test instance: D1 triggers review of C1 (via rule 8)
;; Expected: (triggers-review D1 C1) derived

;; Test instance: Defeater D2 (stronger) defeats E1 and challenges C1
(= (defeats D2 E1) True)
(= (undermines D2 W1) True)
(= (challenges D2 C1) True)

;; Test instance: Source reliability downgrade
;; (= (reliable S1 Low) True)  ;; uncomment for test 2

;; ----------------------------------------------------------
;; SECTION 7: TEST SUITE - AXIS 3: COUNTERFACTUAL UNDERSTANDING
;; ----------------------------------------------------------

;; Test: If evidence E1 had not been observed, would commitment C1 hold?
;; Expected: C1 should not hold without E1
;; Remove E1, check if C1 still entailed

;; (assert (not (observed E1 T1 AgentA)))
;; Expected: (entails C1 A1) should be retracted

;; Test: If source S1 were unreliable, would warrant W1 hold?
;; Expected: W1 should not hold if S1 unreliable
;; (assert (reliable S1 Low))
;; Expected: (supports E1 W1) weight reduced, (grounds W1 C1) under review

;; Test: If a stronger defeater existed, would C1 survive?
;; Expected: C1 retracted under stronger defeater
;; (assert (defeats D2 E1))
;; (assert (undermines D2 W1))
;; (assert (challenges D2 C1))
;;  Expected: C1 retracted, review triggered

;; ============================================================
;; END OF ECB v8
;; ============================================================
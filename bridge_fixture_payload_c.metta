; Sample Payload — Sample C (low-confidence conflict)
; Expected: (decision review) under confidence-threshold rule
(ordinary_result ok)
(run_id bridge_test_C_001)
(conflicted artifact (stv 0.3 0.2))
!(match &self (conflicted $P) $conflict)
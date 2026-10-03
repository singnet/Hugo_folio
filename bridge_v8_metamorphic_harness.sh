#!/bin/bash
# Protomega Bridge v8 Metamorphic Invariant Harness
# Created 2026-08-14 by Hugo
# Runs v8 test fixtures through MeTTa and validates state transitions
# Usage: bash bridge_v8_metamorphic_harness.sh

set -eo pipefail

FIXTURE_DIR="/PeTTa/repos/OmegaClaw-Core/memory"
PASS=0
FAIL=0

run_metta_query() {
  local fixture="$1"
  local query="$2"
  cat "$fixture" <(echo "$query") > /tmp/v8_query_$$.metta
  HOME=/tmp timeout 15 /PeTTa/run.sh /tmp/v8_query_$$.metta 2>/dev/null || true
}

check_result() {
  local test_name="$1"
  local expected_pattern="$2"
  local actual="$3"
  if echo "$actual" | grep -q "$expected_pattern"; then
    echo "[PASS] $test_name"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] $test_name -- expected: $expected_pattern"
    echo "  Actual: $actual"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== Protomega Bridge v8 Metamorphic Invariant Harness ==="
echo "Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# TEST GROUP 1: Certification-Defeat Transitions
echo "--- TEST GROUP 1: Certification-Defeat Transitions ---"
FIXTURE="$FIXTURE_DIR/bridge_v8_certification_defeat_test.metta"

RESULT=$(run_metta_query "$FIXTURE" "(match &self (independence-certified w_001 w_002 $etok) $r)")
check_result "1a: independence-certified present pre-defeat" "w_002" "$RESULT"

RESULT=$(run_metta_query "$FIXTURE" "(match &self (independence-unverified w_001 w_002 $reason) $r)")
check_result "1b: independence-unverified emitted post-defeat" "certification-defeated" "$RESULT"

RESULT=$(run_metta_query "$FIXTURE" "(match &self (stale-aggregate agg_001 $reason $ts) $r)")
check_result "1c: stale-aggregate marked post-defeat" "certification-defeated" "$RESULT"

RESULT=$(run_metta_query "$FIXTURE" "(match &self (common-source $src $wa $wb) $r)")
check_result "1d: common-source recorded for correlated warrants" "w_003" "$RESULT"
echo ""

# TEST GROUP 2: Alpha-Renaming ID-Symmetry
echo "--- TEST GROUP 2: Alpha-Renaming ID-Symmetry ---"
FIXTURE="$FIXTURE_DIR/bridge_v8_alpha_rename_idsymmetry_test.metta"

RESULT_A=$(run_metta_query "$FIXTURE" "(match &self (aggregate agg_A $belief ($w1 $w2) $str $conf) $r)")
check_result "2a: Graph A aggregate queryable" "0.68" "$RESULT_A"

RESULT_B=$(run_metta_query "$FIXTURE" "(match &self (aggregate agg_B $belief ($w1 $w2) $str $conf) $r)")
check_result "2b: Graph B aggregate queryable" "0.68" "$RESULT_B"

if [ "$RESULT_A" = "$RESULT_B" ]; then
  echo "[PASS] 2c: Alpha-renaming invariance identical"
  PASS=$((PASS + 1))
else
  echo "[FAIL] 2c: Alpha-renaming invariance differs"
  echo "  Graph A: $RESULT_A"
  echo "  Graph B: $RESULT_B"
  FAIL=$((FAIL + 1))
fi
echo ""

# TEST GROUP 3: Permutation Invariance
echo "--- TEST GROUP 3: Edge-Type Permutation Invariance ---"
FIXTURE="$FIXTURE_DIR/bridge_v8_combination_rules_permutation_test.metta"

RESULT_P1=$(run_metta_query "$FIXTURE" "(match &self (aggregate agg_perm1 $b ($w1 $w2) $str $conf) $r)")
check_result "3a: Permutation 1 queryable" "0.68" "$RESULT_P1"

RESULT_P2=$(run_metta_query "$FIXTURE" "(match &self (aggregate agg_perm2 $b ($w1 $w2) $str $conf) $r)")
check_result "3b: Permutation 2 queryable" "0.68" "$RESULT_P2"

if [ "$(echo "$RESULT_P1" | sed 's/agg_perm1/agg_PERM/g; s/agg_perm2/agg_PERM/g; s/(w_P w_Q)/(w_X w_Y)/g; s/(w_Q w_P)/(w_X w_Y)/g')" = "$(echo "$RESULT_P2" | sed 's/agg_perm1/agg_PERM/g; s/agg_perm2/agg_PERM/g; s/(w_P w_Q)/(w_X w_Y)/g; s/(w_Q w_P)/(w_X w_Y)/g')" ]; then
  echo "[PASS] 3c: Permutation invariance identical"
  PASS=$((PASS + 1))
else
  echo "[FAIL] 3c: Permutation invariance differs"
  FAIL=$((FAIL + 1))
fi
echo ""

# TEST GROUP 4: Combination Rules Coverage
echo "--- TEST GROUP 4: Warrant Combination Rules ---"

RESULT=$(run_metta_query "$FIXTURE" "(match &self (warrant-combination-rule $w all-required) $r)")
check_result "4a: all-required rule present" "w_001" "$RESULT"

RESULT=$(run_metta_query "$FIXTURE" "(match &self (warrant-combination-rule $w independent-corroboration) $r)")
check_result "4b: independent-corroboration rule present" "w_002" "$RESULT"

RESULT=$(run_metta_query "$FIXTURE" "(match &self (warrant-combination-rule $w weakest-link) $r)")
check_result "4c: weakest-link rule present" "w_003" "$RESULT"

RESULT=$(run_metta_query "$FIXTURE" "(match &self (warrant-combination-rule $w out-of-domain) $r)")
check_result "4d: out-of-domain rule present" "w_004" "$RESULT"
echo ""

# TEST GROUP 5: Diagnostics-Flag Generalization
echo "--- TEST GROUP 5: Diagnostics-Flag Generalization ---"

RESULT=$(run_metta_query "$FIXTURE" "(match &self (diagnostics-flag $agg correlation-detected $detail) $r)")
check_result "5a: correlation-detected flag queryable" "agg_001" "$RESULT"

RESULT=$(run_metta_query "$FIXTURE" "(match &self (diagnostics-flag $agg independence-unverified $detail) $r)")
check_result "5b: independence-unverified flag queryable" "agg_002" "$RESULT"

RESULT=$(run_metta_query "$FIXTURE" "(match &self (diagnostics-flag $agg stale-aggregate $detail) $r)")
check_result "5c: stale-aggregate flag queryable" "agg_003" "$RESULT"
echo ""

# SUMMARY
echo "=== SUMMARY ==="
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo "Total:  $((PASS + FAIL))"
echo "Completed: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

if [ "$FAIL" -gt 0 ]; then
  exit 1
else
  exit 0
fi

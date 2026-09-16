# New Task Generator Design Spec (draft v41, rev2)

## Purpose
Rebuild benchmark task data with full provenance, replacing unvalidated v30-v40 claims. Mechanisms reused from v31 (Haar/attention) and v34 (kernel-FM); this is a NEW benchmark (v41), not a continuation. No continuity claims until approved by Ben.

## Two-part data model
1. Public task manifest (policy-visible): task_id, family, seed, input arrays (base64 npz), p_i params, generation metadata.
2. Sealed evaluator ledger (NOT policy-visible): oracle target labels/actions, J_star, J_random, keyed integrity tags.

## Public manifest schema (JSON per task)
- task_id: v41-{family}-{seq:04d}
- family: haar_encode | attention_2d | fm_kernel_loss
- seed: int (per-task, recorded)
- input: family-specific arrays (base64 npz, canonical serialization)
- p_i: mechanism params
- generator_commit: git SHA + clean-tree status flag
- rng: algorithm + version
- param_dist_version: version of parameter-distribution spec
- source_modules: path + file hash for reused v31/v34 mechanisms
- NO target hashes in public manifest (10-bit targets brute-force reversible)

## Sealed evaluator ledger (JSON per task)
- task_id
- oracle: target labels/actions (policy-forbidden)
- J_star: analytic, computed at generation time
- J_random: analytic where available; if estimated: rollout count, seeds, estimator, CI
- integrity: keyed tag (HMAC-SHA256) over canonical payload; key held in sealed store

## Canonical serialization (required for any hash/tag)
- JSON: sorted keys, no whitespace, UTF-8
- NPZ: fixed dtype and byte order; array order defined per family

## Splits (frozen in index.json)
- train/validation/test assignment frozen at generation; family-stratified counts recorded; held-out disjoint seed range for test

## Action/evaluator contract
- policy emits action a per task; evaluator maps a to deterministic reward; mapping lives only in sealed ledger
- per-family reward from v31/v34 mechanism behavior:
  - haar_encode: reward = reconstruction fidelity vs oracle encoding
  - attention_2d: reward = target-attention alignment score
  - fm_kernel_loss: reward = negative kernel-FM loss vs oracle optimum

## Versioning
- generator version string in every manifest; any mechanism change bumps version

## Status
Design proposal for Ben; not an implementation approval.

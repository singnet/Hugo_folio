# Science-Protocol Benchmark: Draft Write-up

## Goal
Measure genuine scientific-inference ability (hidden-law discovery) across six synthetic worlds: mechanics, chem, eco, gene, astro, geo. Agents see *strict observation prefixes* and must predict an explicitly queried future state (predict_at); all hidden laws/parameters and future target values live in a server-side private manifest.

## Dataset
- 600 tasks (100/world), splits 420/90/90 train/dev/test, shuffled with fixed RNG.
- Seeds are 128-bit, HMAC-SHA256-derived from a private master seed; a public SHA-256 commitment (master_seed.sha256) is committed so the corpus cannot be silently swapped.
- Agent view: id, world, predict_at, observable fields only. Seed keys and hidden fields (law/rules/pos/signs/reg/params/layers) stripped; targets removed from history (prefix ends before predict_at).

## Anti-cheat (adversarial evaluation)
Attacks run against the real evaluator, each must stay at/below a predeclared normalized floor of 0.55 (chance=0, oracle=1):
- *constant*: predicts 0/empty. Score 0.118. PASS
- *copier*: copies last observation of the prefix. Score 0.294. PASS (targets no longer in history)
- *metadata*: hidden fields absent from agent view. Score 0.000. PASS
- *seed match (brute-force)*: regenerates trajectories via public generators across seed space, matches observed initial state, then reads off the target. With 128-bit HMAC-derived seeds no matches are expected; measured score 0.114. PASS (attack runs per-world in evaluate.py via portable generator import)

## Reproducibility
Reproducibility: the corpus derives from committed generators + build_agent_view.py plus the private master seed, whose SHA-256 commitment (master_seed.sha256) is public. A clean clone can verify the commitment and code, but evaluator scores require the private manifest; docs/provenance.json records manifest hash, seed commitment, commit, and attack outputs.

## Scoring
Per-world normalized scores: 0=chance baseline, 1=oracle. Attack scores at/below floor confirm tasks cannot be solved without inferring the hidden law.

## Next steps
- Clarify that attack_corpus_reconstruct is a bounded random-master attack (64 random masters x 8 task indices, fingerprint on first observation), not an exhaustive full-corpus reconstruction; optionally extend to full candidate-corpus fingerprinting.
- Baseline agents (curve-fit, LLM, hybrid) on dev/test.
- Report per-world normalized scores in final write-up (due Monday).
- Baselines: naive curve-fit extrapolation scores 0.283 normalized on dev (n=75 target-bearing tasks), well below attack floor context; LLM baseline TBD.
- Baselines on dev (n=75 target-bearing tasks): last-value 0.944, curve-fit extrapolation 0.283; LLM baseline TBD.

# Science-Protocol Benchmark: Draft Write-up

## Goal
Measure genuine scientific-inference ability (hidden-law discovery) across six synthetic worlds: mechanics, chem, eco, gene, astro, geo. Agents see *strict observation prefixes* and must predict an explicitly queried future state (predict_at); all hidden laws/parameters and future target values live in a server-side private manifest.

## Dataset
- 600 tasks (100/world), splits 420/90/90 train/dev/test, shuffled with fixed RNG.
- Seeds drawn from 2^32 space (not 0-49) after the brute-force seed-match attack scored 1.000 against enumerable seeds; regeneration is now infeasible for attackers.
- Agent view: id, world, predict_at, observable fields only. Seed keys and hidden fields (law/rules/pos/signs/reg/params/layers) stripped; targets removed from history (prefix ends before predict_at).

## Anti-cheat (adversarial evaluation)
Attacks run against the real evaluator, each must stay at/below a predeclared normalized floor of 0.55 (chance=0, oracle=1):
- *constant*: predicts 0/empty. Score 0.118. PASS
- *copier*: copies last observation of the prefix. Score 0.294. PASS (targets no longer in history)
- *metadata*: hidden fields absent from agent view. Score 0.000. PASS
- *seed match (brute-force)*: regenerates trajectories via public generators across seed space, matches observed initial state, then reads off the target. After the 2^32 seed widening, no matches found. Score 0.078. PASS (attack runs per-world in evaluate.py via portable generator import)

## Reproducibility
Private labels manifest is reproducible from the committed public generators + build_agent_view.py; anticheat.py (schema) and evaluate.py (adversarial floor checks) are committed and runnable from a fresh clone given regenerated data.

## Scoring
Per-world normalized scores: 0=chance baseline, 1=oracle. Attack scores at/below floor confirm tasks cannot be solved without inferring the hidden law.

## Next steps
- Extend brute-force seed attack to all six worlds.
- Baseline agents (curve-fit, LLM, hybrid) on dev/test.
- Report per-world normalized scores in final write-up (due Monday).

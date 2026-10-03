# Claim-Coverage & Atom-Validity Benchmark

Scope (shared with Protomega Goertzelbot, approved by Ben Oct 3):
1. *Claim coverage*: for each world task (geo, chem, astro, gene, mechanics, eco), measure how many target claims are formalized vs plain-language.
2. *MeTTa atom validity*: check candidate atoms are syntactically valid MeTTa and semantically coherent across the corpus.

## Fixtures
- Input: seeded worlds from data/ + labels_manifest.json (test split, integrity hashes).
- Fixture format (JSONL per world): task_id, seed, claims[] with fields {claim_id, text, status: full|sketch|candidate_atom|conjecture, metta_atom (nullable)}.

## Scoring
- ClaimCoverageScore = full_formalized / total_claims (per world, macro-avg across worlds).
- AtomValidityScore = valid_atoms / candidate_atoms, where valid = parses as MeTTa s-expr AND passes coherence check (bound variables, consistent arity/types with corpus ontology).
- Report both per-world and aggregate; publish alongside seed + integrity hash for reproducibility.

## Baseline plan
Run comparative baselines against same seeded scenarios (no re-seeding), using v1 frozen behavior (proceed/review/caution) as reference point.
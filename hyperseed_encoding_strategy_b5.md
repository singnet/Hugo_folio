# B5 — Hyperseed Atomspace Encoding Strategy
2026-10-16 — Hugo, for joint review with Haley Lowy (U0BG1E4UUKD)

## Goal
Systematically encode Ben Goertzel's Hyperseed ontology (v1: ~90 concepts; v2: 200+ concepts) into my atomspace so it supports (a) current evaluation tasks and (b) future reasoning over Hyperseeds *and* their interrelations with my existing atoms.

## Guiding Principles
1. Concepts as first-class atoms: (Concept "HS:primitive") etc., with an HS: prefix to namespace Hyperseed terms apart from my organic atoms while remaining joinable.
2. Typed relations, not free text: each ontological edge becomes a typed MeTTa relation, e.g. (--> HS:primitive HS:category), (Relates HS:distinction HS:variety).
3. Timestamped links per our design: (Timestamped (Concept "HS:primitive") "2026-10-16T03:53") so temporal queries stay attached to content — coherent, bidirectionally queryable.
4. Bridge atoms connect Hyperseeds to my corpus: (RelatedTo HS:variety DAS-notes), (AppliesTo HS:occasion ECB-evidence-model), enabling cross-domain reasoning.
5. Provenance: every HS atom carries (Provenance atom "Hyperseed v1/v2 post, date") — falsifiable, auditable.
6. Incremental ingestion: batch-by-batch (10 concepts/batch), each batch committed, queried, and smoke-tested with a reasoning probe (e.g. one PLN implication chain) before the next.
7. Versioning: HS-v1 and HS-v2 kept as distinct content versions (like ECB content-version), so v1→v2 conceptual evolution is itself reasoning material.

## Phases
- P0: Schema design — pick relation vocabulary (Inheritance, Relates, PartOf, EvalLink examples).
- P1: Pilot batch (10 core concepts: primitive, distinction, repetition, variety, occasion, ...), verify with queries + one reasoning probe.
- P2: Full v1 ingestion; P3: v2 ingestion with evolution edges; P4: bridge atoms to existing knowledge; P5: evaluation harness — measure retrieval accuracy and reasoning improvements.

## Open Questions for Haley
- Should bridge relations to my own beliefs carry confidence values (stv)?
- Do you want a coverage report per batch in Slack, or only at milestones?
- Priority order for concept batches — thematic or as-listed?

## Status
Draft v1 — awaiting review.
## Revision 2 — incorporating Protomega review (2026-10-16)
1. P4 bridge design runs in parallel with P1 pilot: early cross-domain queries will shape the relation vocabulary actually needed.
2. All bridge atoms carry STV confidence values, e.g. (AppliesTo HS:occasion ECB-evidence-model) (stv 0.7 0.4), so PLN can chain through bridges without treating speculative links as established fact. Connects to v2 severity layer in dep_disc_spec_v2.md.
3. Batch smoke tests require a discriminating PLN chain (must depend on the specific atoms in that batch, not a trivially-firing chain); each batch defines its pass criterion up front.

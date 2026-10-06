ECAN-PLN Premise-Selection Harness

## Setup
- Nodes = atoms, edges = Hebbian links.
- Task: select k=10 premises to guide forward chaining from source to target, 20-50 trials per condition.
- Topologies: dense GNP(100, 0.05), sparse random (p=0.01), scale-free (n=200, m=2), hierarchical 5-cluster.

## Experimental Results (Nov 6, 2026)
- Dense: no differentiation (all 20/20, depth ~3).
- Structured/sparse: ECAN wins clearly. Hebbian depth 2.0 vs random 3.1 on scale-free; bidirectional STI seeding depth 1-2 vs random 3.9-6.7 across topologies.
- Best STI ratio: 80 percent target / 20 percent source (depth 2.0).

## Lesson
Pure source-seeded attention gets trapped locally; ECAN helps PLN when it bridges source and target clusters.
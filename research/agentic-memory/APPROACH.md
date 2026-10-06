# Agentic-Memory Approach (for Haley)

Goal: a memory architecture that lets an agent accumulate, consolidate, and retrieve task-relevant knowledge autonomously.

## Core ideas
- Layered store: short-term pins (task state), episodic logs (timestamped events), semantic atomspace (distilled facts/skills with confidence).
- Write policy: pin for in-flight state; remember for valuable items; periodic consolidation episodes -> semantic facts (summary + embedding).
- Read policy: query embeddings with short phrases before every response; episodes for time-bounded recall.
- Decay and relevance: older, unretrieved items lose strength (ECAN-style importance spreading) to keep the store compact.
- Agentic loop: self-chosen long-term goals drive curiosity queries; retrieval failures become candidate goals for learning.

## Next steps
- Prototype consolidation script that summarizes episodes into atomspace facts.
- Evaluate retrieval hit-rate on past task transcripts.
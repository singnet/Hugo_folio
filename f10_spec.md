# F10 Spec: Non-Equivocating Public Provenance

## Scope
F09 established tamper-evident *local* provenance via a canonical hash chain.
F10 extends it toward *non-equivocating public* provenance, per Protomega's review.

## Canonical Event Envelope
Every event MUST include:
- `chain_id`: stable identifier of this provenance chain
- `writer_key_id`: identifier of the signing writer key
- `protocol`: protocol name and version (e.g. `omega-provenance/1`)
- `event_id`: monotonically allocated sequence number (no gaps except declared crash gaps)
- `prev_hash`: hash of the previous canonical event (chain genesis: fixed seed)
- `content_hash`: hash of the referenced tool input/output payloads
- canonical serialization: sorted keys, fixed encoding (as in F09)

## Witness Checkpoints
- Periodic checkpoints signed over `(chain_id, event_id, head_hash)`.
- Sent to at least one independently queryable witness.
- Witness failure behavior: writer continues appending, marks checkpoint
  `pending`; if witness remains unavailable past a defined interval, emit
  explicit `witness_unavailable` event. Never fabricate a witnessed checkpoint.

## Execution Intent / Outcome Protocol
- Before any external tool call with side effects, append
  `execution_intent` with a unique `operation_id`.
- After completion, append `execution_result` referencing `operation_id`.
- On recovery after a crash, if intent exists without a matching result,
  append `outcome_unconfirmed` referencing `operation_id`. Never emit a
  completed event without verified execution.
- Retry MUST reuse the same `operation_id` so non-idempotent side effects
  are not silently duplicated.

## Required Tests
1. Fork exposure: two successors with same `prev_hash` from one writer;
   detected after witness checkpoint comparison.
2. Crash at every boundary (before intent, after intent, after execution,
   before receipt append): recovery yields intent + `outcome_unconfirmed`,
   never a misleading completed event.
3. Retry after crash: no silent duplication of external side effects
   (same `operation_id` idempotency).

## Explicit Limitation (carried from F09)
F09 (and F10 before witness deployment) is tamper-evident local provenance;
equivocation detection requires a shared, independently queryable witness
comparison point.
## Trust Model (per Protomega review)
A witness checkpoint establishes *publication to that witness* only — not
universal visibility, and not Byzantine safety by itself. One honest,
independently queryable witness suffices to expose a later conflicting
checkpoint *to parties who compare*. Stronger non-equivocation requires
multiple witnesses/gossip or a transparency-log consistency protocol.

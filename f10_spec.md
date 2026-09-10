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

## Clarifications (round 2, per Protomega review of 2c38bc6)

1. *Signatures*: every checkpoint (and ideally every event) carries signer, signature algorithm (Ed25519), and `writer_key_id` resolvable to a public key via a defined registry; key rotation/revocation events are first-class chain events signed under the outgoing key.
2. *Witness receipts*: witness MUST return a durable, signed receipt (over `(chain_id, event_id, head_hash)`); verifiers query the witness by `(chain_id, event_id)` and validate the receipt signature. Append-only/consistency proofs are required for full transparency-log semantics (deferred).
3. *Retry policy*: `operation_id` deduplication applies only to idempotent or queryable tools. For non-idempotent, non-queryable tools, recovery MUST NOT auto-retry; `outcome_unconfirmed` is retained and human/agent confirmation is required.
4. *Content hash construction*: `content_hash = H(domsep || H(input_blob) || H(output_blob))` with domain separation per event type; input/output artifact hashes are recorded separately; missing blobs resolve to an explicit `blob_unavailable` marker, never silently omitted.

## Terminology
Until witnesses are deployed and verifiable, F10 is a *design for* public non-equivocation, not public non-equivocation itself.

## Security boundaries (round 3, per Protomega review of 6ee45a0)

1. *Normative signature scope*: every checkpoint MUST be signed; an individual event is authenticated only once included under a verified signed checkpoint — the uncheckpointed tail is provisional. Per-event signatures are optional, not required.
2. *Witness equivocation exposure*: the witness receipt API MUST support queries returning *all* receipts for a given `(chain_id, event_id)` (or head-hash range), not single lookups, and MUST expose any conflicting receipts. Trust model explicitly assumes a Byzantine witness may issue and selectively return receipts; equivocation resistance for the witness itself requires an append-only auditable log or gossip across independent witnesses (deferred, stated as limitation).
3. *Key registry trust anchor*: the initial registry entries (writer_key_id -> public key) are the trust anchor, provisioned via a defined out-of-band bootstrap process and recorded as a genesis event on the chain.
4. *Key rotation continuity*: rotation MUST be signed by both old and new keys (dual-signed rotation event); exception: compromise recovery allows single signature by the new key plus a designated recovery quorum, recorded as an explicit `compromise_recovery` event.

With these, F10 spec is regarded as ready to implement and test.

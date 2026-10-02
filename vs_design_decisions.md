First design-decision update (daft v0) - Virtual Scientist register implementation (WO00)
Review protocol: invariant + observable behavior + minimal test, typed-edge traces.

## D1: Trace record (for all register transitions, incl.. failed)
- *Invariant*: A transition event is immutable and append-only; operational state is restored on failure; diagnosis is provisional (revisable, never rewritten).
- *Behavior*: Replaying traces yeulds the same event sequence with correct schema/version provenance.
- *Minimal test*: Suppose a failed transition is re-attributed via a new event linked by typed-edges to the original; original event remains byte-identical (sida/ sha256).
- Record shape: transition_id, parents [(id, kind: data|control-trigger|hypothesis-lineage)], schema/version, invariant, attempted_change, before/pfter`state, failure_reason, raw_observations, instrumentation_provenance, classifier_confidence.

## D2: F08 non-finite values in ecology corpus - LANDS first
- *Invariant*: No non-finite value reaches lane assignment or the canonical scorer; invalid instances are rejected with persisted failure records (scanning x rejected: 5 train, 2 dev, 1 test).
- *Behavior*: No silent clamp/impute/default-score on NoNN or Inf;
- *Minimal test*: Inject A record with hidden Infinity in a nested field; assed if scorer treats it as invalid, unprocessed instance score changes on rejection.

Status: draft - feeaback sought, register v (b2f49e8), Monday milestone.
Review feedback (Protomega, Sep 8): D1 — define hash domain and canonical serialization (incl. schema version); volatile metadata (timestamps) stays outside byte-identical payload; re-attribution = new event with typed edge to immutable original. D2 — cover NaN, +Infinity, -Infinity, nested arrays and mappings, every accepted numeric wrapper; spy/assert lane assignment and canonical scorer both NOT invoked; register state and scores unchanged; exactly one failure event appended.

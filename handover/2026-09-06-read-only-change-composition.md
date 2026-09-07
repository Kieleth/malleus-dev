# Read-only knowledge-change composition

## Accepted slice

Luis approved the Core and Semantic Re-entry ownership split on 2026-09-06.
Core owns reusable runtime mechanisms. Semantic Re-entry owns its requirements,
local contracts, experiments, adapters and consumer. This slice is a
REFERENCE_IMPLEMENTATION of the optional compiler-enabled semantic-history
profile. Without that profile it claims no accepted state, admission or replay.
Its generic and Small Shop tests are CONFORMANCE_FIXTUREs, not domain policy.

Claim: a producer can construct the existing KnowledgeChangeSet from an explicit
immutable context without receiving a writer, mutable graph or callback.
Observation: the result equals independently assembled existing KCS bytes,
composition performs no I/O, ordinary admission/reopen accepts it, and an
intervening evidence append makes admission refuse without further writes.
Reuse: the current history composer, KCS parser, retained-role checks, replay,
admission and public population tests. Existing history and population consumers
must use the same composition implementation as the new read-only consumer.
Excludes: Re-entry policy, source-value interpretation, correction inference,
no-op decisions, external effects, a new persisted grammar, signatures, hostile
Python sandboxing, replacement-engine claims, paper and package policy changes.

Pre-action check: local code/tests/docs, no server or endpoint, no new
dependencies, no missing-field defaults. Extract the existing mechanism rather
than retaining a second serializer. Preserve unrelated worktree changes.

## Boundary contract

Public surface, under `malleus.compiler`:

- `KnowledgeChangeHistory.composition_context()` replays history once, outside
  the producer. It returns `KnowledgeChangeContext` containing only immutable
  base coordinates, contract and receipt identities, and retained input values.
- `compose_change_set(context=..., change_set_id=..., source_record_ids=...,
  evidence_record_ids=..., operations=..., valid_time=..., supersedes=...)`
  returns the existing `KnowledgeChangeSet`. The remaining arguments keep
  their current history-composer types and meanings.
- `KnowledgeChangeHistory.compose_change_set(...)` delegates to this same
  implementation after taking its context. There is no legacy fallback.

The context binds all five KCS base coordinates, effective contract identity,
replay receipt identity, and exact retained input IDs, roles, media types and
bytes. It contains no history, graph, path or I/O capability. An internal
consistency fingerprint rejects field or closure substitution. This is not an
authenticated checkpoint or a new portable artifact grammar. Construction is
through the verified history factory, not arbitrary caller-supplied replay data.

Missing or wrong context/input types refuse with the existing
MALFORMED_CHANGE_SET reason. Inconsistent context fields refuse IDENTITY_MISMATCH.
Unknown IDs and inappropriate source/evidence roles refuse UNRETAINED_INPUT.
The existing KCS parser owns operation, valid-time and canonical-wire checks.
Composition is pure and does not validate source truth or decide admissibility.

Retain needed source/plan evidence before taking the final context. Any later
ledger movement, even evidence-only, is invisible to pure composition and is
checked by ordinary admission as STALE_BASE. The coordinator keeps writing
authority. The producer compares its local contract and read data with the
supplied context; it receives no promise of future freshness.

Dependency projection:

```text
HistoryContextFactory implements VerifiedBaseSnapshot
HistoryContextFactory consumes KnowledgeChangeHistory
HistoryContextFactory produces KnowledgeChangeContext
ChangeComposer implements KnowledgeChangeSetComposition
ChangeComposer consumes KnowledgeChangeContext and explicit operations
ChangeComposer produces KnowledgeChangeSet
ChangeComposer governedBy existing knowledge-change-set/private-v0 rules
KnowledgeChangeSet derivedFrom exact base and retained closure
HistoryComposer delegatesTo ChangeComposer
PopulationPreparation consumes HistoryComposer
SemanticReentryConsumer consumes ChangeComposer
CoreAdmission consumes KnowledgeChangeSet
CoreReplay produces accepted KG
```

The consumer must not author Core APIs, change canonical Shop data, or create a
second change identity. This Core slice does not itself prove Semantic Re-entry.

## Evidence

Initial focused RED: 23 failed because the new public context/factory/composer
do not exist. The old private-only export guard is explicitly superseded by a
facade-only export guard. Pending GREEN and full Shop results.

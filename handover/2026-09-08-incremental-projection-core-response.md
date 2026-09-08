# Incremental projection: Core response to Re-entry

Read-only design assessment at `9a0e8b66`, whose runtime is unchanged by the
following Shop evidence/governance commits. This is a proposed future Core
contract, not implementation authorization. The active shipment-rule work
does not change projection semantics or add a cache.

## Current boundary

`KnowledgeChangeHistory.replay()` reads the ledger and calls
`_replay_envelopes`. That fold begins with an empty accepted graph and rebuilds
the machine state, retained inputs, contract revisions and accepted record
history. `_apply_change` rebuilds the staged graph from the current record
history. These are private implementation seams, not a public incremental
consumer contract.

No incremental `KnowledgeChangeHistory` implementation is active in this Core
lane. The [current backlog](2026-09-08-core-backlog.md) keeps complete projection
closure pending. [The projection design](../design/SEMANTIC_LOG_KNOWLEDGE_PROJECTION.md)
already requires full/incremental and delete/rebuild convergence. Its
`CompleteProjectionClosure` is explicitly a proposed local artifact, not a
shipped object. Recon's separate incremental path is precedent to inspect,
not evidence that its state or cursor can substitute for this history.

## Smallest decision to bring back for approval

Select a bounded, in-memory, read-only incremental projection session over one
identified history. It consumes only committed, contiguous verified suffixes.
It reuses the same event/transition semantics as full replay. Full rebuild
remains the recovery path and test oracle, never a second source of truth.

Before implementation, fix the contract for:

1. A continuation state binding the verified ledger head/count, acceptance and
   materialization heads, active contract, machine state, retained-input and
   record-history state, projector identity and output identity. A graph plus
   a cursor is insufficient for replaying evidence, revisions or later checks.
2. Atomic publication of the new projection, indexes and cursor. A refused or
   interrupted suffix leaves the previous published state unchanged.
3. Read freshness: a result names its consumed head. A request for a newer exact
   head either catches up or reports explicit lag/refusal, never silently
   presents an older view as current.
4. Refusal/recovery for a missing prefix, wrong previous hash, truncated or
   rewritten history, stale contract, and unsupported continuation identity.
   No silent reset to an empty graph and no independent graph write path.

The first TDD witness can reuse the Shop: initial population, evidence-only
append, additive contract revision, correction and two shipment admissions.
At every committed prefix, compare incremental graph, record history, machine
state and all three heads with full replay. Also prove an invalid suffix does
not publish half a state. Do not infer correctness from a faster final query.

Durable checkpoints, a database, asynchronous projection workers, concurrency,
new history semantics and a second projector are not selected by this proposal.
This addresses runtime read cost. It does not replace the adopter's separate
domain-history choices or promote all proposed projection-closure terms.

# Core backlog, current projection

This is a reading view of the existing program and append-only overseer ledger,
not another plan authority or DAG. Status is bounded by the linked evidence.
The sequence was approved by Luis: faster tests and this reconciliation first,
then a partial-shipment Shop exercise. Luis subsequently selected documentation,
push and release; the [release preparation](2026-09-08-core-release.md) records
that bounded publication work.

## Already delivered, do not reopen as missing prerequisites

| Earlier pending item | Current bounded result |
|---|---|
| Public source-to-history-to-graph path | `malleus.compiler` compiles, prepares, structurally admits, reopens, queries and traces. The [default Shop run](2026-09-06-core-shop-default-admission.md) uses Core-owned checks, not caller-authored success outcomes. |
| Full domain-history declarations | [Three shipped profiles](2026-09-03-core-population-p6-report.md), not arbitrary executable projection programs. |
| Ontology evolution in the same knowledge history | [Additive contract revision](2026-09-03-core-population-p5-report.md) and the Shop conformance fixture preserve prior records. This does not close general migration or legacy `ProtocolLedger` evolution. |
| Event population | The selected profile's Event role admits concrete Events and qualified EventParticipation. Event-to-Event ordering and Signal population remain outside the cut. See [implementation status](../docs/IMPLEMENTATION_STATUS.md). |
| No stated domain time | [Explicit `NONE_STATED`](2026-09-06-unstated-valid-time.md), not an invented timestamp. |
| Source/evidence constructor convenience | [Public constructors](2026-09-07-source-input-constructors.md) remove default-bundle envelope assembly. They neither interpret sources nor admit knowledge. |
| Finite executable action history | [Integrated optional attachment](2026-09-08-executable-action-main-integration.md), then [two sequential actions](2026-09-08-sequential-action-plan.md). It does not replace standalone Assent. |
| Action setup on an adopter's existing history | [Four reference constructors](2026-09-08-action-input-producer.md), verified at `0cdf8ed`. No all-stage installed SDK or consumer integration is claimed. |
| Core baseline verification | [3,327 passed and 3 skipped](2026-09-08-core-default-suite.md) at its exact older coordinate, followed by the action producer's separate 742-test gate. Neither count means the full suite ran at every later commit. |

## Approved work completed in this slice

1. Repeated Git ancestry work is removed without weakening validation. Both
   complete governance suites pass. The [results](2026-09-08-core-pareto-results.md)
   give measured timings and exact selectors.
2. This view reconciles the old pending lists without rewriting their receipts.
3. [Partial shipments](../research/ontology_driven_kg_realization/experiments/small_shop/partial_shipments/README.md)
   now run after the existing complete default Shop. The synthetic sibling uses
   existing additive revision, population, structural admission, query and replay.
   Its five tests and the complete 248-test Shop selection pass.
4. The selected [shipment policy episode](../research/ontology_driven_kg_realization/experiments/small_shop/shipment_policy/README.md)
   adds the next proof: the existing rule executor consumes a compiled contract;
   duplicate unit assignments refuse atomically, while distinct units admit and
   replay. The rule stays in Shop artifacts. This uses a fresh selected-policy
   history, not migration of the earlier structural-only example. Its separate
   validation receipt does not replace the historical 248-test result above.

Robotics owns its application integration. Semantic Re-entry owns its consumer
experiment and adapters. Their local successes are not Core results until
reported and bound separately. Neither lane owns Core runtime or governance.

## Implemented: maintained ledger-fed graph

Owner: **Core**. Luis subsequently activated the bounded in-memory slice,
implemented at `851913c0` after RED `7c29da51`.
The [implementation contract](2026-09-08-maintained-projection-plan.md) records
the scope and TDD observations. The earlier
[Core response](2026-09-08-incremental-projection-core-response.md) is design
input, not a frozen implementation contract.

The reader, history, graph and protocol gate passed 469 tests. The complete
Shop gate passed 253 tests; seven targeted Recon replay tests also passed.
Existing compiler-bound Shop evidence remains unchanged. Detailed evidence and
the projection-only timing observation are in the
[result receipt](2026-09-08-maintained-projection-results.md).

Keep a long-lived, replay-derived KG and its history/protocol indexes. Advance
them from verified committed ledger suffixes, without folding the full prefix
on every read or rebuilding every unaffected record on each KCS. The one
append-only ledger remains authoritative. No direct accepted-graph writer or
new public change identity is permitted.

Acceptance requirements for this slice:

1. Reuse full replay's semantic transition interpretation. Publish graph,
   indexes and cursor atomically at complete transaction boundaries.
2. Keep full ledger head/count separate from acceptance and materialization
   heads. Protocol-only events advance their state without changing domain
   facts. Re-entry reads must expose lag or refuse a stale requested state.
3. Bind the effective contract, profile, interpreter and required retained
   inputs, including all history/protocol continuation state. A graph-only
   checkpoint is insufficient.
4. Prove full/incremental convergence for graph, provenance, supersession and
   protocol state, and rebuild/recover from retained JSONL alone.
5. Test gaps, duplicate suffixes, mismatched cursors, interrupted publication
   and supported contract changes. Guard mechanically against repeated
   full-prefix folding and unrelated-record reconstruction during ordinary
   advancement.
6. Measure projection separately from ledger persistence and admission costs.

First reuse the merged supplier Re-entry episode at landing
`4a5cc7658c6147d77fad9224f523bf0be84d5050` as conformance input. Core owns the
eventual contract and implementation. No database, asynchronous service or new
storage profile is selected. The Re-entry task's undesired-observation case
remains consumer-owned work against existing Core seams, not part of this item.

## Larger Core work still pending, not prerequisites for this Shop exercise

| Work | Dependency and bounded next observation |
|---|---|
| Replace handwritten Assent with declarative execution | [Authorization comparison](2026-09-08-authorization-conformance.md) establishes neutral verdict expectations. The [identified rule artifact](2026-09-08-authorization-rule-artifact.md) now replaces handwritten outcome mapping and precedence while preserving old hashes. Full transition parity, evaluation-hash projection, broader profile coverage and old-path removal remain open. This is not the Assent hard cutover. |
| Formal compiler and independent conformance | The [compiler program](../design/contract_compiler/program.md) still distinguishes the Pareto implementation from formal elaboration, artifact, cross-language and replacement gates. Do not mark those workstreams complete from Shop success. |
| Ontology-bound Core governance ledger | The [registered migration workstream](../design/contract_compiler/workstreams/CC-003/manifest.json) remains blocked on the formal artifact gate. Its intended cut is a retained legacy checkpoint, current-state seed, and one replacement writer, not historical translation or dual writes. |
| Complete projection closure | [Accepted design](../design/SEMANTIC_LOG_KNOWLEDGE_PROJECTION.md), not a shipped generic artifact. It needs exact projection inputs, replay/rebuild convergence and a genuinely different projector before replaceability is claimed. |

## Deferred until a concrete consumer needs them

Action recovery after a non-executing decision, retries, concurrent actions,
selected-profile migration and a high-level consumer SDK remain deferred.
The Shop rule likewise does not yet cover reassignment, cancellation, shipment
subclasses, stock availability or delivery. Executed check receipts are retained
attestations, not protection against forged low-level caller events.
So do typed retraction, richer dependent temporal projection, Event-to-Event
ordering, Signal population, non-additive or import-changing contract migration,
multi-writer serialization, stable wire formats and generic graph backends.

Do not add more packaging or version-enforcement work to this sequence. Existing
checks remain in force. The later release request selects the existing
publication gate, not a dependency experiment or wheel project.
A concrete blocker gets an exact reproducer;
an attractive generalization stays here until selected.

## Historical-list reconciliation

The [September 3 Pareto note](2026-09-03-population-pareto-backlog.md) is preserved
as the original cut. Its full-profile item and the additive subset of same-file
evolution have since shipped. Its general migration, concurrency and exhaustive
hardening items have not. The [September 6 adoption report](2026-09-06-core-adoption-docs.md)
predates the source constructors and action attachment; it remains a historical
receipt, not the current queue. The original single-action handoff likewise
describes that exact profile, while the sequential profile is separately selected.

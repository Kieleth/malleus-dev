# Count retrieval repaired, deployment context still missing

E-0306, 2026-09-08. The unchanged graph now returns **19 network instruments**
for CQ-T1-02 and its paraphrase CQ-C-04. It does not substitute the separately
stored 17 useful instruments. All 28 other query objects remain unchanged,
including the complete CO2-degassing argument and its SUPPORTS paths.

This is recovered information, not new capture. Source, ontology, Core 160878c,
164-record graph, 173 historical versions and 45-event ledger remain unchanged.
The new reader is count-query-01, a successor to depth-method-01. The previous
reader and complete snapshot review remain frozen evidence.

## What changed

The old selector required deployed/deployment wording. The stored count instead
describes instruments in the network. Removing the old filter alone would also
admit useful-subset and detection-threshold counts. The replacement accepts
explicit deployment or whole-network membership wording on the count record,
requires an integer count and excludes the tested subset/threshold/negation cases.
Instrument identity can come from the explicit subject; the subject cannot
supply missing count scope. Nothing is inferred from IDs or source locators.

Only instrument_count and its note change in the query program. An AST check
preserves all other functions and declarations. The comparison runner adds one
explicit current-history condition, reusing public replay, frozen source-free
queries and the existing trace machinery. Historical depth reproduction uses
its own frozen reader, so this new count rule cannot enter its old experiment.

## Returned answer and remaining gap

Both questions now return one CountObservation row:

| Returned field | Value |
| --- | --- |
| count | 19 |
| count_scope | ocean-bottom seismometers in the network |
| subject | instrument:obs |
| inline subject | ocean-bottom seismometers, tag OBSs |
| graph paths | None |

The coordinator's source-grounded assessment finds the count and observing
system supported by page:2:block:002, with the distinct total/useful scopes also
confirmed in page:6:block:002. The answer still lacks deployment context.
Assessment: NONE 0/3 to PARTIAL 2/3 for the positive question and its paraphrase.
This is **model-assisted, nonindependent, pending human ratification**. No new
complete answer or aggregate thirty-question score is claimed.

The five newly reached field derivations resolve through their original retained
capture. No population record, source assertion or relation was added. Seeing
the source's deployment statement does not permit the reader to invent it in
the returned answer.

## TDD and reproduction

Corrected RED: sixteen failures and twelve passes. GREEN covers network counts,
zero, explicit deployment counts, useful/recovered/operational subsets,
per-event thresholds, negation, integer shape and non-borrowed scope. The
comparison guards reject unrelated answer changes, modified fields, invented
paths, duplicate/missing rows, changed bindings and runtime drift. Focused
count/depth/answer/subject selection: 88 passed. Final broader paper selection:
548 passed and two subtests. Ruff, formatting and scoped diff checks pass.

The first broader run caught a stale historical AST test, not a graph regression.
It now binds the historical depth reader explicitly, while the new count test
checks the active reader's separate change. No old expected output was rewritten.

Both retained executions produce the same four output files. There are 62 row
occurrences, six paths and 56 traced records. All 292 capture-scoped derivations
resolve. The prior 30 query objects reproduce before the change; exactly two
change afterward. Ledger, graph and replay receipt are byte-identical.

This bounded wording rule is not a general count-role parser. Broader source
context still belongs in the representation. No Core defect was found.

## Evidence and follow-up

[Method binding](../../private/paper-v4-answer-demonstration/count-query-01/method/method.json),
[query output](../../private/paper-v4-answer-demonstration/count-query-01/first/query-result.json),
[repeat](../../private/paper-v4-answer-demonstration/count-query-01/repeat/summary.json),
[assessment](../../private/paper-v4-answer-demonstration/count-query-01/assessment.md).
These are local private evidence links, not a published replication bundle.

Method SHA-256: af604ffe7ffe3c8f3bbcadb26a5f68f94dc139e72c7e2ecd6e08f293c9f94c68.
Query output SHA-256: 10f01d53610a3a6ff9f0c2023f5eb6bb7880b9fe60b6c6a19ef9f62d7b00b6e2.

Next in the [gap plan](GAP-REPAIR-PLAN.md) is source-context repair, separately
bounded before any model proposal. Luis's fourth milestone is another run
comparing progress, not merely another replay of this history. No new capture,
independent reviewer, Core rebind or manuscript edit was launched in this cut.

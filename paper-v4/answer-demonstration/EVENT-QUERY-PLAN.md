# Read the events already referenced by causal claims

E-0326, 2026-09-08. Luis approves implementation after the fresh comparison.

The graph already says which event is the proposed cause and which is the
effect. The current answer displays only their identifiers. Return those event
records so the answer can say what the proposed mechanism is. Do not ask for a
new capture to reproduce content already accepted.

## Bounded change

Keep Core 160878cf14c0d27b11a440e26688708e9b7a7e2b and the exact
sol-fresh-comparison-01/attempt-02 ledger, graph, ontology and original answers.
Start with the frozen duration reader, not a changed historical program.
Only CQ-T4-01, CQ-T4-02 and CQ-T5-01 may gain context, and only when their existing
rows have declared scalar cause_event/effect_event references to Event records.

Append each directly referenced event once, in identifier order, with the
existing row projection and its subject if present. Keep the original rows
unchanged. The claim's reference fields identify the cause and effect. Do not
invent a Relation record or add a path to the existing relation-path list.
No recursive event traversal, lexical inference, source lookup, alias mapping
or extra candidate selection. Missing references do not invent context; present
but broken or mistyped references refuse with an actionable diagnostic.

## Tests, execution, assessment

1. Write failing synthetic tests for expansion, exact role binding, one-hop
   behavior, duplicate suppression, preserved modality and original fields,
   malformed/missing/mistyped targets, and unchanged unrelated queries.
2. Implement the small projection extension without editing frozen readers or
   their executors. Bind it as a new read method. Add an exact-delta guard and
   a pinned-history integration test, including method-drift refusal.
3. Reopen the actual history and reproduce the old thirty answers first. Run
   the successor reader twice, retaining answers, trace closure and comparison.
   Require identical output trees and unchanged ledger, receipt and graph.
4. Assess every changed answer and newly returned event against the retained
   source and existing interpretation. This coordinator assessment is model-
   assisted and not independent; human ratification remains pending. Do not
   silently replace the complete independent review or its aggregate totals.

The intervention can recover event descriptions, not missing network role,
material stage, site scope or snapshot-warning text. No passing score is assumed.
No new producer/reviewer, Core change, source amendment, manuscript edit,
dependency, commit, push or branch/ref change is authorized here.

Pre-action check: no server interaction or API endpoint. Required configuration
and reference fields must fail loudly rather than default. This successor adds
an explicit projection stage, not a fallback to a legacy path. Historical
experiments remain evidence, not a runtime fallback. Guard the observed failure
class with discriminating tests before implementation.

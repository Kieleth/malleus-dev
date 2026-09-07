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
facade-only export guard.

- RED: `8e6c8db1b3045b008a40d7a695b3eb108fcc82a4`.
- Executable GREEN: `741d41b06005db76b032113a8ebc37fc6ef68283`, tree
  `08e14a5650f5e94c90a4fd26cc12626e21a79ef1`.
- New context tests plus existing history tests: **114 passed**.
- Public five-plan Shop run, including an explicit snapshot-only coordinator:
  **4 passed**. The recorded evidence is unchanged byte for byte. Five changes
  cross two contracts; reopening adds no events; supplier e7 traces to e4.
- Full `tests/contract_compiler/pareto` plus
  `research/ontology_driven_kg_realization/experiments/small_shop`:
  **755 passed**, no failures or skips, in the declared project environment.
- `tests/test_status.py` plus the GraphRecipe experiment: **52 passed**.
- Changed-file Ruff and scoped diff checks pass.

Whole-file formatting has one pre-existing difference in the unchanged YAML
literal at `test_knowledge_change_history.py` lines 61-111. It is not part of
this slice and is left untouched. The two production files, new context tests
and changed public Shop test pass format checking.

All pytest commands use `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=src:.`,
`.venv/bin/python -m pytest -q -p no:cacheprovider --tb=short` followed by
the selectors above. This is not a full-repository or release claim.

Semantic Re-entry independently inspected the exact executable GREEN and found
no concrete consumer mismatch. Its local consumer RED is
`a990d4ab7f54d028d4abeef119d8b2ca2c7f698d`, tree
`062fc06f138018213df13fb852da0ef7bc2f4584`: one fixture check passed and 50
specification cases fail because the consumer does not yet exist. These are
not 50 discovered runtime defects, nor completed Re-entry evidence. Its frozen
prerequisite packet remains unchanged. The final Core coordinate must precede
consumer integration. No fixture, mapping, ontology or historical evidence was
changed for this implementation.

## Scoped self-inquisition

Root ontology rites: NOT RUN, no root ontology change. The development skill's
role, optional-profile, artifact-authority and single-ledger checks apply here.

| Claim | Role | Evidence | Unsupported transfer excluded | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| Writer-free composition | REFERENCE_IMPLEMENTATION | Guarded I/O test, frozen context, exact output test | No hostile-code sandbox or signed checkpoint | PASS |
| One existing KCS mechanism | REFERENCE_IMPLEMENTATION | Delegation guard and independent canonical byte expectation | No second serializer or public wire stability | PASS |
| Admission owns accepted changes | OPTIONAL_PROFILE | Evidence-only stale refusal and unchanged admission/reopen | No source truth or epistemic verdict from composition | PASS |
| Shop proves integration | CONFORMANCE_FIXTURE | Exact five-plan evidence, trace and 755-test combined gate | No universal correction policy or completed Re-entry loop | PASS |
| Domain policy stays outside Core | ADOPTER_CHOICE | No new domain names, operations or policy rules in runtime | No automatic decision to propose or stop | PASS |

The internal context fingerprint is a consistency guard over immutable scalar
and retained-input values. It does not authenticate an arbitrary object supplied
by hostile code. The supported factory reads the verified history afresh; it
does not accept an altered disposable replay graph. Producers receive the
result, not the history object. Retention and admission remain coordinator work.

# Action inputs on an adopter-owned history

Luis approved this extraction after the clean Core suite at `386bb42` and
the read-only constructor finding recorded at `1189190`.

## Bounded contract

Classification: REFERENCE_IMPLEMENTATION of the already selected experimental
finite action profile. The new module is repository-local. It is not a public
SDK, new interpreter, protocol invariant or new domain vocabulary. Shop and a
non-Shop history are CONFORMANCE_FIXTURE witnesses. Domain history, selected
programs, sources, policies, actors, timestamps and action meaning remain
ADOPTER_CHOICE inputs.

The claim: one reference producer constructs existing source-registration,
initialization and context/proposal inputs against a caller-owned
`KnowledgeChangeHistory`. It never creates a history, runs Shop, selects a
policy, checks an action, admits a change or performs an effect. Its outputs
remain proposals for the existing owner and selected finite transactions.

The caller first creates/populates its history, retains/selects exact finite
program bytes and registers its chosen prerequisites. The producer reads the
verified replay and exact registered source/policy identities. It accepts
explicit IDs, actors, clock values, source metadata and a caller-built action
record. It emits the existing checkpoint/context bytes and event dictionaries.
No new persisted grammar or initialization migration is introduced.

Reuse: `make_record`, source byte metadata, canonical serialization, the
selected registration/initialization/context programs, and the owning
`append_protocol_events` gate. Initialization remains its existing transaction;
context and proposal still commit together or neither commits. This does not
claim an atomic multi-transaction bootstrap.

Smallest RED: compile/populate a non-Shop domain, prepare real prerequisites,
then invoke the new producer and owning admission in a fresh process that
refuses test and Shop imports. Require exact custom source retention, explicit
metadata, unchanged domain state, atomic context/proposal admission and reopen.
Missing roles/records must refuse clearly; stale or malformed submissions must
preserve ledger bytes. Existing Shop initialization/proposal helpers must
delegate to the same implementation, with the two-action history unchanged.

The prerequisite fixture may reuse existing test builders to prepare the
isolated input prefix. The producer and its fresh-process caller may not import
those builders. Registration of adopter-specific monitors/policies and actual
check execution remain outside this extraction.

Dependency sketch:

```text
selected finite action profile -> governs action input producer
owning history + retained prerequisites + caller action -> consumed by producer
existing checkpoint/context/event inputs -> produced by producer
existing owning finite transaction -> validates and persists inputs
Shop + independent domain -> exercise the same producer
```

## Pre-action checks and exclusions

No server interaction, endpoint, installation, package change or external
effect. Required inputs have no guessed defaults. Remove the old checkpoint
and context assembly from the test helpers, leaving only fixture input choices.
Guard the observed coupling class with a non-Shop, no-test-import witness.

No Robotics domain records, second ledger, new machine instruction, new policy,
recovery, implicit legacy fallback, stable-wire claim, SDK promotion, consumer
merge or remote push. This proves reuse by two fixtures, not replacement by a
second implementation. Performance debt from the prior full suite is separate.

## Implemented entry points

Module: `research.action_history_contract_freeze.programs.action_inputs`.
This is a repository import, not an installed `malleus.compiler` export.

| Constructor | Caller supplies | Result |
| --- | --- | --- |
| `source_event` | Exact bytes, dependencies and explicit origin/representation metadata | Existing source-registration draft |
| `initialization_checkpoint` | Existing history, checkpoint ID, four source IDs and two policy IDs | Existing checkpoint and registered-source references |
| `initialization_event` | Checkpoint, references and explicit metadata | Existing initialization draft |
| `context_proposal` | Existing history, initialization ID, four source IDs, context metadata, action record, proposal/episode keys and optional payload source ID | Existing atomic context/proposal pair |

The source metadata fields are `event_id`, `transaction_time`, `actor_id`,
`role`, `artifact_version`, `media_type` and `locator`. No clock is read and no
record ID is invented. Initialization source roles are `profile`,
`record_contract`, `machine` and `history_binding`; policy roles are `epistemic`
and `authorization`. Context source roles are `goal`, `preservation`, `mapping`
and `pre_state_source`. These roles come from the selected existing profile.

The caller must retain and select the finite program bundle and register its
prerequisites first. The producer does not supply a monitor, policy, grant or
domain mapping. Exact retention does not prove that a goal or mapping is
semantically adequate. `context_proposal` takes an action wrapper with `record_type`
and `record`; the selected program still determines which action record types
are legal. Supplying `payload_source_id` adds the existing sequential profile's
retained-payload reference. Explicit `None` produces the original profile's
pair shape, not an alternative admission route.

Submit returned drafts through the existing owner. For example, after building
`events = context_proposal(history, **explicit_inputs)`:

```python
base = history.replay()
history.append_protocol_events(
    transaction="context-proposal",
    events=events,
    expected_head=base.ledger_head,
    expected_count=base.ledger_event_count,
)
```

The corresponding selected transaction names are `source` and `initialize`
for the other drafts. Construction alone is not admission. A stale context or
invalid second event is refused by the owning transaction without persisting
the first event. A concurrent append after the snapshot is also subject to the
owner's expected-head/count check.

## Proof boundary

The new non-Shop fixture starts with an admitted, three-record domain history.
Prerequisite preparation reuses existing test builders, including its fixture
check outcomes. A separate Python process then prohibits test and Shop imports,
reopens that history, initializes the action context, registers caller bytes
and admits the proposal pair using the new producer. It checks seven added
protocol events, exact source retention and unchanged domain records and KCS
acceptance. This is not a from-zero consumer bootstrap or a real check-executor
proof. The existing two-action Shop test supplies the separate executable-check
regression.

Shop helpers now retain only fixture input choices. Their checkpoint and
context/proposal assembly delegates to the new module. The sequential fixture
creates its action with the payload hash already bound, rather than modifying
action and proposal hashes after construction.

No Robotics or Re-entry consumer was run or rebound in this slice. Their next
step is to consume this exact repository coordinate against their own history.
The finite profile remains experimental; Shop effects and observations remain
synthetic. There is no new interpreter, accepted-graph writer, schema, machine
instruction, public SDK or package change.

### Consumer clarification

Robotics independently inspected `4454199` and asked whether it must author the
remaining prerequisite, assessment, decision and dispatch event data. Yes, that
is the existing low-level route for this experimental profile. Inspection found
no non-fixture, all-stage event constructor beyond the four inputs extracted
here. The retained program builders are reusable; fixture event helpers and
their fixed IDs/timestamps are not a consumer interface.

Reuse these mechanisms rather than copying fixture lifecycle logic:

- `malleus.assent.make_record` and the existing digest/source helpers construct
  explicit record data with caller-owned IDs, clocks and policies.
- `programs.history_checks.run_history_check` runs the existing check executor
  against one actual history prefix and returns its exact prefix coordinates
  plus execution output. It does not append an assessment or establish policy
  acceptance. Carry those coordinates into the later submission checks.
- `malleus.control.evaluate_epistemic_policy` and
  `evaluate_authorization_policy` compute the existing policy results from
  applied records. Do not author a favorable outcome in place of execution.
- `KnowledgeChangeHistory.append_protocol_events` validates and persists the
  caller's explicit event envelopes under the selected retained transaction.
  `KnowledgeChangeHistory.reopen` provides the replay path.

Event envelopes and their required fields come from the selected program's
schemas. Consumers supply data; they must not implement another state machine,
authority check or ledger, nor copy and rename the fixture lifecycle. A future
all-stage authoring helper remains separate work. This clarification does not
claim that Robotics' batch has run through this route, change its frozen pilot
pin or include its independently reported test count in Core's evidence.

## TDD and review journal

RED `55f7a8d082d10e8980af6f1960577e67a7a78c7f` introduces the bounded contract
and eight tests. The missing producer yielded two failures and six fixture-setup
errors, all `ModuleNotFoundError`, not a successful behavioral run.

GREEN `44541993f964674ac4cc994949e121f9de7387ba`, tree
`7ec7da0be2e1bb45991468e098add1f771295c74`, introduces the producer and replaces the fixture assembly in
exactly five Python files. During implementation the new test harness needed
one correction: arbitrary source bytes use their raw SHA-256, not the canonical
JSON `content_digest` function. The final tests also expose child-process stderr,
check typed missing-input reasons and admit/reopen a binary source. Those stronger
assertions were added after the initial missing-module RED. No production hashing
rule changed.

Focused runs in the configured environment:

- New action inputs: 8 passed, no skips, 33.19 seconds.
- Existing initialization and proposal tests: 22 passed, no skips, 78.90 seconds.
- Sequential profile and two-action history: 13 passed, no skips, 291.00 seconds.
- Ruff check, Ruff format check and scoped Git diff check passed.

Self-review: the producer reads verified replay, takes explicit caller choices,
copies the caller action and emits only existing drafts. Old checkpoint/context
assembly was removed from fixture helpers. The selected program and existing
atomic owner still control admission. Neither replay nor accepted state is
reconstructed from an invented test answer. The isolated prefix uses fixture
prerequisite builders, which is disclosed rather than called consumer bootstrap.

The combined run's fresh sequential Shop history has 106 events and raw SHA-256
`cb66165b694d7939a88621a7c275f3a964c15d192abe223a7045bfd32d508477`.
Both match `research/action_history_contract_freeze/sequential-verification.json`
exactly. That older receipt was neither changed nor made a live golden. This
comparison is evidence for this extraction's byte-preservation claim only.

## Combined regression

The committed implementation passed **742 tests, zero skips, zero failures** in
1,770.78 seconds. The selector covers all finite-action program tests, the full
current Small Shop directory and the separate fresh-import tests. This is an
affected integration gate, not a new full-repository, package or release gate.
The earlier focused counts overlap it and must not be added to this total.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider research/action_history_contract_freeze/programs research/ontology_driven_kg_realization/experiments/small_shop tests/contract_compiler/pareto/test_fresh_shop_import.py --tb=short --basetemp=/tmp/malleus-action-inputs.b2xMQg/tests --junitxml=/tmp/malleus-action-inputs.b2xMQg/result.xml
```

The temporary directory was created for this run. Use a fresh temporary parent
when reproducing it. The JUnit XML is
`sha256:cd5b8292ce8053dc8f5184f4da3d86d7e078b4c370efb60cf6d6313550cde6b7`
and reports 742 tests, zero errors, zero failures and zero skips. All five tested
Python files still match GREEN. No runtime,
ontology, program bundle, historical receipt, package, dependency, paper or
downstream consumer file changed. The only remaining mutation is this report
and its append-only governance binding. No remote push was made.

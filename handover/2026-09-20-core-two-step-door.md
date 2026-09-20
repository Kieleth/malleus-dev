# The two-step door: the third entry point, the closed door, the fold

Decision D, paper ledger E-0502 to E-0504, step 2 of two. Luis chose option 1
on 2026-09-20: Core runs every check itself; adopters supply contracts, rules
and change sets, never programs and never outcomes; and a third Core-authored
entry point admits a change set the caller composed, so the public door can
close for everyone.

**This handover records an incomplete step.** Three of the nine numbered parts
of the brief landed and are committed. The migrations that answer the door's
refusal did not. The branch is red on purpose and the measurement below says
by how much and why. Nothing was merged; main is untouched.

## What landed

### The third entry point

`malleus.compiler.check_and_admit_change_set`, implemented in
`src/malleus/_contract_pipeline/admission.py`:

```python
admitted = compiler.check_and_admit_change_set(
    history=history,
    change_set=change_set,
    transaction_time="2026-09-03T00:00:00Z",
    actor_id="actor:producer",
    anchors=(),
)
```

It returns `ChangeSetAdmission(replay, change_set, checks)` and refuses with
`PopulationAdmissionRefusal` at stage `CHECK` or `ADMIT`. No parameter takes
an outcome, pinned by
`test_no_parameter_of_either_entry_point_takes_an_outcome`.

What it shares with `check_and_admit_population_plan` is the whole
implementation after the operations exist. Two functions, called by both and
pinned by an AST test:

- `_check_stage(replay, *, change_set_id, operations, valid_time, plan=None,
  retained_source_texts=())` resolves every required check through
  `resolve_check_contract`, reads the fields the selected machine declares for
  the three protocol events, stages the candidate graph and runs each executor
  in the policy's order. Pure; every refusal leaves the ledger byte-identical.
- `_admit_checked(...)` previews the caller's anchors and then Core's receipts
  through `execute_event` in batch order, mints one retained receipt per check,
  writes `CHANGE_PROPOSED`, one `CHECK_RECORDED` per check and
  `VERDICT_RECORDED` with exactly the declared fields, and appends through
  `_admit`.

`_check_base` and `_check_writes` now take operations rather than a
compilation, and a receipt binds `population_plan_identity` only when a plan
produced the change. The plan path's receipt bytes and ledger bytes did not
move; its 18 tests and the 16 executor tests stayed green throughout.

A composed change set carries no derivation, so `_provenance` returns an empty
`GraphProvenance` rather than inventing one when a required rule layer can read
provenance.

### The door

`admit` and `admit_with_anchors` refuse a caller-supplied `CHECK_RECORDED` or
`VERDICT_RECORDED` with `KnowledgeChangeRefusalReason.CALLER_SUPPLIED_CHECK_EVENT`,
before any append. `_refuse_caller_authored` reads each event and leaves
anything unreadable to `_admit`, which already has the typed refusal for a
malformed batch.

`VERDICT_RECORDED` is refused as well as `CHECK_RECORDED` because
`SELECT_POLICY_VERDICT` derives the verdict from the check records: a caller
who may write the verdict may still decide the outcome by choosing which check
records exist.

Core-authored paths append through `_admit`: `admit_structural_change` and
`check_and_admit_population_plan` call it directly. Neither one's ledger bytes
moved from that routing.

**The brief's escape clause describes a case the code forbids, and the door is
wider than the brief expected.** The brief said "`admit` on a history whose
policy requires no check keeps working". Measured: `PolicyProgram.from_bytes`
refuses an empty `required_checks` with "required checks must be nonempty and
unique" (`machine.py:626`), so no such history can exist. And terminal
acceptance of a change set requires the history binding's decision event, which
is `VERDICT_RECORDED` in every binding in this repository, so refusing it
closes the public admission surface completely rather than only under a policy
that requires a check. That is what D asked for ("so the public door can close
for everyone"), and it is what was built, but it should be stated as the fact
it is: after this change `admit` and `admit_with_anchors` cannot admit
anything, for anyone, under any shipped binding.

`append_protocol_events` was checked and is not a second door: it wraps every
event as `FINITE_PROTOCOL_EVENT`, which the fold routes to the protocol runtime
and never to the machine's proposal and decision handling, so it cannot accept
a change set.

### The fold

`src/malleus/profiles/structural-admission-check.json` is now a
`malleus.check-contract/v1` `CORE_BUILTIN` document naming
`malleus.core.operations-apply-atomically` version `1`.
`structural-admission-policy.json` follows it.

| artifact | before | after |
|---|---|---|
| structural check contract | `sha256:9901f512…` | `sha256:b923c279…` |
| structural admission policy | `sha256:012de44e…` | `sha256:c1d696f2…` |
| structural normative profile | `sha256:aca27bbf…` | `sha256:a39681c4…` |
| structural history bundle | `sha256:0ef377d9…` | `sha256:8a994ed0…` |

The new check identity is exactly the value step 1 measured and published as
the cost of the fold.

`_load_structural_history_bundle` parses the document through
`parse_check_contract` and derives the accepting outcome rather than reading a
`success_outcome` field: it is the one declared outcome the installed policy
maps to the binding's accept verdict, and the loader refuses unless there is
exactly one.

One declared thing was lost and it is worth naming. The v1 grammar closes its
fields to four, so the old document's `checks` list
(`EXACT_BASE_COORDINATES`, `RETAINED_SOURCE_AND_EVIDENCE_CLOSURE`,
`STRUCTURAL_APPLICATION`) and its `non_claims` list (`DOMAIN_ADEQUACY`,
`EPISTEMIC_CORRECTNESS`, `SOURCE_TRUTH`) are gone from the artifact. The same
statement still stands in `StructuralHistoryBundle`'s own docstring and in
`docs/PRINCIPLES.md`. Nothing read those two lists.

`admit_structural_change` is unchanged in behaviour and still writes its own
`CHECK_RECORDED` from the bundle without invoking the builtin the folded
contract now names. What that record attests, "the operations apply
atomically", is exactly what `_admit` validates when it applies the change, so
the attestation is not fabricated; but it is Core attesting its own primitive
rather than Core running the executor the contract declares. Routing it through
`check_and_admit_change_set` would close that gap and would move every
structural history's ledger bytes a second time. It was out of the brief's
scope ("`admit_structural_change` unchanged") and is left as a named residual.

## What did not land, and exactly where the line is

Rewritten 2026-09-20 by the agent that carried the migration, at commit
`980cb609`, and rewritten again the same day by the agent that finished the
nine research programs. "Measured at `980cb609`" and "Measurements" below are
the two earlier measurements of the red branch and are kept as the record of
those states.

### What landed since

**Core's own tests admit through the door.** Every caller-authored admission
under `tests/contract_compiler/pareto` now calls
`check_and_admit_change_set`, or `prepare_population_change` followed by it
where the test's subject is the preparation surface. The fixture policy at
`test_protocol_machine.py` requires two retained
`malleus.check-contract/v1` `CORE_BUILTIN` documents, both naming
`malleus.core.operations-apply-atomically` version `1`, built by
`_check_contract_document` and retained by `_check_contract_anchors`. The
identities that moved with it:

| artifact | before | after |
|---|---|---|
| fixture check contract a | `sha256:aaa…` (no document) | `sha256:b8d7db85…` |
| fixture check contract b | `sha256:bbb…` (no document) | `sha256:448fc87f…` |
| fixture policy | `sha256:2d31a2fc…` | `sha256:ca7a4b54…` |
| fixture partial contract, inspection-note | `sha256:0a9a02ce…` | `sha256:3a216cda…` |

**The door reads its event types from the machine program.** `knowledge.py`
named `CHECK_RECORDED` and `VERDICT_RECORDED` as literals, which
`test_history_binding_is_canonical_and_data_owns_machine_vocabulary` forbids:
the data owns that vocabulary. `_core_authored_events` now reads the installed
program for the events whose instructions carry `REQUIRE_POLICY_CHECK_OUTPUT`
or `SELECT_POLICY_VERDICT`.

**`_check_base` refuses instead of crashing.** Forming the base for a
retirement that a live relation still names raised a bare `ValueError` out of
`KnowledgeGraph.from_records`, before any executor ran. It now refuses at
`CHECK` with `STRUCTURAL_REFUSAL` and the application's own words.

**Two conformance re-baselines, both additive.**
`research/.../fixtures/inspection_note_execution_v4` is a new document
execution; v2 and v3 are untouched and both are now digest-pinned by
`test_previous_execution_remains_exact`. The historical inputs in
`inspection_note_capture_v1` are untouched, which is why the two tests that
compare the adapter output against the committed plan now compare modulo
`contract_identity`, with the reason stated at the assertion.

**RET-010 is migrated and its exported graph is byte-identical.**
`pareto/policy.json` requires one check, `structural-conformance`, whose
document is the new `pareto/checks/structural-conformance.json` at
`sha256:4cef2ab7e63c87ff3b3290026b6c0b1335b01cea18e30b353adfaf6ce52b8bd9`.
`retained-source-integrity` is gone: its identity matched no file and the
program wrote `SATISFIED` from a literal in `mapping.json`. `ret010.py` lost
its 71-line `_protocol_events` and calls `check_and_admit_change_set`.

| artifact | before | after |
|---|---|---|
| pareto policy | `sha256:c0ec653f…` | `sha256:433f2f9b…` |
| pareto mapping | `sha256:4e8851c5…` | `sha256:ba4291a2…` |
| RET-010 exported graph | `b58f6447…` | `b58f6447…`, identical |
| RET-010 accepted state digest | `sha256:4d7d44cc…` | `sha256:4d7d44cc…`, identical |

### What landed on 2026-09-20, after `f52863c0`

**Every research program that wrote its own check outcome is migrated.** Nine
programs were touched. Six of them held the door open; three only pinned a
value that moved.

| program | before | after |
|---|---|---|
| `public_population/run.py` | `admit` with a hand-written `_protocol_events` | `check_and_admit_change_set` |
| `object_event/run.py` | imported that `_protocol_events` | `check_and_admit_change_set` |
| `content_rules/run.py` | `admit_with_anchors`, own `PrologVerifier` call | `check_and_admit_population_plan` |
| `shipment_policy/run.py` | `admit_with_anchors`, own `PrologVerifier` call | `check_and_admit_population_plan` |
| `showcase/run.py` | `admit_with_anchors`, own private-grammar check | `check_and_admit_change_set` with its recompute as an anchor |
| `correction/run.py` | `admit_with_anchors`, two private-grammar checks | `check_and_admit_change_set` with its recompute as an anchor |
| `default_admission/run.py` | `admit_structural_change`, unchanged | plans re-cut |
| `partial_shipments/run.py` | `admit_structural_change`, unchanged | plans re-cut |
| `fresh_import/run.py` | `admit_structural_change`, unchanged | plans re-cut |

`_protocol_events` is gone from `public_population`, `correction` and
`showcase`. No research program writes `CHANGE_PROPOSED`, `CHECK_RECORDED` or
`VERDICT_RECORDED` any more, and none states an outcome.

**Three check contracts were removed, and the reason is the same for all
three: their executor was the adopter's own program, or nothing at all.**

- `retained-source-integrity` at `sha256:8208a293…` matched no file in the
  repository. The pareto programs wrote `SATISFIED` for it from a literal.
  Recorded in `public_population/README.md`, as the brief directed.
- `source-mapping-conformance` at `sha256:d98a2616…` (correction) and
  `sha256:ad5de0ee…` (showcase) named the run program as its executor.
- `structural-conformance` at `sha256:47e59912…` (correction) named it over
  Core's own primitive.

Every migrated policy now requires one contract,
`sha256:4cef2ab7e63c87ff3b3290026b6c0b1335b01cea18e30b353adfaf6ce52b8bd9`, the
`malleus.check-contract/v1` `CORE_BUILTIN` document naming
`malleus.core.operations-apply-atomically` version `1`, except
`content_rules` and `shipment_policy`, which keep their retained Prolog
contracts and resolve as `PROLOG_RULES` through the descriptor and rules pair
they already retain.

**The two experiment-specific verifications were kept, as research-local
evidence.** `correction`'s source-mapping conformance and `showcase`'s
recompute-declared-source both still run, before admission, and both still
retain their result in the same batch as the change. They are declared under
`malleus.small-shop.source-mapping-declaration/private-v0`, which still pins
the exact entrypoint bytes, and their records under
`malleus.small-shop.source-mapping-verification/private-v0`. Each program's
module docstring states in full that Core does not vouch for them.
`correction/_validate_replay` verifies more than before, not less: it
recomputes the source mapping from ledger bytes as it always did, and it now
also recomputes the `result_state_digest` in Core's own structural receipt
rather than trusting the stored value.

**One adopter machine had to change, and it is worth naming.**
`correction/machine.json`, which `correction`, `showcase` and
`shipment_policy` all select, declared on `CHECK_RECORDED`:

```json
{"event_field": "receipt_identity", "opcode": "REQUIRE_REFERENCED_RECORD",
 "record_type": "ArtifactRecord", "refusal": "UNKNOWN_REFERENCE"}
```

That held only because each program anchored its receipt under the receipt's
own digest as the artifact id. Core names a receipt
`receipt:<change-set-id>:<check-contract-id>` and puts the digest in
`receipt_identity`, so the reference resolved to nothing and every admission
refused `UNKNOWN_REFERENCE`. The instruction is removed; the field stays. What
it encoded is now Core's own invariant: `_admit_checked` appends the receipt in
the same batch as the change, unconditionally. `sha256:825c8d99…` to
`sha256:66913e1e…`.

**Every exported graph is byte-identical.** Measured against the committed
`evidence_2026_09_17_policy_rebinding` generation, which is the byte comparison
`assert_current_evidence` performs:

| program | exported graph | result |
|---|---|---|
| RET-010 | `b58f6447…` | identical (measured at `980cb609`) |
| public population | `/graph` and `graph_state_digest` in `evidence.json` | identical, 0 differing paths under `/graph` |
| correction | `graph.json` | identical, 0 changed paths |
| showcase | `graph.json` | identical, 0 changed paths |
| content rules | `graph` in the run report | identical to the connected story's own `export_records()` |
| shipment policy | `shipments` view and `query_relations` | identical |

**A successor evidence generation was cut**:
`evidence_2026_09_20_core_runs_checks`, with `evidence_assertions.CURRENT`
retargeted to it and all four preceding generations pinned, forty outputs where
the previous binding pinned thirty. Its `README.md` carries the whole
transition. Two kinds of non-digest change had to be declared in `binding.json`
because the successor guard refused them, and refusing them was right until
they were stated:

- ledger event counts, which move because Core retains one receipt per check:
  public population 48 to 49, object event 14 to 15, showcase 74 to 80, and
  correction 58 to 55, which falls because two check records and two receipts
  per change became one of each plus its own verification record;
- one field name and one list length: `showcase/explanation.json` renames
  `source_mapping_receipts` to `source_mapping_verifications`, and
  `correction/explanation.json`'s `/checks` goes from six entries to three.

`test_current_evidence`'s successor guard reads `changed_values` and
`changed_keys` for those and still refuses any undeclared non-digest change,
any undeclared key set and any undeclared list length.

**Identities that moved**, old to new, beyond the three above:

| artifact | before | after |
|---|---|---|
| base partial contract, public population | `sha256:ed170fd1…` | `sha256:c8133173…` |
| target partial contract, public population | `sha256:0e1f03bc…` | `sha256:1bbd6aa1…` |
| object-event partial contract | `sha256:90c8bc3e…` | `sha256:d4ce6354…` |
| object-event fixture manifest entry | `sha256:fad3a9c6…` | `sha256:c36e4a93…` |
| correction policy | `sha256:57972777…` | `sha256:724f1670…` |
| correction run program | `sha256:414db35b…` | `sha256:2554fbd5…` |
| showcase policy | `sha256:efa0ac20…` | `sha256:c72450aa…` |
| showcase run program | `sha256:7096c3f8…` | `sha256:bc630676…` |
| showcase partial contract | `sha256:0c43eac9…` | `sha256:2c2b49ad…` |

Every plan under `public_population/plans/` was re-cut for the two partial
contracts, and `ret010.json` for the moved `pareto/mapping.json` evidence
digest. `fixtures/small_shop_fulfilment_object_event_v1/input/population/ret-040.json`
and its manifest were re-cut for the object-event contract. The stage
declarations in `correction/run.json` and `showcase/run.json` lost
`proposal_id`, `decision_id` and `receipt_id` (`receipt_id_prefix` in
correction): Core names the proposal, the decision and every receipt.

**Frozen evidence that was not touched, and why.** The `HISTORICAL` table in
`test_evidence_archive.py` decides. `correction/evidence-role-v1/*`,
`object_event/evidence.json`, `showcase/evidence/*` and every dated archive
(`evidence_2026_09_06`, `evidence_2026_09_08`,
`evidence_2026_09_08_rule_check`, `evidence_2026_09_17_policy_rebinding`) are
frozen history and were left byte-identical, including the six that pin the
superseded `pareto/mapping.json` digest `sha256:4e8851c5…`. So are
`public_population/evidence.json` and `fresh_import/evidence.json`, which the
binding pins as historical outputs in their own right. The only regenerated
outputs are the five scenarios of the new generation.

### Where the line is now

Measured on this tree, with `PYTHONPATH=$PWD/src:$PWD` exported for every
command, which is still the trap that decides whether a subprocess measures
this branch or main.

**Green.**

- `pytest tests/contract_compiler`: **1302 passed, 0 failed**, 540s. Zero
  governance digest guards among them: the governance validator lives in
  `tests/test_contract_compiler_integration.py`, `test_contract_compiler_ledger.py`
  and `test_docs.py`, outside this path, and those 24 failures are the allowed
  residue that sealing `OVR-000472` clears.
- `pytest research/methodology_gedanken_e2e/tests`: **31 passed**.
- `pytest research/.../small_shop/object_event`: **3 passed**.
- `pytest research/.../small_shop`, excluding `connected_story`: every program
  green. The whole path reads 5 failed, 335 passed, 22 errors, and every one
  of the 27 is in `connected_story`, below.
- **The door probe reads four sites, all of them Core's own tests of the
  door.** The probe wraps `KnowledgeChangeHistory.admit` and
  `admit_with_anchors`, and records every call that carries a `CHECK_RECORDED`
  or `VERDICT_RECORDED` event while the history's selected policy requires at
  least one check contract. Run over `tests/contract_compiler`,
  `research/.../small_shop` and `research/methodology_gedanken_e2e`, it names
  exactly these, and no research program:

  1. `tests/contract_compiler/pareto/test_atomic_population_admission.py::test_a_fabricated_check_outcome_can_no_longer_reach_the_ledger`
     (`checks=1 prolog=True via=admit events=CHECK_RECORDED,VERDICT_RECORDED`)
  2. `tests/contract_compiler/pareto/test_atomic_population_admission.py::test_the_public_door_refuses_a_caller_written_verdict_record`
     (`checks=1 prolog=True via=admit events=VERDICT_RECORDED`)
  3. `tests/contract_compiler/pareto/test_knowledge_change_history.py::test_refused_change_never_changes_ledger_or_replayed_graph[rejected]`
     (`checks=2 prolog=False via=admit events=CHECK_RECORDED,VERDICT_RECORDED`)
  4. `tests/contract_compiler/pareto/test_knowledge_change_history.py::test_refused_change_never_changes_ledger_or_replayed_graph[unregistered]`
     (`checks=2 prolog=False via=admit events=CHECK_RECORDED,VERDICT_RECORDED`)

  All four are tests that assert the door refuses. The probed run reports one
  failure not present without it,
  `test_no_public_callable_accepts_a_caller_check_outcome_under_a_policy`: that
  test reads `inspect.signature` of every public method for a `machine_events`
  parameter, and the probe's `(self, *args, **kwargs)` wrapper hides it. The
  test passes on this tree unprobed. It is an artefact of the instrument, not a
  finding.

**Not green, and not this step's work.**

1. **The connected-story re-freeze** (brief step 7, and the previous list's
   item 4). Not started, deliberately: its chain ends in Appendix B, which is
   `paper-v4/` and off limits to this agent. It is the whole of what is red in
   `research/.../small_shop`: 22 errors at fixture setup in
   `connected_story/warehouse/` (12) and `connected_story/partial_shipments/`
   (10), and 5 failures in `connected_story/test_connected_run.py` (1),
   `test_object_timelines.py` (2), `test_shipment_explanation.py` (1) and
   `content_rules/test_content_rules.py` (1, the control that reproduces the
   frozen connected receipt). The cause is one identity: the structural fold
   at `7c3237f0` moved `STRUCTURAL_HISTORY_BUNDLE`, so the story's partial
   contract moved and its ledger with it. Measured:
   `connected_story/run_receipt.json` pins `ledger_sha256: sha256:1c989c55…`
   and a fresh run produces `sha256:dcd140c5…`. Files to re-cut, in order:
   `connected_story/run_receipt.json`, `timeline_receipt.json`,
   `shipment_explanation_receipt.json`, then the four the ledger at E-0467
   names, `connected_story/partial_shipments/input_boundary.json`,
   `connected_story/warehouse/receipt.json`,
   `connected_story/warehouse/ordering_receipt.json`,
   `connected_story/partial_shipments/receipt.json`. Appendix B's
   `32798a67…` and `15c7c1ef…` move with them.
2. **`document_paper/document_run.py:280` is still a caller-authored
   admission, and nothing in the repository exercises it.** This is not a
   regression and it is not the door: `research/.../document_paper` reads
   **7 failed, 150 passed, 7 errors** at `85f0ed54`, at `f52863c0` and on this
   tree, the same three numbers, and the cause is a stale fixture. Its
   `_history_binding` at `test_graph_recipe_change_set.py:177` declares
   `malleus.knowledge-history-binding/private-v0` where Core requires
   `private-v1`, so every test that needs a history errors at setup before
   reaching any admission. The path is not in `testpaths`. Migrating
   `document_run.py` without first repairing that fixture would be a change
   nothing can measure, so it was not made.
3. **The read-only Appendix B run** (`paper-v4/test_shop_connected_calibration.py`,
   `paper-v4/test_shop_calibration.py`). Not re-run here. Its 14 errors at
   `f52863c0` were the connected-story chain of item 1, and the one
   `test_shop_calibration.py` failure was `shipment_policy` hitting the closed
   door, which is now migrated. Expect the second to pass and the first to
   stay red until item 1 lands.
4. **The full default suite.** Not re-run here; `tests/contract_compiler` was
   measured alone, and it is 1302 of the roughly 3658 the whole suite collects.
5. **The four documents.** Untouched, as the brief directed. The exact places
   are unchanged: `.claude/skills/malleus-dev/references/CAPABILITIES.md` lines
   39, 40 and 51 plus a new row for `check_and_admit_change_set` and
   `ChangeSetAdmission`; `docs/contract_compiler/index.md` line 455, "What this
   does not do."; `docs/IMPLEMENTATION_STATUS.md` line 255; `CHANGELOG.md`
   Unreleased; and the skill's "What was built for F1" residual sentence,
   which the Overlord batches into the seal per E-0504.
6. **`OVR-000472`.** Not drafted. `previous_entry_hash` is
   `sha256:7cb9e624476d13a78ed15a5d5d89f219414cb536f3738eda7a91a94f1de984fd`.
7. **`admit_structural_change` still writes its own `CHECK_RECORDED`** from the
   folded bundle without invoking the builtin its contract names. Unchanged
   from the earlier record, still a named residual, and it is what
   `default_admission`, `partial_shipments` and `fresh_import` admit through.

### Measured at `980cb609`

`PYTHONPATH=$PWD/src:$PWD pytest tests/contract_compiler`: **20 failed, 1282
passed**, 142s. Every one of the 20 is downstream of an unmigrated research
program, in four files: `test_default_shop_walkthrough.py` (1),
`test_fresh_shop_import.py` (10), `test_maintained_projection.py` (2),
`test_partial_shipments.py` (3), `test_small_shop_default_admission.py` (4).
The two distinct causes are
`IDENTITY_MISMATCH: evidence digest differs from retained bytes:
artifact:small-shop:baseline-mapping` and a non-zero exit from a research
program run as a subprocess. No test in `tests/contract_compiler/pareto` fails
for the door any more.

`pytest research/.../small_shop/pareto`: **28 passed**.
`pytest research/.../small_shop/{object_event,public_population}`: **4 failed,
2 passed**, all four `PopulationPlanRefusal: IDENTITY_MISMATCH: plan and
partial effective contract disagree`.

Ruff over `src tests research/.../small_shop/pareto`: the same nine
pre-existing findings as `85f0ed54`, plus none.

The E-0501 probe, over `tests/contract_compiler`,
`research/.../experiments/small_shop` and `research/methodology_gedanken_e2e`:
**19 caller-authored admissions, down from 134**. Fifteen are the unmigrated
programs, in `correction/test_correction_vertical.py` (9),
`shipment_policy/test_shipment_policy.py` (4) and
`content_rules/test_content_rules.py` (2). The other four are Core's, and all
four are tests whose subject is the door refusing:
`test_atomic_population_admission.py::test_a_fabricated_check_outcome_can_no_longer_reach_the_ledger`,
`::test_the_public_door_refuses_a_caller_written_verdict_record`, and
`test_knowledge_change_history.py::test_refused_change_never_changes_ledger_or_replayed_graph`
at `[rejected]` and `[unregistered]`. The probe counts the call, not the
outcome, so a zero reading would mean the door had no test at all. Read it as
four expected and fifteen to go.

One probe artifact, so the next reader does not chase it:
`test_no_public_callable_accepts_a_caller_check_outcome_under_a_policy` fails
under the probe and passes without it. It reads `inspect.getsource` of
`admit`, and the probe has replaced it with its own wrapper.

### The earlier agent's list, kept as the record of what it found

Superseded by "Where the line is now" above. Its items 1, 2 and 3 all landed;
its items 4 and 5 are items 1, 5 and 6 there.

Parts 4 through 9 of the brief. In order of what the next agent should do:

1. **Core's own test admissions** (brief step 4). 134 caller-authored
   admissions in 18 files at this commit, by the E-0501 probe as re-measured
   at 9717f050 and confirmed unchanged by E-0503. They reach the door through
   36 call sites, and most of those sit in shared helpers, so the work is
   smaller than the test count suggests. The helpers, by file and line at
   `85f0ed54`:
   - `test_knowledge_change_history.py:501` `_admit_record_change`, plus 15
     direct sites in the same file
   - `test_check_contract_rebinding.py:244` `_admit_new_class`
   - `test_small_shop_contract_revision.py:99` `_admit_ret010`, which
     `test_check_contract_rebinding.py` imports
   - `test_public_compiler.py:229` `_prepare_and_admit`
   - `test_transition_admission.py:123` `admit`
   - `test_governed_population.py` six direct sites
   - `test_population_plan.py:265` and `:1790`
   - `test_change_composition_context.py:193` and `:220`
   - `test_contract_revision.py:207`, `test_small_shop_contract_revision.py:114`,
     `test_population_trace.py:252`, `test_object_event_population.py:291`,
     `test_finite_protocol_history.py:346`
   The fixture policy is `tests/contract_compiler/pareto/test_protocol_machine.py:38`
   `CHECKS`, whose two identities are the fictional `sha256:aaa…` and
   `sha256:bbb…`. Replacing them with two real `CORE_BUILTIN` v1 documents,
   anchored by `_anchored_history`, moves the fixture policy identity, the
   normative profile identity and the partial effective contract identity, and
   with them every frozen coordinate in those files. `test_protocol_machine.py`
   also carries a self-inspecting literal test at line 965 whose
   `fixture_literals` set names `check-contract-a` and `check-contract-b`.
   Note one consequence: histories whose required check is the Prolog rule
   layer (`test_check_contract_rebinding.py` and its dependants) will really
   run `PrologVerifier` once migrated, so those tests acquire the `swipl`
   skip mark that the atomic module already uses.
2. **The two remaining RED tests** the brief names.
   `test_knowledge_change_history.py::test_refused_change_never_changes_ledger_or_replayed_graph[rejected]`
   supplies a caller-authored `VIOLATED` outcome, and
   `test_transition_admission.py::test_low_level_admission_refuses_event_replacement_despite_satisfied_checks`
   supplies satisfied ones. Through the new entry point the outcome is the
   executor's, so the `[rejected]` case is expressed as a change the structural
   builtin cannot apply, which refuses at `CHECK` with
   `CONTENT_RULE_VIOLATED` carrying the underlying refusal name in its detail.
   The other two RED tests are already rewritten, in
   `test_atomic_population_admission.py`.
3. **The research programs** (brief step 5). The brief said twelve; the grep it
   gives returns nine files, and one of those,
   `research/action_history_contract_freeze/programs/sequential_fixture.py`,
   does not call `KnowledgeChangeHistory.admit` at all: both of its `.admit(`
   matches are module-level helpers that call `append_protocol_events`. Its
   real exposure is transitive, through
   `public_population/run.py:328`. So there are **eight** programs to migrate:

   | program | call site | policy | checks | does it run a check? |
   |---|---|---|---|---|
   | `document_paper/document_run.py` | `admit` :280 | in memory, no file | 2, grammar `malleus.paper-v4.check-contract/v1` | yes, in `experiment_run.py` |
   | `small_shop/content_rules/run.py` | `admit_with_anchors` :321 | `content_rules/policy.json` | 1, a real `LogicContract` | yes, `PrologVerifier` :276 |
   | `small_shop/correction/run.py` | `admit_with_anchors` :1477 (x3 stages) | `correction/policy.json` | 2, `malleus.check-contract/private-v0` | yes, `_verify_source_mapping` and `_apply_change` |
   | `small_shop/object_event/run.py` | `admit` :164 | `pareto/policy.json` | 2, no contract file exists | **no** |
   | `small_shop/pareto/ret010.py` | `admit` :1436 | `pareto/policy.json` | 2, no contract file exists | **no** |
   | `small_shop/public_population/run.py` | `admit` :328 (x5 plans) | `pareto/policy.json` | 2, no contract file exists | **no** |
   | `small_shop/shipment_policy/run.py` | `admit_with_anchors` :269 | `shipment_policy/policy.json` | 1, a real `LogicContract` | yes, `PrologVerifier` :221 |
   | `small_shop/showcase/run.py` | `admit_with_anchors` :1340 (x5 stages) | `showcase/policy.json` | 1, `malleus.check-contract/private-v0` | yes, `verify_stage` |

   The three that run no check write `outcome="SATISFIED"` as a literal, two
   of them in code and `ret010` from a string in `pareto/mapping.json`. Their
   policy names two check contracts that exist nowhere:
   `retained-source-integrity` at `sha256:8208a293…` and the pareto
   `structural-conformance` at `sha256:6a0c7419…` match no file in the
   repository. Both go, replaced by one v1 `CORE_BUILTIN` contract, and the
   removal of `retained-source-integrity` is recorded in
   `public_population/README.md` as the brief directs.

   The frozen evidence to re-baseline, found and not yet touched: the current
   generation `small_shop/evidence_2026_09_17_policy_rebinding/binding.json`
   and its `historical_outputs`, `small_shop/test_evidence_archive.py`'s
   `HISTORICAL` table, the literal digest tables in
   `pareto/test_vertical.py` (`FROZEN_SHA256`, the research receipt digest at
   line 341), `correction/test_fixture.py`, `showcase/test_settlement_fixture.py`
   and `showcase/test_run.py:578`, and `correction/evidence*/`,
   `showcase/evidence*/`, `object_event/evidence.json`,
   `public_population/evidence.json`.
4. **The connected story chain moves from the fold alone.** The fold changes
   the structural policy identity, which is inside the partial effective
   contract every structural change set binds, so every structural history's
   bytes move.
   `connected_story/partial_shipments/input_boundary.json` pins
   `baseline_history_sha256: sha256:32798a67…` and will refuse with
   "Synthetic extension requires the exact warehouse history", which is the
   same failure mode E-0466 and E-0467 recorded when the revision policy
   identity moved. The Core-side re-freeze is four files and twelve values,
   named in the ledger at E-0467: `input_boundary.json`,
   `warehouse/receipt.json`, `warehouse/ordering_receipt.json`,
   `partial_shipments/receipt.json`. Appendix B's two digests, `32798a67…`
   and `15c7c1ef…`, move with it and are the paper agent's to re-cut.
5. **Documentation and the overseer entry** (brief steps 8 and 9). Not
   started. No `OVR-000472` was drafted, deliberately: an entry records the
   after-digest of every governed document it covers, and the documents this
   work will change have not been written. Drafting one now would mean
   recording digests of bytes that do not exist. The entry's
   `previous_entry_hash` is
   `sha256:7cb9e624476d13a78ed15a5d5d89f219414cb536f3738eda7a91a94f1de984fd`
   (OVR-000471).

   The exact places that state the open door and must be corrected:
   - `.claude/skills/malleus-dev/references/CAPABILITIES.md` line 40, the
     one-call row, whose last sentence still says a structural history "keeps
     `admit_structural_change`" and which says nothing about the door; line 39,
     the governed-history row; line 51, the re-binding row. A new row is needed
     for `check_and_admit_change_set` and `ChangeSetAdmission`.
   - `docs/contract_compiler/index.md`, the paragraph beginning "What this does
     not do." at line 455, which states that `admit` and `admit_with_anchors`
     remain public and read a caller-supplied outcome, and the sentence after
     it about `structural-admission-check.json` staying in its private grammar.
     Both are now false.
   - `docs/IMPLEMENTATION_STATUS.md` line 255, the same claim in the same
     words.
   - `CHANGELOG.md`, Unreleased.
   - `.claude/skills/malleus-dev/SKILL.md`, "Rules and the ontology", whose
     paragraph "What was built for F1" ends on the residual that the two-step
     door is still open. The Overlord batches the skill's sentences into the
     seal, per E-0504.

## Measurements

Clean worktree at `85f0ed54`, before any edit, full default suite:
**3640 passed, 3 skipped, 0 failed**, 17m09s. That matches the derived figure
in the step-1 handover exactly (3624 at `9717f050` plus the 16 new executor
tests). The checkout's larger number is the five gitignored Assent-path test
modules, as E-0501's addendum records.

RED for the third entry point, measured rather than asserted: the new module
run against a `git archive` of `85f0ed54`'s `src` on `PYTHONPATH`, with the
test tree beside it. **15 failed, 1 passed.** The one that passes is
`test_the_builtin_contract_bytes_are_the_ones_this_module_pins`, which pins the
fixture contract and never touches the entry point. GREEN on this tree: 16
passed, with the 18 atomic and 16 executor tests still green.

Full default suite on this tree, after the door and the fold:
**133 failed, 3515 passed, 3 skipped, 10 errors**, 13m38s. The arithmetic
closes: 3515 plus 133 plus 10 is 3658, and 3658 plus 3 skipped is 3661, which
is the clean 3643 plus the 18 tests added here (16 in
`test_change_set_admission.py`, and `test_atomic_population_admission.py` going
from 18 to 20).

The 133 failures and 10 errors, by file and by cause. The suite run was taken
with `-rf`, so the errors were not itemised in its summary; they were placed
afterwards by re-running the module with `-rE`, which reports
`3 passed, 10 errors in 228.99s`.

| count | file | cause |
|---|---|---|
| 14 | `tests/test_contract_compiler_integration.py` | governance digest guard |
| 7 | `tests/test_contract_compiler_ledger.py` | governance digest guard |
| 3 | `tests/test_docs.py` | governance digest guard, through the strict Sphinx build |
| 27 | `test_knowledge_change_history.py` | migration not done |
| 21 | `test_population_plan.py` | migration not done |
| 19 | `test_transition_admission.py` | migration not done |
| 15 | `test_check_contract_rebinding.py` | migration not done |
| 7 | `test_governed_population.py` | migration not done |
| 4 | `test_population_trace.py` | migration not done |
| 2 | `test_change_composition_context.py` | migration not done |
| 2 | `research/.../public_population/test_run.py` | migration not done |
| 10 errors | `test_maintained_projection.py` | migration not done, at setup |
| 1 each | `test_atomic_population_admission.py`, `test_contract_revision.py`, `test_finite_protocol_history.py`, `test_object_event_population.py`, `test_public_compiler.py`, `test_review_coverage.py`, `test_small_shop_contract_revision.py` | migration not done |
| 1 each | `test_default_shop_walkthrough.py`, `test_document_assertion_time.py`, `test_document_fixture_producer.py`, `test_fresh_shop_import.py`, `test_partial_shipments.py` | the fold: a frozen identity moved |

The 24 governance failures have one cause and one reported path:
`OVR-000464: latest document digest mismatch for
src/malleus/_contract_pipeline/knowledge.py, expected sha256:15b3991f…, got
sha256:28d90605…`. The validator stops at the first mismatch, so
`admission.py`, `compiler.py` and the two profile documents are behind it and
will be reported in turn; all of them are governed documents this work
changed, and sealing `OVR-000472` clears the set. That is the allowed
governance residue and it is the only allowed one.

Every other failure is a consequence this branch created and has not yet
answered. The fold group is a frozen identity that moved, for example
`test_default_shop_walkthrough.py` asserting the structural bundle identity
`sha256:0ef377d9…` where the fold now produces `sha256:8a994ed0…`. The
migration group is the closed door refusing a caller-written check record. The
ten errors are that same refusal one level up: every test in
`test_maintained_projection.py` that takes the `sequence` fixture errors at
setup, because the fixture calls `_admit_record_change`, the shared helper it
imports from `test_knowledge_change_history.py`. The message is
`CALLER_SUPPLIED_CHECK_EVENT: CHECK_RECORDED is Core's to write once it has run
the check`, raised at `knowledge.py:889`. The module's other three tests pass.
Migrating that one helper clears all ten.

Ruff over `src tests`: the same nine pre-existing findings as `85f0ed54`
(`tests/test_kg.py` E401 twice, `tests/test_logic.py` F401 twice,
`tests/test_prolog_verifier.py` E402 five times), none in any changed file.

Appendix B, run read-only on this tree and not edited.
`paper-v4/test_shop_connected_calibration.py`: **14 errors, one cause**, all at
setup of the module-scoped `chain` fixture. The connected story's warehouse
stage refuses `ValueError: Warehouse extension requires the exact Table 1
baseline` at `connected_story/warehouse/run.py:155`. That is the fold: the
structural policy identity is inside the partial effective contract every
structural change set binds, so the Table 1 history's bytes moved and no
longer reproduce the frozen boundary the warehouse stage requires. The chain
cannot be rebuilt on this tree, so the two Appendix B digests have a before
and no after: before `32798a67f4b2d5b6fab2de102ae6c4b41087f04ae794547517497232256ac333`
and `15c7c1eff28ff59496fd937de19181f649e9c8c9c4c1e895cf56252f434bd204`, after
not computable until the connected-story re-freeze of item 4 lands. This is
the same shape of failure as E-0466 and E-0467, one identity further down.

`paper-v4/test_shop_calibration.py`: **1 failed, 1 passed**. The failure is
`test_shipment_policy_figures_and_refusal_match_a_fresh_run`, and the cause is
not the test. It runs `small_shop/shipment_policy/run.py` as a subprocess, and
that unmigrated consumer hits the closed door at its own line 277:
`ShipmentPolicyRefusal: Shop policy SATISFIED: CALLER_SUPPLIED_CHECK_EVENT`.
Neither calibration test uses the closed door itself; both fail through
research programs that do. Neither was edited.

No test in the default suite exercises
`paper-v4/experiment-v4/content-rules-doc-01/run_policy.py` or
`content-rules-doc-02/admit.py`. `paper-v4` is not in `testpaths`, and the only
reference to either path under `tests/` or `research/` is one docstring line in
`test_atomic_population_admission.py`.

The caller-authored admission count was not re-measured here. The E-0501
counting probe needs its module on `PYTHONPATH`, which the first attempt
missed, and a second full-suite run for a number that is not yet zero would
have bought nothing: the migration has not started, so the count stands where
E-0503 left it, 134 caller-authored admissions in 18 files, measured on the
content this commit carries. What is different is that all 134 now refuse
rather than admit, which is what the 109 non-governance failures and the 10
errors above are.

## Commits

- `7c6e3f62` the third entry point and its 16 tests, additive, door still open
- `7c3237f0` the door closed and the structural check folded, breaking
- `bc7fdcbb`, `f6d83c2c`, `ac0dfe50` this handover and its measurements
- `980cb609` Core's own tests admit through the door, and RET-010 with them
- `f52863c0` the door probe measured at 19
- `127c3f67` four research programs stop writing their own check outcomes
- `4a0d6340` the showcase stops presenting its own recompute as a check
- `7bef2db3` correction: Core runs the one check, the recompute stays research
- `934ef948` the successor Shop evidence generation for Core-run checks

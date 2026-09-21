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

### Where the line was after the migrations, 2026-09-20

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

**Not green at that point, and answered below.** Seven items were open: the
connected-story re-freeze, `document_paper/document_run.py`, the read-only
Appendix B run, the full default suite, the four documents, `OVR-000472`, and
`admit_structural_change` writing its own check record. Items 1, 3, 4, 5 and 6
landed in the final pass recorded in the next section. Item 2 stands as the
earlier agent left it: `document_paper/document_run.py:280` is still a
caller-authored admission and nothing in the repository exercises it, because
its `_history_binding` at `test_graph_recipe_change_set.py:177` declares
`malleus.knowledge-history-binding/private-v0` where Core requires `private-v1`,
so every test that needs a history errors at setup; `research/.../document_paper`
reads **7 failed, 150 passed, 7 errors** at `85f0ed54`, at `f52863c0` and here,
the same three numbers, and the path is not in `testpaths`. Item 7 stands too:
`admit_structural_change` still writes its own `CHECK_RECORDED` from the folded
bundle without invoking the builtin its contract names, and that is what
`default_admission`, `partial_shipments` and `fresh_import` admit through.

### Where the line is now, after the final Core pass

**The connected-story re-freeze landed.** The chain rebuilds from the Table 1
baseline. `warehouse/source_boundary.json` was the eighth file, beyond the seven
the previous list named: it carries the baseline gate `append_warehouse` reads,
and it had to move first or nothing downstream could run. 34 values across 8
files, in chain order:

| file | value | before | after |
|---|---|---|---|
| `connected_story/run_receipt.json` | `ledger_sha256` | `1c989c55…` | `dcd140c5…` |
| | `ledger_head` | `0f33125b…` | `9e0cff50…` |
| | `replay_receipt` | `78e211dd…` | `cf0fe19f…` |
| | `partial_contract` | `4dacf4d7…` | `9d3d4638…` |
| | `ledger_bytes` | 895257 | 895097 |
| `connected_story/timeline_receipt.json` | `history_sha256`, `history_head`, `history_receipt` | as above | as above |
| | `report_sha256` | `afc5072a…` | `4aa0b4e7…` |
| `connected_story/shipment_explanation_receipt.json` | `history_sha256`, `history_head`, `history_receipt` | as above | as above |
| | `reports[0].report_sha256` | `d6bb4fcf…` | `39f4bcf2…` |
| | `reports[1].report_sha256` | `bf9bb368…` | `4f40b25d…` |
| | `reports[2].report_sha256` | `458f7084…` | `9bd0c8f0…` |
| `connected_story/warehouse/source_boundary.json` | `baseline_history_sha256` | `1c989c55…` | `dcd140c5…` |
| `connected_story/warehouse/receipt.json` | `baseline_history_sha256` | `1c989c55…` | `dcd140c5…` |
| | `history_sha256` | `32798a67…` | `0f2cf039…` |
| | `history_head` | `72ffab71…` | `25d8eab4…` |
| | `replay_receipt` | `454c9cdb…` | `0de13200…` |
| | `contract_identity` | `b036955e…` | `c746b60f…` |
| | `report_sha256` | `f41d9ae1…` | `6290a5c9…` |
| | `history_bytes` | 1646996 | 1646836 |
| `connected_story/warehouse/ordering_receipt.json` | `binding.history_head` | `72ffab71…` | `25d8eab4…` |
| | `binding.replay_receipt` | `454c9cdb…` | `0de13200…` |
| | `report_sha256` | `1694c1b7…` | `6c1a1f28…` |
| `connected_story/partial_shipments/input_boundary.json` | `baseline_history_sha256` | `32798a67…` | `0f2cf039…` |
| | `baseline_history_bytes` | 1646996 | 1646836 |
| `connected_story/partial_shipments/receipt.json` | `baseline_history_sha256` | `32798a67…` | `0f2cf039…` |
| | `history_sha256` | `15c7c1ef…` | `09995500…` |
| | `history_head` | `0b042ba3…` | `e6491e4e…` |
| | `replay_receipt` | `0d47daff…` | `23fc1bb1…` |
| | `contract_identity` | `0673d839…` | `58fafe28…` |
| | `history_bytes` | 2306379 | 2306219 |

**One value did not move and was nearly re-cut by a wrong derivation.**
`run_receipt.json`'s `contract_facts` is `compile_shop().artifact.facts_sha256`,
the compiled ontology facts, not `replay.partial_contract.validated_fact_set_sha256`.
The two differ (`fb0c0903…` against `e82f3569…`), and the second was checked
against a `git archive` of `85f0ed54` before it was written, which is what
caught it. `history_profile` and `machine_program` did not move either.

**The exported graphs and every domain record are byte-identical**, measured by
running the whole chain on a `git archive` of `85f0ed54` and on this tree and
diffing the dumps. Identical at all three stages: `graph.export_records()`, the
complete `record_history`, the Table 1 account, the partial-shipments report.
The three graph state digests are unchanged, `4a890bb0…`, `e5f36981…` and
`57e3839c…`, and so are the three `graph_sha256` values in the shipment
explanation. The warehouse report and the timeline report differ in their
binding coordinates and in nothing else; every ordering count and witness is
equal. The archive run reproduced all three frozen ledger digests exactly,
which is what established the harness before any value was written.

**Appendix B, computed and not edited.** `paper-v4/` was not touched. Three
digests print there, not two: the Table 1 ledger also moves this time, because
the fold reaches one stage further up than the revision-policy move of E-0467.

| Appendix B value | before | after |
|---|---|---|
| Table 1 ledger | `1c989c554b9aa68e97226c0efc6355496723613f17e901bb7689a4c4da28acbe` | `dcd140c5f2456394cfa4c4ea70bf48c3d895dd42d803babed91664f4c01f9eb3` |
| warehouse ledger | `32798a67f4b2d5b6fab2de102ae6c4b41087f04ae794547517497232256ac333` | `0f2cf039b285185df7f8fc42c9647661ea79792806e1abdbb26a526ac818f56b` |
| synthetic ledger | `15c7c1eff28ff59496fd937de19181f649e9c8c9c4c1e895cf56252f434bd204` | `099955003f3274aea590edf1578520540033321cfb3cabcf9aa6b3dff36063bb` |

`paper-v4/test_shop_connected_calibration.py` and
`paper-v4/test_shop_calibration.py`, run read-only on this tree with the
measurement rule: **6 failed, 10 passed**, 130s. The chain fixture builds, so
the fourteen setup errors are gone. Every failure is a paper-side number, and
the paper agent needs all of them:
`test_ledger_digests_in_the_appendix_match_a_fresh_run` on the three digests
above; `test_table_1_stage_row_matches_a_fresh_run` on `bytes` 895257 to 895097;
`test_warehouse_stage_row_matches_a_fresh_run` on `baseline_bytes` 895257 to
895097 and `history_bytes` 1646996 to 1646836;
`test_shipment_stage_row_matches_a_fresh_run` on `baseline_bytes` 1646996 to
1646836; and both shipment-policy exhibit tests on `event_count` **32 to 31**,
which is not the re-freeze but the migration, because Core now writes one
receipt and one check record where the runner wrote its own pair. The two
calibration files were not edited.

**Suites, with `PYTHONPATH=$PWD/src:$PWD` exported for every command.**

- `research/.../small_shop`, the whole path: **362 passed**, 0 failed, 0 errors,
  678s. It was 5 failed, 335 passed, 22 errors.
- `research/.../small_shop/connected_story` plus `content_rules`: **130 passed**.
- `tests/contract_compiler`, `research/methodology_gedanken_e2e/tests` and
  `research/.../small_shop/object_event`: see the final measurement below.
- `tests/contract_compiler`, `research/methodology_gedanken_e2e/tests` and
  `research/.../small_shop/object_event` in one selection: **1336 passed**, 0
  failed, 529s.
- The full default suite, `pytest -q -p no:cacheprovider tests -rf`: **24
  failed, 3637 passed, 3 skipped**, 838s. Every one of the 24 is a governance
  digest guard, by path: `tests/test_contract_compiler_integration.py` 14,
  `tests/test_contract_compiler_ledger.py` 7, `tests/test_docs.py` 3, the last
  three through the strict Sphinx build, which runs the same validator. The
  validator stops at the first mismatch, so only one path is ever named; it now
  names `OVR-000460: latest document digest mismatch for tests/test_docs.py`.
- Ruff over `src tests research/.../small_shop scripts`: the same nine findings
  as `85f0ed54` and no more. The branch had acquired a tenth, `F841` on a dead
  `before = history.replay()` at `test_knowledge_change_history.py:1485` from
  the migration; it was removed.

**What remains after sealing, stated honestly.** Zero, now that the deletion has
a word. The governance digest mismatches clear when the chain is sealed, and the
deleted-document refusal, `OVR-000352: revised document does not exist`, is
answered by the two `REMOVED` records the chain carries. The scratch run below
validates all 475 entries against this tree, with the two deleted files absent,
which is the state the branch actually holds.

**The four documents are written.** `CHANGELOG.md` (the `check_and_admit_change_set`
entry under Added, the closed door and the fold under Changed, and the stale
sentence in the `check_and_admit_population_plan` entry corrected),
`docs/IMPLEMENTATION_STATUS.md`, `docs/contract_compiler/index.md` and
`.claude/skills/malleus-dev/references/CAPABILITIES.md`, which gains the
`check_and_admit_change_set` row and has its governed-history, one-call,
refusal, builtin-registry and re-binding rows corrected. Two research READMEs
owed a sentence and got it: `content_rules` and `shipment_policy` both said the
runner runs Prolog and submits the result, and Core does both now.
`public_population` already recorded the removal of `retained-source-integrity`;
`partial_shipments`, `default_admission` and `fresh_import` owed nothing, and
`showcase`, `correction`, `object_event` and `pareto` have no README.

**Three governed passages that lagged decision D now state what the code does**,
at commit `6214e2bc`. `.claude/skills/malleus-dev/SKILL.md`, "Rules and the
ontology", said the two-step path remains public and that Prolog is the only
admissible implementation because the contract names no engine; a check contract
does name its executor, `PROLOG_RULES` or `CORE_BUILTIN`, and the closed set is
the reason. The same file's "What was built for F1" said neither consumer is
migrated and the door is open. `ROADMAP.md` F1 carried the same residual. Each
claim was read against the code before it was rewritten: the executor kinds and
the builtin registry in `check_contract.py`, `CALLER_SUPPLIED_CHECK_EVENT` in
`knowledge.py`, `CHECK_CONTRACT_NOT_RETAINED` and `UNRUNNABLE_REQUIRED_CHECK` in
`check_contract.py`, the empty-policy message at `machine.py:627`, and all three
still-two-step paths, which still call `admit` or `admit_with_anchors` with
caller-built events.

**Finding (a), the deleted documents, is answered by a grammar change.**

1. **The branch deletes two governed documents and the overseer ledger had no
   vocabulary for that.** `correction/checks/source-mapping-conformance.json`
   (recorded by OVR-000352, deleted at `7bef2db3`) and
   `showcase/checks/source-mapping-conformance.json` (recorded by OVR-000359,
   deleted at `4a0d6340`) no longer exist. `documentChange.change` was closed to
   `CREATED`, `MODIFIED`, `REPLACED`, and `_validate_semantics` ended by
   requiring every path in `document_history` to be a file on disk, so `check`
   refused with "OVR-000352: revised document does not exist" whatever
   `OVR-000472` recorded. Luis ruled on 2026-09-20 (paper ledger E-0508): the
   grammar gains a deletion kind. Restoring the files and superseding the two
   recording entries were both refused. `REMOVED` landed at commit `623f5c4d`,
   RED first. It carries `before_digest`, the ledger's latest recorded digest for
   the path, and no `after_digest`; the other three kinds still require one, so
   all 471 sealed entries validate unchanged and the schema identity stays
   `malleus.contract-compiler.ledger-entry/v1`. The validator refuses a removal
   of a path the ledger never recorded, a `before_digest` that does not match the
   prior revision, and a removed path that is still a file; a removed path leaves
   `document_history`, so the final walk no longer holds it, and a later
   `CREATED` of the same path is accepted. `REPLACED` was not a candidate: its
   one use, `handover/2026-08-24-contract-compiler-overseer.md` in `OVR-000007`,
   records a file whose whole content was replaced and which still exists.
   `render` and `hash` are unchanged, because the bounded projection in
   `status.md` names no document path and no change kind.
2. **One entry cannot hold this branch.** `documentRevisionData.documents` has
   `maxItems: 20` and the chain covers 73 governed documents. The draft below
   is therefore a chain of four, `OVR-000472` to `OVR-000475`, split by sorted
   path with 20, 20, 20 and 13 documents. The split is mechanical and means
   nothing: the reason, the evidence commits and the subject are `OVR-000472`'s,
   and the other three say so. Each successor's `previous_entry_hash` is the
   literal `<previous entry hash>`, because it is the predecessor's `entry_hash`,
   which only exists once the sealing moment is fixed. That is a third
   placeholder kind beyond the two the brief allowed, and it is unavoidable for
   a chain.

**The full default suite.** Reported in the final measurement section below.
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
- `623f5c4d` the overseer ledger gains `REMOVED`, RED first
- `6214e2bc` three governed passages catch up with decision D
- `bc54ee8e` a removal claims no provenance for a later verified fact
- `19c8b05f` two docs still linked the two deleted check contracts

## The overseer entry: `OVR-000472` to `OVR-000475`

How the document set was computed, mechanically:

1. Every path an active sealed `DOCUMENT_REVISION` entry records, with its
   latest `after_digest`: 720 paths, read from
   `design/contract_compiler/overseer/entries/OVR-*.json`. 721 paths have been
   recorded at some point; one lives only in a superseded entry, which the
   validator does not hold.
2. Everything the branch changed, `git diff --name-only 85f0ed54..HEAD`: 103
   paths.
3. The intersection: **69 MODIFIED and 2 REMOVED**. Nothing in it already stood
   at its recorded digest.
4. Plus two CREATED: `handover/2026-09-20-core-two-step-door.md`, which the
   brief names, and `tests/contract_compiler/pareto/test_change_set_admission.py`,
   by the precedent `OVR-000471` set when it recorded
   `test_check_contract_executor.py` the same way. **73 documents.**

Nothing else qualified. `pyproject.toml` did not change on this branch, its
`include` list declares no new file, and its `testpaths` names
`tests/contract_compiler` as a directory rather than the new module. Every
`before_digest` below was checked against the bytes at `85f0ed54` as well as
against the ledger's own latest recorded digest: all 69 agree, so the two
readings of "the committed bytes at 85f0ed54" are the same bytes. The eight
documents this pass added to the set are
`.claude/skills/malleus-dev/SKILL.md`, `ROADMAP.md`,
`design/contract_compiler/overseer/README.md`,
`design/contract_compiler/overseer/ledger.schema.json`,
`docs/SMALL_SHOP_WALKTHROUGH.md`, `docs/index.md`,
`scripts/contract_compiler_ledger.py` and
`tests/test_contract_compiler_ledger.py`; `CHANGELOG.md` was already in the set
and its `after_digest` moved.

The two deleted documents are recorded as `REMOVED`, the correction's check in
`OVR-000472` and the showcase's in `OVR-000473`, each with `before_digest` the
ledger's latest recorded digest for its path:
`sha256:d98a26162b65c6f517788cc0cc5a0c1492f81918cc61d1674cfac06cc19c82a9` from
`OVR-000352` and
`sha256:ad5de0ee774298c12b641d7a15f1ef7fcab3adf693ad319bcc3e39959148734e` from
`OVR-000359`. Neither path was revised after the entry that created it, so the
creating entry's `after_digest` is the latest recorded digest. `OVR-000472`
also carries this file as `CREATED`, and `OVR-000474` carries
`test_change_set_admission.py`.

All four blocks validate against
`design/contract_compiler/overseer/ledger.schema.json` with
`Draft202012Validator` and a `FormatChecker`, substituting
`sha256:0000...0000` for `entry_hash`, for the placeholdered digest and for the
placeholdered previous hashes, and a real UTC timestamp for the placeholdered
sealing moment: **4 of 4 valid, 0 errors**. The probe reads the fenced `json`
blocks of this file and finds five, of which exactly four parse as an object
with an `entry_id`. `why` is 1197 characters in `OVR-000472` and 335 in each
successor, under the 1200 cap; `summary` is 169, under 240.

Proved end to end in a scratch copy of the repository, hardlinked so every
governed document is the exact byte the branch holds, **with the two deleted
documents left deleted**, the four entries inserted at real hashes and
`head.json` advanced to 475. `python scripts/contract_compiler_ledger.py render`
then `check` reports, verbatim:

```text
validated 475 entries; head OVR-000475 sha256:3d521a9f8998d22dd21068aaef565b253202dc61a86e3699a42e29d8f156d943
```

The scratch run binds this file as it stood immediately before this paragraph
was written; the entry records `<digest of this file once final>`, so sealing
re-derives it. The real worktree was never written to.

### `OVR-000472`

```json
{
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "after_digest": "sha256:b18e426e8e8bfb60217f2dde44cd641dd7b6f53aaf027a820ea20c6a3940d9ab",
        "before_digest": "sha256:931a230b1f2723ff63f236490bb64ecfbf990289d9d20db2e585563e81d2c5c8",
        "change": "MODIFIED",
        "path": ".claude/skills/malleus-dev/SKILL.md"
      },
      {
        "after_digest": "sha256:428abf6449b7f55864e8e8b7cef44dfd23cf808ea738fec997be344c25377240",
        "before_digest": "sha256:224b8278cbb6974f9c3d577cf71446d689f4f1ec4f95883aecb27f67eab3f10e",
        "change": "MODIFIED",
        "path": ".claude/skills/malleus-dev/references/CAPABILITIES.md"
      },
      {
        "after_digest": "sha256:71ee0e48be085c1e75af6658df40719c1b7b1cff933a11f6b731c9840bf696ee",
        "before_digest": "sha256:f637cbba30d0363d068a8e700c400d1e947301d22495f07eccf4bc90678efe49",
        "change": "MODIFIED",
        "path": "CHANGELOG.md"
      },
      {
        "after_digest": "sha256:52e1dc247a8d97535addb5c729f5e7f1d1e84a78fa0ecdfb61e5202ab4cecc83",
        "before_digest": "sha256:e5c3841991c0c5a910a9d5d0b693551f17cb6142b1338febc5ab94867bf27ced",
        "change": "MODIFIED",
        "path": "ROADMAP.md"
      },
      {
        "after_digest": "sha256:f3b88b9e8cf2e651b8c14b2a5f23e10a8cc534bc301c2531cacb0af02ce2b991",
        "before_digest": "sha256:e2eae18a85d937a8759c8a910d9a4c2d17c9af6540c38fbfd54614334aa69f9a",
        "change": "MODIFIED",
        "path": "design/contract_compiler/overseer/README.md"
      },
      {
        "after_digest": "sha256:a4b3e6441238cb30f5b189103fa4bea26100f6dba12efa482b3841792f393858",
        "before_digest": "sha256:034cadaad32401e98e5ee5131461ae7f2e335f1a6a7d8289634219974cd25c07",
        "change": "MODIFIED",
        "path": "design/contract_compiler/overseer/ledger.schema.json"
      },
      {
        "after_digest": "sha256:09feedab1dac003c5ec959ef0367f603070e3c544a5346b9a678320cb5b4d137",
        "before_digest": "sha256:ce786f210433a04b914690ea4fc272f16e5431530fdc98e556b137154e0e3665",
        "change": "MODIFIED",
        "path": "docs/IMPLEMENTATION_STATUS.md"
      },
      {
        "after_digest": "sha256:ce3183b742418bb2af1e8c9806043939ad6a12a9887606c0403843e7a0278fa4",
        "before_digest": "sha256:81ce100a6a0df1fc2fd201e1820c85d1bdcd25fc9b139e8813153a83dc62bc35",
        "change": "MODIFIED",
        "path": "docs/SMALL_SHOP_WALKTHROUGH.md"
      },
      {
        "after_digest": "sha256:a8ff630e712d695f5567505907541b51ec41dbdb84238291635cebc146367797",
        "before_digest": "sha256:006bdea4921ade62c58e1fc51b2043b8ef1855a71530c1c485e6d1e7135bb581",
        "change": "MODIFIED",
        "path": "docs/contract_compiler/index.md"
      },
      {
        "after_digest": "sha256:d5a38750b98118cb26cd68ffdacf9cc4a49892f0f57a8388ff8bb02856d19160",
        "before_digest": "sha256:c87b021e2e1a28e54bf7e7bf086a7598577aa3c218d9574f65b6f52d2556ddd5",
        "change": "MODIFIED",
        "path": "docs/index.md"
      },
      {
        "after_digest": "<digest of this file once final>",
        "change": "CREATED",
        "path": "handover/2026-09-20-core-two-step-door.md"
      },
      {
        "before_digest": "sha256:d98a26162b65c6f517788cc0cc5a0c1492f81918cc61d1674cfac06cc19c82a9",
        "change": "REMOVED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/correction/checks/source-mapping-conformance.json"
      },
      {
        "after_digest": "sha256:4cef2ab7e63c87ff3b3290026b6c0b1335b01cea18e30b353adfaf6ce52b8bd9",
        "before_digest": "sha256:47e59912feaa8584c52a3b3914754b61a0cd5caad6724cef7a910c19c8673fde",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/correction/checks/structural-conformance.json"
      },
      {
        "after_digest": "sha256:66913e1e39bec010c600543f756318dbc53f9ae3ce1767cdf08eb41e8fef29b8",
        "before_digest": "sha256:825c8d998ec311c93426dd7b787fff732eec09b7a9e0805fdfc2f7b215faf375",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/correction/machine.json"
      },
      {
        "after_digest": "sha256:724f16702697e591504c819395a6b1877d85283ba13c1830edb29dec94ba3be9",
        "before_digest": "sha256:57972777e8132ecd4c0430da659c92312e89a80f36779722276e804b4b92850f",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/correction/policy.json"
      },
      {
        "after_digest": "sha256:2554fbd5998c008c14af1a23d98ebbe4cd62f1f7c119b9eb897dd62ddd1eafaa",
        "before_digest": "sha256:414db35b85dd0931be75e27e80001046a8f457dda332425c9f42d244cd0bd160",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/correction/run.json"
      },
      {
        "after_digest": "sha256:9e04076f0181886c53e3ecfc003dfa1881c3c5af033146feb086cec0202c7fb8",
        "before_digest": "sha256:29902a7e7249efcad89637a0c3bea5cb6a2b17adeed85b4abf2bfcaf29114dbe",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/correction/run.py"
      },
      {
        "after_digest": "sha256:023b0e0026aff92e9d3c1cf5273ec7d1e8b4c3dd5b2cbdc5d122bb8266a9d4f9",
        "before_digest": "sha256:63f6068125e89aff5a594f88cca6971f215c4b6635f428bbb4d073a75d31781f",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/correction/test_correction_vertical.py"
      },
      {
        "after_digest": "sha256:81a690dcdc15b32465abcb676973116cf24c9ff4a7baa48f0b4c8e62d0d68726",
        "before_digest": "sha256:0d04ddd11d2de303b7502a4e3287627d6eafa2d81e4c78cca213b1b699b3bfc1",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/evidence_assertions.py"
      },
      {
        "after_digest": "sha256:7b56b161e1c6ed68d4f52a24346fa1f4905c92eedf2fabafa4a95adc31dea0a9",
        "before_digest": "sha256:e0b3541ee706250b78a49ee1b2b784b95993c3e2464425a1f24b67fe85a95023",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/object_event/run.py"
      }
    ]
  },
  "entry_id": "OVR-000472",
  "entry_type": "DOCUMENT_REVISION",
  "ledger": "overseer",
  "previous_entry_hash": "sha256:7cb9e624476d13a78ed15a5d5d89f219414cb536f3738eda7a91a94f1de984fd",
  "recorded_at": "<sealing moment, UTC>",
  "references": [
    {
      "relation": "EVIDENCES",
      "target": "7c6e3f627968e1c59de0bbe7d027179773d3d273",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "7c3237f06a7e1d7a4882d4e3cb787e7c889fd49f",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "980cb609a3d254460ce1958edc89ae335d3e9157",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "127c3f675e09db0d782f0aa0d423a72cd3f8c347",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "934ef948b0046665f6cd477eb67ea564d7de507f",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "623f5c4d69f65dade0120914b1a5051d7d0ca41e",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "6214e2bc9326a83bb0aacc6eab9c56300dd3e049",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "bc54ee8e71622b3adba1a4905a849bb3c69d7c33",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "19c8b05fe4fe041e4f77f5311cc1edfeb943262b",
      "type": "COMMIT"
    },
    {
      "relation": "AFFECTS",
      "target": "CC-R11",
      "type": "WORKSTREAM"
    }
  ],
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "sequence": 472,
  "subject": {
    "id": "core-two-step-door",
    "type": "DOCUMENT"
  },
  "summary": "Close Core's public admission door, add the third Core-authored entry point, fold Core's structural check into the grammar, and migrate every consumer. Documents 1 of 4.",
  "why": "Decision D (E-0502 to E-0508), step 2 of two. Core runs every check itself, so the public door closes. admit and admit_with_anchors refuse a caller-supplied CHECK_RECORDED or VERDICT_RECORDED with CALLER_SUPPLIED_CHECK_EVENT before any append, the verdict too because SELECT_POLICY_VERDICT derives it from the check records. PolicyProgram refuses an empty required_checks and acceptance needs the binding's VERDICT_RECORDED, so the two methods now admit nothing under any shipped binding. check_and_admit_change_set is the third Core-authored entry point, for a caller that composed its own operations; neither entry point takes an outcome. Core's structural check is now a malleus.check-contract/v1 CORE_BUILTIN document, moving STRUCTURAL_HISTORY_BUNDLE 0ef377d9 to 8a994ed0 and every coordinate cut against it. Nine research programs stopped writing their own outcomes, and three check contracts whose executor was their own program, or nothing, were removed. Two of the three were governed documents, so documentChange.change gains REMOVED: the ledger had no word for a deletion and refused whatever this entry recorded. Every exported graph and domain record stays byte-identical to 85f0ed54."
}
```

### `OVR-000473`

```json
{
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "after_digest": "sha256:ba4291a2423d78de1951ab4378f4d4b4ea4b296b0a9ecf28df8aba059eca131e",
        "before_digest": "sha256:4e8851c5b9ded2d9165e2e1c14e70b24b12d4a52e356a94032be60e068614dce",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/pareto/mapping.json"
      },
      {
        "after_digest": "sha256:433f2f9b2da4fa7d5e8740e05eb724b9e852fed051f4e78727570b3e5f265e5f",
        "before_digest": "sha256:c0ec653fbcdaa3a21cc713a224ecd9c059569e1d37305d1217c1b605da96d60b",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/pareto/policy.json"
      },
      {
        "after_digest": "sha256:1c5a75283a3bc74f4a67d471e1d5e63ed05ff5cfc6578efb145d3c4cfed29612",
        "before_digest": "sha256:b8c558b9dc2ca63f274bbae0b46231d7322719421db29bbf6729dbc68e12cc07",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/pareto/ret010.py"
      },
      {
        "after_digest": "sha256:58cff5c5f31f42a7096698fcf922c66d6e6025192971e8298ca1356e759cf4a6",
        "before_digest": "sha256:af7c61c2520db1f8c252274a7cf0432dcad07fa171fccd18458b87cbf63a69df",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/pareto/test_vertical.py"
      },
      {
        "after_digest": "sha256:c535035780d8a684ab7ee96a68cb28b4b80af295f3907f775c0d26e4637e3e46",
        "before_digest": "sha256:e10ecca01bcb24c91305793ce7338edcc858d5e01a092a127d779b778b160f52",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/public_population/README.md"
      },
      {
        "after_digest": "sha256:25162819510ffb6ec29906131326cfdade031420597910d8ce12fb87d7ae5a8f",
        "before_digest": "sha256:db96e3d8d50728ce4da7a08b31f8c6d91e3b17814b749b28e29794a579903232",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/public_population/plans/invoice-base.json"
      },
      {
        "after_digest": "sha256:c5360838a5937ab6f3ee29f1158d2cf3449b9737e7277fdee2b19f894421fcd7",
        "before_digest": "sha256:089cfe786641ab4872bdfb80ec0e463076594c7da57724db053a3e63a7a24e7c",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/public_population/plans/payment-e30.json"
      },
      {
        "after_digest": "sha256:8d17eabd1e70750d571fb544723ef2a9757e2822ce35ad6c4b4a8e50e271f6f9",
        "before_digest": "sha256:3fbf7b59199ac58de24b2924a484e900d43a117dbb6cc262fd636c1dfa8d0f2a",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/public_population/plans/ret010.json"
      },
      {
        "after_digest": "sha256:14305547560d6ec0b48b552be85f0ac4b2bb7061d6edfcd8172ab148793afbd0",
        "before_digest": "sha256:f41275c76212e39523a5f330f7feb2d675e2a9b4e052c8a8cca9b3c25267a78f",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/public_population/plans/supplier-e4.json"
      },
      {
        "after_digest": "sha256:1e9bf84f703730f92eccb1734ccb954e72a040fd451022eef8cc5e19f6ba729d",
        "before_digest": "sha256:2ffa3b1a8364788b22ade0632ce88a972228f403a6a6c34f7a30f208bf6d8cdd",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/public_population/plans/supplier-e7.json"
      },
      {
        "after_digest": "sha256:f45b7d2fb234372dec9908986569dbff5874592b4f2a5d9ee95bb71c18322e0e",
        "before_digest": "sha256:165983419a12c2c637b66b01029035083fd51caa331e39e8c3725d66370e7756",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/public_population/run.py"
      },
      {
        "after_digest": "sha256:4cb7703175fe18390f68df73d2bb5eb342786213beb72bb0f311f92666027808",
        "before_digest": "sha256:5768694ad8e086afeb66026f16130cbc8bc7c6b58bc01e77e9aa03942f8c23d2",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/shipment_policy/README.md"
      },
      {
        "after_digest": "sha256:f1d14f37497829e2871471a3e2413213ba0b34ae55e38413d7e50080568cb415",
        "before_digest": "sha256:bbcba6b52ffc4df1094612b5400ad0db2e1ab169c5ceb2a69f2230a25527f44d",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/shipment_policy/run.py"
      },
      {
        "after_digest": "sha256:e858f4119da735f1b70e6dcb718145430c88c5ee94d4361c5ff4a1c4b212c494",
        "before_digest": "sha256:e4e2ff056a5972ee5e0ee2653ed2565df499de8c52c507b26aed92e43b251fac",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/shipment_policy/test_shipment_policy.py"
      },
      {
        "before_digest": "sha256:ad5de0ee774298c12b641d7a15f1ef7fcab3adf693ad319bcc3e39959148734e",
        "change": "REMOVED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/showcase/checks/source-mapping-conformance.json"
      },
      {
        "after_digest": "sha256:83faaae9cc3fe648fc2618686adad15fe7fcfad1ef69c965ae53790f48424921",
        "before_digest": "sha256:2d964b7b73efd9ce72a409aadfceb64a03c1d1d74f16ae3601eb09ace61affec",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/showcase/evidence.py"
      },
      {
        "after_digest": "sha256:c72450aa97c8e7f248bd6494a297c7076deb38a24d4eb977319898927afdb254",
        "before_digest": "sha256:efa0ac20a3f6dbdad67c210ade3b3c4571ac8296463735fd29eb81d0852d32ed",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/showcase/policy.json"
      },
      {
        "after_digest": "sha256:1f5ff1bb7958fdaea30ab826e40a47896facc0f3f071b98f723c016f4cce48d2",
        "before_digest": "sha256:4e7f04f4ce2a7db1cf0f6dbc93572cd191f475736886e4fb789273e91f0cbb53",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/showcase/query.py"
      },
      {
        "after_digest": "sha256:bc6306762ff331bb106536e71bba37644b70d7e0cc618698f16b661d00d3f449",
        "before_digest": "sha256:7096c3f82e3f96aa7e1efa6f11a120bb2b3a6c441520d66589408fd8895885c6",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/showcase/run.json"
      },
      {
        "after_digest": "sha256:5845af3c2dfb46a997c5014034a5539596b899109b4d2e24558a240d567dff34",
        "before_digest": "sha256:588ab3766625c184992860730fe33bc0ca17550b555fb9635d973e7a77d09244",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/showcase/run.py"
      }
    ]
  },
  "entry_id": "OVR-000473",
  "entry_type": "DOCUMENT_REVISION",
  "ledger": "overseer",
  "previous_entry_hash": "<previous entry hash>",
  "recorded_at": "<sealing moment, UTC>",
  "references": [
    {
      "relation": "EVIDENCES",
      "target": "7c6e3f627968e1c59de0bbe7d027179773d3d273",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "7c3237f06a7e1d7a4882d4e3cb787e7c889fd49f",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "980cb609a3d254460ce1958edc89ae335d3e9157",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "127c3f675e09db0d782f0aa0d423a72cd3f8c347",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "934ef948b0046665f6cd477eb67ea564d7de507f",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "623f5c4d69f65dade0120914b1a5051d7d0ca41e",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "6214e2bc9326a83bb0aacc6eab9c56300dd3e049",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "bc54ee8e71622b3adba1a4905a849bb3c69d7c33",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "19c8b05fe4fe041e4f77f5311cc1edfeb943262b",
      "type": "COMMIT"
    },
    {
      "relation": "AFFECTS",
      "target": "CC-R11",
      "type": "WORKSTREAM"
    }
  ],
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "sequence": 473,
  "subject": {
    "id": "core-two-step-door",
    "type": "DOCUMENT"
  },
  "summary": "Close Core's public admission door, add the third Core-authored entry point, fold Core's structural check into the grammar, and migrate every consumer. Documents 2 of 4.",
  "why": "Continuation of OVR-000472, same work and same commits. The overseer schema caps one DOCUMENT_REVISION at 20 documents and this branch changes 73 governed documents, so the set is split by sorted path across 4 sequential entries. Splitting is mechanical and carries no meaning: the change, the evidence and the reason are OVR-000472's."
}
```

### `OVR-000474`

```json
{
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "after_digest": "sha256:343c23c4c5aa8c107f15e7a0da6bf236b250c578da73d699b762250bae65ae73",
        "before_digest": "sha256:1767f6e65c49faa3a4da3be504f992ab29a13e925b20a3915b9c0ce2d7a76f3e",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/showcase/test_evidence.py"
      },
      {
        "after_digest": "sha256:85778d6b396239aafa8587a06c78d2d74747d2526d57b7f277045862bab29ada",
        "before_digest": "sha256:aee752c22d399983de648b6376a88c37405306f36cee20528234c88300bcb303",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/showcase/test_query.py"
      },
      {
        "after_digest": "sha256:064695217ce8b50743c688eb7ed9ad884078cfc45a08be8dcf743aa7f6fad728",
        "before_digest": "sha256:f2ea7c2cee679262349864557b22a317ca788494946271c0cfdb874bd0340b33",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/showcase/test_run.py"
      },
      {
        "after_digest": "sha256:83f5a3e0cd75c273013b64b8a552cc4d165c79085b1d3562f8b3f00742c22a83",
        "before_digest": "sha256:258d7d77b09248d6315e102fa4a14871b531f24f9951712024c102b010211d06",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/test_current_evidence.py"
      },
      {
        "after_digest": "sha256:c36e4a93be5d14a8fcdcaad2bfc19f8f85acb25d18eecd895269b642cb667af9",
        "before_digest": "sha256:fad3a9c6e136e2b9711c07e6c8163f27a9bc4be5502531614a944e622afe644d",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_object_event_v1/input/population/ret-040.json"
      },
      {
        "after_digest": "sha256:7a69d144f6259802f310a0a112cd53055e07bf91f8a37ef04c06251eedc2704c",
        "before_digest": "sha256:6459c6ebb6d85e3e9be9b2273608137b74fc196519f55210d663f30f993d2113",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_object_event_v1/manifest.json"
      },
      {
        "after_digest": "sha256:cb9f354c59c35fb5f269699a91720fdced343637eb56f91a8d2418c05ac898c8",
        "before_digest": "sha256:ca22ef6dcdf8a8a79f1f93690a3a71a6b0d462a45f4c6e22f9bbdc455be73e58",
        "change": "MODIFIED",
        "path": "scripts/contract_compiler_ledger.py"
      },
      {
        "after_digest": "sha256:df52f876665c96923e97dd3c5dd8f2f49f51cf7659651240b31d30ba31fc1729",
        "before_digest": "sha256:415d7175da82381ef24536c9b9acc237b5d5121f16c18944d8d15cc6679c3a0f",
        "change": "MODIFIED",
        "path": "src/malleus/_contract_pipeline/admission.py"
      },
      {
        "after_digest": "sha256:0d4fa887438300337891684bb7e4d0c63d561d2cb99de5655b635498ac5f801c",
        "before_digest": "sha256:15b3991fb349d72007f4742bc9bd060453d640f92fbb70f1abd880b1adc1f960",
        "change": "MODIFIED",
        "path": "src/malleus/_contract_pipeline/knowledge.py"
      },
      {
        "after_digest": "sha256:5fc3a0253da35bb37c10379c54ad0b4cafcad8593e922f49c07c7cae4d880b5e",
        "before_digest": "sha256:9d856b6c28a68de43ea23a199f5bef36bf3a26b996fb58ce8360919f091ffb12",
        "change": "MODIFIED",
        "path": "src/malleus/compiler.py"
      },
      {
        "after_digest": "sha256:d69971668aa0f002849166f3a90abf39d546b35631abce649492aabc0769f67d",
        "before_digest": "sha256:daa2cc88009b281ae5343497ced2fceea77417ba77b115cf854554d617e1aee9",
        "change": "MODIFIED",
        "path": "src/malleus/profiles/structural-admission-check.json"
      },
      {
        "after_digest": "sha256:1ed8dea5dd6461a7a2e513a70556f7a5a0ce988a543528ec0348426c30421252",
        "before_digest": "sha256:4e0acca2c15b78f66d3994e77d4f9e878ed4cc69047ede08a8aa9b455aa71546",
        "change": "MODIFIED",
        "path": "src/malleus/profiles/structural-admission-policy.json"
      },
      {
        "after_digest": "sha256:62c5e36611c20c3cd9e65834ba184e8bd17877f07e35b2b998ed0c520f73fad6",
        "before_digest": "sha256:5f309d574731a3fe2d19910c3ec9f971bb486483832926d2596eb7d448612f2d",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_atomic_population_admission.py"
      },
      {
        "after_digest": "sha256:9ed4cbb9eac5478ea003ebf4000c644a85e14d013c24ca891ee3fa442d4fd637",
        "before_digest": "sha256:b2858dd0259061ddc628e39a5f968c9c4063841b146487b4a51297a5f3870323",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_change_composition_context.py"
      },
      {
        "after_digest": "sha256:76fe608db81bc05b163a76568ed932c3a4918d1cd0abfecb6cfd30bb5659300b",
        "change": "CREATED",
        "path": "tests/contract_compiler/pareto/test_change_set_admission.py"
      },
      {
        "after_digest": "sha256:d5c712de27dd405c7d947ca6d39607a4fed2580d505226c938c6facddeee0fb7",
        "before_digest": "sha256:39907071b235908d40897bfe44e9578b6ebd0964e64a153517474986f424a338",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_check_contract_executor.py"
      },
      {
        "after_digest": "sha256:c0573d2c0ead48022a619b422f8a225ccfcb6b10bcd9f5bf1f06981ce2085ffe",
        "before_digest": "sha256:b124b9c161b57a3e933c37e555784892f3d45dabc3baca913501976e54894503",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_check_contract_rebinding.py"
      },
      {
        "after_digest": "sha256:63210031c87e3b6fb101904d13250019c9ec0a1a133b4a19b15723539d7ff615",
        "before_digest": "sha256:b79a7799841581683f788bbc726a5b33195c9d0de3d1073d1f598f784edf1c20",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_contract_revision.py"
      },
      {
        "after_digest": "sha256:2ac45f3e2893df38086145edd88e24b1bc865c85a2b1c9bc7dc9c5003b3bcc88",
        "before_digest": "sha256:1940c85af19b73d56f06ce8a6e9bd7fef2be9edf12133af4e70ffb823bd71f00",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_document_fixture_producer.py"
      },
      {
        "after_digest": "sha256:cfdf1e5032acf87d43e92d29581f1bdc0b159dcb5ac2581c8c387637673a7fd8",
        "before_digest": "sha256:6d0c9d791d5bb9a350ef28cf07c1424f8bf0b7382948102f8aff5dfef6bd6057",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_finite_protocol_history.py"
      }
    ]
  },
  "entry_id": "OVR-000474",
  "entry_type": "DOCUMENT_REVISION",
  "ledger": "overseer",
  "previous_entry_hash": "<previous entry hash>",
  "recorded_at": "<sealing moment, UTC>",
  "references": [
    {
      "relation": "EVIDENCES",
      "target": "7c6e3f627968e1c59de0bbe7d027179773d3d273",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "7c3237f06a7e1d7a4882d4e3cb787e7c889fd49f",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "980cb609a3d254460ce1958edc89ae335d3e9157",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "127c3f675e09db0d782f0aa0d423a72cd3f8c347",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "934ef948b0046665f6cd477eb67ea564d7de507f",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "623f5c4d69f65dade0120914b1a5051d7d0ca41e",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "6214e2bc9326a83bb0aacc6eab9c56300dd3e049",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "bc54ee8e71622b3adba1a4905a849bb3c69d7c33",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "19c8b05fe4fe041e4f77f5311cc1edfeb943262b",
      "type": "COMMIT"
    },
    {
      "relation": "AFFECTS",
      "target": "CC-R11",
      "type": "WORKSTREAM"
    }
  ],
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "sequence": 474,
  "subject": {
    "id": "core-two-step-door",
    "type": "DOCUMENT"
  },
  "summary": "Close Core's public admission door, add the third Core-authored entry point, fold Core's structural check into the grammar, and migrate every consumer. Documents 3 of 4.",
  "why": "Continuation of OVR-000472, same work and same commits. The overseer schema caps one DOCUMENT_REVISION at 20 documents and this branch changes 73 governed documents, so the set is split by sorted path across 4 sequential entries. Splitting is mechanical and carries no meaning: the change, the evidence and the reason are OVR-000472's."
}
```

### `OVR-000475`

```json
{
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "after_digest": "sha256:d71ef53f7a1f3fa3c96e0225e04cc76f4abae33c222597c02dc8cafff43a5f86",
        "before_digest": "sha256:70392d0b73093c1e970cf033f8794851f8a0ebfb9309928eee9496918bd21a50",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_governed_population.py"
      },
      {
        "after_digest": "sha256:b2f1f373fa898a5d842178230c2c6c08d0d16e98b3bb87fff3a951e5b6c417e8",
        "before_digest": "sha256:9771738d663490917d626ce2ff74910f717905c93cbcc9bf07b27bc8d3752973",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_knowledge_change_history.py"
      },
      {
        "after_digest": "sha256:5d481487d9d5633d1e2def3b0916dd81883bb5cf44cde399e24119b4bee755dd",
        "before_digest": "sha256:368b200e8cb23a214be8e84404b71aefd00bfa69a07209ae45cd1eb6d70f4853",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_maintained_projection.py"
      },
      {
        "after_digest": "sha256:74f1da917de09b703a95ee37fd74c7db0ddeaab8edd0ad62fcde55b2d0ea8997",
        "before_digest": "sha256:fc9ebe2b1010dd7496a6c2645c8110b5dae413921bbbc500e8184148e6086d28",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_object_event_population.py"
      },
      {
        "after_digest": "sha256:a3a3dbb32fef15bf6ede09eb2528c7025825b230aaf2d9969445af91436f65d3",
        "before_digest": "sha256:1a663a98ccc5a93269e408faf6d69e4f55c3985e74609f3067f5c60a62e0a310",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_population_plan.py"
      },
      {
        "after_digest": "sha256:a1ba73711077437a87e5bbe136391ee57ae2d98299d3052b639d25317c4f082c",
        "before_digest": "sha256:8d6d727ce5a401372668d2fa408758d3aa9a4379b670a96e9b7f2924b560d04a",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_population_trace.py"
      },
      {
        "after_digest": "sha256:e0330970ac35524becd34bae6f2a1471b6022aa089a8882dfc1e19def5d95903",
        "before_digest": "sha256:c32317607d96863234d654ab8a19d4903a1d24f752b33dc0e97afe52c7b122e8",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_protocol_machine.py"
      },
      {
        "after_digest": "sha256:7daa17585759d7f366c916f89a06e3fadace2caeadab59cc0bc8bb6bc70e8e7b",
        "before_digest": "sha256:2224a1d5a98f6eabcc862f01cca097d4783a8929e98f123a6d558000d739c541",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_public_compiler.py"
      },
      {
        "after_digest": "sha256:3883c846e8a33dd57f9cd99a24219fdfd89488af23bd0801007de5b84b56500a",
        "before_digest": "sha256:87d18028d83dd7388d6e2000bdba6360ccc994239e4687421a41dceef300ba88",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_review_coverage.py"
      },
      {
        "after_digest": "sha256:cb4e0230457329fadaab87fa94c5d8965990b134a3b35c18a23b795a1324fd83",
        "before_digest": "sha256:784c33c2ccce87048abeaf31aa99f4dc20898e9aa37e907d852c8d6f06c080e3",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_small_shop_contract_revision.py"
      },
      {
        "after_digest": "sha256:f162f0ba007d19bf17279a7bdebf37ae3a0e5e1affe7f82ddda559763aa38899",
        "before_digest": "sha256:ed2ec2deea36d2a9848e38a3dfde04f3cea5838a0a4fa6705b250f2c485d00a0",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_transition_admission.py"
      },
      {
        "after_digest": "sha256:34ba4633be93601e27e5b1319bb7be6e9d4470f29e958be5338a97985614ad61",
        "before_digest": "sha256:7640d767fb3fcc45db89bb12da7283b548cb5d81d6ad5a9724d7d80ef328e2a0",
        "change": "MODIFIED",
        "path": "tests/test_contract_compiler_ledger.py"
      },
      {
        "after_digest": "sha256:65f763f441da5886fd57e71cb8dcd3165d90e037c2af1d9f5ba7532ad3b3eff9",
        "before_digest": "sha256:0e2d42c75459af2ee8a07e4d6379daad63b85e2d1102c41d6140b2584e36cff6",
        "change": "MODIFIED",
        "path": "tests/test_docs.py"
      }
    ]
  },
  "entry_id": "OVR-000475",
  "entry_type": "DOCUMENT_REVISION",
  "ledger": "overseer",
  "previous_entry_hash": "<previous entry hash>",
  "recorded_at": "<sealing moment, UTC>",
  "references": [
    {
      "relation": "EVIDENCES",
      "target": "7c6e3f627968e1c59de0bbe7d027179773d3d273",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "7c3237f06a7e1d7a4882d4e3cb787e7c889fd49f",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "980cb609a3d254460ce1958edc89ae335d3e9157",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "127c3f675e09db0d782f0aa0d423a72cd3f8c347",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "934ef948b0046665f6cd477eb67ea564d7de507f",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "623f5c4d69f65dade0120914b1a5051d7d0ca41e",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "6214e2bc9326a83bb0aacc6eab9c56300dd3e049",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "bc54ee8e71622b3adba1a4905a849bb3c69d7c33",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "19c8b05fe4fe041e4f77f5311cc1edfeb943262b",
      "type": "COMMIT"
    },
    {
      "relation": "AFFECTS",
      "target": "CC-R11",
      "type": "WORKSTREAM"
    }
  ],
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "sequence": 475,
  "subject": {
    "id": "core-two-step-door",
    "type": "DOCUMENT"
  },
  "summary": "Close Core's public admission door, add the third Core-authored entry point, fold Core's structural check into the grammar, and migrate every consumer. Documents 4 of 4.",
  "why": "Continuation of OVR-000472, same work and same commits. The overseer schema caps one DOCUMENT_REVISION at 20 documents and this branch changes 73 governed documents, so the set is split by sorted path across 4 sequential entries. Splitting is mechanical and carries no meaning: the change, the evidence and the reason are OVR-000472's."
}
```

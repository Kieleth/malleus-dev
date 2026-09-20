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

Ruff over `src tests`: the same nine pre-existing findings as `85f0ed54`
(`tests/test_kg.py` E401 twice, `tests/test_logic.py` F401 twice,
`tests/test_prolog_verifier.py` E402 five times), none in any changed file.

## Commits

- `7c6e3f62` the third entry point and its 16 tests, additive, door still open
- `7c3237f0` the door closed and the structural check folded, breaking

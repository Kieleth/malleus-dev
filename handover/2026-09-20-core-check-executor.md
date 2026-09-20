# Core runs the check its contract names

Decision D, paper ledger E-0502, step 1 of two. Luis: "Lets tackle D now."
Core runs every check itself; adopters supply contracts and rules, never
programs and never outcomes. This step is additive. The public admission door
stays open, no consumer changes, and step 2 closes the door and migrates the
research consumers.

## What landed

**One check-contract grammar Core parses**, `malleus.check-contract/v1`, in
`src/malleus/_contract_pipeline/check_contract.py`. A document is identified by
the exact bytes it is read from, and its `executor.kind` comes from a closed
set:

```json
{"check_contract_id": "malleus.core.structural-conformance",
 "executor": {"builtin_id": "malleus.core.operations-apply-atomically",
              "builtin_version": "1", "kind": "CORE_BUILTIN"},
 "grammar": "malleus.check-contract/v1",
 "outcomes": ["SATISFIED", "VIOLATED"]}
```

`PROLOG_RULES` names the two retained records that carry a pinned rule layer,
by record id, and runs them under `PrologVerifier` in its own process as
before. `CORE_BUILTIN` names a function Core ships, resolved by id and version
from `CORE_BUILTIN_CHECKS`. `outcomes` is a nonempty ordered subset of
`SATISFIED`, `UNKNOWN`, `VIOLATED`.

**There is no adopter-program kind.** The four live research check contracts
name an executor by artifact id and sha256, which is the arbitrary-code escape
hatch architectural law 12 forbids, and it leaves Core recording an outcome it
did not produce. A kind outside the set refuses when the contract is read, and
so does a builtin id or version the registry does not hold.

**How the grammar relates to `LogicContract`.** It references, it does not
widen. `LogicContract.from_bytes` validates an exact field set
(`logic.py:CONTRACT_FIELDS`, enforced by `_exact_fields`), and a `PROLOG_RULES`
executor declares only `descriptor_record_id` and `rules_record_id`; those two
names are disjoint from `CONTRACT_FIELDS`, pinned by
`test_the_grammar_does_not_reopen_the_logic_contract_fields`. The ontology
hash, the rule ids and the rule bytes keep one home.

A bare retained descriptor and rules pair that reproduces a required identity
still resolves as a `PROLOG_RULES` contract, unchanged. That is the form every
live Prolog check is already pinned in, and wrapping one in a v1 document would
mint a second identity for the same rules, moving the policy identity, the
normative profile, the partial effective contract and every coordinate frozen
downstream, which is the OVR-000466 blast radius. Nothing admitted before this
change is admitted differently now.

**How it relates to Core's own `structural-admission-check.json`.** That
contract stays separate in this step, and the reason is mechanical, not
preference. Its bytes hash to
`sha256:9901f51284257e47e25af414f035104373d0dace037d8943c4b6f5c0126ae3de`,
which `src/malleus/profiles/structural-admission-policy.json` names as its
`check_contract_identity` and which every structural history retains as
`malleus:structural-admission-check/v1`. Rewriting it under the new grammar
moves that digest, which moves the policy identity, the normative profile
identity and the partial effective contract identity, and every structural
history ever written refuses on reopen. Appendix B's two Shop calibration
digests sit behind exactly that chain. In an additive step the pinned form
stands.

The fold is available to step 2 at the cost of that re-pin, and the builtin
that would carry it already ships. Written under the new grammar as a
`CORE_BUILTIN` naming `malleus.core.operations-apply-atomically` version `1`,
the same contract hashes to
`sha256:b923c279024e7a2cf18fab86b2e9e80e8f5afecbd8e7da83be437f2fba228f41`.
That is the exact value a fold would have to propagate.

**One Core builtin**, `malleus.core.operations-apply-atomically` version `1`.
It applies a candidate's operations to the accepted state through Core's own
`KnowledgeChangeHistory._apply_change` and reports `result_state_digest`, or
`VIOLATED` carrying the refusal that stopped it and the candidate's record ids
as witnesses. Two adopter check contracts declare that algorithm and implement
it by calling that same Core primitive, so it was Core work already.

Its input is `CandidateChange`, a three-field value carrying exactly what
`_apply_change` reads: `change_set_id`, `operations`, `valid_time`. A composed
`KnowledgeChangeSet` additionally binds ledger coordinates that do not exist
while the check is still deciding whether to admit anything.
`test_the_candidate_change_carries_every_field_the_application_reads` walks the
primitive's AST and asserts the attribute set it reads on `change` equals this
value's field set, so a fourth read fails there rather than with an
`AttributeError` inside a check.

**The operation runs every required check, in policy order.**
`UNEXPECTED_REQUIRED_CHECKS`, which refused any policy not requiring exactly
one contract, is gone. Each check gets its own retained receipt and its own
`CHECK_RECORDED`, and `PopulationAdmission.checks` reports them in the policy's
order; the singular fields name the first of them. A required check the history
does not retain still refuses `CHECK_CONTRACT_NOT_RETAINED`; one whose executor
Core cannot run refuses `UNRUNNABLE_REQUIRED_CHECK`. Both refuse before the
first append.

**Each `CHECK_RECORDED` carries the selected machine's declared field set.**
Core holds a closed superset of values per event type and the machine's own
`record_schemas[...].input_fields` selects from it.
`correction/machine.json` declares seven `CheckRecord` input fields including
`receipt_identity` where the shipped structural machine declares six, and the
operation used to write six whatever the machine said, so that machine refused
`MALFORMED_EVENT` after its retention batch had already been appended. A
declared field Core cannot state refuses `UNSUPPORTED_EVENT_FIELD` at `CHECK`,
with no byte written.

## The two algorithms that did not become builtins

Read from the adopter code, not from the contract names.

`SOURCE_MAPPING_CONFORMS_TO_CHANGE_SET`
(`research/.../small_shop/correction/run.py`, `_verify_source_mapping`) is
experiment-specific. It reads a retained run program's
`artifact_ids.baseline_mapping` and `artifact_ids.correction_mapping`, the
`baseline.source_id_prefix` and `correction.source_id_prefix` values, a
`stages[].mapping_change` selector that is either the literal `"BASELINE"` or
an integer index into `correction.changes`, a `selection_member`, an
`ordinal_base`, a `record_order`, a `temporal_semantics` that must equal
`"ORDER_ONLY"`, and a `supersedes_event_id` on the correction row. It parses
the retained baseline through `Ret010Mapping.from_bytes`. Every one of those is
this experiment's artifact naming, not a property of retained inputs, plan and
change set that Core could state.

`RECOMPUTE_DECLARED_SOURCE_TO_CHANGE_SET`
(`research/.../small_shop/showcase/run.py`, `verify_stage` and `selected`) is
experiment-specific for the same reason and one more. It dispatches on a stage
selector that is `"RET010"`, a string beginning `"CORRECTION:"`, or the
settlement default; it reads members out of a fixture `input/manifest.json`
whose digest the mapping pins; and it parses a member by a declared parser name
(`records(source, "JSON_LINES")`). A closed parser vocabulary for retained
source bytes is not something Core has.

`retained-source-integrity`, the second check
`research/.../small_shop/pareto/policy.json` requires, has no implementation to
promote. Its identity
`sha256:8208a29397002098d74498c4956f5a86d10526f8e4cf806feae4fe769074c19d`
appears only in that policy and in `pareto/mapping.json`; no file in the
repository hashes to it. `pareto/ret010.py` builds the two `CHECK_RECORDED`
events from `mapping.json`'s `protocol.checks[].outcome`, which is the literal
string `"SATISFIED"` in a fixture file. That consumer runs no check at all.

**The proposal for both, for step 2.** Under the one-call operation neither
property needs an executor, because Core compiles the plan itself: the mapping
from retained source bytes to change-set operations is the operation's own
work, so a source mapping that conformed by being recomputed becomes a mapping
that conforms by construction. What remains to promote from them is a
declaration of which retained member and ordinal a record derives from, which
Core already carries as the plan's `derivations`.

## Bound slice

1. **Claim.** A check contract names its executor from a closed set and Core
   runs it. Under a history whose installed policy requires N retained check
   contracts Core can run, one Core operation compiles a producer-written plan,
   runs all N in the policy's order over the would-be accepted state, and
   appends the retained plan, its gaps, the profile artifact, the change set,
   one receipt per check and `CHANGE_PROPOSED`, N `CHECK_RECORDED` and
   `VERDICT_RECORDED`, with each check record carrying exactly the fields the
   selected machine declares. No parameter carries an outcome.
2. **Smallest observation.** A two-check policy, one `CORE_BUILTIN` and one
   Prolog rule layer, admits with both receipts retained and both check records
   written; the same history with a seven-field `CheckRecord` writes
   `receipt_identity`; a plan violating the rule layer refuses at `CHECK` with
   the ledger bytes unchanged.
3. **Reused.** `KnowledgeHistoryReplay.required_checks`,
   `LogicContract.from_bytes`, `PrologVerifier`,
   `KnowledgeChangeHistory._apply_change`, `execute_event`,
   `compile_population_plan`, `prepare_population_change`, `stage_subgraph`.
4. **Excluded.** The public two-step door (unchanged). `admit` and
   `admit_with_anchors` (unchanged). `admit_structural_change` and its ledger
   bytes (unchanged). Core's own structural check contract bytes (unchanged).
   The research experiments (not edited). A second builtin.

**Role classification.** `OPTIONAL_PROFILE`: semantic-history with
logic-monitoring. The grammar and the registry are the
`REFERENCE_IMPLEMENTATION` of the executor boundary. No new
`PROTOCOL_INVARIANT` is claimed: an adopter that claims neither profile has no
ledger and no check contract.

## Not done, and why: Core's own test admissions (step 4 of the brief)

**The step's design does not hold against the code, and I stopped rather than
force it.** The brief asked that every one of the 132 caller-authored
admissions move to a real retained contract *through a Core-authored path*,
naming `check_and_admit_population_plan` or `admit_structural_change`. Neither
can serve them.

Measured, not inferred. Building the exact history
`tests/contract_compiler/pareto/test_knowledge_change_history.py::_anchored_history`
builds and handing its change set to `admit_structural_change`:

```
history binding identity  : sha256:87d653d38f56f771a91668b05f99ec80ffcc2e5e8bbe841c7e6b978db6b89e5e
structural bundle binding : sha256:87d653d38f56f771a91668b05f99ec80ffcc2e5e8bbe841c7e6b978db6b89e5e
bindings equal            : True
admit_structural_change   : KnowledgeChangeRefusal IDENTITY_MISMATCH: transition program changes the structural protocol
```

The binding matches; the normative profile does not. `admit_structural_change`
refuses unless the history's normative profile identity equals the structural
bundle's, and that fixture deliberately installs an adopter machine program and
an adopter policy, which is what `test_protocol_machine.py` exists to exercise.
`check_and_admit_population_plan` takes plan bytes and compiles them; it cannot
admit a hand-composed `KnowledgeChangeSet`, and a large part of those tests
feed deliberately malformed change sets whose whole intent is that `admit`
refuses them.

**What would let them move**, and it is a decision, not an omission: a third
Core-authored entry point that admits a composed `KnowledgeChangeSet` by
resolving the policy's required checks through the new grammar, running them,
and writing the events itself. Every part of it now exists in
`check_contract.py` and `admission.py`. That is not a test-only bypass; it is
the capability a consumer that composes its own change set needs, and step 2
needs it to close the door for those consumers too. **Open for Luis.**

The related half that is safe and was also not done, for the same reason it
would be half a migration: replacing the fixture policy's two fictional check
identities (`sha256:aaa…`, `sha256:bbb…` in
`tests/contract_compiler/pareto/test_protocol_machine.py:CHECKS`) with two real
retained `CORE_BUILTIN` contracts. It moves the policy identity and every
identity downstream of it across two files and six history builders, and the
migration it enables cannot land in the same step.

## Residuals, named

- **The two-step door is open**, by design in this step. `admit` and
  `admit_with_anchors` still read a caller-supplied outcome off a
  `CHECK_RECORDED` event. Step 2 closes it.
- **The receipt ids moved.** `check_and_admit_population_plan` now mints a
  retained receipt id and a `CheckRecord` id that each name the change set and
  the check contract, joined by colons after the `receipt:` and `check:`
  prefixes. The forms they replace named only the change, which cannot say
  which of two receipts is which, and the machine refuses a repeated
  `CheckRecord` id outright. One assertion in
  `test_atomic_population_admission.py` carried the old literal and was updated
  to the new one; no shipped consumer reads these ids, and
  `admit_structural_change` does not mint them.
- **`ADMIT` is still not byte-total**, unchanged from OVR-000468.
- **Core cannot read Prolog.** A `PROLOG_RULES` contract is still an adopter
  assertion about what its rules read, which is what `RULE_DECLARES_ITS_READS`
  (ROADMAP F3, F5) is for.

## Evidence

- `tests/contract_compiler/pareto/test_check_contract_executor.py`, 16 tests,
  all new. `tests/contract_compiler/pareto/test_atomic_population_admission.py`
  stays at 18, with one receipt-id literal updated.
- Full default suite in a clean worktree at `9717f050`: 3624 passed, 3 skipped,
  0 failed. That number is derived, not measured in isolation. The run that
  produced it read `admission.py` while this change was being written, so its
  15 failures were 14 governance digest guards on those in-flight bytes and one
  ruff check over a half-saved file. An archive export was tried as a clean
  substitute and rejected: it is not a repository, so every test that reads
  commit history fails there for that reason alone.
- Full default suite after, on this tree: 3610 passed, 3 skipped, 30 failed.
  The arithmetic closes: 3610 plus 30 is 3640, which is 3624 plus the 16 new
  tests.
- Six of those 30 were mine to fix and are green now. Two,
  `test_inquisition.py::TestPackagingTargetsAreTracked` and
  `TestNoPrivateMaterialCanReachARelease`, refused an untracked
  `check_contract.py` declared in `pyproject.toml`; committing cleared both
  (107 passed, 1 skipped). Four were retained measurements of `pyproject.toml`
  bytes going stale, three in `test_contract_compiler_duplicate_scan.py` and
  one in `test_contract_compiler_divergence.py`. The repository's own record
  commands refreshed them,
  `scripts/contract_compiler_ledger.py refresh-evidence` on
  `conformance/contract_compiler/v0/evidence/CC-X01-environment-contract-correction.json`
  and `scripts/contract_compiler_duplicate_scan.py --write` on
  `conformance/contract_compiler/v0/bundled_declaration_scan.json`. Both files
  are recorded in the entry below (29 passed).
- The remaining 24 are the governance digest guard,
  `OVR-000469: latest document digest mismatch for pyproject.toml`: seven in
  `test_contract_compiler_ledger.py`, fourteen in
  `test_contract_compiler_integration.py`, three in `test_docs.py` where the
  strict Sphinx build runs the same validation. The seal clears them. A second
  full run over the committed tree confirms exactly that residue: 3616 passed,
  3 skipped, 24 failed, and 3616 plus 24 is 3640 again.
- Caller-authored admissions, measured with the read-only counting probe the
  E-0501 agent wrote (it wraps `admit` and `admit_with_anchors` and records,
  per test, whether the events carried `CHECK_RECORDED` or `VERDICT_RECORDED`
  under a policy requiring a check). Before, on `9717f050`: 134 distinct tests
  across 18 files. After, on this tree: 134, file for file. Nothing moved,
  because step 4 was not built. Core-authored admissions went from 44 to 49,
  the five the new module adds. E-0501 reported 132 across 17 files at
  `8933892e`; the difference is 74 commits of test movement, not this change.
- Tests to keep as step 2's RED, because their intent *is* a caller-authored
  check event and closing the door kills their premise:
  `test_atomic_population_admission.py::test_today_a_fabricated_check_outcome_is_admitted_with_no_engine_run`,
  `test_atomic_population_admission.py::test_today_an_admission_with_no_check_event_refuses_under_an_installed_policy`,
  `test_knowledge_change_history.py::test_refused_change_never_changes_ledger_or_replayed_graph[rejected]`,
  which supplies a caller-authored `VIOLATED` outcome, and
  `test_transition_admission.py::test_low_level_admission_refuses_event_replacement_despite_satisfied_checks`.
- The research experiments were not edited and their suites are unchanged:
  `research/ontology_driven_kg_realization/experiments/small_shop` and
  `research/methodology_gedanken_e2e/tests`, 390 passed, 0 failed.
- Appendix B stands. `paper-v4/test_shop_connected_calibration.py` and
  `paper-v4/test_shop_calibration.py`, run read-only on this worktree's Core:
  16 passed, including
  `test_ledger_digests_in_the_appendix_match_a_fresh_run`, which rebuilds the
  connected chain and compares the manuscript's printed digests against it, so
  `32798a67` and `15c7c1ef` both hold.
- Ruff over `src tests scripts`: the same nine pre-existing findings as
  `9717f050` (`tests/test_kg.py` E401 twice, `tests/test_logic.py` F401 twice,
  `tests/test_prolog_verifier.py` E402 five times), none in the changed files.

The draft entry below is unsealed. The Overlord seals it.

## OVR-000471 draft, unsealed

This block lives here, not in `design/contract_compiler/overseer/entries/`,
because that directory holds sealed entries only: an unsealed file there makes
`load_ledger` refuse on the head entry count. This handover is recorded as
`CREATED` with its own digest as a placeholder, because that digest cannot be
computed inside itself; the sealer fills it with the sealed bytes.

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
        "after_digest": "sha256:224b8278cbb6974f9c3d577cf71446d689f4f1ec4f95883aecb27f67eab3f10e",
        "before_digest": "sha256:95460b0cbdfe8f1f4556a646095fdfa6f6f57ce4948f194e69456f2ae1eccac3",
        "change": "MODIFIED",
        "path": ".claude/skills/malleus-dev/references/CAPABILITIES.md"
      },
      {
        "after_digest": "sha256:f637cbba30d0363d068a8e700c400d1e947301d22495f07eccf4bc90678efe49",
        "before_digest": "sha256:e12d9a009e2528a7902b8b3d59d4cd53d60b400c7fd582ac50e7c15809ee2def",
        "change": "MODIFIED",
        "path": "CHANGELOG.md"
      },
      {
        "after_digest": "sha256:e30270a44e1305a355c27cf063ee99b4cd5112f4bb9bcfa74392315252f7e475",
        "before_digest": "sha256:65bc88dd008a2567fd04307214c566713d38bee05b96ba394534673736c564e3",
        "change": "MODIFIED",
        "path": "conformance/contract_compiler/v0/bundled_declaration_scan.json"
      },
      {
        "after_digest": "sha256:c481094613e46a6d28882a332cc9bd5dc6a1816639c5fba98aa34125c26fbd9c",
        "before_digest": "sha256:83a5444a3dafda17bcbe5accca468e1562e20419997976bf6085eab3307d2448",
        "change": "MODIFIED",
        "path": "conformance/contract_compiler/v0/evidence/CC-X01-environment-contract-correction.json"
      },
      {
        "after_digest": "sha256:ce786f210433a04b914690ea4fc272f16e5431530fdc98e556b137154e0e3665",
        "before_digest": "sha256:2231d4d3d8cdb5e067e334840d32e5d28ca791e4e1f23acc8fde359ccb48036c",
        "change": "MODIFIED",
        "path": "docs/IMPLEMENTATION_STATUS.md"
      },
      {
        "after_digest": "sha256:006bdea4921ade62c58e1fc51b2043b8ef1855a71530c1c485e6d1e7135bb581",
        "before_digest": "sha256:18722eac7d88e67cfc7ce569f5a296c38c729fc5a6d017d3d20e76d492a6b8bd",
        "change": "MODIFIED",
        "path": "docs/contract_compiler/index.md"
      },
      {
        "after_digest": "<digest of this file once final>",
        "change": "CREATED",
        "path": "handover/2026-09-20-core-check-executor.md"
      },
      {
        "after_digest": "sha256:037567e39af4eca01f8ff0560625075d053729f8311d5dce3bc9270b0f47a47d",
        "before_digest": "sha256:3f59e5956b9ba5efa7bbfdf5e1a78c507f717e6e2b5393245c4e686c1d1bcad9",
        "change": "MODIFIED",
        "path": "pyproject.toml"
      },
      {
        "after_digest": "sha256:415d7175da82381ef24536c9b9acc237b5d5121f16c18944d8d15cc6679c3a0f",
        "before_digest": "sha256:b77ffdc57b3dcbb060d02e688336647b1c01c00cb3ab4e5bea9fdd09f849ad19",
        "change": "MODIFIED",
        "path": "src/malleus/_contract_pipeline/admission.py"
      },
      {
        "after_digest": "sha256:9b28134f2b29340340c6371217cffce73ddef946dbe861f629648a59373059ca",
        "change": "CREATED",
        "path": "src/malleus/_contract_pipeline/check_contract.py"
      },
      {
        "after_digest": "sha256:9d856b6c28a68de43ea23a199f5bef36bf3a26b996fb58ce8360919f091ffb12",
        "before_digest": "sha256:b1e5d92e495455682f82cb765f2a001e253f21898da6028d1dbc79ac0058f892",
        "change": "MODIFIED",
        "path": "src/malleus/compiler.py"
      },
      {
        "after_digest": "sha256:5f309d574731a3fe2d19910c3ec9f971bb486483832926d2596eb7d448612f2d",
        "before_digest": "sha256:2d28b7bf983d4987f03062f6b29dcb9ce02f4272b5aef7b7f78d5d68dc7206c6",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_atomic_population_admission.py"
      },
      {
        "after_digest": "sha256:39907071b235908d40897bfe44e9578b6ebd0964e64a153517474986f424a338",
        "change": "CREATED",
        "path": "tests/contract_compiler/pareto/test_check_contract_executor.py"
      }
    ]
  },
  "entry_id": "OVR-000471",
  "entry_type": "DOCUMENT_REVISION",
  "ledger": "overseer",
  "previous_entry_hash": "sha256:c57f0f68aeed56810ceb5950b0cd4ad6ca3cf71d39abc19dcffe749e0a85e30b",
  "recorded_at": "<sealing moment, UTC>",
  "references": [
    {
      "relation": "EVIDENCES",
      "target": "b7324a755fc90d60d81f6c4a48346df8d8a64595",
      "type": "COMMIT"
    },
    {
      "relation": "AFFECTS",
      "target": "CC-R11",
      "type": "WORKSTREAM"
    }
  ],
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "sequence": 471,
  "subject": {
    "id": "core-check-executor",
    "type": "DOCUMENT"
  },
  "summary": "Record one check-contract grammar Core parses, its closed executor set, the first Core check builtin, and the one-call operation running every check the policy requires.",
  "why": "Decision D (paper ledger E-0502), step 1 of two, additive. Core runs every check itself; adopters supply contracts and rules, never programs and never outcomes. malleus.check-contract/v1 is the one check-contract grammar Core parses, and executor.kind is closed. PROLOG_RULES references the retained records carrying a pinned rule layer and runs them under PrologVerifier as before; CORE_BUILTIN names a function Core ships, from a closed registry. No adopter-program kind: an executor named by artifact id and sha256, the shape the four live research contracts use, is the escape hatch architectural law 12 forbids. The grammar references LogicContract and restates none of its closed fields, and a retained descriptor and rules pair still resolves, so no pinned identity moved. One builtin ships, malleus.core.operations-apply-atomically/1, which two adopter contracts already implement by calling Core's own _apply_change. The operation now runs every required check in policy order, one receipt and one CHECK_RECORDED each, carrying the fields the selected machine declares; UNEXPECTED_REQUIRED_CHECKS is gone. Not done and reported: Core's 132 caller-authored test admissions."
}
```

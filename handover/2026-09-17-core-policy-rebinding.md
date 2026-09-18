# Policy re-binding across an additive contract revision

The census under `private/shop-progressive-01/census/revision-01` (E-0458) found
that an adopter with a rule layer can never grow its ontology. Core records the
additive revision and the graph replays byte-identical, but the rule layer
cannot follow: re-pinning the same rule bytes to the new ontology hash moves the
check contract identity, hence the policy, hence the normative profile, and
`compile_contract_revision` refuses
`INCOMPATIBLE_CONTRACT: domain revision changes the normative protocol profile`.
Keeping the old pin makes every later admission fail
`Logic contract and compiled facts use different ontologies`. Both refusals are
right alone. Together they are a dead end.

This candidate lets an additive revision carry the re-binding as a declared,
recorded act.

## The slice, bound before any code

**Profile classification.** `OPTIONAL_PROFILE`, the compiler-enabled
semantic-history profile. This is not a base-protocol invariant: an adopter that
does not select the compiler-enabled profile, or that selects it without a
policy whose required checks pin an ontology, is unaffected and gains no
guarantee. The lowest affected profile is the one `KnowledgeChangeHistory`
already governs; nothing in `docs/PRINCIPLES.md`'s base contract moves.

1. **The exact claim.** An additive contract revision may carry, as a declared
   part of the same revision, the re-binding of the selected policy's required
   check contracts to the target ontology, when and only when nothing but the
   ontology binding inside each check contract changes. The revision refuses,
   with a typed reason naming what moved, when anything else about the policy
   moves.
2. **The smallest observation.** One Small Shop history with a check contract
   pinned to the compiled ontology: today the re-binding revision refuses
   `INCOMPATIBLE_CONTRACT`; after the change it is recorded, a later admission
   under the re-pinned check identity is accepted, the earlier check receipts
   still verify against their recorded identities, and reopen replays the same
   graph. Negative controls: changed rule bytes, an added check, a changed
   verdict, each refused with its own typed reason and the ledger byte-identical.
3. **The artifact reused.** `compile_contract_revision`,
   `ContractRevisionPolicy`, `PartialEffectiveContract`,
   `NormativeAdmissionProfile`, `PolicyProgram` and the existing
   `CONTRACT_REVISION_RECORDED` event. No new stage, no new authority, no new
   store.
4. **Excluded.** General policy migration. A revision that changes rule bytes,
   adds or removes a required check, changes a verdict mapping, its precedence,
   the policy identifier, the set of bound policies or the protocol machine
   program. Core still executes no Prolog and produces no check outcome. The
   adopter runner is not changed here.

**No persisted wire format became unreplayable.** One consequence needed care
and is recorded in full under "The revision policy's own digest moved" below:
declaring a change kind moves `CONTRACT_REVISION_POLICY.identity`, which a
recorded revision carries. Both policies are therefore executable by
declaration and a revision names the one it was compiled under, so every
ledger that already holds a recorded revision still replays. Nothing was
rewritten and no operator ruling was needed.

## What the capability is

An additive revision may carry `check_contract_descriptors`, a mapping from a
required check contract's ID to the pair of exact field mappings before and
after the revision:

```python
revision = history.compose_contract_revision(
    revision_id="revision:shop:0.1.0-to-0.2.0",
    target_validated_contract_bytes=target.artifact.artifact_bytes,
    target_partial_contract_bytes=target_partial.canonical_bytes,
    reason="add the state vocabulary and re-pin the rule layer",
    issued_at=TRANSACTION_TIME,
    check_contract_descriptors={"shop-content-rules": (before, after)},
)
```

For a Prolog `LogicContract` the descriptor is the ten semantic fields whose
canonical digest is `LogicContract.contract_hash`: `schema_version`,
`contract_id`, `contract_version`, `ontology_hash`, `fact_contract_version`,
`ruleset_id`, `ruleset_version`, `rule_ids` (sorted), `timeout_seconds`,
`ruleset_hash`. Core does not know that vocabulary and does not name a field
of it. It checks five things:

1. Both mappings hash to the check contract identities the current and target
   policies require. A declared mapping that does not is
   `IDENTITY_MISMATCH`, not a trusted claim.
2. Both mappings carry the same field names.
3. Exactly one field differs, and its value before the revision is the current
   ontology's content hash.
4. That field's value after the revision is the target ontology's content hash.
5. Undoing the declared re-binding inside the target profile reproduces the
   current profile byte for byte.

**Why Core does not look for `ruleset_hash`, stated because it was a decision.**
The brief asks for the rule bytes to be identical. Requiring every field but
the ontology binding to be identical is that condition and more, and it is
expressible without Core learning one consumer's field names. `EXECUTOR_ONLY`
and the 2026-09-03 rule against a contract written from one case both point the
same way: the check contract's vocabulary belongs to the adopter, and a Core
branch that reads `ruleset_hash` would make the Prolog contract's shape
protocol. What the event records instead is `unchanged_fields_digest`, the
digest of the descriptor with the re-bound field removed, identical before and
after. That single value is the proof, and rule-bytes identity follows from it.

`rebound_field` is derived, not declared. Core finds the field that carries the
current ontology hash rather than being told which one it is, so a caller
cannot point the rule at a field of its choosing.

## What refuses, and with which reason

Every refusal below leaves the ledger byte-identical; each test asserts that.

| case | reason | detail |
| :-- | :-- | :-- |
| profile moved, nothing declared | `INCOMPATIBLE_CONTRACT` | `domain revision changes the normative protocol profile` |
| rule bytes changed | `INCOMPATIBLE_CONTRACT` | `check contract <id> changes fields beyond its ontology binding: ruleset_hash` |
| required check added or removed | `INCOMPATIBLE_CONTRACT` | `domain revision changes the required checks of policy <id>: <names>` |
| verdict mapping changed | `INCOMPATIBLE_CONTRACT` | `domain revision changes the outcome verdicts of policy <id>` |
| precedence changed | `INCOMPATIBLE_CONTRACT` | `domain revision changes the verdict precedence of policy <id>` |
| policy identifier changed | `INCOMPATIBLE_CONTRACT` | `domain revision changes the identifier of policy <id>` |
| machine program changed | `INCOMPATIBLE_CONTRACT` | `domain revision changes the protocol machine program` |
| bound policies changed | `INCOMPATIBLE_CONTRACT` | `domain revision changes the bound policy programs: <refs>` |
| check moved, not declared | `INCOMPATIBLE_CONTRACT` | `domain revision changes check contract <id> without declaring its re-binding` |
| declared, nothing needs it | `INCOMPATIBLE_CONTRACT` | `revision declares a re-binding of <id> that no policy requires` |
| re-pinned elsewhere | `INCOMPATIBLE_CONTRACT` | `check contract <id> does not rebind ontology_hash to the target ontology` |
| re-pin with no ontology change | `INCOMPATIBLE_CONTRACT` | `check contract <id> does not pin the current ontology in exactly one changed field` |
| anything the field walk misses | `INCOMPATIBLE_CONTRACT` | `domain revision changes the normative protocol profile beyond the declared re-binding` |
| descriptor does not hash right | `IDENTITY_MISMATCH` | `declared check contract <id> does not hash to the identity the <current\|target> policy requires` |
| re-binding under the superseded policy | `MALFORMED_REVISION` | `unknown contract revision kind: REBIND_CHECK_CONTRACT` |

The last structural row is the authority. The field-by-field walk exists to
produce the named diagnostics above it; the byte comparison is what establishes
that nothing else moved. A `PolicyProgram` names its identifier under a key of
the adopter's choosing, so two policies can carry the same identifier under
different keys and the walk sees nothing while the bytes differ.
`test_a_profile_change_the_field_walk_cannot_see_still_refuses` is that case.

## The revision policy's own digest moved

`CONTRACT_REVISION_POLICY` is the canonical JSON of its declared change kinds,
so adding `REBIND_CHECK_CONTRACT` moves its identity. A recorded revision
carries `policy_identity`, and replay used to require it to equal the single
active policy. Left alone, every ledger holding a recorded revision would have
stopped replaying with `POLICY_REFUSAL`. That is the non-additive wire change
the brief said to stop on, so it was not made.

What landed instead follows the shape already in this repository for
`SUPPORTED_FACT_CONTRACT_VERSIONS`: `SUPPORTED_CONTRACT_REVISION_POLICIES`
holds both policies, `contract_revision_policy(identity)` resolves the one a
revision declares, and `compile_contract_revision` takes that policy as an
explicit argument. Replay passes the revision's own declared policy, so an
ontology-only revision recorded under the superseded policy rebuilds and
matches. Nothing selects a policy implicitly and nothing falls back: new
revisions bind `CONTRACT_REVISION_POLICY`, and a revision that declares the
superseded policy while carrying a re-binding refuses as an unknown change
kind. Both are pinned by tests.

In-repo evidence for the exposure: no committed `.jsonl` contains
`CONTRACT_REVISION_RECORDED`, and the only recorded revisions on this machine
are the census's own scratch copies. The archived live Shop history has zero
contract revisions (E-0458 baseline). The compatibility work is therefore
insurance, not a repair.

## RED and GREEN

`tests/contract_compiler/pareto/test_check_contract_rebinding.py` builds the
Small Shop history the census reached, with one difference from
`test_small_shop_contract_revision.py`: its policy's single required check is a
real `LogicContract` written into `tmp_path` and pinned to the compiled
ontology's content hash, which is the shape that created the dead end.

- RED `b01a165aafe6501be8f60a22a89113a020f83e76`: **12 failed, 2 passed.** Nine
  failures are `TypeError: KnowledgeChangeHistory.compose_contract_revision()
  got an unexpected keyword argument 'check_contract_descriptors'`, one is the
  change-kinds assertion, two are `AttributeError: module 'malleus.compiler'
  has no attribute 'SUPPORTED_CONTRACT_REVISION_POLICIES'`. These are
  missing-signature failures, not failed behavioural assertions, for the same
  reason the gate-hardening change 4 reported: the new behaviour cannot be
  expressed through the old signature.
- The two that passed at RED are the census's two refusals, and they are
  controls that pass before and after:
  `test_an_undeclared_profile_change_still_refuses_the_revision` asserts
  `INCOMPATIBLE_CONTRACT: domain revision changes the normative protocol
  profile` on the exact re-pinned profile, with the ledger unchanged, and
  `test_the_old_pin_cannot_check_the_revised_graph_and_the_new_pin_can` stages
  one `SupplierOrderState` against the graph read under the revised contract
  and shows `PrologVerifier` on the old pin raising `LogicError: Logic contract
  and compiled facts use different ontologies` while the same rule bytes
  re-pinned return `SATISFIED` with zero violations. That second test is the
  census's step-5 isolation, reproduced inside Core; it is skipped where
  `swipl` is absent.
- GREEN `bb3dd75400e7756b40e84c33b435f8b3f344a154`: the module passes 14, and
  with `test_contract_revision.py` and `test_small_shop_contract_revision.py`,
  24.
- `2bbfad891aa2ad9d0d059eaa07469a665b44917f` adds
  `test_a_profile_change_the_field_walk_cannot_see_still_refuses`, and
  `158d5d8c` adds `test_a_re_pin_without_an_ontology_change_cannot_be_expressed`
  after correcting a claim these documents made from reading rather than from
  running. The module collects 16.

The positive path, `test_a_revision_carries_the_re_pinned_check_contract_and_
later_checks_run`, admits one `SupplierOrderState` after the revision using the
re-pinned check identity, reopens from disk, and asserts the recorded
re-binding's two profile identities, the two check identities, the derived
`rebound_field`, the independently recomputed `unchanged_fields_digest`, the
change kinds `{ADD_CLASS, ADD_SLOT, REBIND_CHECK_CONTRACT}`, that the
pre-revision change set still binds the old contract identity while the new one
binds the target, and the graph and receipt after reopen.

`test_the_earlier_check_receipts_keep_the_identity_they_were_recorded_under`
compares the `CheckRecord`s in the machine state before and after the revision:
they are equal, still name the old check contract identity, still read
`SATISFIED`, while `required_checks` names the new one. Archival verification
does not move when the live selection does.

## The accessor a runner reads

`KnowledgeHistoryReplay.required_checks` maps each policy reference to that
policy's `((check_contract_id, check_contract_identity), ...)`. After a revision
carried a re-binding the identity here is the re-pinned one, so a runner loads
the contract that hashes to it instead of an identifier it chose once. The D0
runner's fixed `LOGIC_ID` is adopter code and was not touched; the line it needs
is `replay.required_checks["required-check-verdict"]` for its own policy
reference.

## Exclusions, stated

- Core runs no rule and produces no check outcome. It compares declared
  identities. A `SATISFIED` receipt still comes from the adopter.
- Nothing here admits a new required check, retires one, changes what a verdict
  means, or migrates a policy whose rules actually changed. That is the general
  policy migration `docs/IMPLEMENTATION_STATUS.md` still says does not exist.
- A re-pin with no ontology change cannot be expressed. The one field that may
  move must move from the current ontology's content hash to the target's, so
  when the ontology stands still no field can differ. A check contract that
  bumps its own version instead is refused `check contract <id> does not pin the
  current ontology in exactly one changed field`, pinned by
  `test_a_re_pin_without_an_ontology_change_cannot_be_expressed`. An earlier
  draft of this file said the refusal was `NON_ADDITIVE_CHANGE` from
  `_derive_changes`; that was read off the code rather than run, and it is
  wrong: the re-binding gate runs first.
- Core never verifies that a descriptor describes a real file on disk. It
  verifies the descriptor hashes to the identity the policy requires, which is
  the same guarantee the policy already had.
- No adopter runner, no research file and no paper file was changed. The census
  was not re-run; it is read-only evidence here.
- Cross-language parity of the extended revision grammar is not established.

## Core's default test suite

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -ra -p no:cacheprovider
```

At `bda2e408` with `docs/index.md` already updated: **27 failed, 3486 passed,
3 skipped** in 13:19. Collection is 3,516, which is 3,500 at `d867c3ab` plus
this candidate's 16 and nothing else.

Every failure is accounted for, counted rather than sampled.

- **24 are the governance gate**, and all 24 reach the same first mismatch:
  `LedgerValidationError: OVR-000453: latest document digest mismatch for
  docs/contract_compiler/index.md`. That string appears exactly 24 times in the
  run. They are seven in `tests/test_contract_compiler_ledger.py`, fourteen in
  `tests/test_contract_compiler_integration.py` and three in `tests/test_docs.py`,
  the same three Sphinx builders that call the same validation. Sealing the
  block below removes all 24.
- **3 are frozen-evidence failures this candidate did not cause**:
  `tests/contract_compiler/pareto/test_fresh_shop_import.py::test_fresh_import_replays_and_traces_after_complete_shop`
  and the two in `research/.../small_shop/public_population/test_run.py`, each
  `AssertionError: Output bytes differ: <group>/evidence.json` from
  `evidence_assertions.py:47`. The controlled comparison: the same three tests
  run in this same worktree, once with this candidate's `src/` on the import
  path and once with `d867c3ab`'s own `src/` extracted beside it, give **3
  failed, 12 passed** both times with identical messages. Core is not the
  variable.

  One thing about them is unexplained and is stated rather than smoothed over.
  A `git archive` of `d867c3ab` unpacked as its own tree passes them. So the
  discrepancy depends on something about this checkout rather than on Core, and
  what that is was not found. The produced `fresh_import/evidence.json` differs
  from the committed one in exactly three values, `ledger_head`,
  `ledger_sha256` and `receipt_identity`, so the produced history really does
  differ; it is not a formatting or timestamp artifact. That belongs to whoever
  owns the frozen Shop evidence, and this candidate did not overwrite it.

The three skips are the two `tests/test_ontology.py` LinkML-CLI resolver skips
and the absent private paper-program doctrine, the same three the previous
Core report names.

## Ruff

`ruff 0.11.9`, the pinned version. `ruff check` and `ruff format --check` both
pass on every changed Python file. All three files had zero format drift at
`d867c3ab` and have zero now, so this candidate introduced none. Two findings
its own first draft introduced, an unused `ROOT` import and an unused
`before_receipts` local, were removed in `2bbfad89` rather than left.

## The governance gate, and the block that closes it

`scripts/contract_compiler_ledger.py` records, per path, the latest
`after_digest` any `DOCUMENT_REVISION` block declared, and `_validate_semantics`
then requires every one of those paths to hash to that value today. Eight of the
files this work changes are among them, so `check` fails, every caller of
`load_ledger` fails, and the 24 tests that call it fail with them. The fix is one
appended block, `head.json` re-pinned and `status.md` re-rendered. That is an
overseer act; this session was not given that authority and did not take it.

The block below is schema-valid: it was checked with `jsonschema` 4.26.0
against `design/contract_compiler/overseer/ledger.schema.json` with
`recorded_at` and this file's `after_digest` replaced by schema-shaped
stand-ins for the check only, and `why` is 1,180 characters against the 1,200
limit. Every `before_digest` was verified to equal the `after_digest` the
current ledger records for that path at `d867c3ab`, so the block chains.

The sealer fills `recorded_at` with the sealing moment, takes `after_digest`
for this file once it is final, and computes `entry_hash` with
`python scripts/contract_compiler_ledger.py hash` before binding it in
`head.json` and running `render` then `check`.

Two judgments the sealer owns, not this session:

- `affected_ids` and the `AFFECTS` reference carry `CC-R11` because
  `OVR-000461` and `OVR-000462` do. If this belongs to a different workstream,
  that is the sealer's call.
- `OVR-000463` and `previous_entry_hash` are correct against this worktree's
  head only, which is `OVR-000462` at
  `sha256:4f9d572b…0966b`. An integrator must reconcile against the
  then-current shared head rather than copy a conflicting number.
- `tests/contract_compiler/pareto/test_check_contract_rebinding.py` is listed
  `CREATED` because the file is genuinely new. No prior block records it, so
  `check` does not require it today; listing it starts the ledger tracking it.
  Leaving it out is also defensible and is the sealer's call.

```json
{
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "entry_id": "OVR-000464",
  "ledger": "overseer",
  "sequence": 464,
  "entry_type": "DOCUMENT_REVISION",
  "previous_entry_hash": "sha256:044e08c8a68fda40bb3c75fb7b248ff256cbae403c42f535f3d61e14caaf8e59",
  "recorded_at": "<sealing moment, UTC>",
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "subject": {
    "id": "core-policy-rebinding",
    "type": "DOCUMENT"
  },
  "summary": "Let an additive contract revision carry the re-binding of the selected policy's required check contracts to the target ontology.",
  "why": "E-0458. A policy whose required check contract pins the compiled ontology inside its own digest made ontology growth impossible for that adopter: re-pinning the same rule bytes moved the check identity, the policy and the normative profile, so the revision refused INCOMPATIBLE_CONTRACT, and keeping the old pin left the check unable to execute against the revised graph. Luis ruled the fix is a declared recorded act, not a loophole. A revision may now carry check_contract_descriptors under the new REBIND_CHECK_CONTRACT kind. Core recomputes both declared identities, requires exactly one field to differ and to move from the current ontology's content hash to the target's, and requires undoing the re-binding to reproduce the current profile byte for byte. Changed rule bytes, an added or removed check, a changed verdict, precedence, identifier or machine program each refuse naming what moved. Earlier check receipts keep their recorded identities. Declaring a kind moved the revision policy's digest, so both stay executable by declaration and every recorded revision still replays. RED b01a165a 12 failed 2 passed; GREEN bb3dd754. Core runs no rule: not policy migration.",
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "path": "CHANGELOG.md",
        "change": "MODIFIED",
        "before_digest": "sha256:afae9a902ee11b94b1049a6f5fa21e95f75a3e49c1016f27228097552b0c71d8",
        "after_digest": "sha256:9c216950a24b79a26db18fe22a926fdab3aa7acbc3188b6247260ac7a037a241"
      },
      {
        "path": "docs/IMPLEMENTATION_STATUS.md",
        "change": "MODIFIED",
        "before_digest": "sha256:0998e707949bfb4f2482ad957619b2f1bb16bc2c7f985adbc6bf5399b5d2ec70",
        "after_digest": "sha256:7711f7ff8d3d1fb4cbe3ebc8c448cd1281529f82e85add0245f7a499459a2caa"
      },
      {
        "path": "docs/contract_compiler/index.md",
        "change": "MODIFIED",
        "before_digest": "sha256:2d56b96be1367412881409d0461b7406f21414f5cd50954b408163d40573c9ec",
        "after_digest": "sha256:e74485f203b8f0859f50b9e097740afadf0aa049ce51e73f31a74041417f2232"
      },
      {
        "path": "docs/index.md",
        "change": "MODIFIED",
        "before_digest": "sha256:7457c4a72503cffd945c68c53c503644e3b3630e4ff733ef7112dd43a4d9fc19",
        "after_digest": "sha256:c87b021e2e1a28e54bf7e7bf086a7598577aa3c218d9574f65b6f52d2556ddd5"
      },
      {
        "path": "handover/2026-09-17-core-policy-rebinding.md",
        "change": "CREATED",
        "after_digest": "<digest of this file once final>"
      },
      {
        "path": "src/malleus/_contract_pipeline/knowledge.py",
        "change": "MODIFIED",
        "before_digest": "sha256:d4ac8be73cde6a3058c854c6c20c8a40afd76874706886c5b7e5c1b4bf81cd68",
        "after_digest": "sha256:15b3991fb349d72007f4742bc9bd060453d640f92fbb70f1abd880b1adc1f960"
      },
      {
        "path": "src/malleus/_contract_pipeline/revision.py",
        "change": "MODIFIED",
        "before_digest": "sha256:3e2148df0b3e69ba78eaa1e6f185bebfc5aa51d0cd3bbfbf88606213c90214c2",
        "after_digest": "sha256:e3bc83a7800ef0bb7157af0941cfd0484dfce5a743db24476650ada11f6d5332"
      },
      {
        "path": "src/malleus/compiler.py",
        "change": "MODIFIED",
        "before_digest": "sha256:59087977064c36050a6c9189804e5798e3a3bea5eb00d3ad53dfee0ca382f095",
        "after_digest": "sha256:0da568741f94ecb3582a38f0b1a39eca9e3e7927f9bbe22218fda9667c415145"
      },
      {
        "path": "tests/contract_compiler/pareto/test_check_contract_rebinding.py",
        "change": "CREATED",
        "after_digest": "sha256:b124b9c161b57a3e933c37e555784892f3d45dabc3baca913501976e54894503"
      },
      {
        "path": "tests/contract_compiler/pareto/test_contract_revision.py",
        "change": "MODIFIED",
        "before_digest": "sha256:7a4fe8f20c667785ba2bae2391a89e81015dcfcdb669309d15bbe27b5c33b48a",
        "after_digest": "sha256:b79a7799841581683f788bbc726a5b33195c9d0de3d1073d1f598f784edf1c20"
      }
    ]
  },
  "references": [
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "0becb6936534a5151001fd7bb551edbc4c1aefba"
    },
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "7b86516d74744832bd2ac2b1538e05826e296637"
    },
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "b01a165aafe6501be8f60a22a89113a020f83e76"
    },
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "bb3dd75400e7756b40e84c33b435f8b3f344a154"
    },
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "77cbf024a441ef1c3bb3e0ab95f595a8868bd215"
    },
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "2bbfad891aa2ad9d0d059eaa07469a665b44917f"
    },
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "158d5d8c331d8a2d78c2c62676b6cd4454d1a54d"
    },
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "bda2e408b2bad859603d6ca4a3d132a18e74ef3a"
    },
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "8bb13ea6a4d201d0f14d72908e776b99b7746eb6"
    },
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "c70e97ce8b64e09e1d43e8421ab52a0bd60cc67b"
    },
    {
      "relation": "AFFECTS",
      "type": "WORKSTREAM",
      "target": "CC-R11"
    }
  ],
  "entry_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
}
```

The `entry_hash` above is a placeholder of the right shape, present only so the
draft validates as a complete entry. It is not a hash of anything. The documentation
commits that finalize this file are absent from the reference list for the same
reason its `after_digest` is a placeholder: a file cannot name the commits that
write it. `git log --reverse d867c3ab..HEAD` on the branch lists every commit;
the sealer adds the missing ones alongside the sealing commit.

## What was not done

- The block above was not sealed. Nothing under
  `design/contract_compiler/overseer/` was touched.
- `.claude/skills/malleus-dev/references/CAPABILITIES.md` does not exist in
  this worktree; another agent is creating it on `main`. The line to add, once
  it does:

  > **Check-contract re-binding across an additive revision** ·
  > `malleus.compiler.KnowledgeChangeHistory.compose_contract_revision(...,
  > check_contract_descriptors=...)` · LANDED. An additive revision carries the
  > re-pinning of the selected policy's required check contracts to the target
  > ontology when only the ontology binding inside them moves; read the current
  > selection with `KnowledgeHistoryReplay.required_checks`. Not policy
  > migration: changed rule bytes, an added or removed check, or a changed
  > verdict still refuse.

- The census was not re-run and nothing under
  `private/shop-progressive-01/` was written. It was read only. Each census
  workspace pins its own Core through its runner's runtime export, so it will
  not see this branch until that export is rebuilt. Note also that
  `tools/census.py` declares no re-binding: against new Core its
  `test_a_repinned_rule_layer_refuses_and_writes_nothing` still passes, and
  correctly so. Rerunning the census as a capability check means teaching
  `census.revise` to pass `check_contract_descriptors` built from the loaded
  `LogicContract`'s ten semantic fields.
- The D0 runner's fixed retained rule ID was not changed; it is adopter code.
- Nothing outside this worktree was modified, nothing was pushed, no branch was
  reset and nothing was stashed or deleted.

## Sealer's addition, 2026-09-17

Renumbered from the provisional OVR-000463 to OVR-000464 after the capability-declaration entry took 463 (head 044e08c8…). Before-digests updated to the ledger's latest recorded values and after-digests recomputed from main at the merge commit 0becb693 for: CHANGELOG.md before e52e4edf2dd7->afae9a902ee1; CHANGELOG.md after 4701b9a0e910->9c216950a24b; docs/IMPLEMENTATION_STATUS.md before 0487eb3fa481->0998e707949b; docs/IMPLEMENTATION_STATUS.md after e697253ee05e->7711f7ff8d3d; src/malleus/compiler.py before 93c7b6ea6cc1->59087977064c; src/malleus/compiler.py after 2f91d42f1818->0da568741f94.

## Sealing note for OVR-000464, 2026-09-18

`entries/OVR-000464.json` was sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment
and this file's digest filled in.

## OVR-000466 draft, the Small Shop successor evidence generation

The revision policy identity this change moved forced a successor Small Shop evidence generation (commit 620f3b2b); the two pinned files are recorded here.

```json
{
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "ledger": "overseer",
  "entry_type": "DOCUMENT_REVISION",
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "subject": {
    "id": "core-capability-declaration",
    "type": "DOCUMENT"
  },
  "entry_id": "OVR-000466",
  "sequence": 466,
  "previous_entry_hash": "sha256:fc623656b78d635b55740b538f16dcaca56715e25e8905c5d0a71137f99470c1",
  "recorded_at": "<sealing moment, UTC>",
  "summary": "Record the Small Shop successor evidence generation forced by the revision policy identity moving at OVR-000464.",
  "why": "OVR-000464 declared a fifth contract-revision change kind, REBIND_CHECK_CONTRACT, and the revision policy is content-addressed over its declared kinds, so CONTRACT_REVISION_POLICY.identity moved from 05b68805 to e129b6e8 and every recompiled revision records the new one. The Small Shop's frozen evidence and its connected-story warehouse boundary were cut against the old identity and refused to reproduce (three evidence tests and the fourteen paper calibration tests behind them). Per the ruling that Core is not frozen for its own sake, a successor generation evidence_2026_09_17_policy_rebinding regenerates the five scenarios at 5cc211a6, keeps the 2026-09-08 generation pinned, retargets CURRENT, and re-freezes the chain's boundary and three receipts with the superseded values recorded; only ledger coordinates moved, no domain value. Two pinned files change: evidence_assertions.py and test_current_evidence.py (historical_outputs 20 to 30). small_shop plus fresh import: 371 passed. Lesson recorded: a moved content-addressed policy digest moves every frozen artifact that records a ledger coordinate, and the check is regenerating the family, not grepping. Paper ledger E-0464, E-0466.",
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/evidence_assertions.py",
        "change": "MODIFIED",
        "before_digest": "sha256:d60bdfb87f386e0a142ae29bef26ac3e28fd4763b5052043f025a524fd738fcd",
        "after_digest": "sha256:0d04ddd11d2de303b7502a4e3287627d6eafa2d81e4c78cca213b1b699b3bfc1"
      },
      {
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/test_current_evidence.py",
        "change": "MODIFIED",
        "before_digest": "sha256:0f1edd1be8ab09c74cdcf9c95cabbb958e30801eaacad2b977ddc575ea02f397",
        "after_digest": "sha256:258d7d77b09248d6315e102fa4a14871b531f24f9951712024c102b010211d06"
      },
      {
        "path": "handover/2026-09-17-core-policy-rebinding.md",
        "change": "MODIFIED",
        "before_digest": "sha256:05c81ccc98350011f875a309a55be4006c0a922ab39a2885c439a0e047724db2",
        "after_digest": "<digest of this file once final>"
      }
    ]
  },
  "references": [
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "620f3b2b9e7a523589c24b81e351c569d88970f1"
    },
    {
      "relation": "AFFECTS",
      "type": "WORKSTREAM",
      "target": "CC-R11"
    }
  ],
  "entry_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
}
```

## Sealing note for OVR-000466, 2026-09-18

`entries/OVR-000466.json` was sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment
and this file's digest filled in.

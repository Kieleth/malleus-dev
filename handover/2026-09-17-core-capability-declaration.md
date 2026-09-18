# Core's capability declaration, and the two vocabularies that were hidden

2026-09-17. Core session, working tree only. Nothing staged, nothing committed,
nothing under `private/` run or touched. The paper ledger, the master plan, the
manuscript and `paper-v4/AGENTS.md` are unchanged.

Luis's order: "That core has capabilities we're not using in shop is just
plainly wrong, we work on core so that we can use them." Then: understand why
Core has capabilities the consumer projects do not use, and implement fixes,
which probably includes a declaration of capabilities in the skill so it is
clear what Core can do or not, and instructions that those need to be used at
full when limitations are encountered.

## 1. The inventory

`.claude/skills/malleus-dev/references/CAPABILITIES.md`, 45 rows, six columns:
capability, public entry point, one plain sentence, status, protocol role from
the closed taxonomy of `docs/PRINCIPLES.md`, and the section of
`docs/IMPLEMENTATION_STATUS.md` that carries the boundary statement.

**Implemented, compiler and history path.** Compiled LinkML contracts and their
identity; closed-world ontology and typed-graph validation; ontology source
closure; population plans with 38 closed refusal reasons; the six typed gap
kinds; the document capture adapter and its two-axis census with 17 refusal
reasons; three domain-history profiles; governed history and atomic structural
admission; source and evidence retention anchors; reopen and replay; the
maintained in-memory read projection; record provenance trace; explicit
supersession; the change-set composer; additive ontology revision on a live
history with a migration receipt; valid time and transaction time; identified
machine and policy artifacts with a reference executor; knowledge packs and the
grounding rite; the `malleus-compiler` CLI.

**Implemented, other.** The Prolog fact contract v3 and pinned logic contracts;
the Assent stack (state machines, ledger, staging, typed monitors and epistemic
policy, bitemporal accepted graph, authorization control, evidence records,
review-report recording, Stage 8a declared source identity, Stage 8b adapter
orchestration, Stage 8c dispatch, receipt and observation); Recon's typed
literature ledger and deterministic artifact builds; the OCR evidence-integrity
profile, capability `AUDIT_ONLY`; payload-grammar identity of a schema; the
declared interpretation-review coverage checker.

**Partial.** The experimental finite-program action history. Migration receipts
and migration-aware reads, which carry no transform and no verified delta.

**Not implemented, 18 rows.** The 15 IDs in
`malleus.IMPLEMENTATION_STATUS.pending_capabilities`, plus three the ledger and
the roadmap record and the status document does not: the per-slot source
relation (E-0430), a supersession reason field (E-0456), and provisional
concepts (`ROADMAP.md` A6, with Recon named as the blocked consumer in D1).

## 2. The consumer survey

SHOP is `research/ontology_driven_kg_realization/experiments/small_shop/`.
STAGED is `private/shop-progressive-01/d0/`, read only. PAPER is
`paper-v4/experiment-v4/`. RECON is the `research/*_recon/` projects.

| Capability | SHOP | STAGED | PAPER | RECON |
|---|---|---|---|---|
| Compiled contracts, plans, admission, replay | USED | USED | USED | n/a, own ledger |
| Typed gap kinds | USED | WORKED_AROUND | USED | n/a |
| Document capture adapter | n/a, structured source | n/a, structured source | USED | n/a |
| Domain-history profiles | USED | USED, custom profile | USED | n/a |
| Maintained read projection | USED | UNUSED | UNUSED | n/a |
| Record provenance trace | USED | UNUSED | USED | n/a |
| Supersession | USED | USED | UNUSED, not needed | n/a |
| Change-set composer | USED | UNUSED | UNUSED | n/a |
| Additive ontology revision | USED | WORKED_AROUND | UNUSED | UNUSED |
| Prolog check contract | USED | USED | USED | UNUSED |
| Packs and the grounding rite | USED | USED | USED | n/a |
| Review-coverage checker | UNUSED | USED, refused | UNUSED | UNUSED |
| Assent stack | UNUSED | UNUSED | UNUSED | UNUSED |
| Migration receipts and verifier | UNUSED | UNUSED | UNUSED | USED indirectly |
| Recon family | n/a | n/a | n/a | USED |
| Provisional concepts | not implemented | hits the supersession-reason absence | n/a | named blocked consumer |

Evidence for the USED cells, by file: `small_shop/partial_shipments/run.py:209`
and `small_shop/connected_story/partial_shipments/run.py:92` for additive
revision; `small_shop/connected_story/test_connected_run.py:147` for the
maintained projection; `small_shop/partial_shipments/run.py:297` and
`paper-v4/experiment-v4/run-23/run.py:105` for the trace;
`private/shop-progressive-01/d0/runner.py:224` for the custom profile and
`:609` for `admit_with_anchors`; `private/shop-progressive-01/d0/obligations.py:276`
for the checker; `private/shop-progressive-01/d0/rule_layer.py:90` for the
logic contract.

## 3. Root causes

1. **Additive revision, STAGED.** Zero occurrences of
   `compose_contract_revision`, `record_contract_revision` or "additive"
   anywhere under `private/shop-progressive-01/d0/` or its `design/`. The
   stage-C design plans a `TYPE_ABSENT` gap, and E-0456 records that a contract
   change on an existing history is something "nobody has measured here", while
   `small_shop/partial_shipments` has run exactly that path on a live history
   since 0.14.0. The procedure never named the capability, and no list an agent
   reads first named it either. Contributing: the acolyte skill's step 9 names
   only the low-level `compile_contract_revision`, never the two
   `KnowledgeChangeHistory` methods that bind the live history's base
   coordinates for the caller.
2. **Gap kinds, STAGED.** `_GAP_KINDS` was a private frozenset with no public
   accessor, and `UNKNOWN_GAP_KIND` named only the rejected value. The
   vocabulary had exactly two routes: the acolyte skill's `accepted_gap_kinds`
   block, kept in sync by `tests/test_inquisition.py:2535`, or private code.
   PAPER producers succeed because `run-23/spawn-message.md` tells them to read
   the installed acolyte skill. The STAGED producer reads a hand-written
   procedure (`d0/producer.py:60`) that never mentions the skill, so it probed
   about 5,700 values (E-0438), and the runner was then patched to import the
   private name.
3. **Boundary identity, STAGED.** The only route to a review's required
   `boundary_identity` was calling `check_review_coverage` with an empty review
   tuple and reading the receipt, stated once in a docstring. The refusal named
   no route. Three archived reviews of a launched stage were refused (E-0452).
   Compounding: the checker was absent from `docs/IMPLEMENTATION_STATUS.md`,
   which is the one document the malleus-dev skill names before capability
   claims.
4. **General.** Older Shop cells (`correction/`, `pareto/`, `showcase/`) import
   `malleus._contract_binder`, `malleus._contract_pipeline.knowledge` and
   `malleus._contract_source` directly rather than the `malleus.compiler`
   facade. The facade arrived after them and nothing listed what it now covers.

## 4. What changed

The declaration, referenced from the top of all three skills with Luis's rule
in his words: when a limitation is encountered in a consumer project, read the
declaration and use the capability in full before declaring a gap, writing
adopter code, or working around it; a gap is declared only when the declaration
says the capability does not exist, and then it is filed as a Core requirement.

The mechanical guard, `tests/test_capability_declaration.py`, anchored on
`malleus.IMPLEMENTATION_STATUS` (the status document's own line 7 names it as
its machine-readable source) and on the `## ` section headings of
`docs/IMPLEMENTATION_STATUS.md`. Every entry point must import, every landed
capability ID must appear, every pending ID must be marked `not implemented`,
every section must be declared or listed in the test as carrying none, and each
of the three skills must carry the pointer and the rule.

The two hidden vocabularies: `malleus.compiler.POPULATION_GAP_KINDS` and
`malleus.acquisition.review_boundary_identity`, with both `UNKNOWN_GAP_KIND`
refusals naming every permitted kind and the boundary-identity refusal naming
its accessor.

Two documentation defects the guard found: `docs/IMPLEMENTATION_STATUS.md` named
a Stage 8a helper `source_artifact_fields_from_bytes`, a name no shipped module
defines, and omitted the review-coverage checker that shipped with the work
bound in `25f94cbf`. Both corrected, with the checker also added to
`CHANGELOG.md` under `[Unreleased]`.

The `malleus-paper` skill, created earlier today and never wired into Core's
skill rites, now carries `agents/openai.yaml`, a `## Before you build` scope
gate, and its packaging entries.

### Files, with before and after sha256

`before` is the digest the overseer ledger last recorded for the path, which is
also this checkout's `HEAD` content. `after` is the working tree.

| File | before | after |
|---|---|---|
| `.claude/skills/malleus-acolyte/SKILL.md` | `sha256:f0f24ed896c1433c1d56fceaa00ada291a7acc44b840f5283b0a328eba5841ba` | `sha256:5b050ba92c9849d9377b51a82c01e67ed2549a6e3ec9b4f9967a8113c573a1d4` |
| `.claude/skills/malleus-dev/SKILL.md` | `sha256:09cd92fec20f5c365fff5a8b537b31e1642c9043ba424fe26e099c3433d5ea96` | `sha256:67197a1c5d1ad9b2f1c7c66fa200ba8afe07d825eea77cd10f4fbb3ac3a987b2` |
| `CHANGELOG.md` | `sha256:e52e4edf2dd7de4cd8584e0ba049dd2379963360e68d6a3fa96272950b6bf73e` | `sha256:afae9a902ee11b94b1049a6f5fa21e95f75a3e49c1016f27228097552b0c71d8` |
| `docs/IMPLEMENTATION_STATUS.md` | `sha256:0487eb3fa4814afbba9672e8ea939cb2e747ac7156d6f1f8f3337f5b87f63bca` | `sha256:0998e707949bfb4f2482ad957619b2f1bb16bc2c7f985adbc6bf5399b5d2ec70` |
| `pyproject.toml` | `sha256:385d8a816e5931c3014d1b5e6c281b4ae73260a03b37b1a97b11becd9c0d91d1` | `sha256:6d78a1a76564bb487b26f9bfe97e60b0b6706a002d1056e97dabbaf5037a997f` |
| `src/malleus/_contract_pipeline/document.py` | `sha256:0f5463bca8578ec9e7db3bb7d892bc5f4195e6e084411e556b375c9ce09b649d` | `sha256:02159c937eaddeafeb3d4e20594b569a81f10e53c630f6b0957e6574df227f6d` |
| `src/malleus/_contract_pipeline/population.py` | `sha256:16d73c588fc29412044c5cebe9c6f43f5733f221c73133a759c1bf57ae769411` | `sha256:65813f59732134a7dda63ebd3e207509874278ded5594a8d62ade1cf4c5ea128` |
| `src/malleus/acquisition.py` | `sha256:427dc5ed1b55068c2221d5dcf11c4d8b6afd691599c046e291b9b2934df7a7cb` | `sha256:9d2c4b68c98e398fc0ce6367d0e7c7834e14e9b9cf012d5336b25e153040e127` |
| `src/malleus/compiler.py` | `sha256:93c7b6ea6cc117da2c63322c1ed79fd5299d6a94767fc61bf52ac1b8ea53da63` | `sha256:59087977064c36050a6c9189804e5798e3a3bea5eb00d3ad53dfee0ca382f095` |
| `tests/contract_compiler/pareto/test_document_assertion_adapter.py` | `sha256:7421dd426a6bab3e81951330fceacf66319635946148840689b2c45aba2e9003` | `sha256:26d1f654cc4e461619a7b31ff24060d22ef6393c9e19868e4ad5b0d95d9c8a79` |
| `tests/contract_compiler/pareto/test_population_plan.py` | `sha256:4819623b8d72d4836b3e24a759e1ee1fa06926c07b35aad7b4ad7ebce53e7877` | `sha256:1a663a98ccc5a93269e408faf6d69e4f55c3985e74609f3067f5c60a62e0a310` |
| `tests/contract_compiler/pareto/test_review_coverage.py` | `sha256:c78ffc2d8da3bdad02d0f1db8f0075db1190a7c073fbed92f5d6a0f32d87754a` | `sha256:87d18028d83dd7388d6e2000bdba6360ccc994239e4687421a41dceef300ba88` |
| `.claude/skills/malleus-dev/references/CAPABILITIES.md` | created | `sha256:dcc483be27ca5d563d9b722eb727d36b3d12a852fc675a1d3c11cc61a5820cfb` |
| `.claude/skills/malleus-paper/SKILL.md` | created | `sha256:5c43070ad7c170df78013cc7932fa8e410d3683c58d18e1c57dd1f31d49b2b5a` |
| `.claude/skills/malleus-paper/agents/openai.yaml` | created | `sha256:e53501b7b24764b2e85bb8950eed1728a3f8eed45380926c33a208f38f15b209` |
| `tests/test_capability_declaration.py` | created | `sha256:20a8f71dc89a695455ae31f01418660f3de38470325025032e4cbb2a86efc8b4` |

`.claude/skills/malleus-paper/SKILL.md` is marked created because the ledger has
never recorded it and git has never tracked it. Its body was written by the
paper-front session earlier today (E-0431); this session added only the
`## What Core can do` pointer and the `## Before you build` scope gate. Whoever
seals should read it as the paper front's document receiving its first
governance record, not as this session's authorship.

## 5. The block this needs, drafted and not sealed

Sealing is the overseer's act and is not done here. The draft below is
schema-valid: it was checked with `jsonschema` against
`design/contract_compiler/overseer/ledger.schema.json`, with `recorded_at` and
this file's `after_digest` replaced by schema-shaped stand-ins for the check
only. The verdict was VALID with zero errors. `why` is 1,191 characters against
the 1,200 limit; `summary` is 192 against 240; `documents` holds 17 against the
maximum of 20.

Notes the sealer owns, not this session:

- **The entry number is provisional.** A Core agent is drafting another entry in
  a separate worktree. `OVR-000463` and `previous_entry_hash` are correct
  against this checkout's head only, which is `OVR-000462` at
  `sha256:4f9d572b9c1d775919bca52e273ccaca8c11821a3859152dea62e0169490966b`.
  The Overlord reconciles numbering at sealing; do not copy a conflicting
  number.
- **There is no commit for this work yet.** Nothing was staged or committed, so
  no commit can evidence the RED and GREEN steps. The schema requires at least
  one reference, so the single `EVIDENCES` reference names main's
  `d867c3abf31420607da02070b45d0852d3f81227`, the base this working tree sits
  on, not the change itself. The sealer should add the actual RED and GREEN
  commit refs once they exist, and may then drop the base reference.
- `affected_ids` and the `AFFECTS` reference carry `CC-R11` because
  `OVR-000459` through `OVR-000462` carry it. If a capability declaration
  belongs to a different workstream, that is the sealer's call.
- `ROADMAP.md` is also mismatched against its pin from `OVR-000365`
  (`sha256:ffe6c96e01f4aeee55ab8bc6bad8ffe76142747feceafa3a4bb38b729aa3fa17`
  recorded, `sha256:891c9529a77a0cd999c55e42f63ab9f3ce39fa46c46be63024dd6f7af01733aa`
  on disk). That file was already modified when this session started and this
  session never opened it. It is deliberately **not** in this entry; it needs
  its own from whoever changed it.
- The sealer fills `recorded_at` with the sealing moment, takes `after_digest`
  for this file once it is final, and computes `entry_hash` with
  `python scripts/contract_compiler_ledger.py hash` before binding it in
  `head.json` and running `render` then `check`.

```json
{
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "entry_id": "OVR-000463",
  "ledger": "overseer",
  "sequence": 463,
  "entry_type": "DOCUMENT_REVISION",
  "previous_entry_hash": "sha256:4f9d572b9c1d775919bca52e273ccaca8c11821a3859152dea62e0169490966b",
  "recorded_at": "<sealing moment, UTC>",
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "subject": {
    "id": "core-capability-declaration",
    "type": "DOCUMENT"
  },
  "summary": "Declare Core's shipped capability surface to the skills, make the gap-kind and review-boundary-identity vocabularies public, and record the review-coverage checker the status document omitted.",
  "why": "Luis: \"That core has capabilities we're not using in shop is just plainly wrong, we work on core so that we can use them.\" Three workarounds on 2026-09-17 each hid a shipped capability: a staged run planned a TYPE_ABSENT gap while additive contract revision already runs on a live Shop history; a launched producer searched for the six gap kinds, which lived in a private frozenset; three archived reviews were refused because a review's boundary_identity had no named route. CAPABILITIES.md declares 45 capabilities with entry points and status, referenced from the three skills with the rule: meet a limitation by using the capability in full before declaring a gap. tests/test_capability_declaration.py holds it honest against malleus.IMPLEMENTATION_STATUS IDs and the status headings: RED 10, GREEN 11. POPULATION_GAP_KINDS and review_boundary_identity expose existing vocabulary, and both refusals now name their permitted values or route. No admitted value, refusal reason, profile, ontology or pin changes. The status document gains the review-coverage checker omitted since 25f94cbf and loses a helper name no module defines. Local governance only; reconcile against the shared head.",
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "path": ".claude/skills/malleus-acolyte/SKILL.md",
        "change": "MODIFIED",
        "before_digest": "sha256:f0f24ed896c1433c1d56fceaa00ada291a7acc44b840f5283b0a328eba5841ba",
        "after_digest": "sha256:5b050ba92c9849d9377b51a82c01e67ed2549a6e3ec9b4f9967a8113c573a1d4"
      },
      {
        "path": ".claude/skills/malleus-dev/SKILL.md",
        "change": "MODIFIED",
        "before_digest": "sha256:09cd92fec20f5c365fff5a8b537b31e1642c9043ba424fe26e099c3433d5ea96",
        "after_digest": "sha256:67197a1c5d1ad9b2f1c7c66fa200ba8afe07d825eea77cd10f4fbb3ac3a987b2"
      },
      {
        "path": "CHANGELOG.md",
        "change": "MODIFIED",
        "before_digest": "sha256:e52e4edf2dd7de4cd8584e0ba049dd2379963360e68d6a3fa96272950b6bf73e",
        "after_digest": "sha256:afae9a902ee11b94b1049a6f5fa21e95f75a3e49c1016f27228097552b0c71d8"
      },
      {
        "path": "docs/IMPLEMENTATION_STATUS.md",
        "change": "MODIFIED",
        "before_digest": "sha256:0487eb3fa4814afbba9672e8ea939cb2e747ac7156d6f1f8f3337f5b87f63bca",
        "after_digest": "sha256:0998e707949bfb4f2482ad957619b2f1bb16bc2c7f985adbc6bf5399b5d2ec70"
      },
      {
        "path": "pyproject.toml",
        "change": "MODIFIED",
        "before_digest": "sha256:385d8a816e5931c3014d1b5e6c281b4ae73260a03b37b1a97b11becd9c0d91d1",
        "after_digest": "sha256:6d78a1a76564bb487b26f9bfe97e60b0b6706a002d1056e97dabbaf5037a997f"
      },
      {
        "path": "src/malleus/_contract_pipeline/document.py",
        "change": "MODIFIED",
        "before_digest": "sha256:0f5463bca8578ec9e7db3bb7d892bc5f4195e6e084411e556b375c9ce09b649d",
        "after_digest": "sha256:02159c937eaddeafeb3d4e20594b569a81f10e53c630f6b0957e6574df227f6d"
      },
      {
        "path": "src/malleus/_contract_pipeline/population.py",
        "change": "MODIFIED",
        "before_digest": "sha256:16d73c588fc29412044c5cebe9c6f43f5733f221c73133a759c1bf57ae769411",
        "after_digest": "sha256:65813f59732134a7dda63ebd3e207509874278ded5594a8d62ade1cf4c5ea128"
      },
      {
        "path": "src/malleus/acquisition.py",
        "change": "MODIFIED",
        "before_digest": "sha256:427dc5ed1b55068c2221d5dcf11c4d8b6afd691599c046e291b9b2934df7a7cb",
        "after_digest": "sha256:9d2c4b68c98e398fc0ce6367d0e7c7834e14e9b9cf012d5336b25e153040e127"
      },
      {
        "path": "src/malleus/compiler.py",
        "change": "MODIFIED",
        "before_digest": "sha256:93c7b6ea6cc117da2c63322c1ed79fd5299d6a94767fc61bf52ac1b8ea53da63",
        "after_digest": "sha256:59087977064c36050a6c9189804e5798e3a3bea5eb00d3ad53dfee0ca382f095"
      },
      {
        "path": "tests/contract_compiler/pareto/test_document_assertion_adapter.py",
        "change": "MODIFIED",
        "before_digest": "sha256:7421dd426a6bab3e81951330fceacf66319635946148840689b2c45aba2e9003",
        "after_digest": "sha256:26d1f654cc4e461619a7b31ff24060d22ef6393c9e19868e4ad5b0d95d9c8a79"
      },
      {
        "path": "tests/contract_compiler/pareto/test_population_plan.py",
        "change": "MODIFIED",
        "before_digest": "sha256:4819623b8d72d4836b3e24a759e1ee1fa06926c07b35aad7b4ad7ebce53e7877",
        "after_digest": "sha256:1a663a98ccc5a93269e408faf6d69e4f55c3985e74609f3067f5c60a62e0a310"
      },
      {
        "path": "tests/contract_compiler/pareto/test_review_coverage.py",
        "change": "MODIFIED",
        "before_digest": "sha256:c78ffc2d8da3bdad02d0f1db8f0075db1190a7c073fbed92f5d6a0f32d87754a",
        "after_digest": "sha256:87d18028d83dd7388d6e2000bdba6360ccc994239e4687421a41dceef300ba88"
      },
      {
        "path": ".claude/skills/malleus-dev/references/CAPABILITIES.md",
        "change": "CREATED",
        "after_digest": "sha256:dcc483be27ca5d563d9b722eb727d36b3d12a852fc675a1d3c11cc61a5820cfb"
      },
      {
        "path": ".claude/skills/malleus-paper/SKILL.md",
        "change": "CREATED",
        "after_digest": "sha256:5c43070ad7c170df78013cc7932fa8e410d3683c58d18e1c57dd1f31d49b2b5a"
      },
      {
        "path": ".claude/skills/malleus-paper/agents/openai.yaml",
        "change": "CREATED",
        "after_digest": "sha256:e53501b7b24764b2e85bb8950eed1728a3f8eed45380926c33a208f38f15b209"
      },
      {
        "path": "tests/test_capability_declaration.py",
        "change": "CREATED",
        "after_digest": "sha256:20a8f71dc89a695455ae31f01418660f3de38470325025032e4cbb2a86efc8b4"
      },
      {
        "path": "handover/2026-09-17-core-capability-declaration.md",
        "change": "CREATED",
        "after_digest": "<digest of this file once final>"
      },
      {
        "path": "ROADMAP.md",
        "change": "MODIFIED",
        "before_digest": "sha256:ffe6c96e01f4aeee55ab8bc6bad8ffe76142747feceafa3a4bb38b729aa3fa17",
        "after_digest": "sha256:891c9529a77a0cd999c55e42f63ab9f3ce39fa46c46be63024dd6f7af01733aa"
      }
    ]
  },
  "references": [
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "990a24aec7a2b54d6fc16ae2ebd9faf730249e83"
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
draft validates as a complete entry. It is not a hash of anything.

## 6. What stays red until this is committed

`scripts/contract_compiler_ledger.py check` fails on the first mismatched pin,
and three `tests/test_docs.py` tests fail with it, because they build the docs
through the same validator. That clears when the block above is sealed.

Two `tests/test_inquisition.py` rites fail on untracked files and nothing else:
`TestPackagingTargetsAreTracked::test_declared_targets_exist_and_are_tracked`
("declared in pyproject but not committed") and
`TestNoPrivateMaterialCanReachARelease::test_release_artifacts_are_bounded_and_carry_every_skill`
("the sdist carries untracked source files"). Both name exactly
`.claude/skills/malleus-dev/references/CAPABILITIES.md`,
`.claude/skills/malleus-paper/SKILL.md` and
`.claude/skills/malleus-paper/agents/openai.yaml`. Both clear on commit. This
session was instructed not to commit.

## 7. Two Core requirements this survey surfaced

Both are in the declaration as `not implemented`, and neither is in
`docs/IMPLEMENTATION_STATUS.md`:

- **Per-slot source relation**: whether a slot's value is copied from the
  source, tallied from it, or authored by the producer (E-0430). Without it
  every "the value must appear in the source" rule is an adapter.
- **Supersession reason**: a supersession entry carries `{record_id,
  supersedes_record_id}` and nothing else, which is why stage A's producer wrote
  `"reason": "EXPLICIT_CORRECTION"` and had to remove it, and why stage C's
  honest outcome today is a `TYPE_ABSENT` gap (E-0456). The adopter half of that
  is not blocked: additive contract revision can add a correction-explanation
  class to the live history, and the Shop already exercises that path.

## Sealer's addition, 2026-09-17

ROADMAP.md is added to the documents as MODIFIED (recorded ffe6c96e… at OVR-000365, on disk 891c9529…). The change is section E, "From the paper front, 2026-09-17", written by the paper Overlord on Luis's ruling (paper ledger E-0439): three after-publication items, research-level content rules bubbling up to Core, a formula-ontology-KG submodule, and the per-slot source relation. It is recorded here so that one entry covers every pin this checkout breaks.

## Sealing note for OVR-000463, 2026-09-18

`entries/OVR-000463.json` was sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment
and this file's digest filled in.

## OVR-000465 draft, the re-binding row

One row added to CAPABILITIES.md for the capability sealed at OVR-000464; commit 140967b3.

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
  "entry_id": "OVR-000465",
  "sequence": 465,
  "previous_entry_hash": "sha256:11c298ac75902c458692e899f12399a4589e951a2585cad2dc375419c3b8f68f",
  "recorded_at": "<sealing moment, UTC>",
  "summary": "Declare the check-contract re-binding capability (OVR-000464) in the skills' capability declaration.",
  "why": "Luis's rule of 2026-09-17: consumers use a Core capability in full before declaring a gap, and the declaration in .claude/skills/malleus-dev/references/CAPABILITIES.md is where they read what exists. OVR-000464 landed check-contract re-binding across an additive ontology revision (REBIND_CHECK_CONTRACT, check_contract_descriptors on compose_contract_revision, KnowledgeHistoryReplay.required_checks, SUPPORTED_CONTRACT_REVISION_POLICIES) after the declaration was sealed at OVR-000463, so the declaration lacked the one capability the Shop's staged run needs next. This entry records the single added row; the guard test tests/test_capability_declaration.py passes (11) and no other file moves. Paper ledger E-0462.",
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "path": ".claude/skills/malleus-dev/references/CAPABILITIES.md",
        "change": "MODIFIED",
        "before_digest": "sha256:dcc483be27ca5d563d9b722eb727d36b3d12a852fc675a1d3c11cc61a5820cfb",
        "after_digest": "sha256:6b58a63c45cd80bba1855b50a68dccb3ff1d960d619e15722f4d4afc2678b49d"
      },
      {
        "path": "handover/2026-09-17-core-capability-declaration.md",
        "change": "MODIFIED",
        "before_digest": "sha256:57335b3737adfeb350ed81f1cbd792b8b9d02e1b67fa92701113b187122af4e8",
        "after_digest": "<digest of this file once final>"
      }
    ]
  },
  "references": [
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "140967b3875ec7494e992163b4ff2cdd2715990a"
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

## Sealing note for OVR-000465, 2026-09-18

`entries/OVR-000465.json` was sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment
and this file's digest filled in.

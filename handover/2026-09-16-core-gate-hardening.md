# Core gate hardening: four leaks closed, one ledger block sealed

Four changes that fault-injection-01 and the Shop rule layer showed open are
implemented in this isolated Core candidate, each RED before GREEN. Before the
ledger block was sealed the default suite failed 24 tests for one reason: the
overseer ledger had no `DOCUMENT_REVISION` block for the five tracked
documents this work changes. Luis authorized sealing it on 2026-09-16 through
the Overlord session, so `OVR-000461` is appended here, `head.json` re-pinned
and `status.md` re-rendered by Core's own sealer. Nothing else failed, and the
Shop consumers reproduce every committed receipt byte for byte.

A sealed document cannot record the consequences of its own digest. The
entry's `entry_hash`, the re-pinned head and the post-seal suite counts are in
the sealing commit and in the session report, not in this file.

## Change 1: a record must carry at least one derivation

`PopulationPlanRefusalReason.UNDERIVED_RECORD`, raised by
`compile_population_plan` in `src/malleus/_contract_pipeline/population.py`
immediately after the existing `UNDERIVED_FIELD` block, where the plan's
derivations are already collected.

> records carry no derivation: `<ids>`; every record needs at least one
> derivation naming a source it came from, and a record with no properties and
> no endpoints is not exempt

`UNDERIVED_FIELD` iterates a record's `properties` keys and the two relation
endpoints. A record with neither has nothing required of it, which is why
fault-injection-01 class `RECORD_WITH_NO_SOURCE_NO_FIELDS` was admitted five
times out of five and counted in the graph. The order of the two checks is
deliberate: `UNDERIVED_FIELD` still fires first, so
`RECORD_WITH_NO_SOURCE_WITH_FIELDS` keeps the diagnostic that cell recorded.

The check is satisfiable without inventing a property: a record with nothing
else to point at may derive its `type`. `UNDERIVED_FIELD` requires no
derivation for `type` or `id`, so this is an explicit way out rather than an
exemption.

- RED `8271a71a`: two failures, both `DID NOT RAISE PopulationPlanRefusal`,
  over a `BareObject` entity with `"properties": {}` and no derivation. The
  gap reproduces, so these are behavioural failures rather than a missing
  module.
- GREEN `ff3e99a4`: `tests/contract_compiler/pareto/test_population_plan.py`
  passes 91.
- Positive controls: `test_population_plan_still_admits_every_derived_record`
  and `test_population_plan_admits_a_property_free_record_that_derives_its_type`.
  The first passes before and after and discriminates nothing on its own; it
  is there to show the honest neutral plan is untouched.

## Change 2: a record may cite only an assertion it is derived from

`PopulationPlanRefusalReason.LOCATOR_NOT_DERIVED`, raised by
`compile_population_plan` after the record-derivation check.

> records cite an assertion they are not derived from: `<id>` cites `<L>`,
> derived from `<locators>`; a record's assertion_locator must be the locator
> of one of that record's own derivations

**The definition of "among", stated because it was a decision.** A record's
own derivations are the plan derivations whose `record_id` is that record,
which is the same set `trace_population_record` returns for a record. The
cited `assertion_locator` must equal the `locator` of **at least one** of
them, not all of them. The test names carry it:
`test_population_plan_refuses_a_cited_locator_no_derivation_of_that_record_names`
and `test_population_plan_admits_a_cited_locator_one_own_derivation_names`.

`_digest_defects` in `document.py` asks only that the cited assertion exists in
this capture and that `statement_sha256` matches *that* assertion. Trial
`b2-01` moved both together and was admitted; `verify.locator_disagreements`
saw it afterwards from the export and the trace, and nothing on the admission
path made the comparison. It does now.

Second decision, also pinned by a test: the check follows the slot, not the
profile. Any plan carrying a non-empty `properties.assertion_locator` is
checked, under any domain-history profile
(`test_population_plan_reads_the_cited_locator_under_any_profile`). The neutral
plan compiler already reads one pack-specific slot this way, `subject`, for
`DANGLING_SUBJECT`.

- RED `2f4ffabd`: two failures, both `DID NOT RAISE`.
- GREEN `3f05226f`: `test_population_plan.py`, `test_document_assertion_adapter.py`
  and `test_population_trace.py` pass 165.
- Positive control: `test_population_plan_admits_a_cited_locator_one_own_derivation_names`,
  a record whose two derivations cite `asr:001` and `asr:003` and whose
  `assertion_locator` is `asr:001`.

## Change 3: source binding is mandatory under the source-assertion profile

`PopulationPlanRefusalReason.SOURCE_BINDING_REQUIRED`, raised by
`compile_population_plan`.

> records do not bind the assertion behind them: `<id>` of type `<T>` does not
> set `<slots>`; under the source-assertion profile a record whose type
> declares assertion_locator must set assertion_locator and statement_sha256

**Which layer carries it, stated because it was a decision.** The plan
compiler, not the pack and not the profile document.

- The pack (`ontology/packs/research.yaml`) declares `assertion_locator` and
  `statement_sha256` on the `SourceAsserted` mixin. A `required: true` there
  would bind every adopter of the pack under every profile, which is wider
  than "under the source-assertion profile", and it would move the compiled
  ontology identity that frozen paper artifacts name.
- `src/malleus/profiles/source-assertion.json` is a domain-history profile.
  Its closed field set is change, genesis, grounding, ontology roles, origin,
  projection rule family, semantic unit and time semantics. It has no slot
  vocabulary, so a slot requirement cannot be expressed there without widening
  the profile grammar.
- The plan compiler already holds all three inputs at once: the plan's declared
  history profile, the compiled contract view, and the records. Its refusal
  names the record, its type and each missing slot, which the brief asked for.

The gate is exact: the plan's `history_profile` must carry both the shipped
profile's `profile_id` and its `sha256`. A plan under another profile is
untouched, pinned by
`test_population_plan_requires_source_binding_only_under_that_profile`.

Which records the rule reaches is a contract question, asked of the compiled
contract through a new shared helper `_declares_slot`, which
`document.py::_slot_bearing_types` now also uses so the adapter's census and
the compiler's refusal cannot drift apart. The helper asks
`ContractView.get_slot_constraint`, which resolves both a short type name and
a full URI; the previous `effective_slots` membership test resolved only the
short form. For the research pack, whose records name short types, the two
agree.

- RED `8b47d7cd`: two failures, both `DID NOT RAISE`.
- GREEN `a9a00b58`: `test_population_plan.py`, `test_document_assertion_adapter.py`,
  `test_population_trace.py`, `test_capture_coverage_boundary.py` and
  `test_governed_population.py` pass 222.
- Positive controls:
  `test_population_plan_admits_a_bound_assertion_record_under_the_profile`,
  `test_population_plan_binds_no_source_on_a_type_that_declares_no_locator`,
  and the profile-boundary test above.

### What producers must now emit

A producer writing a population plan under the source-assertion profile must,
from this commit on:

1. Carry at least one derivation for **every** record, including a record with
   no property and no endpoint. Deriving `type` is the minimum.
2. Set `properties.assertion_locator` to the locator of one of that record's
   own derivations. A locator that is merely a real assertion of the capture
   with a matching digest is no longer enough.
3. Set both `assertion_locator` and `statement_sha256` on every record whose
   type declares `assertion_locator`. In run-23's vocabulary that is `Claim`,
   `GeophysicalObservation`, `GeochemicalObservation`, `CountObservation` and
   `ElementRatio`. Run-23's own producer already did this for 236 of 236
   eligible records; a producer that opted out was previously admitted with
   `provenance_coverage` zero and no refusal.

The `provenance_coverage` census still counts and never refuses. Under the
source-assertion profile it now reports a complete axis or the plan does not
compile; under another profile it remains the only reading.

## Change 4: Prolog rules can see provenance

`FACT_CONTRACT_VERSION` is `"3"`. `SUPPORTED_FACT_CONTRACT_VERSIONS` is
`("2", "3")`. Version 3 adds two predicates to the ten:

```prolog
m_derivation(RecordId, FieldPath, SourceId, Locator).
m_source_text(SourceId, Locator, Text).
```

`FieldPath` is the plan's field path joined by `/`, so `properties/analyte`
for a property and `source_id` for a relation endpoint. A path step containing
`/` is refused at construction rather than made ambiguous.

**Whether version 2 stays supported, stated because it was a decision: yes,
by declaration.** `FACT_PREDICATES_BY_VERSION` maps each version to its exact
vocabulary. `LogicContract.load` accepts either. `GraphFactCompiler` is
constructed at a version and `PrologVerifier` builds its compiler from the
contract's declared version, so a version-2 contract receives the ten
predicates, `fact_declarations` emits only those ten `:- dynamic` lines, and a
version-2 rule that reaches for `m_derivation` fails loudly instead of matching
an empty relation. Supplying provenance to a version-2 compiler raises
`LogicError` rather than dropping it.

**Migration: none.** Every in-repo contract pinned at `fact_contract_version:
'2'` keeps working untouched: `prolog/cyp450_logic.yaml`, the Shop's
`shipment_policy/logic.yaml` and `content_rules/logic.yaml`, and the three
`research/methodology_gedanken_e2e` contracts. An adopter opts into the new
facts by bumping their own contract to `"3"`.

Provenance reaches the compiler as an explicit typed artifact, never by the
compiler reading a history: `GraphProvenance(derivations, source_texts)` of
`RecordDerivation(record_id, path, source_id, locator)` and
`RetainedSourceText(source_id, locator, text)`, passed to
`GraphFactCompiler.compile(..., provenance=...)` or to
`PrologVerifier.verify_candidate_subgraph(candidate, *context, provenance=...)`.
The caller supplies them for the candidate change set it is checking and, where
the accepted history retains them, for the context graphs it passed. This
matches how the Shop already executes rules: its runner stages the change and
submits the real Prolog result; Core's machine consumes the outcome and runs no
Prolog itself. A derivation naming a record the compiled graphs do not carry is
refused, and two different texts for one `(source_id, locator)` are refused.

The three new public names are exported from `malleus`: `GraphProvenance`,
`RecordDerivation`, `RetainedSourceText`.

- RED `d6bb53f1`: both `tests/test_logic.py` and `tests/test_prolog_verifier.py`
  failed to collect, `ImportError: cannot import name 'GraphProvenance' from
  'malleus.logic'`. These are missing-implementation errors, not failed
  behavioural assertions; the behavioural RED for this change is the
  fault-injection cell's own gap 1, which no Core test could express before
  the vocabulary existed.
- GREEN `30c738f1`: `tests/test_logic.py` and `tests/test_prolog_verifier.py`
  pass 76; with `tests/test_accepted.py`, `tests/test_protocol.py`,
  `tests/test_control.py` and `tests/test_staging.py`, 500.
- The proof, on a synthetic two-class ontology written in `tmp_path`, not on
  the paper's private reading:
  `test_a_rule_refuses_a_value_absent_from_the_text_the_record_cites` stages
  one `Measurement` whose `analyte` is `FAULT-A-01-SYNTHETIC`, cites
  `assertion:129`, and supplies that locator's retained text. One rule reads a
  derivation fact and a source-text fact:

  ```prolog
  malleus_violation('VALUE_SUPPORTED_BY_CITED_TEXT', 'VALUE_NOT_IN_CITED_TEXT', [RecordId]) :-
      m_property(RecordId, Name, string, Value),
      atomic_list_concat([properties, Name], '/', Path),
      m_derivation(RecordId, Path, SourceId, Locator),
      m_source_text(SourceId, Locator, Text),
      \+ sub_atom(Text, _, _, _, Value).
  ```

  Result `VIOLATED`, one witness.
- Positive control: `test_the_same_rule_admits_a_value_its_cited_text_contains`,
  the same rule and the same provenance with `analyte` set to a phrase the
  cited text contains, result `SATISFIED`.
- `test_a_version_two_contract_refuses_provenance_instead_of_dropping_it`
  pins the version-2 boundary against the shipped CYP450 contract.

`docs/ARCHITECTURE.md` documents both predicates and the version boundary;
`tests/test_logic.py::test_architecture_documents_exact_fact_vocabulary` is
what forced the doc change and passes unmodified.

## The acolyte pre-flight list

`tests/test_inquisition.py::TestSkillsAreInstallable::test_acolyte_preflight_list_is_the_adapters_own_refusal_reasons`
derives the required list from the two refusal enums and fails when Core moves.
It failed with `the pre-flight list omits refusal reasons Core carries:
['LOCATOR_NOT_DERIVED', 'SOURCE_BINDING_REQUIRED', 'UNDERIVED_RECORD']`.
Commit `22145d31` adds the three entries to
`.claude/skills/malleus-acolyte/SKILL.md`.

## Core's default test suite

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -ra -p no:cacheprovider
```

Result at `35942b60`: **24 failed, 3473 passed, 3 skipped**.

This work adds 25 tests, 12 in
`tests/contract_compiler/pareto/test_population_plan.py`, 10 in
`tests/test_logic.py` and 3 in `tests/test_prolog_verifier.py`. Collection goes
from 3,475 at the baseline to 3,500, which is the same 25 and nothing else.

All 24 failures have one cause. Twenty raise
`LedgerValidationError` directly, three are the Sphinx builders that call the
same validation, and one is the ledger CLI subprocess exiting 1 with that error
on its stderr. There is no second cause; the failure lines were counted, not
sampled.

The baseline run at `25f94cbf` reported **1 failed, 3471 passed, 3 skipped**.
That one failure was this session's own first test edit landing mid-run: the
suite had already collected and run the ledger and integration modules before
the edit, and reached `tests/test_docs.py` after it. At `25f94cbf` itself all
700 ledger-tracked document digests match their recorded `after_digest`,
checked blob by blob against the commit, so the clean baseline is 3,472
passing. That last number is arithmetic on the observed run, not a run of its
own.

The three skips are the two `tests/test_ontology.py` LinkML-CLI resolver skips
and the absent private paper-program doctrine, the same three the baseline
reports.

## Consumer regression

Run from a `git archive` of the final commit `35942b60` into a scratch
directory, with the Shop research tree taken from
`/Users/luis/Projects/malleus-dev` at main `18015352` and `content_rules`
copied from that working tree, where it is untracked and therefore absent from
`git archive 18015352`. Every number below was reproduced twice, once from an
export of `30c738f1` and again from an export of `35942b60`, identically.

### The connected Shop chain reproduces all three receipts, byte for byte

| step | expected | observed |
| :-- | :-- | :-- |
| `connected_story.run` | `sha256:1c989c55…acbe` | `sha256:1c989c55…acbe` |
| `warehouse.run --append` | `sha256:ae9bbf87…cc06` | `sha256:ae9bbf87…cc06` |
| `partial_shipments.run --append` | `sha256:b3250849…fa53` | `sha256:b3250849…fa53` |

`graph_sha256` and `report_sha256` also match the committed receipts
(`e5f36981…`, `52f2141b…`, `57e3839c…`, `df3ca88c…`), and
`baseline_prefix_preserved` is true at both appends. No producer-digest
difference appeared, so the tolerance the brief allowed was not needed.
**Changes 1, 2 and 3 refuse nothing in the honest Shop history.**

### `shipment_policy`

`test_shipment_policy.py` passes 5. `run` exits 0 against a fresh history: 3
accepted changes, 32 events, ledger `sha256:633aa2ee…`. Its `logic.yaml` is
pinned at `fact_contract_version: '2'` and loads and executes unchanged.

### `content_rules`: 10 passed, 8 errors, one cause, and it is not an honest history

`test_content_rules.py` gives **10 passed, 8 errors**. All eight are the same
module fixture failing to build, and the cause is one line of the fixture:

```
research/…/small_shop/content_rules/run.py:424 in refuse_synthetic
  PopulationPlanRefusal: UNDERIVED_RECORD: records carry no derivation:
  synthetic:empty-record
```

`synthetic_plan(kind="empty")` builds a record typed
`https://malleus.dev/schema/Entity` with `"properties": {}` and
`derivations = []`, deliberately, to show the directory's own Prolog rule
`NO_EMPTY_RECORD` refusing it. Change 1 now refuses the same fault earlier, at
the plan compiler, so the candidate never reaches Prolog and the fixture's
`prepare()` raises before the check it was written to demonstrate. The
docstring on that function, "Both cite retained Table 1 cells, so neither is
refused for a missing derivation", is no longer true of the `empty` candidate.

This is **not** the STOP the brief defined. Nothing in an honest history is
refused. The honest half was run on its own to prove it: `run(path,
probe=False)` under the Shop's own selected Prolog policy gives **zero
refusals**, 21 accepted changes, 107 historical records, 143 ledger events, 23
entities / 21 events / 62 event participations, which are the numbers
`content_rules/README.md` reports. The `conflict` synthetic candidate is still
refused by the Prolog rule, as before; only `empty` moved.

It is also not a version-pin migration. `content_rules/logic.yaml` stays at
`fact_contract_version: '2'` and needs no change. What the directory needs is a
decision from its owner, and the options are:

1. Give `synthetic:empty-record` one derivation, for example on `["type"]`
   citing a retained Table 1 cell, so the candidate still reaches Prolog and
   `NO_EMPTY_RECORD` remains the mechanism that refuses it. The rule then
   covers the case where a record has a source but no property, which Core
   still admits.
2. Drop the `empty` candidate and the `NO_EMPTY_RECORD` rule, and record that
   Core closed that hole at the structural gate with `UNDERIVED_RECORD`, which
   is stricter than the rule was: Core refuses a record with no derivation
   whether or not it has properties.

Nothing in `/Users/luis/Projects/malleus-dev` was modified.

## Ruff

`ruff 0.11.9`, the pinned version. `ruff check` passes on every changed Python
file except two pre-existing findings that are present at `25f94cbf` and that
this work did not touch: `tests/test_logic.py` two `F401` unused imports of
`ProposedOperation` and `stage_subgraph`, and `tests/test_prolog_verifier.py`
five `E402` module-level imports after `pytestmark`. Counts are identical
before and after.

`ruff format --check` reports drift in five changed files, all of it
pre-existing and all of it outside the changed regions. Hunk counts are
identical at `25f94cbf` and at the final commit:
`src/malleus/_contract_pipeline/population.py` 1, `document.py` 11,
`src/malleus/logic.py` 12, `tests/test_logic.py` 11,
`tests/test_prolog_verifier.py` 17,
`tests/contract_compiler/pareto/test_population_plan.py` 1.
`src/malleus/__init__.py` and `src/malleus/prolog_verifier.py` are clean at
both. Every line this work added is format-clean. Eleven hunks that earlier
drafts introduced were removed before the final commit: four in `logic.py`
before its commit, and seven in the two test modules in `35942b60`, which is
whitespace and quote style only and changed no assertion.

## Changed-file scope

| file | ledger-tracked |
| :-- | :-- |
| `src/malleus/_contract_pipeline/population.py` | yes, `OVR-000420` |
| `src/malleus/_contract_pipeline/document.py` | yes, `OVR-000414` |
| `src/malleus/logic.py` | no |
| `src/malleus/prolog_verifier.py` | no |
| `src/malleus/__init__.py` | no |
| `docs/ARCHITECTURE.md` | yes, `OVR-000361` |
| `tests/contract_compiler/pareto/test_population_plan.py` | yes, `OVR-000418` |
| `tests/test_logic.py` | no |
| `tests/test_prolog_verifier.py` | no |
| `.claude/skills/malleus-acolyte/SKILL.md` | yes, `OVR-000460` |
| `handover/2026-09-16-core-gate-hardening.md` | new |

No ontology pack, no shipped profile JSON, no research file and no paper file
was changed.

## Commits

| commit | |
| :-- | :-- |
| `8271a71a` | test: require at least one source derivation per record |
| `ff3e99a4` | feat: refuse a record that carries no derivation at all |
| `2f4ffabd` | test: require a cited locator to be one of a record's own derivations |
| `3f05226f` | feat: refuse a record citing an assertion it is not derived from |
| `8b47d7cd` | test: require source binding on assertion records under the profile |
| `a9a00b58` | feat: make source binding mandatory under the source-assertion profile |
| `d6bb53f1` | test: specify provenance-bearing facts a Prolog rule can read |
| `30c738f1` | feat: carry derivations and retained source text into fact contract 3 |
| `22145d31` | docs: name the three new refusals in the acolyte pre-flight list |
| `35942b60` | style: format the lines this candidate added to the two test modules |

## Exclusions

- No Core code produces a `GraphProvenance`. Core declares the vocabulary,
  compiles supplied provenance and refuses inconsistent provenance; deriving
  derivations and retained text from a `KnowledgeChangeHistory` at admission
  is not in this slice and no consumer asked for it. `PrologVerifier` does not
  open a history and does not resolve a locator.
- The fact-contract extension is not a claim that a rule reading it is
  correct. `m_source_text` carries what the caller says the locator resolves
  to. Nothing here verifies that against retained bytes; the byte checks
  remain where they were, in `KnowledgeChangeHistory` and the document
  adapter.
- A rule needing a text that was never retained does not fire. Absence of a
  `m_source_text` fact is not evidence that a value is supported.
- Change 2 compares a cited locator with a plan's own derivation locators. It
  does not read the source. `LOCATOR_REPOINTED_COHERENT_DERIVATION` moves the
  locator, the digest and every formalization together and stays invisible,
  exactly as fault-injection-01 recorded.
- Change 3 requires the two slots to be present and non-empty. Whether the
  digest matches is still the document adapter's `DIGEST_MISMATCH`.
- The paper's populations were not re-run. Nothing here was measured against
  run-23 or any other model-produced population; the checks were exercised
  against synthetic plans and the Shop's honest history.
- Cross-language parity of the extended fact contract is not established, and
  no second interpreter consumed it.

## The governance gate, and the block that closes it

`scripts/contract_compiler_ledger.py` records, per path, the latest
`after_digest` any `DOCUMENT_REVISION` block declared, and `_validate_semantics`
(line 603) then requires every one of those 700 paths to hash to that value
today. Five of the files this work changes are among them. So `check` fails,
every caller of `load_ledger` fails, and 24 tests fail with it. Every one of
the 24 reaches the same first mismatch:

```
LedgerValidationError: OVR-000361: latest document digest mismatch for
docs/ARCHITECTURE.md, expected sha256:e6a8336c…a763, got sha256:0981f798…f37b
```

The 24 are seven in `tests/test_contract_compiler_ledger.py`
(`test_overseer_ledger_and_projection_are_current`,
`test_cc002_integrated_candidate_binds_governed_checkpoint_lineage`,
`test_od012_current_policy_supersedes_r3_without_erasing_history`,
`test_verified_facts_do_not_claim_future_artifact_bytes`,
`test_r03_completion_correction_restores_exact_evidence_chronology`,
`test_correction_of_correction_restores_the_original_projection`,
`test_active_typed_replacement_projects_normally`), fourteen in
`tests/test_contract_compiler_integration.py`, and three in
`tests/test_docs.py` (`test_strict_html_build_is_source_pure`,
`test_autodoc_and_autosummary_render_the_existing_package_root`,
`test_doctest_builder_executes_an_infrastructure_only_example`).

The fix is one appended block, `head.json` re-pinned and `status.md`
re-rendered. That is an overseer act. This session was not given that
authority and did not take it, so the block is written out here instead.
Whoever seals it must fill `recorded_at` with the sealing moment, take
`after_digest` for this handover once the file is final, and compute
`entry_hash` with `python scripts/contract_compiler_ledger.py hash` before
binding it in `head.json` and re-running `render`.

Two judgments the sealer owns, not this session:

- `affected_ids` and the `AFFECTS` reference carry `CC-R11` because the two
  preceding local blocks, `OVR-000459` and `OVR-000460`, carry it. `CC-R11` is
  `COMPLETE`. If gate hardening belongs to a different workstream, that is the
  sealer's call.
- The entry number `OVR-000461` and `previous_entry_hash` are correct against
  this isolated candidate's head only. An integrator must reconcile against
  the then-current shared head rather than copy a conflicting number, exactly
  as `OVR-000460`'s handover says.

```json
{
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "entry_id": "OVR-000461",
  "ledger": "overseer",
  "sequence": 461,
  "entry_type": "DOCUMENT_REVISION",
  "previous_entry_hash": "sha256:10b38112f30afc8dc92909780161fb8e5d805a1873c4dc4fbcdb3643dcf846d7",
  "recorded_at": "<sealing moment, UTC>",
  "actor": {"id": "overseer", "type": "OVERSEER"},
  "subject": {"id": "core-gate-hardening", "type": "DOCUMENT"},
  "summary": "Close four admission leaks the fault-injection control and the Shop rule layer recorded, and extend the Prolog fact contract to version 3 with provenance predicates.",
  "why": "Luis decided the four changes. Every record now needs at least one derivation (UNDERIVED_RECORD), a cited assertion_locator must be the locator of one of that record's own derivations (LOCATOR_NOT_DERIVED), assertion_locator and statement_sha256 are mandatory under the source-assertion profile for records whose type declares them (SOURCE_BINDING_REQUIRED), and fact contract version 3 adds m_derivation/4 and m_source_text/3 while version 2 stays supported by declaration so every pinned consumer contract is unchanged. Four RED commits preceded four GREEN commits; the first three REDs were behavioural DID NOT RAISE failures, the fourth was a missing-symbol collection error. One Prolog rule test on a synthetic ontology reads a derivation fact and a source-text fact and refuses a value absent from its cited text, with a positive control that admits a value the text contains. The connected Shop chain reproduces all three committed receipts byte for byte and the honest content_rules population admits with zero refusals, so no honest history is refused. The content_rules synthetic empty candidate is now refused earlier by Core than by its own Prolog rule and needs an owner decision, recorded in the handover; no research file was changed. This is structural admission and a fact vocabulary, not semantic verification: nothing here reads a value against a source, Core produces no provenance itself, and cross-language parity is not established. Local isolated governance only; an integrator must reconcile against the eventual shared head.",
  "data": {
    "affected_ids": ["CC-R11"],
    "documents": [
      {
        "path": ".claude/skills/malleus-acolyte/SKILL.md",
        "change": "MODIFIED",
        "before_digest": "sha256:dfffc66f7e343f42b7803699924d0a6e47cde24ceb8f3dc3a1fec0b7f5d8c46d",
        "after_digest": "sha256:f0f24ed896c1433c1d56fceaa00ada291a7acc44b840f5283b0a328eba5841ba"
      },
      {
        "path": "docs/ARCHITECTURE.md",
        "change": "MODIFIED",
        "before_digest": "sha256:e6a8336cd2165c1507ed493839871fe7de58bc9474020039657d1429aac7a763",
        "after_digest": "sha256:0981f7989651aa6c6cf8cd5da720c35c6e7f10c43ad717b7228fd5ae8865f37b"
      },
      {
        "path": "src/malleus/_contract_pipeline/document.py",
        "change": "MODIFIED",
        "before_digest": "sha256:0d3922344de2245310e6255e4c7e703d36be8669f44a755a1f0af4c6b642885b",
        "after_digest": "sha256:0f5463bca8578ec9e7db3bb7d892bc5f4195e6e084411e556b375c9ce09b649d"
      },
      {
        "path": "src/malleus/_contract_pipeline/population.py",
        "change": "MODIFIED",
        "before_digest": "sha256:5a501a7c416b8414dbfcbe4d83f761ea0c148030b0b80f4b50c4047e650b747a",
        "after_digest": "sha256:07ffd475176dac25bde26ddad740288918d82e93697b907f91b5b60d6397bec5"
      },
      {
        "path": "tests/contract_compiler/pareto/test_population_plan.py",
        "change": "MODIFIED",
        "before_digest": "sha256:b541f0aa6e8fb406faacc0e1b45507b7076524dc74694ea83191075e4ef27e3d",
        "after_digest": "sha256:4285af76878476b1700427e4aff8bbed8a7e9af7ab0633fee9f70fe4f9fae756"
      },
      {
        "path": "handover/2026-09-16-core-gate-hardening.md",
        "change": "CREATED",
        "after_digest": "<digest of this file once final>"
      }
    ]
  },
  "references": [
    {"relation": "EVIDENCES", "type": "COMMIT", "target": "8271a71a"},
    {"relation": "EVIDENCES", "type": "COMMIT", "target": "ff3e99a4"},
    {"relation": "EVIDENCES", "type": "COMMIT", "target": "2f4ffabd"},
    {"relation": "EVIDENCES", "type": "COMMIT", "target": "3f05226f"},
    {"relation": "EVIDENCES", "type": "COMMIT", "target": "8b47d7cd"},
    {"relation": "EVIDENCES", "type": "COMMIT", "target": "a9a00b58"},
    {"relation": "EVIDENCES", "type": "COMMIT", "target": "d6bb53f1"},
    {"relation": "EVIDENCES", "type": "COMMIT", "target": "30c738f1"},
    {"relation": "EVIDENCES", "type": "COMMIT", "target": "22145d31"},
    {"relation": "EVIDENCES", "type": "COMMIT", "target": "35942b60"},
    {"relation": "AFFECTS", "type": "WORKSTREAM", "target": "CC-R11"}
  ]
}
```

`src/malleus/logic.py`, `src/malleus/prolog_verifier.py`,
`src/malleus/__init__.py`, `tests/test_logic.py` and
`tests/test_prolog_verifier.py` also changed. No prior block records them, so
`check` does not require them, and listing them would make this block their
first `CREATED` revision, which they are not. The sealer decides whether the
ledger should start tracking them.

## What was not done

- The overseer block above was not written. Nothing under
  `design/contract_compiler/overseer/` was touched.
- Nothing was pushed, nothing outside this checkout was modified, no branch
  was reset and nothing was stashed or deleted.
- The `content_rules` fixture was not repaired; the two options are above and
  the decision is its owner's.
- The paper's populations, the release and replay candidates, and the live
  consumers were not re-run.

## Sealing note, 2026-09-16

The sealed entry in `entries/OVR-000461.json` differs from the draft block
above in two mechanical ways the ledger schema required: `why` is shortened
to the 1,200-character limit with the same substance, and the ten commit
references carry full hashes. Sealed by the operator with the ledger tool's
own hash, render and check.

---

# Addendum, E-0420: the citation rule was an adapter from one case

This section is append-only. It supersedes two claims in **Change 2** above
rather than editing them, the way the ledger supersedes a block rather than
rewriting it. The superseded claims are the paragraph beginning "Second
decision, also pinned by a test: the check follows the slot, not the profile",
and the test name `test_population_plan_reads_the_cited_locator_under_any_profile`,
which no longer exists. Everything else in Change 2 still holds.

## What refused, and why it was right to refuse

The finish-the-pin step at `c78b6b38` ran S1, the Shop's progressive
interpretation, under its own adopter profile
`shop-authored-payment-context-v1`. Stage B refused it with
`LOCATOR_NOT_DERIVED`. The record cites a passage by its id,
`intro-1-customer`, while its derivations name the packet cells that carry
that id, `row:0:passage_id` and `row:0:text`. Core compares locator strings,
so the two can never match. The refused run is preserved at
`private/shop-progressive-01/gate-evidence/c78b6b38-s1-fresh/`; its
`packets/stage-b/context.jsonl` is where the passage ids and their cells are
visible side by side.

Nothing in that plan is dishonest. The derivations point at exactly the bytes
the value came from, and the citation points at the passage the adopter's
profile says a record cites. Both are correct under their own semantics.

The defect is in the rule, not in S1. `LOCATOR_NOT_DERIVED` was specified from
the document path alone, where a locator names an assertion and a derivation
names that same assertion, so string equality is the whole comparison. That is
one consumer's shape written as though it were the protocol's. The first
structurally different consumer refused it, which is the failure mode the
project already has a rule against: a contract written from one case is that
case's adapter, and it must be labelled as one or generalized before it ships.

## The change

Luis ruled the rule is scoped to the source-assertion profile, where the
`assertion_locator` slot's semantics are fixed, the same place **Change 3**
already lives. Under any other profile the slot means what the adopter says it
means and Core makes no comparison.

One gate serves both checks. `compile_population_plan` computes
`source_asserted` once, from the plan's declared `profile_id` and `sha256`
against the shipped `SOURCE_ASSERTION_PROFILE`, and both
`LOCATOR_NOT_DERIVED` and `SOURCE_BINDING_REQUIRED` sit inside it. The same
comparison is not written twice.

Run-23's `b2-01` fault lives under the source-assertion profile and is still
caught, by
`test_population_plan_refuses_a_cited_locator_no_derivation_of_that_record_names`.
This narrows a refusal. It widens none.

- RED `4e998d85cae22791cee6515e856bcc32e0d83712`: one failure. A plan under
  the state-version profile whose record cites `asr:002` while its derivations
  cite `asr:001` was refused `LOCATOR_NOT_DERIVED` where it must compile. The
  two source-assertion tests passed throughout and are the control.
- GREEN `f4687092ba3b283bd54ec6dafbd69f19db04fe0a`:
  `tests/contract_compiler/pareto/test_population_plan.py` passes 99.
- The replaced test is now
  `test_population_plan_reads_the_cited_locator_only_under_that_profile`,
  named for what it asserts, carrying E-0420 and this reason in its docstring.

## The block this needs, drafted and not sealed

Sealing is the overseer's act and is not done here. The draft below is
schema-valid: it was checked with `jsonschema` against
`design/contract_compiler/overseer/ledger.schema.json` before being written
down, with `recorded_at` and this file's `after_digest` replaced by
schema-shaped stand-ins for the check only. `why` is 1,198 characters against
the 1,200 limit. The sealer fills `recorded_at` with the sealing moment, takes
`after_digest` for this file once it is final, and computes `entry_hash` with
`python scripts/contract_compiler_ledger.py hash` before binding it in
`head.json` and running `render` then `check`.

```json
{
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "entry_id": "OVR-000462",
  "ledger": "overseer",
  "sequence": 462,
  "entry_type": "DOCUMENT_REVISION",
  "previous_entry_hash": "sha256:75680a3517071c1cf314290d4fa2b83a7174ecb14883c8596e948947f1f0d93c",
  "recorded_at": "<sealing moment, UTC>",
  "actor": {"id": "overseer", "type": "OVERSEER"},
  "subject": {"id": "core-gate-hardening", "type": "DOCUMENT"},
  "summary": "Scope the citation-consistency refusal to the source-assertion profile after its first structurally different consumer refused it.",
  "why": "E-0420. OVR-000461 recorded LOCATOR_NOT_DERIVED as following the assertion_locator slot under any domain-history profile. That rule was specified from the document path alone, where a locator names an assertion and a derivation names that same assertion, so string equality was the whole comparison. S1, the first structurally different consumer, was refused at stage B under the adopter profile shop-authored-payment-context-v1: it cites a passage by its id, intro-1-customer, while its derivations name the cells row:0:passage_id and row:0:text whose content is that id. Both are honest and the strings cannot match. Under an adopter profile the slot's semantics are the adopter's, so the rule now applies only under the shipped source-assertion profile, gated on the same profile_id and sha256 SOURCE_BINDING_REQUIRED uses, one gate read once. Run-23's b2-01 fault stays caught there. RED 4e998d85 refused the state-version plan that must compile; GREEN f4687092 compiles it and keeps the source-assertion refusal. No other refusal, profile, ontology or consumer pin changed. This narrows a refusal, it does not widen one. Local governance only; an integrator reconciles against the shared head.",
  "data": {
    "affected_ids": ["CC-R11"],
    "documents": [
      {
        "path": "src/malleus/_contract_pipeline/population.py",
        "change": "MODIFIED",
        "before_digest": "sha256:07ffd475176dac25bde26ddad740288918d82e93697b907f91b5b60d6397bec5",
        "after_digest": "sha256:16d73c588fc29412044c5cebe9c6f43f5733f221c73133a759c1bf57ae769411"
      },
      {
        "path": "tests/contract_compiler/pareto/test_population_plan.py",
        "change": "MODIFIED",
        "before_digest": "sha256:4285af76878476b1700427e4aff8bbed8a7e9af7ab0633fee9f70fe4f9fae756",
        "after_digest": "sha256:4819623b8d72d4836b3e24a759e1ee1fa06926c07b35aad7b4ad7ebce53e7877"
      },
      {
        "path": "handover/2026-09-16-core-gate-hardening.md",
        "change": "MODIFIED",
        "before_digest": "sha256:1d634eff5c9be14fd0d55c4c112cf5b4f8b6d6fb72ab7ec2603b7ea76f033976",
        "after_digest": "<digest of this file once final>"
      }
    ]
  },
  "references": [
    {"relation": "EVIDENCES", "type": "COMMIT", "target": "4e998d85cae22791cee6515e856bcc32e0d83712"},
    {"relation": "EVIDENCES", "type": "COMMIT", "target": "f4687092ba3b283bd54ec6dafbd69f19db04fe0a"},
    {"relation": "AFFECTS", "type": "WORKSTREAM", "target": "CC-R11"}
  ],
  "entry_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
}
```

The `entry_hash` above is a placeholder of the right shape, present only so
the draft validates as a complete entry. It is not a hash of anything.

`src/malleus/logic.py`, `prolog_verifier.py`, `__init__.py`,
`tests/test_logic.py` and `tests/test_prolog_verifier.py` are untouched by this
change and are absent from the block for that reason, not because the ledger
declines to track them.

## Sealing note for OVR-000462, 2026-09-17

`entries/OVR-000462.json` was sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment
and this file's digest filled in.

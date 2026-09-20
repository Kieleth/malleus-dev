# fault-injection-01: what the gate refuses, what it exposes, what it lets through

A deterministic fault-injection control for the paper's model condition. The
paper reports seven model-produced populations admitted with one structural
refusal in total and 2,353 returned facts audited with none unsupported. That
number says nothing on its own: a gate that refuses everything and a gate that
refuses nothing both produce a careful-looking population when the producer was
careful. This cell manufactures the counterfactual. Typed faults go into a
frozen admitted capture, each faulted population goes through the same runner
run-23's population went through, and the run's own refusal or admission is the
observation.

Precedent: E-0355, fourteen faults through three stores on the robotics
history, offline, no model. Method borrowed, code not.

## Coordinates

- Core: `c95dba7b86bb61487bda9a52458e1ea47cce20ab`, exported with
  `git archive --format=tar <commit> src/malleus` and put first on
  `PYTHONPATH`, the way run-23's own parent-side commands ran it
  (`launch-log.json` `runner[0].core_note`) and the way
  `paper-v4/run_active_tests.py:export_core` does it. Nothing under
  `src/malleus` in the working checkout was read, and nothing was changed.
- Base population: run-23's admitted capture and records, read only, from
  `private/paper-v4-v4-run-23/producer/work/document-population.json`.
- Runner: `paper-v4/experiment-v4/run-23/run.py`, unmodified, one process per
  trial. Only `--population` differs between the control and a trial.
- Seed: 23. Every selection is `random.Random("23:<label>")` over a sorted
  candidate list, so the catalog is a function of the capture alone.
- Private outputs: `private/paper-v4-fault-injection-01/`.

## The classification, from the code at that commit, written before the run

Four mechanisms sit on the path a population takes, in the order a record meets
them.

1. **Adapter, structural** — `_contract_pipeline/document.py`,
   `adapt_document_assertions`. Closes the capture's fields, checks every
   assertion's block against the reading's own block inventory and every
   statement against that block's bytes after whitespace collapse
   (`UNKNOWN_BLOCK`, `NOT_VERBATIM`), refuses a repeated record ID while
   snapshotting the records (`MALFORMED_CAPTURE`), and refuses a formalization
   naming a record or a path that is not there
   (`UNKNOWN_FORMALIZATION_TARGET`).
2. **Digest binding** — `_digest_defects` in the same module. For every record
   carrying `assertion_locator`, the locator must name an assertion of this
   capture (`UNKNOWN_ASSERTION_LOCATOR`); where `statement_sha256` is also
   present, it is recomputed from that assertion's statement bytes and must
   match (`DIGEST_MISMATCH`). A digest with no locator refuses under
   `DIGEST_NOT_LOCATED`. Both slots are optional, so this mechanism runs only
   where the producer opted into it. In run-23 all 236 subject-bearing records
   carry both and no other record carries either.
3. **Compiler** — `_rehydrate` in `_contract_pipeline/population.py`, which is
   `KnowledgeGraph.from_records` against the compiled `ContractView`. A type or
   a slot the accepted closure does not declare comes back as
   `RECORDS_NOT_REHYDRATABLE` with the graph gate's own aggregated text.
4. **Admission structural check** — the rest of `compile_population_plan`:
   duplicate record identity in the plan and against history
   (`DUPLICATE_RECORD_ID`), absent relation endpoints (`DANGLING_ENDPOINT`),
   absent subjects (`DANGLING_SUBJECT`), supersession shape, and the rule that
   every `properties` key and both relation endpoints carry a derivation
   (`UNDERIVED_FIELD`).

**Trace derivation** is not on that path. `trace_population_record` reads back
what was admitted; it refuses an inconsistent trace, not a false one. It is
listed below as a catcher only where a check a reader runs *after* admission,
over the run's own export and trace summary, can see the fault.

The seven classes, each against the mechanism the code designates for it:

| Class | Construction | Designed catcher |
| :--- | :--- | :--- |
| a `VALUE_NOT_IN_BLOCK` | one well-typed property value replaced with a synthetic value; cited assertion, locator and digest untouched | **none, review only.** Nothing on the path reads a property value against the sentence. The adapter checks that the *sentence* is verbatim in its block, never that the *value* is in the sentence. |
| b `LOCATOR_REPOINTED_STALE_DIGEST` | `assertion_locator` moved to an assertion in another block, `statement_sha256` left as it was | **digest binding.** The digest is recomputed from the newly cited statement and will not match. |
| b `LOCATOR_REPOINTED_COHERENT_DIGEST` | locator and digest both moved; the capture's own formalizations stay where they were | **trace derivation.** The digest binding is satisfied by construction. Nothing at admission compares a record's cited locator with the locators the plan derives it from, so only a post-admission cross-check of export against trace can see it. |
| b `LOCATOR_REPOINTED_COHERENT_DERIVATION` | locator, digest and every formalization of the record moved together to one assertion in another block, with the same modality | **none, review only.** Nothing inside the change set disagrees with anything else. Only reading the source finds it. |
| c `DIGEST_MISMATCH` | `statement_sha256` replaced with the digest of synthetic bytes | **digest binding.** |
| d `DANGLING_ENDPOINT` | one relation's `target_id` pointed at an absent record identity | **admission structural check.** |
| e `TYPE_OUTSIDE_ONTOLOGY` | record `type` replaced with a type the closure does not declare | **compiler.** |
| e `SLOT_OUTSIDE_ONTOLOGY` | an undeclared property added and cited from one of the record's own assertions, so the fault reaches the contract instead of the adapter's formalization-target check | **compiler.** |
| f `DUPLICATE_RECORD_ID` | one record carried twice in its own family | **admission structural check** is the mechanism the plan compiler declares (`DUPLICATE_RECORD_ID`). The adapter's record snapshot refuses a repeated ID first, under `MALFORMED_CAPTURE`, so through this path the later mechanism is unreachable. Both are refusals; the observed one is recorded. |
| g `RECORD_WITH_NO_SOURCE_WITH_FIELDS` | a new record, one property, no assertion formalizes it | **admission structural check** (`UNDERIVED_FIELD`). |
| g `RECORD_WITH_NO_SOURCE_NO_FIELDS` | the same record carrying no property at all | **none, review only, predicted.** `UNDERIVED_FIELD` is computed over the record's `properties` keys and the two relation endpoints. A record with no properties key has nothing required of it. |

Class (b) is one class with three constructions because the code gives it three
different answers, and reporting only one of them would be the same
selective-reporting problem this cell exists to fix. They are reported as
separate rows and counted separately.

## Outcomes

Fifty-five trials, five per construction, one `run.py` process each. Thirty-five
refused, twenty admitted. Every class landed on the outcome its mechanism
implies; no expectation was adjusted after a result.

| # | class | fault | designed catcher | n | observed outcome | typed diagnostic |
| :-- | :-- | :-- | :-- | --: | :-- | :-- |
| 1 | a | `VALUE_NOT_IN_BLOCK` | none, review only | 5 | ADMITTED, invisible | - |
| 2 | b | `LOCATOR_REPOINTED_STALE_DIGEST` | digest binding | 5 | REFUSED | `DIGEST_MISMATCH` |
| 3 | b | `LOCATOR_REPOINTED_COHERENT_DIGEST` | trace derivation | 5 | ADMITTED, exposed | - |
| 4 | b | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | none, review only | 5 | ADMITTED, invisible | - |
| 5 | c | `DIGEST_MISMATCH` | digest binding | 5 | REFUSED | `DIGEST_MISMATCH` |
| 6 | d | `DANGLING_ENDPOINT` | admission structural check | 5 | REFUSED | `DANGLING_ENDPOINT` |
| 7 | e | `TYPE_OUTSIDE_ONTOLOGY` | compiler | 5 | REFUSED | `RECORDS_NOT_REHYDRATABLE` |
| 8 | e | `SLOT_OUTSIDE_ONTOLOGY` | compiler | 5 | REFUSED | `RECORDS_NOT_REHYDRATABLE` |
| 9 | f | `DUPLICATE_RECORD_ID` | admission structural check | 5 | REFUSED | `MALFORMED_CAPTURE` |
| 10 | g | `RECORD_WITH_NO_SOURCE_WITH_FIELDS` | admission structural check | 5 | REFUSED | `UNDERIVED_FIELD` |
| 11 | g | `RECORD_WITH_NO_SOURCE_NO_FIELDS` | none, review only | 5 | ADMITTED, invisible | - |

One diagnostic per reason, verbatim from the runner's stderr:

- `DIGEST_MISMATCH` (b1-01): `record claim:compilation-covariates names
  assertion assertion:260 with statement digest sha256:2b2c79b9…, and that
  assertion's statement digests to sha256:43014b48…`
- `DANGLING_ENDPOINT` (d-01): `relation rel:hash-used-for-focal has absent
  target_id: fault:d:01:absent-endpoint`
- `RECORDS_NOT_REHYDRATABLE` (et-01): `entities[286] 'claim:focal-not-robust':
  Unknown entity type: 'FaultInjectedTypeE01'`
- `RECORDS_NOT_REHYDRATABLE` (es-01): `entities[162]
  'claim:degassing-volume-change': Unknown property 'fault_injected_slot_e01'
  for Claim`
- `MALFORMED_CAPTURE` (f-01): `repeated record ID: claim:updated-depth-data`
- `UNDERIVED_FIELD` (gw-01): `record fields lack derivations:
  fault:g:with_fields:01:['properties', 'name']; every properties key and both
  relation endpoints need a derivation, type and id do not`

### Every refusal left the history where the honest run left it

Each of the 35 refusals wrote a seven-event ledger: five `ARTIFACT_REGISTERED`,
one `SOURCE_REGISTERED`, one `ARTIFACT_REGISTERED`. None of the four admission
events (`KNOWLEDGE_CHANGE_SET_RETAINED`, `CHANGE_PROPOSED`, `CHECK_RECORDED`,
`VERDICT_RECORDED`) appears in any of them. Thirty of the 35 ledgers are a
byte-exact prefix of the control's fourteen-event ledger. The five that are not
are the `SLOT_OUTSIDE_ONTOLOGY` trials, which change the capture itself: their
first six events are byte-identical to the control's and the seventh, the
retained evidence, differs because it retains different capture bytes. That is
the retention doing its job, not the admission leaking.

After all 55 trials, the honest population was run again through the same
runner. It returned
`sha256:a3abceec58dc93692cbdeabf9a95c03551177ba97d9ee4225fe29198f37f1eec`,
run-23's frozen receipt.

### Every admission carried its fault into the graph

An admission is only a finding if the fault is really in the records that came
back, so each of the 20 was checked against the run's own
`export-records.json`. All 20 witnessed. Examples: `a-01` put
`FAULT-A-01-SYNTHETIC` in `gchem:eq-atlantic-co2-avg.analyte`, a value nothing
in the reading contains, and the record still cites `assertion:129` with a
digest that verifies; `gn-01` added `GeologicFeature` records with no property
and no source, and the graph came back with 418 entities instead of 417.
No admitted trial reproduces run-23's receipt, which is the same statement from
the other side: each faulted graph is a different graph.

### What exposed the five that were exposed

`verify.locator_disagreements` compares each exported record's
`assertion_locator` with the locators its trace derives it from. It reports
nothing on the control and on 15 of the 20 admissions, and exactly one record
on each of the five `LOCATOR_REPOINTED_COHERENT_DIGEST` trials. For `b2-01`:
`claim:deep-events-not-artifacts` cites `assertion:118` and is derived from
`assertion:178`. `verify.digest_disagreements`, which replays the gate's own
digest binding from outside, reports nothing anywhere, as it must: it is the
check that already ran at admission.

## Gaps, with reproducers

Three constructions were admitted with nothing in the run's own artifacts to
show for them. Each is a property of the code at
`c95dba7b86bb61487bda9a52458e1ea47cce20ab` and none was fixed.

**1. No mechanism reads a property value against the sentence it cites.**
The adapter checks that a *statement* is verbatim in its block and that the
statement's *digest* matches. Nothing compares the value a record carries with
the statement behind it. A producer can copy a sentence honestly, bind it by
digest, and put any well-typed value it likes in the record.

    .venv/bin/python paper-v4/experiment-v4/fault-injection-01/run_faults.py \
        --producer private/paper-v4-v4-run-23/producer \
        --private private/paper-v4-fault-injection-01 --only a-01

**2. A record's own locator is never compared with the locators it is derived
from.** `_digest_defects` asks only that the cited assertion exists in this
capture and that the digest matches *that* assertion. It never asks whether
the capture formalizes the record from that assertion. Trial `b2-01` cites one
sentence and is derived from another, in a different block, and is admitted.
The disagreement is visible afterwards, from the export and the trace summary,
which is why this row reads ADMITTED-exposed rather than invisible; no code on
the admission path makes that comparison. Reproducer: `--only b2-01`.

**3. A coherent relocation is invisible.** Move the record's locator, its
digest and every formalization of it onto one sentence in another block with
the same modality, and nothing inside the change set disagrees with anything
else. Trial `b4-01` moves `cnt:subsections` from `assertion:023`
(`page:1:block:005`) to `assertion:247` (`page:9:block:039`). Admitted, both
post-admission checks clean. Only reading the source finds it. Reproducer:
`--only b4-01`.

**4. A record with no properties has no derivation required of it.**
`UNDERIVED_FIELD` is computed over a record's `properties` keys and the two
relation endpoints. An entity with `"properties": {}` has neither, so a record
with no source at all is admitted and counted in the graph. Reproducer:
`--only gn-01`.

Two further observations, both about reach rather than about a fault getting
through:

**5. The digest binding is opt-in and covers 236 of run-23's 440 records.**
`assertion_locator` and `statement_sha256` are optional slots declared on five
types (`Claim`, `GeophysicalObservation`, `GeochemicalObservation`,
`CountObservation`, `ElementRatio`). The other 204 admitted records are of
types that do not declare them, so classes (b) and (c) cannot be constructed
against those records at all: there is no locator to repoint and no digest to
break. Run-23's producer opted in for every record that could. A producer that
opted out would be admitted with `provenance_coverage` reporting zero and no
refusal; the census is what makes that visible, and the census is a number, not
a gate.

**6. The plan compiler's `DUPLICATE_RECORD_ID` is unreachable through this
path.** The adapter's record snapshot refuses a repeated record ID first, under
`MALFORMED_CAPTURE`. Both are refusals, so class (f) is caught either way, but
the mechanism the task's classification names for it is not the one that fires,
and this cell did not exercise it.

## Inputs and outputs, by digest

| artifact | sha256 |
| :-- | :-- |
| Core commit | `c95dba7b86bb61487bda9a52458e1ea47cce20ab` |
| selected reading | `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17` |
| accepted ontology | `sha256:9aa5fdcfb74dc9cad9b36b16b27e8a829b5a71ad1b2bc61892e12a2568b06d21` |
| honest population | `sha256:9d608bffe7cb1259d1f397e6d272290a5e21073744847b6d32a0994543416fd3` |
| control replay receipt | `sha256:a3abceec58dc93692cbdeabf9a95c03551177ba97d9ee4225fe29198f37f1eec` |
| control export records | `sha256:0634e0696a34bc2cc736f84dbeadf6b65416ebcd9f84f0e67eeb11bb9a44a286` |
| control ledger bytes | `sha256:d5ef64c0ca6558967aa664705aa9661d3aec399d73c94aa7a5286ea6a991a908` |
| `outcomes.json` | `sha256:7b7dd161a969f099af5f28f139e74f98198081b73185173dae84b2a74429adb9` |

The control's receipt, export and ledger bytes are run-23's own, reproduced
here from the frozen inputs before any fault was injected. Every trial's
population digest, ledger digest, receipt and diagnostic is in `outcomes.json`.

## Reproducing

    # all 55 trials, about twenty minutes
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
      paper-v4/experiment-v4/fault-injection-01/run_faults.py \
      --producer private/paper-v4-v4-run-23/producer \
      --private private/paper-v4-fault-injection-01

    # the contract
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
      paper-v4/experiment-v4/fault-injection-01/test_faults.py

RED, before any trial ran: 26 failed, 4 passed. GREEN, after: 30 passed.
`ruff check` and `ruff format --check` pass on all four files.

## What was not done

- **Only run-23.** The other six model-produced populations the paper reports
  were not faulted. Nothing here is a claim about them, though the mechanisms
  are Core's and not run-23's.
- **The admission check proper was never reached.** All seven classes are
  caught by the adapter, the digest binding or the plan compiler, or admitted.
  No fault in this set exercises `admit_structural_change`, the structural
  admission policy or the history machine.
- **No supersession fault.** Run-23 carries zero supersessions, so the
  supersession branches (`SUPERSESSION_FORK`, `SUPERSESSION_TYPE_MISMATCH`,
  `SUPERSESSION_VALID_TIME_MISMATCH`) have nothing to be injected into here.
- **No effect on answers was measured.** The table is about admission only. A
  faulted record that is admitted may or may not change what a query returns or
  what a reviewer scores; this cell ran no query and no review.
- **Nothing in Core was changed.** Four constructions passed that arguably
  ought not to. They are recorded above with reproducers and left alone, which
  is the point: making the gate pass the test is the move this experiment
  exists to expose.
- **The seven classes are the task's, not an exhaustive set.** A fault this
  catalog does not construct is not evidence of anything.

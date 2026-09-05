# Appendix evidence catalogue

Read at repository commit `77058f7326a03e788da0b3d6f40484ad9b1e8337` on
2026-09-05. Every snippet under `snippets/` is a verbatim excerpt of a public
repository artifact, named by path and commit in its own header, and cut to at
most 40 lines including that header. Nothing here is copied from `private/` or
from any file listed in a cell's `results/withheld-artifacts.json`.

The Fahland shop fixture carries no reading text and is used wherever a claim
needs a plan, ledger, receipt or trace shape the document runs can only publish
by digest.

Each claim below is a claim the manuscript makes about the mechanism. Under it:
the smallest public artifact that evidences it, and one sentence saying what to
look at. Claims with no retained public artifact are listed last, as gaps.

---

## 1. Typed refusals

The mechanism refuses with a named reason and a detail, never with a repair or a
silent drop.

| snippet | what to see |
| --- | --- |
| `01-typed-refusal-reasons-document-adapter.txt` | The closed enumeration of every refusal the public document adapter can raise; there is no untyped failure branch and no fallback. |
| `02-typed-refusal-grounding-aggregate.json` | A real refusal as the producer received it: reason, stage, count of offending subjects, and the ontology digest it refused. |
| `03-typed-refusal-chained-cause.json` | A compilation refusal whose actionable cause sits in the chained exception; the recorded attempt carries both the reason and the cause. |
| `05-aggregated-underived-fields.txt` | The refusal text names the rule it enforces, so a producer learns the rule from the refusal rather than by guessing. |

## 2. Deterministic lowering

A capture becomes a neutral plan and then an ordered change set by
deterministic code, with canonical bytes and a digest at every hop.

| snippet | what to see |
| --- | --- |
| `22-deterministic-lowering-plan.json` | One neutral population plan: contract identity, grammar, history profile, sources by digest, records in the public record shape, one derivation per field with its locator, valid time. The retained file is a single canonical line. |
| `23-compiler-ir-validated-contract.json` | Compilation output is a flat subject-predicate-object fact set with its own digest, plus the exact adapter, metamodel, canonicalizer and symbol-policy identities that produced it. |
| `24-population-surface-families.txt` | The admissible surface handed to the producer is derived from the compiled contract and the bound profile, not chosen by the evaluator. |
| `21-shop-calibration-assertions.txt` | The fixture's own test asserts that a rerun emits byte-identical evidence. |

## 3. Agreement between admitted and replayed state

| snippet | what to see |
| --- | --- |
| `09-replay-equality-run-05.json` | `reopen_matches_admitted` is true for both the receipt and the export after the in-memory handles were discarded and the file-backed ledger reopened; the admitted and replayed receipt digests are the same string. |
| `10-replay-equality-shop.json` | The same property with no model in the path: 48 ledger events, five change sets, one additive contract revision, nine current and ten historical records. |
| `21-shop-calibration-assertions.txt` | The assertions that hold it: identical evidence bytes across two runs, identical receipt, identical node and relation sets, and an unchanged ledger file after tracing. |

## 4. Write-time validation

Checks run on the write, not on the proposal, and a failed check leaves nothing
behind.

| snippet | what to see |
| --- | --- |
| `06-write-time-verbatim-check.txt` | The verbatim rule as executable code: the captured statement must be a substring of its named block after whitespace collapse, checked before a plan exists. |
| `07-write-time-validation-staged-properties.txt` | The ontology validator runs against the staged graph write; the docstring records why the frozen change-set view has to be thawed first. |
| `25-atomic-admission.txt` | One call validates and admits; the check event is generated inside the call and persisted only if the batch passes, and a stale base refuses before any append. |
| `05-aggregated-underived-fields.txt` | Every properties key and both relation endpoints must carry a derivation before a plan compiles. |

## 5. Aggregated diagnostics

A refusal reports the whole defect set for its class, so a fixed correction
budget is not spent one item at a time.

| snippet | what to see |
| --- | --- |
| `02-typed-refusal-grounding-aggregate.json` | Ten ungrounded project classes in one refusal. |
| `04-aggregated-locator-refusal.txt` | Every unknown block and every non-verbatim statement collected, sorted and rendered into one refusal that also states the method. |
| `05-aggregated-underived-fields.txt` | Every underived field in one `UNDERIVED_FIELD` refusal. |

Read with the gaps section below: three refusal classes in the same adapter are
still one-at-a-time.

## 6. The two-axis census

| snippet | what to see |
| --- | --- |
| `11-two-axis-census.txt` | Three cells side by side. Blocks reviewed against blocks total is one axis; fully, partly and unformalized assertions is the other. They move independently: run-05 reviewed 27 of 186 blocks with one partly formalized assertion, run-04 reviewed all 186 with twenty unformalized. |
| `12-typed-gap-kinds-closed-set.txt` | The gap vocabulary is a closed set in Core; a producer cannot mint a kind. |

## 7. Provenance trace to a reading block

| snippet | what to see |
| --- | --- |
| `13-provenance-trace-document.json` | One replayed record resolved back through its change set, plan, history profile and retained evidence to the assertion locator it was read from; the locator names the reading block, and evidence is selected by record id, never by list position. |
| `14-provenance-trace-shop.json` | The same trace with no model in the path, where the locator is a source row rather than a reading block. |
| `15-supersession-shop.json` | The property the document runs do not exercise: a later change supersedes an earlier record and both stay in history. |

## 8. The type-only binding

| snippet | what to see |
| --- | --- |
| `16-type-only-binding.json` | The binding is pinned to the replay receipt it was written after, and each case names only a source record type, a relation record type, a target record type and projected field names. No record id, locator, value or expected row count appears. |

## 9. Guarded query execution

| snippet | what to see |
| --- | --- |
| `17-guarded-query-region.json` | Row counts per question beside three forbidden-attempt counters at zero: file reads, network calls, imports of named embedding packages. The same block records the replay receipt the binding was frozen against. |

## 10. The leak threshold

| snippet | what to see |
| --- | --- |
| `18-leak-threshold-record.json` | The frozen rule and the measurement ladder: no public file may share a 60-character run with any reading block after whitespace collapse. Every public file measures zero; each withheld file is named by identity and by what it carries. |
| `19-leak-check-test.txt` | The rule as an executable test that enumerates every 60-character window of every block and asserts no frozen artifact contains one. |

## 11. The shop calibration

| snippet | what to see |
| --- | --- |
| `20-shop-attribution.json` | The domain is transcribed, not designed: the chapter DOI, `Table 1` as the source locator, the transcription classification, the accepted claims and the explicitly excluded ones. |
| `10-replay-equality-shop.json` | What the calibration produced: five change sets, one additive contract revision, 48 events, nine current and ten historical records, and its own stated limitations. |
| `21-shop-calibration-assertions.txt` | The test that holds all of it. |
| `22-deterministic-lowering-plan.json` | One of the five adopter-authored plans, public in the repository. |
| `15-supersession-shop.json` | The supersession the document runs never reach. |

## 12. Governance and ledger entry shape

| snippet | what to see |
| --- | --- |
| `08-governance-ledger-entry-shape.json` | One hash-linked governance entry: typed, sequenced, linked to its predecessor by digest, carrying the before and after digest of every file the change touched and the commits that evidence it. |

---

## Claims with no retained public artifact

These are manuscript or journal claims the repository cannot currently support
from a public file. Each is a defect entry in
`handover/2026-09-05-deep-sweep.md`.

1. **Producer isolation.** The read set, the no-network rule and the no-delegation
   rule are recorded as declarations in the spawn message and the run contract.
   Nothing observes them. The manuscript already states this; there is no
   artifact to add.
2. **No fallback and no hand repair.** Recorded as boolean fields
   (`fallback_used`, `hand_repair_used`) written by the parent. No mechanism
   produces them.
3. **Producer cost per cell.** Only run-04 and run-05 publish `results/usage.json`.
   The token figures the overseer journal reports for run-02, run-03, run-06 and
   run-07 exist only in `private/paper-v4-v4-run-0N/usage.json`.
4. **Run-02's source-grounded review.** `paper-v4/evaluation-v4/review-record.preliminary.md`
   is `PRELIMINARY_COMPLETE` with `ratification.disposition` `PENDING`. There is no
   human ratification record for run-02.
5. **Reference veracity.** `paper-v4/test_publication_consistency.py::test_arxiv_citations_and_reproduction_coordinate_are_closed`
   checks that every citation key resolves to a bibliography entry. Nothing
   checks that a bibliography entry describes a work that exists. This is the
   same gap the run-06 fabricated grounding citation exposed one layer down.
6. **Run-04's discarded query bindings.** `results/launch-log.json` names
   `results/native-query-binding.draft-01.json` and `draft-02.json` at paths that
   hold no such files; both drafts and their query outputs are under `private/`
   and appear in no withheld list.
7. **The run-05 diagnostic actually returned to the producer.**
   `ontology-run/attempt-01-diagnostic.json` carries the bare reason. The chained
   cause the producer received is recorded only in `result.json` and the launch
   log, so the retained diagnostic is not the artifact the producer saw.
8. **The damaged-block count in manuscript §4.5.** "Twenty-seven of the 186
   blocks carry a run like that" is reproducible from the private reading at one
   detection threshold and moves between 13 and 49 at nearby ones. The rule is
   not stated and no per-block list is retained.
9. **"137 distinct quantity kinds" (ledger E-0125).** The count of distinct
   `quantity_kind` strings in run-02 cannot be recomputed from any public file;
   the values are in the withheld export. The public trace summary supports only
   "137 records carry a `quantity_kind` derivation".

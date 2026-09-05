# Appendix evidence catalogue

Read at repository commit `77058f7326a03e788da0b3d6f40484ad9b1e8337` on
2026-09-05. Snippets 01 to 25 under `snippets/` are verbatim excerpts of public
repository artifacts, named by path and commit in their own headers, and cut to
at most 40 lines including that header. Nothing in sections 1 to 12 is copied
from `private/` or from any file listed in a cell's
`results/withheld-artifacts.json`. Snippets 26 to 43 and sections 13 to 20 were
added later, at a second read coordinate, and state their own rule; five of them
quote a private diagnostic's own text and say so.

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

---

# The loop of 2026-09-05 and the matrix pass

Read at repository commit `dd55ecd898f56be55fc7c254fbffd6dab2ea99e7`. Everything
above was read at `77058f73` and is left as it was written, except the opening
paragraph, whose scope this extension made wrong: it said every snippet was
public, and five of the ones added here are not.

The night loop ran seven iterations, runs 09 to 15, one named change per cell
with its hypothesis and its falsifier written before the cell ran. Runs 16 and
17 are not iterations: they are the matrix pass, run-15's harness byte for byte
with the producer's model moved, Sonnet 5 and then Haiku 4.5. The journal is
`handover/2026-09-05-overseer-journal.md` from "Night loop"; the per-cell RCAs
are `handover/2026-09-05-v4{3,4,5,6,7,8,9}-rca.md`,
`handover/2026-09-05-run-16-sonnet-rca.md` and
`handover/2026-09-05-run-17-haiku-rca.md`.

Short commits used below, in full: `f6c8c71fd95711fd8f1bec811dff94cd61e535a0`
(run-09's Core coordinate), `dc5254795a78648591d3a1b0bcf602af8d443dc1` (Core-18,
the coordinate runs 14 to 17 pin), `8a6c3f384d02105ad880d0d91f85d8e45f85cff9`
(Core-19), `dd55ecd898f56be55fc7c254fbffd6dab2ea99e7` (the read coordinate),
and the freeze commits `4e96118` (run-13), `e10be6e` (run-14), `139e2ab`
(run-15), `1d06352` (run-16).

**The rule every snippet is held to.** Nothing public may reproduce the reading.
The measure is the one the freezes run: with Unicode whitespace collapsed to one
space, a public file shares no run of 60 characters with any block of
`private/paper-v4-text-layer/selected-reading.json`. Each entry below records
the exact maximum shared run of its snippet, computed as a longest common
substring against the 186 blocks separately, so no match crosses a block
boundary. The check was calibrated on a known leak before it was trusted:
`paper-v4/experiment-v4/run-03/ontology-run/ontology-01.yaml` measures 73, the
article title, which is the run E-0124 located and justified.

**Where a private file is the evidence.** Five snippets quote a diagnostic under
`private/`. Only the diagnostic's own text is reproduced: its head, its record
ids, its reason names, its counts and the rule sentence it closes with. No
statement and no reading block appears. Each source diagnostic was measured
whole before anything was cut from it: run-14's attempt 01 measures 21, run-16's
50-defect attempt 01 measures 35 (a subject's name forms, well under the
threshold), run-17's three attempts measure 13, 13 and 9. Nothing had to be
elided, and no marked ellipsis stands for a name.

---

## 13. The subject element

**Claim.** A source-asserted record names the thing it is about, the adapter
refuses a subject the sentence that asserts it does not name, and how much
attachment a capture left unmade is reported on an axis that gates nothing
(E-0141 to E-0143).

- `26-subject-not-named-refusal.txt` — `src/malleus/_contract_pipeline/document.py`
  at `f6c8c71`; `sha256:ab0b897264e3d5b3d24da263ec44c1fb66b20004954e0115a9a7819dced512e8`;
  maximum shared run 15.
  The derivation rule the refusal states, then the check itself: the name is
  read from this change set, the comparison is whitespace-collapsed and
  case-folded, and the message names the record, the subject, the name it
  looked for and the assertion it looked in.
- `27-subject-coverage-census.txt` — the same file at `f6c8c71`;
  `sha256:3a92fa62d3602a7967c5d274eb80700b600ecec34c1e49309cfc4b460959430e`;
  maximum shared run 13.
  One axis, reported and never refused, and which types may carry a subject is
  a contract question the adapter asks rather than a list it holds. Run-09's
  frozen `results/census.json` reads 106 of 212.

## 14. The word rule

**Claim.** The comparison the subject check rests on matches a name as a word
and not as a substring, and the loosening it replaced had produced eight of
run-12's fifteen wrong projections (E-0158 to E-0161).

- `28-word-rule-predicate.txt` — `src/malleus/_contract_pipeline/document.py`
  at `dc52547`; `sha256:02d22e30ae5621254d64bc99eb0a1884fabe54ef308d7fb12a5e0b3ec90691b0`;
  maximum shared run 14.
  One predicate at both sites, the refusal and the census. Digits, punctuation
  and the ends of the statement bound a word; letters do not. Neither side is
  rewritten.
- `29-word-rule-fixtures.txt` — `tests/contract_compiler/pareto/test_document_assertion_adapter.py`
  at `dc52547`; `sha256:e33ee47277ada90ef17c5e3dbe217002e1c6259764612a0c6d6328121b28a878`;
  maximum shared run 17.
  The two cases that fix the boundary in both directions: a three-letter tag
  inside "vertical" names nothing and refuses; a citation number the text layer
  glues on, "lithosphere13", still names its entity and admits.
- `30-word-rule-correction-e-0160.txt` — `paper-v4/paper-ledger.md` at `dd55ecd`;
  `sha256:d2c09a22244f8cf888e79f0cbcd0505979dd9a7215c98d243a204901b56e6c50`;
  maximum shared run 15.
  The correction the rule forced on the record: eight of fifteen were the
  check's own artefact, the earlier attribution rests on three or four cases,
  and the entry states what the correction does not touch.

## 15. The withdrawal of projection

**Claim.** The adapter sets no subject and reports four outcomes instead, after
a derived subject was wrong thirteen times in fifteen and the producer, knowing
the rule, narrowed its own evidence to avoid it (E-0155, E-0157, E-0158,
E-0159; decision 22).

- `31-projection-withdrawn-decision-22.txt` — `design/KNOWLEDGE_PACKS.md` at
  `dd55ecd`; `sha256:ab6731599c3f41feb067e0d325c6b1a590f7924fbf25177a4f16b82da5dcd7f1`;
  maximum shared run 18.
  Both effects in the decision's own words, and the reason a report replaced a
  rule: a rule the producer can see is a rule the producer works around, and a
  count the producer never reads it cannot.
- `32-subject-outcomes-adapter.txt` — `src/malleus/_contract_pipeline/document.py`
  at `dc52547`; `sha256:10b3578f63d19a41dc79b808c85df13e2b6f50b5bac6e87d1eaf4ac1561b7afb`;
  maximum shared run 10.
  The four outcome names as a closed tuple and the classification that assigns
  them. A producer-set subject is `proposed` and nothing else is computed for
  it; the other three describe what the producer left unset.
- `33-subject-census-run-13.txt` — `paper-v4/experiment-v4/run-13/results/census.json`
  at `dd55ecd`, the cell frozen at `4e96118`;
  `sha256:7cd0ad15ebe74d41aff4af1d6e983d6eea66c4e54acede4ca0e8073e7ad8e3f8`;
  maximum shared run 11.
  The first cell to run with nothing derived: 269 subject-bearing records, 111
  proposed, 33 attachable, 49 ambiguous, 76 unnamed, per type and summed.

## 16. One row per witness

**Claim.** The executor's removal was measured on already-judged rows before it
ran, and it takes run-09's 1,466 rows to 463 without dropping a witness or
moving a label (E-0166).

- `34-one-row-per-witness-offline-validation.json` —
  `paper-v4/experiment-v4/run-15/offline-validation.json` at `dd55ecd`;
  `sha256:351b6df97d5cc1d5e1851aeb8a863a80dd5432c142acc6b1cef0f9cc6b2e4e4d`;
  maximum shared run 13.
  `executes: NOTHING`: the file is a measurement over run-09's frozen rows, not
  a run. 1,466 rows, 630 after the ENTITY restriction, 463 after one row per
  witness; 167 of the 630 were re-projections of a witness the same question had
  already returned, and none of them carried a different label. The file states
  its own non-claim: what the numbers bound is the review, not the result.

## 17. Producer variance at a fixed protocol

**Claim.** At one Core coordinate, one skill and one reading, the axis that
separates the producers is what each verifies before it stops, not what it can
write (E-0164, E-0172, E-0176).

- `35-run-14-runner-diagnostic.txt` —
  `private/paper-v4-v4-run-14/refused-runner-attempt-01/diagnostic.txt`, the
  cell frozen at `e10be6e`;
  `sha256:a89bf212bf040a4d020d286614d86f41fddf256b49089759d664e5eb8b30a43b`;
  maximum shared run 21.
  An Opus cell's one return: seven defects in one refusal, six of them a
  modality the producer's own validator did not check against Core-14's
  equality, and one subject the text layer had glued to the word before it.
- `36-run-16-runner-diagnostic.txt` —
  `private/paper-v4-v4-run-16/refused-runner-attempt-01/diagnostic.txt`, the
  cell frozen at `1d06352`;
  `sha256:d7c1405413890174dd413ee2dfda581089405148543bf21fa8dbe412a6d93358`;
  maximum shared run 21.
  The Sonnet cell's one return at the same protocol: fifty defects in one
  refusal, 45 SUBJECT_NOT_NAMED, 4 MODALITY_NOT_ASSERTED, 1
  EVALUATIVE_SLOT_NOT_EVALUATED. Its validator checked the two rules the
  adapter also checks and none of the three derivation-content rules.
- `37-run-17-runner-diagnostics.txt` —
  `private/paper-v4-v4-run-17/refused-runner-attempt-0{1,2,3}/diagnostic.txt`;
  `sha256:e32c651f756cb169d35dec7b26c2a185019e08162cd23cb827be679aefb5a6fb`;
  maximum shared run 13.
  The Haiku cell's three refusals in order: eight retyped statements
  NOT_VERBATIM in one aggregation, then graph rehydration, then GAP_REQUIRED,
  terminal. The middle one is a bare `ValueError`, the one refusal the cells
  met that carried no typed reason; Core-19 wrapped it as
  `RECORDS_NOT_REHYDRATABLE`.
- `38-producer-model-and-cost.txt` —
  `paper-v4/experiment-v4/run-1{3,4,5,6}/results/usage.json` at `dd55ecd`, and
  `paper-v4/paper-ledger.md` E-0176 for run-17;
  `sha256:c2284ff048daf8dfa57d11b657d5c0b9538223dba591199e793d1f4a0a0ac13c`;
  maximum shared run 12.
  Model and producer tokens per cell beside the outcome, with the per-stage
  split. Run-17's usage.json is private; its figures are the ledger's.

## 18. The anchors

**Claim.** Run-16's producer met the subject rule by attaching one naming clause
to many records, and the census reported the shape before the review judged it
(E-0172, E-0173).

- `39-anchor-census-run-16-run-15.txt` —
  `paper-v4/experiment-v4/run-1{5,6}/results/census.json` at `dd55ecd`, the
  cells frozen at `139e2ab` and `1d06352`;
  `sha256:abaf61331ac506551e2f5cc8e38c39c1a6a1dca453e9c076bdaf2b05585d2b02`;
  maximum shared run 14.
  Run-16: 20 of 32 relations derive from a sentence that is not the relation's
  own, and one 33-character clause on page 1 block 5 formalizes 17 records.
  Run-15, the Opus cell it copies byte for byte: no non-local relation at all,
  and its two large fan-outs (24 and 21) are the reference list, not a subject
  anchor. The per-assertion fan-out map is elided; its distribution is kept.

## 19. Core-19's census shapes

**Claim.** After two matrix cells walked through what the census could not
distinguish, it labels each block and counts how many records carry the route
back to their sentence; neither changes what is admitted (E-0173, E-0176;
decision 24).

- `40-core-19-block-labels.txt` — `tests/contract_compiler/pareto/test_document_assertion_adapter.py`
  at `8a6c3f3`; `sha256:060c2ee11d6f580468bdad82364c7d463a243fe65850ab0f26321801e8aaf6d1`;
  maximum shared run 11.
  `ASSERTED`, `DECLARED_NOTHING_ASSERTABLE` and `UNTOUCHED` with a count each,
  `blocks_reviewed` kept as their sum, and one assertion outweighing a
  declaration beside it.
- `41-core-19-provenance-coverage.txt` — the same file at `8a6c3f3`;
  `sha256:e57771582d6fab224d8afbc998ff4550aa0b7aa8cdd7b3d221e3c415376a33a6`;
  maximum shared run 11.
  `total`, `with_locator` and `with_digest` per locator-bearing type. Which
  types carry the route is a contract question, asked exactly as the subject
  axis asks its own; with no compiled contract the axis is empty.
- `42-core-19-five-cell-census.txt` — `handover/2026-09-05-overseer-journal.md`
  at `dd55ecd`; `sha256:c61ae14297c51a8d8bbcb241ff2977d9b77adca6e6547eba50735fa6b7c423ae`;
  maximum shared run 11.
  The new census applied by script to the five frozen captures. Coverage for
  the paper is `blocks_asserted` (184, 184, 185, 58, 7), not `blocks_reviewed`,
  which reads 186 for run-13, run-15 and run-16 alike.

## 20. The preliminary review outcomes of runs 13 to 16

**Claim.** Across 1,867 rows in the three Opus cells no row was judged
UNSUPPORTED and every digest token written read DIGEST_OK; the Sonnet cell wrote
no digest token at all, because no record it admitted carries a locator
(E-0161, E-0165, E-0169, E-0173).

- `43-review-outcomes-runs-13-16.txt` —
  `paper-v4/evaluation-v4/run-1{3,4,5,6}/review-record.preliminary.md` at
  `dd55ecd`; `sha256:81089ddcef3f3dce18851b807cca214065e2460b732a4416640ab9bc0e56534e`;
  maximum shared run 13.
  Responsiveness per question, support counts and digest tokens, counted from
  each record's own JSON block. No rationale is quoted.

**Non-claim, and it governs the whole of entry 20.** All four records are
`PRELIMINARY_COMPLETE` with `ratification.disposition` `PENDING` and
`ratification.actor_id` `actor:luis`. They are a preliminary reader's reading,
not paper evidence, and they stay that way until the author ratifies them. The
same holds for every review figure quoted in entries 13 to 19. This is the same
gap item 4 of the list above records for run-02.

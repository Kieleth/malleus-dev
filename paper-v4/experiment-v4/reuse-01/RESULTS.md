# reuse-01: one second question set, one graph, one document

Reporting correction, 2026-09-13, approved by Luis. Include this bounded reuse
measurement with both cost accounts. Do not infer a measured break-even point,
comparative precision or cross-session learning. The controls are defective
and excluded from comparative conclusions. Frozen inputs and reviews are unchanged.

This cell does it once. A second, independent set of thirty questions was
authored from the selected reading alone, by a session that had seen no
ontology, no graph, no capture and no earlier question file. It was put to
run-23's already accepted and frozen graph, and to a fresh in-context session,
and both were reviewed under protocol v3.2.

Every figure below comes from a script that ran. The counts are
`paper-v4/experiment-v4/reuse-01/read_results.py` reading the two preliminary
review records, the two input manifests, the question files and the launch logs.
Nothing here is human-ratified. Luis approved reporting these results as
model-assisted evidence with that limitation, not upgrading their status.

## What was measured, and what was not

- **The graph did not move.** No producer ran, no ontology was authored, nothing
  was captured, admitted, disposed or replayed. The ledger at
  `private/paper-v4-v4-run-23/ledger/history.jsonl` was opened read-only and its
  sha256 was `d5ef64c0ca6558967aa664705aa9661d3aec399d73c94aa7a5286ea6a991a908`
  before the query and after it. The ledger head, the replay receipt, the
  accepted ontology and the validated contract are run-23's own, read out of
  run-23's frozen `results/run-result.json`.
- **The question set is independent, not a revision.** Set A
  (`competency-questions-v3.1.json`) stays frozen and binds run-24, run-25 and
  baseline-01. Set B carries the prefix `CQ-B-` so no id of either can be
  mistaken for the other's. Both carry 25 positive questions in five tiers of
  five and, by coincidence of authoring rather than by design, both carry exactly
  102 required elements over those 25 questions. Equal denominators do not
  make their requirements or difficulty equivalent.
- **One document, one graph, one second set, one model family.** This is a
  measurement, not a statistical result.

## The two sets

| | Set A (`v3.1`) | Set B |
| --- | ---: | ---: |
| questions | 30 | 30 |
| positive questions | 25 | 25 |
| required elements over the positives | 102 | 102 |
| required elements over all thirty | 120 | 121 |

Set B is frozen at `paper-v4/experiment-v4/competency-questions-set-b.json`,
`sha256:1d2d1c0f589432ab24b6d4ba6817c0bab3abbce5172364e394bed5a307e10bcf`.

## Elements reached, per tier

Over the 25 positive questions, 102 elements. The graph column is run-23's
frozen graph queried with set B; the baseline column is a fresh session given
the reading and set B.

| Tier | | Graph | In-context |
| --- | --- | ---: | ---: |
| T1 direct facts | of 18 | 15 | 18 |
| T2 relationships | of 21 | 13 | 20 |
| T3 quantities | of 21 | 19 | 21 |
| T4 qualifications | of 21 | 20 | 21 |
| T5 composition | of 21 | 21 | 21 |
| **positive total** | **of 102** | **88** | **101** |
| controls | of 19 | 8 | 7 |
| all thirty | of 121 | 96 | 108 |

Beside the first set, for the same two conditions on the same article:

| | Graph | In-context |
| --- | ---: | ---: |
| set A, elements of 102 | 92 (run-23) | 101 (baseline-01) |
| set B, elements of 102 | 88 (this cell) | 101 (this cell) |

The in-context side reached 101 of 102 on both sets. The graph side reached 92
on the set its type sets were written for and 88 on the second set. The four
that moved are not a clean measure of the set alone: run-23's type sets and this
cell's were written by different authors on different days, and that difference
travels with the question set.

## Questions covered

Over the 25 positive questions:

| | Graph | In-context |
| --- | ---: | ---: |
| COVERED | 15 | 24 |
| PARTIAL | 10 | 1 |
| NONE | 0 | 0 |

Assembly, the descriptor that never moves a label: on the graph, UNLINKED_ROWS
21, ONE_ROW 6, LINKED_ROWS 3, over all thirty questions. On the answer surface
it is NOT_APPLICABLE on all thirty, because a prose answer always assembles.

The in-context side's single miss over the positives is `CQ-B-T2-03`'s
`core_complex_location`: the answer states the dome's position, but the only
claim carrying it is PARTIAL, because the block it cites does not carry the
outside-corner descriptor, and a PARTIAL witness cannot name a semantic.

The graph's fourteen absences over the positives, by the protocol's own codes:

| Code | Count | Where |
| --- | ---: | --- |
| `WITHHELD_STATEMENT` | 6 | the author contributions and the two structural-position questions (`CQ-B-T2-01` ×3, `CQ-B-T2-03` ×2, `CQ-B-T2-04` ×1): the element survives only inside a retained statement the graph binds by locator and digest |
| `NOT_CAPTURED` | 5 | `CQ-B-T1-01` deployment_year, `CQ-B-T2-05` ratio_source_study, `CQ-B-T3-01` rate_source_attribution, `CQ-B-T3-05` solubility_model_source, `CQ-B-T4-01` alternative_count: the contract has a place and no record carries it |
| `NOT_MODELLED` | 2 | `CQ-B-T1-02` received_date and accepted_date: the contract declares no type and no slot for a submission or acceptance date |
| `UNREACHED_RECORD` | 1 | `CQ-B-T2-02` ship_time_funder |

Ten of the fourteen sit in T1 and T2. Four of the five `NOT_CAPTURED` are the
same shape: the question asks *whose* study, model or figure a value came from,
and the producer captured the value without capturing the attribution as a
record. That is a producer modelling choice, not a gate failure.

## Witness support

| | Graph | In-context |
| --- | ---: | ---: |
| witnesses judged | 429 | 102 |
| SUPPORTED | 421 | 100 |
| PARTIAL | 8 | 2 |
| UNSUPPORTED | 0 | 0 |
| NOT_EVALUABLE | 0 | 0 |
| rows or claims | 7,433 | 102 |

The counts are not comparable and the protocol says so: two answers stating one
fact are two claims with no shared identity, while two rows carrying one record
are one witness judged once. What is comparable is that neither surface returned
anything the cited block contradicts.

The graph's eight PARTIAL are of two causes the reviewer names. Six are
block-boundary artefacts of the text layer: the sentence the record rests on
starts or ends in a neighbouring block the witness does not cite
(`obs:depth-uncertainty-bound`, `claim:occ-exhumed-mantle`,
`claim:acknowledgement-discussions`, `claim:fixed-depth-rms-worse`,
`claim:max-depth-not-following-relationship`, `claim:volatiles-reduce-solidus`).
Two record an estimation proxy the cited block does not name
(`gchem:rc2-co2-primary-calc`, `gchem:rc3-co2-primary-calc`). None of the eight
is named by a coverage entry, so none moves a question label. The in-context
side's two PARTIAL are claims that run past the block they cite
(`CQ-B-T2-03:c2`, `CQ-B-T5-05:c4`).

## Controls

| | Graph | In-context |
| --- | ---: | ---: |
| matched | 2 of 5 | 5 of 5 |

Both paraphrase controls matched their named questions on both surfaces. The
three unanswerable controls read NONE on the answer surface, as expected, and
PARTIAL on the graph.

**The graph's three PARTIAL are not a fabrication finding, and the comparison is
not like-for-like.** Each of the three controls names one required element that
the reading does state about the control's own subject, and the graph returns a
row carrying it:

| Control | Named on the graph | The other three elements |
| --- | --- | --- |
| `CQ-B-C-01` sampling rate and sensor type | `instrument_count` | all three `NOT_IN_SOURCE` |
| `CQ-B-C-02` largest local magnitude | `magnitude_scale` | two `NOT_IN_SOURCE`, one `UNREACHED_RECORD` |
| `CQ-B-C-03` per-site depths in the compilation | `site_name` | all three `NOT_IN_SOURCE` |

No row asserts a sampling rate, a sensor type, a maximum magnitude or a per-site
depth. The elements the question was built to be unable to answer are absent on
the graph in every case.

Two things produce the 2 against 5, and both are the instrument rather than the
graph:

1. **The controls of set B carry an in-text semantic.** This is the defect Luis
   fixed in set A at E-0346, by dropping `compilation_source` from `CQ-C-03`
   after both v3 cells covered it and read PARTIAL against an expected NONE. The
   authoring session for set B was asked for questions the reading cannot answer
   and wrote three whose overall answer it cannot give but one of whose required
   elements it states. The set is frozen as written; the defect is recorded, not
   repaired.
2. **The two surfaces have different machinery for saying "not here".** The
   answer grammar carries a per-question `no_answer_in_source` declaration. The
   producer set it on all three controls, which zeroes the claims, so every
   coverage entry must take an absence code and the derived label is NONE by
   construction. A graph has no per-question declaration: it returns the rows its
   type set reaches, and under the subject-tie rule a row carrying the element
   for the question's own subject names it. On these three controls the answer
   surface is not being more truthful than the graph; it is being asked a
   question the graph's representation cannot be asked.

## What each side paid

Token figures are the harness's own report per session, not split into input,
output or cache.

### For this second question set

| | Graph | In-context |
| --- | ---: | ---: |
| question set author (shared, counted once) | 106,882 | 106,882 |
| producer | 0 | 124,886 |
| type sets | 5 tool calls, by hand | , |
| binding and query | 11,912 cases, ~100 s wall clock | , |
| review | 459,121 | 202,886 |
| **total tokens, excluding the shared author** | **459,121** | **327,772** |
| **production only, excluding review** | **0 tokens + 5 tool calls + 100 s** | **124,886** |

The five tool calls are a real cost that no token figure carries: one printed
the surface's record types, families, subject slots and subtype closure, two
read the ledger entries E-0342 and E-0343 for the rule, one wrote the thirty
sets, one ran the closure check. They were written by hand, by the parent
session, and a person doing this work would spend the same kind of effort.

### To exist

| | Graph | In-context |
| --- | ---: | ---: |
| producer | 382,781 (run-23) | 127,303 (baseline-01) |
| review | 487,927 (run-23) | 229,067 (baseline-01) |
| what persists | an accepted ledger, replayable, re-queryable | a prose answer file; not provided to the next fresh baseline |

The in-context row is not a build cost. It is the same cost again, on a
different set. That is the whole point of the comparison, and it is why this
cell exists.

## What the cost measurement establishes

No break-even point was measured. No capture producer ran for the second set,
but its manual bindings and query execution were not free. The recorded
marginal work was five binding tool calls, approximately 100 seconds of query
execution and 459,121 review tokens. The baseline used 124,886 producer tokens
and 202,886 review tokens. Including review gives 459,121 versus 327,772,
or 1.40 times as many reported tokens, with 88 versus 101 answer elements reached.

The original fourth-question-set crossover was an extrapolation from producer
tokens alone. It omitted unpriced binding work, review and differences in answer
coverage. Conversely, one more expensive reviewed use does not establish that
reuse can never repay its initial cost. Costs depend on the workflow measured.
Both accounts are retained; no assumption that production requires no verification
is made. Token totals do not separate input, output, caching or reasoning and
cannot establish financial cost or a reasoning-budget measurement.

The bounded finding is useful: an unchanged accepted graph answered new
questions without another capture. Whether repeated use becomes cheaper,
improves semantic connections or benefits another model remains unmeasured.

## Confounds, all of them we can see

1. **The type sets were written by a session that had seen the graph's surface.**
   The in-context producer had seen no part of the graph at all. The type sets
   are the graph side's question-to-graph adapter and they are a judgement made
   with knowledge of what types the graph declares. They were written from the
   accepted population surface and the questions only, before any row existed,
   and the closure check ran to ACCEPTED; but the asymmetry is real and it favours
   the graph.
2. **The type-set author changed with the question set.** run-23's thirty sets
   and this cell's thirty sets were written by different sessions. The graph's
   drop from 92 to 88 of 102 mixes the question set's difficulty with that
   difference, and this cell cannot separate them.
3. **The baseline producer saw the questions; no graph producer ever did.** This
   is the tilt Section 4.8 declares on purpose, unchanged here. It is what makes
   the result a price and not a contest.
4. **The graph was blind to both sets, but not to the article.** run-23's
   producer was denied set A and never saw set B, so it is question-blind to this
   set in exactly the way it was to the first. Both sets are questions about the
   same eleven-page article, so they overlap in subject matter; "a second
   question set" is not "a second domain".
5. **The review cost is partly an artefact of my binding.** This cell's type sets
   expand to 11,912 cases and return 7,433 rows over 429 witnesses, against
   run-23's 10,063 cases and 6,573 rows over 428. Tighter type sets would return
   fewer rows and cost less to review while possibly reaching fewer elements.
   The 459,121 is one point on that trade, not the graph's intrinsic review cost.
6. **The controls are not comparable across the two surfaces**, for the reason
   given above: one surface can declare a whole question unanswerable and zero
   its claims, and the other cannot.
7. **Three of set B's controls carry an in-text required element**, the defect
   E-0346 fixed in set A. The set is frozen as authored.
8. **Both reviews are model-assisted, by the producers' own model family**, which
   is the setting in which model judges are known to favour their own outputs.
   Neither record is ratified.
9. **A cited block does not prove the answer was read from it.** The in-context
   producer saw the whole article; nothing in this cell excludes a claim composed
   from memory and cited afterwards. Zero UNSUPPORTED on that surface does not
   mean grounded.
10. **The one-hundred-second query figure is wall clock on one laptop** against
    a pinned Core export, not a throughput measurement.

## Where everything is

Public, under `paper-v4/experiment-v4/reuse-01/`: the frozen type sets and their
rationale, the query binding, the query trace summary, the graph reference with
the ledger digest before and after, the launch log, the withheld-artifact record
and this file. Public under `paper-v4/experiment-v4/reuse-01-baseline/`: the run
contract, the producer task, the answer grammar, the validator and the review
package builder. The review packages, records and ticked checklists are public
under `paper-v4/evaluation-v4/reuse-01/` and
`paper-v4/evaluation-v4/reuse-01-baseline/`.

One file is withheld, `query-result.json`, because its projected row fields
reproduce the reading; its digest is public and
`results/withheld-artifacts.json` records the measurement. Every public file
this cell writes under `paper-v4/experiment-v4/reuse-01/`, and every file of the
graph half's review package, was measured against every block of the selected
reading and shares no forty-character normalized run with any of them. The
producer's answer file stays under `private/`, as baseline-01's does.

The two private reuse inputs are now declared in active-test-manifest.json and
test_gate_integration.py. Their absence must fail the active gate, not silently
skip these results. This corrects the earlier report that they were undeclared.

One measurement to record rather than repair. The in-context half's
`review-record.preliminary.md` and `review-witnesses.json` reach ladder rung 40
and share eight distinct fifty-character runs with the reading; neither shares a
sixty-character run, so both clear the threshold every frozen cell clears and
checklist entry C-12 passes as the protocol writes it. The graph half's record,
witnesses, checklist and thirty blocks measure 0 at every rung. The difference is
in how closely the two reviewers paraphrased the blocks they cited. A reviewer's
output is never edited, so it stands as written; a future protocol revision may
want to state the reviewer-side window explicitly instead of leaving it to each
cell's publication rule.

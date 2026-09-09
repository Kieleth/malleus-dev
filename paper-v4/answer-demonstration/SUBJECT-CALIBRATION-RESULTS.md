# Subject-aware reads on the unchanged ultra capture

E-0253, completed at E-0254, master 1.5.15. Retrieval alone makes one additional
distinct question fully covered, plus its paraphrase, and exposes the quantities
needed for a partial segment comparison. No capture or knowledge amendment is
part of this result. Historical outputs and reviews remain unchanged. All
semantic judgments are model-assisted, with human ratification pending.

## Intervention

Use the existing SubjectGraphReads on calibration b. It matches each record's
own text plus its explicit subject's name, description and tags, one hop only.
The original thirty question programs, numeric-field requirements, returned
fields and relation traversal remain unchanged. No new aliases, expected values,
source parsing, model generation or inferred joins are introduced.

This method was selected after the diagnostic described in CALIBRATION-RESULTS.md,
not preregistered before seeing the capture. Exact existing code was recorded
in E-0253 and frozen by the runner before this complete comparison. This is a
retrospective query-only intervention, not a new prospective capture condition.

Core remains 160878cf14c0d27b11a440e26688708e9b7a7e2b. All 159 graph records
remain identical: 138 entities, twenty relations and one domain event. Ledger
head and receipt remain those of calibration b. No Core capability request or
implementation change is required for this reader.

## Executed contrast

The original thirty query bodies reproduce exactly from the reopened history.
The subject-aware pass changes four outputs; the other twenty-six are identical.
Every old row is retained without alteration, and every relation path is unchanged.

| Question | Original rows | Subject-aware rows | Added material |
|---|---:|---:|---|
| CQ-T3-02, primary-melt concentration | 1 | 5 | Four site- and proxy-specific primary-melt estimates |
| CQ-T3-03, pre-eruptive concentration | 1 | 5 | Four site- and proxy-specific pre-eruptive estimates |
| CQ-T5-02, segment comparison | 1 | 5 | The four primary-melt estimates |
| CQ-C-05, primary-melt paraphrase | 1 | 5 | The same four primary-melt estimates |

Total row occurrences increase from forty to fifty-six. Nineteen questions
return candidates in both views. Distinct central witnesses increase from 28
to 36. The added sixteen row occurrences refer to eight existing observations,
not newly derived quantities. Their fields and subjects match the accepted
export exactly. Every old witness retains the same union of projected fields.

All four primary observations identify their stage through a MeltPhase subject,
their site through its segment tag and their proxy through quantity_kind. The
pre-eruptive observations use separate MeltPhase subjects and retain Rb/Ba
labels. These are stored distinctions; the reader has not supplied them from
the source. Site tags are not new spatial edges, and proxy labels are not a
complete typed derivation procedure.

More rows are not automatically better answers. The previously returned
pre-eruptive summary now appears beside distinct estimates and another site's
values. Independent assessment must retain those qualifications and any
unresolved selection rather than choose by the expected number. The reader
cannot construct the still-absent SUPPORTS paths.

## Preservation and reproduction

The public replay matches the exact accepted graph and receipt. Source-file,
network and embedding guard counters are all zero; ledger bytes are unchanged.
An independent repeat matches all eight output files except the declared
execution timestamp in method.json. Query result, traces, summary and frozen
program bytes are identical.

Evidence under private/paper-v4-answer-demonstration/sol-calibration-01/b/:
subject-query-01, subject-query-reproduction-01 and subject-review-01.
The subject query result digest is
8b1fc2fe6bab4f80f31abffd667e8934f2c38b0ed461617a8d163979f3be6c5d;
review manifest e70c6f442be64030ace18f5472ec8c1b703a0ca352b9bcf0b8ea85938cbb02a4.

The independent reviewer received the new packet under the unchanged review
rules, no earlier grades or RCA. First completed submission passed validation:
thirty questions, 121 required semantics, 56 row occurrences and 36 central
witnesses. All 36 returned witnesses were judged SUPPORTED. This does not
certify every graph record or establish scientific truth.

## Source-grounded outcome

| Question | Original review | New review | Evidence for the difference |
|---|---|---|---|
| Primary-melt concentration | NONE | COVERED | Newly returned RC2 quantities retain stage, unit, proxy and ESTIMATED determination |
| Its paraphrase | NONE | COVERED | Same evidence, not a second independent question |
| Segment comparison | NONE | PARTIAL | Both sites' quantities are now returned; comparison and spatial links remain absent |
| Pre-eruptive concentration | COVERED | COVERED | Original summary survives; the other estimates remain separately labelled |

The primary-melt answer must preserve its two proxy estimates. For RC2, Ba90
gives 0.4–3.0 wt% and Rb90 gives 0.5–2.8 wt%. The reviewer credits the explicit
Ba90-specific answer while identifying the Rb90 alternative, rather than merging
them or silently selecting an expected aggregate. RC3 records remain separately
identified. The calculation formula is not represented by the reader.

The new complete review has 5 COVERED, 13 PARTIAL and 12 NONE. On the 25 distinct
positive questions it has 4 COVERED, 13 PARTIAL and 8 NONE. The other cases are
three negative controls, a count paraphrase with NONE and the now-covered
primary-melt paraphrase. No composition question is fully covered. Neither the
preferred hypothesis nor its supporting evidence links changed.

## Attribution, including a review disagreement

The raw covered-semantic total increases from 34 to 48 out of 121. Twelve new
credits name newly retrieved rows: four for the primary-melt question, four
for its paraphrase and four for the segment comparison. Those are eight credits
on distinct positive questions, plus the four repeated by the paraphrase.
This is the improvement supported by new answer evidence on fixed knowledge.

The remaining two credits are different. CQ-T3-04, horizontal uncertainty, has
byte-identical query rows but changes from NONE to PARTIAL. Both reviewers agree
that catalogue, processing-stage and event-set context are missing. The earlier
reviewer therefore credits no site/stage-specific value; the new reviewer
credits the updated statistic and its unit while leaving that context absent.
This is a disagreement about partial coverage, not retrieval improvement. The
original and new judgments are retained unchanged; no hybrid corrected total
is presented. The two corresponding credits need adjudication before a paper
claims an overall coverage delta. All other unchanged queries keep their prior
responsiveness label, and all common witnesses keep SUPPORTED.

The new review is CODEX_PRELIMINARY, completed 2026-09-07T20:45:55Z, digest
acad42df3fc6651d3fc222915e9add8197910e9e027781887fb0a25459f83725.
subject-review-comparison.json, outside both frozen execution directories,
records the exact before/after identities and per-question coverage changes.
It compares validated judgments and rows; it does not evaluate or adjudicate.

## What to improve next

This result fixes a demonstrated read failure without rebuilding the graph.
It does not solve source omissions, incorrect negative dispositions, missing
population qualifications or absent supporting relations. The existing graph
is a useful baseline to preserve. A next capture amendment should target one
of those demonstrated gaps, not repeat full-document generation or rewrite
already supported quantities. The links-only hypothesis-evidence slice is
available through the earlier preservation-checked composition mechanism;
adapting its exact baseline and target IDs needs an explicit bounded plan.

The partial-credit disagreement should also receive blinded adjudication before
aggregate paper comparisons. Neither that adjudication nor a capture amendment
was launched by this query-only approval. No missing Core capability was found.

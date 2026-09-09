# Thirty-question failure-stage audit

E-0277/E-0278 forward result: the approved query-only fix now retrieves the
qualified microseismicity observation and excludes the count/temperature from
CQ-T3-01. The source, graph, ledger and all other 29 query objects stay unchanged.
Two reads reproduce exactly. The earlier selection diagnosis below remains valid
for its frozen reader, not the new depth-method-01. No new coverage grade is
assigned. See DEPTH-QUERY-RESULTS.md.

E-0272/E-0273 forward status: the author approved a prospective qualification
repair on the richer sol-argument-scope-01 baseline, not the older F proposal
below. Missing status was retained in capture but never formalized onto the
observation. The reader returned all stored fields, so no Core read/replay defect
was found. The new cut preserves numbers/subjects and versions only the observation
plus its incident relation. Faithfulness and coverage are now explicitly separate;
before/after use the same newly frozen rule. This is a targeted repair experiment,
not evidence of reliable question-blind acquisition or an automatic evaluation
capability. E-0275: the first candidate admits and reproduces exactly. The graph
now returns added status and observation-window qualifications through the same
SUPPORTS path; all existing values and unrelated records survive. Only CQ-T5-01
changes. E-0276 independent model-assisted review supports both replacements and
finds four of five requirements before, all five after, under the same prospective
rule. Human ratification remains pending, with no historical regrade or global
score. See QUALIFICATION-RESULTS.md.

Read-only post-amendment check: CQ-T3-01 still omits the qualified RC2 record.
Its quantity_kind/description use microseismicity, not the selector's whole-word
seismicity or earthquake terms. The returned candidates also include
count:forced-depth-subset and observation:bdb-temperature, because quantified
accepts any declared numeric field without requiring a length quantity. These
are observed selection limits on the richer current graph, not another extraction
regression. No selector was changed or new Core defect inferred. A query-only
correction remains a separate possible next cut.

E-0250, read-only evidence audit. Historical outputs and labels are unchanged.
Model-assisted judgments remain pending human ratification. This report is not
an input to either calibration producer.

## What the aggregate concealed

The thirty-query results combine missing capture, lost scientific scope,
query-selection failures and a stringent completeness rule. They do not measure
all knowledge present in the graph. Thirty also includes three expected-absence
controls and two paraphrases of positive questions. Report the twenty-five
distinct positive questions separately from controls.

The earlier Sol follow-up already contains separate RC2 and RC3 calculated CO2
quantities, with bounds, units, determinations and distinct subjects. It also
contains an RC2 depth observation. The frozen queries miss all three. The prior
description of missing paired quantities overgeneralized from the returned rows
to the graph. The finding is narrower: paired values exist, but the stage and
comparative role are not fully represented, and restrictive matching hides them.

The first corrected E2E graph stores quantities in a new qualifying slot. Our
previous query correction recovered those fields. That is already a useful
query-only positive control. It did not restore absent site or method scope.

## Exact evidence

All private paths are under `private/paper-v4-answer-demonstration/`.

F is `followup-sol-01/attempt-01/`, original query and review. Its graph and
submitted population are retained as `export-records.json` and
`submitted-population.json`. B is the unchanged corrected E2E graph at
`sol-e2e-corrected-01/attempt-01/public/`, evaluated under the corrected text
binding in `sol-census-01/before-review/`. C is the revised census graph at
`sol-census-01/attempt-03/public/`, reviewed in `sol-census-01/after-review/`.
F's subject-aware query and review are a separate instrument, not the F labels
in the table. Every source locator below is a selected-reading block, written
compactly as p5b005 for `page:5:block:005`.

The frozen F query uses exact-word matching in `contains`, then numeric-field
selection in `quantified`. Its `earthquake_depth` and `primary_carbon` functions select
by wording, not a general semantic query planner. `obs:rc2-depth` says
"deep microseismicity depth", which misses "seismicity". `obs:ntd2-depth`
says "normal-depth earthquakes", which matches and returns a different site.
The two segment observations `obs:rc2-melt-co2` and `obs:rc3-melt-co2` say
"CO2(calculated)", not "primary melt", even after subject-aware matching.
Their retained assertion `assertion:segment-co2-comparison` points to p5b005;
preceding context supplies the melt-stage meaning, not their stored fields.
Widening selection alone therefore cannot certify a complete comparison.

## All thirty questions

C/P/N mean recorded COVERED/PARTIAL/NONE. They describe returned fields, not a
new assessment of the entire graph. T and C IDs have the common `CQ-` prefix.

| ID | F/B/C | Located loss and source witness |
|---|---|---|
| T1-01 | P/N/N | F campaign name exists, acquisition proposition missing; B/C omit campaign. p2b002. |
| T1-02 | N/N/N | F Campaign count exists but deployment-word filter misses it; count scope also incomplete. p2b002, p6b002. |
| T1-03 | N/N/N | Date not captured in F. B/C lack the query's accepted_date slot, silently treated as empty. p1b006. |
| T1-04 | P/N/N | F dataset DOI exists, repository name and deposit relation absent. B/C omit dataset. p8b008–009. |
| T1-05 | N/N/N | Acquisition paragraph retained by F, duration not projected. B/C omit acquisition. p2b002. |
| T2-01 | N/N/N | F RC1/OCC objects exist, fault endpoint and BOUNDED_BY do not. All surfaces allow the relation. p1b005. |
| T2-02 | N/N/N | F methods exist, query-recognized sequence predicates absent from surfaces; NOT_EXPRESSIBLE. p7b004/006. |
| T2-03 | N/N/N | Source retained as hypothesis evidence, not vent/spatial records. p3b002. |
| T2-04 | P/N/N | F thickness, uncertainty and flank exist; age and cited-study relation absent. p2b006. |
| T2-05 | N/N/N | F funding capture absent. B/C lack the fixed query's award_identifier field. p10b044. |
| T3-01 | N/P/N | F RC2 microseismicity quantity missed, NTD2 quantity selected. B quantity lacks full site/datum/origin scope. C drops typed value. p2b004/006. |
| T3-02 | N/P/N | F local text misses primary-melt subject; subject-aware query recovers generic value, not segment pair. B lacks segment. C prose only. p5b004/005, p8b007. |
| T3-03 | N/N/N | Pre-eruptive stage quantity absent, cannot relabel primary-melt value. p5b006, p8b006. |
| T3-04 | N/N/N | Horizontal uncertainty absent. Older rich runs also omit event-set qualification. p7b007. |
| T3-05 | N/N/N | Saturation pressure/temperature pair absent. Older rich runs show disconnected condition subjects. p5b006. |
| T4-01 | P/P/C | F/B preference shell lacks proposition. C supplies mechanism, subject and qualification in one row. p5b002. |
| T4-02 | N/N/N | Hydrothermal explanation returned instead of requested melt-movement argument. Older runs contain claims missed by their query. p4b002/003, p5b001. |
| T4-03 | N/N/N | Trace-element assumption absent here; older run21 stores it but its query misses it. p5b004. |
| T4-04 | N/N/N | No-observations proposition absent here despite retained paragraph. Older run20 overstates absence. p3b002. |
| T4-05 | N/N/N | C limitation exists without query's long-period wording; positive hedged interpretation also absent. p5b008. |
| T5-01 | N/N/P | F/B quantities and hypothesis shell disconnected; C proposition and prose observations still disconnected. Existing composition-01 proves a supported two-link repair. |
| T5-02 | N/P/N | F has both calculated segment quantities but query misses them; stage/adjacency/comparative role incomplete. B only one unscoped value. p5b005, p8b007. |
| T5-03 | N/N/N | Observed depths partially present, expected threshold/classification absent; C numeric evidence becomes prose. p2b004–006. |
| T5-04 | N/N/N | Category set and A/B selection absent; total count or prose quality percentage is insufficient. p2b003, p7b008. |
| T5-05 | N/N/N | C conclusion lacks morphology, off-axis observations and evidential link. F omits argument. p3b001. |
| C-01 | N/N/N | Expected source-absence control, not a positive-question failure. |
| C-02 | N/N/N | Expected source-absence control; snapshot caveat is not recurrence evidence. |
| C-03 | N/N/N | Expected excluded-surface control; do not import figure/table values. |
| C-04 | N/N/N | Paraphrase and same query as T1-02, not independent evidence. |
| C-05 | N/P/N | Paraphrase and same query as T3-02, not independent evidence. |

## Evaluation and faithfulness checks still needed

Most completeness requirements are justified. A quantity without site, stage,
datum or method can answer the wrong question. Lowering the standard would
hide that error. But PARTIAL totals have a demonstrated inconsistency:
F's subject-review gives T5-02 NONE when an unscoped wt% row is returned;
B credits wt% and gives PARTIAL despite missing segment pairing. Different
DERIVED metadata does not repair that missing role. Blinded adjudication is
needed before interpreting the partial-count difference as improvement.

The whole-witness support rule can exclude correct fields when another field
in that row is wrong. That conservative rule should be disclosed; it is not
evidence that the graph contains no correct subfields.

A newly identified source-scope concern exists in C.
`claim:location-quality` attaches the approximately 78% location-quality statement
in p7b008 to `earthquakes:deep-mantle`, selected as mantle-depth earthquakes.
The passage discusses the location catalogue, not explicitly that subset.
Generic earthquakes/events aliases can pass a name check without establishing
population identity. This was not a prior UNSUPPORTED verdict because the record
was not returned for review. A separate independent model assessment now finds
the subject narrowing unsupported, while supporting the statement itself.
It also confirms the paired CO2 values and their incomplete stage representation.
See [scope probe](SCOPE-PROBE.md). Human ratification remains pending; historical
labels are unchanged.

## Incremental probes, after calibration

Calibration b now supplies a richer, separately retained case. This is not B in
the historical table above. It admits 138 entities, twenty relations and one
event on the first submission. Its four site- and proxy-specific primary-melt
estimates carry the stage in their MeltPhase subjects, so the earlier F finding
of missing stage must not be carried over to this run. The frozen query still
misses all four. Reopening the exact Core history and using the existing one-hop
subject reader returns them without source reads or state changes. This moves
retrieval correction ahead of capture repair for those values. It does not
automatically establish all required comparison semantics or a reviewed answer.

Two source blocks incorrectly declared nothing_assertable expose a separate
capture defect, despite zero untouched blocks. Related numbers stored elsewhere
do not preserve every omitted proposition. See CALIBRATION-RESULTS.md and
SCOPE-PROBE.md. The fresh full review uses only the frozen original query.

E-0253/E-0254 follow-up is now complete: the unchanged richer graph was queried
with that existing subject-aware reader, then independently reviewed in full.
It recovers a complete primary-melt answer and its paraphrase, and a partial
site comparison, without adding knowledge. Two additional semantic credits on
unchanged horizontal-uncertainty rows expose another partial-credit disagreement.
They are explicitly separated from retrieval gain. See
[subject comparison](SUBJECT-CALIBRATION-RESULTS.md). No capture amendment or
evaluation-label correction was applied by that query-only condition.

E-0255 through E-0258 now add the separate preservation-checked relation slice.
Sol proposes one modelled-saturation-depth SUPPORTS link, which independently
passes source support assessment. All old records survive and only CQ-T5-01
changes, but that answer remains PARTIAL: volatile-content evidence stays
unreached and the new depth is a model prediction, not a seismic observation.
The source additionally states no observed earthquakes below 20 km, so the
approximately 25 km saturation result must not become a claimed numerical match.
See [links result](LINKS-RESULTS.md).

The new reviewer credits two observational semantics from unchanged qualitative
claim text that the earlier complete review did not credit. Only the explicit
evidence relation is newly covered in its own before/after assessment. This is
another partial-credit interpretation difference, not proof of added observational
content. Historical labels stay intact. The experiment improves one explicit
connection; it does not explain original link omission or establish complete
argument capture. No Core loss or missing relation/read mechanism was found.

E-0259 through E-0262 supply a task-directed completion pass under newly declared
prospective criteria. Two supported links now reach broad abstract melt-content
and earthquake-depth observations. All old records survive and only CQ-T5-01
changes. Independent review still finds PARTIAL: values are returned, but their
subjects do not identify the RC2 scope distinguished by the full article.
The unchanged label must not hide the gained values and explicit evidence paths.
The new before/after interpretation is not a replacement for older reviews.

The local diagnosis separates endpoint choice from projection. RC2-specific
observations exist but were not selected for the new links. Their site-bearing
subjects are stored, while the frozen relation projection returns only the
subject ID, not its properties. The entity-row projection already expands that
reference. A test now preserves both facts and prevents treating the hypothesis's
location as the evidence's location. Expanding a broad subject alone cannot
invent missing scope. No Core loss is established. See
[argument result](ARGUMENT-RESULTS.md) for the exact evidence and proposed
query-only control followed by a separate scoped amendment. Neither is executed.

E-0263 through E-0265 complete that projection-only control in TDD. The active
relation reader now displays and traces each endpoint's own subject properties.
Only CQ-T5-01 changes on the same accepted graph; all rows, selections and paths
are preserved. Displaying the broad subjects still does not supply RC2. No new
semantic grade is assigned, and the scoped link amendment is not executed.
See [scope-projection result](RELATION-SCOPE-RESULTS.md).

E-0266 through E-0270 complete the separate scoped-links amendment. The first
fresh Sol/ultra candidate adds two supported paths to existing RC2 observations.
All old records remain, all thirteen execution files reproduce, and only
CQ-T5-01 changes. The corrected reader is fixed before and after. The geochemical
row now returns the RC2 primary-melt scope and ESTIMATED status. The seismic
row now returns the RC2 range, but no determination. The original assertion
retains MEASURED without formalizing that property on the observation; the new
capture maps it only to a relation endpoint. No Core or query property loss is
established. Link addition cannot repair a property that was never projected
into the graph. See [scoped-links result](SCOPED-LINKS-RESULTS.md).

The independent reviewer keeps PARTIAL, while confirming both new argumentative
connections. Its whole-row support threshold is stricter than the previous
assessment of the same observation properties: missing qualifications now remove
support credits as well as coverage credits. The projection also differs between
the review packets. Their criterion counts are therefore not a clean longitudinal
measure. Preserve the observable graph improvement and the qualification omission
separately from this evaluation-interpretation difference. Any clarification or
adjudication is prospective work, not an excuse to overwrite historical labels.

1. Audit query capacity against declared fields/types/predicates before reading.
   Distinguish inexpressible date/funding queries from expressible empty results.
2. Inspect all existing typed quantities with their stored subjects and
   determinations on unchanged F. This isolates recall loss from missing scope.
   Do not relabel this diagnostic inventory as answers to the frozen questions.
3. Use the existing preservation-checked amendment path for source-supported
   stage/site/method/datum completion. Measure exact additions and preserved
   records. Do not replace the whole graph or supply expected answer values.
4. Test one source-grounded relation slice, such as bounding or evidence support.
   The successful two-SUPPORTS repair proves the mechanism exists, not that the
   broader capture procedure reliably uses it.
5. Calibrate the disputed partial-credit rule with blinded paired rows and
   correctly scoped/wrong-site controls. Keep historical labels unchanged.

These are separate interventions, not a bundle for the current producer pair.
No missing Core read, replay or relation capability was established. All five
currently belong to the paper's adoption/query/evaluation procedure. A generic
Core request requires an actual failing Core reproducer, not a low paper score.

## Concrete next slice, proposed, not dispatched

This design was prepared during calibration from the preserved F history, not
C's replacement. The completed richer calibration b requires an explicit next
baseline decision before dispatch. In particular, its stage/site-bearing
observations should be retrieved before proposing redundant amendments.

F's ledger file digest
is 404f0661c139e4a2e768080130f01a0cb07bada1624413ad1725d557cae17416;
graph e04c9ed5e9d53d417e1ef1848627f2e90251a95e96b00faa61135df234e3679b;
receipt 289952d8f8ce55e1db08c3d10050ea74fb96af649615d594dd2342edecc1c48b.

| Contrast | Keep fixed | Permit changing | Evidence sought |
|---|---|---|---|
| Read inventory | Entire graph and ledger | Diagnostic retrieval only | Existing RC2 depth and two segment quantities become visible; unresolved scope stays explicit. |
| Qualification amendment | Ontology, reader, existing numbers, units and subjects | Same-type, explicitly superseding replacements of three observations and the preferred-claim shell | Source-supported qualification and proposition, without losing earlier values. |
| Links amendment | All accepted entity fields and reader | Justified ResearchRelation additions between existing entities | New inspectable evidence paths, separately from richer endpoint content. |

The middle contrast is finding-guided and question-withheld, not independent
acquisition: RCA selects `obs:rc2-depth`, `obs:rc2-melt-co2`,
`obs:rc3-melt-co2` and `claim:co2-degassing`. Supply the accepted graph and
source, no questions, grades, expected values or desired links. Existing values
are context to preserve, not newly authored answers. If source faithfulness
requires changing a protected field, the bounded condition must refuse or
declare a gap. Do not conceal that need with a broader rewrite.

Reuse repair.py's public admission/replay, ledger-prefix, graph preservation
and history-closure checks. Its current scope is relations only and staging is
hardcoded to run21. A qualification case and explicit baseline/target parameters
are needed before it can execute this proposal. Do not weaken existing cases
or create another execution stack.

Run20's research subject declaration forbids folding subjects into quantity_kind
or names; metrology quantity_kind preserves source wording. The accepted schema
has description, Claim.statement, subject references and MeltPhase, but no
dedicated depth-datum or method-of-determination role. DERIVED_FROM means material
origin, not a generic method link. A no-revision pilot can add qualified prose,
not claim uniform typed role capture. If separately typed stage/site/method/datum
roles prove necessary, propose an additive adopter ontology revision based on
those observed limits. That is not itself a missing Core mechanism.

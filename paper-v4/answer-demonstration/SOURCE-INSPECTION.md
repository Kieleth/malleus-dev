# Six-case source inspection

2026-09-06. Retrospective diagnosis by the query author, not an independent
review, a human-ratified evaluation, or a replacement for either historical
review. The six cases were selected in the approved answer-demonstration plan.
Inspection uses the frozen selected text, retained captures and replayed graphs
of run-20 and run-21. No new producer output is needed for this work.

## Findings

| Case | What the existing graph returns | What the source check establishes |
| --- | --- | --- |
| Instrument count, CQ-T1-02 | Both return 19 with deployment scope. Run-20 also links one count to SMARTIES; run-21's returned count has no subject link. | The count is supported by the Results and Methods. The 17 useful instruments are a different count. A missing campaign link remains missing; retrieving the number does not repair it. |
| Spatial relation, CQ-T2-01 | Both return an actual RC1 BOUNDED_BY detachment edge. Pilot 03 additionally returns run-21's existing, subject-linked claim. | The source puts the bounding fault and core complex east of the axis. Run-21 stores this wording; run-20's inspected projection omits the directional qualifiers. The new query retrieves prose, not a typed east-of relation. |
| Primary-melt concentration, CQ-T3-02 | Both return six candidates with bounds, units and calculation status. They include separate RC2 and RC3 estimates, an abstract summary and a lower bound. | The values and calculated status have source support. The query does not resolve the question's descriptive site reference, so the six rows are not one unambiguous answer. |
| Preferred mechanism, CQ-T4-01 | Both return CO2 degassing, PREFERRED, HYPOTHESISED and an RC2 subject. | The source explicitly presents this as the preferred explanation, not an established cause. Run-20 carries the mechanism in a name; run-21 carries its statement. Neither is a graph-derived causal conclusion. |
| Evidence composition, CQ-T5-01 | Both return the preferred claim but no SUPPORTS path. | The source explicitly relates the degassing calculation to observed deep seismicity. Both captures retain that passage but map it to numerical observations and a model artifact, not an evidential relation. |
| Sulfur/chlorine control, CQ-C-01 | Neither returns a candidate. | Searches of all 186 selected-text blocks found no sulfur, sulphur, chlorine, chloride or standalone Cl occurrence. Inspection of the volatile-estimation passages found CO2 calculations, not the requested concentrations. This is a bounded text-layer check, not a claim about unseen supplements or raster content. |

These findings are not six numerical grades. In particular, correct field
readback, sufficient question coverage and independent source support are
different judgments. The complete thirty-question evaluation remains pending.

## Source trail

Block locators refer to private/paper-v4-text-layer/selected-reading.json,
sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17.
Exact source excerpts remain private.

- Count: page:2:block:002 and page:6:block:002. Run-20 assertions 0041 and
  0164; run-21 assertion 175 for the returned Methods count.
- Bounding: page:1:block:005. Run-20 assertion 0026; run-21 assertion 025.
  Run-21's extra witness is claim:rti-amagmatic, subject feat:rc1.
- Concentration: page:1:block:001 and page:8:block:007. Run-20 assertions
  0006, 0245, 0246; run-21 assertions 006, 259, 260. The Methods distinguish
  estimates using Ba90 and Rb90, and primary from pre-eruptive melts. Do not
  collapse those distinctions into one interchangeable range.
- Preferred mechanism: page:5:block:002. Run-20 assertions 0122 and 0123;
  run-21 assertions 133 and 134. Disposition and mechanism have separate
  field derivations.
- Evidence connection: page:5:block:006. Run-20 assertion 0142; run-21
  assertion 152. Both preserve the same passage. The surrounding interpretation
  also appears in page:1:block:001 and page:5:block:003.
- Control context: page:5:block:004, page:5:block:006 and
  page:8:block:005 through page:8:block:007.

The read-only check resolved all pilot-02 six-case witnesses through retained
capture assertions into exact selected blocks: 16 witnesses and 108 field
derivations for run-20; 14 and 100 for run-21. It checked capture/source digests,
formalized_by record/path membership, exact statement containment, and the
statement hashes carried by returned observation/claim rows. These checks
establish trace consistency, not semantic correctness of each field.

## Why the missing SUPPORTS path is not a Core read failure

Both accepted surfaces declare SUPPORTS on ResearchRelation, with Entity
endpoints. Both proposed populations contain zero such relations, and both
replay exports contain zero. Thus there is no proposed edge for admission,
replay or the public query API to have lost.

At the relevant source passage, both captures map the assertion to saturation
depth, pressure, temperature, a melt threshold and a model artifact. Neither
maps an evidence-to-claim relation. Both assertions have empty gaps lists.
That does not prove the passage was fully represented: successful admission
and field traceability did not require every semantic relationship in the
passage to be projected.

The immediate failure is capture/population completeness. A supporting
relationship would represent the authors' argument, not certify that their
hypothesis is true. Its evidence source and the hypothesis's modality must
remain inspectable. The present data do not establish whether different
generic acquisition instructions would reliably produce it.

No Core capability request follows. A concrete request would require, for
example, a source-grounded relation expressible under the accepted contract
that Core refuses incorrectly or fails to return after acceptance. Neither
case occurred here. A new producer intervention remains an M5 author decision;
no evaluator-authored edge or population repair was made.

## Query-only follow-up completed

Pilot 03 follows the actual BOUNDED_BY edge, then selects stored descriptions
whose subject equals its subsection and whose wording mentions both the fault
and core complex. It adds no answer value, site alias, edge or source excerpt
to the query code. A synthetic regression uses different spatial wording and
rejects unjoined descriptions, wrong subjects and irrelevant claims.

On the old ledgers, run-20 still returns one bounding row. Run-21 now returns
the edge plus the existing claim. The source inspection informed this query
revision, so the result is explicitly exploratory. Pilot 02 remains unchanged.
No published accuracy comparison can treat this as a prospective improvement.

## Paper implication

We now have concrete examples of a supported count, an explicit graph relation,
a retrieved hypothesis with its modality, ambiguity among well-formed numeric
records, and an omitted evidence connection. This is enough to write the worked
example and its limitations while completing evaluation. It is not yet evidence
of reliable multi-hop scientific reasoning or complete document capture.

Next, inspect every returned witness and required semantic across all thirty
questions, including empty and ambiguous outputs. Independent review and
author ratification are still needed before presenting new answer-quality
results. Fable's new runs can test recurrence later; they are not a dependency
for evaluating and writing up these frozen runs.

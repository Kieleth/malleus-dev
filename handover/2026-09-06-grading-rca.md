# RCA: the grading, and why "the graphs answer the questions" is not yet a measurement, 2026-09-06

Overseer session, at Luis's request: an RCA on the grade itself, to find what is missing from the protocol or from the grading, and whether a larger question set with controls would settle it. Evidence: task v4's label definitions (`paper-v4/evaluation-v4/run-21/review-task.md`), protocol v2's judgement sets, `competency-questions.json` (four questions, each with `required_semantics`), the 28 responsiveness rationales of the seven reviewed cells (runs 13, 14, 15, 16, 19, 20, 21), and E-0191. Every rationale was read in full; the reading is quoted nowhere.

## The grade as written

Per row, `source_support`: SUPPORTED, PARTIAL ("supports some but not all, or a needed qualifier is absent"), UNSUPPORTED, NOT_EVALUABLE. Per question, `question_responsiveness`: RESPONSIVE ("the rows directly address every requested part"), PARTIAL ("they address only part of it, or carry material ambiguity"), NOT_RESPONSIVE, NOT_EVALUABLE. Each question also carries a `required_semantics` list (four to six items), which the task never asks the reviewer to use.

Across the seven cells: 14 RESPONSIVE, 14 PARTIAL, 0 NOT_RESPONSIVE, 0 NOT_EVALUABLE.

## What the fourteen PARTIAL rationales say, classified

| cause the reviewer names | cells and questions | count |
|---|---|---|
| A required part is in no row's projected fields, though the sentence behind the row states it | 14-04 (extensional stress), 16-04 (the preferred claim's fields name no mechanism), 19-04 (no row states the mechanism) | 3 |
| A required part is not modelled at all | 16-02 (no field says "beneath the axis"), 19-03 (no bounded depth), 15-04 (volume change, stress), 15-01 (network only as a bare name) | 4 |
| A required part is in the graph and reached by no case | 21-01 (the instrument count, on two subject-less records) | 1 |
| Every part is present; several candidate values sit side by side and nothing marks the answer | 15-03, 16-03, 20-03, 21-03 | 4 |
| Every part is present on separate rows that nothing links | 21-04 | 1 |
| Mixed: the network survives only in a scope string, and two counts are told apart only by prose | 14-01 | 1 |

Only the second row of the table is about whether the graph holds the answer. The other five are about the protocol:

- The first row is the withheld statement. A claim's words reach the graph as a locator and a digest; `Claim.statement` is empty by design (licence-gated). Three PARTIALs are reviewers reading a mechanism through the capture and reporting that the rows alone do not carry it. The ruling "fill Claim.statement" is on the list; this is what it buys.
- The third row is the reachability ruling, already on the list, now with a label on it.
- The fourth row is the binding's design. The type-only binder returns every witness of the case types and selects nothing, by decision at run-08 and run-09, so that no answer can be chosen against the result. A reviewer then judges whether a set that is a superset by construction "directly addresses" the question. Four sessions said the superset carries material ambiguity; run-13's session read the same shape as a precision cost. E-0191 measured that disagreement: the label reproduced on run-20 and not on run-13, and the row-level PARTIAL set had kappa 0.118.
- The fifth row is assembly: the answer is three rows and nothing in a row representation joins them. The protocol excludes free-form synthesis on purpose; the label penalises the exclusion.

## Root cause

One word carries five meanings. "Directly address" is left to the session, and PARTIAL's definition folds a coverage failure ("only part of it") together with a presentation failure ("material ambiguity"). The question file already carries the decomposition that would separate them, `required_semantics`, and the task never binds the reviewer to it. So the grade that is meant to say whether the graph answers the question also says whether the protocol withholds statements, whether the binder selects, whether records without subjects are reachable, and whether rows are joined, and it says all five with one label whose threshold is unwritten. The support fraction is stable because its unit is a row and its question is narrow; the responsiveness label is unstable because its unit is a set and its question is five questions.

Two further absences make the instrument weak independently of the label:

- No control. Every question's answer is in the paper. A graph that fabricated a plausible answer would score RESPONSIVE; a graph that returned everything would score RESPONSIVE; nothing measures the false-positive side.
- Four questions on a coarse surface converge. Run-21's CQ-04 rows are CQ-03's minus 12, in order. With 29 to 44 types, the four questions cannot separate cells from each other; they separate reviewers.

## What is missing, and the fix that follows from the rationales

Protocol v3, grading half:

1. **Coverage per required semantic.** For each `required_semantics` item the reviewer names the row index of a SUPPORTED row whose projected fields carry it, or writes ABSENT with one of four typed reasons: NOT_MODELLED, WITHHELD_STATEMENT, UNREACHED_RECORD, NOT_IN_SOURCE. The responsiveness label is then derived, not chosen: COVERED when every item has a row, PARTIAL with the ABSENT list otherwise, NONE when no item has a row. The reviewer's judgement moves to the unit that has proven stable, one row against one thing.
2. **Assembly as a descriptor, not a grade.** ONE_ROW, LINKED_ROWS, UNLINKED_ROWS, recorded per question. It reports what the fourth and fifth causes above measured and stops it from lowering a label.
3. **Support judged once per witness, not once per row.** Run-21 had 490 rows over 182 witnesses. Coverage per question then maps semantics onto witnesses already judged. Fewer judgements, and the same judgement is never made twice with two outcomes.
4. **Controls in the question set**, each with its expected outcome declared at authoring: questions whose answer is not in the paper (expected NONE; a COVERED is a fabrication finding), questions whose answer is only in a figure or table (excluded surface; expected NONE), and paraphrases of positive questions (expected the same coverage; a difference is a reliability finding).

## The thirty-question set, as a design

Five tiers of five, plus five controls, authored by a fresh session from the reading alone before any further cell, frozen and withheld as the four are now:

| tier | what a row must carry | example shape |
|---|---|---|
| T1 lookup | one field of one record | a name, a count, a date |
| T2 relation | two records and the relation between them | which campaign deployed which instrument kind |
| T3 quantity | a bounded value, its unit, its status, its subject | a depth range at a named segment |
| T4 epistemic | a claim with modality and disposition | which hypotheses the authors declined, and which they prefer |
| T5 composition | two or more rows read together | the preferred mechanism with the observation that motivates it |
| controls | declared expected outcome | two absent-from-paper, one figure-only, two paraphrases |

What it would show that four questions cannot: a coverage profile per tier per cell (where each producer's graph stops carrying the paper), a fabrication rate on the controls, a reliability figure from the paraphrases, and separation between cells whose four-question labels are identical. What it costs: one authoring session; a review whose size is set by witnesses (3 above), not by questions; the type-set judgement thirty times instead of four, which the closure check now guards. What it does not fix: the coarse-surface convergence. Thirty questions over 29 types still return overlapping supersets; the coverage table makes that visible per tier rather than hiding it in one label.

## What this does not claim

Nothing above re-grades a cell. The 14 PARTIAL labels stand as their sessions gave them; the table reads their reasons back. Whether run-13's four RESPONSIVE labels would survive the coverage rule is unknown until it is applied, and applying it to the frozen cells is a re-review, which is a ruling.

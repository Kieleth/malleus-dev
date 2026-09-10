# Learnings after the five cells of the record condition (2026-09-10)

Written by the overseer session for Luis, so that the state and the reading survive any session boundary. Every number is from a frozen file, a validated review record, or a ledger entry named here; nothing is ratified beyond run-21 (E-0205).

## The evidence

Five producers of one condition (Claude Opus 5, Core c95dba7, one skill, one spawn message, one document: the Yu et al. article, CC BY-NC-ND, text layer only), reviewed under two protocols. Table in handover/2026-09-10-run-24-rca.md; script paper-v4 scratchpad cells_table.py (rebuild from the frozen files: results/run-result.json, results/census.json, results/launch-log.json, ontology-run/result.json, results/usage.json per cell, and the review records under paper-v4/evaluation-v4/run-NN/).

| | run-20 | run-21 | run-22 | run-23 | run-24 |
|---|---|---|---|---|---|
| harness / questions | v4.10 / v2 (4) | v4.10 / v2 (4) | v4.12 / v3 (30) | v4.13 / v3 (30) | v4.13 / v3.1 (30) |
| accepted facts | 4,314 | 3,780 | 3,664 | 4,152 | 5,032 |
| entities / relations | 426 / 55 | 508 / 26 | 443 / 31 | 417 / 22 | 400 / 21 |
| declared gaps | 77 | 94 | 15 | 20 | 153 |
| runner attempts | 2 | 1 | 1 | 1 | 1 |
| witnesses supported / partial | 417 / 17 rows | 471 / 19 rows | 449 / 0 | 422 / 6 | 405 / 11 |
| positive questions covered / partial / none | 3 R / 1 P | 1 R / 3 P | 12 / 12 / 1 | 16 / 9 / 0 | 15 / 10 / 0 |
| semantics named of 102 | – | – | 82 | 92 | 90 |
| absences unreached / not modelled / withheld | – | – | 11 / 7 / 2 | 0 / 8 / 2 | 0 / 5 / 7 |
| controls matched of 5 | – | – | 4 | 4 | 5 |

Ledger: E-0196/E-0197 (run-21), E-0205 (ratification 09 to 21), E-0341/E-0342 (run-22), E-0343 to E-0345 (harness v4.13, run-23), E-0346 to E-0349 (questions v3.1, run-24). RCAs: handover/2026-09-09-run-22-rca.md, 2026-09-09-run-23-rca.md, 2026-09-10-run-24-rca.md.

## What is proven

1. The protocol path works end to end, repeatably, without hand repair: ontology accepted by the compiler at the first attempt five of five; population admitted and replayed by Core at the first runner attempt four of five, the fifth at the second.
2. Fidelity holds mechanically. Across 1,293 witness judgements in the three v3 cells: 0 UNSUPPORTED, every statement digest recomputes; 0 fabricated vocabulary citations across the cells (20 URLs checked by fetch). The digest-and-locator design makes invention detectable, and under it the models did not invent.
3. Coverage is measurable and attributable. Once the evaluator's query reach was fixed (harness v4.13, SUBJECT_ANY), 90 to 92 of 102 required semantics of thirty questions are answerable from the graph; every absence carries a cause (licence: WITHHELD_STATEMENT; ontology: NOT_MODELLED); the five controls behave (five of five under questions v3.1).
4. The apparatus corrects itself with a record: every cell's RCA moved the harness or the protocol (v4.10 to v4.13, review v2 to v3, questions v3 to v3.1), each change stated with its expected effect and falsifier before the next cell ran.

## What is not proven

- Generality: one document, one producer family, one skill.
- Agreement: the protocol does not make models agree on what to model (relations 21 to 55, declared gaps 15 to 153 across five producers of one condition). It makes what they model honest and replayable.
- Answers: coverage of required semantics is not a correct assembled answer; in most questions the answer's pieces sit as unlinked rows and composition is the reader's.
- A baseline: no comparison with a model reading the PDF directly; the numbers say what the graphs carry, not that they beat anything.
- Ratification: runs 22 to 24 are preliminary; two of three reviewers saw the control expectations before judging.

## The honest thesis

Malleus turns a model's proposals into knowledge that is faithful to its source and replayable, with provenance and refusals recorded, and measures its own coverage against declared questions. It does not make the knowledge complete or canonical. The contribution is the measurement apparatus (digests, locators, controls, coverage by cause, the leak ladder, the ledger) as much as the numbers.

## Luis's direction on the paper (2026-09-10, verbatim)

"I think the centerpiece of the paper is the shop example/dataset, the pdf, and the robotics challenge." Three surfaces of one protocol: structured rows (the Small Shop fixture; shop-01 at E-0201 to E-0204, Core's connected Shop story of 09-08), a document (the five cells above), and actions (the robotics branch codex/robomme-offline: Core-governed dispatch into a simulator, no task success yet). The earlier writing options (ratify 22 to 24; rewrite on the four questions with the five cells; Codex's 5,170-word draft with its own captures) stand in the chat of 2026-09-10 and are not yet ruled; this direction reframes the spine as three inputs, not one.

## Rules earned on these cells

- A type set that lists a subject-bearing type alone reaches only its subject-less records under v4.12; v4.13 fixed the reach, the evaluator still lists the carrying types (E-0342).
- Write ledger bodies and commit messages to a file before any conditional block (two slips on 09-09).
- A gate that only passes with a path outside the repository on PYTHONPATH has a hidden input (E-0339).
- Every parent-side command runs against Core exported from the pinned commit when the repository has moved (runs 22 to 24).
- Any split of thirty type-based questions across two reviewers shares nearly every witness; one reviewer per cell under v3 (E-0342).
- An excluded-surface control must not carry an in-text semantic (v3.1, E-0346).
- The v3 task template names a locator form (assertion:NNNN) that later captures do not use; harmless so far, to fix at the next protocol revision (E-0349).

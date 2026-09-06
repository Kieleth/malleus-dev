# Stepping back after ten iterations: where the complexity sits, 2026-09-06

Overseer session, written during the hold on Luis's rulings. No change is made here. Every claim points at a ledger entry or a count taken from the tree today. The reading is quoted nowhere.

## 1. The harness is copied twenty times, and the copy is where the fixes went

Counts from the tree: twenty cell directories (run-02 to run-21) each carry six to ten harness scripts, 10,179 lines in run-21 with its tests. `compile_ontology_candidate.py`, `run.py` and `prepare_producer.py` have twenty distinct digests across twenty cells, one per cell, because each embeds its run id; `native_query.py` has five, which are its five real versions. The root copies at `paper-v4/experiment-v4/` are frozen at run-01, and invoking one of them by habit refused run-21's ontology on a stale manifest digest (E-0196, overseer error). The freeze template lives in the scratchpad, derived per cell by sed, and accumulated six fixes across runs 13 to 21 plus two defects the derivation itself introduced (a guard still naming the previous entry; a docstring joined to an import in E-0199's script).

What one design removes: the harness lives once at the experiment root and takes the run id as an argument; a cell pins the harness commit in its run contract exactly as it pins Core; the freeze is a script in the repo with the run id as its parameter. The frozen cells do not move. Cost: one refactor of five scripts and the freeze; the per-cell tests keep reading their own frozen files. Benefit: every fix lands in one place, and the root-versus-cell trap is gone because there is no second copy.

## 2. The per-question type set was never what executed

E-0198 and E-0199: the executor reaches a type and its subtypes and projects from a binding-wide map, so seven of twelve frozen cells' sets were not closed per question and 117 rows belonged to types the question's set never named. Iteration 10 made the set state what it reaches (the closure check). The deeper fact is the second session's note on run-21: CQ-04's 166 rows are CQ-03's 178 minus 12, in the same order, by construction of the type-only binding on a surface of 29 types. With coarse surfaces the four questions converge on the same rows, and only the responsiveness label separates them.

What this means for master plan item 9 (more questions): on this instrument, a fifth question over the same surface will largely return rows the first four already returned. More questions need either a finer surface (which the producer decides, and run-20 versus run-21 shows the grain varies 44 to 29 inside one condition) or a richer binding than type-only, which was retired deliberately at run-08 to keep answer selection out of the binder. The choice between those two is a ruling; the fact that it is a choice is the finding.

## 3. The producer writes its own copy of the adapter

Core-20 put the adapter's 48 refusal reasons into the skill as a pre-flight list (E-0180). Run-20's producer built a checker from it and caught 37 defects before writing; run-21's built two, and caught everything. Each producer's checker is a reimplementation of the adapter from prose, and the one defect that reached run-20's runner was a divergence between its reading of the word rule and the adapter's (E-0189). The ruling on the isolation boundary (allow an adapter dry run) is the simplification: one adapter, called twice, instead of an adapter and a paraphrase of it per session. Nothing new here beyond restating why the ruling matters in these terms.

## 4. The record's weakest joint is a threshold nobody wrote down

E-0191: CQ-03's responsiveness has kappa 0.118 between two Opus sessions on run-20, while the support fraction is stable to two places across cells (E-0197). Run-21's second session named the alternative standard under which both its PARTIAL labels become RESPONSIVE. Every candidate cell of record differs from the next on this label and on nothing mechanical. Review protocol v3 is the ruling; the stepping-back point is that the paper should report the support fraction as the measured quantity and the responsiveness label as a reviewer's judgement with its reliability beside it, whichever way the ruling goes.

## 5. The records themselves

Two hundred ledger entries and eighty-eight journal sections since 2026-09-05T04:10Z. Every count in them came from a script and every correction is in place with its cause. That is the discipline working; it is also the sign that the harness asks the overseer to do by hand what the harness could do once: the launch log, the usage file, the freeze, the review merge and the RCA table each have a script in the scratchpad that reads the same files. Folding them into the repo harness (point 1) turns the overseer's checklist into the cell's own output.

## What I would do first, if asked

Point 1. It is mechanical, it removes a class of overseer error that has already fired, and it makes points 2 to 5 cheaper to act on because each becomes one edit. Points 2, 3 and 4 are rulings and stay open.

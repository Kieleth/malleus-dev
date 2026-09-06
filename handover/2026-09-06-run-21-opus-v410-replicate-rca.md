# RCA: run-21, Opus 5 at v4.10, the run-20 replicate: within-condition variance, 2026-09-06

Overseer session. Run-21 is run-20's harness byte for byte with the run id moved, the same producer block (Opus 5, `claude-opus-5`) at the same Core coordinate (c95dba7, Core-19 reporting, Core-20 pre-flight list). No change under test: the cell measures what one condition varies by. Evidence: `private/paper-v4-v4-run-21/` (launch log, producer work, plan, capture, query result, the pre-amendment binding files), the frozen public results under `paper-v4/experiment-v4/run-21/`, run-20's frozen results, the preliminary review (E-0197), and the scratchpad pass `rca21.py`, which reads both cells' frozen files and nothing typed. The reading is quoted nowhere.

## Outcome

| measure | run-20 | run-21 |
|---|---|---|
| ontology attempts | 1 | 1 |
| facts / project classes / root extensions | 4,314 / 28 / 5 | 3,780 / 13 / 7 |
| surface types (subject-bearing) | 44 (5) | 29 (5) |
| grounding | every term confirmed; 0 none_found | 16 of 17 terms confirmed, 1 unverified; 3 none_found with a search note |
| first runner attempt | refused, 1 defect | admitted |
| assertions (fully / partly / unformalized) | 393 (317 / 21 / 55) | 399 (306 / 93 / 0) |
| blocks asserted / declared / untouched | 184 / 2 / 0 | 186 / 0 / 0 |
| records (entities, events, relations) | 482 (426, 1, 55) | 535 (508, 1, 26) |
| typed gaps | 77 (49 TYPE_ABSENT, 18 REQUIRED_FIELD, 6 RELATION_ABSENT, 4 AGGREGATE_ONLY) | 94 (88 RELATION_ABSENT, 4 REQUIRED_FIELD, 1 INTERVAL, 1 TYPE_ABSENT) |
| subjects proposed / attachable / ambiguous / unnamed (of) | 117 / 33 / 30 / 55 (235) | 77 / 46 / 93 / 98 (314) |
| records with locator and digest | 235 of 235 | 314 of 314 |
| non-local relations / largest hub | 24 of 55 / 16 | 0 of 26 / 10 |
| cases (ENTITY, RELATION, SUBJECT) | 3,068 (38, 2,852, 178) | 1,883 (19, 1,715, 149) |
| rows (by question) / witnesses | 434 (34, 105, 158, 137) / 220 | 490 (24, 122, 178, 166) / 182 |
| rows from more than one case | 33 | 237 |
| review | R R P R; 417 S / 17 P / 0 U; 251 digests | P R P P; 471 S / 19 P / 0 U; 215 digests |
| producer tokens (ontology, population, correction) | 433,787 (189,798; 226,989; 17,000) | 387,470 (179,467; 208,003; none) |

Expected (E-0193): admission within two structural returns and no UNSUPPORTED row at review. Both held: no return, no UNSUPPORTED row.

## What held twice

The floor the protocol sets held in both cells: an ontology accepted at the first attempt with every direct root extension grounded or honestly declared ungrounded; a population admitted within the return budget; every statement a byte span of its block; every source-asserted record carrying a locator and a digest that the census verifies whole; no fabricated citation; no untouched block. Run-21 sits under that floor with nothing left over: zero first-attempt defects, zero declarations, zero non-local relations. The first-attempt defect count across the Opus cells is now 0, 7, 0, 1, 0, and of the three admitted cells whose census reports block labels (runs 19, 20, 21) this is the only one with no declaration.

## What the same block chose differently

The variance is in what the producer modelled, not in whether it met the rules.

- **Ontology shape.** Run-20 minted twenty-eight classes, twelve of them feature subtypes and four material subtypes, and grounded five root extensions to BFO, RO and PROV-O. Run-21 minted thirteen, one feature type carrying `feature_kind` and one material type carrying `material_kind`, grounded four extensions to the Gold Book, DCMI, PROV-O and Schema.org, and declared the three geoscience blocks `none_found` with a search note naming the vocabularies it would not cite unverified. The same instruction produced a taxonomy in one session and an enumeration in the other. Both pass the rite; the surface the questions see is 44 types in one cell and 29 in the other.
- **Where the reading stops.** Run-20 declared 49 TYPE_ABSENT gaps and 6 RELATION_ABSENT; run-21 declared 1 and 88. Run-20's producer met an unmodelled thing by declaring the type absent; run-21's, with coarser types that hold more things, met the unmodelled relation between them by declaring the relation absent. Both are honest gaps under the rule; they are different readings of what the ontology should have carried.
- **Relations.** 55 in run-20 with 24 non-local and a byline hub of 16; 26 in run-21 with none non-local and a largest hub of 10. Run-21 wrote fewer relations and every one on the sentence naming both ends; the 88 RELATION_ABSENT gaps are the relations it would not derive from a neighbouring sentence.
- **Subjects.** Run-20 proposed 117 of 235 and left 30 ambiguous; run-21 proposed 77 of 314 and left 93 ambiguous. Run-21's ReportedClaim carries a subject in 20 of 145 records. The producer's own account names the strict word rule as the reason; on the census this is the more conservative reading of the same rule run-20's correction applied to six records.
- **Records.** 508 entities against 426, with the 100 bibliography blocks captured whole as statements and every running header asserted, by the producer's report; run-20 declared two map-panel blocks nothing-assertable. Run-21's producer took the position that no block of this reading is void, and the census records it.

## The query, and the evaluator's error

The type sets were translated from run-20's judgement onto a surface with one feature and one material type, which made the translation coarser by construction (1,583 cases at acceptance against 3,068). Executing that binding was refused: the v4.9 executor projects every reached record by its own type, an AnalyticalMethod record reached through the Method case had no projection because its type was in no set, and the executor's docstring assigns the correction to the evaluator's sets rather than guessing past it. The acceptance note had claimed Method's case returns its subtypes; right about reach, wrong about projection. Run-20's sets met the rule by listing GeophysicalModel beside Method, so the rule had never fired. The sets were closed under the surface's subtypes (AnalyticalMethod beside Method in CQ-01, CQ-03 and CQ-04, the only omission by a closure check over the is_a chains of the ontology attempt and the four packs) before any row existed; the first sets, note and bindings are frozen beside the amended ones as `*.first.*`, and the launch log records the refusal, the amendment and the reason.

Root cause: a partial read. The note reasoned about the binder's reach from run-20's note and never read the executor's projection rule, which is one docstring away. Classification: overseer error, protocol-visible (the refusal is typed and the correction is the protocol's own), no row selected against.

Fix for a later harness version, not applied now: the binder can compute the same closure at acceptance and refuse a set that lists a type without its surface subtypes, so the error is caught before phase two exists instead of after admission. One check, one place, and the executor's rule becomes redundant rather than load-bearing.

Consequence in the counts: 237 of 490 rows come from more than one case (run-20: 33), because listing the parent beside its subtype reaches the same record through two ENTITY cases and its SUBJECT cases, and the executor merges them into one row per witness per question. The row count is not inflated by it; the witness count (182 against 220) is the comparable figure.

## The overseer's other error

The first gate invocation used the frozen run-01 gate at the experiment root, whose manifest carries the 2026-09-04 pack digests, and it refused on the metrology digest. The cell's own gate under `run-21/` accepted the same bytes seconds later. Parked under `overseer-misinvocation/`, not an attempt, recorded in the launch log. Root cause: a path recalled instead of read; the per-cell copy exists for exactly this reason. Fix: none needed in the harness, the refusal was right; the rule in memory now names the per-cell path.

## What the review found

**CQ-01 and CQ-02 (first session).** CQ-01 PARTIAL, 23 SUPPORTED and 1 PARTIAL of 24: the rows name the campaign, the instrument kind and the acquisition chain, and no row carries the instrument count, which the reviewer reports is in the reading and reaches no row. Checked after the report: the count is in the population twice, as ReportedObservation records of 19 ocean-bottom seismometers formalized by two assertions, both without a subject. A subject-bearing type is reached only through its subject, and an ENTITY case is bound only for types without one (v4.4), so a subject-less ReportedObservation is unreachable by construction. This cell carries 237 such records (125 ReportedClaim, 107 ReportedObservation, 5 ReportedRatio) against run-20's 118, and here the class decided a responsiveness label: run-20's CQ-01 was RESPONSIVE on a CountObservation the producer had given a subject. The one PARTIAL row is the campaign's projected duration, which the cited block gives as the length of continuous recording. CQ-02 RESPONSIVE, 116 SUPPORTED and 6 PARTIAL of 122, the six one defect: a `feature_kind` the cited block does not state (a surface and a termination classified as core complexes, faults classified as normal, a transform valley as axial). Names, orientations and statuses hold in every one. 63 digests verified, 13 RELATION rows all local, 63 SUBJECT rows all in block, three of them by a tag.

**CQ-03 and CQ-04 (second session).** Both PARTIAL, 172 SUPPORTED and 6 PARTIAL of 178, 160 and 6 of 166; the six PARTIAL rows are CQ-02's six feature records again, so eighteen of the cell's nineteen PARTIAL rows are six `feature_kind` values the cited prose does not state, each returned under three questions. Both sessions state that whether a near-miss in a closed vocabulary is a row claim or a modelling decision is not settled by the task, judged it a row claim, and never went past PARTIAL. The responsiveness reason is the reviewers' linking standard, not a content gap: CQ-03 returns several depth ranges and concentration ranges for two segments with nothing marking the answering pair (the material-ambiguity line of runs 15, 19 and 20, which run-13's reviewer read as RESPONSIVE), and CQ-04's mechanism is answerable only by reading two unlinked claim rows together, where run-20's reviewer had the mechanism, its marking and the degassing chain on separate rows and called it RESPONSIVE. The session notes that CQ-04's 166 rows are CQ-03's 178 minus 12 in the same order, so the two support blocks are identical row for row by construction of the type-only binding. 152 digests verified, 28 RELATION rows all local, 147 SUBJECT rows all in block.

**The review as a variance measure.** The support fraction is the same figure twice (417 of 434, 471 of 490). The labels moved on two questions, and neither move is about the producer: CQ-01 fell to PARTIAL because the count the question asks for sits on records no case reaches, and CQ-04 fell because a reviewer's standard for "identifies the answer" is stricter than run-20's reviewer's. One is Luis's reachability ruling; the other is the reviewers' line, measured in E-0191 at kappa 0.118 on CQ-03. Both were open before this cell; this cell shows each one moving a label inside one condition.

## What the replicate says about the condition

Two cells of one condition agree on everything the protocol guarantees and differ on most of what it leaves to the producer: the ontology's grain, the gap kinds, the relation count, the subject rate, the row count. A paper claim about "Opus 5 at v4.10" is a claim about the floor: admission, provenance, citation honesty, no UNSUPPORTED row. The counts above are one draw each, and the matrix now has the pair to say so. The record cell decision stays Luis's; the pair gives it a within-condition range instead of a point.

## Corrections to earlier records

- The journal's run-21 gate entry first wrote the phase-two dispatch as 12:05Z before the dispatch; corrected in place to the transcript's 12:01:59Z.
- The acceptance note's sentence about Method's case is corrected by the note's `amendment` section, not rewritten.

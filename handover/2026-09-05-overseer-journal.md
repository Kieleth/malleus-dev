# Overseer journal, 2026-09-04 to 2026-09-05: the v4.1 matrix, five Core fixes, two ratified cells

Overseer session. Everything below is on disk or in git; paths and commits are given so nothing rests on this text. Private cell directories (`private/paper-v4-v4-run-0N/`) are gitignored and carry reading text; the public record per cell is `paper-v4/experiment-v4/run-0N/` and the paper ledger entries E-0122 to E-0132.

## What the stretch did, in order

1. Audited the overnight Codex work on Core (P1 to P9) and the paper thread, took both roles over (Codex tokens exhausted), and fixed Core in numbered Opus agents: Core-1 (ledger digests, OVR-000385 to 390), Core-7 (aggregated grounding and UNDERIVED_FIELD diagnostics), Core-8 (packs 0.2.0: QUDT quantity kind class, claim locator and digest, source licence; decisions 13 and 14 in `design/KNOWLEDGE_PACKS.md`), Core-9 (skill and adapter fixes from the Haiku RCA, OVR-000397), Core-10 (multivalued properties at admit, OVR-000398).
2. Rebuilt the paper harness per cell (run contract, producer input manifest with `git show` digests, isolation-only spawn message, gate, runner over the public facade, type-only native query, review package) and ran the v4 cells run-02 (Opus, admitted, ratified) and run-03 (Sonnet, refused at ontology), then the v4.1 cells run-04 (Opus), run-05 (Sonnet), run-06 (Haiku) and the paired variant run-07 (Haiku producer plus Haiku checker per phase).
3. Restructured the manuscript to 1.4.x (plain abstract, state of the art with verified references, hashes and run narratives to appendices, latest results lead, the Fahland 2022 shop as calibration) and rendered the PDF at 16 pages with zero warnings.
4. Wrote the Haiku RCA (`handover/2026-09-05-haiku-rca.md`) and journaled every cell in the paper ledger.

## Cells, as they stand

| cell | producer | protocol | ontology | population | review | producer tokens |
|---|---|---|---|---|---|---|
| run-02 | Opus 5 | v4 | accepted, attempt 03 | admitted, 2 returns; 419 entities, 170 relations | ratified (E-0122, E-0123) | 410,064 |
| run-03 | Sonnet 5 | v4 | refused, 3 attempts | not started | none | 259,405 |
| run-04 | Opus 5 | v4.1 | accepted, attempt 02 | admitted at the Core-10 fix, 0 returns; 256/3/144, 403 traced, 186 of 186 blocks | pending | 371,026 |
| run-05 | Sonnet 5 | v4.1 | accepted, attempt 02 | admitted, 0 returns; 47/1/26, 27 of 186 blocks | ratified (E-0131, E-0132) | 382,952 |
| run-06 | Haiku 4.5 | v4.1 | accepted, fabricated citation | refused after 2 returns | none (E-0129) | 137,734 |
| run-07 | Haiku 4.5 pair | v4.1-pair | accepted after 1 check loop | refused after 1 loop and 2 returns | none (E-0130) | 166,959 + 98,381 checker |

Tokens are the harness's cumulative session figures differenced per stage; per-cell `usage.json` sits beside each launch log, public for run-05.

## Defects found in this stretch, with status

Core, fixed:
- Frozen tuples reached the ontology validator at admit, so every multivalued property refused with `must be a list`. First surfaced by run-04, the first population with a list-valued property. Core-10, RED then GREEN, OVR-000398.
- The skill's capture template carried the adapter's call arguments and a contract-identity placeholder, so Haiku wrote a contract identity into its file. Core-9 separates the output file from the call and deletes the placeholder.
- The verbatim rule had no method; the block-id rule did not say ids come from the inventory. Core-9 states both.
- `NOT_VERBATIM` and `UNKNOWN_BLOCK` refused one at a time. Core-9 lists every one in a single refusal (run-07's attempt 2 shows it: two statements in one diagnostic).
- Citations had no honest-gap rule. Core-9 states that a fabricated vocabulary is worse than a `none_found` block.

Harness, fixed:
- The gate script recorded only `str(error)` and dropped the chained `__cause__` for `IMPORT_READER_REFUSED` (run-05 attempt 01); the overseer recovered the cause with the public facade and returned it. The next harness must surface chained causes.
- Runner scripts hardcoded an attempt number; run-06 lost one harness invocation to it (no return consumed).
- Run-05's review task carried run-02's row counts on a wrapped line; the reviewer judged the actual rows, which the manifest enforces; corrected in 1580b79.

Open, protocol:
- Coverage has no gate by design. Sonnet read "stop when another addition would require invention" as "stop when another addition would require choice" and stopped at 27 of 186 blocks. Proposed: one sentence in the next spawn message stating that reviewing the next block is not invention. Recorded in the master plan 1.3.2 as a precondition of the split-producer variant.
- Citation truth is checked nowhere mechanically. Run-06's fabricated standard passed the rite; the review step must verify every vocabulary URL. Not yet in the review task.
- A same-family checker reading the same pinned skill approves what the skill induces (run-07: envelope marked conformant; a mispathed formalization target marked satisfied; two paraphrases not flagged). The pair catches producer errors, not skill errors.
- Formalization target paths: Haiku wrote `['event_type']` where the field lives under `properties`; the diagnostic names it, the skill's template shows the right shape.

Open, modelling and design:
- Event records cannot be relation endpoints, so every cell's Earthquake is an island in the query rows. This is the anchors and participation question, awaiting Luis's three answers (type anchors at roots, every class, or both; source anchors always or per profile; anchors projected or proposed; the overseer recommends projected).
- Hedges are lost on the way into intervals: an approximate 0.7 GPa became a closed `[0.7, 0.7]` with empty uncertainty (run-05, judged PARTIAL). Imported values (a 2 to 3 bar threshold from another work) carry no attribution field. Both are pack questions.
- Spatial relations ("beneath the segment axis") live in free-text `quantity_kind`, not in a relation; CQ-02 was PARTIAL for run-05 on this.

Environment:
- Base conda python (linkml-runtime 1.10.0) refuses the harness; only `.venv` works. The environment lock test does not catch it.
- A Codex worktree's broken editable install shadows `malleus-inquisitor` on PATH; producers reported it and did not fall back.

## Decisions taken by Luis in this stretch

- Manuscript 1.2.1 stays the paper of record; 1.4.x carries the restructure; the v2 and v3 trials are appendix history, not results.
- Runs proceed in "re-run and decide per iteration" mode; Codex cells once malleus is stable; Anthropic cells with model ids pinned.
- Ratified run-05's preliminary review as recorded (E-0132).
- Added to the master plan: split-producer variant if time allows; reviewer swap once the Opus 5 cell of record is settled.
- QUDT quantity kind class adopted (decision 13); the subject-edge rule rejected in favour of ontology anchors in the graph (design pending); the flexible claim locator confirmed as designed (decision 14).

## What is next, in order

1. Run-04, admitted at the Core-10 fix on 2026-09-05: type-only binding, query, freeze, fresh review, ratification. This is the candidate Opus 5 cell of record.
2. Deep sweep for defects and appendix evidence (dispatched 2026-09-05; deliverables under `paper-v4/appendix-evidence/` and `handover/2026-09-05-deep-sweep.md`).
3. The anchors design once the three answers arrive.
4. Manuscript 1.5: the matrix under the final protocol, early trials in the appendix.

## Run-04's 61 typed gaps, read by cause (2026-09-05)

Source: `private/paper-v4-v4-run-04/results/gaps.json` (withheld; carries the producer's gap statements). Grouped by what would remove the gap, not by kind:

| cause | gaps | kinds | what would remove them |
|---|---|---|---|
| A value the source marks approximate has to be stored as an exact bound pair | 25 | INTERVAL_NOT_EXPRESSIBLE | a value qualifier on the metrology pack's quantity value (approximate, about, open bound, exact); the same limit produced run-05's 0.7 GPa PARTIAL at review |
| A year-only date has no place on an Event, whose `occurred_at` is a datetime | 1 | INTERVAL_NOT_EXPRESSIBLE | temporal precision on events, as chronology's Instant already carries; adjacent to the anchors and participation design |
| The text layer destroyed letter spacing in bylines, references and one award number | 20 | REQUIRED_FIELD_ABSENT_IN_SOURCE | nothing in Core: the reading is frozen for the paper; a source limit to report, confined to bylines and references, none in domain content |
| The producer's own ontology made `structure_kind` required and the source names faults without a kind | 1 | REQUIRED_FIELD_ABSENT_IN_SOURCE | the producer's choice; honest gap |
| Figure panels and legends flattened to axis labels; groups described by depth range without a count | 8 | AGGREGATE_ONLY | nothing: figures are excluded by the question scope and a "majority" without a count is correctly not a count |
| No contribution-role vocabulary in the research pack | 2 | TYPE_ABSENT | a grounded role enumeration (the CRediT contributor roles are a published NISO taxonomy) on the research pack's contribution relation |
| Statements about the publication process (competing interests, reprints, a funding programme with no award) | 3 | TYPE_ABSENT | nothing: out of the domain by design |
| The source never states whether two named hydrothermal features are one | 1 | RELATION_ABSENT | nothing: the correct gap |

Reading: 26 of 61 gaps are two pack limits (approximation and event-date precision), 2 are one missing vocabulary, 20 are the text layer, and 13 are the protocol working as designed. Run-02 under v4 reported 84 AGGREGATE_ONLY gaps against run-04's 8 under v4.1; the derivation rule and the revised packs changed what the producer counted as a gap, so the two figures are not comparable as coverage.

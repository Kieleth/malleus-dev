# Overseer journal, 2026-09-04 to 2026-09-05: the v4.1 matrix, five Core fixes, two ratified cells

Overseer session. Everything below is on disk or in git; paths and commits are given so nothing rests on this text. Private cell directories (`private/paper-v4-v4-run-0N/`) are gitignored and carry reading text; the public record per cell is `paper-v4/experiment-v4/run-0N/` and the paper ledger entries E-0122 to E-0132.

## What the stretch did, in order

1. Audited the overnight Codex work on Core (P1 to P9) and the paper thread, took both roles over (Codex tokens exhausted), and fixed Core in numbered Opus agents: Core-1 (ledger digests, OVR-000385 to 390), Core-7 (aggregated grounding and UNDERIVED_FIELD diagnostics), Core-8 (packs 0.2.0: QUDT quantity kind class, claim locator and digest, source licence; decisions 13 and 14 in `design/KNOWLEDGE_PACKS.md`), Core-9 (skill and adapter fixes from the Haiku RCA, OVR-000397), Core-10 (multivalued properties at admit, OVR-000398).
2. Rebuilt the paper harness per cell (run contract, producer input manifest with `git show` digests, isolation-only spawn message, gate, runner over the public facade, type-only native query, review package) and ran the v4 cells run-02 (Opus, admitted, review preliminary) and run-03 (Sonnet, refused at ontology), then the v4.1 cells run-04 (Opus), run-05 (Sonnet), run-06 (Haiku) and the paired variant run-07 (Haiku producer plus Haiku checker per phase).
3. Restructured the manuscript to 1.4.x (plain abstract, state of the art with verified references, hashes and run narratives to appendices, latest results lead, the Fahland 2022 shop as calibration) and rendered the PDF at 16 pages with zero warnings.
4. Wrote the Haiku RCA (`handover/2026-09-05-haiku-rca.md`) and journaled every cell in the paper ledger.

## Cells, as they stand

| cell | producer | protocol | ontology | population | review | producer tokens |
|---|---|---|---|---|---|---|
| run-02 | Opus 5 | v4 | accepted, attempt 03 | admitted, 2 returns; 419 entities, 170 relations | preliminary complete, NOT ratified (E-0122; corrected in E-0134) | 410,064 |
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

## What is next, in order (revised 2026-09-05 after the run-04 ratification and the deep sweep)

Decided by Luis: Core-12, then a v4.2 Opus cell on packs 0.3.0, then analysis.

1. Core-11 (metrology value qualifier, research CRediT roles, OVR-000398 correction), in flight.
2. Core-12 (DIGEST_MISMATCH, modality-disposition consistency, derivation locality and fan-out census axes, skill sentences), scoped in `handover/2026-09-05-run-04-review-rca.md`; dispatches when Core-11 releases the ledger.
3. Run-08, the v4.2 Opus 5 cell: harness under construction by Paper-10 (binding frozen at ontology acceptance, stop rule clarified, gate surfaces chained causes, interpreter preflight, launch-log v2 and public cost record, review task v2); pinned to the post-Core-12 coordinate with `pin.py`; then producer, freeze, review, ratification, and the comparison with run-04 (E-0133, E-0135).
4. Manuscript 1.5 on the ratified Opus cell of record, with run-02 to run-07 in the appendix; run-02's review is unratified (E-0134) and stays so unless Luis ratifies it.
5. The anchors design (events as relation endpoints, event temporal precision, imported values) once Luis's three answers arrive.

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

## Core-12 residuals and a harness catch (2026-09-05, after OVR-000402)

- A record that carries `statement_sha256` and no `assertion_locator` is not checked by DIGEST_MISMATCH, because nothing in the capture can check it. A producer could escape the digest check that way. Candidate for the next Core entry: refuse a digest with no locator, or require the locator whenever the digest is present, decided at the pack.
- `_derivation_census` in the document adapter takes an unused `records_by_id` parameter; found after OVR-000402 sealed and run-08 pinned the commit. One line for whoever holds the next ledger entry.
- The adapter's new `contract_view` argument defaults to None so older runners keep working; a runner that omits it silently skips EVALUATIVE_SLOT_NOT_EVALUATED. Run-08's runner was run-04's bytes and omitted it; fixed before phase two (commit 05f9c5e) and pinned in run-08's pipeline test. Any future runner must pass it; a harness test that greps for the argument is the cheap guard.

## Run-08 (v4.2, Opus 5) against run-04 (v4.1, Opus 5), 2026-09-05

| measure | run-04 (v4.1, packs 0.2.0, Core 8b806f7 + Core-10 at run) | run-08 (v4.2, packs 0.3.0/0.4.0, Core-9 to Core-12) |
|---|---|---|
| ontology | accepted at attempt 02, one return | accepted at attempt 01, no return |
| population | admitted at runner attempt 2 (attempt 1 refused on the Core-10 defect) | admitted at runner attempt 1 |
| assertions / blocks | 349 / 186 of 186 | 349 / 186 of 186 (182 asserted, 4 nothing-assertable) |
| graph | 256 entities, 3 events, 144 relations | 418 entities, 1 event, 26 relations |
| typed gaps | 61 (26 intervals, 21 required-field, 8 aggregate, 5 type, 1 relation) | 27 (16 relation, 6 required-field, 3 type, 1 aggregate, 1 interval) |
| value qualification | n/a | 108 of 131 observations |
| largest hub / non-local relations | 47 records / not measured | 10 records / 6 of 26 |
| binding | exhaustive, revised twice after seeing rows (900 cases) | frozen at acceptance, executed unchanged (2,084 cases) |
| rows CQ-01 to CQ-04 | 17 / 69 / 83 / 71 | 5 / 2 / 0 / 1 |
| producer tokens | 371,026 | 340,313 |

Reading. Every structural measure moved the right way: fewer returns, fewer gaps, hedges carried, digests recomputed, dispositions from disposing sentences, no hubs, a binding that cannot have seen a row. The question rows collapsed. The cause is on disk: run-08's graph holds 131 observations and 85 claims with no relation from any of them to a feature, a sample, a campaign or another claim. Its 26 relations are contribution, funding, archive, software and feature-to-feature links. The research pack's CLAIM_CONCERNS, SUPPORTS, CHALLENGES and OBSERVED_WITH were on the surface and unused; the 16 RELATION_ABSENT gaps are about affiliations and unnamed discontinuities, not about the missing subject links; the session log does not mention them. Run-04 had those links only by hanging them on hub sentences, which Core-12 now names as non-local and the skill now calls a gap. The producer, told that an implied relation is a gap, neither derived the relations that single sentences do support (a depth beneath a named segment's axis is one sentence) nor recorded the rest as gaps; it dropped them. And the query surface is relation-only, so an answer that exists as an unattached observation (34 depth quantities, 20 CO2 quantities) cannot be reached.

Three consequences, for decision:
1. The subject link is not optional. Observations and claims need an edge to what they are about, or the graph is a bag of typed facts. This is Luis's anchors point in its sharpest form; the design should make the subject edge a required, derived part of an observation or claim (from the sentence that states both, else a gap the census counts), not a producer choice.
2. The query surface should reach entities. A case kind that projects a type's fields without a relation (type-only, still value-blind) would have returned every depth and CO2 observation for CQ-03. Cheap; a binding-schema change and a native_query.py change for the next harness.
3. The comparison is one cell against one cell under a different harness, packs and skill; nothing here isolates a cause beyond what the artifacts state.

## Run-08 review outcome and two review-surface debts (2026-09-05)

Preliminary review (fresh Opus 5, 123,865 tokens): CQ-01 PARTIAL, CQ-02, CQ-03 and CQ-04 NOT_RESPONSIVE; 5 rows SUPPORTED, 3 PARTIAL, each PARTIAL a hedge the reading makes and the row carries as settled; all 8 rows derivation-local with the formalizing block a subset of the endpoint blocks; the digest check vacuous because no returned row carries a locator (the Claim, CountObservation and AssertedRatio cases returned no row). Ratification pending.

Debts the reviewer found in the review surface: the retained capture and the query trace summary are named by the task as inputs but are not in the manifest's `materials`, whose list is fixed by the frozen protocol's `review_materials`; both are bound only transitively (the capture through the trace's evidence digest, the trace summary through `stage_identities`). Closing it means a protocol revision (a new frozen protocol version listing seven materials) before the next cell's freeze, or a documented deviation as the CODEX_PRELIMINARY substitution was.

## Decisions of 2026-09-05, late: run-08 ratified, the four v4.2 follow-ups approved

Luis ratified run-08's review as recorded (E-0139) and approved the four items of `handover/2026-09-05-v42-rca.md`. Dispatched in parallel:
- Core-13 (Opus): `subject` on the research pack's SourceAsserted mixin (single, optional, Entity-ranged), SUBJECT_NOT_NAMED aggregated refusal by whitespace-collapsed, case-folded name substring of a formalizing statement, subject-coverage census axis, one skill sentence with guards, research 0.5.0, decision 18; plus Core-12's two residuals (dead parameter; digest without locator refuses). One ledger entry after OVR-000402.
- Paper-11 (Opus): run-09 harness (v4.3) from run-08's: binding schema v3 with RELATION, ENTITY and SUBJECT case kinds, all type-only and frozen at acceptance; review protocol v2 with seven materials (adds the retained capture and the query trace summary); review task v3 template; pin.py; E-0140. Run-09 is measured against run-04's 146 local-relation rows.

Order after both land: re-pin run-09 with `pin.py --commit <post-Core-13>`, verify, stage, launch the Opus 5 producer, gate, citation check, type sets and binding at acceptance, phase two, runner (set the accepted attempt in the runner script), usage from the launch log, freeze, review under protocol v2, ratification, comparison.

## Night loop, from 2026-09-05T04:10Z: Luis's standing instruction and the rules I hold myself to

Instruction, in his words: "continue iterating in loop one change at the time and rerunning, till we find more elegant ways to improve malleus, I want RCA every run, understanding, deep, even if it hurts, and finding novel ways to continue, log/journal, have fun, and remember less is more, many times is about stepping back, reducing complexity and finding a more elegant unified way to achieve things."

Rules for the loop:
1. One change per iteration, named before the cell runs, with the hypothesis it tests written here first.
2. Every cell: gate, citation check, binding at acceptance, phase two, runner, freeze, fresh preliminary review, then the RCA against every earlier cell from the artifacts, with numbers computed by script and the mechanism stated. Reviews stay PRELIMINARY; Luis ratifies in the morning.
3. Core changes: one Opus agent at a time on the ledger, RED then GREEN, additive, every frozen cell still pinned by `git show`. Harness changes: a new run directory, the old ones untouched.
4. Commit with explicit paths, push main after a green gate. Private artifacts stay private; the leak ladder runs on every public file.
5. Prefer removing a rule to adding one. Before each change, ask whether an existing check already implies it; after each RCA, ask which two checks are one check.
6. Nothing irreversible, nothing destructive, no ratification by me, no pushing to any branch but main.

A candidate unification to test when the data supports it: the derivation rule's content checks (verbatim statement, statement digest, subject named in the statement, disposition from a disposing sentence, locality of relation endpoints) are all instances of one rule, "what a pointer derives must be visible in the statement it points at". If one check over every derived scalar (name, number, enum label, subject name) subsumes the rest, four reasons become one and the skill loses four sentences. To be tried after run-09, not before.

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

## Loop iteration 1: run-09 (v4.3, Opus 5), launched 2026-09-05T05:20Z at f6c8c71

Change under test (one idea, two halves): the subject of a source-asserted record is a first-class derived element (Core-13: `subject` on SourceAsserted, SUBJECT_NOT_NAMED by name substring, coverage census, one skill sentence), and the query can see it (binding v3: ENTITY and SUBJECT case kinds beside RELATION, all type-only, frozen at acceptance). Hypothesis: the same model that produced run-08's 131 unattached observations attaches them now, and the questions become reachable without relation records; measured against run-04's 146 local-relation rows and run-08's 8. Falsifier: subject coverage stays low or SUBJECT rows do not reach the answer-bearing quantities.

Also under observation, not under test: the ledger cost of a Core change. Core-13 spent six governance entries, two of them correcting its own evidence and its own count. A Core agent that writes its entry after its last commit, from the diff rather than from the log, would have spent one. Candidate simplification for the ledger procedure, to raise with Luis.

### Iteration 1, first runner attempt (06:13Z): SUBJECT_NOT_NAMED on 98 of 129 subjects

Run-09's population: 343 assertions over all 186 blocks, 775 records (553 entities, 3 events, 219 relations), 129 records carrying a subject, 59 typed gaps. Runner attempt 1 refused at the adapter with one aggregated SUBJECT_NOT_NAMED over 98 records; 31 subjects passed. Measured from the file: the producer named entities with the reading's first descriptive mention ("a short ridge segment (named RC2)", "the brittle-ductile boundary (BDB)", "a network of 19 ocean-bottom seismometers (OBSs)") and asserted about them in sentences that use the short referent ("RC2", "the BDB"); for 47 of the 98 the parenthesised short form occurs in the statement and the descriptive name does not. Returned as structural diagnostic 1 of 2.

Reading. The check is right and the naming convention is missing. Two ways to close it: (a) teach the check aliases (accept a parenthesised abbreviation or a trailing head noun), which is a heuristic that grows; (b) one skill sentence: an entity's `name` is the form the source uses to refer to it in its sentences, the shortest one the reading repeats; the first descriptive mention goes to `description`. (b) is less; (b) also makes names comparable across cells and readable in rows. Candidate for iteration 2 if the producer's repair confirms that renaming is what closes the refusal.

Second finding from the gate, recorded for iteration 2 as well: both Opus cells on the current skill (run-04, run-09) spent their first ontology attempt on a slot with range `date` or `uri`. The elaborator binds five seed scalar types (Boolean, DateTime, Float, Integer, String) and declared classes; the skill's note that every LinkML built-in range loads describes the inquisitor's loader, not the compiler. The elegant fix is the refusal naming the bound ranges and the skill note corrected; no new rule.

### Iteration 1, second runner attempt and query (06:21Z to 06:32Z)

Admitted at runner attempt 2 after the naming repair: 553 entities, 3 events, 219 relations, 775 traced, all 186 blocks, 59 gaps, 9 of 219 relations non-local, largest hub 18 (the byline), subject coverage 106 of 212 (Observation 64 of 114, Claim 37 of 76, CountedObservation 5 of 19, SeismicEvent 0 of 3). Frozen at 92e3800, E-0142.

The v3 query, frozen at acceptance (3,045 cases), returned 1,466 rows: 1,061 ENTITY, 326 SUBJECT, 79 RELATION. Measured before any review:
- CQ-02: 171 SUBJECT rows, 50 of them with subject RC2 (claims and observations about the segment).
- CQ-03: 72 SUBJECT rows; 14 are depth quantities (6 with subject RC2, 4 the BDB) and 12 are CO2 wt% quantities (7 RC2, 5 RC3). Run-08 had these 44 quantities unattached and unreachable.
- CQ-04: the five dispositioned claims come back as SUBJECT rows (the preferred mechanism with subject "mantle"; the four declined ones on the lithosphere and the mantle).
- CQ-01: 10 SUBJECT rows, counts and observations on the instrument network and the datasets.

So the change under test did what the hypothesis said: the same model attached its quantities and claims to named things once the pack had a place for it, and a value-blind query reached them through the subject. The falsifier did not fire.

What the data also says: the ENTITY kind is a flood. It returns every admitted record of every type in a question's set, 1,061 rows that reach the question through nothing, and it makes the review six times run-04's. The elegant correction is a removal, not a rule: a source-asserted record reaches a question only through its subject (SUBJECT kind), and the ENTITY kind is kept for types that carry no subject (structures, campaigns, instruments). That halves the rows and lets the coverage census bite, because an unattached observation then reaches nothing, which is the honest outcome.

Review: four fresh Opus sessions, one per question, merged into one record and validated as one; recorded as a deviation from "one session judges every row", forced by 1,466 rows. Candidates for iteration 2, to be chosen by the RCA once the review is in: (a) the ENTITY-kind removal above (harness); (b) the naming sentence (skill); (c) INVALID_RANGE naming the bound scalar ranges (Core diagnostic) with the skill's range note corrected.

### Iteration 1 closed (06:55Z): review in, RCA written, iteration 2 decided

Review merged from four sessions and validated: R, P, R, P; 1,450 SUPPORTED, 16 PARTIAL; all 1,162 digests DIGEST_OK; every row local. Record at a468a1d, E-0143. RCA at `handover/2026-09-05-v43-rca.md`. Iteration 2: Core-14 (modality single source of truth; INVALID_RANGE names the bound ranges and the skill's range note corrected; the skill says what a name is) and harness v4.4 for run-10 (ENTITY kind only for types without a subject, validated offline: 630 rows, 618 SUPPORTED, 12 PARTIAL). Dispatched both in parallel; run-10 pins after Core-14.

## Loop iteration 2: run-10 (v4.4, Opus 5), launched 2026-09-05T07:38Z at 2026244 (E-0145)

Change under test: a record's modality has one source of truth, its formalizing assertion (Core-14, MODALITY_NOT_ASSERTED, decision 19, one skill sentence). Riding along with separately measurable effects and no semantic change: the INVALID_RANGE refusal names the range that failed and the ranges that bind, the skill's range note corrected; the skill says what a name is. Harness: the ENTITY kind restricted to types without a subject (validated offline on run-09's judged rows: 630 rows, 618 SUPPORTED, 12 PARTIAL). Expected: modality drift 0; no INVALID_RANGE return; no SUBJECT_NOT_NAMED return; about 600 rows over two review sessions; responsiveness at least run-09's R, P, R, P. Falsifiers: drift above 0; either return recurring; SUBJECT rows losing responsiveness.

A slip of mine, recorded: the pin commit d061883 went in with one red paper test because my command chain did not stop on the gate; fixed in b6f16dd four minutes later (E-0145 named the short commit). The chain now writes the gate line to a file and commits only if it reads "passed" and not "failed".

### Iteration 2, gate and first runner attempt (07:54Z to 08:25Z)

Gate: accepted at attempt 01, 5,408 facts, 41 entity types, 7 subject-bearing types, 4 relation types; the producer's log says it avoided `date` and `uri` because the compiler refuses them. Expected effect of the range clarification: held (no INVALID_RANGE return; run-04 and run-09 each spent one).

Runner attempt 1: SUBJECT_NOT_NAMED over 35 of 130 subjects (95 pass; run-09's first attempt: 98 refused of 129). The names are now the source's designators, mean twelve characters, so the naming sentence held. Classified by script: 14 genuinely unnamed in their sentence (the inference class run-09's producer dropped); 7 aliases ("Mid-Atlantic Ridge" named, "the MAR" written); 8 partial names ("Oceanic crust" named, "crust" written); 6 whitespace artefacts ("CO2" named, "CO 2" printed by the text layer). Twenty-one of thirty-five are the check being more literal than names are. Returned as structural diagnostic 1 of 2.

Population before the repair: 346 assertions, all 186 blocks, 420 entities, 2 events, 11 relations (run-09: 219), 130 subjects of 235, 45 gaps (RELATION_ABSENT 21: contributions by initialism the producer would not resolve). Relations fell by twenty-fold against run-09; the RCA will say whether the subject element absorbed them (an observation about RC2 no longer needs a relation) or whether the producer under-derived.

Candidate for iteration 3, one idea: the subject check matches a name the way the reading spells it, any of the entity's names (its `name` or its `tags`, which every Entity already carries) with whitespace ignored. No new slot, no new reason; one comparison and one skill clause. It would clear 21 of today's 35 and leave the 14 that are inference, which is the honest residue.

### Iteration 2, admitted and frozen (08:32Z to 08:40Z); measurements before the review

Run-10 admitted at runner attempt 2 after the naming repair (5 renames to the repeated form, 16 subjects dropped with typed gaps, 2 re-pointed): 420 entities, 2 events, 11 relations, 433 traced, all 186 blocks, 48 gaps, 2 of 11 relations non-local, largest hub 7, subject coverage 114 of 235. Frozen at 0d73afd, E-0146. The v4 binding returned 552 rows (51, 164, 165, 172): 378 SUBJECT, 158 ENTITY on non-subject types, 16 RELATION. Two review sessions dispatched (215 and 337 rows).

Measured from the artifacts:
- Modality drift, the change under test: 0 of 174 records (run-09: 20 of 212). The falsifier did not fire. The adapter's MODALITY_NOT_ASSERTED never had to; the producer's own validator carried the rule from the skill sentence.
- The INVALID_RANGE clarification: no first-attempt refusal (run-04 and run-09 each spent one). The name sentence: refusals fell from 98 of 129 to 35 of 130, and the 35 are a different class.
- Relations, 219 to 11: 189 of run-09's were CONTRIBUTED_TO from reference-list author strings (Person to BibliographicSource, 185) and 8 FUNDED_BY; the geometry relations were 18 against run-10's 10. Run-10 did not model reference authorship as relations and recorded contributions by initialism as gaps. The science content moved into subjects: RidgeSegment 32, LithosphericUnit 18, LithosphericBoundary 12, SpreadingRidge 9, Melt 5, ChemicalSpecies 5 as subject types. No regression of the question-bearing structure; a different choice on the reference list.

Iteration 3, decided: the subject check matches a name the way the reading spells it, the entity's `name` or any of its `tags` (an existing root slot), with whitespace ignored; one skill clause says that the source's other forms of a name go in `tags`. Evidence: 21 of run-10's 35 refused subjects were aliases, partial names or whitespace artefacts. No new slot, no new reason. Harness for run-11: run-10's with no delta.

A larger candidate, from the producer's own validator: 251 of 435 records carry a `name` that occurs in no statement formalizing it, almost all of them labels the producer minted for claims and observations. A source-asserted record's identity is its assertion (locator and digest); a minted label is invention the derivation rule cannot see. The removal would be: source-asserted records carry no `name`, and rows show the quantity, the value and the subject instead. Not this iteration; it changes what every reviewer reads. Recorded for Luis.

### Iteration 2 closed (09:00Z): review in, RCA written, iteration 3 in flight

Review merged from two sessions and validated: P, R, R, P; 542 SUPPORTED, 10 PARTIAL; all 249 digests DIGEST_OK. Record at ceb3271, E-0148. RCA at `handover/2026-09-05-v44-rca.md`: the modality change held (0 of 174); the ENTITY restriction cut the review 59 per cent and priced the 51 per cent of source-asserted records without a subject in two PARTIAL verdicts. Two review-surface defects for the harness after run-11: the locality token scoped to RELATION rows only; hedged categorical values (fault status) have no modality slot. Core-15 and the run-11 harness were dispatched before the review closed; run-11 pins after Core-15.

## Loop iteration 3: run-11 (v4.5, Opus 5), launched 2026-09-05T09:18Z at 9d789f2 (E-0149)

Change under test: the subject check matches a name the way the reading spells it, the entity's `name` or any of its `tags`, whitespace ignored (Core-15, decision 20, OVR-000410; one skill clause). Harness unchanged from run-10 (v4.5 is a version name for a change list one entry longer). Expected: subject refusals near the fourteen that were genuinely unnamed in run-10; coverage above 114 of 235; CQ-01 and CQ-04 regaining their missing semantics if the producer attaches them. Falsifiers: refusals staying near 35 with alias or whitespace classes among them; coverage not rising; the review cost rising above run-10's without more responsive questions.

Queued for the harness after run-11, from the run-10 RCA: the locality token scoped to RELATION rows only; a modality on categorical source-asserted values (fault status), which is decision 15's idea for enums.

### Iteration 3, admitted and frozen (10:08Z to 10:15Z); measurements before the review

Run-11 admitted at runner attempt 1 with no return at either stage, the first cell to do so: 401 entities, 1 event, 30 relations, 432 traced, all 186 blocks, 29 gaps, 1 of 30 relations non-local, largest hub 9. Frozen at 6adaab5, E-0150. The binding returned 457 rows (60, 123, 145, 129); the three science questions share the same 86 SUBJECT rows because the surface has one feature type. Two review sessions dispatched (183 and 274 rows).

Measured:
- The change under test removed the return: no SUBJECT_NOT_NAMED refusal; 27 entities carry tags (MAR for Mid-Atlantic Ridge, Romanche transform for Romanche TF, ridge-transform intersection for RTI, and so on).
- The falsifier on coverage fired: subject coverage 91 of 248 (37 per cent) against run-10's 114 of 235 (49 per cent). The denominator grew (143 observations to run-10's 141 across three subtypes, 102 claims to 89) and the numerator fell.
- Computed from the file: 77 source-asserted records with no subject whose formalizing sentence nonetheless contains the name or a tag of a capture entity (the mantle, the MAR, the RTI, the OCC). The check would have accepted every one. The producer's own validator enforced the check and treated attachment itself as optional; the skill's "carries that thing as its subject" was read as permission, not duty. A rule stated as a duty with no gate behaves as a preference, again.

Iteration 4, decided: projected subject. When a source-asserted record's `subject` is unset and exactly one entity of the capture is named (name or tag, whitespace ignored) in a statement that formalizes the record, the adapter sets the subject and records the derivation as projected from that assertion; the census reports proposed, projected, ambiguous (more than one entity named) and unnamed; a producer-set subject still passes the name check. This is Luis's anchors point in its projected form: what the sentence says is derived by the compiler, not left to the producer's diligence. One skill sentence saying so and telling the producer to set the subject only where the sentence names more than one entity. Expected: coverage above 60 per cent with the same or fewer producer tokens; the projected subjects judged SUPPORTED at review at the same rate as proposed ones. Falsifier: projected subjects judged wrong more often than proposed ones, which would mean a sentence naming one entity is not enough to know what it is about.

Harness for run-12: run-11's plus the review task v4, the locality token scoped to RELATION rows (the run-10 RCA's first review-surface debt); the binder unchanged.

Ledger wart for Luis: governance entry timestamps run ahead of the wall clock since OVR-000409 (recorded 11:20Z at about 07:30Z), and the monotonic rule now pushes each entry further into the future.

### Iteration 3 closed (10:32Z): review in, RCA written

Review merged from two sessions: R, R, R, P, the matrix's best; 450 SUPPORTED, 7 PARTIAL; all 262 digests DIGEST_OK. Record at 3614a22, E-0151. RCA at `handover/2026-09-05-v45-rca.md`. The return is gone; coverage fell; responsiveness rose because the producer attached the instrument counts. Four harness defects queued from the review: the empty relation projection (a v3 defect the reviewers of run-09 and run-10 did not report), tags not projected, subtype duplication, identical rows judged three times. Iteration 4 (Core-16 projected subject; run-12 with task v4) was dispatched before the review closed.

Correction (10:40Z): E-0151 and the v4.5 RCA repeated a reviewer's report that relation rows project an empty relation record. Checked against the frozen query results: false; every relation row carries `relation_type`. Corrected in the RCA and by E-0152. Same error class as E-0134: a reviewer's or agent's claim written into the record before one script checked it. The rule I hold myself to from here: no defect enters an entry without the line of script that shows it.

## Loop iteration 4: run-12 (v4.6, Opus 5), launched 2026-09-05T11:10Z at 90abc79 (E-0154)

Change under test: the projected subject (Core-16, decision 21, OVR-000411). When a source-asserted record's subject is unset and exactly one capture entity is named in a formalizing sentence, the adapter sets it and records the derivation as projected; the census reports proposed, projected, ambiguous, unnamed; nothing refuses. Harness: review task v4 (the locality token only on RELATION rows). Expected: coverage above run-11's 91 of 248 by roughly the 77 attachable records, with the producer's own tokens flat or lower; projected subjects judged SUPPORTED at the rate of proposed ones. Falsifiers: coverage not rising (the producer's sentences name nothing the adapter can use); projected subjects judged wrong more often than proposed ones; a fall in responsiveness.

The harness queue after run-12, from run-11's review: tags projected beside the name in SUBJECT rows; a binding that does not list a type and its subtype in one set; identical rows across questions judged once.

### Iteration 4, gate and first runner attempt (11:25Z to 11:57Z)

Gate: accepted at attempt 01, 4,710 facts, 37 entity types, 4 subject-bearing types. Population: 362 assertions over all 186 blocks (4 nothing-assertable), 333 records (310 entities, 1 event, 22 relations), 62 gaps of which 52 are MODALITY_NOT_EXPRESSIBLE (a closed-set kind the earlier producers did not use); 75 explicit subjects. Runner attempt 1 refused on two subjects (claims naming RC2 where their sentences do not), returned as structural diagnostic 1 of 2.

The finding that matters, from the producer's own report before any runner ran: knowing the adapter projects a subject when a sentence names exactly one capture entity, it enumerated every record that would be projected and found eight where the one entity named is a tool or a model (ZMAP for a b-value, the thermal model for expected depths, the solubility model for saturation conditions, the OCC for a transect half-width), not what the record is about. It did not set the right subject on those; it narrowed the formalizing span so the sentence names nothing, and reports six projections left, all correct by its reading, with 143 records that "could" carry a subject. So the falsifier fires before the review: "exactly one entity named" is not sufficient to know what a sentence is about, because sentences name their instruments and models as often as their subjects; and a projection rule the producer knows about induces evidence-narrowing to avoid it, which is worse than an unset subject. Coverage gain from projection: six records.

Reading, for iteration 5. Two honest options, both removals. (a) Withdraw projection and keep the census only: the subject stays the producer's, proposed or unset, and the count of attachable-but-unset records is reported. (b) Keep projection but restrict the candidate entities to types that can be subjects at all: the entities named as tools and models are Instrument, Method, SoftwareTool, NumericalModel; a pack-level marker of which entity types are "about-able" (features, samples, materials, agents) would exclude them; that is a new declaration, which is more, not less. Or (c), the one that removes a rule: the producer's own explicit subject is the only subject, the adapter checks it, and the attachable-but-unset count becomes a review duty (the reviewer names the records that should have carried a subject). I lean to (a) with the census, because the loop has shown three times that a rule the producer can see it will play around, and a report the producer never sees it cannot. Decide after the review, on the six projected rows' support.

### Iteration 4, admitted and frozen (12:00Z to 12:10Z); iteration 5 decided before the review

Run-12 admitted at runner attempt 2 after a four-record provenance repair: 310 entities, 1 event, 22 relations, 333 traced, all 186 blocks, 62 gaps (52 MODALITY_NOT_EXPRESSIBLE). Subject coverage 90 of 143: 75 proposed, 15 projected, 5 ambiguous, 48 unnamed. Frozen at 891e2c6, E-0155. Rows 408 (48, 117, 131, 112). Two review sessions dispatched under task v4, told to judge a SUBJECT row on whether the block supports that the record is about the subject shown, not only that the name occurs.

The fifteen projected subjects, read from the plan's PROJECTED derivations: thirteen wrong (records attached to HypoDD, SEISAN, NonLinLoc, the OCC, the RTI, the MAR, the OBS array as their instruments, databases or reference frames), two plausible. The falsifier fired before the review, by reading; the review cannot see it, since a projected subject occurs in its block by construction. Two lessons, both about mechanism: a sentence that names one entity names its tool as often as its subject, so "named" is not "about"; and a projection rule the producer knows about, it works around by narrowing the sentence, trading evidence for the absence of a wrong subject.

Iteration 5, decided: withdraw projection, keep the census (Core-17, decision 22): the adapter sets nothing; the census reports proposed, attachable (exactly one entity named, subject unset), ambiguous, unnamed; the check on a proposed subject stands. This is the second withdrawal of the loop (the first was the ENTITY flood) and the second time a report beat a rule. Harness for run-13: run-12's plus the subject's tags projected beside its name in SUBJECT rows, so the review's subject-in-block token stops flagging abbreviations. Expected: coverage back near run-11's proposed share, no wrong subjects, and the attachable count in the census as the honest measure of what the producer left. Falsifier: none that a cell can fire; the change removes a mechanism, and the test is that nothing it removed was worth keeping, which the fifteen already showed.

The loop's tally so far: four iterations, two additions that held (the subject element, one source of truth for modality), one clarification that held (ranges, names), one alias change that held on the return and failed on coverage, one projection that failed, two removals. The two removals and the two clarifications cost the least and taught the most.

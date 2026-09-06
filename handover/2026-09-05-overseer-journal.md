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

### Iteration 4 closed (12:25Z): review in, RCA written

Review merged from two sessions: P, R, R, P; 381 SUPPORTED, 25 PARTIAL, 2 UNSUPPORTED; rows on projected records 18 of 26 PARTIAL against 9 of 382 elsewhere. Record at dae0965, E-0157. RCA at `handover/2026-09-05-v46-rca.md`, with the loop's earned principle: check the output, never steer the producer. Iteration 5 (Core-17 withdrawal, run-13 with tags in SUBJECT rows) was dispatched before the review closed.

## Loop iteration 5: run-13 (v4.7, Opus 5), launched 2026-09-05T12:57Z at 12a04a9 (E-0158)

Change under test: the withdrawal of the projected subject (Core-17, decision 22, OVR-000412). The adapter derives no subject; the producer's explicit subject is the only subject, still held by the Core-15 name-or-tag check; the census reports proposed, attachable, ambiguous, unnamed. The population compiler is byte-identical to its pre-Core-16 revision, so a plan carrying `origin` is refused as MALFORMED_PLAN; run-12's retained plan carries `origin: PROJECTED` and stays as recorded. Harness: run-12's plus the subject's tags projected beside its name in SUBJECT rows (three substitutions in `native_query.py`, executor not binder), so the review's subject-in-block token stops flagging abbreviations. Expected: coverage near run-11's proposed share, no wrong subject by projection, the attachable count as the honest measure of what the producer left. Falsifier: none a cell can fire for a removal; run-12's 18 of 26 PARTIAL on projected rows is the evidence the removal rests on.

Two corrections recorded at the opening, both from Paper-15 and Core-17's reports and checked against the files:
- Run-12's frozen contract records `census_keys_at_pin: []` at a commit where all four Core-16 keys were declared: its `pin.py` scanned the census function's body for literals, and the adapter names outcomes by module constant. Run-12 is not edited; run-13's `pin.py` resolves the adapter's `_SUBJECT_OUTCOMES` tuple by AST and refuses without it. Stated in E-0156 and asserted in run-13's test that reads both side by side.
- E-0156's pin at 2290245 read the governance head as OVR-000411 because Core-17's entry was still being written; re-pinned at 12a04a9 with head OVR-000412 (E-0158, commit 8aa8072).

For Luis: decision 21 is left as written and withdrawn by 22, append-only; if he wants 21 marked in place, one line does it.

Harness queue after run-13, unchanged: no type and its subtype in one set; identical rows across questions judged once; hedged categorical values need a modality; a skill census paragraph naming the census counts.

### Iteration 5, gate through freeze (13:12Z to 14:15Z)

Gate: accepted at attempt 01, 4,943 facts, 40 entity types, 2 event types, 3 relation types, 7 subject-bearing types (SeismicEvent among them: the producer put the magnitude on the event through Quantified because the research pack's subject ranges on Entity). Citations: four of six URLs fetched and their terms found; the OGC GeoSciML page and quakeml.org unreachable from this environment on transport, each standard confirmed at its other home. Population: 374 assertions over 184 of 186 blocks, 469 records (440, 1, 28), 17 gaps (13 RELATION_ABSENT, 2 INTERVAL, 1 REQUIRED_FIELD, 1 TYPE_ABSENT). Admitted at runner attempt 1: no return at either stage, the second such cell after run-11. Census: 357 fully, 10 partly, 7 unformalized; 5 of 28 relations non-local; largest hub 8. Subject coverage 111 of 269, all proposed: 33 attachable, 49 ambiguous, 76 unnamed. Query: 3,013 cases, 515 rows (63, 127, 176, 149; 164 ENTITY, 22 RELATION, 329 SUBJECT) over 198 witnesses. Frozen, E-0159; ladder max 40, no leak. Producer 383,284 tokens (168,092 ontology, 215,192 population), against run-12's 374,055 with a correction. Two review sessions dispatched 14:15Z under task v4 with the aboutness instruction, tags counted as the subject occurring.

Read against the expectation: coverage near run-11's proposed share held (41 per cent against 37), with nothing derived and so nothing wrong by derivation; the attachable count is now a number the census produces rather than one I count by reading. Two producer findings recorded as gaps rather than worked around: no slot for a grant identifier (TYPE_ABSENT), no citation predicate for the 79 cited works (RELATION_ABSENT). The producer typed the four hypotheses' dispositions on STATED assertions, which the Core-12 evaluative check requires; run-04 could not have passed that check. One residual the producer named: `capture.attribution.date` is the year alone; the adapter accepted it.

### Iteration 5, RCA before the review (14:20Z to 14:45Z): the check had no word boundary

Reading run-13's 33 attachable records one by one against the entity each names: 14 name a tool, model or instrument (the OBS network, SEISAN, NonLinLoc, ZMAP, the velocity model, the Wadati method) and of the 17 naming a feature several are not what the record is about (a mean location error "about" the RTI, a supplementary-data claim "about" the LAB). The LAB one gave the game away: the tag LAB sits inside "available". The Core-15 comparison strips whitespace and tests substring; it has no word boundary. Measured by script over the retained captures of runs 11 to 13 (`rca13_letter.py`, rule: the form's non-space characters in order with any whitespace between, case-insensitive, not adjacent to a letter on either side): eight of run-12's fifteen projections were in-word matches of three-letter tags (RTI in "vertical" and "portion", OCC in "occur", MAR in "mark", OBS in "observations"); of the seven real matches three attach a record to its software, one is marginal, three plausible. Run-13's census under the rule: 26 attachable, 43 ambiguous, 89 unnamed against 33, 49, 76. Producer-set subjects refused under the rule: run-11 one ("axial valley" against "valleyﬂoor", a ligature glued by the text layer), run-12 none, run-13 two ("velocity model" against "velocity models"). Corrected in the v4.6 RCA and by E-0160: the subjects were wrong as read; the cause was mostly the check, and "a sentence names its tool as often as its subject" rests on three or four cases, not thirteen. Same class as E-0134 and E-0152: a count read into the record before the mechanism was tested; this time the script came second, and it will come first.

Iteration 6, decided: Core-18, a name occurs as a word. One predicate at both sites (the SUBJECT_NOT_NAMED check and the census), no new declaration; digits and punctuation are boundaries so the text layer's glued citation numbers still name; an inflected or glued form costs the producer a tag. Skill sentence, decision 23, RED with RTI-in-vertical, lithosphere13, R C 2 and an in-word census case. Harness for run-14: run-13's, no delta (Paper-16, E-0162). Expected: attachable and ambiguous fall to the word-bounded counts; a subject matched only inside a word is refused; returns for inflected forms are the cost and the falsifier is a return for a form a reader calls a word. The loop's tally: six iterations, three clarifications of an existing check (ranges and names, tags, words), two removals, two additions that held, one alias change and one projection that failed. The clarifications keep finding the same thing: the rule was right and the comparison was loose.

### Iteration 5 closed (14:50Z): review in, RCA written

Review merged from two sessions: R, R, R, R, the matrix's first cell responsive on every question; 497 SUPPORTED, 18 PARTIAL, 0 UNSUPPORTED; every digest DIGEST_OK. Record E-0161. RCA at `handover/2026-09-05-v47-rca.md`. The eighteen PARTIALs are fifteen aboutness findings on producer-set subjects (figure furniture, direction markers, isotherm provenance), two missing qualifiers, one semantic misread. Harness debts from the review, reordered: rows project the record's own type and identical rows are one row (subtype re-projection hides three digests and duplicates 30 of 127 rows in CQ-02); OPEN_LOWER_BOUND strictness and NEGATED on hedges; clipped statements. Iteration 6 (Core-18 word-bounded names; Paper-16 run-14 with no harness delta) was dispatched before the review closed, on the script evidence alone.

Luis, 14:35Z, for the loop after this one (captured in `paper-v4/paper-master-plan.md` 1.3.2 items 9 to 11, not acted on now): more competency questions and model-split cells; an experiment with adversarial Haiku pairs per reading block holding a whole-paper summary and the population surface as a tool; the small-shop baseline recreated on current Core with more questions.

## Loop iteration 6: run-14 (v4.8, Opus 5), launched 2026-09-05T15:24Z at dc52547 (E-0163)

Change under test: Core-18, a name occurs as a word (decision 23, OVR-000413). One predicate, `_occurs_as_word`, at the SUBJECT_NOT_NAMED check and in the census: the form's non-whitespace characters in order with any whitespace between, case-folded both sides, not adjacent to a letter on either side; the whitespace-free substring helper is gone. The skill says an inflected or glued form goes in tags. Harness: run-13's, no delta (Paper-16, E-0162; 875 active tests). Expected: attachable and ambiguous at the word-bounded counts; a subject matched only inside a word refused; inflected forms cost a tag (two returns in one on run-13's capture). Falsifier: a return for a form a reader calls a word.

Core-18's own check against the RCA cases, from its report: RTI/vertical, OCC/occur, MAR/primary, OBS/observations, LAB/available refuse; "an OCC", "the MAR", lithosphere13, thermal model31, "R C 2", "CO 2", "P- 7" match; "velocity models" and "valleyﬂoor" refuse, the stated cost. Casefold kept over IGNORECASE so decision 20's case semantics stand byte for byte.

### Iteration 6, gate (15:40Z)

Accepted at attempt 01, 3,482 facts, 21 entity types, 2 event types, 4 relation types, 4 subject-bearing types. A flatter ontology than run-13's: one GeologicFeature class with a twenty-value kind enum where run-13 declared fourteen feature subtypes; a SeismicitySet entity for a body of seismicity; GeologicEvent carrying magnitude as slots and bearing no subject. Seven citations, all confirmed (RO's "overlaps" by IRI through OLS added to the earlier checks); none fabricated. Type sets translated to the flat surface (8, 5, 12, 7 types), SeismicitySet added where the question is about the earthquake population, GeologicEvent left out as the event type was in runs 12 and 13; 1,254 cases (19 ENTITY, 1,128 RELATION, 107 SUBJECT). Phase two dispatched 15:41Z.

Two producer observations, recorded in the launch log and not acted on: this session ran a `malleus-inquisitor` console script it found on the ambient PATH (it failed on import, so nothing reached it; run-13's producer declined to probe), and it asked the parent three questions at ONTOLOGY_READY (compass orientations as numerals, whether the licence permits filling Claim.statement, reference-list depth). The protocol answers none; the phase-two message is the fixed one. Both belong in the RCA under producer variance on one skill: the same skill, two sessions, one probes and asks, one neither.

### Iteration 6, population and first runner attempt (16:09Z to 16:18Z)

Population: 344 assertions over 184 of 186 blocks, 461 records (412 entities, 1 event, 48 relations), 27 gaps; 132 explicit subjects of 203 subject-bearing records; the reference list captured as 84 bibliographic works; twelve relations the producer removed under the "one sentence names both endpoints" rule and recorded as RELATION_ABSENT (the four PART_OF links whose parent the sentence calls "It", five contributor credits that name the person and not the work, four REPORTED_BY links whose reference entry never names the tool). The producer took three decisions it had asked the parent about (compass bearings as TYPE_ABSENT gaps, Claim.statement empty under the licence, references as works) and said so. Its own report predicted one SUBJECT_NOT_NAMED: the text layer prints "the melt" as "t h em e l t", so no form of feature:melt occurs as a word.

Runner attempt 1 refused, seven defects in one aggregated diagnostic: six MODALITY_NOT_ASSERTED (records typed STATED whose formalizing assertion is MEASURED, HYPOTHESISED or NEGATED) and the predicted SUBJECT_NOT_NAMED. Returned as structural diagnostic 1 of 2 at 16:18Z. Reading: the modality six are this producer's own check missing Core-14's equality, which runs 12 and 13 satisfied at the first attempt; the subject one is the word rule paying exactly the cost decision 23 names, on text-layer damage, and the skill's remedy is a tag for the glued form. The falsifier ("a return for a form a reader calls a word") does not fire on the reading's bytes: no reader of "t h em e l t" would call "melt" a word of it; the reader of the PDF would, and that gap is malleus-ocr's, declared in the paper's limitations.

### Iteration 6, admitted and frozen (16:21Z to 16:30Z)

Run-14 admitted at runner attempt 2 after the producer split four two-modality sentences, relabelled two records and tagged the glued form "themelt": 412 entities, 1 event, 48 relations, 461 traced, all 186 blocks, 27 gaps (14 RELATION_ABSENT, 12 TYPE_ABSENT). Subject coverage 132 of 203 proposed (65 per cent against run-13's 41), 17 attachable, 21 ambiguous, 33 unnamed under the word rule. Frozen, E-0164; ladder max 0. Rows 919 (190, 195, 323, 211): the flat surface's BibliographicWork carries the 84 references and sits in two sets, which is 168 ENTITY rows of reference works the questions did not ask for, an evaluator's translation cost recorded in the type-set note. Producer 439,761 tokens (182,760 ontology, 239,145 population, 17,856 correction). Two review sessions dispatched 16:30Z under task v4, with one sentence added for the bibliographic ENTITY rows.

Read against the expectation: attachable and ambiguous fell (17 and 21 against run-13's 33 and 49, or 26 and 43 under the word rule on run-13's capture; different captures, so the comparison is loose); the one subject refusal was the named cost, on text-layer damage; the falsifier did not fire. The six modality defects are producer variance, not the change under test. Note for the RCA: this producer's own validator lacked the modality equality until the return; run-13's had it. Same skill, two sessions, different pre-flight sets; what the skill does not list as a check, a producer may or may not run.

### Iteration 6, RCA before the review (16:45Z): what the rows repeat

Census recount under the word rule matches the adapter exactly (17 attachable, 21 ambiguous), so Core-18's predicate and the RCA script agree. Of the 17 attachable, 10 name the producer's catch-all seismicity set "earthquakes" and 4 name a tool (ZMAP twice, the OBS network, the Wadati method); named is not about, third cell running. Modalities: 22 HYPOTHESISED and 5 NEGATED after the split, against run-13's 10 and 6; no MODALITY_NOT_EXPRESSIBLE gap in either, against run-12's 52.

Row duplication, measured on the frozen query results (witness = kind plus record ids): run-13's 515 rows carry 152 repeats of a witness inside one question (93 identical projections; 59 the same record projected with a parent type's fewer fields, which is where the reviewers found digests hidden) and 165 witnesses already returned by an earlier question. Run-14's 919 carry 44 within-question re-projections and 484 cross-question repeats: the 84 bibliographic works twice, the 40 features three times, the 44 agents once, catalogues returned whole by every question whose type set names their type. The within-question part is the executor's: one row per distinct witness per question, projected with the record's own type's fields, is a removal (Paper-17 candidate, harness only). The cross-question part is the evaluator's translation on a flat surface (DataResource became BibliographicWork, which here holds the references), a judgement at acceptance and not a harness matter; the note in `query-type-sets.note.json` says so. Iteration 7's change is decided after the review.

### Iteration 6 closed (16:50Z): review in, RCA written; iteration 7 decided

Review merged from two sessions: P, R, R, P; 897 SUPPORTED, 22 PARTIAL, 0 UNSUPPORTED; every digest DIGEST_OK. Record E-0165. RCA at `handover/2026-09-05-v48-rca.md`. The change held on all three expectations and cost one return of the named kind. The two PARTIAL questions are the producer's modelling (the network never a record) and the empty claim statement (extensional stress only in a statement the projection drops; run-13's producer had put it in the claim's name). That last one is for Luis: with statements empty under the licence, a claim row's content is the label the producer minted, and responsiveness on CQ-04 turns on naming.

Iteration 7, decided: harness only, Core unchanged. The executor emits one row per distinct witness per question, projected with the record's own type (Paper-17, run-15, v4.9); type sets at acceptance name no catalogue type the question does not ask for. A removal, with the falsifier that a row count falls by anything other than the within-question repeats. Dispatched 16:49Z.

Tally after six iterations: three clarifications of an existing check (ranges and names, tags, words), two removals (the ENTITY flood, projection), two additions that held (the subject element, one source of truth for modality), one projection that failed. Every clarification found the rule right and the comparison loose. The cells now return at the runner for producer-side reasons only (modality defaults, a glued form), and the review finds no UNSUPPORTED row two cells running.

## Loop iteration 7: run-15 (v4.9, Opus 5), launched 2026-09-05T17:40Z at dc52547 (E-0166, E-0167)

Change under test: the executor emits one row per distinct witness per question, projected with the record's own type (Paper-17; `case_ordinals`, query-result schema v3); Core unchanged at the v4.8 coordinate, the skill included. On the frozen results the removal takes run-13 from 515 rows to 363 and run-14 from 919 to 875, witnesses unchanged, and gives three ratio records back the digest a parent-type projection hid. Paper-17's two decisions beyond the brief: a witness whose own type the binding never names is a refusal, not a fallback (it fires on neither frozen cell); the subject side of a SUBJECT row projects through its own type too. Expected: rows fall by the within-question repeats and nothing else. Falsifier: a count that falls by anything else, or a refusal for a type the binding does not project. Type sets at acceptance: no catalogue type the question does not ask for.

### Iteration 7, gate refusal at attempt 01 (17:52Z)

Refused at contract compilation: IMPORT_READER_REFUSED, cause chain REJECTED_SOURCE, the schema root carries `default_prefix`, a root field the LinkML adapter rejects. Runs 13 and 14 wrote neither `prefixes` nor `default_prefix`; this producer wrote both, checked grounding blocks, ranges and references by hand, and did not check the root field set. Returned as diagnostic 1 of 2 at 17:53Z with the full cause chain (the gate surfaces it since v4.2). Producer variance again: three sessions on one skill, three different pre-flight sets. This producer also took the honest form on three grounding blocks (none_found with a search note naming GeoSciML, QuakeML, GeoSPARQL as recalled and unverified) where runs 13 and 14 cited URLs from recall; its two citations are SOSA/SSN and PROV-O plus DCMI Terms.

### Iteration 7, gate (17:54Z)

Accepted at attempt 02, attempt 01 minus its `default_prefix` line: 3,221 facts, 20 entity types, 2 event types, 3 relation types, 4 subject-bearing types. Flatter again: GeologicFeature with a string `feature_kind`, EarthMaterial, ResearchAgent, BibliographicSource (a Source subtype for the references), SoftwareTool as a Method subtype, CountObservation and RatioObservation, SeismicEvent with the magnitude as slots. Three citations, all verified, none fabricated; three blocks in the none_found form. Type sets with the catalogue lesson applied: ResearchAgent and BibliographicSource in no set (6, 4, 10, 7 types), 709 cases (14 ENTITY, 603 RELATION, 92 SUBJECT) against run-14's 1,254. Phase two dispatched 17:56Z.

### Iteration 7, admitted and frozen (18:24Z to 18:35Z)

Run-15 admitted at runner attempt 1: 315 entities, 1 event, 35 relations, 351 traced, all 186 blocks, 17 gaps (11 TYPE_ABSENT). No non-local relation, the first cell with none. Subject coverage 80 of 144 proposed (56 per cent), 20 attachable, 18 ambiguous, 26 unnamed. Query under the v3 executor: 709 cases, 433 rows (28, 104, 154, 147; 192 ENTITY, 217 SUBJECT, 24 RELATION) over 160 witnesses, 21 rows merged from more than one case, no witness twice in a question: the change held. Frozen, E-0168 (139e2ab); ladder max 0. Producer 351,253 tokens, the cheapest of the three Opus cells at v4.7 to v4.9 (383,284; 439,761), with one return at the gate and none at the runner. Two review sessions dispatched 18:36Z.

The freeze template caught its own gap this time: the phase-two block missing from the launch log, fixed from the transcript. The three producers' pre-flight sets, for the RCA: run-13 built a byte slicer and a full validator and asked nothing; run-14 probed the ambient PATH, asked three questions, missed the modality equality; run-15 refused to cite from recall, asked nothing, missed the root-field set, and caught its own reference-parser error before writing. Same skill, three sessions.

### Iteration 7, RCA before the review (18:40Z)

Census recount under the word rule: 18 attachable and 18 ambiguous by script against the adapter's 20 and 18 (the script's candidate set differs by two records); of the 18, 14 name a tool or model (the thermal model twice, SEISAN, NonLinLoc, ZMAP twice, the OBS network three times, the Wadati method, the first-motion method twice, model 5) and 4 a feature. Fourth cell, same shape: a sentence naming one entity names its instrument more often than its subject once the producer has set the subjects it can. Modalities: 44 MEASURED, 31 CALCULATED, 17 HYPOTHESISED, 12 NEGATED, the widest spread of the three Opus cells at v4.7 to v4.9 (run-13: 21, 11, 10, 6). Gaps: 11 TYPE_ABSENT (funding identifiers, a magnitude formula, compass bearings), 3 RELATION_ABSENT (funding, the closed ResearchRelationType has no funding predicate), 3 INTERVAL. The 79 references are unnamed BibliographicSource records, which the type sets do not reach.

Rows: 433 for 162 distinct witnesses; 271 rows are a witness a later question also returns (the 33 features three times, the 12 methods and 8 tools three times, the 12 materials twice, and the observation SUBJECT rows in every question whose set holds their subject's type). With the catalogue lesson applied the cross-question repeats are now structural to type-only binding with overlapping sets, not an evaluator's translation. A judgement is a property of the row and its block, not of the question, so one judgement per distinct witness distributed to every question's rows would cut the review to 162 rows here and 391 in run-14 with no information lost; that is a review-protocol change (v3), the candidate for iteration 8, and Luis's to rule on since it changes what the paper calls a review.

### Iteration 7 closed (18:55Z): review in, RCA written; the loop steps back

Review merged from two sessions: P, R, P, P; 427 SUPPORTED, 6 PARTIAL, 0 UNSUPPORTED, the lowest PARTIAL share of any cell; every digest DIGEST_OK; every relation local. Record E-0169. RCA at `handover/2026-09-05-v49-rca.md`. The executor change held exactly. The validator refused the v3 schema at the merge (Paper-17 bumped it without touching review.py); two lines fixed, recorded.

Reading the three Opus cells at the stable Core together: no UNSUPPORTED row in 1,867; the returns are producer-side; the responsiveness movement is producer modelling, reviewer threshold, and two design properties of the type-only binding (subject-less records unreachable; nested type sets give nested answers). No Core defect in three cells. The honest next step is not a Core change: Luis's rulings (Claim.statement, the reviewers' lines, review protocol v3) and the matrix cells at v4.9. Iteration 8, proposed: run-16, Sonnet 5 at v4.9, same harness with the model field moved, as the first matrix cell on the settled protocol.

## Matrix cell: run-16 (v4.9, Sonnet 5), launched 2026-09-05T19:26Z at dc52547 (E-0170, E-0171)

Not a loop iteration: no change under test. Run-15's harness byte for byte with the run id and the producer's model moved (Sonnet 5, `claude-sonnet-5`), the same Core coordinate, the same skill. Measured against run-05 (Sonnet 5 at v4.1: admitted first try, 47 entities, 27 of 186 blocks by choice) and run-15. Expected: more than 27 blocks covered under the rewritten stop rule, at most two returns per stage, no UNSUPPORTED row. Falsifier: any of the three failing. Paper-18 corrected two witness counts from the frozen files (run-15: 160 records traced, 162 distinct kind-witness keys; run-05: 44, as E-0134 had said); E-0171 carries the RCA correction.

### Run-16, gate (19:49Z)

Sonnet 5 accepted at attempt 01, 2,880 facts, 17 entity types, 2 event types, 3 relation types; subject on Claim and Observation only (no count or ratio subtypes), six project classes, three grounded in the none_found form and one citing FOAF Person. The producer excluded the 79 references and the funding identifiers by its own decision and said so. Type sets with the catalogue lesson (4, 3, 8, 5 types), 391 cases (13 ENTITY, 342 RELATION, 36 SUBJECT). Phase two dispatched 19:50Z. Against run-05 (Sonnet at v4.1): that cell's ontology was accepted at attempt 02 after a root-field refusal (`comments`), this one at attempt 01; the comparison that matters is the population's coverage under the rewritten stop rule.

### Run-16, population and first runner attempt (20:16Z to 20:19Z)

Sonnet 5 wrote 132 assertions over 58 blocks and declared 128 blocks nothing-assertable (the 79 references, running headers, acknowledgements, most of the additional information), 194 records (159 entities, 3 events, 32 relations). The census carries one label for a block without assertions, so the producer's scope exclusion and a block with no assertable sentence read the same; the Opus cells captured the references as records, this one calls them nothing-assertable. For the RCA and for the paper's coverage figure: a block declared nothing-assertable is a producer claim the review can check, and here it is false for the reference entries.

Runner attempt 1 refused, fifty defects in one aggregated diagnostic: 45 SUBJECT_NOT_NAMED (RC2 seventeen times, the SMARTIES cruise seven, the MAR six, the Romanche transform four, the OBS network three, HASH twice, hypoDD, a detachment fault: subjects set by topic on sentences that name none of them), 4 MODALITY_NOT_ASSERTED, 1 EVALUATIVE_SLOT_NOT_EVALUATED (the preferred disposition on the sentence that raises the hypothesis). The producer's own validator checked verbatim statements and formalization targets, which the adapter also checks, and none of the three derivation-content rules. Returned as structural diagnostic 1 of 2 at 20:18Z; because the diagnostic is 9,665 bytes, its exact bytes were staged in the producer's workspace and the message reproduced its head and rule sentence, a return form recorded in the launch log. The three Opus cells at this protocol pre-flighted the subject rule and returned zero, seven and zero defects at the runner; the Sonnet cell returned fifty. That is the first measured model difference at a stable protocol, and it is in what the producer checks before it stops, not in what it can write.

### Run-16, admitted and frozen (20:30Z to 20:45Z)

Admitted at runner attempt 2 after the producer split three assertions, retyped the disposition's sentence and added twelve anchor assertions, one clause per subject entity, to formalize the subject fields the rule refused. The census shows the anchors: 99 of 103 subjects proposed, 20 of 32 relations non-local, the RC2 anchor formalizing 17 records. That is the hub pattern E-0135 found in run-04 and Core-12's census was built to count; the rule "a formalizing sentence names the subject" is met by attaching one naming clause to many records, and whether those records are about RC2 is the review's to say. Query 433 rows (36, 112, 144, 141) over 157 witnesses. Frozen, E-0172 (1d06352); ladder max 40. Producer 529,350 tokens, the most of any cell, with 88,264 in the correction. The freeze template hard-coded the Opus producer fields into the ontology-run result and its generated tests; corrected from the launch log before the gate, and the template now reads them from the log. Two review sessions dispatched 20:46Z with one sentence added: where the subject derives from a different assertion than the value, judge on both blocks. Paper-19 dispatched in parallel for run-17, Haiku 4.5 at v4.9 (E-0174; E-0173 reserved for run-16's review).

### Run-16, RCA before the review (20:50Z): anchors and declarations

Anchors: 48 of the 99 proposed subjects are formalized only by an assertion that formalizes no other field of the record (RC2 eighteen, the cruise seven, the MAR six, the Romanche transform four, the OBS network three); the RC2 anchor is a 33-character clause on page 1 block 5 formalizing 17 subject fields and nothing else. The rule was met by attaching a naming clause to the subject slot of records whose value sentence names no subject. The census sees it (20 of 32 relations non-local, hub 17); the review will say whether RC2 is what those records are about. Same skill, same rule, a different producer answer: Opus set subjects where the sentence named them and left the rest unset (26 to 76 unnamed per cell); Sonnet set 99 of 103 and anchored 48.

Declarations: the census counts a block REVIEWED whether it carries assertions or is declared nothing-assertable, so `blocks_reviewed` reads 186 for run-13 (184 asserted, 2 declared), run-15 (185, 1) and run-16 (58, 128). Of run-16's 128 declared blocks, 90 look like reference entries by shape and the Opus cells captured 79 to 84 works from them. A declaration is a producer claim the census cannot check; the paper's coverage figure has to be blocks with assertions, which the census does not report as a number. Candidate Core-19 for after the matrix cells, reporting only: the census's block map carries three labels (ASSERTED, DECLARED_NOTHING_ASSERTABLE, UNTOUCHED) and the counts of each. Not dispatched now; run-17 pins the same coordinate.

Rows: 433 for 157 distinct keys, 276 returned again by a later question; CQ-03 and CQ-04 differ by one row set (Method and sample types in both). Modalities: 90 STATED, 23 MEASURED, 23 CALCULATED, 7 HYPOTHESISED, 5 NEGATED.

### Run-16 closed (21:10Z): review in, RCA written

Review merged from two sessions: R, P, P, P; 370 SUPPORTED, 61 PARTIAL, 2 UNSUPPORTED; no digest token on any row because no record carries a locator. Record E-0173. RCA at `handover/2026-09-05-run-16-sonnet-rca.md`. Two of the four findings are producer variance the protocol handled (fifty defects returned; anchors counted by the census and demoted by the review); two are protocol gaps the cell walked through: a declared block counts as reviewed, and the digest check is optional by the producer's silence. Core-19 candidates after run-17: census block labels (reporting), and a census count of records carrying a locator (reporting) or a pack requirement (a rule, Luis's).

## Matrix cell: run-17 (v4.9, Haiku 4.5), launched 2026-09-05T21:15Z at dc52547 (E-0174, E-0175)

Not a loop iteration: no change under test. Run-16's harness byte for byte with the run id and the producer's model moved (Haiku 4.5, `claude-haiku-4-5-20251001`), the same Core coordinate, the same skill. Measured against runs 06 and 07 (Haiku at v4.1: ontology accepted, population refused after two structural returns, the RCA in `handover/2026-09-05-haiku-rca.md`: paraphrase presented as verbatim, envelope keys, a phantom block id, a fabricated citation) and runs 15 and 16. Expected: admission within two structural returns under the v4.9 skill, whose verbatim method, block-inventory rule and aggregated diagnostics were written from the run-06 RCA; Paper-19 added a test that reads the skill at both coordinates and checks those four things are present now and absent at v4.1. Falsifier: a third refusal. E-0175 corrects one sentence in Paper-19's GREEN commit message.

### Run-17, gate (21:16Z)

Haiku 4.5 accepted at attempt 01 in 89 seconds and 90,064 tokens: 2,687 facts, three project classes (RidgeSegment; DeepMantleEarthquake as a Quantified Event; BasaltSample as a Quantified Sample), research imported and the other packs transitively; subject on Claim and Observation. Three grounding blocks, each citing an institution's home page (IUGG, ISC, IUGS) as a vocabulary for terms those pages do not carry: the URLs are real and the organisations exist, so nothing is fabricated in run-06's sense (a nonexistent ISO standard), and none of the three is a vocabulary; runs 15 and 16 used the none_found form for the same case. Recorded in the launch log as three unsupported vocabulary claims, zero fabricated. Type sets (4, 3, 8, 5), 277 cases (13 ENTITY, 228 RELATION, 36 SUBJECT). Phase two dispatched 21:18Z.

### Run-17, population and first runner attempt (21:19Z to 21:20Z)

Haiku 4.5 wrote 8 assertions over 7 blocks, 9 records (5 ridge segments, 1 campaign, 1 aggregate earthquake event, 2 relations), no nothing-assertable declaration, 179 blocks untouched (written as 178 at the time, corrected by E-0177), and stopped with "the parent can now assess coverage and request expansion if needed", a step the protocol does not have. Runner attempt 1 refused all eight assertions NOT_VERBATIM in one aggregated diagnostic: every statement is a clean retyped sentence ("The MAR here spreads at a half-spreading rate of 16 mm/yr.") that is not a byte span of its block. Run-06 met the same defect one statement per refusal and spent both returns on it; the v4.9 skill states the slicing method and the aggregation names all eight at once. Returned as structural diagnostic 1 of 2 at 21:20Z. Whether the skill's method reaches a Haiku producer on a return is what the second attempt measures.

### Run-17, second runner attempt (21:22Z to 21:23Z)

The eight statements came back verbatim (the skill's byte-slicing method reached a Haiku producer on one return, which run-06's skill did not manage in two). Attempt 2 refused at graph rehydration: six unknown properties on the two project types (co2_concentration_range, mechanism, count, depth_range, focal_depth_range, location), a required event_type missing, and two relation-type values outside the enum (occurs_along, observed_with). The producer wrote records against slots its own accepted surface does not declare; runs 13 to 16 validated every field against the staged surface before writing. Returned as structural diagnostic 2 of 2, the last, at 21:23Z; the message names the staged surface file the phase-two dispatch already named.

An observation for Core-19: this refusal is a raw `ValueError` from `kg.py`'s rehydration ("Cannot rehydrate graph from records: ..."), aggregated and exact in its text but untyped, where every other refusal the cells have met carried a typed reason (DocumentAssertionRefusal, SourceBoundaryRefusal). The paper's claim that every refusal is typed is not true at this stage; the fix is a typed reason around the same message.

### Run-17 closed (21:30Z): refused after the diagnostic budget; the matrix pass is complete

Attempt 3 refused GAP_REQUIRED: the second correction stripped every assertion of its targets and left none with a gap; the reason named one, all eight are empty. Terminal, as runs 06 and 07 at v4.1, one stage later. E-0176; RCA at `handover/2026-09-05-run-17-haiku-rca.md`. Producer 151,411 tokens. The v4.9 skill's methods reached the producer (byte spans on one return, no constructed block id, no fabricated standard); its rules without method did not (validate against the surface; a target or a gap on every assertion).

The matrix pass at the settled protocol: Opus 5 three cells (R R R R; P R R P; P R P P; no UNSUPPORTED in 1,867 rows), Sonnet 5 one cell (R P P P; 2 UNSUPPORTED in 433; fifty defects returned; anchors), Haiku 4.5 one cell (refused after two returns). Core-19 dispatched 21:30Z with the four reporting fixes the two matrix cells surfaced: census block labels, locator coverage, a typed rehydration refusal, aggregated GAP_REQUIRED. No Core change touches admission semantics. Luis's rulings stand open: Claim.statement, the reviewers' lines, review protocol v3, ratification of runs 09 to 17, the locator requirement.

## Core-19 landed (21:56Z): the protocol reports what is true

Commits 0f4da9a (RED), c53d982 (GREEN), 8a6c3f3 (OVR-000414); decision 24; pushed after the active tests (1,143). Verified on disk: the census block map carries ASSERTED, DECLARED_NOTHING_ASSERTABLE and UNTOUCHED with three counts and `blocks_reviewed` kept as the sum with its meaning stated; `provenance_coverage` per type with total, with_locator, with_digest; `RECORDS_NOT_REHYDRATABLE` raised in the population pipeline around the rehydration message; GAP_REQUIRED lists every empty assertion. No admission semantics moved.

The new census applied by script to the five frozen captures at v4.7 to v4.9 (the final capture of each cell; run-17's is the one that was refused):

| cell | blocks asserted | declared | untouched | source-asserted records | with locator | with digest |
|---|---|---|---|---|---|---|
| run-13 | 184 | 2 | 0 | 269 | 269 | 269 |
| run-14 | 184 | 2 | 0 | 242 | 203 | 203 |
| run-15 | 185 | 1 | 0 | 142 | 142 | 142 |
| run-16 | 58 | 128 | 0 | 103 | 0 | 0 |
| run-17 | 7 | 0 | 179 | 0 | 0 | 0 |

Read across the row: the Opus cells asserted 184 to 185 blocks and set locators on most source-asserted records; Sonnet asserted 58, declared 128 and set no locator; Haiku asserted 7. These are the coverage and provenance numbers the paper reports per cell, and from Core-19 on the census computes them at admission.

No new cell is opened. The record cell, the licence ruling on Claim.statement, the locator requirement, review protocol v3 and the reviewers' lines are Luis's; the loop waits on them. The one cell the evidence supports without a ruling is an Opus rerun at the Core-19 coordinate so the record cell's frozen census carries these counts; it costs about 400,000 producer tokens and a review, and it should run after the rulings, not before, so that it is run once.

Core-19's report (22:35Z) matches the disk. Shapes as landed: the fixture census reads `blocks_asserted`, `blocks_declared_nothing_assertable`, `blocks_untouched` beside `blocks_reviewed` and `blocks_total`; `provenance_coverage` has `total`, `with_locator`, `with_digest` and a `by_type` map; `RECORDS_NOT_REHYDRATABLE` is raised by `_rehydrate` in population.py at four sites with `str(error)` as its detail, replacing the property two tests pinned that the graph gate's exception passed through untyped (the tests renamed, decision 24 records the swap); GAP_REQUIRED runs as a pre-pass beside the locator defects. Fixture digests moved (document-census.json 802 to 981 bytes) and are named in OVR-000414. Full suite 3,123, pareto 597, paper 1,143. The agent discarded a cosmetic edit of its own made after sealing the entry (an unused loop variable stays); it said so. Paper-20 dispatched 22:36Z to extend the appendix evidence catalogue with the loop's iterations and the matrix pass, leak-checked at 60 characters, E-0178.

### Appendix evidence extended (23:00Z)

Paper-20 added catalogue entries 13 to 20 (eighteen snippets, `26-` to `43-`): the subject element, the word rule with its fixtures and the E-0160 correction, the withdrawal of projection with run-13's census, the one-row-per-witness removal with run-15's offline validation before and after, producer variance at a fixed protocol (the diagnostic heads of runs 14, 16 and 17 with model and cost), the anchors (run-16's derivation census beside run-15's), Core-19's census shapes and the five-cell table, and the preliminary review outcomes of runs 13 to 16 marked not ratified. Maximum shared run over all eighteen: 21 characters against the 60 threshold, measured per block; the check was calibrated on run-03's known 73. Five snippets quote a private diagnostic's own text (record ids, reasons, counts, the rule sentence) and no statement; the catalogue's opening claim that nothing comes from private/ is scoped to the first twenty-five. E-0178 (fdbdd77). Two standing facts restated there: there is no repository-level leak guard on the catalogue (deep-sweep D-16, unbuilt), and the paper ledger itself measures 73 against the reading through the article title, which is public metadata and the same D-16 hit.

### Catalogue leak guard built (23:20Z)

Paper-21 wrote `paper-v4/appendix-evidence/test_catalogue_leak.py` (E-0179, 8c0d238): the freezes' 60-character window rule copied rather than imported, applied to catalogue.md and every snippet; a bijection test between the catalogue and the snippet directory; digest checks for the eighteen snippets that record one; a calibration test that must find run-03's known leak (73, the article title); a tmp_path negative control. The catalogue's maximum is 21. D-16 is narrowed, not closed: the full walk over paper-v4/ and handover/ with an allowlist is unbuilt, and the ledger, the manuscript and the master plan each measure 73 through the article title, which is public metadata. One correction recorded: D-16's parenthesised numbers were window counts, not run lengths. Active tests 1,148.

## Loop iteration 8 decided (2026-09-06T00:15Z): the refusal list as the skill's pre-flight

No ruling has come, and the night instruction stands. The one change the matrix evidence supports that touches none of Luis's rulings: at a fixed protocol the producers differed in what they checked before stopping, and the adapter's refusal reasons are exactly that list. Core-20: the skill carries the list, one line per reason with the check in plain words, and a guard derives the names from the two enums so the skill cannot drift from Core (decision 25). Nothing in the adapter changes; the list is the adapter's own refusals, so it steers nothing. Measured on a Haiku 4.5 cell (run-18, harness v4.9, the Core-20 coordinate), the cheapest producer and the one the list is for. Expected: admission within two structural returns. Falsifier: a third refusal, which would say a list does not substitute for a producer's own validator, and the paper's claim for small producers stops at "the protocol admits nothing wrong from them". Dispatched 00:15Z.

### Iteration 8, Core-20 landed and run-18 opened (00:45Z to 01:10Z)

Core-20: 80cf448 (RED), f220852 (GREEN), c95dba7 (OVR-000415), decision 25; the skill carries the two enums' 48 reason names between markers, one clause each, and the guard derives the names from the enums; no adapter source moved. Paper-22 opened run-18 (90631c3, 46e91a1, 1fc0b64; E-0180, E-0181) pinned to c95dba7 with Core-19 and Core-20 both read LANDED by AST; one declared input moved against run-17, the skill; 1,234 active tests. The overseer's re-run of the pin rewrote nothing. Launching Haiku 4.5 at 01:10Z.

## Loop iteration 8: run-18 (v4.10, Haiku 4.5), launched 2026-09-06T01:10Z at c95dba7 (E-0180, E-0181)

Change under test: Core-20, the adapter's 48 refusal reasons as the skill's pre-flight list, one clause each, guarded against the two enums (decision 25, OVR-000415); Core-19's reporting rides along at the same coordinate. Harness: run-17's, no delta; the producer Haiku 4.5, the one the list is for. Expected: admission within two structural returns where run-17 was refused after two. Falsifier: a third refusal. Core-20's own residual: the FAMILY_NOT_ADMITTED line states the necessary condition only.

### Run-18, gate (01:11Z)

Haiku 4.5 under the Core-20 skill accepted at attempt 01 in 255 seconds and 94,950 tokens: 2,614 facts, seventeen project classes each with a grounding block, the research pack not imported, so no Claim, Observation, Source, Campaign or Method type and no subject-bearing type; two SSN-grounded measurement entity types stand in for observations. Citations: eight URLs, three real vocabularies (the VIM, read from the fetched PDF, defines "measuring instrument" at 3.1; SSN; the WGS84 Basic Geo vocabulary, which defines no "location"), five institution home pages cited as vocabularies for terms they do not carry, one unreachable on transport; nothing fabricated. The producer ran the ambient malleus-inquisitor (miniconda's 0.13.3), whose Root Currency rite read the repository's ontology/malleus.yaml, a file outside the declared inputs with the same bytes as the staged one; recorded as an isolation observation. Type sets on a surface with no subject-bearing type (2, 4, 10, 6), 646 cases, all ENTITY and RELATION. Phase two dispatched 01:13Z. Whether the pre-flight list reaches this producer is measured at the runner, not here: attempt 01 of run-17 was also accepted at the gate.

### Run-18, population and first runner attempt (01:17Z to 01:18Z)

Haiku 4.5 under the pre-flight list wrote 26 assertions over 23 blocks, declared 163 blocks nothing-assertable, 22 records (11 entities, 6 events, 5 relations), and reported its reading digest verified. Runner attempt 1 refused READING_MISMATCH: the capture's digest is not the supplied bytes'. The pre-flight list states that check in one line; the producer's own check computed the digest of something else. The capture also carries a relation type the surface does not declare (EarthquakeLocatedAt, twice), which the aggregated checks will meet once this fail-fast one clears. Returned as diagnostic 1 of 2 at 01:18Z. Against run-17 (8 assertions, 7 blocks, 179 untouched): three times the assertions, every block accounted for by a declaration; against run-17's first refusal (all eight statements paraphrased): the statements were not the failure this time.

### Run-18, second runner attempt (01:19Z)

The reading digest fixed, attempt 2 refused NOT_VERBATIM on 18 of 26 assertions in one aggregated diagnostic: the same class as run-17's first attempt, with the producer again reporting every statement verbatim. The pre-flight list's first line names the refusal and the method by reference; the producer read the list (its session log quotes the harness block) and did not run the check. Returned as diagnostic 2 of 2, the last, at 01:19Z. The undeclared relation type still waits behind this refusal, so the third attempt meets it if the statements come back as byte spans; the falsifier (a third refusal) is likely to fire. What that says, ahead of the RCA: a list of checks the adapter runs is not a validator the producer runs; the Opus producers wrote one from the rules, and this producer wrote none from the list.

### Run-18 closed; iteration 8 closed (01:30Z): the list is not a validator

Attempt 3 refused NOT_VERBATIM on 11 of 26 (one ligature-only, eight near misses at 0.92 to 0.94, two paraphrases, measured by script without quoting the reading); terminal; the falsifier fired. E-0182; RCA at `handover/2026-09-06-v410-rca.md`. Producer 161,919 tokens. Core-20 stays: harmless, guarded, the one place the adapter's checks are listed for a producer; it did not carry Haiku, and its effect on Opus and Sonnet is unmeasured.

Tally after eight iterations: three clarifications of an existing check that held (ranges and names, tags, words), two removals that held (the ENTITY flood, projection), one executor removal that held (rows per witness), two additions that held (the subject element, one source of truth for modality), one projection that failed, one list that did not carry the producer it was for. Four reporting fixes (Core-19) with no cell of their own. Five Opus and Sonnet cells at a stable Core with no UNSUPPORTED row outside the Sonnet cell's two; four Haiku cells refused with nothing wrong admitted.

The loop pauses. What remains is Luis's: the record cell (an Opus rerun at the Core-20 coordinate, one cell), Claim.statement, locators, review protocol v3, the reviewers' lines, ratification of runs 09 to 18, the D-16 allowlist, and now the isolation boundary (whether a producer may run the adapter's dry run on its own draft).

## Loop iteration 9 decided (2026-09-06T03:05Z): the list measured on Sonnet 5

Luis (02:55Z): "Continue and keep learning". Read as: the loop goes on, the rulings stay his, and the iterations chosen pre-empt none of them. The measurement E-0182 names as missing: the pre-flight list on a producer that builds a validator after a return. Run-19, Sonnet 5 at the Core-20 coordinate, harness v4.9 unchanged (Paper-23, E-0183). Expected: fewer than run-16's fifty defects at the first runner attempt and admission within two returns. Falsifier: fifty or more, or a third refusal. The RCA also reads the anchors, the locators and the declarations, which Core-19's census now counts at admission. After run-19, and unless a ruling says otherwise, run-20 is the Opus cell at the same coordinate, the record-cell candidate, which measures the list on the producer that already checked everything.

## Loop iteration 9: run-19 (v4.10, Sonnet 5), launched 2026-09-06T04:15Z at c95dba7 (E-0183, E-0184)

Paper-23 opened run-19 (07363b4, aba3ace; 1,320 active tests) pinned to the Core-20 coordinate; the overseer's re-run of the pin rewrote nothing; E-0184 (40b1a4b). Paper-23 recomputed run-16's anchor figure from its capture under a stated rule and carries the rule in the contract (48 of 99). Producer Sonnet 5 launched at 04:15Z. Expected: fewer than fifty defects at the first runner attempt, admission within two returns. Falsifier: fifty or more, or a third refusal.

### Run-19, gate (04:30Z)

Sonnet 5 under the pre-flight list accepted at attempt 01, 2,794 facts, five project classes: a feature type, a named seismic event, an EarthquakeCatalogSubset entity for counted bodies of earthquakes (subject-bearing, the producer's answer to subject ranging on Entity, the same device as run-16's SeismicitySet), Person and Organization; every quantity on the metrology Observation shape; two blocks cited (QuakeML, PROV-O, both checked earlier) and two in the none_found form, where run-16's producer cited FOAF and declared three none_found. The producer reports having confirmed that private/ is gitignored, a look at a repository file; recorded as an isolation observation. Type sets with the catalogue lesson (4, 4, 8, 5), 308 cases (11 ENTITY, 242 RELATION, 55 SUBJECT). Phase two dispatched 04:32Z. The measurement is the first runner attempt's defect count against run-16's fifty.

### Run-19, population and first runner attempt (05:02Z to 05:05Z)

Sonnet 5 under the pre-flight list: 157 assertions over 59 blocks, 127 declared nothing-assertable (the reference list and running headers, each documented), 204 records (174 entities, 1 event, 29 relations), 29 subjects set and 73 stripped back to unset by the producer's own check against SUBJECT_NOT_NAMED before it stopped, no locator set. Runner attempt 1 refused three defects, all SUBJECT_NOT_NAMED: the three hypothesis claims with RC2 as subject, whose disposing sentences name no segment, the class run-12's Opus producer was returned for at E-0155. Run-16, the same model at v4.9 without the list, returned fifty at this attempt and then anchored 48 subjects; this producer ran the list and left the subjects unset. Returned as diagnostic 1 of 2 at 05:04Z. The expectation of E-0183 (fewer than fifty) held; the second (admission within two returns) waits on the correction. What did not change: no locator on any record, so the digest check will not run on this cell either; the list names DIGEST_MISMATCH and DIGEST_NOT_LOCATED as checks on a digest a producer sets, not as a reason to set one.

### Run-19, admitted and frozen (05:08Z to 05:20Z)

Admitted at runner attempt 2 after the producer replaced its lenient subject self-check with the strict one and stripped 26 more subjects to unset (97 of 204 records without one); no anchor. Census at admission: 59 asserted, 127 declared, 0 untouched; 26 of 121 subjects proposed, 22 attachable, 13 ambiguous, 60 unnamed; 0 of 121 records with a locator; 10 of 29 relations non-local, hub 8. Query 154 rows (15, 37, 52, 50; 79 ENTITY, 75 SUBJECT, no RELATION row) over 54 witnesses: a third of run-16's, because 95 subject-bearing records carry no subject and the v4.4 restriction leaves them unreachable. Frozen, E-0185 (b8fb2c3); ladder max 0. Producer 517,488 tokens. Two review sessions dispatched 05:21Z; Paper-24 dispatched in parallel for run-20, Opus 5 at the same coordinate, the record-cell candidate (E-0187; E-0186 reserved for run-19's review).

Both of iteration 9's expectations held: three defects against fifty, one return. The list did on Sonnet what it did not do on Haiku: the producer ran the checks and, where a check failed, chose absence over manufacture. The cost of that choice is visible in the rows: the honest subject census leaves two thirds of the subject-bearing records unreachable by any question, which is the v4.4 restriction's price and the strongest case yet for revisiting how a subject-less record is reached (a ruling, since it changes the binding).

### Run-19 closed; iteration 9 closed (05:40Z): the list worked on Sonnet, and honesty is unreachable

Review merged from two sessions: R, R, P, P; 135 SUPPORTED, 19 PARTIAL, 0 UNSUPPORTED; no digest token (no locators), no RELATION row. Record E-0186. RCA at `handover/2026-09-06-run-19-sonnet-v410-rca.md`. Both expectations held. The structural finding, from the second session's trace reading and confirmed by script: the records that answer CQ-03 and CQ-04 are in the graph without a subject and no case reaches them. Measured on the frozen cells, the subject-less subject-bearing records some set names: run-13 158, run-14 71, run-15 64, run-16 4, run-19 95; reaching them as one ENTITY row per question adds up to that many rows per question. That is the ENTITY flood v4.4 cut, now deduplicated; whether to pay it, and how (drop the restriction, or reach only the subject-less), is Luis's, because it changes every cell's comparability. Run-20 (Opus 5, the record-cell candidate) is being opened.

## Run-20 (v4.10, Opus 5), launched 2026-09-06T05:58Z at c95dba7 (E-0187, E-0188): the record-cell candidate

Not a loop iteration: no change under test. Opus 5 at the coordinate whose census reports block labels and provenance coverage and whose skill carries the pre-flight list; harness v4.9 unchanged. Paper-24 opened it (a2148dc, e008d8f; 1,414 active tests) and corrected run-19's contract's reading of run-15's locator count (142 of 351 in `properties`, not 0 at the record's top level); the overseer's re-run of the pin rewrote nothing; E-0188 (7165390). Expected: admission within two structural returns and no UNSUPPORTED row at review, as the three Opus cells at v4.7 to v4.9 gave. Falsifier: a third refusal or one UNSUPPORTED row. Secondary: the first-attempt defect count (0, 7, 0 before) and the census's block and provenance counts at admission.

### Run-20, gate (06:13Z)

Opus 5 under the pre-flight list accepted at attempt 01, 4,314 facts, 28 project classes, five root extensions grounded to BFO, RO and PROV-O with every borrowed term confirmed (four BFO classes in the fetched OWL, three by IRI through OLS; RO's three by OLS earlier; PROV-O's three) and the domain names declared invented with a search note naming the geoscience vocabularies it would not cite unverified: the first cell of the loop with zero unsupported vocabulary claims. Five subject-bearing types (Claim, Observation, CountObservation, GeophysicalEvent, ReportedRatio); every quantity an Observation with a subject; GeophysicalModel under Method by the producer's stated judgement. The producer ran the prescribed capability probe, found the broken ambient shim, and handed the attempt over uncompiled, saying so. Type sets with the catalogue lesson (7, 12, 18, 14 types; PublishedWork and ResearchAgent in no set; the EarthFeature parent in no set, its subtypes named one by one), 3,068 cases (38 ENTITY, 2,852 RELATION, 178 SUBJECT). Phase two dispatched 06:15Z.

### Run-20, population and first runner attempt (06:50Z to 06:52Z)

Opus 5 under the pre-flight list: 393 assertions, 184 blocks asserted and 2 declared, 482 records (426 entities, 1 event, 55 relations), 77 typed gaps, 122 subjects set (20 more proposed and removed by the producer where the sentence says "this model" or "those samples"), 235 records with a locator and digest, every statement a byte span through a harness that refuses an anchor it cannot find. The producer ran the list mechanically and refused to write while any check failed: 37 failures fixed before the file existed. Runner attempt 1 refused one defect: the cold-thick-lithosphere hypothesis claim with RC2 as subject, whose subject slot was formalized by the raising sentence (naming the lithosphere, not the segment) while the disposing sentence names RC2; written here first as the reverse, corrected on the producer's report. The residual subject failure of every cell at this Core is that record class (run-12 two, run-16 three of forty-five, run-19 three, run-20 one); the subject slot can be formalized by the raising sentence, which names the segment, so it is a derivation choice, not a rule the reading cannot meet. The producer's own account of the miss: its reading of the word rule is not the adapter's, case folding in particular. Returned as diagnostic 1 of 2 at 06:52Z. First-attempt defects across the Opus cells: 0, 7, 0, 1.

### Run-20, admitted and frozen (06:55Z to 07:05Z)

Admitted at runner attempt 2 after the producer applied the strict subject reading to all six records of the hypothesis shape, lengthened one span so the preferred hypothesis keeps RC2, and unset five subjects rather than repoint them. Census at admission: 184 asserted, 2 declared, 0 untouched; 117 of 235 subjects proposed, 33 attachable, 30 ambiguous, 55 unnamed; 235 of 235 source-asserted records with a locator and digest, the first cell where the census reports provenance whole; 24 of 55 relations non-local, hub 16 (the byline). Query 434 rows (34, 105, 158, 137; 171 ENTITY, 17 RELATION, 246 SUBJECT) over 220 witnesses, 33 merged from more than one case. Frozen, E-0189 (abc53b4); ladder max 0; 1,422 active tests. Producer 433,787 tokens. Two review sessions dispatched 07:06Z. The record-cell decision stays Luis's; on the mechanical side this cell has everything the loop asked for: all citations confirmed, every statement a byte span, full provenance, one return.

### Run-20 closed (07:30Z): the record-cell candidate; the loop pauses

Review merged from two sessions: R, R, P, R; 417 SUPPORTED, 17 PARTIAL, 0 UNSUPPORTED; 251 digests verified; every SUBJECT row in its block. Record E-0190. RCA at `handover/2026-09-06-run-20-opus-v410-rca.md`. The expectation held on both parts. Mechanically the cleanest cell of the loop; CQ-03's PARTIAL is the reviewers' material-ambiguity line, run-13's reviewer having read the same shape as RESPONSIVE.

Nine iterations and eleven cells since the loop started. Every next step is a ruling of Luis's; the loop pauses with the full progress report in chat, per his rule of 02:40Z.

## Reliability measurement (2026-09-06T08:40Z): a third blind judgement of CQ-03 in run-20 and run-13

No ruling has come. The one measurement that needs none and bears on the record-cell choice: the reviewers' threshold on CQ-03, which read RESPONSIVE in run-13 and PARTIAL in runs 15, 19 and 20 on the same shape (several ranges returned, none marked as the answer). Two fresh Opus sessions re-judge CQ-03 of run-20 (158 rows) and of run-13 (176 rows) under the identical task, blind to the existing blocks, writing to a `reliability/` subdirectory beside each cell's review. The frozen records do not move; the outcome is the per-row agreement with the recorded block and whether the responsiveness label holds, recorded as numbers in the ledger. Dispatched 08:40Z.

### Reliability measured (09:25Z)

Run-20 CQ-03: PARTIAL both times; row agreement 147 of 158 (0.930), Cohen's kappa 0.118; of the recorded seven PARTIAL rows one survived the blind reading, and five other rows became PARTIAL. Run-13 CQ-03: recorded RESPONSIVE, blind PARTIAL for the reason runs 15, 19 and 20 gave; row agreement 174 of 176 (0.989), kappa 0.745. Every digest verified by every session; no UNSUPPORTED row anywhere. The support rate is stable and the PARTIAL set is not: a PARTIAL is a threshold judgement, and the threshold is the session's. Run-13's R R R R did not reproduce on CQ-03. E-0191; `paper-v4/evaluation-v4/reliability.py` committed as the measure. The loop pauses on Luis's rulings with the updated report.

## Declared-blocks audit (2026-09-06T10:35Z): is a declaration true?

No ruling has come. A second measurement that needs none: the census now counts a block declared nothing-assertable, and cannot check the declaration. Run-16's producer declared 128; by shape 90 looked like reference entries, which the Opus cells captured as records. One fresh session judges each of the 128 against the reading alone under the protocol's rule, block ids and one-word kinds only, into `paper-v4/evaluation-v4/run-16/reliability/declared-blocks.json`. The outcome is the count of declared blocks that carry assertable content, a number for the paper's coverage figure and for the ruling on whether the review should sample declarations. Dispatched 10:35Z.

### Declared blocks audited (10:50Z)

Run-16: 111 of 128 declared blocks assertable, 101 of them reference entries; the declaration true for 17 (running headers, figure furniture, boilerplate, severed fragments). The census reports the number and cannot check it; the audit cost one session. For the paper, run-16's coverage is 58 of 169 assertable blocks, not 186 of 186 reviewed. E-0192. The loop pauses on Luis's rulings.

## Replicate and second audit (2026-09-06T10:57Z; first written as 12:00Z, corrected from the wake clock)

No ruling has come; the instruction is to keep learning. Two measurements that need none. Run-21 (Paper-25, E-0193): Opus 5 at the run-20 coordinate, harness byte for byte, the first within-condition replicate the matrix has; the RCA reads first-attempt defects, coverage, subjects, provenance, rows, the review's rates and labels, and cost as variance against run-20, with the same expectation and falsifier. And the declared-blocks audit repeated on run-19's 127 declarations, to corroborate E-0192 on the other Sonnet cell. Dispatched 10:57Z.

### Run-19's declarations audited (11:05Z; first written as 12:15Z, corrected)

92 of 127 declared blocks assertable, 82 of them reference entries; 35 true (24 severed fragments this session read stricter than run-16's auditor, 8 running headers, 2 figure-furniture blocks, one rights stamp). Same shape as run-16 (111 of 128): the two Sonnet cells declared the reference list void and the census counted it as reviewed. The auditors differ on the fragments (bibliographic tails with a venue and year), which is the rule's edge and worth one sentence in the review task if declarations are sampled. Entry E-0194, after Paper-25's E-0193 lands; the file is leak-checked at 60 characters.

## Run-21 (v4.10, Opus 5 replicate of run-20), launched 2026-09-06T11:40Z at c95dba7 (E-0193, E-0195)

No change under test. The same Core coordinate, harness and producer block as run-20; the first within-condition pair the matrix has. Paper-25 (9650095, 55abb34; 1,508 active tests) repaired a carried reader that returned 0 for run-20's one first-attempt defect. The overseer's re-run of the pin rewrote nothing; E-0195 (636f826). Expected: admission within two returns, no UNSUPPORTED row. The RCA reads the rest as variance: first-attempt defects, blocks asserted, records, subjects proposed, provenance, rows, the review's rate and labels, cost.

### Run-21, gate (11:57Z)

Opus 5 accepted at attempt 01, 3,780 facts, 13 project classes, seven root extensions: four grounded to the IUPAC Gold Book, DCMI Metadata Terms, PROV-O and Schema.org (16 of 17 borrowed terms confirmed by fetch or domain-restricted search; the Gold Book's bare "phase" entry unverified because the site refuses the fetch), three declared none_found with a search note naming GeoSciML, GEBCO, the USGS glossary, QuakeML, FDSN and GeoSPARQL as not cited unverified. The same producer block as run-20 minted a different shape: one feature type carrying feature_kind and one material type carrying material_kind where run-20 minted twelve and four; 29 surface types against run-20's 44; five subject-bearing types (Claim, Observation, ReportedClaim, ReportedObservation, ReportedRatio) against run-20's five. The session log records no capability probe. Overseer error, recorded in the launch log: the first gate invocation used the frozen run-01 gate at the experiment root, whose manifest carries the 09-04 pack digests, and it refused on the metrology digest; the diagnostic is parked under `overseer-misinvocation/` and is not an attempt; the cell's own gate accepted the same bytes. Type sets translated from run-20's judgement (6, 5, 12, 9 types; BibliographicSource and ResearchActor in no set; GeophysicalEvent left out as in runs 12 to 20; the one feature type listed because no narrower choice exists), 1,583 cases (16 ENTITY, 1,430 RELATION, 137 SUBJECT) against run-20's 3,068. Phase two dispatched 12:02Z (transcript 12:01:59Z; first written as 12:05Z before the dispatch, corrected).

### Run-21, population, admission and query (12:35Z to 12:39Z)

Opus 5: 399 assertions, 186 of 186 blocks asserted and none declared (the first cell, since the census reports block labels, with nothing declared), 535 records (508 entities, 1 event, 26 relations), 94 typed gaps (88 RELATION_ABSENT), 77 of 314 subjects proposed, 314 of 314 source-asserted records with a locator and digest, 0 of 26 relations non-local. Admitted at runner attempt 1 with no return; first-attempt defects across the Opus cells 0, 7, 0, 1, 0. The producer's report: two pre-flight passes (the builder's checks, then an audit re-reading the emitted file from disk), no statement typed, three judgement calls flagged for the review (the corresponding e-mails assigned by local part and domain, byline initials carried as tags, contribution_role unset everywhere). Then the evaluator's error: the binding frozen at acceptance was refused by the executor, because an AnalyticalMethod record reached through the Method case had no projection for its own type. The acceptance note had claimed Method's case returns its subtypes; right about reach, wrong about projection, and the executor's docstring assigns the correction to the evaluator's sets. The sets were closed under the surface's subtypes (AnalyticalMethod beside Method in CQ-01, CQ-03 and CQ-04, the only omission by a closure check over the is_a chains) with no row in existence; the first sets, note and bindings are kept as `*.first.*` and recorded in the launch log. Re-bound 1,883 cases (19 ENTITY, 1,715 RELATION, 149 SUBJECT), executed 490 rows (24, 122, 178, 166; 239 ENTITY, 41 RELATION, 210 SUBJECT) over 182 witnesses, 237 from more than one case. Producer 387,470 tokens (run-20: 433,787). Harness lesson for a later version, not applied now: the binder can check the subtype closure at acceptance and refuse there, where the executor refuses now.

### Run-21, frozen (12:44Z); two review sessions dispatched 12:46Z

Frozen at c077946, E-0196; ladder max 0, no leak; 23 public artifacts (the four pre-amendment binding files among them, as `*.first.*`), 8 withheld; gate 1516 passed. The freeze template's double-append guard still named E-0195 from the sed derivation and was corrected before the run. Two Opus review sessions dispatched at 12:46:23Z and 12:46:34Z (transcript), rows 24 and 122, 178 and 166, under the same task text as run-20's with the counts moved.

### Run-21 closed (13:02Z): the replicate; the loop pauses

Review merged from two sessions: P, R, P, P; 471 SUPPORTED, 19 PARTIAL, 0 UNSUPPORTED; 215 digests verified; 41 RELATION rows all local; every SUBJECT row in its block. Record E-0197. RCA at `handover/2026-09-06-run-21-opus-v410-replicate-rca.md`. The expectation held on both parts (no return, no UNSUPPORTED row). Eighteen of the nineteen PARTIAL rows are six feature records whose `feature_kind` the block does not state, returned under three questions each; the nineteenth is a campaign duration. CQ-01 fell to PARTIAL for a reason that is not the producer's: the instrument count is in the population twice, on ReportedObservation records without a subject, and no case reaches a subject-less subject-bearing record under the v4.4 binder (237 such records here, 118 in run-20). That is the first responsiveness label the open reachability ruling has decided. CQ-04 fell on the reviewer's linking standard where run-20's reviewer read the same shape as RESPONSIVE. Against run-20 the support fraction is the same to two places (417 of 434, 471 of 490); the ontology's grain, the gap kinds, the relation count and the subject rate vary widely inside one condition; the floor held twice.

Nine iterations and thirteen cells (runs 09 to 21) since the loop started; the replicate is a cell, not an iteration. Run-20's close wrote eleven cells and this entry first wrote twelve; runs 09 to 20 are twelve and 09 to 21 thirteen, corrected here. Every next step is a ruling of Luis's; the loop pauses with the full progress report in chat.

## Loop iteration 10: v4.11, the type-set closure at bind time (2026-09-06T13:30Z to 13:50Z)

Change: one module and six tests (RED 6d4fba3, GREEN 8754b44), no Core change, no cell run; the rerun is the check applied to every frozen cell. `type_set_closure.py` reads the validated contract's subClassOf facts and refuses, per question, a set that lists a type without its surface subtypes; from v4.11 the cell's binder runs it before writing the acceptance binding. Expected: run-21's first sets refused naming AnalyticalMethod in three questions, its amended sets and run-20's closed. The second expectation failed and the check was right: run-20's sets omitted GeophysicalModel under Method in CQ-01 and SoftwareTool in CQ-03 and CQ-04, with 6 and 8 rows behind them in run-20's result, and the executor never refused because its projection map is binding-wide. Measured over the frozen cells: seven of twelve not closed per question (runs 08, 09, 10, 12, 13, 15, 20), five closed. A per-question type set was never a reach filter; the reviews and counts stand, the notes' "only in" sentences did not. E-0198; RCA at `handover/2026-09-06-v411-rca.md`. Gate 1522. The executor-side alternative (filter reach by the listed types) is not taken: it would change every cell's shape, which is Luis's.

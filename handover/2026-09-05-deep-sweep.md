# Deep sweep of the paper stream: open defects and improvements, 2026-09-05

Read-only sweep at repository commit `77058f7326a03e788da0b3d6f40484ad9b1e8337`
(`Freeze run-04: admitted and replayed once Core admits a list, review inputs
bound`). Run-04's public artifacts landed while this sweep was running; every
statement about run-04 is against that commit.

Sources swept: `docs/PRINCIPLES.md`; the overseer journal and the Haiku RCA;
`paper-v4/manuscript.md`, `manuscript-v4-working.md`, `paper-ledger.md`
E-0119 to E-0132, `paper-master-plan.md`; every public cell directory
`paper-v4/experiment-v4/run-02` to `run-07` (contracts, manifests, spawn
messages, launch logs, diagnostics, run results, censuses, gap counts, withheld
lists, bindings, trace summaries, tests); the private launch logs under
`private/paper-v4-v4-run-0N/` read for defects only; `src/malleus/compiler.py`,
`src/malleus/_contract_pipeline/{document,population,knowledge,revision}.py`,
`src/malleus/inquisition/pack_grounding.py`; `ontology/malleus.yaml`,
`ontology/packs/*.yaml`, `ontology/profiles/object-event.yaml`,
`src/malleus/profiles/source-assertion.json`;
`.claude/skills/malleus-acolyte/SKILL.md`; governance entries `OVR-000385` to
`OVR-000398`; and the Small Shop fixture.

The active paper gate was run once during the sweep:
`.venv/bin/python paper-v4/run_active_tests.py` returned **1 failed, 320
passed**, the failure being `run-04/test_contract.py::test_the_run_directories_are_empty_and_carry_only_a_keepfile`
against artifacts that were landing at that moment. It is green at HEAD.

Ordered by leverage. Each entry gives the evidence, what it costs, a proposed
fix, the test that would pin it, and the layer that owns it.

---

## D-01. Run-04's query binding was chosen after its row counts were seen

**Evidence.** `paper-v4/experiment-v4/run-04/results/native-query-binding.json`,
field `bound_by`: a first hand-picked draft of 38 cases "returned no row for
CQ-03 and was replaced by the exhaustive form"; a second draft "included
BibliographicSource in CQ-04's type set, which bound 75 citation rows with no
bearing on the mechanism question, and that type was removed from CQ-04 before
freezing". `results/launch-log.json`, `query.drafts`, records both drafts with
their row counts, including draft-02's full per-question tally
(17 / 69 / 83 / 146). The frozen binding returns 17 / 69 / 83 / 71: CQ-04 lost
exactly the 75 citation rows.

**Cost.** The candidate Opus 5 cell of record's headline numbers come from a
binding that was edited with the row counts in view. Manuscript §2.3 says a
binding "cannot name a document value, population identifier, source locator,
result count, or exact graph closure"; the master plan's submission gate
excludes "best-of-run selection or fallback after a poor result". Both are
violated in kind, not in letter: no value or identifier entered the binding, but
the *selection between bindings* was conditioned on the result. Whatever the
paper says about run-04's rows inherits this.

**Fix, options, no recommendation implied by ordering.** (a) Re-derive the
binding by a stated mechanical rule applied once — for each question, a type set
judged from the surface, then the full cross-product — and freeze the first
output whatever it returns, recording the type-set judgement as the only human
step. (b) Keep the three bindings and publish all three with all three row
counts, reporting draft-01 and draft-02 as results rather than as discards.
(c) Declare run-04's binding non-blind, report the rows as such, and take the
blind binding from a fresh cell. Options (a) and (c) cost a rerun of the query
stage only; the ledger and replay are untouched by any of them.

**Test.** A run-04 contract test asserting that `results/` holds exactly one
binding artifact, that `launch-log.json` `query` carries no `drafts` key with a
row count, and that the binding's `bound_after_replay_receipt_sha256` equals the
run result's `replay_receipt_sha256`. The run-05 harness already has the last
of these (`test_the_query_binding_is_type_only_and_bound_after_the_replay`).

**Owner.** Harness and review. Not Core.

---

## D-02. Events cannot be relation endpoints, and the vocabulary that fixes it is outside the read set

**Evidence.** `ontology/malleus.yaml` lines 283-292: `source_id` and `target_id`
both carry `range: Entity`, both required. `ontology/profiles/object-event.yaml`
declares an abstract `EventParticipation` with `event_id: Event` and
`entity_id: Entity`; `src/malleus/_contract_pipeline/population.py:923` admits
the `event_participations` family only when the compiled contract declares that
type; `OVR-000387` states plainly that `CREATE_EVENT_PARTICIPATION` "stages
participation without widening relation endpoints".
`.claude/skills/malleus-acolyte/SKILL.md` lines 258-262 tells the producer to
load that vocabulary with `bundled_ontology_path("profiles",
"object-event.yaml")`. Every cell's spawn message
(`paper-v4/experiment-v4/run-0N/spawn-message.md`) says "read only the eight
declared inputs under `<PRODUCER_WORKSPACE>/inputs/`", and
`producer-input-manifest.json` lists eight inputs, none of them
`object-event.yaml`.

**Cost.** The skill instructs a route the isolation message forbids. Every cell
that reached population has zero `event_participations`
(run-02 0 events, run-04 3 events, run-05 1 event, all with 0 participations),
and run-05's own binding records the consequence in its `bound_by` field: "Event
types cannot be relation endpoints, so no case binds Earthquake". Run-02 wrote
seven `TYPE_ABSENT` gaps rather than events. The earthquake is an island in
every cell.

**Options at pack level.**
1. **Add `ontology/profiles/object-event.yaml` as a ninth declared input.** No
   Core change, no root change, no new design. The producer subclasses
   `EventParticipation`, the compiled contract declares the type, and
   `population.py` admits the family that already exists. This is the cheapest
   option and it is exercised by the shipped
   `research/.../fixtures/small_shop_fulfilment_object_event_v1` fixture.
2. **Widen `Relation.source_id`/`target_id` to accept `Event`.** One line in the
   root, and it changes the meaning of every relation for every adopter,
   including the ones that rely on the BFO continuant/occurrent disjointness the
   root states in a comment at line 103. Rejected in kind by `OVR-000387`
   already.
3. **Ontology anchors in the graph** (the design Luis already chose over the
   subject-edge rule). Larger, still open, and does not have to block option 1.

**Test.** A pipeline test that adds a grounded Event subclass and an
`EventParticipation` subclass to the harness fixture's own ontology bytes and
asserts one participation record admits, replays and exports. Run-05's
`test_pipeline.py::test_an_event_type_reaches_the_surface_and_one_event_record_is_admitted`
is the Event half of this; the participation half does not exist.

**Owner.** Harness owns the declared input list. Core owns the skill sentence
that currently points outside it. Design owns the anchors question.

---

## D-03. Run-02 is reported as ratified and is not

**Evidence.** The overseer journal's cell table reads
`run-02 | ... | ratified (E-0122, E-0123)`.
`paper-v4/evaluation-v4/review-record.preliminary.md` carries
`"status": "PRELIMINARY_COMPLETE"` and
`"ratification": {"evaluator_kind": "HUMAN_AUTHOR", "disposition": "PENDING",
"completed_at": "", "notes": ""}`. There is no `review-record.human.md` for
run-02. E-0122 says in terms that "the preliminary inspection staged under
`paper-v4/evaluation-v4/` has not been performed and Luis has not ratified";
E-0123 opens run-03 and says nothing about ratification.
`paper-v4/manuscript.md:153` still carries
`<!-- Replace the following sentence when the run-02 human ratification record
exists. -->`.

**Cost.** The state-of-stretch document the next agent reads asserts a
ratification the repository refuses. The manuscript sentence that depends on it
cannot be replaced, and the paper's only ratified v4 cell is run-05.

**Fix.** Correct the journal row to `preliminary, unratified`, or run the
ratification. If the preliminary record is to be ratified, note that its
`preliminary.evaluator_kind` is `CLAUDE_PRELIMINARY` while the run-02 input
manifest's declared kind is `CODEX_PRELIMINARY` — the same deviation E-0132
records for run-05.

**Test.** Extend `paper-v4/evaluation-v4/test_review_v4.py` with an assertion
that any cell the journal or the manuscript calls ratified has a
`review-record.human.md` whose `status` is `HUMAN_RATIFIED`.

**Owner.** Review.

---

## D-04. The manuscript of record is three cells behind, and nothing pins the two newest

**Evidence.** `paper-v4/manuscript.md` is version 1.4.0 and reports run-02 in
§4.2 and run-03 in §4.3 and B.4. Neither run-04 (admitted, replayed, queried,
review inputs frozen) nor run-05 (admitted, replayed, queried, review ratified,
E-0131 and E-0132) appears anywhere in it.
`paper-v4/test_publication_consistency.py` has tests pinning v2, v3, run-02 and
run-03 and no test for run-04 or run-05.

**Cost.** The paper of record omits its only ratified v4.1 cell and its
candidate cell of record. Every number in run-04 and run-05 is unguarded against
manuscript drift.

**Fix.** Manuscript 1.5, as the journal already plans: the matrix under the
final protocol, the v2 and v3 trials in the appendix. Add
`test_publication_claims_match_frozen_v4_run_05_results` in the shape of the
existing run-02 test before the prose lands, so the numbers are pinned as they
are written.

**Owner.** Manuscript.

---

## D-05. Manuscript §4.1 claims a code-drift property that is now false

**Evidence.** `paper-v4/manuscript.md:139`: "That reproduction holds at the
commit carrying this manuscript revision, and no file under the shipped
`malleus` package or under the fixture changed between that commit and the
coordinate the document run is pinned to, so the calibration and the document
run exercise the same implementation."
`git diff --name-only 4881b3a..HEAD -- src/malleus` returns four files:
`_contract_pipeline/document.py`, `_contract_pipeline/knowledge.py`,
`_contract_pipeline/population.py`, `inquisition/pack_grounding.py`. The fixture
is unchanged (`git diff --name-only 4881b3a..HEAD` over the fixture and
experiment directories returns nothing).

**Cost.** The sentence is the only thing joining the calibration to the document
run. It was true when written and is false at HEAD, and it will be false again
after every Core fix. Run-04 and run-05 are pinned to `8b806f7`, which is also
behind HEAD.

**Fix.** Re-pin the sentence to an explicit commit pair rather than to "the
commit carrying this manuscript revision", and state the delta when there is
one: the calibration reproduces at HEAD (verified below) and the document run is
pinned to an earlier coordinate whose difference is listed.

**Test.** `paper-v4/test_publication_consistency.py` asserting the named commit
pair and that `git diff --name-only <a>..<b> -- src/malleus` is empty, or that
its contents match a list the manuscript prints. Verified during this sweep:
`research/.../small_shop/public_population/test_run.py` passes at HEAD, 2 passed.

**Owner.** Manuscript, with a mechanical guard in the publication test.

---

## D-06. Manuscript §4.1 says the calibration plans are private; they are committed

**Evidence.** `paper-v4/manuscript.md:141`: "The plans are adopter-authored and
their format is private." `git ls-files` lists all five under
`research/ontology_driven_kg_realization/experiments/small_shop/public_population/plans/`:
`ret010.json`, `invoice-base.json`, `payment-e30.json`, `supplier-e4.json`,
`supplier-e7.json`.

**Cost.** The sentence hides the paper's best public evidence for deterministic
lowering. A reviewer asking "what does a plan actually look like" is told it
cannot be shown, and it is in the repository. The intended claim is almost
certainly that the *grammar* is a research contract
(`malleus.population-plan/private-v0`), not that the files are withheld.

**Fix.** "The plans are adopter-authored and their grammar is a research
contract, not a stable wire format; the five files are retained at
`research/.../public_population/plans/`." Snippet 22 in
`paper-v4/appendix-evidence/` is the artifact.

**Owner.** Manuscript.

---

## D-07. Four document-adapter refusal classes still fail fast, one item per return

**Evidence.** `src/malleus/_contract_pipeline/document.py`,
`adapt_document_assertions` lines 380-419: after the aggregated
`_locator_defects` pass, the per-assertion loop raises immediately on
`UNKNOWN_MODALITY`, `GAP_REQUIRED`, `UNKNOWN_FORMALIZATION_TARGET` (from
`_append_formalizations`) and `UNKNOWN_GAP_KIND` (from `_append_gaps`). Run-07's
terminal refusal was exactly this: `private/paper-v4-v4-run-07/launch-log.json`,
`population[2]`, reason `UNKNOWN_FORMALIZATION_TARGET`, detail
`missing formalization target: event:deep-earthquake:rc2-cluster:['event_type']`
— one target, terminal, with no return left.

**Cost.** One structural return per mispathed target. This is the failure class
`OVR-000395` fixed for grounding and for `UNDERIVED_FIELD`, and `OVR-000397`
fixed for `NOT_VERBATIM` and `UNKNOWN_BLOCK`. It is still open one layer over,
and it ended a cell.

**Fix.** Extend the existing `_Defect` / `_refuse_defects` machinery to the four
remaining reasons: collect them across the whole assertion loop, sort, and
render one refusal naming every offending assertion, target path and gap kind,
with the same trailing method sentence the locator refusal already carries.

**Test.** RED first: a capture with two bad formalization paths and one unknown
gap kind must produce one refusal naming all three. Nothing tests this today.

**Owner.** Core, document adapter.

---

## D-08. The pack-grounding rite still needs two refusals for one ill-formed schema

**Evidence.** `src/malleus/inquisition/pack_grounding.py`, the project branch
around lines 705-731: the loop collects shape `defects` and separately collects
classes with no grounding block into `missing`, then executes
`if defects: raise _refuse_defects(defects)` **before**
`if missing: raise ... DIRECT_ROOT_GROUNDING_REQUIRED`. A schema with one
malformed block and one ungrounded root reports only the malformed block; the
ungrounded root surfaces on the next attempt.

**Cost.** Two of the two permitted returns for one pass over one schema. This is
what closed run-03 (E-0124) and it is only partly fixed: shape defects now
aggregate among themselves, and missing roots aggregate among themselves, but
the two sets do not aggregate with each other.

**Fix.** Merge `missing` into the defect list as its own `_Defect` reason so one
refusal reports every ungrounded subject and every ill-formed entry with the
field set each position requires.

**Test.** RED first: a schema with one ungrounded root and one unclosed
vocabulary entry must produce one refusal naming both.

**Owner.** Core, inquisition.

---

## D-09. `producer-launch-log/v1` names four incompatible shapes

**Evidence.** All of `run-02`, `run-03`, `run-04`, `run-05` and the private
`run-06`, `run-07` launch logs declare
`"schema": "malleus.paper-v4.producer-launch-log/v1"`. Run-02's has
`launches`, `gate`, `population` and nothing else. Run-05's adds
`protocol`, `usage_cumulative`, `usage_by_resume`, `phase_two`,
`environment_note`, `citation_check` and a whole `query` block. Run-04's adds
`runner` (not `population`), a `shadow` attempt entry and a `core_10` block.
Run-07's adds `check_loops` and `citation_checks`.

**Cost.** No cross-cell reader can be written against the version string. The
cost table in the overseer journal cannot be recomputed from public files for
four of six cells, because only run-04 and run-05 publish
`results/usage.json`.

**Fix.** Either bump to `/v2` with a superset schema and a stated optional-key
list, or split the launch log into per-stage artifacts with their own schemas.
Publish `results/usage.json` for every cell that has one privately; the file
carries no reading text (run-04's and run-05's both measure 0 at 60 characters).

**Test.** A shared test over `paper-v4/experiment-v4/run-0*/results/launch-log.json`
asserting the declared schema's required key set, run once per cell.

**Owner.** Harness.

---

## D-10. Nothing checks the interpreter before a producer is spawned

**Evidence.** `src/malleus/_contract_compiler.py:1595` `_validate_versions`
refuses at compile time when `linkml` or `linkml-runtime` is not exactly the
profile's pinned version (`1.11.1` in
`src/malleus/_contract_compiler_profile.json`). No such check exists in
`paper-v4/experiment-v4/run-05/prepare_producer.py`,
`compile_ontology_candidate.py` or `run.py`, and
`paper-v4/environment/test_environment_lock.py` has three tests, none of which
inspects the running interpreter's resolved versions.

**Cost.** A run launched from the wrong interpreter spends the producer's
ontology-phase tokens and only then refuses at the gate. The journal records
this happening with the base conda python at `linkml-runtime` 1.10.0.

**Fix.** A four-line preflight in `prepare_producer.py` that reads the packaged
compiler profile and asserts the installed `linkml` and `linkml-runtime`
versions before it writes a workspace, refusing with the same message the
compiler would.

**Test.** `test_environment_lock.py` asserting that the executing interpreter's
`importlib.metadata` versions for `linkml`, `linkml-runtime` and `pypdf` equal
the pins in the lock.

**Owner.** Harness.

---

## D-11. Citation veracity has no gate anywhere, including the paper's own bibliography

**Evidence.** Downward: `private/paper-v4-v4-run-06/launch-log.json`,
`gate[1].review_flag_resolution`, `FABRICATED_CITATION`, found by a web search
outside the protocol after stage acceptance. Sideways: run-07's paired checker
listed two citations `UNVERIFIABLE` and the producer moved them to the honest
`none_found` form — the one thing the pair did catch
(`private/paper-v4-v4-run-07/launch-log.json`, `check_loops[0]`). Upward:
`paper-v4/test_publication_consistency.py::test_arxiv_citations_and_reproduction_coordinate_are_closed`
checks only that every `\citep` key resolves to a bibliography entry.
`paper-v4/recon/ledger.jsonl` has eleven events, all about the source PDF; the
fifteen state-of-the-art references have no retained verification receipt.

**Cost.** The paper reports a producer's fabricated standard as a finding while
its own bibliography carries two 2026 works whose verification exists only in an
overseer session. A reviewer who checks one will ask about the other.

**Fix.** Two steps, independent. (a) Make citation verification a named,
recorded step of the review stage, as `OVR-000397` fix 5 and E-0128 already
propose; run-04's and run-05's launch logs already carry a `citation_check`
block with a method and a finding, so the shape exists — promote it from an ad
hoc key to a required one. (b) Record the manuscript's own reference check in
`paper-v4/recon/`, one record per reference, with the access date and what was
seen.

**Test.** A publication test asserting that every bibliography entry has a
matching recon record; a per-cell contract test asserting `gate[*].citation_check`
is present with a `method` and a `finding`.

**Owner.** Review, plus the paper's own recon ledger.

---

## D-12. The withheld-artifacts record is not a complete index of what a run retained

**Evidence.** `paper-v4/experiment-v4/run-04/results/launch-log.json` names
`results/native-query-binding.draft-01.json` and
`results/native-query-binding.draft-02.json`. Neither path exists; both files
are at `private/paper-v4-v4-run-04/results/`, along with
`query-draft-01/` and `query-draft-02/` holding their query results and trace
summaries. `results/withheld-artifacts.json` lists eight withheld files and none
of these four.

**Cost.** For a paper whose gate excludes best-of-run selection, the discarded
candidates must be reachable by identity. Right now they are named at paths that
do not resolve and indexed nowhere.

**Fix.** Either publish the two drafts (both are type-only bindings; the drafts
must be leak-checked first) or list them in `withheld-artifacts.json` with their
digests and their private paths, and correct the launch log's paths.

**Test.** A contract test asserting that every path named anywhere in a cell's
launch log either exists publicly or appears in that cell's withheld list.

**Owner.** Harness.

---

## D-13. E-0131 records four witnesses; the artifact holds forty-four

**Evidence.** `paper-v4/paper-ledger.md:2874`: "the trace summary for their 4
witnesses is public". `paper-v4/experiment-v4/run-05/results/query-trace-summary.json`
carries `"witnesses_traced": 44` and 44 records with 44 unique record ids.

**Cost.** One digit in the ledger entry for the paper's only ratified v4.1 cell.

**Fix.** Correct the entry in place with a dated note; the ledger's convention is
correction rather than silent edit.

**Test.** A run-05 contract assertion tying `witnesses_traced` to the ledger
entry, in the shape of the existing
`test_the_paper_ledger_records_the_admitted_run`.

**Owner.** Ledger.

---

## D-14. The retained diagnostic is not the diagnostic the producer received

**Evidence.** `paper-v4/experiment-v4/run-05/ontology-run/attempt-01-diagnostic.json`
carries `"reason": "IMPORT_READER_REFUSED"` and nothing else.
`ontology-run/result.json` `attempts[0]` and `results/launch-log.json`
`gate[0]` both carry `chained_cause: "REJECTED_SOURCE: schema root contains
rejected field 'comments'"`, and the launch log's `harness_finding` says in terms
that "the diagnostic returned to the producer includes that chained cause
verbatim".

**Cost.** The frozen diagnostic artifact is not the artifact the experiment
describes returning. Any claim about what a producer saw has to be read out of
two other files.

**Fix.** `compile_ontology_candidate.py` should record the chained cause into the
diagnostic file itself, and the returned text should be the file's bytes.

**Test.** RED first: a gate invocation over a schema that trips
`SourceBoundaryRefusal` must write a diagnostic whose text contains the
`__cause__` string.

**Owner.** Harness.

---

## D-15. Two cells apply opposite dispositions to the same leak measurement

**Evidence.** Run-05 withheld `ontology-01.yaml`, `ontology-02.yaml` and
`validated-contract.json` because each shares a 60-character run with the
reading (`results/withheld-artifacts.json`, `shared_run_chars_at_least: 60`, the
note saying the run is the title and citation inside the schema description).
Run-03 publishes `ontology-run/ontology-0{1,2,3}.yaml` whole; measured during
this sweep they contain 14, 381 and 395 matching 60-character windows, justified
in E-0124 by locating every run in the article header or reference list. Run-04
publishes its two ontologies, which measure 40 (below the threshold).

**Cost.** The frozen threshold is applied mechanically in one cell and overridden
by a located-and-justified argument in another. A reviewer comparing cells sees
one cell's ontology and not another's, for reasons that are not the same rule.

**Fix.** Pick one rule and state it in the manuscript: either the threshold is
mechanical and run-03's attempts move to private with their digests public, or
the rule is "mechanical threshold, with a recorded exception when every shared
run is located in a title or reference list", and run-05's ontologies come back
with that exception recorded.

**Test.** A shared test over every cell asserting the disposition of each
artifact follows the stated rule, not a per-cell list.

**Owner.** Harness and manuscript.

---

## D-16. The leak rule is enforced per cell, not over the repository

**Evidence.** `run-05/test_contract.py::test_no_frozen_artifact_reproduces_the_reading`
iterates `FROZEN_ARTIFACTS`, the sixteen files that cell freezes. Nothing checks
anything else. A sweep of all 406 tracked files under `paper-v4/` at width 60
found twelve with a shared run: `manuscript.md` (28), `source-manifest.json`,
`recon/ledger.jsonl`, `recon/candidates/03-work-yu-2025.json`,
`paper-master-plan.md`, `paper-ledger.md`, `manuscript-v4-working.md`,
`arxiv/main.tex` and `experiment-v3/runs/claude-sonnet-5/ontology-run/attempt-01.raw.md`
(14 each), plus run-03's three ontologies. The 14-window files are all the
article title, which is a citation and is meant to be there.

**Cost.** Today the hits are benign. Nothing would catch a non-benign one in a
handover, a ledger entry or a manuscript paragraph, which are exactly the files
a person writes by hand.

**Fix.** One repository-level test that walks every tracked file under
`paper-v4/` and `handover/`, applies the same 60-character window check, and
asserts that any hit is on an allowlist that names the file and the reason.

**Owner.** Harness.

---

## D-17. `manuscript-v4-working.md` is not the restructure the journal describes

**Evidence.** The overseer journal says "Restructured the manuscript to 1.4.x".
`paper-v4/manuscript.md` carries `Version: 1.4.0 working draft`.
`paper-v4/manuscript-v4-working.md` is the older lean draft, last touched at
`ad7be7d`, still carrying eight bracketed placeholders
(`[TERMINAL RUN COUNTS, ...]`, `[FINAL CORE COORDINATE...]`). Every run
contract's `manuscript` block declares `of_record` as
`"1.2.1 on branch paper-v4-multimodel, tag paper-v4-multimodel-v2"`, pinned by
`run-05/test_contract.py::test_the_lean_draft_does_not_replace_the_manuscript_of_record`,
while `manuscript.md` on `main` is the successor of 1.2.1.

**Cost.** A reader following the journal to "the 1.4.x restructure" opens a stale
stub. `paper-v4/test_publication_consistency.py` guards `manuscript.md` for
`TODO`, `TBD` and `PLACEHOLDER` but not for `[BRACKETED FIELD]`, and
`manuscript-v4-working.md` is guarded by nothing.

**Fix.** Decide the roles once: if `manuscript.md` is the paper of record, update
the run contracts' `of_record` string and the test that pins it. Retire
`manuscript-v4-working.md` under `paper-v4/retired/` or delete its placeholders.

**Owner.** Manuscript.

---

## D-18. Review staging is inconsistent between cells, and run-04 asks for 240 row judgments

**Evidence.** Run-02's review package sits at `paper-v4/evaluation-v4/` root;
run-04's and run-05's at `paper-v4/evaluation-v4/run-0N/`. Row counts to judge:
run-02 73 (4 + 32 + 34 + 3), run-05 29 (2 + 5 + 9 + 13), run-04 240
(17 + 69 + 83 + 71, `run-04/review-task.md` lines 72-73). The review protocol
requires a locator and a rationale per row.

**Cost.** Run-04's review is eight times run-05's for one reviewer, and a large
share of its rows come from type pairs the exhaustive cross-product produced
rather than from question relevance — the same property that made draft-02 return
75 citation rows for CQ-04. Reviewer fatigue is a quality risk the protocol
cannot see.

**Fix.** Either sample with a recorded rule (the master plan already says
"ratification samples blocks"), or resolve D-01 in favour of a smaller
mechanically-derived binding. Move run-02's package into `evaluation-v4/run-02/`
so all three cells have one layout.

**Owner.** Review.

---

## D-19. Run-02 publishes no cost artifact

**Evidence.** `paper-v4/experiment-v4/run-02/results/` has no `usage.json`, and
run-02's `launch-log.json` has no usage keys. The journal reports 410,064
producer tokens for run-02; that figure lives in
`private/paper-v4-v4-run-02/usage.json`.

**Cost.** If the paper reports cost per cell, one cell of six has no public
number. Run-03, run-06 and run-07 are in the same position.

**Fix.** Publish `results/usage.json` for run-02 and run-03; both carry only
integers and stage names. Run-06 and run-07 have no public cell directory
content at all (see D-20).

**Owner.** Harness.

---

## D-20. Run-06 and run-07 have no public record

**Evidence.** `paper-v4/experiment-v4/run-06/` and `run-07/` contain the run
contract, manifest, spawn message (and run-07's checker message), the harness
scripts and tests, and `.gitkeep` files in `ontology-run/` and `results/`.
Everything both cells produced is under `private/paper-v4-v4-run-0{6,7}/`.
E-0129 and E-0130 record their outcomes and cite only private paths.

**Cost.** Two of six cells, including the entire paired-checker variant and the
fabricated-citation finding, rest on ledger prose with no public artifact.
Run-06's ontology was accepted at 2,216 facts and run-07's at 2,244; the
grounding receipts, population surfaces and gate diagnostics for both would
almost certainly measure 0 against the reading, as run-05's do.

**Fix.** Freeze the same public set the other cells carry: `ontology-run/result.json`,
the attempt diagnostics, the grounding receipt, the population surface, the
launch log and a withheld list, after a leak check. The refused runner attempts'
diagnostics belong in the public set too — they are the paper's negative cases.

**Test.** Each cell's `test_contract.py` already has a
`test_the_frozen_artifact_set_is_exact_and_digest_pinned` shape to copy.

**Owner.** Harness.

---

## D-21. The withheld-artifacts reason sentence does not match its own measurements

**Evidence.** `run-05/results/withheld-artifacts.json` says "Each file below
reproduces text of the selected reading. Only its identity is public." Two of the
eleven entries measure `shared_run_chars_at_least: 0`: `gaps.json` and
`history.jsonl`, the latter with a note explaining that the ledger stores the
reading JSON-escaped so the ladder cannot see it, and that it "is withheld by
contract, not by the measurement".

**Cost.** Small, and the note already tells the truth. The header sentence
overstates and a reviewer reading only the header will find two counterexamples
in the same file.

**Fix.** Change the reason to name both grounds: reproduces reading text, or
withheld by contract.

**Owner.** Harness.

---

## D-22. The coverage stop rule reads as a licence to stop early

**Evidence.** Every spawn message ends "Stop when another addition would require
invention." Run-05 reviewed 27 of 186 blocks
(`run-05/results/census.json`, `blocks_reviewed: 27`); run-02 and run-04
reviewed 186. The skill's step 6 says the opposite in terms: "coverage of the
retained reading is the objective, never the smallest query- or answer-changing
subset. This rule overrides the global 'smallest observation' ... rules for
document capture."

**Cost.** A five-fold difference in coverage between two cells whose only
declared variable is the producer model, with the stop rule as a plausible
confound. The journal already records the proposed fix and the master plan makes
it a precondition of the split-producer variant.

**Fix.** As the journal proposes: one sentence in the spawn message stating that
reviewing the next block is not invention. Note that this changes the spawn
message, which every cell's `test_contract.py` pins byte for byte against the
previous cell — so it opens a new iteration, not a patch to v4.1.

**Owner.** Harness, with a protocol-iteration decision.

---

## D-23. The gap vocabulary the working manuscript prints is not the closed set

**Evidence.** `src/malleus/_contract_pipeline/population.py:123-132` closes
`_GAP_KINDS` over six kinds: `AGGREGATE_ONLY`, `INTERVAL_NOT_EXPRESSIBLE`,
`MODALITY_NOT_EXPRESSIBLE`, `RELATION_ABSENT`,
`REQUIRED_FIELD_ABSENT_IN_SOURCE`, `TYPE_ABSENT`.
`paper-v4/manuscript-v4-working.md:129-131` enumerates five and omits
`REQUIRED_FIELD_ABSENT_IN_SOURCE`. Run-04 wrote 21 of exactly that kind.

**Cost.** Latent until run-04 enters the manuscript, at which point the printed
vocabulary and the observed counts disagree.

**Fix.** Print the closed set from the code, or print none and cite the code.

**Owner.** Manuscript.

---

# The three modelling questions, with pack-level options

These are the questions the journal names as awaiting Luis. Each is stated with
the evidence, then options that can be costed. No option is recommended by its
position in the list.

## M-1. Events as relation endpoints

Covered in full as **D-02** above, because it is also a harness defect. The
short form: `Relation.source_id` and `target_id` have `range: Entity`; the
`EventParticipation` mechanism that answers this already ships in
`ontology/profiles/object-event.yaml` and is already admitted by
`population.py`; the paper's producers cannot reach it because it is not one of
the eight declared inputs and the spawn message forbids reading anything else.

Options: (1) add the profile as a ninth declared input; (2) widen the root's
endpoint ranges, which contradicts `OVR-000387` and the root's stated
continuant/occurrent disjointness; (3) the anchors design, which is larger and
does not block (1).

## M-2. Hedges lost on the way into intervals

**Evidence.** `ontology/packs/metrology.yaml` slots `value_lower` and
`value_upper`, both `range: float`, the description of `value_lower` reading
"Lower bound, equal to value_upper for an exact value"; `uncertainty` is a bare
float; `determination` is `MEASURED | DERIVED | ESTIMATED | MODELLED`. There is
no field for approximation, for an open bound, or for a bound's closure.
E-0132 records the consequence: of run-05's five `PARTIAL` review rows, one is
"an approximate saturation pressure recorded as an exact closed interval with
empty uncertainty". Run-05's single typed gap is
`INTERVAL_NOT_EXPRESSIBLE` on an open lower bound; run-04 wrote 26 of them.

**Options.**
1. **One enum slot on the `Quantified` mixin**, say `bound_closure` with values
   `CLOSED`, `OPEN_LOWER`, `OPEN_UPPER`, `APPROXIMATE`, `AT_LEAST`, `AT_MOST`.
   Additive, one pack version bump, and it converts run-05's one
   `INTERVAL_NOT_EXPRESSIBLE` gap and run-04's twenty-six into representable
   values. It also lets a query distinguish "0.7" from "about 0.7", which the
   review currently has to do by reading the source.
2. **A free-text `quantity_hedge` slot** in the source's own wording, mirroring
   the doctrine `quantity_kind` already states ("Open on purpose: it is what the
   source said"). Cheapest, readable, and not comparable — the same trade the
   `quantity_kind` / `quantity_kind_class` pair already makes.
3. **Both, paired the way `quantity_kind` and `quantity_kind_class` are paired**:
   the source's hedge retained verbatim, plus the controlled closure. This is the
   shape decision 13 already set for quantity kinds, applied a second time.
4. **Leave it and keep counting the gaps.** Defensible: the gap is the paper's
   own point, and 26 machine-readable losses are a result. The cost is that the
   same loss recurs in every cell and the review keeps labelling rows `PARTIAL`
   for a representation limit rather than a support failure, which E-0132 already
   has to say in its non-claim.

## M-3. Imported values without attribution

**Evidence.** E-0132's `PARTIAL` rows include "an imported pore-pressure
threshold recorded without attribution" — a value the source quotes from another
work, admitted as if the source measured it. The `research` pack has the pieces
but not the join: `SourceAsserted` carries `assertion_modality`,
`assertion_locator` and `statement_sha256`, which point at the *reading block*
that carries the value, not at the *work* the value came from;
`ResearchRelationType` has `REPORTED_BY`; `BibliographicSource` exists as a
project class (run-02 admitted 80 of them). Nothing requires a value borrowed
from a citation to name it.

**Options.**
1. **A `value_provenance` enum on `Quantified`**: `THIS_WORK`, `IMPORTED`,
   `UNSTATED`. One additive slot, forces the distinction, does not say from
   where. Cheapest thing that makes the defect visible in a query row.
2. **A relation rule**: an observation whose value is imported must carry a
   `REPORTED_BY` relation to a `Source` or `BibliographicSource` record. No new
   slot — `ResearchRelationType.REPORTED_BY` already exists — but the rule cannot
   be mechanically enforced without a profile constraint, so it lands in the
   skill and the review, not in the compiler.
3. **A typed gap kind**, `IMPORTED_VALUE_UNATTRIBUTED`, added to `_GAP_KINDS`.
   Keeps the loss machine-readable without changing the packs, and fits the
   paper's existing story that what the vocabulary cannot carry is written down.
   Costs a Core change to a closed set, which every cell's pinned inputs then
   diverge from.
4. **Option 1 plus option 2**: the enum makes it visible, the relation makes it
   resolvable, and the review step checks the pairing.

**Related, same family.** The journal's third open modelling item — spatial
relations such as "beneath the segment axis" living in free-text `quantity_kind`
rather than in a relation — is the same shape of defect and made CQ-02 `PARTIAL`
for run-05. It is a project-ontology choice rather than a pack gap: the producer
had `GeospatialStructureRelation` available in run-04 and used a free-text field
in run-05. Worth deciding whether the metrology pack should refuse a
`quantity_kind` that names a spatial relation, or whether this stays an
adopter-modelling observation the census reports and nothing gates.

---

# What was verified and holds

Stated so the catalogue is not read as a list of everything being wrong.

- Run-02's manuscript numbers recompute exactly from the public artifacts: 329
  assertions (226 + 103), 186 of 186 blocks, 419 entities, 170 relations, 589
  records traced, 104 gaps in the four kinds reported, 126 witnesses, and 194 of
  589 records carrying an `assertion_modality` derivation.
- Run-04's and run-05's `reopen_matches_admitted` are true for both the receipt
  and the export; the admitted and replayed receipt digests are identical
  strings.
- The Small Shop calibration passes at HEAD (2 passed), and its evidence matches
  §4.1's counts: five change sets, one additive contract revision, 48 events,
  nine current and ten historical records, two contract identities.
- Run-04's twenty public artifacts are clean at the 60-character leak threshold,
  checked independently during this sweep.
- The active paper gate is 320 passed at HEAD.
- `_validate_versions` in `src/malleus/_contract_compiler.py` does enforce the
  pinned `linkml` and `linkml-runtime` versions at compile time. The environment
  defect in D-10 is the missing preflight, not a missing check.

---

# Deliverable 2

`paper-v4/appendix-evidence/catalogue.md` and
`paper-v4/appendix-evidence/snippets/` (25 files, each at most 40 lines with its
source path and commit in a header comment). The catalogue maps every mechanism
claim to its smallest public artifact and ends with eight claims that currently
have none.

Leak check over both deliverables and all 25 snippets, run the way
`paper-v4/experiment-v4/run-05/test_contract.py` runs it (`_reading_windows` at
width 60 against `private/paper-v4-text-layer/selected-reading.json`, whitespace
collapsed):

```
reading windows at width 60: 51528
files checked: 27   files with a shared 60-character run: 0
```

Every one of the 27 files reported `CLEAN`. No snippet was deleted.

---

# Landed while this sweep ran

Two commits arrived after the read coordinate and are reconciled here rather
than left to contradict the catalogue.

**`20614d4` Journal: run-04's 61 typed gaps read by cause.** The overseer's own
grouping of run-04's 61 gaps. It confirms and sharpens **M-2**: 25 of the 26
`INTERVAL_NOT_EXPRESSIBLE` gaps are one cause, an approximate value stored as an
exact bound pair, and the journal names the same remedy as M-2 option 1, "a
value qualifier on the metrology pack's quantity value (approximate, about, open
bound, exact)". It adds two items this sweep did not carry:

- **Event date precision.** One gap is a year-only date with nowhere to go,
  because the root's `Event.occurred_at` is a `datetime` while chronology's
  `TemporalExtent` already carries `temporal_precision`. Option: mix
  `TemporalExtent` into project Event classes, or state in the skill that a
  project Event subclass should carry it. Adjacent to M-1; does not depend on it.
- **No contribution-role vocabulary.** Two `TYPE_ABSENT` gaps for contributor
  roles. Option: a grounded role enumeration on the research pack's contribution
  relation, citing the CRediT taxonomy, which is a published NISO standard and
  therefore satisfies the grounding rite without an `invention_search`.

The journal's own reading is worth keeping in the paper: 13 of the 61 gaps are
the protocol working as designed, and run-02's 84 `AGGREGATE_ONLY` gaps against
run-04's 8 are not comparable as coverage because the derivation rule and the
packs changed between them.

**`55e3c0e` Manuscript: declare text-layer damage as a typed gap, not a repair.**
A new limitation paragraph in §4.5. It adds one entry to the "claims with no
retained public artifact" list in the catalogue:

> **D-24. The damaged-block count depends on an unstated detection rule.** The
> paragraph says "Twenty-seven of the 186 blocks carry a run like that". Counting
> blocks in `private/paper-v4-text-layer/selected-reading.json` that contain a run
> of single-character tokens, the answer is 49 at a run of four, 27 at five, 24 at
> six, 18 at seven and 13 at eight. The stated figure is reproducible, at exactly
> one threshold, which the manuscript does not give. **Fix:** state the rule in
> the sentence, or retain the detector and a per-block list as a public artifact
> the way the census is retained. **Owner:** manuscript. **Test:** a publication
> test that recomputes the count from the reading and asserts the printed figure.

Nothing else in this sweep is affected by either commit.

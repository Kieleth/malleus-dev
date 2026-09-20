# The paper rewritten around the results, 2026-09-11

Written by the Claude session that Luis asked, on 2026-09-11, to update the
paper with the latest results and to make it a results paper, not a history of
failures. His words: "I do not want the paper to be a 'historical' paper where
we relate our failures, I want the paper to be, here, here are the results of
how it works, check them out yourself." Robotics was to stay untouched while
it progresses. Nothing here is a decision of Luis's beyond that instruction;
the open items are listed at the end.

## What changed

`paper-v4/manuscript-v4-working.md` is rewritten. It remains the sole prose
and exhibit source of the submission candidate. Title unchanged.

The results are now the five cells of the record condition (run-20 to run-24)
and the three Small Shop fixtures, in that order of presentation: no model
first, model second. The previous manuscript reported run-20 and run-21 as
Capture A and B with 8 and 11 of 30 questions covered, then two Sol repairs
and one task-directed composition amendment. Those sections are removed. The
Sol conditions, the query corrections and the overnight fixed-ontology captures
are not mentioned; their records stay under `paper-v4/answer-demonstration/`
and in the ledger. Eighteen development cells (run-02 to run-19) are named
once as retained and unreported.

Main text 3,409 words after the first pass; 3,699 after the external review's
text fixes (the consistency test caps at 3,750 pending the budget ruling).
Eleven PDF pages after the fixes: five main, one references, five appendix.

Every number in the manuscript is read from a frozen file or a fresh run:

- Five-cell table: `ontology-run/result.json` (fact count, one attempt),
  `results/run-result.json` (graph, gaps by kind, reopen flags, census,
  records traced), `results/launch-log.json` (runner attempts),
  `results/usage.json` (tokens), and the review records under
  `paper-v4/evaluation-v4/run-NN/` (witness support, coverage, controls).
- Faithfulness: 1,293 witnesses across run-22 to run-24, 0 UNSUPPORTED, 17
  PARTIAL (6 in run-23, block boundaries; 11 in run-24, typing beyond the
  block); run-20 and run-21 under protocol v2, 417/17 of 434 rows and 471/19
  of 490 rows; 20 vocabulary URLs fetched, 0 fabricated.
- Coverage: 82, 92, 90 of 102 required elements; absences NOT_MODELLED 7/8/5,
  WITHHELD_STATEMENT 2/2/7, UNREACHED_RECORD 11/0/0; controls 4/4/5 of 5,
  computed from the question file each cell bound (v3 for run-22 and run-23,
  v3.1 for run-24).
- Small Shop: default admission 5 changes, 1 revision, 50 events, 9 current
  and 10 historical records, two runs byte-identical; partial shipments 8
  changes, 2 revisions, 71 events, 20 current records, remaining units 2, 1, 0;
  shipment policy 3 accepted changes, 32 events, one candidate VIOLATED with
  three witnesses and the ledger unchanged. All three run by this session
  today from the repository.

Appendix A exhibits come from run-23 (the highest-coverage cell): the count
row, the preferred-hypothesis row, the three unjoined composition rows and the
NOT_MODELLED coverage entry, the article row plus the TYPE_ABSENT gap for the
acceptance date, one PARTIAL witness, the CQ-C-01 control, and the identities
of all five cells. Source excerpts are quoted with attribution and block
locator (allowed for prose since E-0340). Appendix B prints one derivation and
the policy refusal from the Shop runs.

## Tests rewritten to bind the new manuscript

- `paper-v4/answer-demonstration/test_manuscript.py`: 22 tests. Each table row
  per cell is rebuilt from the frozen files and asserted present; admission,
  replay and provenance claims checked in every cell; faithfulness totals,
  absence table, controls, variance sentences and the token range recomputed;
  every Appendix A exhibit an exact subset of run-23's retained query result
  or its review record; exhibit locators resolve to the blocks named in
  prose; identities per cell present; no `E-0`, no `Sol`, no `run-02` to
  `run-19` anywhere in the text.
- `paper-v4/test_shop_calibration.py` (new, registered in
  `active-test-manifest.json`): runs the three Shop fixtures into temporary
  directories and compares the manuscript's rows and Appendix B exhibits with
  the fresh evidence; two default-admission runs compared byte for byte.
- `paper-v4/submission-candidate/test_prepare.py`: nine citations (Fahland
  added to `references.bib` and to the builder's citation map); the access
  test now covers the linked question files.
- `paper-v4/answer-demonstration/test_overnight.py`: the assertion that the
  manuscript links `OVERNIGHT-RESULTS.md` removed; the report-level phrases stay.
- `EVIDENCE-ACCESS.md` rewritten as a claim-to-file map for the new content.
- `template.tex` date set to 11 September 2026. `README.md` author-decision
  section rewritten.

Results of the checks run by this session: test_manuscript 22 passed;
test_shop_calibration 3 passed (31 s, SWI-Prolog present); test_prepare 9
passed; `prepare.py` build succeeded (TeX Live 2026); `verify_pdf.py`
TRANSCRIPTION_AND_ARCHIVE_PASS over 167 units and 10 exhibits; all ten pages
inspected as rendered images. The whole manifest gate
(`paper-v4/run_active_tests.py`), first run: pinned group 2 failed, 623 passed,
2 subtests; rest group 1,965 passed. The pinned-group rerun named one failure,
`test_overnight.py::test_new_condition_does_not_become_model_ranking_or_typed_composition`,
which required the manuscript to link the overnight Sol report; the second
failure of the first run did not recur and coincided with the manuscript being
rebuilt under the running gate. The overnight test's manuscript assertion was
replaced by a check that its report exists, with the reason in a comment. The
gate was rerun after that fix: pinned group 625 passed, 2 subtests passed;
rest group 1,965 passed. Green. After the two-binder report of run-22 (2026-09-12,
third build, twelve pages, manuscript sha256 0eb2a953…): pinned group 632
passed, 2 subtests; rest group 2,101 passed with one failure inside the
in-flight run-25 cell (its review-package test, expected red until that
agent's step 7 lands). After run-25 landed and was registered (fourth build,
twelve pages): pinned group 636 passed, 2 subtests; rest group 2,102 passed.
Green.

## Also found today, not paper work

The repository's default suite at HEAD 5937d8eb: 17 failed, 3,596 passed, 2
skipped. Six of the failures are in `tests/test_contract_compiler_historic_wire.py`,
with the cause "Current reader source differs at src/malleus/recon/store.py;
record a fresh measurement". The other eleven: seven in
`tests/test_contract_compiler_divergence.py` and four in
`tests/test_contract_compiler_duplicate_scan.py`, all retained-bytes and
source-identity checks of the contract-compiler tooling. Not investigated
further here. This is Core's, not the paper's; nothing in the paper gate
imports those modules.

## Executed from the external review (2026-09-11, second pass)

Items 2 (4.5 rewritten: the gate does not enforce faithfulness; the audit
found none unsupported), 6 (abstract reproducibility sentence; licence stated
from the article's own text, page 11 block 5), 7 (refusals are harness records,
the ledger is the history of acceptances), 8 (replay needs the pinned
implementation; ledger format evolution not addressed), 9 (related work:
nanopublications, trusty URIs, micropublications, SEPIO, Wikidata ranks, AIS,
ALCE; Nexus cited to Sy et al. 2023; PROV terms not emitted), 11 (support is
block-local; exempt record classes named; table 4.3 split into admission and
review tables; A.3 three-ranges note; A.4 locator note), the demotion of
first-attempt compilation out of the abstract and the NOT_MODELLED reframing
from item 3, and from item 1 the naming of the reviewer model (Claude Opus 5,
the producers' family) with the PENDING marker in the abstract. Also fixed on
the way: 4.7 said the protocol makes representations "faithful to its source";
now "auditable against its source". Tests: `test_manuscript.py` 27 passed
(admission and review table rows, earlier-protocol prose, reviewer model bound
to the private dispatch records); `test_prepare.py` 9 passed with sixteen
citations; build and `verify_pdf.py` green, eleven pages. Whole manifest gate
after the fixes: pinned group 630 passed, 2 subtests; rest group 1,965 passed.

## Todo after the external review (Luis, 2026-09-11: "execute the text-only fixes and add the rest to the todo list")

Executed in the manuscript on 2026-09-11: items 2, 6, 7, 8, 9, 11 of the
review, the abstract demotion and NOT_MODELLED reframing from item 3, and the
naming of the reviewer model from item 1 (text only). Remaining, in dependency
order; none is started:

1. **Run-22 rebind and re-review (review item 5).** Done 2026-09-12. Rebind
   under run-23's v4.13 binder on run-22's unchanged ledger (digest equal
   before and after): 4,917 cases, 6,960 rows over 457 witnesses (v4.12: 3,617
   cases, 5,414 rows, 449 witnesses); public record under
   paper-v4/experiment-v4/run-22/rebind-v4.13/. Two fresh Opus reviews of the
   same result, both retained under paper-v4/evaluation-v4/run-22-v413/:
   attempt 01 counted a required element as named by any returned row's
   fields and read 93 of 102 with controls 2 of 5 (three NONE-expected
   controls PARTIAL); Luis ruled option 1, a written clarification
   (review-task-v3-clarification-2026-09-12.md, the subject-tie rule, the
   reading the run-22/23/24 reviewers had applied) and a second fresh session:
   90 of 102, controls 5 of 5, 457 of 457 SUPPORTED. The paper reports run-22
   under both binders and the two readings. Derived CQ-C-03 labels under v3.1
   for run-22 and run-23: NONE, at paper-v4/evaluation-v4/derived-cq-c-03-v3.1.json. Re-bind run-22's frozen
   surface and type sets under the v4.13 binder, re-query the untouched
   ledger, one fresh review session for the newly reached rows under protocol
   v3, and report run-22 under both binders. Derive CQ-C-03's v3.1 label for
   run-22 and run-23 from the existing coverage entries. No dependency.
2. **Protocol v3.2 with a NOT_CAPTURED absence code (review item 4).** Luis,
   2026-09-11: to be designed properly, together with item 3, by an Opus agent
   under the malleus-dev skill; proposal file design/PAPER_EVALUATION_V32_PROPOSAL.md,
   decisions back to Luis in chat. Dispatched. Then re-code the 31 non-reach absences of run-22 to run-24
   from their recorded rationales into a derived file, frozen records
   untouched; at least six NOT_MODELLED entries are "slot exists, left unset"
   (run-23: CQ-T3-04, CQ-T3-05, CQ-T4-02, CQ-T4-03; run-24: CQ-T3-04, CQ-T3-05).
3. **In-context baseline (review item 10).** Designed with item 2 by the same
   agent; not built until Luis chooses an option. Same model, the selected reading
   in context, the thirty questions, answers with block citations; judged under
   the same v3 support and coverage protocol by the same review procedure.
   Adds what the gate costs and what it buys, both measured. No dependency.
4. **Fixed-ontology control (review item 3).** Done 2026-09-12 as cell run-25
   (Luis, 2026-09-11: "4 dispatch, is good control"). One fresh Opus
   population, question-blind, on run-23's accepted ontology (same digest,
   same 4,152 facts, same 10,063 binding cases), questions v3.1; producer
   dispatched 02:01:18Z, 384,287 tokens; 535 records (477 entities, 1 event,
   57 relations), 393 assertions, 186 of 186 blocks asserted, 14 gaps,
   admitted at runner attempt 1, 14 ledger events, reopen equal. Review under
   v3 with the subject-tie addendum: 500 of 505 SUPPORTED, 5 PARTIAL, 0
   UNSUPPORTED; positive 16 / 9 / 0; 93 of 102 reached; NOT_MODELLED 5,
   WITHHELD 4, UNREACHED 0; controls 5 of 5. Read: fixing the ontology moved
   the modelling (57 relations against run-23's 22), not the coverage (93
   against 92); no SUPPORTS or CHALLENGES relation from a sixth producer.
   Cell tests 104 passed; registered in the active manifest by the parent.
   Two returns to the reviewer: the review-package builder's witness count
   (see item 7) and three rationales quoting the source over 60 characters.
   Ledger entries for opening, freeze and review are the overseer's to write.
7. **Review-package builder defect (found by run-25).** The per-cell
   build_review_inputs.py takes witnesses_traced from query-trace-summary.json,
   which counts a record reached only as another row's subject; review.py
   counts row witnesses. Equal on run-22 to run-24, off by one on run-25
   (ratio:vp-vs). Run-25's copy is corrected; run-24's and the template still
   carry the old count. Fix in the template before the next cell.
5. **Independent-judge sample (review item 1).** Ruled 2026-09-11: the judge
   is Fable (Luis: "instead of human we use Fable in xhigh dispatch"), not
   Luis. A seeded random sample of witnesses stratified by cell, judged
   block-locally by a fresh Fable session blind to the recorded labels, with
   agreement and kappa reported beside the model totals. Tooling dispatched to
   an Opus agent (paper-v4/evaluation-v4/sample/). The sample is drawn after
   the run-22 rebind review lands. Note: the Agent tool pins the model, not
   the reasoning effort; the effort is recorded as the harness default, as for
   the producers, unless a way to pin it is found.
6. **Word budget.** Ruled 2026-09-11 (Luis: "forget 3500, those are
   guidelines not requirements"). The consistency test keeps only a floor.

## Rulings read from "let's continue" (2026-09-12) and what starts

Luis: "Add this evidence to v3.2 please to fix it there and let's continue
then." The subject-slot evidence is appended to design/PAPER_EVALUATION_V32_PROPOSAL.md.
"Continue" is read as adoption of the recommended options, restated in chat
so Luis can stop any: A3 re-code now with the four-case split (1a), v3.2 ships
with the baseline cell (2a), no recall audit (3a), a third surface kind for
the in-context baseline (4a), re-code run-23/24 now and run-22 as its v4.13
record lands (5a); sample: SUPPORTED-only random stratum plus all PARTIAL (6a),
200 (7), cells run-22 v4.13, run-23, run-24, run-25 (8a+b), one Fable judge
(9a), disagreement rate with binomial bound as headline (10a).

## Independent-judge sample, progress (2026-09-12)

Seed 20260912, cells run-22-v413, run-23, run-24, run-25. Stratum one: 200
random witnesses recorded SUPPORTED (51 / 47 / 46 / 56 by cell). Stratum two:
all 22 recorded PARTIAL (0 / 6 / 11 / 5). Two fresh Fable sessions, one per
packet, blind; dispatch log private/paper-v4-evaluation-sample/launch-log-20260912.json.
Stratum two judged and validated (VALID, 22 judgements): 18 PARTIAL agree, 4
moved to SUPPORTED by the judge (run-24: three `entity:q:*` quantity records;
run-25: `obs:fig3e-elevation-scale`), none to UNSUPPORTED. Kappa is undefined
or zero on a one-label stratum by construction, which is why this stratum is
reported as a list. Stratum one judged and validated (VALID, 200 judgements):
196 SUPPORTED agree, 4 moved to PARTIAL (one per cell: run-22-v413
claim:fixed-depth-rms-worse, run-23 obs:rc2-valley-width, run-24
entity:data:zenodo, run-25 obs:pore-pressure-trigger), 0 UNSUPPORTED.
One-sided 95 percent Clopper-Pearson upper bounds: 4.5 percent for
over-labelling (4 of 200), 1.5 percent for UNSUPPORTED (0 of 200). Both judge
records and the dispatch log copied to paper-v4/evaluation-v4/sample/ (they
pass the 60-character check by validation). Manuscript: new paragraph in 4.5,
abstract sentence replaced, one sentence in Section 7. Item 5 of the todo is
done; a human ratification remains possible on the same packets.

## Ruling 2026-09-12: the checklist technique for the protocol

Luis: "for protocol, let's embrace the checklist technique, like in aviation
or NASA: what is the check, what are the metrics/conditions to check, what is
the protocol behind each check. Rulebook is good, checklist is the technique
to assure that rules are verified and how." Applied to v3.2 as a `checklist`
section in the protocol file (check, condition or metric, procedure and
verifier, where the outcome lands) and as a numbered list the reviewer works
through in the instantiated task; a test binds every entry to a validator
function or a reviewer judgement that exists. Passed to the v3.2 agent as a
bounded addition. v3 untouched.

## Ruling 2026-09-12: run-26, and one full cell per protocol version

Luis: "we need yes, of course a run-26, we need one for each new version of
the protocol." Recorded as a standing rule in paper-v4/AGENTS.md. Run-26 is
the record condition (fresh Opus 5 authors and populates, question-blind,
harness v4.13, questions v3.1) reviewed natively under protocol v3.2: six
absence codes, the subject-tie rule folded into the task, the checklist
ticked by the reviewer. Opens when the v3.2 agent reports green, in parallel
with the baseline producer. Runs 22 to 25 stay frozen under v3 with the
derived re-coding beside them.

## v3.2 landed, run-26 and the baseline dispatched (2026-09-12)

The v3.2 agent finished green: gate 637 passed, 2 subtests (pinned) and
2,202 passed (rest). Delivered: review-protocol-v3.2.json (six absence codes
with definitions, stage identities per surface kind, the IN_CONTEXT_ANSWER_SET
surface, a normative 13-entry checklist C-01 to C-13 with condition, verifier
and outcome field per check); review.py dispatching on the version each file
declares, all four frozen v3 records validating byte-identical; the derived
re-coding absence-recoding-2026-09-12.json (41 absences: 6 no type or slot, 1
slot without entity, 5 name mismatch, 16 held as digest, 13 undecided with
the recorded code standing) and its 18 tests; the baseline harness
paper-v4/experiment-v4/baseline-01 (answer schema, validator, spawn message,
producer staging, contract, v3.2 review-package builder, 33 tests). One
answer-demonstration edit: selective_review.py's base identity became a
two-entry tuple so the live extension still reopens its 16 retained packets.
Two findings for Core: case (c) uses Core's own word rule; run-24 declared
bare-noun tags and still failed because the text layer glued "the melt".

Dispatched: the baseline producer (Opus 5, questions visible by design,
launch log private/paper-v4-baseline-01/launch-log.json) and run-26 (record
condition, harness v4.13, questions v3.1, reviewed natively under v3.2 with
the checklist; an Opus agent runs the cell including its producer and
reviewer sessions). Manuscript 4.6 carries the four-case split with a test.

## The baseline landed (2026-09-12)

Producer: one fresh Opus 5 session, the reading and the thirty questions,
no skill and no graph; 30 answers, 135 cited claims, 3 questions declared as
having no answer in the source, 127,303 harness-reported tokens; answer file
ACCEPTED by validate_answers (zero 60-character runs shared with the reading).
Review under v3.2 on the IN_CONTEXT_ANSWER_SET surface, one fresh Opus session
with the subject-tie rule and the checklist: validated on the first run; 130 of
135 claims SUPPORTED, 5 PARTIAL, 0 UNSUPPORTED; 24 of 25 positive questions
COVERED; 101 of 102 elements reached, the single absence NOT_CAPTURED
(CQ-T1-05 observing_system, an instrument the answers never named); controls 5
of 5; assembly NOT_APPLICABLE on every question as the protocol requires; all
thirteen checklist entries ticked, two of them re-measured by the reviewer
rather than taken on the task's word. Manuscript: new section 4.8 with the
four-column comparison, two sentences in the abstract and one in the limits;
tests bind every figure to the validated record, the answer file and the
launch log, and assert the four properties the answers do not have. Seventh
build, thirteen pages.

Producer-reported harness defects, both recorded in the baseline launch log
and unfixed: TASK.md names the input receipt one directory below where
prepare_producer.py writes it; and the producer wrote producer_model_id as
"claude-opus-5[1m]" where the contract declares "claude-opus-5", so a string
comparison between the two would not match.

## Gate after the baseline (2026-09-12)

Pinned group 639 passed with one failure of mine, now fixed: the isolated
gate's test pins the private-fixture list exactly, by design, so the two new
private trees (baseline-01 and the judge sample) needed a deliberate edit,
which is made with the reason in a comment. Rest group 2,295 passed with three
failures inside the in-flight run-26 cell (its pipeline tests: a Core-internal
name check and two carried-bytes checks), expected until that agent finishes.
Everything else green; the seventh build verified at thirteen pages.

## The two hypotheses from the baseline result (2026-09-12)

Luis, reading section 4.8: (a) Malleus should do better where the answer is a
specific high-precision number or string in one document; (b) the baseline wins
only because the document fits in context, so what about documents that do not.

(a) is measured and went into 4.8 as a per-tier table plus a precision
paragraph, no new session needed. Of 102 elements by tier, graph cells against
the answers: direct facts 12 to 16 against 15 of 16 (the best cell beats the
answers, question-blind); relationships 16 to 19 against 20 of 20; quantities
21 to 23 against 23 of 23, two cells losing nothing; qualifications 17 to 20
against 20 of 20; composition 20 of 23 in every cell against 23 of 23. So the
gap is the links, not the values, and it is uniform on composition. Precision
runs the other way: partial rate 22 of 1,806 witnesses (1.2 percent) for the
graph against 5 of 135 claims (3.7 percent) for the answers, three times, and
two of those five are numeric scope errors a typed field does not make. The
honest form of (a): parity on values, checkability the prose lacks, and the
graph achieves the parity question-blind.

(b) is not what this experiment tests. The reading is about 15,600 tokens and
fits in context with room to spare; the baseline still spent 127,303 tokens,
eight times the document. The real asymmetry is per-query cost: the graph is
built once (383,000 to 567,000) and its query region runs with no model at
all, while the baseline pays a full read per question set. Crossover at three
to four and a half question sets, which is arithmetic on measured costs and
not a measured result. Dispatched as the reuse-01 experiment: a second,
independently authored question set (prefix CQ-B-, authored blind to every
graph), put to run-23's untouched ledger by binding alone with no producer,
and to a fresh in-context session that pays a second full read; both reviewed
under v3.2; costs recorded per side. The multi-document case, the one that
actually answers (b), is held as the successor paper.

## Gate after the tier finding (2026-09-12)

Pinned group 642 passed, 2 subtests, no failures: the private-fixture pin fix
holds. Rest group 2,294 passed with four failures inside run-26's own contract
tests, the mid-build state (its result directories are no longer empty and its
review package is not yet frozen), the same sequence run-25 passed through.
Eighth build verified at fourteen pages.

## Run-26 landed, the first graph cell under v3.2 (2026-09-12)

Record condition, run-24's producer block byte for byte, harness v4.13,
questions v3.1; ontology accepted at attempt 01 (4,219 facts), admitted at
runner attempt 1, 14 ledger events, reopen equal, 186 of 186 blocks accounted,
11 gaps, 461,468 tokens. Graph 445 entities, 3 events, 152 relations. Query
7,039 rows over 547 witnesses. Freeze leak ladder 0.

Review under v3.2, validated at the first attempt: 545 of 547 SUPPORTED, 2
PARTIAL, 0 UNSUPPORTED; positive questions 19 COVERED, 6 PARTIAL, 0 NONE; 96 of
102 elements, the best of any cell; controls 5 of 5; all eleven text-layer
checklist entries ticked.

The result v3.2 was built for: NOT_MODELLED 0, NOT_CAPTURED 5. The five are a
repository name, a source study, a quantity subject and two evidence relations,
every one of them a place the accepted contract had and the producer did not
use. Under v3 all five would have read NOT_MODELLED. The paper's central
absence claim is now a coded fact rather than an argument.

Second finding from the same cell: 152 relations, seven times run-24's 21 and
nearly three times the control's 57, and the same three composition elements
lost as every other cell. Composition is 20 of 23 in all five graph cells. More
relations do not buy the one relation the composition questions ask for.

Manuscript: run-26 in both tables (the review table's fifth column now pairs
NOT_MODELLED with NOT_CAPTURED and reads "and no code" for the v3 cells), two
new paragraphs in 4.4, totals refreshed everywhere (elements 90 to 96, witnesses
2,353 with 24 partial, partial rate 1.0 percent against the answers' 3.7), the
tier table and 4.8 updated, and the reviewer's disclosed threshold in the
limits. Two claims of mine corrected against the files while integrating: the
abstract's audited total, and a sentence saying run-26 had the fewest partials
when the re-queried run-22 has none at all. 44 manuscript tests, ninth build,
fourteen pages.

Reviewer deviations on the record: it read the question file whole, so the
control expectations were in view, as run-22's, run-23's and run-24's reviewers
also did; and it counted an element carried in a record's name or scope field
as naming a semantic, where a stricter reading requiring the typed slot would
move three questions from covered to partial. Both are in the manuscript's
limits. Citation check: 3 terms unverified (QuakeML does not serve over TLS
under its cited name), 0 fabricated.

## The reuse experiment landed (2026-09-12); the amortization answer splits

Second question set (set B, 30 questions, 102 positive elements, authored by a
fresh Opus session blind to every graph and to set A), frozen at
paper-v4/experiment-v4/competency-questions-set-b.json. Put to run-23's frozen
graph by binding alone, no producer: 11,912 cases, 7,433 rows, 429 witnesses.
Ledger digest d5ef64c0... before and after, verified independently by the
overseer; run-23's directories clean in git. Put to a fresh in-context session
that paid a full read. Both reviewed under v3.2, both records validated first
time. Directories: paper-v4/experiment-v4/reuse-01 and reuse-01-baseline,
paper-v4/evaluation-v4/reuse-01 and reuse-01-baseline, RESULTS.md with ten
named confounds.

| | graph (run-23, set B) | in-context (set B) |
| elements of 102 | 88 | 101 |
| positives C/P/N | 15/10/0 | 24/1/0 |
| witnesses SUPPORTED/PARTIAL | 421/8 | 100/2 |
| controls matched | 2 of 5 | 5 of 5 |
| tokens for this set | 459,121 (review only) | 327,772 (producer + review) |

Three findings, two of them against us.

1. Amortization splits. Marginal: the graph paid zero producer tokens for the
   second set, five hand tool calls and about 100 seconds of query, against
   124,886 for a fresh read; run-23's build is 3.07 such reads, reproducing the
   manuscript's crossover. Total including review: 459,121 against 327,772, a
   ratio of 1.40 for less coverage, so the build never begins to repay. Whether
   review is a use of the graph or the measuring instrument decides which
   applies; both reported, neither netted.
2. Coverage is a property of (graph, question set), not of the graph. The same
   run-23 graph reached 92 on set A and 88 on set B; the baseline reached 101
   on both. The manuscript's "90 to 96" currently reads as a graph property and
   is not one.
3. The graph matched 2 of 5 controls because each of set B's three unanswerable
   controls names one element the reading does state about the control's own
   subject: the defect Luis fixed in set A at E-0346, repeated because the
   author was blind to set A. An instrument defect, not a fabrication. Related
   asymmetry: the answer grammar lets a producer declare a question unanswerable
   and zero its claims, so NONE is derived by construction; a graph has no
   per-question declaration, so the control comparison is not like-for-like.

Closed by the overseer: the reuse cell's two private input trees are declared
in active-test-manifest.json and in the pinned gate test. Gate after run-26's
integration: 647 passed, 2 subtests; 2,334 passed. Green.

Open, Luis's call, because it changes what the paper claims: report the reuse
result in full and revise 4.8's crossover sentence to what was measured
(recommended); or report only the marginal finding; or report it as a
limitation and drop the arithmetic; or hold it out on the instrument defect.

## Open for Luis

1. Ratify runs 22 to 24, or challenge them. The manuscript states PENDING.
2. Ledger entry for this rewrite (next free is E-0361). Not written by this
   session, to avoid a number collision with the robotics session, which was
   about to write E-0361 for L1.
3. Commit. Nothing is committed. The pathspec is: `paper-v4/manuscript-v4-working.md`,
   `paper-v4/answer-demonstration/test_manuscript.py`,
   `paper-v4/answer-demonstration/test_overnight.py`,
   `paper-v4/test_shop_calibration.py`, `paper-v4/active-test-manifest.json`,
   `paper-v4/submission-candidate/{prepare.py,test_prepare.py,references.bib,template.tex,README.md,QA.md,EVIDENCE-ACCESS.md,build-receipt.json,transcription-check.json,candidate-source.tar,main.tex,body.tex,appendix.tex,main.bbl}`,
   and this file. The PDF stays under `output/`, untracked.
4. Whether the shop-01 cell (a model given the Shop rows) enters the paper.
   Its review was frozen unvalidated under a row convention that was not
   declared (E-0201 to E-0204) and never re-reviewed under protocol v3; left
   out.
5. A robotics section when A4 lands. The manuscript has one sentence in the
   limits saying robotics is a candidate application.

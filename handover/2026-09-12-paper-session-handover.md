# Paper handover, 2026-09-12: read this first

Written to survive a session boundary. This is the resume point for the paper
front. The detailed chronology of the same work is in
`handover/2026-09-11-paper-results-rewrite.md`, which grew into the log; this
file is the state, the rulings and what to do next.

Nothing in this work is committed. See "Committing" at the end for the pathspec.

## One paragraph of where we are

The paper was rewritten on Luis's instruction from a history of failures into a
results paper. It now reports seven producer conditions on one article plus the
Small Shop fixtures, an independent judge on a sample of the review labels, and
an in-context baseline that prices the whole apparatus. The candidate PDF builds
and verifies at fourteen pages. Every figure in the main text is bound by a test
to a frozen file, a validated record or a fresh fixture run. What is not yet
settled is how to report the last experiment (reuse-01), the paper ledger
entries, and whether to commit.

## State of the artifacts

- Manuscript: `paper-v4/manuscript-v4-working.md`, sha256
  `702ade425df88e27776373ad7248bf0a59844f320293228f746aa48776bfa98c`,
  6,074 words of main text, 7,203 with appendices.
- Candidate PDF: `output/pdf/malleus-paper-v4-submission-candidate.pdf`, sha256
  `d1b80967b90db6ec91220f1fd5f7f2fb836be0bca485d64852d5a4addb1f6e13`,
  fourteen pages. Source archive sha256
  `f43ffc96806ef2df2fdaee3f45d89f940ad47d3ec1d2141996357e349ba76546`.
- Build: `python paper-v4/submission-candidate/prepare.py`, then
  `verify_pdf.py` from that directory. Both green. QA record in
  `paper-v4/submission-candidate/QA.md` (ninth build).
- Tests: `paper-v4/answer-demonstration/test_manuscript.py` 44 passed, binds
  every table row, total, exhibit and claim to its source file.
- Whole paper gate: `.venv/bin/python paper-v4/run_active_tests.py` ->
  `647 passed, 2 subtests` (pinned group, Core 160878cf) and `2334 passed`
  (rest). Green, re-run after this handover was written and unchanged.
- Repository default suite at HEAD: 17 failures, all in Core's
  contract-compiler tooling (`test_contract_compiler_historic_wire.py` 6,
  `_divergence` 7, `_duplicate_scan` 4). Not the paper's; no paper path
  imports them.

## What the paper now reports

Seven conditions on Yu et al. 2025, one article, 186 reading blocks:

| Cell | What it is | Elements of 102 | Controls |
| --- | --- | ---: | ---: |
| run-20, run-21 | record condition, earlier review protocol (4 questions) | not comparable | not applicable |
| run-22 v4.12 | record condition, first binder | 82 | 4 of 5 |
| run-22 v4.13 | same ledger, corrected binder, re-reviewed twice | 90 | 5 of 5 |
| run-23 | record condition | 92 | 4 of 5 |
| run-24 | record condition | 90 | 5 of 5 |
| run-25 | fixed-ontology control (run-23's ontology, new population) | 93 | 5 of 5 |
| run-26 | record condition, first graph cell under protocol v3.2 | 96 | 5 of 5 |
| baseline-01 | in-context, no Malleus, questions visible | 101 | 5 of 5 |

Plus: the three Small Shop fixtures as calibration with no model in the path;
the independent judge (Fable) on 200 SUPPORTED and all 22 PARTIAL witnesses;
and the derived four-case absence re-coding over the reported cells.

## The results that matter, and which are ours to own

1. **The gate is content-blind and the paper says so.** The digest check proves
   the cited sentence exists, not that the value follows from it. Zero
   UNSUPPORTED over 2,353 witnesses is a property of these producers observed
   through the gate, not a property of Malleus.
2. **Admission and replay are stable.** Every cell admitted, 14 ledger events
   each, reopen equals admission in all of them, every block accounted.
3. **The gap is the links, never the values.** Per tier: quantities 21 to 23 of
   23 (two cells perfect), direct facts up to 16 of 16 (one cell beats the
   baseline, question-blind), composition 20 of 23 in **every** cell. Run-26
   proposed 152 relations, seven times run-24's 21, and lost the same three
   composition elements. More relations do not buy the evidence relation.
4. **No producer ever used SUPPORTS or CHALLENGES**, which the research pack
   ships. Six producers, zero uses. Run-26's v3.2 review turns this from prose
   argument into a code: NOT_MODELLED 0, NOT_CAPTURED 5.
5. **Precision runs our way.** Graph partial rate 24 of 2,353 (1.0 percent)
   against the baseline's 5 of 135 (3.7 percent). All 24 graph partials are a
   record over-reaching its cited block (a boundary cut, or a type the block
   does not state). All 5 baseline partials are joins the block does not carry
   (an ordering, an identity, a reference, a disposition, and one arithmetically
   backwards magnitude comparison). The graph declines to compose and therefore
   cannot compose wrongly; the prose composes freely and every error it makes is
   a bad composition. A bad join propagates; an over-typed record does not.
6. **The baseline beats us on coverage and cost on one document.** 101 of 102
   at 127,303 tokens against 383,000 to 567,000 to build a graph. The paper
   states this plainly and prices what the graph buys instead: admitted state,
   replay, refusals, typed gaps.

## Findings from 2026-09-12 not yet in the paper

### The baseline is a best case, and we never tested degradation

Checked in `private/paper-v4-baseline-01/producer/TASK.md`: the producer had the
reading and the question file in its workspace at once and chose its own reading
order, then answered all thirty questions **in one pass** and wrote one file.

So the condition measured is the strongest possible form of in-context reading:
whole document present, all questions visible, single shot, fresh context,
nothing accumulated. Our comparison is therefore conservative, which is good,
and we have measured nothing about what happens outside that best case, which
must be said. Context rot is entirely untested by us because the session never
had a second turn.

**Action: state in the paper that 101 of 102 is a ceiling under ideal
conditions, not an operating figure.**

### The literature that grounds the degradation argument, already vetted here

All four are in `paper/paper.md` lines 379-384 and
`private/paper_thesis_April2026.md` lines 42-51, checked against primary sources
in April 2026. Use these rather than running our own experiment:

- **Du et al., EMNLP Findings 2025**, arXiv:2510.05381. 13.9 to 85 percent
  degradation from context length alone, *even with perfect retrieval*. The
  strongest one: a bigger document hurts even when the right passage is found.
- **Kuratov et al., BABILong, NeurIPS 2024**, arXiv:2406.10149. Models
  effectively use only 10 to 20 percent of their context. This is the
  thinking-budget argument, measured by someone else.
- **Liu et al., Lost in the Middle, TACL 2024**, arXiv:2307.03172. Over 30
  percent accuracy loss depending on position in the context.
- **Laban et al., ICLR 2026**, arXiv:2505.06120. 39 percent average drop
  multi-turn against single-turn, 200,000+ conversations. The
  repeated-questioning argument.

### Luis's reframe, 2026-09-12, verbatim in substance

Malleus is not competing for single-document accuracy against a fresh context
window. What it provides is *permanent semantic memory storage usable across
LLM sessions*, capturing a domain with some accuracy, whose connecting tissue
grows as the system is used. Two supporting observations of his: as the context
fills with the document, less remains for thinking, relationships and decisions;
and asking repeatedly on top of a loaded context should increase errors.

Read that way the single PDF is a calibration, not a disappointment: it
establishes the ceiling, our distance from it, and which failures are ours (the
missing joins) against the instrument's.

**Honesty check that must survive into the paper:** we cannot yet claim the
cross-session memory benefit, because we have not measured it. What is
supportable today is (i) the baseline is a best case, (ii) the four citations
for why that case does not persist, (iii) the contribution framed as permanent
cross-session memory, (iv) the named next experiments.

### The control defect is a pattern, not bad luck

The unanswerable controls have now been built wrong twice in the same way. In
set A the excluded-surface control carried an in-text semantic; Luis fixed it on
2026-09-06 (E-0346, questions v3.1). In set B all three unanswerable controls
name one element the reading *does* state about the control's own subject, so
the graph matched only 2 of 5. The second author repeated the mistake because it
was deliberately blind to set A and therefore to the lesson.

A ledger entry cannot stop a fresh author. **Proposed fix, unbuilt:** a
validator that, before a question set is frozen, takes every control question
and each of its required semantics and refuses the file if any is answerable
from the reading. Then run both existing sets through it and record how
defective each is. This is the checklist doctrine applied to question authoring.

Related asymmetry worth reporting: the answer grammar lets a producer declare a
whole question unanswerable and zero its claims, so NONE is derived by
construction; a graph has no per-question declaration. The control comparison
across the two surfaces is not like-for-like.

### The reuse experiment, and why its report is undecided

Second question set (set B, 30 questions, 102 positive elements, authored blind
to every graph and to set A), frozen at
`paper-v4/experiment-v4/competency-questions-set-b.json`. Put to run-23's frozen
graph by binding alone, no producer; and to a fresh in-context session.
Run-23's ledger digest `d5ef64c0...` verified identical before and after, and
its directories are clean in git.

| | graph (run-23, set B) | in-context (set B) |
| --- | ---: | ---: |
| elements of 102 | 88 | 101 |
| positives covered / partial / none | 15 / 10 / 0 | 24 / 1 / 0 |
| witnesses supported / partial | 421 / 8 | 100 / 2 |
| controls matched | 2 of 5 | 5 of 5 |
| tokens for this set | 459,121 (review only) | 327,772 (producer + review) |

Three findings, two against us:

1. **Amortization splits.** Marginal cost: the graph paid **zero producer
   tokens** for a second question set, five hand tool calls and about 100
   seconds of query, against 124,886 for a fresh read; run-23's build is 3.07
   such reads, reproducing the manuscript's crossover. Total cost including
   review: 459,121 against 327,772, ratio 1.40, for less coverage, so the build
   never begins to repay. Which applies depends on whether review is a use of
   the graph or the experiment's measuring instrument. In production nobody
   reviews. Both reported, neither netted.
2. **Coverage is a property of (graph, question set), not of the graph.** The
   same run-23 graph reached 92 on set A and 88 on set B; the baseline reached
   101 on both. The manuscript's "90 to 96" currently reads as a graph property
   and is not one. **This caveat is owed on every coverage figure in the paper.**
3. **The graph's 2 of 5 controls is the instrument defect above**, not a
   fabrication finding.

Full detail and ten named confounds: `paper-v4/experiment-v4/reuse-01/RESULTS.md`.

## Rulings Luis has given (all verbatim in substance)

- 2026-09-11: the paper is a results paper, not a history of failures. "Here are
  the results of how it works, check them out yourself."
- 2026-09-11: the 3,500-word figure is a guideline, not a requirement.
- 2026-09-11: robotics stays untouched while it progresses.
- 2026-09-11: the fixed-ontology control is a good control; dispatch it.
- 2026-09-11: the independent judge is Fable, not a human.
- 2026-09-12: on the run-22 control discrepancy, option 1, a written
  clarification plus a fresh review, rather than reporting two standards.
- 2026-09-12: adopt the checklist technique for the protocol. Rulebook is the
  rules; the checklist is how each rule is verified, with the check, its
  condition or metric, its procedure and its verifier.
- 2026-09-12: **one full graph cell for every new version of the protocol.**
  Recorded as a standing rule in `paper-v4/AGENTS.md`. Run-26 is that cell for
  v3.2.
- 2026-09-12: run both the free tier analysis and the reuse experiment.

## Protocol v3.2, what changed

File `paper-v4/evaluation-v4/review-protocol-v3.2.json`, frozen before the
baseline cell. v3 is untouched and every v3 record still validates byte for
byte; `review.py` dispatches on the version each file declares in its own
schema string.

1. Sixth absence code `NOT_CAPTURED`: the contract has a type or slot for the
   element and no record or field carries it and no gap declares it.
   `NOT_MODELLED` narrows to: the contract declares no type and no slot.
2. Stage identities declared **per surface kind**. The graph surfaces keep
   their seven keys; the answer surface requires three (answer file digest,
   producer model id, producer task digest) and is refused if it binds a ledger.
3. Third surface kind `IN_CONTEXT_ANSWER_SET`. A witness is one cited claim
   keyed by claim id. Witness counts are declared non-comparable across
   surfaces; assembly is declared not applicable.
4. A normative `checklist` of thirteen entries, C-01 to C-13, each with the
   check, the condition that passes it, what it reads, its verifier (validator
   function or reviewer judgement) and the field its outcome lands in. The
   protocol refuses an entry naming no verifier or an undeclared outcome field.

Design rationale and the options not taken:
`design/PAPER_EVALUATION_V32_PROPOSAL.md`, including the appended section
"Evidence added 2026-09-12: why subject slots are empty", which traces the
catalogue case end to end and states the four-case split v3.2 must derive.

## The subject-slot chain, since it came up three times

Run-23's uncertainty record has no subject. The chain, all from files:
the contract declares the slot; the producer **did** create the catalogue entity
(`work:eq-catalog`, a ReferencedWork, a legal subject since the slot's range is
Entity); the skill requires a subject's name or tag to occur as a word in the
formalizing sentence and the compiler refuses otherwise; the sentence says "the
final catalog" and the entity is named "earthquake catalog" with no tags, so the
check would have refused it. Both producers searched by names present in the
sentence rather than by what the record is about, because the census's
"attachable" rule became their search procedure. The rule is name-based because
Core-16's mechanical subject projection was wrong 13 of 15 times and was
withdrawn (Core-17, 2026-09-05). The missing half, handing each subject-less
record back to the producer to declare what it is about, is master plan item 12
from 2026-09-06 and was never built.

## Next experiments, in the order I would run them

1. **The control validator** (above). No model session. Closes a defect that has
   fired twice.
2. **Limits and framing rewrite**: the baseline as a ceiling, the four
   citations, Luis's reframe, the question-set dependence caveat. No model
   session. Needs his ruling on how to report reuse-01 first.
3. **The thinking-budget curve.** Partly computable from what we have: the
   document is ~15,600 tokens and the reader spent 127,303, so ~112,000 went on
   reasoning. Scale the document and it eats the window the reasoning needs.
   Measurable directly with the existing baseline harness at several document
   sizes.
4. **A corpus that does not fit in context.** A second document captured into
   the same graph, questions spanning both, a baseline that must re-read both or
   cannot hold them. This is the experiment that answers Luis's real question
   and it is a successor paper, not a section. It also finally tests composition
   across documents.
5. **RAG comparison.** Luis wants SOTA open-source RAG as the comparator. Do
   **not** design this from memory: run a recon pass first (the `malleus-recon`
   skill exists for it) to establish what is current, what benchmarks it reports,
   and whether any has a document-scale condition we can adopt rather than
   invent. Picking the wrong comparator is worse than having none.

## Open decisions for Luis

1. **How to report reuse-01.** Four options: in full with the crossover
   sentence revised to what was measured (recommended); only the marginal-cost
   finding; as a limitation with the arithmetic dropped; or held out on the
   instrument defect.
2. **The paper ledger.** Nothing written. **E-0361 is taken** by the robotics
   session (M3, the learning run, HEAD 6c738959), so the paper starts at
   **E-0362**. Entries owed: the run-22 rebind and both reviews; the subject-tie
   clarification; run-25; the judge sample; protocol v3.2 with its re-coding;
   run-26; the baseline; reuse-01.
3. **Committing.** Nothing is committed.

## Committing

Tracked files modified by this work:

```
paper-v4/AGENTS.md
paper-v4/active-test-manifest.json
paper-v4/answer-demonstration/selective_review.py
paper-v4/answer-demonstration/test_gate_integration.py
paper-v4/answer-demonstration/test_manuscript.py
paper-v4/answer-demonstration/test_overnight.py
paper-v4/evaluation-v4/review.py
paper-v4/manuscript-v4-working.md
paper-v4/paper-master-plan.md
paper-v4/submission-candidate/*  (EVIDENCE-ACCESS.md, QA.md, README.md,
  appendix.tex, body.tex, build-receipt.json, candidate-source.tar, main.bbl,
  main.tex, prepare.py, references.bib, template.tex, test_prepare.py,
  transcription-check.json)
```

New public paths to add:

```
design/PAPER_EVALUATION_V32_PROPOSAL.md
handover/2026-09-11-paper-results-rewrite.md
handover/2026-09-12-paper-session-handover.md
paper-v4/test_shop_calibration.py
paper-v4/experiment-v4/competency-questions-set-b.json
paper-v4/experiment-v4/{run-25,run-26,baseline-01,reuse-01,reuse-01-baseline}/
paper-v4/experiment-v4/run-22/rebind-v4.13/
paper-v4/evaluation-v4/{run-25,run-26,run-22-v413,baseline-01,reuse-01,reuse-01-baseline,sample}/
paper-v4/evaluation-v4/review-protocol-v3.2.json
paper-v4/evaluation-v4/review-task-v3-clarification-2026-09-12.md
paper-v4/evaluation-v4/absence_recoding.py
paper-v4/evaluation-v4/absence-recoding-2026-09-12.json
paper-v4/evaluation-v4/derive_cq_c_03_v31.py
paper-v4/evaluation-v4/derived-cq-c-03-v3.1.json
paper-v4/evaluation-v4/test_absence_recoding.py
paper-v4/evaluation-v4/test_derive_cq_c_03_v31.py
paper-v4/evaluation-v4/test_review_protocol_v32.py
```

Do **not** stage: `output/`, `tmp/`, anything under `private/`, the other
sessions' untracked files (`conformance/recon/`, the 2026-08-20 handovers, the
other `design/` files, `paper-v4/robotics-*.md`, `paper-v4/reentry-paper-plan.md`,
`paper-v4/sol-e2e-plan.md`, `research/neurosymbolic_aws_samples_recon/`).
Stage explicit paths only; never `git add -A`. The robotics session commits to
the same repository.

## Private trees, on disk and gitignored

`private/paper-v4-v4-run-25`, `run-26`, `run-22/rebind-v4.13` outputs under
`private/paper-v4-v4-run-22/rebind-v4.13`, `private/paper-v4-baseline-01`,
`private/paper-v4-reuse-01`, `private/paper-v4-reuse-01-baseline`,
`private/paper-v4-evaluation-sample`. All are declared in
`paper-v4/active-test-manifest.json` and in the pinned list inside
`paper-v4/answer-demonstration/test_gate_integration.py`; adding a private input
requires editing both, by design.

## Harness defects found and left unfixed

1. `baseline-01`'s task text names the input receipt one directory below where
   `prepare_producer.py` writes it. Both baseline producers had to find it.
2. A producer recorded `producer_model_id` as `claude-opus-5[1m]` where the
   contract declares `claude-opus-5`; a string comparison would not match.
3. The per-cell `build_review_inputs.py` took the witness count from the trace
   summary, which counts a record reached only as another row's subject;
   `review.py` counts row witnesses. Equal on run-22 to run-24, off by one on
   run-25. Run-25's and run-26's copies are corrected; run-24's and the template
   still carry the old count. Fix before the next cell.
4. Set B's controls (above).

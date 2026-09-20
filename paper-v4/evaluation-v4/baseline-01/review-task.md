# Malleus paper v4 source-grounded review task, protocol v3.2, in-context answer set

This is baseline-01's review task, written by
`paper-v4/experiment-v4/baseline-01/build_review_inputs.py` from the frozen v3
template at `paper-v4/evaluation-v4/review-task-protocol-v3.template.md`. Every
figure below is substituted from this cell's own frozen question file and answer
file; no placeholder survives instantiation.

Status: the method was frozen before the producer ran, at
`paper-v4/evaluation-v4/review-protocol-v3.2.json`. It is not edited for this
review. That file supersedes `review-protocol-v3.json` for cells opened after
it and changes three things:

- A third evidence surface kind, `IN_CONTEXT_ANSWER_SET`, whose locators are
  reading block ids like the text layer's and whose witness is one cited claim,
  keyed by its `claim_id`. There is no ledger, no replay receipt, no query
  binding and no trace on this surface, so there is no query result and the
  material you read in its place is the answer file.
- Stage identities are declared per surface kind. This cell binds three, and
  none of them is a ledger head: the answer file's digest, the producer's model
  id and the digest of the task the producer was given.
- A sixth absence code, `NOT_CAPTURED`, for an element the surface could carry
  and does not. On this surface it reads as "the answer set does not state it
  and declares no `NO_ANSWER_IN_SOURCE` for it".

**What this cell is.** It is not a Malleus cell. One fresh session was given the
selected reading and the thirty questions and asked to answer them in prose with
block citations. It ran no ontology, no compiler, no admission, no ledger and no
query. It is a baseline, and it exists to price what the typed path costs against
plain reading.

**One thing to hold on to while you judge.** This producer saw the questions.
Every graph producer was denied them. The comparison is tilted toward this cell
on purpose, which is what makes the result a price rather than a contest. Judge
this cell exactly as you would judge a graph cell; the tilt is the author's to
report, not yours to correct for.

You are a fresh Claude session performing the preliminary inspection. Record
your kind as `CLAUDE_PRELIMINARY`, which is the kind the protocol names; if you
are anything else, the substitution is recorded as a deviation in
`paper-v4/evaluation-v4/baseline-01/review-input-manifest.json`, which also binds
every input below by digest. Verify those digests before you begin. This is
AI-assisted preliminary work, not human evidence: Luis ratifies, and only a
record with status `HUMAN_RATIFIED` is evidence for the paper.

## What you judge

Two properties and nothing else: whether the block a claim cites supports that
claim, and which of each question's required semantics the answer's claims
carry. Do not calculate a score, construct a canonical answer, compare against
an oracle, judge the writing, or judge whether the answer is the one you would
have given.

Support is judged against the cited block and not the article around it. That
rule is unchanged from the graph cells, and it is the rule that makes the two
surfaces comparable on coverage.

## Inputs, exactly these

Every one of them is a material in the input manifest, bound by digest.

- `private/paper-v4-text-layer/selected-reading.json`, the selected reading. You cite its block
  identifiers, and it is the only surface that supports anything here.
- `paper-v4/experiment-v4/competency-questions-v3.1.json`, the questions and their `required_semantics`.
- `private/paper-v4-baseline-01/producer/work/answers.json`, the producer's answer file. This is what
  you read where a graph cell's reviewer reads a query result. Its grammar is
  `paper-v4/experiment-v4/baseline-01/answer-file-schema.json`, and it has
  already been checked against that grammar: every claim cites at least one
  block the reading declares, and no answer or claim reproduces the reading.
- `paper-v4/experiment-v4/baseline-01/spawn-message.md`, the message the producer was given.
- this task, the frozen protocol, the input manifest, the per-question review
  blocks in `paper-v4/evaluation-v4/baseline-01/`, and a copy of
  `paper-v4/evaluation-v4/baseline-01/review-record.blank.md`.

There is no query binding, no query result, no population trace, no query trace
summary and no retained capture in this cell, because no stage that produces one
ran. A manifest on this surface that bound one would be refused.

Do not open an answer oracle, a canonical answer, a prior score, a scorer, a
model transcript, another cell's population file or query result, a session log,
the manuscript, a result-bearing paper ledger entry, or any external source. The
source PDF is optional and may be opened only to cross-check whether the text
layer projected a passage faithfully; it is not a second evidence surface.

You have no network.

## What a witness is

One cited claim, keyed by its `claim_id`. The answer file carries, per question,
an answer text and a list of claims; each claim is one sentence-level assertion
with the reading blocks it rests on. The `claim_id` is the witness key you write
in the record, and the rows of a question are its claims in the file's order.

Two differences from a graph cell follow, and both matter:

- **No two claims share an identity.** On a graph surface two rows carrying the
  same `record_id` are one witness, judged once. Here, two answers stating the
  same fact carry two claim ids and are two witnesses. The witness count is
  therefore not comparable with a graph cell's, and the protocol says so. Only
  coverage of the authored elements is comparable.
- **Assembly is not applicable.** A prose answer always assembles, so the
  descriptor would be constant, and a constant token in a comparison table reads
  as a grade. Write `NOT_APPLICABLE` for every question; the validator accepts
  nothing else on this surface.

A question whose answer declares `no_answer_in_source` carries no claim and so
has no row. Its coverage entries all take an absent reason.

## How a witness reaches the surface

Directly. The claim names its own blocks in the answer file, and each of those
is a block id of the selected reading. Open the block, read it, and judge the
claim against it. There is no trace to look a witness up in and no locator to
resolve under a convention, because nothing was derived: the producer wrote a
sentence and named the blocks it read it from.

Cite in the record, for every witness, at least the blocks that claim itself
cites. The validator refuses a witness that omits one of them, because the claim
is judged against the block it rests on. You may cite more, when a neighbouring
block is what decides the judgement, and say so in the rationale.

## The checks, and where each applies

There is one check per witness on this surface, and it is the judgement itself.
The graph cells' mechanical checks do not apply here and you do not write their
tokens: there is no `resolution`, because there is no row to open; no statement
digest, because nothing binds a statement by digest; no derivation locality,
because no relation was derived; and no subject-present token, because there is
no subject slot.

Begin each `rationale` with the fact that decides it, in your own words, and
then the reason. Where a claim is broader than the block it cites, say which
part the block carries and which it does not; that is what separates `PARTIAL`
from `SUPPORTED` here.

One thing this cell cannot establish, and it is worth holding while you judge:
a prose answer can cite a block and still have been composed from the model's
memory of the article. Nothing in this cell excludes that. You judge whether the
cited block supports the claim, which is a different and smaller question, and
zero `UNSUPPORTED` here would not mean the answers were grounded.

## Judgments

Per witness, choose one `source_support`:

- `SUPPORTED`: the cited block supports every material claim in the statement.
- `PARTIAL`: it supports some but not all of it, or a needed qualifier is
  absent.
- `UNSUPPORTED`: it contradicts the statement or supplies no support for it.
- `NOT_EVALUABLE`: the allowed source surface is insufficient to decide.

Per question, you do not choose a label. You fill `coverage`: one entry per item
of that question's `required_semantics`, in the question file's order. For each
item, either name the `row_index` of a claim whose witness is `SUPPORTED` and
whose statement carries that item; or write `null` there and one
`absent_reason`:

- `NOT_CAPTURED`: the answer could have stated it and does not, and the answer
  declares no `NO_ANSWER_IN_SOURCE` for that question.
- `NOT_IN_SOURCE`: the reading itself does not state it.
- `NOT_MODELLED`: reserved for a surface with a contract; it does not arise
  here, since a prose answer has no type and no slot.
- `WITHHELD_STATEMENT`: the element is inside the answer's prose and no claim
  states it, so no witness carries it.
- `UNREACHED_RECORD` and `LOCATOR_NOT_RESOLVABLE` do not arise on this surface.

Then write the `question_responsiveness` the derivation produces:

- `COVERED`: every required semantic names a row.
- `PARTIAL`: some do and some are absent.
- `NONE`: none does.

The validator recomputes it and refuses a label its derivation does not produce.
Write the reason for the absences in `responsiveness_rationale`, in your own
words. Write `NOT_APPLICABLE` for `assembly` on every question.

Judge every claim exactly once, in order: 3 claims for `CQ-T1-01`, 4 for `CQ-T1-02`, 2 for `CQ-T1-03`, 3 for
`CQ-T1-04`, 1 for `CQ-T1-05`, 5 for `CQ-T2-01`, 5 for `CQ-T2-02`, 4 for
`CQ-T2-03`, 5 for `CQ-T2-04`, 5 for `CQ-T2-05`, 6 for `CQ-T3-01`, 6 for
`CQ-T3-02`, 5 for `CQ-T3-03`, 5 for `CQ-T3-04`, 7 for `CQ-T3-05`, 5 for
`CQ-T4-01`, 8 for `CQ-T4-02`, 5 for `CQ-T4-03`, 5 for `CQ-T4-04`, 5 for
`CQ-T4-05`, 6 for `CQ-T5-01`, 6 for `CQ-T5-02`, 7 for `CQ-T5-03`, 5 for
`CQ-T5-04`, 8 for `CQ-T5-05`, 0 for `CQ-C-01`, 0 for `CQ-C-02`, 0 for
`CQ-C-03`, 4 for `CQ-C-04`, 5 for `CQ-C-05`,
135 in all, over 135 distinct claims. Cite at
least one locator per witness and per question. Write each reason in your own
words. Copy no source passage into the record beyond the locator, and add no
numerical aggregate.

## Controls

Some questions in the file carry an `expected_outcome`. Review them exactly as
you review the others and do not read the field before you judge: it names what
a person will compare your coverage against afterwards. A `NOT_IN_SOURCE` or an
`EXCLUDED_SURFACE` control expects `NONE`, and a `PARAPHRASE` control expects
the same label as the question it names. The validator reports each outcome as
a finding and refuses nothing on it.

## The checklist

The protocol is the rulebook; this is how each rule is verified. Work the list
in order. Reproduce it in your handover note beside the record, with a tick and
one line per entry saying how it came out; the record's own key set is exact and
carries no tick. An entry the validator settles is still yours to read: the
validator refuses when it fails, and a refusal you did not expect is a finding.

1. **Every bound input is the bytes that were supplied** (`C-01`). Each
   material's sha256 equals the digest of the bytes handed to the validator,
   the record binds the manifest's digest in
   inputs.review_input_manifest_sha256, and the manifest binds the
   protocol's. Any difference refuses before a single judgement is read.
   Reads: review protocol, review input manifest, every declared material.
   Settled by the validator (review.validate_review_input_manifest).
   Outcome: `review.inputs.review_input_manifest_sha256`.

2. **The identities present are the ones this surface kind declares**
   (`C-02`). fixed_identities and stage_identities carry exactly the key
   sets required_keys_by_surface_kind names for the kind the manifest
   declares: seven ledger-side keys on a graph surface, three and no ledger
   head on the answer surface. A key more or fewer refuses. Reads: review
   protocol, review input manifest. Settled by the validator
   (review.validate_review_input_manifest). Outcome:
   `review-input-manifest.stage_identities`.

3. **Every locator resolves on the declared surface** (`C-03`). On
   SELECTED_READING_TEXT_LAYER and IN_CONTEXT_ANSWER_SET every cited locator
   is a block id the selected reading declares. On STRUCTURED_ROWS the
   locator opens in the source it names, at the row the declared convention
   numbers, and one that does not resolve is LOCATOR_NOT_RESOLVABLE and
   NOT_EVALUABLE by rule. Reads: review record, selected reading or the
   declared source files, review input manifest. Settled by the validator
   (review._check_locators). Outcome: `review.witnesses[].source_locators`.

4. **Support is judged once per distinct witness, against the cited evidence
   only** (`C-04`). review.witnesses judges every returned witness exactly
   once and no other; each carries one source_support token and cites the
   surface at least once. On IN_CONTEXT_ANSWER_SET a witness cites every
   block its own claim cites, so support rests on the cited block and not on
   the article around it. Reads: review record, query result or answer file.
   Settled by the validator (review._witnesses_v3). Outcome:
   `review.witnesses[].witness_key`.

5. **Whether the cited evidence supports the witness** (`C-05`). The
   reviewer opens the cited block or row and chooses SUPPORTED, PARTIAL,
   UNSUPPORTED or NOT_EVALUABLE, and writes the reason in their own words.
   The validator checks that the token is one of the four and never which
   one it is. Reads: the cited block or row, the witness's projected fields.
   Settled by the reviewer (review.witnesses[].source_support). Outcome:
   `review.witnesses[].source_support`.

6. **Every required element names a row or carries one absence code**
   (`C-06`). coverage names the question's required_semantics in the
   question file's order, and each entry either names the row_index of a row
   whose witness is SUPPORTED, or whose resolution is
   VALUE_DERIVED_FROM_ROW, or carries exactly one absent_reason from this
   protocol's six with a note. Naming both, or neither, refuses. Reads:
   review record, competency questions. Settled by the validator
   (review._coverage_v3). Outcome:
   `review.questions[].coverage[].absent_reason`.

7. **Which row carries a required element, or why none does** (`C-07`). For
   each required semantic the reviewer either names the row that carries it,
   or picks the one absence code that states why it is absent and writes
   why. NOT_CAPTURED is the code for an element the surface could carry and
   does not; NOT_MODELLED is only for a surface whose contract has no type
   and no slot for it. Reads: the returned rows or claims, the cited blocks
   or rows. Settled by the reviewer
   (review.questions[].coverage[].row_index). Outcome:
   `review.questions[].coverage[].row_index`.

8. **The question label is derived, never chosen** (`C-08`).
   question_responsiveness equals what the derivation from coverage
   produces: COVERED when every required semantic names a row, NONE when
   none does, PARTIAL otherwise. A stated label the derivation does not
   produce refuses. Reads: review record. Settled by the validator
   (review.derived_responsiveness). Outcome:
   `review.questions[].question_responsiveness`.

9. **Assembly is a descriptor and never a grade** (`C-09`). assembly is one
   of ONE_ROW, LINKED_ROWS or UNLINKED_ROWS on a graph surface and
   NOT_APPLICABLE on IN_CONTEXT_ANSWER_SET, and is never an input to any
   label the validator derives. Reads: review record. Settled by the
   validator (review._questions_v3). Outcome: `review.questions[].assembly`.

10. **Each control's outcome is compared with the expected one and refuses
   nothing** (`C-10`). For every question the competency file marks with an
   expected_outcome, the derived label is compared with NONE, or with the
   named question's label for a PARAPHRASE, and each comparison is reported
   as a finding. No control outcome refuses a record and none changes a
   judgement. Reads: review record, competency questions. Settled by the
   validator (review.control_outcomes). Outcome:
   `control_outcomes[].matched`.

11. **The producer's answer text does not reproduce the reading** (`C-11`).
   No answer text and no claim statement shares a run of sixty characters,
   after whitespace is collapsed, with any block of the selected reading.
   The reading is private and the answer file is published, so a file that
   quotes it is refused before any review package is built. Reads: answer
   file, selected reading. Settled by the validator
   (validate_answers.validate_answers). Outcome:
   `answer-file-validation.status`.

12. **The reviewer's own words do not reproduce the reading** (`C-12`).
   Every rationale and note is written in the reviewer's own words, copies
   no source passage beyond the locator and adds no numerical aggregate.
   Measured the same way as C-11: no run of sixty normalized characters
   shared with a reading block. Reads: review record, selected reading.
   Settled by the reviewer (review.witnesses[].rationale). Outcome:
   `review.witnesses[].rationale`.

13. **Claim ids are unique and every claim cites a resolving block**
   (`C-13`). Every claim_id in the answer file occurs exactly once, so no
   two claims share a witness identity and the witness count is a count of
   claims; and every block a claim cites is a block the selected reading
   declares. The per-question claim counts and the distinct-claim total
   equal the manifest's rows_per_question and witnesses_traced. Reads:
   answer file, selected reading, review input manifest. Settled by the
   validator (review._answer_set_witnesses). Outcome:
   `review.witnesses[].witness_key`.

## Recording

Copy `paper-v4/evaluation-v4/baseline-01/review-record.blank.md`, set `status` to
`PRELIMINARY_COMPLETE`, bind the input manifest digest in
`inputs.review_input_manifest_sha256`, fill `preliminary.actor_id` and
`preliminary.completed_at`, and leave the whole `ratification` block pending.
The per-question review blocks in `paper-v4/evaluation-v4/baseline-01/` carry each
question's claims and its required semantics; fill one and assemble them into
the record's `questions` array in the question file's order.

Then run the paper gate:

```
.venv/bin/python paper-v4/run_active_tests.py
```

and validate your own record with `validate_review` in
`paper-v4/evaluation-v4/review.py`, passing the v3.2 protocol bytes, the input
manifest, the competency questions, the selected reading, and the answer file as
`answer_set_source`. There is no `query_result_source` on this surface. It
checks identities, the claims against the reading, witness uniqueness and row
coverage, that every witness cites the blocks its claim cites, coverage against
`required_semantics` and the derived label. It never chooses or changes a
judgment. Hand the completed record to Luis for ratification.

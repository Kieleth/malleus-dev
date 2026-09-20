# Review checklist, protocol v3.2, reuse-01-baseline preliminary inspection

Handover note beside `review-record.preliminary.md`. The record's own key set is
exact and carries no tick; this file is where the ticks live. Worked in order.
One line per entry saying how it came out.

Actor: `actor:claude-preliminary-reuse-01-baseline`, evaluator kind
`CLAUDE_PRELIMINARY`. Surface kind `IN_CONTEXT_ANSWER_SET`.

- [x] **C-01 Every bound input is the bytes that were supplied.** I recomputed
  sha256 over all four declared materials, the protocol and the subject-tie
  clarification before reading a line of the answer file; every digest equals
  the one the manifest binds, and the clarification matches the digest the task
  quotes. The assembler bound the manifest digest into the record and the
  validator accepted it.

- [x] **C-02 The identities present are the ones this surface kind declares.**
  The manifest declares `IN_CONTEXT_ANSWER_SET` with three fixed identities
  (source, selected reading, competency questions) and three stage identities
  (`answer_file_sha256`, `producer_model_id`, `producer_task_sha256`). No ledger
  head, no query binding, no replay receipt. The validator accepted the key set.

- [x] **C-03 Every locator resolves on the declared surface.** All 102 witness
  locator lists and all 30 question locator lists were checked against the
  selected reading's 186 block ids before assembly; none was unknown. The
  validator repeated the check and refused nothing.

- [x] **C-04 Support is judged once per distinct witness, against the cited
  evidence only.** 102 witnesses, one per cited claim, keys and order identical
  to the answer file's claims, none judged twice. Each witness cites every block
  its own claim cites; I added a neighbouring block in three places only, and in
  each of those the rationale says why.

- [x] **C-05 Whether the cited evidence supports the witness.** Mine to settle:
  100 `SUPPORTED`, 2 `PARTIAL`, no `UNSUPPORTED`, no `NOT_EVALUABLE`. The two
  `PARTIAL` are claims that run past their cited block, one on a position
  descriptor the block does not carry and one on a size-of-gap figure the blocks
  do not state.

- [x] **C-06 Every required element names a row or carries one absence code.**
  121 coverage entries over 30 questions, in the question file's order, each
  carrying exactly one of the two. 108 name a row; 13 carry an absence code with
  a note. The validator accepted.

- [x] **C-07 Which row carries a required element, or why none does.** Mine to
  settle. Absence codes used: `NOT_IN_SOURCE` 8, `NOT_CAPTURED` 5. I read
  `NOT_CAPTURED` as the protocol's answer-surface gloss requires, for an element
  the reading does carry and this question's answer does not state.
  `UNREACHED_RECORD` and `LOCATOR_NOT_RESOLVABLE` do not arise here and were not
  used; `NOT_MODELLED` and `WITHHELD_STATEMENT` have no application on a prose
  answer and were not used.

- [x] **C-08 The question label is derived, never chosen.** I computed each
  label from its own coverage rather than picking one: 26 `COVERED`, 1 `PARTIAL`,
  3 `NONE`. The validator recomputed all thirty and refused none.

- [x] **C-09 Assembly is a descriptor and never a grade.** `NOT_APPLICABLE` on
  all thirty questions, left exactly as the blank blocks carried it. Not touched.

- [x] **C-10 Each control's outcome is compared with the expected one and
  refuses nothing.** The validator produced its findings and accepted the record.
  Per this cell's dispatch I did not read the `expected_outcome` fields, did not
  open the competency question file, and did not inspect or report the findings
  list. Nothing here is a control observation.

- [x] **C-11 The producer's answer text does not reproduce the reading.**
  Settled upstream before the review package was built, per the task. I re-ran
  the measurement anyway over all 30 answer texts and all 102 claim statements
  against all 186 reading blocks: no shared run of sixty characters after
  whitespace collapse. Clean.

- [x] **C-12 The reviewer's own words do not reproduce the reading.** Measured
  the same way over my 102 rationales, 30 responsiveness rationales and 13
  coverage notes, 145 texts in all: no shared run of sixty normalized characters
  with any reading block. No source passage is copied beyond the locator and no
  numerical aggregate is written into the record.

- [x] **C-13 Claim ids are unique and every claim cites a resolving block.** All
  102 claim ids occur once; every block any claim cites is a block the reading
  declares; the per-question claim counts equal the manifest's
  `rows_per_question` and the total equals its `witnesses_traced` of 102. Checked
  by me and again by the validator.

## Two things outside the list, recorded because they shaped judgements

**Sentences split at a block boundary.** The text layer's block rule cuts three
assertions in half. In each case the producer cited the block carrying one half.
I cited the continuation as the neighbouring block that decides the judgement,
said so in the rationale, and judged the claim on the two together:
`CQ-B-T1-05:c2` (the producer itself cited both halves), `CQ-B-T2-01:c5` and
`CQ-B-T2-03:c3`. A fact drawn from elsewhere in the article is a different case
and was never treated this way; where a claim needed one, the claim is `PARTIAL`.

**Deviations from the task, all four recorded in this cell's launch log as
instructions beyond the task.** I did not open the competency question file and
did not read any `expected_outcome`; the blocks carry every field I needed. I
opened no other cell, record or result. I did not edit, reorder or add to any
`rows` array. I did not run `paper-v4/run_active_tests.py`; the parent runs the
whole-experiment gate.

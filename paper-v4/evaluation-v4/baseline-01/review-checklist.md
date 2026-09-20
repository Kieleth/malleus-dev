# baseline-01 preliminary review checklist, protocol v3.2

The thirteen entries of the task's checklist, in order, with how each came out.
Reviewer: `actor:claude-preliminary-baseline-01`, kind `CLAUDE_PRELIMINARY`.
Record: `paper-v4/evaluation-v4/baseline-01/review-record.preliminary.md`,
status `PRELIMINARY_COMPLETE`, ratification left pending.

1. **C-01, every bound input is the bytes that were supplied.** [x] All seven digests recomputed with `shasum -a 256` before any judgement and each matched: the manifest itself (86a46ad5…), the protocol (5dfd59f4…), the selected reading, the competency questions, the answer file, the producer task, and the ruled addendum (2f897a0f…). The record binds the manifest digest in `inputs.review_input_manifest_sha256` and the manifest binds the protocol's; `validate_review` accepted both.
2. **C-02, the identities present are the ones this surface kind declares.** [x] The manifest declares `IN_CONTEXT_ANSWER_SET` and carries three stage identities, the answer file's digest, the producer's model id and the producer task's digest, with no ledger head. `validate_review_input_manifest` accepted the key set for that kind.
3. **C-03, every locator resolves on the declared surface.** [x] Every locator in the record is a block id the selected reading declares, on the 135 witnesses and on all 30 questions. `review._check_locators` raised nothing.
4. **C-04, support is judged once per distinct witness, against the cited evidence only.** [x] 135 witnesses, one per claim id, each judged once and none judged twice; each cites the surface at least once and each cites every block its own claim cites. `review._witnesses_v3` accepted.
5. **C-05, whether the cited evidence supports the witness.** [x] Reviewer-settled. 130 `SUPPORTED`, 5 `PARTIAL`, no `UNSUPPORTED`, no `NOT_EVALUABLE`. The five partials are CQ-T2-05:c3, CQ-T3-04:c5, CQ-T3-05:c6, CQ-T4-02:c1 and CQ-T5-01:c5; each rationale names the part the cited block carries and the part it does not.
6. **C-06, every required element names a row or carries one absence code.** [x] All 120 coverage entries name the required semantics in the question file's order and carry exactly one of a row index or an absence code with a note. `review._coverage_v3` accepted.
7. **C-07, which row carries a required element, or why none does.** [x] Reviewer-settled. 12 elements carry an absence code: one `NOT_CAPTURED` (CQ-T1-05, `observing_system`) and eleven `NOT_IN_SOURCE` across the three questions the answer declares no-answer-in-source for. No `NOT_MODELLED`, which this surface has no contract for.
8. **C-08, the question label is derived, never chosen.** [x] Every `question_responsiveness` was computed from the coverage entries and written as computed; `review.derived_responsiveness` reproduced all 30 without a refusal.
9. **C-09, assembly is a descriptor and never a grade.** [x] `NOT_APPLICABLE` on all 30 questions, which is the only token this surface accepts; `review._questions_v3` accepted.
10. **C-10, each control's outcome is compared with the expected one and refuses nothing.** [x] Five findings, all `matched: true`. CQ-C-01 and CQ-C-02 (`NOT_IN_SOURCE`) and CQ-C-03 (`EXCLUDED_SURFACE`) observed `NONE`; CQ-C-04 (paraphrase of CQ-T1-02) and CQ-C-05 (paraphrase of CQ-T3-02) observed `COVERED` against the same label on the question each names. The `expected_outcome` fields were not opened before judging; they were read only in the validator's findings afterwards.
11. **C-11, the producer's answer text does not reproduce the reading.** [x] Re-ran `paper-v4/experiment-v4/baseline-01/validate_answers.py` against the two frozen files: `status: ACCEPTED`, `verbatim_window: 60`, 30 questions, three declaring no answer in source, claim counts equal to the manifest's.
12. **C-12, the reviewer's own words do not reproduce the reading.** [x] Reviewer-settled and measured the same way as C-11: every rationale, every responsiveness rationale and every coverage note was run against the reading's 60-character normalized windows with `validate_answers.reading_windows` and `_shared_run`. No shared run. Four rationales were rewritten to drop source figures that had been restated; no numerical aggregate appears anywhere in the reviewer's prose.
13. **C-13, claim ids are unique and every claim cites a resolving block.** [x] `review._answer_set_witnesses` accepted: 135 distinct claim ids, every cited block declared by the reading, and the per-question counts and the distinct-claim total equal the manifest's `rows_per_question` and `witnesses_traced`.

No entry could not be ticked, and the validator refused nothing on the first
run of the completed record.

## Two reading decisions the task leaves to the reviewer

**Where a descriptor needs its own support.** Several claims carry a descriptor
the cited block does not state. I treated a descriptor that only identifies an
entity the block itself names as part of the reference and not a separate
material claim, and a descriptor that asserts a further fact about the article
as material. So naming a segment by its compass position, when the block names
that segment and gives its values, does not cost a claim its support; asserting
that a mechanism was set aside, that a reference is the one a calculation cites,
that a figure predates a processing step, or that initials stand for a named
person does, when the cited block carries none of it. The five partials are all
of the second kind.

**The addendum's subject tie.** Applied at CQ-C-01, where the reading names
sample sets for the carbon dioxide estimation and none for a sulfur and chlorine
measurement: the element is written `row_index: null` with `NOT_IN_SOURCE`, not
named from a sample set belonging to another subject. The three no-answer
controls carry no claims at all, so no row could have been named in any case.

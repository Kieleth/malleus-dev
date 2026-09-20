# reuse-01 preliminary review: the protocol checklist, worked

Handover note beside `review-record.preliminary.md`. Not part of the record.
Actor `actor:claude-preliminary-reuse-01`, evaluator kind `CLAUDE_PRELIMINARY`,
protocol v3.2, surface kind `SELECTED_READING_TEXT_LAYER`.

1. **Every bound input is the bytes that were supplied (C-01).** ✓ Each of the
   seven materials was opened at the path the manifest names and its sha256
   recomputed against the manifest entry; all seven matched, as did the
   protocol digest the manifest binds. The record binds the manifest digest the
   assembler computes from the same bytes. The validator accepted on this.

2. **The identities present are the ones this surface kind declares (C-02).** ✓
   The manifest declares `SELECTED_READING_TEXT_LAYER` and carries the three
   fixed identities and the seven ledger-side stage identities, no more and no
   fewer. Read, not edited. The validator accepted on this.

3. **Every locator resolves on the declared surface (C-03).** ✓ Every locator
   written in this record is a block id the selected reading declares. The
   capture uses 184 of the reading's 186 blocks; the two it does not use are the
   ones the capture itself lists as nothing-assertable. No locator failed to
   resolve, so no witness took `LOCATOR_NOT_RESOLVABLE` and none was
   `NOT_EVALUABLE` by that rule.

4. **Support is judged once per distinct witness, against the cited evidence
   only (C-04).** ✓ 429 witnesses judged, one entry each, which is every
   distinct key the 7433 returned rows carry and no other. Each entry cites at
   least one block. Witness keys were resolved through the query trace summary
   by `record_id` or `relation_id`, never by list position; all 429 resolved and
   the trace carries no key the result does not return.

5. **Whether the cited evidence supports the witness (C-05).** ✓ 421
   `SUPPORTED`, 8 `PARTIAL`, no `UNSUPPORTED`, no `NOT_EVALUABLE`. The rule I
   applied, stated once here because it decides all eight: a witness is
   `SUPPORTED` when every material claim on the row is stated by, or follows
   directly from, text inside a block that witness cites; `PARTIAL` when part of
   the row's content is carried by the cited blocks and part of it is completed
   only outside them. Seven of the eight are block-boundary cases where the
   sentence the record rests on begins or ends in a neighbouring block the
   witness does not cite; the eighth records a proxy the cited block does not
   name. The eight are `obs:depth-uncertainty-bound`,
   `gchem:rc2-co2-primary-calc`, `gchem:rc3-co2-primary-calc`,
   `claim:occ-exhumed-mantle`, `claim:acknowledgement-discussions`,
   `claim:fixed-depth-rms-worse`, `claim:max-depth-not-following-relationship`
   and `claim:volatiles-reduce-solidus`. None of them is named by a coverage
   entry, so none of them moves a question label.

   The three per-witness tokens, all computed rather than judged: statement
   digest recomputed for the 236 witnesses whose record binds a statement, all
   `DIGEST_OK` and no mismatch; the remaining 193 carry no such binding and say
   so. Derivation locality checked for all 14 `RELATION` witnesses against the
   blocks that derive their endpoints: all 14 `DERIVATION_LOCAL`. Subject
   presence checked for all 96 `SUBJECT` witnesses: the subject's name or one of
   its tags occurs in a block the derivation reaches in every case, so all 96
   are `SUBJECT_IN_BLOCK`; the 319 `ENTITY` witnesses project no subject and are
   `NO_SUBJECT_IN_ROW`.

6. **Every required element names a row or carries one absence code (C-06).** ✓
   121 coverage entries, one per required semantic in the question file's order
   as the blocks carry it. 96 name a row; 25 carry exactly one absence code with
   a note. None carries both and none carries neither. Every named row's witness
   is `SUPPORTED`.

7. **Which row carries a required element, or why none does (C-07).** ✓ The 25
   absences: 8 `NOT_IN_SOURCE`, 7 `NOT_CAPTURED`, 6 `WITHHELD_STATEMENT`, 2
   `NOT_MODELLED`, 2 `UNREACHED_RECORD`, 0 `LOCATOR_NOT_RESOLVABLE`. The
   retained capture's own declared gaps decided two of the codes rather than my
   reading: the editorial dates take `NOT_MODELLED` because the capture declares
   in that same place that the contract has no type and no slot for them, which
   is also what rules out `NOT_CAPTURED` for them. `WITHHELD_STATEMENT` was used
   only where the element survives inside a statement a returned record binds by
   locator and digest. `NOT_CAPTURED` was used where the reading carries the
   element only as a citation number, or not in any field, and no gap declares
   the omission.

8. **The question label is derived, never chosen (C-08).** ✓ Each label was
   computed from the coverage array and not picked: 15 `COVERED`, 15 `PARTIAL`,
   0 `NONE`. The validator recomputed all thirty and refused none.

9. **Assembly is a descriptor and never a grade (C-09).** ✓ One descriptor per
   question from the three the graph surface allows: 20 `UNLINKED_ROWS`, 7
   `ONE_ROW`, 3 `LINKED_ROWS`. `LINKED_ROWS` was written only where a relation
   the query result returns joins two of the rows the coverage names.
   No descriptor was an input to any label.

10. **Each control's outcome is compared with the expected one and refuses
    nothing (C-10).** ✓ Settled by the validator, which accepted the record. I
    did not read the competency question file and did not read the findings
    list, so I state nothing about which questions are controls or how their
    comparisons came out. The question file's bytes were passed to the
    validator, which is what the comparison runs on.

11. **The reviewer's own words do not reproduce the reading (C-12).** ✓ All 484
    rationales and notes were checked mechanically against all 186 reading
    blocks after normalising case, punctuation, ligatures and accents: no run of
    sixty normalised characters is shared with any block. No source passage is
    copied beyond the locator and no numerical aggregate is added.

## Two things worth the ratifier's eye

- **The gate was not run.** The task's Recording section says to run
  `paper-v4/run_active_tests.py`; the dispatch waived it for this cell because
  another cell of the experiment is in flight. The record was validated with
  `review.validate_review` and nothing else.
- **Eight `PARTIAL` witnesses are a text-layer artefact, not a modelling
  fault.** Seven of the eight arise because the selected reading's block rule
  splits a sentence across two blocks and the producer's derivation cites only
  one of them. If that reading is re-blocked, those seven would resolve. They
  are recorded as they stand.

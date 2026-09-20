# run-26 review checklist, protocol v3.2

Worked in order by the preliminary reviewer (`CLAUDE_PRELIMINARY`) before and
during the judgements. One line per entry of the checklist rendered in
`paper-v4/evaluation-v4/run-26/review-task.md`. The record's own key set carries
no tick; this note carries them.

1. **C-01, every bound input is the bytes that were supplied. [x]** All seven
   materials the manifest lists were hashed with sha256 before any judgement and
   every digest equals the manifest's. The protocol file hashes to the digest the
   manifest binds. The manifest itself hashes to
   `sha256:513351036975caf90e2845820b4b9a7364d3502f6a216ec45df15ecd3bda7a64`,
   which is the value `inputs.review_input_manifest_sha256` takes. The
   clarification file the task quotes the subject-tie rule from also matches the
   digest printed in the task.

2. **C-02, the identities present are the ones this surface kind declares. [x]**
   The manifest declares `SELECTED_READING_TEXT_LAYER`. `fixed_identities` carries
   exactly the three keys the protocol names for that kind and `stage_identities`
   exactly the seven, ledger head included. Nothing more, nothing fewer. Confirmed
   again when the assembled candidate record passed the validator.

3. **C-03, every locator resolves on the declared surface. [x]** Every locator in
   the 547 witness entries and in the 30 question blocks is a block id the
   selected reading declares; checked mechanically against the reading's own block
   ids, no exceptions. No witness carries a `resolution` key, which is right for
   this surface kind, and no locator was unresolvable, so the
   `LOCATOR_NOT_RESOLVABLE` rule never fired.

4. **C-04, support is judged once per distinct witness. [x]** The rows return 547
   distinct witnesses over 7039 rows; each is judged exactly once and no other
   witness is judged. The query trace summary traces 552 records; the five no row
   takes as its own witness (`material:ba`, `material:basalt`, `material:co2`,
   `material:melt-inclusions`, `material:rb`) are left alone. Every entry carries
   one support token and at least one locator.

5. **C-05, whether the cited evidence supports the witness. [x]** 545 SUPPORTED,
   2 PARTIAL, no UNSUPPORTED, no NOT_EVALUABLE. The two partials are
   `agent:geli`, whose cited block begins part way through the acknowledgement and
   carries the surname while the initial the record projects sits in the block
   before it, and `rel:rainbow-at-ntd`, whose block places the massif at a
   non-transform discontinuity without saying which one while the row names a
   particular one as the target endpoint. Every record that carries
   `assertion_locator` and `statement_sha256` was digest-checked: 232 witnesses,
   232 DIGEST_OK, no mismatch. The other 315 carry no statement digest, so their
   rationale opens with the locality or subject token instead. Locality on
   relations: 110 DERIVATION_LOCAL, 1 DERIVATION_NON_LOCAL
   (`rel:melt-from-mantle`, formalized in a block that derives neither endpoint;
   stated as a fact, not used to lower support). Subject tokens: 116
   SUBJECT_IN_BLOCK, verified by finding the subject's own name or one of its
   recorded wordings in the block, and 320 NO_SUBJECT_IN_ROW for projections that
   carry no subject at all.

6. **C-06, every required element names a row or carries one absence code. [x]**
   Each question block carries one coverage entry per item of that question's
   `required_semantics`, in the question file's order, and each entry names a
   `row_index` or exactly one `absent_reason` with a note, never both and never
   neither. Checked mechanically; the validator agreed.

7. **C-07, which row carries a required element, or why none does. [x]** 17
   absences over 6 questions and 3 controls: 5 NOT_CAPTURED, 1
   WITHHELD_STATEMENT, 11 NOT_IN_SOURCE. NOT_MODELLED is not used anywhere in this
   cell; every absence outside the controls is an element the accepted contract
   has a place for. The NOT_CAPTURED calls were made against
   `paper-v4/experiment-v4/run-26/ontology-run/validated-contract.json` and its
   `population-surface.json`: the dataset type's description and locator slots for
   the repository name, the research relation types the run already uses for the
   tie to a source study and for a supporting link, and the observation's subject
   slot for what an average describes. The single WITHHELD_STATEMENT is the
   comparison between the two segments in CQ-T5-02, which survives only in the
   sentence both quantity records bind by locator and digest.

8. **C-08, the question label is derived, never chosen. [x]** 21 COVERED, 6
   PARTIAL, 3 NONE. Each label was written as the derivation from its own coverage
   produces it, and the validator recomputed all thirty without refusing any.

9. **C-09, assembly is a descriptor and never a grade. [x]** ONE_ROW on 8
   questions, LINKED_ROWS on 2, UNLINKED_ROWS on 20. No label anywhere was moved
   by it; the descriptor was written after coverage was settled.

10. **C-10, each control's outcome is compared with the expected one. [x]** The
    validator reported all five control outcomes as findings and all five matched:
    CQ-C-01 and CQ-C-02 NONE against the expected NONE, CQ-C-03 NONE against the
    expected NONE for the excluded surface, CQ-C-04 COVERED equal to CQ-T1-02, and
    CQ-C-05 COVERED equal to CQ-T3-02. **Deviation to report:** the task says not
    to read `expected_outcome` before judging, and the competency question file
    was read whole in one pass at the start, so those fields were in view before
    the five controls were judged. The coverage for the controls was nonetheless
    derived from the returned rows and the subject-tie rule, and the reasoning is
    written out in each note; a reader who wants the control free of that exposure
    should re-judge the three NONE controls.

11. **C-12, the reviewer's own words do not reproduce the reading. [x]** Every
    rationale and every note was checked against every block of the selected
    reading for a shared run of sixty normalized characters. None was found. No
    record name, bibliographic title or source value is quoted in any rationale,
    and no numerical aggregate appears in the record; the counts in this note are
    here and not there.

## Not done here

The paper gate (`paper-v4/run_active_tests.py`) was not run and the record itself
was not assembled or written: the spawn instruction leaves assembly and
validation to the overseer and forbids writing any file beyond the witnesses, the
thirty question blocks and this note. As a self-check only, a candidate record was
assembled in the session scratchpad from the blank, the witness entries and the
thirty question blocks and passed `validate_review` against the v3.2 protocol
bytes, the input manifest, the query result, the competency questions and the
selected reading, with the five control findings above. That candidate is not in
the repository.

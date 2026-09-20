# Root-cause analysis: the third case of the Shop reconsideration experiment

Every defect and incident from paper ledger E-0469 to E-0480, plus two carried
in from the second boundary that this case closed or inherited. For each: what
happened, how it was found, the root cause, the class of error, the guard now in
place or the gap where none is, and whether it could have reached a result.

Then the causes that cut across several of them, then what worked and why, then
proposed learnings for the `malleus-paper` and `malleus-dev` skills. The
proposals are candidate text for Luis to accept or refuse. **No skill file is
edited by this document.**

Every claim cites a ledger entry, a D0-REPORT.md addendum, a test name, or a
file with its digest. Nothing here is written from memory.

Public file. Ids, slots, mechanisms, counts and digests only; no passage of the
Shop chapter's prose.

## Scope note on names

The harness calls the three producer sessions stages A, B and C. Here they are
the **table population**, the **second boundary** and the **third boundary**;
the letters appear only inside file paths and test names.

## Summary

| # | defect | found by | class | guard | could it reach a result |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | the third boundary's isolation message carried the second boundary's body | dry-run read before dispatch | fall-through in a keyed dispatcher | three tests | yes, never did |
| 2 | the third boundary's procedure exported to the second boundary's filename | dry-run read before dispatch | template built by substitution keeping a neighbour's literal | five tests | yes, never did |
| 3 | the table population's harness procedure had drifted; a vocabulary test passed for the wrong reason | the drift guard written for 1 and 2 | launched artifact rewritten by a later build; test reading a mutable copy as the record | three tests | yes, to the record of the run, not to a count |
| 4 | `SOURCE_ALREADY_ANCHORED` on a filename-derived source id | live refusal during the run | identity derived from an incidental attribute | one strict xfail, one locating test; **builder not fixed** | it did reach the producer; it cannot reach the certificate |
| 5 | "as before" status instruction points at a workspace the producer cannot see | post-run read of `status.json` | instruction referencing state the addressee cannot reach | **none** | it did reach the producer |
| 6 | v3.4's `assessment_unit_note` still says three obligations | packet build, read of the protocol | text written for one instance and reused | **none**; the dispatch names the contradiction | yes; the dispatch and the validator blocked it |
| 7 | under "v3.4 wholesale" the validator refused both v3.3-bound records | the Overlord's own validation run | governing document changed after downstream artifacts bound its digest | six tests | no; it blocked validation, not a judgement |
| 8 | the index hard-coded one protocol for all stages | build read (addendum 11) | one value hard-coded where the domain has several | four tests | no |
| 9 | the second boundary's reviews carried the boundary's name, not its digest | the checker, live | handoff field required by a checker and never delivered | six tests, fix lands on the next stage only | it did; it cost that boundary its certificate; it moved no count |
| 10 | the Overlord's first ratification block digested the record under its preliminary status | v3.4's own clause checker, during the write | digest computed over the wrong version of the object | the clause itself, plus five tests | no |

---

## 1. The third boundary's isolation message carried the second boundary's body

**What happened.** `d0/producer.py`'s `spawn_message` had `if stage == "A": …
else: …`. The third boundary fell into the `else` and was served the second
boundary's body verbatim: that it was "stage B of two", that the graph it held
was the one it had exported at the previous stage, and that the history already
held only the first stage. Three statements false of the third boundary, and
they contradicted the first paragraph of the `PROCEDURE.md` sitting in the same
workspace. The dry run printed them and nothing refused. (E-0470; D0-REPORT.md
addendum 12, defect 1.)

**How it was found.** The Overlord read the dry-run output and then
`d0/producer.py`, before dispatch. Not by a test; there was no test.

**Root cause.** A per-stage dispatcher with a catch-all `else`. The missing
branch is the symptom; the `else` is the defect, because it silently serves a
neighbour's value for any key nobody wrote a branch for.

**Class.** Fall-through in a keyed dispatcher over generated text.

**Guard.** In `d0/tests/test_stage_c.py`:
`test_the_stage_c_spawn_message_is_stage_cs_and_not_stage_bs` (phrases flattened
across line breaks, because a raw substring check passes by accident),
`test_the_launched_bodies_would_have_failed_that_test` (kept green as the record
of what was being sent), and
`test_the_spawn_message_refuses_a_stage_it_has_no_body_for`. `spawn_message` now
raises on an unknown stage. A second fix in the same change: `spawn_message` had
taken its input list from module state that only a build fills, so calling it
outside a build produced a message with an empty list; it now takes the declared
map as an argument, which is how the launched messages can be checked against
their launched bytes without rebuilding a launched workspace. (E-0471;
addendum 12.)

**Could it have reached a result.** Yes. It was in the exact bytes the producer
would have been dispatched. It did not, because the read happened before the
launch.

---

## 2. The third boundary's procedure exported to the second boundary's filename

**What happened.** `STAGE_C_PROCEDURE` is built from the second boundary's text
by replacement and had kept `--out work/stage-b-export.json`, while
`inputs/stage-b-export.json` is the graph the third boundary is handed. The
producer would have written its result under the name of its own input.
(E-0470; addendum 12, defect 2.)

**How it was found.** Same dry-run read, same pass.

**Root cause.** A sibling artifact generated by substituting into a neighbour's
text, with one literal left behind. The export name existed twice in the source
and only one copy was keyed.

**Class.** Template built by substitution; neighbour's literal survives.

**Guard.** Export names are now `EXPORT_FILE` keyed by stage, and `EXPORT_NAME`
(what a stage's inherited export is called in its inputs) is derived through the
predecessor rather than written out twice. Tests in `d0/tests/test_stage_c.py`:
`test_each_stage_exports_under_its_own_name`,
`test_no_stage_exports_over_the_file_it_was_handed`,
`test_the_archived_export_reader_is_keyed_by_stage`,
`test_the_archived_export_reader_refuses_an_unlaunched_stage`,
`test_the_archived_export_reader_refuses_an_unknown_stage`. The post-run readers
were checked in the same pass: `archive` copies by `rglob` and names no file,
`index` digests what it finds, and `handoff` named the second boundary's export
as a literal and now calls `archived_export(stage)`. An unused constant carrying
the first stage's literal was deleted. (E-0471; addendum 12.)

**Could it have reached a result.** Yes, and worse than 1: it would have
destroyed the input the producer was meant to read from, inside a launched
workspace. It did not, for the same reason.

---

## 3. The table population's harness procedure had drifted, and a vocabulary test passed for the wrong reason

**What happened.** Two linked facts. First, `producer/stage-a/PROCEDURE.md` on
disk hashed `sha256:06b97a3d5fb47b10…`, the builder's current text, while the
text that session was actually given hashes `sha256:9bab3603e3d446af…`. The
difference is one added section, "Declaring a gap", 28 lines carrying the six
permitted gap kinds, written into the builder *after* that session launched
(E-0438's finding) and copied over the harness file by the 2026-09-17 rebuild
that destroyed the workspace (E-0440). The manifest was later restored from the
producer session's transcript; this file was not. Second, once the file was
restored to the dispatched bytes on Luis's authorisation,
`test_both_procedures_state_the_vocabulary[A]` failed: it had been reading the
harness copy on disk and had passed only because that copy had drifted to
today's builder text. The dispatched procedure contains none of
`AGGREGATE_ONLY`, `INTERVAL_NOT_EXPRESSIBLE`, `MODALITY_NOT_EXPRESSIBLE`,
`RELATION_ABSENT`, `REQUIRED_FIELD_ABSENT_IN_SOURCE`, `TYPE_ABSENT`. (E-0471,
E-0472, E-0473; addenda 12 and 14.)

**How it was found.** By the drift guard written for defects 1 and 2. It was not
being looked for. The Overlord pinned both digests and did not correct the file,
because a launched stage's files are not the builder's to rewrite; Luis
authorised the one-file restore ("ok, go") and it was done as a byte copy from
`producer/workspace-stage-a/PROCEDURE.md`, not through the builder, whose
refusal on launched stages was left untouched. Four sources agree on
`9bab3603`: the launch receipt, the input manifest, the restored workspace copy
and `recovery/stage-a/PROCEDURE.md`.

**Root cause.** Two, and they compound. A builder that rewrites the harness copy
of an artifact belonging to a stage that has already launched. And a test that
reads a file the builder also writes, so it asserts a property of the builder's
current output while claiming to assert a property of the record.

**Class.** Launched artifact rewritten by a later build; test reading a mutable
copy as if it were the record.

**Guard.** `test_a_launched_stages_harness_file_is_the_one_its_receipt_records`
(the receipt is the authority, because it was written at the launch),
`test_a_launched_stages_files_are_the_bytes_its_manifest_records`, and
`test_the_dispatched_stage_a_procedure_is_the_receipts_digest`, which pins
`9bab3603` across receipt, manifest, workspace, recovery and harness. The
vocabulary tests now read `producer.STAGES[stage]["procedure"]`, the builder's
own text, over all three stages
(`test_every_procedure_states_the_vocabulary`, `d0/tests/test_gaps.py`), and
beside them `test_the_dispatched_stage_a_procedure_predates_the_vocabulary`
pins the absence in the launched file so nobody can make the first test pass by
rewriting a launched artifact. The pinned-divergence constant from addendum 12
is deleted. One redundant test that called `producer.build("A")` inside
`pytest.raises` tripped the static guard forbidding that call in test modules;
the test was deleted and the guard stands. (E-0473; addendum 14.)

**Could it have reached a result.** Not a count. It reached the *record of the
run*: for a period the harness asserted, and a test confirmed, that the first
session had been given a gap vocabulary it was never given. That is the
explanation for why that session declared nine gaps in a session log instead of
in its plan, and the drift had made the explanation unreadable from the tree.

---

## 4. `SOURCE_ALREADY_ANCHORED`: a source id derived from a packet filename

**What happened.** The third boundary's producer ran its procedure's anchor
command verbatim and was refused `SOURCE_ALREADY_ANCHORED` on `source:context`.
`runner.source_id_for(packet)` is `f"source:{Path(packet).stem}"`, and the
builder stages both the second and third boundaries' evidence as
`inputs/context.jsonl`, so both derive the same id and the second anchor
collides on one shared history. The refusal is typed and wrote nothing. The
producer stayed inside its own workspace, copied the packet byte for byte to
`work/stage-c-context.jsonl` and anchored that; both files hash
`sha256:d2ff1c6dcbe95709…`. It changed nothing in `inputs/`. (E-0476, E-0477;
addendum 16 section 3; the producer's own `status.json` records the refusal and
the workaround under `refusals` and `anchored_source`.)

**How it was found.** Live, by the run. No test predicted it; the builder's
`packet_target` values had never been compared against each other.

**Root cause.** An identity derived from an incidental attribute of a file. The
packet's filename is a staging convenience; the source id is a ledger identity.
Tying the second to the first means two unrelated staging decisions can collide
in the ledger.

**Class.** Identifier derived from a filename rather than declared or derived
from bytes.

**Guard.** Pinned, not fixed, because the workspace has launched. In
`d0/tests/test_stage_c.py`, `test_no_two_stages_derive_the_same_anchored_source_id`
is a **strict xfail**: it fails while the collision stands and will fail as an
unexpected pass the moment each stage gets its own packet name. Beside it,
`test_the_collision_is_in_the_packet_names_not_in_the_runner` records where the
defect lives, so the fix lands on the builder. The fix is one line in
`STAGES[…]["packet_target"]` on the next build, and it belongs with a decision
about whether the runner should take a declared source id rather than derive
one.

**Could it have reached a result.** It reached the producer. It cannot reach the
certificate, and this is proven by the run rather than assumed: the boundary
binds evidence by packet id and digest (`packet:stage-c:context`,
`d2ff1c6d`), the reviews cite that same pair, and
`check_review_coverage` reads only the boundary and the reviews, never the
ledger. The one real consequence is that the plan's derivation locators bind
`source:stage-c-context` while the boundary names `packet:stage-c:context`, so
the id in the ledger differs from the id in the boundary with the bytes
identical, and an audit looking under `source:context` will not find this
evidence there. The assessor weighed it and no count moved (E-0478).

---

## 5. "as before" points at a workspace the producer cannot see

**What happened.** The table population's procedure specified
`work/status.json` as `{"status": "COMPLETE"}` or
`{"status": "PARTIAL", "reason": …}`. The second and third boundaries'
procedures say only "Write `work/session-log.md` and `work/status.json` as
before" (`d0/producer.py:364`). The third boundary's `status.json` carries a
rich shape — `admissions`, `anchored_source`, `boundary_id`,
`boundary_identity`, `export`, `ledger_events`, `obligations_reviewed`,
`obligations_total`, `refusals`, `reviews`, `stage` — and **no `status` key at
all**. The producer said so plainly in its residuals. (E-0477 item 5;
addendum 16 section 5; addendum 17 item 2; verified by reading the archived
`status.json` keys.)

**How it was found.** By reading the archived `status.json` after the run.

**Root cause.** An instruction that refers to state the addressee cannot reach.
"As before" names a file in another stage's workspace, which the exposure rule
forbids the producer from ever seeing. The producer is a fresh session with no
inherited context by design; the instruction assumes continuity the design
removes.

**Class.** Instruction referencing state outside the addressee's reach.

**Guard.** **None.** No test asserts that a procedure states the shape of every
artifact it asks for, and no test asserts that `status.json` carries a status
token. Nothing in `d0` parses `status.json`: `archive` copies it, `index`
digests it, the packet ships it as material. So the cost today is that a human
reading the archive infers COMPLETE from the counts.

**Could it have reached a result.** It did reach the producer and shaped what it
wrote. It reached no count, because nothing downstream reads the file.

---

## 6. Protocol v3.4's explanatory note still counts three obligations

**What happened.** `assessment/review-protocol-v3.4.json` carries
`judgments.assessment_unit_note`: "Three obligations, three judgements, four
counts that sum to three." It was written at the second boundary, where three
was true. The third boundary has five. The rule it illustrates,
`judgments.assessment_unit: ONE_REVIEW_OBLIGATION`, is correct and the validator
enforces the tally rather than the number, so nothing refused. But the dispatch
tells the assessor to read the protocol first and to prefer it where the two
differ, and the two differ on that line. (E-0477; addendum 16, "One thing I did
not fix"; addendum 17 item 3. Verified by reading the protocol file.)

**How it was found.** By reading the protocol while building the assessment
packet.

**Root cause.** Explanatory text written against one instance of a rule, carried
forward with the rule. The rule generalises; the note does not, and nothing
forces them to move together.

**Class.** Protocol text written for one boundary and reused.

**Guard.** **None.** `DISPATCH.md` (`2aebfe6d`) names the contradiction
explicitly and states the rule as one judgement per obligation. That is a
mitigation in one dispatch, not a guard.

**Could it have reached a result.** Yes: an assessor following the note over the
rule could have tried to produce three judgements for five obligations. Two
things stood in the way and both held. The dispatch named the contradiction, and
the validator refuses counts that do not tally the judgements
(`test_counts_that_do_not_tally_the_judgements_refuse`,
`d0/tests/test_assessment.py`). The record validates with five judgements
summing to five.

**Why it stays.** Re-wording moves v3.4's digest `d01538fb`, which the launched
run contract of the third boundary binds and which both of that boundary's
records now bind. A launched workspace is not rebuilt. It is a decision with a
cost and it is Luis's.

---

## 7. Under "v3.4 wholesale" the validator refused every v3.3-bound record

**What happened.** Luis ruled the index moves to protocol v3.4 wholesale ("lets
start clean all the time", E-0472). The Overlord read that as one protocol for
the index and for validating every record, not as re-deciding the second
boundary's judgements, said so in chat, and dispatched that reading. Implemented
RED before GREEN: `PROTOCOL_PATH` and `GOVERNING` in `d0/assessment.py`, read by
`d0/index.py`, `d0/freeze.py` and `producer.run_contract()`; `PROTOCOL_BY_STAGE`
and `protocol_for` deleted with a test that they no longer exist. Then
`validate_assessment` under v3.4's bytes refused both the second boundary's
archived record and its newly written ratified form:
`AssessmentRefusal: the record binds a different protocol`. Both carry
`inputs.protocol_sha256 = sha256:dddcc098…`, v3.3's file, which is the rulebook
the assessor was actually graded under. (E-0472; addendum 13, "The stop".)

**How it was found.** The Overlord's own validation run after the change. The
Overlord stopped there rather than working around it and put three options to
Luis: a supersession clause in v3.4 (recommended); re-binding the record to
v3.4's digest, which would claim a grading nobody performed and was refused by
the Overlord; re-grading, which Luis had excluded.

**Root cause.** A record binds the exact digest of the rulebook it was graded
under, which is right. The governing document then changed. Without a declared
supersession, the first edit to a protocol strands every record already written
against it.

**Class.** Governing document edited after downstream artifacts bound its
digest, with no supersession path.

**Guard.** Luis approved the clause ("sounds good about the supersession in
3.4", E-0474). v3.4's `supersedes` block now declares `protocol_file_sha256`,
`superseded_digests` `[dddcc098…]`, `records_may_bind`
`THE_GOVERNING_DIGEST_OR_ANY_DIGEST_IN_superseded_digests`, `binds`
`EVERY_STAGE_OF_THIS_RUN`, and `does_not_re_grade` with its reason, replacing a
`does_not_bind` sentence that wholesale had made false.
`assessment.accepted_bindings(declared)` reads that list from the protocol
bytes, never from a constant, and `validate_protocol` refuses a v3.4 file whose
`superseded_digests` is missing or malformed, because a supersession nobody can
read accepts only itself and fails silently. The result dict gained `bound_to`.
Tests in `d0/tests/test_ratification.py`:
`test_v34_declares_the_digests_it_supersedes`,
`test_v34_accepts_the_archived_record_bound_to_the_superseded_digest`,
`test_v34_accepts_the_ratified_form_and_reads_its_ratification`,
`test_v34_still_refuses_a_digest_that_is_neither_governing_nor_superseded`,
`test_the_ratification_clause_is_enforced_on_a_superseded_binding`,
`test_neither_record_file_was_rebound`. Neither record was edited; both still
carry v3.3's digest. (E-0474; addendum 15.)

**Could it have reached a result.** No. It blocked validation of two records
that already existed; it could not change a judgement. The dangerous path was
option 2, which would have made a record claim a grading nobody performed, and
it was refused.

**The Overlord's part.** The Overlord had recommended the weaker option on
defect 8 (name the protocol per stage). Luis overrode it. Per-stage would have
deferred this collision rather than removing it, and the durable fix — a
protocol that declares what it supersedes — exists because Luis ruled wholesale.

---

## 8. The index hard-coded one protocol for all stages

**What happened.** `d0/index.py` named `review-protocol-v3.3.json` as the one
governing protocol in the manifest's `assessment` block and ran the containment
check for all three stages against v3.3's bytes, while v3.4 existed and governed
the third boundary. v3.4's file was indexed as an artifact with its digest, so
nothing was lost, and the two versions declare the same six
`ground_truth.evaluator_only_files`, so the containment verdicts are identical
either way. But the manifest asserted one governing protocol where there were
two. (Addendum 11, "One thing left undone"; E-0470.)

**How it was found.** By the preparation agent reading its own build, and
reported as an open decision rather than fixed.

**Root cause.** A single hard-coded filename standing for a value the run had
made plural.

**Class.** One value hard-coded where the domain has several.

**Guard.** After Luis's wholesale ruling: `test_one_protocol_governs_and_it_is_v34`,
`test_the_index_names_v34_as_the_governing_protocol`,
`test_the_run_contract_names_the_governing_protocol`,
`test_containment_runs_against_v34_for_every_stage`, plus the assertion that
`PROTOCOL_BY_STAGE` and `protocol_for` no longer exist
(`d0/tests/test_ratification.py`). Before the change, a test compared v3.4's
evaluator-only file list against v3.3's and found the same six, so moving
containment to v3.4 loosened nothing. (E-0472; addendum 13.)

**Could it have reached a result.** No. It is a record defect in the manifest.
The containment verdicts were the same under either protocol, which was measured
and not assumed.

---

## 9. Carried in: the second boundary's reviews named the boundary instead of digesting it

**What happened.** `malleus.acquisition.check_review_coverage` over the second
boundary's three archived reviews returned `REFUSED`, `MALFORMED_INPUT`,
`review.boundary_identity`: a lowercase SHA-256 identity is required and all
three reviews carried the boundary's id string `reading:shop-context-stage-b`.
The procedure had told the producer to write "the identity the obligations file
gives", and the staged obligations file contained no identity digest; the only
identity-looking field was `boundary.id`, and the digest was computable only by
calling the checker on the boundary bytes, which the producer was never told to
do. With that one field corrected by the evaluator and nothing else: ACCEPTED,
complete, two pending corrections and one unchanged, receipt `9827ac04`,
recorded as the evaluator's diagnostic and not as the producer's record.
(E-0452.)

**How it was found.** By running the checker, which is the point of the run.

**Root cause.** A field a downstream checker requires was never delivered to the
party asked to write it. The handoff between the boundary builder and the
producer's procedure had no obligation to carry the identity.

**Class.** Handoff field required by a checker and never delivered to its
author.

**Guard.** The identity is a function of the boundary bytes alone, so the
obligations file carries it, beside the boundary and never inside it.
`bind(…, carry_identity=True)` became the default with six tests RED first, in
`d0/tests/test_boundary_identity.py`, including
`test_a_review_written_from_the_file_passes_without_correction` (a review
written by following the procedure literally passes the checker with no
evaluator correction), `test_a_bound_boundary_carries_the_identity_the_checker_computes`,
`test_the_identity_sits_beside_the_boundary_and_not_inside_it`,
`test_the_old_shape_still_refuses`, `test_the_next_stage_procedure_names_the_field`,
and `test_stage_b_keeps_the_shape_it_launched_with`. `handoff.stage_b_inputs()`
passes `carry_identity=False` so the archived second-boundary packet still
reproduces to its receipt's digest: the fix lands on the next stage and the
record of that one stands unedited. (E-0454.)

**Could it have reached a result.** It did. It cost the second boundary its
certificate, and that boundary has none as produced. It moved none of the four
counts: both changes reached the ledger through propose, check and verdict
independently of the checker, so what the defect cost is machine legibility of
completeness. The assessor read only the refusal and the reviews as written and
did not treat the corrected checker output as the producer's run (E-0453).

**Closed here.** The third boundary carried the identity `db3dc7d0` in its
obligations file, the producer wrote it into all five reviews, and the checker
accepted the producer's own bytes with nothing corrected: `complete` true,
`missing` `[]`, `stale` `[]`, coverage identity `5114bbb8` (E-0477). That is
the fix proven on the real path, which is why no re-run of the second boundary
was ordered (E-0469).

---

## 10. The Overlord's own: the first ratification block digested the wrong version of the record

**What happened.** Writing the third boundary's ratified form, the Overlord's
first block computed `record_sha256` over the record with its *preliminary*
status, and v3.4's checker refused it. The clause requires the digest of the
record as it will be stored — status `HUMAN_RATIFIED` — with the ratification
block removed. The file was rewritten before anything read it. The stored value
is `sha256:afb68483b954fc86…`. (E-0479.)

**How it was found.** By the protocol's own clause checker, during the write.

**Root cause.** The Overlord's error. `record_sha256` is a digest over a
mutating object, and the clause fixes exactly one version of it: the object
minus its own block, in the state it is stored. Computing it over the
pre-edit version is the easy mistake, and the clause exists precisely because
"ratifying cannot alter a judgement" has to be checkable.

**Class.** Digest computed over the wrong version of the object being digested.

**Guard.** The clause itself, plus, in `d0/tests/test_ratification.py`,
`test_v34_refuses_a_record_sha256_that_does_not_match`,
`test_v34_accepts_a_properly_bound_ratification`,
`test_the_stage_c_ratification_carries_v34s_seven_fields`,
`test_the_stage_c_ratified_form_changes_no_judgement_and_no_count`,
`test_the_stage_c_binding_file_is_the_one_the_digest_names`. A copy of the
ratified form with one judgement moved is refused on `record_sha256`.

**Could it have reached a result.** No. The clause caught it at the moment of
writing, which is what it was designed for. Under v3.3 there was no clause and
nothing would have caught it: v3.3's validator never read the ratification block
at all and accepted a record asserting `HUMAN_RATIFIED` with the block pending,
emptied or nonsense (measured, addendum 9).

---

## Cross-cutting causes

**Procedures and messages generated from stage-keyed templates with fall-through
branches.** Defects 1 and 2 are one cause seen twice: the text a producer
receives is generated, the generator is keyed by stage, and the keying is
partial. A dispatcher with an `else` serves a neighbour's text; a template built
by replacement keeps whatever the replacement missed. Both were invisible to
every existing test because every existing test checked the stages that had
already launched, whose bytes were correct. The generalisation: **a per-key
generator must raise on an unknown key, and every key-dependent literal inside
it must be keyed, not substituted.**

**Artifacts of a launched stage rewritten by later builds.** Defect 3, and
before it the destruction of the first session's output (E-0440) and the
overwrite of a declared input of the second boundary's launched workspace by a
test (E-0452). Each time, the mechanism is the same: the builder or a fixture
treats a directory as a build product when it has become a record. Each time,
recovery was possible only because something else held the bytes: a transcript,
an archive, a receipt. The generalisation: **a launched artifact's authority is
its launch receipt, and every copy of it must be held to that digest.**

**Identifiers derived from filenames.** Defect 4. A staging filename became a
ledger identity, and two independent staging decisions collided on one history.
The generalisation: **an identity is declared or derived from bytes; never from
a path.**

**Instructions that reference another stage's workspace.** Defect 5, and in a
weaker form defect 9, where the instruction named a field the file did not
carry. Both are the same failure of addressing: the instruction assumes context
the addressee is designed not to have. The generalisation: **an instruction may
only name what the addressee can reach, and it states the shape it wants where
it asks for it.**

**Protocol text written for one boundary and reused.** Defect 6, and defect 9's
procedure wording. A rule generalises across boundaries; the sentence
illustrating it does not, and nothing forces them to move together. The
generalisation: **a protocol note names the rule, never the instance.**

**Digests bound into launched contracts, making later protocol edits costly.**
Defects 6, 7 and 8 share one economics. Binding by digest is what makes a
grading checkable, and it is also what makes the governing document expensive to
correct once anything has launched against it. v3.4's supersession clause is the
answer for records; there is no equivalent for a run contract sitting in a
launched harness, which is why defect 6 stands unfixed. The generalisation:
**a versioned governing document declares, from its first version, which digests
it supersedes, and readers derive the accepted set from its bytes.**

**Outside this RCA's range, same class.** On 2026-09-17 the Overlord attributed
three frozen Shop evidence failures to the checkout rather than to its own
re-binding change, and corrected it a day later after the diagnosis agent read
the producer of the failure (E-0462, corrected in E-0464). It belongs here only
as evidence that the "read the producer of the failure, not your model of it"
rule keeps earning its place.

---

## What worked, and why

**Archive first.** The first action after each producer reported was
`d0.archive --stage …`, before anything else read the workspace. The third
boundary's archive is 11 files, 3,235,181 bytes, every digest equal to
`ARCHIVE.json`, and it was re-verified intact after all subsequent work
(E-0476, E-0477; addendum 16). Everything in this case's verification is
measured from the archive, not from the live workspace. The practice exists
because the first session's output was destroyed after verification (E-0440) and
recovered only from a transcript (E-0441). It converts "the workspace is
precious" from a rule people remember into a file nobody can damage.

**A dry-run read before dispatch, of the bytes and of the code.** Defects 1 and
2 were caught by the Overlord reading the printed prompt *and* `d0/producer.py`,
not by reading the dry run's status fields, which were all green:
`DRY_RUN`, `ALREADY_PRESENT_AND_REVISED`, 13 inputs checked. A dry run
establishes that the inputs check; it says nothing about whether the text is
true. Both defects were in the exact bytes a paid model run would have consumed.

**RED before GREEN, and the drift guards that came with it.** Defect 3 was found
by a guard written for defects 1 and 2 — a guard finding an unrelated defect is
the return on writing it. Each fix in this case was landed RED first, with the
failing reason stated: the second boundary's message body is kept as a test that
still fails the stage-C assertion, as the record of what was being sent
(`test_the_launched_bodies_would_have_failed_that_test`). Keeping the negative
evidence green is what lets a later reader see the defect rather than its
absence.

**Rebuilding through the builder instead of editing files in place.** The third
boundary's packet was rebuilt through `revision.prepare("C")` four times across
E-0470 to E-0474, and every revision identity reproduced exactly each time:
revision `d2176cc2`, migration receipt `8298d681`, boundary `db3dc7d0`,
knowledge pin `a13be43c`, history `1e9c1e91` at 41 events, graph unchanged,
exposure CLEAN, 13 inputs. Editing the two bad files in place would have fixed
the packet and left the builder broken; rebuilding proves the fix reaches the
producer. The guard for that is
`test_the_stage_c_packet_on_disk_is_what_the_builder_writes_now`.

**Digest-bound ratification.** v3.4's clause caught the Overlord's own error
(defect 10) at the moment of the write, and it is the reason "ratified" can no
longer be a word a record asserts about itself. Both binding files state their
scope, including what they do *not* cover.

**The certificate.** `check_review_coverage` accepted the third boundary's five
reviews exactly as written, nothing corrected, and reported the grouping the run
expected: one pending correction, four unchanged. That is what the second
boundary's packet defect had denied the run, and it closes defect 9 on the real
path rather than in a test.

**Typed refusals that write nothing.** The anchoring refusal left the ledger
untouched, so the producer could work around it inside its own workspace without
any partial effect escaping. The re-binding capability's refusals behave the
same way (E-0458, E-0465): every negative control left the history
byte-identical, asserted per case.

**Stopping instead of working around.** The Overlord stopped on defect 7 and put
three options to Luis rather than re-binding a record to a protocol nobody had
graded it under. That is the only reason the second boundary's record is still
the bytes Luis ratified.

---

## Proposed learnings

**Proposals for Luis to accept or refuse. Nothing below has been written into a
skill file.** Each is candidate text in the voice of the skill it would join,
with the evidence that earned it.

### For `.claude/skills/malleus-paper/SKILL.md`

**P-1. Read the dispatch, not the dry run's verdict.** Candidate text, for
"Runs with a model":

> Before a launch, read the exact bytes the producer will receive: the isolation
> message, the procedure, and every instruction that names a file. A dry run
> that returns `DRY_RUN` establishes that the inputs check, not that the text is
> true. On 2026-09-18 a stage-keyed message generator served the third
> boundary's producer the second boundary's body — the wrong stage, the wrong
> predecessor, the wrong history — and a procedure told it to export over its
> own input. Both were caught by reading the printed prompt and the generator's
> code, and both were in the bytes a paid run would have consumed (E-0470).

**P-2. An instruction may only name what the addressee can reach.** Candidate
text, for "Runs with a model":

> A producer session is fresh by design and exposure forbids it from seeing any
> other stage's workspace. So a procedure that says "as before", or names a file
> from an earlier stage, is naming something the addressee cannot open. State
> the shape you want where you ask for it, every time. The third boundary's
> `status.json` came back with no status token because two procedures said "as
> before" about a shape only the first one had ever stated (E-0477, D0-REPORT.md
> addendum 17).

**P-3. A protocol note names the rule, never the instance.** Candidate text, for
"Runs with a model":

> Every new version of the review protocol is exercised by one full graph cell
> before the paper claims it. Add: every sentence in that protocol is read
> against the next boundary, not only the current one. v3.4's explanatory note
> still counts three obligations because it was written where three was true,
> and it went to an assessor judging five. The rule it illustrates was right and
> the validator enforced the tally, so nothing refused; the dispatch had to
> carry the correction by hand (E-0477).

**P-4. A versioned protocol declares what it supersedes, from version one.**
Candidate text, for "Pins, records, leaks":

> A record binds the digest of the protocol it was graded under. That is what
> makes the grading checkable and it is also what strands the record the first
> time the protocol is corrected. Every protocol version therefore declares
> `superseded_digests` and the rule that a record may bind the governing digest
> or one named there, and the validator reads that list from the protocol's own
> bytes. Without it, "start clean" refuses every record written before today
> (E-0472, E-0474).

**P-5. A launched artifact's authority is its launch receipt.** Candidate text,
for "Runs with a model", beside the existing archive rule:

> A launched workspace is precious, and so is the harness copy of everything
> that was dispatched from it. The authority for what a producer was given is
> the launch receipt, never what the builder would write today. Hold every
> launched file to its receipt's digest in a test. On 2026-09-18 the first
> session's procedure was found to have drifted to the builder's later text, and
> a vocabulary test had been passing only because of the drift: it read the
> mutable copy and reported a property of the builder as a property of the
> record (E-0471, E-0473).

### For `.claude/skills/malleus-dev/SKILL.md`

**P-6. No fall-through in a keyed dispatcher.** Candidate text, for
"Architectural law" or beside point 8 (typed diagnostics, fail before partial
effects):

> A dispatcher keyed by a declared value raises on a value it has no branch for.
> An `else` in that position silently serves a neighbour's result and produces
> confident, wrong output with no refusal anywhere. Every key-dependent literal
> inside such a generator is keyed too, never left behind by a substitution.

**P-7. Never derive an identity from a filename.** Candidate text, for
"Architectural law" point 8:

> An identity is declared by its owner or derived from the bytes it identifies.
> Deriving it from a path makes two unrelated staging decisions collide in the
> ledger. A runner that named a retained source after its packet file's stem
> refused a legitimate second anchor on one shared history, because two
> instalments of evidence had been staged under the same filename (E-0476,
> E-0477).

**P-8. A recorded revision retains what it re-binds, and proves it before it
returns.** Candidate text, for the capability's row and for "Implementation
sequence":

> A contract revision that declares a re-bound check contract records an
> identity; it does not retain bytes. The adopter retains the re-pinned contract
> in the same act, and the act verifies by loading the contract back through the
> history's own selector before it returns. Otherwise the history requires a
> check contract it does not hold and the next admission refuses
> `CHECK_CONTRACT_NOT_RETAINED`. This is not a Core defect; it is a step an
> adopter misses exactly once (E-0458, E-0465, D0-REPORT.md addenda 10 and 11).

**P-9. A digest over a mutating object names the version it digests.**
Candidate text, for "Specify every stage" point 3 or for the artifact-identity
rules:

> When a record carries a digest of itself, the contract states exactly which
> version: the object as it will be stored, minus the field holding the digest.
> Anything looser is uncheckable, and the easy mistake is to digest the version
> you started from. v3.4's ratification clause is the worked example, and it
> caught that mistake at the moment of writing (E-0479).

**P-10. A test that reads a file the builder writes is testing the builder.**
Candidate text, for "Implementation sequence" point 3 or the completion gate:

> Freeze a record against its receipt, not against whatever a generator emits
> today. A test that reads a generated file on disk and asserts a property of
> the record will pass for the wrong reason the moment the generator moves, and
> it will keep passing. Assert the generator's output against the generator, and
> the record against its receipt, in two separate tests (E-0473).

### Open, deliberately not proposed as a rule

The four counts remain tallies and not rates, and the two skills already say so.
Nothing in this case changes that, and no proposal above touches it.

---

## What is still open

1. **Packet filenames per stage.** One line in `STAGES[…]["packet_target"]` on
   the next build, plus a decision about whether the runner should take a
   declared source id rather than derive one. Pinned as a strict xfail.
2. **The "as before" status instruction.** The next procedure states the shape
   where it asks for it. No guard exists today.
3. **v3.4's `assessment_unit_note`.** Re-wording moves `d01538fb`, which a
   launched run contract and both third-boundary records bind. Luis's call.

None of the three affects the results recorded in
`handover/2026-09-18-shop-reconsideration-journal.md`.

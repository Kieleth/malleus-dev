# Malleus paper v4 source-grounded review task, protocol v3.2, second question set

This is reuse-01's review task, written by
`paper-v4/evaluation-v4/reuse-01/build_review_inputs.py` from the frozen v3
template at `paper-v4/evaluation-v4/review-task-protocol-v3.template.md`. Every
figure below is substituted from this cell's own frozen question file and query
result; no placeholder survives instantiation.

Status: the method was frozen before this cell's query ran, at
`paper-v4/evaluation-v4/review-protocol-v3.2.json`. It is not edited for this
review. That file supersedes `review-protocol-v3.json` for cells opened after it
and changes three things, of which two reach a graph surface:

- A sixth absence code, `NOT_CAPTURED`, for an element the accepted contract has
  a type or a slot for, that no record or field carries and no gap declares.
  Under v3 that fact and "the contract has no place for this at all" shared the
  token `NOT_MODELLED`, so an absence could not be diagnosed from its code.
- Stage identities are declared per surface kind. This cell binds the seven a
  graph surface carries, unchanged from v3.
- A third surface kind for a prose answer set, which is not this cell.

**What this cell is.** It is not a new graph. The graph is run-23's, already
admitted, replayed, reviewed and frozen; no producer ran here, no ontology was
authored, nothing was captured, admitted or replayed for this cell. What is new
is the question set: thirty questions authored from the selected reading alone
by a session that saw no ontology, no graph and no earlier question file, and
put to run-23's untouched ledger. The graph was built question-blind against the
first set and was equally blind to this one.

**One thing to hold on to while you judge.** You are judging run-23's records
against questions run-23's producer never saw, which is the same condition every
graph cell of this experiment was reviewed under. Judge exactly as you would
judge run-23 itself.

You are a fresh Claude session performing the preliminary inspection. Record
your kind as `CLAUDE_PRELIMINARY`, which is the kind the protocol names; if you
are anything else, the substitution is recorded as a deviation in
`paper-v4/evaluation-v4/reuse-01/review-input-manifest.json`, which also binds
every input below by digest. Verify those digests before you begin. This is
AI-assisted preliminary work, not human evidence: Luis ratifies, and only a
record with status `HUMAN_RATIFIED` is evidence for the paper.

## What you judge

Three properties and nothing else: whether the declared evidence surface
supports each witness, whether each witness's evidence pointer reaches the
place the claim rests on, and which of each question's required semantics the
returned rows carry. Do not calculate a score, construct a canonical answer,
compare against an oracle, or judge the ontology, the modelling decisions, the
retrieval architecture, or whether the sources are right.

## Inputs, exactly these

Every one of them is a material in the input manifest, bound by digest.

- the cell's evidence surface, declared in the manifest under
  `evidence_surface`. On a `SELECTED_READING_TEXT_LAYER` cell that is
  `private/paper-v4-text-layer/selected-reading.json` and you cite its block identifiers. On a
  `STRUCTURED_ROWS` cell it is the source files the manifest lists under
  `evidence_surface.sources`, each with a `source_id`, a path, a digest and a
  format, and you cite `<source_id>#row:N:field` in them.
- `paper-v4/experiment-v4/competency-questions-set-b.json`, the questions and their `required_semantics`.
- `paper-v4/experiment-v4/reuse-01/results/native-query-binding.json`, the type-only binding.
- `private/paper-v4-reuse-01/query/query-result.json`, the rows.
- `paper-v4/experiment-v4/run-23/results/trace-summary.json`, provenance for every populated record, and
  `paper-v4/experiment-v4/reuse-01/results/query-trace-summary.json`, the same for the 429
  witnesses the returned rows use.
- the retained evidence the manifest lists: the retained capture on a document
  cell, the retained population plans on a row cell.
- this task, the frozen protocol, the input manifest, and a copy of
  `paper-v4/evaluation-v4/reuse-01/review-record.blank.md`.

Do not open an answer oracle, a canonical answer, a prior score, a scorer, a
model transcript, the producer's population file, the session log, the
manuscript, a result-bearing paper ledger entry, or any external source. On a
document cell the source PDF is optional and may be opened only to cross-check
whether the text layer projected a passage faithfully; it is not a second
evidence surface. On a cell whose sources are repository fixtures, do not open
any hand-written population of those same files: it is an answer key.

You have no network.

## The three kinds of row

Each row carries a `kind`. The binding is type-only in all three: it names
record types and projected field names and never a record, a value or a count.

- `RELATION`: one relation whose endpoints are of the case's types. Its
  `witness` carries a `relation_id`, a `source_id` and a `target_id`.
- `ENTITY`: one admitted record of the case's type, with no relation. Its
  `witness` carries a `record_id`, which is the record itself.
- `SUBJECT`: one record whose `subject` reference resolves to a record of the
  case's subject type. Its `witness` carries a `record_id` and a `subject_id`.
  It exists only if the producer's ontology carries a `subject` reference. It
  may carry none, and that is not a defect.

The witness key you write in the record is the `relation_id` of a `RELATION`
row and the `record_id` of an `ENTITY` or a `SUBJECT` row. Two rows with the
same key are the same witness and are judged once.

## How a witness reaches the surface

Look every witness identifier up in the query trace summary by `record_id` or
`relation_id`, never by list position. Its `derivations` name a `path` and a
`locator`.

On a `SELECTED_READING_TEXT_LAYER` cell the locator has the form
`assertion:NNNN`. Find that `id` in the retained capture's `assertions`; the
assertion's `block` is the reading block id, and that is what you cite. The
assertion's `statement` is reading text and is inside your allowed surface;
read it.

On a `STRUCTURED_ROWS` cell the locator names a source and a field in a row of
it. Open that file, count to that row **under the convention the manifest
declares**, and read that field. The convention is two facts and both are in
`evidence_surface.locator_convention`: `first_row_index`, which says whether
the first row is numbered 0 or 1, and `csv_header_is_a_row`, which says whether
a CSV header line is counted. A field named with a bracket, `row:0:items[0]`,
is the first element of that field's array. Cite the locator with its source
id, `<source_id>#row:N:field`; a bare `row:N:field` is refused, because
shop-01's record could not say which of five files it meant.

## The checks, and where each applies

**Resolution, `STRUCTURED_ROWS` only, one per witness.** For every derivation
of the witness, open the row the locator names and compare the value in that
field with the value the record carries on that path. Write one `resolution`:

- `VALUE_MATCHES_ROW`: the record's value equals the field's.
- `VALUE_DERIVED_FROM_ROW`: the value follows from the field by a stated
  transformation, an identifier prefix (`payment:P1` from `P1`), a constant
  from a coded field, a unit attached to a bare number. A derivation names the
  field a value came from, not a field that equals it; shop-01's task read
  equality where the grammar means derivation, and the Small Shop fixture's own
  hand-written plan would have failed that reading.
- `VALUE_DIFFERS_FROM_ROW`: the locator resolves and the value neither equals
  the field nor follows from it by a transformation you can state.
- `LOCATOR_NOT_RESOLVABLE`: the locator names no declared source, or the row is
  outside the file under the declared convention, or the field is absent from
  that row.

A `LOCATOR_NOT_RESOLVABLE` witness carries `source_support` `NOT_EVALUABLE`, by
rule, and says in its `rationale` what did not resolve. It is never `PARTIAL`
and never `UNSUPPORTED`. Two sessions gave the same unresolvable locator those
two labels in one cell; the label for a mechanical fact is not a judgement.

**Statement digest, `SELECTED_READING_TEXT_LAYER` only.** A record that carries
`assertion_locator` and `statement_sha256` binds a claim to exact words. For
every such witness, compute the SHA-256 of the located assertion's `statement`
bytes in the retained capture and compare it with the record's
`statement_sha256`. Write `DIGEST_OK` or `DIGEST_MISMATCH` as the first token
of that witness's `rationale`.

**Derivation locality, `RELATION` witnesses only.** Say whether the block or
row that formalizes the relation is among the blocks or rows that derive at
least one of its endpoints. Write `DERIVATION_LOCAL` or `DERIVATION_NON_LOCAL`
as the next token of the `rationale`, then the reason in your own words. The
locality token is a statement of fact and never a reason to downgrade support
on its own.

**Subject present, `SUBJECT` and `ENTITY` witnesses only.** State whether the
subject named in the row occurs in the block or row the derivation reaches.
Write one of `SUBJECT_IN_BLOCK`, `SUBJECT_NOT_IN_BLOCK`, `SUBJECT_IN_ROW`,
`SUBJECT_NOT_IN_ROW` or `NO_SUBJECT_IN_ROW` as the next token of the
`rationale`. `NO_SUBJECT_IN_ROW` is the honest token for a witness whose
projection carries no subject at all.

## Judgments

Per witness, choose one `source_support`:

- `SUPPORTED`: the cited surface supports every material claim in the row.
- `PARTIAL`: it supports some but not all of them, or a needed qualifier is
  absent.
- `UNSUPPORTED`: it contradicts a material claim or supplies no support for it.
- `NOT_EVALUABLE`: the allowed source surface is insufficient to decide.

Per question, you do not choose a label. You fill `coverage`: one entry per item
of that question's `required_semantics`, in the question file's order. For each
item, either name the `row_index` of a row whose witness is `SUPPORTED` and
whose projected fields carry that item; or write `null` there and exactly one
`absent_reason`. These are the protocol's six, each with the protocol's own
definition:

- `NOT_MODELLED`: the accepted contract declares no type and no slot that
  could carry the element.
- `WITHHELD_STATEMENT`: the element survives only inside a retained
  statement the graph binds by locator and digest.
- `UNREACHED_RECORD`: a record carries the element and no query case returns
  it.
- `NOT_IN_SOURCE`: the reading does not state the element.
- `LOCATOR_NOT_RESOLVABLE`: the locator does not resolve under the declared
  convention.
- `NOT_CAPTURED`: the accepted contract has a type or slot for the element
  and no record or field carries it and no gap declares it.

Then write the `question_responsiveness` the derivation produces:

- `COVERED`: every required semantic names a row.
- `PARTIAL`: some do and some are absent.
- `NONE`: none does.

The validator recomputes it and refuses a label its derivation does not
produce. Write the reason for the absences in `responsiveness_rationale`, in
your own words.

Also record one `assembly` descriptor per question, which describes how the
answer is assembled and never moves a label:

- `ONE_ROW`: one row carries the whole answer.
- `LINKED_ROWS`: several rows carry it and a relation in the result joins them.
- `UNLINKED_ROWS`: several rows carry it and nothing in the row representation
  joins them.

Judge every returned row exactly once, in order: 130 rows for `CQ-B-T1-01`, 190 for `CQ-B-T1-02`, 142 for `CQ-B-T1-03`, 214
for `CQ-B-T1-04`, 190 for `CQ-B-T1-05`, 124 for `CQ-B-T2-01`, 31 for `CQ-
B-T2-02`, 270 for `CQ-B-T2-03`, 355 for `CQ-B-T2-04`, 364 for `CQ-B-T2-05`,
355 for `CQ-B-T3-01`, 130 for `CQ-B-T3-02`, 258 for `CQ-B-T3-03`, 278 for
`CQ-B-T3-04`, 339 for `CQ-B-T3-05`, 271 for `CQ-B-T4-01`, 271 for `CQ-
B-T4-02`, 270 for `CQ-B-T4-03`, 234 for `CQ-B-T4-04`, 291 for `CQ-B-T4-05`,
271 for `CQ-B-T5-01`, 356 for `CQ-B-T5-02`, 361 for `CQ-B-T5-03`, 327 for
`CQ-B-T5-04`, 278 for `CQ-B-T5-05`, 130 for `CQ-B-C-01`, 247 for `CQ-
B-C-02`, 355 for `CQ-B-C-03`, 130 for `CQ-B-C-04`, 271 for `CQ-B-C-05`,
7433 in all, over 429 distinct witnesses. Cite
at least one locator per witness and per question. Write each reason in your own
words. Copy no source passage into the record beyond the locator, and add no
numerical aggregate.

## The subject-tie rule

Ruled on 2026-09-12 and handed to every reviewer since, quoted from
`paper-v4/evaluation-v4/review-task-v3-clarification-2026-09-12.md`,
sha256:2f897a0f864b595b4562f7335152907091d7114915a60377404d6e5dd7473c9c:

> A required semantic is named by a returned row only when that row carries the
> element for the question's subject matter. The row's record, subject or
> relation must be the thing the question asks about, or be tied to it by a
> returned relation or by a field on the row itself. A row that carries a
> same-named element for a different subject does not name the semantic; write
> `row_index: null` and the absence cause. A description, `count_scope` or
> `quantity_kind` field can name a semantic only when it does so for the
> question's subject.
>
> Consequently a control whose quantities the source does not state reads NONE
> unless a returned row carries a required element about the control's own
> subject. Sample records that belong to the carbon dioxide estimation do not
> name the `sample_set` of a sulfur and chlorine question.

It binds this cell. A row that carries a same-named element for some
other subject does not name the semantic; write `row_index: null` and
the absence cause.

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

11. **The reviewer's own words do not reproduce the reading** (`C-12`).
   Every rationale and note is written in the reviewer's own words, copies
   no source passage beyond the locator and adds no numerical aggregate.
   Measured the same way as C-11: no run of sixty normalized characters
   shared with a reading block. Reads: review record, selected reading.
   Settled by the reviewer (review.witnesses[].rationale). Outcome:
   `review.witnesses[].rationale`.

## Recording

Copy `paper-v4/evaluation-v4/reuse-01/review-record.blank.md`, set `status` to
`PRELIMINARY_COMPLETE`, bind the input manifest digest in
`inputs.review_input_manifest_sha256`, fill `preliminary.actor_id` and
`preliminary.completed_at`, and leave the whole `ratification` block pending.
The per-question review blocks in `paper-v4/evaluation-v4/reuse-01/` carry each
question's rows, their witness keys and its required semantics; fill one and
assemble them into the record's `questions` array in the question file's order.

Then validate your own record with `validate_review` in
`paper-v4/evaluation-v4/review.py`, passing the v3.2 protocol bytes, the input
manifest, the query result, the competency questions and the selected reading.
It checks identities, the declared surface and its locators, witness uniqueness
and row coverage, coverage against `required_semantics` and the derived label.
It never chooses or changes a judgment. Hand the completed record to Luis for
ratification.

# Malleus paper v4 source-grounded review task, protocol v3

Template, the first written for protocol v3 and the successor of task version 4
(`paper-v4/evaluation-v4/review-task-v4.template.md`, the document form, and
`paper-v4/evaluation-v4/shop-01/review-task.md`, its row translation).
Instantiate it at freeze by substituting `{{RUN_ID}}`, `{{SURFACE_KIND}}`,
`{{QUESTION_ID_1}}` and its siblings, `{{ROWS_QUESTION_1}}` and its siblings,
`{{ROWS_TOTAL}}`, `{{WITNESSES_TOTAL}}` and every path below with the frozen
cell's own figures, and write the result to
`paper-v4/evaluation-v4/{{RUN_ID}}/review-task.md`. Run-05's task carried
run-02's row counts on a wrapped line into a live review; a template with one
substitution point per figure is what stops that happening again. No
placeholder may survive instantiation.

Status: the method was frozen before the producer ran, at
`paper-v4/evaluation-v4/review-protocol-v3.json`. It is not edited for this
review. That file supersedes `review-protocol-v2.json` for cells opened after
it and changes six things, every one of them from a recorded failure:

- The evidence surface is declared by this cell's manifest, not fixed by the
  protocol. It is one of `SELECTED_READING_TEXT_LAYER`, whose locators are
  reading block ids, or `STRUCTURED_ROWS`, whose locators are
  `<source_id>#row:N:field` and whose numbering convention the manifest states.
  Under v2 a row-shaped cell could not be validated at all.
- A row locator is opened in the file it names. Nothing in the pipeline before
  you compares a locator with its row; shop-01's producer counted physical
  lines from 1 with the CSV header as line 1 and its reviewer counted data rows
  from 0 with the header excluded, and the two read the same fifteen
  derivations as fifteen resolvable and two resolvable.
- Source support is judged once per distinct witness, {{WITNESSES_TOTAL}} of
  them here, and the rows that share a witness reference that judgement.
- A witness whose locator does not resolve is `NOT_EVALUABLE` by rule.
- The question label is derived from coverage per required semantic instead of
  chosen. Two sessions reading the same cell disagreed on the chosen label.
- A question the file marks as a control is reported, never refused.

You are a fresh Claude session performing the preliminary inspection. Record
your kind as `CLAUDE_PRELIMINARY`, which is the kind the protocol names; if you
are anything else, the substitution is recorded as a deviation in
`paper-v4/evaluation-v4/{{RUN_ID}}/review-input-manifest.json`, which also binds
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
  `{{SELECTED_READING_PATH}}` and you cite its block identifiers. On a
  `STRUCTURED_ROWS` cell it is the source files the manifest lists under
  `evidence_surface.sources`, each with a `source_id`, a path, a digest and a
  format, and you cite `<source_id>#row:N:field` in them.
- `{{COMPETENCY_QUESTIONS_PATH}}`, the questions and their `required_semantics`.
- `{{QUERY_BINDING_PATH}}`, the type-only binding.
- `{{QUERY_RESULT_PATH}}`, the rows.
- `{{POPULATION_TRACE_PATH}}`, provenance for every populated record, and
  `{{QUERY_TRACE_SUMMARY_PATH}}`, the same for the {{WITNESSES_TOTAL}}
  witnesses the returned rows use.
- the retained evidence the manifest lists: the retained capture on a document
  cell, the retained population plans on a row cell.
- this task, the frozen protocol, the input manifest, and a copy of
  `paper-v4/evaluation-v4/{{RUN_ID}}/review-record.blank.md`.

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
- `NOT_EVALUABLE`: the allowed source surface is insufficient to decide. This
  is the label an unresolvable locator takes, by rule.

Per question, you do not choose a label. You fill `coverage`: one entry per
item of that question's `required_semantics`, in the question file's order. For
each item, either name the `row_index` of a row whose witness is `SUPPORTED`,
or whose `resolution` is `VALUE_DERIVED_FROM_ROW`, and whose projected fields
carry that item; or write `null` there and one `absent_reason`:

- `NOT_MODELLED`: no record or field in the graph carries it.
- `WITHHELD_STATEMENT`: the claim's words carry it and the graph holds them as
  a locator and a digest only.
- `UNREACHED_RECORD`: the graph carries it and no case reaches the record.
- `NOT_IN_SOURCE`: the surface itself does not state it.
- `LOCATOR_NOT_RESOLVABLE`: the row that would carry it cites a locator that
  does not resolve.

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

Judge every returned row exactly once, in order: {{ROWS_QUESTION_1}} rows for
`{{QUESTION_ID_1}}`, {{ROWS_QUESTION_2}} for `{{QUESTION_ID_2}}`,
{{ROWS_TOTAL}} in all, over {{WITNESSES_TOTAL}} distinct witnesses. Cite at
least one locator per witness and per question. Write each reason in your own
words. Copy no source passage and no source row into the record beyond the
locator, and add no numerical aggregate.

## Controls

Some questions in the file carry an `expected_outcome`. Review them exactly as
you review the others and do not read the field before you judge: it names what
a person will compare your coverage against afterwards. A `NOT_IN_SOURCE` or an
`EXCLUDED_SURFACE` control expects `NONE`, and a `PARAPHRASE` control expects
the same label as the question it names. The validator reports each outcome as
a finding and refuses nothing on it.

## Recording

Copy `paper-v4/evaluation-v4/{{RUN_ID}}/review-record.blank.md`, set `status` to
`PRELIMINARY_COMPLETE`, bind the input manifest digest in
`inputs.review_input_manifest_sha256`, fill `preliminary.actor_id` and
`preliminary.completed_at`, and leave the whole `ratification` block pending.
Then run the paper gate:

```
.venv/bin/python paper-v4/run_active_tests.py
```

and validate your own record with `validate_review` in
`paper-v4/evaluation-v4/review.py`, passing the v3 protocol bytes, the input
manifest, the query result, the competency questions, and either the selected
reading or the source-file bytes keyed by `source_id`. It checks identities,
the declared surface and its locators, witness uniqueness, row coverage, the
unresolvable-locator rule, coverage against `required_semantics` and the
derived label. It never chooses or changes a judgment. Hand the completed
record to Luis for ratification.

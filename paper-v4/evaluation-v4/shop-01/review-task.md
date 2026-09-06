# Malleus paper v4 shop-01 source-grounded review task

Template, version 4, translated from `paper-v4/evaluation-v4/run-21/review-task.md`
for a cell whose sources are rows. Instantiate it at freeze by substituting
`5`, `1`, `2`, `9`,
`17` and `9` with the frozen cell's own figures, and
write the result over this file. Run-05's task carried run-02's row counts on a
wrapped line into a live review; a template with one substitution point per
figure is what stops that happening again. No placeholder may survive
instantiation.

Status of the method. The frozen protocol at
`paper-v4/evaluation-v4/review-protocol-v2.json` does **not** bind this cell, and
no protocol has been written that does. Its validator
(`paper-v4/evaluation-v4/review.py`, `validate_protocol`) refuses any protocol
whose authoritative evidence surface is not `SELECTED_READING_TEXT_LAYER` and
whose locator kind is not `SELECTED_READING_BLOCK_ID`, requires
`fixed_identities` to carry exactly the document cell's three keys, and requires a
record's question ids to equal the protocol's `CQ-01` to `CQ-04`. This cell's
evidence surface is five row-shaped files, its locators are rows and fields, and
its questions are `CQ-S1` to `CQ-S4`. The decision, which is Luis's and is
recorded in `paper-v4/experiment-v4/shop-01/run-contract.json` under
`evaluation.review_protocol`, is whether the evaluation layer gains a v3 protocol
and validator or whether this cell's questions are renamed. Until it is taken,
the record you produce is not machine validated. Everything the record binds by
digest is bound in `paper-v4/evaluation-v4/shop-01/review-input-manifest.json`,
which is built at freeze in run-21's shape. Verify those digests before you
begin.

You are a fresh Claude session performing the preliminary inspection. Record your
kind as `CLAUDE_PRELIMINARY`. This is AI-assisted preliminary work, not human
evidence: Luis ratifies, and only a record with status `HUMAN_RATIFIED` is
evidence for the paper.

## What you judge

Three properties and nothing else: whether the five source files support each
row, whether each row's evidence pointer reaches the row the claim rests on, and
whether each question's rows respond to that question. Do not calculate a score,
construct a canonical answer, compare against an oracle, or judge the ontology,
the modelling decisions, the retrieval architecture, or whether the sources are
right.

## Inputs, exactly these

Every one of them is a material in the input manifest, bound by digest.

- the five Small Shop source files, the sole evidence surface:
  `research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input/sources/warehouse.jsonl`,
  `.../small_shop_fulfilment/input/sources/inventory-units.csv`,
  `.../small_shop_fulfilment_settlement_v1/input/sources/invoices.csv`,
  `.../small_shop_fulfilment_settlement_v1/input/sources/payments.jsonl`, and
  `.../small_shop_fulfilment_correction_v1/input/sources/supplier-order-history.jsonl`.
  Cite only row and field locators in them.
- `paper-v4/experiment-v4/shop-01/competency-questions.json`, the four questions.
- `paper-v4/experiment-v4/shop-01/results/native-query-binding.json`, the
  type-only binding, expanded from the evaluator's type sets at ontology
  acceptance and before phase two existed.
- `paper-v4/experiment-v4/shop-01/results/query-result.json`, the rows.
- `paper-v4/experiment-v4/shop-01/results/trace-summary.json`, provenance for
  every populated record, and
  `paper-v4/experiment-v4/shop-01/results/query-trace-summary.json`, the same for
  the 9 witnesses the returned rows use.
- `paper-v4/experiment-v4/shop-01/results/population-plan.01-inventory.json` and
  its three siblings `population-plan.02-warehouse.json`,
  `population-plan.03-supplier-orders.json` and
  `population-plan.04-invoices-payments.json`, the retained population plans,
  which the trace resolves by plan id.
- this task, the input manifest, and a copy of
  `paper-v4/evaluation-v4/shop-01/review-record.blank.md`.

Do not open an answer oracle, a canonical answer, a prior score, a scorer, a
model transcript, the producer's session log, the manuscript, a result-bearing
paper ledger entry, or any external source. In particular, do not open
`research/ontology_driven_kg_realization/experiments/small_shop/public_population/`:
its `plans/`, its `evidence.json` and its `README.md` are a hand-written
population of these same five files and are an answer key for this cell.

You have no network.

## The three kinds of row

Each row carries a `kind`. The binding is type-only in all three: it names record
types and projected field names and never a record, a value or a count.

- `RELATION`: one relation whose endpoints are of the case's types. Its `witness`
  carries a `relation_id`, a `source_id` and a `target_id`.
- `ENTITY`: one admitted record of the case's type, with no relation. Its
  `witness` carries a `record_id`, which is the record itself.
- `SUBJECT`: one record whose `subject` reference resolves to a record of the
  case's subject type. Its `witness` carries a `record_id` and a `subject_id`.
  A `SUBJECT` row exists only if the producer's ontology carries the research
  pack's `subject` reference. It may carry none, and that is not a defect.

## How a row reaches the source

Look every witness identifier up in the query trace summary by `record_id`, never
by list position. Its `derivations` name a `path`, a `source_id` and a `locator`
of the form `row:N:field`, where `N` is the zero-based row of the file the
`source_id` names and `field` is the field in that row. Open that file, count to
that row, and read that field. Cite the locator.

A CSV file's row 0 is the first row after the header. A JSONL file's row 0 is its
first line. A field named with a bracket, `row:0:items[0]`, is the first element
of that field's array.

For a `RELATION` row the derivation that matters is the relation's own, on its
`source_id` and `target_id` paths. For an `ENTITY` or a `SUBJECT` row there is no
relation, so judge the row on the row or rows the witness's own derivations
reach: for `SUBJECT`, the record's derivations, and the subject record's where
the row's subject projection is what you are checking.

## The three checks, and where each applies

**The row opened, every row.** For every derivation of the row's witness, open
the row the locator names and compare the value in that field with the value the
record carries on that path. Write `VALUE_MATCHES_ROW`, `VALUE_DIFFERS_FROM_ROW`
or `LOCATOR_NOT_RESOLVABLE` as the first token of that row's `rationale`.

This check is yours alone. Core pins the source bytes: a plan declares each
source by id and SHA-256, the runner retains those exact bytes, and the plan
compiler refuses `UNRETAINED_SOURCE` if they differ and `UNDERIVED_FIELD` if any
property or relation endpoint carries no derivation at all. What Core does not do
is resolve the locator: a derivation locator is free text to the plan compiler,
so nothing in the pipeline has ever compared `row:0:order` with row 0 of
`warehouse.jsonl`. You are the first thing that does. Run-21's task asked for a
statement digest here instead; a row-derived record carries no
`assertion_locator` and no `statement_sha256`, so there is nothing to recompute
and this replaces it.

**Derivation locality, `RELATION` rows only.** Say whether the row that
formalizes the relation is among the rows that derive at least one of its
endpoints. Write `DERIVATION_LOCAL` or `DERIVATION_NON_LOCAL` as the next token
of that row's `rationale`, then the reason in your own words. Judge
`source_support` on the sources as this task directs; the locality token is a
separate statement of fact and never a reason to downgrade support on its own.

**Subject in the row, `SUBJECT` and `ENTITY` rows only.** State whether the
subject named in the row occurs in the row the witness's derivation reaches.
Write one of `SUBJECT_IN_ROW`, `SUBJECT_NOT_IN_ROW` or `NO_SUBJECT_IN_ROW` as the
next token of that row's `rationale`. `NO_SUBJECT_IN_ROW` is the honest token for
an `ENTITY` row whose projection carries no subject at all, and it is the
expected token for every row of a cell whose ontology declares no `subject`.

So a `RELATION` row carries the row token, then the locality token, and nothing
else. A `SUBJECT` or an `ENTITY` row carries the row token, then this one, and
nothing else.

The record grammar's `rows` entries carry exactly `row_index`, `source_support`,
`source_locators` and `rationale`. The tokens therefore live at the head of
`rationale`, which is why their spelling is fixed here.

## Two questions you judge in two halves

`CQ-S2` asks for the current state of a supplier order **and the earlier state it
superseded**. The executor is type-only and reads the replay-derived current
graph, where a superseded state is not present. The binding therefore reaches the
current state and cannot reach the earlier one, and the executor was not extended
to reach it. Judge the current half from the rows and the superseded half from
`trace-summary.json`, whose per-record `supersedes_record_id`, `superseded_by`
and `valid_to` carry it. Say in the responsiveness rationale which half came from
which.

`CQ-S4` asks which current records derive from the warehouse source **and by
which locators**. A source id and a locator live in the retained plan and the
trace, not in the graph, so a type-only case cannot filter by source. Judge the
records half from the rows and the derivation half from the trace summary, and
say so.

Neither is a defect of the cell. Both are the boundary of a type-only binding,
recorded in the run contract before the producer ran.

## Judgments

Per row, choose one `source_support`:

- `SUPPORTED`: the cited rows support every material claim in the row.
- `PARTIAL`: they support some but not all of them, or a needed qualifier is absent.
- `UNSUPPORTED`: they contradict a material claim or supply no support for it.
- `NOT_EVALUABLE`: the allowed source surface is insufficient to decide.

Per question, choose one `question_responsiveness`:

- `RESPONSIVE`: the rows directly address every requested part of the question.
- `PARTIAL`: they address only part of it, or carry material ambiguity.
- `NOT_RESPONSIVE`: they do not answer it.
- `NOT_EVALUABLE`: the row representation is insufficient to decide.

Judge every returned row exactly once, in order: 5 rows for CQ-S1,
1 for CQ-S2, 2 for CQ-S3, 9 for CQ-S4,
17 in all. Cite at least one row locator per row and per question.
Write each reason in your own words. Copy no source row into the record beyond
the locator, and add no numerical aggregate.

## Recording

Copy `paper-v4/evaluation-v4/shop-01/review-record.blank.md`, set `status` to
`PRELIMINARY_COMPLETE`, bind the input manifest digest in
`inputs.review_input_manifest_sha256`, fill `preliminary.actor_id` and
`preliminary.completed_at`, and leave the whole `ratification` block pending.
Then run the active tests:

```
.venv/bin/python paper-v4/run_active_tests.py
```

Do not run `validate_review` against
`paper-v4/evaluation-v4/review-protocol-v2.json`: it will refuse this record's
question ids, and that refusal is the open decision named at the top of this
task, not a defect in your record. Hand the completed record to Luis for
ratification.

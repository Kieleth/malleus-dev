# Malleus paper v4 {{RUN_ID}} source-grounded review task

Template. Instantiate it at freeze by substituting `{{RUN_ID}}`, `{{ROWS_CQ_01}}`,
`{{ROWS_CQ_02}}`, `{{ROWS_CQ_03}}`, `{{ROWS_CQ_04}}`, `{{ROWS_TOTAL}}` and
`{{WITNESS_COUNT}}` with the frozen cell's own figures, and write the result to
`paper-v4/evaluation-v4/{{RUN_ID}}/review-task.md`. Run-05's task carried
run-02's row counts on a wrapped line into a live review; a template with one
substitution point per figure is what stops that happening again. No placeholder
may survive instantiation.

Status: the method was frozen before the producer ran, at
`paper-v4/evaluation-v4/review-protocol.json`. It is not edited for this review.

You are a fresh Claude session performing the preliminary inspection. Record your
kind as `CLAUDE_PRELIMINARY`. The frozen protocol names `CODEX_PRELIMINARY`; the
substitution is recorded as a deviation in
`paper-v4/evaluation-v4/{{RUN_ID}}/review-input-manifest.json`, which also binds every
input below by digest. Verify those digests before you begin. This is AI-assisted
preliminary work, not human evidence: Luis ratifies, and only a record with
status `HUMAN_RATIFIED` is evidence for the paper.

## What you judge

Three properties and nothing else: whether the selected reading supports each
row, whether each row's evidence pointer reaches the block the claim rests on,
and whether each question's rows respond to that question. Do not calculate a
score, construct a canonical answer, compare against an oracle, or judge the
ontology, the modelling decisions, the retrieval architecture, or whether the
source is right.

## Inputs, exactly these

- `private/paper-v4-text-layer/selected-reading.json`, the sole evidence surface.
  Cite only its block identifiers.
- `paper-v4/experiment-v4/competency-questions.json`, the four questions.
- `paper-v4/experiment-v4/{{RUN_ID}}/results/native-query-binding.json`, the type-only
  binding, expanded from the evaluator's type sets at ontology acceptance and
  before phase two existed.
- `private/paper-v4-v4-{{RUN_ID}}/query/query-result.json`, the rows.
- `paper-v4/experiment-v4/{{RUN_ID}}/results/trace-summary.json`, provenance for every
  populated record, and
  `paper-v4/experiment-v4/{{RUN_ID}}/results/query-trace-summary.json`, the same for
  the {{WITNESS_COUNT}} witnesses the returned rows use.
- `private/paper-v4-v4-{{RUN_ID}}/ledger/retained-capture.json`, the retained capture.
- this task, the frozen protocol, the input manifest, and a copy of
  `paper-v4/evaluation-v4/{{RUN_ID}}/review-record.blank.md`.

Do not open an answer oracle, a canonical answer, a prior score, a scorer, a
model transcript, the producer's population file, the session log, the
manuscript, a result-bearing paper ledger entry, or any external source. The
source PDF is optional and may be opened only to cross-check whether the text
layer projected a passage faithfully. It is not a second evidence surface.

You have no network. The citation-veracity check of the accepted ontology's
grounding blocks is not yours: it is an overseer step taken before phase two and
recorded in the cell's launch log. Do not attempt it and do not judge a
vocabulary's existence.

## How a row reaches the reading

Each row carries a `witness` with a `relation_id`, a `source_id` and a
`target_id`. Look each up in the query trace summary by `record_id`, never by
list position. Its `derivations` name a `path` and a `locator` of the form
`assertion:NNNN`. Find that `id` in the retained capture's `assertions`; the
assertion's `block` is the reading block id. Cite that block.

The retained capture's assertion `statement` is reading text and is inside your
allowed surface. Read it. Run-04's reviewer judged claim rows on a record name
plus a block because the previous task withheld it, and withheld nothing that
needed withholding.

## The two checks run-04's task did not carry

**Statement digest.** A record that carries `assertion_locator` and
`statement_sha256` binds a claim to exact words. For every such row, compute the
SHA-256 of the located assertion's `statement` bytes in the retained capture and
compare it with the record's `statement_sha256`. Write `DIGEST_OK` or
`DIGEST_MISMATCH` as the first token of that row's `rationale`. All 104 of
run-04's located claims carried a correct digest and nothing recomputed one.

**Derivation locality.** For every row, say whether the block of the assertion
that formalizes the relation is among the blocks that formalize at least one of
its endpoints. Write `DERIVATION_LOCAL` or `DERIVATION_NON_LOCAL` as the next
token of that row's `rationale`, then the reason in your own words. Run-04
carried one assertion with thirty-six formalization targets for twelve relations
whose endpoints it names nowhere: the pairings held on the reading and the
evidence pointers did not. Judge `source_support` on the reading as this task
directs; the locality token is a separate statement of fact and never a reason
to downgrade support on its own.

The record grammar's `rows` entries carry exactly `row_index`,
`source_support`, `source_locators` and `rationale`, and the validator is frozen.
Both tokens therefore live at the head of `rationale`, which is why their
spelling is fixed here.

## Judgments

Per row, choose one `source_support`:

- `SUPPORTED`: the cited prose supports every material claim in the row.
- `PARTIAL`: it supports some but not all of them, or a needed qualifier is absent.
- `UNSUPPORTED`: it contradicts a material claim or supplies no support for it.
- `NOT_EVALUABLE`: the allowed source surface is insufficient to decide.

Per question, choose one `question_responsiveness`:

- `RESPONSIVE`: the rows directly address every requested part of the question.
- `PARTIAL`: they address only part of it, or carry material ambiguity.
- `NOT_RESPONSIVE`: they do not answer it.
- `NOT_EVALUABLE`: the row representation is insufficient to decide.

Judge every returned row exactly once, in order: {{ROWS_CQ_01}} rows for CQ-01,
{{ROWS_CQ_02}} for CQ-02, {{ROWS_CQ_03}} for CQ-03, {{ROWS_CQ_04}} for CQ-04,
{{ROWS_TOTAL}} in all. Cite at least one reading block per row and per question.
Write each reason in your own words. Copy no source passage into the record and
add no numerical aggregate.

## Recording

Copy `paper-v4/evaluation-v4/{{RUN_ID}}/review-record.blank.md`, set `status` to
`PRELIMINARY_COMPLETE`, bind the input manifest digest in
`inputs.review_input_manifest_sha256`, fill `preliminary.actor_id` and
`preliminary.completed_at`, and leave the whole `ratification` block pending.
Then run the validator:

```
PYTHONPATH=$PWD:$PWD/src .venv/bin/python -m pytest --import-mode=importlib -q \
    paper-v4/evaluation-v4
```

and validate your own record with `validate_review` in
`paper-v4/evaluation-v4/review.py`. It checks identities, row coverage, locator
membership, allowed labels and authorship state. It never chooses or changes a
judgment. Hand the completed record to Luis for ratification.

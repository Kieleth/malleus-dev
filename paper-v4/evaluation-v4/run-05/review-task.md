# Malleus paper v4 run-05 source-grounded review task

Status: the method was frozen before the run-05 producer ran, at
`paper-v4/evaluation-v4/review-protocol.json`. It is not edited for this review.

You are a fresh Claude session performing the preliminary inspection. Record your
kind as `CLAUDE_PRELIMINARY`. The frozen protocol names `CODEX_PRELIMINARY`;
Codex is unavailable and the substitution is recorded as a deviation in
`paper-v4/evaluation-v4/run-05/review-input-manifest.json`, which also binds every input
below by digest. Verify those digests before you begin. This is AI-assisted
preliminary work, not human evidence: Luis ratifies, and only a record with
status `HUMAN_RATIFIED` is evidence for the paper.

## What you judge

Two properties of the raw graph-query rows, and nothing else: whether the
selected reading supports each row, and whether each question's rows respond to
that question. Do not calculate a score, construct a canonical answer, compare
against an oracle, or judge the ontology, the modelling decisions, the retrieval
architecture, or whether the source is right.

## Inputs, exactly these

- `private/paper-v4-text-layer/selected-reading.json`, the sole evidence surface.
  Cite only its block identifiers.
- `paper-v4/experiment-v4/competency-questions.json`, the four questions.
- `paper-v4/experiment-v4/run-05/results/native-query-binding.json`, the type-only
  binding written after the replay was frozen.
- `private/paper-v4-v4-run-05/query/query-result.json`, the rows. It is private
  because the producer put verbatim source sentences into record properties.
- `paper-v4/experiment-v4/run-05/results/trace-summary.json`, provenance for every
  populated record, and
  `paper-v4/experiment-v4/run-05/results/query-trace-summary.json`, the same for
  the 44 witnesses the returned rows use.
- `private/paper-v4-v4-run-05/ledger/retained-capture.json`, the retained capture,
  read only to resolve a locator to a reading block.
- this task, the frozen protocol, the input manifest, and a copy of
  `paper-v4/evaluation-v4/run-05/review-record.blank.md`.

Do not open an answer oracle, a canonical answer, a prior score, a scorer, a
model transcript, the producer's population file, the session log, the
manuscript, a result-bearing paper ledger entry, or any external source. The
source PDF is optional and may be opened only to cross-check whether the text
layer projected a passage faithfully. It is not a second evidence surface.

## How a row reaches the reading

Each row carries a `witness` with a `relation_id`, a `source_id` and a
`target_id`. Look each up in the query trace summary by `record_id`, never by
list position. Its `derivations` name a `path` and a `locator` of the form
`assertion:NNNN`. Find that `id` in the retained capture's `assertions`; the
assertion's `block` is the reading block id. Cite that block. If a row's claim
rests on a block the derivation does not reach, say so in the reason and judge
the row on the reading alone.

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

Judge every returned row exactly once, in order: 2 rows for CQ-01, 5 for CQ-02,
9 for CQ-03, 13 for CQ-04. Cite at least one reading block per row and per
question. Write each reason in your own words. Copy no source passage into the
record and add no numerical aggregate.

## Recording

Copy `paper-v4/evaluation-v4/run-05/review-record.blank.md`, set `status` to `PRELIMINARY_COMPLETE`, bind the
input manifest digest in `inputs.review_input_manifest_sha256`, fill
`preliminary.actor_id` and `preliminary.completed_at`, and leave the whole
`ratification` block pending. Then run the validator:

```
PYTHONPATH=$PWD:$PWD/src .venv/bin/python -m pytest --import-mode=importlib -q \
    paper-v4/evaluation-v4
```

and validate your own record with `validate_review` in
`paper-v4/evaluation-v4/review.py`. It checks identities, row coverage, locator
membership, allowed labels and authorship state. It never chooses or changes a
judgment. Hand the completed record to Luis for ratification.

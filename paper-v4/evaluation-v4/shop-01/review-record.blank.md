# Malleus paper v4 shop-01 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/shop-01/review-task.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

`inputs.review_protocol_sha256` is empty and stays empty until a frozen protocol
binds this cell. The v2 protocol does not: its validator pins the evidence
surface to the selected reading and its question ids to `CQ-01` to `CQ-04`. The
open decision is recorded in the run contract under `evaluation.review_protocol`
and at the top of the review task.

Fill one `rows` entry per returned row, in order, zero-based: {{ROWS_CQ_S1}} for
CQ-S1, {{ROWS_CQ_S2}} for CQ-S2, {{ROWS_CQ_S3}} for CQ-S3, {{ROWS_CQ_S4}} for
CQ-S4, {{ROWS_TOTAL}} in all. Cite row locators of the form `row:N:field` only,
naming the source file. Write the reasons in your own words and copy no source
row into this record beyond the locator.

Each `rationale` opens with the fixed tokens the task defines: `VALUE_MATCHES_ROW`,
`VALUE_DIFFERS_FROM_ROW` or `LOCATOR_NOT_RESOLVABLE`, then, on a `RELATION` row
only, `DERIVATION_LOCAL` or `DERIVATION_NON_LOCAL`, and on a `SUBJECT` or an
`ENTITY` row only, one of `SUBJECT_IN_ROW`, `SUBJECT_NOT_IN_ROW` or
`NO_SUBJECT_IN_ROW`; then the reason in your own words. The `rows` grammar is
closed at four keys, which is why every finding lives at the head of the text
field.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v2",
  "status": "BLANK",
  "inputs": {
    "review_protocol_sha256": "",
    "review_input_manifest_sha256": ""
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "",
    "completed_at": ""
  },
  "questions": [
    {
      "question_id": "CQ-S1",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-S2",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-S3",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-S4",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "source_locators": [],
      "rows": []
    }
  ],
  "ratification": {
    "evaluator_kind": "HUMAN_AUTHOR",
    "actor_id": "actor:luis",
    "disposition": "PENDING",
    "completed_at": "",
    "notes": ""
  }
}
```

Each `rows` entry has this shape:

```
{
  "row_index": 0,
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "source_locators": ["warehouse.jsonl row:0:order"],
  "rationale": "VALUE_MATCHES_ROW NO_SUBJECT_IN_ROW one or two sentences in your own words"
}
```

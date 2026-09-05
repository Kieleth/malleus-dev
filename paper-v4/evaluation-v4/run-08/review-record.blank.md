# Malleus paper v4 run-08 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: {{ROWS_CQ_01}} for
CQ-01, {{ROWS_CQ_02}} for CQ-02, {{ROWS_CQ_03}} for CQ-03, {{ROWS_CQ_04}} for
CQ-04, {{ROWS_TOTAL}} in all. Cite reading block ids only. Write the reasons in
your own words and copy no source passage into this record.

Each `rationale` opens with the two fixed tokens the task defines, `DIGEST_OK`
or `DIGEST_MISMATCH` where the record carries a statement digest, then
`DERIVATION_LOCAL` or `DERIVATION_NON_LOCAL`, then the reason in your own words.
The `rows` grammar is closed at four keys and the validator is frozen, which is
why both findings live at the head of the text field.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v2",
  "status": "BLANK",
  "inputs": {
    "review_protocol_sha256": "sha256:7cee52a7d6ea5018fe8443e621c72280b05c2bb5cc1e4a2eeaa27208665ed379",
    "review_input_manifest_sha256": ""
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "",
    "completed_at": ""
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-04",
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
  "source_locators": ["page:2:block:004"],
  "rationale": "DIGEST_OK DERIVATION_LOCAL one or two sentences in your own words"
}
```

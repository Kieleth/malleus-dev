# Malleus paper v4 run-14 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task-v4.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 190 for
CQ-01, 195 for CQ-02, 323 for CQ-03, 211 for
CQ-04, 919 in all. Cite reading block ids only. Write the reasons in
your own words and copy no source passage into this record.

Each `rationale` opens with the fixed tokens the task defines: `DIGEST_OK` or
`DIGEST_MISMATCH` where the record carries a statement digest, then, on a
`RELATION` row only, `DERIVATION_LOCAL` or `DERIVATION_NON_LOCAL`, and on a
`SUBJECT` or an `ENTITY` row only, one of `SUBJECT_IN_BLOCK`,
`SUBJECT_NOT_IN_BLOCK` or `NO_SUBJECT_IN_ROW`; then the reason in your own
words. The `rows` grammar is closed at four keys and the validator is frozen,
which is why every finding lives at the head of the text field.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v2",
  "status": "BLANK",
  "inputs": {
    "review_protocol_sha256": "sha256:88b69f6e80a3b9eac3a2c990178186df9c52fed3ced5c4e020162b0c202fa795",
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
  "rationale": "DIGEST_OK SUBJECT_IN_BLOCK one or two sentences in your own words"
}
```

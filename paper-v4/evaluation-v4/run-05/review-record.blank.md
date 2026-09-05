# Malleus paper v4 run-05 source-grounded review record

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 2 for CQ-01, 5
for CQ-02, 9 for CQ-03, 13 for CQ-04. Cite reading block ids only. Write the
reasons in your own words and copy no source passage into this record.

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
  "rationale": "one or two sentences in your own words"
}
```

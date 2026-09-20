# Malleus paper v4 source-grounded review record, protocol v3.2, second question set

This is reuse-01's blank record, written by
`paper-v4/evaluation-v4/reuse-01/build_review_inputs.py` from the frozen v3
template. The question ids are this cell's frozen competency question file's, in
that file's order. The row and witness counts are this cell's query result's.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Write one `witnesses` entry per distinct witness the query result returns,
429 in all, and reference it from every row that shares it.
Rows: 130 rows for `CQ-B-T1-01`, 190 for `CQ-B-T1-02`, 142 for `CQ-B-T1-03`, 214
for `CQ-B-T1-04`, 190 for `CQ-B-T1-05`, 124 for `CQ-B-T2-01`, 31 for `CQ-
B-T2-02`, 270 for `CQ-B-T2-03`, 355 for `CQ-B-T2-04`, 364 for `CQ-B-T2-05`,
355 for `CQ-B-T3-01`, 130 for `CQ-B-T3-02`, 258 for `CQ-B-T3-03`, 278 for
`CQ-B-T3-04`, 339 for `CQ-B-T3-05`, 271 for `CQ-B-T4-01`, 271 for `CQ-
B-T4-02`, 270 for `CQ-B-T4-03`, 234 for `CQ-B-T4-04`, 291 for `CQ-B-T4-05`,
271 for `CQ-B-T5-01`, 356 for `CQ-B-T5-02`, 361 for `CQ-B-T5-03`, 327 for
`CQ-B-T5-04`, 278 for `CQ-B-T5-05`, 130 for `CQ-B-C-01`, 247 for `CQ-
B-C-02`, 355 for `CQ-B-C-03`, 130 for `CQ-B-C-04`, 271 for `CQ-B-C-05`,
7433 in all.

Three things the validator derives or forbids, so that writing them wrong is
refused rather than recorded:

- `question_responsiveness` is derived from `coverage`. Write the label the
  derivation produces, `COVERED` when every required semantic names a row,
  `NONE` when none does, `PARTIAL` otherwise. A label the derivation does not
  produce is refused.
- `assembly` is a descriptor, not a grade. It never moves a label.
- A witness is judged once. Two rows with the same key are the same witness.

This is a `SELECTED_READING_TEXT_LAYER` cell: no witness carries `resolution`
and every locator is a reading block id. Copy no source passage into this record
beyond the locator, and add no numerical aggregate.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v3.2",
  "status": "BLANK",
  "inputs": {
    "review_protocol_sha256": "sha256:5dfd59f4aa479dd72738e2eb55653ee3e84e60886de4cccbcc0a8e66d06e55cd",
    "review_input_manifest_sha256": ""
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "",
    "completed_at": ""
  },
  "witnesses": [],
  "questions": [
    {
      "question_id": "CQ-B-T1-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T1-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T1-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T1-04",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T1-05",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T2-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T2-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T2-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T2-04",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T2-05",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T3-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T3-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T3-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T3-04",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T3-05",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T4-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T4-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T4-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T4-04",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T4-05",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T5-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T5-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T5-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T5-04",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-T5-05",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-C-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-C-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-C-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-C-04",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-B-C-05",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
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

Each `witnesses` entry has this shape, with the fixed tokens the task defines at
the head of the `rationale`:

```
{{
  "witness_key": "obs:instrument-count",
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "source_locators": ["page:2:block:004"],
  "rationale": "DIGEST_OK SUBJECT_IN_BLOCK one or two sentences in your own words"
}}
```

Each `rows` entry names a returned row and the witness it shares:

```
{{
  "row_index": 0,
  "witness_key": "obs:instrument-count"
}}
```

Each `coverage` entry names one required semantic and either the row that
carries it or one typed reason it is absent:

```
{{
  "semantic": "instrument_count",
  "row_index": 3,
  "absent_reason": null,
  "note": ""
}}

{{
  "semantic": "instrument_count",
  "row_index": null,
  "absent_reason": "NOT_MODELLED | NOT_CAPTURED | WITHHELD_STATEMENT | UNREACHED_RECORD | NOT_IN_SOURCE | LOCATOR_NOT_RESOLVABLE",
  "note": "why, in your own words"
}}
```

# Malleus paper v4 source-grounded review record, protocol v3

This is run-22's blank record, written by
`paper-v4/evaluation-v4/run-22/build_review_inputs.py` from the frozen v3
template. The question ids are this cell's frozen competency question file's,
in that file's order. The row and witness counts are figures of a producer
that has not run and are filled by the same script at freeze; no other
placeholder survives either stage.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

The `questions` block below carries one entry per question of the cell's
competency question file, 30 of them, in that file's order. Write one
`witnesses` entry per distinct witness the query result returns,
449 in all, and reference it from every row that shares it.
Rows: 85 rows for `CQ-T1-01`, 85 for `CQ-T1-02`, 147 for `CQ-T1-03`, 147 for
`CQ-T1-04`, 83 for `CQ-T1-05`, 178 for `CQ-T2-01`, 75 for `CQ-T2-02`, 299
for `CQ-T2-03`, 252 for `CQ-T2-04`, 24 for `CQ-T2-05`, 300 for `CQ-T3-01`,
309 for `CQ-T3-02`, 309 for `CQ-T3-03`, 149 for `CQ-T3-04`, 148 for
`CQ-T3-05`, 61 for `CQ-T4-01`, 61 for `CQ-T4-02`, 66 for `CQ-T4-03`, 299 for
`CQ-T4-04`, 62 for `CQ-T4-05`, 143 for `CQ-T5-01`, 309 for `CQ-T5-02`, 300
for `CQ-T5-03`, 148 for `CQ-T5-04`, 299 for `CQ-T5-05`, 153 for `CQ-C-01`,
144 for `CQ-C-02`, 385 for `CQ-C-03`, 85 for `CQ-C-04`, 309 for `CQ-C-05`,
5414 in all.

Three things the validator derives or forbids, so that writing them wrong is
refused rather than recorded:

- `question_responsiveness` is derived from `coverage`. Write the label the
  derivation produces, `COVERED` when every required semantic names a row,
  `NONE` when none does, `PARTIAL` otherwise. A label the derivation does not
  produce is refused.
- A witness whose `resolution` is `LOCATOR_NOT_RESOLVABLE` carries
  `source_support` `NOT_EVALUABLE`, never `PARTIAL` and never `UNSUPPORTED`,
  and says in its `rationale` what did not resolve.
- `assembly` is a descriptor, not a grade. It never moves a label.

On a `STRUCTURED_ROWS` cell every witness carries `resolution` and cites
locators of the form `<source_id>#row:N:field`. On a
`SELECTED_READING_TEXT_LAYER` cell no witness carries `resolution` and every
locator is a reading block id. Copy no source passage or source row into this
record beyond the locator, and add no numerical aggregate.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v3",
  "status": "BLANK",
  "inputs": {
    "review_protocol_sha256": "sha256:17b5744a71a1e6a9ab1985f43b3e28d4d683f2d7d369e7decdb375171c2edc21",
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
      "question_id": "CQ-T1-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T1-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T1-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T1-04",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T1-05",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T2-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T2-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T2-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T2-04",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T2-05",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T3-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T3-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T3-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T3-04",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T3-05",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T4-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T4-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T4-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T4-04",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T4-05",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T5-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T5-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T5-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T5-04",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-T5-05",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-C-01",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-C-02",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-C-03",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-C-04",
      "question_responsiveness": "PENDING",
      "responsiveness_rationale": "",
      "assembly": "PENDING",
      "coverage": [],
      "source_locators": [],
      "rows": []
    },
    {
      "question_id": "CQ-C-05",
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

Each `witnesses` entry has this shape on a `STRUCTURED_ROWS` cell:

```
{
  "witness_key": "invoice:I1",
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "resolution": "VALUE_MATCHES_ROW | VALUE_DERIVED_FROM_ROW | VALUE_DIFFERS_FROM_ROW | LOCATOR_NOT_RESOLVABLE",
  "source_locators": ["source:small-shop:invoices#row:0:invoice_id"],
  "rationale": "one or two sentences in your own words"
}
```

and this shape on a `SELECTED_READING_TEXT_LAYER` cell, with no `resolution`
key and the fixed tokens the task defines at the head of the `rationale`:

```
{
  "witness_key": "obs:instrument-count",
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "source_locators": ["page:2:block:004"],
  "rationale": "DIGEST_OK SUBJECT_IN_BLOCK one or two sentences in your own words"
}
```

Each `rows` entry names a returned row and the witness it shares:

```
{
  "row_index": 0,
  "witness_key": "invoice:I1"
}
```

Each `coverage` entry names one required semantic and either the row that
carries it or one typed reason it is absent:

```
{
  "semantic": "instrument_count",
  "row_index": 3,
  "absent_reason": null,
  "note": ""
}

{
  "semantic": "instrument_count",
  "row_index": null,
  "absent_reason": "NOT_MODELLED | WITHHELD_STATEMENT | UNREACHED_RECORD | NOT_IN_SOURCE | LOCATOR_NOT_RESOLVABLE",
  "note": "why, in your own words"
}
```

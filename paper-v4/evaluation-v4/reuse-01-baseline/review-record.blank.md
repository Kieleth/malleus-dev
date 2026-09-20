# Malleus paper v4 source-grounded review record, protocol v3.2, in-context answer set

This is reuse-01-baseline's blank record, written by
`paper-v4/experiment-v4/reuse-01-baseline/build_review_inputs.py` from the frozen v3
template. The question ids are this cell's frozen competency question file's, in
that file's order. The claim counts are the producer's answer file's.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Write one `witnesses` entry per claim the answer file cites,
102 in all. Claim ids are unique, so no witness is shared and
none is judged twice. Claims: 3 claims for `CQ-B-T1-01`, 3 for `CQ-B-T1-02`, 4 for `CQ-B-T1-03`, 4 for
`CQ-B-T1-04`, 3 for `CQ-B-T1-05`, 6 for `CQ-B-T2-01`, 5 for `CQ-B-T2-02`, 4
for `CQ-B-T2-03`, 4 for `CQ-B-T2-04`, 4 for `CQ-B-T2-05`, 3 for `CQ-
B-T3-01`, 3 for `CQ-B-T3-02`, 4 for `CQ-B-T3-03`, 4 for `CQ-B-T3-04`, 4 for
`CQ-B-T3-05`, 4 for `CQ-B-T4-01`, 4 for `CQ-B-T4-02`, 3 for `CQ-B-T4-03`, 4
for `CQ-B-T4-04`, 2 for `CQ-B-T4-05`, 4 for `CQ-B-T5-01`, 4 for `CQ-
B-T5-02`, 4 for `CQ-B-T5-03`, 4 for `CQ-B-T5-04`, 4 for `CQ-B-T5-05`, 0 for
`CQ-B-C-01`, 0 for `CQ-B-C-02`, 0 for `CQ-B-C-03`, 3 for `CQ-B-C-04`, 4 for
`CQ-B-C-05`,
102 in all.

Three things the validator derives or forbids, so that writing them wrong is
refused rather than recorded:

- `question_responsiveness` is derived from `coverage`. Write the label the
  derivation produces, `COVERED` when every required semantic names a row,
  `NONE` when none does, `PARTIAL` otherwise. A label the derivation does not
  produce is refused.
- `assembly` is `NOT_APPLICABLE` on this surface, on every question. A prose
  answer always assembles, so the descriptor would be constant, and a constant
  token in a comparison table reads as a grade.
- A witness must cite every block its claim cites in the answer file. Support is
  judged against the cited block, not the article around it.

No witness carries `resolution` on this surface and every locator is a reading
block id. Copy no source passage into this record beyond the locator, and add no
numerical aggregate.

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

Each `witnesses` entry has this shape:

```
{
  "witness_key": "CQ-T1-01:c1",
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "source_locators": ["page:2:block:004"],
  "rationale": "one or two sentences in your own words"
}
```

Each `rows` entry names one claim of that question and the witness it is:

```
{
  "row_index": 0,
  "witness_key": "CQ-T1-01:c1"
}
```

Each `coverage` entry names one required semantic and either the claim that
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
  "absent_reason": "NOT_CAPTURED | NOT_IN_SOURCE | WITHHELD_STATEMENT | NOT_MODELLED",
  "note": "why, in your own words"
}
```

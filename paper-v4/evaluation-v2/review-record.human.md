# Paper v4 source-grounded review record

Human ratification record. Copied from the preliminary record; only the status and the ratification block changed.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v1",
  "status": "HUMAN_RATIFIED",
  "inputs": {
    "review_protocol_sha256": "sha256:04cf6bc131d018acc541d0ee9812b18c1a3d40b58b4bc003536598e2d4621d43",
    "review_input_manifest_sha256": "sha256:181e1447a9b7d56e816816d1105f5084114e287e90d5547423fefd1d74568e28"
  },
  "preliminary": {
    "evaluator_kind": "CODEX_PRELIMINARY",
    "actor_id": "actor:codex-paper-v4",
    "completed_at": "2026-09-03T09:18:15Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "source_support": "NOT_EVALUABLE",
      "question_responsiveness": "NOT_RESPONSIVE",
      "row_refs": [],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "The query returned no rows. The cited prose describes the acquisition network, campaign, and deployed instrument count, so an empty result addresses none of the requested parts; with no row claim, source support cannot be assessed."
    },
    {
      "question_id": "CQ-02",
      "source_support": "SUPPORTED",
      "question_responsiveness": "PARTIAL",
      "row_refs": [
        {
          "query_id": "NQ-CQ-02",
          "row_index": 0
        },
        {
          "query_id": "NQ-CQ-02",
          "row_index": 1
        }
      ],
      "source_locators": [
        "page:2:block:004"
      ],
      "rationale": "The cited prose supports the two-row chain from microseismicity to a ridge axis and from that axis to RC2. The rows identify the subsection and an axis relation, but omit the deep qualifier and represent the more specific beneath relation only as occurrence at the axis."
    },
    {
      "question_id": "CQ-03",
      "source_support": "SUPPORTED",
      "question_responsiveness": "RESPONSIVE",
      "row_refs": [
        {
          "query_id": "NQ-CQ-03",
          "row_index": 0
        },
        {
          "query_id": "NQ-CQ-03",
          "row_index": 1
        },
        {
          "query_id": "NQ-CQ-03",
          "row_index": 2
        },
        {
          "query_id": "NQ-CQ-03",
          "row_index": 3
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:5:block:004",
        "page:5:block:005"
      ],
      "rationale": "The cited prose supports the reported earthquake-depth bounds, the calculated primary-melt CO2 bounds, their units, and the RC2 association. The four rows expose both quantities, distinguish observed from calculated status, identify CO2 and primary melt, and locate the melt at RC2."
    },
    {
      "question_id": "CQ-04",
      "source_support": "NOT_EVALUABLE",
      "question_responsiveness": "NOT_RESPONSIVE",
      "row_refs": [],
      "source_locators": [
        "page:5:block:002",
        "page:5:block:003"
      ],
      "rationale": "The query returned no rows. The cited prose explicitly marks a preferred mechanism and states its causal sequence, so the empty result addresses none of the requested causal or epistemic elements; with no row claim, source support cannot be assessed."
    }
  ],
  "ratification": {
    "evaluator_kind": "HUMAN_AUTHOR",
    "actor_id": "actor:luis",
    "disposition": "RATIFIED_AS_RECORDED",
    "completed_at": "2026-09-03T22:15:04Z",
    "notes": "Ratified as recorded. Decided by Luis in chat on 2026-09-03 after reading each verdict against the cited blocks; recorded by the overseer session at his instruction. CQ-02 rows match block page:2:block:004; CQ-03 rows match page:1:block:001 and page:5:block:005, and page:8:block:007 additionally states 'primary melts' for the 0.4-3.0 wt% range."
  }
}
```

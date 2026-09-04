# Paper v4 source-grounded review record

Copy this file for the review. Edit only the JSON block. `BLANK` and `PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify the completed entries.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v1",
  "status": "PRELIMINARY_COMPLETE",
  "inputs": {
    "review_protocol_sha256": "sha256:ccb7158ae88ebc04d4558928cc09e50e80d00f823a11a48fd5229cfa360854f1",
    "review_input_manifest_sha256": "sha256:2eb5c0896c5bd00a8a20e20599d651168785f4dd7ccfc8ead07a810972725d44"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-opus-5-preliminary-reviewer",
    "completed_at": "2026-09-03T16:25:29Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "source_support": "NOT_EVALUABLE",
      "question_responsiveness": "NOT_RESPONSIVE",
      "row_refs": [],
      "source_locators": ["page:2:block:002", "page:6:block:002"],
      "rationale": "Query NQ-CQ-01 returned zero rows, so there are no material claims from the query result to check against the reading; source support cannot be scored on an empty result. Responsiveness is NOT_RESPONSIVE because an empty row set answers no part of the question. The reading itself does describe an OBS network and cruise with an instrument count and spacing, so the gap sits in the query result, not in source coverage."
    },
    {
      "question_id": "CQ-02",
      "source_support": "NOT_EVALUABLE",
      "question_responsiveness": "NOT_RESPONSIVE",
      "row_refs": [],
      "source_locators": ["page:2:block:004", "page:2:block:006"],
      "rationale": "Both cases bound to NQ-CQ-02 returned zero rows, leaving no material claims to weigh against the reading, so source support is not evaluable. Responsiveness is NOT_RESPONSIVE since nothing was returned to name a ridge subsection or place events relative to its axis. The reading names a segment and locates the deep earthquakes beneath its axis, so the empty answer is a retrieval-stage gap rather than a source-coverage gap."
    },
    {
      "question_id": "CQ-03",
      "source_support": "NOT_EVALUABLE",
      "question_responsiveness": "NOT_RESPONSIVE",
      "row_refs": [],
      "source_locators": ["page:1:block:001", "page:2:block:006", "page:8:block:007"],
      "rationale": "All three cases bound to NQ-CQ-03 returned zero rows, so there is no depth-range or CO2-range claim from the query result to check against the reading; source support is not evaluable. Responsiveness is NOT_RESPONSIVE because nothing was returned to give the depth range, the calculated CO2 range, units, or estimate status. The reading reports both figures for the same association, so the empty result is not explained by an absence of source content."
    },
    {
      "question_id": "CQ-04",
      "source_support": "SUPPORTED",
      "question_responsiveness": "NOT_RESPONSIVE",
      "row_refs": [{"query_id": "NQ-CQ-04", "row_index": 0}],
      "source_locators": ["page:5:block:002", "page:5:block:003", "page:5:block:006"],
      "rationale": "The one returned row (case 1, a melt phase saturating with an analyte at a given pressure and temperature) matches the reading's statement of the pressure and temperature at which the melt becomes saturated with that analyte, so on its narrow content the source supports the row. But the row states only a saturation condition; it names no ascending-melt or degassing step, no extensional stress, no earthquake trigger, and carries no epistemic-status marker. The reading states the preferred causal mechanism and marks it explicitly as the authors' preferred hypothesis in separate text the row does not cite, and the second bound case that would link melt generation to the ridge segment returned no row at all. The row is therefore not responsive to what the question asks."
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

# Independent judge record for a sampled witness set

Blank. Copy this file, edit only the JSON block below, and leave the prose
alone. The judging session fills it under
`paper-v4/evaluation-v4/sample/judge-task.template.md` as the dispatching
session instantiated it.

`sample_sha256` is the digest of the sample file the packet was built from, in
the form `sha256:<hex>`. `judgements` carries one entry per sampled witness,
exactly once each, with that witness's own `cell` and `witness_key` copied from
the packet. `source_support` is one of `SUPPORTED`, `PARTIAL`, `UNSUPPORTED`,
`NOT_EVALUABLE`. Every `rationale` is your own words: a rationale that shares a
sixty-character run with the reading is refused.

This record is a second opinion on a sample. It is not a protocol v3 review, it
is not ratified, and no figure in it reaches the paper on its own. Write no
total, no percentage and no aggregate anywhere in this file.

Hand it back when it is complete. The dispatching session validates it with
`paper-v4/evaluation-v4/sample/validate_judge_record.py`, which needs the sample
file; a judging session does not open that file, because its name says which
stratum the packet came from.

```json
{
  "schema": "malleus.paper-v4.independent-judge-record/v1",
  "sample_sha256": "sha256:FILL_WITH_THE_SAMPLE_DIGEST",
  "judge": {
    "evaluator_kind": "INDEPENDENT_MODEL_JUDGE",
    "model_id": "FILL",
    "actor_id": "FILL",
    "reasoning_effort": "FILL"
  },
  "judgements": [
    {
      "cell": "FILL",
      "witness_key": "FILL",
      "source_support": "FILL",
      "rationale": "FILL"
    }
  ]
}
```

# Malleus paper v4 source-grounded review record, protocol v3

This is run-24's blank record, written by
`paper-v4/evaluation-v4/run-24/build_review_inputs.py` from the frozen v3
template. The question ids are this cell's frozen competency question file's,
in that file's order. The row and witness counts are figures of a producer
that has not run and are filled by the same script at freeze; no other
placeholder survives either stage.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

The `questions` block below carries one entry per question of the cell's
competency question file, 30 of them, in that file's order. Write one
`witnesses` entry per distinct witness the query result returns,
416 in all, and reference it from every row that shares it.
Rows: 158 rows for `CQ-T1-01`, 158 for `CQ-T1-02`, 128 for `CQ-T1-03`, 55 for
`CQ-T1-04`, 158 for `CQ-T1-05`, 98 for `CQ-T2-01`, 228 for `CQ-T2-02`, 243
for `CQ-T2-03`, 301 for `CQ-T2-04`, 29 for `CQ-T2-05`, 212 for `CQ-T3-01`,
228 for `CQ-T3-02`, 228 for `CQ-T3-03`, 222 for `CQ-T3-04`, 216 for
`CQ-T3-05`, 68 for `CQ-T4-01`, 68 for `CQ-T4-02`, 80 for `CQ-T4-03`, 243 for
`CQ-T4-04`, 49 for `CQ-T4-05`, 196 for `CQ-T5-01`, 228 for `CQ-T5-02`, 212
for `CQ-T5-03`, 212 for `CQ-T5-04`, 244 for `CQ-T5-05`, 212 for `CQ-C-01`,
197 for `CQ-C-02`, 291 for `CQ-C-03`, 158 for `CQ-C-04`, 228 for `CQ-C-05`,
5348 in all.

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
  "status": "PRELIMINARY_COMPLETE",
  "inputs": {
    "review_protocol_sha256": "sha256:17b5744a71a1e6a9ab1985f43b3e28d4d683f2d7d369e7decdb375171c2edc21",
    "review_input_manifest_sha256": "sha256:9a1fd952b517cf9882e2261d329bb6a0d2e73a68d058ccb5866d073d8a8c27d3"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-24",
    "completed_at": "2026-09-10T02:05:55Z"
  },
  "witnesses": [
    {
      "witness_key": "entity:claim:axis-relocating",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:claim:basalts-degassed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "entity:claim:co2-degassing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, hypothesis_disposition, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002"
      ]
    },
    {
      "witness_key": "entity:claim:cold-thick-lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, hypothesis_disposition, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:claim:confident-hypocenters",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "entity:claim:contexts-differ",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "entity:claim:deepest-documented",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "entity:claim:depth-not-following",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "entity:claim:detachment-inactive",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:claim:enriched-source",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "entity:claim:events-well-constrained",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:001"
      ]
    },
    {
      "witness_key": "entity:claim:fig6-interpretation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:012"
      ]
    },
    {
      "witness_key": "entity:claim:focal-not-robust",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "entity:claim:hydrothermal-cooling",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, hypothesis_disposition, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "entity:claim:keller-flushing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "entity:claim:lab-melt",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:claim:lab-melt-combination",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "entity:claim:long-period",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, hypothesis_disposition, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "entity:claim:magmatic-tectonic",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, hypothesis_disposition, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:4:block:002",
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "entity:claim:magmatism-dominates",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "entity:claim:max-depth-factors",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "entity:claim:max-depth-selection",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "entity:claim:melt-freeze",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "entity:claim:melt-migration-unknown",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:003"
      ]
    },
    {
      "witness_key": "entity:claim:melt-movement-rejected",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "entity:claim:melt-residence",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "entity:claim:model1-inappropriate",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "entity:claim:model5-preferred",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "entity:claim:more-events-needed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "entity:claim:no-active-vents",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "entity:claim:no-competing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:047"
      ]
    },
    {
      "witness_key": "entity:claim:no-detachment-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:4:block:001"
      ]
    },
    {
      "witness_key": "entity:claim:no-eruption",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "entity:claim:not-artifact",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "entity:claim:offaxis-magmatism",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "entity:claim:primary-vs-preeruptive",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "entity:claim:quality-ab",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "entity:claim:ratio-proxy",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "entity:claim:rc2-magmatic",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:claim:reduced-model-reasonable",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "entity:claim:samples-degassed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "entity:claim:shear-zone",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, hypothesis_disposition, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "entity:claim:snapshot",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "entity:claim:trace-element-assumption",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "entity:claim:ultraslow-co2-high",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "entity:claim:volatile-role-unknown",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:claim:volume-change",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "entity:claim:vpvs-reasonable",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states this claim and the projection (claim_kind, name) reports it as the block frames it, including its modality, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:003"
      ]
    },
    {
      "witness_key": "entity:melt:ascending",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this melt and its stage as the row projects them (name), and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:002"
      ]
    },
    {
      "witness_key": "entity:melt:pre-eruptive",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this melt and its stage as the row projects them (melt_stage, name), and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "entity:melt:primary",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this melt and its stage as the row projects them (melt_stage, name), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "entity:melt:primitive",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this melt and its stage as the row projects them (melt_stage, name), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:q:avg-depth-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "entity:q:avg-horizontal-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "entity:q:axial-depth-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "entity:q:b-value",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "entity:q:b-value-groups",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "entity:q:brittle-thickness-expected",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:q:catalog-links",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "entity:q:categories",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "entity:q:cluster-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "entity:q:co2-gas-loss",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "entity:q:cold-lithosphere-age",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "entity:q:criterion-arrivals",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "entity:q:criterion-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "entity:q:criterion-swave",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "entity:q:crustal-age-offaxis",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:q:deep-events-threshold",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "entity:q:depth-uncertainty-final",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "entity:q:dry-melting-onset",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "entity:q:equatorial-co2-average",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "entity:q:equatorial-co2-max",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "entity:q:error-ellipsoid-confidence",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:005"
      ]
    },
    {
      "witness_key": "entity:q:expected-max-depth",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the bound and its unit as the projection has them, but it attributes the expectation to earlier microseismicity studies; the projected MODELLED determination says the figure came from a model, which this block does not say.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:q:fig3-deep-shade",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:4:block:007"
      ]
    },
    {
      "witness_key": "entity:q:fig3-shallow-shade",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:4:block:007"
      ]
    },
    {
      "witness_key": "entity:q:fig3b-halfwidth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:4:block:006"
      ]
    },
    {
      "witness_key": "entity:q:fig4-isotherm",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "entity:q:fixed-depth-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "entity:q:fixed-depth-subset",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "entity:q:focal-fault-plane",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "entity:q:focal-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "entity:q:focal-misfit",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "entity:q:focal-new",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "entity:q:focal-polarities",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "entity:q:focal-probability",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "entity:q:focal-station-ratio",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, value_lower, value_qualification), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "entity:q:focal-total",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "entity:q:full-spreading-rate",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:q:gap-final",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "entity:q:groups",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "entity:q:horizontal-uncertainty-final",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "entity:q:hypodd-iterations",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "entity:q:iceland-depths",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "entity:q:identified-760",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "entity:q:instrument-spacing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "entity:q:lithospheric-age-interval",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "entity:q:located-514",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "entity:q:located-514-methods",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:005"
      ]
    },
    {
      "witness_key": "entity:q:low-frequency-threshold",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "entity:q:magnitude-completeness",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "entity:q:mar-317",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "entity:q:mar-events",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The count is verbatim in the block as a figure label and the projected count holds; the projected scope, that these are the events along the ridge profile, is not stated in the block and rests on the label's position in the extracted figure text.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "entity:q:max-separation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "entity:q:mayotte-depths",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "entity:q:mean-horizontal-error",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "entity:q:mean-vertical-error",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "entity:q:microseismicity-residence",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "entity:q:min-obs-detect",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "entity:q:model1-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "entity:q:model1-velocity",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "entity:q:obs-spacing-focal",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "entity:q:offaxis-swarm-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "entity:q:pore-pressure-trigger",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "entity:q:profile-halfwidth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:005"
      ]
    },
    {
      "witness_key": "entity:q:profile-interval",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:005"
      ]
    },
    {
      "witness_key": "entity:q:quality-d-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "entity:q:rc2-co2-calculated",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "entity:q:rc2-pre-eruptive-co2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "entity:q:rc2-valley-width-2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "entity:q:rc3-co2-calculated",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "entity:q:recording-duration",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "entity:q:relocated-276",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "entity:q:relocated-364",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "entity:q:relocation-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "entity:q:relocation-rms",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "entity:q:relocation-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "entity:q:rms-final",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "entity:q:romanche-events",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The count appears verbatim in the block as a figure label, so the projected count holds; the block states nowhere in prose that these are the events along the transform-fault profile, and the projected scope rests on where the label sits in the extracted figure text rather than on a sentence.",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "entity:q:saturating-melt-co2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "entity:q:saturation-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "entity:q:saturation-pressure",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "entity:q:saturation-temp",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "entity:q:slow-expected-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "entity:q:solubility-temp",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "entity:q:studied-portion-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "entity:q:subdataset",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "entity:q:subevents",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "entity:q:subsection-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "entity:q:temp-below-20",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:007"
      ]
    },
    {
      "witness_key": "entity:q:tf-197",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "entity:q:thermal-model-temp",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:q:two-criteria-share",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "entity:q:ultraslow-expected-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "entity:q:updated-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "entity:q:useful-obs",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "entity:q:velest-iterations",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (count, count_scope, name), with the same count and the same thing counted, and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "entity:q:velocity-constraint-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "entity:q:velocity-perturbation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "entity:q:volatile-melting-onset",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "entity:q:vpvs-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:002"
      ]
    },
    {
      "witness_key": "entity:q:young-crust-age",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "entity:ratio:co2-ba",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block gives this ratio and its uncertainty as the row projects them (denominator_kind, name, numerator_kind, ratio_value, uncertainty), and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "entity:ratio:co2-rb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block gives this ratio and its uncertainty as the row projects them (denominator_kind, name, numerator_kind, ratio_value, uncertainty), and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "entity:ratio:vpvs",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block gives this ratio and its uncertainty as the row projects them (denominator_kind, name, numerator_kind, ratio_value), and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:002"
      ]
    },
    {
      "witness_key": "entity:anhydrous-peridotite",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block reports this rock material and the row projects only its name and kind (name, rock_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "entity:basaltic-rocks",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block reports this rock material and the row projects only its name and kind (name, rock_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:basalts-seafloor",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block reports this rock material and the row projects only its name and kind (name, rock_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:mantle-peridotites",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block reports this rock material and the row projects only its name and kind (name, rock_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "entity:melt-inclusions",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block reports this rock material and the row projects only its name and kind (name, rock_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "entity:morb-samples",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block reports this rock material and the row projects only its name and kind (name, rock_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "entity:peridotite-seafloor",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block reports this rock material and the row projects only its name and kind (name, rock_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "entity:pillow-basalts",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block reports this rock material and the row projects only its name and kind (name, rock_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:popping-rocks",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block reports this rock material and the row projects only its name and kind (name, rock_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:005"
      ]
    },
    {
      "witness_key": "entity:q:abstract-co2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:q:abstract-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (count_scope, determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:q:bdb-isotherm",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, uncertainty, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "entity:q:bdb-shallow-offaxis",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:q:brittle-thickness-ntds",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:q:cold-isotherm",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:q:crust-thickness",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, uncertainty, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "entity:q:deep-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "entity:q:deep-rc2-abstract",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "entity:q:degassing-depth-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "entity:q:fig6-crust-thickness",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, uncertainty, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "entity:q:fig6-deep-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:7:block:012"
      ]
    },
    {
      "witness_key": "entity:q:fig6-isotherm",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "entity:q:half-spreading-rate",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "entity:q:hot-mantle-temp",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "entity:q:lab-melt-fraction",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "entity:q:lab-sub-solidus-temp",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "entity:q:lab-water-content",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "entity:q:mar-coverage",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "entity:q:no-quakes-below-20",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:5:block:007"
      ]
    },
    {
      "witness_key": "entity:q:ntd1-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:q:ntd2-bdb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:q:ntd2-deeper",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:q:ntd2-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:q:ntd2-normal-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "entity:q:ntd2-offset",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:q:occ-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:q:offaxis-shallow",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:q:rc2-alignment",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, value_qualification), and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "entity:q:rc2-ba",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, subject, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "entity:q:rc2-co2-ba",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "entity:q:rc2-co2-rb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "entity:q:rc2-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:q:rc2-primary-ba90",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "entity:q:rc2-primary-floor",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "entity:q:rc2-primary-rb90",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "entity:q:rc2-rb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, subject, unit, value_lower, value_qualification), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "entity:q:rc2-valley-width",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:q:rc3-co2-ba",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "entity:q:rc3-co2-rb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "entity:q:rc3-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:q:rc3-primary-ba90",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "entity:q:rc3-primary-rb90",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "entity:q:shallow-rti",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "entity:q:supersegment-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "entity:q:swir-bdb-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:q:swir-highest-co2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "entity:q:tf-coverage",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity the row projects (name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper), with the same bound, unit and qualification, and the block names the subject the row points at, using the short form the record carries as a tag.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "event:romanche-2016",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block names the event, its magnitude and its magnitude scale, and those projections hold; it gives only the year, while the row projects an exact instant at the start of that year and carries no temporal-precision field to mark the difference, so the instant is finer than anything the block states.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "entity:ref:r1",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:012",
        "page:8:block:013"
      ]
    },
    {
      "witness_key": "entity:ref:r10",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:007"
      ]
    },
    {
      "witness_key": "entity:ref:r11",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:008"
      ]
    },
    {
      "witness_key": "entity:ref:r12",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:009"
      ]
    },
    {
      "witness_key": "entity:ref:r13",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:010"
      ]
    },
    {
      "witness_key": "entity:ref:r14",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:011",
        "page:9:block:012"
      ]
    },
    {
      "witness_key": "entity:ref:r15",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:013"
      ]
    },
    {
      "witness_key": "entity:ref:r16",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (doi, name, page_range, publication_year, venue_name), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:014",
        "page:9:block:015"
      ]
    },
    {
      "witness_key": "entity:ref:r17",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:016"
      ]
    },
    {
      "witness_key": "entity:ref:r18",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:017",
        "page:9:block:018"
      ]
    },
    {
      "witness_key": "entity:ref:r19",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:019"
      ]
    },
    {
      "witness_key": "entity:ref:r2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:014"
      ]
    },
    {
      "witness_key": "entity:ref:r20",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:020",
        "page:9:block:021"
      ]
    },
    {
      "witness_key": "entity:ref:r21",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (doi, name, page_range, publication_year, venue_name), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:022"
      ]
    },
    {
      "witness_key": "entity:ref:r22",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (doi, name, publication_year), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:023",
        "page:9:block:024"
      ]
    },
    {
      "witness_key": "entity:ref:r23",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:025",
        "page:9:block:026"
      ]
    },
    {
      "witness_key": "entity:ref:r24",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:027",
        "page:9:block:028"
      ]
    },
    {
      "witness_key": "entity:ref:r25",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:029"
      ]
    },
    {
      "witness_key": "entity:ref:r26",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:030"
      ]
    },
    {
      "witness_key": "entity:ref:r27",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (doi, name, page_range, publication_year, venue_name), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:031"
      ]
    },
    {
      "witness_key": "entity:ref:r28",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:031",
        "page:9:block:032"
      ]
    },
    {
      "witness_key": "entity:ref:r29",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:033"
      ]
    },
    {
      "witness_key": "entity:ref:r3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:015"
      ]
    },
    {
      "witness_key": "entity:ref:r30",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:034"
      ]
    },
    {
      "witness_key": "entity:ref:r31",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:035"
      ]
    },
    {
      "witness_key": "entity:ref:r32",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:036"
      ]
    },
    {
      "witness_key": "entity:ref:r33",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:037",
        "page:9:block:038"
      ]
    },
    {
      "witness_key": "entity:ref:r34",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:039"
      ]
    },
    {
      "witness_key": "entity:ref:r35",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:040"
      ]
    },
    {
      "witness_key": "entity:ref:r36",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:041"
      ]
    },
    {
      "witness_key": "entity:ref:r37",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:042"
      ]
    },
    {
      "witness_key": "entity:ref:r38",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:043"
      ]
    },
    {
      "witness_key": "entity:ref:r39",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:044",
        "page:9:block:045"
      ]
    },
    {
      "witness_key": "entity:ref:r4",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:016"
      ]
    },
    {
      "witness_key": "entity:ref:r40",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:046",
        "page:9:block:047"
      ]
    },
    {
      "witness_key": "entity:ref:r41",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:048"
      ]
    },
    {
      "witness_key": "entity:ref:r42",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:049"
      ]
    },
    {
      "witness_key": "entity:ref:r43",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:050"
      ]
    },
    {
      "witness_key": "entity:ref:r44",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:051"
      ]
    },
    {
      "witness_key": "entity:ref:r45",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:052"
      ]
    },
    {
      "witness_key": "entity:ref:r46",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:053",
        "page:9:block:054"
      ]
    },
    {
      "witness_key": "entity:ref:r47",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:055"
      ]
    },
    {
      "witness_key": "entity:ref:r48",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:056",
        "page:10:block:001"
      ]
    },
    {
      "witness_key": "entity:ref:r49",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:002"
      ]
    },
    {
      "witness_key": "entity:ref:r5",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:017"
      ]
    },
    {
      "witness_key": "entity:ref:r50",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:003"
      ]
    },
    {
      "witness_key": "entity:ref:r51",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:004",
        "page:10:block:005"
      ]
    },
    {
      "witness_key": "entity:ref:r52",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:006",
        "page:10:block:007"
      ]
    },
    {
      "witness_key": "entity:ref:r53",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:008"
      ]
    },
    {
      "witness_key": "entity:ref:r54",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:009"
      ]
    },
    {
      "witness_key": "entity:ref:r55",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:010"
      ]
    },
    {
      "witness_key": "entity:ref:r56",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:011"
      ]
    },
    {
      "witness_key": "entity:ref:r57",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:012"
      ]
    },
    {
      "witness_key": "entity:ref:r58",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:013",
        "page:10:block:014"
      ]
    },
    {
      "witness_key": "entity:ref:r59",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:015"
      ]
    },
    {
      "witness_key": "entity:ref:r6",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:001",
        "page:9:block:002"
      ]
    },
    {
      "witness_key": "entity:ref:r60",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:016"
      ]
    },
    {
      "witness_key": "entity:ref:r61",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:017"
      ]
    },
    {
      "witness_key": "entity:ref:r62",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:018"
      ]
    },
    {
      "witness_key": "entity:ref:r63",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:019"
      ]
    },
    {
      "witness_key": "entity:ref:r64",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:020"
      ]
    },
    {
      "witness_key": "entity:ref:r65",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:021"
      ]
    },
    {
      "witness_key": "entity:ref:r66",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:022",
        "page:10:block:023"
      ]
    },
    {
      "witness_key": "entity:ref:r67",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:024"
      ]
    },
    {
      "witness_key": "entity:ref:r68",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:025"
      ]
    },
    {
      "witness_key": "entity:ref:r69",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:026"
      ]
    },
    {
      "witness_key": "entity:ref:r7",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (doi, name, page_range, publication_year, venue_name), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:003",
        "page:9:block:004"
      ]
    },
    {
      "witness_key": "entity:ref:r70",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:027",
        "page:10:block:028"
      ]
    },
    {
      "witness_key": "entity:ref:r71",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:029"
      ]
    },
    {
      "witness_key": "entity:ref:r72",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:030"
      ]
    },
    {
      "witness_key": "entity:ref:r73",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (doi, name, publication_year), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:031",
        "page:10:block:032",
        "page:10:block:033"
      ]
    },
    {
      "witness_key": "entity:ref:r74",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:034"
      ]
    },
    {
      "witness_key": "entity:ref:r75",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (doi, name, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:035",
        "page:10:block:036"
      ]
    },
    {
      "witness_key": "entity:ref:r76",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:037"
      ]
    },
    {
      "witness_key": "entity:ref:r77",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:038",
        "page:10:block:039"
      ]
    },
    {
      "witness_key": "entity:ref:r78",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:040"
      ]
    },
    {
      "witness_key": "entity:ref:r79",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:041",
        "page:10:block:042"
      ]
    },
    {
      "witness_key": "entity:ref:r8",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:005"
      ]
    },
    {
      "witness_key": "entity:ref:r9",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (name, page_range, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:9:block:006"
      ]
    },
    {
      "witness_key": "entity:work:yu-2025",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The reference entry in the cited block carries every bibliographic field the row projects (doi, licence, name, publication_year, venue_name, volume_designation), transcribed with the text layer's own spacing, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:045",
        "page:10:block:048",
        "page:11:block:001",
        "page:11:block:003",
        "page:11:block:005",
        "page:11:block:006",
        "page:1:block:001",
        "page:1:block:006",
        "page:2:block:008",
        "page:3:block:006",
        "page:4:block:008",
        "page:5:block:011",
        "page:6:block:006",
        "page:7:block:013",
        "page:8:block:018",
        "page:9:block:056"
      ]
    },
    {
      "witness_key": "entity:gakkel",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (name), and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "entity:juan-de-fuca",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (name), and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "entity:knipovich",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (name), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "entity:mar",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (name), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:001",
        "page:1:block:005",
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "entity:mar-supersegment",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (name), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "entity:ntd1",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (accretion_character, name, structural_orientation), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:ntd2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (name, structural_orientation), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:rc1",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (accretion_character, name), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (accretion_character, name), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:005",
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:rc3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (accretion_character, name, structural_orientation), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:rti",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (description, name), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "entity:swir",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (name), and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:swir-oblique",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (name), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "entity:swir-segment8",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this ridge section and states the attributes the row projects (name), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "relation:rc3:adjacent:rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_NON_LOCAL The methods sentence that formalizes the relation calls one segment the adjacent one to the south of the other, so the relation rests on it; the block derives neither endpoint, both of which come from earlier blocks.",
      "source_locators": [
        "page:8:block:005"
      ]
    },
    {
      "witness_key": "entity:campaign:smarties",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited blocks name the cruise, the size of the network, how long it recorded and when the experiment ran, which is what the row projects (begins_at, count, count_scope, duration, name, temporal_precision), and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:043",
        "page:2:block:002",
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "entity:obs",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_NOT_CARRIED NO_SUBJECT_IN_ROW This Instrument record projects only a name and carries no assertion_locator or statement_sha256, so there is no statement digest to check; the three blocks its derivations reach all name the ocean-bottom seismometers, so the one projected claim rests on the surface.",
      "source_locators": [
        "page:1:block:001",
        "page:2:block:002",
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "entity:software:global-mapper",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited blocks name this software and, where projected, its version and download location (locator, name), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "entity:software:gmt",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited blocks name this software and, where projected, its version and download location (name), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "entity:software:hash",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited blocks name this software and, where projected, its version and download location (locator, name, software_version), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:010",
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "entity:software:hypodd",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited blocks name this software and, where projected, its version and download location (locator, name, software_version), and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:006",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "entity:software:nonlinloc",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited blocks name this software and, where projected, its version and download location (locator, name), and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:004",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "entity:software:seisan",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited blocks name this software and, where projected, its version and download location (locator, name), and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:002",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "entity:software:velest",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited blocks name this software and, where projected, its version and download location (locator, name), and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:004",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "entity:software:zmap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited blocks name this software and, where projected, its version and download location (locator, name), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:010",
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "relation:morb:sampled-from:rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_NON_LOCAL The figure caption that formalizes the relation places the sample set along this segment, but that block derives neither endpoint: the samples come from a methods sentence and the segment from the introduction. The relation still rests on the block that states it.",
      "source_locators": [
        "page:6:block:005"
      ]
    },
    {
      "witness_key": "entity:data:earthquake-catalog",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this resource and the row projects what it states about it (name), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:008"
      ]
    },
    {
      "witness_key": "entity:data:petdb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this resource and the row projects what it states about it (locator, name), and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:005",
        "page:8:block:005"
      ]
    },
    {
      "witness_key": "entity:data:raw-seismic",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this resource and the row projects what it states about it (locator, name), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:008"
      ]
    },
    {
      "witness_key": "entity:data:refraction-profile",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this resource and the row projects what it states about it (name), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "entity:data:seisan-db",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this resource and the row projects what it states about it (name), and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "entity:data:zenodo",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block names the repository and gives the identifier prefix exactly as the record projects it; the block ends mid-identifier and the remaining digits fall in the next reading block, which the capture declared nothing-assertable, so the projected value is faithful to the cited block but is not a complete identifier.",
      "source_locators": [
        "page:8:block:008"
      ]
    },
    {
      "witness_key": "relation:catalog:deposited:zenodo",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation states it between exactly these two records, and its block also derives at least one endpoint; the relation type the row projects is the one the sentence states.",
      "source_locators": [
        "page:8:block:008"
      ]
    },
    {
      "witness_key": "entity:askja",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block names this volcano as one of the comparison sites, so the projected name holds, but it says nothing about its form; narrowing it to a volcanic cone is not stated in the cited block.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "entity:axial-valley-rc1",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:chain-tf",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "entity:detachment-rc1",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Both cited blocks are needed and both hold: the first states the fault, its kind and its dip direction, the second states that it is inactive. The second block frames that status as an inference drawn from an absence of seismicity, and the projection carries the status with no slot for that hedge, which is a modelling limit rather than a gap in the surface.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:fagradalsfjall",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block names this locality as a comparison site, so the projected name holds; it gives it no structural description, so the projected volcanic-cone kind rests on nothing in the cited block.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "entity:hydrothermal-mound",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The figure caption in this block names the feature and calls it inactive, so the projected name, structure kind and status all rest on the block.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "entity:logachev",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "entity:main-axial-faults",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "entity:mayotte",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block names this island as a comparison site and gives the depth of its seismicity, so the projected name holds, but nothing in it describes a seamount; the projected structure kind goes beyond the block.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "entity:mylonite-shear-zones",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "entity:ntd1-faults",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives this fault population and its two strike directions, so the projected name and orientation hold, but it calls them only faults; the projected NORMAL_FAULT kind is not stated for them, and the two places in the same block that do say normal faults are describing a different structure and a different discontinuity.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:ntd1-vent-field",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, status, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "entity:ntd2-faults",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structural_orientation, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:occ",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "entity:occ-corrugated",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:4:block:006"
      ]
    },
    {
      "witness_key": "entity:occ-dome-faults",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:occ-normal-faults",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the faults, their strike and that they point to recent active deformation, which is what the projected name, orientation, kind and status say; the block presents the activity as what the faults suggest and the projection has no slot for that hedge.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:occ-termination",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block names the termination of the core complex, so the projected name holds, but it does not describe it as a corrugated surface; the reading treats the corrugated surface and the termination as two different marked features, so the projected structure kind is not supported by the block cited.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:rainbow",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block names this massif and places it at a non-transform discontinuity, so the projected name holds, but it does not call it an oceanic core complex; that projected kind is not stated in the cited block.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "entity:rc2-axial-faults",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:rc2-bounding-faults",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the faults, their orientation and their inward dip, which the projection carries, but it does not call them normal faults; the projected NORMAL_FAULT kind goes beyond what the cited block says, and the block's only other mention of a fault kind is a denial that detachment faults are present.",
      "source_locators": [
        "page:4:block:001"
      ]
    },
    {
      "witness_key": "entity:rc2-hummocky",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:rc2-median-valley",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:rc2-neovolcanic-ridge",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structural_orientation, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:rc2-volcanic-cones",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "entity:romanche-tf",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "entity:transform-valley",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this feature and states the attributes the row projects (name, structure_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "entity:bdb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this boundary and its kind as the row projects them (boundary_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:001",
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "entity:lab",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this boundary and its kind as the row projects them (boundary_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "entity:moho",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this boundary and its kind as the row projects them (boundary_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "relation:occ:cut-by:faults",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation also derives one endpoint, and it states a cutting relation between exactly these two records; the endpoint order in the row is the inverse of a source-cuts-target reading, which is a question about the relation type's own direction and not about what the block says.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "relation:logachev:part-of:knipovich",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation states it between exactly these two records, and its block also derives at least one endpoint; the relation type the row projects is the one the sentence states.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "relation:occ:beneath:mar",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation states it between exactly these two records, and its block also derives at least one endpoint; the relation type the row projects is the one the sentence states.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "relation:rc1:bounded-by:detachment",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation states it between exactly these two records, and its block also derives at least one endpoint; the relation type the row projects is the one the sentence states.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "relation:rc2:bounded-by:faults",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation states it between exactly these two records, and its block also derives at least one endpoint; the relation type the row projects is the one the sentence states.",
      "source_locators": [
        "page:4:block:001"
      ]
    },
    {
      "witness_key": "entity:method:double-difference",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "entity:method:focal-criterion",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "entity:method:local-magnitude",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "entity:method:location-criteria",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "entity:method:nonlinear-location",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "entity:method:octtree",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:004"
      ]
    },
    {
      "witness_key": "entity:method:stalta",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "entity:method:wadati",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:002"
      ]
    },
    {
      "witness_key": "entity:model:1d-velocity",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "entity:model:average-velocity",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "entity:model:co2-solubility",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "entity:model:fastest",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "entity:model:five-velocity",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "entity:model:iacono-marziano",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "entity:model:minimum-velocity",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "entity:model:thermal",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this method and the row projects its name and kind (method_kind, name), and the row carries no subject reference.",
      "source_locators": [
        "page:3:block:001",
        "page:7:block:012"
      ]
    },
    {
      "witness_key": "entity:brittle-lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this unit and its kind as the row projects them (name, unit_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "entity:crust-free-lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this unit and its kind as the row projects them (name, unit_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "entity:exhumed-mantle",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this unit and its kind as the row projects them (name, unit_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "entity:lower-crust",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this unit and its kind as the row projects them (name, unit_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "entity:mantle",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this unit and its kind as the row projects them (name, unit_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:mantle-source",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this unit and its kind as the row projects them (name, unit_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "entity:oceanic-crust",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this unit and its kind as the row projects them (name, unit_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "entity:oceanic-lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this unit and its kind as the row projects them (name, unit_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "entity:sediment-layers",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this unit and its kind as the row projects them (name, unit_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "entity:western-flank-crust",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this unit and its kind as the row projects them (name, unit_kind), and the row carries no subject reference.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "entity:funder:erc",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The funding block names this organisation and its role, so the projected name and agent type rest on the cited block; the record's assertion_locator points at a second assertion carved from the same block, and the digest of that assertion matches, so provenance stays inside the block that supports the claim.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "entity:funder:nsfc",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "entity:funder:zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "entity:org:1",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "entity:org:2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "entity:org:3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "entity:org:4",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "entity:org:5",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "entity:org:6",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "entity:person:briais",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:046",
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:person:brunelli",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:046",
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:person:grenet",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:person:hamelin",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:person:maia",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:046",
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:person:petracchini",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:046",
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:person:singh",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:044",
        "page:11:block:002",
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:person:yu",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block names this contributor and the projection (agent_type, name) adds nothing it does not state, and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:044",
        "page:11:block:002",
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "entity:award:erc1",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The funding block gives this grant agreement number, which is what the record projects as both name and award identifier; as with the funder record, the assertion_locator names a sibling assertion cut from the same block and its digest matches.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "entity:award:isblue",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited funding block gives this award and its identifier (award_identifier, name), and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "entity:award:nsfc1",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited funding block gives this award and its identifier (award_identifier, name), and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "entity:award:nsfc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited funding block gives this award and its identifier (award_identifier, name), and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "entity:award:zjnsf1",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited funding block gives this award and its identifier (award_identifier, name), and the row carries no subject reference.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "relation:singh:funded-by:erc",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation states it between exactly these two records, and its block also derives at least one endpoint; the relation type the row projects is the one the sentence states.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "relation:yu:funded-by:nsfc",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation states it between exactly these two records, and its block also derives at least one endpoint; the relation type the row projects is the one the sentence states.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "relation:yu:funded-by:zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation states it between exactly these two records, and its block also derives at least one endpoint; the relation type the row projects is the one the sentence states.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "relation:erc1:awarded-by:erc",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation states it between exactly these two records, and its block also derives at least one endpoint; the relation type the row projects is the one the sentence states.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "relation:nsfc1:awarded-by:nsfc",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation states it between exactly these two records, and its block also derives at least one endpoint; the relation type the row projects is the one the sentence states.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "relation:nsfc2:awarded-by:nsfc",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation states it between exactly these two records, and its block also derives at least one endpoint; the relation type the row projects is the one the sentence states.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "relation:zjnsf1:awarded-by:zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalizes the relation states it between exactly these two records, and its block also derives at least one endpoint; the relation type the row projects is the one the sentence states.",
      "source_locators": [
        "page:10:block:044"
      ]
    }
  ],
  "questions": [
    {
      "question_id": "CQ-T1-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names a row. The cruise and the instruments sit in two rows that nothing in the result joins, because this question's case set declares no relation type; the tie between them is readable only from the block both rows cite.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "campaign_name",
          "row_index": 0,
          "absent_reason": null,
          "note": "The campaign row names the cruise."
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "The instrument row names the ocean-bottom seismometers whose recordings the study uses."
        },
        {
          "semantic": "data_acquisition",
          "row_index": 0,
          "absent_reason": null,
          "note": "The same row is bound to the sentence in which the network acquires the microseismicity data, and it carries the size and the scope of that network."
        }
      ],
      "source_locators": [
        "page:10:block:043",
        "page:2:block:002",
        "page:6:block:002",
        "page:1:block:001",
        "page:2:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:campaign:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "entity:obs"
        },
        {
          "row_index": 2,
          "witness_key": "entity:software:global-mapper"
        },
        {
          "row_index": 3,
          "witness_key": "entity:software:gmt"
        },
        {
          "row_index": 4,
          "witness_key": "entity:software:hash"
        },
        {
          "row_index": 5,
          "witness_key": "entity:software:hypodd"
        },
        {
          "row_index": 6,
          "witness_key": "entity:software:nonlinloc"
        },
        {
          "row_index": 7,
          "witness_key": "entity:software:seisan"
        },
        {
          "row_index": 8,
          "witness_key": "entity:software:velest"
        },
        {
          "row_index": 9,
          "witness_key": "entity:software:zmap"
        },
        {
          "row_index": 10,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 11,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 12,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 13,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 14,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 15,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 16,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 17,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 18,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 19,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 20,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 21,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 22,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 23,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 24,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 25,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 26,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 27,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 28,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 29,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 30,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 31,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 32,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 33,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 34,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 35,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 36,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 37,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 38,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 39,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 40,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 41,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 42,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 43,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 44,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 45,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 46,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 47,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 48,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 49,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 50,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 51,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T1-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names a row. Two rows carry the answer and nothing in the result joins them, since the case set for this question declares no relation type.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "instrument_count",
          "row_index": 0,
          "absent_reason": null,
          "note": "The campaign row carries the count and states what is being counted."
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "The instrument row names the instrument type the count applies to."
        },
        {
          "semantic": "deployment_event",
          "row_index": 0,
          "absent_reason": null,
          "note": "The start date and its precision on the same row derive from the methods sentence that states the deployment of the network."
        }
      ],
      "source_locators": [
        "page:10:block:043",
        "page:2:block:002",
        "page:6:block:002",
        "page:1:block:001",
        "page:2:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:campaign:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "entity:obs"
        },
        {
          "row_index": 2,
          "witness_key": "entity:software:global-mapper"
        },
        {
          "row_index": 3,
          "witness_key": "entity:software:gmt"
        },
        {
          "row_index": 4,
          "witness_key": "entity:software:hash"
        },
        {
          "row_index": 5,
          "witness_key": "entity:software:hypodd"
        },
        {
          "row_index": 6,
          "witness_key": "entity:software:nonlinloc"
        },
        {
          "row_index": 7,
          "witness_key": "entity:software:seisan"
        },
        {
          "row_index": 8,
          "witness_key": "entity:software:velest"
        },
        {
          "row_index": 9,
          "witness_key": "entity:software:zmap"
        },
        {
          "row_index": 10,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 11,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 12,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 13,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 14,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 15,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 16,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 17,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 18,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 19,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 20,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 21,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 22,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 23,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 24,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 25,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 26,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 27,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 28,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 29,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 30,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 31,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 32,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 33,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 34,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 35,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 36,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 37,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 38,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 39,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 40,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 41,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 42,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 43,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 44,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 45,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 46,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 47,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 48,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 49,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 50,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 51,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T1-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The article itself is reached by one row. The acceptance date is present in the reading and the ontology gives the published work no place to put it, so neither the event nor its date is carried anywhere in the graph and the question is answered only in part.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "publication_record",
          "row_index": 127,
          "absent_reason": null,
          "note": "One row identifies the article, with its venue, volume, year and identifier."
        },
        {
          "semantic": "acceptance_event",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "The reading states the acceptance alongside the affiliations, and the capture records against that block that the work type declares no slot for a received or accepted date, so no record carries the event."
        },
        {
          "semantic": "calendar_date",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "The date sits in the same unmodelled statement; no record or field in the graph holds it."
        }
      ],
      "source_locators": [
        "page:10:block:045",
        "page:10:block:048",
        "page:11:block:001",
        "page:11:block:003",
        "page:11:block:005",
        "page:11:block:006",
        "page:1:block:001",
        "page:1:block:006",
        "page:2:block:008",
        "page:3:block:006",
        "page:4:block:008",
        "page:5:block:011",
        "page:6:block:006",
        "page:7:block:013",
        "page:8:block:018",
        "page:9:block:056"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:ref:r1"
        },
        {
          "row_index": 49,
          "witness_key": "entity:ref:r10"
        },
        {
          "row_index": 50,
          "witness_key": "entity:ref:r11"
        },
        {
          "row_index": 51,
          "witness_key": "entity:ref:r12"
        },
        {
          "row_index": 52,
          "witness_key": "entity:ref:r13"
        },
        {
          "row_index": 53,
          "witness_key": "entity:ref:r14"
        },
        {
          "row_index": 54,
          "witness_key": "entity:ref:r15"
        },
        {
          "row_index": 55,
          "witness_key": "entity:ref:r16"
        },
        {
          "row_index": 56,
          "witness_key": "entity:ref:r17"
        },
        {
          "row_index": 57,
          "witness_key": "entity:ref:r18"
        },
        {
          "row_index": 58,
          "witness_key": "entity:ref:r19"
        },
        {
          "row_index": 59,
          "witness_key": "entity:ref:r2"
        },
        {
          "row_index": 60,
          "witness_key": "entity:ref:r20"
        },
        {
          "row_index": 61,
          "witness_key": "entity:ref:r21"
        },
        {
          "row_index": 62,
          "witness_key": "entity:ref:r22"
        },
        {
          "row_index": 63,
          "witness_key": "entity:ref:r23"
        },
        {
          "row_index": 64,
          "witness_key": "entity:ref:r24"
        },
        {
          "row_index": 65,
          "witness_key": "entity:ref:r25"
        },
        {
          "row_index": 66,
          "witness_key": "entity:ref:r26"
        },
        {
          "row_index": 67,
          "witness_key": "entity:ref:r27"
        },
        {
          "row_index": 68,
          "witness_key": "entity:ref:r28"
        },
        {
          "row_index": 69,
          "witness_key": "entity:ref:r29"
        },
        {
          "row_index": 70,
          "witness_key": "entity:ref:r3"
        },
        {
          "row_index": 71,
          "witness_key": "entity:ref:r30"
        },
        {
          "row_index": 72,
          "witness_key": "entity:ref:r31"
        },
        {
          "row_index": 73,
          "witness_key": "entity:ref:r32"
        },
        {
          "row_index": 74,
          "witness_key": "entity:ref:r33"
        },
        {
          "row_index": 75,
          "witness_key": "entity:ref:r34"
        },
        {
          "row_index": 76,
          "witness_key": "entity:ref:r35"
        },
        {
          "row_index": 77,
          "witness_key": "entity:ref:r36"
        },
        {
          "row_index": 78,
          "witness_key": "entity:ref:r37"
        },
        {
          "row_index": 79,
          "witness_key": "entity:ref:r38"
        },
        {
          "row_index": 80,
          "witness_key": "entity:ref:r39"
        },
        {
          "row_index": 81,
          "witness_key": "entity:ref:r4"
        },
        {
          "row_index": 82,
          "witness_key": "entity:ref:r40"
        },
        {
          "row_index": 83,
          "witness_key": "entity:ref:r41"
        },
        {
          "row_index": 84,
          "witness_key": "entity:ref:r42"
        },
        {
          "row_index": 85,
          "witness_key": "entity:ref:r43"
        },
        {
          "row_index": 86,
          "witness_key": "entity:ref:r44"
        },
        {
          "row_index": 87,
          "witness_key": "entity:ref:r45"
        },
        {
          "row_index": 88,
          "witness_key": "entity:ref:r46"
        },
        {
          "row_index": 89,
          "witness_key": "entity:ref:r47"
        },
        {
          "row_index": 90,
          "witness_key": "entity:ref:r48"
        },
        {
          "row_index": 91,
          "witness_key": "entity:ref:r49"
        },
        {
          "row_index": 92,
          "witness_key": "entity:ref:r5"
        },
        {
          "row_index": 93,
          "witness_key": "entity:ref:r50"
        },
        {
          "row_index": 94,
          "witness_key": "entity:ref:r51"
        },
        {
          "row_index": 95,
          "witness_key": "entity:ref:r52"
        },
        {
          "row_index": 96,
          "witness_key": "entity:ref:r53"
        },
        {
          "row_index": 97,
          "witness_key": "entity:ref:r54"
        },
        {
          "row_index": 98,
          "witness_key": "entity:ref:r55"
        },
        {
          "row_index": 99,
          "witness_key": "entity:ref:r56"
        },
        {
          "row_index": 100,
          "witness_key": "entity:ref:r57"
        },
        {
          "row_index": 101,
          "witness_key": "entity:ref:r58"
        },
        {
          "row_index": 102,
          "witness_key": "entity:ref:r59"
        },
        {
          "row_index": 103,
          "witness_key": "entity:ref:r6"
        },
        {
          "row_index": 104,
          "witness_key": "entity:ref:r60"
        },
        {
          "row_index": 105,
          "witness_key": "entity:ref:r61"
        },
        {
          "row_index": 106,
          "witness_key": "entity:ref:r62"
        },
        {
          "row_index": 107,
          "witness_key": "entity:ref:r63"
        },
        {
          "row_index": 108,
          "witness_key": "entity:ref:r64"
        },
        {
          "row_index": 109,
          "witness_key": "entity:ref:r65"
        },
        {
          "row_index": 110,
          "witness_key": "entity:ref:r66"
        },
        {
          "row_index": 111,
          "witness_key": "entity:ref:r67"
        },
        {
          "row_index": 112,
          "witness_key": "entity:ref:r68"
        },
        {
          "row_index": 113,
          "witness_key": "entity:ref:r69"
        },
        {
          "row_index": 114,
          "witness_key": "entity:ref:r7"
        },
        {
          "row_index": 115,
          "witness_key": "entity:ref:r70"
        },
        {
          "row_index": 116,
          "witness_key": "entity:ref:r71"
        },
        {
          "row_index": 117,
          "witness_key": "entity:ref:r72"
        },
        {
          "row_index": 118,
          "witness_key": "entity:ref:r73"
        },
        {
          "row_index": 119,
          "witness_key": "entity:ref:r74"
        },
        {
          "row_index": 120,
          "witness_key": "entity:ref:r75"
        },
        {
          "row_index": 121,
          "witness_key": "entity:ref:r76"
        },
        {
          "row_index": 122,
          "witness_key": "entity:ref:r77"
        },
        {
          "row_index": 123,
          "witness_key": "entity:ref:r78"
        },
        {
          "row_index": 124,
          "witness_key": "entity:ref:r79"
        },
        {
          "row_index": 125,
          "witness_key": "entity:ref:r8"
        },
        {
          "row_index": 126,
          "witness_key": "entity:ref:r9"
        },
        {
          "row_index": 127,
          "witness_key": "entity:work:yu-2025"
        }
      ]
    },
    {
      "question_id": "CQ-T1-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The dataset and the repository are two rows joined by a returned deposit relation, so the assembly is linked. The record identifier is the one gap: the block boundary cut it, the completing block was captured as carrying nothing assertable, and no field holds the missing digits.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "dataset_record",
          "row_index": 48,
          "absent_reason": null,
          "note": "One row carries the deposited catalogue and picked arrivals."
        },
        {
          "semantic": "repository_name",
          "row_index": 53,
          "absent_reason": null,
          "note": "A second row names the repository."
        },
        {
          "semantic": "persistent_identifier",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "The repository row's identifier stops exactly where its reading block ends; the digits that complete it fall in the following block, which the capture declared nothing-assertable, so no record carries the record identifier."
        }
      ],
      "source_locators": [
        "page:8:block:008"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:data:earthquake-catalog"
        },
        {
          "row_index": 49,
          "witness_key": "entity:data:petdb"
        },
        {
          "row_index": 50,
          "witness_key": "entity:data:raw-seismic"
        },
        {
          "row_index": 51,
          "witness_key": "entity:data:refraction-profile"
        },
        {
          "row_index": 52,
          "witness_key": "entity:data:seisan-db"
        },
        {
          "row_index": 53,
          "witness_key": "entity:data:zenodo"
        },
        {
          "row_index": 54,
          "witness_key": "relation:catalog:deposited:zenodo"
        }
      ]
    },
    {
      "question_id": "CQ-T1-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names a row. One quantity row carries the interval, its value and its unit; the instruments are a second row, and nothing in the result joins the two.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "recording_interval",
          "row_index": 79,
          "absent_reason": null,
          "note": "One quantity row carries the span of continuous recording."
        },
        {
          "semantic": "duration_value",
          "row_index": 79,
          "absent_reason": null,
          "note": "The same row carries the value and marks it as approximate."
        },
        {
          "semantic": "time_unit",
          "row_index": 79,
          "absent_reason": null,
          "note": "The same row carries the unit."
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "The instrument row names the system that did the recording."
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:1:block:001",
        "page:2:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:campaign:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "entity:obs"
        },
        {
          "row_index": 2,
          "witness_key": "entity:software:global-mapper"
        },
        {
          "row_index": 3,
          "witness_key": "entity:software:gmt"
        },
        {
          "row_index": 4,
          "witness_key": "entity:software:hash"
        },
        {
          "row_index": 5,
          "witness_key": "entity:software:hypodd"
        },
        {
          "row_index": 6,
          "witness_key": "entity:software:nonlinloc"
        },
        {
          "row_index": 7,
          "witness_key": "entity:software:seisan"
        },
        {
          "row_index": 8,
          "witness_key": "entity:software:velest"
        },
        {
          "row_index": 9,
          "witness_key": "entity:software:zmap"
        },
        {
          "row_index": 10,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 11,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 12,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 13,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 14,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 15,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 16,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 17,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 18,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 19,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 20,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 21,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 22,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 23,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 24,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 25,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 26,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 27,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 28,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 29,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 30,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 31,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 32,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 33,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 34,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 35,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 36,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 37,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 38,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 39,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 40,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 41,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 42,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 43,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 44,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 45,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 46,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 47,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 48,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 49,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 50,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 51,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T2-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Three of four are reached and a returned relation joins them, so the answer is assembled rather than inferred. The side of the axis is stated in the very sentence the three rows are bound to and is not modelled anywhere, which is what leaves the question short of complete.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "named_subsection",
          "row_index": 85,
          "absent_reason": null,
          "note": "One row names the subsection and its accretion character."
        },
        {
          "semantic": "structural_feature",
          "row_index": 51,
          "absent_reason": null,
          "note": "A second row carries the bounding fault, its kind and its dip direction."
        },
        {
          "semantic": "bounding_relation",
          "row_index": 95,
          "absent_reason": null,
          "note": "A returned relation row joins the subsection to that fault."
        },
        {
          "semantic": "side_of_axis",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "The same sentence says which side of the ridge axis the core complex sits on. No record carries a side and no relation encodes it; the graph keeps that sentence as a locator and a digest, so the side survives only inside the withheld words."
        }
      ],
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001",
        "page:2:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:askja"
        },
        {
          "row_index": 49,
          "witness_key": "entity:axial-valley-rc1"
        },
        {
          "row_index": 50,
          "witness_key": "entity:chain-tf"
        },
        {
          "row_index": 51,
          "witness_key": "entity:detachment-rc1"
        },
        {
          "row_index": 52,
          "witness_key": "entity:fagradalsfjall"
        },
        {
          "row_index": 53,
          "witness_key": "entity:hydrothermal-mound"
        },
        {
          "row_index": 54,
          "witness_key": "entity:logachev"
        },
        {
          "row_index": 55,
          "witness_key": "entity:main-axial-faults"
        },
        {
          "row_index": 56,
          "witness_key": "entity:mayotte"
        },
        {
          "row_index": 57,
          "witness_key": "entity:mylonite-shear-zones"
        },
        {
          "row_index": 58,
          "witness_key": "entity:ntd1-faults"
        },
        {
          "row_index": 59,
          "witness_key": "entity:ntd1-vent-field"
        },
        {
          "row_index": 60,
          "witness_key": "entity:ntd2-faults"
        },
        {
          "row_index": 61,
          "witness_key": "entity:occ"
        },
        {
          "row_index": 62,
          "witness_key": "entity:occ-corrugated"
        },
        {
          "row_index": 63,
          "witness_key": "entity:occ-dome-faults"
        },
        {
          "row_index": 64,
          "witness_key": "entity:occ-normal-faults"
        },
        {
          "row_index": 65,
          "witness_key": "entity:occ-termination"
        },
        {
          "row_index": 66,
          "witness_key": "entity:rainbow"
        },
        {
          "row_index": 67,
          "witness_key": "entity:rc2-axial-faults"
        },
        {
          "row_index": 68,
          "witness_key": "entity:rc2-bounding-faults"
        },
        {
          "row_index": 69,
          "witness_key": "entity:rc2-hummocky"
        },
        {
          "row_index": 70,
          "witness_key": "entity:rc2-median-valley"
        },
        {
          "row_index": 71,
          "witness_key": "entity:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 72,
          "witness_key": "entity:rc2-volcanic-cones"
        },
        {
          "row_index": 73,
          "witness_key": "entity:romanche-tf"
        },
        {
          "row_index": 74,
          "witness_key": "entity:transform-valley"
        },
        {
          "row_index": 75,
          "witness_key": "entity:bdb"
        },
        {
          "row_index": 76,
          "witness_key": "entity:lab"
        },
        {
          "row_index": 77,
          "witness_key": "entity:moho"
        },
        {
          "row_index": 78,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 79,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 80,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 81,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 82,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 83,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 84,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 85,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 86,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 87,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 88,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 89,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 90,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 91,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 92,
          "witness_key": "relation:occ:cut-by:faults"
        },
        {
          "row_index": 93,
          "witness_key": "relation:logachev:part-of:knipovich"
        },
        {
          "row_index": 94,
          "witness_key": "relation:occ:beneath:mar"
        },
        {
          "row_index": 95,
          "witness_key": "relation:rc1:bounded-by:detachment"
        },
        {
          "row_index": 96,
          "witness_key": "relation:rc2:bounded-by:faults"
        },
        {
          "row_index": 97,
          "witness_key": "relation:rc3:adjacent:rc2"
        }
      ]
    },
    {
      "question_id": "CQ-T2-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Three of four are reached. The ordering is the gap: the two method rows come from the same sentence and that sentence is the only place the sequence exists, so a reader of the rows alone cannot tell which method ran first.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "initial_location_method",
          "row_index": 13,
          "absent_reason": null,
          "note": "One row carries the program that produced the initial hypocentres."
        },
        {
          "semantic": "relocation_method",
          "row_index": 9,
          "absent_reason": null,
          "note": "A second row carries the method applied afterwards."
        },
        {
          "semantic": "method_sequence",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "Both records point at the one sentence that states the order, first locate then relocate. Neither carries an ordering field, no relation in the result joins them, and the sentence is held only as a locator and a digest."
        },
        {
          "semantic": "earthquake_catalog",
          "row_index": 73,
          "absent_reason": null,
          "note": "A third row carries the catalogue the two methods produce."
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:8:block:008"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:obs"
        },
        {
          "row_index": 1,
          "witness_key": "entity:software:global-mapper"
        },
        {
          "row_index": 2,
          "witness_key": "entity:software:gmt"
        },
        {
          "row_index": 3,
          "witness_key": "entity:software:hash"
        },
        {
          "row_index": 4,
          "witness_key": "entity:software:hypodd"
        },
        {
          "row_index": 5,
          "witness_key": "entity:software:nonlinloc"
        },
        {
          "row_index": 6,
          "witness_key": "entity:software:seisan"
        },
        {
          "row_index": 7,
          "witness_key": "entity:software:velest"
        },
        {
          "row_index": 8,
          "witness_key": "entity:software:zmap"
        },
        {
          "row_index": 9,
          "witness_key": "entity:method:double-difference"
        },
        {
          "row_index": 10,
          "witness_key": "entity:method:focal-criterion"
        },
        {
          "row_index": 11,
          "witness_key": "entity:method:local-magnitude"
        },
        {
          "row_index": 12,
          "witness_key": "entity:method:location-criteria"
        },
        {
          "row_index": 13,
          "witness_key": "entity:method:nonlinear-location"
        },
        {
          "row_index": 14,
          "witness_key": "entity:method:octtree"
        },
        {
          "row_index": 15,
          "witness_key": "entity:method:stalta"
        },
        {
          "row_index": 16,
          "witness_key": "entity:method:wadati"
        },
        {
          "row_index": 17,
          "witness_key": "entity:model:1d-velocity"
        },
        {
          "row_index": 18,
          "witness_key": "entity:model:average-velocity"
        },
        {
          "row_index": 19,
          "witness_key": "entity:model:co2-solubility"
        },
        {
          "row_index": 20,
          "witness_key": "entity:model:fastest"
        },
        {
          "row_index": 21,
          "witness_key": "entity:model:five-velocity"
        },
        {
          "row_index": 22,
          "witness_key": "entity:model:iacono-marziano"
        },
        {
          "row_index": 23,
          "witness_key": "entity:model:minimum-velocity"
        },
        {
          "row_index": 24,
          "witness_key": "entity:model:thermal"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 48,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 49,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 50,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 51,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 52,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 53,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 54,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 55,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 56,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 57,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 58,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 59,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 60,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 61,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 62,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 63,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 64,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 65,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 66,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 67,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 68,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 69,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 70,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 71,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 72,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 73,
          "witness_key": "entity:data:earthquake-catalog"
        },
        {
          "row_index": 74,
          "witness_key": "entity:data:petdb"
        },
        {
          "row_index": 75,
          "witness_key": "entity:data:raw-seismic"
        },
        {
          "row_index": 76,
          "witness_key": "entity:data:refraction-profile"
        },
        {
          "row_index": 77,
          "witness_key": "entity:data:seisan-db"
        },
        {
          "row_index": 78,
          "witness_key": "entity:data:zenodo"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 158,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 159,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 160,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 161,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 162,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 163,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 164,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 165,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 166,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 167,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 168,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 169,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 170,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 171,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 172,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 173,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 174,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 175,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 176,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 177,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 178,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 179,
          "witness_key": "relation:catalog:deposited:zenodo"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 212,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 213,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 214,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 215,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 216,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 217,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 218,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 219,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 220,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 221,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 222,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 223,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 224,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 225,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 226,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 227,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T2-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The feature and the discontinuity are each reached, but both halves of the position question are absent. The sentence that carries them formalized into no relation and no record for the present-day axis, so the graph holds the placement only as words behind a digest.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "named_feature",
          "row_index": 59,
          "absent_reason": null,
          "note": "One row carries the vent field and its inactive status."
        },
        {
          "semantic": "host_discontinuity",
          "row_index": 180,
          "absent_reason": null,
          "note": "A second row carries the discontinuity itself; the hosting relation between the two is not in either row, which the next entry records."
        },
        {
          "semantic": "spatial_relation",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "The sentence places the vent field on the eastern flank of the discontinuity and relatively far from the present-day axial valley. No relation record was derived from it and neither row carries a position, so the placement stays inside the statement the vent-field record locks by digest."
        },
        {
          "semantic": "present_day_axis",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "The axial valley the position is measured against appears only in that same sentence; no record was created for it, so nothing in the result identifies the reference the question asks about."
        }
      ],
      "source_locators": [
        "page:3:block:002",
        "page:1:block:005",
        "page:2:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:askja"
        },
        {
          "row_index": 49,
          "witness_key": "entity:axial-valley-rc1"
        },
        {
          "row_index": 50,
          "witness_key": "entity:chain-tf"
        },
        {
          "row_index": 51,
          "witness_key": "entity:detachment-rc1"
        },
        {
          "row_index": 52,
          "witness_key": "entity:fagradalsfjall"
        },
        {
          "row_index": 53,
          "witness_key": "entity:hydrothermal-mound"
        },
        {
          "row_index": 54,
          "witness_key": "entity:logachev"
        },
        {
          "row_index": 55,
          "witness_key": "entity:main-axial-faults"
        },
        {
          "row_index": 56,
          "witness_key": "entity:mayotte"
        },
        {
          "row_index": 57,
          "witness_key": "entity:mylonite-shear-zones"
        },
        {
          "row_index": 58,
          "witness_key": "entity:ntd1-faults"
        },
        {
          "row_index": 59,
          "witness_key": "entity:ntd1-vent-field"
        },
        {
          "row_index": 60,
          "witness_key": "entity:ntd2-faults"
        },
        {
          "row_index": 61,
          "witness_key": "entity:occ"
        },
        {
          "row_index": 62,
          "witness_key": "entity:occ-corrugated"
        },
        {
          "row_index": 63,
          "witness_key": "entity:occ-dome-faults"
        },
        {
          "row_index": 64,
          "witness_key": "entity:occ-normal-faults"
        },
        {
          "row_index": 65,
          "witness_key": "entity:occ-termination"
        },
        {
          "row_index": 66,
          "witness_key": "entity:rainbow"
        },
        {
          "row_index": 67,
          "witness_key": "entity:rc2-axial-faults"
        },
        {
          "row_index": 68,
          "witness_key": "entity:rc2-bounding-faults"
        },
        {
          "row_index": 69,
          "witness_key": "entity:rc2-hummocky"
        },
        {
          "row_index": 70,
          "witness_key": "entity:rc2-median-valley"
        },
        {
          "row_index": 71,
          "witness_key": "entity:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 72,
          "witness_key": "entity:rc2-volcanic-cones"
        },
        {
          "row_index": 73,
          "witness_key": "entity:romanche-tf"
        },
        {
          "row_index": 74,
          "witness_key": "entity:transform-valley"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 158,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 159,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 160,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 161,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 162,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 163,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 164,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 165,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 166,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 167,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 168,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 169,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 170,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 171,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 172,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 173,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 174,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 175,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 176,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 177,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 178,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 179,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 180,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 181,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 182,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 183,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 184,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 185,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 186,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 187,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 188,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 189,
          "witness_key": "relation:occ:cut-by:faults"
        },
        {
          "row_index": 190,
          "witness_key": "relation:logachev:part-of:knipovich"
        },
        {
          "row_index": 191,
          "witness_key": "relation:occ:beneath:mar"
        },
        {
          "row_index": 192,
          "witness_key": "relation:rc1:bounded-by:detachment"
        },
        {
          "row_index": 193,
          "witness_key": "relation:rc2:bounded-by:faults"
        },
        {
          "row_index": 194,
          "witness_key": "relation:rc3:adjacent:rc2"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:tf-coverage"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 212,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 213,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 214,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 215,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 216,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 217,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 218,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 219,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 220,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 221,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 222,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 223,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 224,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 225,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 226,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 227,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 228,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 229,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 230,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 231,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 232,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 233,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 234,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 235,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 236,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 237,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 238,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 239,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 240,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 241,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 242,
          "witness_key": "entity:q:swir-bdb-depth"
        }
      ]
    },
    {
      "question_id": "CQ-T2-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names a row, three of them the same quantity row. Nothing in the result joins the thickness to the study it comes from: the case set carries a scholarly relation type but no citation relation was derived, so a reader has to match the reference number in the block by hand.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "source_study",
          "row_index": 183,
          "absent_reason": null,
          "note": "One row carries the earlier study; the tie from the thickness to it is a superscript in the block rather than a relation in the result."
        },
        {
          "semantic": "crustal_thickness_claim",
          "row_index": 254,
          "absent_reason": null,
          "note": "A second row carries the thickness with its uncertainty and unit."
        },
        {
          "semantic": "location_relation",
          "row_index": 254,
          "absent_reason": null,
          "note": "The subject reference on that same row points at the crust of the western ridge flank, which is the location the thickness belongs to."
        },
        {
          "semantic": "crustal_age",
          "row_index": 254,
          "absent_reason": null,
          "note": "The age of that crust is carried inside the quantity's own label on the same row, not as a separate age quantity."
        }
      ],
      "source_locators": [
        "page:9:block:036",
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:brittle-lithosphere"
        },
        {
          "row_index": 49,
          "witness_key": "entity:crust-free-lithosphere"
        },
        {
          "row_index": 50,
          "witness_key": "entity:exhumed-mantle"
        },
        {
          "row_index": 51,
          "witness_key": "entity:lower-crust"
        },
        {
          "row_index": 52,
          "witness_key": "entity:mantle"
        },
        {
          "row_index": 53,
          "witness_key": "entity:mantle-source"
        },
        {
          "row_index": 54,
          "witness_key": "entity:oceanic-crust"
        },
        {
          "row_index": 55,
          "witness_key": "entity:oceanic-lithosphere"
        },
        {
          "row_index": 56,
          "witness_key": "entity:sediment-layers"
        },
        {
          "row_index": 57,
          "witness_key": "entity:western-flank-crust"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 158,
          "witness_key": "entity:ref:r1"
        },
        {
          "row_index": 159,
          "witness_key": "entity:ref:r10"
        },
        {
          "row_index": 160,
          "witness_key": "entity:ref:r11"
        },
        {
          "row_index": 161,
          "witness_key": "entity:ref:r12"
        },
        {
          "row_index": 162,
          "witness_key": "entity:ref:r13"
        },
        {
          "row_index": 163,
          "witness_key": "entity:ref:r14"
        },
        {
          "row_index": 164,
          "witness_key": "entity:ref:r15"
        },
        {
          "row_index": 165,
          "witness_key": "entity:ref:r16"
        },
        {
          "row_index": 166,
          "witness_key": "entity:ref:r17"
        },
        {
          "row_index": 167,
          "witness_key": "entity:ref:r18"
        },
        {
          "row_index": 168,
          "witness_key": "entity:ref:r19"
        },
        {
          "row_index": 169,
          "witness_key": "entity:ref:r2"
        },
        {
          "row_index": 170,
          "witness_key": "entity:ref:r20"
        },
        {
          "row_index": 171,
          "witness_key": "entity:ref:r21"
        },
        {
          "row_index": 172,
          "witness_key": "entity:ref:r22"
        },
        {
          "row_index": 173,
          "witness_key": "entity:ref:r23"
        },
        {
          "row_index": 174,
          "witness_key": "entity:ref:r24"
        },
        {
          "row_index": 175,
          "witness_key": "entity:ref:r25"
        },
        {
          "row_index": 176,
          "witness_key": "entity:ref:r26"
        },
        {
          "row_index": 177,
          "witness_key": "entity:ref:r27"
        },
        {
          "row_index": 178,
          "witness_key": "entity:ref:r28"
        },
        {
          "row_index": 179,
          "witness_key": "entity:ref:r29"
        },
        {
          "row_index": 180,
          "witness_key": "entity:ref:r3"
        },
        {
          "row_index": 181,
          "witness_key": "entity:ref:r30"
        },
        {
          "row_index": 182,
          "witness_key": "entity:ref:r31"
        },
        {
          "row_index": 183,
          "witness_key": "entity:ref:r32"
        },
        {
          "row_index": 184,
          "witness_key": "entity:ref:r33"
        },
        {
          "row_index": 185,
          "witness_key": "entity:ref:r34"
        },
        {
          "row_index": 186,
          "witness_key": "entity:ref:r35"
        },
        {
          "row_index": 187,
          "witness_key": "entity:ref:r36"
        },
        {
          "row_index": 188,
          "witness_key": "entity:ref:r37"
        },
        {
          "row_index": 189,
          "witness_key": "entity:ref:r38"
        },
        {
          "row_index": 190,
          "witness_key": "entity:ref:r39"
        },
        {
          "row_index": 191,
          "witness_key": "entity:ref:r4"
        },
        {
          "row_index": 192,
          "witness_key": "entity:ref:r40"
        },
        {
          "row_index": 193,
          "witness_key": "entity:ref:r41"
        },
        {
          "row_index": 194,
          "witness_key": "entity:ref:r42"
        },
        {
          "row_index": 195,
          "witness_key": "entity:ref:r43"
        },
        {
          "row_index": 196,
          "witness_key": "entity:ref:r44"
        },
        {
          "row_index": 197,
          "witness_key": "entity:ref:r45"
        },
        {
          "row_index": 198,
          "witness_key": "entity:ref:r46"
        },
        {
          "row_index": 199,
          "witness_key": "entity:ref:r47"
        },
        {
          "row_index": 200,
          "witness_key": "entity:ref:r48"
        },
        {
          "row_index": 201,
          "witness_key": "entity:ref:r49"
        },
        {
          "row_index": 202,
          "witness_key": "entity:ref:r5"
        },
        {
          "row_index": 203,
          "witness_key": "entity:ref:r50"
        },
        {
          "row_index": 204,
          "witness_key": "entity:ref:r51"
        },
        {
          "row_index": 205,
          "witness_key": "entity:ref:r52"
        },
        {
          "row_index": 206,
          "witness_key": "entity:ref:r53"
        },
        {
          "row_index": 207,
          "witness_key": "entity:ref:r54"
        },
        {
          "row_index": 208,
          "witness_key": "entity:ref:r55"
        },
        {
          "row_index": 209,
          "witness_key": "entity:ref:r56"
        },
        {
          "row_index": 210,
          "witness_key": "entity:ref:r57"
        },
        {
          "row_index": 211,
          "witness_key": "entity:ref:r58"
        },
        {
          "row_index": 212,
          "witness_key": "entity:ref:r59"
        },
        {
          "row_index": 213,
          "witness_key": "entity:ref:r6"
        },
        {
          "row_index": 214,
          "witness_key": "entity:ref:r60"
        },
        {
          "row_index": 215,
          "witness_key": "entity:ref:r61"
        },
        {
          "row_index": 216,
          "witness_key": "entity:ref:r62"
        },
        {
          "row_index": 217,
          "witness_key": "entity:ref:r63"
        },
        {
          "row_index": 218,
          "witness_key": "entity:ref:r64"
        },
        {
          "row_index": 219,
          "witness_key": "entity:ref:r65"
        },
        {
          "row_index": 220,
          "witness_key": "entity:ref:r66"
        },
        {
          "row_index": 221,
          "witness_key": "entity:ref:r67"
        },
        {
          "row_index": 222,
          "witness_key": "entity:ref:r68"
        },
        {
          "row_index": 223,
          "witness_key": "entity:ref:r69"
        },
        {
          "row_index": 224,
          "witness_key": "entity:ref:r7"
        },
        {
          "row_index": 225,
          "witness_key": "entity:ref:r70"
        },
        {
          "row_index": 226,
          "witness_key": "entity:ref:r71"
        },
        {
          "row_index": 227,
          "witness_key": "entity:ref:r72"
        },
        {
          "row_index": 228,
          "witness_key": "entity:ref:r73"
        },
        {
          "row_index": 229,
          "witness_key": "entity:ref:r74"
        },
        {
          "row_index": 230,
          "witness_key": "entity:ref:r75"
        },
        {
          "row_index": 231,
          "witness_key": "entity:ref:r76"
        },
        {
          "row_index": 232,
          "witness_key": "entity:ref:r77"
        },
        {
          "row_index": 233,
          "witness_key": "entity:ref:r78"
        },
        {
          "row_index": 234,
          "witness_key": "entity:ref:r79"
        },
        {
          "row_index": 235,
          "witness_key": "entity:ref:r8"
        },
        {
          "row_index": 236,
          "witness_key": "entity:ref:r9"
        },
        {
          "row_index": 237,
          "witness_key": "entity:work:yu-2025"
        },
        {
          "row_index": 238,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 239,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 240,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 241,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 242,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 243,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 244,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 245,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 246,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 247,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 248,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 249,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 250,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 251,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 252,
          "witness_key": "relation:rc3:adjacent:rc2"
        },
        {
          "row_index": 253,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 254,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 255,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 256,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 257,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 258,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 259,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 260,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 261,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 262,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 263,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 264,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 265,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 266,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 267,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 268,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 269,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 270,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 271,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 272,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 273,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 274,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 275,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 276,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 277,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 278,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 279,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 280,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 281,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 282,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 283,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 284,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 285,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 286,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 287,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 288,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 289,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 290,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 291,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 292,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 293,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 294,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 295,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 296,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 297,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 298,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 299,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 300,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T2-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names a row and returned relations join them, so the answer is assembled from the result rather than inferred. The link from the author to the grant is indirect: two relations meet at the funder rather than one relation tying the person to the award.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "funding_record",
          "row_index": 17,
          "absent_reason": null,
          "note": "One row carries the named grant agreement."
        },
        {
          "semantic": "grant_identifier",
          "row_index": 17,
          "absent_reason": null,
          "note": "The same row carries its identifier."
        },
        {
          "semantic": "person",
          "row_index": 15,
          "absent_reason": null,
          "note": "A second row carries the author the grant is attributed to."
        },
        {
          "semantic": "attribution_relation",
          "row_index": 22,
          "absent_reason": null,
          "note": "A returned relation joins that author to the funder; a second returned relation joins the award to the same funder, so the attribution runs through the shared endpoint."
        }
      ],
      "source_locators": [
        "page:10:block:044",
        "page:11:block:002",
        "page:1:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:funder:erc"
        },
        {
          "row_index": 1,
          "witness_key": "entity:funder:nsfc"
        },
        {
          "row_index": 2,
          "witness_key": "entity:funder:zjnsf"
        },
        {
          "row_index": 3,
          "witness_key": "entity:org:1"
        },
        {
          "row_index": 4,
          "witness_key": "entity:org:2"
        },
        {
          "row_index": 5,
          "witness_key": "entity:org:3"
        },
        {
          "row_index": 6,
          "witness_key": "entity:org:4"
        },
        {
          "row_index": 7,
          "witness_key": "entity:org:5"
        },
        {
          "row_index": 8,
          "witness_key": "entity:org:6"
        },
        {
          "row_index": 9,
          "witness_key": "entity:person:briais"
        },
        {
          "row_index": 10,
          "witness_key": "entity:person:brunelli"
        },
        {
          "row_index": 11,
          "witness_key": "entity:person:grenet"
        },
        {
          "row_index": 12,
          "witness_key": "entity:person:hamelin"
        },
        {
          "row_index": 13,
          "witness_key": "entity:person:maia"
        },
        {
          "row_index": 14,
          "witness_key": "entity:person:petracchini"
        },
        {
          "row_index": 15,
          "witness_key": "entity:person:singh"
        },
        {
          "row_index": 16,
          "witness_key": "entity:person:yu"
        },
        {
          "row_index": 17,
          "witness_key": "entity:award:erc1"
        },
        {
          "row_index": 18,
          "witness_key": "entity:award:isblue"
        },
        {
          "row_index": 19,
          "witness_key": "entity:award:nsfc1"
        },
        {
          "row_index": 20,
          "witness_key": "entity:award:nsfc2"
        },
        {
          "row_index": 21,
          "witness_key": "entity:award:zjnsf1"
        },
        {
          "row_index": 22,
          "witness_key": "relation:singh:funded-by:erc"
        },
        {
          "row_index": 23,
          "witness_key": "relation:yu:funded-by:nsfc"
        },
        {
          "row_index": 24,
          "witness_key": "relation:yu:funded-by:zjnsf"
        },
        {
          "row_index": 25,
          "witness_key": "relation:erc1:awarded-by:erc"
        },
        {
          "row_index": 26,
          "witness_key": "relation:nsfc1:awarded-by:nsfc"
        },
        {
          "row_index": 27,
          "witness_key": "relation:nsfc2:awarded-by:nsfc"
        },
        {
          "row_index": 28,
          "witness_key": "relation:zjnsf1:awarded-by:zjnsf"
        }
      ]
    },
    {
      "question_id": "CQ-T3-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names a row. Four come from one quantity row; the reference surface has to be picked up from a second row bound to a different block, and nothing in the result joins the two.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 165,
          "absent_reason": null,
          "note": "One row carries the depth range of the deep earthquakes beneath the segment axis."
        },
        {
          "semantic": "length_unit",
          "row_index": 165,
          "absent_reason": null,
          "note": "The same row carries the unit."
        },
        {
          "semantic": "quantity_subject",
          "row_index": 165,
          "absent_reason": null,
          "note": "Its subject reference points at the magmatic segment the depths belong to."
        },
        {
          "semantic": "measurement_status",
          "row_index": 165,
          "absent_reason": null,
          "note": "The same row's modality marks the range as this study's own observation rather than a figure taken from elsewhere."
        },
        {
          "semantic": "depth_reference_surface",
          "row_index": 168,
          "absent_reason": null,
          "note": "A second row's quantity label states that the depths are measured below the seafloor; the sentence behind the first row does not say so."
        }
      ],
      "source_locators": [
        "page:2:block:006",
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 49,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 50,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 51,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 148,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 149,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 150,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 151,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 152,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 153,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 154,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 155,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 156,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 157,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 158,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 159,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 160,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 161,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 162,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 163,
          "witness_key": "relation:rc3:adjacent:rc2"
        },
        {
          "row_index": 164,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 165,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 166,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 167,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 168,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 169,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 170,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 171,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 172,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 173,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 174,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 175,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 176,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 177,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 178,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 179,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T3-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names the same row, so one returned row carries the whole answer.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 180,
          "absent_reason": null,
          "note": "One row carries the reported range."
        },
        {
          "semantic": "concentration_unit",
          "row_index": 180,
          "absent_reason": null,
          "note": "The same row carries the unit."
        },
        {
          "semantic": "quantity_subject",
          "row_index": 180,
          "absent_reason": null,
          "note": "Its subject reference points at the primary melts."
        },
        {
          "semantic": "calculated_or_measured_status",
          "row_index": 180,
          "absent_reason": null,
          "note": "The same row's modality and determination both mark the figure as calculated rather than measured."
        }
      ],
      "source_locators": [
        "page:1:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:melt:ascending"
        },
        {
          "row_index": 49,
          "witness_key": "entity:melt:pre-eruptive"
        },
        {
          "row_index": 50,
          "witness_key": "entity:melt:primary"
        },
        {
          "row_index": 51,
          "witness_key": "entity:melt:primitive"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 152,
          "witness_key": "entity:ratio:co2-ba"
        },
        {
          "row_index": 153,
          "witness_key": "entity:ratio:co2-rb"
        },
        {
          "row_index": 154,
          "witness_key": "entity:ratio:vpvs"
        },
        {
          "row_index": 155,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 156,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 157,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 158,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 159,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 160,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 161,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 162,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 163,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 164,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 165,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 166,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 167,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 168,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 169,
          "witness_key": "entity:anhydrous-peridotite"
        },
        {
          "row_index": 170,
          "witness_key": "entity:basaltic-rocks"
        },
        {
          "row_index": 171,
          "witness_key": "entity:basalts-seafloor"
        },
        {
          "row_index": 172,
          "witness_key": "entity:mantle-peridotites"
        },
        {
          "row_index": 173,
          "witness_key": "entity:melt-inclusions"
        },
        {
          "row_index": 174,
          "witness_key": "entity:morb-samples"
        },
        {
          "row_index": 175,
          "witness_key": "entity:peridotite-seafloor"
        },
        {
          "row_index": 176,
          "witness_key": "entity:pillow-basalts"
        },
        {
          "row_index": 177,
          "witness_key": "entity:popping-rocks"
        },
        {
          "row_index": 178,
          "witness_key": "relation:rc3:adjacent:rc2"
        },
        {
          "row_index": 179,
          "witness_key": "relation:morb:sampled-from:rc2"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 212,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 213,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 214,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 215,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 216,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 217,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 218,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 219,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 220,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 221,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 222,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 223,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 224,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 225,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 226,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 227,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T3-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names a row. The melt stage sits in a separate row because this quantity record carries no subject reference, and nothing in the result joins the two rows.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 118,
          "absent_reason": null,
          "note": "One row carries the pre-eruptive range."
        },
        {
          "semantic": "concentration_unit",
          "row_index": 118,
          "absent_reason": null,
          "note": "The same row carries the unit."
        },
        {
          "semantic": "melt_stage",
          "row_index": 49,
          "absent_reason": null,
          "note": "A second row carries the melt and its pre-eruptive stage; the quantity row itself is returned without a subject reference."
        },
        {
          "semantic": "estimation_status",
          "row_index": 118,
          "absent_reason": null,
          "note": "The determination on the quantity row marks the range as an estimate."
        }
      ],
      "source_locators": [
        "page:5:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:melt:ascending"
        },
        {
          "row_index": 49,
          "witness_key": "entity:melt:pre-eruptive"
        },
        {
          "row_index": 50,
          "witness_key": "entity:melt:primary"
        },
        {
          "row_index": 51,
          "witness_key": "entity:melt:primitive"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 152,
          "witness_key": "entity:ratio:co2-ba"
        },
        {
          "row_index": 153,
          "witness_key": "entity:ratio:co2-rb"
        },
        {
          "row_index": 154,
          "witness_key": "entity:ratio:vpvs"
        },
        {
          "row_index": 155,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 156,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 157,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 158,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 159,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 160,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 161,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 162,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 163,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 164,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 165,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 166,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 167,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 168,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 169,
          "witness_key": "entity:anhydrous-peridotite"
        },
        {
          "row_index": 170,
          "witness_key": "entity:basaltic-rocks"
        },
        {
          "row_index": 171,
          "witness_key": "entity:basalts-seafloor"
        },
        {
          "row_index": 172,
          "witness_key": "entity:mantle-peridotites"
        },
        {
          "row_index": 173,
          "witness_key": "entity:melt-inclusions"
        },
        {
          "row_index": 174,
          "witness_key": "entity:morb-samples"
        },
        {
          "row_index": 175,
          "witness_key": "entity:peridotite-seafloor"
        },
        {
          "row_index": 176,
          "witness_key": "entity:pillow-basalts"
        },
        {
          "row_index": 177,
          "witness_key": "entity:popping-rocks"
        },
        {
          "row_index": 178,
          "witness_key": "relation:rc3:adjacent:rc2"
        },
        {
          "row_index": 179,
          "witness_key": "relation:morb:sampled-from:rc2"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 212,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 213,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 214,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 215,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 216,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 217,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 218,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 219,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 220,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 221,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 222,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 223,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 224,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 225,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 226,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 227,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T3-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Four of five are reached, from two rows nothing joins. The quantity itself has no subject reference, so the tie between the average uncertainty and the event set has to be made by the reader from the two rows' labels.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 165,
          "absent_reason": null,
          "note": "One row carries the updated average horizontal uncertainty."
        },
        {
          "semantic": "length_unit",
          "row_index": 165,
          "absent_reason": null,
          "note": "The same row carries the unit."
        },
        {
          "semantic": "quantity_subject",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "The uncertainty record's subject slot is absent, so it is returned with no subject and no field on it says which body of events the average describes."
        },
        {
          "semantic": "derivation_status",
          "row_index": 165,
          "absent_reason": null,
          "note": "The row's modality marks the figure as calculated."
        },
        {
          "semantic": "event_set",
          "row_index": 143,
          "absent_reason": null,
          "note": "A second row carries the count of well relocated events that replaced the earlier locations in the final catalogue."
        }
      ],
      "source_locators": [
        "page:7:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:obs"
        },
        {
          "row_index": 1,
          "witness_key": "entity:software:global-mapper"
        },
        {
          "row_index": 2,
          "witness_key": "entity:software:gmt"
        },
        {
          "row_index": 3,
          "witness_key": "entity:software:hash"
        },
        {
          "row_index": 4,
          "witness_key": "entity:software:hypodd"
        },
        {
          "row_index": 5,
          "witness_key": "entity:software:nonlinloc"
        },
        {
          "row_index": 6,
          "witness_key": "entity:software:seisan"
        },
        {
          "row_index": 7,
          "witness_key": "entity:software:velest"
        },
        {
          "row_index": 8,
          "witness_key": "entity:software:zmap"
        },
        {
          "row_index": 9,
          "witness_key": "entity:method:double-difference"
        },
        {
          "row_index": 10,
          "witness_key": "entity:method:focal-criterion"
        },
        {
          "row_index": 11,
          "witness_key": "entity:method:local-magnitude"
        },
        {
          "row_index": 12,
          "witness_key": "entity:method:location-criteria"
        },
        {
          "row_index": 13,
          "witness_key": "entity:method:nonlinear-location"
        },
        {
          "row_index": 14,
          "witness_key": "entity:method:octtree"
        },
        {
          "row_index": 15,
          "witness_key": "entity:method:stalta"
        },
        {
          "row_index": 16,
          "witness_key": "entity:method:wadati"
        },
        {
          "row_index": 17,
          "witness_key": "entity:model:1d-velocity"
        },
        {
          "row_index": 18,
          "witness_key": "entity:model:average-velocity"
        },
        {
          "row_index": 19,
          "witness_key": "entity:model:co2-solubility"
        },
        {
          "row_index": 20,
          "witness_key": "entity:model:fastest"
        },
        {
          "row_index": 21,
          "witness_key": "entity:model:five-velocity"
        },
        {
          "row_index": 22,
          "witness_key": "entity:model:iacono-marziano"
        },
        {
          "row_index": 23,
          "witness_key": "entity:model:minimum-velocity"
        },
        {
          "row_index": 24,
          "witness_key": "entity:model:thermal"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 48,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 49,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 50,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 51,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 52,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 53,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 54,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 55,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 56,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 57,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 58,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 59,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 60,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 61,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 62,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 63,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 64,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 65,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 66,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 67,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 68,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 69,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 70,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 71,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 72,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 158,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 159,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 160,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 161,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 162,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 163,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 164,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 165,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 166,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 167,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 168,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 169,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 170,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 171,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 172,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 173,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 174,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 175,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 176,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 177,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 178,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 179,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 212,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 213,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 214,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 215,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 216,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 217,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 218,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 219,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 220,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 221,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T3-05",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Four of five are reached across two quantity rows that nothing joins. Neither quantity carries a subject, so the melt the conditions belong to is missing from the returned rows.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 147,
          "absent_reason": null,
          "note": "One row carries the saturation pressure."
        },
        {
          "semantic": "pressure_unit",
          "row_index": 147,
          "absent_reason": null,
          "note": "The same row carries the pressure unit."
        },
        {
          "semantic": "temperature_unit",
          "row_index": 148,
          "absent_reason": null,
          "note": "A second row carries the temperature and its unit."
        },
        {
          "semantic": "quantity_subject",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "Both saturation quantities are returned without a subject: their subject slots are absent, so no row ties the pressure or the temperature to the melt they describe."
        },
        {
          "semantic": "model_derived_status",
          "row_index": 147,
          "absent_reason": null,
          "note": "The determination on the pressure row marks it as obtained from a model, and a further row carries the solubility model itself."
        }
      ],
      "source_locators": [
        "page:5:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:method:double-difference"
        },
        {
          "row_index": 1,
          "witness_key": "entity:method:focal-criterion"
        },
        {
          "row_index": 2,
          "witness_key": "entity:method:local-magnitude"
        },
        {
          "row_index": 3,
          "witness_key": "entity:method:location-criteria"
        },
        {
          "row_index": 4,
          "witness_key": "entity:method:nonlinear-location"
        },
        {
          "row_index": 5,
          "witness_key": "entity:method:octtree"
        },
        {
          "row_index": 6,
          "witness_key": "entity:method:stalta"
        },
        {
          "row_index": 7,
          "witness_key": "entity:method:wadati"
        },
        {
          "row_index": 8,
          "witness_key": "entity:model:1d-velocity"
        },
        {
          "row_index": 9,
          "witness_key": "entity:model:average-velocity"
        },
        {
          "row_index": 10,
          "witness_key": "entity:model:co2-solubility"
        },
        {
          "row_index": 11,
          "witness_key": "entity:model:fastest"
        },
        {
          "row_index": 12,
          "witness_key": "entity:model:five-velocity"
        },
        {
          "row_index": 13,
          "witness_key": "entity:model:iacono-marziano"
        },
        {
          "row_index": 14,
          "witness_key": "entity:model:minimum-velocity"
        },
        {
          "row_index": 15,
          "witness_key": "entity:model:thermal"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 48,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 49,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 50,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 51,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 52,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 53,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 54,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 55,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 56,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 57,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 58,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 59,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 60,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 61,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 62,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 63,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 64,
          "witness_key": "entity:melt:ascending"
        },
        {
          "row_index": 65,
          "witness_key": "entity:melt:pre-eruptive"
        },
        {
          "row_index": 66,
          "witness_key": "entity:melt:primary"
        },
        {
          "row_index": 67,
          "witness_key": "entity:melt:primitive"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 158,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 159,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 160,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 161,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 162,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 163,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 164,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 165,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 166,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 167,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 168,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 169,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 170,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 171,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 172,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 173,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 174,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 175,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 176,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 177,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 178,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 179,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 212,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 213,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 214,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 215,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T4-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names the same row, so one returned row carries the whole answer, including the strength of the claim and which explanation it is.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "causal_claim",
          "row_index": 2,
          "absent_reason": null,
          "note": "One row carries the explanation the authors put forward."
        },
        {
          "semantic": "preferred_disposition",
          "row_index": 2,
          "absent_reason": null,
          "note": "Its disposition marks it as the preferred one, derived from the later block that says so."
        },
        {
          "semantic": "epistemic_modality",
          "row_index": 2,
          "absent_reason": null,
          "note": "Its modality marks the claim as hypothesised, matching how the abstract states it."
        },
        {
          "semantic": "claim_subject",
          "row_index": 2,
          "absent_reason": null,
          "note": "The claim's own name identifies what it is about, the deep earthquakes in the mantle."
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:melt:ascending"
        },
        {
          "row_index": 49,
          "witness_key": "entity:melt:pre-eruptive"
        },
        {
          "row_index": 50,
          "witness_key": "entity:melt:primary"
        },
        {
          "row_index": 51,
          "witness_key": "entity:melt:primitive"
        },
        {
          "row_index": 52,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 53,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 54,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 55,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 56,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 57,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 58,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 59,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 60,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 61,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 62,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 63,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 64,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 65,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 66,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 67,
          "witness_key": "relation:rc3:adjacent:rc2"
        }
      ]
    },
    {
      "question_id": "CQ-T4-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names a row. The ground for setting the explanation aside is a separate claim row and no relation in the result joins it to the claim it rebuts.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "candidate_mechanism",
          "row_index": 18,
          "absent_reason": null,
          "note": "One row carries the melt-movement explanation."
        },
        {
          "semantic": "declined_disposition",
          "row_index": 18,
          "absent_reason": null,
          "note": "Its disposition marks it as not supported, derived from the block that sets it aside."
        },
        {
          "semantic": "stated_ground",
          "row_index": 5,
          "absent_reason": null,
          "note": "A second row carries the reason given, that the comparison settings are unlike a mid-ocean ridge."
        },
        {
          "semantic": "claim_subject",
          "row_index": 18,
          "absent_reason": null,
          "note": "The candidate row's name identifies the deep earthquakes it is about."
        }
      ],
      "source_locators": [
        "page:4:block:002",
        "page:5:block:001",
        "page:4:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:melt:ascending"
        },
        {
          "row_index": 49,
          "witness_key": "entity:melt:pre-eruptive"
        },
        {
          "row_index": 50,
          "witness_key": "entity:melt:primary"
        },
        {
          "row_index": 51,
          "witness_key": "entity:melt:primitive"
        },
        {
          "row_index": 52,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 53,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 54,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 55,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 56,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 57,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 58,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 59,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 60,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 61,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 62,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 63,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 64,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 65,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 66,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 67,
          "witness_key": "relation:rc3:adjacent:rc2"
        }
      ]
    },
    {
      "question_id": "CQ-T4-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names the same row. The claim it qualifies is identified inside that row's own text rather than by a link to a separate estimate record, so the answer is complete but the relation is textual.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "qualified_claim",
          "row_index": 59,
          "absent_reason": null,
          "note": "The row's own name states which activity the caveat attaches to, the estimation of carbon dioxide from trace element abundances."
        },
        {
          "semantic": "stated_assumption",
          "row_index": 59,
          "absent_reason": null,
          "note": "The same row states the assumption, that the trace elements reflect the mantle source."
        },
        {
          "semantic": "caveat_disposition",
          "row_index": 59,
          "absent_reason": null,
          "note": "Its claim kind marks it as an assumption rather than a finding."
        },
        {
          "semantic": "claim_subject",
          "row_index": 59,
          "absent_reason": null,
          "note": "The same name identifies the subject of the caveat."
        }
      ],
      "source_locators": [
        "page:5:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:method:double-difference"
        },
        {
          "row_index": 1,
          "witness_key": "entity:method:focal-criterion"
        },
        {
          "row_index": 2,
          "witness_key": "entity:method:local-magnitude"
        },
        {
          "row_index": 3,
          "witness_key": "entity:method:location-criteria"
        },
        {
          "row_index": 4,
          "witness_key": "entity:method:nonlinear-location"
        },
        {
          "row_index": 5,
          "witness_key": "entity:method:octtree"
        },
        {
          "row_index": 6,
          "witness_key": "entity:method:stalta"
        },
        {
          "row_index": 7,
          "witness_key": "entity:method:wadati"
        },
        {
          "row_index": 8,
          "witness_key": "entity:model:1d-velocity"
        },
        {
          "row_index": 9,
          "witness_key": "entity:model:average-velocity"
        },
        {
          "row_index": 10,
          "witness_key": "entity:model:co2-solubility"
        },
        {
          "row_index": 11,
          "witness_key": "entity:model:fastest"
        },
        {
          "row_index": 12,
          "witness_key": "entity:model:five-velocity"
        },
        {
          "row_index": 13,
          "witness_key": "entity:model:iacono-marziano"
        },
        {
          "row_index": 14,
          "witness_key": "entity:model:minimum-velocity"
        },
        {
          "row_index": 15,
          "witness_key": "entity:model:thermal"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 48,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 49,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 50,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 51,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 52,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 53,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 54,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 55,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 56,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 57,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 58,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 59,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 60,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 61,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 62,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 63,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 64,
          "witness_key": "entity:melt:ascending"
        },
        {
          "row_index": 65,
          "witness_key": "entity:melt:pre-eruptive"
        },
        {
          "row_index": 66,
          "witness_key": "entity:melt:primary"
        },
        {
          "row_index": 67,
          "witness_key": "entity:melt:primitive"
        },
        {
          "row_index": 68,
          "witness_key": "entity:ratio:co2-ba"
        },
        {
          "row_index": 69,
          "witness_key": "entity:ratio:co2-rb"
        },
        {
          "row_index": 70,
          "witness_key": "entity:ratio:vpvs"
        },
        {
          "row_index": 71,
          "witness_key": "entity:anhydrous-peridotite"
        },
        {
          "row_index": 72,
          "witness_key": "entity:basaltic-rocks"
        },
        {
          "row_index": 73,
          "witness_key": "entity:basalts-seafloor"
        },
        {
          "row_index": 74,
          "witness_key": "entity:mantle-peridotites"
        },
        {
          "row_index": 75,
          "witness_key": "entity:melt-inclusions"
        },
        {
          "row_index": 76,
          "witness_key": "entity:morb-samples"
        },
        {
          "row_index": 77,
          "witness_key": "entity:peridotite-seafloor"
        },
        {
          "row_index": 78,
          "witness_key": "entity:pillow-basalts"
        },
        {
          "row_index": 79,
          "witness_key": "entity:popping-rocks"
        }
      ]
    },
    {
      "question_id": "CQ-T4-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names the same row, so one returned row carries the whole answer including the direction of the assertion.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "existence_claim",
          "row_index": 29,
          "absent_reason": null,
          "note": "One row carries the statement about active hydrothermal venting."
        },
        {
          "semantic": "negated_disposition",
          "row_index": 29,
          "absent_reason": null,
          "note": "Its modality marks the statement as a negation, an assertion of absence."
        },
        {
          "semantic": "claim_subject",
          "row_index": 29,
          "absent_reason": null,
          "note": "The claim's name identifies active hydrothermal vents as the subject."
        },
        {
          "semantic": "spatial_scope",
          "row_index": 29,
          "absent_reason": null,
          "note": "The same name carries the scope, the axis of the deep-earthquake segment."
        }
      ],
      "source_locators": [
        "page:3:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:askja"
        },
        {
          "row_index": 49,
          "witness_key": "entity:axial-valley-rc1"
        },
        {
          "row_index": 50,
          "witness_key": "entity:chain-tf"
        },
        {
          "row_index": 51,
          "witness_key": "entity:detachment-rc1"
        },
        {
          "row_index": 52,
          "witness_key": "entity:fagradalsfjall"
        },
        {
          "row_index": 53,
          "witness_key": "entity:hydrothermal-mound"
        },
        {
          "row_index": 54,
          "witness_key": "entity:logachev"
        },
        {
          "row_index": 55,
          "witness_key": "entity:main-axial-faults"
        },
        {
          "row_index": 56,
          "witness_key": "entity:mayotte"
        },
        {
          "row_index": 57,
          "witness_key": "entity:mylonite-shear-zones"
        },
        {
          "row_index": 58,
          "witness_key": "entity:ntd1-faults"
        },
        {
          "row_index": 59,
          "witness_key": "entity:ntd1-vent-field"
        },
        {
          "row_index": 60,
          "witness_key": "entity:ntd2-faults"
        },
        {
          "row_index": 61,
          "witness_key": "entity:occ"
        },
        {
          "row_index": 62,
          "witness_key": "entity:occ-corrugated"
        },
        {
          "row_index": 63,
          "witness_key": "entity:occ-dome-faults"
        },
        {
          "row_index": 64,
          "witness_key": "entity:occ-normal-faults"
        },
        {
          "row_index": 65,
          "witness_key": "entity:occ-termination"
        },
        {
          "row_index": 66,
          "witness_key": "entity:rainbow"
        },
        {
          "row_index": 67,
          "witness_key": "entity:rc2-axial-faults"
        },
        {
          "row_index": 68,
          "witness_key": "entity:rc2-bounding-faults"
        },
        {
          "row_index": 69,
          "witness_key": "entity:rc2-hummocky"
        },
        {
          "row_index": 70,
          "witness_key": "entity:rc2-median-valley"
        },
        {
          "row_index": 71,
          "witness_key": "entity:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 72,
          "witness_key": "entity:rc2-volcanic-cones"
        },
        {
          "row_index": 73,
          "witness_key": "entity:romanche-tf"
        },
        {
          "row_index": 74,
          "witness_key": "entity:transform-valley"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 158,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 159,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 160,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 161,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 162,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 163,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 164,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 165,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 166,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 167,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 168,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 169,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 170,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 171,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 172,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 173,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 174,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 175,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 176,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 177,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 178,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 179,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 180,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 181,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 182,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 183,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 184,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 185,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 186,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 187,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 188,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 189,
          "witness_key": "relation:occ:cut-by:faults"
        },
        {
          "row_index": 190,
          "witness_key": "relation:logachev:part-of:knipovich"
        },
        {
          "row_index": 191,
          "witness_key": "relation:occ:beneath:mar"
        },
        {
          "row_index": 192,
          "witness_key": "relation:rc1:bounded-by:detachment"
        },
        {
          "row_index": 193,
          "witness_key": "relation:rc2:bounded-by:faults"
        },
        {
          "row_index": 194,
          "witness_key": "relation:rc3:adjacent:rc2"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:tf-coverage"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 212,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 213,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 214,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 215,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 216,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 217,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 218,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 219,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 220,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 221,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 222,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 223,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 224,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 225,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 226,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 227,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 228,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 229,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 230,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 231,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 232,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 233,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 234,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 235,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 236,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 237,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 238,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 239,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 240,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 241,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 242,
          "witness_key": "entity:q:swir-bdb-depth"
        }
      ]
    },
    {
      "question_id": "CQ-T4-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names a row. The qualification and the limitation come from the same block but are two rows, and nothing in the result joins them.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "hedged_claim",
          "row_index": 17,
          "absent_reason": null,
          "note": "One row carries the suggestion that some events may be long-period."
        },
        {
          "semantic": "hypothesised_disposition",
          "row_index": 17,
          "absent_reason": null,
          "note": "Its disposition is undecided, derived from the block that says not all events show the characteristic."
        },
        {
          "semantic": "epistemic_modality",
          "row_index": 17,
          "absent_reason": null,
          "note": "Its modality marks the claim as hypothesised."
        },
        {
          "semantic": "stated_limitation",
          "row_index": 28,
          "absent_reason": null,
          "note": "A second row carries what is still needed, more earthquakes to study the sources."
        }
      ],
      "source_locators": [
        "page:5:block:008"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "event:romanche-2016"
        }
      ]
    },
    {
      "question_id": "CQ-T5-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Four of five are reached across four rows. What is missing is the join: the graph carries the mechanism and both observations but nothing that says one supports the other, so bringing them together is left to the reader.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "causal_mechanism",
          "row_index": 2,
          "absent_reason": null,
          "note": "One row carries the degassing mechanism."
        },
        {
          "semantic": "supporting_observation",
          "row_index": 148,
          "absent_reason": null,
          "note": "A quantity row carries the reported carbon dioxide content of the primary melts."
        },
        {
          "semantic": "geochemical_evidence",
          "row_index": 113,
          "absent_reason": null,
          "note": "A second quantity row carries the calculated content for the segment where the deep events lie."
        },
        {
          "semantic": "seismic_evidence",
          "row_index": 155,
          "absent_reason": null,
          "note": "A third quantity row carries the observed depth of those earthquakes."
        },
        {
          "semantic": "evidence_relation",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "No returned row links any of the observations to the mechanism. The evidential step is inside the sentences the claim and the quantities are bound to, and the graph holds those only as locators and digests."
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002",
        "page:5:block:005",
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 49,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 50,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 51,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 158,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 159,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 160,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 161,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 162,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 163,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 164,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 165,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 166,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 167,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 168,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 169,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 170,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 171,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 172,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 173,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 174,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 175,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 176,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 177,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 178,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 179,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T5-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Four of five are reached and a returned adjacency relation joins the two segments, so the rows do assemble. The comparison itself, which is what the question asks for, is not modelled: both figures are present and nothing in the result says how they stand to each other.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "comparison_relation",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "The sentence both calculations come from states the enrichment of one segment against the other. Neither quantity row carries a comparison field and no comparison record was derived, so the comparison stays inside the withheld statement."
        },
        {
          "semantic": "first_quantity_subject",
          "row_index": 200,
          "absent_reason": null,
          "note": "A subject row ties the first primary-melt figure to the segment with the deep earthquakes."
        },
        {
          "semantic": "second_quantity_subject",
          "row_index": 207,
          "absent_reason": null,
          "note": "A second subject row ties the other figure to the segment to the south."
        },
        {
          "semantic": "bounded_quantity",
          "row_index": 200,
          "absent_reason": null,
          "note": "The first row carries the bounded range."
        },
        {
          "semantic": "concentration_unit",
          "row_index": 200,
          "absent_reason": null,
          "note": "The same row carries the unit."
        }
      ],
      "source_locators": [
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:melt:ascending"
        },
        {
          "row_index": 49,
          "witness_key": "entity:melt:pre-eruptive"
        },
        {
          "row_index": 50,
          "witness_key": "entity:melt:primary"
        },
        {
          "row_index": 51,
          "witness_key": "entity:melt:primitive"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 152,
          "witness_key": "entity:ratio:co2-ba"
        },
        {
          "row_index": 153,
          "witness_key": "entity:ratio:co2-rb"
        },
        {
          "row_index": 154,
          "witness_key": "entity:ratio:vpvs"
        },
        {
          "row_index": 155,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 156,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 157,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 158,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 159,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 160,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 161,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 162,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 163,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 164,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 165,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 166,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 167,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 168,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 169,
          "witness_key": "entity:anhydrous-peridotite"
        },
        {
          "row_index": 170,
          "witness_key": "entity:basaltic-rocks"
        },
        {
          "row_index": 171,
          "witness_key": "entity:basalts-seafloor"
        },
        {
          "row_index": 172,
          "witness_key": "entity:mantle-peridotites"
        },
        {
          "row_index": 173,
          "witness_key": "entity:melt-inclusions"
        },
        {
          "row_index": 174,
          "witness_key": "entity:morb-samples"
        },
        {
          "row_index": 175,
          "witness_key": "entity:peridotite-seafloor"
        },
        {
          "row_index": 176,
          "witness_key": "entity:pillow-basalts"
        },
        {
          "row_index": 177,
          "witness_key": "entity:popping-rocks"
        },
        {
          "row_index": 178,
          "witness_key": "relation:rc3:adjacent:rc2"
        },
        {
          "row_index": 179,
          "witness_key": "relation:morb:sampled-from:rc2"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 212,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 213,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 214,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 215,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 216,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 217,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 218,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 219,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 220,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 221,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 222,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 223,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 224,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 225,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 226,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 227,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T5-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names a row, but they are four separate rows and nothing in the result joins them; which subsections fall inside the expectation has to be assembled from the individual depth rows by the reader.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "subsection_set",
          "row_index": 134,
          "absent_reason": null,
          "note": "One row carries the number of subsections and states what they are subsections of."
        },
        {
          "semantic": "maximum_depth_claim",
          "row_index": 165,
          "absent_reason": null,
          "note": "A second row carries the observed depth of the deepest events, the one that exceeds the expectation."
        },
        {
          "semantic": "expected_depth_claim",
          "row_index": 129,
          "absent_reason": null,
          "note": "A third row carries the depth expected beneath slow-spreading ridges, with its modelled determination."
        },
        {
          "semantic": "comparison_relation",
          "row_index": 7,
          "absent_reason": null,
          "note": "A claim row states that the maximum depth here does not follow the usual relation to spreading rate."
        }
      ],
      "source_locators": [
        "page:1:block:005",
        "page:2:block:006",
        "page:1:block:004",
        "page:2:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 49,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 50,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 51,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 148,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 149,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 150,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 151,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 152,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 153,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 154,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 155,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 156,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 157,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 158,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 159,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 160,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 161,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 162,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 163,
          "witness_key": "relation:rc3:adjacent:rc2"
        },
        {
          "row_index": 164,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 165,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 166,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 167,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 168,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 169,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 170,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 171,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 172,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 173,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 174,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 175,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 176,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 177,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 178,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 179,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T5-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names a row. The catalogue is reached only as the count of located earthquakes because this question's case set carries no data-resource type, and nothing in the result joins the three rows.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "category_set",
          "row_index": 71,
          "absent_reason": null,
          "note": "One row states the categories the locations were classified into."
        },
        {
          "semantic": "category_count",
          "row_index": 71,
          "absent_reason": null,
          "note": "The same row carries the count."
        },
        {
          "semantic": "selection_for_interpretation",
          "row_index": 52,
          "absent_reason": null,
          "note": "A claim row states which two categories are treated as good quality and used for interpretation."
        },
        {
          "semantic": "earthquake_catalog",
          "row_index": 109,
          "absent_reason": null,
          "note": "A quantity row carries the located earthquakes the classification applies to; the catalogue's own data-resource record is outside this question's case set, so the catalogue is reached as a count rather than as a record."
        }
      ],
      "source_locators": [
        "page:2:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:method:double-difference"
        },
        {
          "row_index": 1,
          "witness_key": "entity:method:focal-criterion"
        },
        {
          "row_index": 2,
          "witness_key": "entity:method:local-magnitude"
        },
        {
          "row_index": 3,
          "witness_key": "entity:method:location-criteria"
        },
        {
          "row_index": 4,
          "witness_key": "entity:method:nonlinear-location"
        },
        {
          "row_index": 5,
          "witness_key": "entity:method:octtree"
        },
        {
          "row_index": 6,
          "witness_key": "entity:method:stalta"
        },
        {
          "row_index": 7,
          "witness_key": "entity:method:wadati"
        },
        {
          "row_index": 8,
          "witness_key": "entity:model:1d-velocity"
        },
        {
          "row_index": 9,
          "witness_key": "entity:model:average-velocity"
        },
        {
          "row_index": 10,
          "witness_key": "entity:model:co2-solubility"
        },
        {
          "row_index": 11,
          "witness_key": "entity:model:fastest"
        },
        {
          "row_index": 12,
          "witness_key": "entity:model:five-velocity"
        },
        {
          "row_index": 13,
          "witness_key": "entity:model:iacono-marziano"
        },
        {
          "row_index": 14,
          "witness_key": "entity:model:minimum-velocity"
        },
        {
          "row_index": 15,
          "witness_key": "entity:model:thermal"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 48,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 49,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 50,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 51,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 52,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 53,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 54,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 55,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 56,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 57,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 58,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 59,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 60,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 61,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 62,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 63,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 158,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 159,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 160,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 161,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 162,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 163,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 164,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 165,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 166,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 167,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 168,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 169,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 170,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 171,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 172,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 173,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 174,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 175,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 176,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 177,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 178,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 179,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-T5-05",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Four of five are reached. The observations and the rejected explanation are all present as rows and no returned row says that the first two are read together against the third, so the argument itself is not in the result.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "candidate_explanation",
          "row_index": 3,
          "absent_reason": null,
          "note": "One row carries the cold and thick lithosphere explanation."
        },
        {
          "semantic": "morphological_observation",
          "row_index": 38,
          "absent_reason": null,
          "note": "A claim row carries the axial morphology reading, that the segment is of magmatic origin."
        },
        {
          "semantic": "seismic_observation",
          "row_index": 212,
          "absent_reason": null,
          "note": "A quantity row carries the off-axis shallow seismicity west of the segment axis."
        },
        {
          "semantic": "evidence_relation",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "Nothing in the result ties either observation to the explanation being argued against. Both blocks carry the argument in their sentences and the graph holds those as locators and digests only."
        },
        {
          "semantic": "declined_disposition",
          "row_index": 3,
          "absent_reason": null,
          "note": "The explanation row's disposition marks it as not supported."
        }
      ],
      "source_locators": [
        "page:3:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:askja"
        },
        {
          "row_index": 49,
          "witness_key": "entity:axial-valley-rc1"
        },
        {
          "row_index": 50,
          "witness_key": "entity:chain-tf"
        },
        {
          "row_index": 51,
          "witness_key": "entity:detachment-rc1"
        },
        {
          "row_index": 52,
          "witness_key": "entity:fagradalsfjall"
        },
        {
          "row_index": 53,
          "witness_key": "entity:hydrothermal-mound"
        },
        {
          "row_index": 54,
          "witness_key": "entity:logachev"
        },
        {
          "row_index": 55,
          "witness_key": "entity:main-axial-faults"
        },
        {
          "row_index": 56,
          "witness_key": "entity:mayotte"
        },
        {
          "row_index": 57,
          "witness_key": "entity:mylonite-shear-zones"
        },
        {
          "row_index": 58,
          "witness_key": "entity:ntd1-faults"
        },
        {
          "row_index": 59,
          "witness_key": "entity:ntd1-vent-field"
        },
        {
          "row_index": 60,
          "witness_key": "entity:ntd2-faults"
        },
        {
          "row_index": 61,
          "witness_key": "entity:occ"
        },
        {
          "row_index": 62,
          "witness_key": "entity:occ-corrugated"
        },
        {
          "row_index": 63,
          "witness_key": "entity:occ-dome-faults"
        },
        {
          "row_index": 64,
          "witness_key": "entity:occ-normal-faults"
        },
        {
          "row_index": 65,
          "witness_key": "entity:occ-termination"
        },
        {
          "row_index": 66,
          "witness_key": "entity:rainbow"
        },
        {
          "row_index": 67,
          "witness_key": "entity:rc2-axial-faults"
        },
        {
          "row_index": 68,
          "witness_key": "entity:rc2-bounding-faults"
        },
        {
          "row_index": 69,
          "witness_key": "entity:rc2-hummocky"
        },
        {
          "row_index": 70,
          "witness_key": "entity:rc2-median-valley"
        },
        {
          "row_index": 71,
          "witness_key": "entity:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 72,
          "witness_key": "entity:rc2-volcanic-cones"
        },
        {
          "row_index": 73,
          "witness_key": "entity:romanche-tf"
        },
        {
          "row_index": 74,
          "witness_key": "entity:transform-valley"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 158,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 159,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 160,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 161,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 162,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 163,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 164,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 165,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 166,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 167,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 168,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 169,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 170,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 171,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 172,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 173,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 174,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 175,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 176,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 177,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 178,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 179,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 180,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 181,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 182,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 183,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 184,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 185,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 186,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 187,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 188,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 189,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 190,
          "witness_key": "relation:occ:cut-by:faults"
        },
        {
          "row_index": 191,
          "witness_key": "relation:logachev:part-of:knipovich"
        },
        {
          "row_index": 192,
          "witness_key": "relation:occ:beneath:mar"
        },
        {
          "row_index": 193,
          "witness_key": "relation:rc1:bounded-by:detachment"
        },
        {
          "row_index": 194,
          "witness_key": "relation:rc2:bounded-by:faults"
        },
        {
          "row_index": 195,
          "witness_key": "relation:rc3:adjacent:rc2"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:tf-coverage"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 212,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 213,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 214,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 215,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 216,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 217,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 218,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 219,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 220,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 221,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 222,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 223,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 224,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 225,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 226,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 227,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 228,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 229,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 230,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 231,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 232,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 233,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 234,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 235,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 236,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 237,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 238,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 239,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 240,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 241,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 242,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 243,
          "witness_key": "entity:q:swir-bdb-depth"
        }
      ]
    },
    {
      "question_id": "CQ-C-01",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "None of the four is reached. The reading reports carbon dioxide and water and states no sulfur or chlorine data at any point, so no row carries the quantity, its unit, the samples it would belong to, or how it was determined.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "No sulfur or chlorine concentration is stated anywhere in the reading; the volatiles it reports are carbon dioxide and water."
        },
        {
          "semantic": "concentration_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "With no such concentration in the reading there is no unit for one."
        },
        {
          "semantic": "sample_set",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading does carry the basalt sample set used for the volatile estimation, but it is the sample set of the carbon dioxide work; no sulfur or chlorine measurement exists for a sample set to belong to."
        },
        {
          "semantic": "measurement_status",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "There is no such measurement in the reading, so nothing states how it was obtained."
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:melt:ascending"
        },
        {
          "row_index": 49,
          "witness_key": "entity:melt:pre-eruptive"
        },
        {
          "row_index": 50,
          "witness_key": "entity:melt:primary"
        },
        {
          "row_index": 51,
          "witness_key": "entity:melt:primitive"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 152,
          "witness_key": "entity:ratio:co2-ba"
        },
        {
          "row_index": 153,
          "witness_key": "entity:ratio:co2-rb"
        },
        {
          "row_index": 154,
          "witness_key": "entity:ratio:vpvs"
        },
        {
          "row_index": 155,
          "witness_key": "entity:anhydrous-peridotite"
        },
        {
          "row_index": 156,
          "witness_key": "entity:basaltic-rocks"
        },
        {
          "row_index": 157,
          "witness_key": "entity:basalts-seafloor"
        },
        {
          "row_index": 158,
          "witness_key": "entity:mantle-peridotites"
        },
        {
          "row_index": 159,
          "witness_key": "entity:melt-inclusions"
        },
        {
          "row_index": 160,
          "witness_key": "entity:morb-samples"
        },
        {
          "row_index": 161,
          "witness_key": "entity:peridotite-seafloor"
        },
        {
          "row_index": 162,
          "witness_key": "entity:pillow-basalts"
        },
        {
          "row_index": 163,
          "witness_key": "entity:popping-rocks"
        },
        {
          "row_index": 164,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 165,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 166,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 167,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 168,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 169,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 170,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 171,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 172,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 173,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 174,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 175,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 176,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 177,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 178,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 179,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-C-02",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "None of the four is reached. The reading describes the record as a brief snapshot and gives magnitude statistics, and it states no repeat time for the deep events, so nothing in the result answers the question.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "temporal_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "No repeat time or recurrence interval for the deep earthquakes is stated in the reading; the time quantities it carries are the recording span and geological ages."
        },
        {
          "semantic": "time_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "With no recurrence interval stated there is no unit for one."
        },
        {
          "semantic": "event_population",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The deep events are described and counted, but no population is defined as the one a recurrence interval would describe, because no such interval is given."
        },
        {
          "semantic": "measurement_status",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "Nothing states how a recurrence interval was obtained, because none is reported."
        }
      ],
      "source_locators": [
        "page:2:block:004",
        "page:8:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 49,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 50,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 51,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 148,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 158,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 159,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 160,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 161,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 162,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 163,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 164,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 165,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 166,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 167,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 168,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 169,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 170,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 171,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 172,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 173,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 174,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 175,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 176,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 177,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 178,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 179,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-C-03",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "None of the three is reached. The per-site depths and rates exist only in the figure and its supplementary table, surfaces this question file's scope excludes, and although the reading names several of the sites in a methods sentence about updating their data, no record carries the compiled set as such.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "site_set",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "Individual comparison sites are named in the reading and several are returned as their own rows, but no record carries the set of sites compiled for the comparison, and no row says which sites the plot contains."
        },
        {
          "semantic": "maximum_depth_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading states no maximum earthquake depth for any of the other sites; those values live in the comparison figure and its supplementary table, which the question file's scope excludes."
        },
        {
          "semantic": "spreading_rate_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The only spreading rates in the reading are those of the study area itself; no rate is stated for any compiled site, for the same reason."
        }
      ],
      "source_locators": [
        "page:8:block:004",
        "page:5:block:010"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 49,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 50,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 51,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 148,
          "witness_key": "entity:ref:r1"
        },
        {
          "row_index": 149,
          "witness_key": "entity:ref:r10"
        },
        {
          "row_index": 150,
          "witness_key": "entity:ref:r11"
        },
        {
          "row_index": 151,
          "witness_key": "entity:ref:r12"
        },
        {
          "row_index": 152,
          "witness_key": "entity:ref:r13"
        },
        {
          "row_index": 153,
          "witness_key": "entity:ref:r14"
        },
        {
          "row_index": 154,
          "witness_key": "entity:ref:r15"
        },
        {
          "row_index": 155,
          "witness_key": "entity:ref:r16"
        },
        {
          "row_index": 156,
          "witness_key": "entity:ref:r17"
        },
        {
          "row_index": 157,
          "witness_key": "entity:ref:r18"
        },
        {
          "row_index": 158,
          "witness_key": "entity:ref:r19"
        },
        {
          "row_index": 159,
          "witness_key": "entity:ref:r2"
        },
        {
          "row_index": 160,
          "witness_key": "entity:ref:r20"
        },
        {
          "row_index": 161,
          "witness_key": "entity:ref:r21"
        },
        {
          "row_index": 162,
          "witness_key": "entity:ref:r22"
        },
        {
          "row_index": 163,
          "witness_key": "entity:ref:r23"
        },
        {
          "row_index": 164,
          "witness_key": "entity:ref:r24"
        },
        {
          "row_index": 165,
          "witness_key": "entity:ref:r25"
        },
        {
          "row_index": 166,
          "witness_key": "entity:ref:r26"
        },
        {
          "row_index": 167,
          "witness_key": "entity:ref:r27"
        },
        {
          "row_index": 168,
          "witness_key": "entity:ref:r28"
        },
        {
          "row_index": 169,
          "witness_key": "entity:ref:r29"
        },
        {
          "row_index": 170,
          "witness_key": "entity:ref:r3"
        },
        {
          "row_index": 171,
          "witness_key": "entity:ref:r30"
        },
        {
          "row_index": 172,
          "witness_key": "entity:ref:r31"
        },
        {
          "row_index": 173,
          "witness_key": "entity:ref:r32"
        },
        {
          "row_index": 174,
          "witness_key": "entity:ref:r33"
        },
        {
          "row_index": 175,
          "witness_key": "entity:ref:r34"
        },
        {
          "row_index": 176,
          "witness_key": "entity:ref:r35"
        },
        {
          "row_index": 177,
          "witness_key": "entity:ref:r36"
        },
        {
          "row_index": 178,
          "witness_key": "entity:ref:r37"
        },
        {
          "row_index": 179,
          "witness_key": "entity:ref:r38"
        },
        {
          "row_index": 180,
          "witness_key": "entity:ref:r39"
        },
        {
          "row_index": 181,
          "witness_key": "entity:ref:r4"
        },
        {
          "row_index": 182,
          "witness_key": "entity:ref:r40"
        },
        {
          "row_index": 183,
          "witness_key": "entity:ref:r41"
        },
        {
          "row_index": 184,
          "witness_key": "entity:ref:r42"
        },
        {
          "row_index": 185,
          "witness_key": "entity:ref:r43"
        },
        {
          "row_index": 186,
          "witness_key": "entity:ref:r44"
        },
        {
          "row_index": 187,
          "witness_key": "entity:ref:r45"
        },
        {
          "row_index": 188,
          "witness_key": "entity:ref:r46"
        },
        {
          "row_index": 189,
          "witness_key": "entity:ref:r47"
        },
        {
          "row_index": 190,
          "witness_key": "entity:ref:r48"
        },
        {
          "row_index": 191,
          "witness_key": "entity:ref:r49"
        },
        {
          "row_index": 192,
          "witness_key": "entity:ref:r5"
        },
        {
          "row_index": 193,
          "witness_key": "entity:ref:r50"
        },
        {
          "row_index": 194,
          "witness_key": "entity:ref:r51"
        },
        {
          "row_index": 195,
          "witness_key": "entity:ref:r52"
        },
        {
          "row_index": 196,
          "witness_key": "entity:ref:r53"
        },
        {
          "row_index": 197,
          "witness_key": "entity:ref:r54"
        },
        {
          "row_index": 198,
          "witness_key": "entity:ref:r55"
        },
        {
          "row_index": 199,
          "witness_key": "entity:ref:r56"
        },
        {
          "row_index": 200,
          "witness_key": "entity:ref:r57"
        },
        {
          "row_index": 201,
          "witness_key": "entity:ref:r58"
        },
        {
          "row_index": 202,
          "witness_key": "entity:ref:r59"
        },
        {
          "row_index": 203,
          "witness_key": "entity:ref:r6"
        },
        {
          "row_index": 204,
          "witness_key": "entity:ref:r60"
        },
        {
          "row_index": 205,
          "witness_key": "entity:ref:r61"
        },
        {
          "row_index": 206,
          "witness_key": "entity:ref:r62"
        },
        {
          "row_index": 207,
          "witness_key": "entity:ref:r63"
        },
        {
          "row_index": 208,
          "witness_key": "entity:ref:r64"
        },
        {
          "row_index": 209,
          "witness_key": "entity:ref:r65"
        },
        {
          "row_index": 210,
          "witness_key": "entity:ref:r66"
        },
        {
          "row_index": 211,
          "witness_key": "entity:ref:r67"
        },
        {
          "row_index": 212,
          "witness_key": "entity:ref:r68"
        },
        {
          "row_index": 213,
          "witness_key": "entity:ref:r69"
        },
        {
          "row_index": 214,
          "witness_key": "entity:ref:r7"
        },
        {
          "row_index": 215,
          "witness_key": "entity:ref:r70"
        },
        {
          "row_index": 216,
          "witness_key": "entity:ref:r71"
        },
        {
          "row_index": 217,
          "witness_key": "entity:ref:r72"
        },
        {
          "row_index": 218,
          "witness_key": "entity:ref:r73"
        },
        {
          "row_index": 219,
          "witness_key": "entity:ref:r74"
        },
        {
          "row_index": 220,
          "witness_key": "entity:ref:r75"
        },
        {
          "row_index": 221,
          "witness_key": "entity:ref:r76"
        },
        {
          "row_index": 222,
          "witness_key": "entity:ref:r77"
        },
        {
          "row_index": 223,
          "witness_key": "entity:ref:r78"
        },
        {
          "row_index": 224,
          "witness_key": "entity:ref:r79"
        },
        {
          "row_index": 225,
          "witness_key": "entity:ref:r8"
        },
        {
          "row_index": 226,
          "witness_key": "entity:ref:r9"
        },
        {
          "row_index": 227,
          "witness_key": "entity:work:yu-2025"
        },
        {
          "row_index": 228,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 229,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 230,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 231,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 232,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 233,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 234,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 235,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 236,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 237,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 238,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 239,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 240,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 241,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 242,
          "witness_key": "relation:rc3:adjacent:rc2"
        },
        {
          "row_index": 243,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 244,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 245,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 246,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 247,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 248,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 249,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 250,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 251,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 252,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 253,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 254,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 255,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 256,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 257,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 258,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 259,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 260,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 261,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 262,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 263,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 264,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 265,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 266,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 267,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 268,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 269,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 270,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 271,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 272,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 273,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 274,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 275,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 276,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 277,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 278,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 279,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 280,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 281,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 282,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 283,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 284,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 285,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 286,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 287,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 288,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 289,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 290,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-C-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names a row, and the same two rows carry it as in the question this one rewords. Nothing in the result joins them, because the case set declares no relation type.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "instrument_count",
          "row_index": 0,
          "absent_reason": null,
          "note": "The campaign row carries the count and states what is counted."
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "The instrument row names the instrument type."
        },
        {
          "semantic": "deployment_event",
          "row_index": 0,
          "absent_reason": null,
          "note": "The start date and precision on the same row derive from the methods sentence that states the deployment."
        }
      ],
      "source_locators": [
        "page:10:block:043",
        "page:2:block:002",
        "page:6:block:002",
        "page:1:block:001",
        "page:2:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:campaign:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "entity:obs"
        },
        {
          "row_index": 2,
          "witness_key": "entity:software:global-mapper"
        },
        {
          "row_index": 3,
          "witness_key": "entity:software:gmt"
        },
        {
          "row_index": 4,
          "witness_key": "entity:software:hash"
        },
        {
          "row_index": 5,
          "witness_key": "entity:software:hypodd"
        },
        {
          "row_index": 6,
          "witness_key": "entity:software:nonlinloc"
        },
        {
          "row_index": 7,
          "witness_key": "entity:software:seisan"
        },
        {
          "row_index": 8,
          "witness_key": "entity:software:velest"
        },
        {
          "row_index": 9,
          "witness_key": "entity:software:zmap"
        },
        {
          "row_index": 10,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 11,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 12,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 13,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 14,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 15,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 16,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 17,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 18,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 19,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 20,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 21,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 22,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 23,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 24,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 25,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 26,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 27,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 28,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 29,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 30,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 31,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 32,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 33,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 34,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 35,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 36,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 37,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 38,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 39,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 40,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 41,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 42,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 43,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 44,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 45,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 46,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 47,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 48,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 49,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 50,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 51,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 152,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 153,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 154,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 155,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 156,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 157,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
    },
    {
      "question_id": "CQ-C-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required semantic names the same row, the same row that answers the question this one rewords, so one returned row carries the whole answer.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 180,
          "absent_reason": null,
          "note": "One row carries the reported range."
        },
        {
          "semantic": "concentration_unit",
          "row_index": 180,
          "absent_reason": null,
          "note": "The same row carries the unit."
        },
        {
          "semantic": "quantity_subject",
          "row_index": 180,
          "absent_reason": null,
          "note": "Its subject reference points at the primary melts."
        },
        {
          "semantic": "calculated_or_measured_status",
          "row_index": 180,
          "absent_reason": null,
          "note": "The same row's modality and determination mark the figure as calculated."
        }
      ],
      "source_locators": [
        "page:1:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "entity:claim:axis-relocating"
        },
        {
          "row_index": 1,
          "witness_key": "entity:claim:basalts-degassed"
        },
        {
          "row_index": 2,
          "witness_key": "entity:claim:co2-degassing"
        },
        {
          "row_index": 3,
          "witness_key": "entity:claim:cold-thick-lithosphere"
        },
        {
          "row_index": 4,
          "witness_key": "entity:claim:confident-hypocenters"
        },
        {
          "row_index": 5,
          "witness_key": "entity:claim:contexts-differ"
        },
        {
          "row_index": 6,
          "witness_key": "entity:claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "entity:claim:depth-not-following"
        },
        {
          "row_index": 8,
          "witness_key": "entity:claim:detachment-inactive"
        },
        {
          "row_index": 9,
          "witness_key": "entity:claim:enriched-source"
        },
        {
          "row_index": 10,
          "witness_key": "entity:claim:events-well-constrained"
        },
        {
          "row_index": 11,
          "witness_key": "entity:claim:fig6-interpretation"
        },
        {
          "row_index": 12,
          "witness_key": "entity:claim:focal-not-robust"
        },
        {
          "row_index": 13,
          "witness_key": "entity:claim:hydrothermal-cooling"
        },
        {
          "row_index": 14,
          "witness_key": "entity:claim:keller-flushing"
        },
        {
          "row_index": 15,
          "witness_key": "entity:claim:lab-melt"
        },
        {
          "row_index": 16,
          "witness_key": "entity:claim:lab-melt-combination"
        },
        {
          "row_index": 17,
          "witness_key": "entity:claim:long-period"
        },
        {
          "row_index": 18,
          "witness_key": "entity:claim:magmatic-tectonic"
        },
        {
          "row_index": 19,
          "witness_key": "entity:claim:magmatism-dominates"
        },
        {
          "row_index": 20,
          "witness_key": "entity:claim:max-depth-factors"
        },
        {
          "row_index": 21,
          "witness_key": "entity:claim:max-depth-selection"
        },
        {
          "row_index": 22,
          "witness_key": "entity:claim:melt-freeze"
        },
        {
          "row_index": 23,
          "witness_key": "entity:claim:melt-migration-unknown"
        },
        {
          "row_index": 24,
          "witness_key": "entity:claim:melt-movement-rejected"
        },
        {
          "row_index": 25,
          "witness_key": "entity:claim:melt-residence"
        },
        {
          "row_index": 26,
          "witness_key": "entity:claim:model1-inappropriate"
        },
        {
          "row_index": 27,
          "witness_key": "entity:claim:model5-preferred"
        },
        {
          "row_index": 28,
          "witness_key": "entity:claim:more-events-needed"
        },
        {
          "row_index": 29,
          "witness_key": "entity:claim:no-active-vents"
        },
        {
          "row_index": 30,
          "witness_key": "entity:claim:no-competing"
        },
        {
          "row_index": 31,
          "witness_key": "entity:claim:no-detachment-rc2"
        },
        {
          "row_index": 32,
          "witness_key": "entity:claim:no-eruption"
        },
        {
          "row_index": 33,
          "witness_key": "entity:claim:not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "entity:claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "entity:claim:primary-vs-preeruptive"
        },
        {
          "row_index": 36,
          "witness_key": "entity:claim:quality-ab"
        },
        {
          "row_index": 37,
          "witness_key": "entity:claim:ratio-proxy"
        },
        {
          "row_index": 38,
          "witness_key": "entity:claim:rc2-magmatic"
        },
        {
          "row_index": 39,
          "witness_key": "entity:claim:reduced-model-reasonable"
        },
        {
          "row_index": 40,
          "witness_key": "entity:claim:samples-degassed"
        },
        {
          "row_index": 41,
          "witness_key": "entity:claim:shear-zone"
        },
        {
          "row_index": 42,
          "witness_key": "entity:claim:snapshot"
        },
        {
          "row_index": 43,
          "witness_key": "entity:claim:trace-element-assumption"
        },
        {
          "row_index": 44,
          "witness_key": "entity:claim:ultraslow-co2-high"
        },
        {
          "row_index": 45,
          "witness_key": "entity:claim:volatile-role-unknown"
        },
        {
          "row_index": 46,
          "witness_key": "entity:claim:volume-change"
        },
        {
          "row_index": 47,
          "witness_key": "entity:claim:vpvs-reasonable"
        },
        {
          "row_index": 48,
          "witness_key": "entity:melt:ascending"
        },
        {
          "row_index": 49,
          "witness_key": "entity:melt:pre-eruptive"
        },
        {
          "row_index": 50,
          "witness_key": "entity:melt:primary"
        },
        {
          "row_index": 51,
          "witness_key": "entity:melt:primitive"
        },
        {
          "row_index": 52,
          "witness_key": "entity:q:avg-depth-uncertainty"
        },
        {
          "row_index": 53,
          "witness_key": "entity:q:avg-horizontal-uncertainty"
        },
        {
          "row_index": 54,
          "witness_key": "entity:q:axial-depth-range"
        },
        {
          "row_index": 55,
          "witness_key": "entity:q:b-value"
        },
        {
          "row_index": 56,
          "witness_key": "entity:q:b-value-groups"
        },
        {
          "row_index": 57,
          "witness_key": "entity:q:brittle-thickness-expected"
        },
        {
          "row_index": 58,
          "witness_key": "entity:q:catalog-links"
        },
        {
          "row_index": 59,
          "witness_key": "entity:q:categories"
        },
        {
          "row_index": 60,
          "witness_key": "entity:q:cluster-depth"
        },
        {
          "row_index": 61,
          "witness_key": "entity:q:co2-gas-loss"
        },
        {
          "row_index": 62,
          "witness_key": "entity:q:cold-lithosphere-age"
        },
        {
          "row_index": 63,
          "witness_key": "entity:q:criterion-arrivals"
        },
        {
          "row_index": 64,
          "witness_key": "entity:q:criterion-gap"
        },
        {
          "row_index": 65,
          "witness_key": "entity:q:criterion-swave"
        },
        {
          "row_index": 66,
          "witness_key": "entity:q:crustal-age-offaxis"
        },
        {
          "row_index": 67,
          "witness_key": "entity:q:deep-events-threshold"
        },
        {
          "row_index": 68,
          "witness_key": "entity:q:depth-uncertainty-final"
        },
        {
          "row_index": 69,
          "witness_key": "entity:q:dry-melting-onset"
        },
        {
          "row_index": 70,
          "witness_key": "entity:q:equatorial-co2-average"
        },
        {
          "row_index": 71,
          "witness_key": "entity:q:equatorial-co2-max"
        },
        {
          "row_index": 72,
          "witness_key": "entity:q:error-ellipsoid-confidence"
        },
        {
          "row_index": 73,
          "witness_key": "entity:q:expected-max-depth"
        },
        {
          "row_index": 74,
          "witness_key": "entity:q:fig3-deep-shade"
        },
        {
          "row_index": 75,
          "witness_key": "entity:q:fig3-shallow-shade"
        },
        {
          "row_index": 76,
          "witness_key": "entity:q:fig3b-halfwidth"
        },
        {
          "row_index": 77,
          "witness_key": "entity:q:fig4-isotherm"
        },
        {
          "row_index": 78,
          "witness_key": "entity:q:fixed-depth-range"
        },
        {
          "row_index": 79,
          "witness_key": "entity:q:fixed-depth-subset"
        },
        {
          "row_index": 80,
          "witness_key": "entity:q:focal-fault-plane"
        },
        {
          "row_index": 81,
          "witness_key": "entity:q:focal-gap"
        },
        {
          "row_index": 82,
          "witness_key": "entity:q:focal-misfit"
        },
        {
          "row_index": 83,
          "witness_key": "entity:q:focal-new"
        },
        {
          "row_index": 84,
          "witness_key": "entity:q:focal-polarities"
        },
        {
          "row_index": 85,
          "witness_key": "entity:q:focal-probability"
        },
        {
          "row_index": 86,
          "witness_key": "entity:q:focal-station-ratio"
        },
        {
          "row_index": 87,
          "witness_key": "entity:q:focal-total"
        },
        {
          "row_index": 88,
          "witness_key": "entity:q:full-spreading-rate"
        },
        {
          "row_index": 89,
          "witness_key": "entity:q:gap-final"
        },
        {
          "row_index": 90,
          "witness_key": "entity:q:groups"
        },
        {
          "row_index": 91,
          "witness_key": "entity:q:horizontal-uncertainty-final"
        },
        {
          "row_index": 92,
          "witness_key": "entity:q:hypodd-iterations"
        },
        {
          "row_index": 93,
          "witness_key": "entity:q:iceland-depths"
        },
        {
          "row_index": 94,
          "witness_key": "entity:q:identified-760"
        },
        {
          "row_index": 95,
          "witness_key": "entity:q:instrument-spacing"
        },
        {
          "row_index": 96,
          "witness_key": "entity:q:lithospheric-age-interval"
        },
        {
          "row_index": 97,
          "witness_key": "entity:q:located-514"
        },
        {
          "row_index": 98,
          "witness_key": "entity:q:located-514-methods"
        },
        {
          "row_index": 99,
          "witness_key": "entity:q:low-frequency-threshold"
        },
        {
          "row_index": 100,
          "witness_key": "entity:q:magnitude-completeness"
        },
        {
          "row_index": 101,
          "witness_key": "entity:q:mar-317"
        },
        {
          "row_index": 102,
          "witness_key": "entity:q:mar-events"
        },
        {
          "row_index": 103,
          "witness_key": "entity:q:max-separation"
        },
        {
          "row_index": 104,
          "witness_key": "entity:q:mayotte-depths"
        },
        {
          "row_index": 105,
          "witness_key": "entity:q:mean-horizontal-error"
        },
        {
          "row_index": 106,
          "witness_key": "entity:q:mean-vertical-error"
        },
        {
          "row_index": 107,
          "witness_key": "entity:q:microseismicity-residence"
        },
        {
          "row_index": 108,
          "witness_key": "entity:q:min-obs-detect"
        },
        {
          "row_index": 109,
          "witness_key": "entity:q:model1-depth"
        },
        {
          "row_index": 110,
          "witness_key": "entity:q:model1-velocity"
        },
        {
          "row_index": 111,
          "witness_key": "entity:q:obs-spacing-focal"
        },
        {
          "row_index": 112,
          "witness_key": "entity:q:offaxis-swarm-depth"
        },
        {
          "row_index": 113,
          "witness_key": "entity:q:pore-pressure-trigger"
        },
        {
          "row_index": 114,
          "witness_key": "entity:q:profile-halfwidth"
        },
        {
          "row_index": 115,
          "witness_key": "entity:q:profile-interval"
        },
        {
          "row_index": 116,
          "witness_key": "entity:q:quality-d-uncertainty"
        },
        {
          "row_index": 117,
          "witness_key": "entity:q:rc2-co2-calculated"
        },
        {
          "row_index": 118,
          "witness_key": "entity:q:rc2-pre-eruptive-co2"
        },
        {
          "row_index": 119,
          "witness_key": "entity:q:rc2-valley-width-2"
        },
        {
          "row_index": 120,
          "witness_key": "entity:q:rc3-co2-calculated"
        },
        {
          "row_index": 121,
          "witness_key": "entity:q:recording-duration"
        },
        {
          "row_index": 122,
          "witness_key": "entity:q:relocated-276"
        },
        {
          "row_index": 123,
          "witness_key": "entity:q:relocated-364"
        },
        {
          "row_index": 124,
          "witness_key": "entity:q:relocation-gap"
        },
        {
          "row_index": 125,
          "witness_key": "entity:q:relocation-rms"
        },
        {
          "row_index": 126,
          "witness_key": "entity:q:relocation-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "entity:q:rms-final"
        },
        {
          "row_index": 128,
          "witness_key": "entity:q:romanche-events"
        },
        {
          "row_index": 129,
          "witness_key": "entity:q:saturating-melt-co2"
        },
        {
          "row_index": 130,
          "witness_key": "entity:q:saturation-depth"
        },
        {
          "row_index": 131,
          "witness_key": "entity:q:saturation-pressure"
        },
        {
          "row_index": 132,
          "witness_key": "entity:q:saturation-temp"
        },
        {
          "row_index": 133,
          "witness_key": "entity:q:slow-expected-depth"
        },
        {
          "row_index": 134,
          "witness_key": "entity:q:solubility-temp"
        },
        {
          "row_index": 135,
          "witness_key": "entity:q:studied-portion-length"
        },
        {
          "row_index": 136,
          "witness_key": "entity:q:subdataset"
        },
        {
          "row_index": 137,
          "witness_key": "entity:q:subevents"
        },
        {
          "row_index": 138,
          "witness_key": "entity:q:subsection-length"
        },
        {
          "row_index": 139,
          "witness_key": "entity:q:temp-below-20"
        },
        {
          "row_index": 140,
          "witness_key": "entity:q:tf-197"
        },
        {
          "row_index": 141,
          "witness_key": "entity:q:thermal-model-temp"
        },
        {
          "row_index": 142,
          "witness_key": "entity:q:two-criteria-share"
        },
        {
          "row_index": 143,
          "witness_key": "entity:q:ultraslow-expected-depth"
        },
        {
          "row_index": 144,
          "witness_key": "entity:q:updated-uncertainty"
        },
        {
          "row_index": 145,
          "witness_key": "entity:q:useful-obs"
        },
        {
          "row_index": 146,
          "witness_key": "entity:q:velest-iterations"
        },
        {
          "row_index": 147,
          "witness_key": "entity:q:velocity-constraint-depth"
        },
        {
          "row_index": 148,
          "witness_key": "entity:q:velocity-perturbation"
        },
        {
          "row_index": 149,
          "witness_key": "entity:q:volatile-melting-onset"
        },
        {
          "row_index": 150,
          "witness_key": "entity:q:vpvs-range"
        },
        {
          "row_index": 151,
          "witness_key": "entity:q:young-crust-age"
        },
        {
          "row_index": 152,
          "witness_key": "entity:ratio:co2-ba"
        },
        {
          "row_index": 153,
          "witness_key": "entity:ratio:co2-rb"
        },
        {
          "row_index": 154,
          "witness_key": "entity:ratio:vpvs"
        },
        {
          "row_index": 155,
          "witness_key": "entity:gakkel"
        },
        {
          "row_index": 156,
          "witness_key": "entity:juan-de-fuca"
        },
        {
          "row_index": 157,
          "witness_key": "entity:knipovich"
        },
        {
          "row_index": 158,
          "witness_key": "entity:mar"
        },
        {
          "row_index": 159,
          "witness_key": "entity:mar-supersegment"
        },
        {
          "row_index": 160,
          "witness_key": "entity:ntd1"
        },
        {
          "row_index": 161,
          "witness_key": "entity:ntd2"
        },
        {
          "row_index": 162,
          "witness_key": "entity:rc1"
        },
        {
          "row_index": 163,
          "witness_key": "entity:rc2"
        },
        {
          "row_index": 164,
          "witness_key": "entity:rc3"
        },
        {
          "row_index": 165,
          "witness_key": "entity:rti"
        },
        {
          "row_index": 166,
          "witness_key": "entity:swir"
        },
        {
          "row_index": 167,
          "witness_key": "entity:swir-oblique"
        },
        {
          "row_index": 168,
          "witness_key": "entity:swir-segment8"
        },
        {
          "row_index": 169,
          "witness_key": "entity:anhydrous-peridotite"
        },
        {
          "row_index": 170,
          "witness_key": "entity:basaltic-rocks"
        },
        {
          "row_index": 171,
          "witness_key": "entity:basalts-seafloor"
        },
        {
          "row_index": 172,
          "witness_key": "entity:mantle-peridotites"
        },
        {
          "row_index": 173,
          "witness_key": "entity:melt-inclusions"
        },
        {
          "row_index": 174,
          "witness_key": "entity:morb-samples"
        },
        {
          "row_index": 175,
          "witness_key": "entity:peridotite-seafloor"
        },
        {
          "row_index": 176,
          "witness_key": "entity:pillow-basalts"
        },
        {
          "row_index": 177,
          "witness_key": "entity:popping-rocks"
        },
        {
          "row_index": 178,
          "witness_key": "relation:rc3:adjacent:rc2"
        },
        {
          "row_index": 179,
          "witness_key": "relation:morb:sampled-from:rc2"
        },
        {
          "row_index": 180,
          "witness_key": "entity:q:abstract-co2"
        },
        {
          "row_index": 181,
          "witness_key": "entity:q:abstract-depth"
        },
        {
          "row_index": 182,
          "witness_key": "entity:q:deep-rc2"
        },
        {
          "row_index": 183,
          "witness_key": "entity:q:deep-rc2-abstract"
        },
        {
          "row_index": 184,
          "witness_key": "entity:q:fig6-crust-thickness"
        },
        {
          "row_index": 185,
          "witness_key": "entity:q:fig6-deep-depth"
        },
        {
          "row_index": 186,
          "witness_key": "entity:q:half-spreading-rate"
        },
        {
          "row_index": 187,
          "witness_key": "entity:q:mar-coverage"
        },
        {
          "row_index": 188,
          "witness_key": "entity:q:no-quakes-below-20"
        },
        {
          "row_index": 189,
          "witness_key": "entity:q:ntd1-length"
        },
        {
          "row_index": 190,
          "witness_key": "entity:q:ntd2-deeper"
        },
        {
          "row_index": 191,
          "witness_key": "entity:q:ntd2-depth"
        },
        {
          "row_index": 192,
          "witness_key": "entity:q:ntd2-normal-depth"
        },
        {
          "row_index": 193,
          "witness_key": "entity:q:ntd2-offset"
        },
        {
          "row_index": 194,
          "witness_key": "entity:q:offaxis-shallow"
        },
        {
          "row_index": 195,
          "witness_key": "entity:q:rc2-alignment"
        },
        {
          "row_index": 196,
          "witness_key": "entity:q:rc2-ba"
        },
        {
          "row_index": 197,
          "witness_key": "entity:q:rc2-co2-ba"
        },
        {
          "row_index": 198,
          "witness_key": "entity:q:rc2-co2-rb"
        },
        {
          "row_index": 199,
          "witness_key": "entity:q:rc2-length"
        },
        {
          "row_index": 200,
          "witness_key": "entity:q:rc2-primary-ba90"
        },
        {
          "row_index": 201,
          "witness_key": "entity:q:rc2-primary-floor"
        },
        {
          "row_index": 202,
          "witness_key": "entity:q:rc2-primary-rb90"
        },
        {
          "row_index": 203,
          "witness_key": "entity:q:rc2-rb"
        },
        {
          "row_index": 204,
          "witness_key": "entity:q:rc3-co2-ba"
        },
        {
          "row_index": 205,
          "witness_key": "entity:q:rc3-co2-rb"
        },
        {
          "row_index": 206,
          "witness_key": "entity:q:rc3-length"
        },
        {
          "row_index": 207,
          "witness_key": "entity:q:rc3-primary-ba90"
        },
        {
          "row_index": 208,
          "witness_key": "entity:q:rc3-primary-rb90"
        },
        {
          "row_index": 209,
          "witness_key": "entity:q:shallow-rti"
        },
        {
          "row_index": 210,
          "witness_key": "entity:q:supersegment-length"
        },
        {
          "row_index": 211,
          "witness_key": "entity:q:swir-highest-co2"
        },
        {
          "row_index": 212,
          "witness_key": "entity:q:bdb-isotherm"
        },
        {
          "row_index": 213,
          "witness_key": "entity:q:bdb-shallow-offaxis"
        },
        {
          "row_index": 214,
          "witness_key": "entity:q:brittle-thickness-ntds"
        },
        {
          "row_index": 215,
          "witness_key": "entity:q:cold-isotherm"
        },
        {
          "row_index": 216,
          "witness_key": "entity:q:crust-thickness"
        },
        {
          "row_index": 217,
          "witness_key": "entity:q:degassing-depth-range"
        },
        {
          "row_index": 218,
          "witness_key": "entity:q:fig6-isotherm"
        },
        {
          "row_index": 219,
          "witness_key": "entity:q:hot-mantle-temp"
        },
        {
          "row_index": 220,
          "witness_key": "entity:q:lab-melt-fraction"
        },
        {
          "row_index": 221,
          "witness_key": "entity:q:lab-sub-solidus-temp"
        },
        {
          "row_index": 222,
          "witness_key": "entity:q:lab-water-content"
        },
        {
          "row_index": 223,
          "witness_key": "entity:q:ntd2-bdb"
        },
        {
          "row_index": 224,
          "witness_key": "entity:q:occ-depth"
        },
        {
          "row_index": 225,
          "witness_key": "entity:q:rc2-valley-width"
        },
        {
          "row_index": 226,
          "witness_key": "entity:q:swir-bdb-depth"
        },
        {
          "row_index": 227,
          "witness_key": "entity:q:tf-coverage"
        }
      ]
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

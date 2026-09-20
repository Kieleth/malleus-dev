# Malleus paper v4 source-grounded review record, protocol v3

This is run-22's blank record for its query under harness v4.13, written by
`paper-v4/evaluation-v4/run-22-v413/build_review_inputs.py` from the frozen v3
template. The question ids are this cell's frozen competency question file's,
in that file's order. The row and witness counts are figures of a producer
that has not run and are filled by the same script at freeze; no other
placeholder survives either stage.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

The `questions` block below carries one entry per question of the cell's
competency question file, 30 of them, in that file's order. Write one
`witnesses` entry per distinct witness the query result returns,
457 in all, and reference it from every row that shares it.
Rows: 142 rows for `CQ-T1-01`, 142 for `CQ-T1-02`, 209 for `CQ-T1-03`, 209 for
`CQ-T1-04`, 140 for `CQ-T1-05`, 185 for `CQ-T2-01`, 137 for `CQ-T2-02`, 315
for `CQ-T2-03`, 261 for `CQ-T2-04`, 24 for `CQ-T2-05`, 316 for `CQ-T3-01`,
322 for `CQ-T3-02`, 322 for `CQ-T3-03`, 269 for `CQ-T3-04`, 268 for
`CQ-T3-05`, 124 for `CQ-T4-01`, 124 for `CQ-T4-02`, 129 for `CQ-T4-03`, 315
for `CQ-T4-04`, 125 for `CQ-T4-05`, 263 for `CQ-T5-01`, 322 for `CQ-T5-02`,
316 for `CQ-T5-03`, 268 for `CQ-T5-04`, 315 for `CQ-T5-05`, 270 for
`CQ-C-01`, 264 for `CQ-C-02`, 400 for `CQ-C-03`, 142 for `CQ-C-04`, 322 for
`CQ-C-05`,
6960 in all.

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
    "review_input_manifest_sha256": "sha256:3103248045b7bb89725528bb30715e5148b7863516213aa8605dada928756196"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-22-v413",
    "completed_at": "2026-09-12T02:16:34Z"
  },
  "witnesses": [
    {
      "witness_key": "sample:basaltic-rocks",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its rock type, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "sample:basalts",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its rock type, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "sample:melt-inclusions",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its rock type, which is all this row claims."
    },
    {
      "witness_key": "sample:morb",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its rock type, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "sample:peridotites",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its rock type, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "sample:pillow-basalts",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its rock type, which is all this row claims."
    },
    {
      "witness_key": "sample:popping-rocks",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its rock type, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:all-authors-discussed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:046"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:arrivals-checked-manually",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:average-model-best-fitting",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:axial-valley-floor-character",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:ba90-rb90-calculated",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:categories-ab-good-quality",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:category-criteria",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:circles-show-location-qualities",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:co2-behaves-like-incompatible-elements",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:co2-calculated-from-rb90-ba90",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:co2-solubility-pressure-dependent",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:compiled-maximum-depths",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:compiled-morb-analyses",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:deeper-earthquakes-associations",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:deepest-earthquakes-documented",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:depth-resolution-tests",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:depth-selection-criterion",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:depth-tests-support-deep-events",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:depths-forced-fixed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:fig2b-depth-profiles",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:fig3-depth-shading",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:fig4-content",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:fig5-content",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:fixed-depth-rms-worse",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:focal-mechanisms-not-robust",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:focus-on-ridge-subsections",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:influencing-information-included",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:isotherms-from-thermal-model",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:012"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:local-magnitudes-determined",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:magmatic-tectonic-events-need-eruptions",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:max-depth-depends-on-other-factors",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:max-depths-affected-by-processes",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:maximum-likelihood-preferred",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:may-produce-long-period-earthquakes",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:measured-co2-close-to-solubility",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:mechanism-similar-to-volcanoes",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:melt-focused-beneath-ridge-axis",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:melt-movement-brittle-failure",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:melt-movement-not-applicable",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:model-selection-criterion",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:more-earthquakes-needed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:no-competing-interests",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:047"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:no-detachment-faults-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:no-permission-for-adapted-material",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:11:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:ntd1-magmatic-tectonic-origin",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:peer-review",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:11:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:poor-azimuthal-distribution",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:record-is-a-snapshot",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:reduced-velocity-model-reasonable",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:samples-are-degassed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:selected-model-preferred",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:station-corrections-and-swave-delays",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:station-corrections-iterated",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:swave-delays-removed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:trace-element-assumption",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:velocity-structure-matters",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:volatile-ratios-examined",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:volatile-role-melt-migration",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "claim:volatiles-control-magma-properties",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the kind of claim it is and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "claim:volatiles-extend-melting-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the kind of claim it is and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "claim:vpvs-17-reasonable",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the kind of claim it is and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "cnt:depth-test-subset",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the count, the population the count is taken over and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "cnt:events-mar",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:004",
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the count, the population the count is taken over and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "cnt:events-romanche-tf",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:003",
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the count, the population the count is taken over and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "cnt:hypodd-iterations",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the count, the population the count is taken over and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "cnt:identified-earthquakes",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the count, the population the count is taken over and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "cnt:location-categories",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the count, the population the count is taken over and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "cnt:magnitude-groups",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the count, the population the count is taken over and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "cnt:new-focal-mechanisms",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the count, the population the count is taken over and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "cnt:non-transform-discontinuities",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the count, the population the count is taken over and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "cnt:obs-network",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the count, the population the count is taken over and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "cnt:obs-without-data",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the count, the population the count is taken over and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "cnt:relocated-events",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the count, the population the count is taken over and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "cnt:romanche-2016-subevents",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the count, the population the count is taken over and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "cnt:subsections",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the count, the population the count is taken over and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "cnt:total-focal-mechanisms",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the count, the population the count is taken over and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "cnt:useful-obs",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the count, the population the count is taken over and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "cnt:velest-iterations",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the count, the population the count is taken over and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "cnt:velest-subdataset",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the count, the population the count is taken over and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "cnt:velocity-models",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:003",
        "page:7:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the count, the population the count is taken over and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "cnt:well-relocated-events",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the count, the population the count is taken over and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:average-depth-uncertainty",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:avg-horizontal-uncertainty",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:004",
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:axial-event-depth-stability",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:azimuthal-gap-relocated",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:b-value-catalog",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:b-values-groups",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the lower bound, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:brittle-lithospheric-thickness",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:co2-gas-phase-loss",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:co2-saturation-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:co2-saturation-pressure",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:co2-saturation-temperature",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:criterion-arrivals",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the lower bound and how the bounds are qualified, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:criterion-azimuthal-gap",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:criterion-swave-distance",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:crustal-age-bdb-shallow",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:deep-events-threshold",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound and how the bounds are qualified, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:depth-test-subset-range",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:depth-uncertainty-catalog",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:error-ellipsoid-confidence",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:expected-max-depth-here",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:expected-max-depth-slow-ridges",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:expected-max-depth-ultraslow-ridges",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:fm-criterion-fault-plane",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:fm-criterion-gap",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:fm-criterion-misfit",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:fm-criterion-polarities",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the lower bound and how the bounds are qualified, which is all this row claims."
    },
    {
      "witness_key": "obs:fm-criterion-probability",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound and how the bounds are qualified, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:fm-criterion-station-ratio",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the lower bound and how the bounds are qualified, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:fraction-meeting-two-criteria",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:full-spreading-rate",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:high-frequency-energy-threshold",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound and how the bounds are qualified, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:horizontal-uncertainty-catalog",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:iceland-magmatic-tectonic-depths",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound and how the bounds are qualified, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:instrument-spacing",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:magnitude-completeness",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:max-event-separation",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:mean-horizontal-error",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:mean-vertical-error",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:min-catalog-links",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the lower bound and how the bounds are qualified, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:min-obs-per-detection",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the lower bound and how the bounds are qualified, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:min-obs-per-relocated-event",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the lower bound and how the bounds are qualified, which is all this row claims."
    },
    {
      "witness_key": "obs:offaxis-cluster-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:offaxis-swarm-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:pore-pressure-trigger",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:profile-marker-interval",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:pwave-velocity-fastest-model",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound and how the bounds are qualified, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:recording-duration",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:rms-residual-catalog",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:rms-residual-relocated",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:solubility-model-temperature",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:station-gap-catalog",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:studied-portion-length",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:subsection-length",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:temperature-below-20km",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound and how the bounds are qualified, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:uncertainty-relocated",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:velest-max-gap",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:velest-min-arrivals",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the lower bound and how the bounds are qualified, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:velocity-constraint-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:velocity-perturbation",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "obs:vpvs-ratio",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects, the quantity it stands for, the class of that quantity, the lower bound, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "obs:vpvs-test-range",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the quantity it stands for, the class of that quantity, the lower bound, how the bounds are qualified and the upper bound, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "obs:young-crust-age-threshold",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, which is all this row claims."
    },
    {
      "witness_key": "claim:morb-samples-rc2-rc3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:ratios-are-good-proxy",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:seafloor-basalts-degassed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:obs-experiment-conducted",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:thanks-to-cruise-party",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:043"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:amplitude-from-wood-anderson",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:analyzed-rc2-rc3-samples",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:ascending-melt-resides-in-mantle",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:bdb-shallower-southward",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:co2-influences-melt-at-lab",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:cold-thick-lithosphere",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is, the disposition the authors give it and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:crust-formed-by-mantle-melt",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:deep-earthquakes-along-transform-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:deep-eq-aligned-n150e",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:deep-eq-interpreted-as-degassing",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:012"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:deep-events-not-location-artifact",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:deep-events-well-constrained",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:deep-microseismicity-related-to-co2-degassing",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:degassing-causes-deep-earthquakes",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is, the disposition the authors give it and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:degassing-volume-change-triggers-earthquakes",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:detachment-fault-inactive",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:earthquakes-occur-in-mantle",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:enrichment-from-low-degree-melting",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:estimated-primary-melt-co2-on-maps",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:fastest-model-shallow-events",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:009"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:faults-favor-melt-migration",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:fig3-transects",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:fig3a-content",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:fig6-brittle-ductile-patches",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:011"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:hummocky-seafloor-and-cones",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:hydrothermal-cooling",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is, the disposition the authors give it and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:iceland-mayotte-contexts-differ",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:magmatic-tectonic-hypothesis",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002",
        "page:5:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is, the disposition the authors give it and the name it projects."
    },
    {
      "witness_key": "claim:magmatism-dominates-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:mantle-beneath-rc2-is-hot",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:max-depth-does-not-follow-spreading-rate",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:melt-at-lab-from-co2-and-h2o",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:melt-freezes-at-lithosphere-base",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:melt-migration-not-understood",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:morb-compiled-from-petdb",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:no-active-vents-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:no-current-eruption",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:normal-vpvs-in-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:offaxis-magmatism-in-crust",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:pre-eruptive-co2-estimated",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:primary-vs-pre-eruptive",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:rainbow-at-ntd",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:rc1-amagmatic",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:rc1-exhumed-mantle",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:rc2-magmatic-origin",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:rc2-magmatically-robust",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:rc3-magmatic",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:ridge-axis-relocating",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:shallow-eq-from-high-angle-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:shear-zone-hypothesis",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is, the disposition the authors give it and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:small-pressure-increase-induces-earthquakes",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:southern-flank-crust-free",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:transform-faults-in-equatorial-atlantic",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:ultraslow-ridges-high-co2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:updated-compiled-data",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "claim:velocity-model-set",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the kind of claim it is and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "claim:volatiles-flush-melt-to-lab",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:010"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the kind of claim it is and the name it projects, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "claim:zero-position-is-rti",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the kind of claim it is and the name it projects."
    },
    {
      "witness_key": "cnt:located-earthquakes",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003",
        "page:6:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the count, the population the count is taken over and the name it projects, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:bdb-depth-if-cold",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:bdb-depth-ntd2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:bdb-depth-offaxis",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:brittle-lithosphere-thickness-ntds",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:co2-ba-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:co2-ba-rc3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:co2-ba90-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:co2-ba90-rc3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:co2-calculated-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:co2-calculated-rc3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:co2-primary-melt-abstract",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:co2-primary-melt-rc2-floor",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound and how the bounds are qualified, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:co2-rb-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:co2-rb-rc3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:co2-rb90-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:co2-rb90-rc3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:coverage-mar-axis",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:coverage-romanche-tf",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:crust-age-western-flank",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:crust-thickness-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:011"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the stated uncertainty, the unit, the lower bound, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:crust-thickness-western-flank",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the stated uncertainty, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:deep-eq-depth-abstract",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:deep-eq-depth-bsf",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:012"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:deep-eq-rc2-axis",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:deep-microseismicity-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:degassing-earthquake-depth-range",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:dry-melting-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:equatorial-atlantic-co2-average",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:equatorial-atlantic-co2-max",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:lab-melt-fraction",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:lab-subsolidus-temperature",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:lab-water-content",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:lithosphere-age-cold-edge",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:mantle-temperature-gt-1100",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound and how the bounds are qualified, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:mar-half-spreading-rate",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:mar-segment-length-romanche-chain",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:mayotte-depths",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound and how the bounds are qualified, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:no-earthquakes-below-20km",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound and how the bounds are qualified."
    },
    {
      "witness_key": "obs:normal-depth-eq-ntd2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:ntd1-length",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:ntd2-eq-depth-down-to",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:ntd2-max-eq-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:ntd2-ridge-offset",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:occ-max-eq-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:offaxis-microseismicity-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the unit, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:pre-eruptive-co2-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:rc2-ba-enrichment",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound and how the bounds are qualified."
    },
    {
      "witness_key": "obs:rc2-length",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:rc2-median-valley-width",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:rc2-rb-enrichment",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound and how the bounds are qualified."
    },
    {
      "witness_key": "obs:rc3-length",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:shallow-eq-depth-rti",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:swir-highest-co2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "obs:temperature-10-20km",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block the derivation reaches names the subject and states how the value was arrived at, the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so the row's claims all rest on the cited surface."
    },
    {
      "witness_key": "obs:transect-half-width",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The subject is named in the same block that states the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound, so nothing the row asserts goes beyond the cited surface."
    },
    {
      "witness_key": "obs:volatile-melting-initiation-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block both names the subject the row points at and carries the name it projects, the quantity it stands for, the class of that quantity, the unit, the lower bound, how the bounds are qualified and the upper bound."
    },
    {
      "witness_key": "event:romanche-2016",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the event type, the name it projects, the quantity it stands for, the class of that quantity, the lower bound, how the bounds are qualified and the upper bound, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:ascending-melt",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:002",
        "page:7:block:012"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:askja",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:axial-valley",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its feature kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:chain-tf",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:detachment-fault-rti",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the descriptive slot, its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:equatorial-atlantic",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its feature kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:extinct-vent-field",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:fagradalsfjall",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:gakkel",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its feature kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:iceland",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:inactive-hydrothermal-mound",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:juan-de-fuca",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its feature kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:knipovich-ridge",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:lithosphere",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006",
        "page:7:block:011"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:logachev-seamount",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its feature kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:magma-reservoir",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:mantle",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:mar",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its feature kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:mayotte",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:mylonite-shear-zones",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:ntd1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its feature kind, the name it projects and the orientation, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:ntd1-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the descriptive slot, the name it projects and the orientation, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:ntd2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its feature kind, the name it projects and the orientation, which is all this row claims."
    },
    {
      "witness_key": "feature:ntd2-normal-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the descriptive slot, its feature kind, the name it projects and the orientation, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:occ",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:occ-corrugated-surface",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the descriptive slot and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:occ-normal-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the descriptive slot, its feature kind, the name it projects and the orientation, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:oceanic-crust",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:pre-eruptive-melt",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006",
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the descriptive slot, its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:primary-melt",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:004",
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its feature kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:rainbow-massif",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:rc1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its feature kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:rc2-inward-dipping-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the descriptive slot, the name it projects and the orientation, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:rc2-median-valley",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:rc2-neovolcanic-ridge",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its feature kind, the name it projects and the orientation, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:rc3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind, the name it projects and the orientation, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:romanche-tf",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:rti",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its feature kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:sedimentary-layers",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:swir",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "feature:volcanic-cones",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its feature kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "feature:western-indian-ocean",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its feature kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "feature:western-ridge-flank",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the descriptive slot, its feature kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "ref:001",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:012",
        "page:8:block:013"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:002",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:014"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:003",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:015"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:004",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:016"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:005",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:017"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:006",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:001",
        "page:9:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:007",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the DOI, the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:008",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:009",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:010",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:011",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:012",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:013",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:014",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:012"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:015",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:013"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:016",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:014"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:017",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:016"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:018",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:017",
        "page:9:block:018"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:019",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:019"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:020",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:020",
        "page:9:block:021"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:021",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:022"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the DOI, the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:022",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:023",
        "page:9:block:024"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the DOI, the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:023",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:025",
        "page:9:block:026"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:024",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:028"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:025",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:029"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:026",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:030"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:027",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:031"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the DOI and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "ref:028",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:031",
        "page:9:block:032"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:029",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:033"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:030",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:034"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:031",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:035"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:032",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:036"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:033",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:037",
        "page:9:block:038"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:034",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:039"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:035",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:040"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:036",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:041"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:037",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:042"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:038",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:043"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:039",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:044",
        "page:9:block:045"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:040",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:046",
        "page:9:block:047"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:041",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:048"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:042",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:049"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:043",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:050"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:044",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:051"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:045",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:052"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:046",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:053"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:047",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:055"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:048",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:9:block:056",
        "page:10:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW DIGEST_OK NO_SUBJECT_IN_ROW The two cited blocks state the reference this row stands for, but the title breaks across the page and the name the row projects stops at that break, so the surface supports only part of the name and shows that it continues."
    },
    {
      "witness_key": "ref:049",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:050",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:051",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:004",
        "page:10:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:052",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:006",
        "page:10:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:053",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:054",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:055",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:056",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:011"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:057",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:012"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:058",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:013",
        "page:10:block:014"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:059",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:015"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:060",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:016"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:061",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:017"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:062",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:018"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:063",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:019"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:064",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:020"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:065",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:021"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:066",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:023"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:067",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:024"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:068",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:025"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:069",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:026"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:070",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:027",
        "page:10:block:028"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:071",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:029"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:072",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:030"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:073",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:032"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:074",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:034"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:075",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:035",
        "page:10:block:036"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the DOI, the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:076",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:037"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "ref:077",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:038",
        "page:10:block:039"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "ref:078",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:040"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the name it projects and its source kind, which is all this row claims."
    },
    {
      "witness_key": "ref:079",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:041",
        "page:10:block:042"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "source:article:yu-2025",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001",
        "page:1:block:006",
        "page:2:block:008",
        "page:3:block:006",
        "page:4:block:008",
        "page:5:block:011",
        "page:6:block:006",
        "page:7:block:013",
        "page:8:block:018",
        "page:11:block:005",
        "page:11:block:006",
        "page:10:block:048"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the DOI, the licence, the name it projects and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "source:cc-licence",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:11:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the descriptive slot, the name it projects and the location it gives, which is all this row claims."
    },
    {
      "witness_key": "source:cruise-website",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the descriptive slot, the name it projects, the location it gives and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "source:petdb",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:005",
        "page:8:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the name it projects, the location it gives and its source kind, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "source:supplementary",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:11:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the descriptive slot, the name it projects and the location it gives, which is all this row claims."
    },
    {
      "witness_key": "source:zenodo-catalog",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the descriptive slot, the name it projects and its source kind, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "rel:corrugated-surface-part-of-occ",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:006"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalises the relation states it between the two endpoints and carries the relation type."
    },
    {
      "witness_key": "rel:mar-within-equatorial-atlantic",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The relation and the relation type are stated in the block the derivation reaches, with both endpoints named there."
    },
    {
      "witness_key": "rel:ntd2-faults-within",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalises the relation states it between the two endpoints and carries the relation type."
    },
    {
      "witness_key": "rel:occ-cut-by-normal-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The relation and the relation type are stated in the block the derivation reaches, with both endpoints named there."
    },
    {
      "witness_key": "rel:rc1-bounded-by-detachment",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalises the relation states it between the two endpoints and carries the relation type."
    },
    {
      "witness_key": "rel:rc2-adjacent-ntd1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The relation and the relation type are stated in the block the derivation reaches, with both endpoints named there."
    },
    {
      "witness_key": "rel:rc2-bounded-by-inward-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:001"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalises the relation states it between the two endpoints and carries the relation type."
    },
    {
      "witness_key": "rel:rc3-adjacent-ntd2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The relation and the relation type are stated in the block the derivation reaches, with both endpoints named there."
    },
    {
      "witness_key": "campaign:smarties",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "NO_SUBJECT_IN_ROW The block the derivation reaches states the descriptive slot, the name it projects and how precisely it is dated, so the cited surface supports every claim the row makes. This record projects no locator and no statement digest, so there is no digest to check; the trace still names the block its slots were drawn from."
    },
    {
      "witness_key": "instrument:obs",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001"
      ],
      "rationale": "NO_SUBJECT_IN_ROW Everything the row asserts, the descriptive slot and the name it projects, is stated in the block the derivation reaches. This record projects no locator and no statement digest, so there is no digest to check; the trace still names the block its slots were drawn from."
    },
    {
      "witness_key": "rel:obs-part-of-smarties",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalises the relation states it between the two endpoints and carries the relation type."
    },
    {
      "witness_key": "boundary:bdb",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its boundary kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "boundary:isotherm-600-800",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its boundary kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "boundary:isotherm-700",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its boundary kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "boundary:isotherm-750",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its boundary kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "boundary:lab",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:010",
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, its boundary kind and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "boundary:moho",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:011"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries its boundary kind and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "boundary:solidus-peridotite",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states its boundary kind and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "rel:bdb-corresponds-isotherm-700",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalises the relation states it between the two endpoints and carries the relation type."
    },
    {
      "witness_key": "rel:bdb-corresponds-isotherm-750",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:011"
      ],
      "rationale": "DIGEST_OK DERIVATION_NON_LOCAL The relation and the relation type are stated in the block the derivation reaches, with both endpoints named there. The block that carries the relation is not among the blocks either endpoint is derived from, which is a fact about where the two records came from and not a reason to doubt the relation."
    },
    {
      "witness_key": "method:double-difference",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "NO_SUBJECT_IN_ROW The block the derivation reaches states the descriptive slot and the name it projects, so the cited surface supports every claim the row makes. This record projects no locator and no statement digest, so there is no digest to check; the trace still names the block its slots were drawn from."
    },
    {
      "witness_key": "method:local-magnitude",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002"
      ],
      "rationale": "NO_SUBJECT_IN_ROW Everything the row asserts, the descriptive slot and the name it projects, is stated in the block the derivation reaches. This record projects no locator and no statement digest, so there is no digest to check; the trace still names the block its slots were drawn from."
    },
    {
      "witness_key": "method:nonlinear-location",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "NO_SUBJECT_IN_ROW The cited block carries the descriptive slot and the name it projects, which is all this row claims. This record projects no locator and no statement digest, so there is no digest to check; the trace still names the block its slots were drawn from."
    },
    {
      "witness_key": "method:refraction-profile",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "NO_SUBJECT_IN_ROW The block the derivation reaches states the descriptive slot and the name it projects, so the cited surface supports every claim the row makes. This record projects no locator and no statement digest, so there is no digest to check; the trace still names the block its slots were drawn from."
    },
    {
      "witness_key": "method:sta-lta",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "NO_SUBJECT_IN_ROW Everything the row asserts, the descriptive slot and the name it projects, is stated in the block the derivation reaches. This record projects no locator and no statement digest, so there is no digest to check; the trace still names the block its slots were drawn from."
    },
    {
      "witness_key": "software:global-mapper",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the descriptive slot, the name it projects and the location it gives, which is all this row claims."
    },
    {
      "witness_key": "software:gmt",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the descriptive slot and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "software:hash",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003",
        "page:8:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the descriptive slot, the name it projects, the location it gives and the version, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "software:hypodd",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006",
        "page:8:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the descriptive slot, the name it projects, the location it gives and the version, which is all this row claims."
    },
    {
      "witness_key": "software:nonlinloc",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:004",
        "page:8:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the descriptive slot, the name it projects and the location it gives, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "software:seisan",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002",
        "page:8:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, the descriptive slot, the name it projects and the location it gives, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "software:velest",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:004",
        "page:8:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the descriptive slot, the name it projects and the location it gives, which is all this row claims."
    },
    {
      "witness_key": "software:zmap",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002",
        "page:8:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states the descriptive slot, the name it projects and the location it gives, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "agent:anne-briais",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, whether the agent is a person or an organisation and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "agent:brittany",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries whether the agent is a person or an organisation and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "agent:cedric-hamelin",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states whether the agent is a person or an organisation and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "agent:cnr-igag",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, whether the agent is a person or an organisation, the descriptive slot and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "agent:daniele-brunelli",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries whether the agent is a person or an organisation and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "agent:erc",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states whether the agent is a person or an organisation and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "agent:french-fleet",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, whether the agent is a person or an organisation and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "agent:geo-ocean",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries whether the agent is a person or an organisation, the descriptive slot and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "agent:ipgp",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states whether the agent is a person or an organisation, the descriptive slot and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "agent:isblue",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, whether the agent is a person or an organisation, the descriptive slot and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "agent:lea-grenet",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries whether the agent is a person or an organisation and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "agent:lorenzo-petracchini",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states whether the agent is a person or an organisation and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "agent:marcia-maia",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, whether the agent is a person or an organisation and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "agent:nsfc",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries whether the agent is a person or an organisation and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "agent:satish-singh",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:11:block:002",
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states whether the agent is a person or an organisation and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "agent:sio",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, whether the agent is a person or an organisation, the descriptive slot and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "agent:springer-nature",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:11:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries whether the agent is a person or an organisation and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "agent:univ-modena",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block the derivation reaches states whether the agent is a person or an organisation, the descriptive slot and the name it projects, so the cited surface supports every claim the row makes."
    },
    {
      "witness_key": "agent:zhiteng-yu",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:11:block:002",
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW Everything the row asserts, whether the agent is a person or an organisation and the name it projects, is stated in the block the derivation reaches."
    },
    {
      "witness_key": "agent:zjnsf",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries whether the agent is a person or an organisation and the name it projects, which is all this row claims."
    },
    {
      "witness_key": "credit:erc-transatlanticilab",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The relation and the award identifier and the relation type are stated in the block the derivation reaches, with both endpoints named there."
    },
    {
      "witness_key": "credit:nsfc-42330308",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalises the relation states it between the two endpoints and carries the award identifier and the relation type."
    },
    {
      "witness_key": "credit:nsfc-42422603",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The relation and the award identifier and the relation type are stated in the block the derivation reaches, with both endpoints named there."
    },
    {
      "witness_key": "credit:zjnsf",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK DERIVATION_LOCAL The block that formalises the relation states it between the two endpoints and carries the award identifier and the relation type."
    }
  ],
  "questions": [
    {
      "question_id": "CQ-T1-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All three items are returned and two of them are joined by a relation the result also returns, so the cruise, the network and the acquisition can be read off the rows without leaving them.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "campaign_name",
          "row_index": 0,
          "absent_reason": null,
          "note": "the campaign record names the cruise"
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "the instrument record stands for the ocean-bottom seismometer network"
        },
        {
          "semantic": "data_acquisition",
          "row_index": 84,
          "absent_reason": null,
          "note": "the relation places the network inside the cruise, and the block it comes from is the one that reports the acquisition"
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:1:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "campaign:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instrument:obs"
        },
        {
          "row_index": 2,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 3,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 4,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 5,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 6,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 7,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 8,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 9,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 17,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 18,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 19,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 20,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 21,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 22,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 23,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 24,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 25,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 26,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 27,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 28,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 29,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 30,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 31,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 32,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 33,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 34,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 35,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 36,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 37,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 38,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 39,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 40,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 41,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 42,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 43,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 44,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 45,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 46,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 47,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 48,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 49,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 50,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 51,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 52,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 53,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 54,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 55,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 56,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 57,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 58,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 59,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 60,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 61,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 62,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 63,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 64,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 65,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 66,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 67,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 68,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 69,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 70,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 71,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 72,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 73,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 74,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 75,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 76,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 77,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 78,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 79,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 80,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 81,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 82,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 83,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 84,
          "witness_key": "rel:obs-part-of-smarties"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 86,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 87,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 88,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 89,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 90,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 91,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 92,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 93,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 94,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 95,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 96,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 97,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 98,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 99,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 100,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 101,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 102,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 103,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 104,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 105,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 106,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 107,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 108,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 109,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 110,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 112,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 113,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 114,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 115,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 116,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 117,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 118,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 119,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 120,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 121,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 122,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 123,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 124,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 125,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 126,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 127,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 128,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 129,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 130,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 131,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 132,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 133,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 134,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 135,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 136,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 137,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 138,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 139,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 140,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 141,
          "witness_key": "obs:volatile-melting-initiation-depth"
        }
      ]
    },
    {
      "question_id": "CQ-T1-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every item names a row. The deployment is carried as the campaign the network belongs to rather than as an event record of its own, which is the only form the graph gives it.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "instrument_count",
          "row_index": 11,
          "absent_reason": null,
          "note": "the count record carries the number and the population it counts"
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "the instrument record stands for the network"
        },
        {
          "semantic": "deployment_event",
          "row_index": 0,
          "absent_reason": null,
          "note": "the campaign record is the cruise during which the network went into the water; no separate dated deployment record exists"
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002",
        "page:1:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "campaign:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instrument:obs"
        },
        {
          "row_index": 2,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 3,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 4,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 5,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 6,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 7,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 8,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 9,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 17,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 18,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 19,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 20,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 21,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 22,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 23,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 24,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 25,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 26,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 27,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 28,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 29,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 30,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 31,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 32,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 33,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 34,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 35,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 36,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 37,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 38,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 39,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 40,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 41,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 42,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 43,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 44,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 45,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 46,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 47,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 48,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 49,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 50,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 51,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 52,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 53,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 54,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 55,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 56,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 57,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 58,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 59,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 60,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 61,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 62,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 63,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 64,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 65,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 66,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 67,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 68,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 69,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 70,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 71,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 72,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 73,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 74,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 75,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 76,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 77,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 78,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 79,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 80,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 81,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 82,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 83,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 84,
          "witness_key": "rel:obs-part-of-smarties"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 86,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 87,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 88,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 89,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 90,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 91,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 92,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 93,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 94,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 95,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 96,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 97,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 98,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 99,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 100,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 101,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 102,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 103,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 104,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 105,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 106,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 107,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 108,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 109,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 110,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 112,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 113,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 114,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 115,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 116,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 117,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 118,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 119,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 120,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 121,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 122,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 123,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 124,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 125,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 126,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 127,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 128,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 129,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 130,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 131,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 132,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 133,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 134,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 135,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 136,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 137,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 138,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 139,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 140,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 141,
          "witness_key": "obs:volatile-melting-initiation-depth"
        }
      ]
    },
    {
      "question_id": "CQ-T1-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The article is reached, the acceptance is not. The reading carries the acceptance line, the capture keeps it as an assertion, and the producer recorded that the accepted ontology declares no slot for it, so nothing downstream of population can return it.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "publication_record",
          "row_index": 79,
          "absent_reason": null,
          "note": "the article record carries the paper itself"
        },
        {
          "semantic": "acceptance_event",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "the capture holds the acceptance line as an assertion but formalises it into no record, recording that the accepted ontology has no slot for it"
        },
        {
          "semantic": "calendar_date",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "the same gap removes the date; no record in the graph carries a calendar date at all"
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:1:block:006",
        "page:2:block:008",
        "page:3:block:006",
        "page:4:block:008",
        "page:5:block:011",
        "page:6:block:006",
        "page:7:block:013",
        "page:8:block:018",
        "page:11:block:005",
        "page:11:block:006",
        "page:10:block:048"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "ref:001"
        },
        {
          "row_index": 1,
          "witness_key": "ref:002"
        },
        {
          "row_index": 2,
          "witness_key": "ref:003"
        },
        {
          "row_index": 3,
          "witness_key": "ref:004"
        },
        {
          "row_index": 4,
          "witness_key": "ref:005"
        },
        {
          "row_index": 5,
          "witness_key": "ref:006"
        },
        {
          "row_index": 6,
          "witness_key": "ref:007"
        },
        {
          "row_index": 7,
          "witness_key": "ref:008"
        },
        {
          "row_index": 8,
          "witness_key": "ref:009"
        },
        {
          "row_index": 9,
          "witness_key": "ref:010"
        },
        {
          "row_index": 10,
          "witness_key": "ref:011"
        },
        {
          "row_index": 11,
          "witness_key": "ref:012"
        },
        {
          "row_index": 12,
          "witness_key": "ref:013"
        },
        {
          "row_index": 13,
          "witness_key": "ref:014"
        },
        {
          "row_index": 14,
          "witness_key": "ref:015"
        },
        {
          "row_index": 15,
          "witness_key": "ref:016"
        },
        {
          "row_index": 16,
          "witness_key": "ref:017"
        },
        {
          "row_index": 17,
          "witness_key": "ref:018"
        },
        {
          "row_index": 18,
          "witness_key": "ref:019"
        },
        {
          "row_index": 19,
          "witness_key": "ref:020"
        },
        {
          "row_index": 20,
          "witness_key": "ref:021"
        },
        {
          "row_index": 21,
          "witness_key": "ref:022"
        },
        {
          "row_index": 22,
          "witness_key": "ref:023"
        },
        {
          "row_index": 23,
          "witness_key": "ref:024"
        },
        {
          "row_index": 24,
          "witness_key": "ref:025"
        },
        {
          "row_index": 25,
          "witness_key": "ref:026"
        },
        {
          "row_index": 26,
          "witness_key": "ref:027"
        },
        {
          "row_index": 27,
          "witness_key": "ref:028"
        },
        {
          "row_index": 28,
          "witness_key": "ref:029"
        },
        {
          "row_index": 29,
          "witness_key": "ref:030"
        },
        {
          "row_index": 30,
          "witness_key": "ref:031"
        },
        {
          "row_index": 31,
          "witness_key": "ref:032"
        },
        {
          "row_index": 32,
          "witness_key": "ref:033"
        },
        {
          "row_index": 33,
          "witness_key": "ref:034"
        },
        {
          "row_index": 34,
          "witness_key": "ref:035"
        },
        {
          "row_index": 35,
          "witness_key": "ref:036"
        },
        {
          "row_index": 36,
          "witness_key": "ref:037"
        },
        {
          "row_index": 37,
          "witness_key": "ref:038"
        },
        {
          "row_index": 38,
          "witness_key": "ref:039"
        },
        {
          "row_index": 39,
          "witness_key": "ref:040"
        },
        {
          "row_index": 40,
          "witness_key": "ref:041"
        },
        {
          "row_index": 41,
          "witness_key": "ref:042"
        },
        {
          "row_index": 42,
          "witness_key": "ref:043"
        },
        {
          "row_index": 43,
          "witness_key": "ref:044"
        },
        {
          "row_index": 44,
          "witness_key": "ref:045"
        },
        {
          "row_index": 45,
          "witness_key": "ref:046"
        },
        {
          "row_index": 46,
          "witness_key": "ref:047"
        },
        {
          "row_index": 47,
          "witness_key": "ref:048"
        },
        {
          "row_index": 48,
          "witness_key": "ref:049"
        },
        {
          "row_index": 49,
          "witness_key": "ref:050"
        },
        {
          "row_index": 50,
          "witness_key": "ref:051"
        },
        {
          "row_index": 51,
          "witness_key": "ref:052"
        },
        {
          "row_index": 52,
          "witness_key": "ref:053"
        },
        {
          "row_index": 53,
          "witness_key": "ref:054"
        },
        {
          "row_index": 54,
          "witness_key": "ref:055"
        },
        {
          "row_index": 55,
          "witness_key": "ref:056"
        },
        {
          "row_index": 56,
          "witness_key": "ref:057"
        },
        {
          "row_index": 57,
          "witness_key": "ref:058"
        },
        {
          "row_index": 58,
          "witness_key": "ref:059"
        },
        {
          "row_index": 59,
          "witness_key": "ref:060"
        },
        {
          "row_index": 60,
          "witness_key": "ref:061"
        },
        {
          "row_index": 61,
          "witness_key": "ref:062"
        },
        {
          "row_index": 62,
          "witness_key": "ref:063"
        },
        {
          "row_index": 63,
          "witness_key": "ref:064"
        },
        {
          "row_index": 64,
          "witness_key": "ref:065"
        },
        {
          "row_index": 65,
          "witness_key": "ref:066"
        },
        {
          "row_index": 66,
          "witness_key": "ref:067"
        },
        {
          "row_index": 67,
          "witness_key": "ref:068"
        },
        {
          "row_index": 68,
          "witness_key": "ref:069"
        },
        {
          "row_index": 69,
          "witness_key": "ref:070"
        },
        {
          "row_index": 70,
          "witness_key": "ref:071"
        },
        {
          "row_index": 71,
          "witness_key": "ref:072"
        },
        {
          "row_index": 72,
          "witness_key": "ref:073"
        },
        {
          "row_index": 73,
          "witness_key": "ref:074"
        },
        {
          "row_index": 74,
          "witness_key": "ref:075"
        },
        {
          "row_index": 75,
          "witness_key": "ref:076"
        },
        {
          "row_index": 76,
          "witness_key": "ref:077"
        },
        {
          "row_index": 77,
          "witness_key": "ref:078"
        },
        {
          "row_index": 78,
          "witness_key": "ref:079"
        },
        {
          "row_index": 79,
          "witness_key": "source:article:yu-2025"
        },
        {
          "row_index": 80,
          "witness_key": "source:cc-licence"
        },
        {
          "row_index": 81,
          "witness_key": "source:cruise-website"
        },
        {
          "row_index": 82,
          "witness_key": "source:petdb"
        },
        {
          "row_index": 83,
          "witness_key": "source:supplementary"
        },
        {
          "row_index": 84,
          "witness_key": "source:zenodo-catalog"
        },
        {
          "row_index": 85,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 87,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 88,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 89,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 90,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 91,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 92,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 93,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 94,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 95,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 96,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 97,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 98,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 99,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 100,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 101,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 102,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 103,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 104,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 105,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 106,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 107,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 108,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 109,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 110,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 111,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 112,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 113,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 114,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 115,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 116,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 117,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 118,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 119,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 120,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 121,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 122,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 123,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 124,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 125,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 126,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 127,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 128,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 129,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 130,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 131,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 132,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 133,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 134,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 135,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 136,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 137,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 138,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 139,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 140,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 141,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 142,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 143,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 144,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 145,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 146,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 147,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 148,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 149,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 150,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 151,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 152,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 153,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 154,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 155,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 156,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 157,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 158,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 159,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 160,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 161,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 162,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 163,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 164,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 165,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 166,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 167,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 168,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 169,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 170,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 171,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 172,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 173,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 174,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 175,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 176,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 177,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 178,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 179,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 180,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 181,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 182,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 183,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 184,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 185,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 186,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 187,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 188,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 189,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 190,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 191,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 192,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 193,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 194,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 195,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 196,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 197,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 198,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 199,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 200,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 201,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 202,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 203,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 204,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 205,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 206,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 207,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 208,
          "witness_key": "claim:zero-position-is-rti"
        }
      ]
    },
    {
      "question_id": "CQ-T1-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The repository and the deposit are in one row and the identifier is in none. The identifier is present in the reading but broken across a block boundary, and the producer chose not to assemble it across blocks, so the graph holds the deposit without a way to cite it.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "dataset_record",
          "row_index": 84,
          "absent_reason": null,
          "note": "the deposit record stands for the catalogue and the picked arrivals"
        },
        {
          "semantic": "repository_name",
          "row_index": 84,
          "absent_reason": null,
          "note": "the same row names the repository"
        },
        {
          "semantic": "persistent_identifier",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "the deposit record carries no identifier slot value; the capture records that the identifier is split across two reading blocks and so was not carried from either"
        }
      ],
      "source_locators": [
        "page:8:block:008"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "ref:001"
        },
        {
          "row_index": 1,
          "witness_key": "ref:002"
        },
        {
          "row_index": 2,
          "witness_key": "ref:003"
        },
        {
          "row_index": 3,
          "witness_key": "ref:004"
        },
        {
          "row_index": 4,
          "witness_key": "ref:005"
        },
        {
          "row_index": 5,
          "witness_key": "ref:006"
        },
        {
          "row_index": 6,
          "witness_key": "ref:007"
        },
        {
          "row_index": 7,
          "witness_key": "ref:008"
        },
        {
          "row_index": 8,
          "witness_key": "ref:009"
        },
        {
          "row_index": 9,
          "witness_key": "ref:010"
        },
        {
          "row_index": 10,
          "witness_key": "ref:011"
        },
        {
          "row_index": 11,
          "witness_key": "ref:012"
        },
        {
          "row_index": 12,
          "witness_key": "ref:013"
        },
        {
          "row_index": 13,
          "witness_key": "ref:014"
        },
        {
          "row_index": 14,
          "witness_key": "ref:015"
        },
        {
          "row_index": 15,
          "witness_key": "ref:016"
        },
        {
          "row_index": 16,
          "witness_key": "ref:017"
        },
        {
          "row_index": 17,
          "witness_key": "ref:018"
        },
        {
          "row_index": 18,
          "witness_key": "ref:019"
        },
        {
          "row_index": 19,
          "witness_key": "ref:020"
        },
        {
          "row_index": 20,
          "witness_key": "ref:021"
        },
        {
          "row_index": 21,
          "witness_key": "ref:022"
        },
        {
          "row_index": 22,
          "witness_key": "ref:023"
        },
        {
          "row_index": 23,
          "witness_key": "ref:024"
        },
        {
          "row_index": 24,
          "witness_key": "ref:025"
        },
        {
          "row_index": 25,
          "witness_key": "ref:026"
        },
        {
          "row_index": 26,
          "witness_key": "ref:027"
        },
        {
          "row_index": 27,
          "witness_key": "ref:028"
        },
        {
          "row_index": 28,
          "witness_key": "ref:029"
        },
        {
          "row_index": 29,
          "witness_key": "ref:030"
        },
        {
          "row_index": 30,
          "witness_key": "ref:031"
        },
        {
          "row_index": 31,
          "witness_key": "ref:032"
        },
        {
          "row_index": 32,
          "witness_key": "ref:033"
        },
        {
          "row_index": 33,
          "witness_key": "ref:034"
        },
        {
          "row_index": 34,
          "witness_key": "ref:035"
        },
        {
          "row_index": 35,
          "witness_key": "ref:036"
        },
        {
          "row_index": 36,
          "witness_key": "ref:037"
        },
        {
          "row_index": 37,
          "witness_key": "ref:038"
        },
        {
          "row_index": 38,
          "witness_key": "ref:039"
        },
        {
          "row_index": 39,
          "witness_key": "ref:040"
        },
        {
          "row_index": 40,
          "witness_key": "ref:041"
        },
        {
          "row_index": 41,
          "witness_key": "ref:042"
        },
        {
          "row_index": 42,
          "witness_key": "ref:043"
        },
        {
          "row_index": 43,
          "witness_key": "ref:044"
        },
        {
          "row_index": 44,
          "witness_key": "ref:045"
        },
        {
          "row_index": 45,
          "witness_key": "ref:046"
        },
        {
          "row_index": 46,
          "witness_key": "ref:047"
        },
        {
          "row_index": 47,
          "witness_key": "ref:048"
        },
        {
          "row_index": 48,
          "witness_key": "ref:049"
        },
        {
          "row_index": 49,
          "witness_key": "ref:050"
        },
        {
          "row_index": 50,
          "witness_key": "ref:051"
        },
        {
          "row_index": 51,
          "witness_key": "ref:052"
        },
        {
          "row_index": 52,
          "witness_key": "ref:053"
        },
        {
          "row_index": 53,
          "witness_key": "ref:054"
        },
        {
          "row_index": 54,
          "witness_key": "ref:055"
        },
        {
          "row_index": 55,
          "witness_key": "ref:056"
        },
        {
          "row_index": 56,
          "witness_key": "ref:057"
        },
        {
          "row_index": 57,
          "witness_key": "ref:058"
        },
        {
          "row_index": 58,
          "witness_key": "ref:059"
        },
        {
          "row_index": 59,
          "witness_key": "ref:060"
        },
        {
          "row_index": 60,
          "witness_key": "ref:061"
        },
        {
          "row_index": 61,
          "witness_key": "ref:062"
        },
        {
          "row_index": 62,
          "witness_key": "ref:063"
        },
        {
          "row_index": 63,
          "witness_key": "ref:064"
        },
        {
          "row_index": 64,
          "witness_key": "ref:065"
        },
        {
          "row_index": 65,
          "witness_key": "ref:066"
        },
        {
          "row_index": 66,
          "witness_key": "ref:067"
        },
        {
          "row_index": 67,
          "witness_key": "ref:068"
        },
        {
          "row_index": 68,
          "witness_key": "ref:069"
        },
        {
          "row_index": 69,
          "witness_key": "ref:070"
        },
        {
          "row_index": 70,
          "witness_key": "ref:071"
        },
        {
          "row_index": 71,
          "witness_key": "ref:072"
        },
        {
          "row_index": 72,
          "witness_key": "ref:073"
        },
        {
          "row_index": 73,
          "witness_key": "ref:074"
        },
        {
          "row_index": 74,
          "witness_key": "ref:075"
        },
        {
          "row_index": 75,
          "witness_key": "ref:076"
        },
        {
          "row_index": 76,
          "witness_key": "ref:077"
        },
        {
          "row_index": 77,
          "witness_key": "ref:078"
        },
        {
          "row_index": 78,
          "witness_key": "ref:079"
        },
        {
          "row_index": 79,
          "witness_key": "source:article:yu-2025"
        },
        {
          "row_index": 80,
          "witness_key": "source:cc-licence"
        },
        {
          "row_index": 81,
          "witness_key": "source:cruise-website"
        },
        {
          "row_index": 82,
          "witness_key": "source:petdb"
        },
        {
          "row_index": 83,
          "witness_key": "source:supplementary"
        },
        {
          "row_index": 84,
          "witness_key": "source:zenodo-catalog"
        },
        {
          "row_index": 85,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 87,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 88,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 89,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 90,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 91,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 92,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 93,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 94,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 95,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 96,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 97,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 98,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 99,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 100,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 101,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 102,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 103,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 104,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 105,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 106,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 107,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 108,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 109,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 110,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 111,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 112,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 113,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 114,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 115,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 116,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 117,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 118,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 119,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 120,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 121,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 122,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 123,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 124,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 125,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 126,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 127,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 128,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 129,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 130,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 131,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 132,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 133,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 134,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 135,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 136,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 137,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 138,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 139,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 140,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 141,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 142,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 143,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 144,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 145,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 146,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 147,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 148,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 149,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 150,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 151,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 152,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 153,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 154,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 155,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 156,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 157,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 158,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 159,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 160,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 161,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 162,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 163,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 164,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 165,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 166,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 167,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 168,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 169,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 170,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 171,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 172,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 173,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 174,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 175,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 176,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 177,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 178,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 179,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 180,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 181,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 182,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 183,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 184,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 185,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 186,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 187,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 188,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 189,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 190,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 191,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 192,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 193,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 194,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 195,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 196,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 197,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 198,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 199,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 200,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 201,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 202,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 203,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 204,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 205,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 206,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 207,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 208,
          "witness_key": "claim:zero-position-is-rti"
        }
      ]
    },
    {
      "question_id": "CQ-T1-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The duration is in one row with its unit. The observing system is only named inside the scope of a count row, because this question's types do not include the instrument record that stands for the network, and nothing in the result joins the two rows.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "recording_interval",
          "row_index": 67,
          "absent_reason": null,
          "note": "the observation is of the continuous recording period"
        },
        {
          "semantic": "duration_value",
          "row_index": 67,
          "absent_reason": null,
          "note": "the same row carries the bounds"
        },
        {
          "semantic": "time_unit",
          "row_index": 67,
          "absent_reason": null,
          "note": "and the unit"
        },
        {
          "semantic": "observing_system",
          "row_index": 10,
          "absent_reason": null,
          "note": "the count row names the ocean-bottom seismometer network as the population it is scoped to; this question reaches no instrument record"
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "campaign:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 2,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 3,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 4,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 5,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 6,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 7,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 8,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 9,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 17,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 18,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 19,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 20,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 21,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 22,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 23,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 24,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 25,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 26,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 27,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 28,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 29,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 30,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 31,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 32,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 33,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 34,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 35,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 36,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 37,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 38,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 39,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 40,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 41,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 42,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 43,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 44,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 45,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 46,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 47,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 48,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 49,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 50,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 51,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 52,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 53,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 54,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 55,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 56,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 57,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 58,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 59,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 60,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 61,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 62,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 63,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 64,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 65,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 66,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 67,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 68,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 69,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 70,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 71,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 72,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 73,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 74,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 75,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 76,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 77,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 78,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 79,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 80,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 81,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 82,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 83,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 84,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 85,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 86,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 87,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 88,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 89,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 90,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 91,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 92,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 93,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 94,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 95,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 96,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 97,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 98,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 99,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 100,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 101,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 102,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 103,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 105,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 106,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 107,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 108,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 109,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 110,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 111,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 112,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 113,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 114,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 115,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 116,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 117,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 118,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 119,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 120,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 121,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 122,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 123,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 124,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 125,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 126,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 127,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 128,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 129,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 130,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 131,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 132,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 133,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 134,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 135,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 136,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 137,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 138,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 139,
          "witness_key": "obs:volatile-melting-initiation-depth"
        }
      ]
    },
    {
      "question_id": "CQ-T2-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four items are in the rows and the relation joins two of them. The side is carried in the fault's own description rather than on the core complex, which is the only place the projection puts it.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "named_subsection",
          "row_index": 38,
          "absent_reason": null,
          "note": "the ridge segment record names the subsection"
        },
        {
          "semantic": "structural_feature",
          "row_index": 11,
          "absent_reason": null,
          "note": "the fault record carries the structure and its kind"
        },
        {
          "semantic": "bounding_relation",
          "row_index": 118,
          "absent_reason": null,
          "note": "the relation states the bounding and both endpoints are returned"
        },
        {
          "semantic": "side_of_axis",
          "row_index": 11,
          "absent_reason": null,
          "note": "the fault record's descriptive slot states which side it bounds the segment on"
        }
      ],
      "source_locators": [
        "page:1:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "boundary:bdb"
        },
        {
          "row_index": 1,
          "witness_key": "boundary:isotherm-600-800"
        },
        {
          "row_index": 2,
          "witness_key": "boundary:isotherm-700"
        },
        {
          "row_index": 3,
          "witness_key": "boundary:isotherm-750"
        },
        {
          "row_index": 4,
          "witness_key": "boundary:lab"
        },
        {
          "row_index": 5,
          "witness_key": "boundary:moho"
        },
        {
          "row_index": 6,
          "witness_key": "boundary:solidus-peridotite"
        },
        {
          "row_index": 7,
          "witness_key": "feature:ascending-melt"
        },
        {
          "row_index": 8,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 9,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 10,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 11,
          "witness_key": "feature:detachment-fault-rti"
        },
        {
          "row_index": 12,
          "witness_key": "feature:equatorial-atlantic"
        },
        {
          "row_index": 13,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 14,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 15,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 16,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 17,
          "witness_key": "feature:inactive-hydrothermal-mound"
        },
        {
          "row_index": 18,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 19,
          "witness_key": "feature:knipovich-ridge"
        },
        {
          "row_index": 20,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 21,
          "witness_key": "feature:logachev-seamount"
        },
        {
          "row_index": 22,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 24,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 25,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 26,
          "witness_key": "feature:mylonite-shear-zones"
        },
        {
          "row_index": 27,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd2-normal-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 32,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ-normal-faults"
        },
        {
          "row_index": 34,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 35,
          "witness_key": "feature:pre-eruptive-melt"
        },
        {
          "row_index": 36,
          "witness_key": "feature:primary-melt"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rainbow-massif"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-inward-dipping-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc2-median-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 44,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 45,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 46,
          "witness_key": "feature:sedimentary-layers"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 49,
          "witness_key": "feature:western-indian-ocean"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-ridge-flank"
        },
        {
          "row_index": 51,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 53,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 55,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 56,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 57,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 58,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 61,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 62,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 63,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 64,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 65,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 66,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 67,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 68,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 69,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 71,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 72,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 73,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 74,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 75,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 76,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 77,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 78,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 79,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 80,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 81,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 82,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 83,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 84,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 85,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 86,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 87,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 88,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 89,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 90,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 91,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 92,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 93,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 94,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 95,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 96,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 97,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 98,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 99,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 100,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 101,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 102,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 103,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 104,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 105,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 106,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 107,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 108,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 109,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 110,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 111,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 112,
          "witness_key": "rel:bdb-corresponds-isotherm-700"
        },
        {
          "row_index": 113,
          "witness_key": "rel:bdb-corresponds-isotherm-750"
        },
        {
          "row_index": 114,
          "witness_key": "rel:corrugated-surface-part-of-occ"
        },
        {
          "row_index": 115,
          "witness_key": "rel:mar-within-equatorial-atlantic"
        },
        {
          "row_index": 116,
          "witness_key": "rel:ntd2-faults-within"
        },
        {
          "row_index": 117,
          "witness_key": "rel:occ-cut-by-normal-faults"
        },
        {
          "row_index": 118,
          "witness_key": "rel:rc1-bounded-by-detachment"
        },
        {
          "row_index": 119,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 120,
          "witness_key": "rel:rc2-bounded-by-inward-faults"
        },
        {
          "row_index": 121,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 122,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 123,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 124,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 125,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 126,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 127,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 128,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 129,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 130,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 131,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 132,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 133,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 134,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 135,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 136,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 137,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 138,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 139,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 140,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 141,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 142,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 143,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 144,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 145,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 146,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 147,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 148,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 149,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 150,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 151,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 152,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 153,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 154,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 155,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 156,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 157,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 158,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 159,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 160,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 161,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 162,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 163,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 164,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 165,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 166,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 167,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 168,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 169,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 170,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 171,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 172,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 173,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 174,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 175,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 176,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 177,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 178,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 179,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 180,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 181,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 182,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 183,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 184,
          "witness_key": "claim:seafloor-basalts-degassed"
        }
      ]
    },
    {
      "question_id": "CQ-T2-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The two programs and their order come out of the rows. The catalogue they act on does not: the graph carries it, and this question's type set reaches neither the source record nor the count records that stand for it.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "initial_location_method",
          "row_index": 9,
          "absent_reason": null,
          "note": "the package record says it produced the first hypocentres"
        },
        {
          "semantic": "relocation_method",
          "row_index": 8,
          "absent_reason": null,
          "note": "the package record says it was used for the relocation"
        },
        {
          "semantic": "method_sequence",
          "row_index": 9,
          "absent_reason": null,
          "note": "the ordering is carried by the two descriptions, one calling its output the initial locations and the other calling its work relocation; no relation states the sequence"
        },
        {
          "semantic": "earthquake_catalog",
          "row_index": null,
          "absent_reason": "UNREACHED_RECORD",
          "note": "records for the catalogue exist and are returned to other questions, but this question's types reach neither the deposit nor the counts of located and relocated events"
        }
      ],
      "source_locators": [
        "page:7:block:004",
        "page:8:block:010",
        "page:7:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 1,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 2,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 3,
          "witness_key": "method:refraction-profile"
        },
        {
          "row_index": 4,
          "witness_key": "method:sta-lta"
        },
        {
          "row_index": 5,
          "witness_key": "software:global-mapper"
        },
        {
          "row_index": 6,
          "witness_key": "software:gmt"
        },
        {
          "row_index": 7,
          "witness_key": "software:hash"
        },
        {
          "row_index": 8,
          "witness_key": "software:hypodd"
        },
        {
          "row_index": 9,
          "witness_key": "software:nonlinloc"
        },
        {
          "row_index": 10,
          "witness_key": "software:seisan"
        },
        {
          "row_index": 11,
          "witness_key": "software:velest"
        },
        {
          "row_index": 12,
          "witness_key": "software:zmap"
        },
        {
          "row_index": 13,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 14,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 15,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 16,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 17,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 18,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 19,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 20,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 21,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 22,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 23,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 24,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 25,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 26,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 27,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 28,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 29,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 30,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 31,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 32,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 33,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 34,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 35,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 36,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 37,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 38,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 39,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 40,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 41,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 42,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 43,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 44,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 45,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 46,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 47,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 48,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 49,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 50,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 51,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 52,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 53,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 54,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 55,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 56,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 57,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 58,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 59,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 60,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 61,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 62,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 63,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 64,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 65,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 66,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 67,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 68,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 69,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 70,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 71,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 72,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 73,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 74,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 75,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 76,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 77,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 78,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 79,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 80,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 81,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 82,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 83,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 84,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 85,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 86,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 87,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 88,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 89,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 90,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 91,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 92,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 93,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 94,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 95,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 96,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 97,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 98,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 99,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 100,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 101,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 102,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 103,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 104,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 105,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 106,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 107,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 108,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 109,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 110,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 111,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 112,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 113,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 114,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 115,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 116,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 117,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 118,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 119,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 120,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 121,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 122,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 123,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 124,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 125,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 126,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 127,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 128,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 129,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 130,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 131,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 132,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 133,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 134,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 135,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 136,
          "witness_key": "claim:zero-position-is-rti"
        }
      ]
    },
    {
      "question_id": "CQ-T2-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The three things are each named and nothing ties them together. The sentence that places the vent field on the flank of the discontinuity and far from the axis was captured, but it produced a feature record with a name and a kind only, so the placement survives as words behind a digest.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "named_feature",
          "row_index": 6,
          "absent_reason": null,
          "note": "the feature record names the extinct field"
        },
        {
          "semantic": "host_discontinuity",
          "row_index": 20,
          "absent_reason": null,
          "note": "the discontinuity is returned as its own record"
        },
        {
          "semantic": "spatial_relation",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "the flank it sits on and its distance from the present axis are in the block the feature record points at, and the graph keeps them only as that locator and digest"
        },
        {
          "semantic": "present_day_axis",
          "row_index": 2,
          "absent_reason": null,
          "note": "the axial valley is returned as its own record"
        }
      ],
      "source_locators": [
        "page:3:block:002",
        "page:1:block:005",
        "page:2:block:001",
        "page:4:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:ascending-melt"
        },
        {
          "row_index": 1,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 4,
          "witness_key": "feature:detachment-fault-rti"
        },
        {
          "row_index": 5,
          "witness_key": "feature:equatorial-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 9,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 10,
          "witness_key": "feature:inactive-hydrothermal-mound"
        },
        {
          "row_index": 11,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 12,
          "witness_key": "feature:knipovich-ridge"
        },
        {
          "row_index": 13,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "feature:logachev-seamount"
        },
        {
          "row_index": 15,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 16,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mylonite-shear-zones"
        },
        {
          "row_index": 20,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 21,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 22,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd2-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 25,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 26,
          "witness_key": "feature:occ-normal-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 28,
          "witness_key": "feature:pre-eruptive-melt"
        },
        {
          "row_index": 29,
          "witness_key": "feature:primary-melt"
        },
        {
          "row_index": 30,
          "witness_key": "feature:rainbow-massif"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2-inward-dipping-faults"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-median-valley"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 39,
          "witness_key": "feature:sedimentary-layers"
        },
        {
          "row_index": 40,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 41,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 42,
          "witness_key": "feature:western-indian-ocean"
        },
        {
          "row_index": 43,
          "witness_key": "feature:western-ridge-flank"
        },
        {
          "row_index": 44,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 45,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 46,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 47,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 48,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 49,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 50,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 51,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 52,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 53,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 54,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 55,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 56,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 57,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 58,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 59,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 60,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 61,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 62,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 63,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 64,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 65,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 66,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 67,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 68,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 69,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 70,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 71,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 72,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 73,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 74,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 75,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 76,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 77,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 78,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 79,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 80,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 81,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 82,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 83,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 84,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 85,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 86,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 87,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 88,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 89,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 90,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 91,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 92,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 93,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 94,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 95,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 96,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 97,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 98,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 99,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 100,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 101,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 102,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 103,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 104,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 116,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 117,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 118,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 119,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 120,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 121,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 122,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 123,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 124,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 125,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 126,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 128,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 129,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 130,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 131,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 132,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 133,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 134,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 135,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 136,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 137,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 138,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 139,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 140,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 141,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 142,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 143,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 144,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 145,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 146,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 147,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 148,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 149,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 150,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 151,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 152,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 153,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 154,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 155,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 156,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 157,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 158,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 159,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 160,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 161,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 162,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 163,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 164,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 165,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 166,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 167,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 168,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 169,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 170,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 171,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 172,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 173,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 174,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 175,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 176,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 177,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 178,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 179,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 180,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 181,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 182,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 183,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 184,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 185,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 186,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 187,
          "witness_key": "rel:corrugated-surface-part-of-occ"
        },
        {
          "row_index": 188,
          "witness_key": "rel:mar-within-equatorial-atlantic"
        },
        {
          "row_index": 189,
          "witness_key": "rel:ntd2-faults-within"
        },
        {
          "row_index": 190,
          "witness_key": "rel:occ-cut-by-normal-faults"
        },
        {
          "row_index": 191,
          "witness_key": "rel:rc1-bounded-by-detachment"
        },
        {
          "row_index": 192,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 193,
          "witness_key": "rel:rc2-bounded-by-inward-faults"
        },
        {
          "row_index": 194,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 195,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 196,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 197,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 198,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 199,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 200,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 201,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 202,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 203,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 204,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 205,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 206,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 207,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 208,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 209,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 210,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 211,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 212,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 213,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 214,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 215,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 216,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 217,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 218,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 219,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 220,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 221,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 222,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 223,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 224,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 225,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 226,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 227,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 229,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 230,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 231,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 232,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 233,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 234,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 235,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 236,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 237,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 238,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 239,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 240,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 241,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 242,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 243,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 244,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 245,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 246,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 247,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 248,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 249,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 250,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 251,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 252,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 253,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 254,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 255,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 256,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 257,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 258,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 259,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 260,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 261,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 262,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 263,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 264,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 265,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 266,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 267,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 268,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 269,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 270,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 271,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 272,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 273,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 274,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 275,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 276,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 277,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 278,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 279,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 280,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 281,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 282,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 283,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 284,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 285,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 286,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 287,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 288,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 289,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 290,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 291,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 292,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 293,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 294,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 295,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 296,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 297,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 298,
          "witness_key": "obs:volatile-melting-initiation-depth"
        },
        {
          "row_index": 299,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 300,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 301,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 302,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 303,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 304,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 305,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 306,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 307,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 308,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 309,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 310,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 311,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 312,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 313,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 314,
          "witness_key": "obs:lab-water-content"
        }
      ]
    },
    {
      "question_id": "CQ-T2-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The flank and the age are in one row and the study is in another, with nothing joining them. The thickness itself is the one thing this question cannot reach, because the observation records that carry it are of a type this question's cases do not open.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "source_study",
          "row_index": 75,
          "absent_reason": null,
          "note": "the reference record is the earlier study the thickness is taken from; nothing in the result links it to the thickness"
        },
        {
          "semantic": "crustal_thickness_claim",
          "row_index": null,
          "absent_reason": "UNREACHED_RECORD",
          "note": "the thickness is carried by observation records that other questions return; this question's types do not include them"
        },
        {
          "semantic": "location_relation",
          "row_index": 43,
          "absent_reason": null,
          "note": "the flank record's description says the measured crust is that flank's"
        },
        {
          "semantic": "crustal_age",
          "row_index": 43,
          "absent_reason": null,
          "note": "the same description carries the age of that crust"
        }
      ],
      "source_locators": [
        "page:9:block:036",
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:ascending-melt"
        },
        {
          "row_index": 1,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 4,
          "witness_key": "feature:detachment-fault-rti"
        },
        {
          "row_index": 5,
          "witness_key": "feature:equatorial-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 9,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 10,
          "witness_key": "feature:inactive-hydrothermal-mound"
        },
        {
          "row_index": 11,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 12,
          "witness_key": "feature:knipovich-ridge"
        },
        {
          "row_index": 13,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "feature:logachev-seamount"
        },
        {
          "row_index": 15,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 16,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mylonite-shear-zones"
        },
        {
          "row_index": 20,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 21,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 22,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd2-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 25,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 26,
          "witness_key": "feature:occ-normal-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 28,
          "witness_key": "feature:pre-eruptive-melt"
        },
        {
          "row_index": 29,
          "witness_key": "feature:primary-melt"
        },
        {
          "row_index": 30,
          "witness_key": "feature:rainbow-massif"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2-inward-dipping-faults"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-median-valley"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 39,
          "witness_key": "feature:sedimentary-layers"
        },
        {
          "row_index": 40,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 41,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 42,
          "witness_key": "feature:western-indian-ocean"
        },
        {
          "row_index": 43,
          "witness_key": "feature:western-ridge-flank"
        },
        {
          "row_index": 44,
          "witness_key": "ref:001"
        },
        {
          "row_index": 45,
          "witness_key": "ref:002"
        },
        {
          "row_index": 46,
          "witness_key": "ref:003"
        },
        {
          "row_index": 47,
          "witness_key": "ref:004"
        },
        {
          "row_index": 48,
          "witness_key": "ref:005"
        },
        {
          "row_index": 49,
          "witness_key": "ref:006"
        },
        {
          "row_index": 50,
          "witness_key": "ref:007"
        },
        {
          "row_index": 51,
          "witness_key": "ref:008"
        },
        {
          "row_index": 52,
          "witness_key": "ref:009"
        },
        {
          "row_index": 53,
          "witness_key": "ref:010"
        },
        {
          "row_index": 54,
          "witness_key": "ref:011"
        },
        {
          "row_index": 55,
          "witness_key": "ref:012"
        },
        {
          "row_index": 56,
          "witness_key": "ref:013"
        },
        {
          "row_index": 57,
          "witness_key": "ref:014"
        },
        {
          "row_index": 58,
          "witness_key": "ref:015"
        },
        {
          "row_index": 59,
          "witness_key": "ref:016"
        },
        {
          "row_index": 60,
          "witness_key": "ref:017"
        },
        {
          "row_index": 61,
          "witness_key": "ref:018"
        },
        {
          "row_index": 62,
          "witness_key": "ref:019"
        },
        {
          "row_index": 63,
          "witness_key": "ref:020"
        },
        {
          "row_index": 64,
          "witness_key": "ref:021"
        },
        {
          "row_index": 65,
          "witness_key": "ref:022"
        },
        {
          "row_index": 66,
          "witness_key": "ref:023"
        },
        {
          "row_index": 67,
          "witness_key": "ref:024"
        },
        {
          "row_index": 68,
          "witness_key": "ref:025"
        },
        {
          "row_index": 69,
          "witness_key": "ref:026"
        },
        {
          "row_index": 70,
          "witness_key": "ref:027"
        },
        {
          "row_index": 71,
          "witness_key": "ref:028"
        },
        {
          "row_index": 72,
          "witness_key": "ref:029"
        },
        {
          "row_index": 73,
          "witness_key": "ref:030"
        },
        {
          "row_index": 74,
          "witness_key": "ref:031"
        },
        {
          "row_index": 75,
          "witness_key": "ref:032"
        },
        {
          "row_index": 76,
          "witness_key": "ref:033"
        },
        {
          "row_index": 77,
          "witness_key": "ref:034"
        },
        {
          "row_index": 78,
          "witness_key": "ref:035"
        },
        {
          "row_index": 79,
          "witness_key": "ref:036"
        },
        {
          "row_index": 80,
          "witness_key": "ref:037"
        },
        {
          "row_index": 81,
          "witness_key": "ref:038"
        },
        {
          "row_index": 82,
          "witness_key": "ref:039"
        },
        {
          "row_index": 83,
          "witness_key": "ref:040"
        },
        {
          "row_index": 84,
          "witness_key": "ref:041"
        },
        {
          "row_index": 85,
          "witness_key": "ref:042"
        },
        {
          "row_index": 86,
          "witness_key": "ref:043"
        },
        {
          "row_index": 87,
          "witness_key": "ref:044"
        },
        {
          "row_index": 88,
          "witness_key": "ref:045"
        },
        {
          "row_index": 89,
          "witness_key": "ref:046"
        },
        {
          "row_index": 90,
          "witness_key": "ref:047"
        },
        {
          "row_index": 91,
          "witness_key": "ref:048"
        },
        {
          "row_index": 92,
          "witness_key": "ref:049"
        },
        {
          "row_index": 93,
          "witness_key": "ref:050"
        },
        {
          "row_index": 94,
          "witness_key": "ref:051"
        },
        {
          "row_index": 95,
          "witness_key": "ref:052"
        },
        {
          "row_index": 96,
          "witness_key": "ref:053"
        },
        {
          "row_index": 97,
          "witness_key": "ref:054"
        },
        {
          "row_index": 98,
          "witness_key": "ref:055"
        },
        {
          "row_index": 99,
          "witness_key": "ref:056"
        },
        {
          "row_index": 100,
          "witness_key": "ref:057"
        },
        {
          "row_index": 101,
          "witness_key": "ref:058"
        },
        {
          "row_index": 102,
          "witness_key": "ref:059"
        },
        {
          "row_index": 103,
          "witness_key": "ref:060"
        },
        {
          "row_index": 104,
          "witness_key": "ref:061"
        },
        {
          "row_index": 105,
          "witness_key": "ref:062"
        },
        {
          "row_index": 106,
          "witness_key": "ref:063"
        },
        {
          "row_index": 107,
          "witness_key": "ref:064"
        },
        {
          "row_index": 108,
          "witness_key": "ref:065"
        },
        {
          "row_index": 109,
          "witness_key": "ref:066"
        },
        {
          "row_index": 110,
          "witness_key": "ref:067"
        },
        {
          "row_index": 111,
          "witness_key": "ref:068"
        },
        {
          "row_index": 112,
          "witness_key": "ref:069"
        },
        {
          "row_index": 113,
          "witness_key": "ref:070"
        },
        {
          "row_index": 114,
          "witness_key": "ref:071"
        },
        {
          "row_index": 115,
          "witness_key": "ref:072"
        },
        {
          "row_index": 116,
          "witness_key": "ref:073"
        },
        {
          "row_index": 117,
          "witness_key": "ref:074"
        },
        {
          "row_index": 118,
          "witness_key": "ref:075"
        },
        {
          "row_index": 119,
          "witness_key": "ref:076"
        },
        {
          "row_index": 120,
          "witness_key": "ref:077"
        },
        {
          "row_index": 121,
          "witness_key": "ref:078"
        },
        {
          "row_index": 122,
          "witness_key": "ref:079"
        },
        {
          "row_index": 123,
          "witness_key": "source:article:yu-2025"
        },
        {
          "row_index": 124,
          "witness_key": "source:cc-licence"
        },
        {
          "row_index": 125,
          "witness_key": "source:cruise-website"
        },
        {
          "row_index": 126,
          "witness_key": "source:petdb"
        },
        {
          "row_index": 127,
          "witness_key": "source:supplementary"
        },
        {
          "row_index": 128,
          "witness_key": "source:zenodo-catalog"
        },
        {
          "row_index": 129,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 130,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 131,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 132,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 133,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 134,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 135,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 136,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 137,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 138,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 139,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 140,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 141,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 142,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 143,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 144,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 145,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 146,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 147,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 148,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 149,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 150,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 151,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 152,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 153,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 154,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 155,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 156,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 157,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 158,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 159,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 160,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 161,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 162,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 163,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 164,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 165,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 166,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 167,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 168,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 169,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 170,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 171,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 172,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 173,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 174,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 175,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 176,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 177,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 178,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 179,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 180,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 181,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 182,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 183,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 184,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 185,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 186,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 187,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 188,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 189,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 190,
          "witness_key": "rel:corrugated-surface-part-of-occ"
        },
        {
          "row_index": 191,
          "witness_key": "rel:mar-within-equatorial-atlantic"
        },
        {
          "row_index": 192,
          "witness_key": "rel:ntd2-faults-within"
        },
        {
          "row_index": 193,
          "witness_key": "rel:occ-cut-by-normal-faults"
        },
        {
          "row_index": 194,
          "witness_key": "rel:rc1-bounded-by-detachment"
        },
        {
          "row_index": 195,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 196,
          "witness_key": "rel:rc2-bounded-by-inward-faults"
        },
        {
          "row_index": 197,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 198,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 199,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 200,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 201,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 202,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 203,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 204,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 205,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 206,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 207,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 208,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 209,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 210,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 211,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 212,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 213,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 214,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 215,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 216,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 217,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 218,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 219,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 220,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 221,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 222,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 223,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 224,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 225,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 226,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 227,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 228,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 229,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 230,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 231,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 232,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 233,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 234,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 235,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 236,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 237,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 238,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 239,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 240,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 241,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 242,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 243,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 244,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 245,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 246,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 247,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 248,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 249,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 250,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 251,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 252,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 253,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 254,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 255,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 256,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 257,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 258,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 259,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 260,
          "witness_key": "claim:seafloor-basalts-degassed"
        }
      ]
    },
    {
      "question_id": "CQ-T2-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "This is the one question whose answer is a single relation with both of its endpoints in the result, so the grant, the funder and the person can be read as one connected thing.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "funding_record",
          "row_index": 20,
          "absent_reason": null,
          "note": "the credit relation is the funding record, with funder and recipient as its endpoints"
        },
        {
          "semantic": "grant_identifier",
          "row_index": 20,
          "absent_reason": null,
          "note": "the same row carries the award identifier"
        },
        {
          "semantic": "person",
          "row_index": 14,
          "absent_reason": null,
          "note": "the recipient is returned as an agent record"
        },
        {
          "semantic": "attribution_relation",
          "row_index": 20,
          "absent_reason": null,
          "note": "the relation type is the attribution"
        }
      ],
      "source_locators": [
        "page:10:block:044",
        "page:11:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "agent:anne-briais"
        },
        {
          "row_index": 1,
          "witness_key": "agent:brittany"
        },
        {
          "row_index": 2,
          "witness_key": "agent:cedric-hamelin"
        },
        {
          "row_index": 3,
          "witness_key": "agent:cnr-igag"
        },
        {
          "row_index": 4,
          "witness_key": "agent:daniele-brunelli"
        },
        {
          "row_index": 5,
          "witness_key": "agent:erc"
        },
        {
          "row_index": 6,
          "witness_key": "agent:french-fleet"
        },
        {
          "row_index": 7,
          "witness_key": "agent:geo-ocean"
        },
        {
          "row_index": 8,
          "witness_key": "agent:ipgp"
        },
        {
          "row_index": 9,
          "witness_key": "agent:isblue"
        },
        {
          "row_index": 10,
          "witness_key": "agent:lea-grenet"
        },
        {
          "row_index": 11,
          "witness_key": "agent:lorenzo-petracchini"
        },
        {
          "row_index": 12,
          "witness_key": "agent:marcia-maia"
        },
        {
          "row_index": 13,
          "witness_key": "agent:nsfc"
        },
        {
          "row_index": 14,
          "witness_key": "agent:satish-singh"
        },
        {
          "row_index": 15,
          "witness_key": "agent:sio"
        },
        {
          "row_index": 16,
          "witness_key": "agent:springer-nature"
        },
        {
          "row_index": 17,
          "witness_key": "agent:univ-modena"
        },
        {
          "row_index": 18,
          "witness_key": "agent:zhiteng-yu"
        },
        {
          "row_index": 19,
          "witness_key": "agent:zjnsf"
        },
        {
          "row_index": 20,
          "witness_key": "credit:erc-transatlanticilab"
        },
        {
          "row_index": 21,
          "witness_key": "credit:nsfc-42330308"
        },
        {
          "row_index": 22,
          "witness_key": "credit:nsfc-42422603"
        },
        {
          "row_index": 23,
          "witness_key": "credit:zjnsf"
        }
      ]
    },
    {
      "question_id": "CQ-T3-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Everything is present. Four items come from one observation and the fifth from a second observation of the same depths, and the two are joined by pointing at the same subject record, which the result also returns.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 269,
          "absent_reason": null,
          "note": "the observation carries the depth bounds"
        },
        {
          "semantic": "length_unit",
          "row_index": 269,
          "absent_reason": null,
          "note": "and its unit"
        },
        {
          "semantic": "quantity_subject",
          "row_index": 269,
          "absent_reason": null,
          "note": "its subject reference resolves to the ridge record the depths are beneath"
        },
        {
          "semantic": "measurement_status",
          "row_index": 268,
          "absent_reason": null,
          "note": "a second observation of the same depths carries the slot saying they were measured here"
        },
        {
          "semantic": "depth_reference_surface",
          "row_index": 269,
          "absent_reason": null,
          "note": "the quantity is named as a depth below the sea floor"
        }
      ],
      "source_locators": [
        "page:7:block:012",
        "page:1:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:ascending-melt"
        },
        {
          "row_index": 1,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 4,
          "witness_key": "feature:detachment-fault-rti"
        },
        {
          "row_index": 5,
          "witness_key": "feature:equatorial-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 9,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 10,
          "witness_key": "feature:inactive-hydrothermal-mound"
        },
        {
          "row_index": 11,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 12,
          "witness_key": "feature:knipovich-ridge"
        },
        {
          "row_index": 13,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "feature:logachev-seamount"
        },
        {
          "row_index": 15,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 16,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mylonite-shear-zones"
        },
        {
          "row_index": 20,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 21,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 22,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd2-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 25,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 26,
          "witness_key": "feature:occ-normal-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 28,
          "witness_key": "feature:pre-eruptive-melt"
        },
        {
          "row_index": 29,
          "witness_key": "feature:primary-melt"
        },
        {
          "row_index": 30,
          "witness_key": "feature:rainbow-massif"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2-inward-dipping-faults"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-median-valley"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 39,
          "witness_key": "feature:sedimentary-layers"
        },
        {
          "row_index": 40,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 41,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 42,
          "witness_key": "feature:western-indian-ocean"
        },
        {
          "row_index": 43,
          "witness_key": "feature:western-ridge-flank"
        },
        {
          "row_index": 44,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 45,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 46,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 47,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 48,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 49,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 50,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 51,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 52,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 53,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 54,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 55,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 56,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 57,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 58,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 59,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 60,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 61,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 62,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 63,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 64,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 65,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 66,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 67,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 68,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 69,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 70,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 71,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 72,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 73,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 74,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 75,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 76,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 77,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 78,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 79,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 80,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 81,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 82,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 83,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 84,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 85,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 87,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 88,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 89,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 90,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 91,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 92,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 93,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 94,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 95,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 96,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 97,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 98,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 99,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 100,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 101,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 102,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 103,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 104,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 105,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 116,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 117,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 118,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 119,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 120,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 121,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 122,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 123,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 124,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 125,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 126,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 128,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 129,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 130,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 131,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 132,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 133,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 134,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 135,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 136,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 137,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 138,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 139,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 140,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 141,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 142,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 143,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 144,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 145,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 146,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 147,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 148,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 149,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 150,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 151,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 152,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 153,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 155,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 156,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 157,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 158,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 159,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 160,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 161,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 162,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 163,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 164,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 165,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 166,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 167,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 168,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 169,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 170,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 171,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 172,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 173,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 174,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 175,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 176,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 177,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 178,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 179,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 180,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 181,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 182,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 183,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 184,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 185,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 186,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 187,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 188,
          "witness_key": "rel:corrugated-surface-part-of-occ"
        },
        {
          "row_index": 189,
          "witness_key": "rel:mar-within-equatorial-atlantic"
        },
        {
          "row_index": 190,
          "witness_key": "rel:ntd2-faults-within"
        },
        {
          "row_index": 191,
          "witness_key": "rel:occ-cut-by-normal-faults"
        },
        {
          "row_index": 192,
          "witness_key": "rel:rc1-bounded-by-detachment"
        },
        {
          "row_index": 193,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 194,
          "witness_key": "rel:rc2-bounded-by-inward-faults"
        },
        {
          "row_index": 195,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 196,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 197,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 198,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 199,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 200,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 201,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 202,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 203,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 204,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 205,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 206,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 207,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 208,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 209,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 210,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 211,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 212,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 213,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 214,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 215,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 216,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 217,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 218,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 219,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 220,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 221,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 222,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 223,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 224,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 225,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 226,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 227,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 228,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 229,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 230,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 231,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 232,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 233,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 234,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 235,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 236,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 237,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 238,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 239,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 240,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 241,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 242,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 243,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 244,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 245,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 246,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 247,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 248,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 249,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 250,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 251,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 252,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 253,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 254,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 255,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 256,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 257,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 258,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 259,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 260,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 261,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 262,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 263,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 264,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 265,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 266,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 267,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 268,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 269,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 270,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 271,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 272,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 273,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 274,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 275,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 276,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 277,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 278,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 279,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 280,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 281,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 282,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 283,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 284,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 285,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 286,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 287,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 288,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 289,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 290,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 291,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 292,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 293,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 294,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 295,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 296,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 297,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 298,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 299,
          "witness_key": "obs:volatile-melting-initiation-depth"
        },
        {
          "row_index": 300,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 301,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 302,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 303,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 304,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 305,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 306,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 307,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 308,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 309,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 310,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 311,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 312,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 313,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 314,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 315,
          "witness_key": "obs:lab-water-content"
        }
      ]
    },
    {
      "question_id": "CQ-T3-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One row answers the whole question: the content, its unit, the segment it belongs to and how it was arrived at are all slots of the same observation.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 270,
          "absent_reason": null,
          "note": "the observation carries both bounds"
        },
        {
          "semantic": "concentration_unit",
          "row_index": 270,
          "absent_reason": null,
          "note": "and the unit"
        },
        {
          "semantic": "quantity_subject",
          "row_index": 270,
          "absent_reason": null,
          "note": "its subject reference resolves to the segment"
        },
        {
          "semantic": "calculated_or_measured_status",
          "row_index": 270,
          "absent_reason": null,
          "note": "and it records that the value was estimated rather than measured"
        }
      ],
      "source_locators": [
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:ascending-melt"
        },
        {
          "row_index": 1,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 4,
          "witness_key": "feature:detachment-fault-rti"
        },
        {
          "row_index": 5,
          "witness_key": "feature:equatorial-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 9,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 10,
          "witness_key": "feature:inactive-hydrothermal-mound"
        },
        {
          "row_index": 11,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 12,
          "witness_key": "feature:knipovich-ridge"
        },
        {
          "row_index": 13,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "feature:logachev-seamount"
        },
        {
          "row_index": 15,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 16,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mylonite-shear-zones"
        },
        {
          "row_index": 20,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 21,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 22,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd2-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 25,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 26,
          "witness_key": "feature:occ-normal-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 28,
          "witness_key": "feature:pre-eruptive-melt"
        },
        {
          "row_index": 29,
          "witness_key": "feature:primary-melt"
        },
        {
          "row_index": 30,
          "witness_key": "feature:rainbow-massif"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2-inward-dipping-faults"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-median-valley"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 39,
          "witness_key": "feature:sedimentary-layers"
        },
        {
          "row_index": 40,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 41,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 42,
          "witness_key": "feature:western-indian-ocean"
        },
        {
          "row_index": 43,
          "witness_key": "feature:western-ridge-flank"
        },
        {
          "row_index": 44,
          "witness_key": "sample:basaltic-rocks"
        },
        {
          "row_index": 45,
          "witness_key": "sample:basalts"
        },
        {
          "row_index": 46,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 47,
          "witness_key": "sample:morb"
        },
        {
          "row_index": 48,
          "witness_key": "sample:peridotites"
        },
        {
          "row_index": 49,
          "witness_key": "sample:pillow-basalts"
        },
        {
          "row_index": 50,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 51,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 53,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 55,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 56,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 57,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 58,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 61,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 62,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 63,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 64,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 65,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 66,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 67,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 68,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 69,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 71,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 72,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 73,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 74,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 75,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 76,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 77,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 78,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 79,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 80,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 81,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 82,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 83,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 84,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 85,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 86,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 87,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 88,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 89,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 90,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 91,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 92,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 93,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 94,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 95,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 96,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 97,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 98,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 99,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 100,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 101,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 102,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 103,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 104,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 105,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 106,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 107,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 108,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 109,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 110,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 111,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 116,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 117,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 118,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 119,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 120,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 121,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 122,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 123,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 124,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 125,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 126,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 127,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 128,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 129,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 130,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 131,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 132,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 133,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 134,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 135,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 136,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 137,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 138,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 139,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 140,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 141,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 142,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 143,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 144,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 145,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 146,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 147,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 148,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 149,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 150,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 151,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 152,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 153,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 156,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 157,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 158,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 159,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 160,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 161,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 162,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 163,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 164,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 165,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 166,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 167,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 168,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 169,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 170,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 171,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 172,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 173,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 174,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 175,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 176,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 177,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 178,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 179,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 180,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 181,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 182,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 183,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 184,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 185,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 186,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 187,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 188,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 189,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 190,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 191,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 192,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 193,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 194,
          "witness_key": "rel:corrugated-surface-part-of-occ"
        },
        {
          "row_index": 195,
          "witness_key": "rel:mar-within-equatorial-atlantic"
        },
        {
          "row_index": 196,
          "witness_key": "rel:ntd2-faults-within"
        },
        {
          "row_index": 197,
          "witness_key": "rel:occ-cut-by-normal-faults"
        },
        {
          "row_index": 198,
          "witness_key": "rel:rc1-bounded-by-detachment"
        },
        {
          "row_index": 199,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 200,
          "witness_key": "rel:rc2-bounded-by-inward-faults"
        },
        {
          "row_index": 201,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 202,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 203,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 204,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 205,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 206,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 207,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 208,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 209,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 210,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 211,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 212,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 213,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 214,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 215,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 216,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 217,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 218,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 219,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 220,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 221,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 222,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 223,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 224,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 225,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 226,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 227,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 229,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 230,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 231,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 232,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 233,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 234,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 235,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 236,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 237,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 238,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 239,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 240,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 241,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 242,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 243,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 244,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 245,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 246,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 247,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 248,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 249,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 250,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 251,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 252,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 253,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 254,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 255,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 256,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 257,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 258,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 259,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 260,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 261,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 262,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 263,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 264,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 265,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 266,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 267,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 268,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 269,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 270,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 271,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 272,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 273,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 274,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 275,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 276,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 277,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 278,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 279,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 280,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 281,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 282,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 283,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 284,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 285,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 286,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 287,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 288,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 289,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 290,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 291,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 292,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 293,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 294,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 295,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 296,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 297,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 298,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 299,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 300,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 301,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 302,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 303,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 304,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 305,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 306,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 307,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 308,
          "witness_key": "obs:volatile-melting-initiation-depth"
        },
        {
          "row_index": 309,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 310,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 311,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 312,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 313,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 314,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 315,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 316,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 317,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 318,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 319,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 320,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 321,
          "witness_key": "obs:lab-water-content"
        }
      ]
    },
    {
      "question_id": "CQ-T3-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One observation carries the range, the unit, the melt stage and the fact that it is an estimate, so nothing has to be assembled.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 298,
          "absent_reason": null,
          "note": "the observation carries the range"
        },
        {
          "semantic": "concentration_unit",
          "row_index": 298,
          "absent_reason": null,
          "note": "and the unit"
        },
        {
          "semantic": "melt_stage",
          "row_index": 298,
          "absent_reason": null,
          "note": "the quantity it names is the pre-eruptive one"
        },
        {
          "semantic": "estimation_status",
          "row_index": 298,
          "absent_reason": null,
          "note": "and it says the range was estimated"
        }
      ],
      "source_locators": [
        "page:5:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:ascending-melt"
        },
        {
          "row_index": 1,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 4,
          "witness_key": "feature:detachment-fault-rti"
        },
        {
          "row_index": 5,
          "witness_key": "feature:equatorial-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 9,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 10,
          "witness_key": "feature:inactive-hydrothermal-mound"
        },
        {
          "row_index": 11,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 12,
          "witness_key": "feature:knipovich-ridge"
        },
        {
          "row_index": 13,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "feature:logachev-seamount"
        },
        {
          "row_index": 15,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 16,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mylonite-shear-zones"
        },
        {
          "row_index": 20,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 21,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 22,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd2-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 25,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 26,
          "witness_key": "feature:occ-normal-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 28,
          "witness_key": "feature:pre-eruptive-melt"
        },
        {
          "row_index": 29,
          "witness_key": "feature:primary-melt"
        },
        {
          "row_index": 30,
          "witness_key": "feature:rainbow-massif"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2-inward-dipping-faults"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-median-valley"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 39,
          "witness_key": "feature:sedimentary-layers"
        },
        {
          "row_index": 40,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 41,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 42,
          "witness_key": "feature:western-indian-ocean"
        },
        {
          "row_index": 43,
          "witness_key": "feature:western-ridge-flank"
        },
        {
          "row_index": 44,
          "witness_key": "sample:basaltic-rocks"
        },
        {
          "row_index": 45,
          "witness_key": "sample:basalts"
        },
        {
          "row_index": 46,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 47,
          "witness_key": "sample:morb"
        },
        {
          "row_index": 48,
          "witness_key": "sample:peridotites"
        },
        {
          "row_index": 49,
          "witness_key": "sample:pillow-basalts"
        },
        {
          "row_index": 50,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 51,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 53,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 55,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 56,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 57,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 58,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 61,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 62,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 63,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 64,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 65,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 66,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 67,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 68,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 69,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 71,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 72,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 73,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 74,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 75,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 76,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 77,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 78,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 79,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 80,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 81,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 82,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 83,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 84,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 85,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 86,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 87,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 88,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 89,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 90,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 91,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 92,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 93,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 94,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 95,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 96,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 97,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 98,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 99,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 100,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 101,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 102,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 103,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 104,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 105,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 106,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 107,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 108,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 109,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 110,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 111,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 116,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 117,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 118,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 119,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 120,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 121,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 122,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 123,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 124,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 125,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 126,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 127,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 128,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 129,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 130,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 131,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 132,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 133,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 134,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 135,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 136,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 137,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 138,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 139,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 140,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 141,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 142,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 143,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 144,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 145,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 146,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 147,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 148,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 149,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 150,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 151,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 152,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 153,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 156,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 157,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 158,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 159,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 160,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 161,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 162,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 163,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 164,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 165,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 166,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 167,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 168,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 169,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 170,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 171,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 172,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 173,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 174,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 175,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 176,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 177,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 178,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 179,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 180,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 181,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 182,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 183,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 184,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 185,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 186,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 187,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 188,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 189,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 190,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 191,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 192,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 193,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 194,
          "witness_key": "rel:corrugated-surface-part-of-occ"
        },
        {
          "row_index": 195,
          "witness_key": "rel:mar-within-equatorial-atlantic"
        },
        {
          "row_index": 196,
          "witness_key": "rel:ntd2-faults-within"
        },
        {
          "row_index": 197,
          "witness_key": "rel:occ-cut-by-normal-faults"
        },
        {
          "row_index": 198,
          "witness_key": "rel:rc1-bounded-by-detachment"
        },
        {
          "row_index": 199,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 200,
          "witness_key": "rel:rc2-bounded-by-inward-faults"
        },
        {
          "row_index": 201,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 202,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 203,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 204,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 205,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 206,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 207,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 208,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 209,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 210,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 211,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 212,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 213,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 214,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 215,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 216,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 217,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 218,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 219,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 220,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 221,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 222,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 223,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 224,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 225,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 226,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 227,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 229,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 230,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 231,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 232,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 233,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 234,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 235,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 236,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 237,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 238,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 239,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 240,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 241,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 242,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 243,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 244,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 245,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 246,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 247,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 248,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 249,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 250,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 251,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 252,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 253,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 254,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 255,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 256,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 257,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 258,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 259,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 260,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 261,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 262,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 263,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 264,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 265,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 266,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 267,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 268,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 269,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 270,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 271,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 272,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 273,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 274,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 275,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 276,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 277,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 278,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 279,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 280,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 281,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 282,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 283,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 284,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 285,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 286,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 287,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 288,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 289,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 290,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 291,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 292,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 293,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 294,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 295,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 296,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 297,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 298,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 299,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 300,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 301,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 302,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 303,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 304,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 305,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 306,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 307,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 308,
          "witness_key": "obs:volatile-melting-initiation-depth"
        },
        {
          "row_index": 309,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 310,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 311,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 312,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 313,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 314,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 315,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 316,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 317,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 318,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 319,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 320,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 321,
          "witness_key": "obs:lab-water-content"
        }
      ]
    },
    {
      "question_id": "CQ-T3-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The uncertainty and the set of events it describes are both returned, in two rows that nothing in the result joins; the reader has to put them side by side.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 88,
          "absent_reason": null,
          "note": "the observation carries the value"
        },
        {
          "semantic": "length_unit",
          "row_index": 88,
          "absent_reason": null,
          "note": "and the unit"
        },
        {
          "semantic": "quantity_subject",
          "row_index": 88,
          "absent_reason": null,
          "note": "the quantity is named as the average uncertainty after relocation"
        },
        {
          "semantic": "derivation_status",
          "row_index": 88,
          "absent_reason": null,
          "note": "the row records that it was measured and that it follows relocation"
        },
        {
          "semantic": "event_set",
          "row_index": 86,
          "absent_reason": null,
          "note": "a count row names the relocated events that make up the final catalogue"
        }
      ],
      "source_locators": [
        "page:3:block:004",
        "page:7:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 1,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 2,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 3,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 4,
          "witness_key": "method:refraction-profile"
        },
        {
          "row_index": 5,
          "witness_key": "method:sta-lta"
        },
        {
          "row_index": 6,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 7,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 8,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 9,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 10,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 11,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 12,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 13,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 14,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 15,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 16,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 17,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 18,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 19,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 20,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 21,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 22,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 23,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 24,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 25,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 26,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 27,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 28,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 29,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 30,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 31,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 32,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 33,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 34,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 35,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 36,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 37,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 38,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 39,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 40,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 41,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 42,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 43,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 44,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 45,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 46,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 47,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 48,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 49,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 50,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 51,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 52,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 53,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 54,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 55,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 56,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 57,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 58,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 59,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 60,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 61,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 62,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 63,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 64,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 65,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 66,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 67,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 68,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 70,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 71,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 72,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 73,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 74,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 82,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 83,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 84,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 86,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 87,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 88,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 89,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 90,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 91,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 92,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 93,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 94,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 95,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 96,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 97,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 98,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 99,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 100,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 101,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 102,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 103,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 104,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 105,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 106,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 107,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 108,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 109,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 110,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 111,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 112,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 113,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 114,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 115,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 116,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 117,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 118,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 119,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 120,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 121,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 122,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 123,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 124,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 125,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 126,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 127,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 128,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 129,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 130,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 131,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 132,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 133,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 134,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 135,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 136,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 137,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 138,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 139,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 140,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 141,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 142,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 143,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 144,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 145,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 146,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 147,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 148,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 149,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 150,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 151,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 152,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 153,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 154,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 155,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 156,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 157,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 158,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 159,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 160,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 161,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 162,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 163,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 164,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 165,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 166,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 167,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 168,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 169,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 170,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 171,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 172,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 173,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 174,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 175,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 176,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 177,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 178,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 179,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 180,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 181,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 182,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 183,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 184,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 185,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 186,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 187,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 188,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 189,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 190,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 191,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 192,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 193,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 194,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 195,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 196,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 197,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 198,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 199,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 200,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 201,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 202,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 203,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 204,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 205,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 206,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 207,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 208,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 209,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 210,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 211,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 212,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 213,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 214,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 215,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 216,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 217,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 218,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 219,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 220,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 221,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 222,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 223,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 224,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 225,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 226,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 227,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 229,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 230,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 231,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 232,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 233,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 234,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 235,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 237,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 238,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 239,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 241,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 242,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 244,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 245,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 248,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 249,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 250,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 251,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 253,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 254,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 255,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 256,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 257,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 258,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 260,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 261,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 262,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 263,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 264,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 265,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 266,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 267,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 268,
          "witness_key": "obs:volatile-melting-initiation-depth"
        }
      ]
    },
    {
      "question_id": "CQ-T3-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Pressure and temperature come back as two separate observations, both saying they were modelled. Nothing in the result joins them, so the pair is only a pair to a reader who notices they describe the same condition.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 95,
          "absent_reason": null,
          "note": "the pressure observation carries the value"
        },
        {
          "semantic": "pressure_unit",
          "row_index": 95,
          "absent_reason": null,
          "note": "and its unit"
        },
        {
          "semantic": "temperature_unit",
          "row_index": 96,
          "absent_reason": null,
          "note": "the paired temperature observation carries the other unit"
        },
        {
          "semantic": "quantity_subject",
          "row_index": 95,
          "absent_reason": null,
          "note": "the quantity is named as the saturation condition of the melt"
        },
        {
          "semantic": "model_derived_status",
          "row_index": 95,
          "absent_reason": null,
          "note": "and the row records that it was modelled"
        }
      ],
      "source_locators": [
        "page:5:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 1,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 2,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 3,
          "witness_key": "method:refraction-profile"
        },
        {
          "row_index": 4,
          "witness_key": "method:sta-lta"
        },
        {
          "row_index": 5,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 6,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 7,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 8,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 9,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 10,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 11,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 12,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 13,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 14,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 15,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 16,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 17,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 18,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 19,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 20,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 21,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 22,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 23,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 24,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 25,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 26,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 27,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 28,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 29,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 30,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 31,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 32,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 33,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 34,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 35,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 36,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 37,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 38,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 39,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 40,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 41,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 42,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 43,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 44,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 45,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 46,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 47,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 48,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 49,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 50,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 51,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 52,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 53,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 54,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 55,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 56,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 57,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 58,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 59,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 60,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 61,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 62,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 63,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 64,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 65,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 66,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 67,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 68,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 70,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 71,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 72,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 73,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 74,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 82,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 83,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 84,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 86,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 87,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 88,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 89,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 90,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 91,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 92,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 93,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 94,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 95,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 96,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 97,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 98,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 99,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 100,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 101,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 102,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 103,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 104,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 105,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 106,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 107,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 108,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 109,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 110,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 111,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 112,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 113,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 114,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 115,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 116,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 117,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 118,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 119,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 120,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 121,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 122,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 123,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 124,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 125,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 126,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 127,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 128,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 129,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 130,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 131,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 132,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 133,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 134,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 135,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 136,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 137,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 138,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 139,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 140,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 141,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 142,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 143,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 144,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 145,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 146,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 147,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 148,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 149,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 150,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 151,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 152,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 153,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 154,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 155,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 156,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 157,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 158,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 159,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 160,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 161,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 162,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 163,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 164,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 165,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 166,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 167,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 168,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 169,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 170,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 171,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 172,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 173,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 174,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 175,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 176,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 177,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 178,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 179,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 180,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 181,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 182,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 183,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 184,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 185,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 186,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 187,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 188,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 189,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 190,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 191,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 192,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 193,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 194,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 195,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 196,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 197,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 198,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 199,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 200,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 201,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 202,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 203,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 204,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 205,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 206,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 207,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 208,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 209,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 210,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 212,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 213,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 214,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 215,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 216,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 217,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 218,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 219,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 220,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 221,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 222,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 223,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 224,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 225,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 226,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 227,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 228,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 229,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 230,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 231,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 232,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 233,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 234,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 235,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 238,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 239,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 240,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 241,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 242,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 244,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 248,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 249,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 250,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 253,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 254,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 255,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 256,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 257,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 260,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 261,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 262,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 263,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 264,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 265,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 266,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 267,
          "witness_key": "obs:volatile-melting-initiation-depth"
        }
      ]
    },
    {
      "question_id": "CQ-T4-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One claim row carries the explanation, the fact that it is the authors' preferred one, the strength it is stated with and what it is about. This is the shape the question asks for.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "causal_claim",
          "row_index": 76,
          "absent_reason": null,
          "note": "the claim states the mechanism"
        },
        {
          "semantic": "preferred_disposition",
          "row_index": 76,
          "absent_reason": null,
          "note": "and carries the slot marking it the preferred one"
        },
        {
          "semantic": "epistemic_modality",
          "row_index": 76,
          "absent_reason": null,
          "note": "and the modality it is asserted under"
        },
        {
          "semantic": "claim_subject",
          "row_index": 76,
          "absent_reason": null,
          "note": "and a subject reference for what it is about"
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 1,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 2,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 3,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 4,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 5,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 6,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 7,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 8,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 9,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 10,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 11,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 12,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 13,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 14,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 15,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 16,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 17,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 18,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 19,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 20,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 21,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 22,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 23,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 24,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 25,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 26,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 27,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 28,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 29,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 30,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 31,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 32,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 33,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 34,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 35,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 36,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 37,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 38,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 39,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 40,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 41,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 42,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 43,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 44,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 45,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 46,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 47,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 48,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 49,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 50,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 51,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 52,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 53,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 54,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 55,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 56,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 57,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 58,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 59,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 60,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 61,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 62,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 63,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 64,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 65,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 66,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 67,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 68,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 69,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 70,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 71,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 72,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 73,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 74,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 75,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 76,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 77,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 78,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 79,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 80,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 81,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 82,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 83,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 84,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 85,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 86,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 87,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 88,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 89,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 90,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 91,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 92,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 93,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 94,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 95,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 96,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 97,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 98,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 99,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 100,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 101,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 102,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 103,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 104,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 105,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 106,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 107,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 108,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 109,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 110,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 111,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 112,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 113,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 114,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 115,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 116,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 117,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 118,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 119,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 120,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 121,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 122,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 123,
          "witness_key": "claim:zero-position-is-rti"
        }
      ]
    },
    {
      "question_id": "CQ-T4-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The candidate and its rejection are one row; the ground is another, pointing at a different subject, and nothing in the result ties the two together.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "candidate_mechanism",
          "row_index": 90,
          "absent_reason": null,
          "note": "the claim states the candidate explanation, and its derivations reach both the block that raises it and the block that sets it aside"
        },
        {
          "semantic": "declined_disposition",
          "row_index": 90,
          "absent_reason": null,
          "note": "the same row carries the slot saying it is not supported"
        },
        {
          "semantic": "stated_ground",
          "row_index": 100,
          "absent_reason": null,
          "note": "a second claim carries the ground on which it is declined"
        },
        {
          "semantic": "claim_subject",
          "row_index": 90,
          "absent_reason": null,
          "note": "the candidate claim carries a subject reference"
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
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 1,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 2,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 3,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 4,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 5,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 6,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 7,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 8,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 9,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 10,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 11,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 12,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 13,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 14,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 15,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 16,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 17,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 18,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 19,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 20,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 21,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 22,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 23,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 24,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 25,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 26,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 27,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 28,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 29,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 30,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 31,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 32,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 33,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 34,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 35,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 36,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 37,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 38,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 39,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 40,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 41,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 42,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 43,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 44,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 45,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 46,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 47,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 48,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 49,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 50,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 51,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 52,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 53,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 54,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 55,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 56,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 57,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 58,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 59,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 60,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 61,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 62,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 63,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 64,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 65,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 66,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 67,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 68,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 69,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 70,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 71,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 72,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 73,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 74,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 75,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 76,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 77,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 78,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 79,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 80,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 81,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 82,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 83,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 84,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 85,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 86,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 87,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 88,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 89,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 90,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 91,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 92,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 93,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 94,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 95,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 96,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 97,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 98,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 99,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 100,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 101,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 102,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 103,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 104,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 105,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 106,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 107,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 108,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 109,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 110,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 111,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 112,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 113,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 114,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 115,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 116,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 117,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 118,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 119,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 120,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 121,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 122,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 123,
          "witness_key": "claim:zero-position-is-rti"
        }
      ]
    },
    {
      "question_id": "CQ-T4-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The caveat and the claim it qualifies are both returned, but only as two claims standing separately; the one that matters here has no subject, so the question's fourth item has nowhere to come from.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "qualified_claim",
          "row_index": 14,
          "absent_reason": null,
          "note": "the procedure claim is the one the caveat bears on, and it comes from the same block"
        },
        {
          "semantic": "stated_assumption",
          "row_index": 59,
          "absent_reason": null,
          "note": "the caveat claim states the assumption"
        },
        {
          "semantic": "caveat_disposition",
          "row_index": 59,
          "absent_reason": null,
          "note": "the same row types itself as a limitation"
        },
        {
          "semantic": "claim_subject",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "the caveat is carried by a claim record whose subject slot is empty, so no case can reach it through what it is about and no row carries its subject"
        }
      ],
      "source_locators": [
        "page:5:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 1,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 2,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 3,
          "witness_key": "method:refraction-profile"
        },
        {
          "row_index": 4,
          "witness_key": "method:sta-lta"
        },
        {
          "row_index": 5,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 6,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 7,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 8,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 9,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 10,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 11,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 12,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 13,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 14,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 15,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 16,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 17,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 18,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 19,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 20,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 21,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 22,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 23,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 24,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 25,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 26,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 27,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 28,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 29,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 30,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 31,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 32,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 33,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 34,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 35,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 36,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 37,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 38,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 39,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 40,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 41,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 42,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 43,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 44,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 45,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 46,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 47,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 48,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 49,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 50,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 51,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 52,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 53,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 54,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 55,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 56,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 57,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 58,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 59,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 60,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 61,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 62,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 63,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 64,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 65,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 66,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 67,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 68,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 69,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 70,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 71,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 72,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 73,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 74,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 75,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 76,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 77,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 78,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 79,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 80,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 81,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 82,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 83,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 84,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 85,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 86,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 87,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 88,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 89,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 90,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 91,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 92,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 93,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 94,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 95,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 96,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 97,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 98,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 99,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 100,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 101,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 102,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 103,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 104,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 105,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 106,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 107,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 108,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 109,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 110,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 111,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 112,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 113,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 114,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 115,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 116,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 117,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 118,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 119,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 120,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 121,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 122,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 123,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 124,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 125,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 126,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 127,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 128,
          "witness_key": "claim:zero-position-is-rti"
        }
      ]
    },
    {
      "question_id": "CQ-T4-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One row carries the statement, its negative sense, its subject and its scope, so the question is answered by a single record without assembly.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "existence_claim",
          "row_index": 225,
          "absent_reason": null,
          "note": "the claim states what the authors report about venting"
        },
        {
          "semantic": "negated_disposition",
          "row_index": 225,
          "absent_reason": null,
          "note": "and the modality slot records that it is an assertion of absence"
        },
        {
          "semantic": "claim_subject",
          "row_index": 225,
          "absent_reason": null,
          "note": "and it points at the segment"
        },
        {
          "semantic": "spatial_scope",
          "row_index": 225,
          "absent_reason": null,
          "note": "and the claim it names is scoped to that segment's axis"
        }
      ],
      "source_locators": [
        "page:3:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:ascending-melt"
        },
        {
          "row_index": 1,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 4,
          "witness_key": "feature:detachment-fault-rti"
        },
        {
          "row_index": 5,
          "witness_key": "feature:equatorial-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 9,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 10,
          "witness_key": "feature:inactive-hydrothermal-mound"
        },
        {
          "row_index": 11,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 12,
          "witness_key": "feature:knipovich-ridge"
        },
        {
          "row_index": 13,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "feature:logachev-seamount"
        },
        {
          "row_index": 15,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 16,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mylonite-shear-zones"
        },
        {
          "row_index": 20,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 21,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 22,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd2-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 25,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 26,
          "witness_key": "feature:occ-normal-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 28,
          "witness_key": "feature:pre-eruptive-melt"
        },
        {
          "row_index": 29,
          "witness_key": "feature:primary-melt"
        },
        {
          "row_index": 30,
          "witness_key": "feature:rainbow-massif"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2-inward-dipping-faults"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-median-valley"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 39,
          "witness_key": "feature:sedimentary-layers"
        },
        {
          "row_index": 40,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 41,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 42,
          "witness_key": "feature:western-indian-ocean"
        },
        {
          "row_index": 43,
          "witness_key": "feature:western-ridge-flank"
        },
        {
          "row_index": 44,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 45,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 46,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 47,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 48,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 49,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 50,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 51,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 52,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 53,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 54,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 55,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 56,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 57,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 58,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 59,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 60,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 61,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 62,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 63,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 64,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 65,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 66,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 67,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 68,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 69,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 70,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 71,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 72,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 73,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 74,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 75,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 76,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 77,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 78,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 79,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 80,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 81,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 82,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 83,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 84,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 85,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 86,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 87,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 88,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 89,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 90,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 91,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 92,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 93,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 94,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 95,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 96,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 97,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 98,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 99,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 100,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 101,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 102,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 103,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 104,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 116,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 117,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 118,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 119,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 120,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 121,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 122,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 123,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 124,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 125,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 126,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 128,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 129,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 130,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 131,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 132,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 133,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 134,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 135,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 136,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 137,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 138,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 139,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 140,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 141,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 142,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 143,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 144,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 145,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 146,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 147,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 148,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 149,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 150,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 151,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 152,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 153,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 154,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 155,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 156,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 157,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 158,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 159,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 160,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 161,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 162,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 163,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 164,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 165,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 166,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 167,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 168,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 169,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 170,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 171,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 172,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 173,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 174,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 175,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 176,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 177,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 178,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 179,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 180,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 181,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 182,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 183,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 184,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 185,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 186,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 187,
          "witness_key": "rel:corrugated-surface-part-of-occ"
        },
        {
          "row_index": 188,
          "witness_key": "rel:mar-within-equatorial-atlantic"
        },
        {
          "row_index": 189,
          "witness_key": "rel:ntd2-faults-within"
        },
        {
          "row_index": 190,
          "witness_key": "rel:occ-cut-by-normal-faults"
        },
        {
          "row_index": 191,
          "witness_key": "rel:rc1-bounded-by-detachment"
        },
        {
          "row_index": 192,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 193,
          "witness_key": "rel:rc2-bounded-by-inward-faults"
        },
        {
          "row_index": 194,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 195,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 196,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 197,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 198,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 199,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 200,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 201,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 202,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 203,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 204,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 205,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 206,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 207,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 208,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 209,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 210,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 211,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 212,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 213,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 214,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 215,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 216,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 217,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 218,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 219,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 220,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 221,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 222,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 223,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 224,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 225,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 226,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 227,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 229,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 230,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 231,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 232,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 233,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 234,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 235,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 236,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 237,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 238,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 239,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 240,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 241,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 242,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 243,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 244,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 245,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 246,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 247,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 248,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 249,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 250,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 251,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 252,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 253,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 254,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 255,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 256,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 257,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 258,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 259,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 260,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 261,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 262,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 263,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 264,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 265,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 266,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 267,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 268,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 269,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 270,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 271,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 272,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 273,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 274,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 275,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 276,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 277,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 278,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 279,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 280,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 281,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 282,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 283,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 284,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 285,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 286,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 287,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 288,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 289,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 290,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 291,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 292,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 293,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 294,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 295,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 296,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 297,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 298,
          "witness_key": "obs:volatile-melting-initiation-depth"
        },
        {
          "row_index": 299,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 300,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 301,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 302,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 303,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 304,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 305,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 306,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 307,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 308,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 309,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 310,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 311,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 312,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 313,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 314,
          "witness_key": "obs:lab-water-content"
        }
      ]
    },
    {
      "question_id": "CQ-T4-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The hedge and what would settle it are both returned, as two claims with nothing joining them. Both carry the qualification in their own slots rather than only in their wording.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "hedged_claim",
          "row_index": 34,
          "absent_reason": null,
          "note": "the claim carries the hedged statement"
        },
        {
          "semantic": "hypothesised_disposition",
          "row_index": 34,
          "absent_reason": null,
          "note": "its kind slot marks it a candidate consequence"
        },
        {
          "semantic": "epistemic_modality",
          "row_index": 34,
          "absent_reason": null,
          "note": "and its modality slot marks it hypothesised"
        },
        {
          "semantic": "stated_limitation",
          "row_index": 41,
          "absent_reason": null,
          "note": "a second claim carries what the authors say is still needed"
        }
      ],
      "source_locators": [
        "page:5:block:008"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 1,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 2,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 3,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 4,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 5,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 6,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 7,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 8,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 9,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 10,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 11,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 12,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 13,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 14,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 15,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 16,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 17,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 18,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 19,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 20,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 21,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 22,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 23,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 24,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 25,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 26,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 27,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 28,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 29,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 30,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 31,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 32,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 33,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 34,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 35,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 36,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 37,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 38,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 39,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 40,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 41,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 42,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 43,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 44,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 45,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 46,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 47,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 48,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 49,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 50,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 51,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 52,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 53,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 54,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 55,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 56,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 57,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 58,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 59,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 60,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 61,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 62,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 63,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 64,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 65,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 66,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 67,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 68,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 69,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 70,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 71,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 72,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 73,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 74,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 75,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 76,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 77,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 78,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 79,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 80,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 81,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 82,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 83,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 84,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 85,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 86,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 87,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 88,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 89,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 90,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 91,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 92,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 93,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 94,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 95,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 96,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 97,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 98,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 99,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 100,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 101,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 102,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 103,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 104,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 105,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 106,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 107,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 108,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 109,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 110,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 111,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 112,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 113,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 114,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 115,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 116,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 117,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 118,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 119,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 120,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 121,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 122,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 123,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 124,
          "witness_key": "claim:zero-position-is-rti"
        }
      ]
    },
    {
      "question_id": "CQ-T5-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All five items are returned. The tie between evidence and mechanism is carried inside the wording of a claim rather than as a relation or an evidence record, and none of the five rows is joined to any other by the result.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "causal_mechanism",
          "row_index": 159,
          "absent_reason": null,
          "note": "the claim states the mechanism"
        },
        {
          "semantic": "supporting_observation",
          "row_index": 231,
          "absent_reason": null,
          "note": "the observation of deep microseismicity beneath the segment is the observation brought to it"
        },
        {
          "semantic": "geochemical_evidence",
          "row_index": 215,
          "absent_reason": null,
          "note": "the calculated volatile content of the same segment"
        },
        {
          "semantic": "seismic_evidence",
          "row_index": 228,
          "absent_reason": null,
          "note": "the reported earthquake depths"
        },
        {
          "semantic": "evidence_relation",
          "row_index": 157,
          "absent_reason": null,
          "note": "a claim states the tie between the seismic observation and the degassing mechanism"
        }
      ],
      "source_locators": [
        "page:5:block:003",
        "page:2:block:004",
        "page:5:block:005",
        "page:1:block:001",
        "page:5:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 1,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 2,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 3,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 4,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 5,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 6,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 7,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 8,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 9,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 10,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 11,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 12,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 13,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 14,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 15,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 16,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 17,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 18,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 19,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 20,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 21,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 22,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 23,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 24,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 25,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 26,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 27,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 28,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 29,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 30,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 31,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 32,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 33,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 34,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 35,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 36,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 37,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 38,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 39,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 40,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 41,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 42,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 43,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 44,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 45,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 46,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 47,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 48,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 49,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 50,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 51,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 52,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 53,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 54,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 55,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 56,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 57,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 58,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 59,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 60,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 61,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 62,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 63,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 64,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 65,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 66,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 67,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 68,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 70,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 71,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 72,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 73,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 74,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 81,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 82,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 83,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 84,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 85,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 86,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 87,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 88,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 89,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 90,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 91,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 92,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 93,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 94,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 95,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 96,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 97,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 98,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 99,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 100,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 101,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 102,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 103,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 104,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 105,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 106,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 107,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 108,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 109,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 110,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 111,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 112,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 113,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 114,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 115,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 116,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 117,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 118,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 119,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 120,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 121,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 122,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 124,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 125,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 126,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 127,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 128,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 129,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 130,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 131,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 132,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 133,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 134,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 135,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 136,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 137,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 138,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 139,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 140,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 141,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 142,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 143,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 144,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 145,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 146,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 147,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 148,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 149,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 150,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 151,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 152,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 153,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 154,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 155,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 156,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 157,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 158,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 159,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 160,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 161,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 162,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 163,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 164,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 165,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 166,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 167,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 168,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 169,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 170,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 171,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 172,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 173,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 174,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 175,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 176,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 177,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 178,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 179,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 180,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 181,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 182,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 183,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 184,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 185,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 186,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 187,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 188,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 189,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 190,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 191,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 192,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 193,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 194,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 195,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 196,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 197,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 198,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 199,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 200,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 201,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 202,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 203,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 204,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 205,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 206,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 207,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 208,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 209,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 210,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 211,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 212,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 213,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 214,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 215,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 216,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 217,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 218,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 219,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 220,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 221,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 222,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 223,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 224,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 225,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 226,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 227,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 228,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 229,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 230,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 231,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 232,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 233,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 235,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 236,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 237,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 238,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 239,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 240,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 241,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 242,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 243,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 244,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 245,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 246,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 248,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 249,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 250,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 251,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 252,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 253,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 254,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 255,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 256,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 259,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 260,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 261,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 262,
          "witness_key": "obs:volatile-melting-initiation-depth"
        }
      ]
    },
    {
      "question_id": "CQ-T5-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Both segments' contents come back with their units and their subjects, and the comparison between them does not. The comparing words were captured and each produced one of the two observations, so what survives is two values a reader may compare, not the authors' comparison.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "comparison_relation",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "the sentences that call one segment enriched against the other and the other significantly lower are the statements these observations point at; the graph keeps the comparison only as those locators and digests"
        },
        {
          "semantic": "first_quantity_subject",
          "row_index": 264,
          "absent_reason": null,
          "note": "the observation points at the segment with the deep earthquakes"
        },
        {
          "semantic": "second_quantity_subject",
          "row_index": 265,
          "absent_reason": null,
          "note": "the paired observation points at the adjacent segment"
        },
        {
          "semantic": "bounded_quantity",
          "row_index": 264,
          "absent_reason": null,
          "note": "the first observation carries its bounds"
        },
        {
          "semantic": "concentration_unit",
          "row_index": 264,
          "absent_reason": null,
          "note": "and its unit"
        }
      ],
      "source_locators": [
        "page:5:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:ascending-melt"
        },
        {
          "row_index": 1,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 4,
          "witness_key": "feature:detachment-fault-rti"
        },
        {
          "row_index": 5,
          "witness_key": "feature:equatorial-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 9,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 10,
          "witness_key": "feature:inactive-hydrothermal-mound"
        },
        {
          "row_index": 11,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 12,
          "witness_key": "feature:knipovich-ridge"
        },
        {
          "row_index": 13,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "feature:logachev-seamount"
        },
        {
          "row_index": 15,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 16,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mylonite-shear-zones"
        },
        {
          "row_index": 20,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 21,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 22,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd2-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 25,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 26,
          "witness_key": "feature:occ-normal-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 28,
          "witness_key": "feature:pre-eruptive-melt"
        },
        {
          "row_index": 29,
          "witness_key": "feature:primary-melt"
        },
        {
          "row_index": 30,
          "witness_key": "feature:rainbow-massif"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2-inward-dipping-faults"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-median-valley"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 39,
          "witness_key": "feature:sedimentary-layers"
        },
        {
          "row_index": 40,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 41,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 42,
          "witness_key": "feature:western-indian-ocean"
        },
        {
          "row_index": 43,
          "witness_key": "feature:western-ridge-flank"
        },
        {
          "row_index": 44,
          "witness_key": "sample:basaltic-rocks"
        },
        {
          "row_index": 45,
          "witness_key": "sample:basalts"
        },
        {
          "row_index": 46,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 47,
          "witness_key": "sample:morb"
        },
        {
          "row_index": 48,
          "witness_key": "sample:peridotites"
        },
        {
          "row_index": 49,
          "witness_key": "sample:pillow-basalts"
        },
        {
          "row_index": 50,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 51,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 53,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 55,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 56,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 57,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 58,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 61,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 62,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 63,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 64,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 65,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 66,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 67,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 68,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 69,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 71,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 72,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 73,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 74,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 75,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 76,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 77,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 78,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 79,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 80,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 81,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 82,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 83,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 84,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 85,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 86,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 87,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 88,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 89,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 90,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 91,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 92,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 93,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 94,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 95,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 96,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 97,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 98,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 99,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 100,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 101,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 102,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 103,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 104,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 105,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 106,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 107,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 108,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 109,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 110,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 111,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 116,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 117,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 118,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 119,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 120,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 121,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 122,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 123,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 124,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 125,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 126,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 127,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 128,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 129,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 130,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 131,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 132,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 133,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 134,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 135,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 136,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 137,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 138,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 139,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 140,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 141,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 142,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 143,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 144,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 145,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 146,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 147,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 148,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 149,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 150,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 151,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 152,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 153,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 156,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 157,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 158,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 159,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 160,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 161,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 162,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 163,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 164,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 165,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 166,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 167,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 168,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 169,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 170,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 171,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 172,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 173,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 174,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 175,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 176,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 177,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 178,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 179,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 180,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 181,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 182,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 183,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 184,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 185,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 186,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 187,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 188,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 189,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 190,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 191,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 192,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 193,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 194,
          "witness_key": "rel:corrugated-surface-part-of-occ"
        },
        {
          "row_index": 195,
          "witness_key": "rel:mar-within-equatorial-atlantic"
        },
        {
          "row_index": 196,
          "witness_key": "rel:ntd2-faults-within"
        },
        {
          "row_index": 197,
          "witness_key": "rel:occ-cut-by-normal-faults"
        },
        {
          "row_index": 198,
          "witness_key": "rel:rc1-bounded-by-detachment"
        },
        {
          "row_index": 199,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 200,
          "witness_key": "rel:rc2-bounded-by-inward-faults"
        },
        {
          "row_index": 201,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 202,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 203,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 204,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 205,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 206,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 207,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 208,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 209,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 210,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 211,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 212,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 213,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 214,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 215,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 216,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 217,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 218,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 219,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 220,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 221,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 222,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 223,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 224,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 225,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 226,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 227,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 229,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 230,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 231,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 232,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 233,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 234,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 235,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 236,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 237,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 238,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 239,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 240,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 241,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 242,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 243,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 244,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 245,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 246,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 247,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 248,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 249,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 250,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 251,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 252,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 253,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 254,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 255,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 256,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 257,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 258,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 259,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 260,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 261,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 262,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 263,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 264,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 265,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 266,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 267,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 268,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 269,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 270,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 271,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 272,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 273,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 274,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 275,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 276,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 277,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 278,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 279,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 280,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 281,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 282,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 283,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 284,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 285,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 286,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 287,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 288,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 289,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 290,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 291,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 292,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 293,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 294,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 295,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 296,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 297,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 298,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 299,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 300,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 301,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 302,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 303,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 304,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 305,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 306,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 307,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 308,
          "witness_key": "obs:volatile-melting-initiation-depth"
        },
        {
          "row_index": 309,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 310,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 311,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 312,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 313,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 314,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 315,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 316,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 317,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 318,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 319,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 320,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 321,
          "witness_key": "obs:lab-water-content"
        }
      ]
    },
    {
      "question_id": "CQ-T5-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The set, the observed depth, the expected depth and the statement that one departs from the other are all returned, in four rows nothing joins. Which subsections stay inside the expectation has to be read off the individual depth observations one at a time.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "subsection_set",
          "row_index": 70,
          "absent_reason": null,
          "note": "the scope claim names the subsections the study treats"
        },
        {
          "semantic": "maximum_depth_claim",
          "row_index": 270,
          "absent_reason": null,
          "note": "the observation of the deepest events beneath the magmatic segment"
        },
        {
          "semantic": "expected_depth_claim",
          "row_index": 145,
          "absent_reason": null,
          "note": "the observation of what depth is expected at this spreading rate"
        },
        {
          "semantic": "comparison_relation",
          "row_index": 223,
          "absent_reason": null,
          "note": "a claim states that the observed maximum does not follow the expected relation"
        }
      ],
      "source_locators": [
        "page:2:block:003",
        "page:2:block:006",
        "page:2:block:005",
        "page:2:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:ascending-melt"
        },
        {
          "row_index": 1,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 4,
          "witness_key": "feature:detachment-fault-rti"
        },
        {
          "row_index": 5,
          "witness_key": "feature:equatorial-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 9,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 10,
          "witness_key": "feature:inactive-hydrothermal-mound"
        },
        {
          "row_index": 11,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 12,
          "witness_key": "feature:knipovich-ridge"
        },
        {
          "row_index": 13,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "feature:logachev-seamount"
        },
        {
          "row_index": 15,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 16,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mylonite-shear-zones"
        },
        {
          "row_index": 20,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 21,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 22,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd2-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 25,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 26,
          "witness_key": "feature:occ-normal-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 28,
          "witness_key": "feature:pre-eruptive-melt"
        },
        {
          "row_index": 29,
          "witness_key": "feature:primary-melt"
        },
        {
          "row_index": 30,
          "witness_key": "feature:rainbow-massif"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2-inward-dipping-faults"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-median-valley"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 39,
          "witness_key": "feature:sedimentary-layers"
        },
        {
          "row_index": 40,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 41,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 42,
          "witness_key": "feature:western-indian-ocean"
        },
        {
          "row_index": 43,
          "witness_key": "feature:western-ridge-flank"
        },
        {
          "row_index": 44,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 45,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 46,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 47,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 48,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 49,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 50,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 51,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 52,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 53,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 54,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 55,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 56,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 57,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 58,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 59,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 60,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 61,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 62,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 63,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 64,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 65,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 66,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 67,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 68,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 69,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 70,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 71,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 72,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 73,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 74,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 75,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 76,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 77,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 78,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 79,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 80,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 81,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 82,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 83,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 84,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 85,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 87,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 88,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 89,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 90,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 91,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 92,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 93,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 94,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 95,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 96,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 97,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 98,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 99,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 100,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 101,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 102,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 103,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 104,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 105,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 116,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 117,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 118,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 119,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 120,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 121,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 122,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 123,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 124,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 125,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 126,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 128,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 129,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 130,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 131,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 132,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 133,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 134,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 135,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 136,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 137,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 138,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 139,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 140,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 141,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 142,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 143,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 144,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 145,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 146,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 147,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 148,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 149,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 150,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 151,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 152,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 153,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 155,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 156,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 157,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 158,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 159,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 160,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 161,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 162,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 163,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 164,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 165,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 166,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 167,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 168,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 169,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 170,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 171,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 172,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 173,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 174,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 175,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 176,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 177,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 178,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 179,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 180,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 181,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 182,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 183,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 184,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 185,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 186,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 187,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 188,
          "witness_key": "rel:corrugated-surface-part-of-occ"
        },
        {
          "row_index": 189,
          "witness_key": "rel:mar-within-equatorial-atlantic"
        },
        {
          "row_index": 190,
          "witness_key": "rel:ntd2-faults-within"
        },
        {
          "row_index": 191,
          "witness_key": "rel:occ-cut-by-normal-faults"
        },
        {
          "row_index": 192,
          "witness_key": "rel:rc1-bounded-by-detachment"
        },
        {
          "row_index": 193,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 194,
          "witness_key": "rel:rc2-bounded-by-inward-faults"
        },
        {
          "row_index": 195,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 196,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 197,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 198,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 199,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 200,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 201,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 202,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 203,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 204,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 205,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 206,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 207,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 208,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 209,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 210,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 211,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 212,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 213,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 214,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 215,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 216,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 217,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 218,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 219,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 220,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 221,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 222,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 223,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 224,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 225,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 226,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 227,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 228,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 229,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 230,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 231,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 232,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 233,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 234,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 235,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 236,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 237,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 238,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 239,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 240,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 241,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 242,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 243,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 244,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 245,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 246,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 247,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 248,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 249,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 250,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 251,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 252,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 253,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 254,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 255,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 256,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 257,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 258,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 259,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 260,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 261,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 262,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 263,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 264,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 265,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 266,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 267,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 268,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 269,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 270,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 271,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 272,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 273,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 274,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 275,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 276,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 277,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 278,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 279,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 280,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 281,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 282,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 283,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 284,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 285,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 286,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 287,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 288,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 289,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 290,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 291,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 292,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 293,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 294,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 295,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 296,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 297,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 298,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 299,
          "witness_key": "obs:volatile-melting-initiation-depth"
        },
        {
          "row_index": 300,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 301,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 302,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 303,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 304,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 305,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 306,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 307,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 308,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 309,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 310,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 311,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 312,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 313,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 314,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 315,
          "witness_key": "obs:lab-water-content"
        }
      ]
    },
    {
      "question_id": "CQ-T5-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four items come back, spread over two claims and two counts with nothing joining them.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "category_set",
          "row_index": 11,
          "absent_reason": null,
          "note": "the claim names the categories and what each one meets"
        },
        {
          "semantic": "category_count",
          "row_index": 71,
          "absent_reason": null,
          "note": "the count row carries how many there are"
        },
        {
          "semantic": "selection_for_interpretation",
          "row_index": 10,
          "absent_reason": null,
          "note": "a claim says which categories are used for interpretation"
        },
        {
          "semantic": "earthquake_catalog",
          "row_index": 211,
          "absent_reason": null,
          "note": "the count of located earthquakes stands for the catalogue that was classified"
        }
      ],
      "source_locators": [
        "page:7:block:008",
        "page:2:block:003",
        "page:6:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 1,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 2,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 3,
          "witness_key": "method:refraction-profile"
        },
        {
          "row_index": 4,
          "witness_key": "method:sta-lta"
        },
        {
          "row_index": 5,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 6,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 7,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 8,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 9,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 10,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 11,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 12,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 13,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 14,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 15,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 16,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 17,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 18,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 19,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 20,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 21,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 22,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 23,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 24,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 25,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 26,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 27,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 28,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 29,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 30,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 31,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 32,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 33,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 34,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 35,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 36,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 37,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 38,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 39,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 40,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 41,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 42,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 43,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 44,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 45,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 46,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 47,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 48,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 49,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 50,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 51,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 52,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 53,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 54,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 55,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 56,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 57,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 58,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 59,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 60,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 61,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 62,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 63,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 64,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 65,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 66,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 67,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 68,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 70,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 71,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 72,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 73,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 74,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 82,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 83,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 84,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 86,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 87,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 88,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 89,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 90,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 91,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 92,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 93,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 94,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 95,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 96,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 97,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 98,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 99,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 100,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 101,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 102,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 103,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 104,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 105,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 106,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 107,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 108,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 109,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 110,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 111,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 112,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 113,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 114,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 115,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 116,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 117,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 118,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 119,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 120,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 121,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 122,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 123,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 124,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 125,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 126,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 127,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 128,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 129,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 130,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 131,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 132,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 133,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 134,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 135,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 136,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 137,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 138,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 139,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 140,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 141,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 142,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 143,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 144,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 145,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 146,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 147,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 148,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 149,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 150,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 151,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 152,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 153,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 154,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 155,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 156,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 157,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 158,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 159,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 160,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 161,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 162,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 163,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 164,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 165,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 166,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 167,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 168,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 169,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 170,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 171,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 172,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 173,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 174,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 175,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 176,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 177,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 178,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 179,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 180,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 181,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 182,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 183,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 184,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 185,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 186,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 187,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 188,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 189,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 190,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 191,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 192,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 193,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 194,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 195,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 196,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 197,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 198,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 199,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 200,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 201,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 202,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 203,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 204,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 205,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 206,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 207,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 208,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 209,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 210,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 212,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 213,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 214,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 215,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 216,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 217,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 218,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 219,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 220,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 221,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 222,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 223,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 224,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 225,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 226,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 227,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 228,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 229,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 230,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 231,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 232,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 233,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 234,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 235,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 238,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 239,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 240,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 241,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 242,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 244,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 248,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 249,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 250,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 253,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 254,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 255,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 256,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 257,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 260,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 261,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 262,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 263,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 264,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 265,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 266,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 267,
          "witness_key": "obs:volatile-melting-initiation-depth"
        }
      ]
    },
    {
      "question_id": "CQ-T5-05",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The explanation, its rejection and both observations are returned, and the argument that connects them is not. Everything here comes out of one block, which is where the connection stayed.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "candidate_explanation",
          "row_index": 198,
          "absent_reason": null,
          "note": "the claim states the explanation being argued against"
        },
        {
          "semantic": "morphological_observation",
          "row_index": 47,
          "absent_reason": null,
          "note": "a claim from the same block characterises the axial morphology"
        },
        {
          "semantic": "seismic_observation",
          "row_index": 287,
          "absent_reason": null,
          "note": "an observation carries the off-axis shallow seismicity"
        },
        {
          "semantic": "evidence_relation",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "the reasoning that reads the morphology and the off-axis seismicity against the cold and thick lithosphere is in the block these records point at, and no field or relation carries it"
        },
        {
          "semantic": "declined_disposition",
          "row_index": 198,
          "absent_reason": null,
          "note": "the candidate claim carries the slot saying it is not supported"
        }
      ],
      "source_locators": [
        "page:3:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:ascending-melt"
        },
        {
          "row_index": 1,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 4,
          "witness_key": "feature:detachment-fault-rti"
        },
        {
          "row_index": 5,
          "witness_key": "feature:equatorial-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 9,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 10,
          "witness_key": "feature:inactive-hydrothermal-mound"
        },
        {
          "row_index": 11,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 12,
          "witness_key": "feature:knipovich-ridge"
        },
        {
          "row_index": 13,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "feature:logachev-seamount"
        },
        {
          "row_index": 15,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 16,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mylonite-shear-zones"
        },
        {
          "row_index": 20,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 21,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 22,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd2-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 25,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 26,
          "witness_key": "feature:occ-normal-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 28,
          "witness_key": "feature:pre-eruptive-melt"
        },
        {
          "row_index": 29,
          "witness_key": "feature:primary-melt"
        },
        {
          "row_index": 30,
          "witness_key": "feature:rainbow-massif"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2-inward-dipping-faults"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-median-valley"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 39,
          "witness_key": "feature:sedimentary-layers"
        },
        {
          "row_index": 40,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 41,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 42,
          "witness_key": "feature:western-indian-ocean"
        },
        {
          "row_index": 43,
          "witness_key": "feature:western-ridge-flank"
        },
        {
          "row_index": 44,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 45,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 46,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 47,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 48,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 49,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 50,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 51,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 52,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 53,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 54,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 55,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 56,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 57,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 58,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 59,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 60,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 61,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 62,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 63,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 64,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 65,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 66,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 67,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 68,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 69,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 70,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 71,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 72,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 73,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 74,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 75,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 76,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 77,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 78,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 79,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 80,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 81,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 82,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 83,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 84,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 85,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 86,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 87,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 88,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 89,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 90,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 91,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 92,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 93,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 94,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 95,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 96,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 97,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 98,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 99,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 100,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 101,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 102,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 103,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 104,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 116,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 117,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 118,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 119,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 120,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 121,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 122,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 123,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 124,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 125,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 126,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 128,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 129,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 130,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 131,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 132,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 133,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 134,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 135,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 136,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 137,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 138,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 139,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 140,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 141,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 142,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 143,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 144,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 145,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 146,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 147,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 148,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 149,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 150,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 151,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 152,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 153,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 154,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 155,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 156,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 157,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 158,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 159,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 160,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 161,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 162,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 163,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 164,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 165,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 166,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 167,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 168,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 169,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 170,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 171,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 172,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 173,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 174,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 175,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 176,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 177,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 178,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 179,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 180,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 181,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 182,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 183,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 184,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 185,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 186,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 187,
          "witness_key": "rel:corrugated-surface-part-of-occ"
        },
        {
          "row_index": 188,
          "witness_key": "rel:mar-within-equatorial-atlantic"
        },
        {
          "row_index": 189,
          "witness_key": "rel:ntd2-faults-within"
        },
        {
          "row_index": 190,
          "witness_key": "rel:occ-cut-by-normal-faults"
        },
        {
          "row_index": 191,
          "witness_key": "rel:rc1-bounded-by-detachment"
        },
        {
          "row_index": 192,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 193,
          "witness_key": "rel:rc2-bounded-by-inward-faults"
        },
        {
          "row_index": 194,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 195,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 196,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 197,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 198,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 199,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 200,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 201,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 202,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 203,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 204,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 205,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 206,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 207,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 208,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 209,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 210,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 211,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 212,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 213,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 214,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 215,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 216,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 217,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 218,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 219,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 220,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 221,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 222,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 223,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 224,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 225,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 226,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 227,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 229,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 230,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 231,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 232,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 233,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 234,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 235,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 236,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 237,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 238,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 239,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 240,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 241,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 242,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 243,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 244,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 245,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 246,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 247,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 248,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 249,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 250,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 251,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 252,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 253,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 254,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 255,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 256,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 257,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 258,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 259,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 260,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 261,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 262,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 263,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 264,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 265,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 266,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 267,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 268,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 269,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 270,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 271,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 272,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 273,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 274,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 275,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 276,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 277,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 278,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 279,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 280,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 281,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 282,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 283,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 284,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 285,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 286,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 287,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 288,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 289,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 290,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 291,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 292,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 293,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 294,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 295,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 296,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 297,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 298,
          "witness_key": "obs:volatile-melting-initiation-depth"
        },
        {
          "row_index": 299,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 300,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 301,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 302,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 303,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 304,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 305,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 306,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 307,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 308,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 309,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 310,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 311,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 312,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 313,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 314,
          "witness_key": "obs:lab-water-content"
        }
      ]
    },
    {
      "question_id": "CQ-C-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The question asks for something the paper does not report. The sample set it names does exist as a record and comes back through the type expansion; the sulfur and chlorine figures do not exist in the reading at all, so three of the four items have nothing behind them.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "the reading carries no sulfur or chlorine measurement anywhere"
        },
        {
          "semantic": "concentration_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "with no such measurement there is no unit for one"
        },
        {
          "semantic": "sample_set",
          "row_index": 0,
          "absent_reason": null,
          "note": "the basalt sample record the volatile work rests on is returned"
        },
        {
          "semantic": "measurement_status",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "and no status, for the same reason"
        }
      ],
      "source_locators": [
        "page:1:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "sample:basaltic-rocks"
        },
        {
          "row_index": 1,
          "witness_key": "sample:basalts"
        },
        {
          "row_index": 2,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 3,
          "witness_key": "sample:morb"
        },
        {
          "row_index": 4,
          "witness_key": "sample:peridotites"
        },
        {
          "row_index": 5,
          "witness_key": "sample:pillow-basalts"
        },
        {
          "row_index": 6,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 7,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 8,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 9,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 10,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 11,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 12,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 13,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 14,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 15,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 16,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 17,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 18,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 19,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 20,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 21,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 22,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 23,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 24,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 25,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 26,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 27,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 28,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 29,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 30,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 31,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 32,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 33,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 34,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 35,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 36,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 37,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 38,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 39,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 40,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 41,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 42,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 43,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 44,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 45,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 46,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 47,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 48,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 49,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 50,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 51,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 52,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 53,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 54,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 55,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 56,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 57,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 58,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 59,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 60,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 61,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 62,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 63,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 64,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 65,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 66,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 67,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 68,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 70,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 71,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 72,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 73,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 74,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 82,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 83,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 84,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 86,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 87,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 88,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 89,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 90,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 91,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 92,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 93,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 94,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 95,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 96,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 97,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 98,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 99,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 100,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 101,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 102,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 103,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 104,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 105,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 106,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 107,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 108,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 109,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 110,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 111,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 112,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 113,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 114,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 115,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 116,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 117,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 118,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 119,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 120,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 121,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 122,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 123,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 124,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 125,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 126,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 127,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 128,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 129,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 130,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 131,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 132,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 133,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 134,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 135,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 136,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 137,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 138,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 139,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 140,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 141,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 142,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 143,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 144,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 145,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 146,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 147,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 148,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 149,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 150,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 151,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 152,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 153,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 154,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 155,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 156,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 157,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 158,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 159,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 160,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 161,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 162,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 163,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 164,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 165,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 166,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 167,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 168,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 169,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 170,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 171,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 172,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 173,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 174,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 175,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 176,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 177,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 178,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 179,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 180,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 181,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 182,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 183,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 184,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 185,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 186,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 187,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 188,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 189,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 190,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 191,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 192,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 193,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 194,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 195,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 196,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 197,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 198,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 199,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 200,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 201,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 202,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 203,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 204,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 205,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 206,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 207,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 208,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 209,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 210,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 211,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 212,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 213,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 214,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 215,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 216,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 217,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 218,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 219,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 220,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 221,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 222,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 223,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 224,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 225,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 226,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 227,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 228,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 229,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 230,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 231,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 232,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 233,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 234,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 235,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 237,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 238,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 239,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 240,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 241,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 242,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 244,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 245,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 246,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 248,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 249,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 250,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 251,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 252,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 253,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 254,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 255,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 256,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 257,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 258,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 259,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 260,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 261,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 262,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 263,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 264,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 265,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 266,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 267,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 268,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 269,
          "witness_key": "obs:volatile-melting-initiation-depth"
        }
      ]
    },
    {
      "question_id": "CQ-C-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Nothing in the reading gives a repeat time for these events. The population the question names is reached, because observations about those earthquakes are of a type this question opens, so one item lands and three cannot.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "temporal_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "the reading gives no recurrence interval for these earthquakes"
        },
        {
          "semantic": "time_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "with no interval there is no unit for one"
        },
        {
          "semantic": "event_population",
          "row_index": 230,
          "absent_reason": null,
          "note": "the deep earthquakes beneath the axis are carried by a depth observation that points at the ridge"
        },
        {
          "semantic": "measurement_status",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "and no status, for the same reason"
        }
      ],
      "source_locators": [
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 1,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 2,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 3,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 4,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 5,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 6,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 7,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 8,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 9,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 10,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 11,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 12,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 13,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 14,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 15,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 16,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 17,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 18,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 19,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 20,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 21,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 22,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 23,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 24,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 25,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 26,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 27,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 28,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 29,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 30,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 31,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 32,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 33,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 34,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 35,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 36,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 37,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 38,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 39,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 40,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 41,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 42,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 43,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 44,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 45,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 46,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 47,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 48,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 49,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 50,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 51,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 52,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 53,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 54,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 55,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 56,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 57,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 58,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 59,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 60,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 61,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 62,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 63,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 64,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 65,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 66,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 67,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 68,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 70,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 71,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 72,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 73,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 74,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 82,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 83,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 84,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 85,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 86,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 87,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 88,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 89,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 90,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 91,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 92,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 93,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 94,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 95,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 96,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 97,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 98,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 99,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 100,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 101,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 102,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 103,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 104,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 105,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 106,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 107,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 108,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 109,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 110,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 111,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 112,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 113,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 114,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 115,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 116,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 117,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 118,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 119,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 120,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 121,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 122,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 123,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 124,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 125,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 126,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 127,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 128,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 129,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 130,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 131,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 132,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 133,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 134,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 135,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 136,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 137,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 138,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 139,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 140,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 141,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 142,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 143,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 144,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 145,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 146,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 147,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 148,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 149,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 150,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 151,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 152,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 153,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 154,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 155,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 156,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 157,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 158,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 159,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 160,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 161,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 162,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 163,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 164,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 165,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 166,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 167,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 168,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 169,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 170,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 171,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 172,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 173,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 174,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 175,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 176,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 177,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 178,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 179,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 180,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 181,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 182,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 183,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 184,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 185,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 186,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 187,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 188,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 189,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 190,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 191,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 192,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 193,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 194,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 195,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 196,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 197,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 198,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 199,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 200,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 201,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 202,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 203,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 204,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 205,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 206,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 207,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 208,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 209,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 210,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 211,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 212,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 213,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 214,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 215,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 216,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 217,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 218,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 219,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 220,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 221,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 222,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 223,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 224,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 225,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 226,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 227,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 229,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 230,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 231,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 232,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 233,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 234,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 236,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 237,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 238,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 239,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 240,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 241,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 242,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 243,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 244,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 245,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 246,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 247,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 248,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 249,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 251,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 252,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 253,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 254,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 255,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 256,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 259,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 260,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 261,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 262,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 263,
          "witness_key": "obs:volatile-melting-initiation-depth"
        }
      ]
    },
    {
      "question_id": "CQ-C-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The compilation and some of the sites in it are named in the running text and come back; the numbers the question asks for live in a figure and a supplementary table, which this evidence surface excludes, so they are absent from the source rather than from the graph.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "site_set",
          "row_index": 329,
          "absent_reason": null,
          "note": "a claim names the compiled sites whose values were updated; the full compiled set is in a figure and a supplementary table, which are outside this surface"
        },
        {
          "semantic": "maximum_depth_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "the per-site depths are plotted and tabulated, not stated in the reading"
        },
        {
          "semantic": "spreading_rate_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "the per-site spreading rates are in the same figure and table"
        },
        {
          "semantic": "compilation_source",
          "row_index": 140,
          "absent_reason": null,
          "note": "a claim states that the depths and rates were compiled for slow and ultraslow ridges worldwide"
        }
      ],
      "source_locators": [
        "page:8:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:ascending-melt"
        },
        {
          "row_index": 1,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 4,
          "witness_key": "feature:detachment-fault-rti"
        },
        {
          "row_index": 5,
          "witness_key": "feature:equatorial-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 9,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 10,
          "witness_key": "feature:inactive-hydrothermal-mound"
        },
        {
          "row_index": 11,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 12,
          "witness_key": "feature:knipovich-ridge"
        },
        {
          "row_index": 13,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "feature:logachev-seamount"
        },
        {
          "row_index": 15,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 16,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mylonite-shear-zones"
        },
        {
          "row_index": 20,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 21,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 22,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd2-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 25,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 26,
          "witness_key": "feature:occ-normal-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 28,
          "witness_key": "feature:pre-eruptive-melt"
        },
        {
          "row_index": 29,
          "witness_key": "feature:primary-melt"
        },
        {
          "row_index": 30,
          "witness_key": "feature:rainbow-massif"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2-inward-dipping-faults"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-median-valley"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 39,
          "witness_key": "feature:sedimentary-layers"
        },
        {
          "row_index": 40,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 41,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 42,
          "witness_key": "feature:western-indian-ocean"
        },
        {
          "row_index": 43,
          "witness_key": "feature:western-ridge-flank"
        },
        {
          "row_index": 44,
          "witness_key": "ref:001"
        },
        {
          "row_index": 45,
          "witness_key": "ref:002"
        },
        {
          "row_index": 46,
          "witness_key": "ref:003"
        },
        {
          "row_index": 47,
          "witness_key": "ref:004"
        },
        {
          "row_index": 48,
          "witness_key": "ref:005"
        },
        {
          "row_index": 49,
          "witness_key": "ref:006"
        },
        {
          "row_index": 50,
          "witness_key": "ref:007"
        },
        {
          "row_index": 51,
          "witness_key": "ref:008"
        },
        {
          "row_index": 52,
          "witness_key": "ref:009"
        },
        {
          "row_index": 53,
          "witness_key": "ref:010"
        },
        {
          "row_index": 54,
          "witness_key": "ref:011"
        },
        {
          "row_index": 55,
          "witness_key": "ref:012"
        },
        {
          "row_index": 56,
          "witness_key": "ref:013"
        },
        {
          "row_index": 57,
          "witness_key": "ref:014"
        },
        {
          "row_index": 58,
          "witness_key": "ref:015"
        },
        {
          "row_index": 59,
          "witness_key": "ref:016"
        },
        {
          "row_index": 60,
          "witness_key": "ref:017"
        },
        {
          "row_index": 61,
          "witness_key": "ref:018"
        },
        {
          "row_index": 62,
          "witness_key": "ref:019"
        },
        {
          "row_index": 63,
          "witness_key": "ref:020"
        },
        {
          "row_index": 64,
          "witness_key": "ref:021"
        },
        {
          "row_index": 65,
          "witness_key": "ref:022"
        },
        {
          "row_index": 66,
          "witness_key": "ref:023"
        },
        {
          "row_index": 67,
          "witness_key": "ref:024"
        },
        {
          "row_index": 68,
          "witness_key": "ref:025"
        },
        {
          "row_index": 69,
          "witness_key": "ref:026"
        },
        {
          "row_index": 70,
          "witness_key": "ref:027"
        },
        {
          "row_index": 71,
          "witness_key": "ref:028"
        },
        {
          "row_index": 72,
          "witness_key": "ref:029"
        },
        {
          "row_index": 73,
          "witness_key": "ref:030"
        },
        {
          "row_index": 74,
          "witness_key": "ref:031"
        },
        {
          "row_index": 75,
          "witness_key": "ref:032"
        },
        {
          "row_index": 76,
          "witness_key": "ref:033"
        },
        {
          "row_index": 77,
          "witness_key": "ref:034"
        },
        {
          "row_index": 78,
          "witness_key": "ref:035"
        },
        {
          "row_index": 79,
          "witness_key": "ref:036"
        },
        {
          "row_index": 80,
          "witness_key": "ref:037"
        },
        {
          "row_index": 81,
          "witness_key": "ref:038"
        },
        {
          "row_index": 82,
          "witness_key": "ref:039"
        },
        {
          "row_index": 83,
          "witness_key": "ref:040"
        },
        {
          "row_index": 84,
          "witness_key": "ref:041"
        },
        {
          "row_index": 85,
          "witness_key": "ref:042"
        },
        {
          "row_index": 86,
          "witness_key": "ref:043"
        },
        {
          "row_index": 87,
          "witness_key": "ref:044"
        },
        {
          "row_index": 88,
          "witness_key": "ref:045"
        },
        {
          "row_index": 89,
          "witness_key": "ref:046"
        },
        {
          "row_index": 90,
          "witness_key": "ref:047"
        },
        {
          "row_index": 91,
          "witness_key": "ref:048"
        },
        {
          "row_index": 92,
          "witness_key": "ref:049"
        },
        {
          "row_index": 93,
          "witness_key": "ref:050"
        },
        {
          "row_index": 94,
          "witness_key": "ref:051"
        },
        {
          "row_index": 95,
          "witness_key": "ref:052"
        },
        {
          "row_index": 96,
          "witness_key": "ref:053"
        },
        {
          "row_index": 97,
          "witness_key": "ref:054"
        },
        {
          "row_index": 98,
          "witness_key": "ref:055"
        },
        {
          "row_index": 99,
          "witness_key": "ref:056"
        },
        {
          "row_index": 100,
          "witness_key": "ref:057"
        },
        {
          "row_index": 101,
          "witness_key": "ref:058"
        },
        {
          "row_index": 102,
          "witness_key": "ref:059"
        },
        {
          "row_index": 103,
          "witness_key": "ref:060"
        },
        {
          "row_index": 104,
          "witness_key": "ref:061"
        },
        {
          "row_index": 105,
          "witness_key": "ref:062"
        },
        {
          "row_index": 106,
          "witness_key": "ref:063"
        },
        {
          "row_index": 107,
          "witness_key": "ref:064"
        },
        {
          "row_index": 108,
          "witness_key": "ref:065"
        },
        {
          "row_index": 109,
          "witness_key": "ref:066"
        },
        {
          "row_index": 110,
          "witness_key": "ref:067"
        },
        {
          "row_index": 111,
          "witness_key": "ref:068"
        },
        {
          "row_index": 112,
          "witness_key": "ref:069"
        },
        {
          "row_index": 113,
          "witness_key": "ref:070"
        },
        {
          "row_index": 114,
          "witness_key": "ref:071"
        },
        {
          "row_index": 115,
          "witness_key": "ref:072"
        },
        {
          "row_index": 116,
          "witness_key": "ref:073"
        },
        {
          "row_index": 117,
          "witness_key": "ref:074"
        },
        {
          "row_index": 118,
          "witness_key": "ref:075"
        },
        {
          "row_index": 119,
          "witness_key": "ref:076"
        },
        {
          "row_index": 120,
          "witness_key": "ref:077"
        },
        {
          "row_index": 121,
          "witness_key": "ref:078"
        },
        {
          "row_index": 122,
          "witness_key": "ref:079"
        },
        {
          "row_index": 123,
          "witness_key": "source:article:yu-2025"
        },
        {
          "row_index": 124,
          "witness_key": "source:cc-licence"
        },
        {
          "row_index": 125,
          "witness_key": "source:cruise-website"
        },
        {
          "row_index": 126,
          "witness_key": "source:petdb"
        },
        {
          "row_index": 127,
          "witness_key": "source:supplementary"
        },
        {
          "row_index": 128,
          "witness_key": "source:zenodo-catalog"
        },
        {
          "row_index": 129,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 130,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 131,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 132,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 133,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 134,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 135,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 136,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 137,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 138,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 139,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 140,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 141,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 142,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 143,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 144,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 145,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 146,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 147,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 148,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 149,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 150,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 151,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 152,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 153,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 154,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 155,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 156,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 157,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 158,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 159,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 160,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 161,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 162,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 163,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 164,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 165,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 166,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 167,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 168,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 169,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 170,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 171,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 172,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 173,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 174,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 175,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 176,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 177,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 178,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 179,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 180,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 181,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 182,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 183,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 184,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 185,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 186,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 187,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 188,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 189,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 190,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 191,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 192,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 193,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 194,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 195,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 196,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 197,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 198,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 199,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 200,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 201,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 202,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 203,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 204,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 205,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 206,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 207,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 208,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 209,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 210,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 211,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 212,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 213,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 214,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 215,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 216,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 217,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 218,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 219,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 220,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 221,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 222,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 223,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 224,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 225,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 226,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 227,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 228,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 229,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 230,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 231,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 232,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 233,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 234,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 235,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 236,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 237,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 238,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 239,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 240,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 241,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 242,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 243,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 244,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 245,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 248,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 249,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 250,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 251,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 252,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 253,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 254,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 255,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 256,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 259,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 260,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 261,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 262,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 263,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 264,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 265,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 266,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 267,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 268,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 269,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 270,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 271,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 272,
          "witness_key": "rel:corrugated-surface-part-of-occ"
        },
        {
          "row_index": 273,
          "witness_key": "rel:mar-within-equatorial-atlantic"
        },
        {
          "row_index": 274,
          "witness_key": "rel:ntd2-faults-within"
        },
        {
          "row_index": 275,
          "witness_key": "rel:occ-cut-by-normal-faults"
        },
        {
          "row_index": 276,
          "witness_key": "rel:rc1-bounded-by-detachment"
        },
        {
          "row_index": 277,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 278,
          "witness_key": "rel:rc2-bounded-by-inward-faults"
        },
        {
          "row_index": 279,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 280,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 281,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 282,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 283,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 284,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 285,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 286,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 287,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 288,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 289,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 290,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 291,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 292,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 293,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 294,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 295,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 296,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 297,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 298,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 299,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 300,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 301,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 302,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 303,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 304,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 305,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 306,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 307,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 308,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 309,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 310,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 311,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 312,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 313,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 314,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 315,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 316,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 317,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 318,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 319,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 320,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 321,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 322,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 323,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 324,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 325,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 326,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 327,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 328,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 329,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 330,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 331,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 332,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 333,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 334,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 335,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 336,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 337,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 338,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 339,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 340,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 341,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 342,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 343,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 344,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 345,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 346,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 347,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 348,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 349,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 350,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 351,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 352,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 353,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 354,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 355,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 356,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 357,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 358,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 359,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 360,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 361,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 362,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 363,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 364,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 365,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 366,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 367,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 368,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 369,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 370,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 371,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 372,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 373,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 374,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 375,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 376,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 377,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 378,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 379,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 380,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 381,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 382,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 383,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 384,
          "witness_key": "obs:volatile-melting-initiation-depth"
        },
        {
          "row_index": 385,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 386,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 387,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 388,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 389,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 390,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 391,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 392,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 393,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 394,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 395,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 396,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 397,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 398,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 399,
          "witness_key": "obs:lab-water-content"
        }
      ]
    },
    {
      "question_id": "CQ-C-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "This question returns the same rows as the one it restates, and the same three items land on the same three records, with the relation between two of them also returned.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "instrument_count",
          "row_index": 11,
          "absent_reason": null,
          "note": "the count record carries the number and what it counts"
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "the instrument record stands for the network"
        },
        {
          "semantic": "deployment_event",
          "row_index": 0,
          "absent_reason": null,
          "note": "the campaign record is the cruise the network was placed during"
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002",
        "page:1:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "campaign:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instrument:obs"
        },
        {
          "row_index": 2,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 3,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 4,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 5,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 6,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 7,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 8,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 9,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 17,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 18,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 19,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 20,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 21,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 22,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 23,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 24,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 25,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 26,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 27,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 28,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 29,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 30,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 31,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 32,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 33,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 34,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 35,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 36,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 37,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 38,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 39,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 40,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 41,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 42,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 43,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 44,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 45,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 46,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 47,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 48,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 49,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 50,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 51,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 52,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 53,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 54,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 55,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 56,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 57,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 58,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 59,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 60,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 61,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 62,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 63,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 64,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 65,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 66,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 67,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 68,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 69,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 70,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 71,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 72,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 73,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 74,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 75,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 76,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 77,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 78,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 79,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 80,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 81,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 82,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 83,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 84,
          "witness_key": "rel:obs-part-of-smarties"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 86,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 87,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 88,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 89,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 90,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 91,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 92,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 93,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 94,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 95,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 96,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 97,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 98,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 99,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 100,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 101,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 102,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 103,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 104,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 105,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 106,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 107,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 108,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 109,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 110,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 112,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 113,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 114,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 115,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 116,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 117,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 118,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 119,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 120,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 121,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 122,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 123,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 124,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 125,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 126,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 127,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 128,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 129,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 130,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 131,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 132,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 133,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 134,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 135,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 136,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 137,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 138,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 139,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 140,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 141,
          "witness_key": "obs:volatile-melting-initiation-depth"
        }
      ]
    },
    {
      "question_id": "CQ-C-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "This question restates one already asked and returns the same rows, so the same single observation carries the content, the unit, the segment and how the value was obtained.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 270,
          "absent_reason": null,
          "note": "the observation carries both bounds"
        },
        {
          "semantic": "concentration_unit",
          "row_index": 270,
          "absent_reason": null,
          "note": "and the unit"
        },
        {
          "semantic": "quantity_subject",
          "row_index": 270,
          "absent_reason": null,
          "note": "its subject reference resolves to the segment"
        },
        {
          "semantic": "calculated_or_measured_status",
          "row_index": 270,
          "absent_reason": null,
          "note": "and the slot saying the value was estimated"
        }
      ],
      "source_locators": [
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:ascending-melt"
        },
        {
          "row_index": 1,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 4,
          "witness_key": "feature:detachment-fault-rti"
        },
        {
          "row_index": 5,
          "witness_key": "feature:equatorial-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 9,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 10,
          "witness_key": "feature:inactive-hydrothermal-mound"
        },
        {
          "row_index": 11,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 12,
          "witness_key": "feature:knipovich-ridge"
        },
        {
          "row_index": 13,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "feature:logachev-seamount"
        },
        {
          "row_index": 15,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 16,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mylonite-shear-zones"
        },
        {
          "row_index": 20,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 21,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 22,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd2-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 25,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 26,
          "witness_key": "feature:occ-normal-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 28,
          "witness_key": "feature:pre-eruptive-melt"
        },
        {
          "row_index": 29,
          "witness_key": "feature:primary-melt"
        },
        {
          "row_index": 30,
          "witness_key": "feature:rainbow-massif"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2-inward-dipping-faults"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-median-valley"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc2-neovolcanic-ridge"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 39,
          "witness_key": "feature:sedimentary-layers"
        },
        {
          "row_index": 40,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 41,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 42,
          "witness_key": "feature:western-indian-ocean"
        },
        {
          "row_index": 43,
          "witness_key": "feature:western-ridge-flank"
        },
        {
          "row_index": 44,
          "witness_key": "sample:basaltic-rocks"
        },
        {
          "row_index": 45,
          "witness_key": "sample:basalts"
        },
        {
          "row_index": 46,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 47,
          "witness_key": "sample:morb"
        },
        {
          "row_index": 48,
          "witness_key": "sample:peridotites"
        },
        {
          "row_index": 49,
          "witness_key": "sample:pillow-basalts"
        },
        {
          "row_index": 50,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 51,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 53,
          "witness_key": "claim:average-model-best-fitting"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axial-valley-floor-character"
        },
        {
          "row_index": 55,
          "witness_key": "claim:ba90-rb90-calculated"
        },
        {
          "row_index": 56,
          "witness_key": "claim:categories-ab-good-quality"
        },
        {
          "row_index": 57,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 58,
          "witness_key": "claim:circles-show-location-qualities"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-behaves-like-incompatible-elements"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-calculated-from-rb90-ba90"
        },
        {
          "row_index": 61,
          "witness_key": "claim:co2-solubility-pressure-dependent"
        },
        {
          "row_index": 62,
          "witness_key": "claim:compiled-maximum-depths"
        },
        {
          "row_index": 63,
          "witness_key": "claim:compiled-morb-analyses"
        },
        {
          "row_index": 64,
          "witness_key": "claim:deeper-earthquakes-associations"
        },
        {
          "row_index": 65,
          "witness_key": "claim:deepest-earthquakes-documented"
        },
        {
          "row_index": 66,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 67,
          "witness_key": "claim:depth-selection-criterion"
        },
        {
          "row_index": 68,
          "witness_key": "claim:depth-tests-support-deep-events"
        },
        {
          "row_index": 69,
          "witness_key": "claim:depths-forced-fixed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:fig2b-depth-profiles"
        },
        {
          "row_index": 71,
          "witness_key": "claim:fig3-depth-shading"
        },
        {
          "row_index": 72,
          "witness_key": "claim:fig4-content"
        },
        {
          "row_index": 73,
          "witness_key": "claim:fig5-content"
        },
        {
          "row_index": 74,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 75,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 76,
          "witness_key": "claim:focus-on-ridge-subsections"
        },
        {
          "row_index": 77,
          "witness_key": "claim:influencing-information-included"
        },
        {
          "row_index": 78,
          "witness_key": "claim:isotherms-from-thermal-model"
        },
        {
          "row_index": 79,
          "witness_key": "claim:local-magnitudes-determined"
        },
        {
          "row_index": 80,
          "witness_key": "claim:magmatic-tectonic-events-need-eruptions"
        },
        {
          "row_index": 81,
          "witness_key": "claim:max-depth-depends-on-other-factors"
        },
        {
          "row_index": 82,
          "witness_key": "claim:max-depths-affected-by-processes"
        },
        {
          "row_index": 83,
          "witness_key": "claim:maximum-likelihood-preferred"
        },
        {
          "row_index": 84,
          "witness_key": "claim:may-produce-long-period-earthquakes"
        },
        {
          "row_index": 85,
          "witness_key": "claim:measured-co2-close-to-solubility"
        },
        {
          "row_index": 86,
          "witness_key": "claim:mechanism-similar-to-volcanoes"
        },
        {
          "row_index": 87,
          "witness_key": "claim:melt-focused-beneath-ridge-axis"
        },
        {
          "row_index": 88,
          "witness_key": "claim:melt-movement-brittle-failure"
        },
        {
          "row_index": 89,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 90,
          "witness_key": "claim:model-selection-criterion"
        },
        {
          "row_index": 91,
          "witness_key": "claim:more-earthquakes-needed"
        },
        {
          "row_index": 92,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 93,
          "witness_key": "claim:no-detachment-faults-rc2"
        },
        {
          "row_index": 94,
          "witness_key": "claim:no-permission-for-adapted-material"
        },
        {
          "row_index": 95,
          "witness_key": "claim:ntd1-magmatic-tectonic-origin"
        },
        {
          "row_index": 96,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 97,
          "witness_key": "claim:poor-azimuthal-distribution"
        },
        {
          "row_index": 98,
          "witness_key": "claim:record-is-a-snapshot"
        },
        {
          "row_index": 99,
          "witness_key": "claim:reduced-velocity-model-reasonable"
        },
        {
          "row_index": 100,
          "witness_key": "claim:samples-are-degassed"
        },
        {
          "row_index": 101,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 102,
          "witness_key": "claim:station-corrections-and-swave-delays"
        },
        {
          "row_index": 103,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 104,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 105,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 106,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 107,
          "witness_key": "claim:volatile-ratios-examined"
        },
        {
          "row_index": 108,
          "witness_key": "claim:volatile-role-melt-migration"
        },
        {
          "row_index": 109,
          "witness_key": "claim:volatiles-control-magma-properties"
        },
        {
          "row_index": 110,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 111,
          "witness_key": "claim:vpvs-17-reasonable"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:depth-test-subset"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:events-romanche-tf"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 116,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 117,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 118,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 119,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 120,
          "witness_key": "cnt:non-transform-discontinuities"
        },
        {
          "row_index": 121,
          "witness_key": "cnt:obs-network"
        },
        {
          "row_index": 122,
          "witness_key": "cnt:obs-without-data"
        },
        {
          "row_index": 123,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 124,
          "witness_key": "cnt:romanche-2016-subevents"
        },
        {
          "row_index": 125,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 126,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 127,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 128,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 129,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 130,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 131,
          "witness_key": "cnt:well-relocated-events"
        },
        {
          "row_index": 132,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 133,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 134,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 135,
          "witness_key": "obs:azimuthal-gap-relocated"
        },
        {
          "row_index": 136,
          "witness_key": "obs:b-value-catalog"
        },
        {
          "row_index": 137,
          "witness_key": "obs:b-values-groups"
        },
        {
          "row_index": 138,
          "witness_key": "obs:brittle-lithospheric-thickness"
        },
        {
          "row_index": 139,
          "witness_key": "obs:co2-gas-phase-loss"
        },
        {
          "row_index": 140,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 141,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 142,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 143,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 144,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 145,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 146,
          "witness_key": "obs:crustal-age-bdb-shallow"
        },
        {
          "row_index": 147,
          "witness_key": "obs:deep-events-threshold"
        },
        {
          "row_index": 148,
          "witness_key": "obs:depth-test-subset-range"
        },
        {
          "row_index": 149,
          "witness_key": "obs:depth-uncertainty-catalog"
        },
        {
          "row_index": 150,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 151,
          "witness_key": "obs:expected-max-depth-here"
        },
        {
          "row_index": 152,
          "witness_key": "obs:expected-max-depth-slow-ridges"
        },
        {
          "row_index": 153,
          "witness_key": "obs:expected-max-depth-ultraslow-ridges"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fm-criterion-fault-plane"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fm-criterion-gap"
        },
        {
          "row_index": 156,
          "witness_key": "obs:fm-criterion-misfit"
        },
        {
          "row_index": 157,
          "witness_key": "obs:fm-criterion-polarities"
        },
        {
          "row_index": 158,
          "witness_key": "obs:fm-criterion-probability"
        },
        {
          "row_index": 159,
          "witness_key": "obs:fm-criterion-station-ratio"
        },
        {
          "row_index": 160,
          "witness_key": "obs:fraction-meeting-two-criteria"
        },
        {
          "row_index": 161,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 162,
          "witness_key": "obs:high-frequency-energy-threshold"
        },
        {
          "row_index": 163,
          "witness_key": "obs:horizontal-uncertainty-catalog"
        },
        {
          "row_index": 164,
          "witness_key": "obs:iceland-magmatic-tectonic-depths"
        },
        {
          "row_index": 165,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 166,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 167,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 168,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 169,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 170,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 171,
          "witness_key": "obs:min-obs-per-detection"
        },
        {
          "row_index": 172,
          "witness_key": "obs:min-obs-per-relocated-event"
        },
        {
          "row_index": 173,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 174,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 175,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 176,
          "witness_key": "obs:profile-marker-interval"
        },
        {
          "row_index": 177,
          "witness_key": "obs:pwave-velocity-fastest-model"
        },
        {
          "row_index": 178,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 179,
          "witness_key": "obs:rms-residual-catalog"
        },
        {
          "row_index": 180,
          "witness_key": "obs:rms-residual-relocated"
        },
        {
          "row_index": 181,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 182,
          "witness_key": "obs:station-gap-catalog"
        },
        {
          "row_index": 183,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 184,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 185,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 186,
          "witness_key": "obs:uncertainty-relocated"
        },
        {
          "row_index": 187,
          "witness_key": "obs:velest-max-gap"
        },
        {
          "row_index": 188,
          "witness_key": "obs:velest-min-arrivals"
        },
        {
          "row_index": 189,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 190,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 191,
          "witness_key": "obs:vpvs-ratio"
        },
        {
          "row_index": 192,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 193,
          "witness_key": "obs:young-crust-age-threshold"
        },
        {
          "row_index": 194,
          "witness_key": "rel:corrugated-surface-part-of-occ"
        },
        {
          "row_index": 195,
          "witness_key": "rel:mar-within-equatorial-atlantic"
        },
        {
          "row_index": 196,
          "witness_key": "rel:ntd2-faults-within"
        },
        {
          "row_index": 197,
          "witness_key": "rel:occ-cut-by-normal-faults"
        },
        {
          "row_index": 198,
          "witness_key": "rel:rc1-bounded-by-detachment"
        },
        {
          "row_index": 199,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 200,
          "witness_key": "rel:rc2-bounded-by-inward-faults"
        },
        {
          "row_index": 201,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 202,
          "witness_key": "claim:analyzed-rc2-rc3-samples"
        },
        {
          "row_index": 203,
          "witness_key": "claim:ascending-melt-resides-in-mantle"
        },
        {
          "row_index": 204,
          "witness_key": "claim:co2-influences-melt-at-lab"
        },
        {
          "row_index": 205,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 206,
          "witness_key": "claim:crust-formed-by-mantle-melt"
        },
        {
          "row_index": 207,
          "witness_key": "claim:deep-earthquakes-along-transform-faults"
        },
        {
          "row_index": 208,
          "witness_key": "claim:deep-eq-aligned-n150e"
        },
        {
          "row_index": 209,
          "witness_key": "claim:deep-eq-interpreted-as-degassing"
        },
        {
          "row_index": 210,
          "witness_key": "claim:deep-events-not-location-artifact"
        },
        {
          "row_index": 211,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 212,
          "witness_key": "claim:deep-microseismicity-related-to-co2-degassing"
        },
        {
          "row_index": 213,
          "witness_key": "claim:degassing-causes-deep-earthquakes"
        },
        {
          "row_index": 214,
          "witness_key": "claim:degassing-volume-change-triggers-earthquakes"
        },
        {
          "row_index": 215,
          "witness_key": "claim:detachment-fault-inactive"
        },
        {
          "row_index": 216,
          "witness_key": "claim:earthquakes-occur-in-mantle"
        },
        {
          "row_index": 217,
          "witness_key": "claim:enrichment-from-low-degree-melting"
        },
        {
          "row_index": 218,
          "witness_key": "claim:estimated-primary-melt-co2-on-maps"
        },
        {
          "row_index": 219,
          "witness_key": "claim:fastest-model-shallow-events"
        },
        {
          "row_index": 220,
          "witness_key": "claim:faults-favor-melt-migration"
        },
        {
          "row_index": 221,
          "witness_key": "claim:fig3-transects"
        },
        {
          "row_index": 222,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 223,
          "witness_key": "claim:fig6-brittle-ductile-patches"
        },
        {
          "row_index": 224,
          "witness_key": "claim:hummocky-seafloor-and-cones"
        },
        {
          "row_index": 225,
          "witness_key": "claim:iceland-mayotte-contexts-differ"
        },
        {
          "row_index": 226,
          "witness_key": "claim:magmatic-tectonic-hypothesis"
        },
        {
          "row_index": 227,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "claim:mantle-beneath-rc2-is-hot"
        },
        {
          "row_index": 229,
          "witness_key": "claim:max-depth-does-not-follow-spreading-rate"
        },
        {
          "row_index": 230,
          "witness_key": "claim:melt-freezes-at-lithosphere-base"
        },
        {
          "row_index": 231,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 232,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 233,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 234,
          "witness_key": "claim:normal-vpvs-in-rc2"
        },
        {
          "row_index": 235,
          "witness_key": "claim:offaxis-magmatism-in-crust"
        },
        {
          "row_index": 236,
          "witness_key": "claim:pre-eruptive-co2-estimated"
        },
        {
          "row_index": 237,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 238,
          "witness_key": "claim:rainbow-at-ntd"
        },
        {
          "row_index": 239,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 240,
          "witness_key": "claim:rc1-exhumed-mantle"
        },
        {
          "row_index": 241,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 242,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 243,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 244,
          "witness_key": "claim:ridge-axis-relocating"
        },
        {
          "row_index": 245,
          "witness_key": "claim:shallow-eq-from-high-angle-faults"
        },
        {
          "row_index": 246,
          "witness_key": "claim:shear-zone-hypothesis"
        },
        {
          "row_index": 247,
          "witness_key": "claim:small-pressure-increase-induces-earthquakes"
        },
        {
          "row_index": 248,
          "witness_key": "claim:southern-flank-crust-free"
        },
        {
          "row_index": 249,
          "witness_key": "claim:transform-faults-in-equatorial-atlantic"
        },
        {
          "row_index": 250,
          "witness_key": "claim:ultraslow-ridges-high-co2"
        },
        {
          "row_index": 251,
          "witness_key": "claim:updated-compiled-data"
        },
        {
          "row_index": 252,
          "witness_key": "claim:velocity-model-set"
        },
        {
          "row_index": 253,
          "witness_key": "claim:volatiles-flush-melt-to-lab"
        },
        {
          "row_index": 254,
          "witness_key": "claim:zero-position-is-rti"
        },
        {
          "row_index": 255,
          "witness_key": "claim:morb-samples-rc2-rc3"
        },
        {
          "row_index": 256,
          "witness_key": "claim:ratios-are-good-proxy"
        },
        {
          "row_index": 257,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 258,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 259,
          "witness_key": "obs:brittle-lithosphere-thickness-ntds"
        },
        {
          "row_index": 260,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 261,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 262,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 263,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 264,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 265,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 266,
          "witness_key": "obs:co2-primary-melt-abstract"
        },
        {
          "row_index": 267,
          "witness_key": "obs:co2-primary-melt-rc2-floor"
        },
        {
          "row_index": 268,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 269,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 270,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 271,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 272,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 273,
          "witness_key": "obs:coverage-romanche-tf"
        },
        {
          "row_index": 274,
          "witness_key": "obs:crust-age-western-flank"
        },
        {
          "row_index": 275,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 276,
          "witness_key": "obs:crust-thickness-western-flank"
        },
        {
          "row_index": 277,
          "witness_key": "obs:deep-eq-depth-abstract"
        },
        {
          "row_index": 278,
          "witness_key": "obs:deep-eq-depth-bsf"
        },
        {
          "row_index": 279,
          "witness_key": "obs:deep-eq-rc2-axis"
        },
        {
          "row_index": 280,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 281,
          "witness_key": "obs:degassing-earthquake-depth-range"
        },
        {
          "row_index": 282,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 283,
          "witness_key": "obs:equatorial-atlantic-co2-average"
        },
        {
          "row_index": 284,
          "witness_key": "obs:equatorial-atlantic-co2-max"
        },
        {
          "row_index": 285,
          "witness_key": "obs:lithosphere-age-cold-edge"
        },
        {
          "row_index": 286,
          "witness_key": "obs:mantle-temperature-gt-1100"
        },
        {
          "row_index": 287,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 288,
          "witness_key": "obs:mar-segment-length-romanche-chain"
        },
        {
          "row_index": 289,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 290,
          "witness_key": "obs:no-earthquakes-below-20km"
        },
        {
          "row_index": 291,
          "witness_key": "obs:normal-depth-eq-ntd2"
        },
        {
          "row_index": 292,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 293,
          "witness_key": "obs:ntd2-eq-depth-down-to"
        },
        {
          "row_index": 294,
          "witness_key": "obs:ntd2-max-eq-depth"
        },
        {
          "row_index": 295,
          "witness_key": "obs:ntd2-ridge-offset"
        },
        {
          "row_index": 296,
          "witness_key": "obs:occ-max-eq-depth"
        },
        {
          "row_index": 297,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 298,
          "witness_key": "obs:pre-eruptive-co2-rc2"
        },
        {
          "row_index": 299,
          "witness_key": "obs:rc2-ba-enrichment"
        },
        {
          "row_index": 300,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 301,
          "witness_key": "obs:rc2-median-valley-width"
        },
        {
          "row_index": 302,
          "witness_key": "obs:rc2-rb-enrichment"
        },
        {
          "row_index": 303,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 304,
          "witness_key": "obs:shallow-eq-depth-rti"
        },
        {
          "row_index": 305,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 306,
          "witness_key": "obs:temperature-10-20km"
        },
        {
          "row_index": 307,
          "witness_key": "obs:transect-half-width"
        },
        {
          "row_index": 308,
          "witness_key": "obs:volatile-melting-initiation-depth"
        },
        {
          "row_index": 309,
          "witness_key": "claim:obs-experiment-conducted"
        },
        {
          "row_index": 310,
          "witness_key": "claim:thanks-to-cruise-party"
        },
        {
          "row_index": 311,
          "witness_key": "claim:amplitude-from-wood-anderson"
        },
        {
          "row_index": 312,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 313,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 314,
          "witness_key": "claim:melt-at-lab-from-co2-and-h2o"
        },
        {
          "row_index": 315,
          "witness_key": "claim:morb-compiled-from-petdb"
        },
        {
          "row_index": 316,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 317,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 318,
          "witness_key": "obs:bdb-depth-offaxis"
        },
        {
          "row_index": 319,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 320,
          "witness_key": "obs:lab-subsolidus-temperature"
        },
        {
          "row_index": 321,
          "witness_key": "obs:lab-water-content"
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

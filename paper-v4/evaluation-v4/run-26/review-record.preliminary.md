# Malleus paper v4 source-grounded review record, protocol v3.2

This is run-26's blank record, written by
`paper-v4/evaluation-v4/run-26/build_review_inputs.py` from the frozen v3
template under protocol v3.2. The question ids are this cell's frozen
competency question file's, in that file's order. The row and witness counts
are figures of a producer that has not run and are filled by the same script
at freeze; no other placeholder survives either stage.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

The `questions` block below carries one entry per question of the cell's
competency question file, 30 of them, in that file's order. Write one
`witnesses` entry per distinct witness the query result returns,
547 in all, and reference it from every row that shares it.
Rows: 148 rows for `CQ-T1-01`, 148 for `CQ-T1-02`, 247 for `CQ-T1-03`, 97 for
`CQ-T1-04`, 148 for `CQ-T1-05`, 158 for `CQ-T2-01`, 266 for `CQ-T2-02`, 296
for `CQ-T2-03`, 455 for `CQ-T2-04`, 31 for `CQ-T2-05`, 299 for `CQ-T3-01`,
312 for `CQ-T3-02`, 312 for `CQ-T3-03`, 260 for `CQ-T3-04`, 253 for
`CQ-T3-05`, 168 for `CQ-T4-01`, 168 for `CQ-T4-02`, 121 for `CQ-T4-03`, 296
for `CQ-T4-04`, 91 for `CQ-T4-05`, 226 for `CQ-T5-01`, 312 for `CQ-T5-02`,
299 for `CQ-T5-03`, 248 for `CQ-T5-04`, 299 for `CQ-T5-05`, 237 for
`CQ-C-01`, 229 for `CQ-C-02`, 455 for `CQ-C-03`, 148 for `CQ-C-04`, 312 for
`CQ-C-05`,
7039 in all.

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
  "schema": "malleus.paper-v4.source-grounded-review/v3.2",
  "status": "PRELIMINARY_COMPLETE",
  "inputs": {
    "review_protocol_sha256": "sha256:5dfd59f4aa479dd72738e2eb55653ee3e84e60886de4cccbcc0a8e66d06e55cd",
    "review_input_manifest_sha256": "sha256:513351036975caf90e2845820b4b9a7364d3502f6a216ec45df15ecd3bda7a64"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-26",
    "completed_at": "2026-09-12T06:56:05Z"
  },
  "witnesses": [
    {
      "witness_key": "material:melt",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this material. Its MELT kind is what the block is talking about. All 6 blocks the derivations reach are cited.",
      "source_locators": [
        "page:1:block:001",
        "page:1:block:003",
        "page:5:block:002",
        "page:5:block:003",
        "page:6:block:001",
        "page:7:block:012"
      ]
    },
    {
      "witness_key": "material:melt:primary",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This material is named in the block. Its MELT kind is what the block is talking about, and the block says which stage of the melt it means, which is the stage the row records. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:1:block:001",
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "material:melt:primitive",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The material the row projects appears there by name. Its MELT kind is what the block is talking about, and the block says which stage of the melt it means, which is the stage the row records.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "melt:pre-eruptive-rc2",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this material. Its MELT kind is what the block is talking about, and the block says which stage of the melt it means, which is the stage the row records.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "melt:rc2-calculated",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This material is named in the block. Its MELT kind is what the block is talking about, and the block says which stage of the melt it means, which is the stage the row records.",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "sample:basaltic-rocks",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this sample material, and that sentence is where the row's fields come from.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "sample:morb",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this sample material and describes where it comes from, and that sentence is where the row's fields come from. All 3 blocks the derivations reach are cited.",
      "source_locators": [
        "page:5:block:004",
        "page:6:block:005",
        "page:8:block:005"
      ]
    },
    {
      "witness_key": "sample:rock-samples",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this sample material and describes where it comes from, and that sentence is where the row's fields come from.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "claim:bg:deeper-eq-observed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its BACKGROUND kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "claim:bg:max-depth-factors",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "claim:categories-ab-good",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The claim the record stands for is the one the block makes. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "claim:category-definitions",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "claim:contexts-different",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:copyright",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The claim the record stands for is the one the block makes. Its BACKGROUND kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:11:block:006"
      ]
    },
    {
      "witness_key": "claim:deepest-documented",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:degassing-volume-change",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "claim:depths-not-artifact",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The claim the record stands for is the one the block makes. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:fig3-transect-halfwidth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:4:block:006"
      ]
    },
    {
      "witness_key": "claim:fixed-depth-worse-rms",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its INTERPRETATION kind and MEASURED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:001"
      ]
    },
    {
      "witness_key": "claim:focal-mechanisms-not-robust",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The claim the record stands for is the one the block makes. Its LIMITATION kind and NEGATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "claim:h-magmatic-tectonic",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its HYPOTHESIS kind and HYPOTHESISED modality match how the block puts it, and the disposition NOT_SUPPORTED matches the way the block disposes of the hypothesis. The projection carries no subject slot, so there is no subject to look for in the block. All 3 blocks the derivations reach are cited.",
      "source_locators": [
        "page:4:block:002",
        "page:4:block:003",
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "claim:long-period-events",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its HYPOTHESIS kind and HYPOTHESISED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "claim:magmatic-tectonic-eruptions",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The claim the record stands for is the one the block makes. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:max-depth-influences",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "claim:max-depth-not-following",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its INTERPRETATION kind and NEGATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "claim:max-depth-selection",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The claim the record stands for is the one the block makes. Its LIMITATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "claim:mechanism-similar-volcanoes",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "claim:melt-movement-not-applicable",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its INTERPRETATION kind and NEGATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "claim:melt-movement-strain",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The claim the record stands for is the one the block makes. Its BACKGROUND kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "claim:model1-inappropriate",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its INTERPRETATION kind and NEGATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "claim:more-events-needed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its LIMITATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "claim:no-competing-interests",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The claim the record stands for is the one the block makes. Its BACKGROUND kind and NEGATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:10:block:047"
      ]
    },
    {
      "witness_key": "claim:ntd1-origin",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:offaxis-magmatism",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "claim:peer-review",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The claim the record stands for is the one the block makes. Its BACKGROUND kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:11:block:003"
      ]
    },
    {
      "witness_key": "claim:perturbed-models-deep-events",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "claim:publisher-note",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its BACKGROUND kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:11:block:004"
      ]
    },
    {
      "witness_key": "claim:rc1-tectonic-origin",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The claim the record stands for is the one the block makes. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:samples-degassed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its INTERPRETATION kind and CALCULATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "claim:shear-zone-with-detachments",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its BACKGROUND kind and HYPOTHESISED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "claim:snapshot-limitation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The claim the record stands for is the one the block makes. Its LIMITATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "claim:trace-element-assumption",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its LIMITATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "claim:ultraslow-co2-high",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its IMPLICATION kind and HYPOTHESISED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "claim:volatiles-control-magma",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The claim the record stands for is the one the block makes. Its BACKGROUND kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:002"
      ]
    },
    {
      "witness_key": "claim:volatiles-extend-melting-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the record names is the claim the block puts forward. Its IMPLICATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "claim:vp-vs-reasonable",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the claim this record stands for. Its INTERPRETATION kind and STATED modality match how the block puts it. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:003"
      ]
    },
    {
      "witness_key": "cnt:catalog-links",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the block states is the count together with what is being counted. The figure is written out in words there, or is the number of items the block enumerates. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "cnt:criterion-arrivals",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The count and its scope are both stated in the block. The figure appears there as a digit. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "cnt:forced-depth-tests",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the count and the thing counted. The figure is written out in words there, or is the number of items the block enumerates. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "cnt:hypodd-iterations",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the block states is the count together with what is being counted. The figure is written out in words there, or is the number of items the block enumerates. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "cnt:identified-earthquakes",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The count and its scope are both stated in the block. The figure appears there as a digit. The scope wording the row projects follows what the block counts, and the determination token DERIVED matches how the block says the number was arrived at, with modality MEASURED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "cnt:located-earthquakes-methods",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the count and the thing counted. The figure appears there as a digit. The scope wording the row projects follows what the block counts, and the determination token DERIVED matches how the block says the number was arrived at, with modality MEASURED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:6:block:005"
      ]
    },
    {
      "witness_key": "cnt:location-categories",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the block states is the count together with what is being counted. The figure is written out in words there, or is the number of items the block enumerates. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "cnt:magnitude-groups",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The count and its scope are both stated in the block. The figure is written out in words there, or is the number of items the block enumerates. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "cnt:min-obs-per-event",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the count and the thing counted. The figure is written out in words there, or is the number of items the block enumerates. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "cnt:min-obs-relocated",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the block states is the count together with what is being counted. The figure appears there as a digit. The scope wording the row projects follows what the block counts, with modality MEASURED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "cnt:new-focal-mechanisms",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The count and its scope are both stated in the block. The figure is written out in words there, or is the number of items the block enumerates. The scope wording the row projects follows what the block counts, and the determination token DERIVED matches how the block says the number was arrived at, with modality MEASURED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "cnt:polarity-criterion",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the count and the thing counted. The figure appears there as a digit. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "cnt:relocated-events",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the block states is the count together with what is being counted. The figure appears there as a digit. The scope wording the row projects follows what the block counts, and the determination token DERIVED matches how the block says the number was arrived at, with modality MEASURED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "cnt:sub-dataset-arrivals",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The count and its scope are both stated in the block. The figure appears there as a digit. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "cnt:subsections",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the count and the thing counted. The figure is written out in words there, or is the number of items the block enumerates. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "cnt:total-focal-mechanisms",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the block states is the count together with what is being counted. The figure is written out in words there, or is the number of items the block enumerates. The scope wording the row projects follows what the block counts, and the determination token DERIVED matches how the block says the number was arrived at, with modality MEASURED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "cnt:well-relocated",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The count and its scope are both stated in the block. The figure appears there as a digit. The scope wording the row projects follows what the block counts, and the determination token DERIVED matches how the block says the number was arrived at, with modality MEASURED matching the capture. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "obs:axial-event-depth-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "obs:dry-melting-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "obs:expected-depth-slow",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_upper, unit, depth_reference, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination MODELLED, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "obs:expected-depth-ultraslow",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_upper, unit, depth_reference, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination MODELLED, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "obs:expected-max-depth-32",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:fig3-deep-shading",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_lower, unit, quantity_kind agree with it, and the qualification token OPEN_LOWER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:4:block:007"
      ]
    },
    {
      "witness_key": "obs:fig3-shallow-shading",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:4:block:007"
      ]
    },
    {
      "witness_key": "obs:onset-volatile-melting-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "obs:saturation-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, with determination MODELLED, modality CALCULATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "obs:average-depth-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "obs:avg-horizontal-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "obs:b-value",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_lower, value_upper, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination DERIVED, modality CALCULATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "obs:brittle-thickness-expected",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:brittle-thickness-ntds",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:criterion-azimuthal-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "obs:criterion-s-distance",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_lower, value_upper, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "obs:crustal-age-offaxis",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:depth-uncertainty-bound",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:error-ellipsoid-confidence",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:005"
      ]
    },
    {
      "witness_key": "obs:fm-azimuthal-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fm-fault-plane-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fm-misfit",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fm-probability",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, unit, quantity_kind agree with it, and the qualification token OPEN_LOWER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fm-station-ratio",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_lower, quantity_kind agree with it, and the qualification token OPEN_LOWER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fraction-two-criteria",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "obs:full-spreading-rate",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:group-b-values",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_lower, value_upper, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination DERIVED, modality CALCULATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "obs:horizontal-uncertainty-bound",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:instrument-spacing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "obs:isotherm-750",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "obs:lithospheric-age-contour",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "obs:low-frequency-cutoff",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, unit, quantity_kind agree with it, and the qualification token OPEN_LOWER_BOUND matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "obs:magnitude-completeness",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_lower, value_upper, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination DERIVED, modality CALCULATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "obs:max-event-separation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "obs:mean-horizontal-error",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:mean-vertical-error",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:model1-pwave-velocity",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_lower, unit, quantity_kind agree with it, and the qualification token OPEN_LOWER_BOUND matches the way the block bounds the value, with determination MODELLED, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "obs:pore-pressure-trigger",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "obs:profile-halfwidth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:3:block:005"
      ]
    },
    {
      "witness_key": "obs:quality-abc-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "obs:quality-d-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "obs:recording-duration",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "obs:relocated-azimuthal-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "obs:relocated-rms",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "obs:relocated-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "obs:rms-residual-bound",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:saturation-pressure",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, with determination MODELLED, modality CALCULATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "obs:saturation-temperature",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination MODELLED, modality CALCULATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "obs:solubility-model-temperature",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality CALCULATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "obs:station-gap-bound",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:sub-dataset-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "obs:subsection-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "obs:temp-below-20km",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, unit, quantity_kind agree with it, and the qualification token OPEN_LOWER_BOUND matches the way the block bounds the value, with determination MODELLED, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:5:block:007"
      ]
    },
    {
      "witness_key": "obs:updated-horizontal-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, with determination DERIVED, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "obs:velocity-perturbation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "obs:vp-vs-test-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected value_lower, value_upper, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:002"
      ]
    },
    {
      "witness_key": "obs:young-crust-age",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "ratio:vp-vs",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected ratio_value agree with it, and the qualification token it records matches the way the block bounds the value, modality MEASURED. The projection carries no subject slot, so there is no subject to look for in the block.",
      "source_locators": [
        "page:7:block:002"
      ]
    },
    {
      "witness_key": "claim:bg:melt-focusing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "claim:bg:migration-not-understood",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its BACKGROUND kind and NEGATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:1:block:003"
      ]
    },
    {
      "witness_key": "claim:bg:migration-unknown",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its BACKGROUND kind and NEGATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "claim:continued-degassing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its INTERPRETATION kind and HYPOTHESISED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "claim:fig5-estimated-primary",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its INTERPRETATION kind and CALCULATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:6:block:005"
      ]
    },
    {
      "witness_key": "claim:implication:lab-melt",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its IMPLICATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "claim:melt-resides-fractionates",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "claim:primary-vs-pre-eruptive",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "obs:abstract:co2-primary",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "obs:co2-ba90-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination ESTIMATED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "obs:co2-calculated-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination DERIVED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "obs:co2-primary-rc2-floor",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, unit, quantity_kind agree with it, and the qualification token OPEN_LOWER_BOUND matches the way the block bounds the value, with determination ESTIMATED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "obs:co2-rb90-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination ESTIMATED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "claim:model5-best-fitting",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "claim:selected-model-more-events",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "claim:axis-relocating",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "claim:bdb-shallower-southward",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:bg:melt-lens-bdb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "claim:bg:tf-deep-eq",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "claim:bg:volatile-role",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "claim:co2-behaves-incompatible",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "claim:co2-degassing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its HYPOTHESIS kind and HYPOTHESISED modality match how the block puts it, and the disposition PREFERRED matches the way the block disposes of the hypothesis. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002"
      ]
    },
    {
      "witness_key": "claim:co2-solubility-pressure",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "claim:deep-eq-alignment",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its INTERPRETATION kind and MEASURED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:deep-events-well-constrained",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:8:block:001"
      ]
    },
    {
      "witness_key": "claim:detachment-inactive",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "claim:enriched-source-interpretation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "claim:eq-in-mantle",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:faults-favor-migration",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:fig6-interpretation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:7:block:012"
      ]
    },
    {
      "witness_key": "claim:h-cold-lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its HYPOTHESIS kind and HYPOTHESISED modality match how the block puts it, and the disposition NOT_SUPPORTED matches the way the block disposes of the hypothesis. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "claim:h-hydrothermal",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its HYPOTHESIS kind and HYPOTHESISED modality match how the block puts it, and the disposition NOT_SUPPORTED matches the way the block disposes of the hypothesis. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "claim:h-shear-zone",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its HYPOTHESIS kind and HYPOTHESISED modality match how the block puts it, and the disposition NOT_SUPPORTED matches the way the block disposes of the hypothesis. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "claim:keller-volatile-flushing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "claim:lab-melt-co2-h2o",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its INTERPRETATION kind and HYPOTHESISED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "claim:magmatism-dominates",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "claim:measurements-near-solubility",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its INTERPRETATION kind and MEASURED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "claim:melt-freeze-lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its IMPLICATION kind and HYPOTHESISED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "claim:no-active-vents-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its INTERPRETATION kind and NEGATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "claim:no-current-eruption",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its INTERPRETATION kind and NEGATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:no-eq-below-20",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its INTERPRETATION kind and NEGATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:007"
      ]
    },
    {
      "witness_key": "claim:obs-no-data",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its LIMITATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "claim:occ-recent-deformation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:occ-shallow-ruptures",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "claim:ratios-good-proxy",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "claim:rc1-amagmatic",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "claim:rc2-magmatic-origin",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "claim:rc2-magmatically-robust",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:rc2-mantle-hot",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its INTERPRETATION kind and CALCULATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "claim:rc2-no-detachment",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its INTERPRETATION kind and NEGATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:4:block:001"
      ]
    },
    {
      "witness_key": "claim:rc3-magmatic",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:seafloor-basalts-degassed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its INTERPRETATION kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "claim:small-pressure-induces",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the record names is the claim the block puts forward. Its HYPOTHESIS kind and HYPOTHESISED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "claim:tomography-normal-vpvs",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the claim this record stands for. Its BACKGROUND kind and STATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:7:block:003"
      ]
    },
    {
      "witness_key": "claim:vent-field-too-far",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim the record stands for is the one the block makes. Its INTERPRETATION kind and NEGATED modality match how the block puts it. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "cnt:velocity-models",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The count and its scope are both stated in the block. The figure is written out in words there, or is the number of items the block enumerates. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "cnt:events-mar",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the count and the thing counted. The figure appears there as a digit. The scope wording the row projects follows what the block counts, and the determination token DERIVED matches how the block says the number was arrived at, with modality MEASURED matching the capture. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "cnt:events-romanche",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the block states is the count together with what is being counted. The figure appears there as a digit. The scope wording the row projects follows what the block counts, and the determination token DERIVED matches how the block says the number was arrived at, with modality MEASURED matching the capture. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "cnt:located-earthquakes",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The count and its scope are both stated in the block. The figure appears there as a digit. The scope wording the row projects follows what the block counts, and the determination token DERIVED matches how the block says the number was arrived at, with modality MEASURED matching the capture. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "cnt:obs-deployed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the count and the thing counted. The figure appears there as a digit. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "cnt:obs-deployed-methods",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the block states is the count together with what is being counted. The figure appears there as a digit. The scope wording the row projects follows what the block counts, with modality STATED matching the capture. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "cnt:useful-obs",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The count and its scope are both stated in the block. The figure appears there as a digit. The scope wording the row projects follows what the block counts, with modality MEASURED matching the capture. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "obs:velocity-constraint-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_upper, unit, depth_reference, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "obs:abstract:deep-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it. A gap is declared on the evidence this record rests on, of kind REQUIRED_FIELD_ABSENT_IN_SOURCE; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "obs:bdb-depth-if-cold",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality HYPOTHESISED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:bdb-depth-ntd2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:bdb-shallow-offaxis",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:deep-eq-bsf",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, depth_reference, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination MEASURED, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:7:block:012"
      ]
    },
    {
      "witness_key": "obs:deep-eq-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:deep-microseismicity-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "obs:depth-under-ntd2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:depth-under-occ",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:iceland-depths",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, unit, quantity_kind agree with it, and the qualification token OPEN_LOWER_BOUND matches the way the block bounds the value. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "obs:mayotte-depths",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, unit, quantity_kind agree with it, and the qualification token OPEN_LOWER_BOUND matches the way the block bounds the value. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "obs:normal-depth-ntd2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "obs:ntd2-eq-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:offaxis-shallow-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:offaxis-swarm-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "obs:shallow-eq-rti",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "obs:western-cluster-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it. A gap is declared on the evidence this record rests on, of kind TYPE_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:ba-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, unit, quantity_kind agree with it, and the qualification token OPEN_LOWER_BOUND matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "obs:bdb-isotherm-temp",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, uncertainty, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "obs:co2-atlantic-average",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "obs:co2-atlantic-max",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "obs:co2-ba-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination ESTIMATED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-ba-rc3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination ESTIMATED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-ba90-rc3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination ESTIMATED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "obs:co2-calculated-rc3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination DERIVED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "obs:co2-loss-fraction",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "obs:co2-pre-eruptive-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination ESTIMATED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-rb-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination ESTIMATED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-rb-rc3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination ESTIMATED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-rb90-rc3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination ESTIMATED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "obs:co2-swir-highest",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "obs:cold-lithosphere-age",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:coverage-mar-axis",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "obs:coverage-romanche",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "obs:crust-thickness-fig6",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, uncertainty, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "obs:crust-thickness-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, uncertainty, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:hot-mantle-temp",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, unit, quantity_kind agree with it, and the qualification token OPEN_LOWER_BOUND matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "obs:isotherm-600-800",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality HYPOTHESISED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:lab-melt-fraction",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, with determination MODELLED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "obs:lab-water-content",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_upper, unit, quantity_kind agree with it, and the qualification token OPEN_UPPER_BOUND matches the way the block bounds the value, with determination MODELLED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "obs:mar-half-spreading-rate",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "obs:mar-segment-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "obs:median-valley-width",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:ntd1-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:ntd2-offset",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:rb-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, unit, quantity_kind agree with it, and the qualification token OPEN_LOWER_BOUND matches the way the block bounds the value, with determination MEASURED, modality MEASURED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "obs:rc2-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:rc3-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:study-area-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it. A gap is declared on the evidence this record rests on, of kind AGGREGATE_ONLY; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "obs:subsolidus-temp",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token APPROXIMATE matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "obs:temp-10-20km",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the quantity this record carries. The projected value_lower, value_upper, unit, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, with determination MODELLED, modality CALCULATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "ratio:co2-ba",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The quantity the record carries is stated in the block. The projected uncertainty, ratio_value agree with it, and the qualification token it records matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "ratio:co2-rb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK What the row projects is a quantity the block states outright. The projected uncertainty, ratio_value agree with it, and the qualification token it records matches the way the block bounds the value, modality STATED. The subject the row resolves to is named in the block, by its own name or by one of the wordings the record keeps for it. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "event:romanche-2016",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the quantity this record carries. The projected value_lower, value_upper, quantity_kind agree with it, and the qualification token EXACT matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block. A gap is declared on the evidence this record rests on, of kind INTERVAL_NOT_EXPRESSIBLE; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "event:romanche-2016:sub1",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The quantity the record carries is stated in the block. The projected fields agree with it, and the qualification token it records matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block. A gap is declared on the evidence this record rests on, of kind INTERVAL_NOT_EXPRESSIBLE; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "event:romanche-2016:sub2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW What the row projects is a quantity the block states outright. The projected fields agree with it, and the qualification token it records matches the way the block bounds the value, modality STATED. The projection carries no subject slot, so there is no subject to look for in the block. A gap is declared on the evidence this record rests on, of kind INTERVAL_NOT_EXPRESSIBLE; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "work:ref:01",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:8:block:012",
        "page:8:block:013"
      ]
    },
    {
      "witness_key": "work:ref:02",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:8:block:014"
      ]
    },
    {
      "witness_key": "work:ref:03",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:8:block:015"
      ]
    },
    {
      "witness_key": "work:ref:04",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:8:block:016"
      ]
    },
    {
      "witness_key": "work:ref:05",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:8:block:017"
      ]
    },
    {
      "witness_key": "work:ref:06",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:001",
        "page:9:block:002"
      ]
    },
    {
      "witness_key": "work:ref:07",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_pages, publication_year, doi, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:003",
        "page:9:block:004"
      ]
    },
    {
      "witness_key": "work:ref:08",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:005"
      ]
    },
    {
      "witness_key": "work:ref:09",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:006"
      ]
    },
    {
      "witness_key": "work:ref:10",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:007"
      ]
    },
    {
      "witness_key": "work:ref:11",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:008"
      ]
    },
    {
      "witness_key": "work:ref:12",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:009"
      ]
    },
    {
      "witness_key": "work:ref:13",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:010"
      ]
    },
    {
      "witness_key": "work:ref:14",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:011",
        "page:9:block:012"
      ]
    },
    {
      "witness_key": "work:ref:15",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:013"
      ]
    },
    {
      "witness_key": "work:ref:16",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_pages, publication_year, doi, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:014",
        "page:9:block:015"
      ]
    },
    {
      "witness_key": "work:ref:17",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:016"
      ]
    },
    {
      "witness_key": "work:ref:18",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:017",
        "page:9:block:018"
      ]
    },
    {
      "witness_key": "work:ref:19",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:019"
      ]
    },
    {
      "witness_key": "work:ref:20",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:020",
        "page:9:block:021"
      ]
    },
    {
      "witness_key": "work:ref:21",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_pages, publication_year, doi, is present in that entry.",
      "source_locators": [
        "page:9:block:022"
      ]
    },
    {
      "witness_key": "work:ref:22",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 4 projected fields, creators_as_stated, name, publication_year, doi, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:023",
        "page:9:block:024"
      ]
    },
    {
      "witness_key": "work:ref:23",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:025",
        "page:9:block:026"
      ]
    },
    {
      "witness_key": "work:ref:24",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:027",
        "page:9:block:028"
      ]
    },
    {
      "witness_key": "work:ref:25",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 5 projected fields, creators_as_stated, name, container_title, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:029"
      ]
    },
    {
      "witness_key": "work:ref:26",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:030"
      ]
    },
    {
      "witness_key": "work:ref:27",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_pages, publication_year, doi, is present in that entry.",
      "source_locators": [
        "page:9:block:031"
      ]
    },
    {
      "witness_key": "work:ref:28",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:031",
        "page:9:block:032"
      ]
    },
    {
      "witness_key": "work:ref:29",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:033"
      ]
    },
    {
      "witness_key": "work:ref:30",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:034"
      ]
    },
    {
      "witness_key": "work:ref:31",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:035"
      ]
    },
    {
      "witness_key": "work:ref:32",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:036"
      ]
    },
    {
      "witness_key": "work:ref:33",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:037",
        "page:9:block:038"
      ]
    },
    {
      "witness_key": "work:ref:34",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:039"
      ]
    },
    {
      "witness_key": "work:ref:35",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:040"
      ]
    },
    {
      "witness_key": "work:ref:36",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:041"
      ]
    },
    {
      "witness_key": "work:ref:37",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:042"
      ]
    },
    {
      "witness_key": "work:ref:38",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:043"
      ]
    },
    {
      "witness_key": "work:ref:39",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:044",
        "page:9:block:045"
      ]
    },
    {
      "witness_key": "work:ref:40",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:046",
        "page:9:block:047"
      ]
    },
    {
      "witness_key": "work:ref:41",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:048"
      ]
    },
    {
      "witness_key": "work:ref:42",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:049"
      ]
    },
    {
      "witness_key": "work:ref:43",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:050"
      ]
    },
    {
      "witness_key": "work:ref:44",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:051"
      ]
    },
    {
      "witness_key": "work:ref:45",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:052"
      ]
    },
    {
      "witness_key": "work:ref:46",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:9:block:053",
        "page:9:block:054"
      ]
    },
    {
      "witness_key": "work:ref:47",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:9:block:055"
      ]
    },
    {
      "witness_key": "work:ref:48",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:10:block:001",
        "page:9:block:056"
      ]
    },
    {
      "witness_key": "work:ref:49",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:002"
      ]
    },
    {
      "witness_key": "work:ref:50",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:003"
      ]
    },
    {
      "witness_key": "work:ref:51",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:10:block:004",
        "page:10:block:005"
      ]
    },
    {
      "witness_key": "work:ref:52",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:10:block:006",
        "page:10:block:007"
      ]
    },
    {
      "witness_key": "work:ref:53",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:008"
      ]
    },
    {
      "witness_key": "work:ref:54",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:009"
      ]
    },
    {
      "witness_key": "work:ref:55",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:010"
      ]
    },
    {
      "witness_key": "work:ref:56",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:011"
      ]
    },
    {
      "witness_key": "work:ref:57",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:012"
      ]
    },
    {
      "witness_key": "work:ref:58",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:10:block:013",
        "page:10:block:014"
      ]
    },
    {
      "witness_key": "work:ref:59",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:015"
      ]
    },
    {
      "witness_key": "work:ref:60",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:016"
      ]
    },
    {
      "witness_key": "work:ref:61",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:017"
      ]
    },
    {
      "witness_key": "work:ref:62",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:018"
      ]
    },
    {
      "witness_key": "work:ref:63",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:019"
      ]
    },
    {
      "witness_key": "work:ref:64",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:020"
      ]
    },
    {
      "witness_key": "work:ref:65",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:021"
      ]
    },
    {
      "witness_key": "work:ref:66",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:10:block:022",
        "page:10:block:023"
      ]
    },
    {
      "witness_key": "work:ref:67",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:024"
      ]
    },
    {
      "witness_key": "work:ref:68",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:025"
      ]
    },
    {
      "witness_key": "work:ref:69",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:026"
      ]
    },
    {
      "witness_key": "work:ref:70",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:10:block:027",
        "page:10:block:028"
      ]
    },
    {
      "witness_key": "work:ref:71",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:029"
      ]
    },
    {
      "witness_key": "work:ref:72",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:030"
      ]
    },
    {
      "witness_key": "work:ref:73",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 4 projected fields, creators_as_stated, name, publication_year, doi, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:10:block:031",
        "page:10:block:032",
        "page:10:block:033"
      ]
    },
    {
      "witness_key": "work:ref:74",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:034"
      ]
    },
    {
      "witness_key": "work:ref:75",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, publication_year, doi, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:10:block:035",
        "page:10:block:036"
      ]
    },
    {
      "witness_key": "work:ref:76",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:037"
      ]
    },
    {
      "witness_key": "work:ref:77",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block cited is the entry this work has in the article's reference list. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:10:block:038",
        "page:10:block:039"
      ]
    },
    {
      "witness_key": "work:ref:78",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This record rests on the reference-list entry the article gives the work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry.",
      "source_locators": [
        "page:10:block:040"
      ]
    },
    {
      "witness_key": "work:ref:79",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The derivation reaches the numbered reference-list entry for this work. Every one of the 6 projected fields, creators_as_stated, name, container_title, bibliographic_volume, bibliographic_pages, publication_year, is present in that entry across the two blocks the entry spans.",
      "source_locators": [
        "page:10:block:041",
        "page:10:block:042"
      ]
    },
    {
      "witness_key": "work:yu-2025",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This is the article itself, and its nine projected fields are derived from the title block, the dates panel, the running heads and the licence paragraph. Each of those blocks is cited and each carries the field it derives.",
      "source_locators": [
        "page:10:block:048",
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
        "page:8:block:018"
      ]
    },
    {
      "witness_key": "feature:askja",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its VOLCANO kind is what the block describes. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:4:block:002",
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "feature:atlantic",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its OCEAN_BASIN kind is what the block describes.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:axial-valley",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its AXIAL_VALLEY kind is what the block describes. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:2:block:005",
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "feature:axial-valley-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its NORMAL_FAULT kind is what the block describes.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "feature:bdb",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its STRUCTURAL_INTERFACE kind is what the block describes. A gap is declared on the evidence this record rests on, of kind REQUIRED_FIELD_ABSENT_IN_SOURCE; it concerns something the row does not project and leaves the judged fields untouched. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:1:block:001",
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "feature:chain-tf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its TRANSFORM_FAULT kind is what the block describes.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:detachment-rti",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its DETACHMENT_FAULT kind is what the block describes.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:extinct-vent-field",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its HYDROTHERMAL_VENT_FIELD kind is what the block describes.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "feature:fagradalsfjall",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its PENINSULA kind is what the block describes. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:4:block:002",
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "feature:gakkel",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its MID_OCEAN_RIDGE kind is what the block describes.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "feature:iceland",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its ISLAND kind is what the block describes.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "feature:inactive-mound",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its HYDROTHERMAL_MOUND kind is what the block describes, with the description following the same sentence.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "feature:indian-ocean",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its OCEAN_BASIN kind is what the block describes.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "feature:juan-de-fuca",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its TECTONIC_PLATE kind is what the block describes.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "feature:knipovich",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its MID_OCEAN_RIDGE kind is what the block describes.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "feature:lab",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its STRUCTURAL_INTERFACE kind is what the block describes.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "feature:lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its LITHOSPHERIC_LAYER kind is what the block describes. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:2:block:006",
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "feature:logachev",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its SEAMOUNT kind is what the block describes.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "feature:magma-reservoir",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its MAGMA_RESERVOIR kind is what the block describes.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "feature:mantle",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its LITHOSPHERIC_LAYER kind is what the block describes.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "feature:mar",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its MID_OCEAN_RIDGE kind is what the block describes. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "feature:mar-axis",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its RIDGE_AXIS kind is what the block describes. A gap is declared on the evidence this record rests on, of kind REQUIRED_FIELD_ABSENT_IN_SOURCE; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "feature:mar-segment",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its RIDGE_SEGMENT kind is what the block describes, with the description following the same sentence.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:mayotte",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its ISLAND kind is what the block describes. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:4:block:002",
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "feature:median-valley",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its AXIAL_VALLEY kind is what the block describes, with the description following the same sentence.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:melt-lens",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its MELT_LENS kind is what the block describes.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "feature:moho",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its STRUCTURAL_INTERFACE kind is what the block describes, with the description following the same sentence.",
      "source_locators": [
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "feature:neovolcanic-ridge",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its NEOVOLCANIC_RIDGE kind is what the block describes, and the orientation wording the row keeps is the block's own.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:ntd1",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its NON_TRANSFORM_DISCONTINUITY kind is what the block describes, and the orientation wording the row keeps is the block's own. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:ntd1-east-flank",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its RIDGE_FLANK kind is what the block describes.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "feature:ntd1-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its FAULT kind is what the block describes, and the orientation wording the row keeps is the block's own, with the description following the same sentence.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:ntd2",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its NON_TRANSFORM_DISCONTINUITY kind is what the block describes, and the orientation wording the row keeps is the block's own. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:ntd2-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its NORMAL_FAULT kind is what the block describes, and the orientation wording the row keeps is the block's own, with the description following the same sentence.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:occ",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its OCEANIC_CORE_COMPLEX kind is what the block describes. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:1:block:005",
        "page:4:block:006"
      ]
    },
    {
      "witness_key": "feature:occ-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its NORMAL_FAULT kind is what the block describes, and the orientation wording the row keeps is the block's own, with the description following the same sentence.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:oceanic-crust",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its LITHOSPHERIC_LAYER kind is what the block describes.",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "feature:rainbow",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its MASSIF kind is what the block describes. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "feature:rc1",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its RIDGE_SEGMENT kind is what the block describes, with the description following the same sentence.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:rc2",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its RIDGE_SEGMENT kind is what the block describes, with the description following the same sentence. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:rc2-axis",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its RIDGE_AXIS kind is what the block describes.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "feature:rc2-bounding-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its FAULT kind is what the block describes, and the orientation wording the row keeps is the block's own.",
      "source_locators": [
        "page:4:block:001"
      ]
    },
    {
      "witness_key": "feature:rc3",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its RIDGE_SEGMENT kind is what the block describes, and the orientation wording the row keeps is the block's own, with the description following the same sentence. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:romanche-tf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its TRANSFORM_FAULT kind is what the block describes.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:rti",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its RIDGE_TRANSFORM_INTERSECTION kind is what the block describes, with the description following the same sentence. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:1:block:005",
        "page:3:block:005"
      ]
    },
    {
      "witness_key": "feature:seafloor",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its SEAFLOOR kind is what the block describes.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "feature:shear-zones-tf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its SHEAR_ZONE kind is what the block describes. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:1:block:004",
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "feature:study-area",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its STUDY_AREA kind is what the block describes. A gap is declared on the evidence this record rests on, of kind AGGREGATE_ONLY; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:swir",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its MID_OCEAN_RIDGE kind is what the block describes. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:3:block:001",
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "feature:transform-valley",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The feature the row projects is named there. Its TRANSFORM_VALLEY kind is what the block describes.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "feature:volcanic-cones",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this feature. Its VOLCANIC_CONE kind is what the block describes. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:3:block:001",
        "page:4:block:007"
      ]
    },
    {
      "witness_key": "feature:western-flank",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW This feature is named in the block. Its RIDGE_FLANK kind is what the block describes.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-01",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:8:block:012"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-02",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:8:block:014"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-03",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:8:block:015"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-04",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:8:block:016"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-05",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:8:block:017"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-06",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:001"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-07",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:003"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-08",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:005"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-09",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:006"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-10",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:007"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-11",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:008"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-12",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:009"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-13",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:010"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-14",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:011"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-15",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:013"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-16",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:014"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-17",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:016"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-18",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:017"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-19",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:019"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-20",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:020"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-21",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:022"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-22",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:023"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-23",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:025"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-24",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:027"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-25",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:029"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-26",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:030"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-27",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:031"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-28",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:031"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-29",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:033"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-30",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:034"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-31",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:035"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-32",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:036"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-33",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:037"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-34",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:039"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-35",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:040"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-36",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:041"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-37",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:042"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-38",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:043"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-39",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:044"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-40",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:046"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-41",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:048"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-42",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:049"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-43",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:050"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-44",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:051"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-45",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:052"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-46",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:9:block:053"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-47",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:9:block:055"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-48",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:9:block:056"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-49",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:10:block:002"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-50",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:10:block:003"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-51",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:10:block:004"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-52",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:10:block:006"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-53",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:10:block:008"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-54",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:10:block:009"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-55",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:10:block:010"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-56",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:10:block:011"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-57",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:10:block:012"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-58",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:10:block:013"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-59",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:10:block:015"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-60",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:10:block:016"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-61",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:10:block:017"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-62",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:10:block:018"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-63",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:10:block:019"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-64",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:10:block:020"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-65",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:10:block:021"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-66",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:10:block:022"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-67",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:10:block:024"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-68",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:10:block:025"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-69",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:10:block:026"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-70",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:10:block:027"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-71",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:10:block:029"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-72",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:10:block:030"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-73",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:10:block:031"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-74",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:10:block:034"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-75",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:10:block:035"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-76",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:10:block:037"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-77",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL This row is a citation link of type REPORTED_BY, and the block it rests on is the numbered entry for that work in the article's own reference list. The same entry derives the target record, so the block that formalizes the link is also an endpoint block.",
      "source_locators": [
        "page:10:block:038"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-78",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The REPORTED_BY link between the article and this earlier work rests on the numbered entry the article's reference list gives it. Because that entry also derives the endpoint record, the formalizing block sits among the endpoint blocks.",
      "source_locators": [
        "page:10:block:040"
      ]
    },
    {
      "witness_key": "rel:yu-2025-cites-79",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block is the article's own reference-list entry for the target work, which is what a REPORTED_BY link between them rests on. That entry derives the endpoint as well, which is why the locality reads local.",
      "source_locators": [
        "page:10:block:041"
      ]
    },
    {
      "witness_key": "rel:axial-valley-cut-by-faults",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block names both features and the CUT_BY relation the row projects between them. The block also derives an endpoint record, so the relation is formalized locally.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "rel:mar-in-atlantic",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL A LOCATED_IN relation between the two named features is what the block states. The block also derives an endpoint record, so the relation is formalized locally.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:mar-segment-bounded-chain",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block gives both features and the BOUNDED_BY relation between them, qualifier included. It is also a block from which one of the endpoint records is derived.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:mar-segment-bounded-romanche",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block states this BOUNDED_BY relation between the two named features and carries the qualifier wording the row projects. It is also a block from which one of the endpoint records is derived.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:ntd1-part-of-study-area",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL A PART_OF relation between the two named features is what the block states. The block also derives an endpoint record, so the relation is formalized locally.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:ntd2-part-of-study-area",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL Both endpoints and the PART_OF relation between them are stated in the block. The block also derives an endpoint record, so the relation is formalized locally.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:occ-adjacent-axis",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block states this ADJACENT_TO relation between the two named features and carries the qualifier wording the row projects. It is also a block from which one of the endpoint records is derived.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:occ-cut-by-faults",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL A CUT_BY relation between the two features is stated in the block, together with the qualifier the row repeats. It is also a block from which one of the endpoint records is derived.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "rel:occ-on-outside-corner",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block gives both features and the LOCATED_IN relation between them, qualifier included. It is also a block from which one of the endpoint records is derived.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "rel:rainbow-at-ntd",
      "source_support": "PARTIAL",
      "rationale": "DERIVATION_LOCAL The block places the source feature at a non-transform discontinuity of an unnamed identity, so the LOCATED_IN type and the source endpoint hold but the particular target feature this row names is not settled there. The producer's own gap on that assertion says the same, and the endpoint blocks the target record carries are elsewhere in the reading, so the cited block supports part of the row and not all of it.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "rel:rc1-bounded-detachment",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL A BOUNDED_BY relation between the two features is stated in the block, together with the qualifier the row repeats. It is also a block from which one of the endpoint records is derived.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:rc1-part-of-study-area",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL Both endpoints and the PART_OF relation between them are stated in the block. The block also derives an endpoint record, so the relation is formalized locally.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:rc2-bounded-by-faults",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block names both features and the BOUNDED_BY relation the row projects between them. The block also derives an endpoint record, so the relation is formalized locally.",
      "source_locators": [
        "page:4:block:001"
      ]
    },
    {
      "witness_key": "rel:rc2-part-of-study-area",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL A PART_OF relation between the two named features is what the block states. The block also derives an endpoint record, so the relation is formalized locally.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:rc3-adjacent-ntd2",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block gives both features and the ADJACENT_TO relation between them, qualifier included. It is also a block from which one of the endpoint records is derived.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:study-area-in-mar-segment",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block states this LOCATED_IN relation between the two named features and carries the qualifier wording the row projects. It is also a block from which one of the endpoint records is derived.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:study-area-offset-ntd1",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block states that the studied stretch is offset by two discontinuities and, a little further on, names them one by one, so the OFFSET_BY relation and the particular target this row names both rest on the block that is cited. The producer's gap notes that the counting sentence alone does not name them; the naming sentence sits in the same block, and the block is the unit that is cited here.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:study-area-offset-ntd2",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block states that the studied stretch is offset by two discontinuities and, a little further on, names them one by one, so the OFFSET_BY relation and the particular target this row names both rest on the block that is cited. The producer's gap notes that the counting sentence alone does not name them; the naming sentence sits in the same block, and the block is the unit that is cited here.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:vent-field-on-ntd1-flank",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block names both features and the LOCATED_IN relation the row projects between them. The block also derives an endpoint record, so the relation is formalized locally.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "campaign:smarties",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The blocks name the cruise and say when it ran; the months the row records and the MONTH precision it declares follow those sentences. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:10:block:043",
        "page:10:block:044",
        "page:10:block:046",
        "page:2:block:002",
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "instrument:obs",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the instruments the recordings come from, which is all this row projects. A gap is declared on the evidence this record rests on, of kind REQUIRED_FIELD_ABSENT_IN_SOURCE; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "software:global-mapper",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this program and gives the address the row records.",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:gmt",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this program and gives the address the row records. The blocks where the program is used are cited alongside the availability block. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:8:block:010",
        "page:8:block:011"
      ]
    },
    {
      "witness_key": "software:hash",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this program and gives the address the row records, and the version appears in the same availability sentence. The blocks where the program is used are cited alongside the availability block. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:8:block:003",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:hypodd",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this program and gives the address the row records, and the version appears in the same availability sentence. The blocks where the program is used are cited alongside the availability block. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:7:block:006",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:nonlinloc",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this program and gives the address the row records. The blocks where the program is used are cited alongside the availability block. All 3 blocks the derivations reach are cited.",
      "source_locators": [
        "page:7:block:004",
        "page:7:block:005",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:seisan",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this program and gives the address the row records. The blocks where the program is used are cited alongside the availability block. All 3 blocks the derivations reach are cited.",
      "source_locators": [
        "page:6:block:002",
        "page:8:block:002",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:velest",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this program and gives the address the row records. The blocks where the program is used are cited alongside the availability block. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:6:block:004",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:zmap",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this program and gives the address the row records. The blocks where the program is used are cited alongside the availability block. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:8:block:002",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "rel:melt-from-mantle",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_NON_LOCAL The block states that the source material comes from the target layer and carries the setting qualifier the row projects, which is what a DERIVED_FROM link asserts. The block is not one of those deriving either endpoint record; that is a statement of where the link was formalized and it does not weaken the support the block gives.",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "rel:melt-rc2-in-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block states this LOCATED_IN relation between the two named features and carries the qualifier wording the row projects. It is also a block from which one of the endpoint records is derived.",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "rel:morb-sampled-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL A SAMPLED_FROM relation between the two named features is what the block states. The block also derives an endpoint record, so the relation is formalized locally.",
      "source_locators": [
        "page:8:block:005"
      ]
    },
    {
      "witness_key": "rel:morb-sampled-rc3",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL Both endpoints and the SAMPLED_FROM relation between them are stated in the block. The block also derives an endpoint record, so the relation is formalized locally.",
      "source_locators": [
        "page:8:block:005"
      ]
    },
    {
      "witness_key": "rel:samples-from-rti-area",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block names both features and the SAMPLED_FROM relation the row projects between them. The block also derives an endpoint record, so the relation is formalized locally.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "dataset:final-catalog",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this data collection, and the description the row carries follows the same sentence.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "dataset:original-catalog",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this data collection, and the description the row carries follows the same sentence.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "dataset:petdb",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this data collection and gives the address the row records. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:6:block:005",
        "page:8:block:005"
      ]
    },
    {
      "witness_key": "dataset:raw-seismic",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this data collection and gives the address the row records.",
      "source_locators": [
        "page:8:block:008"
      ]
    },
    {
      "witness_key": "dataset:refraction-profile",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this data collection, and the description the row carries follows the same sentence. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:2:block:002",
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "dataset:sub-360",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this data collection, and the description the row carries follows the same sentence.",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "dataset:subset-45",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this data collection, and the description the row carries follows the same sentence.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "dataset:supplementary",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this data collection and gives the identifier the row records.",
      "source_locators": [
        "page:11:block:001"
      ]
    },
    {
      "witness_key": "dataset:zenodo-catalog",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this data collection and gives the identifier the row records. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:8:block:008",
        "page:8:block:009"
      ]
    },
    {
      "witness_key": "method:ba90-rb90",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The procedure the record stands for is what the block describes. The row's name restates it rather than quoting it.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "method:depth-resolution-tests",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW What the record names is the procedure the block sets out. The row's name restates it rather than quoting it, and the description follows the same sentence.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "method:double-difference",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block describes the procedure this record stands for. The row's name restates it rather than quoting it, and the description follows the same sentence. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:2:block:002",
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "method:fc-correction",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The procedure the record stands for is what the block describes. The row's name restates it rather than quoting it.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "method:focal-mechanism",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW What the record names is the procedure the block sets out. The row's name restates it rather than quoting it.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "method:local-magnitude",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block describes the procedure this record stands for. The row's name restates it rather than quoting it, and the description follows the same sentence. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:2:block:002",
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "method:manual-arrival-check",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The procedure the record stands for is what the block describes. The row's name restates it rather than quoting it, and the description follows the same sentence.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "method:max-depth-compilation",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW What the record names is the procedure the block sets out. The row's name restates it rather than quoting it, and the description follows the same sentence.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "method:morb-compilation",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block describes the procedure this record stands for. The row's name restates it rather than quoting it.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "method:nonlinear-location",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The procedure the record stands for is what the block describes. The row's name restates it rather than quoting it, and the description follows the same sentence. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:2:block:002",
        "page:7:block:004"
      ]
    },
    {
      "witness_key": "method:quality-classification",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW What the record names is the procedure the block sets out. The row's name restates it rather than quoting it, and the description follows the same sentence. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:2:block:003",
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "method:stalta",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block describes the procedure this record stands for. The row's name restates it rather than quoting it, and the description follows the same sentence. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "method:station-corrections",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The procedure the record stands for is what the block describes. The row's name restates it rather than quoting it, and the description follows the same sentence. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:2:block:002",
        "page:7:block:005"
      ]
    },
    {
      "witness_key": "method:wadati",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW What the record names is the procedure the block sets out. The row's name restates it rather than quoting it, and the description follows the same sentence.",
      "source_locators": [
        "page:7:block:002"
      ]
    },
    {
      "witness_key": "model:co2-solubility",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this model, and the row projects nothing the block does not carry. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:5:block:006",
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "model:minimum-1d",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this model, and the row projects nothing the block does not carry.",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "model:thermal",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this model, and the row projects nothing the block does not carry. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:3:block:001",
        "page:7:block:012"
      ]
    },
    {
      "witness_key": "model:velocity-1d",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this model, and the row projects nothing the block does not carry. All 2 blocks the derivations reach are cited.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "model:velocity-average",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this model and describes what it is, and the row projects nothing the block does not carry.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "model:velocity-fastest",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this model and describes what it is, and the row projects nothing the block does not carry.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "rel:tests-support-constrained",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block says in its own sentence that the testing bears out the conclusion, which is exactly the SUPPORTS link this row projects. The claim endpoint is derived from the same block, so the link is formalized where one of its endpoints is.",
      "source_locators": [
        "page:8:block:001"
      ]
    },
    {
      "witness_key": "rel:tests-support-deep",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The block says in its own sentence that the testing bears out the conclusion, which is exactly the SUPPORTS link this row projects. The claim endpoint is derived from the same block, so the link is formalized where one of its endpoints is.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "rel:velocity-model-from-profile",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL Both endpoints and the OBSERVED_WITH relation between them are stated in the block. The block also derives an endpoint record, so the relation is formalized locally.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "agent:ab",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this person where the article introduces it, and the row projects nothing beyond that. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:ayyang",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this person where the article introduces it, and the row projects nothing beyond that.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:cartigny",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this person where the article introduces it, and the row projects nothing beyond that.",
      "source_locators": [
        "page:10:block:043"
      ]
    },
    {
      "witness_key": "agent:ch",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this person where the article introduces it, and the row projects nothing beyond that. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:crew",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that, the description being the place the block gives it.",
      "source_locators": [
        "page:10:block:043"
      ]
    },
    {
      "witness_key": "agent:db",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this person where the article introduces it, and the row projects nothing beyond that. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:geli",
      "source_support": "PARTIAL",
      "rationale": "NO_SUBJECT_IN_ROW The block starts part way through the list of people thanked and carries the surname only. The initial this row projects sits in the block before it, which the derivation does not reach, so the cited block supports the person but not the whole name as written.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:lg",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this person where the article introduces it, and the row projects nothing beyond that. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:lp",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this person where the article introduces it, and the row projects nothing beyond that. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:mm",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this person where the article introduces it, and the row projects nothing beyond that. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:scs",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this person where the article introduces it, and the row projects nothing beyond that. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:zwang",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this person where the article introduces it, and the row projects nothing beyond that.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:zy",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this person where the article introduces it, and the row projects nothing beyond that. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "org:brittany",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that, the description being the place the block gives it.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:cnr-igag",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that, the description being the place the block gives it. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "org:erc",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:french-gov",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that, the description being the place the block gives it.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:geo-ocean",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that, the description being the place the block gives it. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "org:independent",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that, the description being the place the block gives it. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "org:ipgp",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that, the description being the place the block gives it. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "org:isblue",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:modena",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that, the description being the place the block gives it. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "org:nsfc",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:sio",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that, the description being the place the block gives it. A gap is declared on the evidence this record rests on, of kind RELATION_ABSENT; it concerns something the row does not project and leaves the judged fields untouched.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "org:tgir",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names this body where the article introduces it, and the row projects nothing beyond that.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:fund:erc-advanced",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The funding sentence in the block carries the funder, the award identifier and the recipient, the recipient given by the initials the article uses for its authors, so the CONTRIBUTED_TO link with role FUNDING_ACQUISITION rests on it. The recipient's written-out name belongs to the endpoint record and is judged with that record; the block also derives the funder endpoint.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:fund:erc-fp7",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The funding sentence in the block carries the funder, the award identifier and the recipient, the recipient given by the initials the article uses for its authors, so the CONTRIBUTED_TO link with role FUNDING_ACQUISITION rests on it. The recipient's written-out name belongs to the endpoint record and is judged with that record; the block also derives the funder endpoint.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:fund:nsfc:42330308",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The funding sentence in the block carries the funder, the award identifier and the recipient, the recipient given by the initials the article uses for its authors, so the CONTRIBUTED_TO link with role FUNDING_ACQUISITION rests on it. The recipient's written-out name belongs to the endpoint record and is judged with that record; the block also derives the funder endpoint.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:fund:nsfc:42422603",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The funding sentence in the block carries the funder, the award identifier and the recipient, the recipient given by the initials the article uses for its authors, so the CONTRIBUTED_TO link with role FUNDING_ACQUISITION rests on it. The recipient's written-out name belongs to the endpoint record and is judged with that record; the block also derives the funder endpoint.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:fund:zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The funding sentence in the block carries the funder, the award identifier and the recipient, the recipient given by the initials the article uses for its authors, so the CONTRIBUTED_TO link with role FUNDING_ACQUISITION rests on it. The recipient's written-out name belongs to the endpoint record and is judged with that record; the block also derives the funder endpoint.",
      "source_locators": [
        "page:10:block:044"
      ]
    }
  ],
  "questions": [
    {
      "question_id": "CQ-T1-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Each element is carried by a returned row: the cruise by its own record, the network by the instrument record, and the acquisition of the data by the scope field of the count row whose subject is that network. Nothing in the result joins the cruise to the network, which the assembly descriptor records.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "campaign_name",
          "row_index": 0,
          "absent_reason": null,
          "note": "The cruise is returned as its own record and its name field is what the question asks for."
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "The instrument record names the seafloor seismometers whose recordings the study uses."
        },
        {
          "semantic": "data_acquisition",
          "row_index": 84,
          "absent_reason": null,
          "note": "The count row's scope field ties the network to the acquisition of the microseismicity data, which is the acquisition the question is about."
        }
      ],
      "source_locators": [
        "page:10:block:043",
        "page:10:block:044",
        "page:10:block:046",
        "page:1:block:001",
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
          "witness_key": "instrument:obs"
        },
        {
          "row_index": 2,
          "witness_key": "software:global-mapper"
        },
        {
          "row_index": 3,
          "witness_key": "software:gmt"
        },
        {
          "row_index": 4,
          "witness_key": "software:hash"
        },
        {
          "row_index": 5,
          "witness_key": "software:hypodd"
        },
        {
          "row_index": 6,
          "witness_key": "software:nonlinloc"
        },
        {
          "row_index": 7,
          "witness_key": "software:seisan"
        },
        {
          "row_index": 8,
          "witness_key": "software:velest"
        },
        {
          "row_index": 9,
          "witness_key": "software:zmap"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 17,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 18,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 19,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 20,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 21,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 22,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 23,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 24,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 25,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 26,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 27,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 28,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 29,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 30,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 31,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 32,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 33,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 34,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 35,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 36,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 37,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 38,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 39,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 40,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 41,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 42,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 43,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 44,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 45,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 46,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 47,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 48,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 49,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 50,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 51,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 52,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 53,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 54,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 55,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 56,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 57,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 58,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 59,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 60,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 61,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 62,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 63,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 64,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 65,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 66,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 67,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 68,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 69,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 70,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 71,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 72,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 73,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 74,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 75,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 76,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 77,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 78,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 79,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 80,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 81,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 82,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 83,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 84,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 86,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 87,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 88,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 91,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 92,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 93,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 94,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 95,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 96,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 97,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 98,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 99,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 100,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 101,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 102,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 103,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 105,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 106,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 108,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 109,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 110,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 112,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 113,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 114,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 115,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 116,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 120,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 121,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 122,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 123,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 124,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 125,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 126,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 127,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 128,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 129,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 130,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 131,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 132,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 133,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 134,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 135,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 136,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 137,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 138,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 139,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 140,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 141,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 142,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 143,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 144,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 145,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 146,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 147,
          "witness_key": "obs:temp-10-20km"
        }
      ]
    },
    {
      "question_id": "CQ-T1-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The count row carries both the number and, through its subject, the network it counts; a second count row on the methods side carries the deployment of that network. No absence.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "instrument_count",
          "row_index": 84,
          "absent_reason": null,
          "note": "The row carries the number of seismometers in the network as a count, with the network as its subject."
        },
        {
          "semantic": "observing_system",
          "row_index": 84,
          "absent_reason": null,
          "note": "The same row resolves its subject to the instrument record, so the observing system is named on the row itself."
        },
        {
          "semantic": "deployment_event",
          "row_index": 85,
          "absent_reason": null,
          "note": "The methods-side count row states that the network was deployed for the passive experiment, which is the deployment the question asks about."
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
          "witness_key": "instrument:obs"
        },
        {
          "row_index": 2,
          "witness_key": "software:global-mapper"
        },
        {
          "row_index": 3,
          "witness_key": "software:gmt"
        },
        {
          "row_index": 4,
          "witness_key": "software:hash"
        },
        {
          "row_index": 5,
          "witness_key": "software:hypodd"
        },
        {
          "row_index": 6,
          "witness_key": "software:nonlinloc"
        },
        {
          "row_index": 7,
          "witness_key": "software:seisan"
        },
        {
          "row_index": 8,
          "witness_key": "software:velest"
        },
        {
          "row_index": 9,
          "witness_key": "software:zmap"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 17,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 18,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 19,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 20,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 21,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 22,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 23,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 24,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 25,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 26,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 27,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 28,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 29,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 30,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 31,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 32,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 33,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 34,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 35,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 36,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 37,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 38,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 39,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 40,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 41,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 42,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 43,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 44,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 45,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 46,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 47,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 48,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 49,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 50,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 51,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 52,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 53,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 54,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 55,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 56,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 57,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 58,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 59,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 60,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 61,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 62,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 63,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 64,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 65,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 66,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 67,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 68,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 69,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 70,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 71,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 72,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 73,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 74,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 75,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 76,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 77,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 78,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 79,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 80,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 81,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 82,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 83,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 84,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 86,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 87,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 88,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 91,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 92,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 93,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 94,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 95,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 96,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 97,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 98,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 99,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 100,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 101,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 102,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 103,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 105,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 106,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 108,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 109,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 110,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 112,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 113,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 114,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 115,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 116,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 120,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 121,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 122,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 123,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 124,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 125,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 126,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 127,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 128,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 129,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 130,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 131,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 132,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 133,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 134,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 135,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 136,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 137,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 138,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 139,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 140,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 141,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 142,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 143,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 144,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 145,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 146,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 147,
          "witness_key": "obs:temp-10-20km"
        }
      ]
    },
    {
      "question_id": "CQ-T1-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The article's own bibliographic record carries all three: the record itself, the acceptance, and the date the acceptance is given on, in the article's wording.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "publication_record",
          "row_index": 79,
          "absent_reason": null,
          "note": "The article's own bibliographic record is returned and is the publication the question asks about."
        },
        {
          "semantic": "acceptance_event",
          "row_index": 79,
          "absent_reason": null,
          "note": "The acceptance is carried on that record by the field that records the acceptance date as the article states it."
        },
        {
          "semantic": "calendar_date",
          "row_index": 79,
          "absent_reason": null,
          "note": "The same field carries the day, month and year, in the article's own wording."
        }
      ],
      "source_locators": [
        "page:10:block:048",
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
        "page:8:block:018"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "work:ref:01"
        },
        {
          "row_index": 1,
          "witness_key": "work:ref:02"
        },
        {
          "row_index": 2,
          "witness_key": "work:ref:03"
        },
        {
          "row_index": 3,
          "witness_key": "work:ref:04"
        },
        {
          "row_index": 4,
          "witness_key": "work:ref:05"
        },
        {
          "row_index": 5,
          "witness_key": "work:ref:06"
        },
        {
          "row_index": 6,
          "witness_key": "work:ref:07"
        },
        {
          "row_index": 7,
          "witness_key": "work:ref:08"
        },
        {
          "row_index": 8,
          "witness_key": "work:ref:09"
        },
        {
          "row_index": 9,
          "witness_key": "work:ref:10"
        },
        {
          "row_index": 10,
          "witness_key": "work:ref:11"
        },
        {
          "row_index": 11,
          "witness_key": "work:ref:12"
        },
        {
          "row_index": 12,
          "witness_key": "work:ref:13"
        },
        {
          "row_index": 13,
          "witness_key": "work:ref:14"
        },
        {
          "row_index": 14,
          "witness_key": "work:ref:15"
        },
        {
          "row_index": 15,
          "witness_key": "work:ref:16"
        },
        {
          "row_index": 16,
          "witness_key": "work:ref:17"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref:18"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref:19"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref:20"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref:21"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref:22"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref:23"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref:24"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref:25"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref:26"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref:27"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref:28"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref:29"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref:30"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref:31"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref:32"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref:33"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref:34"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref:35"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref:36"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref:37"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref:38"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref:39"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref:40"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref:41"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref:42"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref:43"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref:44"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref:45"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref:46"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref:47"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref:48"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref:49"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref:50"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref:51"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref:52"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref:53"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref:54"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref:55"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref:56"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref:57"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref:58"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref:59"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref:60"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref:61"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref:62"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref:63"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref:64"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref:65"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref:66"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref:67"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref:68"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref:69"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref:70"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref:71"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref:72"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref:73"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref:74"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref:75"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref:76"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref:77"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref:78"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref:79"
        },
        {
          "row_index": 79,
          "witness_key": "work:yu-2025"
        },
        {
          "row_index": 80,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 81,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 82,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 83,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 84,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 85,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 86,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 87,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 88,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 89,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 90,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 91,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 92,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 93,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 94,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 98,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 99,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 100,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 101,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 102,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 103,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 104,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 105,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 106,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 107,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 108,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 109,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 110,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 111,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 112,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 113,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 114,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 115,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 116,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 117,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 118,
          "witness_key": "rel:yu-2025-cites-01"
        },
        {
          "row_index": 119,
          "witness_key": "rel:yu-2025-cites-02"
        },
        {
          "row_index": 120,
          "witness_key": "rel:yu-2025-cites-03"
        },
        {
          "row_index": 121,
          "witness_key": "rel:yu-2025-cites-04"
        },
        {
          "row_index": 122,
          "witness_key": "rel:yu-2025-cites-05"
        },
        {
          "row_index": 123,
          "witness_key": "rel:yu-2025-cites-06"
        },
        {
          "row_index": 124,
          "witness_key": "rel:yu-2025-cites-07"
        },
        {
          "row_index": 125,
          "witness_key": "rel:yu-2025-cites-08"
        },
        {
          "row_index": 126,
          "witness_key": "rel:yu-2025-cites-09"
        },
        {
          "row_index": 127,
          "witness_key": "rel:yu-2025-cites-10"
        },
        {
          "row_index": 128,
          "witness_key": "rel:yu-2025-cites-11"
        },
        {
          "row_index": 129,
          "witness_key": "rel:yu-2025-cites-12"
        },
        {
          "row_index": 130,
          "witness_key": "rel:yu-2025-cites-13"
        },
        {
          "row_index": 131,
          "witness_key": "rel:yu-2025-cites-14"
        },
        {
          "row_index": 132,
          "witness_key": "rel:yu-2025-cites-15"
        },
        {
          "row_index": 133,
          "witness_key": "rel:yu-2025-cites-16"
        },
        {
          "row_index": 134,
          "witness_key": "rel:yu-2025-cites-17"
        },
        {
          "row_index": 135,
          "witness_key": "rel:yu-2025-cites-18"
        },
        {
          "row_index": 136,
          "witness_key": "rel:yu-2025-cites-19"
        },
        {
          "row_index": 137,
          "witness_key": "rel:yu-2025-cites-20"
        },
        {
          "row_index": 138,
          "witness_key": "rel:yu-2025-cites-21"
        },
        {
          "row_index": 139,
          "witness_key": "rel:yu-2025-cites-22"
        },
        {
          "row_index": 140,
          "witness_key": "rel:yu-2025-cites-23"
        },
        {
          "row_index": 141,
          "witness_key": "rel:yu-2025-cites-24"
        },
        {
          "row_index": 142,
          "witness_key": "rel:yu-2025-cites-25"
        },
        {
          "row_index": 143,
          "witness_key": "rel:yu-2025-cites-26"
        },
        {
          "row_index": 144,
          "witness_key": "rel:yu-2025-cites-27"
        },
        {
          "row_index": 145,
          "witness_key": "rel:yu-2025-cites-28"
        },
        {
          "row_index": 146,
          "witness_key": "rel:yu-2025-cites-29"
        },
        {
          "row_index": 147,
          "witness_key": "rel:yu-2025-cites-30"
        },
        {
          "row_index": 148,
          "witness_key": "rel:yu-2025-cites-31"
        },
        {
          "row_index": 149,
          "witness_key": "rel:yu-2025-cites-32"
        },
        {
          "row_index": 150,
          "witness_key": "rel:yu-2025-cites-33"
        },
        {
          "row_index": 151,
          "witness_key": "rel:yu-2025-cites-34"
        },
        {
          "row_index": 152,
          "witness_key": "rel:yu-2025-cites-35"
        },
        {
          "row_index": 153,
          "witness_key": "rel:yu-2025-cites-36"
        },
        {
          "row_index": 154,
          "witness_key": "rel:yu-2025-cites-37"
        },
        {
          "row_index": 155,
          "witness_key": "rel:yu-2025-cites-38"
        },
        {
          "row_index": 156,
          "witness_key": "rel:yu-2025-cites-39"
        },
        {
          "row_index": 157,
          "witness_key": "rel:yu-2025-cites-40"
        },
        {
          "row_index": 158,
          "witness_key": "rel:yu-2025-cites-41"
        },
        {
          "row_index": 159,
          "witness_key": "rel:yu-2025-cites-42"
        },
        {
          "row_index": 160,
          "witness_key": "rel:yu-2025-cites-43"
        },
        {
          "row_index": 161,
          "witness_key": "rel:yu-2025-cites-44"
        },
        {
          "row_index": 162,
          "witness_key": "rel:yu-2025-cites-45"
        },
        {
          "row_index": 163,
          "witness_key": "rel:yu-2025-cites-46"
        },
        {
          "row_index": 164,
          "witness_key": "rel:yu-2025-cites-47"
        },
        {
          "row_index": 165,
          "witness_key": "rel:yu-2025-cites-48"
        },
        {
          "row_index": 166,
          "witness_key": "rel:yu-2025-cites-49"
        },
        {
          "row_index": 167,
          "witness_key": "rel:yu-2025-cites-50"
        },
        {
          "row_index": 168,
          "witness_key": "rel:yu-2025-cites-51"
        },
        {
          "row_index": 169,
          "witness_key": "rel:yu-2025-cites-52"
        },
        {
          "row_index": 170,
          "witness_key": "rel:yu-2025-cites-53"
        },
        {
          "row_index": 171,
          "witness_key": "rel:yu-2025-cites-54"
        },
        {
          "row_index": 172,
          "witness_key": "rel:yu-2025-cites-55"
        },
        {
          "row_index": 173,
          "witness_key": "rel:yu-2025-cites-56"
        },
        {
          "row_index": 174,
          "witness_key": "rel:yu-2025-cites-57"
        },
        {
          "row_index": 175,
          "witness_key": "rel:yu-2025-cites-58"
        },
        {
          "row_index": 176,
          "witness_key": "rel:yu-2025-cites-59"
        },
        {
          "row_index": 177,
          "witness_key": "rel:yu-2025-cites-60"
        },
        {
          "row_index": 178,
          "witness_key": "rel:yu-2025-cites-61"
        },
        {
          "row_index": 179,
          "witness_key": "rel:yu-2025-cites-62"
        },
        {
          "row_index": 180,
          "witness_key": "rel:yu-2025-cites-63"
        },
        {
          "row_index": 181,
          "witness_key": "rel:yu-2025-cites-64"
        },
        {
          "row_index": 182,
          "witness_key": "rel:yu-2025-cites-65"
        },
        {
          "row_index": 183,
          "witness_key": "rel:yu-2025-cites-66"
        },
        {
          "row_index": 184,
          "witness_key": "rel:yu-2025-cites-67"
        },
        {
          "row_index": 185,
          "witness_key": "rel:yu-2025-cites-68"
        },
        {
          "row_index": 186,
          "witness_key": "rel:yu-2025-cites-69"
        },
        {
          "row_index": 187,
          "witness_key": "rel:yu-2025-cites-70"
        },
        {
          "row_index": 188,
          "witness_key": "rel:yu-2025-cites-71"
        },
        {
          "row_index": 189,
          "witness_key": "rel:yu-2025-cites-72"
        },
        {
          "row_index": 190,
          "witness_key": "rel:yu-2025-cites-73"
        },
        {
          "row_index": 191,
          "witness_key": "rel:yu-2025-cites-74"
        },
        {
          "row_index": 192,
          "witness_key": "rel:yu-2025-cites-75"
        },
        {
          "row_index": 193,
          "witness_key": "rel:yu-2025-cites-76"
        },
        {
          "row_index": 194,
          "witness_key": "rel:yu-2025-cites-77"
        },
        {
          "row_index": 195,
          "witness_key": "rel:yu-2025-cites-78"
        },
        {
          "row_index": 196,
          "witness_key": "rel:yu-2025-cites-79"
        },
        {
          "row_index": 197,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 198,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 199,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 200,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 201,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 202,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 203,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 204,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 205,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 206,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 207,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 208,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 209,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 210,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 211,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 212,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 213,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 214,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 215,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 216,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 217,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 218,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 219,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 220,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 221,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 222,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 223,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 224,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 225,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 226,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 227,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 228,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 229,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 230,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 231,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 232,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 233,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 234,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 235,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 236,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 237,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 238,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 239,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 240,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 241,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 242,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 243,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 244,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 245,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 246,
          "witness_key": "claim:vent-field-too-far"
        }
      ]
    },
    {
      "question_id": "CQ-T1-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The deposit and its identifier are both on one returned row. The repository is named in the reading and is not on any row: the dataset type has slots that other dataset records in this run use for exactly that, this record leaves them unset, and no gap declares it, which is plain omission rather than an ontology limit.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "dataset_record",
          "row_index": 8,
          "absent_reason": null,
          "note": "The deposited catalogue and arrivals are returned as one dataset record, which is the deposit the question asks about."
        },
        {
          "semantic": "repository_name",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The dataset type in the accepted contract carries description and locator slots, and sibling dataset records in this run use them to name where the data sit; this record leaves both unset, nothing else on the row names the repository, and no gap is declared for it."
        },
        {
          "semantic": "persistent_identifier",
          "row_index": 8,
          "absent_reason": null,
          "note": "The row carries the deposit's identifier in its own field."
        }
      ],
      "source_locators": [
        "page:8:block:008",
        "page:8:block:009"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "dataset:final-catalog"
        },
        {
          "row_index": 1,
          "witness_key": "dataset:original-catalog"
        },
        {
          "row_index": 2,
          "witness_key": "dataset:petdb"
        },
        {
          "row_index": 3,
          "witness_key": "dataset:raw-seismic"
        },
        {
          "row_index": 4,
          "witness_key": "dataset:refraction-profile"
        },
        {
          "row_index": 5,
          "witness_key": "dataset:sub-360"
        },
        {
          "row_index": 6,
          "witness_key": "dataset:subset-45"
        },
        {
          "row_index": 7,
          "witness_key": "dataset:supplementary"
        },
        {
          "row_index": 8,
          "witness_key": "dataset:zenodo-catalog"
        },
        {
          "row_index": 9,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 10,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 11,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 12,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 13,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 14,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 15,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 16,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 17,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 18,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 19,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 20,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 21,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 22,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 23,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 24,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 25,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 26,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 27,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 28,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 29,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 30,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 31,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 32,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 33,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 34,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 35,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 36,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 37,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 38,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 39,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 40,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 41,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 42,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 43,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 44,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 45,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 46,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 47,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 48,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 49,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 50,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 51,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 52,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 53,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 54,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 55,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 56,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 57,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 58,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 60,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 61,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 62,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 63,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 64,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 65,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 66,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 67,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 68,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 69,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 70,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 71,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 72,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 73,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 74,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 75,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 76,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 77,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 78,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 79,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 80,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 81,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 82,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 83,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 84,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 85,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 86,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 87,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 88,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 89,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 90,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 91,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 92,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 93,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 94,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 95,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vent-field-too-far"
        }
      ]
    },
    {
      "question_id": "CQ-T1-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The continuous recording stretch, its length and its unit are all on one quantity row, and the instruments that did the recording are a second row. Nothing joins the two, which the assembly descriptor records.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "recording_interval",
          "row_index": 68,
          "absent_reason": null,
          "note": "The row is the continuous recording stretch of the deployment, which is the interval the question asks about."
        },
        {
          "semantic": "duration_value",
          "row_index": 68,
          "absent_reason": null,
          "note": "The same row carries the length of that stretch as a bounded value."
        },
        {
          "semantic": "time_unit",
          "row_index": 68,
          "absent_reason": null,
          "note": "The unit field on that row states the unit the length is given in."
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "The instrument record names the seismometers that did the recording."
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:2:block:002"
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
          "witness_key": "software:global-mapper"
        },
        {
          "row_index": 3,
          "witness_key": "software:gmt"
        },
        {
          "row_index": 4,
          "witness_key": "software:hash"
        },
        {
          "row_index": 5,
          "witness_key": "software:hypodd"
        },
        {
          "row_index": 6,
          "witness_key": "software:nonlinloc"
        },
        {
          "row_index": 7,
          "witness_key": "software:seisan"
        },
        {
          "row_index": 8,
          "witness_key": "software:velest"
        },
        {
          "row_index": 9,
          "witness_key": "software:zmap"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 17,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 18,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 19,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 20,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 21,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 22,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 23,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 24,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 25,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 26,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 27,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 28,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 29,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 30,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 31,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 32,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 33,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 34,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 35,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 36,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 37,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 38,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 39,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 40,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 41,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 42,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 43,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 44,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 45,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 46,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 47,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 48,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 49,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 50,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 51,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 52,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 53,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 54,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 55,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 56,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 57,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 58,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 59,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 60,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 61,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 62,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 63,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 64,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 65,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 66,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 67,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 68,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 69,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 70,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 71,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 72,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 73,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 74,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 75,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 76,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 77,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 78,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 79,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 80,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 81,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 82,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 83,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 84,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 86,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 87,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 88,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 91,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 92,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 93,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 94,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 95,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 96,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 97,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 98,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 99,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 100,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 101,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 102,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 103,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 105,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 106,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 108,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 109,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 110,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 112,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 113,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 114,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 115,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 116,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 120,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 121,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 122,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 123,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 124,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 125,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 126,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 127,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 128,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 129,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 130,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 131,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 132,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 133,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 134,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 135,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 136,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 137,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 138,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 139,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 140,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 141,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 142,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 143,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 144,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 145,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 146,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 147,
          "witness_key": "obs:temp-10-20km"
        }
      ]
    },
    {
      "question_id": "CQ-T2-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Both features, the bounding relation between them and the side of the axis are returned, the last two as relations whose endpoints are the returned features.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "named_subsection",
          "row_index": 37,
          "absent_reason": null,
          "note": "The ridge-transform intersection subsection is returned by name as a ridge segment."
        },
        {
          "semantic": "structural_feature",
          "row_index": 6,
          "absent_reason": null,
          "note": "The detachment fault that bounds it is returned as its own feature record."
        },
        {
          "semantic": "bounding_relation",
          "row_index": 99,
          "absent_reason": null,
          "note": "A returned relation carries the bounding of that subsection by that fault, with the side qualifier the source uses."
        },
        {
          "semantic": "side_of_axis",
          "row_index": 95,
          "absent_reason": null,
          "note": "A returned relation places the core complex relative to the ridge axis and carries the side wording on the row."
        }
      ],
      "source_locators": [
        "page:1:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 4,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 5,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 6,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 7,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 11,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 12,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 18,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 20,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 21,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 22,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 24,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 25,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 26,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 27,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 32,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 34,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 42,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 44,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 45,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 49,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 51,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 53,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 54,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 55,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 56,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 57,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 58,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 59,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 60,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 61,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 62,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 63,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 64,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 65,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 67,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 68,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 69,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 70,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 71,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 72,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 73,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 75,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 76,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 77,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 78,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 79,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 80,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 83,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 84,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 85,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 86,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 87,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 88,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 89,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 90,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 91,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 92,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 93,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 94,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 95,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 96,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 97,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 98,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 99,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 100,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 101,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 102,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 103,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 104,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 105,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 106,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 107,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 108,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 109,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 110,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 111,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 112,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 113,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 114,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 115,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 116,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 117,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 118,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 119,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 120,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 121,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 122,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 123,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 124,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 125,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 126,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 127,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 128,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 129,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 130,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 131,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 132,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 133,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 134,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 135,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 136,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 137,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 138,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 139,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 140,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 141,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 142,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 143,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 144,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 145,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 146,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 147,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 148,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 149,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 150,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 151,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 152,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 153,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 154,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 155,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 156,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 157,
          "witness_key": "claim:seafloor-basalts-degassed"
        }
      ]
    },
    {
      "question_id": "CQ-T2-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Both programs are returned as software records and the catalogue as a dataset record. The ordering is carried in prose on the relocation method's description rather than by a typed link, since the contract has no relation that orders one method after another; the element is on the row, so it names the semantic.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "initial_location_method",
          "row_index": 33,
          "absent_reason": null,
          "note": "The program that produced the first hypocentres is returned as a software record."
        },
        {
          "semantic": "relocation_method",
          "row_index": 32,
          "absent_reason": null,
          "note": "The program applied afterwards is returned as its own software record."
        },
        {
          "semantic": "method_sequence",
          "row_index": 11,
          "absent_reason": null,
          "note": "The method row's description says this procedure relocates hypocentres already obtained, which is the ordering the question asks for; no typed ordering between methods exists in the contract, so the ordering is carried in prose on the row."
        },
        {
          "semantic": "earthquake_catalog",
          "row_index": 0,
          "absent_reason": null,
          "note": "The catalogue the relocated events end up in is returned as a dataset record."
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:7:block:004",
        "page:7:block:005",
        "page:7:block:006",
        "page:7:block:007",
        "page:8:block:010"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "dataset:final-catalog"
        },
        {
          "row_index": 1,
          "witness_key": "dataset:original-catalog"
        },
        {
          "row_index": 2,
          "witness_key": "dataset:petdb"
        },
        {
          "row_index": 3,
          "witness_key": "dataset:raw-seismic"
        },
        {
          "row_index": 4,
          "witness_key": "dataset:refraction-profile"
        },
        {
          "row_index": 5,
          "witness_key": "dataset:sub-360"
        },
        {
          "row_index": 6,
          "witness_key": "dataset:subset-45"
        },
        {
          "row_index": 7,
          "witness_key": "dataset:supplementary"
        },
        {
          "row_index": 8,
          "witness_key": "dataset:zenodo-catalog"
        },
        {
          "row_index": 9,
          "witness_key": "method:ba90-rb90"
        },
        {
          "row_index": 10,
          "witness_key": "method:depth-resolution-tests"
        },
        {
          "row_index": 11,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 12,
          "witness_key": "method:fc-correction"
        },
        {
          "row_index": 13,
          "witness_key": "method:focal-mechanism"
        },
        {
          "row_index": 14,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 15,
          "witness_key": "method:manual-arrival-check"
        },
        {
          "row_index": 16,
          "witness_key": "method:max-depth-compilation"
        },
        {
          "row_index": 17,
          "witness_key": "method:morb-compilation"
        },
        {
          "row_index": 18,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 19,
          "witness_key": "method:quality-classification"
        },
        {
          "row_index": 20,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 21,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 22,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 23,
          "witness_key": "model:co2-solubility"
        },
        {
          "row_index": 24,
          "witness_key": "model:minimum-1d"
        },
        {
          "row_index": 25,
          "witness_key": "model:thermal"
        },
        {
          "row_index": 26,
          "witness_key": "model:velocity-1d"
        },
        {
          "row_index": 27,
          "witness_key": "model:velocity-average"
        },
        {
          "row_index": 28,
          "witness_key": "model:velocity-fastest"
        },
        {
          "row_index": 29,
          "witness_key": "software:global-mapper"
        },
        {
          "row_index": 30,
          "witness_key": "software:gmt"
        },
        {
          "row_index": 31,
          "witness_key": "software:hash"
        },
        {
          "row_index": 32,
          "witness_key": "software:hypodd"
        },
        {
          "row_index": 33,
          "witness_key": "software:nonlinloc"
        },
        {
          "row_index": 34,
          "witness_key": "software:seisan"
        },
        {
          "row_index": 35,
          "witness_key": "software:velest"
        },
        {
          "row_index": 36,
          "witness_key": "software:zmap"
        },
        {
          "row_index": 37,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 38,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 39,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 40,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 41,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 42,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 43,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 44,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 45,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 46,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 47,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 48,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 49,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 50,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 51,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 52,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 53,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 54,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 55,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 56,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 57,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 58,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 59,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 60,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 61,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 62,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 63,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 64,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 65,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 66,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 67,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 68,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 69,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 70,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 71,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 72,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 73,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 74,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 82,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 83,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 84,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 86,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 87,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 88,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 91,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 92,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 93,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 94,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 95,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 96,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 97,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 98,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 99,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 100,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 101,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 102,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 103,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 104,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 105,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 106,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 107,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 108,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 109,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 110,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 111,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 112,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 113,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 114,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 115,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 116,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 117,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 118,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 119,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 120,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 121,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 122,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 123,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 124,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 125,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 126,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 127,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 128,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 129,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 130,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 131,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 132,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 133,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 134,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 135,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 136,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 137,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 138,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 139,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 140,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 141,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 142,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 143,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 144,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 145,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 147,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 148,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 149,
          "witness_key": "rel:tests-support-constrained"
        },
        {
          "row_index": 150,
          "witness_key": "rel:tests-support-deep"
        },
        {
          "row_index": 151,
          "witness_key": "rel:velocity-model-from-profile"
        },
        {
          "row_index": 152,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 153,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 154,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 155,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 156,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 157,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 158,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 159,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 160,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 161,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 162,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 163,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 164,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 165,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 166,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 167,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 168,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 169,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 170,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 171,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 172,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 173,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 174,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 175,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 176,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 177,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 178,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 179,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 180,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 181,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 182,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 183,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 184,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 185,
          "witness_key": "claim:melt-resides-fractionates"
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
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 189,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 190,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 191,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 192,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 193,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 194,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 195,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 196,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 197,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 198,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 199,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 200,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 201,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 202,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 203,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 204,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 205,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 206,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 207,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 208,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 209,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 210,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 211,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 212,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 213,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 214,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 215,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 216,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 217,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 218,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 219,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 220,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 221,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 222,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 223,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 224,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 226,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 227,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 228,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 229,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 230,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 231,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 232,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 233,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 234,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 235,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 236,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 238,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 239,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 240,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 241,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 242,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 243,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 244,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 245,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 246,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 247,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 248,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 249,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 250,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 251,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 252,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 253,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 254,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 255,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 256,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 257,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 258,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 259,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 260,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 261,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 262,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 263,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 264,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 265,
          "witness_key": "obs:temp-10-20km"
        }
      ]
    },
    {
      "question_id": "CQ-T2-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The vent field, the discontinuity whose flank it sits on, its distance from the present-day valley and that valley itself are all carried by returned rows, the discontinuity through a relation whose endpoint names it.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "named_feature",
          "row_index": 7,
          "absent_reason": null,
          "note": "The extinct vent field is returned as its own feature record."
        },
        {
          "semantic": "host_discontinuity",
          "row_index": 181,
          "absent_reason": null,
          "note": "A returned relation puts that vent field on the flank of the first discontinuity, and the flank record names which discontinuity it belongs to."
        },
        {
          "semantic": "spatial_relation",
          "row_index": 214,
          "absent_reason": null,
          "note": "The claim row, whose subject is the vent field, carries its distance from the present-day valley as the element of the claim."
        },
        {
          "semantic": "present_day_axis",
          "row_index": 214,
          "absent_reason": null,
          "note": "The same row names the present-day axial valley as the thing the vent field is placed against."
        }
      ],
      "source_locators": [
        "page:3:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 4,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 5,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 6,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 7,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 11,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 12,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 18,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 20,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 21,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 22,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 24,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 25,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 26,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 27,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 32,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 34,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 42,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 44,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 45,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 49,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 51,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 53,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 54,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 55,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 56,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 57,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 58,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 59,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 60,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 61,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 62,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 63,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 64,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 65,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 67,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 68,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 69,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 70,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 71,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 72,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 73,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 75,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 76,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 77,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 78,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 79,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 80,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 83,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 84,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 85,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 86,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 87,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 88,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 91,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 92,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 93,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 94,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 95,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 96,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 106,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 107,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 108,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 109,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 110,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 111,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 112,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 113,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 114,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 115,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 116,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 117,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 118,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 119,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 120,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 122,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 123,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 124,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 125,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 126,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 128,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 129,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 130,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 131,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 132,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 133,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 134,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 135,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 136,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 137,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 138,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 139,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 140,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 141,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 142,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 143,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 144,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 145,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 147,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 148,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 149,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 150,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 151,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 152,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 153,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 154,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 155,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 156,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 158,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 159,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 160,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 161,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 162,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 163,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 164,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 165,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 166,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 167,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 168,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 169,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 170,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 171,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 174,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 175,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 176,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 177,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 178,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 179,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 180,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 181,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 182,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 183,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 184,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 185,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 186,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 187,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 188,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 189,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 190,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 191,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 192,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 193,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 194,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 195,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 196,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 197,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 198,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 199,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 200,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 201,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 202,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 203,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 204,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 205,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 206,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 207,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 208,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 209,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 212,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 213,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 214,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 215,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 216,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 217,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 218,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 219,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 220,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 221,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 222,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 223,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 224,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 225,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 226,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 227,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 228,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 229,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 230,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 231,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 232,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 234,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 236,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 237,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 238,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 239,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 240,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 241,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 242,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 243,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 244,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 245,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 246,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 247,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 248,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 249,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 250,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 251,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 252,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 253,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 254,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 255,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 256,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 257,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 259,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 260,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 261,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 262,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 263,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 264,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 265,
          "witness_key": "obs:temp-10-20km"
        },
        {
          "row_index": 266,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 267,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 268,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 269,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 270,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 271,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 272,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 273,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 274,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 275,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 276,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 277,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 278,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 279,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 280,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 281,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 282,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 283,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 284,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 285,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 286,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 287,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 288,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 289,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 290,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 291,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 292,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 293,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 294,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 295,
          "witness_key": "obs:rb-rc2"
        }
      ]
    },
    {
      "question_id": "CQ-T2-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The thickness, the flank it belongs to and the age of that crust are all on one quantity row, the flank as its subject and the age in its name. The earlier study that supplies the figure is not tied to it by anything returned: the contract has research relations for exactly that tie and uses them elsewhere in the run, so this is an omission rather than a missing type.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "source_study",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The contract carries research relations that can tie a record to a bibliographic source, and the run uses them for the article's own reference list; nothing ties this thickness to the earlier study the article credits it to, and no gap declares the omission."
        },
        {
          "semantic": "crustal_thickness_claim",
          "row_index": 410,
          "absent_reason": null,
          "note": "The thickness is returned as a quantity row with its bound and unit."
        },
        {
          "semantic": "location_relation",
          "row_index": 410,
          "absent_reason": null,
          "note": "The same row resolves its subject to the ridge flank the thickness belongs to."
        },
        {
          "semantic": "crustal_age",
          "row_index": 410,
          "absent_reason": null,
          "note": "The age of that crust is carried on the same row's name, tied to the same flank; it is prose on the row rather than a separate quantity record."
        }
      ],
      "source_locators": [
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "work:ref:01"
        },
        {
          "row_index": 1,
          "witness_key": "work:ref:02"
        },
        {
          "row_index": 2,
          "witness_key": "work:ref:03"
        },
        {
          "row_index": 3,
          "witness_key": "work:ref:04"
        },
        {
          "row_index": 4,
          "witness_key": "work:ref:05"
        },
        {
          "row_index": 5,
          "witness_key": "work:ref:06"
        },
        {
          "row_index": 6,
          "witness_key": "work:ref:07"
        },
        {
          "row_index": 7,
          "witness_key": "work:ref:08"
        },
        {
          "row_index": 8,
          "witness_key": "work:ref:09"
        },
        {
          "row_index": 9,
          "witness_key": "work:ref:10"
        },
        {
          "row_index": 10,
          "witness_key": "work:ref:11"
        },
        {
          "row_index": 11,
          "witness_key": "work:ref:12"
        },
        {
          "row_index": 12,
          "witness_key": "work:ref:13"
        },
        {
          "row_index": 13,
          "witness_key": "work:ref:14"
        },
        {
          "row_index": 14,
          "witness_key": "work:ref:15"
        },
        {
          "row_index": 15,
          "witness_key": "work:ref:16"
        },
        {
          "row_index": 16,
          "witness_key": "work:ref:17"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref:18"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref:19"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref:20"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref:21"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref:22"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref:23"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref:24"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref:25"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref:26"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref:27"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref:28"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref:29"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref:30"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref:31"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref:32"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref:33"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref:34"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref:35"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref:36"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref:37"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref:38"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref:39"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref:40"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref:41"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref:42"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref:43"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref:44"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref:45"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref:46"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref:47"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref:48"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref:49"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref:50"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref:51"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref:52"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref:53"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref:54"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref:55"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref:56"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref:57"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref:58"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref:59"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref:60"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref:61"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref:62"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref:63"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref:64"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref:65"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref:66"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref:67"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref:68"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref:69"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref:70"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref:71"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref:72"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref:73"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref:74"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref:75"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref:76"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref:77"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref:78"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref:79"
        },
        {
          "row_index": 79,
          "witness_key": "work:yu-2025"
        },
        {
          "row_index": 80,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 81,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 82,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 83,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 84,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 85,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 86,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 87,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 88,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 89,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 90,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 91,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 92,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 93,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 94,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 95,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 96,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 97,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 98,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 99,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 100,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 101,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 102,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 103,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 104,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 105,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 106,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 107,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 108,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 109,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 110,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 111,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 112,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 113,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 114,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 115,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 116,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 117,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 118,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 119,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 120,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 121,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 122,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 123,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 124,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 125,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 126,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 127,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 128,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 129,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 130,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 131,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 132,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 133,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 134,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 135,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 136,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 137,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 138,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 139,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 140,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 141,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 142,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 143,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 144,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 145,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 146,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 147,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 148,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 149,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 150,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 151,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 152,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 153,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 154,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 155,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 156,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 157,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 158,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 159,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 160,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 161,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 162,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 163,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 164,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 165,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 166,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 167,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 168,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 169,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 170,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 171,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 172,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 173,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 174,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 175,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 176,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 177,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 178,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 179,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 184,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 186,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 187,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 188,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 189,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 190,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 191,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 192,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 193,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 194,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 195,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 196,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 197,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 198,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 199,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 200,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 201,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 202,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 203,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 204,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 206,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 207,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 208,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 209,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 210,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 211,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 212,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 213,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 214,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 215,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 216,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 217,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 218,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 219,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 220,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 221,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 222,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 223,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 224,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 226,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 227,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 228,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 229,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 230,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 231,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 232,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 233,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 234,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 235,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 236,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 237,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 238,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 239,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 240,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 241,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 242,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 243,
          "witness_key": "rel:yu-2025-cites-01"
        },
        {
          "row_index": 244,
          "witness_key": "rel:yu-2025-cites-02"
        },
        {
          "row_index": 245,
          "witness_key": "rel:yu-2025-cites-03"
        },
        {
          "row_index": 246,
          "witness_key": "rel:yu-2025-cites-04"
        },
        {
          "row_index": 247,
          "witness_key": "rel:yu-2025-cites-05"
        },
        {
          "row_index": 248,
          "witness_key": "rel:yu-2025-cites-06"
        },
        {
          "row_index": 249,
          "witness_key": "rel:yu-2025-cites-07"
        },
        {
          "row_index": 250,
          "witness_key": "rel:yu-2025-cites-08"
        },
        {
          "row_index": 251,
          "witness_key": "rel:yu-2025-cites-09"
        },
        {
          "row_index": 252,
          "witness_key": "rel:yu-2025-cites-10"
        },
        {
          "row_index": 253,
          "witness_key": "rel:yu-2025-cites-11"
        },
        {
          "row_index": 254,
          "witness_key": "rel:yu-2025-cites-12"
        },
        {
          "row_index": 255,
          "witness_key": "rel:yu-2025-cites-13"
        },
        {
          "row_index": 256,
          "witness_key": "rel:yu-2025-cites-14"
        },
        {
          "row_index": 257,
          "witness_key": "rel:yu-2025-cites-15"
        },
        {
          "row_index": 258,
          "witness_key": "rel:yu-2025-cites-16"
        },
        {
          "row_index": 259,
          "witness_key": "rel:yu-2025-cites-17"
        },
        {
          "row_index": 260,
          "witness_key": "rel:yu-2025-cites-18"
        },
        {
          "row_index": 261,
          "witness_key": "rel:yu-2025-cites-19"
        },
        {
          "row_index": 262,
          "witness_key": "rel:yu-2025-cites-20"
        },
        {
          "row_index": 263,
          "witness_key": "rel:yu-2025-cites-21"
        },
        {
          "row_index": 264,
          "witness_key": "rel:yu-2025-cites-22"
        },
        {
          "row_index": 265,
          "witness_key": "rel:yu-2025-cites-23"
        },
        {
          "row_index": 266,
          "witness_key": "rel:yu-2025-cites-24"
        },
        {
          "row_index": 267,
          "witness_key": "rel:yu-2025-cites-25"
        },
        {
          "row_index": 268,
          "witness_key": "rel:yu-2025-cites-26"
        },
        {
          "row_index": 269,
          "witness_key": "rel:yu-2025-cites-27"
        },
        {
          "row_index": 270,
          "witness_key": "rel:yu-2025-cites-28"
        },
        {
          "row_index": 271,
          "witness_key": "rel:yu-2025-cites-29"
        },
        {
          "row_index": 272,
          "witness_key": "rel:yu-2025-cites-30"
        },
        {
          "row_index": 273,
          "witness_key": "rel:yu-2025-cites-31"
        },
        {
          "row_index": 274,
          "witness_key": "rel:yu-2025-cites-32"
        },
        {
          "row_index": 275,
          "witness_key": "rel:yu-2025-cites-33"
        },
        {
          "row_index": 276,
          "witness_key": "rel:yu-2025-cites-34"
        },
        {
          "row_index": 277,
          "witness_key": "rel:yu-2025-cites-35"
        },
        {
          "row_index": 278,
          "witness_key": "rel:yu-2025-cites-36"
        },
        {
          "row_index": 279,
          "witness_key": "rel:yu-2025-cites-37"
        },
        {
          "row_index": 280,
          "witness_key": "rel:yu-2025-cites-38"
        },
        {
          "row_index": 281,
          "witness_key": "rel:yu-2025-cites-39"
        },
        {
          "row_index": 282,
          "witness_key": "rel:yu-2025-cites-40"
        },
        {
          "row_index": 283,
          "witness_key": "rel:yu-2025-cites-41"
        },
        {
          "row_index": 284,
          "witness_key": "rel:yu-2025-cites-42"
        },
        {
          "row_index": 285,
          "witness_key": "rel:yu-2025-cites-43"
        },
        {
          "row_index": 286,
          "witness_key": "rel:yu-2025-cites-44"
        },
        {
          "row_index": 287,
          "witness_key": "rel:yu-2025-cites-45"
        },
        {
          "row_index": 288,
          "witness_key": "rel:yu-2025-cites-46"
        },
        {
          "row_index": 289,
          "witness_key": "rel:yu-2025-cites-47"
        },
        {
          "row_index": 290,
          "witness_key": "rel:yu-2025-cites-48"
        },
        {
          "row_index": 291,
          "witness_key": "rel:yu-2025-cites-49"
        },
        {
          "row_index": 292,
          "witness_key": "rel:yu-2025-cites-50"
        },
        {
          "row_index": 293,
          "witness_key": "rel:yu-2025-cites-51"
        },
        {
          "row_index": 294,
          "witness_key": "rel:yu-2025-cites-52"
        },
        {
          "row_index": 295,
          "witness_key": "rel:yu-2025-cites-53"
        },
        {
          "row_index": 296,
          "witness_key": "rel:yu-2025-cites-54"
        },
        {
          "row_index": 297,
          "witness_key": "rel:yu-2025-cites-55"
        },
        {
          "row_index": 298,
          "witness_key": "rel:yu-2025-cites-56"
        },
        {
          "row_index": 299,
          "witness_key": "rel:yu-2025-cites-57"
        },
        {
          "row_index": 300,
          "witness_key": "rel:yu-2025-cites-58"
        },
        {
          "row_index": 301,
          "witness_key": "rel:yu-2025-cites-59"
        },
        {
          "row_index": 302,
          "witness_key": "rel:yu-2025-cites-60"
        },
        {
          "row_index": 303,
          "witness_key": "rel:yu-2025-cites-61"
        },
        {
          "row_index": 304,
          "witness_key": "rel:yu-2025-cites-62"
        },
        {
          "row_index": 305,
          "witness_key": "rel:yu-2025-cites-63"
        },
        {
          "row_index": 306,
          "witness_key": "rel:yu-2025-cites-64"
        },
        {
          "row_index": 307,
          "witness_key": "rel:yu-2025-cites-65"
        },
        {
          "row_index": 308,
          "witness_key": "rel:yu-2025-cites-66"
        },
        {
          "row_index": 309,
          "witness_key": "rel:yu-2025-cites-67"
        },
        {
          "row_index": 310,
          "witness_key": "rel:yu-2025-cites-68"
        },
        {
          "row_index": 311,
          "witness_key": "rel:yu-2025-cites-69"
        },
        {
          "row_index": 312,
          "witness_key": "rel:yu-2025-cites-70"
        },
        {
          "row_index": 313,
          "witness_key": "rel:yu-2025-cites-71"
        },
        {
          "row_index": 314,
          "witness_key": "rel:yu-2025-cites-72"
        },
        {
          "row_index": 315,
          "witness_key": "rel:yu-2025-cites-73"
        },
        {
          "row_index": 316,
          "witness_key": "rel:yu-2025-cites-74"
        },
        {
          "row_index": 317,
          "witness_key": "rel:yu-2025-cites-75"
        },
        {
          "row_index": 318,
          "witness_key": "rel:yu-2025-cites-76"
        },
        {
          "row_index": 319,
          "witness_key": "rel:yu-2025-cites-77"
        },
        {
          "row_index": 320,
          "witness_key": "rel:yu-2025-cites-78"
        },
        {
          "row_index": 321,
          "witness_key": "rel:yu-2025-cites-79"
        },
        {
          "row_index": 322,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 323,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 324,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 325,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 326,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 327,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 328,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 329,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 330,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 331,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 332,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 333,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 334,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 335,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 336,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 337,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 338,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 339,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 340,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 341,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 342,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 343,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 344,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 345,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 346,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 347,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 348,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 349,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 350,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 351,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 352,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 353,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 354,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 355,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 356,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 357,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 358,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 359,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 360,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 361,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 362,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 363,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 364,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 365,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 366,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 367,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 368,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 369,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 370,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 371,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 372,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 373,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 374,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 375,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 376,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 377,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 378,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 379,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 380,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 381,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 382,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 383,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 384,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 385,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 386,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 387,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 388,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 389,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 390,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 391,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 392,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 393,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 394,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 395,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 396,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 397,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 398,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 399,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 400,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 401,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 402,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 403,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 404,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 405,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 406,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 407,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 408,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 409,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 410,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 411,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 412,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 413,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 414,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 415,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 416,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 417,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 418,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 419,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 420,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 421,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 422,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 423,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 424,
          "witness_key": "obs:temp-10-20km"
        },
        {
          "row_index": 425,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 426,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 427,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 428,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 429,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 430,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 431,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 432,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 433,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 434,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 435,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 436,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 437,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 438,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 439,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 440,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 441,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 442,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 443,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 444,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 445,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 446,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 447,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 448,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 449,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 450,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 451,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 452,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 453,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 454,
          "witness_key": "obs:rb-rc2"
        }
      ]
    },
    {
      "question_id": "CQ-T2-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One funding relation carries all four: the funding record, the award identifier, the individual it is attributed to and the attribution itself.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "funding_record",
          "row_index": 26,
          "absent_reason": null,
          "note": "A returned funding relation is the funding record the question asks about."
        },
        {
          "semantic": "grant_identifier",
          "row_index": 26,
          "absent_reason": null,
          "note": "The award identifier is a field on that relation row."
        },
        {
          "semantic": "person",
          "row_index": 26,
          "absent_reason": null,
          "note": "The relation's target endpoint is the individual author the grant is attributed to."
        },
        {
          "semantic": "attribution_relation",
          "row_index": 26,
          "absent_reason": null,
          "note": "The relation type and the contribution role on the row are the attribution itself."
        }
      ],
      "source_locators": [
        "page:10:block:044"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "agent:ab"
        },
        {
          "row_index": 1,
          "witness_key": "agent:ayyang"
        },
        {
          "row_index": 2,
          "witness_key": "agent:cartigny"
        },
        {
          "row_index": 3,
          "witness_key": "agent:ch"
        },
        {
          "row_index": 4,
          "witness_key": "agent:crew"
        },
        {
          "row_index": 5,
          "witness_key": "agent:db"
        },
        {
          "row_index": 6,
          "witness_key": "agent:geli"
        },
        {
          "row_index": 7,
          "witness_key": "agent:lg"
        },
        {
          "row_index": 8,
          "witness_key": "agent:lp"
        },
        {
          "row_index": 9,
          "witness_key": "agent:mm"
        },
        {
          "row_index": 10,
          "witness_key": "agent:scs"
        },
        {
          "row_index": 11,
          "witness_key": "agent:zwang"
        },
        {
          "row_index": 12,
          "witness_key": "agent:zy"
        },
        {
          "row_index": 13,
          "witness_key": "org:brittany"
        },
        {
          "row_index": 14,
          "witness_key": "org:cnr-igag"
        },
        {
          "row_index": 15,
          "witness_key": "org:erc"
        },
        {
          "row_index": 16,
          "witness_key": "org:french-gov"
        },
        {
          "row_index": 17,
          "witness_key": "org:geo-ocean"
        },
        {
          "row_index": 18,
          "witness_key": "org:independent"
        },
        {
          "row_index": 19,
          "witness_key": "org:ipgp"
        },
        {
          "row_index": 20,
          "witness_key": "org:isblue"
        },
        {
          "row_index": 21,
          "witness_key": "org:modena"
        },
        {
          "row_index": 22,
          "witness_key": "org:nsfc"
        },
        {
          "row_index": 23,
          "witness_key": "org:sio"
        },
        {
          "row_index": 24,
          "witness_key": "org:tgir"
        },
        {
          "row_index": 25,
          "witness_key": "org:zjnsf"
        },
        {
          "row_index": 26,
          "witness_key": "rel:fund:erc-advanced"
        },
        {
          "row_index": 27,
          "witness_key": "rel:fund:erc-fp7"
        },
        {
          "row_index": 28,
          "witness_key": "rel:fund:nsfc:42330308"
        },
        {
          "row_index": 29,
          "witness_key": "rel:fund:nsfc:42422603"
        },
        {
          "row_index": 30,
          "witness_key": "rel:fund:zjnsf"
        }
      ]
    },
    {
      "question_id": "CQ-T3-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The depth range, unit, subject and measurement status come from the quantity row whose subject is the segment's axis; the datum the depths are measured from is carried by a second row for the same events. Nothing joins the two rows.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 226,
          "absent_reason": null,
          "note": "The depth range of the deep events beneath the magmatic segment's axis is returned as a bounded quantity."
        },
        {
          "semantic": "length_unit",
          "row_index": 226,
          "absent_reason": null,
          "note": "The unit field on that row states the unit."
        },
        {
          "semantic": "quantity_subject",
          "row_index": 226,
          "absent_reason": null,
          "note": "That row resolves its subject to the axis of the magmatic segment, which is the subject the question names."
        },
        {
          "semantic": "measurement_status",
          "row_index": 226,
          "absent_reason": null,
          "note": "The determination field on the row says the depths were measured here rather than taken from elsewhere."
        },
        {
          "semantic": "depth_reference_surface",
          "row_index": 225,
          "absent_reason": null,
          "note": "A second depth row for the same deep events carries the datum the depths are measured from."
        }
      ],
      "source_locators": [
        "page:2:block:006",
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 4,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 5,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 6,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 7,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 11,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 12,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 18,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 20,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 21,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 22,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 24,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 25,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 26,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 27,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 32,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 34,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 42,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 44,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 45,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 49,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 51,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 53,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 54,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 55,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 56,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 57,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 58,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 59,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 60,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 61,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 62,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 63,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 64,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 65,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 67,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 68,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 69,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 70,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 71,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 72,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 73,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 75,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 76,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 77,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 78,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 79,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 80,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 83,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 84,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 85,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 86,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 87,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 88,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 91,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 92,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 93,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 94,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 95,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 96,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 106,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 107,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 108,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 109,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 110,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 111,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 112,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 113,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 114,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 115,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 116,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 117,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 118,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 119,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 120,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 122,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 123,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 124,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 125,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 126,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 128,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 129,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 130,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 131,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 132,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 133,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 134,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 135,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 136,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 137,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 138,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 139,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 140,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 141,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 142,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 143,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 144,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 145,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 147,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 148,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 149,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 150,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 151,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 152,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 153,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 154,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 155,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 156,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 158,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 159,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 160,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 161,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 162,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 163,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 164,
          "witness_key": "event:romanche-2016:sub1"
        },
        {
          "row_index": 165,
          "witness_key": "event:romanche-2016:sub2"
        },
        {
          "row_index": 166,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 167,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 168,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 169,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 170,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 171,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 172,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 173,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 174,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 175,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 176,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 177,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 178,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 179,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 180,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 181,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 182,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 183,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 184,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 185,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 186,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 187,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 188,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 189,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 190,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 191,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 192,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 193,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 194,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 195,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 196,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 197,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 198,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 199,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 200,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 201,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 202,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 203,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 204,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 205,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 206,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 207,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 209,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 212,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 213,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 214,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 215,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 216,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 217,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 218,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 219,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 220,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 221,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 222,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 223,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 224,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 225,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 226,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 227,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 229,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 230,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 231,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 232,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 233,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 237,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 238,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 239,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 240,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 241,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 242,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 243,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 244,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 245,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 246,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 247,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 248,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 249,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 250,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 251,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 252,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 253,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 254,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 255,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 256,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 257,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 258,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 259,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 260,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 261,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 262,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 263,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 264,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 265,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 266,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 267,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 268,
          "witness_key": "obs:temp-10-20km"
        },
        {
          "row_index": 269,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 270,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 271,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 272,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 273,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 274,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 275,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 276,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 277,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 278,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 279,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 280,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 281,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 282,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 283,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 284,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 285,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 286,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 287,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 288,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 289,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 290,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 291,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 292,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 293,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 294,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 295,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 296,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 297,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 298,
          "witness_key": "obs:rb-rc2"
        }
      ]
    },
    {
      "question_id": "CQ-T3-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One quantity row carries the range, the unit, the melts it belongs to and the fact that the figure was calculated.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 289,
          "absent_reason": null,
          "note": "The primary-melt carbon dioxide content of the studied segment is returned as a bounded quantity."
        },
        {
          "semantic": "concentration_unit",
          "row_index": 289,
          "absent_reason": null,
          "note": "The unit field on that row states the concentration unit."
        },
        {
          "semantic": "quantity_subject",
          "row_index": 289,
          "absent_reason": null,
          "note": "The row's subject resolves to the primary melts, and its name ties the figure to the studied segment."
        },
        {
          "semantic": "calculated_or_measured_status",
          "row_index": 289,
          "absent_reason": null,
          "note": "The determination and modality fields on the row say the content was arrived at by calculation rather than measured."
        }
      ],
      "source_locators": [
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 4,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 5,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 6,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 7,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 11,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 12,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 18,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 20,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 21,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 22,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 24,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 25,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 26,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 27,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 32,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 34,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 42,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 44,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 45,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 49,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 51,
          "witness_key": "material:melt"
        },
        {
          "row_index": 52,
          "witness_key": "material:melt:primary"
        },
        {
          "row_index": 53,
          "witness_key": "material:melt:primitive"
        },
        {
          "row_index": 54,
          "witness_key": "melt:pre-eruptive-rc2"
        },
        {
          "row_index": 55,
          "witness_key": "melt:rc2-calculated"
        },
        {
          "row_index": 56,
          "witness_key": "sample:basaltic-rocks"
        },
        {
          "row_index": 57,
          "witness_key": "sample:morb"
        },
        {
          "row_index": 58,
          "witness_key": "sample:rock-samples"
        },
        {
          "row_index": 59,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 60,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 62,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 63,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 64,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 65,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 66,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 67,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 68,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 69,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 70,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 71,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 72,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 73,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 74,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 75,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 76,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 77,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 78,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 79,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 80,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 81,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 83,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 84,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 85,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 86,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 87,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 88,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 89,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 90,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 91,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 92,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 93,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 114,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 115,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 116,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 117,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 118,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 119,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 120,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 121,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 122,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 124,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 125,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 126,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 127,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 128,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 129,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 130,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 131,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 132,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 133,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 134,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 135,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 136,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 137,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 138,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 139,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 140,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 141,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 142,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 143,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 144,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 145,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 146,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 147,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 148,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 149,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 150,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 151,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 153,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 159,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 160,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 161,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 162,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 163,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 164,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 165,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 166,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 167,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 168,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 169,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 170,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 171,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 172,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 173,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 174,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 175,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 176,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 177,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 178,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 179,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 180,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 181,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 182,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 183,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 184,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 185,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 186,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 187,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 188,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 189,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 190,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 191,
          "witness_key": "rel:melt-from-mantle"
        },
        {
          "row_index": 192,
          "witness_key": "rel:melt-rc2-in-rc2"
        },
        {
          "row_index": 193,
          "witness_key": "rel:morb-sampled-rc2"
        },
        {
          "row_index": 194,
          "witness_key": "rel:morb-sampled-rc3"
        },
        {
          "row_index": 195,
          "witness_key": "rel:samples-from-rti-area"
        },
        {
          "row_index": 196,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 197,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 198,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 199,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 200,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 201,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 202,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 203,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 204,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 205,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 206,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 207,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 209,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 210,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 211,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 212,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 213,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 214,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 215,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 216,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 217,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 218,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 219,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 220,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 221,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 222,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 223,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 224,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 225,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 226,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 227,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 228,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 229,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 230,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 231,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 232,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 233,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 234,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 235,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 236,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 237,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 238,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 239,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 240,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 241,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 242,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 243,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 244,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 245,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 246,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 247,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 248,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 249,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 250,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 251,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 253,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 254,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 255,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 256,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 257,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 258,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 259,
          "witness_key": "obs:co2-atlantic-max"
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
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 263,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 264,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 265,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 266,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 267,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 268,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 269,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 270,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 271,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 272,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 273,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 274,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 275,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 276,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 277,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 278,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 279,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 280,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 281,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 282,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 283,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 284,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 285,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 286,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 287,
          "witness_key": "obs:temp-10-20km"
        },
        {
          "row_index": 288,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 289,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 290,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 291,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 292,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 293,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 294,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 295,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 296,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 297,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 298,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 299,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 300,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 301,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 302,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 303,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 304,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 305,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 306,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 307,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 308,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 309,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 310,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 311,
          "witness_key": "ratio:co2-rb"
        }
      ]
    },
    {
      "question_id": "CQ-T3-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The range, the unit and the estimate status are on one quantity row; the pre-eruptive stage is carried as a typed field on a melt record for the same segments. Nothing in the result joins the two rows.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 264,
          "absent_reason": null,
          "note": "The pre-eruptive concentration range for the studied segment is returned as a bounded quantity."
        },
        {
          "semantic": "concentration_unit",
          "row_index": 264,
          "absent_reason": null,
          "note": "The unit field on that row states the concentration unit."
        },
        {
          "semantic": "melt_stage",
          "row_index": 54,
          "absent_reason": null,
          "note": "A returned melt record carries the pre-eruptive stage as a typed field, for the melts of the same segments."
        },
        {
          "semantic": "estimation_status",
          "row_index": 264,
          "absent_reason": null,
          "note": "The determination field on the quantity row says the range is an estimate."
        }
      ],
      "source_locators": [
        "page:5:block:006",
        "page:8:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 4,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 5,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 6,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 7,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 11,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 12,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 18,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 20,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 21,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 22,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 24,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 25,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 26,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 27,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 32,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 34,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 42,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 44,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 45,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 49,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 51,
          "witness_key": "material:melt"
        },
        {
          "row_index": 52,
          "witness_key": "material:melt:primary"
        },
        {
          "row_index": 53,
          "witness_key": "material:melt:primitive"
        },
        {
          "row_index": 54,
          "witness_key": "melt:pre-eruptive-rc2"
        },
        {
          "row_index": 55,
          "witness_key": "melt:rc2-calculated"
        },
        {
          "row_index": 56,
          "witness_key": "sample:basaltic-rocks"
        },
        {
          "row_index": 57,
          "witness_key": "sample:morb"
        },
        {
          "row_index": 58,
          "witness_key": "sample:rock-samples"
        },
        {
          "row_index": 59,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 60,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 62,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 63,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 64,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 65,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 66,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 67,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 68,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 69,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 70,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 71,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 72,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 73,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 74,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 75,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 76,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 77,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 78,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 79,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 80,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 81,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 83,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 84,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 85,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 86,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 87,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 88,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 89,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 90,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 91,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 92,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 93,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 114,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 115,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 116,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 117,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 118,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 119,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 120,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 121,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 122,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 124,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 125,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 126,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 127,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 128,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 129,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 130,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 131,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 132,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 133,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 134,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 135,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 136,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 137,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 138,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 139,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 140,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 141,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 142,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 143,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 144,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 145,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 146,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 147,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 148,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 149,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 150,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 151,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 153,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 159,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 160,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 161,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 162,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 163,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 164,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 165,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 166,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 167,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 168,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 169,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 170,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 171,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 172,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 173,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 174,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 175,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 176,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 177,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 178,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 179,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 180,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 181,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 182,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 183,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 184,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 185,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 186,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 187,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 188,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 189,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 190,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 191,
          "witness_key": "rel:melt-from-mantle"
        },
        {
          "row_index": 192,
          "witness_key": "rel:melt-rc2-in-rc2"
        },
        {
          "row_index": 193,
          "witness_key": "rel:morb-sampled-rc2"
        },
        {
          "row_index": 194,
          "witness_key": "rel:morb-sampled-rc3"
        },
        {
          "row_index": 195,
          "witness_key": "rel:samples-from-rti-area"
        },
        {
          "row_index": 196,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 197,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 198,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 199,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 200,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 201,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 202,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 203,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 204,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 205,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 206,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 207,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 209,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 210,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 211,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 212,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 213,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 214,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 215,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 216,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 217,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 218,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 219,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 220,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 221,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 222,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 223,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 224,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 225,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 226,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 227,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 228,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 229,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 230,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 231,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 232,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 233,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 234,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 235,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 236,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 237,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 238,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 239,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 240,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 241,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 242,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 243,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 244,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 245,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 246,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 247,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 248,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 249,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 250,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 251,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 253,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 254,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 255,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 256,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 257,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 258,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 259,
          "witness_key": "obs:co2-atlantic-max"
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
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 263,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 264,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 265,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 266,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 267,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 268,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 269,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 270,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 271,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 272,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 273,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 274,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 275,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 276,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 277,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 278,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 279,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 280,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 281,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 282,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 283,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 284,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 285,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 286,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 287,
          "witness_key": "obs:temp-10-20km"
        },
        {
          "row_index": 288,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 289,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 290,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 291,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 292,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 293,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 294,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 295,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 296,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 297,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 298,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 299,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 300,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 301,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 302,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 303,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 304,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 305,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 306,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 307,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 308,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 309,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 310,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 311,
          "witness_key": "ratio:co2-rb"
        }
      ]
    },
    {
      "question_id": "CQ-T3-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The figure, its unit, its derived status and the set of events that went through relocation are all carried by returned rows. What the average describes is not: the observation type has a subject slot, both uncertainty records leave it unset and nothing else on those rows says which events they cover.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 137,
          "absent_reason": null,
          "note": "The updated average horizontal uncertainty after relocation is returned as a quantity row."
        },
        {
          "semantic": "length_unit",
          "row_index": 137,
          "absent_reason": null,
          "note": "The unit field on that row states the unit."
        },
        {
          "semantic": "quantity_subject",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "Both uncertainty rows leave the subject slot the observation type provides unset, and nothing else in their projections says which events the average describes; no gap is declared for it."
        },
        {
          "semantic": "derivation_status",
          "row_index": 137,
          "absent_reason": null,
          "note": "The determination field on the row says the figure is derived rather than read off."
        },
        {
          "semantic": "event_set",
          "row_index": 79,
          "absent_reason": null,
          "note": "A returned count row names the well-constrained events that went through the relocation, which is the set the catalogue figure describes."
        }
      ],
      "source_locators": [
        "page:7:block:006",
        "page:7:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "instrument:obs"
        },
        {
          "row_index": 1,
          "witness_key": "method:ba90-rb90"
        },
        {
          "row_index": 2,
          "witness_key": "method:depth-resolution-tests"
        },
        {
          "row_index": 3,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 4,
          "witness_key": "method:fc-correction"
        },
        {
          "row_index": 5,
          "witness_key": "method:focal-mechanism"
        },
        {
          "row_index": 6,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 7,
          "witness_key": "method:manual-arrival-check"
        },
        {
          "row_index": 8,
          "witness_key": "method:max-depth-compilation"
        },
        {
          "row_index": 9,
          "witness_key": "method:morb-compilation"
        },
        {
          "row_index": 10,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 11,
          "witness_key": "method:quality-classification"
        },
        {
          "row_index": 12,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 13,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 14,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 15,
          "witness_key": "model:co2-solubility"
        },
        {
          "row_index": 16,
          "witness_key": "model:minimum-1d"
        },
        {
          "row_index": 17,
          "witness_key": "model:thermal"
        },
        {
          "row_index": 18,
          "witness_key": "model:velocity-1d"
        },
        {
          "row_index": 19,
          "witness_key": "model:velocity-average"
        },
        {
          "row_index": 20,
          "witness_key": "model:velocity-fastest"
        },
        {
          "row_index": 21,
          "witness_key": "software:global-mapper"
        },
        {
          "row_index": 22,
          "witness_key": "software:gmt"
        },
        {
          "row_index": 23,
          "witness_key": "software:hash"
        },
        {
          "row_index": 24,
          "witness_key": "software:hypodd"
        },
        {
          "row_index": 25,
          "witness_key": "software:nonlinloc"
        },
        {
          "row_index": 26,
          "witness_key": "software:seisan"
        },
        {
          "row_index": 27,
          "witness_key": "software:velest"
        },
        {
          "row_index": 28,
          "witness_key": "software:zmap"
        },
        {
          "row_index": 29,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 30,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 31,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 32,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 33,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 34,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 35,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 36,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 37,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 38,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 39,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 40,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 41,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 42,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 43,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 44,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 45,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 46,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 47,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 48,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 49,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 50,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 51,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 53,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 54,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 55,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 56,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 57,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 58,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 59,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 60,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 61,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 62,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 63,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 64,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 65,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 66,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 67,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 68,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:forced-depth-tests"
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
          "witness_key": "cnt:located-earthquakes-methods"
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
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:sub-dataset-arrivals"
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
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 84,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 85,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 86,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 87,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 88,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 89,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 90,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 91,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 92,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 93,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 94,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 95,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 96,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 97,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 98,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 99,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 100,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 101,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 102,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 103,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 104,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 105,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 106,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 107,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 108,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 109,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 110,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 111,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 112,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 113,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 114,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 115,
          "witness_key": "obs:low-frequency-cutoff"
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
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 121,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 122,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 124,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 125,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 126,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 127,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 128,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 129,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 130,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 131,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 132,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 133,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 134,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 135,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 136,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 137,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 138,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 139,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 140,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 141,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 142,
          "witness_key": "event:romanche-2016:sub1"
        },
        {
          "row_index": 143,
          "witness_key": "event:romanche-2016:sub2"
        },
        {
          "row_index": 144,
          "witness_key": "rel:tests-support-constrained"
        },
        {
          "row_index": 145,
          "witness_key": "rel:tests-support-deep"
        },
        {
          "row_index": 146,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 147,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 148,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 149,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 150,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 151,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 152,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 153,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 154,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 155,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 156,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 157,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 158,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 159,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 160,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 161,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 162,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 163,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 164,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 165,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 166,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 167,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 168,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 169,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 170,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 171,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 172,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 173,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 174,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 175,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 176,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 177,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 178,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 179,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 180,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 181,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 182,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 183,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 184,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 185,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 186,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 187,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 188,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 189,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 190,
          "witness_key": "claim:rc1-amagmatic"
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
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 194,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 195,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 196,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 197,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 198,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 199,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 200,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 201,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 202,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 203,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 204,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 205,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 206,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 207,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 208,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 209,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 210,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 211,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 212,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 213,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 214,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 215,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 216,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 217,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 218,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 219,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 220,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 221,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 222,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 223,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 224,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 225,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 226,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 227,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 228,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 229,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 230,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 231,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 232,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 233,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 234,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 235,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 236,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 237,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 238,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 239,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 240,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 241,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 242,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 243,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 244,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 245,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 246,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 247,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 248,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 249,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 250,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 251,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 253,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 254,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 255,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 256,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 257,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 259,
          "witness_key": "obs:temp-10-20km"
        }
      ]
    },
    {
      "question_id": "CQ-T3-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Pressure and temperature are separate quantity rows, each with its unit, and both record that the conditions come from a solubility model. The melt is named on the pressure row rather than resolved through a subject slot, which is enough to name the bearer.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 126,
          "absent_reason": null,
          "note": "The saturation pressure is returned as a quantity row."
        },
        {
          "semantic": "pressure_unit",
          "row_index": 126,
          "absent_reason": null,
          "note": "The unit field on that row states the pressure unit."
        },
        {
          "semantic": "temperature_unit",
          "row_index": 127,
          "absent_reason": null,
          "note": "The companion row for the saturation temperature carries the temperature unit."
        },
        {
          "semantic": "quantity_subject",
          "row_index": 126,
          "absent_reason": null,
          "note": "The row's name identifies the melt as the thing that becomes saturated, which is the bearer the question asks about; the subject slot itself is unset."
        },
        {
          "semantic": "model_derived_status",
          "row_index": 126,
          "absent_reason": null,
          "note": "The determination field says the conditions come from a model rather than from measurement."
        }
      ],
      "source_locators": [
        "page:5:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "material:melt"
        },
        {
          "row_index": 1,
          "witness_key": "material:melt:primary"
        },
        {
          "row_index": 2,
          "witness_key": "material:melt:primitive"
        },
        {
          "row_index": 3,
          "witness_key": "melt:pre-eruptive-rc2"
        },
        {
          "row_index": 4,
          "witness_key": "melt:rc2-calculated"
        },
        {
          "row_index": 5,
          "witness_key": "method:ba90-rb90"
        },
        {
          "row_index": 6,
          "witness_key": "method:depth-resolution-tests"
        },
        {
          "row_index": 7,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 8,
          "witness_key": "method:fc-correction"
        },
        {
          "row_index": 9,
          "witness_key": "method:focal-mechanism"
        },
        {
          "row_index": 10,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 11,
          "witness_key": "method:manual-arrival-check"
        },
        {
          "row_index": 12,
          "witness_key": "method:max-depth-compilation"
        },
        {
          "row_index": 13,
          "witness_key": "method:morb-compilation"
        },
        {
          "row_index": 14,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 15,
          "witness_key": "method:quality-classification"
        },
        {
          "row_index": 16,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 17,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 18,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 19,
          "witness_key": "model:co2-solubility"
        },
        {
          "row_index": 20,
          "witness_key": "model:minimum-1d"
        },
        {
          "row_index": 21,
          "witness_key": "model:thermal"
        },
        {
          "row_index": 22,
          "witness_key": "model:velocity-1d"
        },
        {
          "row_index": 23,
          "witness_key": "model:velocity-average"
        },
        {
          "row_index": 24,
          "witness_key": "model:velocity-fastest"
        },
        {
          "row_index": 25,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 26,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 27,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 28,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 29,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 30,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 31,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 32,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 33,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 34,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 35,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 36,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 37,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 38,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 39,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 41,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 42,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 43,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 44,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 45,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 46,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 47,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 48,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 49,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 50,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 51,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 52,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 53,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 54,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 55,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 56,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 57,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 58,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 59,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 60,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 61,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 62,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 63,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 64,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 65,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 66,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 67,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 68,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 70,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 71,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 72,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 73,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 74,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 80,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 81,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 82,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 83,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 84,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 85,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 86,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 87,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 88,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 89,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 90,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 91,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 92,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 93,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 94,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 95,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 96,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 97,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 98,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 99,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 100,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 101,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 102,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 103,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 104,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 105,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 106,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 107,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 108,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 109,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 110,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 111,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 112,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 113,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 114,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 115,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 116,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 117,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 118,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 119,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 120,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 121,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 122,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 123,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 124,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 125,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 126,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 127,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 128,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 129,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 130,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 131,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 132,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 133,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 134,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 135,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 136,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 137,
          "witness_key": "rel:tests-support-constrained"
        },
        {
          "row_index": 138,
          "witness_key": "rel:tests-support-deep"
        },
        {
          "row_index": 139,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 140,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 141,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 142,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 143,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 144,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 145,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 146,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 147,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 148,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 149,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 150,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 151,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 152,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 153,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 154,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 155,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 156,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 157,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 158,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 159,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 160,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 161,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 162,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 163,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 164,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 165,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 166,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 167,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 168,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 169,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 170,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 171,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 172,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 173,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 174,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 175,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 176,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 177,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 178,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 179,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 180,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 181,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 182,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 183,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 184,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 185,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 186,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 187,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 188,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 189,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 190,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 191,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 192,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 193,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 194,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 195,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 196,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 197,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 198,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 199,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 200,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 201,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 202,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 203,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 204,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 205,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 206,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 207,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 208,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 209,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 210,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 211,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 212,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 213,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 214,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 215,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 216,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 217,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 218,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 219,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 220,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 221,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 222,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 223,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 224,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 225,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 226,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 227,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 228,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 229,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 230,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 231,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 232,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 233,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 234,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 235,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 236,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 237,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 238,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 239,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 240,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 241,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 242,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 243,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 244,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 245,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 246,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 247,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 248,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 249,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 250,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 251,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 252,
          "witness_key": "obs:temp-10-20km"
        }
      ]
    },
    {
      "question_id": "CQ-T4-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One claim row carries the explanation, its preferred standing, the strength with which it is put and the segment it is about.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "causal_claim",
          "row_index": 122,
          "absent_reason": null,
          "note": "The degassing explanation is returned as a claim record of its own."
        },
        {
          "semantic": "preferred_disposition",
          "row_index": 122,
          "absent_reason": null,
          "note": "The hypothesis disposition field on that row marks it as the authors' preferred one."
        },
        {
          "semantic": "epistemic_modality",
          "row_index": 122,
          "absent_reason": null,
          "note": "The modality field records the hedged strength with which it is put."
        },
        {
          "semantic": "claim_subject",
          "row_index": 122,
          "absent_reason": null,
          "note": "The row resolves its subject to the segment the deep earthquakes lie under."
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 4,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 5,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 6,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 7,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 11,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 12,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 18,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 20,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 21,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 22,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 24,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 25,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 26,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 27,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 32,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 34,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 42,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 44,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 45,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 49,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 51,
          "witness_key": "material:melt"
        },
        {
          "row_index": 52,
          "witness_key": "material:melt:primary"
        },
        {
          "row_index": 53,
          "witness_key": "material:melt:primitive"
        },
        {
          "row_index": 54,
          "witness_key": "melt:pre-eruptive-rc2"
        },
        {
          "row_index": 55,
          "witness_key": "melt:rc2-calculated"
        },
        {
          "row_index": 56,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 57,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 58,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 59,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 60,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 61,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 62,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 63,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 64,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 65,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 66,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 67,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 68,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 69,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 70,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 71,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 72,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 73,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 74,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 75,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 76,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 77,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 78,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 79,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 80,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 81,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 82,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 83,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 84,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 85,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 86,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 88,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 89,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 90,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 91,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 92,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 93,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 94,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 95,
          "witness_key": "event:romanche-2016:sub1"
        },
        {
          "row_index": 96,
          "witness_key": "event:romanche-2016:sub2"
        },
        {
          "row_index": 97,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 98,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 99,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 100,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 101,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 102,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 103,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 104,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 105,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 106,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 107,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 108,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 109,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 110,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 111,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 112,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 113,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 114,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 115,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 116,
          "witness_key": "rel:melt-from-mantle"
        },
        {
          "row_index": 117,
          "witness_key": "rel:melt-rc2-in-rc2"
        },
        {
          "row_index": 118,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 119,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 120,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 121,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 122,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 123,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 124,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 125,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 126,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 127,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 128,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 129,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 130,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 131,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 132,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 133,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 134,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 135,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 136,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 137,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 138,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 139,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 140,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 141,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 142,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 143,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 144,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 145,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 146,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 147,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 148,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 149,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 150,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 151,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 152,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 153,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 154,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 155,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 156,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 157,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 158,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 159,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 160,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 161,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 162,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 163,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 164,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 165,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 166,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 167,
          "witness_key": "claim:seafloor-basalts-degassed"
        }
      ]
    },
    {
      "question_id": "CQ-T4-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The mechanism and its declined standing are on one hypothesis row and the ground for setting it aside on another claim row. The subject of the declined hypothesis is named in that row's own name rather than through the subject slot.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "candidate_mechanism",
          "row_index": 68,
          "absent_reason": null,
          "note": "The melt-movement explanation is returned as a hypothesis record."
        },
        {
          "semantic": "declined_disposition",
          "row_index": 68,
          "absent_reason": null,
          "note": "The disposition field on that row records that the hypothesis is not supported."
        },
        {
          "semantic": "stated_ground",
          "row_index": 138,
          "absent_reason": null,
          "note": "A returned claim carries the ground given for setting it aside, namely that no current eruption is in evidence in the valley."
        },
        {
          "semantic": "claim_subject",
          "row_index": 68,
          "absent_reason": null,
          "note": "The row's name identifies the deep earthquakes as what the hypothesis is about; the subject slot on the record is unset."
        }
      ],
      "source_locators": [
        "page:4:block:002",
        "page:4:block:003",
        "page:5:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 4,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 5,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 6,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 7,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 11,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 12,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 18,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 20,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 21,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 22,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 24,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 25,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 26,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 27,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 32,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 34,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 42,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 44,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 45,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 49,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 51,
          "witness_key": "material:melt"
        },
        {
          "row_index": 52,
          "witness_key": "material:melt:primary"
        },
        {
          "row_index": 53,
          "witness_key": "material:melt:primitive"
        },
        {
          "row_index": 54,
          "witness_key": "melt:pre-eruptive-rc2"
        },
        {
          "row_index": 55,
          "witness_key": "melt:rc2-calculated"
        },
        {
          "row_index": 56,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 57,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 58,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 59,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 60,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 61,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 62,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 63,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 64,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 65,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 66,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 67,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 68,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 69,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 70,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 71,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 72,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 73,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 74,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 75,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 76,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 77,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 78,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 79,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 80,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 81,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 82,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 83,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 84,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 85,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 86,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 88,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 89,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 90,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 91,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 92,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 93,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 94,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 95,
          "witness_key": "event:romanche-2016:sub1"
        },
        {
          "row_index": 96,
          "witness_key": "event:romanche-2016:sub2"
        },
        {
          "row_index": 97,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 98,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 99,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 100,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 101,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 102,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 103,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 104,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 105,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 106,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 107,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 108,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 109,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 110,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 111,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 112,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 113,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 114,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 115,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 116,
          "witness_key": "rel:melt-from-mantle"
        },
        {
          "row_index": 117,
          "witness_key": "rel:melt-rc2-in-rc2"
        },
        {
          "row_index": 118,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 119,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 120,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 121,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 122,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 123,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 124,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 125,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 126,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 127,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 128,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 129,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 130,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 131,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 132,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 133,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 134,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 135,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 136,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 137,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 138,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 139,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 140,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 141,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 142,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 143,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 144,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 145,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 146,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 147,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 148,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 149,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 150,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 151,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 152,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 153,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 154,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 155,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 156,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 157,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 158,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 159,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 160,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 161,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 162,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 163,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 164,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 165,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 166,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 167,
          "witness_key": "claim:seafloor-basalts-degassed"
        }
      ]
    },
    {
      "question_id": "CQ-T4-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The caveat, its limitation standing and what it is about are on one claim row; the claim it qualifies is returned as a separate claim row, which nothing in the result joins to the caveat.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "qualified_claim",
          "row_index": 108,
          "absent_reason": null,
          "note": "The proxy claim the caveat qualifies is returned as its own claim record."
        },
        {
          "semantic": "stated_assumption",
          "row_index": 61,
          "absent_reason": null,
          "note": "The assumption behind the estimate is returned as a claim record."
        },
        {
          "semantic": "caveat_disposition",
          "row_index": 61,
          "absent_reason": null,
          "note": "The claim kind on that row marks it as a limitation, which is the caveat status the question asks about."
        },
        {
          "semantic": "claim_subject",
          "row_index": 61,
          "absent_reason": null,
          "note": "The row's name identifies the estimation of carbon dioxide from trace elements as what the caveat is about."
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "material:melt"
        },
        {
          "row_index": 1,
          "witness_key": "material:melt:primary"
        },
        {
          "row_index": 2,
          "witness_key": "material:melt:primitive"
        },
        {
          "row_index": 3,
          "witness_key": "melt:pre-eruptive-rc2"
        },
        {
          "row_index": 4,
          "witness_key": "melt:rc2-calculated"
        },
        {
          "row_index": 5,
          "witness_key": "method:ba90-rb90"
        },
        {
          "row_index": 6,
          "witness_key": "method:depth-resolution-tests"
        },
        {
          "row_index": 7,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 8,
          "witness_key": "method:fc-correction"
        },
        {
          "row_index": 9,
          "witness_key": "method:focal-mechanism"
        },
        {
          "row_index": 10,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 11,
          "witness_key": "method:manual-arrival-check"
        },
        {
          "row_index": 12,
          "witness_key": "method:max-depth-compilation"
        },
        {
          "row_index": 13,
          "witness_key": "method:morb-compilation"
        },
        {
          "row_index": 14,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 15,
          "witness_key": "method:quality-classification"
        },
        {
          "row_index": 16,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 17,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 18,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 19,
          "witness_key": "model:co2-solubility"
        },
        {
          "row_index": 20,
          "witness_key": "model:minimum-1d"
        },
        {
          "row_index": 21,
          "witness_key": "model:thermal"
        },
        {
          "row_index": 22,
          "witness_key": "model:velocity-1d"
        },
        {
          "row_index": 23,
          "witness_key": "model:velocity-average"
        },
        {
          "row_index": 24,
          "witness_key": "model:velocity-fastest"
        },
        {
          "row_index": 25,
          "witness_key": "sample:basaltic-rocks"
        },
        {
          "row_index": 26,
          "witness_key": "sample:morb"
        },
        {
          "row_index": 27,
          "witness_key": "sample:rock-samples"
        },
        {
          "row_index": 28,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 29,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 30,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 31,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 32,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 33,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 34,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 35,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 36,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 37,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 38,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 39,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 40,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 41,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 42,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 43,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 44,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 45,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 46,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 47,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 48,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 49,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 50,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 51,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 52,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 53,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 54,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 55,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 56,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 57,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 58,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 59,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 60,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 61,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 62,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 63,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 64,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 65,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 66,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 67,
          "witness_key": "rel:tests-support-constrained"
        },
        {
          "row_index": 68,
          "witness_key": "rel:tests-support-deep"
        },
        {
          "row_index": 69,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 70,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 71,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 72,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 73,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 74,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 75,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 76,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 77,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 78,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 79,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 80,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 81,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 82,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 83,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 84,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 85,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 86,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 87,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 88,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 89,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 90,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 91,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 92,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 93,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 94,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 95,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 96,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 97,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 98,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 99,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 100,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 101,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 102,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 103,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 104,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 105,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 106,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 107,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 108,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 109,
          "witness_key": "claim:rc1-amagmatic"
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
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 113,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 114,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 115,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 116,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 117,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 118,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 119,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 120,
          "witness_key": "ratio:co2-rb"
        }
      ]
    },
    {
      "question_id": "CQ-T4-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One claim row carries the statement, its negated standing, the axis it concerns and the scope that axis fixes.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "existence_claim",
          "row_index": 201,
          "absent_reason": null,
          "note": "The statement about active venting on that axis is returned as a claim record."
        },
        {
          "semantic": "negated_disposition",
          "row_index": 201,
          "absent_reason": null,
          "note": "The modality field on the row records it as a negation, so it is an assertion of absence."
        },
        {
          "semantic": "claim_subject",
          "row_index": 201,
          "absent_reason": null,
          "note": "The row resolves its subject to the axis of the deep-earthquake segment."
        },
        {
          "semantic": "spatial_scope",
          "row_index": 201,
          "absent_reason": null,
          "note": "That same subject is the spatial scope the statement covers, and the row's name repeats it."
        }
      ],
      "source_locators": [
        "page:3:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 4,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 5,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 6,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 7,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 11,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 12,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 18,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 20,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 21,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 22,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 24,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 25,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 26,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 27,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 32,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 34,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 42,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 44,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 45,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 49,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 51,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 53,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 54,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 55,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 56,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 57,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 58,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 59,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 60,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 61,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 62,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 63,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 64,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 65,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 67,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 68,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 69,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 70,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 71,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 72,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 73,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 75,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 76,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 77,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 78,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 79,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 80,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 83,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 84,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 85,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 86,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 87,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 88,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 91,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 92,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 93,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 94,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 95,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 96,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 106,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 107,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 108,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 109,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 110,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 111,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 112,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 113,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 114,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 115,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 116,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 117,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 118,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 119,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 120,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 122,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 123,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 124,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 125,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 126,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 128,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 129,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 130,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 131,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 132,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 133,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 134,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 135,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 136,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 137,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 138,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 139,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 140,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 141,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 142,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 143,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 144,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 145,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 147,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 148,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 149,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 150,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 151,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 152,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 153,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 154,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 155,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 156,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 158,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 159,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 160,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 161,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 162,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 163,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 164,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 165,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 166,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 167,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 168,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 169,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 170,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 171,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 174,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 175,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 176,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 177,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 178,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 179,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 180,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 181,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 182,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 183,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 184,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 185,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 186,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 187,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 188,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 189,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 190,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 191,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 192,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 193,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 194,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 195,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 196,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 197,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 198,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 199,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 200,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 201,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 202,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 203,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 204,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 205,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 206,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 207,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 208,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 209,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 212,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 213,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 214,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 215,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 216,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 217,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 218,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 219,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 220,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 221,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 222,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 223,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 224,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 225,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 226,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 227,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 228,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 229,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 230,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 231,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 232,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 234,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 236,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 237,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 238,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 239,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 240,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 241,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 242,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 243,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 244,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 245,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 246,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 247,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 248,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 249,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 250,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 251,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 252,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 253,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 254,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 255,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 256,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 257,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 259,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 260,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 261,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 262,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 263,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 264,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 265,
          "witness_key": "obs:temp-10-20km"
        },
        {
          "row_index": 266,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 267,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 268,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 269,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 270,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 271,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 272,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 273,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 274,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 275,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 276,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 277,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 278,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 279,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 280,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 281,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 282,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 283,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 284,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 285,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 286,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 287,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 288,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 289,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 290,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 291,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 292,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 293,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 294,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 295,
          "witness_key": "obs:rb-rc2"
        }
      ]
    },
    {
      "question_id": "CQ-T4-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The hedged reading, its hypothesis standing and its modality are on one claim row; what is still needed is a second claim row recorded as a limitation. The hypothesis disposition slot on the first row is unset, but the claim kind carries that it is put as a hypothesis.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "hedged_claim",
          "row_index": 13,
          "absent_reason": null,
          "note": "The long-period reading of the deep events is returned as a claim record."
        },
        {
          "semantic": "hypothesised_disposition",
          "row_index": 13,
          "absent_reason": null,
          "note": "The claim kind on that row marks it as a hypothesis; the disposition slot itself is left unset."
        },
        {
          "semantic": "epistemic_modality",
          "row_index": 13,
          "absent_reason": null,
          "note": "The modality field records the hedge with which it is stated."
        },
        {
          "semantic": "stated_limitation",
          "row_index": 22,
          "absent_reason": null,
          "note": "A returned claim carries what the authors say is still needed, recorded as a limitation."
        }
      ],
      "source_locators": [
        "page:5:block:008"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 1,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 2,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 3,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 4,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 5,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 6,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 8,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 9,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 10,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 11,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 12,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 13,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 14,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 15,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 16,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 17,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 18,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 19,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 20,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 21,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 22,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 23,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 24,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 25,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 26,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 27,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 28,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 29,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 30,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 31,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 32,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 33,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 34,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 35,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 36,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 37,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 38,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 39,
          "witness_key": "event:romanche-2016:sub1"
        },
        {
          "row_index": 40,
          "witness_key": "event:romanche-2016:sub2"
        },
        {
          "row_index": 41,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 42,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 43,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 44,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 45,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 46,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 47,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 48,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 49,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 50,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 51,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 52,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 53,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 54,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 55,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 56,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 57,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 58,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 59,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 60,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 61,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 62,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 63,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 64,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 65,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 66,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 67,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 68,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 69,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 70,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 71,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 72,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 73,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 74,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 75,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 76,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 77,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 78,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 79,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 80,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 81,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 82,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 83,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 84,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 85,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 86,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 87,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 88,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 89,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 90,
          "witness_key": "claim:vent-field-too-far"
        }
      ]
    },
    {
      "question_id": "CQ-T5-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The mechanism and both observations are returned, each with the subject it belongs to. What is missing is the tie between them: the contract has a supporting relation, this run uses it elsewhere, the query for this question does return research relations, and none of them links either observation to the degassing claim.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "causal_mechanism",
          "row_index": 123,
          "absent_reason": null,
          "note": "The degassing mechanism is returned as a claim record marked as the preferred one."
        },
        {
          "semantic": "supporting_observation",
          "row_index": 196,
          "absent_reason": null,
          "note": "The volatile enrichment of the melts along the segment is returned as an observation row."
        },
        {
          "semantic": "geochemical_evidence",
          "row_index": 187,
          "absent_reason": null,
          "note": "The reported carbon dioxide content of the primary melts is returned as a quantity row with the melts as its subject."
        },
        {
          "semantic": "seismic_evidence",
          "row_index": 176,
          "absent_reason": null,
          "note": "The depth of the deep microseismicity beneath the segment's axis is returned as a quantity row with that axis as its subject."
        },
        {
          "semantic": "evidence_relation",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The contract carries a research relation type for one record supporting another, and the run uses it elsewhere to tie the resolution tests to a conclusion; nothing ties either observation to the degassing claim, the query for this question does return research relations, and no gap declares the omission."
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:2:block:004",
        "page:5:block:002",
        "page:5:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 1,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 2,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 3,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 4,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 5,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 6,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 8,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 9,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 10,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 11,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 12,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 13,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 14,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 15,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 16,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 17,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 18,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 19,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 20,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 21,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 22,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 23,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 24,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 25,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 26,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 27,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 28,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 29,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 30,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 31,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 32,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 33,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 34,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 35,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 36,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 37,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 38,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 39,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 40,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 41,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 42,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 43,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 44,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 45,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 46,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 47,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 48,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 49,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 50,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 51,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 52,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 53,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 54,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 55,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 56,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 57,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 58,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 59,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 60,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 61,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 62,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 63,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 64,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 65,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 66,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 67,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 68,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 69,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 70,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 71,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 72,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 73,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 74,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 75,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 76,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 77,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 78,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 79,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 80,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 81,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 82,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 83,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 84,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 85,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 86,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 87,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 88,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 89,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 90,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 91,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 92,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 93,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 94,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 95,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 96,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 97,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 98,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 99,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 100,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 101,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 102,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 103,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 104,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 105,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 106,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 107,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 108,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 109,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 110,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 111,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 112,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 113,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 114,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 115,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 116,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 117,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 118,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 119,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 120,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 121,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 122,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 123,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 124,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 125,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 126,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 127,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 128,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 129,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 130,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 131,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 132,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 133,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 134,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 135,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 136,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 137,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 138,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 139,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 140,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 141,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 142,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 143,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 144,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 145,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 146,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 147,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 148,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 149,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 150,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 151,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 152,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 153,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 154,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 155,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 156,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 157,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 158,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 159,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 160,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 161,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 162,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 163,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 164,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 165,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 166,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 167,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 168,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 169,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 170,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 171,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 172,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 173,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 174,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 175,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 176,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 177,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 178,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 179,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 180,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 181,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 182,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 183,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 184,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 185,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 186,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 187,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 188,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 189,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 190,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 191,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 192,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 193,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 194,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 195,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 196,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 197,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 198,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 199,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 200,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 201,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 202,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 203,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 204,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 205,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 206,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 207,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 208,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 209,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 210,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 211,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 212,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 213,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 214,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 215,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 216,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 217,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 218,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 219,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 220,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 221,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 222,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 223,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 224,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 225,
          "witness_key": "obs:temp-10-20km"
        }
      ]
    },
    {
      "question_id": "CQ-T5-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Both quantities, their subjects and the unit are returned. The comparison between the two segments is not on any row: both records bind the one sentence that makes the comparison by locator and digest, and that sentence is retained rather than projected.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "comparison_relation",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "Both quantity rows are bound by locator and digest to the one sentence that sets the two segments against each other; the comparison lives only in that retained sentence, and no field on either row and no returned relation carries it."
        },
        {
          "semantic": "first_quantity_subject",
          "row_index": 290,
          "absent_reason": null,
          "note": "The row for the segment with the deep earthquakes resolves its subject to the melts generated along that segment."
        },
        {
          "semantic": "second_quantity_subject",
          "row_index": 263,
          "absent_reason": null,
          "note": "The row for the adjacent southern segment resolves its subject to that segment."
        },
        {
          "semantic": "bounded_quantity",
          "row_index": 290,
          "absent_reason": null,
          "note": "The calculated content is carried as a bounded quantity on that row."
        },
        {
          "semantic": "concentration_unit",
          "row_index": 290,
          "absent_reason": null,
          "note": "The unit field on the row states the concentration unit."
        }
      ],
      "source_locators": [
        "page:5:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 4,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 5,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 6,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 7,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 11,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 12,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 18,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 20,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 21,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 22,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 24,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 25,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 26,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 27,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 32,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 34,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 42,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 44,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 45,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 49,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 51,
          "witness_key": "material:melt"
        },
        {
          "row_index": 52,
          "witness_key": "material:melt:primary"
        },
        {
          "row_index": 53,
          "witness_key": "material:melt:primitive"
        },
        {
          "row_index": 54,
          "witness_key": "melt:pre-eruptive-rc2"
        },
        {
          "row_index": 55,
          "witness_key": "melt:rc2-calculated"
        },
        {
          "row_index": 56,
          "witness_key": "sample:basaltic-rocks"
        },
        {
          "row_index": 57,
          "witness_key": "sample:morb"
        },
        {
          "row_index": 58,
          "witness_key": "sample:rock-samples"
        },
        {
          "row_index": 59,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 60,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 62,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 63,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 64,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 65,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 66,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 67,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 68,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 69,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 70,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 71,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 72,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 73,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 74,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 75,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 76,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 77,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 78,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 79,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 80,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 81,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 83,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 84,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 85,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 86,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 87,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 88,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 89,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 90,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 91,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 92,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 93,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 114,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 115,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 116,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 117,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 118,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 119,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 120,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 121,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 122,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 124,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 125,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 126,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 127,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 128,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 129,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 130,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 131,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 132,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 133,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 134,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 135,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 136,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 137,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 138,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 139,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 140,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 141,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 142,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 143,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 144,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 145,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 146,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 147,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 148,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 149,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 150,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 151,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 153,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 159,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 160,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 161,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 162,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 163,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 164,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 165,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 166,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 167,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 168,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 169,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 170,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 171,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 172,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 173,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 174,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 175,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 176,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 177,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 178,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 179,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 180,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 181,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 182,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 183,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 184,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 185,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 186,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 187,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 188,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 189,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 190,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 191,
          "witness_key": "rel:melt-from-mantle"
        },
        {
          "row_index": 192,
          "witness_key": "rel:melt-rc2-in-rc2"
        },
        {
          "row_index": 193,
          "witness_key": "rel:morb-sampled-rc2"
        },
        {
          "row_index": 194,
          "witness_key": "rel:morb-sampled-rc3"
        },
        {
          "row_index": 195,
          "witness_key": "rel:samples-from-rti-area"
        },
        {
          "row_index": 196,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 197,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 198,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 199,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 200,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 201,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 202,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 203,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 204,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 205,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 206,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 207,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 209,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 210,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 211,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 212,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 213,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 214,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 215,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 216,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 217,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 218,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 219,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 220,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 221,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 222,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 223,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 224,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 225,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 226,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 227,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 228,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 229,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 230,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 231,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 232,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 233,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 234,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 235,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 236,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 237,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 238,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 239,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 240,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 241,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 242,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 243,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 244,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 245,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 246,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 247,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 248,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 249,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 250,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 251,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 253,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 254,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 255,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 256,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 257,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 258,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 259,
          "witness_key": "obs:co2-atlantic-max"
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
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 263,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 264,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 265,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 266,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 267,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 268,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 269,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 270,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 271,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 272,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 273,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 274,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 275,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 276,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 277,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 278,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 279,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 280,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 281,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 282,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 283,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 284,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 285,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 286,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 287,
          "witness_key": "obs:temp-10-20km"
        },
        {
          "row_index": 288,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 289,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 290,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 291,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 292,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 293,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 294,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 295,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 296,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 297,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 298,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 299,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 300,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 301,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 302,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 303,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 304,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 305,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 306,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 307,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 308,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 309,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 310,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 311,
          "witness_key": "ratio:co2-rb"
        }
      ]
    },
    {
      "question_id": "CQ-T5-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The set of subsections, the deepest observed depths, the depth expected at this spreading rate and the departure from it are each carried by a returned row. Nothing in the result joins them.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "subsection_set",
          "row_index": 103,
          "absent_reason": null,
          "note": "A returned count row carries the set of subsections the studied stretch divides into, with its scope naming them as subsections of that stretch."
        },
        {
          "semantic": "maximum_depth_claim",
          "row_index": 226,
          "absent_reason": null,
          "note": "The deepest events, beneath the magmatic segment's axis, are returned as a quantity row with that axis as its subject."
        },
        {
          "semantic": "expected_depth_claim",
          "row_index": 110,
          "absent_reason": null,
          "note": "The depth expected at this spreading rate is returned as its own quantity row."
        },
        {
          "semantic": "comparison_relation",
          "row_index": 67,
          "absent_reason": null,
          "note": "A returned claim carries the departure of the observed maximum depth from the expected relationship, which is the comparison the question asks for."
        }
      ],
      "source_locators": [
        "page:1:block:005",
        "page:2:block:005",
        "page:2:block:006",
        "page:2:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 4,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 5,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 6,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 7,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 11,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 12,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 18,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 20,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 21,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 22,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 24,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 25,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 26,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 27,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 32,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 34,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 42,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 44,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 45,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 49,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 51,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 53,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 54,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 55,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 56,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 57,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 58,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 59,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 60,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 61,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 62,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 63,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 64,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 65,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 67,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 68,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 69,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 70,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 71,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 72,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 73,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 75,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 76,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 77,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 78,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 79,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 80,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 83,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 84,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 85,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 86,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 87,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 88,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 91,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 92,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 93,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 94,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 95,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 96,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 106,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 107,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 108,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 109,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 110,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 111,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 112,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 113,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 114,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 115,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 116,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 117,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 118,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 119,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 120,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 122,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 123,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 124,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 125,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 126,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 128,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 129,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 130,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 131,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 132,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 133,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 134,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 135,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 136,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 137,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 138,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 139,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 140,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 141,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 142,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 143,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 144,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 145,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 147,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 148,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 149,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 150,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 151,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 152,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 153,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 154,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 155,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 156,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 158,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 159,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 160,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 161,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 162,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 163,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 164,
          "witness_key": "event:romanche-2016:sub1"
        },
        {
          "row_index": 165,
          "witness_key": "event:romanche-2016:sub2"
        },
        {
          "row_index": 166,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 167,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 168,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 169,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 170,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 171,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 172,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 173,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 174,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 175,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 176,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 177,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 178,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 179,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 180,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 181,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 182,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 183,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 184,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 185,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 186,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 187,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 188,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 189,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 190,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 191,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 192,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 193,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 194,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 195,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 196,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 197,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 198,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 199,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 200,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 201,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 202,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 203,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 204,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 205,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 206,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 207,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 209,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 212,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 213,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 214,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 215,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 216,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 217,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 218,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 219,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 220,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 221,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 222,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 223,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 224,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 225,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 226,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 227,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 229,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 230,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 231,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 232,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 233,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 237,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 238,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 239,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 240,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 241,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 242,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 243,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 244,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 245,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 246,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 247,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 248,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 249,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 250,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 251,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 252,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 253,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 254,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 255,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 256,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 257,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 258,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 259,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 260,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 261,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 262,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 263,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 264,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 265,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 266,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 267,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 268,
          "witness_key": "obs:temp-10-20km"
        },
        {
          "row_index": 269,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 270,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 271,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 272,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 273,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 274,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 275,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 276,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 277,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 278,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 279,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 280,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 281,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 282,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 283,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 284,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 285,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 286,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 287,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 288,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 289,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 290,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 291,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 292,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 293,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 294,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 295,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 296,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 297,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 298,
          "witness_key": "obs:rb-rc2"
        }
      ]
    },
    {
      "question_id": "CQ-T5-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The categories, their number, which of them are used for interpretation and the catalogue being classified are each carried by a returned row.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "category_set",
          "row_index": 10,
          "absent_reason": null,
          "note": "The classification procedure is returned as a method row whose description names the four categories."
        },
        {
          "semantic": "category_count",
          "row_index": 64,
          "absent_reason": null,
          "note": "A returned count row carries how many categories there are."
        },
        {
          "semantic": "selection_for_interpretation",
          "row_index": 22,
          "absent_reason": null,
          "note": "A returned claim states which of the categories are kept for interpretation."
        },
        {
          "semantic": "earthquake_catalog",
          "row_index": 63,
          "absent_reason": null,
          "note": "A returned count row names the located events of the final catalogue, which is the catalogue being classified."
        }
      ],
      "source_locators": [
        "page:2:block:003",
        "page:6:block:005",
        "page:7:block:008"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:ba90-rb90"
        },
        {
          "row_index": 1,
          "witness_key": "method:depth-resolution-tests"
        },
        {
          "row_index": 2,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 3,
          "witness_key": "method:fc-correction"
        },
        {
          "row_index": 4,
          "witness_key": "method:focal-mechanism"
        },
        {
          "row_index": 5,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 6,
          "witness_key": "method:manual-arrival-check"
        },
        {
          "row_index": 7,
          "witness_key": "method:max-depth-compilation"
        },
        {
          "row_index": 8,
          "witness_key": "method:morb-compilation"
        },
        {
          "row_index": 9,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 10,
          "witness_key": "method:quality-classification"
        },
        {
          "row_index": 11,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 12,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 13,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 14,
          "witness_key": "model:co2-solubility"
        },
        {
          "row_index": 15,
          "witness_key": "model:minimum-1d"
        },
        {
          "row_index": 16,
          "witness_key": "model:thermal"
        },
        {
          "row_index": 17,
          "witness_key": "model:velocity-1d"
        },
        {
          "row_index": 18,
          "witness_key": "model:velocity-average"
        },
        {
          "row_index": 19,
          "witness_key": "model:velocity-fastest"
        },
        {
          "row_index": 20,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 21,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 22,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 23,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 24,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 25,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 26,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 27,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 28,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 29,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 30,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 31,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 32,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 33,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 34,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 35,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 36,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 37,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 38,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 39,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 40,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 41,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 42,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 43,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 44,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 45,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 46,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 47,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 48,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 49,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 50,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 51,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 52,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 53,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 54,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 55,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 56,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 57,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 58,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 59,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 60,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 61,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 62,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 63,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 64,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 65,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 66,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 67,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 68,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 70,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 71,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 72,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 73,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 74,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 75,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 76,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 77,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 78,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 79,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 80,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 81,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 82,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 83,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 84,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 85,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 86,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 87,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 88,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 89,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 90,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 91,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 92,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 93,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 94,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 95,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 96,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 97,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 98,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 99,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 100,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 101,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 102,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 103,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 104,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 105,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 106,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 107,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 108,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 109,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 110,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 111,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 112,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 113,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 114,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 115,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 116,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 117,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 118,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 119,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 120,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 121,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 122,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 123,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 124,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 125,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 126,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 127,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 128,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 129,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 130,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 131,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 132,
          "witness_key": "rel:tests-support-constrained"
        },
        {
          "row_index": 133,
          "witness_key": "rel:tests-support-deep"
        },
        {
          "row_index": 134,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 135,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 136,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 137,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 138,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 139,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 140,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 141,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 142,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 143,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 144,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 145,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 146,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 147,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 148,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 149,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 150,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 151,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 152,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 153,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 154,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 155,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 156,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 157,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 158,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 159,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 160,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 161,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 162,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 163,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 164,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 165,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 166,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 167,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 168,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 169,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 170,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 171,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 172,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 173,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 174,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 175,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 176,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 177,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 178,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 179,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 180,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 181,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 182,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 183,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 184,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 186,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 187,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 188,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 189,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 190,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 191,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 192,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 193,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 194,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 195,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 196,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 197,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 198,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 199,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 200,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 201,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 202,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 203,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 204,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 205,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 206,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 207,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 208,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 209,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 210,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 211,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 212,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 213,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 214,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 215,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 216,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 217,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 218,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 219,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 220,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 221,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 222,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 223,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 224,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 225,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 226,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 227,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 228,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 229,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 230,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 231,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 232,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 233,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 234,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 235,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 236,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 237,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 238,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 239,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 240,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 241,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 242,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 243,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 244,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 245,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 246,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 247,
          "witness_key": "obs:temp-10-20km"
        }
      ]
    },
    {
      "question_id": "CQ-T5-05",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The declined explanation with its disposition, the morphological reading and the off-axis seismicity are all returned. The reading of the two observations together against the explanation is not: the contract has relations for supporting and challenging a claim and nothing uses them here.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "candidate_explanation",
          "row_index": 197,
          "absent_reason": null,
          "note": "The cold and thick lithosphere explanation is returned as a hypothesis record."
        },
        {
          "semantic": "morphological_observation",
          "row_index": 210,
          "absent_reason": null,
          "note": "A returned claim carries the axial morphology reading of the segment, which is the morphological observation argued from."
        },
        {
          "semantic": "seismic_observation",
          "row_index": 234,
          "absent_reason": null,
          "note": "The shallow off-axis seismicity west of the axis is returned as a quantity row with that axis as its subject."
        },
        {
          "semantic": "evidence_relation",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The contract carries research relation types for one record supporting or challenging another, used elsewhere in this run, and nothing ties either observation to the declined explanation; no gap declares the omission."
        },
        {
          "semantic": "declined_disposition",
          "row_index": 197,
          "absent_reason": null,
          "note": "The disposition field on the hypothesis row records that it is not supported."
        }
      ],
      "source_locators": [
        "page:3:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 4,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 5,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 6,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 7,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 11,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 12,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 18,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 20,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 21,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 22,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 24,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 25,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 26,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 27,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 32,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 34,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 42,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 44,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 45,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 49,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 51,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 53,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 54,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 55,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 56,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 57,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 58,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 59,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 60,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 61,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 62,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 63,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 64,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 65,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 67,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 68,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 69,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 70,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 71,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 72,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 73,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 75,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 76,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 77,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 78,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 79,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 80,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 83,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 84,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 85,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 86,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 87,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 88,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 91,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 92,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 93,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 94,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 95,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 96,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 106,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 107,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 108,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 109,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 110,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 111,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 112,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 113,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 114,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 115,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 116,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 117,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 118,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 119,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 120,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 122,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 123,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 124,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 125,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 126,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 128,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 129,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 130,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 131,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 132,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 133,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 134,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 135,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 136,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 137,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 138,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 139,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 140,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 141,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 142,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 143,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 144,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 145,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 147,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 148,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 149,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 150,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 151,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 152,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 153,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 154,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 155,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 156,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 158,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 159,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 160,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 161,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 162,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 163,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 164,
          "witness_key": "event:romanche-2016:sub1"
        },
        {
          "row_index": 165,
          "witness_key": "event:romanche-2016:sub2"
        },
        {
          "row_index": 166,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 167,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 168,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 169,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 170,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 171,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 172,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 173,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 174,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 175,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 176,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 177,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 178,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 179,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 180,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 181,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 182,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 183,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 184,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 185,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 186,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 187,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 188,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 189,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 190,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 191,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 192,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 193,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 194,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 195,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 196,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 197,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 198,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 199,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 200,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 201,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 202,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 203,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 204,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 205,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 206,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 207,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 209,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 212,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 213,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 214,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 215,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 216,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 217,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 218,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 219,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 220,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 221,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 222,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 223,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 224,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 225,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 226,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 227,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 229,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 230,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 231,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 232,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 233,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 237,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 238,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 239,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 240,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 241,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 242,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 243,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 244,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 245,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 246,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 247,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 248,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 249,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 250,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 251,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 252,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 253,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 254,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 255,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 256,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 257,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 258,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 259,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 260,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 261,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 262,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 263,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 264,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 265,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 266,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 267,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 268,
          "witness_key": "obs:temp-10-20km"
        },
        {
          "row_index": 269,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 270,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 271,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 272,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 273,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 274,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 275,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 276,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 277,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 278,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 279,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 280,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 281,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 282,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 283,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 284,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 285,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 286,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 287,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 288,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 289,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 290,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 291,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 292,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 293,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 294,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 295,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 296,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 297,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 298,
          "witness_key": "obs:rb-rc2"
        }
      ]
    },
    {
      "question_id": "CQ-C-01",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "The reading reports no sulfur or chlorine data at all, so no quantity, unit or measurement status for them can be on a row. The sample records that are returned belong to the carbon dioxide estimation and, by the subject-tie rule, do not name the sample set of a measurement the source never made.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading states concentrations for carbon dioxide and for trace elements, and none for sulfur or chlorine; a carbon dioxide quantity is a quantity about a different substance and does not name this one."
        },
        {
          "semantic": "concentration_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "With no sulfur or chlorine concentration stated anywhere in the reading, there is no unit for one to carry."
        },
        {
          "semantic": "sample_set",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The sample records returned belong to the carbon dioxide estimation, so under the subject-tie rule they do not name the sample set of a sulfur and chlorine measurement, which the reading does not report."
        },
        {
          "semantic": "measurement_status",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "No sulfur or chlorine measurement is stated, so nothing in the reading says whether such values were measured or derived."
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "material:melt"
        },
        {
          "row_index": 1,
          "witness_key": "material:melt:primary"
        },
        {
          "row_index": 2,
          "witness_key": "material:melt:primitive"
        },
        {
          "row_index": 3,
          "witness_key": "melt:pre-eruptive-rc2"
        },
        {
          "row_index": 4,
          "witness_key": "melt:rc2-calculated"
        },
        {
          "row_index": 5,
          "witness_key": "sample:basaltic-rocks"
        },
        {
          "row_index": 6,
          "witness_key": "sample:morb"
        },
        {
          "row_index": 7,
          "witness_key": "sample:rock-samples"
        },
        {
          "row_index": 8,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 9,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 10,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 11,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 12,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 13,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 14,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 15,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 16,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 17,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 18,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 19,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 20,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 21,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 22,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 23,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 24,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 25,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 26,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 27,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 28,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 29,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 30,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 31,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 32,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 33,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 34,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 35,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 36,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 37,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 38,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 39,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 40,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 41,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 42,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 43,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 44,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 45,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 46,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 47,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 48,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 49,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 50,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 51,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 52,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 53,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 54,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 55,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 56,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 57,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 58,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 59,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 60,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 61,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 62,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 63,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 64,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 65,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 66,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 67,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 68,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 69,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 70,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 71,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 72,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 73,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 74,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 75,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 76,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 77,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 78,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 79,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 80,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 81,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 82,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 83,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 84,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 85,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 86,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 87,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 88,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 89,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 90,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 91,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 92,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 93,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 94,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 95,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 96,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 97,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 98,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 99,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 100,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 101,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 102,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 103,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 104,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 105,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 106,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 107,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 108,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 109,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 110,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 111,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 112,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 113,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 114,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 115,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 116,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 117,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 118,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 119,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 120,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 121,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 122,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 123,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 124,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 125,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 126,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 127,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 128,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 129,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 130,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 131,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 132,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 133,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 134,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 135,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 136,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 137,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 138,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 139,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 140,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 141,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 142,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 143,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 144,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 145,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 146,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 147,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 148,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 149,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 150,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 151,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 152,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 153,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 154,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 155,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 156,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 157,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 158,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 159,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 160,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 161,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 162,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 163,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 164,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 165,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 166,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 167,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 168,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 169,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 170,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 171,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 172,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 173,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 174,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 175,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 176,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 177,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 178,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 179,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 183,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 184,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 185,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 186,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 187,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 188,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 189,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 190,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 191,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 192,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 193,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 194,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 195,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 196,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 197,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 198,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 199,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 200,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 201,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 202,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 203,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 204,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 205,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 206,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 207,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 208,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 209,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 210,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 211,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 212,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 213,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 214,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 215,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 216,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 217,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 218,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 219,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 220,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 221,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 222,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 223,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 224,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 225,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 226,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 227,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 228,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 229,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 230,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 231,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 232,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 233,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 234,
          "witness_key": "obs:temp-10-20km"
        },
        {
          "row_index": 235,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 236,
          "witness_key": "ratio:co2-rb"
        }
      ]
    },
    {
      "question_id": "CQ-C-02",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "No repeat time for the deep events is stated anywhere in the reading. The temporal quantities that are returned belong to the recording and to the catalogue statistics, and the depth rows about the deep events belong to the depth claim, so none of them names an element of a recurrence statement.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "temporal_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading gives the length of the recording and magnitude statistics for the catalogue, but no repeat time for the deep events; a recording length is a quantity about a different thing."
        },
        {
          "semantic": "time_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "With no recurrence interval stated, no row carries a unit for one."
        },
        {
          "semantic": "event_population",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "Rows about the deep events carry their depths, which belong to the depth claim; none of them carries the population of a recurrence statement, because the reading makes none."
        },
        {
          "semantic": "measurement_status",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "There is no recurrence figure in the reading, so nothing states how one would have been arrived at."
        }
      ],
      "source_locators": [
        "page:2:block:004",
        "page:8:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 1,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 2,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 3,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 4,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 5,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 6,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 7,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 8,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 9,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 10,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 11,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 12,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 13,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 14,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 15,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 16,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 17,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 18,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 19,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 20,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 21,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 22,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 23,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 24,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 25,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 26,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 27,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 28,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 29,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 30,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 31,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 32,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 33,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 34,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 35,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 36,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 37,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 38,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 39,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 40,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 41,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 42,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 43,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 44,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 45,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 46,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 47,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 48,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 49,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 50,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 51,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 52,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 53,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 54,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 55,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 56,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 57,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 58,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 59,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 60,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 61,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 62,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 63,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 64,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 65,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 66,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 67,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 68,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 69,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 70,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 71,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 72,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 73,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 74,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 75,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 76,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 77,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 78,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 79,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 80,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 81,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 82,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 83,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 84,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 85,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 86,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 87,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 88,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 89,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 90,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 91,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 92,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 93,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 94,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 95,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 96,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 97,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 98,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 99,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 100,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 101,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 102,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 103,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 104,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 105,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 106,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 107,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 108,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 109,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 110,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 111,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 112,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 113,
          "witness_key": "event:romanche-2016:sub1"
        },
        {
          "row_index": 114,
          "witness_key": "event:romanche-2016:sub2"
        },
        {
          "row_index": 115,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 116,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 117,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 118,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 119,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 120,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 121,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 122,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 123,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 124,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 125,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 126,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 127,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 128,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 129,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 130,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 131,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 132,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 133,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 134,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 135,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 136,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 137,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 138,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 139,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 140,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 141,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 142,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 143,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 144,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 145,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 146,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 147,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 148,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 149,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 150,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 151,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 152,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 153,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 154,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 155,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 156,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 157,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 158,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 159,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 160,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 161,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 162,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 163,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 164,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 165,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 166,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 167,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 168,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 169,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 170,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 171,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 172,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 173,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 174,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 175,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 176,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 177,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 178,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 179,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 180,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 181,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 182,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 183,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 184,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 185,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 186,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 187,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 188,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 189,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 190,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 191,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 192,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 193,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 194,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 195,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 196,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 197,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 198,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 199,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 200,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 201,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 202,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 203,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 204,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 205,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 206,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 207,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 208,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 209,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 210,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 211,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 212,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 213,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 214,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 215,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 216,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 217,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 218,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 219,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 220,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 221,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 222,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 223,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 224,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 225,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 226,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 227,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 228,
          "witness_key": "obs:temp-10-20km"
        }
      ]
    },
    {
      "question_id": "CQ-C-03",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "The per-site depths and rates live in the comparison figure and its supplementary table, which the question file's scope excludes, and the reading does not state the compiled site list either. The depth and rate rows that are returned describe this study's own ridge and subsections, a different subject.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "site_set",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading names a handful of sites whose figures were updated, but the list of sites compiled for the comparison lives in the figure and its supplementary table, which the question file's scope excludes; no returned row carries the set."
        },
        {
          "semantic": "maximum_depth_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The per-site maximum depths are not stated in the reading. The depth rows returned belong to this study's own subsections and are quantities about a different subject."
        },
        {
          "semantic": "spreading_rate_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The per-site spreading rates are likewise absent from the reading; the one rate row returned is the rate of the ridge under study, not of a compiled site."
        }
      ],
      "source_locators": [
        "page:5:block:010",
        "page:8:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "work:ref:01"
        },
        {
          "row_index": 1,
          "witness_key": "work:ref:02"
        },
        {
          "row_index": 2,
          "witness_key": "work:ref:03"
        },
        {
          "row_index": 3,
          "witness_key": "work:ref:04"
        },
        {
          "row_index": 4,
          "witness_key": "work:ref:05"
        },
        {
          "row_index": 5,
          "witness_key": "work:ref:06"
        },
        {
          "row_index": 6,
          "witness_key": "work:ref:07"
        },
        {
          "row_index": 7,
          "witness_key": "work:ref:08"
        },
        {
          "row_index": 8,
          "witness_key": "work:ref:09"
        },
        {
          "row_index": 9,
          "witness_key": "work:ref:10"
        },
        {
          "row_index": 10,
          "witness_key": "work:ref:11"
        },
        {
          "row_index": 11,
          "witness_key": "work:ref:12"
        },
        {
          "row_index": 12,
          "witness_key": "work:ref:13"
        },
        {
          "row_index": 13,
          "witness_key": "work:ref:14"
        },
        {
          "row_index": 14,
          "witness_key": "work:ref:15"
        },
        {
          "row_index": 15,
          "witness_key": "work:ref:16"
        },
        {
          "row_index": 16,
          "witness_key": "work:ref:17"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref:18"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref:19"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref:20"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref:21"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref:22"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref:23"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref:24"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref:25"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref:26"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref:27"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref:28"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref:29"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref:30"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref:31"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref:32"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref:33"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref:34"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref:35"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref:36"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref:37"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref:38"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref:39"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref:40"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref:41"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref:42"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref:43"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref:44"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref:45"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref:46"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref:47"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref:48"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref:49"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref:50"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref:51"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref:52"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref:53"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref:54"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref:55"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref:56"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref:57"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref:58"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref:59"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref:60"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref:61"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref:62"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref:63"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref:64"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref:65"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref:66"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref:67"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref:68"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref:69"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref:70"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref:71"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref:72"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref:73"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref:74"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref:75"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref:76"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref:77"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref:78"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref:79"
        },
        {
          "row_index": 79,
          "witness_key": "work:yu-2025"
        },
        {
          "row_index": 80,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 81,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 82,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 83,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 84,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 85,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 86,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 87,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 88,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 89,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 90,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 91,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 92,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 93,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 94,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 95,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 96,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 97,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 98,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 99,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 100,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 101,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 102,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 103,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 104,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 105,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 106,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 107,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 108,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 109,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 110,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 111,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 112,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 113,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 114,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 115,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 116,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 117,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 118,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 119,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 120,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 121,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 122,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 123,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 124,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 125,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 126,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 127,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 128,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 129,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 130,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 131,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 132,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 133,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 134,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 135,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 136,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 137,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 138,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 139,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 140,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 141,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 142,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 143,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 144,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 145,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 146,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 147,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 148,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 149,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 150,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 151,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 152,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 153,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 154,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 155,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 156,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 157,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 158,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 159,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 160,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 161,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 162,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 163,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 164,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 165,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 166,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 167,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 168,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 169,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 170,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 171,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 172,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 173,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 174,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 175,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 176,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 177,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 178,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 179,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 184,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 186,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 187,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 188,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 189,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 190,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 191,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 192,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 193,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 194,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 195,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 196,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 197,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 198,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 199,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 200,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 201,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 202,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 203,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 204,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 206,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 207,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 208,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 209,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 210,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 211,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 212,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 213,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 214,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 215,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 216,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 217,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 218,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 219,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 220,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 221,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 222,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 223,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 224,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 226,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 227,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 228,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 229,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 230,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 231,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 232,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 233,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 234,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 235,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 236,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 237,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 238,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 239,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 240,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 241,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 242,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 243,
          "witness_key": "rel:yu-2025-cites-01"
        },
        {
          "row_index": 244,
          "witness_key": "rel:yu-2025-cites-02"
        },
        {
          "row_index": 245,
          "witness_key": "rel:yu-2025-cites-03"
        },
        {
          "row_index": 246,
          "witness_key": "rel:yu-2025-cites-04"
        },
        {
          "row_index": 247,
          "witness_key": "rel:yu-2025-cites-05"
        },
        {
          "row_index": 248,
          "witness_key": "rel:yu-2025-cites-06"
        },
        {
          "row_index": 249,
          "witness_key": "rel:yu-2025-cites-07"
        },
        {
          "row_index": 250,
          "witness_key": "rel:yu-2025-cites-08"
        },
        {
          "row_index": 251,
          "witness_key": "rel:yu-2025-cites-09"
        },
        {
          "row_index": 252,
          "witness_key": "rel:yu-2025-cites-10"
        },
        {
          "row_index": 253,
          "witness_key": "rel:yu-2025-cites-11"
        },
        {
          "row_index": 254,
          "witness_key": "rel:yu-2025-cites-12"
        },
        {
          "row_index": 255,
          "witness_key": "rel:yu-2025-cites-13"
        },
        {
          "row_index": 256,
          "witness_key": "rel:yu-2025-cites-14"
        },
        {
          "row_index": 257,
          "witness_key": "rel:yu-2025-cites-15"
        },
        {
          "row_index": 258,
          "witness_key": "rel:yu-2025-cites-16"
        },
        {
          "row_index": 259,
          "witness_key": "rel:yu-2025-cites-17"
        },
        {
          "row_index": 260,
          "witness_key": "rel:yu-2025-cites-18"
        },
        {
          "row_index": 261,
          "witness_key": "rel:yu-2025-cites-19"
        },
        {
          "row_index": 262,
          "witness_key": "rel:yu-2025-cites-20"
        },
        {
          "row_index": 263,
          "witness_key": "rel:yu-2025-cites-21"
        },
        {
          "row_index": 264,
          "witness_key": "rel:yu-2025-cites-22"
        },
        {
          "row_index": 265,
          "witness_key": "rel:yu-2025-cites-23"
        },
        {
          "row_index": 266,
          "witness_key": "rel:yu-2025-cites-24"
        },
        {
          "row_index": 267,
          "witness_key": "rel:yu-2025-cites-25"
        },
        {
          "row_index": 268,
          "witness_key": "rel:yu-2025-cites-26"
        },
        {
          "row_index": 269,
          "witness_key": "rel:yu-2025-cites-27"
        },
        {
          "row_index": 270,
          "witness_key": "rel:yu-2025-cites-28"
        },
        {
          "row_index": 271,
          "witness_key": "rel:yu-2025-cites-29"
        },
        {
          "row_index": 272,
          "witness_key": "rel:yu-2025-cites-30"
        },
        {
          "row_index": 273,
          "witness_key": "rel:yu-2025-cites-31"
        },
        {
          "row_index": 274,
          "witness_key": "rel:yu-2025-cites-32"
        },
        {
          "row_index": 275,
          "witness_key": "rel:yu-2025-cites-33"
        },
        {
          "row_index": 276,
          "witness_key": "rel:yu-2025-cites-34"
        },
        {
          "row_index": 277,
          "witness_key": "rel:yu-2025-cites-35"
        },
        {
          "row_index": 278,
          "witness_key": "rel:yu-2025-cites-36"
        },
        {
          "row_index": 279,
          "witness_key": "rel:yu-2025-cites-37"
        },
        {
          "row_index": 280,
          "witness_key": "rel:yu-2025-cites-38"
        },
        {
          "row_index": 281,
          "witness_key": "rel:yu-2025-cites-39"
        },
        {
          "row_index": 282,
          "witness_key": "rel:yu-2025-cites-40"
        },
        {
          "row_index": 283,
          "witness_key": "rel:yu-2025-cites-41"
        },
        {
          "row_index": 284,
          "witness_key": "rel:yu-2025-cites-42"
        },
        {
          "row_index": 285,
          "witness_key": "rel:yu-2025-cites-43"
        },
        {
          "row_index": 286,
          "witness_key": "rel:yu-2025-cites-44"
        },
        {
          "row_index": 287,
          "witness_key": "rel:yu-2025-cites-45"
        },
        {
          "row_index": 288,
          "witness_key": "rel:yu-2025-cites-46"
        },
        {
          "row_index": 289,
          "witness_key": "rel:yu-2025-cites-47"
        },
        {
          "row_index": 290,
          "witness_key": "rel:yu-2025-cites-48"
        },
        {
          "row_index": 291,
          "witness_key": "rel:yu-2025-cites-49"
        },
        {
          "row_index": 292,
          "witness_key": "rel:yu-2025-cites-50"
        },
        {
          "row_index": 293,
          "witness_key": "rel:yu-2025-cites-51"
        },
        {
          "row_index": 294,
          "witness_key": "rel:yu-2025-cites-52"
        },
        {
          "row_index": 295,
          "witness_key": "rel:yu-2025-cites-53"
        },
        {
          "row_index": 296,
          "witness_key": "rel:yu-2025-cites-54"
        },
        {
          "row_index": 297,
          "witness_key": "rel:yu-2025-cites-55"
        },
        {
          "row_index": 298,
          "witness_key": "rel:yu-2025-cites-56"
        },
        {
          "row_index": 299,
          "witness_key": "rel:yu-2025-cites-57"
        },
        {
          "row_index": 300,
          "witness_key": "rel:yu-2025-cites-58"
        },
        {
          "row_index": 301,
          "witness_key": "rel:yu-2025-cites-59"
        },
        {
          "row_index": 302,
          "witness_key": "rel:yu-2025-cites-60"
        },
        {
          "row_index": 303,
          "witness_key": "rel:yu-2025-cites-61"
        },
        {
          "row_index": 304,
          "witness_key": "rel:yu-2025-cites-62"
        },
        {
          "row_index": 305,
          "witness_key": "rel:yu-2025-cites-63"
        },
        {
          "row_index": 306,
          "witness_key": "rel:yu-2025-cites-64"
        },
        {
          "row_index": 307,
          "witness_key": "rel:yu-2025-cites-65"
        },
        {
          "row_index": 308,
          "witness_key": "rel:yu-2025-cites-66"
        },
        {
          "row_index": 309,
          "witness_key": "rel:yu-2025-cites-67"
        },
        {
          "row_index": 310,
          "witness_key": "rel:yu-2025-cites-68"
        },
        {
          "row_index": 311,
          "witness_key": "rel:yu-2025-cites-69"
        },
        {
          "row_index": 312,
          "witness_key": "rel:yu-2025-cites-70"
        },
        {
          "row_index": 313,
          "witness_key": "rel:yu-2025-cites-71"
        },
        {
          "row_index": 314,
          "witness_key": "rel:yu-2025-cites-72"
        },
        {
          "row_index": 315,
          "witness_key": "rel:yu-2025-cites-73"
        },
        {
          "row_index": 316,
          "witness_key": "rel:yu-2025-cites-74"
        },
        {
          "row_index": 317,
          "witness_key": "rel:yu-2025-cites-75"
        },
        {
          "row_index": 318,
          "witness_key": "rel:yu-2025-cites-76"
        },
        {
          "row_index": 319,
          "witness_key": "rel:yu-2025-cites-77"
        },
        {
          "row_index": 320,
          "witness_key": "rel:yu-2025-cites-78"
        },
        {
          "row_index": 321,
          "witness_key": "rel:yu-2025-cites-79"
        },
        {
          "row_index": 322,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 323,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 324,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 325,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 326,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 327,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 328,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 329,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 330,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 331,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 332,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 333,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 334,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 335,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 336,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 337,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 338,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 339,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 340,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 341,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 342,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 343,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 344,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 345,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 346,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 347,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 348,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 349,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 350,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 351,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 352,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 353,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 354,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 355,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 356,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 357,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 358,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 359,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 360,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 361,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 362,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 363,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 364,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 365,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 366,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 367,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 368,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 369,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 370,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 371,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 372,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 373,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 374,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 375,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 376,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 377,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 378,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 379,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 380,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 381,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 382,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 383,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 384,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 385,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 386,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 387,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 388,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 389,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 390,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 391,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 392,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 393,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 394,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 395,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 396,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 397,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 398,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 399,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 400,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 401,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 402,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 403,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 404,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 405,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 406,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 407,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 408,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 409,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 410,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 411,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 412,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 413,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 414,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 415,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 416,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 417,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 418,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 419,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 420,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 421,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 422,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 423,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 424,
          "witness_key": "obs:temp-10-20km"
        },
        {
          "row_index": 425,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 426,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 427,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 428,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 429,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 430,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 431,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 432,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 433,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 434,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 435,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 436,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 437,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 438,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 439,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 440,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 441,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 442,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 443,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 444,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 445,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 446,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 447,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 448,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 449,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 450,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 451,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 452,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 453,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 454,
          "witness_key": "obs:rb-rc2"
        }
      ]
    },
    {
      "question_id": "CQ-C-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Asked in different words, this reaches the same rows as its source question: the count with the network as its subject, and the methods-side count for the deployment.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "instrument_count",
          "row_index": 84,
          "absent_reason": null,
          "note": "The row carries the number of seismometers placed on the seafloor for this experiment, with the network as its subject."
        },
        {
          "semantic": "observing_system",
          "row_index": 84,
          "absent_reason": null,
          "note": "The same row resolves its subject to the instrument record for the network."
        },
        {
          "semantic": "deployment_event",
          "row_index": 85,
          "absent_reason": null,
          "note": "The methods-side count row states that the network was put out for the passive experiment."
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
          "witness_key": "instrument:obs"
        },
        {
          "row_index": 2,
          "witness_key": "software:global-mapper"
        },
        {
          "row_index": 3,
          "witness_key": "software:gmt"
        },
        {
          "row_index": 4,
          "witness_key": "software:hash"
        },
        {
          "row_index": 5,
          "witness_key": "software:hypodd"
        },
        {
          "row_index": 6,
          "witness_key": "software:nonlinloc"
        },
        {
          "row_index": 7,
          "witness_key": "software:seisan"
        },
        {
          "row_index": 8,
          "witness_key": "software:velest"
        },
        {
          "row_index": 9,
          "witness_key": "software:zmap"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 17,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 18,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 19,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 20,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 21,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 22,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 23,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 24,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 25,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 26,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 27,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 28,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 29,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 30,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 31,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 32,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 33,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 34,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 35,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 36,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 37,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 38,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 39,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 40,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 41,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 42,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 43,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 44,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 45,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 46,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 47,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 48,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 49,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 50,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 51,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 52,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 53,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 54,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 55,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 56,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 57,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 58,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 59,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 60,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 61,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 62,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 63,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 64,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 65,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 66,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 67,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 68,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 69,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 70,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 71,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 72,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 73,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 74,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 75,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 76,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 77,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 78,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 79,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 80,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 81,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 82,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 83,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 84,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 86,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 87,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 88,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 91,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 92,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 93,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 94,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 95,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 96,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 97,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 98,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 99,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 100,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 101,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 102,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 103,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 105,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 106,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 108,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 109,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 110,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 112,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 113,
          "witness_key": "obs:co2-atlantic-max"
        },
        {
          "row_index": 114,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 115,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 116,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 120,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 121,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 122,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 123,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 124,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 125,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 126,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 127,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 128,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 129,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 130,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 131,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 132,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 133,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 134,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 135,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 136,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 137,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 138,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 139,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 140,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 141,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 142,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 143,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 144,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 145,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 146,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 147,
          "witness_key": "obs:temp-10-20km"
        }
      ]
    },
    {
      "question_id": "CQ-C-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Reworded, this reaches the same single quantity row as its source question, which carries the range, the unit, the melts and the calculated status.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 289,
          "absent_reason": null,
          "note": "The carbon dioxide content of the primary melts of the studied segment is returned as a bounded quantity."
        },
        {
          "semantic": "concentration_unit",
          "row_index": 289,
          "absent_reason": null,
          "note": "The unit field on that row states the concentration unit."
        },
        {
          "semantic": "quantity_subject",
          "row_index": 289,
          "absent_reason": null,
          "note": "The row's subject resolves to the primary melts and its name ties the figure to the studied segment."
        },
        {
          "semantic": "calculated_or_measured_status",
          "row_index": 289,
          "absent_reason": null,
          "note": "The determination and modality fields say the figure was calculated rather than measured."
        }
      ],
      "source_locators": [
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:atlantic"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:axial-valley-faults"
        },
        {
          "row_index": 4,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 5,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 6,
          "witness_key": "feature:detachment-rti"
        },
        {
          "row_index": 7,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 11,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 12,
          "witness_key": "feature:indian-ocean"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 18,
          "witness_key": "feature:magma-reservoir"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mantle"
        },
        {
          "row_index": 20,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 21,
          "witness_key": "feature:mar-axis"
        },
        {
          "row_index": 22,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 23,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 24,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 25,
          "witness_key": "feature:melt-lens"
        },
        {
          "row_index": 26,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 27,
          "witness_key": "feature:neovolcanic-ridge"
        },
        {
          "row_index": 28,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 29,
          "witness_key": "feature:ntd1-east-flank"
        },
        {
          "row_index": 30,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 31,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 32,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 33,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 34,
          "witness_key": "feature:occ-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:oceanic-crust"
        },
        {
          "row_index": 36,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 37,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 38,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rc2-axis"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 41,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 42,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 43,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 44,
          "witness_key": "feature:seafloor"
        },
        {
          "row_index": 45,
          "witness_key": "feature:shear-zones-tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:study-area"
        },
        {
          "row_index": 47,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 48,
          "witness_key": "feature:transform-valley"
        },
        {
          "row_index": 49,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 50,
          "witness_key": "feature:western-flank"
        },
        {
          "row_index": 51,
          "witness_key": "material:melt"
        },
        {
          "row_index": 52,
          "witness_key": "material:melt:primary"
        },
        {
          "row_index": 53,
          "witness_key": "material:melt:primitive"
        },
        {
          "row_index": 54,
          "witness_key": "melt:pre-eruptive-rc2"
        },
        {
          "row_index": 55,
          "witness_key": "melt:rc2-calculated"
        },
        {
          "row_index": 56,
          "witness_key": "sample:basaltic-rocks"
        },
        {
          "row_index": 57,
          "witness_key": "sample:morb"
        },
        {
          "row_index": 58,
          "witness_key": "sample:rock-samples"
        },
        {
          "row_index": 59,
          "witness_key": "claim:bg:deeper-eq-observed"
        },
        {
          "row_index": 60,
          "witness_key": "claim:bg:max-depth-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:categories-ab-good"
        },
        {
          "row_index": 62,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 63,
          "witness_key": "claim:contexts-different"
        },
        {
          "row_index": 64,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 65,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 66,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 67,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 68,
          "witness_key": "claim:fig3-transect-halfwidth"
        },
        {
          "row_index": 69,
          "witness_key": "claim:fixed-depth-worse-rms"
        },
        {
          "row_index": 70,
          "witness_key": "claim:focal-mechanisms-not-robust"
        },
        {
          "row_index": 71,
          "witness_key": "claim:h-magmatic-tectonic"
        },
        {
          "row_index": 72,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 73,
          "witness_key": "claim:magmatic-tectonic-eruptions"
        },
        {
          "row_index": 74,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 75,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 76,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 77,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 78,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 79,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 80,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 81,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 83,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 84,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 85,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 86,
          "witness_key": "claim:perturbed-models-deep-events"
        },
        {
          "row_index": 87,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 88,
          "witness_key": "claim:rc1-tectonic-origin"
        },
        {
          "row_index": 89,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 90,
          "witness_key": "claim:shear-zone-with-detachments"
        },
        {
          "row_index": 91,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 92,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 93,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:criterion-arrivals"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:forced-depth-tests"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:hypodd-iterations"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:located-earthquakes-methods"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:min-obs-relocated"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:polarity-criterion"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:sub-dataset-arrivals"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 114,
          "witness_key": "obs:axial-event-depth-range"
        },
        {
          "row_index": 115,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 116,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 117,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 118,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 119,
          "witness_key": "obs:fig3-deep-shading"
        },
        {
          "row_index": 120,
          "witness_key": "obs:fig3-shallow-shading"
        },
        {
          "row_index": 121,
          "witness_key": "obs:onset-volatile-melting-depth"
        },
        {
          "row_index": 122,
          "witness_key": "obs:saturation-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 124,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 125,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 126,
          "witness_key": "obs:brittle-thickness-expected"
        },
        {
          "row_index": 127,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 128,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 129,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 130,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 131,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 132,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 133,
          "witness_key": "obs:fm-azimuthal-gap"
        },
        {
          "row_index": 134,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 135,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 136,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 137,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 138,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 139,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 140,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 141,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 142,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 143,
          "witness_key": "obs:isotherm-750"
        },
        {
          "row_index": 144,
          "witness_key": "obs:lithospheric-age-contour"
        },
        {
          "row_index": 145,
          "witness_key": "obs:low-frequency-cutoff"
        },
        {
          "row_index": 146,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 147,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 148,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 149,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 150,
          "witness_key": "obs:model1-pwave-velocity"
        },
        {
          "row_index": 151,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 153,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocated-azimuthal-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocated-rms"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocated-uncertainty"
        },
        {
          "row_index": 159,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 160,
          "witness_key": "obs:saturation-pressure"
        },
        {
          "row_index": 161,
          "witness_key": "obs:saturation-temperature"
        },
        {
          "row_index": 162,
          "witness_key": "obs:solubility-model-temperature"
        },
        {
          "row_index": 163,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 164,
          "witness_key": "obs:sub-dataset-gap"
        },
        {
          "row_index": 165,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 166,
          "witness_key": "obs:temp-below-20km"
        },
        {
          "row_index": 167,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 168,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 169,
          "witness_key": "obs:vp-vs-test-range"
        },
        {
          "row_index": 170,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 171,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 172,
          "witness_key": "rel:axial-valley-cut-by-faults"
        },
        {
          "row_index": 173,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 174,
          "witness_key": "rel:mar-segment-bounded-chain"
        },
        {
          "row_index": 175,
          "witness_key": "rel:mar-segment-bounded-romanche"
        },
        {
          "row_index": 176,
          "witness_key": "rel:ntd1-part-of-study-area"
        },
        {
          "row_index": 177,
          "witness_key": "rel:ntd2-part-of-study-area"
        },
        {
          "row_index": 178,
          "witness_key": "rel:occ-adjacent-axis"
        },
        {
          "row_index": 179,
          "witness_key": "rel:occ-cut-by-faults"
        },
        {
          "row_index": 180,
          "witness_key": "rel:occ-on-outside-corner"
        },
        {
          "row_index": 181,
          "witness_key": "rel:rainbow-at-ntd"
        },
        {
          "row_index": 182,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 183,
          "witness_key": "rel:rc1-part-of-study-area"
        },
        {
          "row_index": 184,
          "witness_key": "rel:rc2-bounded-by-faults"
        },
        {
          "row_index": 185,
          "witness_key": "rel:rc2-part-of-study-area"
        },
        {
          "row_index": 186,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 187,
          "witness_key": "rel:study-area-in-mar-segment"
        },
        {
          "row_index": 188,
          "witness_key": "rel:study-area-offset-ntd1"
        },
        {
          "row_index": 189,
          "witness_key": "rel:study-area-offset-ntd2"
        },
        {
          "row_index": 190,
          "witness_key": "rel:vent-field-on-ntd1-flank"
        },
        {
          "row_index": 191,
          "witness_key": "rel:melt-from-mantle"
        },
        {
          "row_index": 192,
          "witness_key": "rel:melt-rc2-in-rc2"
        },
        {
          "row_index": 193,
          "witness_key": "rel:morb-sampled-rc2"
        },
        {
          "row_index": 194,
          "witness_key": "rel:morb-sampled-rc3"
        },
        {
          "row_index": 195,
          "witness_key": "rel:samples-from-rti-area"
        },
        {
          "row_index": 196,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 197,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 198,
          "witness_key": "claim:bg:melt-lens-bdb"
        },
        {
          "row_index": 199,
          "witness_key": "claim:bg:tf-deep-eq"
        },
        {
          "row_index": 200,
          "witness_key": "claim:co2-degassing"
        },
        {
          "row_index": 201,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 202,
          "witness_key": "claim:deep-events-well-constrained"
        },
        {
          "row_index": 203,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 204,
          "witness_key": "claim:enriched-source-interpretation"
        },
        {
          "row_index": 205,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 206,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 207,
          "witness_key": "claim:fig6-interpretation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:h-cold-lithosphere"
        },
        {
          "row_index": 209,
          "witness_key": "claim:h-hydrothermal"
        },
        {
          "row_index": 210,
          "witness_key": "claim:h-shear-zone"
        },
        {
          "row_index": 211,
          "witness_key": "claim:keller-volatile-flushing"
        },
        {
          "row_index": 212,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 213,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 214,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 215,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 216,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 217,
          "witness_key": "claim:no-eq-below-20"
        },
        {
          "row_index": 218,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 219,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 220,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 221,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 222,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 223,
          "witness_key": "claim:rc2-mantle-hot"
        },
        {
          "row_index": 224,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 225,
          "witness_key": "claim:rc3-magmatic"
        },
        {
          "row_index": 226,
          "witness_key": "claim:small-pressure-induces"
        },
        {
          "row_index": 227,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 228,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 229,
          "witness_key": "claim:bg:melt-focusing"
        },
        {
          "row_index": 230,
          "witness_key": "claim:bg:migration-not-understood"
        },
        {
          "row_index": 231,
          "witness_key": "claim:bg:migration-unknown"
        },
        {
          "row_index": 232,
          "witness_key": "claim:continued-degassing"
        },
        {
          "row_index": 233,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 234,
          "witness_key": "claim:implication:lab-melt"
        },
        {
          "row_index": 235,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 236,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 237,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 238,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 239,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 240,
          "witness_key": "obs:abstract:deep-depth"
        },
        {
          "row_index": 241,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 242,
          "witness_key": "obs:bdb-depth-ntd2"
        },
        {
          "row_index": 243,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 244,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 245,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 246,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 247,
          "witness_key": "obs:depth-under-ntd2"
        },
        {
          "row_index": 248,
          "witness_key": "obs:depth-under-occ"
        },
        {
          "row_index": 249,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 250,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 251,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 253,
          "witness_key": "obs:offaxis-shallow-depth"
        },
        {
          "row_index": 254,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 255,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 256,
          "witness_key": "obs:western-cluster-depth"
        },
        {
          "row_index": 257,
          "witness_key": "obs:bdb-isotherm-temp"
        },
        {
          "row_index": 258,
          "witness_key": "obs:co2-atlantic-average"
        },
        {
          "row_index": 259,
          "witness_key": "obs:co2-atlantic-max"
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
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 263,
          "witness_key": "obs:co2-calculated-rc3"
        },
        {
          "row_index": 264,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 265,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 266,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 267,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 268,
          "witness_key": "obs:co2-swir-highest"
        },
        {
          "row_index": 269,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 270,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 271,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 272,
          "witness_key": "obs:crust-thickness-fig6"
        },
        {
          "row_index": 273,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 274,
          "witness_key": "obs:hot-mantle-temp"
        },
        {
          "row_index": 275,
          "witness_key": "obs:isotherm-600-800"
        },
        {
          "row_index": 276,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 277,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 278,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 279,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 280,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 281,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 282,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 283,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 284,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 285,
          "witness_key": "obs:study-area-length"
        },
        {
          "row_index": 286,
          "witness_key": "obs:subsolidus-temp"
        },
        {
          "row_index": 287,
          "witness_key": "obs:temp-10-20km"
        },
        {
          "row_index": 288,
          "witness_key": "obs:abstract:co2-primary"
        },
        {
          "row_index": 289,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 290,
          "witness_key": "obs:co2-calculated-rc2"
        },
        {
          "row_index": 291,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 292,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 293,
          "witness_key": "claim:model5-best-fitting"
        },
        {
          "row_index": 294,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 295,
          "witness_key": "claim:bg:volatile-role"
        },
        {
          "row_index": 296,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 297,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 298,
          "witness_key": "claim:measurements-near-solubility"
        },
        {
          "row_index": 299,
          "witness_key": "claim:obs-no-data"
        },
        {
          "row_index": 300,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 301,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 302,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 303,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 304,
          "witness_key": "cnt:obs-deployed-methods"
        },
        {
          "row_index": 305,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 306,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 307,
          "witness_key": "obs:ba-rc2"
        },
        {
          "row_index": 308,
          "witness_key": "obs:co2-loss-fraction"
        },
        {
          "row_index": 309,
          "witness_key": "obs:rb-rc2"
        },
        {
          "row_index": 310,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 311,
          "witness_key": "ratio:co2-rb"
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
  "absent_reason": "NOT_MODELLED | WITHHELD_STATEMENT | UNREACHED_RECORD | NOT_IN_SOURCE | LOCATOR_NOT_RESOLVABLE | NOT_CAPTURED",
  "note": "why, in your own words"
}
```

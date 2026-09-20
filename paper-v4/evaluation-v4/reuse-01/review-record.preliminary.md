# Malleus paper v4 source-grounded review record, protocol v3.2, reuse-01

Assembled by `paper-v4/evaluation-v4/reuse-01/assemble_record.py` from the preliminary
reviewer's `review-witnesses.json` and its thirty filled review blocks. The rows are
rebuilt from the query result, not copied from the blocks. `PRELIMINARY_COMPLETE` is
not paper evidence; Luis ratifies.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v3.2",
  "status": "PRELIMINARY_COMPLETE",
  "inputs": {
    "review_protocol_sha256": "sha256:5dfd59f4aa479dd72738e2eb55653ee3e84e60886de4cccbcc0a8e66d06e55cd",
    "review_input_manifest_sha256": "sha256:64e23c8ed8a85cb7517a40b8771f09e67ba17b555dbfe1fb0ad9d693726d7c8f"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-reuse-01",
    "completed_at": "2026-09-12T07:01:49Z"
  },
  "witnesses": [
    {
      "witness_key": "cruise:smarties",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:043",
        "page:10:block:046",
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the deployment, say what it was mounted for and give the span over which it recorded. Fields judged: description, duration, name."
    },
    {
      "witness_key": "instr:obs",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001",
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the instruments and say whose records the study works from. Fields judged: description, name."
    },
    {
      "witness_key": "cnt:catalog-links",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "cnt:final-located",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "cnt:identified-earthquakes",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "cnt:location-categories",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "cnt:magnitude-groups",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "cnt:new-focal-mechanisms",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "cnt:ntds",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "cnt:relocated-events",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "cnt:relocation-iterations",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "cnt:subsections",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name, quantity_kind, quantity_kind_class, unit, value_lower, value_upper."
    },
    {
      "witness_key": "cnt:total-focal-mechanisms",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "cnt:velest-iterations",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "cnt:velest-subdataset",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "cnt:velocity-models",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "cnt:well-relocated",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the tally and what it counts. Fields judged: assertion_modality, count, count_scope, name."
    },
    {
      "witness_key": "gchem:abstract-co2-primary",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the analyte, the melt stage, the bounds and the unit the row records. Fields judged: analyte, assertion_modality, determination, melt_stage, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:average-depth-uncertainty",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:axial-event-depth-stability",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:b-value",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:brittle-thickness",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:co2-gas-loss",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:co2-saturation-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:co2-saturation-pressure",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:co2-saturation-temperature",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, determination, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:criterion-arrivals",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification."
    },
    {
      "witness_key": "obs:criterion-azimuthal-gap",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:criterion-swave-distance",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:crust-age-west-flank",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:crust-thickness-west-flank",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, uncertainty, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:degassing-eq-depth-range",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:depth-uncertainty-bound",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:7:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block opens part-way through the sentence, so the bound it carries is not labelled there as a depth uncertainty and is not tied there to the located events; the number and the unit are in the block and the label is not. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:dry-melting-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_upper."
    },
    {
      "witness_key": "obs:error-ellipsoid-confidence",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:expected-max-depth-slow",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, depth_reference, determination, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:expected-max-depth-ultraslow",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, depth_reference, determination, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:fig3-shading-threshold",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:fig4-isotherm",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:focal-selection-criteria",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification."
    },
    {
      "witness_key": "obs:fraction-two-criteria",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:full-spreading-rate",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:group-b-values",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:high-frequency-threshold",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification."
    },
    {
      "witness_key": "obs:horizontal-uncertainty-bound",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:instrument-spacing",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:lithosphere-age-45ma",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:lithospheric-age-contours",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:magnitude-completeness",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:mean-horizontal-error",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:mean-horizontal-uncertainty",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:mean-vertical-error",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:melting-initiation-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:model1-vp",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification."
    },
    {
      "witness_key": "obs:offaxis-cluster-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:offaxis-swarm-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:predicted-max-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:profile-halfwidth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:profile-tick-interval",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:quality-abc-uncertainty",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:quality-d-uncertainty",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:relocation-gap",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:relocation-obs-threshold",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification."
    },
    {
      "witness_key": "obs:relocation-rms",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:relocation-uncertainty",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:rms-residual-bound",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:solubility-calc-temperature",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:station-gap-bound",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:studied-portion-length",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:triggering-pore-pressure",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:updated-horizontal-uncertainty",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:velocity-constraint-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, depth_reference, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:velocity-perturbation",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:vpvs-test-range",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:young-crust-age",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block states the quantity, its bounds and its unit at the modality the row records. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "cnt:min-obs-per-event",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the tally and what it counts. The subject the row names occurs in that same block. Fields judged: assertion_modality, count, count_scope, name, subject."
    },
    {
      "witness_key": "cnt:obs-deployed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the tally and what it counts. The subject the row names occurs in that same block. Fields judged: assertion_modality, count, count_scope, name, subject."
    },
    {
      "witness_key": "cnt:useful-obs",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the tally and what it counts. The subject the row names occurs in that same block. Fields judged: assertion_modality, count, count_scope, name, subject."
    },
    {
      "witness_key": "cnt:events-mar",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the tally and what it counts. The subject the row names occurs in that same block. Fields judged: assertion_modality, count, count_scope, name, subject."
    },
    {
      "witness_key": "cnt:events-romanche",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the tally and what it counts. The subject the row names occurs in that same block. Fields judged: assertion_modality, count, count_scope, name, subject."
    },
    {
      "witness_key": "cnt:forced-depth-subset",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the tally and what it counts. The subject the row names occurs in that same block. Fields judged: assertion_modality, count, count_scope, name, subject."
    },
    {
      "witness_key": "cnt:located-earthquakes",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the tally and what it counts. The subject the row names occurs in that same block. Fields judged: assertion_modality, count, count_scope, name, subject."
    },
    {
      "witness_key": "gchem:eq-atlantic-co2-avg",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, estimation_proxy, name, quantity_kind, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:eq-atlantic-co2-max",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, estimation_proxy, name, quantity_kind, subject, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:rc2-ba",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, melt_stage, name, quantity_kind, subject, unit, value_lower, value_qualification."
    },
    {
      "witness_key": "gchem:rc2-co2-ba",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, estimation_proxy, melt_stage, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:rc2-co2-ba90",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, estimation_proxy, melt_stage, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:rc2-co2-minimum",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, melt_stage, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification."
    },
    {
      "witness_key": "gchem:rc2-co2-preeruptive",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, melt_stage, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:rc2-co2-primary-calc",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block gives the segment, the range and the unit, but it does not name the two proxy elements the row records as the basis of the estimate; those are named in a block this witness does not reach. Fields judged: analyte, assertion_modality, determination, estimation_proxy, melt_stage, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:rc2-co2-rb",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, estimation_proxy, melt_stage, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:rc2-co2-rb90",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, estimation_proxy, melt_stage, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:rc2-rb",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, melt_stage, name, quantity_kind, subject, unit, value_lower, value_qualification."
    },
    {
      "witness_key": "gchem:rc3-co2-ba",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, estimation_proxy, melt_stage, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:rc3-co2-ba90",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, estimation_proxy, melt_stage, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:rc3-co2-primary-calc",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block gives the segment, the range and the unit, but it does not name the two proxy elements the row records as the basis of the estimate; those are named in a block this witness does not reach. Fields judged: analyte, assertion_modality, determination, estimation_proxy, melt_stage, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:rc3-co2-rb",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, estimation_proxy, melt_stage, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:rc3-co2-rb90",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, determination, estimation_proxy, melt_stage, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "gchem:swir-co2-highest",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the analyte, the melt stage, the bounds and the unit the row records. The subject the row names occurs in that same block. Fields judged: analyte, assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:abstract-deep-eq-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:bdb-isotherm",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, uncertainty, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:coverage-mar",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:coverage-romanche",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:deep-eq-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:deep-micro-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:forced-depths",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:h1-bdb-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:h1-isotherms",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:iceland-magmatic-depths",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification."
    },
    {
      "witness_key": "obs:interpreted-deep-eq-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:012"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, depth_reference, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:lab-melt-fraction",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:lab-water-content",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, subject, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:mar-half-spreading-rate",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:mar-segment-length",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:mayotte-depths",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification."
    },
    {
      "witness_key": "obs:no-eq-below-20km",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification."
    },
    {
      "witness_key": "obs:normal-depth-ntd2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:ntd1-length",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:ntd2-depth-10",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:ntd2-depth-range",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:ntd2-offset",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:occ-depth-range",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:offaxis-bdb-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:offaxis-crustal-age",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:rc2-crust-thickness",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:011"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, uncertainty, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:rc2-length",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:rc2-valley-width",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:rc3-length",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:shallow-eq-rti",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "obs:thermal-model-temp",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the quantity, its bounds and its unit at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, determination, name, quantity_kind, quantity_kind_class, subject, unit, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "method:cross-correlation",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "method:depth-resolution-tests",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "method:double-difference",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "method:fc-correction",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "method:first-motion",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "method:local-magnitude",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:8:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "method:location-criteria",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003",
        "page:7:block:008"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "method:ml-formula",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "method:nonlinear-location",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "method:stalta",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "method:station-corrections",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "method:swave-delay-removal",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "method:wadati",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the procedure and says what it was used for. Fields judged: description, name."
    },
    {
      "witness_key": "event:romanche-2016",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:004"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the event and the magnitude the row projects. Fields judged: event_type, name, quantity_kind, quantity_kind_class, value_lower, value_qualification, value_upper."
    },
    {
      "witness_key": "claim:ab-good-quality",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:acknowledgement-crew",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:043"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:acknowledgement-discussions",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:10:block:043"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block opens the thanks and breaks off inside the list of names, so it carries neither the reason given for the thanks nor more than one of the people thanked. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:all-authors-discussed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:046"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:axial-valley-floor-basaltic",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:both-perturbations-deep",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:brittle-10km-at-ntds",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:category-definitions",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:co2-behaves-incompatible",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:co2-solubility-pressure",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:compilation-covariates",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:correlations-used-globally",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:correspondence",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:11:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:crust-from-mantle-melt",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:deeper-eq-observed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:deepest-documented",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:degassing-volume-change",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:eq-in-mantle-below-10km",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:fig3-panel-content",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, claim_kind, name."
    },
    {
      "witness_key": "claim:fixed-depth-rms-worse",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:8:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the slower decrease and the higher final residuals, but the condition being described and the higher starting residuals fall in the block before it. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:focus-on-segments",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:h3-mylonite",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, claim_kind, hypothesis_disposition, name."
    },
    {
      "witness_key": "claim:h4-magmatic-tectonic",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002",
        "page:5:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, claim_kind, hypothesis_disposition, name."
    },
    {
      "witness_key": "claim:long-period-events",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:magmatic-tectonic-contexts-differ",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:manual-check",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:max-depth-compilation",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:max-depth-other-factors",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:max-depth-selection",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, claim_kind, name."
    },
    {
      "witness_key": "claim:max-depths-affected",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:mechanism-similar-volcanoes",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:melt-focused-narrow-zone",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:melt-migration-not-understood",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, claim_kind, name."
    },
    {
      "witness_key": "claim:melt-movement-not-applicable",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:melt-movement-strain",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:melt-resides-fractionates",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:more-events-needed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, claim_kind, name."
    },
    {
      "witness_key": "claim:no-competing-interests",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:047"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:no-current-eruption",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:ntd1-origin",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:occ-exhumed-mantle",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block carries the inference about exhumed mantle and the tectonic origin, but the sentence starts in the block before it, so the block does not say that peridotites are what indicate it. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:offaxis-magmatism",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:peer-review",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:11:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:preexisting-faults-favor-migration",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:primary-vs-preeruptive",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:publisher-note",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:11:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:ratios-good-proxy",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:reduced-velocity-preferred",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:samples-degassed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:seafloor-basalts-degassed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:shear-zone-with-detachment",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:shiptime-funded",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:station-corrections-iterated",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:swave-delays-removed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:005"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:tests-support-deep",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:tf-deep-eq-mylonite",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:trace-element-assumption",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, claim_kind, name."
    },
    {
      "witness_key": "claim:ultraslow-co2-high",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:updated-depth-data",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:velocity-model-matters",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:volatile-controls-magma",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:volatile-role-unknown",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, claim_kind, name."
    },
    {
      "witness_key": "claim:volatiles-extend-melting-depth",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:vpvs-reasonable",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:003"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block asserts what the row names, at the modality the row records. Fields judged: assertion_modality, name."
    },
    {
      "witness_key": "claim:axis-relocating",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:bdb-shallower-southward",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:co2-degassing-deep-eq",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, claim_kind, hypothesis_disposition, name, subject."
    },
    {
      "witness_key": "claim:co2-influences-lab-melt",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, claim_kind, name, subject."
    },
    {
      "witness_key": "claim:deep-eq-aligned",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003",
        "page:5:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:deep-events-not-artifacts",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:depths-not-artifact",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:detachment-inactive",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:enriched-basalts-low-melting",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:extinct-vent-too-far",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:fig3-panels",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:006"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, claim_kind, name, subject."
    },
    {
      "witness_key": "claim:fig6-panels",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:011"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, claim_kind, name, subject."
    },
    {
      "witness_key": "claim:five-models-enumerated",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:focal-not-robust",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, claim_kind, name, subject."
    },
    {
      "witness_key": "claim:h1-cold-lithosphere",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, claim_kind, hypothesis_disposition, name, subject."
    },
    {
      "witness_key": "claim:h2-hydrothermal-cooling",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, claim_kind, hypothesis_disposition, name, subject."
    },
    {
      "witness_key": "claim:higher-temp-hinders-nucleation",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:keller-volatiles-flush",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:010"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:lab-melt-co2-h2o",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:magmatism-dominates-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:mantle-hot",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:max-depth-not-following-relationship",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:2:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block states the mismatch but stops before the phrase ends, and it does not say that the relationship in question is one observed at other sites. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:melt-lens-defines-bdb",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:model1-inappropriate",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:model5-selected",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:no-active-vents-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:ntd2-bdb-normal",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:occ-recent-deformation",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:occ-shallow-ruptures",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:one-obs-no-data",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:007"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:rc2-magmatic-origin",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:rc2-no-detachment",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:rc2-rc3-analysed",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:rc2-robust",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:refraction-profile-used",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:rti-amagmatic",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:selected-model-more-events",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:small-pressure-increase-induces",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:snapshot-limitation",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:004"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, claim_kind, name, subject."
    },
    {
      "witness_key": "claim:tomography-normal-vpvs",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:003"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block asserts what the row names, at the modality the row records. The subject the row names occurs in that same block. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "claim:volatiles-reduce-solidus",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cited block carries the consequence and the boundary it applies to, but what does the reducing is named only in the block before it. Fields judged: assertion_modality, name, subject."
    },
    {
      "witness_key": "geo:askja",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:bdb",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001",
        "page:1:block:004"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: name."
    },
    {
      "witness_key": "geo:chain-tf",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:detachment-east",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:equatorial-atlantic",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: name."
    },
    {
      "witness_key": "geo:extinct-vent-field",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:fagradalsfjall",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:gakkel",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:iceland",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: name."
    },
    {
      "witness_key": "geo:inactive-mound",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:007"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:juan-de-fuca",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:knipovich",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:lab",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: name."
    },
    {
      "witness_key": "geo:logachev",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:mar",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001",
        "page:1:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: name."
    },
    {
      "witness_key": "geo:mayotte",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:moho",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:010",
        "page:7:block:011"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:neovolcanic-ridge",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, feature_orientation, name."
    },
    {
      "witness_key": "geo:ntd1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, feature_orientation, name."
    },
    {
      "witness_key": "geo:ntd1-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, feature_orientation, name."
    },
    {
      "witness_key": "geo:ntd2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, feature_orientation, name."
    },
    {
      "witness_key": "geo:ntd2-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, feature_orientation, name."
    },
    {
      "witness_key": "geo:occ",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:occ-normal-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, feature_orientation, name."
    },
    {
      "witness_key": "geo:rainbow",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:004"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:rc1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:rc2-bounding-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, feature_orientation, name."
    },
    {
      "witness_key": "geo:rc3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, feature_orientation, name."
    },
    {
      "witness_key": "geo:romanche-tf",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:rti",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "geo:swir",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the feature and support the kind and orientation the row projects. Fields judged: feature_kind, name."
    },
    {
      "witness_key": "work:article",
      "source_support": "SUPPORTED",
      "source_locators": [
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
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: container_title, doi, licence, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:cruise-portal",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:008"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: access_url, description, name, source_kind."
    },
    {
      "witness_key": "work:eq-catalog",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:008",
        "page:8:block:009"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: description, doi, name, source_kind."
    },
    {
      "witness_key": "work:petdb",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:005",
        "page:8:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: access_url, description, name, source_kind."
    },
    {
      "witness_key": "work:ref-001",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:012",
        "page:8:block:013"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-002",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:014"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-003",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:015"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-004",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:016"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-005",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:017"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-006",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:001",
        "page:9:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-007",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:003",
        "page:9:block:004"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, doi, name, pages, publication_year, source_kind."
    },
    {
      "witness_key": "work:ref-008",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-009",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:006"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-010",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:007"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-011",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:008"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-012",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:009"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-013",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:010"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-014",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:011",
        "page:9:block:012"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-015",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:013"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-016",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:014",
        "page:9:block:015"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, doi, name, pages, publication_year, source_kind."
    },
    {
      "witness_key": "work:ref-017",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:016"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-018",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:017",
        "page:9:block:018"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-019",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:019"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-020",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:020",
        "page:9:block:021"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-021",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:022"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, doi, name, pages, publication_year, source_kind."
    },
    {
      "witness_key": "work:ref-022",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:023",
        "page:9:block:024"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, doi, name, publication_year, source_kind."
    },
    {
      "witness_key": "work:ref-023",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:025",
        "page:9:block:026"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-024",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:027",
        "page:9:block:028"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-025",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:029"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind."
    },
    {
      "witness_key": "work:ref-026",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:030"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-027",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:031"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, doi, name, pages, publication_year, source_kind."
    },
    {
      "witness_key": "work:ref-028",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:031",
        "page:9:block:032"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-029",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:033"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-030",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:034"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-031",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:035"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-032",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:036"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-033",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:037",
        "page:9:block:038"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-034",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:039"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-035",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:040"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-036",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:041"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-037",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:042"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-038",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:043"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-039",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:044",
        "page:9:block:045"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-040",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:046",
        "page:9:block:047"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-041",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:048"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-042",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:049"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-043",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:050"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-044",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:051"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-045",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:052"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-046",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:053",
        "page:9:block:054"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-047",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:055"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-048",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:001",
        "page:9:block:056"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-049",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-050",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:003"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-051",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:004",
        "page:10:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-052",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:006",
        "page:10:block:007"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-053",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:008"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-054",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:009"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-055",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:010"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-056",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:011"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-057",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:012"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-058",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:013",
        "page:10:block:014"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-059",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:015"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-060",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:016"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-061",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:017"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-062",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:018"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-063",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:019"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-064",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:020"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-065",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:021"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-066",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:022",
        "page:10:block:023"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-067",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:024"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-068",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:025"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-069",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:026"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-070",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:027",
        "page:10:block:028"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-071",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:029"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-072",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:030"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-073",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:031",
        "page:10:block:032",
        "page:10:block:033"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: access_url, author_statement, name, publication_year, source_kind."
    },
    {
      "witness_key": "work:ref-074",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:034"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-075",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:035",
        "page:10:block:036"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, doi, name, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-076",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:037"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-077",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:038",
        "page:10:block:039"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-078",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:040"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:ref-079",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:041",
        "page:10:block:042"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: author_statement, container_title, name, pages, publication_year, source_kind, volume."
    },
    {
      "witness_key": "work:zenodo",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:008"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited reference blocks carry the bibliographic fields the row projects for this entry. Fields judged: name, source_kind."
    },
    {
      "witness_key": "rel:mar-in-atlantic",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "rel:rc1-bounded-detachment",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "rel:rc2-adjacent-ntd1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "rel:rc2-bounded-faults",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "rel:rc3-adjacent-ntd2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "rel:catalog-in-zenodo",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:008"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "sw:global-mapper",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:010"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the package, say what it did and give where it can be obtained. Fields judged: access_url, description, name."
    },
    {
      "witness_key": "sw:gmt6",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:010",
        "page:8:block:011"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the package, say what it did and give where it can be obtained. Fields judged: access_url, description, name, software_version."
    },
    {
      "witness_key": "sw:hash",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003",
        "page:8:block:010"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the package, say what it did and give where it can be obtained. Fields judged: access_url, description, name, software_version."
    },
    {
      "witness_key": "sw:hypodd",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006",
        "page:8:block:010"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the package, say what it did and give where it can be obtained. Fields judged: access_url, description, name, software_version."
    },
    {
      "witness_key": "sw:nonlinloc",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:004",
        "page:8:block:010"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the package, say what it did and give where it can be obtained. Fields judged: access_url, description, name."
    },
    {
      "witness_key": "sw:seisan",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002",
        "page:8:block:002",
        "page:8:block:010"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the package, say what it did and give where it can be obtained. Fields judged: access_url, description, name."
    },
    {
      "witness_key": "sw:velest",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:004",
        "page:8:block:010"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the package, say what it did and give where it can be obtained. Fields judged: access_url, description, name."
    },
    {
      "witness_key": "sw:zmap",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:002",
        "page:8:block:010"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the package, say what it did and give where it can be obtained. Fields judged: access_url, description, name."
    },
    {
      "witness_key": "rel:hash-used-for-focal",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:003"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "rel:nonlinloc-used-for-location",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:004"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "rel:seisan-used-for-stalta",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "agent:briais",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045",
        "page:1:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:brittany",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:brunelli",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045",
        "page:1:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:erc",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:french-government",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:grenet",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045",
        "page:1:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:hamelin",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045",
        "page:1:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:maia",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045",
        "page:1:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:nsfc",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:org-cnr-igag",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:org-geoocean",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:org-ipgp",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:org-sio",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:org-unimore",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:petracchini",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045",
        "page:1:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:singh",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044",
        "page:11:block:002",
        "page:1:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:tgir",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:yu",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044",
        "page:11:block:002",
        "page:1:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "agent:zjnsf",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited blocks name the person or body and support the kind of agent the row projects. Fields judged: agent_type, name."
    },
    {
      "witness_key": "award:erc-advanced",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the award and the identifier or programme the row projects. Fields judged: award_identifier, name."
    },
    {
      "witness_key": "award:fp7",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the award and the identifier or programme the row projects. Fields judged: award_programme, name."
    },
    {
      "witness_key": "award:investissements",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the award and the identifier or programme the row projects. Fields judged: award_programme, name."
    },
    {
      "witness_key": "award:isblue",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the award and the identifier or programme the row projects. Fields judged: award_identifier, award_programme, name."
    },
    {
      "witness_key": "award:nsfc",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the award and the identifier or programme the row projects. Fields judged: award_identifier, name."
    },
    {
      "witness_key": "award:sad",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the award and the identifier or programme the row projects. Fields judged: award_programme, name."
    },
    {
      "witness_key": "award:zjnsf",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the award and the identifier or programme the row projects. Fields judged: award_identifier, name."
    },
    {
      "witness_key": "rel:singh-funded-erc",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "rel:singh-funded-fp7",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "rel:yu-funded-nsfc",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "rel:yu-funded-zjnsf",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "sample:melt-inclusions",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the sample set and the material it is made of. Fields judged: description, name, sample_material."
    },
    {
      "witness_key": "sample:morb-obs-network",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the sample set and the material it is made of. Fields judged: description, name, sample_material."
    },
    {
      "witness_key": "sample:morb-rc2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the sample set and the material it is made of. Fields judged: description, name, sample_material."
    },
    {
      "witness_key": "sample:morb-rc3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the sample set and the material it is made of. Fields judged: description, name, sample_material."
    },
    {
      "witness_key": "sample:popping-rocks",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the sample set and the material it is made of. Fields judged: description, name, sample_material."
    },
    {
      "witness_key": "ratio:co2-ba",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block gives the ratio, the two elements it is taken between and the spread around it. Fields judged: assertion_modality, denominator_kind, name, numerator_kind, ratio_value, uncertainty."
    },
    {
      "witness_key": "ratio:co2-rb",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block gives the ratio, the two elements it is taken between and the spread around it. Fields judged: assertion_modality, denominator_kind, name, numerator_kind, ratio_value, uncertainty."
    },
    {
      "witness_key": "ratio:vp-vs",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:002"
      ],
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block gives the ratio, the two elements it is taken between and the spread around it. Fields judged: assertion_modality, denominator_kind, name, numerator_kind, ratio_value."
    },
    {
      "witness_key": "rel:morb-from-petdb",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:005"
      ],
      "rationale": "NO_STATEMENT_DIGEST DERIVATION_LOCAL The block that states the tie also derives both of its endpoints, so the link rests on one place in the reading. Fields judged: relation_type, source_id, target_id."
    },
    {
      "witness_key": "model:co2-solubility",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the model and says what it was used for. Fields judged: description, model_kind, name."
    },
    {
      "witness_key": "model:iacono-marziano",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the model and says what it was used for. Fields judged: description, model_kind, name."
    },
    {
      "witness_key": "model:min-1d",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:004"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the model and says what it was used for. Fields judged: description, model_kind, name."
    },
    {
      "witness_key": "model:thermal",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the model and says what it was used for. Fields judged: description, model_kind, name."
    },
    {
      "witness_key": "model:thermal-simulated",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:012"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the model and says what it was used for. Fields judged: description, model_kind, name."
    },
    {
      "witness_key": "model:velocity-1d",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the model and says what it was used for. Fields judged: description, model_kind, name."
    },
    {
      "witness_key": "model:velocity-model-1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:009"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the model and says what it was used for. Fields judged: description, model_kind, name."
    },
    {
      "witness_key": "model:velocity-model-5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:003"
      ],
      "rationale": "NO_STATEMENT_DIGEST NO_SUBJECT_IN_ROW The cited block names the model and says what it was used for. Fields judged: description, model_kind, name."
    }
  ],
  "questions": [
    {
      "question_id": "CQ-B-T1-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The deployment and the number of instruments each come back on a row of their own; the year it was carried out does not, so the answer is short by one element.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "cruise_name",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "deployment_year",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The reading gives the year of the deployment twice, in the results and again in the methods, and the contract carries year-valued fields on other types; no returned record or field holds a year for this deployment and the capture declares no gap for it."
        },
        {
          "semantic": "instrument_count",
          "row_index": 76,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:10:block:043",
        "page:10:block:046",
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "cruise:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instr:obs"
        },
        {
          "row_index": 2,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 3,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 4,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 5,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 6,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 7,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 8,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 9,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 17,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 18,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 19,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 20,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 21,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 22,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 23,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 24,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 25,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 26,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 27,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 28,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 29,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 30,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 31,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 32,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 33,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 34,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 35,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 36,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 37,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 38,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 39,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 40,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 41,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 42,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 43,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 44,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 45,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 46,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 47,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 48,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 49,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 50,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 51,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 52,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 53,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 54,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 55,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 56,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 57,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 58,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 59,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 60,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 61,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 62,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 63,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 64,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 65,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 66,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 67,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 68,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 69,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 70,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 71,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 72,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 73,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 74,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 82,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 83,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 84,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 85,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 86,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 87,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 88,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 89,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 90,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 91,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 92,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 93,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 94,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 95,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 96,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 97,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 98,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 99,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 100,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 101,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 102,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 103,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 105,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 106,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 108,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 109,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 110,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 111,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 112,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 113,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 114,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 115,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 116,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 117,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 118,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 119,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 120,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 121,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 122,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 124,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 125,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 126,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 127,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 128,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 129,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-B-T1-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The identifier comes back on the article row; neither editorial date does, and the capture says in so many words that the contract has nowhere to put them.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "article_doi",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "received_date",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "The capture keeps the editorial dates in an assertion of their own and declares there that the contract has no type and no slot for them, so nothing in the graph could carry this date."
        },
        {
          "semantic": "accepted_date",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "Same declared absence as the received date: the dates are retained in one assertion that formalizes no record, under a stated absence of any type or slot for them."
        }
      ],
      "source_locators": [
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
          "witness_key": "work:article"
        },
        {
          "row_index": 1,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 2,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 3,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 4,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 5,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 6,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 7,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 8,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 9,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 10,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 11,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 12,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 13,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 14,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 15,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 16,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 83,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 84,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 85,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 86,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 87,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 88,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 89,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 90,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 91,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 92,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 93,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 94,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 95,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 96,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 97,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 98,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 99,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 100,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 101,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 102,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 103,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 104,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 105,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 106,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 107,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 108,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 109,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 110,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 111,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 112,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 113,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 114,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 115,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 116,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 117,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 118,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 119,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 120,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 121,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 122,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 123,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 124,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 125,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 126,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 127,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 128,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 129,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 130,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 131,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 132,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 133,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 134,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 135,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 136,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 137,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 138,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 139,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 140,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 141,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 142,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 143,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 144,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 145,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 146,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 147,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 148,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 149,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 150,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 151,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 152,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 153,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 154,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 155,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 156,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 157,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 158,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 159,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 160,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 161,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 162,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 163,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 164,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 165,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 166,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 167,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 168,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 169,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 170,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 171,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 172,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 173,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 174,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 175,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 176,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 177,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 178,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 179,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 180,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 181,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 182,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 183,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 184,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 185,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 186,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 187,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 188,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 189,
          "witness_key": "claim:volatiles-reduce-solidus"
        }
      ]
    },
    {
      "question_id": "CQ-B-T1-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four elements come back: the ridge, the ocean region it lies in, the four subsection labels one per row, and the name of the segment to the south.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "study_area_name",
          "row_index": 14,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "ocean_region",
          "row_index": 4,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "subsection_labels",
          "row_index": 25,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "adjacent_segment_label",
          "row_index": 28,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:1:block:005",
        "page:2:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 33,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 35,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 36,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 37,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 38,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 39,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 42,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 43,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 45,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 46,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 48,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 49,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 50,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 52,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 53,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 55,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 56,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 57,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 58,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 62,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 63,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 68,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 69,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 71,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 72,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 73,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 74,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 75,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 76,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 77,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 78,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 79,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 80,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 81,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 84,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 85,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 88,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 89,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 90,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 91,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 92,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 95,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 96,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 97,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 98,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 99,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 100,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 101,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 102,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 103,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 104,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 105,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 106,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 107,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 108,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 109,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 110,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 111,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 112,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 113,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 114,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 115,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 116,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 117,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 118,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 119,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 120,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 121,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 122,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 123,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 124,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 125,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 126,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 127,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 128,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 129,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 130,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 132,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 133,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 134,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 135,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 136,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 137,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 138,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 139,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 140,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 141,
          "witness_key": "claim:selected-model-more-events"
        }
      ]
    },
    {
      "question_id": "CQ-B-T1-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All three named tools come back as rows of their own, and each of them carries the place it can be obtained from, so the availability element rides on the same rows.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "phase_picking_software",
          "row_index": 102,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "location_software",
          "row_index": 101,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "relocation_software",
          "row_index": 100,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "software_availability_source",
          "row_index": 102,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:6:block:002",
        "page:7:block:004",
        "page:7:block:006",
        "page:8:block:002",
        "page:8:block:010"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:cross-correlation"
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
          "witness_key": "method:first-motion"
        },
        {
          "row_index": 5,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 6,
          "witness_key": "method:location-criteria"
        },
        {
          "row_index": 7,
          "witness_key": "method:ml-formula"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 10,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 11,
          "witness_key": "method:swave-delay-removal"
        },
        {
          "row_index": 12,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 13,
          "witness_key": "work:article"
        },
        {
          "row_index": 14,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 15,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 16,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 96,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 97,
          "witness_key": "sw:global-mapper"
        },
        {
          "row_index": 98,
          "witness_key": "sw:gmt6"
        },
        {
          "row_index": 99,
          "witness_key": "sw:hash"
        },
        {
          "row_index": 100,
          "witness_key": "sw:hypodd"
        },
        {
          "row_index": 101,
          "witness_key": "sw:nonlinloc"
        },
        {
          "row_index": 102,
          "witness_key": "sw:seisan"
        },
        {
          "row_index": 103,
          "witness_key": "sw:velest"
        },
        {
          "row_index": 104,
          "witness_key": "sw:zmap"
        },
        {
          "row_index": 105,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 106,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 107,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 108,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 109,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 110,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 111,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 112,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 113,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 114,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 115,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 116,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 117,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 118,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 119,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 120,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 121,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 122,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 123,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 124,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 125,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 126,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 127,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 128,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 129,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 130,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 131,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 132,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 133,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 134,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 135,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 136,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 137,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 138,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 139,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 140,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 141,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 142,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 143,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 144,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 145,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 146,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 147,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 148,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 149,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 150,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 151,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 152,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 153,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 154,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 155,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 156,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 157,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 158,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 159,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 160,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 161,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 162,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 163,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 164,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 165,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 166,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 167,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 168,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 169,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 170,
          "witness_key": "rel:hash-used-for-focal"
        },
        {
          "row_index": 171,
          "witness_key": "rel:nonlinloc-used-for-location"
        },
        {
          "row_index": 172,
          "witness_key": "rel:seisan-used-for-stalta"
        },
        {
          "row_index": 173,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 174,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 175,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 176,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 177,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 178,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 179,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 180,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 181,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 182,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 183,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 184,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 185,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 186,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 187,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 188,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 189,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 190,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 191,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 192,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 193,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 194,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 195,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 196,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 197,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 198,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 199,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 200,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 201,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 202,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 203,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 204,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 205,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 206,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 207,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 208,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 209,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 210,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 211,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 212,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 213,
          "witness_key": "claim:volatiles-reduce-solidus"
        }
      ]
    },
    {
      "question_id": "CQ-B-T1-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four come back: the repository, the deposited dataset with its identifier and what it holds, and a separate route for the raw recordings.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "repository_name",
          "row_index": 83,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "dataset_identifier",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "deposited_data_description",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "raw_data_access_route",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:8:block:008",
        "page:8:block:009"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "work:article"
        },
        {
          "row_index": 1,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 2,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 3,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 4,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 5,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 6,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 7,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 8,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 9,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 10,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 11,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 12,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 13,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 14,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 15,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 16,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 83,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 84,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 85,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 86,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 87,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 88,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 89,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 90,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 91,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 92,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 93,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 94,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 95,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 96,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 97,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 98,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 99,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 100,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 101,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 102,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 103,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 104,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 105,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 106,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 107,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 108,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 109,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 110,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 111,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 112,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 113,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 114,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 115,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 116,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 117,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 118,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 119,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 120,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 121,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 122,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 123,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 124,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 125,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 126,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 127,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 128,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 129,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 130,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 131,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 132,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 133,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 134,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 135,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 136,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 137,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 138,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 139,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 140,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 141,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 142,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 143,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 144,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 145,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 146,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 147,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 148,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 149,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 150,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 151,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 152,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 153,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 154,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 155,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 156,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 157,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 158,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 159,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 160,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 161,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 162,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 163,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 164,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 165,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 166,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 167,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 168,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 169,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 170,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 171,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 172,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 173,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 174,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 175,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 176,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 177,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 178,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 179,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 180,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 181,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 182,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 183,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 184,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 185,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 186,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 187,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 188,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 189,
          "witness_key": "claim:volatiles-reduce-solidus"
        }
      ]
    },
    {
      "question_id": "CQ-B-T2-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The authors come back as rows, and nothing else does: what each of them did, who supervised the seismic work and who designed the project are all left inside the retained contribution statements rather than in any field.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "author_name",
          "row_index": 17,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "contribution_role",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "Each author's share of the work stays inside the retained contribution statements the author rows reach by locator; no field projected on an author row carries a role, and the capture's own gap says the role slot was left unset because the source states the work in its own words rather than in the taxonomy the contract carries."
        },
        {
          "semantic": "supervision_relation",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "Who oversaw acquisition and processing is stated only in the same retained contribution statement; no returned row or relation carries that tie."
        },
        {
          "semantic": "project_design_credit",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "Who designed the project is likewise only in the retained contribution statement, with no projected field or relation carrying it."
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
          "witness_key": "agent:briais"
        },
        {
          "row_index": 1,
          "witness_key": "agent:brittany"
        },
        {
          "row_index": 2,
          "witness_key": "agent:brunelli"
        },
        {
          "row_index": 3,
          "witness_key": "agent:erc"
        },
        {
          "row_index": 4,
          "witness_key": "agent:french-government"
        },
        {
          "row_index": 5,
          "witness_key": "agent:grenet"
        },
        {
          "row_index": 6,
          "witness_key": "agent:hamelin"
        },
        {
          "row_index": 7,
          "witness_key": "agent:maia"
        },
        {
          "row_index": 8,
          "witness_key": "agent:nsfc"
        },
        {
          "row_index": 9,
          "witness_key": "agent:org-cnr-igag"
        },
        {
          "row_index": 10,
          "witness_key": "agent:org-geoocean"
        },
        {
          "row_index": 11,
          "witness_key": "agent:org-ipgp"
        },
        {
          "row_index": 12,
          "witness_key": "agent:org-sio"
        },
        {
          "row_index": 13,
          "witness_key": "agent:org-unimore"
        },
        {
          "row_index": 14,
          "witness_key": "agent:petracchini"
        },
        {
          "row_index": 15,
          "witness_key": "agent:singh"
        },
        {
          "row_index": 16,
          "witness_key": "agent:tgir"
        },
        {
          "row_index": 17,
          "witness_key": "agent:yu"
        },
        {
          "row_index": 18,
          "witness_key": "agent:zjnsf"
        },
        {
          "row_index": 19,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 20,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 21,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 22,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 23,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 24,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 25,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 26,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 27,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 28,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 29,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 30,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 31,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 32,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 33,
          "witness_key": "claim:deeper-eq-observed"
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
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 37,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 38,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 39,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 40,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 41,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 42,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 43,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 44,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 45,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 46,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 47,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 48,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 49,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 50,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 51,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 52,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 53,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 54,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 55,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 56,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 57,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 58,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 59,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 60,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 61,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 62,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 63,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 64,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 65,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 66,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 67,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 68,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 69,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 70,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 71,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 72,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 73,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 74,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 75,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 76,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 77,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 78,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 79,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 80,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 81,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 82,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 83,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 84,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 85,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 86,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 87,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 88,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 89,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 90,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 91,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 92,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 93,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 94,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 95,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 96,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 97,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 98,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 99,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 100,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 101,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 102,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 103,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 104,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 105,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 106,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 107,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 108,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 109,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 110,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 111,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 112,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 113,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 114,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 115,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 116,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 117,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 118,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 119,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 120,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 121,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 122,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 123,
          "witness_key": "claim:volatiles-reduce-solidus"
        }
      ]
    },
    {
      "question_id": "CQ-B-T2-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Bodies, grant references and the tie between an author and an award all come back; who paid for the time at sea does not, because the record that says so is outside this question's cases.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "funder_name",
          "row_index": 11,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "grant_identifier",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "funded_party",
          "row_index": 27,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "ship_time_funder",
          "row_index": null,
          "absent_reason": "UNREACHED_RECORD",
          "note": "A record does state who paid for the time at sea, and this question's cases do not return it; the body itself comes back only as an organisation, with nothing on that row tying it to the ship time."
        }
      ],
      "source_locators": [
        "page:10:block:044"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "cruise:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "award:erc-advanced"
        },
        {
          "row_index": 2,
          "witness_key": "award:fp7"
        },
        {
          "row_index": 3,
          "witness_key": "award:investissements"
        },
        {
          "row_index": 4,
          "witness_key": "award:isblue"
        },
        {
          "row_index": 5,
          "witness_key": "award:nsfc"
        },
        {
          "row_index": 6,
          "witness_key": "award:sad"
        },
        {
          "row_index": 7,
          "witness_key": "award:zjnsf"
        },
        {
          "row_index": 8,
          "witness_key": "agent:briais"
        },
        {
          "row_index": 9,
          "witness_key": "agent:brittany"
        },
        {
          "row_index": 10,
          "witness_key": "agent:brunelli"
        },
        {
          "row_index": 11,
          "witness_key": "agent:erc"
        },
        {
          "row_index": 12,
          "witness_key": "agent:french-government"
        },
        {
          "row_index": 13,
          "witness_key": "agent:grenet"
        },
        {
          "row_index": 14,
          "witness_key": "agent:hamelin"
        },
        {
          "row_index": 15,
          "witness_key": "agent:maia"
        },
        {
          "row_index": 16,
          "witness_key": "agent:nsfc"
        },
        {
          "row_index": 17,
          "witness_key": "agent:org-cnr-igag"
        },
        {
          "row_index": 18,
          "witness_key": "agent:org-geoocean"
        },
        {
          "row_index": 19,
          "witness_key": "agent:org-ipgp"
        },
        {
          "row_index": 20,
          "witness_key": "agent:org-sio"
        },
        {
          "row_index": 21,
          "witness_key": "agent:org-unimore"
        },
        {
          "row_index": 22,
          "witness_key": "agent:petracchini"
        },
        {
          "row_index": 23,
          "witness_key": "agent:singh"
        },
        {
          "row_index": 24,
          "witness_key": "agent:tgir"
        },
        {
          "row_index": 25,
          "witness_key": "agent:yu"
        },
        {
          "row_index": 26,
          "witness_key": "agent:zjnsf"
        },
        {
          "row_index": 27,
          "witness_key": "rel:singh-funded-erc"
        },
        {
          "row_index": 28,
          "witness_key": "rel:singh-funded-fp7"
        },
        {
          "row_index": 29,
          "witness_key": "rel:yu-funded-nsfc"
        },
        {
          "row_index": 30,
          "witness_key": "rel:yu-funded-zjnsf"
        }
      ]
    },
    {
      "question_id": "CQ-B-T2-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The two bounding faults come back on one row's own wording and the bounding relation comes back as a returned link; where the study area sits inside the segment and where the dome sits relative to the axis are both left in retained statements.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounding_transform_names",
          "row_index": 245,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "segment_position",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "Where the study area sits inside that segment survives only in the statement the length record binds by locator and digest; no projected field carries a position."
        },
        {
          "semantic": "core_complex_location",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "Where the dome sits relative to the ridge axis survives only in the statement the amagmatic-segment claim binds by locator and digest; the feature row carries a name and a kind and no position."
        },
        {
          "semantic": "fault_relation",
          "row_index": 170,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:1:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 33,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 35,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 36,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 37,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 38,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 39,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 42,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 43,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 45,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 46,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 48,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 49,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 50,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 52,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 53,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 55,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 56,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 57,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 58,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 62,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 63,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 68,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 69,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 71,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 72,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 73,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 74,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 75,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 76,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 77,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 78,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 79,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 80,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 81,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 84,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 85,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 88,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 89,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 90,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 91,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 92,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 95,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 96,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 111,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 112,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 113,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 114,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 115,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 116,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 120,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 122,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 123,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 124,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 125,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 126,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 127,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 128,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 129,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 130,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 131,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 132,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 133,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 134,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 135,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 136,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 137,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 138,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 139,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 140,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 141,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 142,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 143,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 144,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 145,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 146,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 147,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 148,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 149,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 150,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 151,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-tick-interval"
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
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 159,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 160,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 161,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 162,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 163,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 164,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 165,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 167,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 168,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 169,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 170,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 171,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 174,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 175,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 176,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 177,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 178,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 179,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 180,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 181,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 182,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 183,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 184,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 185,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 186,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 187,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 188,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 189,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 190,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 191,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 192,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 193,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 194,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 195,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 196,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 197,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 198,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 199,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 200,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 201,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 202,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 203,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 204,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 205,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 206,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 207,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 209,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 210,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 212,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 213,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 214,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 231,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 232,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 233,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 234,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 235,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 238,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 239,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 240,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 241,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 242,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 244,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 247,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 248,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 249,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 250,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 253,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 254,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 255,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 256,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 260,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 261,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 262,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 263,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 264,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 265,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 266,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 267,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 268,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 269,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-T2-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The flank, the inference about depth and the layer the events sit in all come back; which earlier work the thickness rests on is only in the bound statement.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "crustal_thickness_source",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "Which earlier work the thickness rests on survives only inside the statement the thickness record binds by locator and digest; no field on any returned row names it."
        },
        {
          "semantic": "flank_identification",
          "row_index": 208,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "depth_inference",
          "row_index": 133,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "hosting_layer",
          "row_index": 133,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "work:article"
        },
        {
          "row_index": 33,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 34,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 35,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 96,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 97,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 98,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 99,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 100,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 101,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 102,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 103,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 104,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 105,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 106,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 107,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 108,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 109,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 110,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 111,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 112,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 113,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 114,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 115,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 116,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 117,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 118,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 119,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 120,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 121,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 122,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 123,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 124,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 125,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 126,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 127,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 128,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 129,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 130,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 132,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 133,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 134,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 135,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 136,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 137,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 138,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 139,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 140,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 141,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 142,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 143,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 144,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 145,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 146,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 147,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 148,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 149,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 150,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 151,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 152,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 153,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 154,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 155,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 156,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 157,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 158,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 159,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 160,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 161,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 162,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 163,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 164,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 165,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 166,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 167,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 168,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 169,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 170,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 171,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 172,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 173,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 174,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 175,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 176,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 177,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 178,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 179,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 184,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 186,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 187,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 188,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 189,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 190,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 191,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 192,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 193,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 194,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 195,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 196,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 197,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 198,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 199,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 200,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 201,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 202,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 203,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 204,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 205,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 206,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 207,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 208,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 209,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 210,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 211,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 212,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 213,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 214,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 215,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 216,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 217,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 218,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 219,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 220,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 221,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 222,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 223,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 224,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 225,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 226,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 227,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 228,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 229,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 230,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 231,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 232,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 237,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 238,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 239,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 240,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 241,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 242,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 243,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 244,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 245,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 246,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 248,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 249,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 251,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 252,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 253,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 254,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 255,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 256,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 257,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 258,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 259,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 260,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 261,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 262,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 263,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 264,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 265,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 266,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 267,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 268,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 269,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 270,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 271,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 272,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 273,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 274,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 275,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 276,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 277,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 278,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 279,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 280,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 281,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 282,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 283,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 284,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 285,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 286,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 287,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 288,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 289,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 290,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 291,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 292,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 293,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 294,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 295,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 296,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 297,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 298,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 299,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 300,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 301,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 302,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 303,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 304,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 305,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 306,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 307,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 308,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 309,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 310,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 311,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 312,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 313,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 314,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 315,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 316,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 317,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 318,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 319,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 320,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 321,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 322,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 323,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 324,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 325,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 326,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 327,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 328,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 329,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 330,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 331,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 332,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 333,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 334,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 335,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 336,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 337,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 338,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 339,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 340,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 341,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 342,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 343,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 344,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 345,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 346,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 347,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 348,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 349,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 350,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 351,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 352,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 353,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 354,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-T2-05",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Four of five come back: the ratio pair, the database, the purpose the ratios were put to and the segment they were applied to. Whose compilation supplied the ratios is only a citation number.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "ratio_pair_identity",
          "row_index": 201,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "ratio_source_study",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The reading attributes both ratios by citation number alone; the graph holds reference records, no returned field or relation ties either ratio to one of them, and the capture declares no gap here."
        },
        {
          "semantic": "sample_database_name",
          "row_index": 35,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "computation_purpose",
          "row_index": 132,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "target_segment_label",
          "row_index": 316,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:6:block:005",
        "page:8:block:005",
        "page:8:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "work:article"
        },
        {
          "row_index": 33,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 34,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 35,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 96,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 97,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 98,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 99,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 100,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 101,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 102,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 103,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 104,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 105,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 106,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 107,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 108,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 109,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 110,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 111,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 112,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 113,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 114,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 115,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 116,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 117,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 118,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 119,
          "witness_key": "sample:morb-rc3"
        },
        {
          "row_index": 120,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 121,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 122,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 123,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 124,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 125,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 126,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 127,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 128,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 129,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 130,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 131,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 132,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 133,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 134,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 135,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 136,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 137,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 138,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 139,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 140,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 141,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 142,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 143,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 144,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 145,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 146,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 147,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 148,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 149,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 150,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 151,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 152,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 153,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 154,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 155,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 156,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 157,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 158,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 159,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 160,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 161,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 162,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 163,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 164,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 165,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 166,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 167,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 168,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 169,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 170,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 171,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 172,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 173,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 174,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 175,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 176,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 177,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 178,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 179,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 180,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 181,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 182,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 183,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 184,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 186,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 187,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 188,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 189,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 190,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 191,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 192,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 193,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 194,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 195,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 196,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 197,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 198,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 199,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 200,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 201,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 202,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 203,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 204,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 205,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 206,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 207,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 208,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 209,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 210,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 211,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 212,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 213,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 214,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 215,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 216,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 217,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 218,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 219,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 220,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 221,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 222,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 223,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 224,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 225,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 226,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 227,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 228,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 229,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 230,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 231,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 232,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 233,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 234,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 235,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 236,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 237,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 238,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 239,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 240,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 241,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 242,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 243,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 244,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 245,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 246,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 247,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 248,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 249,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 250,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 251,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 252,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 253,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 254,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 255,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 256,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 257,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 258,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 259,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 260,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 261,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 262,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 263,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 264,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 265,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 266,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 267,
          "witness_key": "rel:morb-from-petdb"
        },
        {
          "row_index": 268,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 269,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 270,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 271,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 272,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 273,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 274,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 275,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 276,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 277,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 278,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 279,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 280,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 281,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 282,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 283,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 284,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 285,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 286,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 287,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 288,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 289,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 290,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 291,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 292,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 293,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 294,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 295,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 296,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 297,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 298,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 299,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 300,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 301,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 302,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 303,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 304,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 305,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 306,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 307,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 308,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 309,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 310,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 311,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 312,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 313,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 314,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 315,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 316,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 317,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 318,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 319,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 320,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 321,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 322,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 323,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 324,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 325,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 326,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 327,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 328,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 329,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 330,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 331,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 332,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 333,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 334,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 335,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 336,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 337,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 338,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 339,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 340,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 341,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 342,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 343,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 344,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 345,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 346,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 347,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 348,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 349,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 350,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 351,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 352,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 353,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 354,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 355,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 356,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 357,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 358,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 359,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 360,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 361,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 362,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 363,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-T3-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Both rates and the unit come back on rows of their own; whose earlier work the figures rest on is carried only as a citation number in the bound statement.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "half_rate_value",
          "row_index": 329,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "full_rate_value",
          "row_index": 219,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "rate_unit",
          "row_index": 219,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "rate_source_attribution",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The figure is attributed by a citation number inside the bound statement; the work it points to is a record in the graph, nothing returned ties the rate to it, and no gap declares the omission."
        }
      ],
      "source_locators": [
        "page:1:block:005",
        "page:2:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "work:article"
        },
        {
          "row_index": 33,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 34,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 35,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 96,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 97,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 98,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 99,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 100,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 101,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 102,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 103,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 104,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 105,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 106,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 107,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 108,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 109,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 110,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 111,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 112,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 113,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 114,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 115,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 116,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 117,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 118,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 119,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 120,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 121,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 122,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 123,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 124,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 125,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 126,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 127,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 128,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 129,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 130,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 132,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 133,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 134,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 135,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 136,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 137,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 138,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 139,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 140,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 141,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 142,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 143,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 144,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 145,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 146,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 147,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 148,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 149,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 150,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 151,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 152,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 153,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 154,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 155,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 156,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 157,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 158,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 159,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 160,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 161,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 162,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 163,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 164,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 165,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 166,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 167,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 168,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 169,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 170,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 171,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 172,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 173,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 174,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 175,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 176,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 177,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 178,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 179,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 184,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 186,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 187,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 188,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 189,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 190,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 191,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 192,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 193,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 194,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 195,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 196,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 197,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 198,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 199,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 200,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 201,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 202,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 203,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 204,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 205,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 206,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 207,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 208,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 209,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 210,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 211,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 212,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 213,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 214,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 215,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 216,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 217,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 218,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 219,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 220,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 221,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 222,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 223,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 224,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 225,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 226,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 227,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 228,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 229,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 230,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 231,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 232,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 237,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 238,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 239,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 240,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 241,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 242,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 243,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 244,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 245,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 246,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 248,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 249,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 251,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 252,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 253,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 254,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 255,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 256,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 257,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 258,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 259,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 260,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 261,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 262,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 263,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 264,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 265,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 266,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 267,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 268,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 269,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 270,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 271,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 272,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 273,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 274,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 275,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 276,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 277,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 278,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 279,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 280,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 281,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 282,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 283,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 284,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 285,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 286,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 287,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 288,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 289,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 290,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 291,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 292,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 293,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 294,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 295,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 296,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 297,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 298,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 299,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 300,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 301,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 302,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 303,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 304,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 305,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 306,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 307,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 308,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 309,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 310,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 311,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 312,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 313,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 314,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 315,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 316,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 317,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 318,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 319,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 320,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 321,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 322,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 323,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 324,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 325,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 326,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 327,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 328,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 329,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 330,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 331,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 332,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 333,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 334,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 335,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 336,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 337,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 338,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 339,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 340,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 341,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 342,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 343,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 344,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 345,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 346,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 347,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 348,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 349,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 350,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 351,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 352,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 353,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 354,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-T3-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four come back: the recording span on the deployment row, the spacing, and the two instrument counts on separate count rows.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "recording_duration",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "instrument_spacing",
          "row_index": 45,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "usable_instrument_count",
          "row_index": 77,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "instrument_count",
          "row_index": 76,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:10:block:043",
        "page:10:block:046",
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "cruise:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instr:obs"
        },
        {
          "row_index": 2,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 3,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 4,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 5,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 6,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 7,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 8,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 9,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 17,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 18,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 19,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 20,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 21,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 22,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 23,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 24,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 25,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 26,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 27,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 28,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 29,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 30,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 31,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 32,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 33,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 34,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 35,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 36,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 37,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 38,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 39,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 40,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 41,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 42,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 43,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 44,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 45,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 46,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 47,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 48,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 49,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 50,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 51,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 52,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 53,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 54,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 55,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 56,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 57,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 58,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 59,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 60,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 61,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 62,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 63,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 64,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 65,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 66,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 67,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 68,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 69,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 70,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 71,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 72,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 73,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 74,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 82,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 83,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 84,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 85,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 86,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 87,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 88,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 89,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 90,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 91,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 92,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 93,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 94,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 95,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 96,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 97,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 98,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 99,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 100,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 101,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 102,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 103,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 105,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 106,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 108,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 109,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 110,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 111,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 112,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 113,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 114,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 115,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 116,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 117,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 118,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 119,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 120,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 121,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 122,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 124,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 125,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 126,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 127,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 128,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 129,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-B-T3-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four come back: the located count, the relocated count, and the average horizontal uncertainty with its unit on one row.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "located_event_count",
          "row_index": 87,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "relocated_event_count",
          "row_index": 93,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "horizontal_uncertainty_value",
          "row_index": 154,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "uncertainty_unit",
          "row_index": 154,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:6:block:005",
        "page:7:block:006",
        "page:7:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:cross-correlation"
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
          "witness_key": "method:first-motion"
        },
        {
          "row_index": 5,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 6,
          "witness_key": "method:location-criteria"
        },
        {
          "row_index": 7,
          "witness_key": "method:ml-formula"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 10,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 11,
          "witness_key": "method:swave-delay-removal"
        },
        {
          "row_index": 12,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 13,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 14,
          "witness_key": "sw:global-mapper"
        },
        {
          "row_index": 15,
          "witness_key": "sw:gmt6"
        },
        {
          "row_index": 16,
          "witness_key": "sw:hash"
        },
        {
          "row_index": 17,
          "witness_key": "sw:hypodd"
        },
        {
          "row_index": 18,
          "witness_key": "sw:nonlinloc"
        },
        {
          "row_index": 19,
          "witness_key": "sw:seisan"
        },
        {
          "row_index": 20,
          "witness_key": "sw:velest"
        },
        {
          "row_index": 21,
          "witness_key": "sw:zmap"
        },
        {
          "row_index": 22,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 23,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 24,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 25,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 26,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 27,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 28,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 29,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 30,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 31,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 32,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 33,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 34,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 35,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 36,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 37,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 38,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 39,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 40,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 41,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 42,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 43,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 44,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 45,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 46,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 47,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 48,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 49,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 50,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 51,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 52,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 53,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 54,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 55,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 56,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 57,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 58,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 59,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 60,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 61,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 62,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 63,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 64,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 65,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 66,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 67,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 68,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 69,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 70,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 71,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 72,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 73,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 74,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 75,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 76,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 77,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 78,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 79,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 80,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 81,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 82,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 83,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 84,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 85,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 86,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 87,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 88,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 91,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 92,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 93,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 94,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 95,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 96,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 101,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 102,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 103,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 104,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 105,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 106,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 107,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 108,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 109,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 110,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 111,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 112,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 113,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 114,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 115,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 116,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 117,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 118,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 119,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 120,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 121,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 122,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 123,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 124,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 125,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 126,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 127,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 128,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 129,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 130,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 131,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 132,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 133,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 134,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 135,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 136,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 137,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 138,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 139,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 140,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 141,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 142,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 143,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 144,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 145,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 146,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 147,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 148,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 149,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 150,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 151,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 152,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 153,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 154,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 156,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 157,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 158,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 159,
          "witness_key": "rel:hash-used-for-focal"
        },
        {
          "row_index": 160,
          "witness_key": "rel:nonlinloc-used-for-location"
        },
        {
          "row_index": 161,
          "witness_key": "rel:seisan-used-for-stalta"
        },
        {
          "row_index": 162,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 163,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 164,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 165,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 166,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 167,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 168,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 169,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 170,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 171,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 172,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 173,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 174,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 175,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 176,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 177,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 178,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 179,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 180,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 181,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 182,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 183,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 184,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 185,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 186,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 187,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 188,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 189,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 190,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 191,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 192,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 193,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 194,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 195,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 196,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 197,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 198,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 199,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 200,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 201,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 202,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 203,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 204,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 205,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 206,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 207,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 208,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 209,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 210,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 211,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 212,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 213,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 214,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 227,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 228,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 229,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 230,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 231,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 232,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 233,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 234,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 236,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 237,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 238,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 239,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 240,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 241,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 242,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 243,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 244,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 245,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 246,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 247,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 248,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 249,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 250,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 251,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 252,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 253,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 254,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 255,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 256,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 257,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-B-T3-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One row carries all five: the range, the unit, the segment it belongs to, the proxy element it was estimated from and the fact that it is an estimate rather than a measurement.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "concentration_range",
          "row_index": 226,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "concentration_unit",
          "row_index": 226,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "segment_label",
          "row_index": 226,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "proxy_element",
          "row_index": 226,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "calculation_status",
          "row_index": 226,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 33,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 34,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 35,
          "witness_key": "sample:morb-rc3"
        },
        {
          "row_index": 36,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 37,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 38,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 39,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 41,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 42,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 43,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 44,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 45,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 46,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 47,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 48,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 49,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 50,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 51,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 53,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 54,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 55,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 56,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 57,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 58,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 59,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 60,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 61,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 62,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 63,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 64,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 65,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 67,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 69,
          "witness_key": "claim:melt-migration-not-understood"
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
          "witness_key": "claim:melt-resides-fractionates"
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
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 76,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 77,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 78,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 79,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 80,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 81,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 82,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 83,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 84,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 85,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 88,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 89,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 90,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 91,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 92,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 93,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 94,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 95,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 96,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 97,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 98,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 99,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 100,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 116,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 117,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 118,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 119,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 120,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 121,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 122,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 123,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 124,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 125,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 126,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 127,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 128,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 129,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 130,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 131,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 132,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 133,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 134,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 135,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 136,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 137,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 138,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 139,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 140,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 141,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 142,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 143,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 144,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 145,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 146,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 147,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 148,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 149,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 150,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 151,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 152,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 153,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 154,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 155,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 156,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 157,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 158,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 159,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 160,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 161,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 162,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 163,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 164,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 165,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 166,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 167,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 168,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 169,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 170,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 171,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 172,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 173,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 174,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 175,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 176,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 177,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 178,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 179,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 180,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 181,
          "witness_key": "rel:rc3-adjacent-ntd2"
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
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 185,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 186,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 187,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 188,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 189,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 190,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 191,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 192,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 193,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 194,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 195,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 196,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 197,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 198,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 199,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 200,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 201,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 202,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 203,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 204,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 205,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 206,
          "witness_key": "claim:ntd2-bdb-normal"
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
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 212,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 213,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 214,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 215,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 216,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 217,
          "witness_key": "claim:volatiles-reduce-solidus"
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
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 221,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 232,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 233,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 234,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 235,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 236,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 237,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 238,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 239,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 241,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 242,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 243,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 244,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 245,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 246,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 247,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 248,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 249,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 251,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 252,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 253,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 254,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 255,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 256,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 257,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 259,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 260,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 261,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 262,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 263,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 264,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 265,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 266,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 267,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 268,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 269,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 270,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 271,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 272,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 273,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 274,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 275,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 276,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 277,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-T3-05",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The pressure, the equivalent depth and the temperature each come back on a row of their own; whose model produces them does not, although the model itself is a returned row.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "saturation_pressure",
          "row_index": 191,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "saturation_depth",
          "row_index": 190,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "saturation_temperature",
          "row_index": 192,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "solubility_model_source",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "A row names the model itself, but the question asks whose it is and no returned field or relation carries that; the reading attributes it by citation number only and no gap declares the omission."
        }
      ],
      "source_locators": [
        "page:5:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:cross-correlation"
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
          "witness_key": "method:first-motion"
        },
        {
          "row_index": 5,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 6,
          "witness_key": "method:location-criteria"
        },
        {
          "row_index": 7,
          "witness_key": "method:ml-formula"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 10,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 11,
          "witness_key": "method:swave-delay-removal"
        },
        {
          "row_index": 12,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 13,
          "witness_key": "model:co2-solubility"
        },
        {
          "row_index": 14,
          "witness_key": "model:iacono-marziano"
        },
        {
          "row_index": 15,
          "witness_key": "model:min-1d"
        },
        {
          "row_index": 16,
          "witness_key": "model:thermal"
        },
        {
          "row_index": 17,
          "witness_key": "model:thermal-simulated"
        },
        {
          "row_index": 18,
          "witness_key": "model:velocity-1d"
        },
        {
          "row_index": 19,
          "witness_key": "model:velocity-model-1"
        },
        {
          "row_index": 20,
          "witness_key": "model:velocity-model-5"
        },
        {
          "row_index": 21,
          "witness_key": "work:article"
        },
        {
          "row_index": 22,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 23,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 24,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 96,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 97,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 98,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 99,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 100,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 101,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 102,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 103,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 104,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 105,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 106,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 107,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 108,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 109,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 110,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 111,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 112,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 113,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 114,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 115,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 116,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 117,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 118,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 119,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 120,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 121,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 122,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 123,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 124,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 125,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 126,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 127,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 128,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 129,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 130,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 131,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 132,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 133,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 134,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 135,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 136,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 137,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 138,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 139,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 140,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 141,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 142,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 143,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 144,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 145,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 146,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 147,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 148,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 149,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 150,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 151,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 152,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 153,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 154,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 155,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 156,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 157,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 158,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 159,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 160,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 161,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 162,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 163,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 164,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 165,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 166,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 167,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 168,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 169,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 170,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 171,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 172,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 173,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 174,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 175,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 176,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 177,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 178,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 179,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 184,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 185,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 186,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 187,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 188,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 189,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 190,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 191,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 192,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 193,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 194,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 195,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 196,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 197,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 198,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 199,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 200,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 201,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 202,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 203,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 204,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 206,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 207,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 208,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 209,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 210,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 211,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 212,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 213,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 214,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 215,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 216,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 217,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 218,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 219,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 220,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 221,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 222,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 223,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 224,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 226,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 227,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 228,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 229,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 230,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 231,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 232,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 233,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 234,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 235,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 236,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 237,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 238,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 239,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 240,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 241,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 242,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 243,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 244,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 245,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 246,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 247,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 248,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 249,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 250,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 251,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 252,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 253,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 254,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 255,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 256,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 257,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 258,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 259,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 260,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 261,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 262,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 263,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 264,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 265,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 266,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 267,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 268,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 269,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 270,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 271,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 272,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 273,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 274,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 275,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 276,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 277,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 278,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 279,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 280,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 281,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 282,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 283,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 284,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 285,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 286,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 287,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 288,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 289,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 290,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 291,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 292,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 293,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 294,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 295,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 296,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 297,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 298,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 299,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 300,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 301,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 302,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 303,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 304,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 305,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 306,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 307,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 308,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 309,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 310,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 311,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 312,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 313,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 314,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 315,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 316,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 317,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 318,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 319,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 320,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 321,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 322,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 323,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 324,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 325,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 326,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 327,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 328,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 329,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 330,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 331,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 332,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 333,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 334,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 335,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 336,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 337,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 338,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-B-T4-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The preferred account, the wording that marks it as preferred and the physical process it rests on all come back; how many rivals were weighed is nowhere counted.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "preferred_mechanism",
          "row_index": 177,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "alternative_count",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The reading introduces the rival accounts with ordinal words and never counts them; the contract carries a count type, no returned record holds such a count, and no gap declares it."
        },
        {
          "semantic": "preference_wording",
          "row_index": 177,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "mechanism_physical_basis",
          "row_index": 49,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002",
        "page:5:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 33,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 35,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 36,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 37,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 38,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 39,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 40,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 42,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 43,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 45,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 46,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 48,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 49,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 50,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 52,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 53,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 55,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 56,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 57,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 58,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 62,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 63,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 69,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 71,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 72,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 73,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 74,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 75,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 76,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 77,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 79,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 80,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 84,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 85,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 86,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 88,
          "witness_key": "claim:tf-deep-eq-mylonite"
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
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 92,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 112,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 113,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 114,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 115,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 116,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 120,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 122,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 123,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 124,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 125,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 126,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 127,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 128,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 129,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 130,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 131,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 132,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 133,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 134,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 135,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 136,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 137,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 138,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 139,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 140,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 141,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 142,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 143,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 144,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 145,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 147,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 148,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 149,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 150,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 151,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 153,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 159,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 160,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 161,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 162,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 163,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 164,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 165,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 167,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 168,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 169,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 170,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 171,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 174,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 175,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 176,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 177,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 178,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 179,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 180,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 181,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 182,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 183,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 184,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 185,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 186,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 187,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 188,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 189,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 190,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 191,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 192,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 193,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 194,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 195,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 196,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 197,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 198,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 199,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 200,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 201,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 202,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 203,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 204,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 205,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 206,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 207,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 208,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 209,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 210,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 212,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 213,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 214,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 232,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 234,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 235,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 238,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 239,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 241,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 242,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 244,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 248,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 249,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 250,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 253,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 254,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 255,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 256,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 260,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 261,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 262,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 263,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 264,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 265,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 266,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 267,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 268,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 269,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 270,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-T4-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four come back: the declined account with its disposition, the magmatic origin that is given against it, the ridge the seafloor is contrasted with, and a measurement of the valley's shape.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "declined_explanation",
          "row_index": 188,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "rejection_evidence",
          "row_index": 202,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "comparison_setting",
          "row_index": 31,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "morphology_observation",
          "row_index": 259,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:001",
        "page:3:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 33,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 35,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 36,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 37,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 38,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 39,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 40,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 42,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 43,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 45,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 46,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 48,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 49,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 50,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 52,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 53,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 55,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 56,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 57,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 58,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 62,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 63,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 69,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 71,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 72,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 73,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 74,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 75,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 76,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 77,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 79,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 80,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 84,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 85,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 86,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 88,
          "witness_key": "claim:tf-deep-eq-mylonite"
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
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 92,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 112,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 113,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 114,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 115,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 116,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 120,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 122,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 123,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 124,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 125,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 126,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 127,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 128,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 129,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 130,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 131,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 132,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 133,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 134,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 135,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 136,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 137,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 138,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 139,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 140,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 141,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 142,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 143,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 144,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 145,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 147,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 148,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 149,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 150,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 151,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 153,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 159,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 160,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 161,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 162,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 163,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 164,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 165,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 167,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 168,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 169,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 170,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 171,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 174,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 175,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 176,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 177,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 178,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 179,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 180,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 181,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 182,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 183,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 184,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 185,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 186,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 187,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 188,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 189,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 190,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 191,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 192,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 193,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 194,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 195,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 196,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 197,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 198,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 199,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 200,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 201,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 202,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 203,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 204,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 205,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 206,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 207,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 208,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 209,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 210,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 212,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 213,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 214,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 232,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 234,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 235,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 238,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 239,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 241,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 242,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 244,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 248,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 249,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 250,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 253,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 254,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 255,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 256,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 260,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 261,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 262,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 263,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 264,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 265,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 266,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 267,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 268,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 269,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 270,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-T4-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four come back: the declined account, the absence of active vents that is given against it, the extinct field that is conceded, and the distance qualifier that comes with the concession.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "declined_explanation",
          "row_index": 188,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "rejection_evidence",
          "row_index": 197,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "conceded_observation",
          "row_index": 183,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "spatial_qualification",
          "row_index": 183,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:3:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 33,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 35,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 36,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 37,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 38,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 39,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 42,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 43,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 45,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 46,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 48,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 49,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 50,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 52,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 53,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 55,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 56,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 57,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 58,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 62,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 63,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 68,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 69,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 71,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 72,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 73,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 74,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 75,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 76,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 77,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 78,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 79,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 80,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 81,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 84,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 85,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 88,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 89,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 90,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 91,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 92,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 95,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 96,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 111,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 112,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 113,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 114,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 115,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 116,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 120,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 122,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 123,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 124,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 125,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 126,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 127,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 128,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 129,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 130,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 131,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 132,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 133,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 134,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 135,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 136,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 137,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 138,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 139,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 140,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 141,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 142,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 143,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 144,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 145,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 146,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 147,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 148,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 149,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 150,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 151,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-tick-interval"
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
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 159,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 160,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 161,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 162,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 163,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 164,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 165,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 167,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 168,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 169,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 170,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 171,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 174,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 175,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 176,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 177,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 178,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 179,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 180,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 181,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 182,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 183,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 184,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 185,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 186,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 187,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 188,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 189,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 190,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 191,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 192,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 193,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 194,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 195,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 196,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 197,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 198,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 199,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 200,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 201,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 202,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 203,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 204,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 205,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 206,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 207,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 209,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 210,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 212,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 213,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 214,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 231,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 232,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 233,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 234,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 235,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 238,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 239,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 240,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 241,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 242,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 244,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 247,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 248,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 249,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 250,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 253,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 254,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 255,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 256,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 260,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 261,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 262,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 263,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 264,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 265,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 266,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 267,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 268,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 269,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-T4-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four come back: the hedged reading of the events, the spectral observation behind it, and the limitation and the future requirement, which share one row.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "hedged_claim",
          "row_index": 24,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "supporting_observation",
          "row_index": 106,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "stated_limitation",
          "row_index": 37,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "future_requirement",
          "row_index": 37,
          "absent_reason": null,
          "note": ""
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
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 2,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 3,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 4,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 5,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 6,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 7,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 8,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 9,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 10,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 11,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 12,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 13,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 14,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 15,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 16,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 17,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 18,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 19,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 20,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 21,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 22,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 23,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 24,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 25,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 26,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 27,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 28,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 29,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 30,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 31,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 32,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 33,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 34,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 35,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 36,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 37,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 38,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 39,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 40,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 41,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 42,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 43,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 44,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 45,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 46,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 47,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 48,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 49,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 50,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 51,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 52,
          "witness_key": "claim:shiptime-funded"
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
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 56,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 57,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 58,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 59,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 60,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 61,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 62,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 63,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 64,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 65,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 66,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 67,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 68,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 70,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 71,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 72,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 73,
          "witness_key": "cnt:relocation-iterations"
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
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 80,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 81,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 82,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 83,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 84,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 85,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 86,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 87,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 88,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 89,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 90,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 91,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 92,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 93,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 94,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 95,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 96,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 97,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 98,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 99,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 100,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 101,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 102,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 103,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 104,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 105,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 106,
          "witness_key": "obs:high-frequency-threshold"
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
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 110,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 111,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 112,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 113,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 114,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 115,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 116,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 117,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 118,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 119,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 120,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 121,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 122,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 123,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 124,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 125,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 126,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 127,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 128,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 129,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 130,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 131,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 132,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 133,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 134,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 135,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 136,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 137,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 138,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 139,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 140,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 141,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 142,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 143,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 144,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 145,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 146,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 147,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 148,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 149,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 150,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 151,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 152,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 153,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 154,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 155,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 156,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 157,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 158,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 159,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 160,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 161,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 162,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 163,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 164,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 165,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 166,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 167,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 168,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 169,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 170,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 171,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 172,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 173,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 174,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 175,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 176,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 177,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 178,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 179,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 184,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 186,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 187,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 188,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 189,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 190,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 191,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 192,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 193,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 194,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 195,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 196,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 197,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 198,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 199,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 200,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 201,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 202,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 203,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 204,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 205,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 206,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 207,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 208,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 209,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 210,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 211,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 212,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 213,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 214,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 215,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 216,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 217,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 218,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 219,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 220,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 221,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 222,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 223,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 224,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 225,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 226,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 227,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 228,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 229,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 230,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 231,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 232,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 233,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-B-T4-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All five come back: the assumption and the way it is flagged on one row, and the lower bound with its unit and its segment on another.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "method_assumption",
          "row_index": 106,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "caveat_wording",
          "row_index": 106,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "asserted_minimum",
          "row_index": 240,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "concentration_unit",
          "row_index": 240,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "segment_label",
          "row_index": 240,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "method:cross-correlation"
        },
        {
          "row_index": 33,
          "witness_key": "method:depth-resolution-tests"
        },
        {
          "row_index": 34,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 35,
          "witness_key": "method:fc-correction"
        },
        {
          "row_index": 36,
          "witness_key": "method:first-motion"
        },
        {
          "row_index": 37,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 38,
          "witness_key": "method:location-criteria"
        },
        {
          "row_index": 39,
          "witness_key": "method:ml-formula"
        },
        {
          "row_index": 40,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 41,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 42,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 43,
          "witness_key": "method:swave-delay-removal"
        },
        {
          "row_index": 44,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 45,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 46,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 47,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 48,
          "witness_key": "sample:morb-rc3"
        },
        {
          "row_index": 49,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 50,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 51,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 52,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 53,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 55,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 56,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 57,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 58,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 60,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 61,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 62,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 63,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 64,
          "witness_key": "claim:deeper-eq-observed"
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
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 68,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 69,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 70,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 71,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 72,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 73,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 74,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 75,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 76,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 77,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 78,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 79,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 80,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 81,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 82,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 83,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 84,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 85,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 86,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 88,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 89,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 90,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 91,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 92,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 93,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 94,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 95,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 96,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 97,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 98,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 99,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 100,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 101,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 102,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 103,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 104,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 105,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 106,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 107,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 108,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 109,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 110,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 111,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 112,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 113,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:final-located"
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
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 121,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 122,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 123,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 124,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 125,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 126,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 127,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 128,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 129,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 130,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 131,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 132,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 133,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 134,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 135,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 136,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 137,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 138,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 139,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 140,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 141,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 142,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 143,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 144,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 145,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 146,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 147,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 148,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 149,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 150,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 151,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 152,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 153,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 154,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 156,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 157,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 158,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 159,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 160,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 161,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 162,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 163,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 164,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 165,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 166,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 167,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 168,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 169,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 170,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 171,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 172,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 173,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 174,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 175,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 176,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 177,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 178,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 179,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 180,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 181,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 182,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 183,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 184,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 185,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 186,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 187,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 188,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 189,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 190,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 191,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 192,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 193,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 194,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 195,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 196,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 197,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 198,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 199,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 200,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 201,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 202,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 203,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 204,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 205,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 206,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 207,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 208,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 209,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 210,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 211,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 212,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 213,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 214,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 215,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 216,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 217,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 218,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 219,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 220,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 221,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 222,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 223,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 224,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 225,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 226,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 227,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 228,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 229,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 230,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 231,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 232,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 233,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 234,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 235,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 236,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 237,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 238,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 239,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 240,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 241,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 242,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 243,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 244,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 245,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 246,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 247,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 248,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 249,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 250,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 251,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 252,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 253,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 254,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 255,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 256,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 257,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 258,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 259,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 260,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 261,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 262,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 263,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 264,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 265,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 266,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 267,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 268,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 269,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 270,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 271,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 272,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 273,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 274,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 275,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 276,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 277,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 278,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 279,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 280,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 281,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 282,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 283,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 284,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 285,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 286,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 287,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 288,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 289,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 290,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-T5-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four come back: the expected bound, the depths actually recorded beneath the segment, the rate the bound is derived from, and the segment label on the observation row.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "expected_depth_bound",
          "row_index": 151,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "observed_depth_range",
          "row_index": 236,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "spreading_rate_basis",
          "row_index": 136,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "segment_label",
          "row_index": 236,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:005",
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 33,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 35,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 36,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 37,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 38,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 39,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 40,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 42,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 43,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 45,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 46,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 48,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 49,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 50,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 52,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 53,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 55,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 56,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 57,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 58,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 62,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 63,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 69,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 71,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 72,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 73,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 74,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 75,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 76,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 77,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 79,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 80,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 84,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 85,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 86,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 88,
          "witness_key": "claim:tf-deep-eq-mylonite"
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
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 92,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 112,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 113,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 114,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 115,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 116,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 120,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 122,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 123,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 124,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 125,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 126,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 127,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 128,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 129,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 130,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 131,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 132,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 133,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 134,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 135,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 136,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 137,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 138,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 139,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 140,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 141,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 142,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 143,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 144,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 145,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 147,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 148,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 149,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 150,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 151,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 153,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 159,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 160,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 161,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 162,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 163,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 164,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 165,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 167,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 168,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 169,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 170,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 171,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 174,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 175,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 176,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 177,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 178,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 179,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 180,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 181,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 182,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 183,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 184,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 185,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 186,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 187,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 188,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 189,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 190,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 191,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 192,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 193,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 194,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 195,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 196,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 197,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 198,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 199,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 200,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 201,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 202,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 203,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 204,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 205,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 206,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 207,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 208,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 209,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 210,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 212,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 213,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 214,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 232,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 234,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 235,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 238,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 239,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 241,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 242,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 244,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 248,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 249,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 250,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 253,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 254,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 255,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 256,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 260,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 261,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 262,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 263,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 264,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 265,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 266,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 267,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 268,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 269,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 270,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-T5-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All five come back: the thickness with its stated error on one row, the observed depths on another, and the inference and the hosting layer on a third.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "crustal_thickness_value",
          "row_index": 209,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "thickness_uncertainty",
          "row_index": 209,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "observed_depth_range",
          "row_index": 321,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "depth_inference",
          "row_index": 134,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "hosting_layer",
          "row_index": 134,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "work:article"
        },
        {
          "row_index": 33,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 34,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 35,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 96,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 97,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 98,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 99,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 100,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 101,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 102,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 103,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 104,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 105,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 106,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 107,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 108,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 109,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 110,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 111,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 112,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 113,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 114,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 115,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 116,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 117,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 118,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 119,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 120,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 121,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 122,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 123,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 124,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 125,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 126,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 127,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 128,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 129,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 130,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 131,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 132,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 133,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 134,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 135,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 136,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 137,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 138,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 139,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 140,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 141,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 142,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 143,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 144,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 145,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 146,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 147,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 148,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 149,
          "witness_key": "claim:melt-migration-not-understood"
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
          "witness_key": "claim:melt-resides-fractionates"
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
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 156,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 157,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 158,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 159,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 160,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 161,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 162,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 163,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 164,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 165,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 166,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 167,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 168,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 169,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 170,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 171,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 172,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 173,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 174,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 175,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 176,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 177,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 178,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 179,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 180,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 184,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 186,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 187,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 188,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 189,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 190,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 191,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 192,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 193,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 194,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 195,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 196,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 197,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 198,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 199,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 200,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 201,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 202,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 203,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 204,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 205,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 206,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 207,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 208,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 209,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 210,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 211,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 212,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 213,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 214,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 215,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 216,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 217,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 218,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 219,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 220,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 221,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 222,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 223,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 224,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 225,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 226,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 227,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 228,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 229,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 230,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 231,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 232,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 233,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 237,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 238,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 239,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 240,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 241,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 242,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 243,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 244,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 245,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 246,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 247,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 248,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 249,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 250,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 251,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 252,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 253,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 254,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 255,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 256,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 257,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 258,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 259,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 260,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 261,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 262,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 263,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 264,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 265,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 266,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 267,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 268,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 269,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 270,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 271,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 272,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 273,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 274,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 275,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 276,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 277,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 278,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 279,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 280,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 281,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 282,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 283,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 284,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 285,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 286,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 287,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 288,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 289,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 290,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 291,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 292,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 293,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 294,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 295,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 296,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 297,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 298,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 299,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 300,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 301,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 302,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 303,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 304,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 305,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 306,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 307,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 308,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 309,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 310,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 311,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 312,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 313,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 314,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 315,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 316,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 317,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 318,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 319,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 320,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 321,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 322,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 323,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 324,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 325,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 326,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 327,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 328,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 329,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 330,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 331,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 332,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 333,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 334,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 335,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 336,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 337,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 338,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 339,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 340,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 341,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 342,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 343,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 344,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 345,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 346,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 347,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 348,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 349,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 350,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 351,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 352,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 353,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 354,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 355,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-T5-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four come back: this study's range with its unit, and the earlier maximum with the ridge it was reported at.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "concentration_range",
          "row_index": 309,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "prior_maximum_value",
          "row_index": 321,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "prior_maximum_location",
          "row_index": 321,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "concentration_unit",
          "row_index": 309,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:009",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "work:article"
        },
        {
          "row_index": 33,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 34,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 35,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 96,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 97,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 98,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 99,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 100,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 101,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 102,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 103,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 104,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 105,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 106,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 107,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 108,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 109,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 110,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 111,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 112,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 113,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 114,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 115,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 116,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 117,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 118,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 119,
          "witness_key": "sample:morb-rc3"
        },
        {
          "row_index": 120,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 121,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 122,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 123,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 124,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 125,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 126,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 127,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 128,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 129,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 130,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 131,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 132,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 133,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 134,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 135,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 136,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 137,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 138,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 139,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 140,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 141,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 142,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 143,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 144,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 145,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 146,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 147,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 148,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 149,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 150,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 151,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 152,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 153,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 154,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 155,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 156,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 157,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 158,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 159,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 160,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 161,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 162,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 163,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 164,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 165,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 166,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 167,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 168,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 169,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 170,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 171,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 172,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 173,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 174,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 175,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 176,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 177,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 178,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 179,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 180,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 181,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 182,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 183,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 184,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 186,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 187,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 188,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 189,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 190,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 191,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 192,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 193,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 194,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 195,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 196,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 197,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 198,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 199,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 200,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 201,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 202,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 203,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 204,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 205,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 206,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 207,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 208,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 209,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 210,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 211,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 212,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 213,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 214,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 215,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 216,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 217,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 218,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 219,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 220,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 221,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 222,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 223,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 224,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 225,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 226,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 227,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 228,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 229,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 230,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 231,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 232,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 233,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 234,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 235,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 237,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 238,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 239,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 241,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 242,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 243,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 244,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 245,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 246,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 247,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 248,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 249,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 250,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 251,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 252,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 253,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 254,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 255,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 256,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 257,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 258,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 259,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 260,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 261,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 262,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 263,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 264,
          "witness_key": "rel:morb-from-petdb"
        },
        {
          "row_index": 265,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 266,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 267,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 268,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 269,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 270,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 271,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 272,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 273,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 274,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 275,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 276,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 277,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 278,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 279,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 280,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 281,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 282,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 283,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 284,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 285,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 286,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 287,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 288,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 289,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 290,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 291,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 292,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 293,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 294,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 295,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 296,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 297,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 298,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 299,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 300,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 301,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 302,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 303,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 304,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 305,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 306,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 307,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 308,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 309,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 310,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 311,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 312,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 313,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 314,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 315,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 316,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 317,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 318,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 319,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 320,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 321,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 322,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 323,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 324,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 325,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 326,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 327,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 328,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 329,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 330,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 331,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 332,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 333,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 334,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 335,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 336,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 337,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 338,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 339,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 340,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 341,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 342,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 343,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 344,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 345,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 346,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 347,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 348,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 349,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 350,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 351,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 352,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 353,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 354,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 355,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 356,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 357,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 358,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 359,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 360,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-T5-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four come back: the modelled temperature range, the depth below which nothing is observed, the explanation offered for that, and the model the temperatures come from.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "modelled_temperature_range",
          "row_index": 326,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "depth_cutoff",
          "row_index": 312,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "absence_explanation",
          "row_index": 250,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "thermal_model_source",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:3:block:001",
        "page:5:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "model:co2-solubility"
        },
        {
          "row_index": 1,
          "witness_key": "model:iacono-marziano"
        },
        {
          "row_index": 2,
          "witness_key": "model:min-1d"
        },
        {
          "row_index": 3,
          "witness_key": "model:thermal"
        },
        {
          "row_index": 4,
          "witness_key": "model:thermal-simulated"
        },
        {
          "row_index": 5,
          "witness_key": "model:velocity-1d"
        },
        {
          "row_index": 6,
          "witness_key": "model:velocity-model-1"
        },
        {
          "row_index": 7,
          "witness_key": "model:velocity-model-5"
        },
        {
          "row_index": 8,
          "witness_key": "work:article"
        },
        {
          "row_index": 9,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 10,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 11,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 12,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 13,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 14,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 15,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 16,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 91,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 92,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 93,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 94,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 95,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 96,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 97,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 98,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 99,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 100,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 101,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 102,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 103,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 104,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 105,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 106,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 107,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 108,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 109,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 110,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 111,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 112,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 113,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 114,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 115,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 116,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 117,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 118,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 119,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 120,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 121,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 122,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 123,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 124,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 125,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 126,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 127,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 128,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 129,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 130,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 131,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 132,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 133,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 134,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 135,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 136,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 137,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 138,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 139,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 140,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 141,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 142,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 143,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 144,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 145,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 146,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 147,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 148,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 149,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 150,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 151,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 152,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 153,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 154,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 155,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 156,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 157,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 158,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 159,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 160,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 161,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 162,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 163,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 164,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 165,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 166,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 167,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 168,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 169,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 170,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 171,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 172,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 173,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 174,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 175,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 176,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 177,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 178,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 179,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 180,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 181,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 182,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 183,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 184,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 185,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 186,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 187,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 188,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 189,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 190,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 191,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 192,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 193,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 194,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 195,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 196,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 197,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 198,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 199,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 200,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 201,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 202,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 203,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 204,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 205,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 206,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 207,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 208,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 209,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 210,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 211,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 212,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 213,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 214,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 215,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 216,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 217,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 218,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 219,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 220,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 221,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 222,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 223,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 224,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 225,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 226,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 227,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 228,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 229,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 230,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 231,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 232,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 233,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 234,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 235,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 236,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 237,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 238,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 239,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 240,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 241,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 242,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 243,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 244,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 245,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 246,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 247,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 248,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 249,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 250,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 251,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 252,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 253,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 254,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 255,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 256,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 257,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 258,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 259,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 260,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 261,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 262,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 263,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 264,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 265,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 266,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 267,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 268,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 269,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 270,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 271,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 272,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 273,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 274,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 275,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 276,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 277,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 278,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 279,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 280,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 281,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 282,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 283,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 284,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 285,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 286,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 287,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 288,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 289,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 290,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 291,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 292,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 293,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 294,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 295,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 296,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 297,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 298,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 299,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 300,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 301,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 302,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 303,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 304,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 305,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 306,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 307,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 308,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 309,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 310,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 311,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 312,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 313,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 314,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 315,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 316,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 317,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 318,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 319,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 320,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 321,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 322,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 323,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 324,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 325,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 326,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-B-T5-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four come back: the trace-element floor for the segment with the deep events, the estimated range and its segment, and the same estimate for the segment to the south.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "trace_element_threshold",
          "row_index": 232,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "concentration_range",
          "row_index": 226,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "segment_label",
          "row_index": 226,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "comparison_segment_label",
          "row_index": 234,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 33,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 34,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 35,
          "witness_key": "sample:morb-rc3"
        },
        {
          "row_index": 36,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 37,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 38,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 39,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 41,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 42,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 43,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 44,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 45,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 46,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 47,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 48,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 49,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 50,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 51,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 53,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 54,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 55,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 56,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 57,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 58,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 59,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 60,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 61,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 62,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 63,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 64,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 65,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 67,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 69,
          "witness_key": "claim:melt-migration-not-understood"
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
          "witness_key": "claim:melt-resides-fractionates"
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
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 76,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 77,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 78,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 79,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 80,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 81,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 82,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 83,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 84,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 85,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 88,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 89,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 90,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 91,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 92,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 93,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 94,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 95,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 96,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 97,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 98,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 99,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 100,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 116,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 117,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 118,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 119,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 120,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 121,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 122,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 123,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 124,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 125,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 126,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 127,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 128,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 129,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 130,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 131,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 132,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 133,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 134,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 135,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 136,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 137,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 138,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 139,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 140,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 141,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 142,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 143,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 144,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 145,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 146,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 147,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 148,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 149,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 150,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 151,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 152,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 153,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 154,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 155,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 156,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 157,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 158,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 159,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 160,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 161,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 162,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 163,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 164,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 165,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 166,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 167,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 168,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 169,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 170,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 171,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 172,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 173,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 174,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 175,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 176,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 177,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 178,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 179,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 180,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 181,
          "witness_key": "rel:rc3-adjacent-ntd2"
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
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 185,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 186,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 187,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 188,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 189,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 190,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 191,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 192,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 193,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 194,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 195,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 196,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 197,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 198,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 199,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 200,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 201,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 202,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 203,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 204,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 205,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 206,
          "witness_key": "claim:ntd2-bdb-normal"
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
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 212,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 213,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 214,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 215,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 216,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 217,
          "witness_key": "claim:volatiles-reduce-solidus"
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
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 221,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 232,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 233,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 234,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 235,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 236,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 237,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 238,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 239,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 241,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 242,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 243,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 244,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 245,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 246,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 247,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 248,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 249,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 251,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 252,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 253,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 254,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 255,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 256,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 257,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 259,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 260,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 261,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 262,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 263,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 264,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 265,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 266,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 267,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 268,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 269,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 270,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 271,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 272,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 273,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 274,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 275,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 276,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 277,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-C-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Only the number of instruments comes back. The reading states no sampling rate, no sensor kind and no other setting of the instruments, so three of the four elements have nothing behind them.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "sampling_rate_value",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading nowhere states a sampling rate for the seafloor instruments."
        },
        {
          "semantic": "sensor_type",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading names the instruments by their kind of platform and never says what sensor they carry."
        },
        {
          "semantic": "instrument_configuration_detail",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading gives the deployment geometry and the recording span; it states no setting of the instruments themselves."
        },
        {
          "semantic": "instrument_count",
          "row_index": 76,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "cruise:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instr:obs"
        },
        {
          "row_index": 2,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 3,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 4,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 5,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 6,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 7,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 8,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 9,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 17,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 18,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 19,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 20,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 21,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 22,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 23,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 24,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 25,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 26,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 27,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 28,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 29,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 30,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 31,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 32,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 33,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 34,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 35,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 36,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 37,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 38,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 39,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 40,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 41,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 42,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 43,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 44,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 45,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 46,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 47,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 48,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 49,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 50,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 51,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 52,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 53,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 54,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 55,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 56,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 57,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 58,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 59,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 60,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 61,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 62,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 63,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 64,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 65,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 66,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 67,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 68,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 69,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 70,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 71,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 72,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 73,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 74,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 82,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 83,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 84,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 85,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 86,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 87,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 88,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 89,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 90,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 91,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 92,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 93,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 94,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 95,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 96,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 97,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 98,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 99,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 100,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 101,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 102,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 103,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 105,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 106,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 108,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 109,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 110,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 111,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 112,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 113,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 114,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 115,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 116,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 117,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 118,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 119,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 120,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 121,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 122,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 124,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 125,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 126,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 127,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 128,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 129,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-B-C-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The magnitude scale comes back. The largest magnitude recorded and the event that carried it are not in the reading at all, and the record that would give the recording span is outside this question's cases.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "maximum_magnitude_value",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading gives the completeness magnitude and the b value of the catalogue and never the largest local magnitude among the events recorded."
        },
        {
          "semantic": "magnitude_scale",
          "row_index": 7,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "event_identification",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "No event of this deployment is identified in the reading; the one event it names by magnitude belongs to an earlier year and to a different subject."
        },
        {
          "semantic": "recording_period",
          "row_index": null,
          "absent_reason": "UNREACHED_RECORD",
          "note": "A record does carry the span over which the instruments recorded, and this question's cases do not return it."
        }
      ],
      "source_locators": [
        "page:8:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:cross-correlation"
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
          "witness_key": "method:first-motion"
        },
        {
          "row_index": 5,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 6,
          "witness_key": "method:location-criteria"
        },
        {
          "row_index": 7,
          "witness_key": "method:ml-formula"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 10,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 11,
          "witness_key": "method:swave-delay-removal"
        },
        {
          "row_index": 12,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 13,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 14,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 15,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 16,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 17,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 18,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 19,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 20,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 21,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 22,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 23,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 24,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 25,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 26,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 27,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 28,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 29,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 30,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 31,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 32,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 33,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 34,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 35,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 36,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 37,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 38,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 39,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 40,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 41,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 42,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 43,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 44,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 45,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 46,
          "witness_key": "claim:melt-migration-not-understood"
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
          "witness_key": "claim:melt-resides-fractionates"
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
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 53,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 54,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 55,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 56,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 57,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 58,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 59,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 60,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 61,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 62,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 63,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 64,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 65,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 66,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 67,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 68,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 69,
          "witness_key": "claim:tf-deep-eq-mylonite"
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
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 73,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 74,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 75,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 76,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 77,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:identified-earthquakes"
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
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 84,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 86,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 87,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 88,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 91,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 92,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 93,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 94,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 95,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 96,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 97,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 98,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 99,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 100,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 101,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 102,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 103,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 104,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 105,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 106,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 107,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 108,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 109,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 110,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 111,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 112,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 113,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 114,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 115,
          "witness_key": "obs:focal-selection-criteria"
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
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 120,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 121,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 122,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 123,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 124,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 125,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 126,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 128,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 129,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 130,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 131,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 132,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 133,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 134,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 135,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 136,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 137,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 138,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 139,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 140,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 141,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 142,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 143,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 144,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 145,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 146,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 147,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 148,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 149,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 150,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 151,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 152,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 153,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 154,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 155,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 156,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 157,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 158,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 159,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 160,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 161,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 162,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 163,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 164,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 165,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 166,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 167,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 168,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 169,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 170,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 171,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 172,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 173,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 174,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 175,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 176,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 177,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 178,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 179,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 180,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 181,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 182,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 183,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 184,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 185,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 186,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 187,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 188,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 189,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 190,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 191,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 192,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 193,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 194,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 195,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 196,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 197,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 198,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 199,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 200,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 201,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 202,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 203,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 204,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 205,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 206,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 207,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 208,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 209,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 210,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 211,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 212,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 213,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 214,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 216,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 217,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 218,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 219,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 220,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 221,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 222,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 223,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 224,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 225,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 226,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 227,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 228,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 229,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 230,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 231,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 232,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 233,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 234,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 235,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 236,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 237,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 238,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 239,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 241,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 242,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 243,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 244,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 245,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 246,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-B-C-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "A site of the compilation comes back by name. The depth, the rate and the unit that would go with each site live in a supplementary table the reading does not carry.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "site_name",
          "row_index": 24,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "maximum_depth_value",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The per-site depths of that compilation sit in a supplementary table the reading does not carry; no returned row gives a maximum depth for any site of it."
        },
        {
          "semantic": "full_rate_value",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The per-site opening rates sit in the same table; the one rate returned belongs to the studied segment and is stated there to predict that segment's own maximum depth."
        },
        {
          "semantic": "depth_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "No depth is given for any site of the compilation, so no unit for one is given either."
        }
      ],
      "source_locators": [
        "page:8:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "work:article"
        },
        {
          "row_index": 33,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 34,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 35,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 96,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 97,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 98,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 99,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 100,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 101,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 102,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 103,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 104,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 105,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 106,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 107,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 108,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 109,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 110,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 111,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 112,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 113,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 114,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 115,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 116,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 117,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 118,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 119,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 120,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 121,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 122,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 123,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 124,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 125,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 126,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 127,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 128,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 129,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 130,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 132,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 133,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 134,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 135,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 136,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 137,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 138,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 139,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 140,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 141,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 142,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 143,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 144,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 145,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 146,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 147,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 148,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 149,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 150,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 151,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 152,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 153,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 154,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 155,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 156,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 157,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 158,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 159,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 160,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 161,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 162,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 163,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 164,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 165,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 166,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 167,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 168,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 169,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 170,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 171,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 172,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 173,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 174,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 175,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 176,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 177,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 178,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 179,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 184,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 186,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 187,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 188,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 189,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 190,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 191,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 192,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 193,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 194,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 195,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 196,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 197,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 198,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 199,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 200,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 201,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 202,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 203,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 204,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 205,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 206,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 207,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 208,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 209,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 210,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 211,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 212,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 213,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 214,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 215,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 216,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 217,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 218,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 219,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 220,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 221,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 222,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 223,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 224,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 225,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 226,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 227,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 228,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 229,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 230,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 231,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 232,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 237,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 238,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 239,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 240,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 241,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 242,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 243,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 244,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 245,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 246,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 248,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 249,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 251,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 252,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 253,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 254,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 255,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 256,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 257,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 258,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 259,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 260,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 261,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 262,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 263,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 264,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 265,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 266,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 267,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 268,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 269,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 270,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 271,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 272,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 273,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 274,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 275,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 276,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 277,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 278,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 279,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 280,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 281,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 282,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 283,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 284,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 285,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 286,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 287,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 288,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 289,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 290,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 291,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 292,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 293,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 294,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 295,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 296,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 297,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 298,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 299,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 300,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 301,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 302,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 303,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 304,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 305,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 306,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 307,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 308,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 309,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 310,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 311,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 312,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 313,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 314,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 315,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 316,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 317,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 318,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 319,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 320,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 321,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 322,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 323,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 324,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 325,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 326,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 327,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 328,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 329,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 330,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 331,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 332,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 333,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 334,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 335,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 336,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 337,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 338,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 339,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 340,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 341,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 342,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 343,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 344,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 345,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 346,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 347,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 348,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 349,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 350,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 351,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 352,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 353,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 354,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-B-C-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The expedition and the number of recording units each come back on a row; when it ran does not.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "cruise_name",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "deployment_year",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The reading states the year of the expedition in the results and again in the methods, and the contract carries year-valued fields on other types; no returned record or field holds a year for this expedition and the capture declares no gap for it."
        },
        {
          "semantic": "instrument_count",
          "row_index": 76,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:10:block:043",
        "page:10:block:046",
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "cruise:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instr:obs"
        },
        {
          "row_index": 2,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 3,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 4,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 5,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 6,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 7,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 8,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 9,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 17,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 18,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 19,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 20,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 21,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 22,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 23,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 24,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 25,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 26,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 27,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 28,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 29,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 30,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 31,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 32,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 33,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 34,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 35,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 36,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 37,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 38,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 39,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 40,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 41,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 42,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 43,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 44,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 45,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 46,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 47,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 48,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 49,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 50,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 51,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 52,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 53,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 54,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 55,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 56,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 57,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 58,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 59,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 60,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 61,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 62,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 63,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 64,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 65,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 66,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 67,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 68,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 69,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 70,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 71,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 72,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 73,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 74,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 82,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 83,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 84,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 85,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 86,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 87,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 88,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 89,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 90,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 91,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 92,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 93,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 94,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 95,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 96,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 97,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 98,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 99,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 100,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 101,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 102,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 103,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 105,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 106,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 108,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 109,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 110,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 111,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 112,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 113,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 114,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 115,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 116,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 117,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 118,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 119,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 120,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 121,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 122,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 124,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 125,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 126,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 127,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 128,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 129,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-B-C-05",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The chosen account, the wording that marks it as chosen and the physics behind it all come back; how many competitors were weighed is nowhere counted.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "preferred_mechanism",
          "row_index": 177,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "alternative_count",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The reading introduces the competing accounts with ordinal words and never counts them; the contract carries a count type, no returned record holds such a count, and no gap declares it."
        },
        {
          "semantic": "preference_wording",
          "row_index": 177,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "mechanism_physical_basis",
          "row_index": 49,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002",
        "page:5:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 33,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 35,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 36,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 37,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 38,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 39,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 40,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 42,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 43,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 45,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 46,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 48,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 49,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 50,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 52,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 53,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 55,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 56,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 57,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 58,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 62,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 63,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 69,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 71,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 72,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 73,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 74,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 75,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 76,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 77,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 79,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 80,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 84,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 85,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 86,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 88,
          "witness_key": "claim:tf-deep-eq-mylonite"
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
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 92,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 112,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 113,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 114,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 115,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 116,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 120,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 122,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 123,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 124,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 125,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 126,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 127,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 128,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 129,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 130,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 131,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 132,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 133,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 134,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 135,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 136,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 137,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 138,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 139,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 140,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 141,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 142,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 143,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 144,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 145,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 147,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 148,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 149,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 150,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 151,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 153,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 159,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 160,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 161,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 162,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 163,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 164,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 165,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 167,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 168,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 169,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 170,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 171,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 174,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 175,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 176,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 177,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 178,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 179,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 180,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 181,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 182,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 183,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 184,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 185,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 186,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 187,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 188,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 189,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 190,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 191,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 192,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 193,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 194,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 195,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 196,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 197,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 198,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 199,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 200,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 201,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 202,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 203,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 204,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 205,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 206,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 207,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 208,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 209,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 210,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 212,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 213,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 214,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 232,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 234,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 235,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 238,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 239,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 241,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 242,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 244,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 248,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 249,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 250,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 253,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 254,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 255,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 256,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 260,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 261,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 262,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 263,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 264,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 265,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 266,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 267,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 268,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 269,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 270,
          "witness_key": "cnt:useful-obs"
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

# Inspection-note capture fixture

A neutral conformance fixture for the document-assertion adapter and the
neutral population plan. Two consumers, one plan shape: a synthetic maintenance
inspection note (document source) and two Small Shop supplier-order rows
(structured source).

The inspection note, its LinkML ontology, its reading, its capture, and the
plan, change set and census derived from them are synthetic and authored for
Malleus. No paper, customer or private document enters this fixture. The Small
Shop members restate the plans and change set built from
`small_shop_fulfilment_correction_v1/input/sources/supplier-order-history.jsonl`;
no design decision assigns this fixture a fixture object id, and it carries no
protocol authority of its own.

## Source

Copied byte for byte from `handover/2026-09-03-core-population-v2/examples`,
which `handover/2026-09-03-core-population-v2/validate_examples.py` writes.
`manifest.json` pins every member by length and digest. The handover copy is
the spec's archived evidence: it is pinned by the overseer ledger, it is not
read by any test, and Core's tests read this directory instead.

## Members

- `reading.json`, `inspection-note.yaml`, `document-capture.json`: the document
  consumer's inputs.
- `document-plan.json`, `document-change.json`, `document-census.json`: the
  plan the adapter emits, its lowering, and the two-axis census.
- `small-shop-plan-e4.json`, `small-shop-plan-e7.json`,
  `small-shop-change-e7.json`: the row consumer's plans and the lowered
  correction.
- `profile-source-assertion.json`, `profile-state-version.json`: the shipped
  `malleus.domain-history-profile/private-v1` bytes each plan binds.

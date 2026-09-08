# Two partial shipments, one retained Shop history

This is a synthetic conformance extension, not more data from the retailer
paper. Order `SYN-PS-ORDER` contains two distinct units. Shipment `SYN-S1`
carries the first; `SYN-S2` carries the second. Their tracking IDs stay distinct.
No domain date is stated, so the plans use `NONE_STATED`.

Run the existing complete default Shop first. Admit the synthetic order under
that existing ontology. Add Shipment vocabulary through one additive contract
revision, then admit each shipment with its order and unit relations. Reopen
from the ledger alone, query the remaining unit after each stage, and trace
both shipments to exact retained source rows. Previous Shop records and the
original ledger prefix must remain intact.

`expected.json` is the independently authored answer key. The runner must not
read it. This exercises the existing public compiler, state-version profile,
structural admission, revision, query and trace. It adds no protocol rule,
stock allocation, delivery authorization, effect, re-entry or source-truth
claim. It is the additive entity/independent-tracking portion of the planned
shipment evolution, not migration of an existing shipment activity into an
entity. A later domain policy must decide over-shipment and fulfilment rules.

## Run it

From the configured repository environment, choose a new output directory:

```sh
python -m research.ontology_driven_kg_realization.experiments.small_shop.partial_shipments.run --output /tmp/shop-partial-shipments
```

The command prints the three query checkpoints and writes `evidence.json` plus
`shop/history.jsonl`. The nested `shop/evidence.json` is the unchanged baseline
runner's receipt for the initial prefix, not the final extended history.
An existing output directory refuses rather than overwriting a prior run.

| Point in the history | Recorded shipments | Units not yet assigned to a shipment |
|---|---|---|
| Order admitted | none | SYN-PS-X1, SYN-PS-X2 |
| First shipment admitted | SYN-S1, tracking SYN-TRACK-1 | SYN-PS-X2 |
| Second shipment admitted | both, with distinct tracking | none |

This is why the ontology extension matters: a shipment becomes something we can
identify and query independently of its order. Two shipments no longer have to
be squeezed into one order property. Existing order and unit records are reused;
neither unit supersedes the other. "Not yet assigned" is a set difference over
these recorded associations, not proof of physical delivery.

## Inspect the inputs and mechanism

- [order.jsonl](order.jsonl) declares the synthetic order's two physical units.
- [shipments.jsonl](shipments.jsonl) declares two distinct shipments, trackers,
  and unit assignments. It states no dates or external observations.
- [mapping.json](mapping.json) names the types, relation kinds, identity rule,
  unchanged-value transformation and zero-based row locators. It describes this
  fixture, not a generic mapping language.
- [small-shop-with-shipments.yaml](small-shop-with-shipments.yaml) preserves the
  existing full Shop declarations. Its compiled additive delta is three classes,
  one tracking slot and two relation enum values. This fixture version is not a
  package release. The new classes are `Shipment`, `OrderHasShipment` and
  `ShipmentContainsUnit`.
- [run.py](run.py) reuses the prior Shop producer and public Core APIs. It builds
  neutral plans from the retained rows. Core performs structural checks and
  admission; the runner does not author successful check outcomes.

The single retained history contains the baseline's five changes, one new order
change and two shipment changes. It crosses two additive revisions in total,
including the original Shop revision. After reopen it has 20 current records
and 21 historical records, including the original superseded supplier state.
The report binds the original prefix, final head/count, revision, plans, source
digests and record-level derivations. Both shipments can be traced through
`trace_population_record` to their retained rows and mapping.

No GraphRecipe/OTTR template or new projection engine is needed for this fixed
topology. Population plans contain the operation dependency order; the existing
projector and reader are unchanged. An activity-to-entity migration, arbitrary
shipment policy and full source-coverage proof remain outside this fixture.

The run is a sequence of transactions, not one giant transaction. The negative
tests check refusal before preparation writes for absent Shipment vocabulary
and a missing endpoint, and no additional write when later evidence makes a
prepared shipment stale. Prior successful source retention is not rolled back.

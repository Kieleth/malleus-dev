# Synthetic partial shipments in the connected Shop history

## Approved cut

Keep the chapter's Table 1 and Figure 14 history as an exact prefix. Append
the existing synthetic order and its two shipments as a separately labelled
conformance extension, not new observations from the chapter. The synthetic
order has its own units; no association with a chapter order is invented.

Use the current structural admission policy. The existing duplicate-unit
policy proof stays separate. Same-history policy evolution is a Core-owned
future capability, not implemented here.

The observable result is simple: two units remain unassigned after the order,
one after its first shipment, none after its second. Distinct tracking IDs
remain queryable. This means recorded assignment, not physical shipment or
delivery. Source bytes state no domain time, so all three changes retain
`NONE_STATED`.

## Schema before code

[shop.yaml](shop.yaml) is an additive successor of the exact warehouse schema.
It preserves its root and imports. `Shipment` extends `ShopObject` and adds
required `tracking_id`. `OrderContainsUnit`, `OrderHasShipment`, and
`ShipmentContainsUnit` are separate relations with narrowed endpoints and
exact fixed predicates. These names reuse the earlier synthetic fixture;
their local grounding records do not attribute them to the chapter.

An optional `product_code` is attached to `InventoryUnit`, reusing the existing
slot with a class-local `required: false`. The synthetic source's stated code
can therefore be retained without adding values or requirements to older
units. No existing slot or semantic fact is removed or narrowed.

Reuse the original [order](../../partial_shipments/order.jsonl),
[shipments](../../partial_shipments/shipments.jsonl) and
[independent expected results](../../partial_shipments/expected.json).
The row adapter changes only the representation needed by the connected
schema: source identifiers remain on enduring objects. All populated fields
and endpoints must trace to retained source fields. The existing
`partial_shipments.run.shipment_view` supplies the query, not a second query
implementation.

The TDD proof checks prefix and prior-record preservation, the unchanged
policy, all three query checkpoints, source derivations, full and maintained
replay, refusal before mutation, and the explicit limit that structural
admission alone does not reject duplicate assignments.

RED observation: the focused test file collects 12 cases. All 12 report
missing-module errors before the runner exists (`12 errors in 0.68s`). A
separate first-error run confirms the missing module is this directory's
`run`, not a missing Core dependency. No history is created by that RED run.

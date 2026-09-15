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

## Result and why it matters

The chapter already has Ship occurrences. This extension does not reinterpret
them as shipment objects. It adds a separate synthetic cohort with explicitly
identified shipments, then runs the earlier shipment query against the richer
connected model.

| Accepted checkpoint | Recorded shipment assignments | Units remaining unassigned |
|---|---|---|
| Order recorded | None | SYN-PS-X1, SYN-PS-X2 |
| First shipment recorded | SYN-S1, tracking SYN-TRACK-1, contains SYN-PS-X1 | SYN-PS-X2 |
| Second shipment recorded | SYN-S2, tracking SYN-TRACK-2, contains SYN-PS-X2 | None |

This demonstrates representation growth inside an existing history, not just
two examples that work separately. The schema adds four classes and two
applicable slots. The history adds three changes containing eleven records:
five objects and six associations. Earlier observations, quantity versions and
source evidence remain retained. New inventory units carry the stated product
code; old units are not backfilled.

[The receipt](receipt.json) records the generated identities and checkpoints.
The result has 37 accepted changes, two recorded ontology revisions, 216
protocol events and 144 historical records. Its previous 1,646,996 bytes are
the exact warehouse history, not a reconstructed approximation of it.

The important policy limit is executable, too. In a separate test history, the
same structural policy admits two shipments assigning the same unit. The query
then still shows the other unit unassigned. That is **not** a successful test
of duplicate-assignment enforcement. The stricter
[existing policy fixture](../../shipment_policy/README.md) remains separate;
Core currently refuses changing this history's admission policy through an
ontology revision.

## Reproduce and inspect

Run from the repository with its declared development environment. Use a new
history path; this command builds Table 1, appends Figure 14, then appends the
synthetic cohort. The directory below is temporary output, not another source.

```bash
shop_run_dir=$(mktemp -d /private/tmp/shop-connected-shipments.XXXXXX)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.partial_shipments.run "$shop_run_dir/history.jsonl" --from-empty
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.partial_shipments.run "$shop_run_dir/history.jsonl" --reopen
```

`--append` accepts only the exact warehouse prefix named by
[input_boundary.json](input_boundary.json), and verifies both synthetic source
digests before any write. `--reopen` reads the retained history and prints the
three views plus all eleven records' field-level source witnesses. It does not
append events. A derivation names a source row and field; the retained mapping
explains how that field selects a relation or supplies a copied value.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q --tb=short -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop/connected_story/partial_shipments/test_connected_shipments.py
```

The tests build a fresh history, compare maintained and full replay, reuse the
earlier independent expected results, and exercise the append and read-only
commands. Exact test results and frozen commits belong to the chronological
[validation journal](../VALIDATION.md). The
[adopter self-check](MALLEUS_INQUISITION.md) names the schema and claim limits.

Frozen GREEN: `b255adf151cfb98a7cac61fc3fa697ef00c7f149`. Focused integration:
12 passes, zero skips. The clean detached whole-Shop plus transition-rule
regression passes 370 tests, zero skips; these include the 12 focused cases.
The clean run reproduces the history bytes and receipt JSON data.

No delivery, stock reservation, source-truth verification, complete business
policy, interrupted-import resume, or whole-import rollback is claimed. This
is a repository-local conformance fixture using public Core APIs, not a new
public API, stable wire, package release or external carrier integration.

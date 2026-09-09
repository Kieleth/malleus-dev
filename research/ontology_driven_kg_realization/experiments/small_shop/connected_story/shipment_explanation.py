"""Read the Shop shipment evidence, never infer an unpaid balance from absence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import malleus.compiler as api

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    run,
)


def check_invoice_limit(observations, *, account_complete, maximum_unpaid):
    """Bounds over explicit statuses. No truth, closure, or authorization attestation.

    The real source has UNKNOWN statuses. PAID/UNPAID inputs in this slice are
    synthetic controls, not derived from missing or present clearing events.
    """
    if (
        type(account_complete) is not bool
        or type(maximum_unpaid) is not int
        or maximum_unpaid < 0
    ):
        raise ValueError(
            "Explicit account completeness and a nonnegative integer limit are required"
        )
    seen, unpaid, unknown = set(), [], []
    for item in observations:
        if set(item) != {"invoice", "status"}:
            raise ValueError("Each observation requires exactly invoice and status")
        invoice, status = item["invoice"], item["status"]
        if not isinstance(invoice, str) or not invoice or invoice in seen:
            raise ValueError("Invoice identifiers must be nonempty and unique")
        if status not in ("UNPAID", "PAID", "UNKNOWN"):
            raise ValueError(f"Unknown explicit invoice status: {status}")
        seen.add(invoice)
        if status == "UNPAID":
            unpaid.append(invoice)
        elif status == "UNKNOWN":
            unknown.append(invoice)
    lower = len(unpaid)
    upper = lower + len(unknown) if account_complete else None
    outcome = "CANNOT_DETERMINE"
    if lower > maximum_unpaid:
        outcome = "VIOLATED"
    elif upper is not None and upper <= maximum_unpaid:
        outcome = "SATISFIED"
    return {
        "outcome": outcome,
        "unpaid_lower_bound": lower,
        "unpaid_upper_bound": upper,
        "known_unpaid_invoices": sorted(unpaid),
        "unknown_status_invoices": sorted(unknown),
    }


def _inputs(replay):
    spec_bytes = (run.HERE / "shipment_read_spec.json").read_bytes()
    spec = json.loads(spec_bytes)
    if spec["account_completeness"] != "NOT_ESTABLISHED":
        raise ValueError("This source has no complete customer-account evidence")
    context = replay.retained_bytes(spec["context"]["source_id"])
    if run.digest(context) != spec["context"]["sha256"]:
        raise ValueError(
            "Shipment explanation requires its exact retained context bytes"
        )
    passages = {}
    for ordinal, line in enumerate(context.splitlines()):
        passage = json.loads(line)
        if passage["passage_id"] in passages:
            raise ValueError("Repeated retained context passage")
        passages[passage["passage_id"]] = {
            "passage_id": passage["passage_id"],
            "text": passage["text"],
            "publication_locator": passage["locator"],
            "locator": f"row:{ordinal}:text",
            "source_id": spec["context"]["source_id"],
            "sha256": run.digest(context),
        }
    selected = {
        role: passages[identifier]
        for role, identifier in spec["context"]["passages"].items()
    }
    rows = [
        json.loads(line) for line in replay.retained_bytes(run.SOURCE_ID).splitlines()
    ]
    mapping = json.loads(replay.retained_bytes(run.MAPPING_ID))
    return spec_bytes, spec, selected, rows, mapping


def _events(graph, mapping, activity):
    return sorted(
        graph.query(
            "ShopOccurrence", event_type=mapping["activities"][activity]["event_type"]
        ),
        key=lambda event: event["id"],
    )


def _members(graph, mapping, event_id, column):
    return sorted(
        graph.get_node(link["entity_id"])["source_identifier"]
        for link in graph.query_event_participations(
            event_id=event_id, qualifier=mapping["object_columns"][column]["qualifier"]
        )
    )


def inspect_invoice_evidence(graph, replay):
    """Inspect a read projection against retained scope, never shrink missing inputs.

    This lower-level function also permits checked hypothetical graphs in tests.
    It issues no replay receipt. explain_shipments selects real replay graphs.
    """
    _, spec, _, rows, mapping = _inputs(replay)
    invoices, payments, gaps = [], {}, []
    receipts = _events(graph, mapping, "Receive Payment")
    clearings = _events(graph, mapping, "Clear Invoice")
    for payment in graph.query(mapping["object_columns"]["payment_ids"]["type"]):
        identifier = payment["source_identifier"]
        payments[identifier] = {
            "receipt_events": [
                event["id"]
                for event in receipts
                if identifier in _members(graph, mapping, event["id"], "payment_ids")
            ],
            "cleared_invoices": [],
        }
    for ordinal, row in enumerate(rows):
        if row["activity"] != "Create Invoice":
            continue
        if len(row["order_ids"]) != 1:
            raise ValueError("Invoice creation requires one explicit source order")
        order = row["order_ids"][0]
        if order not in spec["scope_orders"]:
            continue
        for identifier in row["invoice_ids"]:
            if any(item["invoice"] == identifier for item in invoices):
                raise ValueError(f"Ambiguous source invoice ownership: {identifier}")
            node_id = (
                f"{mapping['object_columns']['invoice_ids']['prefix']}:{identifier}"
            )
            event = graph.get_node(row["event_id"])
            expected_kind = mapping["activities"]["Create Invoice"]["event_type"]
            represented = graph.get_node(node_id) is not None
            linked = (
                event is not None
                and event["event_type"] == expected_kind
                and _members(graph, mapping, event["id"], "order_ids") == [order]
                and identifier in _members(graph, mapping, event["id"], "invoice_ids")
            )
            if not represented:
                gaps.append(f"INVOICE_NOT_REPRESENTED:{identifier}")
            if not linked:
                gaps.append(f"INVOICE_ORDER_LINK_MISMATCH:{identifier}")
            clearing_events = []
            for clearing in clearings:
                if identifier not in _members(
                    graph, mapping, clearing["id"], "invoice_ids"
                ):
                    continue
                payment_ids = _members(graph, mapping, clearing["id"], "payment_ids")
                if not payment_ids or any(
                    not payments[p]["receipt_events"] for p in payment_ids
                ):
                    gaps.append(f"PAYMENT_RECEIPT_NOT_REPRESENTED:{identifier}")
                    continue
                if represented and linked:
                    clearing_events.append(clearing["id"])
                    for payment_id in payment_ids:
                        payments[payment_id]["cleared_invoices"].append(identifier)
            if not clearing_events:
                gaps.append(f"NO_SUPPORTED_CLEARING_RECORDED:{identifier}")
            witnesses = []
            if represented and linked:
                # Use the existing public trace, not a guessed participation ID.
                for link in graph.query_event_participations(event_id=row["event_id"]):
                    if link["entity_id"] == node_id:
                        trace = api.trace_population_record(replay, link["id"])
                        witnesses.extend(
                            {
                                "record_id": link["id"],
                                "source_id": d["source_id"],
                                "locator": d["locator"],
                            }
                            for d in trace.derivations
                        )
            invoices.append(
                {
                    "invoice": identifier,
                    "order": order,
                    "ownership_source": {
                        "source_id": run.SOURCE_ID,
                        "locator": f"row:{ordinal}:order_ids[0]",
                    },
                    "status": "UNKNOWN",
                    "represented": represented,
                    "order_link_confirmed": linked,
                    "clearing_events": sorted(clearing_events),
                    "source_witnesses": witnesses,
                }
            )
    for payment in payments.values():
        payment["cleared_invoices"] = sorted(set(payment["cleared_invoices"]))
    return {
        "invoices": sorted(invoices, key=lambda item: item["invoice"]),
        "payments": dict(sorted(payments.items())),
        "gaps": sorted(set(gaps)),
    }


def explain_shipments(replay, *, at_occurrence=None):
    """Join evidence at a real accepted checkpoint. Context is the full source account."""
    spec_bytes, spec, passages, _, mapping = _inputs(replay)
    change_id = None
    graph = replay.graph
    if at_occurrence is not None:
        matches = [
            change
            for change in replay.change_sets
            if any(
                op.operation_type == "CREATE_EVENT" and op.record_id == at_occurrence
                for op in change.operations
            )
        ]
        if len(matches) != 1:
            raise ValueError(
                f"Unknown or ambiguous accepted occurrence: {at_occurrence}"
            )
        change_id = matches[0].change_set_id
        graph = replay.graph_at_change(change_id)
    result = inspect_invoice_evidence(graph, replay)
    orders = {}
    for order in spec["scope_orders"]:
        packed = [
            event
            for event in _events(graph, mapping, "Pack Shipment")
            if order in _members(graph, mapping, event["id"], "order_ids")
        ]
        orders[order] = {
            "invoices": sorted(
                item["invoice"]
                for item in result["invoices"]
                if item["order"] == order and item["order_link_confirmed"]
            ),
            "packing_events": [event["id"] for event in packed],
            "packed_units": sorted(
                {
                    unit
                    for event in packed
                    for unit in _members(graph, mapping, event["id"], "item_ids")
                }
            ),
            "shipping_events": [
                event["id"]
                for event in _events(graph, mapping, "Ship")
                if order in _members(graph, mapping, event["id"], "order_ids")
            ],
        }
    result.update(
        {
            "purpose": "SHOP_READ_REPORT_NOT_ADMISSION_OR_AUTHORIZATION",
            "orders": orders,
            "customer_identifier": None,
            "account_completeness": spec["account_completeness"],
            "invoice_limit": check_invoice_limit(
                [
                    {"invoice": item["invoice"], "status": item["status"]}
                    for item in result["invoices"]
                ],
                account_complete=False,
                maximum_unpaid=spec["maximum_unpaid"],
            ),
            "rule": {
                "maximum_unpaid": spec["maximum_unpaid"],
                "source": passages.pop("rule"),
            },
            "source_account": passages,
            "checkpoint": {
                "kind": "ACCEPTED_IMPORT_POSITION_NOT_DOMAIN_TIME",
                "after_occurrence": at_occurrence,
                "change_set_id": change_id,
                "graph_sha256": graph.state_digest(),
                "containing_history_head": replay.ledger_head,
                "containing_history_receipt": replay.receipt.identity,
            },
            "reader": {
                "spec_id": spec["id"],
                "spec_sha256": run.digest(spec_bytes),
                "implementation_sha256": run.digest(Path(__file__).read_bytes()),
                "mapping_sha256": run.digest(replay.retained_bytes(run.MAPPING_ID)),
                "table_sha256": run.digest(replay.retained_bytes(run.SOURCE_ID)),
            },
            "authorization": "NOT_ASSESSED",
            "limits": [
                "The source reports O2's delay; these joins do not establish causation.",
                "Clearance occurrence is not a complete status or balance snapshot.",
                "No complete customer invoice inventory or explicit unpaid balances are supplied.",
                "Context and expected invoice scope use the full retained source, not information claimed available at the historical business time.",
                "No calendar, duration, domain event order, permission or execution is inferred.",
            ],
        }
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history", type=Path)
    parser.add_argument(
        "--at-occurrence",
        help="Read the accepted graph just after this occurrence's change, not a domain-time cutoff",
    )
    args = parser.parse_args()
    replay = api.KnowledgeChangeHistory.reopen(args.history).replay()
    print(
        json.dumps(
            explain_shipments(replay, at_occurrence=args.at_occurrence),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

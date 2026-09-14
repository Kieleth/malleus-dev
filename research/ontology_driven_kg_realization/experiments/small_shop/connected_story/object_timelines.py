"""Read separate Shop object paths without inventing calendar time or new events."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

import malleus.compiler as api

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    run,
)


def _printed_coordinate(text):
    """DD-MM HH:MM display coordinates only. No default year or repaired date."""
    if not isinstance(text, str):
        raise ValueError("time_text must be the source's explicit string")
    if len(text) != 11 or (text[2], text[5], text[8]) != ("-", " ", ":"):
        return None
    fields = (text[:2], text[3:5], text[6:8], text[9:])
    if any(not x.isascii() or not x.isdecimal() for x in fields):
        return None
    day, month, hour, minute = map(int, fields)
    # February 29 needs an unstated year, so it cannot be placed by this view.
    month_days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if not (
        1 <= month <= 12
        and 1 <= day <= month_days[month - 1]
        and 0 <= hour < 24
        and 0 <= minute < 60
    ):
        return None
    return month, day, hour, minute


def order_printed_events(events):
    """Group by printed coordinates, not admission position or an ID tiebreaker."""
    grouped, unplaced, seen = defaultdict(list), [], set()
    for event in events:
        if "id" not in event or "time_text" not in event:
            raise ValueError("Every occurrence requires id and time_text")
        identifier = event["id"]
        if not isinstance(identifier, str) or not identifier or identifier in seen:
            raise ValueError("Occurrence IDs must be nonempty and unique")
        seen.add(identifier)
        coordinate = _printed_coordinate(event["time_text"])
        if coordinate is None:
            unplaced.append(identifier)
        else:
            grouped[coordinate].append(identifier)
    sequence = [sorted(grouped[key]) for key in sorted(grouped)]
    gaps = []
    if any(len(group) > 1 for group in sequence):
        gaps.append("TIED_PRINTED_TIMES")
    if unplaced:
        gaps.append("UNPLACED_EVENTS")
    return {
        "printed_sequence": sequence,
        "unplaced_events": sorted(unplaced),
        "ordering_gaps": gaps,
    }


def _spec():
    raw = (run.HERE / "timeline_read_spec.json").read_bytes()
    spec = json.loads(raw)
    if spec["interpretation"]["printed_time_format"] != "DD-MM HH:MM":
        raise ValueError("This reader implements only the declared DD-MM HH:MM display")
    return raw, spec


def inspect_object_views(graph, mapping):
    """Read a checked graph. Hypothetical tests get no accepted-history receipt."""
    _, spec = _spec()
    events, objects = {}, {}
    for event in sorted(graph.query(spec["occurrence_type"]), key=lambda x: x["id"]):
        participants = defaultdict(list)
        for link in graph.query_event_participations(event_id=event["id"]):
            participants[link["qualifier"]].append(link["entity_id"])
        events[event["id"]] = {
            "event_type": event["event_type"],
            "time_text": event["time_text"],
            "participants": {
                key: sorted(value) for key, value in sorted(participants.items())
            },
        }
    for column in mapping["object_columns"].values():
        for node in graph.query(column["type"]):
            links = graph.query_event_participations(
                entity_id=node["id"], qualifier=column["qualifier"]
            )
            identifiers = sorted({link["event_id"] for link in links})
            objects[node["id"]] = {
                "type": node["type"],
                "source_identifier": node["source_identifier"],
                "event_ids": identifiers,
                "participation_ids": sorted(link["id"] for link in links),
                **order_printed_events(
                    [
                        {"id": key, "time_text": events[key]["time_text"]}
                        for key in identifiers
                    ]
                ),
            }
    return {"events": events, "objects": dict(sorted(objects.items()))}


def _order_views(objects, account, mapping):
    """Reuse recorded joins; no transitive event flattening or early ownership."""
    columns = mapping["object_columns"]

    def node_id(column, identifier):
        return f"{columns[column]['prefix']}:{identifier}"

    views = {}
    for lane in objects.values():
        if lane["type"] != columns["order_ids"]["type"]:
            continue
        order = lane["source_identifier"]
        invoices = {
            invoice
            for invoice, orders in account["invoice_orders"].items()
            if order in orders
        }
        units = set(account["packed_units"].get(order, ()))
        payments = {
            payment
            for payment, cleared in account["payment_invoices"].items()
            if invoices.intersection(cleared)
        }
        suppliers = {
            supplier
            for supplier, received in account["received_units"].items()
            if units.intersection(received)
        }
        related = {node_id("order_ids", order)}
        for column, identifiers in (
            ("invoice_ids", invoices),
            ("item_ids", units),
            ("payment_ids", payments),
            ("supplier_order_ids", suppliers),
        ):
            related.update(node_id(column, identifier) for identifier in identifiers)
        if not related.issubset(objects):
            raise ValueError("An order join references an absent object view")
        views[order] = {
            "scope": "RETROSPECTIVE_RECORDED_JOINS",
            "objects": sorted(related),
        }
    return dict(sorted(views.items()))


def read_timelines(replay):
    """Derive a report from one accepted replay; write neither graph nor ledger."""
    spec_bytes, spec = _spec()
    source = replay.retained_bytes(spec["source_id"])
    if run.digest(source) != spec["source_sha256"]:
        raise ValueError("Object views require the exact retained Shop table")
    mapping_bytes = replay.retained_bytes(run.MAPPING_ID)
    mapping = json.loads(mapping_bytes)
    result = inspect_object_views(replay.graph, mapping)
    rows = {row["event_id"]: row for row in map(json.loads, source.splitlines())}
    expected_events = {
        op.record_id
        for change in replay.change_sets
        for op in change.operations
        if op.operation_type == "CREATE_EVENT"
    }
    if set(result["events"]) != expected_events:
        raise ValueError("Object views must account for every admitted Shop occurrence")

    def witnesses(record_ids):
        return [
            {
                "record_id": identifier,
                "source_id": d["source_id"],
                "locator": d["locator"],
            }
            for identifier in sorted(record_ids)
            for d in api.trace_population_record(replay, identifier).derivations
        ]

    for identifier, event in result["events"].items():
        row = rows[identifier]
        expected_participants = {
            column["qualifier"]: sorted(
                f"{column['prefix']}:{value}" for value in row[field]
            )
            for field, column in mapping["object_columns"].items()
            if field in row
        }
        if (
            event["time_text"] != row["time_text"]
            or event["event_type"]
            != mapping["activities"][row["activity"]]["event_type"]
            or event["participants"] != expected_participants
        ):
            raise ValueError(
                f"Occurrence view differs from its retained row: {identifier}"
            )
        event["witnesses"] = witnesses([identifier])
    for lane in result["objects"].values():
        lane["witnesses"] = witnesses(lane["participation_ids"])
    result.update(
        {
            "order_views": _order_views(
                result["objects"], run.explain(replay), mapping
            ),
            "interpretation": spec["interpretation"],
            "limits": spec["limits"],
            "checkpoint": {
                "kind": "ACCEPTED_IMPORT_POSITION_NOT_DOMAIN_TIME",
                "history_head": replay.ledger_head,
                "history_receipt": replay.receipt.identity,
                "graph_sha256": replay.graph.state_digest(),
            },
            "reader": {
                "spec_id": spec["id"],
                "spec_sha256": run.digest(spec_bytes),
                "implementation_sha256": run.digest(Path(__file__).read_bytes()),
                "mapping_sha256": run.digest(mapping_bytes),
                "source_sha256": run.digest(source),
            },
        }
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history", type=Path)
    args = parser.parse_args()
    replay = api.KnowledgeChangeHistory.reopen(args.history).replay()
    print(json.dumps(read_timelines(replay), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

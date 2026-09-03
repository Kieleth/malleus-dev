"""Private research-local Small Shop queries over one verified history.

This showcase has no stable API or wire-format compatibility contract.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Callable, Mapping

from malleus._contract_pipeline.knowledge import (
    KnowledgeChangeHistory,
    KnowledgeChangeRefusal,
    KnowledgeChangeSet,
    KnowledgeHistoryReplay,
    KnowledgeRecordHistory,
    KnowledgeRetainedInput,
    KnowledgeValidTime,
)
from malleus.kg import KnowledgeGraph
from research.ontology_driven_kg_realization.experiments.small_shop.showcase.run import (
    verify_source_mapping_receipts,
)


_SCHEMA = "malleus.small-shop.query-result/private-v0"


class QueryError(ValueError):
    """A requested Small Shop query cannot produce one exact answer."""


def _require_identifier(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise QueryError(f"{label} must be a nonempty string")
    return value


def _plain(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    return value


def _canonical(value: object) -> bytes:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, UnicodeError, ValueError) as error:
        raise QueryError("query answer is not canonical JSON") from error


def _time(value: KnowledgeValidTime | None) -> dict[str, str] | None:
    if value is None:
        return None
    return {"kind": value.kind, "value": value.value}


def _record(record_id: str, history: KnowledgeRecordHistory) -> dict[str, object]:
    operation = history.operation
    endpoints = (
        {"source_id": operation.source_id, "target_id": operation.target_id}
        if operation.source_id is not None or operation.target_id is not None
        else {}
    )
    return {
        "id": record_id,
        "type": operation.record_type,
        **endpoints,
        **_plain(operation.properties),
    }


def _history(value: KnowledgeRecordHistory) -> dict[str, object]:
    return {
        "change_set_id": value.change_set_id,
        "superseded_by": value.superseded_by,
        "supersedes_record_id": value.supersedes_record_id,
        "valid_from": _time(value.valid_from),
        "valid_to": _time(value.valid_to),
    }


def _change(
    replay: KnowledgeHistoryReplay, change_set_id: str
) -> tuple[int, KnowledgeChangeSet]:
    for index, change in enumerate(replay.change_sets):
        if change.change_set_id == change_set_id:
            return index, change
    raise QueryError(f"unknown accepted change: {change_set_id}")


def _graph_and_coordinates(
    replay: KnowledgeHistoryReplay,
    change_set_id: str | None,
) -> tuple[KnowledgeGraph, dict[str, object]]:
    if not isinstance(replay, KnowledgeHistoryReplay):
        raise QueryError("a verified KnowledgeHistoryReplay is required")
    if not replay.change_sets:
        raise QueryError("history has no accepted knowledge change")

    selected_id = change_set_id or replay.change_sets[-1].change_set_id
    index, _ = _change(replay, selected_id)
    graph = (
        replay.graph
        if index == len(replay.change_sets) - 1
        else replay.graph_at_change(selected_id)
    )
    graph_digest = graph.state_digest()
    if index == len(replay.change_sets) - 1:
        if replay.ledger_head != replay.acceptance_head:
            raise QueryError(
                "current graph lacks an exact accepted-state ledger prefix"
            )
        values = {
            "acceptance_head": replay.acceptance_head,
            "ledger_event_count": replay.ledger_event_count,
            "ledger_head": replay.ledger_head,
            "materialization_head": replay.materialization_head,
        }
    else:
        following = replay.change_sets[index + 1]
        if following.base_ledger_head != following.base_acceptance_head:
            raise QueryError(
                "historical graph lacks an exact accepted-state ledger prefix"
            )
        if following.base_accepted_state_digest != graph_digest:
            raise QueryError("historical graph and following change base disagree")
        values = {
            "acceptance_head": following.base_acceptance_head,
            "ledger_event_count": following.base_ledger_event_count,
            "ledger_head": following.base_ledger_head,
            "materialization_head": following.base_materialization_head,
        }
    return graph, {
        **values,
        "after_change_set_id": selected_id,
        "graph_state_digest": graph_digest,
    }


def _answer(
    replay: KnowledgeHistoryReplay,
    command: str,
    result: object,
    *,
    change_set_id: str | None = None,
) -> bytes:
    _, coordinates = _graph_and_coordinates(replay, change_set_id)
    return _canonical(
        {
            "command": command,
            "coordinates": coordinates,
            "result": result,
            "schema": _SCHEMA,
        }
    )


def order_contents(replay: KnowledgeHistoryReplay, order_id: str = "O1") -> bytes:
    """Return one sales order and its contained inventory units."""
    identifier = _require_identifier(order_id, "sales order ID")
    order = replay.graph.get_node(identifier)
    if order is None or order.get("type") != "SalesOrder":
        raise QueryError(f"unknown sales order: {identifier}")

    contents = []
    relations = replay.graph.query_relations(
        relation_type="OrderContainsUnit", source_id=identifier
    )
    for relation in sorted(
        relations, key=lambda item: (item["key"], item["target_id"])
    ):
        unit = replay.graph.get_node(relation["target_id"])
        if unit is None:
            raise QueryError(f"relation {relation['key']} has an unknown target")
        normalized_relation = dict(relation)
        normalized_relation["id"] = normalized_relation.pop("key")
        contents.append({"relation": normalized_relation, "unit": unit})
    return _answer(
        replay,
        "order-contents",
        {"contents": contents, "order": order},
    )


def current_supplier_order(
    replay: KnowledgeHistoryReplay, supplier_order_id: str = "B"
) -> bytes:
    """Return the one current state of a supplier order."""
    identifier = _require_identifier(supplier_order_id, "supplier order ID")
    matches = sorted(
        replay.graph.query(
            entity_type="SupplierOrderState", supplier_order_id=identifier
        ),
        key=lambda item: item["id"],
    )
    if not matches:
        raise QueryError(f"unknown supplier order: {identifier}")
    if len(matches) != 1:
        raise QueryError(f"supplier order has multiple current states: {identifier}")
    return _answer(
        replay,
        "current-supplier-order",
        {"supplier_order": matches[0]},
    )


def _payment_settlement_result(
    graph: KnowledgeGraph, payment_number: str
) -> dict[str, object]:
    payments = sorted(
        graph.query(entity_type="Payment", payment_number=payment_number),
        key=lambda item: item["id"],
    )
    if not payments:
        raise QueryError(f"unknown payment: {payment_number}")
    if len(payments) != 1:
        raise QueryError(f"payment number is not unique: {payment_number}")
    payment = payments[0]
    payment_id = payment["id"]

    settlements = []
    relations = graph.query_relations(
        relation_type="PaymentSettlesInvoiceRelation", source_id=payment_id
    )
    for relation in sorted(
        relations, key=lambda item: (item["target_id"], item["key"])
    ):
        if (
            relation.get("type") != "PaymentSettlesInvoiceRelation"
            or relation.get("relation_type") != "PAYMENT_SETTLES_INVOICE"
            or relation.get("source_id") != payment_id
        ):
            raise QueryError(f"malformed payment settlement: {relation.get('key')}")
        target_id = relation.get("target_id")
        invoice = graph.get_node(target_id)
        if invoice is None or invoice.get("type") != "Invoice":
            raise QueryError(f"settlement target is not an Invoice: {target_id}")
        normalized_relation = dict(relation)
        normalized_relation["id"] = normalized_relation.pop("key")
        settlements.append({"invoice": invoice, "relation": normalized_relation})
    return {"payment": payment, "settlements": settlements}


def payment_settlements(
    replay: KnowledgeHistoryReplay, payment_number: str = "P1"
) -> bytes:
    """Return invoices settled by one current Payment."""
    identifier = _require_identifier(payment_number, "payment number")
    return _answer(
        replay,
        "payment-settlements",
        _payment_settlement_result(replay.graph, identifier),
    )


def supplier_order_history(
    replay: KnowledgeHistoryReplay, supplier_order_id: str = "B"
) -> bytes:
    """Return every accepted state of a supplier order in change order."""
    identifier = _require_identifier(supplier_order_id, "supplier order ID")
    change_order = {
        change.change_set_id: index for index, change in enumerate(replay.change_sets)
    }
    states = []
    for record_id, history in replay.record_history.items():
        operation = history.operation
        if (
            operation.record_type != "SupplierOrderState"
            or operation.properties.get("supplier_order_id") != identifier
        ):
            continue
        states.append(
            {
                **_history(history),
                "record": _record(record_id, history),
                "_sort": (
                    change_order[history.change_set_id],
                    operation.ordinal,
                    record_id,
                ),
            }
        )
    if not states:
        raise QueryError(f"unknown supplier order: {identifier}")
    states.sort(key=lambda item: item.pop("_sort"))
    return _answer(
        replay,
        "supplier-order-history",
        {"states": states, "supplier_order_id": identifier},
    )


def state_after_change(replay: KnowledgeHistoryReplay, change_set_id: str) -> bytes:
    """Return the graph immediately after one named accepted change."""
    identifier = _require_identifier(change_set_id, "change-set ID")
    graph, _ = _graph_and_coordinates(replay, identifier)
    return _answer(
        replay,
        "state-after-change",
        {"change_set_id": identifier, "graph": graph.snapshot()},
        change_set_id=identifier,
    )


def _retained_closure(
    replay: KnowledgeHistoryReplay,
    declared: tuple[tuple[str, str], ...],
    roles: frozenset[str],
) -> list[dict[str, str]]:
    retained = {item.record_id: item for item in replay.retained_inputs}
    result = []
    for record_id, identity in declared:
        item: KnowledgeRetainedInput | None = retained.get(record_id)
        if item is None or item.identity != identity or item.role not in roles:
            raise QueryError(f"declared retained input is unavailable: {record_id}")
        result.append(
            {
                "media_type": item.media_type,
                "record_id": item.record_id,
                "role": item.role,
                "sha256": item.identity,
            }
        )
    return sorted(result, key=lambda item: (item["record_id"], item["sha256"]))


def record_change_provenance(replay: KnowledgeHistoryReplay, record_id: str) -> bytes:
    """Return change-level provenance, never per-operation causality."""
    identifier = _require_identifier(record_id, "record ID")
    try:
        history = replay.record_history[identifier]
    except KeyError as error:
        raise QueryError(f"unknown record: {identifier}") from error
    _, change = _change(replay, history.change_set_id)
    record = _record(identifier, history)
    record["history"] = _history(history)
    result = {
        "change": {"identity": change.identity, "value": _plain(change.data)},
        "change_evidence_closure": _retained_closure(
            replay,
            change.evidence,
            frozenset({"RETAINED_EVIDENCE", "VALIDATED_CONTRACT"}),
        ),
        "change_source_closure": _retained_closure(
            replay, change.sources, frozenset({"RETAINED_SOURCE"})
        ),
        "provenance_scope": "CHANGE_LEVEL_NOT_PER_OPERATION_CAUSALITY",
        "record": record,
    }
    return _answer(replay, "record-change-provenance", result)


def query_state_coordinates(replay: KnowledgeHistoryReplay) -> bytes:
    """Return identities needed to reproduce the current queried state."""
    result = {
        "effective_contract_identity": replay.partial_contract.identity,
        "history_binding_identity": replay.binding.identity,
        "history_receipt_identity": replay.receipt.identity,
        "validated_fact_set_identity": replay.graph.snapshot()["ontology_hash"],
    }
    return _answer(replay, "coordinates", result)


_Query = Callable[[KnowledgeHistoryReplay, str], bytes]
_COMMANDS: dict[
    str, tuple[_Query | Callable[[KnowledgeHistoryReplay], bytes], bool]
] = {
    "coordinates": (query_state_coordinates, False),
    "current-supplier-order": (current_supplier_order, True),
    "order-contents": (order_contents, True),
    "payment-settlements": (payment_settlements, True),
    "record-change-provenance": (record_change_provenance, True),
    "state-after-change": (state_after_change, True),
    "supplier-order-history": (supplier_order_history, True),
}


def execute_query(
    replay: KnowledgeHistoryReplay, command: str, identifier: str | None = None
) -> bytes:
    """Dispatch one closed query command against an already verified replay."""
    try:
        function, needs_identifier = _COMMANDS[command]
    except (KeyError, TypeError) as error:
        raise QueryError(f"unknown query command: {command}") from error
    if needs_identifier:
        selected = _require_identifier(identifier, f"{command} identifier")
        return function(replay, selected)
    if identifier is not None:
        raise QueryError(f"query command does not accept an identifier: {command}")
    return function(replay)


def open_history(path: str | Path) -> KnowledgeHistoryReplay:
    """Reopen Core history and recompute its retained Small Shop receipts."""
    replay = KnowledgeChangeHistory.reopen(path).replay()
    verify_source_mapping_receipts(replay)
    return replay


def main(argv: tuple[str, ...] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--history", required=True, type=Path)
    parser.add_argument("command")
    parser.add_argument("identifier", nargs="?")
    arguments = parser.parse_args(argv)
    try:
        answer = execute_query(
            open_history(arguments.history), arguments.command, arguments.identifier
        )
    except (KnowledgeChangeRefusal, QueryError) as error:
        parser.error(str(error))
    sys.stdout.buffer.write(answer + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

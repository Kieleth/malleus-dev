"""Contract tests for the read-only Small Shop query showcase."""

from __future__ import annotations

import ast
from dataclasses import replace
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path
import subprocess
import sys

import pytest

from malleus._contract_pipeline.knowledge import KnowledgeChangeHistory
from malleus.kg import KnowledgeGraph, OpStatus
from malleus.ontology import OntologyRegistry
from research.ontology_driven_kg_realization.experiments.small_shop.showcase import (
    query as query_module,
)
from research.ontology_driven_kg_realization.experiments.small_shop.showcase.query import (
    QueryError,
    current_supplier_order,
    execute_query,
    order_contents,
    payment_settlements,
    query_state_coordinates,
    record_change_provenance,
    state_after_change,
    supplier_order_history,
)
from research.ontology_driven_kg_realization.experiments.small_shop.showcase.run import (
    run_showcase,
)


O1 = "O1"
B = "B"
E4_CHANGE = "change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e4"
E7_CHANGE = "change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e7"
E4_RECORD = "supplier-order-state:B:e4"
E7_RECORD = "supplier-order-state:B:e7"
ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(scope="module")
def proof(tmp_path_factory: pytest.TempPathFactory):
    output = tmp_path_factory.mktemp("small-shop-query") / "proof"
    result = run_showcase(output)
    return output / "history.jsonl", result.replay


def _value(source: bytes) -> dict[str, object]:
    value = json.loads(source)
    assert isinstance(value, dict)
    assert source == json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    coordinates = value["coordinates"]
    assert isinstance(coordinates, dict)
    assert {
        "acceptance_head",
        "after_change_set_id",
        "graph_state_digest",
        "ledger_event_count",
        "ledger_head",
        "materialization_head",
    } == set(coordinates)
    return value


def test_order_contents_and_current_supplier_order_are_typed_current_queries(
    proof,
) -> None:
    _, replay = proof

    contents = _value(order_contents(replay, O1))
    assert contents["command"] == "order-contents"
    assert contents["result"] == {
        "contents": [
            {
                "relation": {
                    "id": "contains:O1:X1",
                    "relation_type": "ORDER_CONTAINS_UNIT",
                    "source_id": "O1",
                    "target_id": "X1",
                    "type": "OrderContainsUnit",
                },
                "unit": {
                    "id": "X1",
                    "product_code": "X",
                    "type": "InventoryUnit",
                },
            }
        ],
        "order": {"id": "O1", "order_number": "O1", "type": "SalesOrder"},
    }

    supplier = _value(current_supplier_order(replay, B))
    assert supplier["command"] == "current-supplier-order"
    assert supplier["result"] == {
        "supplier_order": {
            "id": E7_RECORD,
            "ordered_quantity": 2,
            "product_code": "Y",
            "source_occurrence_id": "e7",
            "supplier_order_id": "B",
            "type": "SupplierOrderState",
        }
    }


def test_supplier_order_history_preserves_both_states_and_temporal_links(
    proof,
) -> None:
    _, replay = proof

    answer = _value(supplier_order_history(replay, B))

    assert answer["command"] == "supplier-order-history"
    assert answer["result"] == {
        "states": [
            {
                "change_set_id": E4_CHANGE,
                "record": {
                    "id": E4_RECORD,
                    "ordered_quantity": 1,
                    "product_code": "Y",
                    "source_occurrence_id": "e4",
                    "supplier_order_id": "B",
                    "type": "SupplierOrderState",
                },
                "superseded_by": E7_RECORD,
                "supersedes_record_id": None,
                "valid_from": {"kind": "ORDER_ONLY", "value": "e4"},
                "valid_to": {"kind": "ORDER_ONLY", "value": "e7"},
            },
            {
                "change_set_id": E7_CHANGE,
                "record": {
                    "id": E7_RECORD,
                    "ordered_quantity": 2,
                    "product_code": "Y",
                    "source_occurrence_id": "e7",
                    "supplier_order_id": "B",
                    "type": "SupplierOrderState",
                },
                "superseded_by": None,
                "supersedes_record_id": E4_RECORD,
                "valid_from": {"kind": "ORDER_ONLY", "value": "e7"},
                "valid_to": None,
            },
        ],
        "supplier_order_id": "B",
    }


def test_state_after_change_binds_the_historical_graph_and_its_exact_prefix(
    proof,
) -> None:
    _, replay = proof

    answer = _value(state_after_change(replay, E4_CHANGE))
    coordinates = answer["coordinates"]
    e4_index = next(
        index
        for index, change in enumerate(replay.change_sets)
        if change.change_set_id == E4_CHANGE
    )
    next_change = replay.change_sets[e4_index + 1]

    assert coordinates == {
        "acceptance_head": next_change.base_acceptance_head,
        "after_change_set_id": E4_CHANGE,
        "graph_state_digest": next_change.base_accepted_state_digest,
        "ledger_event_count": next_change.base_ledger_event_count,
        "ledger_head": next_change.base_ledger_head,
        "materialization_head": next_change.base_materialization_head,
    }
    graph = answer["result"]["graph"]
    assert {node["id"] for node in graph["nodes"]} == {
        O1,
        "X1",
        "invoice:I1",
        "invoice:I2",
        "payment:P1",
        E4_RECORD,
    }
    assert E7_RECORD not in {node["id"] for node in graph["nodes"]}
    assert answer["result"]["change_set_id"] == E4_CHANGE


def test_record_change_provenance_joins_history_and_change_level_closures(
    proof,
) -> None:
    _, replay = proof

    answer = _value(record_change_provenance(replay, E4_RECORD))
    result = answer["result"]
    change = result["change"]

    assert answer["command"] == "record-change-provenance"
    assert result["provenance_scope"] == "CHANGE_LEVEL_NOT_PER_OPERATION_CAUSALITY"
    assert result["record"]["id"] == E4_RECORD
    assert result["record"]["history"]["change_set_id"] == E4_CHANGE
    assert change["value"]["change_set_id"] == E4_CHANGE
    assert (
        "sha256:"
        + sha256(
            json.dumps(
                change["value"],
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        == change["identity"]
    )
    assert [item["record_id"] for item in result["change_source_closure"]] == sorted(
        item["record_id"] for item in result["change_source_closure"]
    )
    assert {item["record_id"] for item in result["change_source_closure"]} == {
        identifier
        for change in replay.change_sets
        if change.change_set_id == E4_CHANGE
        for identifier, _ in change.sources
    }
    assert all(
        item["role"] == "RETAINED_SOURCE" for item in result["change_source_closure"]
    )
    assert {item["record_id"] for item in result["change_evidence_closure"]} == {
        identifier
        for change in replay.change_sets
        if change.change_set_id == E4_CHANGE
        for identifier, _ in change.evidence
    }
    assert all(
        item["role"] in {"RETAINED_EVIDENCE", "VALIDATED_CONTRACT"}
        for item in result["change_evidence_closure"]
    )


def test_coordinate_query_identifies_the_reopened_current_state(proof) -> None:
    _, replay = proof

    answer = _value(query_state_coordinates(replay))

    assert answer["coordinates"] == {
        "acceptance_head": replay.acceptance_head,
        "after_change_set_id": E7_CHANGE,
        "graph_state_digest": replay.graph.state_digest(),
        "ledger_event_count": replay.ledger_event_count,
        "ledger_head": replay.ledger_head,
        "materialization_head": replay.materialization_head,
    }
    assert answer["result"] == {
        "effective_contract_identity": replay.partial_contract.identity,
        "history_binding_identity": replay.binding.identity,
        "history_receipt_identity": replay.receipt.identity,
        "validated_fact_set_identity": replay.graph.snapshot()["ontology_hash"],
    }


@pytest.mark.parametrize(
    ("function", "identifier", "message"),
    [
        (order_contents, "missing-order", "unknown sales order"),
        (current_supplier_order, "missing-order", "unknown supplier order"),
        (supplier_order_history, "missing-order", "unknown supplier order"),
        (state_after_change, "missing-change", "unknown accepted change"),
        (record_change_provenance, "missing-record", "unknown record"),
        (payment_settlements, "missing-payment", "unknown payment"),
    ],
)
def test_unknown_identifiers_fail_loudly_without_partial_answers(
    proof, function, identifier: str, message: str
) -> None:
    _, replay = proof

    with pytest.raises(QueryError, match=message):
        function(replay, identifier)

    with pytest.raises(QueryError, match="unknown query command"):
        execute_query(replay, "invented-command")


def test_all_commands_are_canonical_deterministic_and_leave_history_unchanged(
    proof,
) -> None:
    history_path, replay = proof
    history_before = history_path.read_bytes()
    graph_before = replay.graph.snapshot()
    commands = (
        ("order-contents", O1),
        ("current-supplier-order", B),
        ("supplier-order-history", B),
        ("state-after-change", E4_CHANGE),
        ("record-change-provenance", E4_RECORD),
        ("coordinates", None),
    )

    first = [
        execute_query(replay, command, identifier) for command, identifier in commands
    ]
    second = [
        execute_query(replay, command, identifier) for command, identifier in commands
    ]

    assert first == second
    assert all(
        _value(answer)["schema"] == "malleus.small-shop.query-result/private-v0"
        for answer in first
    )
    assert history_path.read_bytes() == history_before
    assert replay.graph.snapshot() == graph_before


def test_cli_reopens_one_history_and_prints_the_same_canonical_answer(proof) -> None:
    history_path, _ = proof
    history_before = history_path.read_bytes()
    command = [
        sys.executable,
        "-m",
        query_module.__name__,
        "--history",
        str(history_path),
        "current-supplier-order",
        B,
    ]

    completed = subprocess.run(command, check=True, capture_output=True)

    assert completed.stdout.rstrip(b"\n") == execute_query(
        query_module.open_history(history_path),
        "current-supplier-order",
        B,
    )
    assert completed.stderr == b""
    assert history_path.read_bytes() == history_before


def test_open_history_recomputes_retained_mapping_receipts(
    proof, monkeypatch: pytest.MonkeyPatch
) -> None:
    history_path, _ = proof
    verified = []
    verifier = query_module.verify_source_mapping_receipts

    def observe(replay):
        verified.append(replay)
        return verifier(replay)

    monkeypatch.setattr(query_module, "verify_source_mapping_receipts", observe)

    reopened = query_module.open_history(history_path)

    assert verified == [reopened]


def test_query_layer_has_no_ledger_parser_evaluator_or_write_path() -> None:
    source_path = Path(query_module.__file__)
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    calls = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }

    assert "oracle" not in source.lower()
    assert "evaluation" not in source.lower()
    assert "JsonlLedger" not in imports
    assert "json.loads" not in source
    assert "read_bytes" not in calls
    assert "record-provenance" not in source
    assert "record_provenance" not in source
    assert not calls & {
        "admit",
        "append_anchor",
        "append_anchors",
        "append_many",
        "create_entity",
        "create_event",
        "create_relation",
        "create_signal",
        "materialize_into",
        "write_bytes",
        "write_text",
    }


def test_current_query_refuses_when_post_acceptance_history_has_no_exact_graph_prefix(
    tmp_path: Path,
) -> None:
    output = tmp_path / "proof"
    run_showcase(output)
    history_path = output / "history.jsonl"
    history = KnowledgeChangeHistory.reopen(history_path)
    before = history.replay()
    retained = b"post-acceptance audit evidence\n"
    identity = "sha256:" + sha256(retained).hexdigest()
    event = json.dumps(
        {
            "event_type": "ARTIFACT_REGISTERED",
            "payload": {
                "artifact_id": "artifact:post-acceptance-audit",
                "artifact_identity": identity,
            },
        },
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    history.append_anchor(
        machine_event=event,
        retained_bytes=retained,
        media_type="text/plain",
        role="RETAINED_EVIDENCE",
        transaction_time="2026-09-03T00:06:00Z",
        actor_id="actor:small-shop-auditor",
    )
    replay = history.replay()
    ledger_after_anchor = history_path.read_bytes()

    assert replay.graph.snapshot() == before.graph.snapshot()
    assert replay.ledger_head != replay.acceptance_head
    with pytest.raises(QueryError, match="exact accepted-state ledger prefix"):
        current_supplier_order(replay, B)
    assert history_path.read_bytes() == ledger_after_anchor


def test_historical_query_refuses_an_unproven_following_base(proof) -> None:
    _, replay = proof
    e4_index = next(
        index
        for index, change in enumerate(replay.change_sets)
        if change.change_set_id == E4_CHANGE
    )
    following = replace(
        replay.change_sets[e4_index + 1], base_ledger_head="sha256:" + "0" * 64
    )
    incompatible = replace(
        replay,
        change_sets=(*replay.change_sets[: e4_index + 1], following),
    )

    with pytest.raises(QueryError, match="exact accepted-state ledger prefix"):
        state_after_change(incompatible, E4_CHANGE)

    assert replay.graph_at_change(E4_CHANGE).state_digest() == (
        replay.change_sets[e4_index + 1].base_accepted_state_digest
    )


@pytest.fixture
def settlement_graph() -> KnowledgeGraph:
    fixture_root = (
        ROOT
        / "research/ontology_driven_kg_realization/fixtures"
        / "small_shop_fulfilment_settlement_v1/input/tbox"
    )
    correction_root = fixture_root.parents[2] / (
        "small_shop_fulfilment_correction_v1/input/tbox"
    )
    base_root = fixture_root.parents[2] / "small_shop_fulfilment/input/tbox"
    registry = OntologyRegistry(
        fixture_root / "small-shop-settlement.yaml",
        {
            "linkml:types": Path(
                str(
                    files("linkml_runtime").joinpath(
                        "linkml_model", "model", "schema", "types.yaml"
                    )
                )
            ),
            "malleus": ROOT / "ontology/malleus.yaml",
            "small-shop": base_root / "small-shop.yaml",
            "small-shop-correction": correction_root / "small-shop-correction.yaml",
        },
    )
    graph = KnowledgeGraph(registry)
    operations = (
        graph.create_entity("Invoice", "invoice:I2", {"invoice_number": "I2"}),
        graph.create_entity("Invoice", "invoice:I1", {"invoice_number": "I1"}),
        graph.create_entity("Payment", "payment:P1", {"payment_number": "P1"}),
        graph.create_relation(
            "PaymentSettlesInvoiceRelation",
            "relation:P1:I2",
            "payment:P1",
            "invoice:I2",
            {"relation_type": "PAYMENT_SETTLES_INVOICE"},
        ),
        graph.create_relation(
            "PaymentSettlesInvoiceRelation",
            "relation:P1:I1",
            "payment:P1",
            "invoice:I1",
            {"relation_type": "PAYMENT_SETTLES_INVOICE"},
        ),
    )
    assert all(operation.op_status is OpStatus.COMMITTED for operation in operations)
    return graph


def test_payment_settlement_logic_is_typed_sorted_deterministic_and_read_only(
    settlement_graph: KnowledgeGraph,
) -> None:
    before = settlement_graph.snapshot()

    first = query_module._payment_settlement_result(settlement_graph, "P1")
    second = query_module._payment_settlement_result(settlement_graph, "P1")

    assert (
        first
        == second
        == {
            "payment": {
                "id": "payment:P1",
                "payment_number": "P1",
                "type": "Payment",
            },
            "settlements": [
                {
                    "invoice": {
                        "id": "invoice:I1",
                        "invoice_number": "I1",
                        "type": "Invoice",
                    },
                    "relation": {
                        "id": "relation:P1:I1",
                        "relation_type": "PAYMENT_SETTLES_INVOICE",
                        "source_id": "payment:P1",
                        "target_id": "invoice:I1",
                        "type": "PaymentSettlesInvoiceRelation",
                    },
                },
                {
                    "invoice": {
                        "id": "invoice:I2",
                        "invoice_number": "I2",
                        "type": "Invoice",
                    },
                    "relation": {
                        "id": "relation:P1:I2",
                        "relation_type": "PAYMENT_SETTLES_INVOICE",
                        "source_id": "payment:P1",
                        "target_id": "invoice:I2",
                        "type": "PaymentSettlesInvoiceRelation",
                    },
                },
            ],
        }
    )
    assert settlement_graph.snapshot() == before


def test_payment_business_key_queries_the_real_five_stage_replay(
    tmp_path: Path,
) -> None:
    output = tmp_path / "proof"
    replay = run_showcase(output).replay
    history_before = (output / "history.jsonl").read_bytes()

    answer = _value(payment_settlements(replay, payment_number="P1"))

    result = answer["result"]
    assert result["payment"] == {
        "id": "payment:P1",
        "payment_number": "P1",
        "type": "Payment",
    }
    assert [item["invoice"]["id"] for item in result["settlements"]] == [
        "invoice:I1",
        "invoice:I2",
    ]
    assert [item["relation"]["id"] for item in result["settlements"]] == [
        "relation:P1:I1",
        "relation:P1:I2",
    ]
    assert (output / "history.jsonl").read_bytes() == history_before


class _BrokenSettlementGraph:
    def __init__(self, target: dict[str, object] | None) -> None:
        self._target = target

    def query(self, **_filters) -> list[dict[str, object]]:
        return [{"id": "payment:P1", "payment_number": "P1", "type": "Payment"}]

    def get_node(self, identifier: str) -> dict[str, object] | None:
        return self._target

    def query_relations(self, **_filters) -> list[dict[str, object]]:
        return [
            {
                "key": "settles:P1:broken",
                "relation_type": "PAYMENT_SETTLES_INVOICE",
                "source_id": "payment:P1",
                "target_id": "broken",
                "type": "PaymentSettlesInvoiceRelation",
            }
        ]


@pytest.mark.parametrize(
    "target",
    [None, {"id": "broken", "type": "Payment", "payment_number": "broken"}],
)
def test_payment_settlement_logic_refuses_missing_or_wrong_target(target) -> None:
    with pytest.raises(QueryError, match="is not an Invoice"):
        query_module._payment_settlement_result(_BrokenSettlementGraph(target), "P1")


def test_payment_business_key_must_resolve_one_typed_graph_record(
    settlement_graph: KnowledgeGraph,
) -> None:
    assert (
        settlement_graph.create_entity(
            "Payment", "payment:P1:duplicate", {"payment_number": "P1"}
        ).op_status
        is OpStatus.COMMITTED
    )

    with pytest.raises(QueryError, match="payment number is not unique"):
        query_module._payment_settlement_result(settlement_graph, "P1")

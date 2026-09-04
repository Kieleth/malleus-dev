"""Small Shop proof of one public additive contract revision and replay."""

from __future__ import annotations

from importlib.resources import files
import json
from pathlib import Path

import malleus.compiler as compiler

from tests.contract_compiler.pareto.test_public_compiler import (
    ROOT,
    SHOP_BASE,
    SHOP_FIXTURE,
    SHOP_RUNTIME,
    TRANSACTION_TIME,
    _anchor,
    _bootstrap,
    _digest,
    _event,
    _prepare_and_admit,
    _protocol_events,
    _runtime,
)


BASE_INPUT = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "small_shop_fulfilment/input"
)
REVISION_TARGET = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "small_shop_fulfilment_contract_revision_v1/input/tbox/small-shop.yaml"
)


def _compile(source: bytes):
    return compiler.compile_linkml_contract(
        root_locator="small-shop",
        sources={
            "small-shop": source,
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": (
                files("linkml_runtime")
                .joinpath("linkml_model", "model", "schema", "types.yaml")
                .read_bytes()
            ),
        },
    )


def _retain_source(
    history: compiler.KnowledgeChangeHistory,
    *,
    artifact_id: str,
    source_id: str,
    content: bytes,
) -> None:
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id=artifact_id,
            artifact_identity=_digest(content),
        ),
        content,
        "SOURCE_ARTIFACT",
    )
    _anchor(
        history,
        _event(
            "SOURCE_REGISTERED",
            artifact_id=artifact_id,
            source_id=source_id,
            source_identity=_digest(content),
        ),
        content,
        "RETAINED_SOURCE",
    )


def _operation(raw: dict[str, object]) -> compiler.KnowledgeOperation:
    relation = raw["operation_type"] == "CREATE_RELATION"
    return compiler.KnowledgeOperation(
        ordinal=raw["ordinal"],
        operation_id=raw["operation_id"],
        operation_type=raw["operation_type"],
        record_type=raw["record_type"],
        record_id=raw["record_id"],
        properties=raw["properties"],
        depends_on=tuple(raw["depends_on"]),
        source_id=raw["source_id"] if relation else None,
        target_id=raw["target_id"] if relation else None,
    )


def _admit_ret010(
    history: compiler.KnowledgeChangeHistory,
    policy: compiler.PolicyProgram,
    mapping: dict[str, object],
) -> compiler.KnowledgeChangeSet:
    before = history.replay()
    operations = tuple(_operation(raw) for raw in mapping["operations"])
    change = history.compose_change_set(
        change_set_id="change:RET-010:genesis",
        source_record_ids=("source:ret010:warehouse", "source:ret010:inventory"),
        evidence_record_ids=("artifact:ret010-mapping",),
        operations=operations,
        valid_time=compiler.KnowledgeValidTime("INSTANT", mapping["valid_time"]),
        supersedes=(),
    )
    history.admit(
        change_set=change,
        machine_events=_protocol_events(
            policy,
            change,
            before.machine_state.identity,
            "ret010-revision-fixture",
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:public-adopter",
    )
    return change


def test_small_shop_replays_one_history_across_one_contract_revision(
    tmp_path: Path,
) -> None:
    base = _compile(SHOP_BASE.read_bytes())
    target = _compile(REVISION_TARGET.read_bytes())
    supplier_source = (
        SHOP_FIXTURE / "input/sources/supplier-order-history.jsonl"
    ).read_bytes()
    warehouse_source = (BASE_INPUT / "sources/warehouse.jsonl").read_bytes()
    inventory_source = (BASE_INPUT / "sources/inventory-units.csv").read_bytes()
    mapping_bytes = (SHOP_RUNTIME / "mapping.json").read_bytes()
    mapping = json.loads(mapping_bytes)
    history, base_partial, policy = _runtime(
        compiler, base, tmp_path / "small-shop-revision-history.jsonl"
    )
    _bootstrap(compiler, history, base, base_partial, supplier_source)
    _retain_source(
        history,
        artifact_id="artifact:ret010-source:warehouse",
        source_id="source:ret010:warehouse",
        content=warehouse_source,
    )
    _retain_source(
        history,
        artifact_id="artifact:ret010-source:inventory",
        source_id="source:ret010:inventory",
        content=inventory_source,
    )
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id="artifact:ret010-mapping",
            artifact_identity=_digest(mapping_bytes),
        ),
        mapping_bytes,
        "RETAINED_EVIDENCE",
    )
    initial = _admit_ret010(history, policy, mapping)

    target_partial = compiler.compose_partial_effective_contract(
        validated_fact_set_sha256=target.artifact.validated_fact_set_sha256,
        normative_profile=base_partial.normative_profile,
    )
    revision = history.compose_contract_revision(
        revision_id="revision:shop:0.1.0-to-0.2.0",
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=target_partial.canonical_bytes,
        reason="add supplier-order state vocabulary",
        issued_at=TRANSACTION_TIME,
    )
    history.record_contract_revision(
        revision=revision,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:public-adopter",
    )
    e4 = _prepare_and_admit(
        compiler, history, target_partial, policy, supplier_source, "e4"
    )
    e7 = _prepare_and_admit(
        compiler, history, target_partial, policy, supplier_source, "e7"
    )
    reopened = compiler.KnowledgeChangeHistory.reopen(history.path).replay()

    assert tuple((change.kind, change.subject) for change in revision.changes) == (
        (
            "ADD_CLASS",
            "https://malleus.dev/schema/small-shop-fulfilment/SupplierOrderState",
        ),
        (
            "ADD_SLOT",
            "https://malleus.dev/schema/small-shop-fulfilment/ordered_quantity",
        ),
        (
            "ADD_SLOT",
            "https://malleus.dev/schema/small-shop-fulfilment/source_occurrence_id",
        ),
        (
            "ADD_SLOT",
            "https://malleus.dev/schema/small-shop-fulfilment/supplier_order_id",
        ),
    )
    assert tuple(change.contract_identity for change in reopened.change_sets) == (
        initial.contract_identity,
        target_partial.identity,
        target_partial.identity,
    )
    assert initial.contract_identity == base_partial.identity
    assert tuple(change.identity for change in reopened.change_sets) == (
        initial.identity,
        e4.change_sets[-1].identity,
        e7.change_sets[-1].identity,
    )
    assert reopened.contract_revisions == (revision,)
    assert reopened.graph.query("SalesOrder") == [
        {"id": "O1", "order_number": "O1", "type": "SalesOrder"}
    ]
    assert reopened.graph.query("InventoryUnit") == [
        {"id": "X1", "product_code": "X", "type": "InventoryUnit"}
    ]
    assert reopened.graph.query_relations("OrderContainsUnit") == [
        {
            "key": "contains:O1:X1",
            "relation_type": "ORDER_CONTAINS_UNIT",
            "source_id": "O1",
            "target_id": "X1",
            "type": "OrderContainsUnit",
        }
    ]
    assert reopened.graph.query("SupplierOrderState") == [
        {
            "id": "supplier-order-state:B:e7",
            "ordered_quantity": 2,
            "product_code": "Y",
            "source_occurrence_id": "e7",
            "supplier_order_id": "B",
            "type": "SupplierOrderState",
        }
    ]
    assert (
        reopened.record_history["supplier-order-state:B:e4"].superseded_by
        == "supplier-order-state:B:e7"
    )
    assert reopened.receipt == e7.receipt

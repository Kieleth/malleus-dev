"""Full Small Shop conformance run through the public population facade."""

from __future__ import annotations

import ast
from importlib import import_module
import json
from pathlib import Path

import malleus.compiler as compiler


HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
OLD_GRAPH = HERE.parent / "showcase/evidence/graph.json"
EXPECTED_EVIDENCE = HERE / "evidence.json"
DATA_SOURCES = {
    "source:small-shop:inventory": (
        ROOT
        / "research/ontology_driven_kg_realization/fixtures"
        / "small_shop_fulfilment/input/sources/inventory-units.csv"
    ),
    "source:small-shop:invoices": (
        ROOT
        / "research/ontology_driven_kg_realization/fixtures"
        / "small_shop_fulfilment_settlement_v1/input/sources/invoices.csv"
    ),
    "source:small-shop:payments": (
        ROOT
        / "research/ontology_driven_kg_realization/fixtures"
        / "small_shop_fulfilment_settlement_v1/input/sources/payments.jsonl"
    ),
    "source:small-shop:supplier-orders": (
        ROOT
        / "research/ontology_driven_kg_realization/fixtures"
        / "small_shop_fulfilment_correction_v1/input/sources"
        / "supplier-order-history.jsonl"
    ),
    "source:small-shop:warehouse": (
        ROOT
        / "research/ontology_driven_kg_realization/fixtures"
        / "small_shop_fulfilment/input/sources/warehouse.jsonl"
    ),
}
CURRENT_RECORD_IDS = {
    "O1",
    "X1",
    "contains:O1:X1",
    "invoice:I1",
    "invoice:I2",
    "payment:P1",
    "relation:P1:I1",
    "relation:P1:I2",
    "supplier-order-state:B:e7",
}
HISTORICAL_RECORD_IDS = CURRENT_RECORD_IDS | {"supplier-order-state:B:e4"}


def _module():
    return import_module(
        "research.ontology_driven_kg_realization.experiments.small_shop"
        ".public_population.run"
    )


def test_full_run_uses_only_the_public_core_facade() -> None:
    module = _module()
    source = Path(module.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    malleus_imports = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module is not None
        and node.module.startswith("malleus")
    } | {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
        if alias.name.startswith("malleus")
    }

    assert malleus_imports == {"malleus.compiler"}
    assert "_contract_pipeline" not in source
    assert tuple(path.name for path in module.PLAN_PATHS) == (
        "ret010.json",
        "invoice-base.json",
        "payment-e30.json",
        "supplier-e4.json",
        "supplier-e7.json",
    )


def test_full_run_admits_reopens_queries_and_traces_every_record(
    tmp_path: Path,
) -> None:
    module = _module()
    output = tmp_path / "full-shop"

    first = module.run_full_shop(output)
    ledger_before_trace = (output / "history.jsonl").read_bytes()
    second = module.run_full_shop(output)

    assert first.evidence_bytes == second.evidence_bytes
    assert first.evidence_bytes == EXPECTED_EVIDENCE.read_bytes()
    assert first.replay.receipt == second.replay.receipt
    assert (output / "history.jsonl").read_bytes() == ledger_before_trace

    old_graph = json.loads(OLD_GRAPH.read_bytes())
    new_graph = second.replay.graph.snapshot()
    assert new_graph["nodes"] == old_graph["nodes"]
    assert new_graph["relations"] == old_graph["relations"]
    assert set(second.replay.record_history) == HISTORICAL_RECORD_IDS
    assert {record["id"] for record in new_graph["nodes"]} | {
        record["key"] for record in new_graph["relations"]
    } == CURRENT_RECORD_IDS
    assert len(second.replay.change_sets) == 5
    assert len(second.replay.contract_revisions) == 1
    assert len({change.contract_identity for change in second.replay.change_sets}) == 2

    expected_source_bytes = {
        identifier: path.read_bytes() for identifier, path in DATA_SOURCES.items()
    }
    observed_sources: set[str] = set()
    observed_plans: set[str] = set()
    plan_paths = {
        json.loads(path.read_bytes())["plan_id"]: path for path in module.PLAN_PATHS
    }
    for record_id, history in second.replay.record_history.items():
        trace = compiler.trace_population_record(second.replay, record_id)
        assert trace.history_profile == compiler.STATE_VERSION_PROFILE
        assert trace.record_history == history
        assert trace.change_set.change_set_id == history.change_set_id
        assert trace.population_plan_identity.startswith("sha256:")
        assert trace.population_plan_bytes == second.replay.retained_bytes(
            trace.population_plan["plan_id"]
        )
        assert (
            trace.population_plan_bytes
            == plan_paths[trace.population_plan["plan_id"]].read_bytes()
        )
        assert trace.sources
        assert trace.evidence
        assert all(
            member.content == expected_source_bytes[member.record_id]
            for member in trace.sources
        )
        observed_sources.update(member.record_id for member in trace.sources)
        observed_plans.add(trace.population_plan["plan_id"])

        operation = history.operation
        expected_paths = {("properties", field) for field in operation.properties}
        if operation.operation_type == "CREATE_RELATION":
            expected_paths |= {("source_id",), ("target_id",)}
        assert {tuple(item["path"]) for item in trace.derivations} == expected_paths

    assert observed_sources == set(DATA_SOURCES)
    assert observed_plans == {
        "plan:small-shop:ret010",
        "plan:small-shop:invoice-base",
        "plan:small-shop:payment-e30",
        "plan:small-shop:supplier-e4",
        "plan:small-shop:supplier-e7",
    }
    assert (
        second.replay.record_history["supplier-order-state:B:e4"].superseded_by
        == "supplier-order-state:B:e7"
    )
    assert (
        second.replay.record_history["supplier-order-state:B:e7"].supersedes_record_id
        == "supplier-order-state:B:e4"
    )
    assert (output / "history.jsonl").read_bytes() == ledger_before_trace

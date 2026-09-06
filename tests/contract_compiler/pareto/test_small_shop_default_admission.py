"""The full Shop uses Core's admission checks, not caller-made outcomes."""

from __future__ import annotations

import ast
from hashlib import sha256
from importlib import import_module
import json
from pathlib import Path
import shutil

import pytest

import malleus.compiler as api


ROOT = Path(__file__).resolve().parents[3]
SHOP = ROOT / "research/ontology_driven_kg_realization/experiments/small_shop"
BASELINE = SHOP / "public_population"
MODULE = (
    "research.ontology_driven_kg_realization.experiments.small_shop"
    ".default_admission.run"
)
CURRENT = {
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
PRIOR = "supplier-order-state:B:e4"
TIMES = tuple(f"2026-09-06T00:{minute:02d}:00Z" for minute in range(10))
ACTOR = "actor:shop-default-conformance"


def _example():
    return import_module(MODULE)


def _digest(content: bytes) -> str:
    return "sha256:" + sha256(content).hexdigest()


def _before_payment(path: Path):
    example = _example()
    history = example.start_shop(path, transaction_time=TIMES[0], actor_id=ACTOR)
    example.accept_plan(history, "ret010", transaction_time=TIMES[1], actor_id=ACTOR)
    example.revise_shop(history, transaction_time=TIMES[2], actor_id=ACTOR)
    example.accept_plan(
        history, "invoice-base", transaction_time=TIMES[3], actor_id=ACTOR
    )
    return history


def test_example_uses_public_default_admission_without_asserting_outcomes() -> None:
    example = _example()
    source = Path(example.__file__).read_text()
    tree = ast.parse(source)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            imports.add(node.module or "")
        elif isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
    assert {name for name in imports if name.startswith("malleus")} == {
        "malleus.compiler"
    }
    assert not any(name.startswith("research.") for name in imports)
    assert "_contract_pipeline" not in source
    assert "CHECK_RECORDED" not in source
    assert "SATISFIED" not in source
    called = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert {
        "create_structural_history",
        "population_retention_events",
        "admit_structural_change",
    } <= called
    assert "admit" not in called
    assert "ProtocolMachineProgram.from_bytes" not in source
    assert "PolicyProgram.from_bytes" not in source


def test_full_shop_reopens_from_ledger_alone_and_traces_both_versions(
    tmp_path: Path,
) -> None:
    example = _example()
    first = example.run_shop(tmp_path / "first")
    history_bytes = (tmp_path / "first/history.jsonl").read_bytes()
    second = example.run_shop(tmp_path / "second")
    assert (tmp_path / "second/history.jsonl").read_bytes() == history_bytes
    assert (tmp_path / "first/evidence.json").read_bytes() == (
        tmp_path / "second/evidence.json"
    ).read_bytes()
    assert first.receipt == second.receipt

    isolated = tmp_path / "reopened/history.jsonl"
    isolated.parent.mkdir()
    shutil.copyfile(tmp_path / "first/history.jsonl", isolated)
    reopened = api.KnowledgeChangeHistory.reopen(isolated).replay()
    assert reopened.receipt == first.receipt
    assert reopened.graph.export_records() == first.graph.export_records()
    assert len(reopened.change_sets) == 5
    assert len(reopened.contract_revisions) == 1
    assert len({item.contract_identity for item in reopened.change_sets}) == 2
    graph = reopened.graph.snapshot()
    expected = json.loads((BASELINE / "evidence.json").read_bytes())["graph"]
    assert graph["nodes"] == expected["nodes"]
    assert graph["relations"] == expected["relations"]
    assert set(reopened.record_history) == CURRENT | {PRIOR}
    assert {row["id"] for row in graph["nodes"]} | {
        row["key"] for row in graph["relations"]
    } == CURRENT
    assert (
        reopened.graph.query("SupplierOrderState", supplier_order_id="B")[0][
            "ordered_quantity"
        ]
        == 2
    )
    assert {
        row["target_id"]
        for row in reopened.graph.query_relations("PaymentSettlesInvoiceRelation")
    } == {"invoice:I1", "invoice:I2"}

    checks = [
        record
        for record in reopened.machine_state.records
        if record.record_type == "CheckRecord"
    ]
    assert len(checks) == 5
    bundle = api.STRUCTURAL_HISTORY_BUNDLE
    assert all(
        record.fields["check_contract_identity"] == bundle.check_contract_identity
        for record in checks
    )
    assert all(record.fields["outcome"] == bundle.success_outcome for record in checks)

    for record_id in sorted(CURRENT | {PRIOR}):
        trace = api.trace_population_record(reopened, record_id)
        assert trace.history_profile == api.STATE_VERSION_PROFILE
        assert (
            trace.population_plan["contract_identity"]
            == trace.change_set.contract_identity
        )
        assert trace.sources and trace.derivations
        assert all(_digest(item.content) == item.identity for item in trace.sources)
        assert trace.population_plan_bytes == reopened.retained_bytes(
            trace.population_plan["plan_id"]
        )
    assert reopened.record_history[PRIOR].superseded_by == "supplier-order-state:B:e7"
    assert (
        reopened.record_history["supplier-order-state:B:e7"].supersedes_record_id
        == PRIOR
    )
    before_correction = reopened.graph_at_change("change:plan:small-shop:supplier-e4")
    assert before_correction.query("SupplierOrderState")[0]["ordered_quantity"] == 1
    assert [
        node for node in before_correction.snapshot()["nodes"] if node["id"] != PRIOR
    ] == [node for node in graph["nodes"] if node["id"] != "supplier-order-state:B:e7"]
    assert before_correction.snapshot()["relations"] == graph["relations"]
    assert isolated.read_bytes() == history_bytes


def test_rebound_plans_retain_templates_without_changing_domain_choices(
    tmp_path: Path,
) -> None:
    replay = _example().run_shop(tmp_path / "shop")
    for change in replay.change_sets:
        record_id = change.operations[0].record_id
        trace = api.trace_population_record(replay, record_id)
        name = trace.population_plan["plan_id"].removeprefix("plan:small-shop:")
        template_bytes = (BASELINE / "plans" / f"{name}.json").read_bytes()
        template = json.loads(template_bytes)
        rebound = json.loads(trace.population_plan_bytes)
        assert rebound.pop("contract_identity") != template.pop("contract_identity")
        assert rebound == template
        assert replay.retained_bytes(f"template:small-shop:{name}") == template_bytes


def test_stale_payment_preparation_refuses_without_further_mutation(
    tmp_path: Path,
) -> None:
    example = _example()
    history = _before_payment(tmp_path / "history.jsonl")
    plan = example.plan_for(history, "payment-e30")
    prepared = example.prepare_plan(
        history, plan, transaction_time=TIMES[4], actor_id=ACTOR
    )
    example.accept_plan(
        history, "supplier-e4", transaction_time=TIMES[5], actor_id=ACTOR
    )
    before_bytes = history.path.read_bytes()
    before = history.replay()
    with pytest.raises(api.KnowledgeChangeRefusal) as refused:
        api.admit_structural_change(
            history=history,
            preparation=prepared,
            transaction_time=TIMES[6],
            actor_id=ACTOR,
        )
    assert refused.value.reason is api.KnowledgeChangeRefusalReason.STALE_BASE
    assert history.path.read_bytes() == before_bytes
    after = api.KnowledgeChangeHistory.reopen(history.path).replay()
    assert after.receipt == before.receipt
    assert after.graph.export_records() == before.graph.export_records()
    assert after.graph.query("Payment") == []


def test_broken_payment_endpoint_refuses_before_any_retention_or_population(
    tmp_path: Path,
) -> None:
    example = _example()
    history = _before_payment(tmp_path / "history.jsonl")
    plan = example.plan_for(history, "payment-e30")
    plan["records"]["relations"][1]["target_id"] = "invoice:missing"
    before_bytes = history.path.read_bytes()
    before = history.replay()
    with pytest.raises(api.PopulationPlanRefusal) as refused:
        example.prepare_plan(history, plan, transaction_time=TIMES[4], actor_id=ACTOR)
    assert refused.value.reason is api.PopulationPlanRefusalReason.DANGLING_ENDPOINT
    assert history.path.read_bytes() == before_bytes
    after = api.KnowledgeChangeHistory.reopen(history.path).replay()
    assert after.receipt == before.receipt
    assert after.graph.export_records() == before.graph.export_records()
    assert after.graph.query("Payment") == []

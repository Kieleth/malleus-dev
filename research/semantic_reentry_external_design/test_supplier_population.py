"""Authored-source compatibility, not capture, action execution or admission."""

from importlib import import_module
import json
from pathlib import Path

import malleus.compiler as api
from research.semantic_reentry_external_design.test_supplier_components import (
    FIXTURE,
    MODULE,
    SOURCE_ID,
    digest,
    mapper,
)
from research.semantic_reentry_protocol.test_prerequisites import (
    ACTOR,
    E4,
    TIME,
    artifact,
    event,
    load_plan,
)


def test_gate_paths_and_public_runtime_belong_to_selected_checkout():
    root = Path(__file__).resolve().parents[2]
    gate = json.loads(
        Path(__file__).with_name("supplier-component-gate.json").read_bytes()
    )
    assert set(gate) == {"classification", "claim", "tests"}
    assert gate["classification"] == "CONFORMANCE_FIXTURE"
    assert len(gate["tests"]) == len(set(gate["tests"]))
    assert str(Path(__file__).resolve().relative_to(root)) in gate["tests"]
    for name in gate["tests"]:
        path = (root / name).resolve()
        assert path.is_relative_to(root) and path.is_file(), (
            f"Gate input absent from selected checkout: {name}"
        )
    assert Path(api.__file__).resolve().is_relative_to(root / "src")
    assert (
        Path(import_module(MODULE).__file__).resolve().is_relative_to(root / "research")
    )


def test_authored_source_mapping_compiles_without_knowledge_or_ledger_change(
    shop,
    inputs,
    supplied_after,
):
    # Retention is explicit fixture setup, not a component capability or capture.
    # The legacy shop setup already contains e7. This test does not use that row.
    history, path = shop
    mapping_id = "artifact:reentry:supplier:authored-component-mapping"
    source_artifact = "artifact:reentry:supplier:authored-component-input"
    mapping_bytes = (FIXTURE / "case.json").read_bytes()
    initial = history.replay()
    history.append_anchors(
        anchors=(
            artifact(mapping_id, mapping_bytes),
            artifact(
                source_artifact,
                supplied_after,
                "SOURCE_ARTIFACT",
                "application/x-ndjson",
            ),
            api.KnowledgeAnchorInput(
                machine_event=event(
                    "SOURCE_REGISTERED",
                    artifact_id=source_artifact,
                    source_id=SOURCE_ID,
                    source_identity=digest(supplied_after),
                ),
                retained_bytes=supplied_after,
                media_type="application/x-ndjson",
                role="RETAINED_SOURCE",
            ),
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    assert history.replay().graph.state_digest() == initial.graph.state_digest()
    replay = history.replay()
    ledger_before = path.read_bytes()
    implementation_bytes = Path(import_module(MODULE).__file__).read_bytes()
    plan = load_plan(history, "supplier-e7")
    plan.update(json.loads(mapper(inputs, supplied_after)))
    plan["plan_id"] = "plan:reentry:supplier:authored-component-compatibility"
    plan["adapter"] = {"adapter_id": MODULE, "version": digest(implementation_bytes)}
    plan["evidence"] = [{"evidence_id": mapping_id, "sha256": digest(mapping_bytes)}]
    compiled = api.compile_population_plan(
        plan,
        partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=api.PopulationBaseState.from_replay(replay),
        history_profile=api.STATE_VERSION_PROFILE,
    )
    assert compiled.status is api.PopulationPlanStatus.CHANGE_SET
    assert len(compiled.operations) == 1
    operation = compiled.operations[0]
    assert operation.record_id == inputs["mapping"]["replacement_record_id"]
    assert operation.record_type == "SupplierOrderState"
    assert dict(operation.properties) == {
        "supplier_order_id": "B",
        "product_code": "Y",
        "ordered_quantity": 2,
        "source_occurrence_id": "reentry-amendment-1",
    }
    assert operation.supersedes_record_id == E4
    assert compiled.source_record_ids == (SOURCE_ID,)
    # The Core compiler owns the complete profile/plan/mapping evidence closure.
    assert compiled.evidence_record_ids == (
        "profile:state-version",
        plan["plan_id"],
        mapping_id,
    )
    assert compiled.valid_time == api.KnowledgeValidTime(
        "ORDER_ONLY", "reentry-amendment-1"
    )
    assert all(item["locator"].startswith("row:0:") for item in plan["derivations"])
    assert replay.retained_bytes(SOURCE_ID) == supplied_after
    assert path.read_bytes() == ledger_before
    assert history.replay().receipt == replay.receipt
    assert history.replay().graph.export_records() == initial.graph.export_records()
    assert history.replay().record_history == initial.record_history
    assert (
        history.replay().graph.query("SupplierOrderState", supplier_order_id="B")[0][
            "ordered_quantity"
        ]
        == 1
    )

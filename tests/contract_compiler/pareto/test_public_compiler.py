"""Public adopter contract for compiler, population, history, and query."""

from __future__ import annotations

from hashlib import sha256
from importlib import import_module
from importlib.resources import files
import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[3]
SHOP_FIXTURE = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "small_shop_fulfilment_correction_v1"
)
SHOP_BASE = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "small_shop_fulfilment/input/tbox/small-shop.yaml"
)
SHOP_RUNTIME = (
    ROOT / "research/ontology_driven_kg_realization/experiments/small_shop/pareto"
)
EXAMPLES = ROOT / "handover/2026-09-03-core-population-v2/examples"
TRANSACTION_TIME = "2026-09-03T00:00:00Z"


def _api():
    return import_module("malleus.compiler")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _event(event_type: str, **payload: object) -> bytes:
    return _canonical({"event_type": event_type, "payload": payload})


def _shop_sources() -> dict[str, bytes]:
    return {
        "small-shop-correction": (
            SHOP_FIXTURE / "input/tbox/small-shop-correction.yaml"
        ).read_bytes(),
        "small-shop": SHOP_BASE.read_bytes(),
        "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
        "linkml:types": (
            files("linkml_runtime")
            .joinpath("linkml_model", "model", "schema", "types.yaml")
            .read_bytes()
        ),
    }


def _compiled_shop(api):
    return api.compile_linkml_contract(
        root_locator="small-shop-correction",
        sources=_shop_sources(),
    )


def _runtime(api, compiled, path: Path):
    machine = api.ProtocolMachineProgram.from_bytes(
        (SHOP_RUNTIME / "machine.json").read_bytes()
    )
    policy = api.PolicyProgram.from_bytes((SHOP_RUNTIME / "policy.json").read_bytes())
    normative = api.compose_normative_profile(
        protocol_machine_program=machine,
        policy_programs={"required-check-verdict": policy},
        capability_refs=(),
    )
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256,
        normative_profile=normative,
    )
    mapping = json.loads((SHOP_RUNTIME / "mapping.json").read_bytes())
    binding = api.KnowledgeChangeHistoryBinding.from_bytes(
        _canonical(mapping["history_binding"])
    )
    return (
        api.KnowledgeChangeHistory(
            path,
            partial_contract=partial,
            contract_view=compiled.view,
            binding=binding,
        ),
        partial,
        policy,
    )


def _anchor(history, event: bytes, content: bytes, role: str) -> None:
    result = history.append_anchor(
        machine_event=event,
        retained_bytes=content,
        media_type="application/octet-stream",
        role=role,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:public-adopter",
    )
    assert result.machine_receipt.outcome == "APPLIED"


def _bootstrap(api, history, compiled, partial, source: bytes) -> None:
    binding = history.binding
    anchors = (
        (
            "artifact:validated-contract",
            compiled.artifact.artifact_bytes,
            "VALIDATED_CONTRACT",
        ),
        (
            "artifact:partial-contract",
            partial.canonical_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        (
            "artifact:history-binding",
            binding.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        ("artifact:supplier-order-source", source, "SOURCE_ARTIFACT"),
    )
    for record_id, content, role in anchors:
        _anchor(
            history,
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id=record_id,
                artifact_identity=_digest(content),
            ),
            content,
            role,
        )
    _anchor(
        history,
        _event(
            "SOURCE_REGISTERED",
            artifact_id="artifact:supplier-order-source",
            source_id="source:supplier-order-history",
            source_identity=_digest(source),
        ),
        source,
        "RETAINED_SOURCE",
    )


def _plan(api, partial, source: bytes, occurrence: str) -> dict[str, object]:
    plan = json.loads((EXAMPLES / f"small-shop-plan-{occurrence}.json").read_bytes())
    plan["contract_identity"] = partial.identity
    plan["history_profile"]["sha256"] = api.STATE_VERSION_PROFILE.identity
    plan["sources"][0]["sha256"] = _digest(source)
    return plan


def _retention_events(api, plan: dict[str, object], include_profile: bool):
    events = {
        plan["plan_id"]: _event(
            "ARTIFACT_REGISTERED",
            artifact_id=plan["plan_id"],
            artifact_identity=_digest(_canonical(plan)),
        )
    }
    if include_profile:
        events["profile:state-version"] = _event(
            "ARTIFACT_REGISTERED",
            artifact_id="profile:state-version",
            artifact_identity=api.STATE_VERSION_PROFILE.identity,
        )
    return events


def _protocol_events(policy, change_set, state_identity: str, suffix: str):
    proposal_id = f"proposal:public:{suffix}"
    events = [
        _event(
            "CHANGE_PROPOSED",
            expected_machine_state_identity=state_identity,
            knowledge_change_set_identity=change_set.identity,
            policy_id=policy.identifier,
            policy_identity=policy.identity,
            proposal_id=proposal_id,
        )
    ]
    events.extend(
        _event(
            "CHECK_RECORDED",
            check_contract_id=check_id,
            check_contract_identity=check_identity,
            outcome="SATISFIED",
            policy_identity=policy.identity,
            proposal_id=proposal_id,
            receipt_id=f"receipt:public:{suffix}:{ordinal}",
        )
        for ordinal, (check_id, check_identity) in enumerate(policy.required_checks)
    )
    events.append(
        _event(
            "VERDICT_RECORDED",
            decision_id=f"decision:public:{suffix}",
            proposal_id=proposal_id,
        )
    )
    return tuple(events)


def _prepare_and_admit(api, history, partial, policy, source, occurrence: str):
    plan = _plan(api, partial, source, occurrence)
    prepared = api.prepare_population_change(
        history=history,
        plan=plan,
        profile=json.loads(api.STATE_VERSION_PROFILE.canonical_bytes),
        retention_events=_retention_events(api, plan, occurrence == "e4"),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:public-adopter",
    )
    assert prepared.change_set is not None
    return history.admit(
        change_set=prepared.change_set,
        machine_events=_protocol_events(
            policy,
            prepared.change_set,
            prepared.retention_replay.machine_state.identity,
            occurrence,
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:public-adopter",
    )


def test_public_module_exposes_the_executable_pipeline_without_private_imports() -> (
    None
):
    api = _api()
    required = {
        "KnowledgeChangeHistory",
        "KnowledgeChangeHistoryBinding",
        "PopulationBaseState",
        "PopulationPlanRefusal",
        "PopulationPlanRefusalReason",
        "ProtocolMachineProgram",
        "PolicyProgram",
        "STATE_VERSION_PROFILE",
        "compile_linkml_contract",
        "compile_population_plan",
        "compose_normative_profile",
        "compose_partial_effective_contract",
        "prepare_population_change",
    }

    assert required <= set(api.__all__)
    source = Path(__file__).read_text(encoding="utf-8")
    assert "from malleus._contract_pipeline" not in source
    assert "import malleus._contract_pipeline" not in source
    assert "import research." not in source
    assert "from research." not in source


def test_public_adopter_compiles_admits_reopens_and_queries_e4_e7(
    tmp_path: Path,
) -> None:
    api = _api()
    compiled = _compiled_shop(api)
    history, partial, policy = _runtime(
        api, compiled, tmp_path / "small-shop-history.jsonl"
    )
    source = (SHOP_FIXTURE / "input/sources/supplier-order-history.jsonl").read_bytes()
    _bootstrap(api, history, compiled, partial, source)

    _prepare_and_admit(api, history, partial, policy, source, "e4")
    admitted = _prepare_and_admit(api, history, partial, policy, source, "e7")
    reopened = api.KnowledgeChangeHistory.reopen(history.path).replay()

    expected = [
        {
            "id": "supplier-order-state:B:e7",
            "ordered_quantity": 2,
            "product_code": "Y",
            "source_occurrence_id": "e7",
            "supplier_order_id": "B",
            "type": "SupplierOrderState",
        }
    ]
    assert admitted.graph.query("SupplierOrderState", supplier_order_id="B") == expected
    assert reopened.graph.query("SupplierOrderState", supplier_order_id="B") == expected
    assert (
        reopened.record_history["supplier-order-state:B:e4"].superseded_by
        == "supplier-order-state:B:e7"
    )
    assert reopened.receipt == admitted.receipt


def test_public_population_refuses_event_records_by_family() -> None:
    api = _api()
    compiled = _compiled_shop(api)
    machine = api.ProtocolMachineProgram.from_bytes(
        (SHOP_RUNTIME / "machine.json").read_bytes()
    )
    policy = api.PolicyProgram.from_bytes((SHOP_RUNTIME / "policy.json").read_bytes())
    normative = api.compose_normative_profile(
        protocol_machine_program=machine,
        policy_programs={"required-check-verdict": policy},
        capability_refs=(),
    )
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256,
        normative_profile=normative,
    )
    source = (SHOP_FIXTURE / "input/sources/supplier-order-history.jsonl").read_bytes()
    plan = _plan(api, partial, source, "e4")
    plan["history_profile"] = {
        "profile_id": "domain-history-not-selected",
        "sha256": "sha256:" + "0" * 64,
    }
    plan["records"]["events"] = [
        {"id": "event:1", "properties": {}, "type": "DomainEvent"}
    ]

    with pytest.raises(api.PopulationPlanRefusal) as refusal:
        api.compile_population_plan(
            plan,
            partial_contract=partial,
            contract_view=compiled.view,
            base_state=api.PopulationBaseState.empty(),
        )

    assert refusal.value.reason is api.PopulationPlanRefusalReason.FAMILY_NOT_ADMITTED


def test_compiler_cli_compiles_exact_named_sources() -> None:
    command = [
        sys.executable,
        "-m",
        "malleus.compiler_cli",
        "contract",
        "--root",
        "small-shop-correction",
    ]
    for locator, path in (
        (
            "small-shop-correction",
            SHOP_FIXTURE / "input/tbox/small-shop-correction.yaml",
        ),
        ("small-shop", SHOP_BASE),
        ("malleus", ROOT / "ontology/malleus.yaml"),
        (
            "linkml:types",
            Path(
                str(
                    files("linkml_runtime").joinpath(
                        "linkml_model", "model", "schema", "types.yaml"
                    )
                )
            ),
        ),
    ):
        command.extend(("--source", locator, str(path)))

    result = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)

    assert result.returncode == 0, result.stderr.decode()
    artifact = json.loads(result.stdout)
    assert artifact["grammar"] == "malleus.validated-contract-artifact/private-v0"
    assert "ontology-digest" not in result.args

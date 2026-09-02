"""Pareto RED contract for the private RET-010 source-to-query vertical."""

from __future__ import annotations

import ast
from hashlib import sha256
import inspect
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

import research.ontology_driven_kg_realization.experiments.small_shop.pareto.ret010 as ret010_module
from research.ontology_driven_kg_realization.experiments.small_shop.pareto.ret010 import (
    Ret010Refusal,
    Ret010RefusalReason,
    load_ret010_vertical,
    run_ret010,
)


ROOT = Path(__file__).resolve().parents[5]
FIXTURE = (
    ROOT
    / "research"
    / "ontology_driven_kg_realization"
    / "fixtures"
    / "small_shop_fulfilment"
)
PARETO = Path(__file__).parent
MACHINE = PARETO / "machine.json"
POLICY = PARETO / "policy.json"
MAPPING = PARETO / "mapping.json"
ORACLE = FIXTURE / "oracle/ret-000-ret-010.json"
FROZEN_SHA256 = {
    "input/configuration/ret-010-selection.json": (
        "11000db0f0262137a7c0075987c7d7202452ab32232f8e94fa8821f80b8a1af7"
    ),
    "input/configuration/time-context.json": (
        "799cae6f980615a087e3d97bdc824ceda4410be2c93d92723829cd96c9a00561"
    ),
    "input/manifest.json": (
        "7583bfbc6f9aff6382727a7befa333c82b73bed221d8958d6bb7e1a55d0549e8"
    ),
    "input/sources/inventory-units.csv": (
        "2e18a2a88c5964b80036799fe9f044d91e4dc790789b701df5f50a86c24a59ec"
    ),
    "input/sources/warehouse.jsonl": (
        "6ff31debb3603892de9d015f4e412da9f40a4add384f3f939b506ab7066e640e"
    ),
    "input/tbox/small-shop-description-only.yaml": (
        "e4a5898ccf85493c7a866c3891055ffe4ecb776361dfc1306b538627c7b6c74f"
    ),
    "input/tbox/small-shop-root-instances.yaml": (
        "fbb37113a0546a0e1dced65579e830fbdc4087c918b4d98a534852a574eb961b"
    ),
    "input/tbox/small-shop.yaml": (
        "f374c7f1c1cba4ecbf747ca9471511307ea5cca1051540d5bf533a17360ca528"
    ),
    "oracle/ret-000-ret-010.json": (
        "4565c5f2dd84670c762c0a53e5a0868fe8cab6f1781a9757ecb41581e7f32fcc"
    ),
    "oracle/tbox-expectations.json": (
        "0a8d3fdae6f16117643d898eb7576022e61700d3f83d286ff164fb66f6ae0f31"
    ),
}


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_bytes())


def _write_canonical(path: Path, value: object) -> None:
    path.write_bytes(_canonical(value))


def _rebind_member(fixture: Path, relative: str) -> None:
    manifest_path = fixture / "input/manifest.json"
    manifest = _load(manifest_path)
    member = next(item for item in manifest["members"] if item["path"] == relative)
    content = (fixture / "input" / relative).read_bytes()
    member["byte_length"] = len(content)
    member["sha256"] = "sha256:" + sha256(content).hexdigest()
    _write_canonical(manifest_path, manifest)


def _rebind_mapping(mapping_path: Path, fixture: Path) -> None:
    mapping = _load(mapping_path)
    mapping["input_manifest_sha256"] = "sha256:" + _digest(
        fixture / "input/manifest.json"
    )
    _write_canonical(mapping_path, mapping)


def _run(
    ledger: Path,
    *,
    fixture: Path = FIXTURE,
    mapping: Path = MAPPING,
):
    return run_ret010(
        ledger,
        fixture_root=fixture,
        machine_path=MACHINE,
        policy_path=POLICY,
        mapping_path=mapping,
    )


def test_frozen_fixture_and_private_program_data_are_explicit() -> None:
    assert {relative: _digest(FIXTURE / relative) for relative in FROZEN_SHA256} == (
        FROZEN_SHA256
    )
    assert all(path.is_file() for path in (MACHINE, POLICY, MAPPING))

    artifacts = {path: _load(path) for path in (MACHINE, POLICY, MAPPING)}
    assert all(path.read_bytes() == _canonical(artifacts[path]) for path in artifacts)
    machine, policy, mapping = (artifacts[path] for path in (MACHINE, POLICY, MAPPING))
    assert machine["grammar"] == "malleus.protocol-machine/private-v0"
    assert machine["capabilities"] == []
    assert {item["check_contract_id"] for item in policy["required_checks"]} == {
        "retained-source-integrity",
        "structural-conformance",
    }
    assert policy["outcome_verdicts"] == {
        "SATISFIED": "ACCEPT",
        "UNKNOWN": "DEFER",
        "VIOLATED": "REJECT",
    }
    assert mapping["input_manifest_sha256"] == (
        "sha256:" + FROZEN_SHA256["input/manifest.json"]
    )
    assert mapping["selection_id"] == "RET-010"
    assert mapping["selection"]["ordinal_base"] == 1
    assert mapping["selection"]["record_order"] == "SOURCE_ORDER"
    assert mapping["valid_time"] == "2000-05-07T17:00:00Z"
    assert [item["ordinal"] for item in mapping["operations"]] == [0, 1, 2]
    assert [item["record_id"] for item in mapping["operations"]] == [
        "O1",
        "X1",
        "contains:O1:X1",
    ]
    assert "oracle" not in json.dumps(mapping).lower()
    assert mapping["publication_contract"] == (
        "PRIVATE_FIXTURE_LOCAL_NO_PUBLIC_ABOX_FORMAT"
    )


@pytest.mark.parametrize("mutation", ["unknown", "missing"])
def test_mapping_has_one_closed_required_root_schema(
    tmp_path: Path, mutation: str
) -> None:
    payload = _load(MAPPING)
    expected_fields = {
        "actor_id",
        "anchor_events",
        "artifact_ids",
        "artifact_roles",
        "change_set",
        "compiler",
        "grammar",
        "history_binding",
        "input_manifest_sha256",
        "inventory_lookup",
        "operation_bindings",
        "operations",
        "policy_ref",
        "protocol",
        "publication_contract",
        "selection",
        "selection_id",
        "source_artifact_id_prefix",
        "time",
        "transaction_time",
        "valid_time",
    }
    assert set(payload) == expected_fields
    if mutation == "unknown":
        payload["unknown_semantic_switch"] = "ACCEPT"
    else:
        del payload["history_binding"]
    changed = tmp_path / "mapping.json"
    _write_canonical(changed, payload)

    with pytest.raises(Ret010Refusal) as refusal:
        load_ret010_vertical(
            fixture_root=FIXTURE,
            machine_path=MACHINE,
            policy_path=POLICY,
            mapping_path=changed,
        )
    assert refusal.value.reason is Ret010RefusalReason.MALFORMED_CONFIGURATION


@pytest.mark.parametrize("mutation", ["unknown_root", "empty_root", "missing_paths"])
def test_operation_bindings_cannot_skip_retained_values(
    tmp_path: Path, mutation: str
) -> None:
    payload = _load(MAPPING)
    payload["operations"][1]["properties"]["product_code"] = "Y"
    binding = next(
        item
        for item in payload["operation_bindings"]
        if item["input_path"] == ["lookup", "product_code"]
    )
    if mutation == "unknown_root":
        binding["input_path"] = ["lookpu", "product_code"]
    elif mutation == "empty_root":
        binding["input_path"] = []
    else:
        binding["input_path"] = ["lookup", "missing"]
        binding["operation_path"] = ["properties", "missing"]
    mapping = tmp_path / "mapping.json"
    _write_canonical(mapping, payload)
    ledger = tmp_path / "semantic.jsonl"

    with pytest.raises(Ret010Refusal) as refusal:
        _run(ledger, mapping=mapping)
    assert refusal.value.reason is Ret010RefusalReason.MALFORMED_CONFIGURATION
    assert not ledger.exists()


def test_unknown_source_record_order_refuses(tmp_path: Path) -> None:
    payload = _load(MAPPING)
    payload["selection"]["record_order"] = "UNDECLARED_ORDER"
    mapping = tmp_path / "mapping.json"
    _write_canonical(mapping, payload)
    ledger = tmp_path / "semantic.jsonl"

    with pytest.raises(Ret010Refusal) as refusal:
        _run(ledger, mapping=mapping)
    assert refusal.value.reason is Ret010RefusalReason.MALFORMED_CONFIGURATION
    assert not ledger.exists()


def test_source_to_ledger_to_query_vertical_matches_independent_oracle(
    tmp_path: Path,
) -> None:
    from malleus._contract_pipeline.knowledge import KnowledgeChangeHistory

    fixture = tmp_path / "fixture-without-answer-key"
    shutil.copytree(FIXTURE / "input", fixture / "input")
    ledger = tmp_path / "state/semantic.jsonl"
    result = _run(ledger, fixture=fixture)

    oracle = _load(ORACLE)["cases"]["RET-010"]["expected_outputs"]
    receipt = json.loads(result.receipt.canonical_bytes)
    assert result.receipt.canonical_bytes == _canonical(receipt)
    assert set(receipt) == {
        "contract_identity",
        "graph_state_digest",
        "history_binding_identity",
        "knowledge_change_set_identity",
        "ledger_event_count",
        "ledger_head",
        "machine_identity",
        "machine_state_identity",
        "policy_identity",
        "queries",
        "source_identities",
        "validated_fact_set_sha256",
    }
    assert receipt["contract_identity"] == result.effective_contract.identity
    assert receipt["machine_identity"] == result.machine_program.identity
    assert receipt["policy_identity"] == result.policy_program.identity
    assert receipt["knowledge_change_set_identity"] == result.change_set.identity
    assert receipt["ledger_head"] == result.replay.ledger_head
    assert receipt["ledger_event_count"] == result.replay.ledger_event_count
    assert receipt["machine_state_identity"] == result.replay.machine_state.identity
    assert receipt["graph_state_digest"] == result.replay.graph.state_digest()
    assert receipt["source_identities"] == {
        relative: "sha256:" + digest
        for relative, digest in FROZEN_SHA256.items()
        if relative.startswith("input/")
    }
    assert [operation.ordinal for operation in result.change_set.operations] == [
        0,
        1,
        2,
    ]
    expected_entities = [
        {
            "id": entity["fixture_key"],
            "type": entity["class"],
            **entity["attributes"],
        }
        for entity in oracle["logical_entities"]
    ]
    expected_relation = oracle["logical_relation"]
    assert receipt["queries"]["entities"] == expected_entities
    assert receipt["queries"]["relations"] == [
        {
            "key": "contains:O1:X1",
            "relation_type": expected_relation["relation_type"],
            "source_id": expected_relation["source_fixture_key"],
            "target_id": expected_relation["target_fixture_key"],
            "type": expected_relation["class"],
        }
    ]
    assert result.change_set.valid_time.value == oracle["valid_time"]

    shutil.rmtree(fixture)
    ledger_replay = KnowledgeChangeHistory.reopen(ledger).replay()
    assert ledger_replay.graph.snapshot() == result.replay.graph.snapshot()
    assert ledger_replay.machine_state.identity == result.replay.machine_state.identity
    assert (
        ledger_replay.receipt.canonical_bytes == result.replay.receipt.canonical_bytes
    )
    assert ledger_replay.partial_contract.identity == result.effective_contract.identity
    assert ledger_replay.binding.identity == result.history_binding.identity
    assert ledger_replay.contract_view.content_hash() == (
        result.replay.contract_view.content_hash()
    )
    assert tuple(ledger.parent.iterdir()) == (ledger,)


@pytest.mark.parametrize(
    ("case", "reason"),
    [
        ("missing", Ret010RefusalReason.MISSING_SOURCE_MEMBER),
        ("drift", Ret010RefusalReason.SOURCE_DIGEST_MISMATCH),
        ("lookup", Ret010RefusalReason.INVALID_INVENTORY_LOOKUP),
        ("duplicate_lookup", Ret010RefusalReason.AMBIGUOUS_INVENTORY_LOOKUP),
        ("selection_ordinal", Ret010RefusalReason.INVALID_SOURCE_SELECTION),
        ("selection_event", Ret010RefusalReason.INVALID_SOURCE_SELECTION),
        ("selection_order", Ret010RefusalReason.INVALID_SOURCE_SELECTION),
        ("selection_item", Ret010RefusalReason.INVALID_SOURCE_SELECTION),
        ("time_value", Ret010RefusalReason.SOURCE_TIME_MISMATCH),
        ("time_ambiguous", Ret010RefusalReason.AMBIGUOUS_SOURCE_TIME),
    ],
)
def test_invalid_source_bundle_refuses_before_change_set_or_ledger(
    tmp_path: Path, case: str, reason: Ret010RefusalReason
) -> None:
    fixture = tmp_path / "fixture"
    shutil.copytree(FIXTURE, fixture)
    mapping = tmp_path / "mapping.json"
    shutil.copyfile(MAPPING, mapping)
    warehouse = fixture / "input/sources/warehouse.jsonl"
    inventory = fixture / "input/sources/inventory-units.csv"

    if case == "missing":
        warehouse.unlink()
    elif case == "drift":
        warehouse.write_bytes(warehouse.read_bytes() + b" ")
    elif case == "lookup":
        inventory.write_text("inventory_unit_id,product_code\nX2,X\n", encoding="utf-8")
        _rebind_member(fixture, "sources/inventory-units.csv")
        _rebind_mapping(mapping, fixture)
    elif case == "duplicate_lookup":
        inventory.write_text(
            "inventory_unit_id,product_code\nX1,X\nX1,Y\n", encoding="utf-8"
        )
        _rebind_member(fixture, "sources/inventory-units.csv")
        _rebind_mapping(mapping, fixture)
    elif case.startswith("selection_"):
        selection_path = fixture / "input/configuration/ret-010-selection.json"
        selection = _load(selection_path)
        mutations = {
            "selection_event": ("event_id", "e28"),
            "selection_item": ("inventory_unit_id", "X2"),
            "selection_order": ("order_id", "O2"),
            "selection_ordinal": ("source_record_ordinal", 0),
        }
        field, value = mutations[case]
        selection[field] = value
        _write_canonical(selection_path, selection)
        _rebind_member(fixture, "configuration/ret-010-selection.json")
        _rebind_mapping(mapping, fixture)
    elif case == "time_value":
        event = json.loads(warehouse.read_text(encoding="utf-8"))
        event["time"] = "08-05 17:00"
        warehouse.write_bytes(_canonical(event) + b"\n")
        _rebind_member(fixture, "sources/warehouse.jsonl")
        _rebind_mapping(mapping, fixture)
    else:
        event = json.loads(warehouse.read_text(encoding="utf-8"))
        event["time"] = "29-10 01:30"
        warehouse.write_bytes(_canonical(event) + b"\n")
        context_path = fixture / "input/configuration/time-context.json"
        context = _load(context_path)
        context["timezone"] = "America/Los_Angeles"
        context["timezone_semantics"] = "IANA_TIMEZONE"
        _write_canonical(context_path, context)
        _rebind_member(fixture, "sources/warehouse.jsonl")
        _rebind_member(fixture, "configuration/time-context.json")
        _rebind_mapping(mapping, fixture)

    ledger = tmp_path / "refused.jsonl"
    with pytest.raises(Ret010Refusal) as refusal:
        _run(ledger, fixture=fixture, mapping=mapping)
    assert refusal.value.reason is reason
    assert not ledger.exists()


def test_reopen_module_command_and_fresh_genesis_are_deterministic(
    tmp_path: Path,
) -> None:
    ledger = tmp_path / "semantic.jsonl"
    first = _run(ledger)
    ledger_bytes = ledger.read_bytes()
    reopened = run_ret010(ledger)

    assert reopened.receipt.canonical_bytes == first.receipt.canonical_bytes
    assert ledger.read_bytes() == ledger_bytes
    assert reopened.replay.graph.snapshot() == first.replay.graph.snapshot()
    assert tuple(ledger.parent.iterdir()) == (ledger,)

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "research.ontology_driven_kg_realization.experiments.small_shop.pareto.ret010",
            "--ledger",
            str(ledger),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=False,
    )
    assert process.returncode == 0, process.stderr.decode()
    assert process.stdout == first.receipt.canonical_bytes + b"\n"
    assert ledger.read_bytes() == ledger_bytes

    ledger.unlink()
    rebuilt = _run(ledger)
    assert rebuilt.receipt.canonical_bytes == first.receipt.canonical_bytes
    assert rebuilt.replay.graph.snapshot() == first.replay.graph.snapshot()


@pytest.mark.parametrize("failure", ["missing_source", "invalid_late_role"])
def test_runtime_mapping_refuses_before_writing_any_history(
    tmp_path: Path, failure: str
) -> None:
    payload = _load(MAPPING)
    if failure == "missing_source":
        del payload["artifact_roles"]["source"]
    else:
        payload["artifact_roles"]["mapping"] = "INVALID_ROLE"
    mapping = tmp_path / "mapping.json"
    _write_canonical(mapping, payload)
    ledger = tmp_path / "semantic.jsonl"

    for _ in range(2):
        with pytest.raises(Ret010Refusal) as refusal:
            _run(ledger, mapping=mapping)
        assert refusal.value.reason is Ret010RefusalReason.MALFORMED_CONFIGURATION
        assert not ledger.exists()


def test_partial_jsonl_is_not_reported_as_a_completed_run(tmp_path: Path) -> None:
    ledger = tmp_path / "semantic.jsonl"
    _run(ledger)
    lines = ledger.read_bytes().splitlines(keepends=True)
    retained_change = next(
        index
        for index, line in enumerate(lines)
        if json.loads(line)["event_type"] == "KNOWLEDGE_CHANGE_SET_RETAINED"
    )
    partial = b"".join(lines[:retained_change])
    ledger.write_bytes(partial)

    with pytest.raises(Ret010Refusal) as refusal:
        _run(ledger)
    assert refusal.value.reason is Ret010RefusalReason.INCOMPLETE_HISTORY
    assert ledger.read_bytes() == partial


def test_existing_ledger_reopens_without_fixture_or_program_files(
    tmp_path: Path,
) -> None:
    fixture = tmp_path / "fixture"
    shutil.copytree(FIXTURE / "input", fixture / "input")
    programs = tmp_path / "programs"
    programs.mkdir()
    machine = programs / "machine.json"
    policy = programs / "policy.json"
    mapping = programs / "mapping.json"
    for source, target in (
        (MACHINE, machine),
        (POLICY, policy),
        (MAPPING, mapping),
    ):
        shutil.copyfile(source, target)
    ledger = tmp_path / "semantic.jsonl"
    first = run_ret010(
        ledger,
        fixture_root=fixture,
        machine_path=machine,
        policy_path=policy,
        mapping_path=mapping,
    )
    ledger_bytes = ledger.read_bytes()
    shutil.rmtree(fixture)
    machine.unlink()
    policy.unlink()
    mapping.unlink()

    reopened = run_ret010(
        ledger,
        fixture_root=fixture,
        machine_path=machine,
        policy_path=policy,
        mapping_path=mapping,
    )
    assert reopened.receipt.canonical_bytes == first.receipt.canonical_bytes
    assert reopened.replay.graph.snapshot() == first.replay.graph.snapshot()
    assert ledger.read_bytes() == ledger_bytes


def test_existing_ledger_must_be_the_exact_ret010_vertical(tmp_path: Path) -> None:
    from tests.contract_compiler.pareto.test_knowledge_change_history import (
        _anchored_history,
        _base_payload,
        _load_change,
        _protocol_events,
    )

    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    before = history.replay()
    change_set = _load_change(_base_payload(history, partial, source, evidence))
    history.admit(
        change_set=change_set,
        machine_events=_protocol_events(change_set, before.machine_state.identity),
        transaction_time="2026-09-01T00:00:00Z",
        actor_id="actor:test",
    )
    ledger_before = history.path.read_bytes()

    with pytest.raises(Ret010Refusal) as refusal:
        _run(history.path)
    assert refusal.value.reason is Ret010RefusalReason.INCOMPATIBLE_HISTORY
    assert history.path.read_bytes() == ledger_before


@pytest.mark.parametrize("failure", ["declared", "programmer"])
def test_compiler_translation_does_not_mask_programmer_errors(
    monkeypatch: pytest.MonkeyPatch, failure: str
) -> None:
    from malleus._contract_pipeline import (
        ElaborationRefusal,
        ElaborationRefusalReason,
    )

    if failure == "declared":
        error: Exception = ElaborationRefusal(
            ElaborationRefusalReason.INVALID_FACT_SET,
            "declared compiler refusal",
        )
    else:
        error = RuntimeError("implementation defect")

    def fail(_binding):
        raise error

    monkeypatch.setattr(ret010_module, "compile_binding", fail)
    if failure == "programmer":
        with pytest.raises(RuntimeError, match="implementation defect"):
            load_ret010_vertical(
                fixture_root=FIXTURE,
                machine_path=MACHINE,
                policy_path=POLICY,
                mapping_path=MAPPING,
            )
    else:
        with pytest.raises(Ret010Refusal) as refusal:
            load_ret010_vertical(
                fixture_root=FIXTURE,
                machine_path=MACHINE,
                policy_path=POLICY,
                mapping_path=MAPPING,
            )
        assert refusal.value.reason is Ret010RefusalReason.CONTRACT_COMPILATION_FAILED


def test_fixture_producer_uses_private_data_not_oracle_or_inline_output_magic() -> None:
    vertical = load_ret010_vertical(
        fixture_root=FIXTURE,
        machine_path=MACHINE,
        policy_path=POLICY,
        mapping_path=MAPPING,
    )
    source = inspect.getsource(ret010_module)
    tree = ast.parse(source)
    semantic_tokens = [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
    semantic_tokens.extend(
        node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
    )
    semantic_tokens.extend(
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    )
    assert all("oracle" not in token.lower() for token in semantic_tokens)
    assert all(
        literal not in source
        for literal in (
            "2000-05-07T17:00:00Z",
            "ORDER_CONTAINS_UNIT",
            "OrderContainsUnit",
            "SalesOrder",
            "InventoryUnit",
            "contains:O1:X1",
            "retained-source-integrity",
            "structural-conformance",
        )
    )
    assert vertical.mapping.publication_contract == (
        "PRIVATE_FIXTURE_LOCAL_NO_PUBLIC_ABOX_FORMAT"
    )

"""End-to-end tests for the bounded Small Shop correction proof."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from malleus._contract_pipeline.knowledge import KnowledgeChangeHistory
import research.ontology_driven_kg_realization.experiments.small_shop.correction.run as correction_module
from research.ontology_driven_kg_realization.experiments.small_shop.correction.run import (
    CorrectionRefusal,
    CorrectionRefusalReason,
    run_correction,
)


ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).parent
FIXTURE = (
    ROOT
    / "research"
    / "ontology_driven_kg_realization"
    / "fixtures"
    / "small_shop_fulfilment_correction_v1"
)
BASE_FIXTURE = FIXTURE.with_name("small_shop_fulfilment")
MACHINE = HERE / "machine.json"
POLICY = HERE / "policy.json"
RUN_PROGRAM = HERE / "run.json"
MAPPING = HERE / "mapping.json"
CHECKS = HERE / "checks"
EVIDENCE = HERE / "evidence"
ORACLE = FIXTURE / "oracle/shop-supplier-order-correction.json"


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_bytes())
    assert isinstance(value, dict)
    return value


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def test_program_policy_machine_and_checks_are_closed_canonical_data() -> None:
    paths = (
        MACHINE,
        POLICY,
        RUN_PROGRAM,
        CHECKS / "source-mapping-conformance.json",
        CHECKS / "structural-conformance.json",
    )
    values = {path: _load(path) for path in paths}
    assert all(path.read_bytes() == _canonical(values[path]) for path in paths)

    machine = values[MACHINE]
    policy = values[POLICY]
    program = values[RUN_PROGRAM]
    assert machine["grammar"] == "malleus.protocol-machine/private-v0"
    assert policy["grammar"] == "malleus.policy-program/private-v0"
    assert program["grammar"] == "malleus.small-shop.correction-run/private-v0"
    assert [item["check_contract_identity"] for item in policy["required_checks"]] == [
        _digest(CHECKS / "source-mapping-conformance.json"),
        _digest(CHECKS / "structural-conformance.json"),
    ]
    assert {path.name for path in CHECKS.iterdir()} == {
        "source-mapping-conformance.json",
        "structural-conformance.json",
    }
    check_instructions = machine["events"]["CHECK_RECORDED"]["instructions"]
    assert {
        "event_field": "receipt_identity",
        "opcode": "REQUIRE_REFERENCED_RECORD",
        "record_type": "ArtifactRecord",
        "refusal": "UNKNOWN_REFERENCE",
    } in check_instructions
    assert "small-shop" not in MACHINE.read_text().lower()
    assert "supplier" not in MACHINE.read_text().lower()
    assert "small-shop" not in POLICY.read_text().lower()
    assert "supplier" not in POLICY.read_text().lower()


def test_source_to_log_to_current_and_historical_graph(tmp_path: Path) -> None:
    output = tmp_path / "proof"
    result = run_correction(output)
    replay = result.replay

    assert [change.change_set_id for change in replay.change_sets] == [
        "change:RET-010:genesis",
        "change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e4",
        "change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e7",
    ]
    assert [item["id"] for item in replay.graph.snapshot()["nodes"]] == [
        "O1",
        "X1",
        "supplier-order-state:B:e7",
    ]
    assert [item["key"] for item in replay.graph.snapshot()["relations"]] == [
        "contains:O1:X1"
    ]
    assert replay.graph.get_node("supplier-order-state:B:e4") is None
    assert replay.graph.get_node("supplier-order-state:B:e7") == {
        "id": "supplier-order-state:B:e7",
        "ordered_quantity": 2,
        "product_code": "Y",
        "source_occurrence_id": "e7",
        "supplier_order_id": "B",
        "type": "SupplierOrderState",
    }

    at_e4 = replay.graph_at_change(
        "change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e4"
    )
    assert at_e4.get_node("supplier-order-state:B:e4")["ordered_quantity"] == 1
    assert at_e4.get_node("supplier-order-state:B:e7") is None
    assert {item["id"] for item in at_e4.snapshot()["nodes"]} == {
        "O1",
        "X1",
        "supplier-order-state:B:e4",
    }

    earlier = replay.record_history["supplier-order-state:B:e4"]
    later = replay.record_history["supplier-order-state:B:e7"]
    assert earlier.valid_from.value == "e4"
    assert earlier.valid_to == later.valid_from
    assert earlier.superseded_by == "supplier-order-state:B:e7"
    assert later.supersedes_record_id == "supplier-order-state:B:e4"
    assert later.valid_to is None


def test_real_check_receipts_are_retained_and_bound_to_protocol_records(
    tmp_path: Path,
) -> None:
    result = run_correction(tmp_path / "proof")
    replay = result.replay
    retained = {item.record_id: item for item in replay.retained_inputs}
    checks = [
        record
        for record in replay.machine_state.records
        if record.record_type == "CheckRecord"
    ]
    assert len(checks) == 6

    for check in checks:
        identity = check.fields["receipt_identity"]
        artifact = retained[identity]
        receipt = json.loads(artifact.content)
        assert artifact.role == "RETAINED_EVIDENCE"
        assert artifact.identity == identity
        assert _canonical(receipt) == artifact.content
        assert receipt["outcome"] == check.fields["outcome"] == "SATISFIED"
        assert receipt["check_contract_id"] == check.fields["check_contract_id"]
        assert receipt["check_contract_identity"] == (
            check.fields["check_contract_identity"]
        )
        assert receipt["change"]["contract_identity"] == (
            replay.partial_contract.identity
        )
    assert retained["artifact:small-shop-proof:check-entrypoint"].media_type == (
        "text/x-python"
    )


def test_explanation_traces_every_record_to_mapping_and_exact_source_bytes(
    tmp_path: Path,
) -> None:
    result = run_correction(tmp_path / "proof")
    explanation = json.loads(result.explanation_bytes)
    changes = {item["change_set_id"]: item for item in explanation["changes"]}
    retained = {item.record_id: item for item in result.replay.retained_inputs}

    assert changes["change:RET-010:genesis"]["selected_source"] | {
        "record_sha256": "ignored"
    } == {
        "mapping_artifact_id": "artifact:small-shop-proof:ret010-mapping",
        "mapping_sha256": retained[
            "artifact:small-shop-proof:ret010-mapping"
        ].identity,
        "member": "ret010:input/sources/warehouse.jsonl",
        "member_sha256": retained["ret010:input/sources/warehouse.jsonl"].identity,
        "ordinal": 1,
        "ordinal_base": 1,
        "record_order": "SOURCE_ORDER",
        "record_sha256": "ignored",
    }
    assert [
        changes[change_id]["selected_source"]["ordinal"]
        for change_id in (
            "change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e4",
            "change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e7",
        )
    ] == [0, 1]
    for change in changes.values():
        selected = change["selected_source"]
        source = retained[selected["member"]]
        rows = tuple(line for line in source.content.splitlines() if line.strip())
        row = rows[selected["ordinal"] - selected["ordinal_base"]]
        assert selected["member_sha256"] == source.identity
        assert selected["record_sha256"] == "sha256:" + sha256(row).hexdigest()
        assert selected["mapping_sha256"] == retained[
            selected["mapping_artifact_id"]
        ].identity
    assert all(
        changes[record["change_set_id"]]["selected_source"]["member_sha256"]
        == retained[
            changes[record["change_set_id"]]["selected_source"]["member"]
        ].identity
        for record in explanation["history"]["records"]
    )


def test_runtime_result_matches_the_independent_oracle_without_consuming_it(
    tmp_path: Path,
) -> None:
    oracle = _load(ORACLE)
    result = run_correction(tmp_path / "proof")
    replay = result.replay
    runtime = {}
    for record_id, item in replay.record_history.items():
        if item.operation.record_type != "SupplierOrderState":
            continue
        properties = dict(item.operation.properties)
        key = f"{properties['supplier_order_id']}@{properties['source_occurrence_id']}"
        runtime[key] = (record_id, item, properties)

    assert set(runtime) == {
        state["fixture_state_key"] for state in oracle["expected_states"]
    }
    for state in oracle["expected_states"]:
        _, history, properties = runtime[state["fixture_state_key"]]
        assert history.operation.record_type == state["class"]
        assert properties == state["attributes"]
        assert {
            "kind": history.valid_from.kind,
            "value": history.valid_from.value,
        } == state["valid_time"]

    current_key = oracle["expected_current_fixture_state_key"]
    assert runtime[current_key][1].superseded_by is None
    supersession = oracle["expected_supersession"]
    earlier_id = runtime[supersession["earlier_fixture_state_key"]][0]
    later_id = runtime[supersession["later_fixture_state_key"]][0]
    assert replay.record_history[earlier_id].superseded_by == later_id
    assert replay.record_history[later_id].supersedes_record_id == earlier_id

    snapshot = replay.graph.snapshot()
    current_ids = {item["id"] for item in snapshot["nodes"]} | {
        item["key"] for item in snapshot["relations"]
    }
    assert set(oracle["preservation"]["baseline_ret010_record_ids"]) <= current_ids
    oracle_identity = _digest(ORACLE)
    assert all(item.identity != oracle_identity for item in replay.retained_inputs)


def test_reopen_is_read_only_and_regenerates_exact_outputs(tmp_path: Path) -> None:
    output = tmp_path / "proof"
    first = run_correction(output)
    history = output / "history.jsonl"
    before = history.read_bytes()
    expected = {
        name: (output / name).read_bytes()
        for name in ("receipt.json", "graph.json", "explanation.json")
    }
    for name in expected:
        (output / name).unlink()

    second = run_correction(output)

    assert history.read_bytes() == before
    assert first.replay.receipt == second.replay.receipt
    assert {
        name: (output / name).read_bytes() for name in expected
    } == expected


def test_checked_in_evidence_is_exactly_regenerated(tmp_path: Path) -> None:
    output = tmp_path / "proof"
    run_correction(output)
    assert {
        name: (output / name).read_bytes()
        for name in ("receipt.json", "graph.json", "explanation.json")
    } == {
        name: (EVIDENCE / name).read_bytes()
        for name in ("receipt.json", "graph.json", "explanation.json")
    }


def test_tampered_source_refuses_before_history_creation(tmp_path: Path) -> None:
    fixture = tmp_path / "fixture"
    shutil.copytree(FIXTURE, fixture)
    source = fixture / "input/sources/supplier-order-history.jsonl"
    source.write_bytes(source.read_bytes().replace(b'"quantity":2', b'"quantity":3'))
    output = tmp_path / "proof"

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output, correction_fixture=fixture)

    assert refusal.value.reason is CorrectionRefusalReason.SOURCE_DIGEST_MISMATCH
    assert not (output / "history.jsonl").exists()


def test_tampered_check_contract_refuses_before_history_creation(
    tmp_path: Path,
) -> None:
    checks = tmp_path / "checks"
    shutil.copytree(CHECKS, checks)
    contract = checks / "source-mapping-conformance.json"
    contract.write_bytes(contract.read_bytes().replace(b"CONFORMS", b"DIFFERS"))
    output = tmp_path / "proof"

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output, checks_root=checks)

    assert refusal.value.reason is CorrectionRefusalReason.CONFIGURATION_IDENTITY_MISMATCH
    assert not (output / "history.jsonl").exists()


@pytest.mark.parametrize("mutation", ["EXTRA_FIELD", "WRONG_GRAMMAR"])
def test_check_contract_shape_is_closed_for_fresh_and_replay_paths(
    tmp_path: Path, mutation: str
) -> None:
    checks = tmp_path / "checks"
    shutil.copytree(CHECKS, checks)
    contract_path = checks / "source-mapping-conformance.json"
    contract = _load(contract_path)
    if mutation == "EXTRA_FIELD":
        contract["unexpected"] = True
    else:
        contract["grammar"] = "malleus.check-contract/unsupported"
    changed = _canonical(contract)
    contract_path.write_bytes(changed)
    output = tmp_path / "proof"

    with pytest.raises(CorrectionRefusal) as fresh:
        run_correction(output, checks_root=checks)

    assert fresh.value.reason is CorrectionRefusalReason.MALFORMED_CONFIGURATION
    assert not (output / "history.jsonl").exists()

    with pytest.raises(CorrectionRefusal) as replay:
        correction_module._check_contract(
            changed,
            entrypoint_id="artifact:small-shop-proof:check-entrypoint",
            entrypoint_identity=_digest(Path(correction_module.__file__)),
            shape_reason=CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
            identity_reason=CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
        )

    assert replay.value.reason is CorrectionRefusalReason.INCOMPATIBLE_HISTORY


def _assert_bootstrap_only(output: Path) -> None:
    replay = KnowledgeChangeHistory.reopen(output / "history.jsonl").replay()
    assert replay.change_sets == ()
    assert replay.graph.node_count == replay.graph.edge_count == 0
    assert all(
        b'"grammar":"malleus.check-receipt/private-v0"' not in item.content
        for item in replay.retained_inputs
    )


def _assert_first_correction_not_admitted(output: Path) -> None:
    replay = KnowledgeChangeHistory.reopen(output / "history.jsonl").replay()
    assert [change.change_set_id for change in replay.change_sets] == [
        "change:RET-010:genesis"
    ]
    assert replay.graph.get_node("supplier-order-state:B:e4") is None
    assert sum(
        item.content.startswith(b'{"base":')
        and b'"grammar":"malleus.check-receipt/private-v0"' in item.content
        for item in replay.retained_inputs
    ) == 2


def test_receipt_content_mismatch_cannot_become_a_protocol_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    execute = correction_module._check_receipts

    def mismatch(*args, **kwargs):
        receipts = list(execute(*args, **kwargs))
        receipt = json.loads(receipts[0])
        receipt["check_contract_id"] = "different-check"
        receipts[0] = _canonical(receipt)
        return tuple(receipts)

    monkeypatch.setattr(correction_module, "_check_receipts", mismatch)
    output = tmp_path / "proof"

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output)

    assert refusal.value.reason is CorrectionRefusalReason.CHECK_FAILED
    _assert_bootstrap_only(output)


def test_receipt_with_extra_field_refuses_atomically(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    execute = correction_module._check_receipts

    def extra_field(*args, **kwargs):
        receipts = list(execute(*args, **kwargs))
        receipt = json.loads(receipts[0])
        receipt["unexpected"] = True
        receipts[0] = _canonical(receipt)
        return tuple(receipts)

    monkeypatch.setattr(correction_module, "_check_receipts", extra_field)
    output = tmp_path / "proof"

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output)

    assert refusal.value.reason is CorrectionRefusalReason.CHECK_FAILED
    _assert_bootstrap_only(output)


def test_receipt_with_source_artifact_role_refuses_atomically(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    anchor = correction_module._artifact_anchor

    def wrong_role(*, record_id, content, role, media_type="application/json"):
        if b'"grammar":"malleus.check-receipt/private-v0"' in content:
            role = "SOURCE_ARTIFACT"
        return anchor(
            record_id=record_id,
            content=content,
            role=role,
            media_type=media_type,
        )

    monkeypatch.setattr(correction_module, "_artifact_anchor", wrong_role)
    output = tmp_path / "proof"

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output)

    assert refusal.value.reason is CorrectionRefusalReason.CHECK_FAILED
    _assert_bootstrap_only(output)


@pytest.mark.parametrize("claim", ["BASE", "CHANGE", "RESULT"])
def test_false_receipt_semantics_preserve_every_bootstrap_byte(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, claim: str
) -> None:
    execute = correction_module._check_receipts
    output = tmp_path / "proof"
    before: dict[str, bytes] = {}

    def false_claim(*args, **kwargs):
        before["ledger"] = (output / "history.jsonl").read_bytes()
        receipts = list(execute(*args, **kwargs))
        receipt = json.loads(receipts[0])
        if claim == "BASE":
            receipt["base"]["accepted_state_digest"] = "sha256:" + "0" * 64
        elif claim == "CHANGE":
            receipt["change"]["contract_identity"] = "sha256:" + "0" * 64
        else:
            receipt["result"]["mapping_sha256"] = "sha256:" + "0" * 64
        receipts[0] = _canonical(receipt)
        return tuple(receipts)

    monkeypatch.setattr(correction_module, "_check_receipts", false_claim)

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output)

    assert refusal.value.reason is CorrectionRefusalReason.CHECK_FAILED
    assert (output / "history.jsonl").read_bytes() == before["ledger"]
    _assert_bootstrap_only(output)


def test_mapping_value_that_differs_from_retained_source_refuses_atomically(
    tmp_path: Path,
) -> None:
    mapping = _load(MAPPING)
    mapping["changes"][0]["operations"][0]["properties"][
        "ordered_quantity"
    ] = 999
    changed = tmp_path / "mapping.json"
    changed.write_bytes(_canonical(mapping))
    output = tmp_path / "proof"

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output, correction_mapping=changed)

    assert refusal.value.reason is CorrectionRefusalReason.CHECK_FAILED
    _assert_first_correction_not_admitted(output)


def test_incomplete_mapping_cannot_hide_a_wrong_source_value(tmp_path: Path) -> None:
    mapping = _load(MAPPING)
    mapping["state_bindings"] = [
        binding
        for binding in mapping["state_bindings"]
        if binding["source_field"] != "quantity"
    ]
    mapping["changes"][0]["operations"][0]["properties"][
        "ordered_quantity"
    ] = 999
    changed = tmp_path / "mapping.json"
    changed.write_bytes(_canonical(mapping))
    output = tmp_path / "proof"

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output, correction_mapping=changed)

    assert refusal.value.reason is CorrectionRefusalReason.CHECK_FAILED
    _assert_first_correction_not_admitted(output)


def test_mapping_must_select_every_source_row_once_in_order(tmp_path: Path) -> None:
    mapping = _load(MAPPING)
    mapping["changes"][1]["source_record_ordinal"] = 0
    changed = tmp_path / "mapping.json"
    changed.write_bytes(_canonical(mapping))
    output = tmp_path / "proof"

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output, correction_mapping=changed)

    assert refusal.value.reason is CorrectionRefusalReason.MALFORMED_CONFIGURATION
    assert not (output / "history.jsonl").exists()


def test_unsupported_correction_mapping_grammar_refuses_before_history(
    tmp_path: Path,
) -> None:
    mapping = _load(MAPPING)
    mapping["grammar"] = "malleus.small-shop.unsupported/private-v0"
    changed = tmp_path / "mapping.json"
    changed.write_bytes(_canonical(mapping))
    output = tmp_path / "proof"

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output, correction_mapping=changed)

    assert refusal.value.reason is CorrectionRefusalReason.MALFORMED_CONFIGURATION
    assert not (output / "history.jsonl").exists()


@pytest.mark.parametrize(
    "mutation", ["ABSOLUTE", "TRAVERSAL", "DUPLICATE_LOCATOR", "EXTRA_FIELD"]
)
def test_invalid_compiler_source_declaration_refuses_before_history(
    tmp_path: Path, mutation: str
) -> None:
    mapping = _load(MAPPING)
    sources = mapping["compiler"]["sources"]
    repository_source = next(
        source for source in sources if source["kind"] == "REPOSITORY_PATH"
    )
    if mutation == "ABSOLUTE":
        repository_source["path"] = str(ROOT / "ontology/malleus.yaml")
    elif mutation == "TRAVERSAL":
        repository_source["path"] = "../ontology/malleus.yaml"
    elif mutation == "DUPLICATE_LOCATOR":
        sources[1]["locator"] = sources[0]["locator"]
    else:
        repository_source["unexpected"] = True
    changed = tmp_path / "mapping.json"
    changed.write_bytes(_canonical(mapping))
    output = tmp_path / "proof"

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output, correction_mapping=changed)

    assert refusal.value.reason is CorrectionRefusalReason.MALFORMED_CONFIGURATION
    assert not (output / "history.jsonl").exists()


@pytest.mark.parametrize("kind", ["TRAVERSAL", "ABSOLUTE"])
def test_output_names_cannot_escape_the_selected_directory(
    tmp_path: Path, kind: str
) -> None:
    outside = tmp_path / ("outside.json" if kind == "TRAVERSAL" else "absolute.json")
    unsafe = "../outside.json" if kind == "TRAVERSAL" else str(outside)
    program = _load(RUN_PROGRAM)
    program["outputs"]["graph"] = unsafe
    changed = tmp_path / "run.json"
    changed.write_bytes(_canonical(program))
    output = tmp_path / "proof"
    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output, program_path=changed)

    assert refusal.value.reason is CorrectionRefusalReason.MALFORMED_CONFIGURATION
    assert not outside.exists()
    assert not (output / "history.jsonl").exists()


@pytest.mark.parametrize("kind", ["COLLISION", "RENAMED_HISTORY"])
def test_history_output_name_is_fixed_and_cannot_collide(
    tmp_path: Path, kind: str
) -> None:
    program = _load(RUN_PROGRAM)
    if kind == "COLLISION":
        program["outputs"]["receipt"] = "history.jsonl"
    else:
        program["outputs"]["history"] = "events.jsonl"
    changed = tmp_path / "run.json"
    changed.write_bytes(_canonical(program))
    output = tmp_path / "proof"

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output, program_path=changed)

    assert refusal.value.reason is CorrectionRefusalReason.MALFORMED_CONFIGURATION
    assert not output.exists()


def test_existing_output_symlink_cannot_overwrite_an_outside_file(
    tmp_path: Path,
) -> None:
    output = tmp_path / "proof"
    output.mkdir()
    victim = tmp_path / "victim.json"
    victim.write_bytes(b"preserve me")
    (output / "graph.json").symlink_to(victim)

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output)

    assert refusal.value.reason is CorrectionRefusalReason.MALFORMED_CONFIGURATION
    assert victim.read_bytes() == b"preserve me"
    assert not (output / "history.jsonl").exists()


def test_reopen_refuses_changed_active_entrypoint_without_mutating_history(
    tmp_path: Path,
) -> None:
    output = tmp_path / "proof"
    run_correction(output)
    history = output / "history.jsonl"
    before = history.read_bytes()
    changed_entrypoint = tmp_path / "run.py"
    changed_entrypoint.write_bytes(
        Path(correction_module.__file__).read_bytes() + b"\n# changed\n"
    )

    with pytest.raises(CorrectionRefusal) as refusal:
        run_correction(output, entrypoint_path=changed_entrypoint)

    assert refusal.value.reason is CorrectionRefusalReason.INCOMPATIBLE_HISTORY
    assert history.read_bytes() == before


def test_module_command_writes_the_public_evidence_bundle(tmp_path: Path) -> None:
    output = tmp_path / "proof"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            (
                "research.ontology_driven_kg_realization.experiments."
                "small_shop.correction.run"
            ),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout) == json.loads(
        (output / "explanation.json").read_bytes()
    )
    assert {path.name for path in output.iterdir()} == {
        "explanation.json",
        "graph.json",
        "history.jsonl",
        "receipt.json",
    }

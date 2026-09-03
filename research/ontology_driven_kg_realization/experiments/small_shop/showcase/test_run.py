"""TDD contract for the lean five-stage Small Shop showcase."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import shutil

import pytest

from malleus._contract_pipeline.knowledge import KnowledgeChangeHistory
from research.ontology_driven_kg_realization.experiments.small_shop.showcase import (
    run as run_module,
)
from research.ontology_driven_kg_realization.experiments.small_shop.showcase.run import (
    ShowcaseRefusal,
    _admit_stage,
    _prepare_showcase,
    run_showcase,
    verify_source_mapping_receipts,
)


ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).parent
RUN = HERE / "run.json"
MAPPING = HERE / "settlement-mapping.json"
CHECK = HERE / "checks/source-mapping-conformance.json"
POLICY = HERE / "policy.json"
FIXTURE = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "small_shop_fulfilment_settlement_v1"
)
BASE_FIXTURE = FIXTURE.with_name("small_shop_fulfilment")
CORRECTION_FIXTURE = FIXTURE.with_name("small_shop_fulfilment_correction_v1")
CORRECTION_EVIDENCE = (
    ROOT
    / "research/ontology_driven_kg_realization/experiments"
    / "small_shop/correction/evidence/receipt.json"
)
CORRECTION_MAPPING = CORRECTION_EVIDENCE.parents[1] / "mapping.json"

CHANGE_IDS = [
    "change:RET-010:genesis",
    "change:SHOP-PAYMENT-SETTLEMENT:invoice-base",
    "change:SHOP-PAYMENT-SETTLEMENT:P1:e30",
    "change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e4",
    "change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e7",
]
CURRENT_IDS = {
    "O1",
    "X1",
    "contains:O1:X1",
    "supplier-order-state:B:e7",
    "invoice:I1",
    "invoice:I2",
    "payment:P1",
    "relation:P1:I1",
    "relation:P1:I2",
}


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_bytes())
    assert isinstance(value, dict)
    return value


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.write_bytes(_canonical(value))


def _rehash_fixture_member(fixture: Path, relative: str) -> str:
    manifest_path = fixture / "input/manifest.json"
    manifest = _load(manifest_path)
    member_path = fixture / "input" / relative
    member = next(item for item in manifest["members"] if item["path"] == relative)
    member["byte_length"] = len(member_path.read_bytes())
    member["sha256"] = _digest(member_path)
    _write_json(manifest_path, manifest)
    return _digest(manifest_path)


@pytest.fixture(scope="module")
def proof(tmp_path_factory: pytest.TempPathFactory):
    output = tmp_path_factory.mktemp("small-shop-showcase") / "proof"
    return output, run_showcase(output)


def test_run_program_records_the_closed_automatic_decisions() -> None:
    program = _load(RUN)
    assert RUN.read_bytes() == _canonical(program)
    assert set(program["decisions"]) == {
        "accepted_query_surface",
        "history_shape",
        "invoice_valid_time",
        "provenance_granularity",
        "scoring",
        "source_arrival_model",
        "transaction_prefix_read",
    }
    assert program["decisions"] == {
        "accepted_query_surface": {
            "choice": "CUSTOM_READ_ONLY_QUERY_FACADE",
            "deferred": "CYPHER_ADAPTER",
        },
        "history_shape": {
            "choice": "FRESH_SINGLE_CONTRACT_FIVE_STAGE_HISTORY",
            "order_basis": "FROZEN_RET_TEST_LADDER_NOT_BUSINESS_EVENT_CHRONOLOGY",
        },
        "invoice_valid_time": {
            "choice": "ORDER_ONLY",
            "meaning": "FIXTURE_ORCHESTRATION_NOT_SOURCE_EVENT_OR_TIMESTAMP",
            "value": "fixture:invoice-base-before-e30",
        },
        "provenance_granularity": {
            "choice": "CHANGE_LEVEL_SOURCE_AND_EVIDENCE_CLOSURE",
            "deferred": "OPERATION_LEVEL_PROVENANCE",
        },
        "scoring": {
            "choice": "EXCLUDED",
            "meaning": "NO_EVALUATOR_OR_ANSWER_COMPARISON_IN_CORE_SHOWCASE",
        },
        "source_arrival_model": {
            "choice": "PREPROVISIONED_BOOTSTRAP",
            "deferred": "STAGE_WISE_SOURCE_REGISTRATION_AND_OBSERVATION",
            "meaning": "STAGED_ADMISSION_NOT_LIVE_OBSERVATION",
        },
        "transaction_prefix_read": {
            "choice": "DEFERRED",
            "meaning": "GRAPH_AT_ACCEPTED_CHANGE_ONLY",
        },
    }
    assert [stage["selector"] for stage in program["stages"]] == [
        "RET010",
        "SETTLEMENT:0",
        "SETTLEMENT:1",
        "CORRECTION:0",
        "CORRECTION:1",
    ]


def test_one_contract_five_changes_and_exact_current_graph(proof) -> None:
    _, result = proof
    replay = result.replay
    assert [change.change_set_id for change in replay.change_sets] == CHANGE_IDS
    assert {change.contract_identity for change in replay.change_sets} == {
        replay.partial_contract.identity
    }
    snapshot = replay.graph.snapshot()
    assert {node["id"] for node in snapshot["nodes"]} | {
        relation["key"] for relation in snapshot["relations"]
    } == CURRENT_IDS


def test_named_changes_preserve_published_correction_semantics(proof) -> None:
    _, result = proof
    replay = result.replay
    first = replay.graph_at_change(CHANGE_IDS[0]).snapshot()
    assert {node["id"] for node in first["nodes"]} == {"O1", "X1"}
    assert {relation["key"] for relation in first["relations"]} == {"contains:O1:X1"}
    e4 = replay.graph_at_change("change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e4")
    assert e4.get_node("supplier-order-state:B:e4")["ordered_quantity"] == 1
    e7 = replay.graph_at_change("change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e7")
    assert e7.get_node("supplier-order-state:B:e4") is None
    assert e7.get_node("supplier-order-state:B:e7")["ordered_quantity"] == 2
    earlier = replay.record_history["supplier-order-state:B:e4"]
    later = replay.record_history["supplier-order-state:B:e7"]
    assert earlier.superseded_by == "supplier-order-state:B:e7"
    assert earlier.valid_to == later.valid_from
    assert later.supersedes_record_id == "supplier-order-state:B:e4"


def test_invoices_exist_before_the_fixed_two_invoice_payment(proof) -> None:
    _, result = proof
    replay = result.replay
    invoice_graph = replay.graph_at_change(
        "change:SHOP-PAYMENT-SETTLEMENT:invoice-base"
    )
    assert invoice_graph.get_node("invoice:I1") == {
        "id": "invoice:I1",
        "invoice_number": "I1",
        "type": "Invoice",
    }
    assert invoice_graph.get_node("invoice:I2")["invoice_number"] == "I2"
    assert invoice_graph.get_node("payment:P1") is None
    invoice_change = next(
        change
        for change in replay.change_sets
        if change.change_set_id == "change:SHOP-PAYMENT-SETTLEMENT:invoice-base"
    )
    assert invoice_change.valid_time.kind == "ORDER_ONLY"
    assert invoice_change.valid_time.value == "fixture:invoice-base-before-e30"

    payment = replay.graph.get_node("payment:P1")
    assert payment == {
        "id": "payment:P1",
        "payment_number": "P1",
        "type": "Payment",
    }
    relations = replay.graph.query_relations(source_id="payment:P1")
    assert [(item["key"], item["target_id"]) for item in relations] == [
        ("relation:P1:I1", "invoice:I1"),
        ("relation:P1:I2", "invoice:I2"),
    ]
    payment_change = next(
        change
        for change in replay.change_sets
        if change.change_set_id == "change:SHOP-PAYMENT-SETTLEMENT:P1:e30"
    )
    assert payment_change.valid_time.kind == "ORDER_ONLY"
    assert payment_change.valid_time.value == "e30"


def test_each_stage_has_one_recomputable_source_mapping_receipt(proof) -> None:
    _, result = proof
    verified = verify_source_mapping_receipts(result.replay)
    assert [item.change_set_id for item in verified] == CHANGE_IDS
    assert len({item.receipt_identity for item in verified}) == 5
    checks = [
        record
        for record in result.replay.machine_state.records
        if record.record_type == "CheckRecord"
    ]
    assert len(checks) == 5
    assert {record.fields["receipt_identity"] for record in checks} == {
        item.receipt_identity for item in verified
    }
    retained = {item.record_id: item for item in result.replay.retained_inputs}
    first_receipt = json.loads(retained[verified[0].receipt_identity].content)
    assert [item["member"] for item in first_receipt["selected_records"]] == [
        "ret010:input/sources/warehouse.jsonl",
        "ret010:input/sources/inventory-units.csv",
    ]
    assert (
        len({item["record_sha256"] for item in first_receipt["selected_records"]}) == 2
    )


def test_retained_inputs_preserve_their_declared_media_types(proof) -> None:
    _, result = proof
    retained = {item.record_id: item for item in result.replay.retained_inputs}

    assert retained["artifact:small-shop-showcase:entrypoint"].media_type == (
        "text/x-python"
    )
    assert retained["ret010:input/sources/inventory-units.csv"].media_type == (
        "text/csv"
    )
    assert retained["ret010:input/sources/warehouse.jsonl"].media_type == (
        "application/x-ndjson"
    )
    assert retained["settlement:input/tbox/small-shop-settlement.yaml"].media_type == (
        "application/yaml"
    )


def test_run_program_is_retained_at_its_exact_digest_and_oracle_is_not(proof) -> None:
    _, result = proof
    retained = {item.record_id: item for item in result.replay.retained_inputs}
    item = retained["artifact:small-shop-showcase:run-program"]
    assert item.content == RUN.read_bytes()
    assert item.identity == _digest(RUN)
    oracle = FIXTURE / "oracle/shop-payment-settlement.json"
    assert _digest(oracle) not in {item.identity for item in retained.values()}
    assert all("oracle" not in item.record_id.lower() for item in retained.values())
    assert all(
        dict(change.evidence)[item.record_id] == item.identity
        for change in result.replay.change_sets
    )


def test_ledger_only_reopen_needs_no_ambient_fixture_or_program(
    proof, monkeypatch: pytest.MonkeyPatch
) -> None:
    output, result = proof
    copied = output.parent / "copied-history.jsonl"
    copied.write_bytes((output / "history.jsonl").read_bytes())
    reopened = KnowledgeChangeHistory.reopen(copied).replay()
    assert reopened.receipt == result.replay.receipt
    assert reopened.graph.snapshot() == result.replay.graph.snapshot()
    assert verify_source_mapping_receipts(reopened) == verify_source_mapping_receipts(
        result.replay
    )

    def ambient_read_is_forbidden(_path: Path, _label: str) -> bytes:
        raise AssertionError("ledger reopen touched ambient declarations")

    monkeypatch.setattr(run_module, "read", ambient_read_is_forbidden)
    assert run_showcase(output).replay.receipt == result.replay.receipt


def test_changed_automatic_decision_refuses_before_history(tmp_path: Path) -> None:
    program = _load(RUN)
    program["decisions"]["scoring"]["choice"] = "INCLUDED"
    changed = tmp_path / "run.json"
    changed.write_bytes(_canonical(program))
    output = tmp_path / "proof"
    with pytest.raises(ShowcaseRefusal):
        run_showcase(output, program_path=changed)
    assert not (output / "history.jsonl").exists()


def test_nonstandard_json_number_refuses_as_configuration_before_history(
    tmp_path: Path,
) -> None:
    changed = tmp_path / "run.json"
    changed.write_bytes(
        RUN.read_bytes().replace(
            b'"transaction_time":"2026-09-03T00:00:00Z"',
            b'"transaction_time":NaN',
        )
    )
    output = tmp_path / "proof"

    with pytest.raises(ShowcaseRefusal, match="MALFORMED_CONFIGURATION"):
        run_showcase(output, program_path=changed)

    assert not (output / "history.jsonl").exists()


@pytest.mark.parametrize(
    ("mutation", "value"),
    [
        ("MISSING_PROPOSAL_ID", None),
        ("EXTRA_FIELD", "unexpected"),
        ("EMPTY_DECISION_ID", ""),
        ("BAD_TRANSACTION_TIME", 7),
    ],
)
def test_malformed_stage_declaration_refuses_before_bootstrap(
    tmp_path: Path, mutation: str, value: object
) -> None:
    program = _load(RUN)
    stage = program["stages"][0]
    if mutation == "MISSING_PROPOSAL_ID":
        stage.pop("proposal_id")
    elif mutation == "EXTRA_FIELD":
        stage["unexpected"] = value
    elif mutation == "EMPTY_DECISION_ID":
        stage["decision_id"] = value
    else:
        stage["transaction_time"] = value
    changed = tmp_path / "run.json"
    _write_json(changed, program)
    output = tmp_path / "proof"

    with pytest.raises(ShowcaseRefusal, match="MALFORMED_CONFIGURATION"):
        run_showcase(output, program_path=changed)

    assert not (output / "history.jsonl").exists()


@pytest.mark.parametrize("fixture_name", ["settlement", "correction"])
def test_coherently_rehashed_selection_drift_refuses_before_history(
    tmp_path: Path, fixture_name: str
) -> None:
    program = _load(RUN)
    output = tmp_path / "proof"
    if fixture_name == "settlement":
        fixture = tmp_path / "settlement-fixture"
        shutil.copytree(FIXTURE, fixture)
        relative = "configuration/shop-payment-settlement-selection.json"
        selection_path = fixture / "input" / relative
        selection = _load(selection_path)
        selection["payment_record_ordinal"] = 99
        _write_json(selection_path, selection)
        mapping = _load(MAPPING)
        mapping["input_manifest_sha256"] = _rehash_fixture_member(fixture, relative)
        mapping_path = tmp_path / "settlement-mapping.json"
        _write_json(mapping_path, mapping)
        program["inputs"]["settlement"]["mapping_sha256"] = _digest(mapping_path)
        program_path = tmp_path / "run.json"
        _write_json(program_path, program)
        arguments = {
            "program_path": program_path,
            "settlement_fixture": fixture,
            "settlement_mapping": mapping_path,
        }
    else:
        fixture = tmp_path / "correction-fixture"
        shutil.copytree(CORRECTION_FIXTURE, fixture)
        relative = "configuration/shop-supplier-order-correction-selection.json"
        selection_path = fixture / "input" / relative
        selection = _load(selection_path)
        selection["correction"]["source_record_ordinal"] = 99
        _write_json(selection_path, selection)
        mapping = _load(CORRECTION_MAPPING)
        mapping["input_manifest_sha256"] = _rehash_fixture_member(fixture, relative)
        mapping_path = tmp_path / "correction-mapping.json"
        _write_json(mapping_path, mapping)
        program["inputs"]["correction"]["mapping_sha256"] = _digest(mapping_path)
        program_path = tmp_path / "run.json"
        _write_json(program_path, program)
        arguments = {
            "program_path": program_path,
            "correction_fixture": fixture,
            "correction_mapping": mapping_path,
        }

    with pytest.raises(ShowcaseRefusal, match="selection and mapping differ"):
        run_showcase(output, **arguments)
    assert not (output / "history.jsonl").exists()


@pytest.mark.parametrize("mutation", ["ID", "ALGORITHM", "OUTCOMES"])
def test_coherently_rehashed_unsupported_check_contract_refuses_before_history(
    tmp_path: Path, mutation: str
) -> None:
    check = _load(CHECK)
    if mutation == "ID":
        check["check_contract_id"] = "different-check"
    elif mutation == "ALGORITHM":
        check["algorithm"] = "TRUST_RECORDED_OUTCOME"
    else:
        check["outcomes"] = ["SATISFIED"]
    check_path = tmp_path / "check.json"
    _write_json(check_path, check)

    policy = _load(POLICY)
    policy["required_checks"][0]["check_contract_id"] = check["check_contract_id"]
    policy["required_checks"][0]["check_contract_identity"] = _digest(check_path)
    policy_path = tmp_path / "policy.json"
    _write_json(policy_path, policy)

    program = _load(RUN)
    program["inputs"]["check_contract"]["sha256"] = _digest(check_path)
    program["inputs"]["policy"]["sha256"] = _digest(policy_path)
    program_path = tmp_path / "run.json"
    _write_json(program_path, program)
    output = tmp_path / "proof"

    with pytest.raises(ShowcaseRefusal, match="unsupported source-mapping check"):
        run_showcase(
            output,
            program_path=program_path,
            policy_path=policy_path,
            check_contract=check_path,
        )
    assert not (output / "history.jsonl").exists()


@pytest.mark.parametrize(
    ("relative", "needle", "replacement"),
    [
        ("input/manifest.json", b'"fixture_id": "OKG-FX001"', b'"fixture_id": "BAD"'),
        ("input/sources/payments.jsonl", b'"payment_id":"P1"', b'"payment_id":"P9"'),
        (
            "input/configuration/shop-payment-settlement-selection.json",
            b'"payment_id": "P1"',
            b'"payment_id": "P9"',
        ),
    ],
)
def test_tampered_settlement_input_refuses_before_history(
    tmp_path: Path, relative: str, needle: bytes, replacement: bytes
) -> None:
    fixture = tmp_path / "fixture"
    shutil.copytree(FIXTURE, fixture)
    path = fixture / relative
    path.write_bytes(path.read_bytes().replace(needle, replacement))
    output = tmp_path / "proof"
    with pytest.raises(ShowcaseRefusal):
        run_showcase(output, settlement_fixture=fixture)
    assert not (output / "history.jsonl").exists()


def test_tampered_mapping_refuses_before_history(tmp_path: Path) -> None:
    mapping = tmp_path / "mapping.json"
    mapping.write_bytes(MAPPING.read_bytes().replace(b'"Payment"', b'"Invoice"', 1))
    output = tmp_path / "proof"
    with pytest.raises(ShowcaseRefusal):
        run_showcase(output, settlement_mapping=mapping)
    assert not (output / "history.jsonl").exists()


@pytest.mark.parametrize("mutation", ["WRONG_ENDPOINT", "WRONG_TYPE", "MISSING_I2"])
def test_invalid_payment_shape_refuses_one_stage_atomically(
    tmp_path: Path, mutation: str
) -> None:
    mapping_value = _load(MAPPING)
    if mutation == "WRONG_ENDPOINT":
        mapping_value["stages"][1]["operations"][1]["target_id"] = "X1"
    elif mutation == "WRONG_TYPE":
        mapping_value["stages"][1]["operations"][1]["record_type"] = "OrderContainsUnit"
    else:
        mapping_value["stages"][0]["operations"] = mapping_value["stages"][0][
            "operations"
        ][:1]
        mapping_value["stages"][0]["selections"] = mapping_value["stages"][0][
            "selections"
        ][:1]
    changed_mapping = tmp_path / "settlement-mapping.json"
    changed_mapping.write_bytes(_canonical(mapping_value))
    program = _load(RUN)
    program["inputs"]["settlement"]["mapping_sha256"] = _digest(changed_mapping)
    changed_program = tmp_path / "run.json"
    changed_program.write_bytes(_canonical(program))
    output = tmp_path / "proof"
    if mutation == "MISSING_I2":
        with pytest.raises(ShowcaseRefusal, match="mapping shape is incomplete"):
            run_showcase(
                output,
                program_path=changed_program,
                settlement_mapping=changed_mapping,
            )
        assert not (output / "history.jsonl").exists()
        return

    prepared = _prepare_showcase(
        output, program_path=changed_program, settlement_mapping=changed_mapping
    )
    target_index = next(
        index
        for index, stage in enumerate(prepared.stages)
        if stage.selector == "SETTLEMENT:1"
    )
    for stage in prepared.stages[:target_index]:
        _admit_stage(prepared, stage)
    before_bytes = (output / "history.jsonl").read_bytes()
    before = prepared.history.replay()

    with pytest.raises(ShowcaseRefusal):
        _admit_stage(prepared, prepared.stages[target_index])

    after = prepared.history.replay()
    assert (output / "history.jsonl").read_bytes() == before_bytes
    assert after.receipt == before.receipt
    assert after.graph.snapshot() == before.graph.snapshot()


def test_unexpected_compiler_errors_are_not_mislabeled_as_contract_refusals(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def programming_error(_closure):
        raise RuntimeError("programming defect")

    monkeypatch.setattr(run_module, "adapt_linkml_closure", programming_error)
    with pytest.raises(RuntimeError, match="programming defect"):
        run_showcase(tmp_path / "proof")


def test_unexpected_stage_errors_propagate_without_mutating_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "proof"
    prepared = _prepare_showcase(output)
    history_path = output / "history.jsonl"
    before = history_path.read_bytes()

    def programming_error(_stage):
        raise ValueError("programming defect")

    monkeypatch.setattr(run_module, "verify_stage", programming_error)

    with pytest.raises(ValueError, match="programming defect"):
        _admit_stage(prepared, prepared.stages[0])

    assert history_path.read_bytes() == before


def test_published_predecessor_bytes_remain_exact(proof) -> None:
    _ = proof
    assert _digest(BASE_FIXTURE / "input/manifest.json") == (
        "sha256:7583bfbc6f9aff6382727a7befa333c82b73bed221d8958d6bb7e1a55d0549e8"
    )
    assert _digest(CORRECTION_FIXTURE / "input/manifest.json") == (
        "sha256:3ae5281e505882ba14fab159ff85e7f433ba79a6936c1113a5f0e54a1cc8ad13"
    )
    assert _digest(CORRECTION_EVIDENCE) == (
        "sha256:c764c8eba79a533b3162ec3f383dab15c330127f4248df96b9bafeebe3b69aea"
    )

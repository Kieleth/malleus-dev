"""TDD contract for the compact Small Shop showcase evidence projection."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import pytest

from research.ontology_driven_kg_realization.experiments.small_shop.showcase import (
    evidence as evidence_module,
)
from research.ontology_driven_kg_realization.experiments.small_shop.showcase.evidence import (
    generate_evidence,
)
from research.ontology_driven_kg_realization.experiments.small_shop.showcase.query import (
    current_supplier_order,
    order_contents,
    payment_settlements,
    query_state_coordinates,
    record_change_provenance,
    state_after_change,
    supplier_order_history,
)
from research.ontology_driven_kg_realization.experiments.small_shop.showcase.run import (
    retained_context,
    run_showcase,
    verify_source_mapping_receipts,
)


HERE = Path(__file__).parent
EVIDENCE = HERE / "evidence"
FILES = ("explanation.json", "graph.json", "queries.json", "receipt.json")
E4_CHANGE = "change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e4"
E4_RECORD = "supplier-order-state:B:e4"
CURRENT_IDS = {
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


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _value(source: bytes) -> dict[str, object]:
    value = json.loads(source)
    assert isinstance(value, dict)
    assert source == _canonical(value)
    return value


@pytest.fixture(scope="module")
def projection(tmp_path_factory: pytest.TempPathFactory):
    root = tmp_path_factory.mktemp("small-shop-evidence")
    output = root / "evidence"
    generated = generate_evidence(output)
    replay = run_showcase(root / "independent-run").replay
    return output, generated, replay


def test_regeneration_is_canonical_byte_identical_and_matches_runner(
    projection, tmp_path: Path
) -> None:
    output, generated, replay = projection
    second = tmp_path / "evidence"
    regenerated = generate_evidence(second)

    assert tuple(sorted(path.name for path in output.iterdir())) == FILES
    assert tuple(sorted(generated)) == FILES
    assert generated == regenerated
    assert {name: (output / name).read_bytes() for name in FILES} == generated
    assert {name: (second / name).read_bytes() for name in FILES} == generated
    assert {name: (EVIDENCE / name).read_bytes() for name in FILES} == generated
    assert generated["receipt.json"] == replay.receipt.canonical_bytes
    assert generated["graph.json"] == _canonical(replay.graph.snapshot())
    assert all(_value(source) for source in generated.values())


def test_explanation_is_an_exact_projection_of_the_verified_replay(projection) -> None:
    _, generated, replay = projection
    explanation = _value(generated["explanation.json"])
    receipt = _value(generated["receipt.json"])
    graph = _value(generated["graph.json"])
    program, _, _ = retained_context(replay)
    retained = {item.record_id: item for item in replay.retained_inputs}
    contract = retained["artifact:small-shop-showcase:validated-contract"]
    contract_value = _value(contract.content)

    assert explanation["schema"] == "malleus.small-shop.showcase-evidence/private-v0"
    assert explanation["scope"] == "RESEARCH_LOCAL_NO_STABLE_API_OR_WIRE"
    assert explanation["runtime_oracle_named_inputs"] == []
    assert explanation["coordinates"] == {
        "contract": {
            "effective_contract_identity": replay.partial_contract.identity,
            "fact_count": contract_value["fact_count"],
            "facts_identity": contract_value["facts_sha256"],
            "validated_contract_artifact_id": contract.record_id,
            "validated_contract_artifact_identity": contract.identity,
            "validated_fact_set_identity": contract_value["validated_fact_set_sha256"],
        },
        "graph": {
            "current_record_count": 9,
            "ontology_identity": graph["ontology_hash"],
            "state_digest": receipt["graph_state_digest"],
        },
        "history": {
            "acceptance_head": replay.acceptance_head,
            "binding_identity": replay.binding.identity,
            "event_count": replay.ledger_event_count,
            "ledger_head": replay.ledger_head,
            "materialization_head": replay.materialization_head,
            "receipt_identity": replay.receipt.identity,
        },
    }
    assert [item["change_set_id"] for item in explanation["accepted_changes"]] == [
        change.change_set_id for change in replay.change_sets
    ]
    assert [item["identity"] for item in explanation["accepted_changes"]] == [
        change.identity for change in replay.change_sets
    ]
    assert all(
        item["contract_identity"] == replay.partial_contract.identity
        for item in explanation["accepted_changes"]
    )
    assert [item["ordinal"] for item in explanation["accepted_changes"]] == list(
        range(5)
    )
    changes = {item["change_set_id"]: item for item in explanation["accepted_changes"]}
    assert changes[E4_CHANGE]["operations"][0]["properties"]["ordered_quantity"] == 1
    assert (
        changes["change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e7"]["operations"][0][
            "properties"
        ]["ordered_quantity"]
        == 2
    )
    assert explanation["source_mapping_receipts"] == [
        {
            "change_set_id": item.change_set_id,
            "receipt_identity": item.receipt_identity,
        }
        for item in verify_source_mapping_receipts(replay)
    ]
    assert len(explanation["source_mapping_receipts"]) == 5
    assert explanation["run_program"] == {
        "decisions": program["decisions"],
        "identity": retained["artifact:small-shop-showcase:run-program"].identity,
        "limitations": program["limitations"],
        "record_id": "artifact:small-shop-showcase:run-program",
    }

    contract_facts = contract_value["facts"]
    selected = explanation["representative_contract_facts"]
    assert len(selected) == 5
    assert all(fact in contract_facts for fact in selected)
    assert {fact["subject"].rsplit("/", 1)[-1] for fact in selected} == {
        "Invoice",
        "Payment",
        "PaymentSettlesInvoiceRelation",
        "SalesOrder",
        "SupplierOrderState",
    }


def test_current_graph_and_full_record_history_remain_distinct(projection) -> None:
    _, generated, replay = projection
    graph = _value(generated["graph.json"])
    explanation = _value(generated["explanation.json"])

    current_ids = {node["id"] for node in graph["nodes"]} | {
        relation["key"] for relation in graph["relations"]
    }
    assert current_ids == CURRENT_IDS
    assert E4_RECORD not in current_ids
    assert {item["record_id"] for item in explanation["record_history"]} == set(
        replay.record_history
    )
    e4 = next(
        item for item in explanation["record_history"] if item["record_id"] == E4_RECORD
    )
    assert e4 == {
        "change_set_id": E4_CHANGE,
        "record_id": E4_RECORD,
        "superseded_by": "supplier-order-state:B:e7",
        "supersedes_record_id": None,
        "valid_from": {"kind": "ORDER_ONLY", "value": "e4"},
        "valid_to": {"kind": "ORDER_ONLY", "value": "e7"},
    }
    assert [
        (relation["source_id"], relation["target_id"])
        for relation in graph["relations"]
        if relation["type"] == "PaymentSettlesInvoiceRelation"
    ] == [
        ("payment:P1", "invoice:I1"),
        ("payment:P1", "invoice:I2"),
    ]


def test_query_evidence_contains_only_canonical_existing_query_answers(
    projection,
) -> None:
    _, generated, replay = projection
    queries = _value(generated["queries.json"])
    expected = [
        order_contents(replay, "O1"),
        payment_settlements(replay, "P1"),
        current_supplier_order(replay, "B"),
        supplier_order_history(replay, "B"),
        state_after_change(replay, E4_CHANGE),
        record_change_provenance(replay, "relation:P1:I1"),
        record_change_provenance(replay, E4_RECORD),
        query_state_coordinates(replay),
    ]

    assert queries == {
        "answers": [json.loads(source) for source in expected],
        "schema": "malleus.small-shop.showcase-queries/private-v0",
        "scope": "READ_ONLY_REPLAY_DERIVED_RESEARCH_EVIDENCE",
    }
    assert all(source == _canonical(json.loads(source)) for source in expected)


def test_generation_reads_no_oracle_and_writes_only_below_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "evidence"
    seen_runs: list[Path] = []
    seen_writes: list[Path] = []
    real_run = evidence_module.run_showcase
    real_read = Path.read_bytes
    real_write = Path.write_bytes

    def guarded_read(path: Path) -> bytes:
        if "oracle" in {part.lower() for part in path.parts}:
            raise AssertionError(f"oracle read: {path}")
        return real_read(path)

    def observed_run(path: Path):
        selected = Path(path)
        seen_runs.append(selected)
        return real_run(selected)

    def observed_write(path: Path, source: bytes) -> int:
        selected = Path(path)
        seen_writes.append(selected)
        return real_write(selected, source)

    monkeypatch.setattr(Path, "read_bytes", guarded_read)
    monkeypatch.setattr(Path, "write_bytes", observed_write)
    monkeypatch.setattr(evidence_module, "run_showcase", observed_run)

    generated = generate_evidence(output)

    boundary = output.resolve()
    assert len(seen_runs) == 2
    assert all(path.resolve().is_relative_to(boundary) for path in seen_runs)
    assert all(path.resolve().is_relative_to(boundary) for path in seen_writes)
    assert set(tmp_path.iterdir()) == {output}
    assert tuple(sorted(path.name for path in output.iterdir())) == FILES
    assert generated["receipt.json"]

    replay = real_run(output / "independent-check").replay
    retained = replay.retained_inputs
    oracle = (
        HERE.parents[2]
        / "fixtures/small_shop_fulfilment_settlement_v1"
        / "oracle/shop-payment-settlement.json"
    )
    oracle_identity = "sha256:" + sha256(real_read(oracle)).hexdigest()
    assert oracle_identity not in {item.identity for item in retained}
    assert all("oracle" not in item.record_id.lower() for item in retained)


def test_generator_has_no_raw_ledger_parser_or_second_authority() -> None:
    source = Path(evidence_module.__file__).read_text(encoding="utf-8")
    assert "history.jsonl" not in source
    assert "KnowledgeChangeHistory" not in source
    assert "jsonlines" not in source
    assert "oracle/shop-payment-settlement.json" not in source


def test_all_output_targets_are_preflighted_before_any_write(tmp_path: Path) -> None:
    output = tmp_path / "evidence"
    outside = tmp_path / "outside.json"
    output.mkdir()
    (output / "receipt.json").symlink_to(outside)

    with pytest.raises(evidence_module.EvidenceError, match="symlink output"):
        evidence_module._write(
            output,
            {"graph.json": b"{}", "receipt.json": b"{}"},
        )

    assert not outside.exists()
    assert not (output / "graph.json").exists()

"""Frozen input/oracle checks only, not an action or protocol implementation."""

from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures/supplier_commitment_v1"
CANONICAL = (
    ROOT / "research/ontology_driven_kg_realization/fixtures"
    "/small_shop_fulfilment_correction_v1/input/sources/supplier-order-history.jsonl"
)
FIELDS = {"event_id", "supplier_order_id", "product_code", "quantity"}


def read_json(name):
    return json.loads((FIXTURE / name).read_bytes())


@pytest.fixture
def source_validator():
    schema = read_json("source.schema.json")
    Draft202012Validator.check_schema(schema)
    assert schema["additionalProperties"] is False
    assert set(schema["properties"]) == FIELDS
    assert set(schema["required"]) == FIELDS
    return Draft202012Validator(schema)


def test_initial_source_is_exact_canonical_e4_only(source_validator):
    content = (FIXTURE / "input/supplier-before.jsonl").read_bytes()
    assert content == CANONICAL.read_bytes().splitlines(keepends=True)[0]
    row = json.loads(content)
    assert row == {
        "event_id": "e4",
        "product_code": "Y",
        "quantity": 1,
        "supplier_order_id": "B",
    }
    source_validator.validate(row)


def test_after_file_is_an_oracle_not_observed_input(source_validator):
    case = read_json("case.json")
    after = case["expected_source"]
    assert after["path"] == "oracle/supplier-after.jsonl"
    assert after["role"] == "EXPECTED_OUTPUT_ONLY"
    assert sorted(path.name for path in (FIXTURE / "input").iterdir()) == [
        "supplier-before.jsonl"
    ]
    row = json.loads((FIXTURE / after["path"]).read_bytes())
    assert row == {
        "event_id": "reentry-amendment-1",
        "product_code": "Y",
        "quantity": 2,
        "supplier_order_id": "B",
    }
    assert row["event_id"] not in {"e4", "e7"}
    source_validator.validate(row)


def test_fixture_contract_and_exact_source_hashes():
    case = read_json("case.json")
    assert set(case) == {
        "schema",
        "classification",
        "claim",
        "episode",
        "source",
        "expected_source",
        "goal",
        "operator",
        "mapping",
        "preservation",
        "stopping",
        "protocol_dependency",
    }
    assert case["schema"] == "malleus.reentry.supplier-fixture/research-v1"
    assert case["classification"] == "CONFORMANCE_FIXTURE"
    assert case["claim"] == "FROZEN_INPUTS_NOT_EXECUTED_ACTION"
    assert case["source"]["path"] == "input/supplier-before.jsonl"
    assert case["source"]["role"] == "SYNTHETIC_INITIAL_SOURCE"
    assert case["source"]["sha256"] != case["expected_source"]["sha256"]
    for name in ("source", "expected_source"):
        entry = case[name]
        assert set(entry) == {"path", "sha256", "role"}
        actual = "sha256:" + sha256((FIXTURE / entry["path"]).read_bytes()).hexdigest()
        assert entry["sha256"] == actual
    assert case["protocol_dependency"] == "CORE_COMPILED_ASSENT_CLOSURE_REQUIRED"
    assert case["episode"]["action_key"] == case["episode"]["id"]
    assert case["goal"] == {
        "kind": "GoalPredicate",
        "supplier_order_id": "B",
        "product_code": "Y",
        "operator": "EQUALS",
        "quantity": 2,
    }
    assert case["operator"] == {
        "kind": "AMEND_SUPPLIER_ORDER",
        "expected_quantity": 1,
        "requested_quantity": 2,
        "new_source_occurrence_id": "reentry-amendment-1",
        "precondition": "EXACT_CAPTURED_PRESTATE_BYTES",
        "changed_fields": ["event_id", "quantity"],
    }
    assert case["stopping"] == {
        "candidate_budget": 1,
        "dispatch_attempt_budget": 1,
        "automatic_retry": False,
        "ambiguity": "REFUSE_IF_NOT_UNIQUE",
        "pending_is_satisfied": False,
    }


def test_mapping_covers_every_source_field_without_forged_runtime_coordinates():
    case = read_json("case.json")
    assert case["mapping"] == {
        "type": "SupplierOrderState",
        "initial_record_id": "supplier-order-state:B:e4",
        "replacement_record_id": "supplier-order-state:B:reentry-amendment-1",
        "supersedes_record_id": "supplier-order-state:B:e4",
        "valid_time_kind": "ORDER_ONLY",
        "fields": {
            "source_occurrence_id": "event_id",
            "ordered_quantity": "quantity",
            "product_code": "product_code",
            "supplier_order_id": "supplier_order_id",
        },
    }
    assert set(case["mapping"]["fields"].values()) == FIELDS
    assert case["preservation"] == {
        "mode": "ALL_OTHER_ACCEPTED_RECORDS_AND_HISTORY",
        "required_ids": ["O1", "X1", "contains:O1:X1"],
    }


@pytest.mark.parametrize("field", sorted(FIELDS))
def test_source_contract_refuses_each_missing_field(source_validator, field):
    row = json.loads((FIXTURE / "input/supplier-before.jsonl").read_bytes())
    del row[field]
    assert not source_validator.is_valid(row)


@pytest.mark.parametrize(
    "change",
    [
        {"extra": "undeclared"},
        {"quantity": True},
        {"quantity": "1"},
        {"event_id": ""},
        {"product_code": None},
    ],
)
def test_source_contract_refuses_unknown_or_mistyped_meaning(source_validator, change):
    row = json.loads((FIXTURE / "input/supplier-before.jsonl").read_bytes())
    row.update(change)
    assert not source_validator.is_valid(row)


def test_well_formed_quantity_three_is_not_a_source_grammar_failure(source_validator):
    row = json.loads((FIXTURE / "input/supplier-before.jsonl").read_bytes())
    row["quantity"] = 3
    source_validator.validate(row)
    assert row["quantity"] != read_json("case.json")["goal"]["quantity"]


def test_oracle_delays_kg_change_until_acceptance():
    expected = read_json("oracle/expected.json")
    assert expected["claim"] == "EXPECTED_OBSERVATIONS_NOT_EXECUTION_RESULTS"
    stages = expected["success_path"]
    assert [stage["stage"] for stage in stages] == [
        "INITIAL_KCS_ACCEPTED",
        "ACTION_PROPOSED",
        "ACTION_ACCEPTED",
        "AUTHORIZED",
        "DISPATCHED",
        "EXECUTION_RECORDED",
        "OBSERVATION_RECORDED",
        "OBSERVED_KCS_PROPOSED",
        "OBSERVED_KCS_ACCEPTED",
        "FRESH_REASSESSMENT",
    ]
    assert [stage["accepted_quantity"] for stage in stages] == [1] * 8 + [2, 2]
    assert stages[-1]["result"] == "SATISFIED"
    assert stages[-1]["new_candidates"] == 0
    assert stages[-1]["writes"] == 0
    outcomes = expected["negative_cases"]
    assert set(outcomes) == {
        "success_receipt_unchanged_source",
        "failure_without_capture",
        "failure_after_write_with_supporting_capture",
        "pending_reassessment",
        "well_formed_quantity_three",
        "stale_satisfied_projection",
    }
    assert outcomes["failure_without_capture"]["accepted_quantity"] == 1
    assert outcomes["success_receipt_unchanged_source"]["accepted_quantity"] == 1
    assert outcomes["pending_reassessment"]["result"] == "PENDING"
    assert outcomes["well_formed_quantity_three"]["result"] == "UNREALIZABLE"
    assert outcomes["stale_satisfied_projection"]["result"] == "STALE_BASE"
    failure = outcomes["failure_after_write_with_supporting_capture"]
    assert failure["execution_status"] == "FAILED"
    assert failure["accepted_quantity_after_kcs"] == 2
    assert failure["causality_claim"] is False


def test_source_schema_does_not_supply_required_defaults():
    schema = read_json("source.schema.json")
    assert set(schema) == {
        "$schema",
        "title",
        "type",
        "additionalProperties",
        "required",
        "properties",
    }
    assert schema["type"] == "object"
    assert all("default" not in field for field in schema["properties"].values())

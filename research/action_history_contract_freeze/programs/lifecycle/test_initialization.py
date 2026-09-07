"""Static initialization/registration definitions, with no history execution."""

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from malleus.assent import ProtocolError, _canonical_unique
from malleus.ledger import content_digest, record_hash
from malleus.source import source_artifact_digest
from research.action_history_contract_freeze.programs.packet_validator import (
    FORMATS,
    PacketRefusal,
    validate_program,
)
from research.action_history_contract_freeze.programs.test_input_carrier import (
    candidate,
    source_record,
)
from research.action_history_contract_freeze.test_definition import shape_witness
from tests.contract_compiler.pareto.test_assent_contract_compatibility import _compile


HERE = Path(__file__).parent


def packet(name):
    return json.loads((HERE / f"{name}.json").read_bytes())


def check(value):
    return validate_program(
        value["program"],
        profile=value["profile"],
        instruction_schema=json.loads(
            (HERE.parents[1] / "instructions.schema.json").read_bytes()
        ),
    )


@pytest.mark.parametrize("name", ["initialization", "source-registration"])
def test_definitions_are_static_and_preserve_inputs(name):
    value = packet(name)
    before = deepcopy(value)
    assert check(value) == {
        "status": "STATIC_VALID",
        "steps": len(value["program"]["steps"]),
        "runtime_executed": False,
    }
    assert value == before
    assert value["status"] == "STATIC_VALID_PARTIAL"
    assert value["runtime_executed"] is False
    assert value["unresolved"] and all(isinstance(x, str) for x in value["unresolved"])


def test_initialization_keeps_checkpoint_shape_and_exact_dependency_roles():
    value = packet("initialization")
    checkpoint = shape_witness("initialization")
    schema = value["program"]["inputs"]["artifact"]["checkpoint"]
    Draft202012Validator(schema, format_checker=FORMATS).validate({"value": checkpoint})
    shape = schema["properties"]["value"]
    assert set(checkpoint) == set(shape["properties"]) == set(shape["required"])
    steps = value["program"]["steps"]
    resolves = [s for s in steps if s["opcode"] == "RESOLVE_RECORD"]
    assert {s["result"] for s in resolves} == {
        "profile",
        "record_contract",
        "machine",
        "history_binding",
        "epistemic_policy",
        "authorization_policy",
    }
    assert all(s["scope"] == "APPLIED" for s in resolves)
    for role in ("profile", "record_contract", "machine", "history_binding"):
        step = next(
            s for s in steps if s["refusal"] == f"{role.upper()}_BYTES_MISMATCH"
        )
        assert step["left"]["path"][-1] == "source_content_digest"
        assert step["right"]["path"][-1] == "bytes_sha256"


def test_initialization_uses_one_singleton_and_only_checkpoint_digest_for_a():
    value = packet("initialization")
    steps = value["program"]["steps"]
    unique = next(s for s in steps if s["refusal"] == "ALREADY_INITIALIZED")
    assert unique["target_index"] == "initialization"
    assert unique["records"] == {
        "root": "artifact",
        "name": "singleton",
        "path": ["value"],
    }
    assert unique["key_paths"] == [["key"]]
    singleton = value["program"]["inputs"]["artifact"]["singleton"]
    assert (
        singleton["properties"]["value"]["items"]["properties"]["key"]["const"]
        == "ACTIVE"
    )
    effects = [s for s in steps if s["opcode"] == "SET_PROTOCOL_STATE"]
    assert len(effects) == 2
    assert {s["target"] for s in effects} == {
        "PROTOCOL_INDEX",
        "ACTION_ACCEPTANCE_HEAD",
    }
    assert all(
        s["value"] == {"root": "result", "name": "checkpoint-hash", "path": ["value"]}
        for s in effects
    )
    hash_step = next(s for s in steps if s.get("result") == "checkpoint-hash")
    assert hash_step["opcode"] == "HASH" and hash_step["recipe"] == "VALUE"
    assert hash_step["value"] == {
        "root": "artifact",
        "name": "checkpoint",
        "path": ["value"],
    }
    assert steps.index(unique) < next(
        i for i, s in enumerate(steps) if s["opcode"] == "INTRODUCE_RECORDS"
    )


@pytest.mark.parametrize("name", ["initialization", "source-registration"])
def test_source_record_variant_is_complete_under_real_assent(name):
    value = packet(name)
    source = source_record(candidate(), "registration-shape", b"exact bytes")
    assert _compile().view.validate_instance("SourceArtifact", source) == []
    shape = value["program"]["inputs"]["event"]["records"]
    Draft202012Validator(shape, format_checker=FORMATS).validate(
        {"value": [{"record_type": "SourceArtifact", "record": source}]}
    )
    record = shape["properties"]["value"]["items"]["properties"]["record"]
    assert set(record["properties"]) == set(record["required"]) == set(source)


def test_source_hash_projection_matches_existing_recipe_and_not_provenance_hash():
    value = packet("source-registration")
    projection = value["semantic_hash_contract"]["preimage_fields"]
    assert projection == {
        "source_schema_version": "source_schema_version",
        "artifact_id": "id",
        "artifact_version": "artifact_version",
        "source_content_digest": "source_content_digest",
        "source_byte_length": "source_byte_length",
        "source_media_type": "source_media_type",
        "source_locator": "source_locator",
    }
    record = source_record(candidate(), "source-projection", b"exact bytes")
    expected = source_artifact_digest(
        schema_version=record["source_schema_version"],
        artifact_id=record["id"],
        artifact_version=record["artifact_version"],
        source_content_digest=record["source_content_digest"],
        source_byte_length=record["source_byte_length"],
        source_media_type=record["source_media_type"],
        source_locator=record["source_locator"],
    )
    assert (
        content_digest({key: record[field] for key, field in projection.items()})
        == expected
    )
    assert expected == record["artifact_hash"] != record["content_hash"]
    changed = {**record, "responsible_actor_id": "actor:other"}
    assert record_hash("SourceArtifact", changed) != record["content_hash"]
    assert (
        content_digest({key: changed[field] for key, field in projection.items()})
        == expected
    )
    contract_shape = value["program"]["inputs"]["artifact"]["source_contract"]
    Draft202012Validator(contract_shape).validate(
        {"value": value["semantic_hash_contract"]}
    )


@pytest.mark.parametrize(
    "fault", ["domain-head", "unbound-input", "wrong-a-source", "domain-target"]
)
def test_initialization_definition_rejects_coordinate_and_binding_errors(fault):
    value = packet("initialization")
    steps = value["program"]["steps"]
    if fault == "domain-head":
        step = next(s for s in steps if s["refusal"] == "STALE_FULL_HEAD")
        step["right"]["path"] = ["domain", "kcs_acceptance_head"]
    elif fault == "unbound-input":
        del value["program"]["inputs"]["current"]["selected"]
    elif fault == "wrong-a-source":
        steps[-1]["value"] = {
            "root": "current",
            "name": "base",
            "path": ["domain", "accepted_graph_digest"],
        }
    else:
        steps[-1]["target"] = "KCS_ACCEPTANCE_HEAD"
    with pytest.raises(PacketRefusal):
        check(value)


def test_existing_order_rule_and_missing_instruction_are_separate_observations():
    value = packet("registration-order-gap")
    assert value["status"] == "INSTRUCTION_DECISION_REQUIRED"
    _canonical_unique(value["positive"], "ordered witness")
    with pytest.raises(ProtocolError):
        _canonical_unique(value["negative"], "reversed witness")
    assert set(value["positive"]) == set(value["negative"])
    schema = json.loads((HERE.parents[1] / "instructions.schema.json").read_bytes())
    assert not Draft202012Validator(schema).is_valid(value["attempted_instruction"])
    with pytest.raises(PacketRefusal) as caught:
        check(value)
    assert caught.value.reason == "INSTRUCTION_SHAPE"
    unique_only = deepcopy(value)
    unique_only["program"]["steps"] = unique_only["program"]["steps"][:1]
    assert check(unique_only)["status"] == "STATIC_VALID"
    assert value["attempted_instruction"]["value_kind"] == "STRING"
    assert value["attempted_instruction"]["comparison"] == "LT"

"""Existing carrier/typed-content compatibility, without retention or execution."""

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
import pytest

import malleus.compiler as api
from malleus.assent import make_record
from malleus.ledger import canonical_json, record_hash
from malleus.source import source_artifact_fields, source_bytes_digest
from research.action_history_contract_freeze.programs.packet_validator import (
    FORMATS,
    PacketRefusal,
    validate_content,
    validate_interval,
)
from research.action_history_contract_freeze.test_definition import shape_witness
from tests.contract_compiler.pareto.test_assent_contract_compatibility import _compile


HERE = Path(__file__).parent
ROLES = (
    "record_contract",
    "scope_association",
    "requested_interval",
    "original_context",
    "current_context",
)


def candidate():
    return json.loads((HERE / "input-bindings.json").read_bytes())


@pytest.fixture(scope="module")
def compiled():
    return _compile()


def input_bytes(role, compiled):
    if role == "record_contract":
        return compiled.artifact.artifact_bytes
    examples = json.loads((HERE / "content-examples.json").read_bytes())
    values = {
        "scope_association": examples["scope"],
        "requested_interval": {"start": "2026-09-07T00:00:00Z"},
        "original_context": shape_witness("original-context"),
        "current_context": examples["current"],
    }
    return canonical_json(values[role]).encode()


def source_record(definition, role, content):
    """Uses existing constructors, not an input resolver or a new producer."""
    return make_record(
        definition["carrier"]["record_type"],
        id=f"input:{role}:shape-only",
        event_id="event:source-shape",
        generated_at="2026-09-07T00:00:00Z",
        actor_id="actor:registrar",
        role="registrar",
        source_record_ids=[],
        artifact_kind=definition["carrier"]["artifact_kind"],
        artifact_version="shape-v1",
        **source_artifact_fields(
            artifact_id=f"input:{role}:shape-only",
            artifact_version="shape-v1",
            source_bytes=content,
            media_type="application/json",
            locator=f"urn:shape-only:check-input:{role}",
        ),
    )


def check_content(kind, content):
    """Test-only closed routing to existing parsers. No callable in input data."""
    if kind == "compiled-record-contract":
        return api.load_validated_contract_artifact(content)
    value = json.loads(content)
    if kind in {"scope", "current"}:
        return validate_content(kind, value)
    if kind == "interval":
        return validate_interval(value)
    assert kind == "original-context"
    schema = json.loads((HERE.parent / "contexts.schema.json").read_bytes())
    Draft202012Validator(schema, format_checker=FORMATS).validate(value)
    assert value["schema"] == "malleus.action-history.original-context/research-v1"


@pytest.mark.parametrize("role", ROLES)
def test_existing_carrier_and_role_content_both_validate(compiled, role):
    definition, content = candidate(), input_bytes(role, compiled)
    record = source_record(definition, role, content)
    before = deepcopy(record)
    assert compiled.view.is_subtype_of(
        definition["carrier"]["record_type"], "ProtocolArtifact"
    )
    assert (
        compiled.view.validate_instance(definition["carrier"]["record_type"], record)
        == []
    )
    links = definition["identity_fields"]
    assert links == {
        "reference_id": "id",
        "reference_bytes_sha256": "source_content_digest",
        "record_hash": "content_hash",
        "semantic_artifact_hash": "artifact_hash",
        "byte_length": "source_byte_length",
    }
    assert record[links["byte_length"]] == len(content)
    assert record[links["reference_bytes_sha256"]] == source_bytes_digest(content)
    assert record[links["record_hash"]] == record_hash("SourceArtifact", record)
    assert (
        len(
            {
                record[key]
                for key in ("content_hash", "artifact_hash", "source_content_digest")
            }
        )
        == 3
    )
    check_content(definition["byte_inputs"][role], content)
    assert record == before
    altered = source_record(definition, role, content + b" ")
    for field in (
        "content_hash",
        "artifact_hash",
        "source_content_digest",
        "source_byte_length",
    ):
        assert altered[field] != record[field]


@pytest.mark.parametrize("role", ROLES)
def test_valid_byte_carrier_does_not_establish_content_type(compiled, role):
    definition = candidate()
    content = b"{}"
    record = source_record(definition, role, content)
    assert compiled.view.validate_instance("SourceArtifact", record) == []
    # The existing carrier honestly describes these bytes, but they are not
    # any of the declared role contents. Never promote byte validity to readiness.
    with pytest.raises((api.ArtifactRefusal, PacketRefusal, ValidationError)):
        check_content(definition["byte_inputs"][role], content)


def test_table_covers_existing_invocation_roles_without_coercion(compiled):
    definition = candidate()
    contract = json.loads((HERE / "monitor-contract.json").read_bytes())
    declared = (
        set(definition["byte_inputs"])
        | set(definition["record_inputs"])
        | set(definition["scalar_inputs"])
    )
    roles = set(contract["TYPE"]["ordered_inputs"]) | set(
        contract["DIRECT_GRANT"]["ordered_inputs"]
    )
    assert declared == roles
    assert definition["record_inputs"] == {
        "proposal": "ProposedSubgraph",
        "action": "ActionProposal",
        "grant": "AuthorityGrant",
        "authorization_policy": "AuthorizationPolicyArtifact",
    }
    for record_type in definition["record_inputs"].values():
        assert compiled.view.is_subtype_of(record_type, "ProtocolRecord")
    assert definition["scalar_inputs"] == {"executor_id": "string"}
    assert definition["carrier"] == {
        "record_type": "SourceArtifact",
        "artifact_kind": "SOURCE",
    }
    assert tuple(definition["byte_inputs"]) == ROLES
    assert definition["status"] == "ACCEPTED_CARRIER_NOT_RUNTIME_BINDING"
    assert not (HERE / "input-carrier-candidate.json").exists()
    assert definition["unbound"] == [
        "history_retention_event_binding",
        "applied_prefix_resolution",
        "content_id_association",
        "static_dependency_set",
        "input_and_source_closure_order",
        "producer_implementations",
    ]

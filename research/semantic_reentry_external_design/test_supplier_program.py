"""Fresh supplier program data must cross Core's actual definition boundary."""

from copy import deepcopy
from importlib import import_module
import json

import pytest

from malleus._contract_pipeline.protocol_runtime import load_bundle, raw
from research.semantic_reentry_external_design.test_supplier_action_contract import (
    FIELDS,
    action_compilation as action_compilation,
)


MODULE = "research.semantic_reentry_external_design.supplier_program"
SOURCES = {
    role: "source:supplier:selected:" + role
    for role in ("profile", "record_contract", "machine", "history_binding")
}
POLICIES = {role: "policy:supplier:" + role for role in ("epistemic", "authorization")}


def builder():
    return import_module(MODULE).build_supplier_program


@pytest.fixture(scope="module")
def supplied_program(action_compilation):
    return builder()(
        action_compilation.artifact.artifact_bytes,
        source_ids=SOURCES,
        policy_ids=POLICIES,
    )


def test_fresh_program_binds_actual_compilation_and_all_lifecycle_stages(
    supplied_program, action_compilation
):
    assert type(supplied_program) is bytes
    bundle = load_bundle(supplied_program)
    assert (
        raw(bundle["record_contract_base64"])
        == action_compilation.artifact.artifact_bytes
    )
    assert bundle["constants"]["initialization"]["sources"] == SOURCES
    assert bundle["constants"]["initialization"]["policies"] == POLICIES
    assert set(bundle["transactions"]) >= {
        "source",
        "monitor",
        "epistemic",
        "authorization",
        "grant",
        "initialize",
        "context-proposal",
        "type-completed",
        "type-unavailable",
        "capture-current",
        "authority-completed",
        "authority-unavailable",
        "dispatch",
        "observation",
    }
    assert "SupplierOrderAmendment" in bundle["profile"]["record_schemas"]
    assert "LocalAction" not in bundle["profile"]["record_schemas"]


def test_new_payload_fields_come_from_the_compiled_contract(supplied_program):
    catalog = load_bundle(supplied_program)["profile"]["record_schemas"]
    schema = catalog["SupplierOrderAmendment"]
    for field, value in FIELDS.items():
        assert field in schema["required"]
        assert schema["properties"][field]["type"] == (
            "integer" if type(value) is int else "string"
        )
    assert schema["properties"]["action_type"] == {
        "type": "string",
        "const": "AMEND_SUPPLIER_ORDER",
        "format": "nonblank",
    }


def test_program_references_use_the_supplier_type_not_the_neutral_fixture(
    supplied_program,
):
    # This ordinary case has no caller ID using either old spelling.
    bundle = json.loads(supplied_program)
    assert '"LocalAction"' not in json.dumps(bundle)
    assert '"LOCAL_ACTION"' not in json.dumps(bundle)
    assert all(
        target["target"] in {"PROTOCOL_INDEX", "ACTION_HEAD"}
        for target in bundle["profile"]["targets"].values()
    )


def test_program_authoring_is_deterministic_and_preserves_inputs(
    action_compilation, supplied_program
):
    sources, policies = deepcopy(SOURCES), deepcopy(POLICIES)
    actual = builder()(
        action_compilation.artifact.artifact_bytes,
        source_ids=sources,
        policy_ids=policies,
    )
    assert actual == supplied_program
    assert sources == SOURCES and policies == POLICIES


def test_type_specialization_does_not_rewrite_ordinary_caller_identifiers(
    action_compilation,
):
    sources, policies = deepcopy(SOURCES), deepcopy(POLICIES)
    sources["profile"] = "LocalAction"
    policies["epistemic"] = "LOCAL_ACTION"
    bundle = load_bundle(
        builder()(
            action_compilation.artifact.artifact_bytes,
            source_ids=sources,
            policy_ids=policies,
        )
    )
    assert bundle["constants"]["initialization"]["sources"] == sources
    assert bundle["constants"]["initialization"]["policies"] == policies


@pytest.mark.parametrize(
    "missing", ["profile", "record_contract", "machine", "history_binding"]
)
def test_missing_selected_role_never_uses_a_fixture_default(
    action_compilation, missing
):
    sources = {k: v for k, v in SOURCES.items() if k != missing}
    with pytest.raises(ValueError):
        builder()(
            action_compilation.artifact.artifact_bytes,
            source_ids=sources,
            policy_ids=POLICIES,
        )


def test_malformed_compiled_contract_refuses_before_program_authoring():
    with pytest.raises(ValueError):
        builder()(b"{}", source_ids=SOURCES, policy_ids=POLICIES)

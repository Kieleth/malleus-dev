"""Monitor invocation metadata, not a monitor invocation or assessment result."""

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from malleus.ledger import content_digest


HERE = Path(__file__).parent


def invocation():
    # These hashes identify labeled lexical witnesses, never implementations.
    digest = content_digest({"fixture": "invocation-shape-only"})
    return {
        "kind": "TYPE",
        "event": {
            "id": "event:shape",
            "generated_at": "2026-09-07T00:00:00Z",
            "responsible_actor_id": "actor:shape",
            "responsible_role": "type-monitor",
        },
        "output_ids": {"assessment": "assessment:shape", "failure": "failure:shape"},
        "monitor": {"id": "monitor:shape", "record_hash": digest},
        "implementation": {
            "id": "shape-only-not-a-producer",
            "version": "fixture",
            "bytes_sha256": digest,
        },
        "inputs": [
            {
                "role": "proposal",
                "value": {"id": "proposal:shape", "record_hash": digest},
            },
            {"role": "action", "value": {"id": "action:shape", "record_hash": digest}},
            {
                "role": "record_contract",
                "value": {"id": "contract:shape", "bytes_sha256": digest},
            },
        ],
    }


def validator():
    from research.action_history_contract_freeze.programs.packet_validator import FORMATS

    schema = json.loads((HERE / "invocation.schema.json").read_bytes())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FORMATS)


def test_invocation_has_no_implicit_ids_actors_or_clock():
    check, value = validator(), invocation()
    check.validate(value)
    for field in value:
        missing = deepcopy(value)
        del missing[field]
        assert not check.is_valid(missing), field
    for block in ("event", "output_ids", "monitor", "implementation"):
        for field in value[block]:
            missing = deepcopy(value)
            del missing[block][field]
            assert not check.is_valid(missing), (block, field)


@pytest.mark.parametrize(
    "field", ["outcome", "verdict", "callback", "clock", "defaults"]
)
def test_invocation_cannot_supply_outcome_or_ambient_dependency(field):
    assert not validator().is_valid({**invocation(), field: "SATISFIED"})


def test_input_roles_cannot_be_reordered_duplicated_or_omitted():
    value, check = invocation(), validator()
    value["inputs"].reverse()
    assert not check.is_valid(value)
    value = invocation()
    value["inputs"][1] = deepcopy(value["inputs"][0])
    assert not check.is_valid(value)
    value = invocation()
    value["inputs"].pop()
    assert not check.is_valid(value)


@pytest.mark.parametrize(
    "field,value", [("generated_at", "2026-09-07"), ("generated_at", None)]
)
def test_invocation_requires_explicit_zoned_protocol_time(field, value):
    candidate = invocation()
    candidate["event"][field] = value
    assert not validator().is_valid(candidate)


def test_invocation_digest_must_be_a_digest_not_an_implementation_claim():
    candidate = invocation()
    candidate["implementation"]["bytes_sha256"] = "UNBOUND"
    assert not validator().is_valid(candidate)


def test_direct_grant_invocation_roles_are_explicit_and_closed():
    value = invocation()
    digest = value["monitor"]["record_hash"]
    contract = json.loads((HERE / "monitor-contract.json").read_bytes())
    record_roles = {"proposal", "action", "grant", "authorization_policy"}
    value["kind"] = "DIRECT_GRANT"
    value["inputs"] = []
    for role in contract["DIRECT_GRANT"]["ordered_inputs"]:
        bound = (
            "executor:shape"
            if role == "executor_id"
            else {
                "id": f"{role}:shape",
                "record_hash" if role in record_roles else "bytes_sha256": digest,
            }
        )
        value["inputs"].append({"role": role, "value": bound})
    validator().validate(value)
    value["inputs"][-1]["value"]["ambient_state"] = True
    assert not validator().is_valid(value)


def test_membership_gap_uses_real_multivalued_assent_field():
    from tests.contract_compiler.pareto.test_assent_contract_compatibility import (
        _compile,
        _record,
    )

    view = _compile().view
    record = _record(
        "AuthorityGrant",
        artifact_kind="AUTHORITY_GRANT",
        artifact_version="fixture",
        artifact_hash=content_digest({"fixture": "grant-shape-only"}),
        grantor_actor_id="actor:grantor",
        grantee_actor_id="actor:executor",
        permitted_action_types=["READ", "AMEND"],
        scope_record_id="scope:fixture",
        may_subdelegate=False,
        grant_valid_from="2026-09-07T00:00:00Z",
    )
    assert view.validate_instance("AuthorityGrant", record) == []
    assert view.get_slot_constraint(
        "AuthorityGrant", "permitted_action_types"
    ).multivalued
    # This establishes the actual schema's list shape, not authorization.
    attempt = json.loads((HERE / "missing-membership.json").read_bytes())
    assert (
        record["permitted_action_types"]
        == attempt["positive"]["permitted_action_types"]
    )

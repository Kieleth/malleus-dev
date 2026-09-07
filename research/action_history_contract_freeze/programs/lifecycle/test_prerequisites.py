"""Bounded registration definitions and existing semantics, no event executor."""

from copy import deepcopy
from functools import lru_cache
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from malleus.assent import ProtocolError, _nonblank_values, _time_fields, make_record
from malleus.control import (
    ControlError,
    authorization_policy_digest,
    epistemic_policy_digest,
    monitor_specification_digest,
)
from malleus.ledger import content_digest, record_hash
from research.action_history_contract_freeze.programs.packet_validator import (
    FORMATS,
    PacketRefusal,
    validate_program,
)
from tests.contract_compiler.pareto.test_assent_contract_compatibility import _compile


HERE = Path(__file__).parent
KINDS = {
    "grant": "AuthorityGrant",
    "monitor": "MonitorSpecificationArtifact",
    "epistemic": "EpistemicPolicyArtifact",
    "authorization": "AuthorizationPolicyArtifact",
}
T0 = "2026-09-07T00:00:00Z"
T1 = "2026-09-07T01:00:00Z"


def packet(name):
    return json.loads((HERE / f"{name}-registration.json").read_bytes())


def check(value):
    return validate_program(
        value["program"],
        profile=value["profile"],
        instruction_schema=json.loads(
            (HERE.parents[1] / "instructions.schema.json").read_bytes()
        ),
    )


@lru_cache
def compiled():
    return _compile().view


def record(kind, identifier, **fields):
    return make_record(
        kind,
        id=identifier,
        event_id="event:registration-shape",
        generated_at=T0,
        actor_id="actor:registrar",
        role="registrar",
        source_record_ids=[],
        **fields,
    )


def specimen(name):
    digest = content_digest({"purpose": "shape only, not an implementation"})
    common = dict(artifact_version="shape-v1", artifact_hash=digest)
    if name == "grant":
        return record(
            KINDS[name],
            "grant:shape",
            **common,
            artifact_kind="AUTHORITY_GRANT",
            grantor_actor_id="actor:registrar",
            grantee_actor_id="actor:executor",
            permitted_action_types=["AMEND", "READ"],
            scope_record_id="scope:shape",
            may_subdelegate=False,
            grant_valid_from=T0,
            grant_valid_to=T1,
        )
    if name == "monitor":
        return record(
            KINDS[name],
            "monitor:shape",
            **common,
            artifact_kind="MONITOR_SPECIFICATION",
            monitor_schema_version="1",
            assessment_kind="TYPE",
            monitor_implementation_hash=digest,
            input_artifact_ids=["input:a", "input:b"],
            input_artifact_record_hashes=[digest, digest],
        )
    fields = dict(
        **common,
        artifact_kind="EPISTEMIC_POLICY"
        if name == "epistemic"
        else "AUTHORIZATION_POLICY",
        policy_schema_version="1",
        required_monitor_ids=["monitor:a", "monitor:b"],
        required_monitor_record_hashes=[digest, digest],
    )
    if name == "epistemic":
        fields.update(
            ruleset_id="ruleset:shape",
            ruleset_record_hash=digest,
            ruleset_artifact_hash=digest,
            violation_verdicts=["REJECT", "CONTEST"],
            unknown_verdicts=["DEFER", "CONTEST"],
            control_precedence=["REJECT", "DEFER", "CONTEST"],
        )
    return record(KINDS[name], f"policy:{name}:shape", **fields)


def existing_digest(name, value):
    if name == "monitor":
        return monitor_specification_digest(
            schema_version=value["monitor_schema_version"],
            monitor_id=value["id"],
            monitor_version=value["artifact_version"],
            assessment_kind=value["assessment_kind"],
            implementation_hash=value["monitor_implementation_hash"],
            input_artifact_ids=value["input_artifact_ids"],
            input_artifact_record_hashes=value["input_artifact_record_hashes"],
        )
    fields = dict(
        schema_version=value["policy_schema_version"],
        policy_id=value["id"],
        policy_version=value["artifact_version"],
        required_monitor_ids=value["required_monitor_ids"],
        required_monitor_record_hashes=value["required_monitor_record_hashes"],
    )
    if name == "authorization":
        return authorization_policy_digest(**fields)
    return epistemic_policy_digest(
        **fields,
        ruleset_id=value["ruleset_id"],
        ruleset_record_hash=value["ruleset_record_hash"],
        ruleset_artifact_hash=value["ruleset_artifact_hash"],
        violation_verdicts=value["violation_verdicts"],
        unknown_verdicts=value["unknown_verdicts"],
        control_precedence=value["control_precedence"],
    )


@pytest.mark.parametrize("name", KINDS)
def test_full_registration_shapes_and_static_programs(name):
    value, sample = packet(name), specimen(name)
    before = deepcopy(value)
    assert check(value)["runtime_executed"] is False
    assert value["status"] == "STATIC_VALID_PARTIAL"
    assert value["runtime_executed"] is False and value["unresolved"]
    assert compiled().validate_instance(KINDS[name], sample) == []
    shape = value["program"]["inputs"]["event"]["records"]
    Draft202012Validator(shape, format_checker=FORMATS).validate(
        {"value": [{"record_type": KINDS[name], "record": sample}]}
    )
    fields = shape["properties"]["value"]["items"]["properties"]["record"]
    assert set(fields["properties"]) == set(fields["required"]) == set(sample)
    assert value == before


@pytest.mark.parametrize("name", KINDS)
def test_registration_keeps_shared_metadata_hashes_and_introduction_order(name):
    steps = packet(name)["program"]["steps"]
    reasons = {step["refusal"] for step in steps}
    assert {
        "RECORD_HASH_MISMATCH",
        "GENERATION_EVENT_ID_MISMATCH",
        "GENERATED_AT_MISMATCH",
        "RESPONSIBLE_ACTOR_ID_MISMATCH",
        "RESPONSIBLE_ROLE_MISMATCH",
        "DUPLICATE_RECORD",
    } <= reasons
    assert steps[0]["opcode"] == "VALIDATE_RECORD"
    assert steps[-1]["opcode"] == "INTRODUCE_RECORDS"
    assert not any(step["opcode"] == "SET_PROTOCOL_STATE" for step in steps)
    canonical = next(s for s in steps if s["opcode"] == "REQUIRE_SORTED_UNIQUE_STRINGS")
    assert (
        canonical["values"]["path"][-1]
        == {
            "grant": "permitted_action_types",
            "monitor": "input_artifact_ids",
            "epistemic": "required_monitor_ids",
            "authorization": "required_monitor_ids",
        }[name]
    )


@pytest.mark.parametrize("name", ["monitor", "epistemic", "authorization"])
def test_semantic_preimage_is_fully_bound_and_matches_existing_hash_recipe(name):
    value, sample = packet(name), specimen(name)
    definition = value["semantic_preimage"]
    preimage = deepcopy(definition["template"])
    bindings = definition["bindings"]
    for binding in bindings:
        source = sample
        for field in binding["record_path"]:
            source = source[field]
        target = preimage
        for field in binding["preimage_path"][:-1]:
            target = target[field]
        target[binding["preimage_path"][-1]] = source
    assert content_digest(preimage) == existing_digest(name, sample)
    shape = value["program"]["inputs"]["artifact"]["preimage"]
    Draft202012Validator(shape, format_checker=FORMATS).validate({"value": preimage})
    steps = value["program"]["steps"]
    for index, binding in enumerate(bindings):
        step = next(
            s for s in steps if s["refusal"] == f"PREIMAGE_FIELD_{index}_MISMATCH"
        )
        assert step["left"]["path"] == ["value", 0, "record", *binding["record_path"]]
        assert step["right"]["path"] == ["value", *binding["preimage_path"]]
    hashed = next(s for s in steps if s.get("result") == "semantic-hash")
    assert hashed["recipe"] == "VALUE"
    assert hashed["value"] == {
        "root": "artifact",
        "name": "preimage",
        "path": ["value"],
    }
    assert steps.index(hashed) > max(
        i for i, s in enumerate(steps) if s["refusal"].startswith("PREIMAGE_FIELD_")
    )
    # Provenance is record identity, not monitor or policy semantic identity.
    changed = {**sample, "responsible_actor_id": "actor:other"}
    assert existing_digest(name, changed) == existing_digest(name, sample)
    assert record_hash(KINDS[name], changed) != sample["content_hash"]


@pytest.mark.parametrize("name", ["monitor", "epistemic", "authorization"])
def test_each_declared_dependency_uses_record_hash_and_prior_scope(name):
    steps = packet(name)["program"]["steps"]
    resolved = [s for s in steps if s["opcode"] == "RESOLVE_RECORD"]
    assert len(resolved) == (3 if name == "epistemic" else 2)
    for step in resolved:
        assert step["scope"] == "APPLIED"
        assert "artifact_hash" not in step["record_hash"]["path"]
        assert step["record_hash"]["path"][-2:] in (
            ["input_artifact_record_hashes", 0],
            ["input_artifact_record_hashes", 1],
            ["required_monitor_record_hashes", 0],
            ["required_monitor_record_hashes", 1],
            ["record", "ruleset_record_hash"],
        )
        assert any(
            s["opcode"] == "REQUIRE_MEMBER" and s["value"]["name"] == step["result"]
            for s in steps
        )
    if name == "epistemic":
        rule = next(
            s for s in steps if s["refusal"] == "RULESET_SEMANTIC_HASH_MISMATCH"
        )
        assert rule["right"]["path"][-1] == "artifact_hash"


@pytest.mark.parametrize("name", KINDS)
def test_missing_header_binding_refuses_definition(name):
    value = packet(name)
    del value["program"]["inputs"]["event"]["header"]["properties"]["actor_id"]
    value["program"]["inputs"]["event"]["header"]["required"].remove("actor_id")
    with pytest.raises(PacketRefusal) as caught:
        check(value)
    assert caught.value.reason == "UNRESOLVED_PATH"


def test_grant_actor_interval_and_nonblank_gap_are_not_conflated():
    value = packet("grant")
    steps = value["program"]["steps"]
    grantor = next(s for s in steps if s["refusal"] == "WRONG_GRANTOR")
    assert grantor["left"]["path"][-1] == "grantor_actor_id"
    assert grantor["right"]["path"] == ["actor_id"]
    interval = next(s for s in steps if s["refusal"] == "INVALID_GRANT_INTERVAL")
    assert interval["comparison"] == "LT" and interval["value_kind"] == "INSTANT"
    assert interval["left"]["path"][-1] == "grant_valid_from"
    assert interval["right"]["path"][-1] == "grant_valid_to"
    bad = {**specimen("grant"), "grant_valid_to": T0}
    with pytest.raises(ProtocolError):
        _time_fields(bad, "existing grant interval")
    gap = json.loads((HERE / "registration-nonblank-gap.json").read_bytes())
    blank = {**specimen("grant"), "permitted_action_types": gap["negative"]}
    blank["content_hash"] = record_hash("AuthorityGrant", blank)
    assert compiled().validate_instance("AuthorityGrant", blank) == []
    shape = value["program"]["inputs"]["event"]["records"]
    Draft202012Validator(shape, format_checker=FORMATS).validate(
        {"value": [{"record_type": "AuthorityGrant", "record": blank}]}
    )
    with pytest.raises(ProtocolError):
        _nonblank_values(blank["permitted_action_types"], "existing grant rule")
    assert "NONBLANK" in " ".join(value["unresolved"])
    assert gap["runtime_executed"] is False


@pytest.mark.parametrize("name", ["monitor", "epistemic", "authorization"])
def test_bounded_parallel_arrays_and_existing_semantics_discriminate_bad_input(name):
    value, sample = packet(name), specimen(name)
    field = (
        "input_artifact_record_hashes"
        if name == "monitor"
        else "required_monitor_record_hashes"
    )
    sample[field] = sample[field][:-1]
    shape = value["program"]["inputs"]["event"]["records"]
    assert not Draft202012Validator(shape).is_valid(
        {"value": [{"record_type": KINDS[name], "record": sample}]}
    )
    with pytest.raises(ControlError):
        existing_digest(name, sample)

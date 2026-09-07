"""Static definition checks, not history resolution or transaction execution."""

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from malleus.assent import make_record
from malleus.ledger import content_digest
from research.action_history_contract_freeze.programs.packet_validator import (
    FORMATS,
    PacketRefusal,
    validate_program,
)
from research.action_history_contract_freeze.programs.test_input_carrier import (
    candidate,
    source_record,
)
from tests.contract_compiler.pareto.test_assent_contract_compatibility import (
    _compile,
    _records,
)


HERE = Path(__file__).parent


def packet():
    return json.loads((HERE / "context-proposal.json").read_bytes())


def check(value):
    return validate_program(
        value["program"],
        instruction_schema=json.loads(
            (HERE.parents[1] / "instructions.schema.json").read_bytes()
        ),
        profile=value["profile"],
    )


def test_input_origins_close_the_declared_monitor_roles_without_runtime_claims():
    origins = json.loads((HERE.parent / "retained-input-origins.json").read_bytes())
    monitors = json.loads((HERE.parent / "monitor-contract.json").read_bytes())
    bindings = candidate()
    roles = set(bindings["record_inputs"]) | set(bindings["byte_inputs"])
    roles |= set(bindings["scalar_inputs"])
    assert set(origins["monitor_inputs"]) == roles
    assert set(origins["invocation_order"]) == {"TYPE", "DIRECT_GRANT"}
    for kind in origins["invocation_order"]:
        assert origins["invocation_order"][kind] == monitors[kind]["ordered_inputs"]
    assert origins["status"] == "DEFINITION_ONLY"
    assert origins["runtime_resolution"] == "UNIMPLEMENTED"
    assert isinstance(origins["current_context_rule"], str)
    assert all(
        isinstance(item, str) for item in origins["unresolved_runtime_contracts"]
    )
    assert all(isinstance(item, str) for item in origins["non_claims"])
    for role in bindings["byte_inputs"]:
        entry = origins["monitor_inputs"][role]
        assert entry["scope"] == "APPLIED"
        assert entry["carrier"] == "SourceArtifact"
        assert entry["bytes_identity_field"] == "source_content_digest"
        assert entry["record_identity_field"] == "content_hash"
        assert entry["semantic_identity_field"] == "artifact_hash"
        assert entry["content"] == bindings["byte_inputs"][role]
    assert origins["monitor_inputs"]["executor_id"]["origin"] == "INVOCATION_SCALAR"
    assert origins["transaction_inputs"]["original_context"]["scope"] == (
        "APPLIED_AND_EARLIER_STAGED"
    )
    assert origins["transaction_inputs"]["prerequisites"]["scope"] == "APPLIED"
    assert origins["monitor_inputs"]["current_context"]["freshness"] == (
        "VERIFY_RETAINED_PREFIX_THEN_COMPARE_CURRENT_A_AND_D"
    )


def test_atomic_pair_is_explicit_and_static_only():
    value = packet()
    before = deepcopy(value)
    result = check(value)
    assert result == {
        "status": "STATIC_VALID",
        "steps": len(value["program"]["steps"]),
        "runtime_executed": False,
    }
    assert value == before
    decision = json.loads((HERE.parents[1] / "proposal-transaction.json").read_bytes())
    assert value["transaction"] == decision
    assert value["status"] == "STATIC_VALID_PARTIAL"
    assert value["runtime_executed"] is False
    assert isinstance(value["scope"], str)
    assert all(isinstance(item, str) for item in value["unresolved"])
    assert value["program"]["introductions"] == [
        {"name": "context", "depends_on": []},
        {"name": "action", "depends_on": ["context"]},
        {"name": "proposal", "depends_on": ["context", "action"]},
    ]
    steps = value["program"]["steps"]
    codes = [step["refusal"] for step in steps]
    assert len(codes) == len(set(codes))
    for code in (
        "STALE_FULL_HEAD",
        "STALE_FULL_COUNT",
        "STALE_CONTRACT",
        "STALE_KCS_HEAD",
        "STALE_MATERIALIZATION",
        "STALE_GRAPH",
        "STALE_ACTION_HEAD",
        "WRONG_INITIALIZATION",
        "CONTEXT_BYTES_MISMATCH",
        "CONTEXT_ID_MISMATCH",
        "CONTEXT_NOT_EARLIER_STAGED",
        "WRONG_PROPOSAL_ID",
        "WRONG_ACTION_ID",
        "WRONG_ACTION_MEMBER",
        "WRONG_MEMBER_HASH",
        "DUPLICATE_ACTION_KEY",
        "EPIS_POLICY_NOT_APPLIED",
        "AUTH_POLICY_NOT_APPLIED",
        "EPIS_POLICY_HASH_MISMATCH",
        "AUTH_POLICY_HASH_MISMATCH",
        "PROPOSAL_SOURCE_CONTEXT_MISSING",
        "ACTION_SOURCE_CONTEXT_MISSING",
    ):
        assert code in codes
    assert codes.index("INTRODUCE_CONTEXT") < codes.index("CONTEXT_NOT_EARLIER_STAGED")
    assert codes.index("INTRODUCE_ACTION") < codes.index("INTRODUCE_PROPOSAL")
    resolutions = {
        s["refusal"]: s["scope"] for s in steps if s["opcode"] == "RESOLVE_RECORD"
    }
    assert resolutions == {
        "EPIS_POLICY_NOT_APPLIED": "APPLIED",
        "AUTH_POLICY_NOT_APPLIED": "APPLIED",
        "CONTEXT_NOT_EARLIER_STAGED": "APPLIED_AND_EARLIER_STAGED",
    }
    effects = [s for s in steps if s["opcode"] == "SET_PROTOCOL_STATE"]
    assert {s["name"] for s in effects} == {
        "context_by_proposal",
        "proposal_states",
        "authorization_states",
        "action_to_proposal",
        "latest_action_by_key",
    }
    assert all(s["target"] == "PROTOCOL_INDEX" and len(s["keys"]) == 1 for s in effects)
    assert {s["storage_path"][0] for s in value["profile"]["targets"].values()} == {
        "protocol"
    }


@pytest.mark.parametrize(
    "change",
    [
        "domain-head",
        "missing-input",
        "forward-result",
        "missing-key",
        "domain-write",
        "forward-introduction",
    ],
)
def test_invalid_definition_refuses(change):
    value = packet()
    program = value["program"]
    if change == "domain-head":
        step = next(s for s in program["steps"] if s["refusal"] == "STALE_ACTION_HEAD")
        step["right"]["path"] = ["domain", "kcs_acceptance_head"]
    elif change == "missing-input":
        del program["inputs"]["current"]["base"]
    elif change == "forward-result":
        step = next(
            s for s in program["steps"] if s["refusal"] == "CONTEXT_BYTES_MISMATCH"
        )
        step["right"]["name"] = "not-produced"
    elif change == "missing-key":
        del program["steps"][-1]["keys"]
    elif change == "domain-write":
        program["steps"][-1]["target"] = "KG"
    else:
        program["introductions"][0]["depends_on"] = ["proposal"]
    with pytest.raises(PacketRefusal):
        check(value)


def test_selected_full_record_variants_match_compiled_assent():
    value = packet()
    compiled = _compile().view
    action = _records()[0][1]
    context = source_record(candidate(), "original_context", b"{}")
    digest = content_digest({"purpose": "shape only"})
    proposal = make_record(
        "ProposedSubgraph",
        id="proposal:shape",
        event_id="event:shape",
        generated_at="2026-09-07T00:00:00Z",
        actor_id="actor:shape",
        role="proposer",
        source_record_ids=[context["id"]],
        proposal_key="episode:shape",
        revision=1,
        base_acceptance_head=digest,
        epistemic_policy_id="epistemic:shape",
        epistemic_policy_hash=digest,
        member_content_hashes=[action["content_hash"]],
        claim_version_ids=[],
        evidence_ids=[],
        evidence_assertion_ids=[],
        action_proposal_ids=[action["id"]],
    )
    for name, record_type, record in (
        ("context", "SourceArtifact", context),
        ("action", "LocalAction", action),
        ("proposal", "ProposedSubgraph", proposal),
    ):
        assert compiled.validate_instance(record_type, record) == []
        shape = value["program"]["inputs"]["event"][name]
        Draft202012Validator(shape, format_checker=FORMATS).validate(
            {"value": [{"record_type": record_type, "record": record}]}
        )
        fields = shape["properties"]["value"]["items"]["properties"]["record"]
        assert set(record) == set(fields["properties"])
        assert set(record) == set(fields["required"])
    # No actual reference resolution, proposal admission or source parsing occurs.


def test_selected_record_variant_refuses_non_action_members_and_revisions():
    record = packet()["program"]["inputs"]["event"]["proposal"]["properties"]["value"][
        "items"
    ]["properties"]["record"]
    assert record["properties"]["revision"]["const"] == 1
    for field in ("claim_version_ids", "evidence_ids", "evidence_assertion_ids"):
        assert record["properties"][field]["maxItems"] == 0
    for field in ("member_content_hashes", "action_proposal_ids"):
        assert record["properties"][field]["minItems"] == 1
        assert record["properties"][field]["maxItems"] == 1
    for field in ("revises_proposal_id", "candidate_artifact_id"):
        assert field not in record["properties"]


def test_episode_metadata_does_not_alias_independent_protocol_lineage_keys():
    # O retains the episode key by content identity. No accepted rule says
    # proposal_key, action_key and episode_key must have equal strings.
    for step in packet()["program"]["steps"]:
        if step["opcode"] != "REQUIRE_COMPARE":
            continue
        operands = (step["left"], step["right"])
        assert not (
            any(o["path"][-1] == "episode_key" for o in operands)
            and any(o["path"][-1] in {"proposal_key", "action_key"} for o in operands)
        )


def test_policy_reference_hashes_keep_existing_record_identity_semantics():
    # ProtocolLedger._artifact_ref resolves policy references by content_hash,
    # not artifact_hash. Both are digests but they name different objects.
    steps = packet()["program"]["steps"]
    for code in ("EPIS_POLICY_HASH_MISMATCH", "AUTH_POLICY_HASH_MISMATCH"):
        step = next(s for s in steps if s["refusal"] == code)
        assert step["right"]["path"] == ["value", "content_hash"]


@pytest.mark.parametrize(
    "record_type", ["EpistemicPolicyArtifact", "AuthorizationPolicyArtifact"]
)
def test_resolved_policy_shapes_preserve_all_compiled_required_fields(record_type):
    digest = content_digest({"purpose": "policy shape only"})
    fields = {
        "artifact_kind": "EPISTEMIC_POLICY"
        if record_type == "EpistemicPolicyArtifact"
        else "AUTHORIZATION_POLICY",
        "artifact_version": "shape-v1",
        "artifact_hash": digest,
        "policy_schema_version": "1",
        "required_monitor_ids": ["monitor:shape"],
        "required_monitor_record_hashes": [digest],
    }
    if record_type == "EpistemicPolicyArtifact":
        fields.update(
            ruleset_id="rules:shape",
            ruleset_record_hash=digest,
            ruleset_artifact_hash=digest,
            violation_verdicts=["REJECT"],
            unknown_verdicts=["DEFER"],
            control_precedence=["REJECT", "CONTEST", "DEFER"],
        )
    policy = make_record(
        record_type,
        id="policy:shape",
        event_id="event:shape",
        generated_at="2026-09-07T00:00:00Z",
        actor_id="actor:shape",
        role="registrar",
        source_record_ids=[],
        **fields,
    )
    assert policy["content_hash"] != policy["artifact_hash"]
    assert _compile().view.validate_instance(record_type, policy) == []
    shape = packet()["profile"]["record_schemas"][record_type]
    assert set(shape["properties"]) == set(policy)
    assert set(shape["required"]) == set(policy)
    Draft202012Validator(shape, format_checker=FORMATS).validate(policy)

"""Complete supplied inputs, not retained history or monitor execution."""

from copy import deepcopy
from importlib import import_module
import json

import pytest

from malleus.assent import make_record
from malleus.ledger import content_digest, record_hash
from research.action_history_contract_freeze.programs.test_input_carrier import (
    HERE,
    candidate,
    input_bytes,
    source_record,
)
from research.action_history_contract_freeze.programs.test_invocation_definition import (
    invocation,
)
from tests.contract_compiler.pareto.test_assent_contract_compatibility import (
    _compile,
    _records,
)


def api():
    return import_module(
        "research.action_history_contract_freeze.programs.input_preflight"
    )


@pytest.fixture(scope="module")
def compiled():
    return _compile()


def specimen(compiled, kind="TYPE"):
    definition = candidate()
    contract = json.loads((HERE / "monitor-contract.json").read_bytes())
    wrappers, blobs = {}, {}
    for record_type, record, _, _ in _records():
        if record_type in {"LocalAction", "AuthorityGrant"}:
            record["id"] = {
                "LocalAction": "action:shape",
                "AuthorityGrant": "grant:shape",
            }[record_type]
            record["content_hash"] = record_hash(record_type, record)
            wrappers[record["id"]] = {"record_type": record_type, "record": record}
    for role, record_type, fields in [
        (
            "proposal",
            "ProposedSubgraph",
            {
                "proposal_key": "proposal-key:shape",
                "revision": 1,
                "base_acceptance_head": content_digest("proposal-head"),
                "epistemic_policy_id": "policy:shape",
                "epistemic_policy_hash": content_digest("policy"),
                "member_content_hashes": [
                    wrappers["action:shape"]["record"]["content_hash"]
                ],
                "claim_version_ids": [],
                "evidence_ids": [],
                "evidence_assertion_ids": [],
                "action_proposal_ids": ["action:shape"],
            },
        ),
        (
            "authorization_policy",
            "AuthorizationPolicyArtifact",
            {
                "artifact_kind": "AUTHORIZATION_POLICY",
                "artifact_version": "shape",
                "artifact_hash": content_digest("policy"),
                "policy_schema_version": "1",
                "required_monitor_ids": ["monitor:shape"],
                "required_monitor_record_hashes": [content_digest("monitor")],
            },
        ),
    ]:
        record = make_record(
            record_type,
            id=f"{role}:shape",
            event_id="event:shape",
            generated_at="2026-09-07T00:00:00Z",
            actor_id="actor:shape",
            role="proposer",
            source_record_ids=[],
            **fields,
        )
        wrappers[record["id"]] = {"record_type": record_type, "record": record}
    value = invocation()
    value["kind"] = kind
    value["inputs"] = []
    for role in contract[kind]["ordered_inputs"]:
        if role in definition["byte_inputs"]:
            content = input_bytes(role, compiled)
            record = source_record(definition, role, content)
            wrappers[record["id"]] = {"record_type": "SourceArtifact", "record": record}
            blobs[record["id"]] = content
            reference = {
                "id": record["id"],
                "bytes_sha256": record["source_content_digest"],
            }
        elif role in definition["record_inputs"]:
            record = wrappers[f"{role}:shape"]["record"]
            reference = {"id": record["id"], "record_hash": record["content_hash"]}
        else:
            assert role == "executor_id"
            reference = "actor:executor"
        value["inputs"].append({"role": role, "value": reference})
    return {
        "invocation": value,
        "records": wrappers,
        "retained_bytes": blobs,
        "contract_bytes": compiled.artifact.artifact_bytes,
    }


def run(value):
    return api().validate_input_specimen(**value)


@pytest.mark.parametrize("kind", ["TYPE", "DIRECT_GRANT"])
def test_complete_input_specimen_is_static_not_applied_or_executed(compiled, kind):
    value = specimen(compiled, kind)
    before = deepcopy(value)
    assert run(value) == {
        "status": "STATIC_INPUTS_VALID",
        "retention_verified": False,
        "runtime_executed": False,
        "roles": [entry["role"] for entry in value["invocation"]["inputs"]],
    }
    assert value == before


@pytest.mark.parametrize(
    "fault,reason",
    [
        ("missing_record", "INPUT_NOT_SUPPLIED"),
        ("outer_id", "INPUT_RECORD_ID"),
        ("record_hash", "INPUT_RECORD_HASH"),
        ("reference_record_hash", "INPUT_RECORD_HASH"),
        ("abstract_record", "INPUT_RECORD_TYPE"),
        ("wrong_record_type", "INPUT_RECORD_TYPE"),
        ("missing_bytes", "INPUT_NOT_SUPPLIED"),
        ("corrupt_bytes", "INPUT_BYTE_BINDING"),
        ("reference_digest_domain", "INPUT_BYTE_BINDING"),
        ("artifact_semantic_hash", "INPUT_BYTE_BINDING"),
        ("wrong_length", "INPUT_BYTE_BINDING"),
        ("missing_required", "INPUT_RECORD_SHAPE"),
        ("source_ids_absent", "INPUT_RECORD_SHAPE"),
        ("supplied_outcome", "INVOCATION_SHAPE"),
        ("missing_carrier_field", "INPUT_RECORD_SHAPE"),
        ("string_bytes", "INPUT_BYTE_BINDING"),
    ],
)
def test_input_binding_refusals_preserve_the_specimen(compiled, fault, reason):
    value = specimen(compiled)
    action = value["records"]["action:shape"]
    reference = value["invocation"]["inputs"][-1]["value"]
    source = value["records"][reference["id"]]["record"]
    if fault == "missing_record":
        del value["records"]["action:shape"]
    elif fault == "outer_id":
        action["record"]["id"] = "different:id"
    elif fault == "record_hash":
        action["record"]["revision"] = 2
    elif fault == "reference_record_hash":
        value["invocation"]["inputs"][1]["value"]["record_hash"] = content_digest(
            "wrong"
        )
    elif fault == "abstract_record":
        action["record_type"] = "ActionProposal"
    elif fault == "wrong_record_type":
        action["record_type"] = "TypeAssessment"
    elif fault == "missing_bytes":
        del value["retained_bytes"][reference["id"]]
    elif fault == "corrupt_bytes":
        value["retained_bytes"][reference["id"]] += b" "
    elif fault == "reference_digest_domain":
        reference["bytes_sha256"] = source["content_hash"]
    elif fault == "artifact_semantic_hash":
        source["artifact_hash"] = source["source_content_digest"]
        source["content_hash"] = record_hash("SourceArtifact", source)
    elif fault == "wrong_length":
        source["source_byte_length"] += 1
        source["content_hash"] = record_hash("SourceArtifact", source)
    elif fault == "missing_required":
        del action["record"]["revision"]
    elif fault == "source_ids_absent":
        del action["record"]["source_record_ids"]
    elif fault == "supplied_outcome":
        value["invocation"]["outcome"] = "SATISFIED"
    elif fault == "missing_carrier_field":
        del source["source_locator"]
    elif fault == "string_bytes":
        value["retained_bytes"][reference["id"]] = "not bytes"
    else:
        raise AssertionError(fault)
    before = deepcopy(value)
    with pytest.raises(api().PacketRefusal) as caught:
        run(value)
    assert caught.value.reason == reason
    assert value == before


@pytest.mark.parametrize(
    "role",
    ["scope_association", "requested_interval", "original_context", "current_context"],
)
def test_exact_source_identity_does_not_bypass_content_contract(compiled, role):
    value = specimen(compiled, "DIRECT_GRANT")
    entry = next(item for item in value["invocation"]["inputs"] if item["role"] == role)
    record = source_record(candidate(), role, b"{}")
    value["records"][record["id"]] = {"record_type": "SourceArtifact", "record": record}
    value["retained_bytes"][record["id"]] = b"{}"
    entry["value"] = {
        "id": record["id"],
        "bytes_sha256": record["source_content_digest"],
    }
    before = deepcopy(value)
    with pytest.raises(api().PacketRefusal) as caught:
        run(value)
    assert caught.value.reason == "INPUT_CONTENT"
    assert value == before


def test_type_contract_cannot_differ_from_selected_validation_contract(compiled):
    other = _compile("assent")
    value = specimen(compiled)
    record = source_record(
        candidate(), "record_contract", other.artifact.artifact_bytes
    )
    value["records"][record["id"]] = {"record_type": "SourceArtifact", "record": record}
    value["retained_bytes"][record["id"]] = other.artifact.artifact_bytes
    value["invocation"]["inputs"][-1]["value"]["bytes_sha256"] = record[
        "source_content_digest"
    ]
    with pytest.raises(api().PacketRefusal) as caught:
        run(value)
    assert caught.value.reason == "INPUT_CONTRACT_MISMATCH"

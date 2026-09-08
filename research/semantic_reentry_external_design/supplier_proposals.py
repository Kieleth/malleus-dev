"""Supplier action entry through Core, without synthesis or domain application.

An authored candidate is data, not permission. Checks run outside append/replay;
the selected Core program owns admission and the action-only transition.
"""

from datetime import datetime
from functools import wraps
from hashlib import sha256
import json

import malleus.compiler as core
from malleus.assent import make_record
from malleus.control import evaluate_epistemic_policy
from malleus.ledger import canonical_json, content_digest, record_hash
from malleus.source import source_artifact_fields
from research.action_history_contract_freeze.programs.check_executor import (
    CheckRefusal,
    load_check_executor,
)
from research.action_history_contract_freeze.programs.decision_bundle import TARGETS
from research.action_history_contract_freeze.programs.history_checks import (
    run_history_check,
)
from research.action_history_contract_freeze.programs.proposal_bundle import ROLES
from research.action_history_contract_freeze.programs.registration_bundle import (
    SOURCE_PROJECTION,
)
from research.semantic_reentry_external_design.accepted_read_view import (
    AcceptedReadView,
    freeze_accepted_replay,
)


PAYLOAD_FIELDS = (
    "logical_source_id",
    "supplier_order_id",
    "product_code",
    "expected_quantity",
    "requested_quantity",
    "expected_source_digest",
    "new_source_occurrence_id",
)


class SupplierProtocolError(ValueError):
    def __init__(self, reason, detail):
        self.reason, self.detail = reason, detail
        super().__init__(f"{reason}: {detail}")


def _guarded(function):
    @wraps(function)
    def invoke(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (
            SupplierProtocolError,
            core.ProtocolProgramRefusal,
            core.KnowledgeChangeRefusal,
            CheckRefusal,
        ):
            raise
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            RecursionError,
        ) as error:
            raise SupplierProtocolError("MALFORMED_INPUT", str(error)) from error

    return invoke


def _require(condition, reason, detail):
    if not condition:
        raise SupplierProtocolError(reason, detail)


def _text(*values):
    _require(
        all(type(v) is str and v.strip() for v in values),
        "MALFORMED_INPUT",
        "explicit nonblank identifiers required",
    )


def _canonical(value):
    return canonical_json(value).encode()


def _digest(content):
    _require(type(content) is bytes, "MALFORMED_INPUT", "exact bytes required")
    return "sha256:" + sha256(content).hexdigest()


def _object(content):
    _digest(content)
    value = json.loads(content)
    _require(
        type(value) is dict and _canonical(value) == content,
        "MALFORMED_INPUT",
        "canonical JSON object required",
    )
    return value


def _time(value):
    _text(value)
    _require(
        datetime.fromisoformat(value.replace("Z", "+00:00")).utcoffset() is not None,
        "MALFORMED_INPUT",
        "timezone-aware time required",
    )


def _owner(history, expected_head, expected_count):
    _require(
        type(history) is core.KnowledgeChangeHistory,
        "MALFORMED_INPUT",
        "actual owning public Core history required",
    )
    _text(expected_head)
    _require(
        type(expected_count) is int and expected_count >= 0,
        "MALFORMED_INPUT",
        "nonnegative integer event count required",
    )
    replay = history.replay()
    _require(
        (expected_head, expected_count)
        == (replay.ledger_head, replay.ledger_event_count),
        "STALE_BASE",
        "expected full ledger head/count differ",
    )
    _require(
        replay.protocol_replay is not None,
        "UNSUPPORTED",
        "selected experimental action attachment required",
    )
    return replay


def _record(records, identifier, kind):
    _text(identifier)
    entry = records[identifier]
    value = entry["record"]
    _require(
        entry["record_type"] == kind
        and value["id"] == identifier
        and record_hash(kind, value) == value["content_hash"],
        "MALFORMED_INPUT",
        "wrong typed record or record hash: " + identifier,
    )
    return value


def _reference(value):
    return {"id": value["id"], "record_hash": value["content_hash"]}


def _source(view, identifier):
    value = _record(view.protocol["records"], identifier, "SourceArtifact")
    members = [m for m in view.context.retained_inputs if m.record_id == identifier]
    _require(
        len(members) == 1,
        "MALFORMED_INPUT",
        "one retained source required: " + identifier,
    )
    member = members[0]
    _require(
        type(member) is core.KnowledgeRetainedInput
        and member.identity == _digest(member.content) == value["source_content_digest"]
        and type(value["source_byte_length"]) is int
        and len(member.content) == value["source_byte_length"],
        "MALFORMED_INPUT",
        "source bytes/metadata disagree: " + identifier,
    )
    return value, member.content


def _initialization(view, identifier):
    value, content = _source(view, identifier)
    checkpoint = _object(content)
    active = view.protocol["state"]["protocol"]["initialization"]
    _require(
        active == [{"keys": ["ACTIVE"], "value": _digest(content)}]
        and checkpoint["id"] == identifier
        and checkpoint["schema"] == "malleus.action-history.initialization/research-v1",
        "MALFORMED_INPUT",
        "source is not the applied initialization",
    )
    for role, kind in (
        ("epistemic", "EpistemicPolicyArtifact"),
        ("authorization", "AuthorizationPolicyArtifact"),
    ):
        ref = checkpoint[role + "_policy"]
        policy = _record(view.protocol["records"], ref["id"], kind)
        _require(
            ref == _reference(policy),
            "MALFORMED_INPUT",
            "initialization policy differs from its retained record",
        )
    return checkpoint, value


def _active_initialization(view):
    active = view.protocol["state"]["protocol"]["initialization"]
    _require(
        len(active) == 1 and active[0]["keys"] == ["ACTIVE"],
        "MALFORMED_INPUT",
        "one applied initialization required",
    )
    identifiers = [
        m.record_id
        for m in view.context.retained_inputs
        if m.identity == active[0]["value"]
    ]
    _require(
        len(identifiers) == 1,
        "MALFORMED_INPUT",
        "applied initialization bytes must resolve uniquely",
    )
    return identifiers[0]


def _event(record, event_type, data, retained):
    return {
        "event_id": record["generation_event_id"],
        "event_type": event_type,
        "actor_id": record["responsible_actor_id"],
        "transaction_time": record["generated_at"],
        "data": data,
        "retained": retained,
    }


def _value(kind, record):
    return {"value": [{"record_type": kind, "record": record}]}


@_guarded
def original_supplier_context(
    *,
    view,
    initialization_id,
    source_ids,
    context_id,
    action_id,
    proposal_id,
    episode_key,
):
    """Construct Core's existing O value without retention or mutable graph access."""
    _require(
        type(view) is AcceptedReadView,
        "MALFORMED_INPUT",
        "verified graph-free accepted read required",
    )
    _text(initialization_id, context_id, action_id, proposal_id, episode_key)
    _require(
        type(source_ids) is dict and set(source_ids) == set(ROLES),
        "MALFORMED_INPUT",
        "all four closed source roles required",
    )
    _text(*source_ids.values())
    _require(
        len(set(source_ids.values())) == len(ROLES),
        "MALFORMED_INPUT",
        "source roles require distinct records",
    )
    context, receipt = view.context, _object(view.receipt_bytes)
    _require(
        type(context) is core.KnowledgeChangeContext
        and type(context.base_ledger_event_count) is int
        and _digest(view.receipt_bytes) == context.receipt_identity
        and _digest(view.protocol_bytes) == receipt["protocol_replay_identity"]
        and receipt["ledger_head"] == context.base_ledger_head
        and receipt["ledger_event_count"] == context.base_ledger_event_count
        and receipt["contract_identity"] == context.contract_identity
        and receipt["graph_state_digest"] == context.base_accepted_state_digest,
        "STALE_BASE",
        "accepted read identity chain differs",
    )
    checkpoint, _ = _initialization(view, initialization_id)
    sources = {role: _source(view, source_ids[role])[0] for role in ROLES}
    return _canonical(
        {
            "schema": "malleus.action-history.original-context/research-v1",
            "id": context_id,
            "prefix": {
                "head": context.base_ledger_head,
                "event_count": context.base_ledger_event_count,
            },
            "domain": {
                "effective_contract_identity": context.contract_identity,
                "kcs_acceptance_head": context.base_acceptance_head,
                "materialization_head": context.base_materialization_head,
                "accepted_graph_digest": context.base_accepted_state_digest,
            },
            "action_acceptance_head": view.protocol["state"]["action_acceptance_head"],
            "initialization_identity": content_digest(checkpoint),
            "epistemic_policy": checkpoint["epistemic_policy"],
            "authorization_policy": checkpoint["authorization_policy"],
            "proposal_id": proposal_id,
            "action_id": action_id,
            "episode_key": episode_key,
            **{
                role: {
                    "id": value["id"],
                    "bytes_sha256": value["source_content_digest"],
                }
                for role, value in sources.items()
            },
        }
    )


@_guarded
def submit_supplier_proposal(
    *,
    history,
    original_context_bytes,
    action_bytes,
    proposal_key,
    context_actor_id,
    artifact_version,
    expected_head,
    expected_count,
):
    """Submit the exact authored action and its O artifact as one atomic pair."""
    replay = _owner(history, expected_head, expected_count)
    _text(proposal_key, context_actor_id, artifact_version)
    original, action = _object(original_context_bytes), _object(action_bytes)
    _time(action["generated_at"])
    view = freeze_accepted_replay(replay=replay, context=history.composition_context())
    initialization_id = _active_initialization(view)
    checkpoint, init_record = _initialization(view, initialization_id)
    source_ids = {role: original[role]["id"] for role in ROLES}
    expected = original_supplier_context(
        view=view,
        initialization_id=initialization_id,
        source_ids=source_ids,
        context_id=original["id"],
        action_id=original["action_id"],
        proposal_id=original["proposal_id"],
        episode_key=original["episode_key"],
    )
    _require(
        original_context_bytes == expected,
        "STALE_BASE",
        "original context differs from the exact current accepted inputs",
    )
    contract_record, contract_bytes = _source(view, checkpoint["record_contract"]["id"])
    _require(
        checkpoint["record_contract"]["bytes_sha256"]
        == contract_record["source_content_digest"],
        "MALFORMED_INPUT",
        "selected record contract bytes differ",
    )
    errors = core.load_validated_contract_artifact(contract_bytes).validate_instance(
        "SupplierOrderAmendment", action
    )
    _require(not errors, "UNSUPPORTED", "invalid supplier action: " + str(errors))
    _require(
        record_hash("SupplierOrderAmendment", action) == action["content_hash"],
        "MALFORMED_INPUT",
        "action record hash differs",
    )
    _require(
        content_digest({name: action[name] for name in PAYLOAD_FIELDS})
        == action["action_payload_hash"],
        "MALFORMED_INPUT",
        "action payload hash differs",
    )
    context_record = make_record(
        "SourceArtifact",
        id=original["id"],
        event_id="event:" + original["id"],
        generated_at=action["generated_at"],
        actor_id=context_actor_id,
        role="registrar",
        source_record_ids=[source_ids[role] for role in ROLES] + [initialization_id],
        artifact_kind="SOURCE",
        artifact_version=artifact_version,
        **source_artifact_fields(
            artifact_id=original["id"],
            artifact_version=artifact_version,
            source_bytes=original_context_bytes,
            media_type="application/json",
            locator="urn:retained:" + original["id"],
        ),
    )
    policy = original["epistemic_policy"]
    proposal = make_record(
        "ProposedSubgraph",
        id=original["proposal_id"],
        event_id=action["generation_event_id"],
        generated_at=action["generated_at"],
        actor_id=action["responsible_actor_id"],
        role="proposer",
        source_record_ids=[original["id"], action["id"], policy["id"]],
        proposal_key=proposal_key,
        revision=1,
        base_acceptance_head=original["action_acceptance_head"],
        epistemic_policy_id=policy["id"],
        epistemic_policy_hash=policy["record_hash"],
        member_content_hashes=[action["content_hash"]],
        claim_version_ids=[],
        evidence_ids=[],
        evidence_assertion_ids=[],
        action_proposal_ids=[action["id"]],
    )
    first = _event(
        context_record,
        "ARTIFACT_RECORDED",
        {
            "records": _value("SourceArtifact", context_record),
            "dependencies": {"value": context_record["source_record_ids"]},
            "preimage": {
                "value": {k: context_record[v] for k, v in SOURCE_PROJECTION.items()}
            },
            "initialization": {
                "value": checkpoint,
                "record_hash": init_record["content_hash"],
            },
            "references": {
                role: _reference(_source(view, source_ids[role])[0]) for role in ROLES
            },
        },
        {
            "source": {
                "record_id": original["id"],
                "content": original_context_bytes,
                "media_type": "application/json",
                "role": "SOURCE_ARTIFACT",
                "encoding": "CANONICAL_JSON",
            }
        },
    )
    second = _event(
        action,
        "PROPOSAL_RECORDED",
        {
            "action": _value("SupplierOrderAmendment", action),
            "proposal": _value("ProposedSubgraph", proposal),
            "action_dependencies": {"value": action["source_record_ids"]},
            "proposal_dependencies": {"value": proposal["source_record_ids"]},
        },
        {},
    )
    return history.append_protocol_events(
        transaction="context-proposal",
        events=(first, second),
        expected_head=expected_head,
        expected_count=expected_count,
    )


def _proposal_inputs(replay, proposal_id, context_id):
    records = replay.protocol_replay.data["records"]
    proposal = _record(records, proposal_id, "ProposedSubgraph")
    _record(records, context_id, "SourceArtifact")
    original = _object(replay.retained_bytes(context_id))
    _require(
        original["proposal_id"] == proposal_id and original["id"] == context_id,
        "MALFORMED_INPUT",
        "wrong original proposal context",
    )
    _require(
        len(proposal["action_proposal_ids"]) == 1,
        "UNSUPPORTED",
        "exactly one action per proposal required",
    )
    action = _record(
        records, proposal["action_proposal_ids"][0], "SupplierOrderAmendment"
    )
    policy = _record(
        records, proposal["epistemic_policy_id"], "EpistemicPolicyArtifact"
    )
    return records, original, proposal, action, policy


@_guarded
def record_supplier_type_check(
    *,
    history,
    proposal_id,
    context_id,
    monitor_id,
    assessment_id,
    failure_id,
    actor_id,
    generated_at,
    expected_head,
    expected_count,
):
    """Run the actual producer, then submit its completed or unavailable output."""
    replay = _owner(history, expected_head, expected_count)
    _text(proposal_id, context_id, monitor_id, assessment_id, failure_id, actor_id)
    _time(generated_at)
    records, original, proposal, action, policy = _proposal_inputs(
        replay, proposal_id, context_id
    )
    _require(
        monitor_id in policy["required_monitor_ids"],
        "UNSUPPORTED",
        "monitor is not required by the selected policy",
    )
    _require(
        assessment_id != failure_id
        and assessment_id not in records
        and failure_id not in records,
        "MALFORMED_INPUT",
        "fresh distinct output IDs required",
    )
    monitor = _record(records, monitor_id, "MonitorSpecificationArtifact")
    view = freeze_accepted_replay(replay=replay, context=history.composition_context())
    checkpoint, _ = _initialization(view, _active_initialization(view))
    contract, _ = _source(view, checkpoint["record_contract"]["id"])
    request = {
        "kind": "TYPE",
        "event": {
            "id": "event:" + assessment_id,
            "generated_at": generated_at,
            "responsible_actor_id": actor_id,
            "responsible_role": "type-monitor",
        },
        "output_ids": {"assessment": assessment_id, "failure": failure_id},
        "monitor": _reference(monitor),
        "implementation": load_check_executor().implementation_reference,
        "inputs": [
            {"role": "proposal", "value": _reference(proposal)},
            {"role": "action", "value": _reference(action)},
            {
                "role": "record_contract",
                "value": {
                    "id": contract["id"],
                    "bytes_sha256": contract["source_content_digest"],
                },
            },
        ],
    }
    result = run_history_check(history, invocation=request)
    _require(
        (result.ledger_head, result.ledger_event_count)
        == (expected_head, expected_count),
        "STALE_BASE",
        "check producer used a different prefix",
    )
    output = result.execution.data["records"]
    _require(len(output) in (1, 2), "UNSUPPORTED", "unexpected check result arity")
    assessment = output[-1]["record"]
    ids = {
        "proposal": proposal_id,
        "action": action["id"],
        "monitor": monitor_id,
        "policy": policy["id"],
        "contract": contract["id"],
        "context": context_id,
        "static0": monitor["input_artifact_ids"][0],
        "static1": monitor["input_artifact_ids"][1],
    }
    data = {
        "assessment": {"value": [output[-1]]},
        "assessment_dependencies": {"value": assessment["source_record_ids"]},
        "references": {
            role: _reference(records[i]["record"]) for role, i in ids.items()
        },
        "original": {"value": original},
    }
    if len(output) == 2:
        data["failure"] = {"value": [output[0]]}
        data["failure_dependencies"] = {
            "value": output[0]["record"]["source_record_ids"]
        }
    return history.append_protocol_events(
        transaction="type-unavailable" if len(output) == 2 else "type-completed",
        events=(_event(assessment, "ASSESSMENT_RECORDED", data, {}),),
        expected_head=expected_head,
        expected_count=expected_count,
    )


@_guarded
def decide_supplier_proposal(
    *,
    history,
    proposal_id,
    context_id,
    assessment_ids,
    decision_id,
    transition_id,
    actor_id,
    generated_at,
    expected_head,
    expected_count,
):
    """Record the public policy evaluator's verdict, never a supplied verdict."""
    replay = _owner(history, expected_head, expected_count)
    _text(proposal_id, context_id, decision_id, transition_id, actor_id)
    _time(generated_at)
    _require(
        type(assessment_ids) is tuple,
        "MALFORMED_INPUT",
        "immutable explicit assessment IDs required",
    )
    _text(*assessment_ids)
    records, original, proposal, _, policy = _proposal_inputs(
        replay, proposal_id, context_id
    )
    monitors = [
        _record(records, i, "MonitorSpecificationArtifact")
        for i in policy["required_monitor_ids"]
    ]
    outputs = []
    for identifier in assessment_ids:
        kind = records[identifier]["record_type"]
        _require(
            kind in ("TypeAssessment", "UnavailableAssessment"),
            "UNSUPPORTED",
            "only recorded TYPE outcomes are inputs",
        )
        outputs.append(_record(records, identifier, kind))
    evaluation = evaluate_epistemic_policy(
        policy,
        {m["id"]: m for m in monitors},
        outputs,
        proposal_id=proposal_id,
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
    )
    header = dict(
        event_id="event:" + decision_id, generated_at=generated_at, actor_id=actor_id
    )
    decision = make_record(
        "EpistemicDecision",
        **header,
        id=decision_id,
        role="epistemic-controller",
        source_record_ids=[
            proposal_id,
            policy["id"],
            policy["ruleset_id"],
            *evaluation.assessment_ids,
        ],
        proposal_id=proposal_id,
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
        epistemic_verdict=evaluation.verdict,
        assessment_ids=list(evaluation.assessment_ids),
        triggered_assessment_ids=list(evaluation.triggered_assessment_ids),
        policy_evaluation_hash=evaluation.evaluation_hash,
        evidence_assertion_ids=[],
        request_ids=[],
        claim_revision_ids=[],
        policy_id=policy["id"],
        policy_hash=policy["content_hash"],
        ruleset_id=policy["ruleset_id"],
        ruleset_hash=policy["ruleset_record_hash"],
        rationale_codes=["POLICY_RESULT"],
        rationale="The selected policy determines this decision.",
    )
    transition = make_record(
        "TransitionRecord",
        **header,
        id=transition_id,
        role="state-controller",
        source_record_ids=[decision_id],
        transition_subject_id=proposal_id,
        from_state="PROPOSED",
        to_state=TARGETS[evaluation.verdict],
        triggering_record_id=decision_id,
        ledger_event_id=header["event_id"],
        sequence=replay.ledger_event_count + 1,
        transition_time=generated_at,
    )
    ids = {
        "proposal": proposal_id,
        "policy": policy["id"],
        "context": context_id,
        "rules": policy["ruleset_id"],
    }
    data = {
        "references": {
            role: _reference(records[i]["record"]) for role, i in ids.items()
        },
        "original": {"value": original},
        "control": {
            "recipe": "ASSENT_EPISTEMIC_CONTROL_V1",
            "monitors": monitors,
            "bindings": {
                "proposal_id": proposal_id,
                "proposal_content_hash": proposal["content_hash"],
                "base_acceptance_head": proposal["base_acceptance_head"],
            },
        },
        "outputs": outputs,
        "decision": _value("EpistemicDecision", decision),
        "transition": _value("TransitionRecord", transition),
        "decision_dependencies": {"value": decision["source_record_ids"]},
        "transition_dependencies": {"value": transition["source_record_ids"]},
    }
    if evaluation.verdict == "ACCEPT":
        data["acceptance_preimage"] = {
            "previous_acceptance_head": proposal["base_acceptance_head"],
            "proposal_content_hash": proposal["content_hash"],
            "decision_content_hash": decision["content_hash"],
            "revision_content_hashes": [],
        }
    return history.append_protocol_events(
        transaction="epistemic-" + evaluation.verdict.lower(),
        events=(_event(decision, "EPISTEMIC_DECIDED", data, {}),),
        expected_head=expected_head,
        expected_count=expected_count,
    )

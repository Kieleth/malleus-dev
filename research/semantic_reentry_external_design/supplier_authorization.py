"""Actual supplier direct-grant checks and policy control, without dispatch."""

from functools import wraps
import json

import malleus.compiler as core
from malleus.assent import AUTHORIZATION_TARGETS, make_record
from malleus.control import evaluate_authorization_policy
from malleus.ledger import aware_datetime, canonical_json, content_digest, record_hash
from malleus.source import source_artifact_fields
from research.action_history_contract_freeze.programs.check_executor import (
    load_check_executor,
)
from research.action_history_contract_freeze.programs.history_checks import (
    run_history_check,
)
from research.action_history_contract_freeze.programs.registration_bundle import (
    SOURCE_PROJECTION,
)


class SupplierAuthorityError(ValueError):
    def __init__(self, reason, detail):
        self.reason, self.detail = reason, detail
        super().__init__(f"{reason}: {detail}")


def _guarded(function):
    @wraps(function)
    def invoke(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (TypeError, KeyError, AttributeError, RecursionError) as error:
            raise SupplierAuthorityError("MALFORMED_INPUT", str(error)) from error

    return invoke


def _need(condition, reason, detail):
    if not condition:
        raise SupplierAuthorityError(reason, detail)


def _text(*values):
    _need(
        all(type(v) is str and v.strip() for v in values),
        "MALFORMED_INPUT",
        "explicit nonblank identifiers required",
    )


def _canonical(value):
    try:
        return canonical_json(value).encode()
    except ValueError as error:
        raise SupplierAuthorityError("MALFORMED_INPUT", str(error)) from error


def _object(content):
    _need(type(content) is bytes, "MALFORMED_INPUT", "exact bytes required")
    try:
        value = json.loads(content)
    except ValueError as error:
        raise SupplierAuthorityError("MALFORMED_INPUT", str(error)) from error
    _need(
        type(value) is dict and _canonical(value) == content,
        "MALFORMED_INPUT",
        "canonical JSON object required",
    )
    return value


def _instant(value):
    try:
        return aware_datetime(value, "supplier authority time")
    except ValueError as error:
        raise SupplierAuthorityError("MALFORMED_INPUT", str(error)) from error


def _owner(history, head, count):
    _need(
        type(history) is core.KnowledgeChangeHistory,
        "MALFORMED_INPUT",
        "actual owning Core history required",
    )
    _text(head)
    _need(
        type(count) is int and count >= 0,
        "MALFORMED_INPUT",
        "nonnegative integer event count required",
    )
    replay = history.replay()
    _need(
        (head, count) == (replay.ledger_head, replay.ledger_event_count),
        "STALE_BASE",
        "expected ledger head/count differ",
    )
    _need(
        replay.protocol_replay is not None,
        "UNSUPPORTED",
        "selected experimental action attachment required",
    )
    return replay


def _record(replay, identifier, kind):
    _text(identifier)
    entry = replay.protocol_replay.data["records"][identifier]
    value = entry["record"]
    _need(
        entry["record_type"] == kind
        and value["id"] == identifier
        and record_hash(kind, value) == value["content_hash"],
        "MALFORMED_INPUT",
        "wrong typed record or hash: " + identifier,
    )
    return value


def _reference(record):
    return {"id": record["id"], "record_hash": record["content_hash"]}


def _source(replay, identifier):
    value = _record(replay, identifier, "SourceArtifact")
    return value, _object(replay.retained_bytes(identifier))


def _domain(replay):
    return {
        "effective_contract_identity": replay.partial_contract.identity,
        "kcs_acceptance_head": replay.acceptance_head,
        "materialization_head": replay.materialization_head,
        "accepted_graph_digest": replay.graph.state_digest(),
    }


def _index(replay, name, identifier):
    rows = replay.protocol_replay.data["state"]["protocol"][name]
    matches = [r["value"] for r in rows if r["keys"] == [identifier]]
    _need(
        len(matches) == 1, "MALFORMED_INPUT", "one applied " + name + " entry required"
    )
    return matches[0]


def _accepted(replay, original_context_id):
    _, original = _source(replay, original_context_id)
    proposal = _record(replay, original["proposal_id"], "ProposedSubgraph")
    action = _record(replay, original["action_id"], "SupplierOrderAmendment")
    _need(
        _index(replay, "context_by_proposal", proposal["id"]) == original_context_id
        and _index(replay, "proposal_states", proposal["id"]) == "ACCEPTED",
        "NOT_ACCEPTED",
        "actual supplier proposal ACCEPT is required",
    )
    decision = _record(
        replay,
        _index(replay, "epistemic_decisions", proposal["id"]),
        "EpistemicDecision",
    )
    _need(
        decision["epistemic_verdict"] == "ACCEPT",
        "NOT_ACCEPTED",
        "the applied decision did not accept this proposal",
    )
    _need(
        original["domain"] == _domain(replay),
        "STALE_BASE",
        "domain context changed since the proposal",
    )
    return original, proposal, action, decision


def _draft(record, event_type, data, retained):
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


def _source_draft(identifier, content, dependencies, actor, time, version, encoding):
    value = make_record(
        "SourceArtifact",
        id=identifier,
        event_id="event:" + identifier,
        generated_at=time,
        actor_id=actor,
        role="registrar",
        source_record_ids=dependencies,
        artifact_kind="SOURCE",
        artifact_version=version,
        **source_artifact_fields(
            artifact_id=identifier,
            artifact_version=version,
            source_bytes=content,
            media_type="application/json",
            locator="urn:retained:" + identifier,
        ),
    )
    return _draft(
        value,
        "PREREQUISITE_RECORDED",
        {
            "records": _value("SourceArtifact", value),
            "dependencies": {"value": dependencies},
            "preimage": {"value": {k: value[v] for k, v in SOURCE_PROJECTION.items()}},
        },
        {
            "source": {
                "record_id": identifier,
                "content": content,
                "media_type": "application/json",
                "role": "SOURCE_ARTIFACT",
                "encoding": encoding,
            }
        },
    )


def _append(history, replay, transaction, event):
    return history.append_protocol_events(
        transaction=transaction,
        events=(event,),
        expected_head=replay.ledger_head,
        expected_count=replay.ledger_event_count,
    )


@_guarded
def prepare_supplier_authority(
    *,
    history,
    expected_head,
    expected_count,
    original_context_id,
    grant_bytes,
    scope_association_id,
    requested_interval_id,
    current_context_id,
    requested_interval_bytes,
    actor_id,
    generated_at,
    artifact_version,
):
    """Register actual grant inputs and capture current context, not permission."""
    replay = _owner(history, expected_head, expected_count)
    _text(
        original_context_id,
        scope_association_id,
        requested_interval_id,
        current_context_id,
        actor_id,
        artifact_version,
    )
    _instant(generated_at)
    original, _, _, _ = _accepted(replay, original_context_id)
    grant, interval = _object(grant_bytes), _object(requested_interval_bytes)
    _need(
        set(interval) == {"start", "end"},
        "MALFORMED_INPUT",
        "closed requested start/end interval required",
    )
    _need(
        _instant(interval["start"]) < _instant(interval["end"]),
        "MALFORMED_INPUT",
        "requested interval must have positive duration",
    )
    # The applied initialization already binds the exact retained record contract.
    members = [
        m
        for m in replay.retained_inputs
        if m.identity == original["initialization_identity"]
    ]
    _need(
        len(members) == 1, "MALFORMED_INPUT", "unique applied initialization required"
    )
    checkpoint = _object(members[0].content)
    _need(
        _index(replay, "initialization", "ACTIVE")
        == original["initialization_identity"],
        "MALFORMED_INPUT",
        "original initialization is not applied",
    )
    contract = core.load_validated_contract_artifact(
        replay.retained_bytes(checkpoint["record_contract"]["id"])
    )
    errors = contract.validate_instance("AuthorityGrant", grant)
    _need(not errors, "MALFORMED_INPUT", "invalid AuthorityGrant: " + str(errors))
    _need(
        record_hash("AuthorityGrant", grant) == grant["content_hash"],
        "MALFORMED_INPUT",
        "grant record hash differs",
    )
    fields = {
        name: grant[name]
        for name in (
            "grantor_actor_id",
            "grantee_actor_id",
            "permitted_action_types",
            "scope_record_id",
            "may_subdelegate",
            "grant_valid_from",
            "grant_valid_to",
        )
    }
    _need(
        content_digest(fields) == grant["artifact_hash"],
        "MALFORMED_INPUT",
        "grant artifact hash differs",
    )
    _need(
        grant["responsible_actor_id"] == grant["grantor_actor_id"],
        "MALFORMED_INPUT",
        "grant must be recorded by its declared grantor",
    )
    _instant(grant["generated_at"])
    _need(
        _instant(grant["grant_valid_from"]) < _instant(grant["grant_valid_to"]),
        "MALFORMED_INPUT",
        "grant interval must have positive duration",
    )
    identifiers = [
        grant["id"],
        scope_association_id,
        requested_interval_id,
        current_context_id,
    ]
    _text(*identifiers)
    used = set(replay.protocol_replay.data["records"]) | {
        m.record_id for m in replay.retained_inputs
    }
    _need(
        len(set(identifiers)) == len(identifiers)
        and not used.intersection(identifiers),
        "MALFORMED_INPUT",
        "fresh distinct prerequisite IDs required",
    )
    grant_scope, _ = _source(replay, grant["scope_record_id"])
    action_scope, _ = _source(replay, original["goal"]["id"])
    association = {
        "id": scope_association_id,
        "comparison": "EXACT_RECORD_ID_AND_HASH",
        "grant_scope": _reference(grant_scope),
        "action_scope": _reference(action_scope),
    }
    association_event = _source_draft(
        scope_association_id,
        _canonical(association),
        sorted({grant_scope["id"], action_scope["id"]}),
        actor_id,
        generated_at,
        artifact_version,
        "BYTES",
    )
    interval_event = _source_draft(
        requested_interval_id,
        requested_interval_bytes,
        [],
        actor_id,
        generated_at,
        artifact_version,
        "BYTES",
    )
    grant_event = _draft(
        grant,
        "PREREQUISITE_RECORDED",
        {
            "records": _value("AuthorityGrant", grant),
            "dependencies": {"value": grant["source_record_ids"]},
        },
        {},
    )
    for transaction, event in (
        ("source", association_event),
        ("source", interval_event),
        ("grant", grant_event),
    ):
        replay = _append(history, replay, transaction, event)
    original, _, _, _ = _accepted(replay, original_context_id)
    current = {
        "id": current_context_id,
        "prefix": {
            "head": replay.ledger_head,
            "event_count": replay.ledger_event_count,
        },
        "domain": _domain(replay),
        "action_acceptance_head": replay.protocol_replay.data["state"][
            "action_acceptance_head"
        ],
        "initialization_identity": original["initialization_identity"],
        "epistemic_policy": original["epistemic_policy"],
        "authorization_policy": original["authorization_policy"],
    }
    event = _source_draft(
        current_context_id,
        _canonical(current),
        [current[role + "_policy"]["id"] for role in ("epistemic", "authorization")],
        actor_id,
        generated_at,
        artifact_version,
        "CANONICAL_JSON",
    )
    return _append(history, replay, "capture-current", event)


def _bindings(
    replay,
    original_context_id,
    current_context_id,
    grant_id,
    scope_association_id,
    requested_interval_id,
    executor_id,
):
    _text(executor_id)
    original, proposal, action, epistemic = _accepted(replay, original_context_id)
    original_record, _ = _source(replay, original_context_id)
    current_record, current = _source(replay, current_context_id)
    grant = _record(replay, grant_id, "AuthorityGrant")
    association, _ = _source(replay, scope_association_id)
    interval, requested = _source(replay, requested_interval_id)
    policy = _record(
        replay, original["authorization_policy"]["id"], "AuthorizationPolicyArtifact"
    )
    roles = {
        "proposal": _reference(proposal),
        "action": _reference(action),
        "executor_id": executor_id,
        "grant": _reference(grant),
        **{
            role: {"id": value["id"], "bytes_sha256": value["source_content_digest"]}
            for role, value in (
                ("scope_association", association),
                ("requested_interval", interval),
            )
        },
        "authorization_policy": _reference(policy),
        **{
            role: {"id": value["id"], "bytes_sha256": value["source_content_digest"]}
            for role, value in (
                ("original_context", original_record),
                ("current_context", current_record),
            )
        },
    }
    return (
        roles,
        original,
        current,
        proposal,
        action,
        epistemic,
        grant,
        policy,
        requested,
    )


def _context_data(replay, roles, original, current, epistemic, monitor):
    ids = {role: value["id"] for role, value in roles.items() if role != "executor_id"}
    ids.update(
        monitor=monitor["id"],
        epistemic=epistemic["id"],
        static0=monitor["input_artifact_ids"][0],
        static1=monitor["input_artifact_ids"][1],
    )
    records = replay.protocol_replay.data["records"]
    return {
        "references": {
            role: _reference(records[i]["record"]) for role, i in ids.items()
        },
        "contents": {"original_context": original, "current_context": current},
        "executor_id": roles["executor_id"],
    }


@_guarded
def record_supplier_authority_check(
    *,
    history,
    expected_head,
    expected_count,
    original_context_id,
    current_context_id,
    grant_id,
    scope_association_id,
    requested_interval_id,
    executor_id,
    monitor_id,
    assessment_id,
    failure_id,
    actor_id,
    generated_at,
):
    """Compute real DIRECT_GRANT output before its separate atomic admission."""
    replay = _owner(history, expected_head, expected_count)
    _text(monitor_id, assessment_id, failure_id, actor_id)
    _instant(generated_at)
    roles, original, current, _, _, epistemic, _, policy, _ = _bindings(
        replay,
        original_context_id,
        current_context_id,
        grant_id,
        scope_association_id,
        requested_interval_id,
        executor_id,
    )
    _need(
        monitor_id in policy["required_monitor_ids"],
        "UNSUPPORTED",
        "required authority monitor expected",
    )
    records = replay.protocol_replay.data["records"]
    _need(
        assessment_id != failure_id
        and assessment_id not in records
        and failure_id not in records,
        "MALFORMED_INPUT",
        "fresh distinct output IDs required",
    )
    monitor = _record(replay, monitor_id, "MonitorSpecificationArtifact")
    invocation = {
        "kind": "DIRECT_GRANT",
        "event": {
            "id": "event:" + assessment_id,
            "generated_at": generated_at,
            "responsible_actor_id": actor_id,
            "responsible_role": "authority-monitor",
        },
        "output_ids": {"assessment": assessment_id, "failure": failure_id},
        "monitor": _reference(monitor),
        "implementation": load_check_executor().implementation_reference,
        "inputs": [{"role": role, "value": value} for role, value in roles.items()],
    }
    result = run_history_check(history, invocation=invocation)
    _need(
        (result.ledger_head, result.ledger_event_count)
        == (expected_head, expected_count),
        "STALE_BASE",
        "producer used a different prefix",
    )
    output = result.execution.data["records"]
    _need(len(output) in (1, 2), "UNSUPPORTED", "unexpected authority output arity")
    assessment = output[-1]["record"]
    data = _context_data(replay, roles, original, current, epistemic, monitor)
    data.update(
        assessment={"value": [output[-1]]},
        assessment_dependencies={"value": assessment["source_record_ids"]},
    )
    if len(output) == 2:
        data["failure"] = {"value": [output[0]]}
        data["failure_dependencies"] = {
            "value": output[0]["record"]["source_record_ids"]
        }
    return history.append_protocol_events(
        transaction="authority-unavailable"
        if len(output) == 2
        else "authority-completed",
        events=(_draft(assessment, "ASSESSMENT_RECORDED", data, {}),),
        expected_head=expected_head,
        expected_count=expected_count,
    )


@_guarded
def decide_supplier_authorization(
    *,
    history,
    expected_head,
    expected_count,
    original_context_id,
    current_context_id,
    grant_id,
    scope_association_id,
    requested_interval_id,
    executor_id,
    assessment_ids,
    decision_id,
    transition_id,
    actor_id,
    generated_at,
):
    """Record actual AUTHORIZE/BLOCK/CLARIFY, without dispatch or domain mutation."""
    replay = _owner(history, expected_head, expected_count)
    _text(decision_id, transition_id, actor_id)
    _instant(generated_at)
    _need(
        type(assessment_ids) is tuple,
        "MALFORMED_INPUT",
        "immutable assessment IDs required",
    )
    _text(*assessment_ids)
    roles, original, current, proposal, action, epistemic, grant, policy, interval = (
        _bindings(
            replay,
            original_context_id,
            current_context_id,
            grant_id,
            scope_association_id,
            requested_interval_id,
            executor_id,
        )
    )
    records = replay.protocol_replay.data["records"]
    monitors = [
        _record(replay, i, "MonitorSpecificationArtifact")
        for i in policy["required_monitor_ids"]
    ]
    outputs = []
    for identifier in assessment_ids:
        kind = records[identifier]["record_type"]
        _need(
            kind in ("AuthorityAssessment", "UnavailableAuthorityAssessment"),
            "UNSUPPORTED",
            "only recorded authority outcomes are inputs",
        )
        outputs.append(_record(replay, identifier, kind))
    head = replay.protocol_replay.data["state"]["action_acceptance_head"]
    evaluated = evaluate_authorization_policy(
        policy,
        {m["id"]: m for m in monitors},
        outputs,
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        action_id=action["id"],
        action_content_hash=action["content_hash"],
        evaluated_actor_id=executor_id,
        base_acceptance_head=head,
    )
    header = dict(
        event_id="event:" + decision_id, generated_at=generated_at, actor_id=actor_id
    )
    decision = make_record(
        "AuthorizationDecision",
        **header,
        id=decision_id,
        role="authorizer",
        source_record_ids=[
            action["id"],
            policy["id"],
            epistemic["id"],
            *evaluated.assessment_ids,
            grant_id,
        ],
        base_acceptance_head=head,
        policy_id=policy["id"],
        policy_hash=policy["content_hash"],
        rationale_codes=["POLICY_RESULT"],
        rationale="The retained policy computes permission.",
        action_proposal_id=action["id"],
        action_content_hash=action["content_hash"],
        authorization_verdict=evaluated.verdict,
        epistemic_decision_ids=[epistemic["id"]],
        relied_on_claim_version_ids=[],
        authority_assessment_ids=list(evaluated.assessment_ids),
        triggered_assessment_ids=list(evaluated.triggered_assessment_ids),
        policy_evaluation_hash=evaluated.evaluation_hash,
        authority_grant_id=grant_id,
        authority_grant_hash=grant["content_hash"],
        authorized_actor_id=executor_id,
        authorization_valid_from=interval["start"]
        if evaluated.verdict == "AUTHORIZE"
        else None,
        authorization_valid_to=interval["end"]
        if evaluated.verdict == "AUTHORIZE"
        else None,
    )
    transition = make_record(
        "TransitionRecord",
        **header,
        id=transition_id,
        role="state-controller",
        source_record_ids=[decision_id],
        transition_subject_id=action["id"],
        from_state="PENDING",
        to_state=AUTHORIZATION_TARGETS[evaluated.verdict].value,
        triggering_record_id=decision_id,
        ledger_event_id=header["event_id"],
        sequence=replay.ledger_event_count + 1,
        transition_time=generated_at,
    )
    data = _context_data(replay, roles, original, current, epistemic, monitors[0])
    data.update(
        outputs=outputs,
        control={
            "recipe": "ASSENT_AUTHORIZATION_CONTROL_V1",
            "monitors": monitors,
            "bindings": {
                "proposal_id": proposal["id"],
                "proposal_content_hash": proposal["content_hash"],
                "base_acceptance_head": head,
                "action_proposal_id": action["id"],
                "action_content_hash": action["content_hash"],
                "evaluated_actor_id": executor_id,
                "authority_policy_id": policy["id"],
                "authority_policy_hash": policy["content_hash"],
            },
        },
        decision=_value("AuthorizationDecision", decision),
        transition=_value("TransitionRecord", transition),
        decision_dependencies={"value": decision["source_record_ids"]},
        transition_dependencies={"value": transition["source_record_ids"]},
    )
    if evaluated.verdict == "AUTHORIZE":
        data["intervals"] = {
            "authorization": {
                "start": decision["authorization_valid_from"],
                "end": decision["authorization_valid_to"],
            },
            "grant": {
                "start": grant["grant_valid_from"],
                "end": grant["grant_valid_to"],
            },
        }
    return history.append_protocol_events(
        transaction="authorization-" + evaluated.verdict.lower(),
        events=(_draft(decision, "AUTHORIZATION_DECIDED", data, {}),),
        expected_head=expected_head,
        expected_count=expected_count,
    )

"""Reference input constructors for the selected finite action profile.

No history creation, policy selection, admission or effects. Registered inputs
come from verified replay. The existing owner validates each returned draft;
construction does not establish that it is admissible. This is research-local
authoring, not a stable SDK or a replacement for the selected program.
"""

from collections.abc import Mapping
from copy import deepcopy
import json

from malleus.assent import make_record
from malleus.ledger import content_digest
from malleus.source import source_artifact_fields
from malleus._contract_pipeline.protocol_runtime import (
    ProtocolProgramRefusal,
    canonical,
)
from research.action_history_contract_freeze.programs.initialization_bundle import (
    DEFINITIONS,
    POLICY_TYPES,
)
from research.action_history_contract_freeze.programs.proposal_bundle import ROLES
from research.action_history_contract_freeze.programs.registration_bundle import (
    SOURCE_PROJECTION,
)


__all__ = (
    "source_event",
    "initialization_checkpoint",
    "initialization_event",
    "context_proposal",
)


def source_event(
    record_id,
    content,
    *,
    source_record_ids,
    event_id,
    transaction_time,
    actor_id,
    role,
    artifact_version,
    media_type,
    locator,
):
    """Build a source-registration draft from exact bytes and explicit origin."""
    record = make_record(
        "SourceArtifact",
        id=record_id,
        event_id=event_id,
        generated_at=transaction_time,
        actor_id=actor_id,
        role=role,
        source_record_ids=sorted(source_record_ids),
        artifact_kind="SOURCE",
        artifact_version=artifact_version,
        **source_artifact_fields(
            artifact_id=record_id,
            artifact_version=artifact_version,
            source_bytes=content,
            media_type=media_type,
            locator=locator,
        ),
    )
    return {
        "event_id": event_id,
        "event_type": "PREREQUISITE_RECORDED",
        "actor_id": actor_id,
        "transaction_time": transaction_time,
        "data": {
            "records": {"value": [{"record_type": "SourceArtifact", "record": record}]},
            "dependencies": {"value": list(record["source_record_ids"])},
            "preimage": {"value": {k: record[v] for k, v in SOURCE_PROJECTION.items()}},
        },
        "retained": {
            "source": {
                "record_id": record_id,
                "content": content,
                "media_type": media_type,
                "role": "SOURCE_ARTIFACT",
                "encoding": "BYTES",
            }
        },
    }


def _replay(history):
    replay = history.replay()
    if replay.protocol_replay is None:
        raise ProtocolProgramRefusal(
            "UNSELECTED_PROGRAM", "select retained action programs first"
        )
    return replay


def _registered(replay, identifier, record_type):
    try:
        value = replay.protocol_replay.data["records"][identifier]
    except KeyError as error:
        raise ProtocolProgramRefusal(
            "MISSING_ACTION_INPUT", "register input record: " + identifier
        ) from error
    if value["record_type"] != record_type:
        raise ProtocolProgramRefusal(
            "WRONG_ACTION_INPUT_TYPE", f"{identifier} must be {record_type}"
        )
    return value["record"]


def _role_records(replay, identifiers, types):
    if not isinstance(identifiers, Mapping) or set(identifiers) != set(types):
        raise ProtocolProgramRefusal(
            "MISSING_ACTION_INPUT", "exact input roles required: " + ", ".join(types)
        )
    snapshot = dict(identifiers)
    return {
        role: _registered(replay, snapshot[role], kind) for role, kind in types.items()
    }


def _coordinates(replay):
    return {
        "prefix": {
            "head": replay.ledger_head,
            "event_count": replay.ledger_event_count,
        },
        "domain": {
            "effective_contract_identity": replay.partial_contract.identity,
            "kcs_acceptance_head": replay.acceptance_head,
            "materialization_head": replay.materialization_head,
            "accepted_graph_digest": replay.graph.state_digest(),
        },
    }


def _references(records):
    return {
        role: {"id": value["id"], "record_hash": value["content_hash"]}
        for role, value in records.items()
    }


def _source_identities(records):
    return {
        role: {"id": value["id"], "bytes_sha256": value["source_content_digest"]}
        for role, value in records.items()
    }


def initialization_checkpoint(history, *, record_id, source_ids, policy_ids):
    """Read one owner snapshot and bind its already registered prerequisites."""
    replay = _replay(history)
    sources = _role_records(
        replay, source_ids, {role: "SourceArtifact" for role in DEFINITIONS}
    )
    policies = _role_records(replay, policy_ids, POLICY_TYPES)
    checkpoint = {
        "schema": "malleus.action-history.initialization/research-v1",
        "id": record_id,
        **_coordinates(replay),
        **_source_identities(sources),
        **{role + "_policy": value for role, value in _references(policies).items()},
    }
    return checkpoint, _references(sources)


def initialization_event(checkpoint, references, **source_metadata):
    """Encode the existing checkpoint draft; the initialize transaction gates it."""
    dependencies = [value["id"] for value in references.values()] + [
        checkpoint[role + "_policy"]["id"] for role in POLICY_TYPES
    ]
    event = source_event(
        checkpoint["id"],
        canonical(checkpoint),
        source_record_ids=dependencies,
        **source_metadata,
    )
    event["retained"]["source"]["encoding"] = "CANONICAL_JSON"
    event["data"]["references"] = deepcopy(references)
    return event


def context_proposal(
    history,
    *,
    initialization_id,
    source_ids,
    context_id,
    context_metadata,
    action,
    proposal_id,
    proposal_key,
    episode_key,
    payload_source_id,
):
    """Build the existing atomic pair using an explicit caller-authored action.

    All source roles and policy records must already be retained and registered.
    ``context_metadata`` supplies the seven required origin/representation kwargs
    of ``source_event``. Proposal attribution comes from the supplied action.
    ``payload_source_id`` explicitly selects the retained-payload input required
    by the sequential profile; None emits the original profile's pair shape.
    Neither choice bypasses the selected transaction's checks.
    """
    replay = _replay(history)
    initial = _registered(replay, initialization_id, "SourceArtifact")
    checkpoint = json.loads(replay.retained_bytes(initialization_id))
    sources = _role_records(
        replay, source_ids, {role: "SourceArtifact" for role in ROLES}
    )
    action = deepcopy(action)
    record = action["record"]
    context = {
        "schema": "malleus.action-history.original-context/research-v1",
        "id": context_id,
        **_coordinates(replay),
        "action_acceptance_head": replay.protocol_replay.data["state"][
            "action_acceptance_head"
        ],
        "initialization_identity": content_digest(checkpoint),
        **{role + "_policy": checkpoint[role + "_policy"] for role in POLICY_TYPES},
        "proposal_id": proposal_id,
        "action_id": record["id"],
        "episode_key": episode_key,
        **_source_identities(sources),
    }
    dependencies = [value["id"] for value in sources.values()] + [initialization_id]
    first = source_event(
        context_id,
        canonical(context),
        source_record_ids=dependencies,
        **context_metadata,
    )
    first["event_type"] = "ARTIFACT_RECORDED"
    first["retained"]["source"]["encoding"] = "CANONICAL_JSON"
    first["data"].update(
        initialization={"value": checkpoint, "record_hash": initial["content_hash"]},
        references=_references(sources),
    )
    policy = checkpoint["epistemic_policy"]
    proposal = make_record(
        "ProposedSubgraph",
        id=proposal_id,
        event_id=record["generation_event_id"],
        generated_at=record["generated_at"],
        actor_id=record["responsible_actor_id"],
        role=record["responsible_role"],
        source_record_ids=[context_id, record["id"], policy["id"]],
        proposal_key=proposal_key,
        revision=record["revision"],
        base_acceptance_head=context["action_acceptance_head"],
        epistemic_policy_id=policy["id"],
        epistemic_policy_hash=policy["record_hash"],
        member_content_hashes=[record["content_hash"]],
        claim_version_ids=[],
        evidence_ids=[],
        evidence_assertion_ids=[],
        action_proposal_ids=[record["id"]],
    )
    second = {
        "event_id": record["generation_event_id"],
        "event_type": "PROPOSAL_RECORDED",
        "actor_id": record["responsible_actor_id"],
        "transaction_time": record["generated_at"],
        "retained": {},
        "data": {
            "action": {"value": [action]},
            "proposal": {
                "value": [{"record_type": "ProposedSubgraph", "record": proposal}]
            },
            "action_dependencies": {"value": list(record["source_record_ids"])},
            "proposal_dependencies": {"value": list(proposal["source_record_ids"])},
        },
    }
    if payload_source_id is not None:
        payload = _registered(replay, payload_source_id, "SourceArtifact")
        second["data"]["payload"] = {
            "id": payload["id"],
            "record_hash": payload["content_hash"],
        }
    return first, second

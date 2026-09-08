"""Current-context capture and real grant checks from the owning Shop history."""

from copy import deepcopy
from importlib import import_module
import json

import pytest

from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest
from research.action_history_contract_freeze.programs import (
    test_decision_history as decisions,
)
from research.action_history_contract_freeze.programs.decision_bundle import (
    add_epistemic_decision,
)
from research.action_history_contract_freeze.programs.history_checks import (
    run_history_check,
)
from research.action_history_contract_freeze.programs.check_executor import (
    load_check_executor,
)
from research.action_history_contract_freeze.programs.test_initialization_history import (
    POLICY_IDS,
    SOURCE_IDS,
    reopen,
)
from research.action_history_contract_freeze.programs.test_proposal_history import (
    source,
    preimage,
)
from research.action_history_contract_freeze.programs.test_registration_history import (
    append,
    draft,
    record,
    TIME,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import api, canonical


@pytest.fixture(scope="module")
def accepted(tmp_path_factory):
    extend = import_module(
        "research.action_history_contract_freeze.programs.current_bundle"
    ).add_current_context
    bundle = extend(
        add_epistemic_decision(
            decisions.add_type_assessment(
                decisions.add_context_proposal(
                    decisions.add_initialization(
                        decisions.builder().build_registration_bundle(
                            decisions.compiled().artifact_bytes
                        ),
                        source_ids=SOURCE_IDS,
                        policy_ids=POLICY_IDS,
                    )
                )
            )
        )
    )
    directory = tmp_path_factory.mktemp("accepted-action-prefix")
    return accepted_prefix(directory, bundle)


def accepted_prefix(directory, bundle):
    decisions.proposed_prefix(directory, bundle)
    history = KnowledgeChangeHistory.reopen(directory / "history.jsonl")
    decisions.assess(history)
    event, evaluation = decisions.decision_event(history)
    decisions.decide(history, event, evaluation.verdict)
    return history.path.read_bytes()


def current_content(history, identifier):
    replay = history.replay()
    state = replay.protocol_replay.data
    return {
        "id": identifier,
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
        "action_acceptance_head": state["state"]["action_acceptance_head"],
        "initialization_identity": state["state"]["protocol"]["initialization"][0][
            "value"
        ],
        **{
            name + "_policy": {
                "id": identifier,
                "record_hash": state["records"][identifier]["record"]["content_hash"],
            }
            for name, identifier in POLICY_IDS.items()
        },
    }


def current_event(value):
    content = canonical(value)
    carrier = source(value["id"], content, list(POLICY_IDS.values()))
    event = draft(
        "SourceArtifact", carrier, preimage=preimage(carrier), content=content
    )
    event["retained"]["source"]["encoding"] = "CANONICAL_JSON"
    return event


def retain_source(history, identifier, value, sources):
    content = canonical(value)
    carrier = source(identifier, content, sources)
    append(
        history,
        "source",
        draft("SourceArtifact", carrier, preimage=preimage(carrier), content=content),
    )
    return carrier


def grant_inputs(history, *, grantee):
    values = history.replay().protocol_replay.data["records"]
    scope = values["source:goal"]["record"]
    association = retain_source(
        history,
        "source:scope-association",
        {
            "id": "source:scope-association",
            "comparison": "EXACT_RECORD_ID_AND_HASH",
            "grant_scope": {"id": scope["id"], "record_hash": scope["content_hash"]},
            "action_scope": {"id": scope["id"], "record_hash": scope["content_hash"]},
        },
        [scope["id"]],
    )
    interval = retain_source(
        history,
        "source:requested-interval",
        {"start": TIME, "end": "2026-09-07T01:00:00Z"},
        [],
    )
    grant_fields = dict(
        grantor_actor_id="actor:registrar",
        grantee_actor_id=grantee,
        permitted_action_types=["LOCAL_ACTION"],
        scope_record_id=scope["id"],
        may_subdelegate=False,
        grant_valid_from=TIME,
        grant_valid_to="2026-09-07T02:00:00Z",
    )
    grant = record(
        "AuthorityGrant",
        "grant:direct",
        [scope["id"]],
        artifact_kind="AUTHORITY_GRANT",
        artifact_version="v1",
        artifact_hash=content_digest(grant_fields),
        **grant_fields,
    )
    append(history, "grant", draft("AuthorityGrant", grant))
    current = current_content(history, "source:current-context")
    append(history, "capture-current", current_event(current))
    replay = history.replay()
    values = {k: v["record"] for k, v in replay.protocol_replay.data["records"].items()}
    policy = values[POLICY_IDS["authorization"]]
    monitor = values[policy["required_monitor_ids"][0]]
    roles = {
        "proposal": {
            "id": "proposal:1",
            "record_hash": values["proposal:1"]["content_hash"],
        },
        "action": {"id": "action:1", "record_hash": values["action:1"]["content_hash"]},
        "executor_id": "actor:executor",
        "grant": {"id": grant["id"], "record_hash": grant["content_hash"]},
        "scope_association": {
            "id": association["id"],
            "bytes_sha256": association["source_content_digest"],
        },
        "requested_interval": {
            "id": interval["id"],
            "bytes_sha256": interval["source_content_digest"],
        },
        "authorization_policy": {
            "id": policy["id"],
            "record_hash": policy["content_hash"],
        },
        "original_context": {
            "id": "context:1",
            "bytes_sha256": values["context:1"]["source_content_digest"],
        },
        "current_context": {
            "id": current["id"],
            "bytes_sha256": values[current["id"]]["source_content_digest"],
        },
    }
    return {
        "kind": "DIRECT_GRANT",
        "event": {
            "id": "event:authority-assessment:0",
            "generated_at": TIME,
            "responsible_actor_id": "actor:authority-checker",
            "responsible_role": "authority-monitor",
        },
        "output_ids": {
            "assessment": "authority-assessment:0",
            "failure": "authority-failure:0",
        },
        "monitor": {"id": monitor["id"], "record_hash": monitor["content_hash"]},
        "implementation": load_check_executor().implementation_reference,
        "inputs": [{"role": name, "value": value} for name, value in roles.items()],
    }


def test_current_context_is_retained_against_actual_prefix_without_changing_heads(
    tmp_path, accepted
):
    history = reopen(tmp_path, accepted)
    before = history.replay()
    value = current_content(history, "source:current")
    after = append(history, "capture-current", current_event(value))
    assert after.protocol_replay.data["state"]["protocol"]["current_contexts"] == [
        {"keys": [value["id"]], "value": content_digest(value)}
    ]
    assert json.loads(after.retained_bytes(value["id"])) == value
    assert after.graph.export_records() == before.graph.export_records()
    assert after.change_sets == before.change_sets
    assert after.acceptance_head == before.acceptance_head
    assert (
        after.protocol_replay.data["state"]["action_acceptance_head"]
        == before.protocol_replay.data["state"]["action_acceptance_head"]
    )
    assert KnowledgeChangeHistory.reopen(history.path).replay().receipt == after.receipt


@pytest.mark.parametrize(
    "fault", ["prefix", "domain", "action", "initialization", "policy"]
)
def test_forged_current_context_refuses_before_retention(tmp_path, accepted, fault):
    history = reopen(tmp_path, accepted)
    value = deepcopy(current_content(history, "source:forged-current"))
    if fault == "prefix":
        value["prefix"]["event_count"] -= 1
    elif fault == "domain":
        value["domain"]["accepted_graph_digest"] = content_digest("wrong")
    elif fault == "action":
        value["action_acceptance_head"] = content_digest("wrong")
    elif fault == "initialization":
        value["initialization_identity"] = content_digest("wrong")
    else:
        value["authorization_policy"]["record_hash"] = content_digest("wrong")
    before = history.path.read_bytes()
    with pytest.raises(api().ProtocolProgramRefusal):
        append(history, "capture-current", current_event(value))
    assert history.path.read_bytes() == before


@pytest.mark.parametrize(
    "grantee,outcome", [("actor:executor", "SATISFIED"), ("actor:other", "VIOLATED")]
)
def test_real_direct_grant_check_consumes_actual_retained_inputs_without_permission(
    tmp_path, accepted, grantee, outcome
):
    history = reopen(tmp_path, accepted)
    request = grant_inputs(history, grantee=grantee)
    before = history.path.read_bytes()
    result = run_history_check(history, invocation=request)
    output = result.execution.data["records"][0]
    assert output["record_type"] == "AuthorityAssessment"
    assert output["record"]["assessment_outcome"] == outcome
    assert output["record"]["violated_policy_predicates"] == (
        [] if outcome == "SATISFIED" else ["GRANTEE_MATCH"]
    )
    replay = history.replay()
    assert (
        output["record"]["base_acceptance_head"]
        == replay.protocol_replay.data["state"]["action_acceptance_head"]
    )
    assert output["record"]["evaluated_actor_id"] == "actor:executor"
    assert history.path.read_bytes() == before
    assert output["record"]["id"] not in replay.protocol_replay.data["records"]
    assert replay.protocol_replay.data["state"]["protocol"]["authorization_states"] == [
        {"keys": ["action:1"], "value": "PENDING"}
    ]

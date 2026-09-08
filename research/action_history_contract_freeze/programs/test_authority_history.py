"""Actual direct-grant outputs, bound to ACCEPT and retained contexts."""

from copy import deepcopy
from importlib import import_module
import json

import pytest

from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest, record_hash
from research.action_history_contract_freeze.programs import check_executor
from research.action_history_contract_freeze.programs import (
    test_current_history as current,
)
from research.action_history_contract_freeze.programs import (
    test_decision_history as decisions,
)
from research.action_history_contract_freeze.programs.current_bundle import (
    add_current_context,
)
from research.action_history_contract_freeze.programs.decision_bundle import (
    add_epistemic_decision,
)
from research.action_history_contract_freeze.programs.history_checks import (
    run_history_check,
)
from research.action_history_contract_freeze.programs.test_initialization_history import (
    SOURCE_IDS,
    POLICY_IDS,
    reopen,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import api


def test_shared_census_generation_preserves_exact_type_output_shapes():
    from research.action_history_contract_freeze.programs.assessment_bundle import output_schemas

    assert content_digest(output_schemas(prefix="type", closure_length=6, role="type-monitor")) == (
        "sha256:0af96d5d651bb3bf14f676d1ba27409ce97e0a8cd6f2f8ba6e4dda1699f545f7"
    )


@pytest.fixture(scope="module")
def prepared(tmp_path_factory):
    extend = import_module(
        "research.action_history_contract_freeze.programs.authority_bundle"
    ).add_authority_assessment
    bundle = extend(
        add_current_context(
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
    )
    directory = tmp_path_factory.mktemp("authority-prefix")
    content = current.accepted_prefix(directory, bundle)
    result = {}
    for grantee in ("actor:executor", "actor:other"):
        history = reopen(tmp_path_factory.mktemp("grant-prefix"), content)
        request = current.grant_inputs(history, grantee=grantee)
        result[grantee] = (history.path.read_bytes(), request)
    return result


def event(history, result, request):
    replay = history.replay()
    values = {k: v["record"] for k, v in replay.protocol_replay.data["records"].items()}
    output = result.execution.data["records"]
    assessment = output[-1]["record"]
    roles = {entry["role"]: entry["value"] for entry in request["inputs"]}
    ids = {role: value["id"] for role, value in roles.items() if role != "executor_id"}
    monitor = values[request["monitor"]["id"]]
    ids.update(
        monitor=monitor["id"],
        epistemic="decision:1",
        static0=monitor["input_artifact_ids"][0],
        static1=monitor["input_artifact_ids"][1],
    )
    data = {
        "references": {
            name: {"id": identifier, "record_hash": values[identifier]["content_hash"]}
            for name, identifier in ids.items()
        },
        "contents": {
            name: json.loads(replay.retained_bytes(ids[name]))
            for name in ("original_context", "current_context")
        },
        "executor_id": roles["executor_id"],
        "assessment": {"value": [output[-1]]},
        "assessment_dependencies": {"value": deepcopy(assessment["source_record_ids"])},
    }
    if len(output) == 2:
        data["failure"] = {"value": [output[0]]}
        data["failure_dependencies"] = {
            "value": deepcopy(output[0]["record"]["source_record_ids"])
        }
    return {
        "event_id": assessment["generation_event_id"],
        "event_type": "ASSESSMENT_RECORDED",
        "actor_id": assessment["responsible_actor_id"],
        "transaction_time": assessment["generated_at"],
        "data": data,
        "retained": {},
    }


def admit(history, result, draft):
    return history.append_protocol_events(
        transaction="authority-unavailable"
        if "failure" in draft["data"]
        else "authority-completed",
        events=(draft,),
        expected_head=result.ledger_head,
        expected_count=result.ledger_event_count,
    )


@pytest.mark.parametrize("grantee", ["actor:executor", "actor:other"])
def test_real_authority_outputs_are_retained_judgments_not_permission(
    tmp_path, prepared, grantee, monkeypatch
):
    content, request = prepared[grantee]
    history = reopen(tmp_path, content)
    before = history.replay()
    result = run_history_check(history, invocation=request)
    draft = event(history, result, request)

    def forbidden(*args, **kwargs):
        raise AssertionError("producer ran during authority admission or replay")

    monkeypatch.setattr(check_executor.CheckExecutor, "execute", forbidden)
    after = admit(history, result, draft)
    state = after.protocol_replay.data
    assert state["records"]["authority-assessment:0"]["record"][
        "assessment_outcome"
    ] == ("SATISFIED" if grantee == "actor:executor" else "VIOLATED")
    assert len(state["state"]["protocol"]["authority_assessments"]) == 1
    assert state["state"]["protocol"]["authorization_states"] == [
        {"keys": ["action:1"], "value": "PENDING"}
    ]
    assert (
        state["state"]["action_acceptance_head"]
        == before.protocol_replay.data["state"]["action_acceptance_head"]
    )
    for field in (
        "change_sets",
        "record_history",
        "acceptance_head",
        "materialization_head",
    ):
        assert getattr(after, field) == getattr(before, field)
    assert after.graph.export_records() == before.graph.export_records()
    assert KnowledgeChangeHistory.reopen(history.path).replay().receipt == after.receipt


@pytest.mark.parametrize("bad_second", [False, True])
def test_real_authority_failure_pair_is_atomic(
    tmp_path, prepared, monkeypatch, bad_second
):
    content, request = prepared["actor:executor"]
    history = reopen(tmp_path, content)
    with monkeypatch.context() as patch:

        def unavailable(*args, **kwargs):
            raise RuntimeError("controlled grant-check failure")

        patch.setattr(check_executor, "execute_program", unavailable)
        result = run_history_check(history, invocation=request)
    draft = event(history, result, request)
    before = history.path.read_bytes()
    if bad_second:
        draft["data"]["assessment_dependencies"]["value"].pop()
        with pytest.raises(
            api().ProtocolProgramRefusal, match="INVALID_AUTHORITY_INTRODUCTION"
        ):
            admit(history, result, draft)
        assert history.path.read_bytes() == before
    else:
        after = admit(history, result, draft)
        records = after.protocol_replay.data["records"]
        assert (
            records["authority-failure:0"]["record"]["failed_assessment_kind"]
            == "AUTHORITY"
        )
        assert (
            records["authority-assessment:0"]["record_type"]
            == "UnavailableAuthorityAssessment"
        )
        assert (
            records["authority-assessment:0"]["record"]["assessment_outcome"]
            == "UNKNOWN"
        )
        assert (
            KnowledgeChangeHistory.reopen(history.path).replay().receipt
            == after.receipt
        )


@pytest.mark.parametrize(
    "fault", ["grant", "actor", "context", "closure", "monitor", "duplicate"]
)
def test_authority_bindings_refuse_before_append(tmp_path, prepared, fault):
    content, request = prepared["actor:executor"]
    history = reopen(tmp_path, content)
    request = deepcopy(request)
    result = run_history_check(history, invocation=request)
    draft = event(history, result, request)
    if fault == "duplicate":
        admit(history, result, draft)
        request["event"]["id"] += ":again"
        request["output_ids"] = {
            k: v + ":again" for k, v in request["output_ids"].items()
        }
        result = run_history_check(history, invocation=request)
        draft = event(history, result, request)
    value = draft["data"]["assessment"]["value"][0]["record"]
    if fault == "grant":
        value["evaluated_authority_grant_hash"] = content_digest("wrong")
    elif fault == "actor":
        value["evaluated_actor_id"] = "actor:wrong"
    elif fault == "context":
        draft["data"]["contents"]["current_context"]["action_acceptance_head"] = (
            content_digest("wrong")
        )
    elif fault == "closure":
        value["input_record_ids"].reverse()
    elif fault == "monitor":
        value["monitor_hash"] = content_digest("wrong")
    value["content_hash"] = record_hash("AuthorityAssessment", value)
    before = history.path.read_bytes()
    with pytest.raises(api().ProtocolProgramRefusal):
        admit(history, result, draft)
    assert history.path.read_bytes() == before

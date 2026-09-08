"""Actual TYPE outputs enter the same history, including real failure pairs."""

from importlib import import_module
import json

import pytest

from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest, record_hash
from research.action_history_contract_freeze.programs import check_executor
from research.action_history_contract_freeze.programs.history_checks import (
    run_history_check,
)
from research.action_history_contract_freeze.programs.initialization_bundle import (
    add_initialization,
)
from research.action_history_contract_freeze.programs.proposal_bundle import (
    add_context_proposal,
)
from research.action_history_contract_freeze.programs.test_history_checks import (
    invocation,
)
from research.action_history_contract_freeze.programs.test_initialization_history import (
    SOURCE_IDS,
    POLICY_IDS,
    reopen,
)
from research.action_history_contract_freeze.programs.test_proposal_history import (
    proposal_prefix,
    pair,
    submit,
)
from research.action_history_contract_freeze.programs.test_registration_history import (
    builder,
    compiled,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import api
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    _evidence_anchor,
)
from research.action_history_contract_freeze.programs.test_registration_history import (
    TIME,
)


@pytest.fixture(scope="module")
def proposed(tmp_path_factory):
    extend = import_module(
        "research.action_history_contract_freeze.programs.assessment_bundle"
    ).add_type_assessment
    bundle = extend(
        add_context_proposal(
            add_initialization(
                builder().build_registration_bundle(compiled().artifact_bytes),
                source_ids=SOURCE_IDS,
                policy_ids=POLICY_IDS,
            )
        )
    )
    directory = tmp_path_factory.mktemp("assessment-prefix")
    content, checkpoint, init_record, sources = proposal_prefix(directory, bundle)
    history = KnowledgeChangeHistory.reopen(directory / "history.jsonl")
    submit(history, pair(history, checkpoint, init_record, sources))
    return history.path.read_bytes()


def event(history, result):
    replay = history.replay()
    records = replay.protocol_replay.data["records"]
    output = result.execution.data["records"]
    assessment = output[-1]["record"]
    policy = records["policy:epistemic"]["record"]
    monitor = records[assessment["monitor_id"]]["record"]
    ids = {
        "proposal": assessment["proposal_id"],
        "action": "action:1",
        "monitor": monitor["id"],
        "policy": policy["id"],
        "contract": "source:selected:record_contract",
        "context": "context:1",
        "static0": monitor["input_artifact_ids"][0],
        "static1": monitor["input_artifact_ids"][1],
    }
    data = {
        "assessment": {"value": [output[-1]]},
        "assessment_dependencies": {"value": assessment["source_record_ids"]},
        "references": {
            name: {
                "id": identifier,
                "record_hash": records[identifier]["record"]["content_hash"],
            }
            for name, identifier in ids.items()
        },
        "original": {"value": json.loads(replay.retained_bytes(ids["context"]))},
    }
    if len(output) == 2:
        data["failure"] = {"value": [output[0]]}
        data["failure_dependencies"] = {
            "value": output[0]["record"]["source_record_ids"]
        }
    return {
        "event_id": assessment["generation_event_id"],
        "event_type": "ASSESSMENT_RECORDED",
        "transaction_time": assessment["generated_at"],
        "actor_id": assessment["responsible_actor_id"],
        "data": data,
        "retained": {},
    }


def admit(history, result, draft):
    variant = "unavailable" if "failure" in draft["data"] else "completed"
    return history.append_protocol_events(
        transaction="type-" + variant,
        events=(draft,),
        expected_head=result.ledger_head,
        expected_count=result.ledger_event_count,
    )


def test_real_assessments_admit_without_rerunning_producers_on_replay(
    tmp_path, proposed, monkeypatch
):
    history = reopen(tmp_path, proposed)
    before = history.replay()
    for ordinal in range(2):
        result = run_history_check(
            history, invocation=invocation(history.replay(), ordinal)
        )
        draft = event(history, result)
        with monkeypatch.context() as patch:

            def forbidden(*args, **kwargs):
                raise AssertionError("producer called during append/replay")

            patch.setattr(check_executor.CheckExecutor, "execute", forbidden)
            after = admit(history, result, draft)
            assert (
                KnowledgeChangeHistory.reopen(history.path).replay().receipt
                == after.receipt
            )
    state = after.protocol_replay.data
    assert len(state["state"]["protocol"]["type_assessments"]) == 2
    assert (
        state["records"]["assessment:0"]["record"]["assessment_outcome"] == "SATISFIED"
    )
    assert (
        state["records"]["assessment:1"]["record"]["assessment_outcome"] == "SATISFIED"
    )
    assert after.graph.export_records() == before.graph.export_records()
    assert after.record_history == before.record_history
    assert after.change_sets == before.change_sets
    assert after.acceptance_head == before.acceptance_head
    assert (
        state["state"]["action_acceptance_head"]
        == before.protocol_replay.data["state"]["action_acceptance_head"]
    )


def test_actual_unavailability_pair_is_atomic_and_replays_after_recovery(
    tmp_path, proposed, monkeypatch
):
    history = reopen(tmp_path, proposed)
    request = invocation(history.replay(), 0)
    with monkeypatch.context() as patch:

        def unavailable(*args, **kwargs):
            raise RuntimeError("controlled engine failure")

        patch.setattr(check_executor, "execute_program", unavailable)
        result = run_history_check(history, invocation=request)
    draft = event(history, result)
    after = admit(history, result, draft)
    records = after.protocol_replay.data["records"]
    assert records["failure:0"]["record_type"] == "MonitorFailure"
    assert records["assessment:0"]["record_type"] == "UnavailableAssessment"
    assert records["assessment:0"]["record"]["assessment_outcome"] == "UNKNOWN"
    assert records["assessment:0"]["record"]["monitor_failure_id"] == "failure:0"
    assert KnowledgeChangeHistory.reopen(history.path).replay().receipt == after.receipt


def test_bad_second_failure_record_discards_the_staged_failure(
    tmp_path, proposed, monkeypatch
):
    history = reopen(tmp_path, proposed)
    with monkeypatch.context() as patch:

        def unavailable(*args, **kwargs):
            raise RuntimeError("controlled engine failure")

        patch.setattr(check_executor, "execute_program", unavailable)
        result = run_history_check(history, invocation=invocation(history.replay(), 0))
    draft = event(history, result)
    assert draft["data"]["assessment_dependencies"]["value"][-1] == "failure:0"
    draft["data"]["assessment_dependencies"]["value"] = draft["data"][
        "assessment_dependencies"
    ]["value"][:-1]
    assert (
        draft["data"]["assessment"]["value"][0]["record"]["source_record_ids"][-1]
        == "failure:0"
    )
    before = history.path.read_bytes()
    with pytest.raises(
        api().ProtocolProgramRefusal, match="INVALID_CHECK_OUTPUT_INTRODUCTION"
    ):
        admit(history, result, draft)
    assert history.path.read_bytes() == before


def test_intervening_history_event_refuses_a_precomputed_check_append(
    tmp_path, proposed
):
    history = reopen(tmp_path, proposed)
    result = run_history_check(history, invocation=invocation(history.replay(), 0))
    draft = event(history, result)
    history.append_anchors(
        anchors=(_evidence_anchor("unrelated:evidence", b"retained test evidence"),),
        transaction_time=TIME,
        actor_id="actor:registrar",
    )
    before = history.path.read_bytes()
    with pytest.raises(api().ProtocolProgramRefusal, match="STALE_PROTOCOL_BASE"):
        admit(history, result, draft)
    assert history.path.read_bytes() == before


@pytest.mark.parametrize(
    "fault", ["hash", "monitor", "proposal", "closure", "context", "duplicate"]
)
def test_misbound_assessment_refuses_atomically(tmp_path, proposed, fault):
    history = reopen(tmp_path, proposed)
    result = run_history_check(history, invocation=invocation(history.replay(), 0))
    draft = event(history, result)
    if fault == "duplicate":
        admit(history, result, draft)
        request = invocation(history.replay(), 0)
        request["event"]["id"] += ":again"
        request["output_ids"] = {
            k: v + ":again" for k, v in request["output_ids"].items()
        }
        result = run_history_check(history, invocation=request)
        draft = event(history, result)
    record = draft["data"]["assessment"]["value"][0]["record"]
    if fault == "monitor":
        record["monitor_hash"] = content_digest("wrong")
    elif fault == "proposal":
        record["proposal_content_hash"] = content_digest("wrong")
    elif fault == "closure":
        record["input_record_ids"].reverse()
    elif fault == "context":
        draft["data"]["original"]["value"]["domain"]["accepted_graph_digest"] = (
            content_digest("wrong")
        )
    record["content_hash"] = record_hash("TypeAssessment", record)
    if fault == "hash":
        record["content_hash"] = content_digest("wrong")
    before = history.path.read_bytes()
    with pytest.raises(api().ProtocolProgramRefusal):
        admit(history, result, draft)
    assert history.path.read_bytes() == before

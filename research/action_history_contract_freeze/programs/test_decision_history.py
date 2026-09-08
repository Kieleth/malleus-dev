"""Policy recomputation and atomic action-only decision in the real Shop log."""

from copy import deepcopy
from importlib import import_module
import json

import pytest

from malleus.accepted import acceptance_result_head
from malleus.assent import make_record
from malleus.compiler import KnowledgeChangeHistory
from malleus.control import evaluate_epistemic_policy
from malleus.ledger import content_digest, record_hash
from research.action_history_contract_freeze.programs import check_executor
from research.action_history_contract_freeze.programs.assessment_bundle import (
    add_type_assessment,
)
from research.action_history_contract_freeze.programs.history_checks import (
    run_history_check,
)
from research.action_history_contract_freeze.programs.initialization_bundle import (
    add_initialization,
)
from research.action_history_contract_freeze.programs.proposal_bundle import (
    add_context_proposal,
)
from research.action_history_contract_freeze.programs.test_assessment_history import (
    admit as admit_assessment,
    event as assessment_event,
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
    TIME,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import api


@pytest.fixture(scope="module")
def proposed(tmp_path_factory):
    extend = import_module(
        "research.action_history_contract_freeze.programs.decision_bundle"
    ).add_epistemic_decision
    bundle = extend(
        add_type_assessment(
            add_context_proposal(
                add_initialization(
                    builder().build_registration_bundle(compiled().artifact_bytes),
                    source_ids=SOURCE_IDS,
                    policy_ids=POLICY_IDS,
                )
            )
        )
    )
    directory = tmp_path_factory.mktemp("decision-prefix")
    return proposed_prefix(directory, bundle)


def proposed_prefix(directory, bundle):
    _, checkpoint, init_record, sources = proposal_prefix(directory, bundle)
    history = KnowledgeChangeHistory.reopen(directory / "history.jsonl")
    submit(history, pair(history, checkpoint, init_record, sources))
    return history.path.read_bytes()


def assess(history, *, unavailable=False):
    for ordinal in range(2):
        with pytest.MonkeyPatch.context() as patch:
            if unavailable and ordinal == 0:

                def fail(*args, **kwargs):
                    raise RuntimeError("controlled TYPE engine failure")

                patch.setattr(check_executor, "execute_program", fail)
            result = run_history_check(
                history, invocation=invocation(history.replay(), ordinal)
            )
        admit_assessment(history, result, assessment_event(history, result))


@pytest.fixture(scope="module")
def assessed(tmp_path_factory, proposed):
    prefixes = {}
    for unavailable in (False, True):
        history = reopen(tmp_path_factory.mktemp("checked-decision-prefix"), proposed)
        assess(history, unavailable=unavailable)
        prefixes[unavailable] = history.path.read_bytes()
    return prefixes


def decision_event(history):
    base = history.replay()
    records = base.protocol_replay.data["records"]
    values = {key: value["record"] for key, value in records.items()}
    proposal, policy = values["proposal:1"], values["policy:epistemic"]
    monitors = [values[i] for i in policy["required_monitor_ids"]]
    outputs = [values["assessment:" + str(i)] for i in range(2)]
    evaluation = evaluate_epistemic_policy(
        policy,
        {m["id"]: m for m in monitors},
        outputs,
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
    )
    header = dict(
        event_id="event:decision:1", generated_at=TIME, actor_id="actor:controller"
    )
    decision = make_record(
        "EpistemicDecision",
        **header,
        id="decision:1",
        role="epistemic-controller",
        source_record_ids=[
            proposal["id"],
            policy["id"],
            policy["ruleset_id"],
            *evaluation.assessment_ids,
        ],
        proposal_id=proposal["id"],
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
    target = {
        "ACCEPT": "ACCEPTED",
        "REJECT": "REJECTED",
        "DEFER": "DEFERRED",
        "CONTEST": "CONTESTED",
    }[evaluation.verdict]
    transition = make_record(
        "TransitionRecord",
        **header,
        id="transition:1",
        role="state-controller",
        source_record_ids=[decision["id"]],
        transition_subject_id=proposal["id"],
        from_state="PROPOSED",
        to_state=target,
        triggering_record_id=decision["id"],
        ledger_event_id=header["event_id"],
        sequence=base.ledger_event_count + 1,
        transition_time=TIME,
    )
    ids = {
        "proposal": proposal["id"],
        "policy": policy["id"],
        "context": "context:1",
        "rules": policy["ruleset_id"],
    }
    data = {
        "references": {
            role: {"id": i, "record_hash": values[i]["content_hash"]}
            for role, i in ids.items()
        },
        "original": {"value": json.loads(base.retained_bytes("context:1"))},
        "control": {
            "recipe": "ASSENT_EPISTEMIC_CONTROL_V1",
            "monitors": monitors,
            "bindings": {
                "proposal_id": proposal["id"],
                "proposal_content_hash": proposal["content_hash"],
                "base_acceptance_head": proposal["base_acceptance_head"],
            },
        },
        "outputs": outputs,
        "decision": {
            "value": [{"record_type": "EpistemicDecision", "record": decision}]
        },
        "transition": {
            "value": [{"record_type": "TransitionRecord", "record": transition}]
        },
        "decision_dependencies": {"value": deepcopy(decision["source_record_ids"])},
        "transition_dependencies": {"value": deepcopy(transition["source_record_ids"])},
    }
    if evaluation.verdict == "ACCEPT":
        data["acceptance_preimage"] = {
            "previous_acceptance_head": proposal["base_acceptance_head"],
            "proposal_content_hash": proposal["content_hash"],
            "decision_content_hash": decision["content_hash"],
            "revision_content_hashes": [],
        }
    return {
        "event_id": header["event_id"],
        "event_type": "EPISTEMIC_DECIDED",
        "transaction_time": TIME,
        "actor_id": header["actor_id"],
        "data": data,
        "retained": {},
    }, evaluation


def decide(history, draft, verdict):
    base = history.replay()
    return history.append_protocol_events(
        transaction="epistemic-" + verdict.lower(),
        events=(draft,),
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
    )


@pytest.mark.parametrize("unavailable", [False, True])
def test_real_policy_result_and_transition_replay_without_producer_or_graph_effect(
    tmp_path,
    assessed,
    unavailable,
    monkeypatch,
):
    history = reopen(tmp_path, assessed[unavailable])
    before = history.replay()
    draft, evaluation = decision_event(history)
    assert evaluation.verdict == ("DEFER" if unavailable else "ACCEPT")

    def forbidden(*args, **kwargs):
        raise AssertionError("check producer ran inside decision or replay")

    monkeypatch.setattr(check_executor.CheckExecutor, "execute", forbidden)
    after = decide(history, draft, evaluation.verdict)
    assert KnowledgeChangeHistory.reopen(history.path).replay().receipt == after.receipt
    state = after.protocol_replay.data["state"]
    assert state["protocol"]["proposal_states"] == [
        {"keys": ["proposal:1"], "value": "DEFERRED" if unavailable else "ACCEPTED"}
    ]
    assert state["protocol"]["authorization_states"] == [
        {"keys": ["action:1"], "value": "PENDING"}
    ]
    assert state["protocol"]["epistemic_decisions"] == [
        {"keys": ["proposal:1"], "value": "decision:1"}
    ]
    prior_head = before.protocol_replay.data["state"]["action_acceptance_head"]
    expected = (
        prior_head
        if unavailable
        else acceptance_result_head(**draft["data"]["acceptance_preimage"])
    )
    assert state["action_acceptance_head"] == expected
    assert (expected == prior_head) is unavailable
    for field in (
        "acceptance_head",
        "materialization_head",
        "change_sets",
        "contract_revisions",
        "record_history",
    ):
        assert getattr(after, field) == getattr(before, field)
    assert after.graph.export_records() == before.graph.export_records()


@pytest.mark.parametrize(
    "fault",
    [
        "verdict",
        "evaluation",
        "output",
        "order",
        "policy",
        "head",
        "transition",
        "transition_time",
        "dependencies",
        "duplicate",
    ],
)
def test_decision_binding_and_late_transition_refuse_without_partial_append(
    tmp_path, assessed, fault
):
    history = reopen(tmp_path, assessed[False])
    draft, evaluation = decision_event(history)
    decision = draft["data"]["decision"]["value"][0]["record"]
    transition = draft["data"]["transition"]["value"][0]["record"]
    selected_verdict = evaluation.verdict
    if fault == "verdict":
        decision["epistemic_verdict"] = "REJECT"
        transition["to_state"] = "REJECTED"
        selected_verdict = "REJECT"
        del draft["data"]["acceptance_preimage"]
    elif fault == "evaluation":
        decision["policy_evaluation_hash"] = content_digest("forged")
    elif fault == "output":
        draft["data"]["outputs"][0]["assessment_outcome"] = "VIOLATED"
    elif fault == "order":
        decision["assessment_ids"].reverse()
    elif fault == "policy":
        decision["policy_hash"] = content_digest("wrong")
    elif fault == "head":
        draft["data"]["acceptance_preimage"]["previous_acceptance_head"] = (
            content_digest("wrong")
        )
    elif fault == "transition":
        transition["sequence"] += 1
    elif fault == "transition_time":
        transition["transition_time"] = "2026-09-07T01:00:00+01:00"
    elif fault == "dependencies":
        draft["data"]["transition_dependencies"]["value"] = []
    elif fault == "duplicate":
        decide(history, draft, evaluation.verdict)
        draft["event_id"] += ":again"
        decision["generation_event_id"] = draft["event_id"]
        transition["generation_event_id"] = draft["event_id"]
    decision["content_hash"] = record_hash("EpistemicDecision", decision)
    transition["content_hash"] = record_hash("TransitionRecord", transition)
    if "acceptance_preimage" in draft["data"]:
        draft["data"]["acceptance_preimage"]["decision_content_hash"] = decision[
            "content_hash"
        ]
    before = history.path.read_bytes()
    reasons = {
        "verdict": "FORGED_EPISTEMIC_VERDICT",
        "evaluation": "FORGED_EVALUATION_IDENTITY",
        "output": "FORGED_CONTROL_OUTPUT",
        "order": "WRONG_POLICY_ASSESSMENT_ORDER",
        "policy": "MISBOUND_DECISION",
        "head": "WRONG_ACTION_ACCEPTANCE_PREIMAGE",
        "transition": "MISBOUND_DECISION_TRANSITION",
        "transition_time": "MISBOUND_DECISION_TRANSITION",
        "dependencies": "INVALID_DECISION_INTRODUCTION",
        "duplicate": "STALE_ACTION_HEAD",
    }
    with pytest.raises(api().ProtocolProgramRefusal, match=reasons[fault]):
        decide(history, draft, selected_verdict)
    assert history.path.read_bytes() == before

"""Authorization is recomputed from real retained judgments, never KG presence."""

from research.action_history_contract_freeze.programs.fixture_episode import FIRST

from copy import deepcopy
from importlib import import_module

import pytest

from malleus.assent import make_record
from malleus.control import evaluate_authorization_policy
from malleus.ledger import content_digest, record_hash
from malleus.compiler import KnowledgeChangeHistory
from research.action_history_contract_freeze.programs import check_executor
from research.action_history_contract_freeze.programs import (
    test_authority_history as authority,
)
from research.action_history_contract_freeze.programs.authority_bundle import (
    add_authority_assessment,
)
from research.action_history_contract_freeze.programs.history_checks import (
    run_history_check,
)
from research.action_history_contract_freeze.programs.test_initialization_history import (
    reopen,
    SOURCE_IDS,
    POLICY_IDS,
)
from research.action_history_contract_freeze.programs.test_registration_history import (
    TIME,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import api


def build_bundle():
    extend = import_module(
        "research.action_history_contract_freeze.programs.authorization_bundle"
    ).add_authorization
    d = authority.decisions
    return extend(
        add_authority_assessment(
            authority.add_current_context(
                authority.add_epistemic_decision(
                    d.add_type_assessment(
                        d.add_context_proposal(
                            d.add_initialization(
                                d.builder().build_registration_bundle(
                                    d.compiled().artifact_bytes
                                ),
                                source_ids=SOURCE_IDS,
                                policy_ids=POLICY_IDS,
                            )
                        )
                    )
                )
            )
        )
    )


def assessed_prefix(directory, content, verdict):
    history = reopen(directory, content)
    request = authority.current.grant_inputs(
        history, grantee="actor:other" if verdict == "BLOCK" else "actor:executor"
    )
    first_request = deepcopy(request)
    for ordinal in range(2):
        replay = history.replay()
        records = replay.protocol_replay.data["records"]
        monitor_id = records["policy:authorization"]["record"]["required_monitor_ids"][
            ordinal
        ]
        request["monitor"] = {
            "id": monitor_id,
            "record_hash": records[monitor_id]["record"]["content_hash"],
        }
        request["event"]["id"] = "event:authority-assessment:" + str(ordinal)
        request["output_ids"] = {
            "assessment": "authority-assessment:" + str(ordinal),
            "failure": "authority-failure:" + str(ordinal),
        }
        with pytest.MonkeyPatch.context() as patch:
            if verdict == "CLARIFY" and ordinal == 0:

                def unavailable(*args, **kwargs):
                    raise RuntimeError("controlled authority engine failure")

                patch.setattr(check_executor, "execute_program", unavailable)
            result = run_history_check(history, invocation=request)
        authority.admit(history, result, authority.event(history, result, request))
    return history.path.read_bytes(), first_request


@pytest.fixture(scope="module")
def assessed(tmp_path_factory):
    content = authority.current.accepted_prefix(
        tmp_path_factory.mktemp("authorization-base"), build_bundle()
    )
    return {
        verdict: assessed_prefix(
            tmp_path_factory.mktemp("authorization-inputs"), content, verdict
        )
        for verdict in ("AUTHORIZE", "BLOCK", "CLARIFY")
    }


def event(history, request, episode=FIRST):
    replay = history.replay()
    values = {
        key: item["record"]
        for key, item in replay.protocol_replay.data["records"].items()
    }
    policy, action, proposal = (
        values["policy:authorization"],
        values[episode.id("action:1")],
        values[episode.id("proposal:1")],
    )
    outputs = [values[episode.id("authority-assessment:" + str(i))] for i in range(2)]
    monitors = [values[i] for i in policy["required_monitor_ids"]]
    head = replay.protocol_replay.data["state"]["action_acceptance_head"]
    evaluated = evaluate_authorization_policy(
        policy,
        {m["id"]: m for m in monitors},
        outputs,
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        action_id=action["id"],
        action_content_hash=action["content_hash"],
        evaluated_actor_id="actor:executor",
        base_acceptance_head=head,
    )
    sources = [
        action["id"],
        policy["id"],
        episode.id("decision:1"),
        *evaluated.assessment_ids,
        episode.id("grant:direct"),
    ]
    header = dict(
        event_id=episode.id("event:authorization"),
        generated_at=episode.time(TIME),
        actor_id="actor:authorizer",
    )
    decision = make_record(
        "AuthorizationDecision",
        **header,
        id=episode.id("authorization:1"),
        role="authorizer",
        source_record_ids=sources,
        base_acceptance_head=head,
        policy_id=policy["id"],
        policy_hash=policy["content_hash"],
        rationale_codes=["POLICY_RESULT"],
        rationale="The retained policy computes permission.",
        action_proposal_id=action["id"],
        action_content_hash=action["content_hash"],
        authorization_verdict=evaluated.verdict,
        epistemic_decision_ids=[episode.id("decision:1")],
        relied_on_claim_version_ids=[],
        authority_assessment_ids=list(evaluated.assessment_ids),
        triggered_assessment_ids=list(evaluated.triggered_assessment_ids),
        policy_evaluation_hash=evaluated.evaluation_hash,
        authority_grant_id=episode.id("grant:direct"),
        authority_grant_hash=values[episode.id("grant:direct")]["content_hash"],
        authorized_actor_id="actor:executor",
        authorization_valid_from=episode.time(TIME)
        if evaluated.verdict == "AUTHORIZE"
        else None,
        authorization_valid_to=episode.time("2026-09-07T01:00:00Z")
        if evaluated.verdict == "AUTHORIZE"
        else None,
    )
    transition = make_record(
        "TransitionRecord",
        **header,
        id=episode.id("authorization-transition:1"),
        role="state-controller",
        source_record_ids=[decision["id"]],
        transition_subject_id=action["id"],
        from_state="PENDING",
        to_state={
            "AUTHORIZE": "AUTHORIZED",
            "BLOCK": "BLOCKED",
            "CLARIFY": "CLARIFICATION_REQUIRED",
        }[evaluated.verdict],
        triggering_record_id=decision["id"],
        ledger_event_id=header["event_id"],
        sequence=replay.ledger_event_count + 1,
        transition_time=episode.time(TIME),
    )

    data = authority.context_data(history, request, episode=episode)
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
                "evaluated_actor_id": "actor:executor",
                "authority_policy_id": policy["id"],
                "authority_policy_hash": policy["content_hash"],
            },
        },
        decision={
            "value": [{"record_type": "AuthorizationDecision", "record": decision}]
        },
        transition={
            "value": [{"record_type": "TransitionRecord", "record": transition}]
        },
        decision_dependencies={"value": deepcopy(sources)},
        transition_dependencies={"value": [decision["id"]]},
    )
    if evaluated.verdict == "AUTHORIZE":
        data["intervals"] = {
            "authorization": {
                "start": decision["authorization_valid_from"],
                "end": decision["authorization_valid_to"],
            },
            "grant": {
                "start": values[episode.id("grant:direct")]["grant_valid_from"],
                "end": values[episode.id("grant:direct")]["grant_valid_to"],
            },
        }
    return {
        "event_id": header["event_id"],
        "event_type": "AUTHORIZATION_DECIDED",
        "transaction_time": episode.time(TIME),
        "actor_id": header["actor_id"],
        "data": data,
        "retained": {},
    }, evaluated


def authorize(history, draft, verdict):
    base = history.replay()
    return history.append_protocol_events(
        transaction="authorization-" + verdict.lower(),
        events=(draft,),
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
    )


@pytest.mark.parametrize("verdict", ["AUTHORIZE", "BLOCK", "CLARIFY"])
def test_actual_policy_outcomes_advance_permission_only_and_reopen(
    tmp_path, assessed, verdict, monkeypatch
):
    content, request = assessed[verdict]
    history = reopen(tmp_path, content)
    before = history.replay()
    draft, evaluation = event(history, request)
    assert evaluation.verdict == verdict

    def forbidden(*args, **kwargs):
        raise AssertionError("producer ran in authorization/replay")

    monkeypatch.setattr(check_executor.CheckExecutor, "execute", forbidden)
    after = authorize(history, draft, verdict)
    target = {
        "AUTHORIZE": "AUTHORIZED",
        "BLOCK": "BLOCKED",
        "CLARIFY": "CLARIFICATION_REQUIRED",
    }[verdict]
    assert after.protocol_replay.data["state"]["protocol"]["authorization_states"] == [
        {"keys": ["action:1"], "value": target}
    ]
    assert after.protocol_replay.data["state"]["protocol"][
        "authorization_decisions"
    ] == [{"keys": ["action:1"], "value": "authorization:1"}]
    assert (
        after.protocol_replay.data["state"]["action_acceptance_head"]
        == before.protocol_replay.data["state"]["action_acceptance_head"]
    )
    assert after.graph.export_records() == before.graph.export_records()
    assert after.change_sets == before.change_sets
    assert after.acceptance_head == before.acceptance_head
    assert KnowledgeChangeHistory.reopen(history.path).replay().receipt == after.receipt


@pytest.mark.parametrize(
    "fault",
    [
        "verdict",
        "output",
        "evaluation",
        "order",
        "grant",
        "actor",
        "interval",
        "transition",
        "dependencies",
    ],
)
def test_forged_permission_and_invalid_transition_refuse_atomically(
    tmp_path, assessed, fault
):
    content, request = assessed["BLOCK" if fault == "verdict" else "AUTHORIZE"]
    history = reopen(tmp_path, content)
    draft, evaluated = event(history, request)
    data = draft["data"]
    decision = data["decision"]["value"][0]["record"]
    transition = data["transition"]["value"][0]["record"]
    variant = evaluated.verdict
    if fault == "verdict":
        variant = "AUTHORIZE"
        decision.update(
            authorization_verdict=variant,
            authorization_valid_from=TIME,
            authorization_valid_to="2026-09-07T01:00:00Z",
        )
        transition["to_state"] = "AUTHORIZED"
    elif fault == "output":
        data["outputs"][0]["assessment_outcome"] = "VIOLATED"
    elif fault == "evaluation":
        decision["policy_evaluation_hash"] = content_digest("forged")
    elif fault == "order":
        decision["authority_assessment_ids"].reverse()
    elif fault == "grant":
        decision["authority_grant_hash"] = content_digest("wrong")
    elif fault == "actor":
        decision["authorized_actor_id"] = "actor:other"
    elif fault == "interval":
        decision["authorization_valid_to"] = "2026-09-07T03:00:00Z"
    elif fault == "transition":
        transition["sequence"] += 1
    else:
        data["transition_dependencies"]["value"] = []
    decision["content_hash"] = record_hash("AuthorizationDecision", decision)
    transition["content_hash"] = record_hash("TransitionRecord", transition)
    if variant == "AUTHORIZE":
        grant = history.replay().protocol_replay.data["records"]["grant:direct"][
            "record"
        ]
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
    before = history.path.read_bytes()
    reasons = {
        "verdict": "FORGED_AUTHORIZATION_VERDICT",
        "output": "FORGED_AUTHORIZATION_OUTPUT",
        "evaluation": "FORGED_AUTHORIZATION_EVALUATION",
        "order": "WRONG_AUTHORIZATION_ASSESSMENT_ORDER",
        "grant": "MISBOUND_AUTHORIZATION_DECISION",
        "actor": "MISBOUND_AUTHORIZATION_DECISION",
        "interval": "AUTHORIZATION_EXCEEDS_GRANT",
        "transition": "MISBOUND_AUTHORIZATION_TRANSITION",
        "dependencies": "INVALID_AUTHORIZATION_INTRODUCTION",
    }
    with pytest.raises(api().ProtocolProgramRefusal, match=reasons[fault]):
        authorize(history, draft, variant)
    assert history.path.read_bytes() == before


def test_reused_authority_prefix_has_no_effects_or_control(assessed, tmp_path):
    import json

    history = reopen(tmp_path, assessed["AUTHORIZE"][0])
    identity = history.replay().protocol_replay.data["bundle_identity"]
    bundle = next(
        json.loads(item.content)
        for item in history.replay().retained_inputs
        if item.identity == identity
    )
    steps = bundle["transactions"]["authority-completed"]["program"]["steps"]
    boundary = next(
        i for i, step in enumerate(steps) if step["opcode"] == "VALIDATE_RECORD"
    )
    assert boundary > 0
    assert {step["opcode"] for step in steps[:boundary]} <= {
        "RESOLVE_RECORD",
        "HASH",
        "REQUIRE_COMPARE",
        "REQUIRE_MEMBER",
    }
    constants = bundle["constants"]
    assert "authorization" in constants
    assert "authorization_decision" in constants
    for transaction in bundle["transactions"].values():
        schema = transaction["program"]["inputs"]["artifact"]["constants"][
            "properties"
        ]["value"]
        assert len(schema["required"]) == len(set(schema["required"]))

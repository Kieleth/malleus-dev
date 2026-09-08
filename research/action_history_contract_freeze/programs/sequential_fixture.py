"""Reference conformance driver. Effects and observations are synthetic inputs.

Every admission uses the real owner, actual retained records, real TYPE/direct
grant checks and policy evaluators. No producer runs during replay. The Shop
correction is independent, not evidence that either synthetic action succeeded.
"""

from copy import deepcopy
import sys

import pytest

from malleus.compiler import KnowledgeChangeHistory, PolicyProgram
from malleus.ledger import content_digest, record_hash
from research.action_history_contract_freeze.programs import (
    test_assessment_history as assessments,
    test_authorization_history as authorization,
    test_decision_history as decisions,
    test_dispatch_history as dispatching,
    test_execution_history as executions,
    test_initialization_history as initialization,
    test_observation_history as observations,
    test_proposal_history as proposals,
)
from research.action_history_contract_freeze.programs.dispatch_bundle import (
    add_dispatch,
)
from research.action_history_contract_freeze.programs.execution_bundle import (
    add_execution,
)
from research.action_history_contract_freeze.programs.fixture_episode import (
    FIRST,
    FixtureEpisode,
)
from research.action_history_contract_freeze.programs.history_checks import (
    run_history_check,
)
from research.action_history_contract_freeze.programs.observation_bundle import (
    add_observation,
)
from research.action_history_contract_freeze.programs.sequential_bundle import (
    add_sequential_actions,
)
from research.action_history_contract_freeze.programs.test_history_checks import (
    invocation,
)
from research.action_history_contract_freeze.programs.test_registration_history import (
    append,
    draft,
)
from research.action_history_contract_freeze.programs.test_shop_action_composition import (
    shop,
    shop_through_e4,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import canonical


def proposal(history, metadata, episode, *, bad_payload=False):
    content = canonical(
        {"operation": "SYNTHETIC_CONFORMANCE", "episode": episode.label}
    )
    payload = proposals.source(
        episode.id("source:action-payload"), content, [], episode=episode
    )
    append(
        history,
        "source",
        draft(
            "SourceArtifact",
            payload,
            preimage=proposals.preimage(payload),
            content=content,
        ),
    )
    first, second = proposals.pair(
        history,
        metadata["checkpoint"],
        metadata["initialization"],
        metadata["sources"],
        suffix=episode.id("1"),
        episode=episode,
    )
    action = second["data"]["action"]["value"][0]["record"]
    action["action_payload_hash"] = (
        content_digest("wrong payload")
        if bad_payload
        else payload["source_content_digest"]
    )
    action["source_record_ids"].append(payload["id"])
    action["content_hash"] = record_hash("LocalAction", action)
    value = second["data"]["proposal"]["value"][0]["record"]
    value["member_content_hashes"] = [action["content_hash"]]
    value["content_hash"] = record_hash("ProposedSubgraph", value)
    second["data"]["payload"] = {
        "id": payload["id"],
        "record_hash": payload["content_hash"],
    }
    return first, second


def authorize_episode(history, episode, checkpoints):
    saved = {}
    for ordinal in range(2):
        result = run_history_check(
            history, invocation=invocation(history.replay(), ordinal, episode=episode)
        )
        event = assessments.event(history, result, episode=episode)
        assessments.admit(history, result, event)
        saved["type"] = ("type-completed", deepcopy(event))
    event, evaluated = decisions.decision_event(history, episode=episode)
    decisions.decide(history, event, evaluated.verdict)
    request = authorization.authority.current.grant_inputs(
        history, grantee="actor:executor", episode=episode
    )
    for ordinal in range(2):
        records = history.replay().protocol_replay.data["records"]
        monitor_id = records["policy:authorization"]["record"]["required_monitor_ids"][
            ordinal
        ]
        request["monitor"] = {
            "id": monitor_id,
            "record_hash": records[monitor_id]["record"]["content_hash"],
        }
        request["event"]["id"] = episode.id(
            "event:authority-assessment:" + str(ordinal)
        )
        request["output_ids"] = {
            "assessment": episode.id("authority-assessment:" + str(ordinal)),
            "failure": episode.id("authority-failure:" + str(ordinal)),
        }
        result = run_history_check(history, invocation=request)
        event = authorization.authority.event(history, result, request, episode=episode)
        authorization.authority.admit(history, result, event)
        saved["authority"] = ("authority-completed", deepcopy(event))
    checkpoints[episode.label + ":before-authorization"] = history.path.read_bytes()
    event, evaluated = authorization.event(history, request, episode=episode)
    authorization.authorize(history, event, evaluated.verdict)
    saved["authorization"] = ("authorization-authorize", deepcopy(event))
    return saved


def finish_episode(history, episode, states):
    saved = {}
    event = dispatching.event(history, episode=episode)
    dispatching.dispatch(history, event)
    saved["dispatch"] = ("dispatch", deepcopy(event))
    executions.execute(history, executions.event(history, episode=episode))
    states["first_executed" if episode == FIRST else "second_executed"] = (
        history.path.read_bytes()
    )
    observations.observer_inputs(history, episode=episode)
    event = observations.event(history, episode=episode)
    append(history, "observation", event)
    saved["observation"] = ("observation", deepcopy(event))
    return saved


def correct(history, *, when="2026-09-07T00:35:00Z"):
    return shop._admit_plan(
        history,
        PolicyProgram.from_bytes(shop.POLICY_PATH.read_bytes()),
        shop.PLAN_PATHS[-1],
        when,
    )


def run_sequence(directory, *, base_bundle=None):
    if base_bundle is None:
        base_bundle = add_observation(
            add_execution(add_dispatch(authorization.build_bundle()))
        )
    bundle = add_sequential_actions(base_bundle)
    with pytest.MonkeyPatch.context() as patch:
        # Only choose the real starting Shop fixture, never a runtime/check patch.
        patch.setattr(initialization, "run_full_shop", shop_through_e4)
        _, checkpoint, initial, sources = proposals.proposal_prefix(directory, bundle)
    history = KnowledgeChangeHistory.reopen(directory / "history.jsonl")
    metadata = {
        "checkpoint": checkpoint,
        "initialization": initial,
        "sources": sources,
        "path": history.path,
    }
    states = {}
    for episode in (FIRST, FixtureEpisode("2", 60)):
        proposals.submit(history, proposal(history, metadata, episode))
        if episode != FIRST:
            states["second_proposed"] = history.path.read_bytes()
        saved = authorize_episode(history, episode, states)
        states[episode.label + ":authorized"] = history.path.read_bytes()
        saved.update(finish_episode(history, episode, states))
        if episode == FIRST:
            states["first_observed"] = history.path.read_bytes()
            metadata["first_events"] = saved
            metadata["corrected_graph"] = correct(history).graph.state_digest()
            states["corrected"] = history.path.read_bytes()
    return sys.modules[__name__], states, metadata

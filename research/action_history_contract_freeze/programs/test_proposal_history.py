"""The actual finite context/proposal pair in the populated owning history.

LocalAction is a protocol conformance specimen, not supplier action semantics.
"""

from research.action_history_contract_freeze.programs.fixture_episode import FIRST

from copy import deepcopy
from importlib import import_module

import pytest

from malleus.assent import make_record
from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest, record_hash
from research.action_history_contract_freeze.programs.action_inputs import (
    context_proposal,
    source_event,
)
from research.action_history_contract_freeze.programs.initialization_bundle import (
    add_initialization,
)
from research.action_history_contract_freeze.programs.test_initialization_history import (
    SOURCE_IDS,
    POLICY_IDS,
    initialization_prefix,
    event as initialization_event,
    reopen,
)
from research.action_history_contract_freeze.programs.test_registration_history import (
    TIME,
    append,
    builder,
    compiled,
    draft,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import api, canonical


@pytest.fixture(scope="module")
def inputs(tmp_path_factory):
    extend = import_module(
        "research.action_history_contract_freeze.programs.proposal_bundle"
    ).add_context_proposal
    bundle = extend(
        add_initialization(
            builder().build_registration_bundle(compiled().artifact_bytes),
            source_ids=SOURCE_IDS,
            policy_ids=POLICY_IDS,
        )
    )
    return proposal_prefix(tmp_path_factory.mktemp("proposal-prefix"), bundle)


def proposal_prefix(directory, bundle):
    content, checkpoint, references = initialization_prefix(directory, bundle)
    history = KnowledgeChangeHistory.reopen(directory / "history.jsonl")
    init = initialization_event(checkpoint, references)
    append(history, "initialize", init)
    sources = {}
    for name, data in {
        "goal": {"target": "neutral protocol conformance only"},
        "preservation": {"accepted_knowledge": "UNCHANGED"},
        "mapping": {"effect": "NONE"},
        "pre_state_source": {"fixture": "populated Shop, no supplier amendment"},
    }.items():
        value = source("source:" + name, canonical(data), [])
        append(
            history,
            "source",
            draft(
                "SourceArtifact",
                value,
                preimage=preimage(value),
                content=canonical(data),
            ),
        )
        sources[name] = value
    init_record = init["data"]["records"]["value"][0]["record"]
    return history.path.read_bytes(), checkpoint, init_record, sources


def preimage(value):
    return {k: value[v] for k, v in builder().SOURCE_PROJECTION.items()}


def source(identifier, content, sources, episode=FIRST):
    event = source_event(
        identifier,
        content,
        source_record_ids=sources,
        event_id="event:" + identifier,
        transaction_time=episode.time(TIME),
        actor_id="actor:registrar",
        role="registrar",
        artifact_version="v1",
        media_type="application/json",
        locator="urn:retained:" + identifier,
    )
    return event["data"]["records"]["value"][0]["record"]


def pair(history, checkpoint, init_record, sources, *, suffix="1", episode=FIRST):
    context_id, proposal_id = "context:" + suffix, "proposal:" + suffix
    action = make_record(
        "LocalAction",
        id="action:" + suffix,
        event_id="event:" + proposal_id,
        generated_at=episode.time(TIME),
        actor_id="actor:proposer",
        role="proposer",
        source_record_ids=[context_id, POLICY_IDS["authorization"]],
        action_type="LOCAL_ACTION",
        action_payload_hash=content_digest("shape only"),
        action_key="independent-action-key:" + suffix,
        revision=1,
        authorization_policy_id=POLICY_IDS["authorization"],
        authorization_policy_hash=checkpoint["authorization_policy"]["record_hash"],
    )
    return context_proposal(
        history,
        initialization_id=init_record["id"],
        source_ids={k: v["id"] for k, v in sources.items()},
        context_id=context_id,
        context_metadata={
            "event_id": "event:" + context_id,
            "transaction_time": episode.time(TIME),
            "actor_id": "actor:registrar",
            "role": "registrar",
            "artifact_version": "v1",
            "media_type": "application/json",
            "locator": "urn:retained:" + context_id,
        },
        action={"record_type": "LocalAction", "record": action},
        proposal_id=proposal_id,
        proposal_key="independent-proposal-key:" + suffix,
        episode_key="episode:independent",
        payload_source_id=None,
    )


def submit(history, events):
    base = history.replay()
    return history.append_protocol_events(
        transaction="context-proposal",
        events=events,
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
    )


def test_context_and_real_proposal_commit_together_and_reopen(tmp_path, inputs):
    content, checkpoint, init_record, sources = inputs
    history = reopen(tmp_path, content)
    before = history.replay()
    events = pair(history, checkpoint, init_record, sources)
    after = submit(history, events)
    assert after.ledger_event_count == before.ledger_event_count + 2
    assert (
        after.retained_bytes("context:1") == events[0]["retained"]["source"]["content"]
    )
    protocol = after.protocol_replay.data
    assert set(protocol["records"]) - set(before.protocol_replay.data["records"]) == {
        "context:1",
        "action:1",
        "proposal:1",
    }
    indexes = protocol["state"]["protocol"]
    assert indexes["context_by_proposal"] == [
        {"keys": ["proposal:1"], "value": "context:1"}
    ]
    assert indexes["proposal_states"] == [{"keys": ["proposal:1"], "value": "PROPOSED"}]
    assert indexes["authorization_states"] == [
        {"keys": ["action:1"], "value": "PENDING"}
    ]
    assert (
        protocol["state"]["action_acceptance_head"]
        == before.protocol_replay.data["state"]["action_acceptance_head"]
    )
    assert after.graph.export_records() == before.graph.export_records()
    assert after.record_history == before.record_history
    assert after.change_sets == before.change_sets
    assert after.acceptance_head == before.acceptance_head
    assert KnowledgeChangeHistory.reopen(history.path).replay().receipt == after.receipt


@pytest.mark.parametrize(
    "fault",
    [
        "missing-second",
        "bad-proposal",
        "stale-prefix",
        "stale-domain",
        "stale-action",
        "wrong-initialization",
        "forged-checkpoint",
        "missing-source",
        "wrong-source-digest",
        "context-artifact-hash",
        "policy",
        "duplicate-action-key",
    ],
)
def test_proposal_failure_preserves_exact_history(tmp_path, inputs, fault):
    content, checkpoint, init_record, sources = deepcopy(inputs)
    history = reopen(tmp_path, content)
    if fault == "duplicate-action-key":
        submit(history, pair(history, checkpoint, init_record, sources))
    events = pair(history, checkpoint, init_record, sources, suffix="2")
    original = events[0]["retained"]["source"]
    import json

    context = json.loads(original["content"])
    if fault == "missing-second":
        events = events[:1]
    elif fault == "bad-proposal":
        events[1]["data"]["proposal"]["value"][0]["record"]["member_content_hashes"] = [
            content_digest("wrong")
        ]
    elif fault == "stale-prefix":
        context["prefix"]["event_count"] -= 1
    elif fault == "stale-domain":
        context["domain"]["accepted_graph_digest"] = content_digest("wrong")
    elif fault == "stale-action":
        context["action_acceptance_head"] = content_digest("wrong")
    elif fault == "wrong-initialization":
        context["initialization_identity"] = content_digest("wrong")
    elif fault == "forged-checkpoint":
        events[0]["data"]["initialization"]["value"]["id"] = "forged"
    elif fault == "missing-source":
        events[0]["data"]["references"]["goal"]["record_hash"] = content_digest("wrong")
    elif fault == "wrong-source-digest":
        context["goal"]["bytes_sha256"] = content_digest("wrong")
    elif fault == "policy":
        context["epistemic_policy"]["id"] = "wrong-policy"
    elif fault == "duplicate-action-key":
        events[1]["data"]["action"]["value"][0]["record"]["action_key"] = (
            "independent-action-key:1"
        )
    original["content"] = canonical(context)
    first_record = events[0]["data"]["records"]["value"][0]["record"]
    replacement = source(
        first_record["id"], original["content"], first_record["source_record_ids"]
    )
    if fault == "context-artifact-hash":
        replacement["artifact_hash"] = content_digest("wrong")
        replacement["content_hash"] = record_hash("SourceArtifact", replacement)
    events[0]["data"]["records"]["value"][0]["record"] = replacement
    events[0]["data"]["preimage"]["value"] = preimage(replacement)
    for wrapper in events[-1]["data"].values():
        if (
            type(wrapper) is dict
            and "value" in wrapper
            and type(wrapper["value"]) is list
        ):
            for item in wrapper["value"]:
                if type(item) is dict and "record_type" in item:
                    item["record"]["content_hash"] = record_hash(
                        item["record_type"], item["record"]
                    )
    if fault == "duplicate-action-key":
        proposal = events[1]["data"]["proposal"]["value"][0]["record"]
        proposal["member_content_hashes"] = [
            events[1]["data"]["action"]["value"][0]["record"]["content_hash"]
        ]
        proposal["content_hash"] = record_hash("ProposedSubgraph", proposal)
    before = history.path.read_bytes()
    reasons = {
        "missing-second": "PROTOCOL_PROGRAM_REFUSAL",
        "bad-proposal": "WRONG_MEMBER_HASH",
        "stale-prefix": "STALE_FULL_COUNT",
        "stale-domain": "STALE_GRAPH",
        "stale-action": "STALE_ACTION_HEAD",
        "wrong-initialization": "WRONG_INITIALIZATION",
        "forged-checkpoint": "UNAPPLIED_INITIALIZATION_CONTENT",
        "missing-source": "UNAPPLIED_CONTEXT_SOURCE",
        "wrong-source-digest": "MISBOUND_CONTEXT_SOURCE_BYTES",
        "context-artifact-hash": "SOURCE_SEMANTIC_HASH_MISMATCH",
        "policy": "WRONG_EPIS_POLICY_ID",
        "duplicate-action-key": "DUPLICATE_ACTION_KEY",
    }
    with pytest.raises(api().ProtocolProgramRefusal) as caught:
        submit(history, events)
    assert caught.value.reason == reasons[fault]
    assert history.path.read_bytes() == before

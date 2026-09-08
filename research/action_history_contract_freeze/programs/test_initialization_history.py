"""Initialize the separate action head from a retained, owner-bound checkpoint."""

from copy import deepcopy
from importlib import import_module

import pytest

from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest
from research.action_history_contract_freeze.programs.action_inputs import (
    initialization_checkpoint,
    initialization_event,
    source_event,
)
from research.action_history_contract_freeze.programs.test_registration_history import (
    TIME,
    append,
    builder,
    compiled,
    prerequisites,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import api, canonical
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    _evidence_anchor,
)
from research.ontology_driven_kg_realization.experiments.small_shop.public_population.run import (
    run_full_shop,
)


SOURCE_IDS = {
    k: "source:selected:" + k
    for k in ("profile", "record_contract", "machine", "history_binding")
}
POLICY_IDS = {k: "policy:" + k for k in ("epistemic", "authorization")}


@pytest.fixture(scope="module")
def initialized_inputs(tmp_path_factory):
    # Missing implementation fails before expensive fixture setup in RED.
    build = import_module(
        "research.action_history_contract_freeze.programs.initialization_bundle"
    ).add_initialization
    bundle = build(
        builder().build_registration_bundle(compiled().artifact_bytes),
        source_ids=SOURCE_IDS,
        policy_ids=POLICY_IDS,
    )
    return initialization_prefix(
        tmp_path_factory.mktemp("initialization-prefix"), bundle
    )


def initialization_prefix(directory, bundle):
    run_full_shop(directory)
    history = KnowledgeChangeHistory.reopen(directory / "history.jsonl")
    history.append_anchors(
        anchors=(_evidence_anchor("action-programs", canonical(bundle)),),
        transaction_time=TIME,
        actor_id="actor:test",
    )
    base = history.replay()
    history.select_protocol_programs(
        record_id="action-programs",
        identity=content_digest(bundle),
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
        event_id="event:selection",
        transaction_time=TIME,
        actor_id="actor:registrar",
    )
    prerequisites(history)
    for name, content in {
        "profile": canonical(bundle["profile"]),
        "record_contract": compiled().artifact_bytes,
        "machine": canonical(bundle),
        "history_binding": history.binding.canonical_bytes,
    }.items():
        identifier = SOURCE_IDS[name]
        append(
            history,
            "source",
            source_event(
                identifier,
                content,
                source_record_ids=(),
                event_id="event:" + identifier,
                transaction_time=TIME,
                actor_id="actor:registrar",
                role="registrar",
                artifact_version="v1",
                media_type="application/json",
                locator="urn:retained:" + identifier,
            ),
        )
    checkpoint, references = initialization_checkpoint(
        history,
        record_id="action:initialization",
        source_ids=SOURCE_IDS,
        policy_ids=POLICY_IDS,
    )
    return history.path.read_bytes(), checkpoint, references


def event(checkpoint, references):
    return initialization_event(
        checkpoint,
        references,
        event_id="event:" + checkpoint["id"],
        transaction_time=TIME,
        actor_id="actor:registrar",
        role="registrar",
        artifact_version="v1",
        media_type="application/json",
        locator="urn:retained:" + checkpoint["id"],
    )


def reopen(tmp_path, content):
    path = tmp_path / "history.jsonl"
    path.write_bytes(content)
    return KnowledgeChangeHistory.reopen(path)


def test_initialization_retains_checkpoint_and_derives_only_action_head(
    tmp_path, initialized_inputs
):
    content, checkpoint, references = initialized_inputs
    history = reopen(tmp_path, content)
    before = history.replay()
    after = append(history, "initialize", event(checkpoint, references))
    assert after.ledger_event_count == before.ledger_event_count + 1
    assert after.protocol_replay.data["state"][
        "action_acceptance_head"
    ] == content_digest(checkpoint)
    assert after.retained_bytes(checkpoint["id"]) == canonical(checkpoint)
    assert after.graph.export_records() == before.graph.export_records()
    assert after.change_sets == before.change_sets
    assert after.acceptance_head == before.acceptance_head
    assert after.materialization_head == before.materialization_head
    assert KnowledgeChangeHistory.reopen(history.path).replay().receipt == after.receipt


def test_initialization_preserves_populated_shop_history(tmp_path, initialized_inputs):
    content, checkpoint, references = initialized_inputs
    history = reopen(tmp_path, content)
    before = history.replay()
    assert len(before.change_sets) == 5
    assert len(before.contract_revisions) == 1
    assert before.graph.get_node("supplier-order-state:B:e7")["ordered_quantity"] == 2
    assert (
        before.record_history["supplier-order-state:B:e4"].superseded_by
        == "supplier-order-state:B:e7"
    )
    after = append(history, "initialize", event(checkpoint, references))
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()
    assert after.receipt == reopened.receipt
    assert after.graph.export_records() == before.graph.export_records()
    assert after.record_history == before.record_history
    assert after.change_sets == before.change_sets
    assert after.contract_revisions == before.contract_revisions


@pytest.mark.parametrize(
    "fault", ["prefix", "count", "domain", "definition", "policy", "source", "second"]
)
def test_initialization_misbindings_refuse_without_append(
    tmp_path, initialized_inputs, fault
):
    content, checkpoint, references = deepcopy(initialized_inputs)
    history = reopen(tmp_path, content)
    if fault == "second":
        append(history, "initialize", event(checkpoint, references))
        base = history.replay()
        checkpoint["id"] = "action:second-initialization"
        checkpoint["prefix"] = {
            "head": base.ledger_head,
            "event_count": base.ledger_event_count,
        }
    elif fault == "prefix":
        checkpoint["prefix"]["head"] = content_digest("forged")
    elif fault == "count":
        checkpoint["prefix"]["event_count"] += 1
    elif fault == "domain":
        checkpoint["domain"]["accepted_graph_digest"] = content_digest("forged")
    elif fault == "definition":
        checkpoint["machine"]["bytes_sha256"] = content_digest("forged")
    elif fault == "policy":
        checkpoint["epistemic_policy"]["record_hash"] = content_digest("forged")
    else:
        references["profile"]["record_hash"] = content_digest("forged")
    before = history.path.read_bytes()
    with pytest.raises(api().ProtocolProgramRefusal):
        append(history, "initialize", event(checkpoint, references))
    assert history.path.read_bytes() == before

"""Initialize the separate action head from a retained, owner-bound checkpoint."""

from copy import deepcopy
from importlib import import_module

import pytest

from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest
from malleus.source import source_artifact_fields
from research.action_history_contract_freeze.programs.test_registration_history import (
    TIME,
    append,
    builder,
    compiled,
    draft,
    prerequisites,
    record,
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
    policies = prerequisites(history)
    sources = {}
    for name, content in {
        "profile": canonical(bundle["profile"]),
        "record_contract": compiled().artifact_bytes,
        "machine": canonical(bundle),
        "history_binding": history.binding.canonical_bytes,
    }.items():
        identifier = SOURCE_IDS[name]
        value = record(
            "SourceArtifact",
            identifier,
            [],
            artifact_kind="SOURCE",
            artifact_version="v1",
            **source_artifact_fields(
                artifact_id=identifier,
                artifact_version="v1",
                source_bytes=content,
                media_type="application/json",
                locator="urn:retained:" + identifier,
            ),
        )
        append(
            history,
            "source",
            draft(
                "SourceArtifact",
                value,
                preimage={k: value[v] for k, v in builder().SOURCE_PROJECTION.items()},
                content=content,
            ),
        )
        sources[name] = value
    base = history.replay()
    checkpoint = {
        "schema": "malleus.action-history.initialization/research-v1",
        "id": "action:initialization",
        "prefix": {"head": base.ledger_head, "event_count": base.ledger_event_count},
        "domain": {
            "effective_contract_identity": base.partial_contract.identity,
            "kcs_acceptance_head": base.acceptance_head,
            "materialization_head": base.materialization_head,
            "accepted_graph_digest": base.graph.state_digest(),
        },
        **{
            name: {"id": value["id"], "bytes_sha256": value["source_content_digest"]}
            for name, value in sources.items()
        },
        **{
            name + "_policy": {"id": value["id"], "record_hash": value["content_hash"]}
            for name, value in policies.items()
        },
    }
    references = {
        name: {"id": value["id"], "record_hash": value["content_hash"]}
        for name, value in sources.items()
    }
    return history.path.read_bytes(), checkpoint, references


def event(checkpoint, references):
    content = canonical(checkpoint)
    sources = [v["id"] for v in references.values()] + [
        checkpoint[k + "_policy"]["id"] for k in POLICY_IDS
    ]
    value = record(
        "SourceArtifact",
        checkpoint["id"],
        sources,
        artifact_kind="SOURCE",
        artifact_version="v1",
        **source_artifact_fields(
            artifact_id=checkpoint["id"],
            artifact_version="v1",
            source_bytes=content,
            media_type="application/json",
            locator="urn:retained:" + checkpoint["id"],
        ),
    )
    result = draft(
        "SourceArtifact",
        value,
        preimage={k: value[v] for k, v in builder().SOURCE_PROJECTION.items()},
        content=content,
    )
    result["retained"]["source"]["encoding"] = "CANONICAL_JSON"
    result["data"]["references"] = references
    return result


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

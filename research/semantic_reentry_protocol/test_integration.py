"""Real Core integration for one retained-observation Shop correction.

The caller prepares retention outside synthesis. No prepared KCS enters the
producer, and no action or external-world change is asserted by this slice.
"""

import ast
import builtins
from dataclasses import replace
from importlib import import_module
import io
import json
import os
from pathlib import Path
import shutil

import pytest

import malleus.compiler as api
from research.semantic_reentry_protocol.test_consumer import bundle
from research.semantic_reentry_protocol.test_prerequisites import (
    ACTOR, E4, E7, MAPPING, SOURCE, TIME,
    admit, artifact, canonical, compilation, complement, digest, load_plan,
    prepare, shop,
)


def producer():
    # Import at invocation so missing implementation is executable RED.
    return import_module("research.semantic_reentry_protocol.synthesis")


def bind(history):
    implementation = producer()
    policy = import_module("research.semantic_reentry_protocol.consumer")
    request = bundle(history)
    request["contract"]["synthesizer_identity"] = implementation.SYNTHESIZER_IDENTITY
    replay = history.replay()
    inputs = {
        **{key: value for key, value in request.items() if key != "contract"},
        "contract": policy.ReentryContract.from_bytes(canonical(request["contract"])),
        "context": history.composition_context(),
        "partial_contract": replay.partial_contract,
        "contract_view": replay.contract_view,
        "base_state": api.PopulationBaseState.from_replay(replay),
        "history_profile": api.STATE_VERSION_PROFILE,
    }
    return implementation, policy, request, replay, inputs


def stage(history):
    prepared = prepare(history, load_plan(history, "supplier-e7"))
    assert prepared.change_set is not None
    return prepared, bind(history)


def test_observed_correction_admission_reopen_trace_complement_and_quiescence(shop, tmp_path):
    history, path = shop
    implementation, policy, _, before, initial = bind(history)
    before_retention = path.read_bytes()
    assessment = policy.assess_request(
        contract=initial["contract"], view_bytes=initial["view_bytes"],
        plan_bytes=initial["plan_bytes"], source_bytes=initial["source_bytes"],
        mapping_bytes=initial["mapping_bytes"],
        synthesizer_identity=implementation.SYNTHESIZER_IDENTITY,
    )
    assert assessment.status.value == "READY"
    assert path.read_bytes() == before_retention
    prepared, (_, _, _, retained, inputs) = stage(history)
    before_synthesis = path.read_bytes()
    assert before_synthesis != before_retention
    assert retained.graph.state_digest() == before.graph.state_digest()

    candidates = implementation.synthesize(**inputs)
    assert type(candidates) is tuple and len(candidates) == 1
    candidate = candidates[0]
    assert type(candidate) is api.KnowledgeChangeSet
    assert candidate == prepared.change_set
    assert api.KnowledgeChangeSet.from_bytes(candidate.canonical_bytes) == candidate
    assert path.read_bytes() == before_synthesis
    assert history.replay().graph.state_digest() == before.graph.state_digest()

    final = admit(history, replace(prepared, change_set=candidate))
    isolated = tmp_path / "ledger-only"
    isolated.mkdir()
    copy = isolated / "history.jsonl"
    shutil.copyfile(path, copy)
    reopened_history = api.KnowledgeChangeHistory.reopen(copy)
    reopened = reopened_history.replay()
    assert [member.name for member in isolated.iterdir()] == ["history.jsonl"]
    assert reopened.receipt == final.receipt
    assert complement(reopened) == complement(before)
    query = reopened.graph.query("SupplierOrderState", supplier_order_id="B")
    assert query == [{
        "id": E7, "type": "SupplierOrderState", "supplier_order_id": "B",
        "product_code": "Y", "source_occurrence_id": "e7", "ordered_quantity": 2,
    }]
    assert reopened.record_history[E4].superseded_by == E7
    assert reopened.record_history[E7].supersedes_record_id == E4
    trace = api.trace_population_record(reopened, E7)
    assert trace.change_set == candidate
    assert trace.sources[0].content == before.retained_bytes(SOURCE)
    assert trace.change_set.valid_time == api.KnowledgeValidTime("ORDER_ONLY", "e7")
    assert json.loads(trace.population_plan_bytes)["supersessions"] == [{
        "record_id": E7, "supersedes_record_id": E4}]

    _, _, _, _, satisfied = bind(reopened_history)
    final_bytes = copy.read_bytes()
    assert implementation.synthesize(**satisfied) == ()
    assert copy.read_bytes() == final_bytes
    assert path.read_bytes() == final_bytes
    assert reopened_history.replay().receipt == reopened.receipt
    print("SEMANTIC_REENTRY_INTEGRATION_EVIDENCE=" + canonical({
        "claim": "bounded retained-observation internal knowledge correction",
        "synthesizer_identity": implementation.SYNTHESIZER_IDENTITY,
        "contract_identity": inputs["contract"].identity,
        "change_set_id": candidate.change_set_id,
        "change_set_identity": candidate.identity,
        "base": json.loads(inputs["view_bytes"])["coordinates"],
        "final_receipt_identity": reopened.receipt.identity,
        "final_state_digest": reopened.graph.state_digest(),
        "final_ledger_sha256": digest(final_bytes),
        "query": query,
        "complement_sha256": digest(canonical(complement(reopened))),
        "source_sha256": digest(trace.sources[0].content),
        "mapping_sha256": digest(before.retained_bytes(MAPPING)),
        "traced_plan_sha256": trace.population_plan_identity,
        "no_op_candidates": 0,
    }).decode())


def test_identical_bound_inputs_produce_identical_existing_kcs_bytes(shop):
    history, path = shop
    prepared, (implementation, _, _, _, inputs) = stage(history)
    before = path.read_bytes()
    first = implementation.synthesize(**inputs)
    second = implementation.synthesize(**inputs)
    assert [member.canonical_bytes for member in first] == [prepared.change_set.canonical_bytes]
    assert first == second
    assert path.read_bytes() == before


def test_synthesis_never_uses_ambient_io_writer_or_live_graph_mutation(shop, monkeypatch):
    history, path = shop
    prepared, (implementation, _, _, replay, inputs) = stage(history)
    before = path.read_bytes()
    graph_before = replay.graph.export_records()

    def forbidden(*args, **kwargs):
        raise AssertionError("synthesis accessed ambient IO, writer, or live graph")

    with monkeypatch.context() as blocked:
        for owner, method in ((builtins, "open"), (io, "open"), (os, "open")):
            blocked.setattr(owner, method, forbidden)
        for method in ("open", "read_bytes", "read_text", "write_bytes", "write_text"):
            blocked.setattr(Path, method, forbidden)
        for method in ("replay", "admit", "append_anchors", "compose_change_set",
                       "composition_context"):
            blocked.setattr(api.KnowledgeChangeHistory, method, forbidden)
        graph_type = type(replay.graph)
        for method in ("create_entity", "create_relation", "create_signal",
                       "create_event", "create_event_participation", "set_turn"):
            original = getattr(graph_type, method)

            def guard(receiver, *args, _original=original, **kwargs):
                if receiver is replay.graph:
                    forbidden()
                return _original(receiver, *args, **kwargs)

            blocked.setattr(graph_type, method, guard)
        assert implementation.synthesize(**inputs) == (prepared.change_set,)
    assert replay.graph.export_records() == graph_before
    assert path.read_bytes() == before


def test_pinned_synthesis_needs_retention_but_cannot_perform_it(shop):
    history, path = shop
    implementation, _, _, _, inputs = bind(history)
    before = path.read_bytes()
    with pytest.raises(api.KnowledgeChangeRefusal) as refused:
        implementation.synthesize(**inputs)
    assert refused.value.reason is api.KnowledgeChangeRefusalReason.UNRETAINED_INPUT
    assert path.read_bytes() == before


def test_evidence_only_append_stales_candidate_at_ordinary_admission(shop):
    history, path = shop
    prepared, (implementation, _, _, replay, inputs) = stage(history)
    candidate, = implementation.synthesize(**inputs)
    history.append_anchors(anchors=(artifact("artifact:integration-head-change", b"{}"),),
                           transaction_time=TIME, actor_id=ACTOR)
    before = path.read_bytes()
    assert history.replay().graph.state_digest() == replay.graph.state_digest()
    with pytest.raises(api.KnowledgeChangeRefusal) as refused:
        admit(history, replace(prepared, change_set=candidate))
    assert refused.value.reason is api.KnowledgeChangeRefusalReason.STALE_BASE
    assert path.read_bytes() == before


def test_old_contract_refuses_before_new_state_satisfaction(shop):
    history, path = shop
    prepared, (implementation, policy, _, _, inputs) = stage(history)
    candidate, = implementation.synthesize(**inputs)
    admit(history, replace(prepared, change_set=candidate))
    _, _, _, _, latest = bind(history)
    latest["contract"] = inputs["contract"]
    before = path.read_bytes()
    with pytest.raises(policy.ReentryRefusal) as refused:
        implementation.synthesize(**latest)
    assert refused.value.reason.value == "STALE_BASE"
    assert path.read_bytes() == before


def test_valid_context_from_different_head_cannot_match_old_read_model(shop):
    history, path = shop
    _, (implementation, policy, _, replay, inputs) = stage(history)
    history.append_anchors(anchors=(artifact("artifact:integration-context-change", b"{}"),),
                           transaction_time=TIME, actor_id=ACTOR)
    inputs["context"] = history.composition_context()
    assert history.replay().graph.state_digest() == replay.graph.state_digest()
    before = path.read_bytes()
    with pytest.raises(policy.ReentryRefusal) as refused:
        implementation.synthesize(**inputs)
    assert refused.value.reason.value == "STALE_BASE"
    assert path.read_bytes() == before


@pytest.mark.parametrize("input_name", ["plan_bytes", "source_bytes", "mapping_bytes"])
def test_producer_cannot_bypass_bound_input_identity_checks(shop, input_name):
    history, path = shop
    _, (implementation, policy, _, _, inputs) = stage(history)
    inputs[input_name] += b"\n"
    before = path.read_bytes()
    with pytest.raises(policy.ReentryRefusal) as refused:
        implementation.synthesize(**inputs)
    assert refused.value.reason.value == "INPUT_IDENTITY_MISMATCH"
    assert path.read_bytes() == before


def test_producer_imports_only_public_malleus_facade_and_no_test_helpers():
    implementation = producer()
    tree = ast.parse(Path(implementation.__file__).read_text())
    modules = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)
    assert "malleus.compiler" in modules
    assert all(module == "malleus.compiler" for module in modules
               if module == "malleus" or module.startswith("malleus."))
    assert not any("test_" in module or module.endswith(".run") for module in modules)

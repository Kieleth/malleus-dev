"""Actual Core read closure, not the supplier source/effect E2E."""

from dataclasses import FrozenInstanceError, replace
from importlib import import_module
import json
from pathlib import Path

import pytest

import malleus.compiler as api
from malleus.ledger import content_digest
from research.ontology_driven_kg_realization.experiments.small_shop.public_population.run import (
    run_full_shop,
)
from research.semantic_reentry_external_design.supplier_program import (
    build_supplier_program,
)
from research.semantic_reentry_external_design.test_supplier_action_contract import (
    compile_supplier_action as compile_supplier_action,
)


MODULE = "research.semantic_reentry_external_design.accepted_read_view"
TIME = "2026-09-08T03:00:00Z"
ACTOR = "actor:reentry-read-conformance"


def module():
    return import_module(MODULE)


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


@pytest.fixture(scope="module")
def selected_prefix(tmp_path_factory, action_compilation):
    module()  # RED names the absent adapter before expensive Core setup.
    directory = tmp_path_factory.mktemp("accepted-read-core")
    run_full_shop(directory)
    history = api.KnowledgeChangeHistory.reopen(directory / "history.jsonl")
    # Historical e7 is legitimate here: this is only a read-boundary test.
    unattached = history.path.read_bytes()
    bundle = build_supplier_program(
        action_compilation.artifact.artifact_bytes,
        source_ids={
            k: "source:read:" + k
            for k in ("profile", "record_contract", "machine", "history_binding")
        },
        policy_ids={k: "policy:read:" + k for k in ("epistemic", "authorization")},
    )
    identity = content_digest(json.loads(bundle))
    history.append_anchors(
        anchors=(
            api.structural_evidence_anchor(
                record_id="artifact:read:program",
                content=bundle,
                media_type="application/json",
            ),
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    replay = history.replay()
    history.select_protocol_programs(
        record_id="artifact:read:program",
        identity=identity,
        expected_head=replay.ledger_head,
        expected_count=replay.ledger_event_count,
        event_id="event:read:selection",
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    return history.path.read_bytes(), unattached


@pytest.fixture
def owner(tmp_path, selected_prefix):
    path = tmp_path / "history.jsonl"
    path.write_bytes(selected_prefix[0])
    history = api.KnowledgeChangeHistory.reopen(path)
    return history, history.replay(), history.composition_context()


def freeze(replay, context):
    return module().freeze_accepted_replay(replay=replay, context=context)


def test_real_replay_freezes_without_a_writer_or_graph(owner):
    history, replay, context = owner
    before = history.path.read_bytes()
    view = freeze(replay, context)
    assert view.context == context
    assert view.receipt_identity == replay.receipt.identity
    assert view.records == replay.graph.export_records()
    assert view.protocol == replay.protocol_replay.data
    assert view.receipt == json.loads(replay.receipt.canonical_bytes)
    assert view.contract_view is replay.contract_view
    for name in ("graph", "replay", "history", "path", "admit", "append_anchors"):
        assert not hasattr(view, name)
    assert history.path.read_bytes() == before
    assert freeze(replay, context) == view
    assert (
        Path(api.__file__)
        .resolve()
        .is_relative_to(Path(__file__).resolve().parents[2] / "src")
    )


def test_outputs_are_frozen_and_defensive(owner):
    _, replay, context = owner
    view = freeze(replay, context)
    with pytest.raises((FrozenInstanceError, AttributeError)):
        view.receipt_bytes = b"changed"
    view.records["entities"][0]["properties"].clear()
    view.protocol["state"].clear()
    view.receipt.clear()
    assert view.records == replay.graph.export_records()
    assert view.protocol == replay.protocol_replay.data
    assert view.receipt == json.loads(replay.receipt.canonical_bytes)


@pytest.mark.parametrize(
    "field",
    [
        "base_ledger_head",
        "base_ledger_event_count",
        "base_acceptance_head",
        "base_materialization_head",
        "base_accepted_state_digest",
        "contract_identity",
        "receipt_identity",
    ],
)
def test_every_context_coordinate_is_bound_to_the_actual_replay(owner, field):
    history, replay, context = owner
    before = history.path.read_bytes()
    value = (
        context.base_ledger_event_count + 1
        if field == "base_ledger_event_count"
        else content_digest("wrong")
    )
    with pytest.raises(module().AcceptedViewRefusal) as refused:
        freeze(replay, replace(context, **{field: value}))
    assert refused.value.reason == "STALE_BASE"
    assert history.path.read_bytes() == before


def test_mutated_projection_cannot_copy_the_accepted_header(owner):
    history, replay, context = owner
    before = history.path.read_bytes()
    replay.graph.create_entity("InventoryUnit", "forged", {"product_code": "X"})
    with pytest.raises(module().AcceptedViewRefusal) as refused:
        freeze(replay, context)
    assert refused.value.reason == "STALE_BASE"
    assert history.path.read_bytes() == before
    assert not history.replay().graph.has_node("forged")


def test_protocol_bytes_cannot_borrow_a_receipt_identity(owner):
    _, replay, context = owner
    data = replay.protocol_replay.data
    data["state"]["action_acceptance_head"] = content_digest("forged")
    altered = replace(
        replay,
        protocol_replay=replace(
            replay.protocol_replay, canonical_bytes=canonical(data)
        ),
    )
    with pytest.raises(module().AcceptedViewRefusal) as refused:
        freeze(altered, context)
    assert refused.value.reason == "STALE_BASE"


def test_receipt_bytes_cannot_borrow_a_receipt_identity(owner):
    _, replay, context = owner
    altered = replace(replay, receipt=replace(replay.receipt, canonical_bytes=b"{}"))
    with pytest.raises(module().AcceptedViewRefusal) as refused:
        freeze(altered, context)
    assert refused.value.reason == "STALE_BASE"


@pytest.mark.parametrize(
    "field,value",
    [
        ("content", b"tampered"),
        ("role", "RETAINED_SOURCE"),
        ("media_type", "application/tampered"),
        ("record_id", "forged:input"),
    ],
)
def test_retained_bytes_roles_and_ids_must_match(owner, field, value):
    _, replay, context = owner
    member = next(
        item for item in context.retained_inputs if item.role == "RETAINED_EVIDENCE"
    )
    altered = replace(
        context,
        retained_inputs=tuple(
            replace(item, **{field: value}) if item == member else item
            for item in context.retained_inputs
        ),
    )
    with pytest.raises(module().AcceptedViewRefusal) as refused:
        freeze(replay, altered)
    assert refused.value.reason in {"STALE_BASE", "MALFORMED_INPUT"}


def test_missing_protocol_is_not_an_empty_satisfied_episode(owner, selected_prefix):
    history, _, _ = owner
    history.path.write_bytes(selected_prefix[1])
    history = api.KnowledgeChangeHistory.reopen(history.path)
    with pytest.raises(module().AcceptedViewRefusal) as refused:
        freeze(history.replay(), history.composition_context())
    assert refused.value.reason == "MALFORMED_INPUT"


@pytest.mark.parametrize("which", ["replay", "context"])
def test_wrong_input_kinds_refuse_loudly(owner, which):
    _, replay, context = owner
    with pytest.raises(module().AcceptedViewRefusal) as refused:
        freeze(
            {} if which == "replay" else replay, {} if which == "context" else context
        )
    assert refused.value.reason == "MALFORMED_INPUT"


def test_new_full_head_needs_a_fresh_context_even_when_graph_unchanged(owner):
    history, replay, context = owner
    content = b"explicit conformance note"
    history.append_anchors(
        anchors=(
            api.structural_evidence_anchor(
                record_id="artifact:read:next",
                content=content,
                media_type="text/plain",
            ),
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    fresh = history.replay()
    assert fresh.graph.state_digest() == replay.graph.state_digest()
    with pytest.raises(module().AcceptedViewRefusal) as refused:
        freeze(fresh, context)
    assert refused.value.reason == "STALE_BASE"
    assert (
        freeze(fresh, history.composition_context()).records
        == freeze(replay, context).records
    )


def test_freezing_needs_no_files_processes_or_network(owner, monkeypatch):
    import builtins
    import os
    import socket
    import subprocess

    _, replay, context = owner
    implementation = module()

    def forbidden(*args, **kwargs):
        raise AssertionError("read adapter crossed its no-I/O boundary")

    for target, name in (
        (builtins, "open"),
        (os, "open"),
        (Path, "open"),
        (socket, "socket"),
        (subprocess, "Popen"),
    ):
        monkeypatch.setattr(target, name, forbidden)
    actual = implementation.freeze_accepted_replay(replay=replay, context=context)
    assert actual.receipt_identity == context.receipt_identity


def test_boolean_ledger_count_does_not_acquire_integer_semantics(owner):
    _, replay, context = owner
    with pytest.raises(module().AcceptedViewRefusal) as refused:
        freeze(replay, replace(context, base_ledger_event_count=True))
    assert refused.value.reason == "MALFORMED_INPUT"


def test_adapter_imports_no_private_core_or_research_helpers():
    import ast

    implementation = module()
    tree = ast.parse(Path(implementation.__file__).read_bytes())
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0
            imported.append(node.module)
    assert all(
        not name.startswith(("malleus._", "research", "tests")) for name in imported
    )


def test_accepted_lineage_fields_are_required_immutable_inputs():
    from dataclasses import MISSING, fields

    declared = {field.name: field for field in fields(module().AcceptedReadView)}
    for name in ("accepted_change_sets", "record_history"):
        assert name in declared
        assert declared[name].default is MISSING
        assert declared[name].default_factory is MISSING


def test_actual_accepted_lineage_is_frozen_without_copying_private_state(owner):
    history, replay, context = owner
    before = history.path.read_bytes()
    view = freeze(replay, context)
    assert view.accepted_change_sets == replay.change_sets
    assert view.record_history == tuple(sorted(replay.record_history.items()))
    assert type(view.accepted_change_sets) is type(view.record_history) is tuple
    assert all(
        type(change) is api.KnowledgeChangeSet for change in view.accepted_change_sets
    )
    with pytest.raises((FrozenInstanceError, AttributeError)):
        view.record_history = ()
    with pytest.raises(TypeError):
        view.accepted_change_sets[0].data["change_set_id"] = "forged"
    assert history.path.read_bytes() == before


@pytest.mark.parametrize(
    "fault",
    [
        "missing-change",
        "reordered-changes",
        "duplicate-change",
        "missing-history",
        "wrong-operation",
        "broken-supersession",
    ],
)
def test_inconsistent_accepted_lineage_refuses_before_return(owner, fault):
    history, replay, context = owner
    altered = replay
    if fault == "missing-change":
        altered = replace(replay, change_sets=replay.change_sets[:-1])
    elif fault == "reordered-changes":
        altered = replace(replay, change_sets=tuple(reversed(replay.change_sets)))
    elif fault == "duplicate-change":
        altered = replace(
            replay, change_sets=(replay.change_sets[0], *replay.change_sets)
        )
    else:
        # Adversarial fake replay only; production reads the public history property.
        entries = dict(replay.record_history)
        identifier = next(iter(entries))
        if fault == "missing-history":
            del entries[identifier]
        elif fault == "wrong-operation":
            item = entries[identifier]
            entries[identifier] = replace(
                item, operation=replace(item.operation, record_id="forged")
            )
        else:
            identifier = next(
                key for key, value in entries.items() if value.superseded_by is not None
            )
            entries[identifier] = replace(
                entries[identifier], superseded_by="absent-successor"
            )
        altered = replace(replay, _record_history=entries)
    before = history.path.read_bytes()
    with pytest.raises(module().AcceptedViewRefusal) as caught:
        freeze(altered, context)
    assert caught.value.reason == "STALE_BASE"
    assert history.path.read_bytes() == before


def test_retained_candidate_bytes_do_not_become_accepted_lineage(owner):
    history, replay, _ = owner
    # Explicit retained conformance references, not a claim of source faithfulness.
    # The candidate is deliberately never admitted or represented as accepted fact.
    sources = tuple(identifier for identifier, _ in replay.change_sets[-1].sources)
    evidence = tuple(identifier for identifier, _ in replay.change_sets[-1].evidence)
    assert sources and evidence, "candidate fixture requires both retained closures"
    candidate = history.compose_change_set(
        change_set_id="change:read:unaccepted",
        source_record_ids=sources,
        evidence_record_ids=evidence,
        operations=(
            api.KnowledgeOperation(
                ordinal=0,
                operation_id="operation:read:unaccepted",
                operation_type="CREATE_ENTITY",
                record_type="InventoryUnit",
                record_id="unit:read:unaccepted",
                properties={"product_code": "X"},
                depends_on=(),
            ),
        ),
        valid_time=api.KnowledgeValidTime("NONE_STATED", None),
        supersedes=(),
    )
    assert tuple(identifier for identifier, _ in candidate.sources) == sources
    assert tuple(identifier for identifier, _ in candidate.evidence) == evidence
    history.append_anchors(
        anchors=(
            api.structural_evidence_anchor(
                record_id="evidence:read:unaccepted-kcs",
                content=candidate.canonical_bytes,
                media_type="application/json",
            ),
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    after = history.replay()
    view = freeze(after, history.composition_context())
    assert any(
        item.content == candidate.canonical_bytes
        for item in view.context.retained_inputs
    )
    assert view.accepted_change_sets == replay.change_sets
    assert candidate not in view.accepted_change_sets
    assert view.record_history == tuple(sorted(replay.record_history.items()))
    assert view.records == replay.graph.export_records()

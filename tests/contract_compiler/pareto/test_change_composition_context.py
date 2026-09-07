"""One composer, no writer capability in the producer's input."""

from dataclasses import fields, replace
import inspect
from pathlib import Path

import pytest

import malleus.compiler as api
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    TRANSACTION_TIME,
    _anchored_history,
    _base_payload,
    _evidence_anchor,
    _load_change,
    _protocol_events,
)


@pytest.fixture
def anchored(tmp_path):
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    expected = _load_change(_base_payload(history, partial, source, evidence))
    arguments = dict(
        change_set_id=expected.change_set_id,
        source_record_ids=("source-generic",),
        evidence_record_ids=("evidence-generic",),
        operations=expected.operations,
        valid_time=expected.valid_time,
        supersedes=expected.supersedes,
    )
    return history, expected, arguments


def test_public_context_and_pure_composer_have_no_writer_argument():
    assert {"KnowledgeChangeContext", "compose_change_set"} <= set(api.__all__)
    assert set(inspect.signature(api.compose_change_set).parameters) == {
        "context",
        "change_set_id",
        "source_record_ids",
        "evidence_record_ids",
        "operations",
        "valid_time",
        "supersedes",
    }


def test_snapshot_composition_matches_independent_bytes_without_io(
    anchored, monkeypatch
):
    history, expected, arguments = anchored
    before = history.path.read_bytes()
    context = history.composition_context()
    assert isinstance(context, api.KnowledgeChangeContext)

    def forbidden(*args, **kwargs):
        pytest.fail("pure composition attempted I/O or replay")

    with monkeypatch.context() as guard:
        guard.setattr(history, "replay", forbidden)
        guard.setattr(Path, "open", forbidden)
        guard.setattr("builtins.open", forbidden)
        actual = api.compose_change_set(context=context, **arguments)
        assert api.compose_change_set(context=context, **arguments) == actual
    assert actual == expected
    assert actual.canonical_bytes == expected.canonical_bytes
    assert history.path.read_bytes() == before


def test_history_method_delegates_to_one_composer(anchored, monkeypatch):
    import malleus._contract_pipeline.knowledge as implementation

    history, expected, arguments = anchored
    original = implementation.compose_change_set
    calls = []

    def observed(**kwargs):
        calls.append(kwargs["context"])
        return original(**kwargs)

    monkeypatch.setattr(implementation, "compose_change_set", observed)
    assert history.compose_change_set(**arguments) == expected
    assert len(calls) == 1


def test_context_contains_only_immutable_values_and_isolates_disposable_replay(
    anchored,
):
    history, expected, arguments = anchored
    replay = history.replay()
    context = history.composition_context()
    assert context.receipt_identity == replay.receipt.identity
    assert context.contract_identity == replay.partial_contract.identity
    assert context.base_accepted_state_digest == replay.graph.state_digest()
    assert context.base_ledger_head == replay.ledger_head
    assert context.base_ledger_event_count == replay.ledger_event_count
    assert context.base_acceptance_head == replay.acceptance_head
    assert context.base_materialization_head == replay.materialization_head
    assert all(
        type(getattr(context, field.name)) in (str, int, tuple)
        for field in fields(context)
    )
    with pytest.raises(AttributeError):
        context.base_ledger_head = "changed"
    with pytest.raises(AttributeError):
        context.retained_inputs[0].content = b"changed"
    replay.graph.create_entity("LeftObject", "local-only", {"label": "not accepted"})
    assert history.composition_context() == context
    assert api.compose_change_set(context=context, **arguments) == expected


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
def test_context_coordinate_substitution_refuses_before_effects(anchored, field):
    history, _, arguments = anchored
    context = history.composition_context()
    replacement = (
        context.base_ledger_event_count + 1
        if field == "base_ledger_event_count"
        else "sha256:" + "f" * 64
    )
    changed = replace(context, **{field: replacement})
    before = history.path.read_bytes()
    with pytest.raises(api.KnowledgeChangeRefusal) as error:
        api.compose_change_set(context=changed, **arguments)
    assert error.value.reason is api.KnowledgeChangeRefusalReason.IDENTITY_MISMATCH
    assert history.path.read_bytes() == before


@pytest.mark.parametrize(
    "field,value",
    [
        ("content", b"substituted"),
        ("record_id", "wrong-id"),
        ("role", "RETAINED_SOURCE"),
        ("identity", "sha256:" + "e" * 64),
    ],
)
def test_retained_closure_substitution_refuses(anchored, field, value):
    history, _, arguments = anchored
    context = history.composition_context()
    retained = tuple(
        replace(member, **{field: value})
        if member.record_id == "evidence-generic"
        else member
        for member in context.retained_inputs
    )
    before = history.path.read_bytes()
    with pytest.raises(api.KnowledgeChangeRefusal) as error:
        api.compose_change_set(
            context=replace(context, retained_inputs=retained), **arguments
        )
    assert error.value.reason is api.KnowledgeChangeRefusalReason.IDENTITY_MISMATCH
    assert history.path.read_bytes() == before


@pytest.mark.parametrize(
    "replacement,reason",
    [
        ({"context": None}, "MALFORMED_CHANGE_SET"),
        ({"source_record_ids": ("missing",)}, "UNRETAINED_INPUT"),
        ({"source_record_ids": ("evidence-generic",)}, "UNRETAINED_INPUT"),
        ({"evidence_record_ids": ("source-generic",)}, "UNRETAINED_INPUT"),
        ({"operations": (object(),)}, "MALFORMED_CHANGE_SET"),
        ({"operations": ()}, "MALFORMED_CHANGE_SET"),
    ],
)
def test_pure_path_keeps_existing_typed_refusals(anchored, replacement, reason):
    history, _, arguments = anchored
    inputs = dict(context=history.composition_context(), **arguments)
    inputs.update(replacement)
    before = history.path.read_bytes()
    with pytest.raises(api.KnowledgeChangeRefusal) as error:
        api.compose_change_set(**inputs)
    assert error.value.reason.name == reason
    assert history.path.read_bytes() == before


def test_snapshot_candidate_crosses_unchanged_admission_reopen_and_query(anchored):
    history, expected, arguments = anchored
    context = history.composition_context()
    candidate = api.compose_change_set(context=context, **arguments)
    history.admit(
        change_set=candidate,
        machine_events=_protocol_events(
            candidate, history.replay().machine_state.identity
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    reopened = api.KnowledgeChangeHistory.reopen(history.path).replay()
    assert reopened.change_sets == (expected,)
    assert reopened.graph.get_node("left-1")["label"] == "left"


def test_evidence_append_is_stale_even_when_graph_is_unchanged(anchored):
    history, expected, arguments = anchored
    before = history.replay()
    context = history.composition_context()
    history.append_anchors(
        anchors=(_evidence_anchor("extra-evidence", b"additional evidence"),),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    assert history.replay().graph.state_digest() == before.graph.state_digest()
    candidate = api.compose_change_set(context=context, **arguments)
    assert candidate == expected  # Pure composition does not secretly refresh.
    retained = history.path.read_bytes()
    with pytest.raises(api.KnowledgeChangeRefusal) as error:
        history.admit(
            change_set=candidate,
            machine_events=_protocol_events(
                candidate, history.replay().machine_state.identity
            ),
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )
    assert error.value.reason is api.KnowledgeChangeRefusalReason.STALE_BASE
    assert history.path.read_bytes() == retained

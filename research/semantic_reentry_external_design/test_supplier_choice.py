"""Two permitted translations, no implicit selection or new authority."""

from dataclasses import FrozenInstanceError
from importlib import import_module
import json
from pathlib import Path
import shutil

import pytest

import malleus.compiler as core
from malleus import KnowledgeGraph
from research.semantic_reentry_external_design import supplier_reentry as child
from research.semantic_reentry_external_design import supplier_walkthrough as single
from research.semantic_reentry_external_design.accepted_read_view import freeze_accepted_replay


def api():
    return import_module("research.semantic_reentry_external_design.supplier_choice")


def runner():
    return import_module("research.semantic_reentry_external_design.supplier_choice_walkthrough")


@pytest.fixture(scope="module")
def prefix(tmp_path_factory):
    path = tmp_path_factory.mktemp("choice-prefix")
    runner().prepare(path)
    return path


@pytest.fixture
def inputs(prefix, tmp_path):
    path = tmp_path / "episode"
    shutil.copytree(prefix, path)
    history = core.KnowledgeChangeHistory.reopen(path / "history.jsonl")
    return path, history


def read(history):
    replay = history.replay()
    return freeze_accepted_replay(replay=replay, context=history.composition_context())


def evaluate(history, rule_id):
    view = read(history)
    contract = api().bind_supplier_choice(view=view, rule_source_id=rule_id)
    return contract, synthesize(contract, view)


def synthesize(contract, view, **engines):
    return api().SupplierChoiceSynthesizer().synthesize(
        contract, view,
        synthesizer=engines.pop("synthesizer", child.SupplierReentrySynthesizer()),
        model=engines.pop("model", child.SupplierSourceModel()),
        update_strategy=engines.pop("update_strategy", child.SupplierActionStrategy()),
    )


def forbidden(*args, **kwargs):
    raise AssertionError("pure Re-entry crossed a forbidden boundary")


def test_choice_contract_roundtrip_and_pure_explicit_selection(inputs, monkeypatch):
    path, history = inputs
    view = read(history)
    contract = api().bind_supplier_choice(view=view, rule_source_id=runner().RULE)
    assert api().SupplierChoiceContract.from_bytes(contract.canonical_bytes) == contract
    with pytest.raises(FrozenInstanceError):
        contract.canonical_bytes = b"{}"
    before = history.path.read_bytes(), view.records_bytes
    with monkeypatch.context() as patch:
        for name in ("admit", "append_anchors", "append_protocol_events", "replay"):
            patch.setattr(core.KnowledgeChangeHistory, name, forbidden)
        patch.setattr(KnowledgeGraph, "create_entity", forbidden)
        patch.setattr(Path, "read_bytes", forbidden)
        result = synthesize(contract, view)
        assert result == synthesize(contract, view)
    assert result.status == "CANDIDATES" and result.selected_order == "B"
    assert [(a.order_id, a.predicted_total) for a in result.alternatives] == [("B", 3), ("C", 3)]
    assert len(result.candidates) == 1
    assert json.loads(result.candidates[0])["supplier_order_id"] == "B"
    assert (history.path.read_bytes(), read(history).records_bytes) == before


@pytest.mark.parametrize("selection,expected", [
    ({"strategy": "REFUSE_IF_NOT_UNIQUE", "order_preference": []}, "AMBIGUOUS"),
    ({"strategy": "ORDER_PREFERENCE", "order_preference": ["C", "B"]}, "C"),
])
def test_selection_is_data_not_enumeration(inputs, selection, expected):
    _, history = inputs
    rule = runner().variant(history, selection=selection, reverse_alternatives=True)
    before = history.path.read_bytes()
    _, result = evaluate(history, rule)
    assert [a.order_id for a in result.alternatives] == ["B", "C"]
    assert history.path.read_bytes() == before
    if expected == "AMBIGUOUS":
        assert (result.status, result.reason, result.candidates) == ("REFUSED", expected, ())
    else:
        assert result.selected_order == expected
        assert json.loads(result.candidates[0])["supplier_order_id"] == expected


@pytest.mark.parametrize("change,reason", [
    ({"selection": {"strategy": "CHEAPEST", "order_preference": []}}, "UNSUPPORTED"),
    ({"selection": {"strategy": "ORDER_PREFERENCE", "order_preference": ["B"]}}, "MALFORMED_INPUT"),
    ({"selection": {"strategy": "ORDER_PREFERENCE", "order_preference": ["B", "B"]}}, "MALFORMED_INPUT"),
    ({"candidate_budget": 0}, "BUDGET_EXHAUSTED"),
    ({"evaluation_budget": 1}, "BUDGET_EXHAUSTED"),
    ({"automatic_retry": True}, "UNSUPPORTED"),
    ({"dispatch_attempt_budget": 2}, "UNSUPPORTED"),
    ({"goal": {"kind": "GoalPredicate", "operator": "EXACTLY", "product_code": "Y", "quantity": 3, "order_ids": ["B", "C"]}}, "UNSUPPORTED"),
])
def test_invalid_rule_refuses_before_effect(inputs, change, reason):
    _, history = inputs
    rule = runner().variant(history, changes=change)
    before = history.path.read_bytes(), read(history).records_bytes
    try:
        _, result = evaluate(history, rule)
    except api().ChoiceRefusal as error:
        assert error.reason == reason
    else:
        assert (result.status, result.reason, result.candidates) == ("REFUSED", reason, ())
    assert (history.path.read_bytes(), read(history).records_bytes) == before


def test_stale_head_refuses_before_model_or_satisfied_shortcut(inputs, monkeypatch):
    _, history = inputs
    old, _ = evaluate(history, runner().RULE)
    single.retain_source(history, "source:choice:later-evidence", b"evidence", [])
    view = read(history)
    monkeypatch.setattr(child.SupplierSourceModel, "predict", forbidden)
    result = synthesize(old, view)
    assert (result.status, result.reason, result.candidates) == ("REFUSED", "STALE_BASE", ())


def test_model_cannot_invent_an_unsupported_amendment(inputs):
    _, history = inputs

    class BadModel(child.SupplierSourceModel):
        def predict(self, **kwargs):
            value = json.loads(super().predict(**kwargs))
            value["quantity"] = 9
            return single.canonical(value) + b"\n"

    view = read(history)
    contract = api().bind_supplier_choice(view=view, rule_source_id=runner().RULE)
    result = synthesize(contract, view, model=BadModel())
    assert result.status == "REFUSED" and result.candidates == ()


def test_full_choice_loop_observes_before_knowledge_changes(inputs):
    path, _ = inputs
    result = runner().finish(path)
    expected = json.loads((runner().FIXTURE / "oracle/expected.json").read_bytes())
    assert result["accepted_initial"] == expected["accepted_initial"]
    assert result["predicted_totals"] == expected["predicted_totals"]
    assert result["without_preference"] == expected["without_preference"]
    assert result["executed_not_observed"] == expected["executed_not_observed"]
    assert result["accepted_final"] == expected["accepted_final"]
    assert result["final"] == expected["final"]
    assert result["dispatch_attempts"] == expected["dispatch_attempts"]
    reopened = core.KnowledgeChangeHistory.reopen(path / "history.jsonl")
    _, fresh = evaluate(reopened, runner().RULE)
    assert (fresh.status, fresh.reason, fresh.candidates) == ("SATISFIED", "LINKED_OBSERVED_KCS", ())


def test_missing_contract_fields_do_not_default(inputs):
    _, history = inputs
    contract, _ = evaluate(history, runner().RULE)
    for field in json.loads(contract.canonical_bytes):
        value = json.loads(contract.canonical_bytes)
        del value[field]
        with pytest.raises(api().ChoiceRefusal, match="MALFORMED_INPUT"):
            api().SupplierChoiceContract.from_bytes(single.canonical(value))

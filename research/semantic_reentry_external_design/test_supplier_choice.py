"""Two permitted translations, no implicit selection or new authority."""

from dataclasses import FrozenInstanceError, fields
import builtins
from contextlib import contextmanager
from importlib import import_module
import json
from hashlib import sha256
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

import malleus.compiler as core
from malleus import KnowledgeGraph
from research.semantic_reentry_external_design import supplier_reentry as child
from research.semantic_reentry_external_design import supplier_walkthrough as single
from research.semantic_reentry_external_design.accepted_read_view import (
    freeze_accepted_replay,
)


CORE_SOURCE_TREE = "3b4fd1c9eb66d84c31050b5f0fd970a6fc2572a8"
HISTORICAL_GUARD = (
    "research/semantic_reentry_external_design/test_supplier_replay_laws.py"
    "::test_unified_gate_has_one_compatible_runtime_epoch"
)


def require_current_gate(source_tree, selectors):
    if source_tree != CORE_SOURCE_TREE:
        raise ValueError("Unreviewed Core source epoch: " + source_tree)
    if any(
        HISTORICAL_GUARD == s or HISTORICAL_GUARD.startswith(s + "::")
        for s in selectors
    ):
        raise ValueError("Historical epoch guard included in current gate")


def api():
    return import_module("research.semantic_reentry_external_design.supplier_choice")


def runner():
    return import_module(
        "research.semantic_reentry_external_design.supplier_choice_walkthrough"
    )


@contextmanager
def no_test_or_oracle_inputs():
    original_import, original_open = builtins.__import__, Path.open

    def checked_import(name, *args, **kwargs):
        if name.startswith("research.") and any(
            part.startswith("test_") for part in name.split(".")
        ):
            raise AssertionError("production runner imported a test helper")
        return original_import(name, *args, **kwargs)

    def checked_open(path, *args, **kwargs):
        if "oracle" in path.parts:
            raise AssertionError("execution consumed expected output")
        return original_open(path, *args, **kwargs)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(builtins, "__import__", checked_import)
        patch.setattr(Path, "open", checked_open)
        yield


@pytest.fixture(scope="module")
def prefix(tmp_path_factory):
    path = tmp_path_factory.mktemp("choice-prefix")
    with no_test_or_oracle_inputs():
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
    return (
        api()
        .SupplierChoiceSynthesizer()
        .synthesize(
            contract,
            view,
            synthesizer=engines.pop("synthesizer", child.SupplierReentrySynthesizer()),
            model=engines.pop("model", child.SupplierSourceModel()),
            update_strategy=engines.pop(
                "update_strategy", child.SupplierActionStrategy()
            ),
        )
    )


def forbidden(*args, **kwargs):
    raise AssertionError("pure Re-entry crossed a forbidden boundary")


def test_alternative_diagnostics_cannot_carry_proposal_bytes():
    assert {field.name for field in fields(api().ChoiceAlternative)} == {
        "order_id",
        "predicted_total",
    }


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
    assert [(a.order_id, a.predicted_total) for a in result.alternatives] == [
        ("B", 3),
        ("C", 3),
    ]
    assert len(result.candidates) == 1
    assert json.loads(result.candidates[0])["supplier_order_id"] == "B"
    assert (history.path.read_bytes(), read(history).records_bytes) == before


@pytest.mark.parametrize(
    "selection,expected",
    [
        ({"strategy": "REFUSE_IF_NOT_UNIQUE", "order_preference": []}, "AMBIGUOUS"),
        ({"strategy": "ORDER_PREFERENCE", "order_preference": ["C", "B"]}, "C"),
    ],
)
def test_selection_is_data_not_enumeration(inputs, selection, expected):
    _, history = inputs
    rule = runner().variant(history, selection=selection, reverse_alternatives=True)
    before = history.path.read_bytes()
    contract, result = evaluate(history, rule)
    assert [a.order_id for a in result.alternatives] == ["B", "C"]
    assert history.path.read_bytes() == before
    if expected == "AMBIGUOUS":
        assert (result.status, result.reason, result.candidates) == (
            "REFUSED",
            expected,
            (),
        )
    else:
        assert result.selected_order == expected
        assert json.loads(result.candidates[0])["supplier_order_id"] == expected
        original = json.loads(contract.canonical_bytes)["original_contexts"][expected]
        prior = history.replay().graph.export_records()
        single.proposals.submit_supplier_proposal(
            history=history,
            **single.position(history),
            original_context_bytes=single.canonical(original),
            action_bytes=result.candidates[0],
            proposal_key="supplier:synthesized:proposal",
            context_actor_id=single.ACTOR,
            artifact_version="research-v1",
        )
        assert history.replay().graph.export_records() == prior
        assert history.replay().protocol_replay.data["records"][original["action_id"]][
            "record"
        ] == json.loads(result.candidates[0])


@pytest.mark.parametrize(
    "change,reason",
    [
        (
            {"selection": {"strategy": "CHEAPEST", "order_preference": []}},
            "UNSUPPORTED",
        ),
        (
            {"selection": {"strategy": "ORDER_PREFERENCE", "order_preference": ["B"]}},
            "MALFORMED_INPUT",
        ),
        (
            {
                "selection": {
                    "strategy": "ORDER_PREFERENCE",
                    "order_preference": ["B", "B"],
                }
            },
            "MALFORMED_INPUT",
        ),
        ({"candidate_budget": 0}, "BUDGET_EXHAUSTED"),
        ({"evaluation_budget": 1}, "BUDGET_EXHAUSTED"),
        ({"automatic_retry": True}, "UNSUPPORTED"),
        ({"dispatch_attempt_budget": 2}, "UNSUPPORTED"),
        (
            {
                "goal": {
                    "kind": "GoalPredicate",
                    "operator": "EXACTLY",
                    "product_code": "Y",
                    "quantity": 3,
                    "order_ids": ["B", "C"],
                }
            },
            "UNSUPPORTED",
        ),
    ],
)
def test_invalid_rule_refuses_before_effect(inputs, change, reason):
    _, history = inputs
    rule = runner().variant(history, changes=change)
    before = history.path.read_bytes(), read(history).records_bytes
    try:
        _, result = evaluate(history, rule)
    except api().ChoiceRefusal as error:
        assert error.reason == reason
    else:
        assert (result.status, result.reason, result.candidates) == (
            "REFUSED",
            reason,
            (),
        )
    assert (history.path.read_bytes(), read(history).records_bytes) == before


def test_stale_head_refuses_before_model_or_satisfied_shortcut(inputs, monkeypatch):
    _, history = inputs
    old, _ = evaluate(history, runner().RULE)
    single.retain_source(history, "source:choice:later-evidence", b"evidence", [])
    view = read(history)
    monkeypatch.setattr(child.SupplierSourceModel, "predict", forbidden)
    result = synthesize(old, view)
    assert (result.status, result.reason, result.candidates) == (
        "REFUSED",
        "STALE_BASE",
        (),
    )


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


def test_full_choice_loop_observes_before_knowledge_changes(inputs, monkeypatch):
    path, _ = inputs
    opened = []
    original_open = core.KnowledgeHistoryProjection.open

    def tracked_open(ledger_path):
        opened.append(ledger_path)
        return original_open(ledger_path)

    with monkeypatch.context() as patch, no_test_or_oracle_inputs():
        patch.setattr(
            core.KnowledgeHistoryProjection, "open", staticmethod(tracked_open)
        )
        result = runner().finish(path)
    assert opened == [path / "history.jsonl"]
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
    assert (fresh.status, fresh.reason, fresh.candidates) == (
        "SATISFIED",
        "LINKED_OBSERVED_KCS",
        (),
    )
    # Rebuild from JSONL only, then consume the published read without disk or engines.
    isolated = path / "jsonl-only"
    isolated.mkdir()
    shutil.copyfile(path / "history.jsonl", isolated / "history.jsonl")
    owner = core.KnowledgeChangeHistory.reopen(isolated / "history.jsonl")
    context = owner.composition_context()
    projection = core.KnowledgeHistoryProjection.open(owner.path)
    coordinates = dict(
        expected_head_hash=context.base_ledger_head,
        expected_event_count=context.base_ledger_event_count,
    )
    rebuilt = projection.refresh(**coordinates)
    view = freeze_accepted_replay(replay=rebuilt, context=context)
    contract = api().bind_supplier_choice(view=view, rule_source_id=runner().RULE)
    with monkeypatch.context() as patch:
        patch.setattr(Path, "read_bytes", forbidden)
        patch.setattr(core.KnowledgeChangeHistory, "replay", forbidden)
        patch.setattr(core.KnowledgeChangeHistory, "admit", forbidden)
        patch.setattr(child.SupplierSourceModel, "predict", forbidden)
        patch.setattr(single.execution, "_attempt", forbidden)
        assert projection.current(**coordinates).receipt == rebuilt.receipt
        assert synthesize(contract, view) == fresh


def test_missing_contract_fields_do_not_default(inputs):
    _, history = inputs
    contract, _ = evaluate(history, runner().RULE)
    for field in json.loads(contract.canonical_bytes):
        value = json.loads(contract.canonical_bytes)
        del value[field]
        with pytest.raises(api().ChoiceRefusal, match="MALFORMED_INPUT"):
            api().SupplierChoiceContract.from_bytes(single.canonical(value))


def test_satisfied_goal_checks_engines_and_head_without_model_calls(
    inputs, monkeypatch
):
    _, history = inputs
    goal = dict(
        json.loads((runner().FIXTURE / "case.json").read_bytes())["goal"], quantity=2
    )
    rule = runner().variant(history, changes={"goal": goal})
    view = read(history)
    contract = api().bind_supplier_choice(view=view, rule_source_id=rule)
    monkeypatch.setattr(child.SupplierSourceModel, "predict", forbidden)
    before = history.path.read_bytes()
    result = synthesize(contract, view)
    assert (result.status, result.reason, result.candidates) == (
        "SATISFIED",
        "INITIAL_SATISFIED",
        (),
    )

    class Unselected(child.SupplierSourceModel):
        implementation_identity = "sha256:" + "0" * 64

    result = synthesize(contract, view, model=Unselected())
    assert (result.status, result.reason) == ("REFUSED", "UNSUPPORTED_IMPLEMENTATION")
    assert history.path.read_bytes() == before
    single.retain_source(history, "source:choice:after-satisfied", b"evidence", [])
    result = synthesize(contract, read(history))
    assert (result.status, result.reason) == ("REFUSED", "STALE_BASE")


def test_stale_selected_proposal_cannot_be_submitted(inputs):
    _, history = inputs
    contract, result = evaluate(history, runner().RULE)
    original = json.loads(contract.canonical_bytes)["original_contexts"]["B"]
    single.retain_source(history, "source:choice:before-submit", b"evidence", [])
    before = history.path.read_bytes()
    with pytest.raises(single.proposals.SupplierProtocolError, match="STALE_BASE"):
        single.proposals.submit_supplier_proposal(
            history=history,
            **single.position(history),
            original_context_bytes=single.canonical(original),
            action_bytes=result.candidates[0],
            proposal_key="supplier:synthesized:proposal",
            context_actor_id=single.ACTOR,
            artifact_version="research-v1",
        )
    assert history.path.read_bytes() == before


def test_unknown_child_operation_cannot_be_selected(inputs):
    _, history = inputs
    rule = json.loads(history.replay().retained_bytes(runner().RULE))
    alternative = rule["alternatives"][0]
    original_rule = alternative["rule_source_id"]
    unsupported = json.loads(history.replay().retained_bytes(original_rule))
    unsupported["operator"]["kind"] = "DELETE_SUPPLIER_ORDER"
    identifier = original_rule + ":unsupported"
    dependencies = history.replay().protocol_replay.data["records"][original_rule][
        "record"
    ]["source_record_ids"]
    single.retain_source(
        history, identifier, single.canonical(unsupported), dependencies
    )
    alternative["rule_source_id"] = identifier
    variant = runner().variant(history, changes={"alternatives": rule["alternatives"]})
    with pytest.raises(api().ChoiceRefusal, match="UNSUPPORTED"):
        evaluate(history, variant)


def test_model_failure_has_a_typed_empty_result(inputs):
    _, history = inputs

    class Broken(child.SupplierSourceModel):
        def predict(self, **kwargs):
            raise RuntimeError("controlled engine failure")

    view = read(history)
    contract = api().bind_supplier_choice(view=view, rule_source_id=runner().RULE)
    result = synthesize(contract, view, model=Broken())
    assert (result.status, result.reason, result.candidates) == (
        "REFUSED",
        "ENGINE_FAILURE",
        (),
    )


def test_gate_uses_inspected_core_without_modifying_it():
    gate = json.loads(
        (Path(__file__).parent / "supplier-choice-gate.json").read_bytes()
    )
    source_tree = subprocess.check_output(
        ["git", "rev-parse", "HEAD:src"], text=True
    ).strip()
    selectors = [s for group in gate["groups"].values() for s in group]
    require_current_gate(source_tree, selectors)
    assert source_tree == gate["core_source_tree"]
    assert gate["base_commit"] == "e2b9e77912f9b36fdbfe2fca310548a789bffb4d"
    assert len(selectors) == len(set(selectors))
    assert gate["historical_epoch_guard"]["selector"] == HISTORICAL_GUARD
    root = Path(__file__).resolve().parents[2]
    for entry in gate["historical_evidence"]:
        assert (
            sha256((root / entry["path"]).read_bytes()).hexdigest() == entry["sha256"]
        )
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] == "malleus" and getattr(module, "__file__", None):
            assert Path(module.__file__).resolve().is_relative_to(root / "src/malleus")
    assert (
        subprocess.check_output(
            [
                "git",
                "status",
                "--porcelain",
                "--untracked-files=all",
                "--",
                "src",
                "ontology",
            ],
            text=True,
        )
        == ""
    )


@pytest.mark.parametrize(
    "epoch",
    [
        "763d3b72ad2143bc5735eed32d47a69e3f6b8cd1",
        "31e11514b1f999dd145724c3a0f9b7e95c126595",
        "unknown",
    ],
)
def test_gate_rejects_older_or_unknown_core(epoch):
    with pytest.raises(ValueError, match="Unreviewed Core source epoch"):
        require_current_gate(epoch, [])


@pytest.mark.parametrize(
    "selector", [HISTORICAL_GUARD, HISTORICAL_GUARD.split("::")[0]]
)
def test_gate_rejects_direct_or_implicit_historical_guard(selector):
    with pytest.raises(ValueError, match="Historical epoch guard"):
        require_current_gate(CORE_SOURCE_TREE, [selector])


@pytest.mark.parametrize("fault", ["after-write", "unchanged-success"])
def test_effect_receipt_never_substitutes_for_observation(inputs, monkeypatch, fault):
    path, history = inputs
    write = single.execution._write_source

    def controlled(target, content):
        if fault == "after-write":
            write(target, content)
            raise OSError("controlled failure after actual write")

    monkeypatch.setattr(single.execution, "_write_source", controlled)
    if fault == "after-write":
        result = runner().finish(path)
        assert result["accepted_final"] == {"B": 2, "C": 1}
        assert result["final"]["status"] == "SATISFIED"
    else:
        with pytest.raises(single.WalkthroughError, match="observed KCS required"):
            runner().finish(path)
    history = core.KnowledgeChangeHistory.reopen(history.path)
    replay = history.replay()
    expected_status = "FAILED" if fault == "after-write" else "SUCCEEDED"
    assert (
        replay.protocol_replay.data["records"]["execution:supplier:1"]["record"][
            "execution_status"
        ]
        == expected_status
    )
    monkeypatch.setattr(child.SupplierSourceModel, "predict", forbidden)
    _, final = evaluate(history, runner().RULE)
    assert not final.candidates
    if fault == "unchanged-success":
        assert (final.status, final.reason) == ("REFUSED", "EPISODE_TERMINAL")
        assert runner().quantities(replay) == {"B": 1, "C": 1}

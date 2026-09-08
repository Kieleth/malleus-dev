"""Adversarial inputs at the pure boundary, using actual accepted Core fixtures."""

from base64 import b64decode
from dataclasses import FrozenInstanceError
import json
from pathlib import Path

import pytest

import malleus.compiler as core
from research.semantic_reentry_external_design import test_supplier_reentry as entry
from research.semantic_reentry_external_design.test_supplier_reentry import (
    compile_supplier_action as compile_supplier_action,
    reentry_prefix as reentry_prefix,
    reentry_inputs as reentry_inputs,
)


def changed_rule(owner, original_bytes, value):
    original = json.loads(original_bytes)
    rule_id, goal_id = entry.RULE + ":boundary", entry.GOAL + ":boundary"
    goal_bytes = owner.replay().retained_bytes(original["goal"]["id"])
    entry.retain_source(
        owner,
        rule_id,
        entry.entry.ingress.canonical(value),
        [entry.IMPLEMENTATION, entry.EXECUTOR, entry.MAPPER, entry.OBSERVER],
    )
    entry.retain_source(owner, goal_id, goal_bytes, [rule_id])
    view = entry.freeze_accepted_replay(
        replay=owner.replay(), context=owner.composition_context()
    )
    source_ids = {
        role: original[role]["id"]
        for role in ("goal", "mapping", "preservation", "pre_state_source")
    }
    source_ids["goal"] = goal_id
    new_original = entry.entry.api().original_supplier_context(
        view=view,
        initialization_id=value["initialization_id"],
        source_ids=source_ids,
        context_id=original["id"],
        action_id=original["action_id"],
        proposal_id=original["proposal_id"],
        episode_key=original["episode_key"],
    )
    return view, new_original, rule_id


@pytest.mark.parametrize("fault", ["target", "prediction"])
def test_strategy_output_cannot_escape_bound_goal(reentry_inputs, monkeypatch, fault):
    owner, view, _, contract = reentry_inputs
    ordinary = entry.api().SupplierActionStrategy.payload

    def wrong_output(self, **kwargs):
        if fault == "prediction":
            # A faulty strategy must not be trusted to validate a faulty model.
            corrected = dict(kwargs)
            corrected["prediction"] = entry.supplier_components.model_amendment(
                kwargs["before_bytes"],
                source_sha256=kwargs["source_sha256"],
                goal=kwargs["goal"],
                operator=kwargs["operator"],
            )
            return ordinary(self, **corrected)
        payload = json.loads(ordinary(self, **kwargs))
        payload["supplier_order_id"] = "different-supplier-order"
        return entry.entry.ingress.canonical(payload)

    if fault == "prediction":

        def wrong_model(self, **kwargs):
            row = json.loads(kwargs["before_bytes"])
            row["quantity"] = 3
            row["event_id"] = kwargs["operator"]["new_source_occurrence_id"]
            return entry.entry.ingress.canonical(row) + b"\n"

        monkeypatch.setattr(entry.api().SupplierSourceModel, "predict", wrong_model)
    monkeypatch.setattr(entry.api().SupplierActionStrategy, "payload", wrong_output)
    before = owner.path.read_bytes(), entry.authority.domain_frame(owner.replay())
    result = entry.synthesize(contract, view)
    assert result.status == "REFUSED"
    assert result.reason in {"MODEL_DISAGREEMENT", "UNSUPPORTED_CHANGE"}
    assert not result.candidates
    assert (
        owner.path.read_bytes(),
        entry.authority.domain_frame(owner.replay()),
    ) == before


def test_zero_candidate_budget_refuses_without_model(
    reentry_inputs, reentry_prefix, monkeypatch
):
    owner, _, original, _ = reentry_inputs
    value = entry.rule_value(reentry_prefix[1], reentry_prefix[2])
    value["candidate_budget"] = 0
    view, original, rule_id = changed_rule(owner, original, value)
    contract = entry.api().bind_supplier_reentry(
        view=view, original_context_bytes=original, rule_source_id=rule_id
    )

    def forbidden(*args, **kwargs):
        pytest.fail("zero candidate budget invoked a model")

    monkeypatch.setattr(entry.api().SupplierSourceModel, "predict", forbidden)
    before = owner.path.read_bytes()
    result = entry.synthesize(contract, view)
    assert (result.status, result.reason) == ("REFUSED", "BUDGET_EXHAUSTED")
    assert result.candidates == () and owner.path.read_bytes() == before


def test_contract_and_view_cannot_receive_direct_graph_mutation(reentry_inputs):
    owner, view, _, contract = reentry_inputs
    before = owner.path.read_bytes(), view.records_bytes
    for value in (view, contract):
        with pytest.raises((FrozenInstanceError, AttributeError, TypeError)):
            value.graph = owner.replay().graph
        assert not hasattr(value, "graph")
    projection = view.records
    projection["entities"].clear()
    assert (owner.path.read_bytes(), view.records_bytes) == before


def test_implementation_capsule_contains_exact_selected_sources():
    api = entry.api()
    value = json.loads(api.IMPLEMENTATION_BYTES)
    root = Path(api.__file__).resolve().parent
    assert value["schema"] == "malleus.reentry.source-capsule/research-v1"
    assert set(value["files"]) == {
        "supplier_reentry.py",
        "supplier_components.py",
        "supplier_proposals.py",
        "accepted_read_view.py",
    }
    for name, content in value["files"].items():
        assert b64decode(content, validate=True) == (root / name).read_bytes()
    assert (
        entry.entry.ingress.digest(api.IMPLEMENTATION_BYTES)
        == api.IMPLEMENTATION_IDENTITY
    )
    assert Path(core.__file__).resolve().is_relative_to(root.parents[1] / "src")

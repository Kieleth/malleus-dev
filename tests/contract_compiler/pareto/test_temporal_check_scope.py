"""Existing admission scopes, measured before extending temporal meaning.

These are baseline observations, not correction support or a new rule policy.
The observer passes every call to the real executor unchanged.
"""

from dataclasses import replace

import malleus.compiler as api
from malleus._contract_pipeline import admission
from malleus.staging import CandidateSubgraph
from tests.contract_compiler.pareto import test_temporal_history as prices
from tests.contract_compiler.pareto import test_change_set_admission as orders


compilation = prices.compilation
history = prices.history


def observe_checks(monkeypatch):
    observed = []
    execute = admission._run_check

    def observe(contract, request, provenance):
        assert isinstance(request.candidate_graph, CandidateSubgraph)
        observed.append((contract.executor_kind, request))
        return execute(contract, request, provenance)

    monkeypatch.setattr(admission, "_run_check", observe)
    return observed


def test_price_transition_checks_new_graph_not_an_earlier_period(history, monkeypatch):
    prices.accept(
        history,
        prices.proposed(
            history, "price:old", 750, {"kind": "INSTANT", "value": prices.MAY_1}
        ),
    )
    change = prices.proposed(
        history,
        "price:new",
        800,
        {"kind": "INSTANT", "value": prices.MAY_12},
        supersedes="price:old",
    )
    observed = observe_checks(monkeypatch)
    result = prices.accept(history, change)

    assert len(observed) == 1
    executor_kind, request = observed[0]
    assert executor_kind is api.CheckExecutorKind.CORE_BUILTIN
    assert request.replay.record_history["price:old"].operation.properties == {
        "price_cents": 750
    }
    graph = request.candidate_graph.overlay()
    assert graph.get_node("price:old") is None
    assert graph.get_node("price:new")["price_cents"] == 800
    assert request.candidate.valid_time == change.valid_time
    assert result.record_history["price:old"].valid_to.value == prices.MAY_12


@orders.swipl
def test_real_prolog_rule_sees_replacement_not_retired_order(tmp_path, monkeypatch):
    history, _, logic, _ = orders._shop_shaped(tmp_path)
    first = orders._composed(
        history, orders._record("e1", 2), change_set_id="change:scope:first"
    )
    orders._admit(history, first)
    operation = replace(
        orders._operations(orders._record("e2", 5))[0],
        supersedes_record_id="supplier-order-state:B:e1",
    )
    next_change = history.compose_change_set(
        change_set_id="change:scope:next",
        source_record_ids=(orders.SOURCE_ID,),
        evidence_record_ids=("artifact:logic",),
        operations=(operation,),
        valid_time=api.KnowledgeValidTime("ORDER_ONLY", "e2"),
        supersedes=(),
    )
    observed = observe_checks(monkeypatch)
    accepted = orders._admit(history, next_change)

    assert len(observed) == 1
    executor_kind, request = observed[0]
    assert executor_kind is api.CheckExecutorKind.PROLOG_RULES
    graph = request.candidate_graph.overlay()
    assert graph.get_node("supplier-order-state:B:e1") is None
    assert graph.get_node("supplier-order-state:B:e2") is not None
    assert "supplier-order-state:B:e1" in request.replay.record_history
    assert accepted.checks[0].check_contract_id == logic.contract_id
    assert accepted.checks[0].outcome == "SATISFIED"
    assert api.KnowledgeChangeHistory.reopen(history.path).replay().receipt == (
        accepted.replay.receipt
    )

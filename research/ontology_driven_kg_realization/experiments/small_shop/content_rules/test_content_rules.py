"""Rule-level and admission-level tests for the Shop content policy."""

from __future__ import annotations

import json

import pytest

import malleus.compiler as api
from malleus.kg import KnowledgeGraph
from malleus.prolog_verifier import PrologVerifier
from malleus.staging import ProposedOperation, stage_subgraph

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    run as story,
)
from research.ontology_driven_kg_realization.experiments.small_shop.content_rules import (
    run as content,
)


ORDER = {"source_identifier": "O1"}
BASE_ENTITY = "https://malleus.dev/schema/Entity"


@pytest.fixture(scope="module")
def view():
    return story.compile_shop().view


@pytest.fixture(scope="module")
def verifier():
    return PrologVerifier(content.load_contract())


@pytest.fixture(scope="module")
def admitted(tmp_path_factory):
    """One honest Table 1 history under the content policy, built once."""
    path = tmp_path_factory.mktemp("content-rules") / "history.jsonl"
    return content.run(path), path


@pytest.fixture(scope="module")
def connected(tmp_path_factory):
    """The same rows through the connected story's own unpolicied build path."""
    path = tmp_path_factory.mktemp("connected") / "history.jsonl"
    return story.run_story(path), path


def state(record_id, product, quantity, occurrence="e1"):
    return ProposedOperation.entity(
        "SalesOrderState",
        record_id,
        {
            "order_id": "order:O1",
            "product_code": product,
            "ordered_quantity": quantity,
            "source_occurrence_id": occurrence,
        },
    )


def check(view, verifier, writes):
    graph = KnowledgeGraph(view)
    graph.create_entity("SalesOrder", "order:O1", dict(ORDER))
    return verifier.verify_candidate_subgraph(stage_subgraph(graph, writes))


def codes(result):
    return sorted((item.rule_id, item.violation_code) for item in result.violations)


# RED 1: a second live quantity for the same order and product must be caught.
def test_conflicting_quantity_is_violated(view, verifier):
    result = check(view, verifier, [state("s1", "X", 2), state("s2", "X", 3, "e2")])
    assert result.outcome == "VIOLATED"
    assert codes(result) == [("NO_CONFLICTING_QUANTITY", "QUANTITY_DISAGREEMENT")]
    assert result.violations[0].witness_record_ids == ("s1", "s2")


# RED 2: a record with no property at all must be caught.
def test_empty_record_is_violated(view, verifier):
    result = check(
        view, verifier, [ProposedOperation.entity(BASE_ENTITY, "synthetic:empty", {})]
    )
    assert result.outcome == "VIOLATED"
    assert codes(result) == [("NO_EMPTY_RECORD", "RECORD_WITHOUT_PROPERTIES")]
    assert result.violations[0].witness_record_ids == ("synthetic:empty",)


# Positive control 1: agreeing and unrelated quantities are not a disagreement.
def test_agreeing_and_distinct_quantities_are_satisfied(view, verifier):
    result = check(
        view,
        verifier,
        [
            state("s1", "X", 2),
            state("s2", "X", 2, "e2"),
            state("s3", "Y", 7, "e3"),
        ],
    )
    assert result.outcome == "SATISFIED"
    assert result.violations == ()


# Positive control 2: a record carrying one property is not an empty record.
def test_record_with_properties_is_satisfied(view, verifier):
    result = check(
        view,
        verifier,
        [
            ProposedOperation.entity(
                "SalesOrder", "order:O2", {"source_identifier": "O2"}
            )
        ],
    )
    assert result.outcome == "SATISFIED"
    assert result.violations == ()


def test_both_rules_run_on_every_check(view, verifier):
    contract = content.load_contract()
    assert sorted(contract.rule_ids) == ["NO_CONFLICTING_QUANTITY", "NO_EMPTY_RECORD"]
    result = check(view, verifier, [state("s1", "X", 2)])
    assert sorted(result.checked_rule_ids) == sorted(contract.rule_ids)


def test_policy_selects_the_exact_contract():
    policy = content.load_policy()
    contract = content.load_contract()
    assert policy.required_checks == ((contract.contract_id, contract.contract_hash),)
    assert policy.outcome_verdicts["VIOLATED"] == "REJECT"
    assert policy.outcome_verdicts["SATISFIED"] == "ACCEPT"


def test_honest_population_admits_with_zero_refusals(admitted):
    report, _ = admitted
    assert report["accepted_changes"] == 21
    assert report["historical_records"] == 107


def test_synthetic_conflict_refuses_and_leaves_the_ledger(admitted):
    report, _ = admitted
    refusal = next(item for item in report["refusals"] if item["kind"] == "conflict")
    assert refusal["outcome"] == "VIOLATED"
    assert refusal["refusal_reason"] == "REJECTED_CHANGE"
    assert refusal["ledger_unchanged"] is True
    assert [item["violation_code"] for item in refusal["violations"]] == [
        "QUANTITY_DISAGREEMENT"
    ]


def test_synthetic_empty_record_refuses_and_leaves_the_ledger(admitted):
    report, _ = admitted
    refusal = next(item for item in report["refusals"] if item["kind"] == "empty")
    assert refusal["outcome"] == "VIOLATED"
    assert refusal["refusal_reason"] == "REJECTED_CHANGE"
    assert refusal["ledger_unchanged"] is True
    assert [item["violation_code"] for item in refusal["violations"]] == [
        "RECORD_WITHOUT_PROPERTIES"
    ]


def test_baseline_reproduces_the_committed_connected_receipt(connected):
    """The control is verified, not quoted: it must return the frozen receipt."""
    replay, _ = connected
    committed = json.loads((story.HERE / "run_receipt.json").read_bytes())
    assert replay.receipt.identity == committed["replay_receipt"]
    assert replay.ledger_event_count == committed["protocol_ledger_events"]
    assert len(replay.record_history) == committed["historical_records"]


def test_domain_records_match_the_connected_story(admitted, connected):
    report, _ = admitted
    replay, _ = connected
    assert report["graph"] == replay.graph.export_records()


def test_record_history_and_derivations_match(admitted, connected):
    _, path = admitted
    policied = api.KnowledgeChangeHistory.reopen(path).replay()
    replay, _ = connected
    assert set(policied.record_history) == set(replay.record_history)
    for record_id, member in policied.record_history.items():
        other = replay.record_history[record_id]
        assert member.operation.record_type == other.operation.record_type
        assert dict(member.operation.properties) == dict(other.operation.properties)
        assert member.supersedes_record_id == other.supersedes_record_id
        assert member.superseded_by == other.superseded_by


def test_retained_plans_differ_only_in_the_bound_contract(admitted, connected):
    """Every plan binds the effective contract, and the policy is part of it."""
    _, path = admitted
    policied = api.KnowledgeChangeHistory.reopen(path).replay()
    replay, _ = connected
    rows, _ = story.load_sources(story.HERE)
    for row in rows:
        plan_id = f"plan:shop-connected:{row['event_id']}"
        mine = json.loads(policied.retained_bytes(plan_id))
        theirs = json.loads(replay.retained_bytes(plan_id))
        assert mine["contract_identity"] == policied.partial_contract.identity
        assert theirs["contract_identity"] == replay.partial_contract.identity
        assert mine["contract_identity"] != theirs["contract_identity"]
        del mine["contract_identity"], theirs["contract_identity"]
        assert mine == theirs


def test_check_receipt_binds_the_rules(admitted):
    _, path = admitted
    policied = api.KnowledgeChangeHistory.reopen(path).replay()
    contract = content.load_contract()
    receipts = [
        json.loads(policied.retained_bytes(member.record_id))
        for member in policied.retained_inputs
        if member.record_id.startswith("receipt:")
    ]
    assert len(receipts) == 21
    for receipt in receipts:
        assert receipt["check"]["contract_hash"] == contract.contract_hash
        assert receipt["check"]["ruleset_hash"] == contract.ruleset_hash
        assert receipt["check"]["violations"] == []
        assert sorted(receipt["check"]["checked_rule_ids"]) == sorted(contract.rule_ids)


def test_reopen_is_stable(admitted):
    report, path = admitted
    assert (
        api.KnowledgeChangeHistory.reopen(path).replay().receipt.identity
        == (report["history_identity"])
    )


@pytest.fixture(scope="module")
def policied_clean(tmp_path_factory):
    """The honest rows alone, so the ledger difference is only the policy."""
    path = tmp_path_factory.mktemp("content-rules-clean") / "history.jsonl"
    return content.run(path, probe=False), path


def ledger_records(path):
    """Every retention event in one ledger, as record ID to retained digest."""
    retained = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        if entry["event_type"] in ("ARTIFACT_REGISTERED", "SOURCE_REGISTERED"):
            payload = entry["payload"]
            retained[payload["record_id"]] = payload["retained_sha256"]
    return retained


def ledger_types(path):
    counts = {}
    for line in path.read_text().splitlines():
        if line.strip():
            name = json.loads(line)["event_type"]
            counts[name] = counts.get(name, 0) + 1
    return counts


def test_only_retention_events_differ(policied_clean, connected):
    """The policy adds retained artifacts; it changes no other event count."""
    _, path = policied_clean
    _, other = connected
    mine, theirs = ledger_types(path), ledger_types(other)
    assert mine.pop("ARTIFACT_REGISTERED") == 57
    assert theirs.pop("ARTIFACT_REGISTERED") == 35
    assert mine == theirs
    assert mine == {
        "CHANGE_PROPOSED": 21,
        "CHECK_RECORDED": 21,
        "KNOWLEDGE_CHANGE_SET_RETAINED": 21,
        "SOURCE_REGISTERED": 2,
        "VERDICT_RECORDED": 21,
    }


def test_added_and_removed_retentions_are_the_rule_layer(policied_clean, connected):
    _, path = policied_clean
    _, other = connected
    mine, theirs = ledger_records(path), ledger_records(other)
    added = set(mine) - set(theirs)
    assert added == {content.LOGIC_ID, content.RULES_ID} | {
        f"receipt:change:plan:shop-connected:{row['event_id']}"
        for row in story.load_sources(story.HERE)[0]
    }
    assert set(theirs) - set(mine) == {"malleus:structural-admission-check/v1"}


def test_shared_retentions_differ_only_where_the_contract_is_bound(
    policied_clean, connected
):
    _, path = policied_clean
    _, other = connected
    mine, theirs = ledger_records(path), ledger_records(other)
    shared = set(mine) & set(theirs)
    differing = {key for key in shared if mine[key] != theirs[key]}
    assert differing == {"malleus:bootstrap:partial-effective-contract"} | {
        f"plan:shop-connected:{row['event_id']}"
        for row in story.load_sources(story.HERE)[0]
    }
    assert len(shared - differing) == 14
    assert (
        mine["malleus:bootstrap:validated-contract"]
        == (theirs["malleus:bootstrap:validated-contract"])
    )

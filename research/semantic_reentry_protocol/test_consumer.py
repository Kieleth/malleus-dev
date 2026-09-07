"""Consumer RED: local request policy, not a substitute KCS composition API."""

from copy import deepcopy
from dataclasses import FrozenInstanceError
from importlib import import_module
import json
from pathlib import Path

import pytest

import malleus.compiler as api
from research.semantic_reentry_protocol.test_prerequisites import (
    ACTOR, E4, E7, MAPPING, SOURCE, TIME,
    admit, artifact, canonical, compilation, digest, load_plan, prepare, shop,
)


MECHANISM = digest(b"semantic-reentry-policy-test-mechanism/v1")
PRESERVED = ("O1", "X1", "contains:O1:X1")


def consumer():
    # Deferred import keeps RED collection possible without an implementation.
    return import_module("research.semantic_reentry_protocol.consumer")


def view_bytes(replay):
    """Read-model from real replay, not a Core composition context."""
    return canonical({
        "coordinates": {
            "ledger_head": replay.ledger_head,
            "ledger_event_count": replay.ledger_event_count,
            "acceptance_head": replay.acceptance_head,
            "materialization_head": replay.materialization_head,
            "graph_state_digest": replay.graph.state_digest(),
            "contract_identity": replay.partial_contract.identity,
            "receipt_identity": replay.receipt.identity,
        },
        "records": replay.graph.export_records(),
        "record_history": {
            record_id: {
                "supersedes_record_id": member.supersedes_record_id,
                "superseded_by": member.superseded_by,
                "valid_from": {"kind": member.valid_from.kind,
                               "value": member.valid_from.value},
            }
            for record_id, member in replay.record_history.items()
        },
        "retained": {
            member.record_id: {"sha256": member.identity, "role": member.role}
            for member in replay.retained_inputs
        },
    })


def bundle(history):
    replay = history.replay()
    view = view_bytes(replay)
    plan = canonical(load_plan(history, "supplier-e7"))
    source = replay.retained_bytes(SOURCE)
    mapping = replay.retained_bytes(MAPPING)
    contract = {
        "grammar": "malleus.semantic-reentry.shop-consumer/research-v0",
        "input_kind": "ViewDelta",
        "output_kind": "KnowledgeChangeSet",
        "base": json.loads(view)["coordinates"],
        "projection_sha256": digest(view),
        "request": {
            "plan_sha256": digest(plan), "source_sha256": digest(source),
            "mapping_sha256": digest(mapping), "source_id": SOURCE,
            "mapping_id": MAPPING, "occurrence_id": "e7",
            "prior_record_id": E4, "target_record_id": E7,
        },
        "permitted_operations": ["CREATE_ENTITY"],
        "update_strategy": "EXPLICIT_MAPPING_SUPERSESSION",
        "preservation": "EXACT_COMPLEMENT",
        "ambiguity_strategy": "REFUSE_IF_NOT_UNIQUE",
        "candidate_budget": 1,
        "stopping_rule": "EXACT_TARGET_AND_SUPERSESSION",
        "synthesizer_identity": MECHANISM,
    }
    return {"contract": contract, "view_bytes": view, "plan_bytes": plan,
            "source_bytes": source, "mapping_bytes": mapping}


def assess(sut, request):
    contract = sut.ReentryContract.from_bytes(canonical(request["contract"]))
    return sut.assess_request(
        contract=contract, view_bytes=request["view_bytes"],
        plan_bytes=request["plan_bytes"], source_bytes=request["source_bytes"],
        mapping_bytes=request["mapping_bytes"], synthesizer_identity=MECHANISM,
    )


def refused(sut, request, reason):
    with pytest.raises(sut.ReentryRefusal) as refusal:
        assess(sut, request)
    assert refusal.value.reason.value == reason


def edit_plan(request, edit):
    plan = json.loads(request["plan_bytes"])
    edit(plan)
    request["plan_bytes"] = canonical(plan)
    # Rebind the input hash to test policy, not merely digest mismatch.
    request["contract"]["request"]["plan_sha256"] = digest(request["plan_bytes"])


def test_policy_fixture_is_real_e4_and_requires_no_plan_retention(shop):
    history, path = shop
    before = path.read_bytes()
    request = bundle(history)
    view = json.loads(request["view_bytes"])
    assert set(view["record_history"]) == {*PRESERVED, E4}
    assert "plan:small-shop:supplier-e7" not in view["retained"]
    assert request["contract"]["base"]["receipt_identity"] == history.replay().receipt.identity
    assert path.read_bytes() == before


def test_contract_round_trip_and_nested_immutability(shop):
    sut = consumer()
    request = bundle(shop[0])
    wire = canonical(request["contract"])
    contract = sut.ReentryContract.from_bytes(wire)
    assert contract.canonical_bytes == wire
    assert contract.identity == digest(wire)
    assert sut.ReentryContract.from_bytes(contract.canonical_bytes) == contract
    with pytest.raises((FrozenInstanceError, AttributeError)):
        contract.canonical_bytes = b"{}"
    with pytest.raises(TypeError):
        contract.data["request"]["target_record_id"] = "changed"


@pytest.mark.parametrize("field", [
    "grammar", "input_kind", "output_kind", "base", "projection_sha256",
    "request", "permitted_operations", "update_strategy", "preservation",
    "ambiguity_strategy", "candidate_budget", "stopping_rule", "synthesizer_identity",
])
def test_contract_missing_required_field_refuses(shop, field):
    sut = consumer()
    request = bundle(shop[0])
    del request["contract"][field]
    refused(sut, request, "MALFORMED_CONTRACT")


@pytest.mark.parametrize("change", [
    {"undeclared": True}, {"candidate_budget": True}, {"candidate_budget": -1},
    {"request": {}}, {"base": {}},
])
def test_contract_unknown_or_malformed_fields_refuse(shop, change):
    sut = consumer()
    request = bundle(shop[0])
    request["contract"].update(change)
    refused(sut, request, "MALFORMED_CONTRACT")


def test_noncanonical_contract_refuses(shop):
    sut = consumer()
    wire = json.dumps(bundle(shop[0])["contract"], indent=2).encode()
    with pytest.raises(sut.ReentryRefusal) as refusal:
        sut.ReentryContract.from_bytes(wire)
    assert refusal.value.reason.value == "NONCANONICAL_CONTRACT"


@pytest.mark.parametrize("field,value", [
    ("input_kind", "GoalPredicate"), ("output_kind", "ActionProposal"),
    ("update_strategy", "LAST_ROW_WINS"), ("preservation", "NONE"),
    ("ambiguity_strategy", "FIRST"), ("stopping_rule", "QUANTITY_ONLY"),
    ("permitted_operations", ["CREATE_RELATION"]),
])
def test_undeclared_policy_or_operator_refuses(shop, field, value):
    sut = consumer()
    request = bundle(shop[0])
    request["contract"][field] = value
    refused(sut, request, "UNSUPPORTED_CONTRACT")


def test_ready_finding_is_deterministic_and_changes_only_declared_fields(shop):
    sut = consumer()
    history, path = shop
    request = bundle(history)
    before = path.read_bytes()
    result = assess(sut, request)
    assert result == assess(sut, deepcopy(request))
    assert result.status.value == "READY"
    assert result.changed_fields == ("ordered_quantity", "source_occurrence_id")
    assert result.preserved_record_ids == PRESERVED
    assert not isinstance(result, api.KnowledgeChangeSet)
    assert path.read_bytes() == before
    with pytest.raises((FrozenInstanceError, AttributeError)):
        result.changed_fields = ()


def test_assessment_never_reads_or_writes_ambient_state(shop, monkeypatch):
    sut = consumer()
    history, path = shop
    request = bundle(history)
    before = path.read_bytes()

    def forbidden(*args, **kwargs):
        raise AssertionError("pure request assessment attempted ambient access")

    with monkeypatch.context() as blocked:
        for method in ("open", "read_bytes", "read_text", "write_bytes", "write_text"):
            blocked.setattr(Path, method, forbidden)
        for method in ("replay", "admit", "append_anchors", "compose_change_set"):
            blocked.setattr(api.KnowledgeChangeHistory, method, forbidden)
        assert assess(sut, request).status.value == "READY"
    assert path.read_bytes() == before


@pytest.mark.parametrize("value_kind", ["writer", "mutable_replay"])
def test_writer_and_mutable_replay_are_not_policy_inputs(shop, value_kind):
    sut = consumer()
    history, path = shop
    request = bundle(history)
    request["view_bytes"] = history if value_kind == "writer" else history.replay()
    before = path.read_bytes()
    refused(sut, request, "MALFORMED_INPUT")
    assert path.read_bytes() == before


@pytest.mark.parametrize("field,value", [
    ("ordered_quantity", 999), ("product_code", "Z"),
    ("supplier_order_id", "C"), ("source_occurrence_id", "e4"),
])
def test_cited_source_values_must_agree_with_proposed_properties(shop, field, value):
    sut = consumer()
    history, path = shop
    request = bundle(history)
    edit_plan(request, lambda plan: plan["records"]["entities"][0]["properties"].update({field: value}))
    before = path.read_bytes()
    refused(sut, request, "SOURCE_DISAGREEMENT")
    assert path.read_bytes() == before


@pytest.mark.parametrize("input_name", ["plan_bytes", "source_bytes", "mapping_bytes"])
def test_substituted_input_bytes_refuse(shop, input_name):
    sut = consumer()
    request = bundle(shop[0])
    request[input_name] += b"\n"
    refused(sut, request, "INPUT_IDENTITY_MISMATCH")


def test_synthesizer_identity_cannot_be_substituted(shop):
    sut = consumer()
    request = bundle(shop[0])
    request["contract"]["synthesizer_identity"] = digest(b"different-mechanism")
    refused(sut, request, "SYNTHESIZER_MISMATCH")


@pytest.mark.parametrize("edit", [
    lambda plan: plan["supersessions"][0].update({"supersedes_record_id": "O1"}),
    lambda plan: plan.update({"supersessions": []}),
    lambda plan: plan.update({"valid_time": {"kind": "NONE_STATED", "value": None}}),
    lambda plan: plan["records"]["entities"][0].update({"type": "InventoryUnit"}),
])
def test_replacement_semantics_must_match_explicit_mapping(shop, edit):
    sut = consumer()
    request = bundle(shop[0])
    edit_plan(request, edit)
    refused(sut, request, "UNSUPPORTED_CHANGE")


def test_extra_structurally_valid_entity_violates_preservation(shop):
    sut = consumer()
    request = bundle(shop[0])
    edit_plan(request, lambda plan: plan["records"]["entities"].append({
        "id": "extra", "type": "InventoryUnit", "properties": {"product_code": "X"}}))
    refused(sut, request, "PRESERVATION_VIOLATION")


def test_competing_mapping_matches_refuse_without_implicit_selection(shop):
    sut = consumer()
    history, path = shop
    mapping = json.loads(history.replay().retained_bytes(MAPPING))
    mapping["changes"].append(deepcopy(mapping["changes"][1]))
    content = canonical(mapping)
    record_id = "artifact:negative-test:ambiguous-mapping"
    # Retain adversarial evidence in this test's ledger, never edit Shop inputs.
    history.append_anchors(anchors=(artifact(record_id, content),),
                           transaction_time=TIME, actor_id=ACTOR)
    request = bundle(history)
    request["mapping_bytes"] = content
    request["contract"]["request"].update({
        "mapping_id": record_id, "mapping_sha256": digest(content)})
    edit_plan(request, lambda plan: plan.update({"evidence": [
        {"evidence_id": record_id, "sha256": digest(content)}]}))
    before = path.read_bytes()
    refused(sut, request, "AMBIGUOUS")
    assert path.read_bytes() == before


def test_zero_budget_refuses_unsatisfied_request(shop):
    sut = consumer()
    request = bundle(shop[0])
    request["contract"]["candidate_budget"] = 0
    refused(sut, request, "BUDGET_EXHAUSTED")


def test_evidence_only_append_stales_the_bound_request(shop):
    sut = consumer()
    history, path = shop
    request = bundle(history)
    old_graph = history.replay().graph.state_digest()
    history.append_anchors(anchors=(artifact("artifact:policy-head-change", b"{}"),),
                           transaction_time=TIME, actor_id=ACTOR)
    assert history.replay().graph.state_digest() == old_graph
    request["view_bytes"] = view_bytes(history.replay())
    before = path.read_bytes()
    refused(sut, request, "STALE_BASE")
    assert path.read_bytes() == before


def test_exact_observed_success_is_noop_even_with_zero_budget(shop):
    sut = consumer()
    history, path = shop
    # Core creates the satisfied fixture; no Re-entry E2E is claimed here.
    admit(history, prepare(history, load_plan(history, "supplier-e7")))
    request = bundle(history)
    request["contract"]["candidate_budget"] = 0
    before = path.read_bytes()
    result = assess(sut, request)
    assert result.status.value == "SATISFIED"
    assert result.changed_fields == ()
    assert result.preserved_record_ids == PRESERVED
    assert path.read_bytes() == before


def test_staleness_precedes_satisfied_goal_shortcut(shop):
    sut = consumer()
    history, path = shop
    old_request = bundle(history)
    admit(history, prepare(history, load_plan(history, "supplier-e7")))
    old_request["view_bytes"] = view_bytes(history.replay())
    before = path.read_bytes()
    refused(sut, old_request, "STALE_BASE")
    assert path.read_bytes() == before


def test_equal_quantity_with_wrong_occurrence_is_not_quiescence(shop):
    sut = consumer()
    history, path = shop
    wrong = load_plan(history, "supplier-e7")
    wrong["records"]["entities"][0]["properties"]["source_occurrence_id"] = "e4"
    # Structural admission does not establish source truth. Negative fixture only.
    admit(history, prepare(history, wrong))
    request = bundle(history)
    before = path.read_bytes()
    refused(sut, request, "STATE_CONFLICT")
    assert path.read_bytes() == before

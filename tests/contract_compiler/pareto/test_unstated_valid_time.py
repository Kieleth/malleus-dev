"""No source time is not a fabricated instant or a domain-order claim."""

from copy import deepcopy
import json

import pytest

import malleus.compiler as api
from tests.contract_compiler.pareto.test_public_compiler import (
    ROOT,
    SHOP_FIXTURE,
    _canonical,
    _compiled_shop,
    _digest,
    _event,
    _plan,
)


TIME = "2026-09-06T00:00:00Z"
ACTOR = "actor:shop-unstated-time"
NONE_STATED = {"kind": "NONE_STATED", "value": None}


@pytest.fixture
def shop(tmp_path):
    source = (SHOP_FIXTURE / "input/sources/supplier-order-history.jsonl").read_bytes()
    history = api.create_structural_history(
        tmp_path / "history.jsonl",
        compilation=_compiled_shop(api),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    for event, role in (
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="artifact:supplier-orders",
                artifact_identity=_digest(source),
            ),
            "SOURCE_ARTIFACT",
        ),
        (
            _event(
                "SOURCE_REGISTERED",
                artifact_id="artifact:supplier-orders",
                source_id="source:supplier-order-history",
                source_identity=_digest(source),
            ),
            "RETAINED_SOURCE",
        ),
    ):
        history.append_anchor(
            machine_event=event,
            retained_bytes=source,
            media_type="application/x-ndjson",
            role=role,
            transaction_time=TIME,
            actor_id=ACTOR,
        )
    return history, source, tmp_path / "history.jsonl"


def _prepare(shop, occurrence, valid_time, *, replacement=False):
    history, source, _ = shop
    plan = _plan(api, history.partial_contract, source, occurrence)
    plan["valid_time"] = deepcopy(valid_time)
    if not replacement:
        plan["supersessions"] = []
    replay = history.replay()
    profile = api.STATE_VERSION_PROFILE
    compiled = api.compile_population_plan(
        plan,
        partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=api.PopulationBaseState.from_replay(replay),
        history_profile=profile,
    )
    return api.prepare_population_change(
        history=history,
        plan=plan,
        profile=json.loads(profile.canonical_bytes),
        retention_events=api.population_retention_events(
            history=history, compilation=compiled, profile=profile
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )


def _admit(shop, occurrence, valid_time, *, replacement=False):
    prepared = _prepare(shop, occurrence, valid_time, replacement=replacement)
    assert prepared.change_set is not None
    wire = prepared.change_set.canonical_bytes
    assert json.loads(wire)["valid_time"] == valid_time
    assert api.KnowledgeChangeSet.from_bytes(wire).canonical_bytes == wire
    return api.admit_structural_change(
        history=shop[0], preparation=prepared, transaction_time=TIME, actor_id=ACTOR
    )


@pytest.mark.parametrize("replacement", [False, True])
def test_shop_unstated_time_admits_reopens_and_traces_without_inventing_order(
    shop, replacement
):
    _admit(shop, "e4", NONE_STATED)
    final = _admit(shop, "e7", NONE_STATED, replacement=replacement)
    _, source, path = shop
    before = path.read_bytes()
    replay = api.KnowledgeChangeHistory.reopen(path).replay()
    assert replay.receipt == final.receipt
    rows = replay.graph.query(entity_type="SupplierOrderState")
    assert sorted(row["ordered_quantity"] for row in rows) == (
        [2] if replacement else [1, 2]
    )
    old = replay.record_history["supplier-order-state:B:e4"]
    assert old.superseded_by == ("supplier-order-state:B:e7" if replacement else None)
    assert old.valid_to == (
        api.KnowledgeValidTime("NONE_STATED", None) if replacement else None
    )
    for occurrence in ("e4", "e7"):
        trace = api.trace_population_record(
            replay, f"supplier-order-state:B:{occurrence}"
        )
        assert trace.change_set.valid_time == api.KnowledgeValidTime(
            "NONE_STATED", None
        )
        assert trace.record_history.valid_from == trace.change_set.valid_time
        assert trace.population_plan["valid_time"] == NONE_STATED
        assert trace.sources[0].content == source
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "invalid",
    [
        None,
        {},
        {"kind": "NONE_STATED"},
        {"kind": "NONE_STATED", "value": ""},
        {"kind": "NONE_STATED", "value": "e4"},
        {"kind": "NONE_STATED", "value": False},
        {"kind": "NONE_STATED", "value": None, "reason": "unknown"},
        {"kind": "ORDER_ONLY", "value": None},
        {"kind": "INSTANT", "value": None},
    ],
)
def test_malformed_time_refuses_in_plan_and_change_set_without_writes(shop, invalid):
    # Obtain a valid existing-kind envelope without relying on the new branch.
    prepared = _prepare(shop, "e4", {"kind": "ORDER_ONLY", "value": "e4"})
    payload = json.loads(prepared.change_set.canonical_bytes)
    before = shop[2].read_bytes()
    with pytest.raises(api.PopulationPlanRefusal) as error:
        _prepare(shop, "e7", invalid)
    assert error.value.reason == api.PopulationPlanRefusalReason.UNSUPPORTED_VALID_TIME
    payload["valid_time"] = invalid
    with pytest.raises(api.KnowledgeChangeRefusal) as error:
        api.KnowledgeChangeSet.from_bytes(_canonical(payload))
    assert error.value.reason == api.KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET
    assert shop[2].read_bytes() == before


@pytest.mark.parametrize(
    "other",
    [{"kind": "ORDER_ONLY", "value": "e7"}, {"kind": "INSTANT", "value": TIME}],
)
@pytest.mark.parametrize("unstated_first", [False, True])
def test_cross_kind_replacement_refuses_before_retention(shop, other, unstated_first):
    first, second = (NONE_STATED, other) if unstated_first else (other, NONE_STATED)
    _admit(shop, "e4", first)
    before = shop[2].read_bytes()
    with pytest.raises(api.PopulationPlanRefusal) as error:
        _prepare(shop, "e7", second, replacement=True)
    assert (
        error.value.reason
        == api.PopulationPlanRefusalReason.SUPERSESSION_VALID_TIME_MISMATCH
    )
    assert shop[2].read_bytes() == before


def test_skill_missing_time_example_passes_the_public_plan_and_history(shop):
    skill = (ROOT / ".claude/skills/malleus-acolyte/SKILL.md").read_text()
    section = skill.split("### Missing valid time", 1)[1]
    example = json.loads(section.split("```json\n", 1)[1].split("```", 1)[0])
    assert example == {"valid_time": NONE_STATED}
    _admit(shop, "e4", example["valid_time"])

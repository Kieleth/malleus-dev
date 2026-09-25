"""Authored temporal controls, using the public compiler/history boundary."""

from datetime import datetime
from importlib.resources import files
import json
from pathlib import Path

import pytest

import malleus.compiler as api
from malleus.valid_time import BoundaryRelation, ValidTime


ROOT = Path(__file__).resolve().parents[3]
TX = "2026-09-24T00:00:00+00:00"
MAY_1 = "2026-05-01T00:00:00+00:00"
MAY_12 = "2026-05-12T00:00:00+00:00"
SCHEMA = b"""\
id: https://example.malleus.dev/temporal-control
name: temporal_control
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
imports:
  - linkml:types
  - malleus
slots:
  price_cents:
    range: integer
    required: true
classes:
  PriceState:
    is_a: Entity
    slots: [price_cents]
"""


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


@pytest.fixture(scope="module")
def compilation():
    return api.compile_linkml_contract(
        root_locator="temporal-control",
        sources={
            "temporal-control": SCHEMA,
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model", "model", "schema", "types.yaml")
            .read_bytes(),
        },
    )


@pytest.fixture
def history(tmp_path, compilation):
    return api.create_structural_history(
        tmp_path / "history.jsonl",
        compilation=compilation,
        transaction_time=TX,
        actor_id="actor:temporal-control",
    )


def proposed(history, identifier, price, valid_from, *, supersedes=None):
    """Author a source and one exact record, without an extraction claim."""
    content = canonical(
        {"id": identifier, "price_cents": price, "valid_from": valid_from}
    )
    source_id = f"source:{identifier}"
    evidence_id = f"evidence:{identifier}"
    history.append_anchors(
        anchors=(
            *api.structural_source_anchors(
                source_id=source_id,
                artifact_id=f"artifact:{identifier}",
                content=content,
                media_type="application/json",
            ),
            api.structural_evidence_anchor(
                record_id=evidence_id,
                content=b"Authored synthetic control, not extracted prose.",
                media_type="text/plain",
            ),
        ),
        transaction_time=TX,
        actor_id="actor:temporal-control",
    )
    return history.compose_change_set(
        change_set_id=f"change:{identifier}",
        source_record_ids=(source_id,),
        evidence_record_ids=(evidence_id,),
        operations=(
            api.KnowledgeOperation(
                ordinal=0,
                operation_id=f"operation:{identifier}",
                operation_type="CREATE_ENTITY",
                record_type="PriceState",
                record_id=identifier,
                properties={"price_cents": price},
                depends_on=(),
                supersedes_record_id=supersedes,
            ),
        ),
        valid_time=api.KnowledgeValidTime.from_data(valid_from),
        supersedes=(),
    )


def accept(history, change):
    return api.check_and_admit_change_set(
        history=history,
        change_set=change,
        transaction_time=TX,
        actor_id="actor:temporal-control",
    ).replay


@pytest.fixture
def episode(history):
    original = proposed(history, "price:old", 750, {"kind": "INSTANT", "value": MAY_1})
    before = accept(history, original)
    replacement = proposed(
        history,
        "price:new",
        800,
        {"kind": "INSTANT", "value": MAY_12},
        supersedes="price:old",
    )
    after = accept(history, replacement)
    return history, before, after


def test_baseline_retains_old_graph_and_declared_transition(episode):
    history, before, after = episode
    assert after.graph.get_node("price:new")["price_cents"] == 800
    assert after.graph.get_node("price:old") is None
    assert (
        after.graph_at_change("change:price:old").snapshot() == before.graph.snapshot()
    )
    assert after.record_history["price:old"].valid_to.value == MAY_12
    assert (
        api.KnowledgeChangeHistory.reopen(history.path).replay().receipt
        == after.receipt
    )


def test_baseline_same_period_correction_refuses_without_admission_writes(history):
    accept(
        history,
        proposed(history, "price:old", 750, {"kind": "INSTANT", "value": MAY_1}),
    )
    correction = proposed(
        history,
        "price:corrected",
        800,
        {"kind": "INSTANT", "value": MAY_1},
        supersedes="price:old",
    )
    # Source retention above is a separate explicit act. The refusal measured
    # here is the admission, not a claim that no evidence was ever retained.
    before = history.path.read_bytes()
    with pytest.raises(api.PopulationAdmissionRefusal) as failure:
        accept(history, correction)
    assert failure.value.stage is api.PopulationAdmissionStage.CHECK
    assert "valid time" in str(failure.value).lower()
    assert history.path.read_bytes() == before
    assert history.replay().graph.get_node("price:old")["price_cents"] == 750


def test_baseline_unstated_time_does_not_invent_a_date(history):
    unknown = {"kind": "NONE_STATED", "value": None}
    accept(history, proposed(history, "price:old", 750, unknown))
    final = accept(
        history, proposed(history, "price:new", 800, unknown, supersedes="price:old")
    )
    old = final.record_history["price:old"]
    assert old.valid_from == old.valid_to == api.KnowledgeValidTime("NONE_STATED", None)


def test_baseline_latest_graph_is_not_a_domain_time_view(history):
    accept(
        history,
        proposed(history, "price:old", 750, {"kind": "INSTANT", "value": MAY_1}),
    )
    future = "2026-12-01T00:00:00+00:00"
    latest = accept(
        history,
        proposed(
            history,
            "price:future",
            800,
            {"kind": "INSTANT", "value": future},
            supersedes="price:old",
        ),
    )
    # Admission in September is before the declared December transition.
    # The existing graph is latest accepted version selection, NOT a claim
    # that the December price already applies at the admission time.
    assert latest.graph.get_node("price:future")["price_cents"] == 800
    assert latest.graph.get_node("price:old") is None
    assert latest.record_history["price:old"].valid_to.value == future
    assert (
        latest.graph_at_change("change:price:old").get_node("price:old")["price_cents"]
        == 750
    )


def test_baseline_cannot_correct_a_previously_retired_period(episode):
    history, _, _ = episode
    correction = proposed(
        history,
        "price:corrected-past",
        775,
        {"kind": "INSTANT", "value": MAY_1},
        supersedes="price:old",
    )
    original = history.path.read_bytes()
    with pytest.raises(api.PopulationAdmissionRefusal) as failure:
        accept(history, correction)
    assert failure.value.stage is api.PopulationAdmissionStage.CHECK
    assert "forks prior record" in str(failure.value)
    assert history.path.read_bytes() == original
    assert history.replay().graph.get_node("price:new")["price_cents"] == 800


def test_baseline_existing_precision_boundary_does_not_guess():
    boundary = ValidTime.bounded_interval(
        "2026-06-03T09:00:00+00:00",
        "2026-06-03T10:00:00+00:00",
        indeterminacy_reason="The source supplies a transition window only.",
    )
    for instant, expected in (
        ("2026-06-03T08:59:59+00:00", BoundaryRelation.BEFORE),
        ("2026-06-03T09:30:00+00:00", BoundaryRelation.INDETERMINATE),
        ("2026-06-03T10:00:01+00:00", BoundaryRelation.AFTER),
    ):
        assert boundary.relation_at(datetime.fromisoformat(instant)) is expected


def test_control_catalogue_keeps_correction_distinct_from_transition():
    catalogue = json.loads((ROOT / "design/temporal/situations.json").read_bytes())
    cases = {case["id"]: case for case in catalogue["cases"]}
    assert len(cases) == 6
    assert cases["T-WORLD-CHANGE"]["expected"][0]["price_cents"] == 750
    assert cases["T-REPORT-CORRECTION"]["expected"][1]["price_cents"] == 800
    assert cases["T-CALCULATION-PREMISES"]["expected"][2]["state"] == "NOT_COMPUTED"

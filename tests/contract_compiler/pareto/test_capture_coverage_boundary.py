"""Synthetic Shop conformance: mapping counts are not semantic completeness."""

from copy import deepcopy
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import pytest

from malleus import bundled_ontology_path
import malleus.compiler as api
from malleus.inquisition.cli import main as inquisitor


ROOT = Path(__file__).resolve().parents[3]
TIME = "2026-01-01T00:00:00Z"
ACTOR = "actor:shop-capture-fixture"
NOTE = (
    "The clerk reports stock of 2 units and a request for 2 units. "
    "This stock count supports the claim that the request can be filled."
)
SCHEMA = b"""id: https://example.org/shop-capture
name: shop_capture
imports: [linkml:types, malleus]
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
classes:
  ReportedQuantity:
    is_a: Entity
    slots: [quantity]
  ReportedClaim:
    is_a: Entity
    slots: [statement]
  ShopSupports:
    is_a: Relation
    slot_usage:
      relation_type:
        range: ShopRelationType
slots:
  quantity:
    range: integer
    required: true
enums:
  ShopRelationType:
    permissible_values:
      SUPPORTS:
"""
LABELS = {
    "FULLY_FORMALIZED": "Mapped fields, no declared gaps",
    "PARTLY_FORMALIZED": "Mapped fields and declared gaps",
    "UNFORMALIZED": "No mapped fields",
}


def _canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def _digest(value):
    return "sha256:" + sha256(value).hexdigest()


def _case(*, relation=False, gap=False):
    reading = _canonical(
        {
            "pages": [
                {
                    "blocks": [
                        {"id": "shop-note", "ordinal": 0, "text": NOTE},
                    ]
                }
            ]
        }
    )
    records = {
        "entities": [
            {
                "id": "count:stock",
                "type": "ReportedQuantity",
                "properties": {"quantity": 2},
            },
            {
                "id": "count:request",
                "type": "ReportedQuantity",
                "properties": {"quantity": 2},
            },
            {
                "id": "claim:fill",
                "type": "ReportedClaim",
                "properties": {"statement": "the request can be filled"},
            },
        ],
        "relations": [],
    }
    targets = [
        {"record_id": record["id"], "path": ["properties", key]}
        for record in records["entities"]
        for key in record["properties"]
    ]
    if relation:
        records["relations"].append(
            {
                "id": "support:stock:fill",
                "type": "ShopSupports",
                "source_id": "count:stock",
                "target_id": "claim:fill",
                "properties": {"relation_type": "SUPPORTS"},
            }
        )
        targets.extend(
            {"record_id": "support:stock:fill", "path": path}
            for path in (["source_id"], ["target_id"], ["properties", "relation_type"])
        )
    capture = {
        "schema": api.DOCUMENT_CAPTURE_GRAMMAR,
        "reading_sha256": _digest(reading),
        "attribution": {
            "author": "Synthetic shop clerk",
            "date": "2026-01-01",
            "source_id": "source:shop-note",
        },
        "nothing_assertable": [],
        "assertions": [
            {
                "id": "assertion:shop",
                "block": "shop-note",
                "statement": NOTE,
                "modality": "STATED",
                "formalized_by": targets,
                "gaps": (
                    [
                        {
                            "kind": "MODALITY_NOT_EXPRESSIBLE",
                            "statement": "The fixture records do not carry STATED modality.",
                        }
                    ]
                    if gap
                    else []
                ),
            }
        ],
    }
    return reading, capture, records


def _history(tmp_path, reading, capture):
    compiled = api.compile_linkml_contract(
        root_locator="shop",
        sources={
            "shop": SCHEMA,
            "malleus": bundled_ontology_path("malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    )
    history = api.create_structural_history(
        tmp_path / "history.jsonl",
        compilation=compiled,
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    anchors = []
    for event_type, payload, content, role in (
        (
            "ARTIFACT_REGISTERED",
            {
                "artifact_id": "artifact:shop-note",
                "artifact_identity": _digest(reading),
            },
            reading,
            "SOURCE_ARTIFACT",
        ),
        (
            "SOURCE_REGISTERED",
            {
                "artifact_id": "artifact:shop-note",
                "source_id": "source:shop-note",
                "source_identity": _digest(reading),
            },
            reading,
            "RETAINED_SOURCE",
        ),
        (
            "ARTIFACT_REGISTERED",
            {
                "artifact_id": "capture:shop-note",
                "artifact_identity": _digest(_canonical(capture)),
            },
            _canonical(capture),
            "RETAINED_EVIDENCE",
        ),
    ):
        anchors.append(
            api.KnowledgeAnchorInput(
                machine_event=_canonical(
                    {"event_type": event_type, "payload": payload}
                ),
                retained_bytes=content,
                media_type="application/json",
                role=role,
            )
        )
    history.append_anchors(
        anchors=tuple(anchors), transaction_time=TIME, actor_id=ACTOR
    )
    return history, compiled


def _adapt(history, compiled, reading, capture, records):
    return api.adapt_document_assertions(
        reading_bytes=reading,
        capture_bytes=_canonical(capture),
        capture_id="capture:shop-note",
        plan_id="plan:shop-note",
        contract_identity=history.partial_contract.identity,
        records=records,
        supersessions=[],
        contract_view=compiled.view,
    )


def _prepare(history, adapted):
    plan = json.loads(adapted.canonical_plan_bytes)
    profile = api.SOURCE_ASSERTION_PROFILE
    replay = history.replay()
    compilation = api.compile_population_plan(
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
            history=history, compilation=compilation, profile=profile
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )


@pytest.mark.parametrize("relation", [False, True])
def test_shop_replay_contains_only_supplied_relationships(tmp_path, relation):
    reading, capture, records = _case(relation=relation)
    history, compiled = _history(tmp_path, reading, capture)
    adapted = _adapt(history, compiled, reading, capture, records)
    census = json.loads(adapted.canonical_census_bytes)
    assert census["assertions"] == {
        "FULLY_FORMALIZED": 1,
        "PARTLY_FORMALIZED": 0,
        "UNFORMALIZED": 0,
    }
    admitted = api.admit_structural_change(
        history=history,
        preparation=_prepare(history, adapted),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    replay = api.KnowledgeChangeHistory.reopen(history.path).replay()
    assert replay.receipt == admitted.receipt
    assert len(replay.graph.query_relations("ShopSupports")) == int(relation)
    assert replay.graph.get_node("count:stock")["quantity"] == 2
    assert replay.graph.get_node("count:request")["quantity"] == 2
    assert "name" not in replay.graph.get_node("claim:fill")
    trace = api.trace_population_record(replay=replay, record_id="claim:fill")
    assert any(item.record_id == "capture:shop-note" for item in trace.evidence)
    assert _canonical(capture) == adapted.capture_bytes


def test_declared_gap_changes_accounting_not_missing_relation_detection(tmp_path):
    reading, capture, records = _case(gap=True)
    history, compiled = _history(tmp_path, reading, capture)
    adapted = _adapt(history, compiled, reading, capture, records)
    assert json.loads(adapted.canonical_census_bytes)["assertions"] == {
        "FULLY_FORMALIZED": 0,
        "PARTLY_FORMALIZED": 1,
        "UNFORMALIZED": 0,
    }
    assert json.loads(adapted.canonical_plan_bytes)["records"]["relations"] == []


def test_supplied_dangling_relationship_refuses_before_writing(tmp_path):
    reading, capture, records = _case(relation=True)
    records = deepcopy(records)
    records["relations"][0]["target_id"] = "claim:absent"
    history, compiled = _history(tmp_path, reading, capture)
    adapted = _adapt(history, compiled, reading, capture, records)
    before = history.path.read_bytes()
    with pytest.raises(api.PopulationPlanRefusal) as refusal:
        _prepare(history, adapted)
    assert refusal.value.reason is api.PopulationPlanRefusalReason.DANGLING_ENDPOINT
    assert history.path.read_bytes() == before
    assert (
        api.KnowledgeChangeHistory.reopen(history.path).replay().graph.query_relations()
        == []
    )


def _assert_guidance(text):
    normalized = " ".join(text.split())
    for value, label in LABELS.items():
        assert f"`{value}` | {label}" in normalized
    assert "Semantic completeness is not assessed" in normalized
    assert "proposition identity" in normalized
    assert "optional label" in normalized
    assert "retained context and attribution" in normalized
    assert "direction and endpoints" in normalized
    assert (
        "A relation's endpoints are formalized by an assertion whose statement names both"
        not in normalized
    )


def test_public_census_explanation_states_the_executable_limit():
    _assert_guidance((ROOT / "docs/contract_compiler/index.md").read_text())


def test_installed_acolyte_states_the_same_limit(tmp_path):
    assert (
        inquisitor(["install-skills", "--agent", "codex", "--project", str(tmp_path)])
        == 0
    )
    _assert_guidance((tmp_path / ".codex/skills/malleus-acolyte/SKILL.md").read_text())

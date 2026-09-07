"""Executable baseline audit, not a Semantic Re-entry implementation.

The strict xfail is an unmet pure-stage requirement, not a promised Core bug.
Use pytest --runxfail -k pure_stage for its retained RED reproducer.
"""

from dataclasses import FrozenInstanceError
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path
import shutil

import pytest

import malleus.compiler as api


ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/ontology_driven_kg_realization"
SHOP = RESEARCH / "experiments/small_shop"
FIXTURES = RESEARCH / "fixtures"
CORRECTION = FIXTURES / "small_shop_fulfilment_correction_v1/input"
BASE = FIXTURES / "small_shop_fulfilment/input"
TIME = "2026-09-06T00:00:00Z"
ACTOR = "actor:semantic-reentry-prerequisite-audit"
E4 = "supplier-order-state:B:e4"
E7 = "supplier-order-state:B:e7"
SOURCE = "source:small-shop:supplier-orders"
MAPPING = "artifact:small-shop:correction-mapping"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode()


def digest(content):
    return "sha256:" + sha256(content).hexdigest()


def event(kind, **payload):
    return canonical({"event_type": kind, "payload": payload})


def artifact(record_id, content, role="RETAINED_EVIDENCE",
             media_type="application/json"):
    return api.KnowledgeAnchorInput(
        machine_event=event("ARTIFACT_REGISTERED", artifact_id=record_id,
                            artifact_identity=digest(content)),
        retained_bytes=content, media_type=media_type, role=role,
    )


def load_plan(history, name):
    """Instantiate an existing template, explicitly rebinding two coordinates.

    These are new plan bytes, not the frozen template identity. All source,
    evidence, record, lineage and supersession data remain unchanged.
    """
    plan = json.loads((SHOP / "public_population/plans" / f"{name}.json").read_bytes())
    plan["contract_identity"] = history.partial_contract.identity
    plan["history_profile"]["sha256"] = api.STATE_VERSION_PROFILE.identity
    return plan


def prepare(history, plan):
    replay = history.replay()
    compiled = api.compile_population_plan(
        plan, partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=api.PopulationBaseState.from_replay(replay),
        history_profile=api.STATE_VERSION_PROFILE,
    )
    return api.prepare_population_change(
        history=history, plan=plan,
        profile=json.loads(api.STATE_VERSION_PROFILE.canonical_bytes),
        retention_events=api.population_retention_events(
            history=history, compilation=compiled, profile=api.STATE_VERSION_PROFILE),
        transaction_time=TIME, actor_id=ACTOR,
    )


def admit(history, prepared):
    assert prepared.change_set is not None
    return api.admit_structural_change(
        history=history, preparation=prepared, transaction_time=TIME, actor_id=ACTOR)


@pytest.fixture(scope="session")
def compilation():
    return api.compile_linkml_contract(
        root_locator="small-shop-correction",
        sources={
            "small-shop-correction": (CORRECTION / "tbox/small-shop-correction.yaml").read_bytes(),
            "small-shop": (BASE / "tbox/small-shop.yaml").read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime").joinpath(
                "linkml_model", "model", "schema", "types.yaml").read_bytes(),
        },
    )


@pytest.fixture
def shop(tmp_path, compilation):
    path = tmp_path / "history.jsonl"
    history = api.create_structural_history(
        path, compilation=compilation, transaction_time=TIME, actor_id=ACTOR)
    assert history.replay().record_history == {}
    anchors = [
        artifact(MAPPING, (SHOP / "correction/mapping.json").read_bytes()),
        artifact("artifact:small-shop:baseline-mapping", (SHOP / "pareto/mapping.json").read_bytes()),
    ]
    for source_id, source_path, media in (
        (SOURCE, CORRECTION / "sources/supplier-order-history.jsonl", "application/x-ndjson"),
        ("source:small-shop:warehouse", BASE / "sources/warehouse.jsonl", "application/x-ndjson"),
        ("source:small-shop:inventory", BASE / "sources/inventory-units.csv", "text/csv"),
    ):
        content = source_path.read_bytes()
        artifact_id = source_id.replace("source:", "artifact:source:", 1)
        anchors.extend((
            artifact(artifact_id, content, "SOURCE_ARTIFACT", media),
            api.KnowledgeAnchorInput(
                machine_event=event("SOURCE_REGISTERED", artifact_id=artifact_id,
                                    source_id=source_id, source_identity=digest(content)),
                retained_bytes=content, media_type=media, role="RETAINED_SOURCE"),
        ))
    history.append_anchors(anchors=tuple(anchors), transaction_time=TIME, actor_id=ACTOR)
    for name in ("ret010", "supplier-e4"):
        admit(history, prepare(history, load_plan(history, name)))
    assert set(history.replay().record_history) == {"O1", "X1", "contains:O1:X1", E4}
    return history, path


def complement(replay):
    return {
        family: [record for record in members if record["id"] not in {E4, E7}]
        for family, members in replay.graph.export_records().items()
    }


def test_exact_existing_source_mapping_and_independent_oracle(shop):
    history, _ = shop
    replay = history.replay()
    source = replay.retained_bytes(SOURCE)
    mapping_bytes = replay.retained_bytes(MAPPING)
    assert digest(source) == "sha256:a441c49f325670e09d9fc09fd8e6510669258bed1d5532cfb2b1104c4eceb081"
    assert digest(mapping_bytes) == "sha256:77bcc53ef39b301a940ee051c1afd6d3e08e90ba6e8bd344a7ba14ff6f101795"
    mapping = json.loads(mapping_bytes)
    rows = [json.loads(line) for line in source.splitlines()]
    oracle = json.loads((CORRECTION.parent / "oracle/shop-supplier-order-correction.json").read_bytes())
    for index, name in enumerate(("supplier-e4", "supplier-e7")):
        plan = load_plan(history, name)
        record = plan["records"]["entities"][0]
        selected = mapping["changes"][index]
        assert record["properties"] == oracle["expected_states"][index]["attributes"]
        assert record["properties"] == selected["operations"][0]["properties"]
        assert plan["valid_time"] == selected["valid_time"]
        for binding in mapping["state_bindings"]:
            assert binding["target_path"][0] == "properties"
            assert record["properties"][binding["target_path"][1]] == rows[index][binding["source_field"]]
    assert load_plan(history, "supplier-e7")["supersessions"] == [
        {"record_id": E7, "supersedes_record_id": E4}]


def test_core_correction_admission_reopen_trace_and_complement(shop, tmp_path):
    history, path = shop
    before = history.replay()
    prepared = prepare(history, load_plan(history, "supplier-e7"))
    assert prepared.change_set is not None
    assert history.replay().graph.state_digest() == before.graph.state_digest()
    final = admit(history, prepared)
    isolated = tmp_path / "ledger-only"
    isolated.mkdir()
    copy = isolated / "history.jsonl"
    shutil.copyfile(path, copy)
    reopened = api.KnowledgeChangeHistory.reopen(copy).replay()
    assert sorted(member.name for member in isolated.iterdir()) == ["history.jsonl"]
    assert reopened.receipt == final.receipt
    assert complement(reopened) == complement(before)
    assert reopened.graph.query("SupplierOrderState", supplier_order_id="B") == [{
        "id": E7, "type": "SupplierOrderState", "supplier_order_id": "B",
        "product_code": "Y", "source_occurrence_id": "e7", "ordered_quantity": 2,
    }]
    assert reopened.record_history[E4].superseded_by == E7
    assert reopened.record_history[E7].supersedes_record_id == E4
    trace = api.trace_population_record(reopened, E7)
    assert trace.sources[0].content == before.retained_bytes(SOURCE)
    assert trace.change_set.identity == prepared.change_set.identity
    assert trace.change_set.valid_time == api.KnowledgeValidTime("ORDER_ONLY", "e7")
    assert trace.population_plan["supersessions"][0]["supersedes_record_id"] == E4


def test_history_composer_is_pure_but_has_a_writer_receiver(shop):
    history, path = shop
    prepared = prepare(history, load_plan(history, "supplier-e7"))
    before = path.read_bytes()
    compiled = prepared.compilation
    composed = history.compose_change_set(
        change_set_id=prepared.change_set.change_set_id,
        source_record_ids=compiled.source_record_ids,
        evidence_record_ids=compiled.evidence_record_ids,
        operations=compiled.operations, valid_time=compiled.valid_time,
        supersedes=compiled.supersedes,
    )
    assert composed == prepared.change_set
    assert path.read_bytes() == before
    assert callable(history.admit) and callable(history.append_anchors)
    assert api.KnowledgeChangeSet.from_bytes(composed.canonical_bytes) == composed
    with pytest.raises((FrozenInstanceError, AttributeError)):
        composed.identity = "changed"
    with pytest.raises(TypeError):
        composed.operations[0].properties["ordered_quantity"] = 999


@pytest.mark.xfail(strict=True, reason="Open Core dependency: population preparation retains anchors; no agreed immutable-base KCS composer")
def test_population_preparation_satisfies_pure_stage_requirement(shop):
    history, path = shop
    before_bytes = path.read_bytes()
    before_state = history.replay().graph.state_digest()
    prepared = prepare(history, load_plan(history, "supplier-e7"))
    assert isinstance(prepared.change_set, api.KnowledgeChangeSet)
    assert history.replay().graph.state_digest() == before_state
    assert path.read_bytes() == before_bytes, (
        "Population preparation appends evidence. It cannot be the pure Re-entry "
        "Synthesizer; supply a Core-owned immutable-base composer instead."
    )


def test_evidence_only_head_change_makes_prepared_candidate_stale(shop):
    history, path = shop
    prepared = prepare(history, load_plan(history, "supplier-e7"))
    before_state = history.replay().graph.state_digest()
    history.append_anchors(anchors=(artifact("artifact:unrelated-audit", b"{}"),),
                           transaction_time=TIME, actor_id=ACTOR)
    before_bytes = path.read_bytes()
    assert history.replay().graph.state_digest() == before_state
    with pytest.raises(api.KnowledgeChangeRefusal) as refused:
        admit(history, prepared)
    assert refused.value.reason is api.KnowledgeChangeRefusalReason.STALE_BASE
    assert path.read_bytes() == before_bytes


def test_disposable_projection_mutation_is_not_an_authoritative_write(shop):
    history, path = shop
    before_bytes = path.read_bytes()
    replay = history.replay()
    before_state = replay.graph.state_digest()
    replay.graph.create_entity("InventoryUnit", "local-only", {"product_code": "X"})
    assert replay.graph.state_digest() != before_state
    assert path.read_bytes() == before_bytes
    fresh = api.KnowledgeChangeHistory.reopen(path).replay()
    assert fresh.graph.state_digest() == before_state
    assert not fresh.graph.has_node("local-only")


@pytest.mark.parametrize("field,value", [
    ("ordered_quantity", 999), ("product_code", "Z"),
    ("supplier_order_id", "C"), ("source_occurrence_id", "e4"),
])
def test_valid_locators_do_not_establish_source_value_agreement(shop, field, value):
    """Diagnostic boundary witness, the future adopter guard must reject this."""
    history, path = shop
    plan = load_plan(history, "supplier-e7")
    plan["records"]["entities"][0]["properties"][field] = value
    before = path.read_bytes()
    replay = history.replay()
    compiled = api.compile_population_plan(
        plan, partial_contract=replay.partial_contract, contract_view=replay.contract_view,
        base_state=api.PopulationBaseState.from_replay(replay),
        history_profile=api.STATE_VERSION_PROFILE,
    )
    assert compiled.status is api.PopulationPlanStatus.CHANGE_SET
    assert compiled.operations[0].properties[field] == value
    assert path.read_bytes() == before


def test_repeating_accepted_plan_is_not_core_quiescence(shop):
    history, path = shop
    plan = load_plan(history, "supplier-e7")
    admit(history, prepare(history, plan))
    before = path.read_bytes()
    with pytest.raises(api.PopulationPlanRefusal) as refused:
        prepare(history, plan)
    assert refused.value.reason is api.PopulationPlanRefusalReason.DUPLICATE_RECORD_ID
    assert path.read_bytes() == before

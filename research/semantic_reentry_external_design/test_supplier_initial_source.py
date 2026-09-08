"""Actual e4-only initial source path. No supplier effect or future e7 source."""

from copy import deepcopy
from hashlib import sha256
from importlib import import_module
import json
from pathlib import Path
import shutil

import pytest

import malleus.compiler as api


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SHOP = ROOT / "research/ontology_driven_kg_realization/experiments/small_shop"
BASE = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input"
)
FIXTURE = HERE / "fixtures/supplier_commitment_v1"
COMPONENT = "research.semantic_reentry_external_design.supplier_components"
PRODUCER = "research.semantic_reentry_external_design.supplier_initial_source"
SOURCE_ID = "source:reentry:supplier:initial"
ARTIFACT_ID = "artifact:source:reentry:supplier:initial"
MAPPING_ID = "artifact:reentry:supplier:initial-mapping"
PLAN_ID = "plan:reentry:supplier:initial"
TIME = "2026-09-08T04:00:00Z"
ACTOR = "actor:reentry:initial-population"


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(content):
    return "sha256:" + sha256(content).hexdigest()


@pytest.fixture
def initial_inputs():
    case = json.loads((FIXTURE / "case.json").read_bytes())
    return {
        "source_bytes": (FIXTURE / "input/supplier-before.jsonl").read_bytes(),
        "source_sha256": case["source"]["sha256"],
        "mapping": case["mapping"],
        "source_id": SOURCE_ID,
    }


def initial_map(values):
    return import_module(COMPONENT).map_initial_source(**values)


@pytest.mark.parametrize("quantity", [-1, 0, 1, 2, 3])
def test_initial_mapping_represents_source_quantity_not_the_goal(
    initial_inputs, quantity
):
    row = json.loads(initial_inputs["source_bytes"])
    row["quantity"] = quantity
    initial_inputs["source_bytes"] = canonical(row) + b"\n"
    initial_inputs["source_sha256"] = digest(initial_inputs["source_bytes"])
    before = deepcopy(initial_inputs)
    result = initial_map(initial_inputs)
    value = json.loads(result)
    assert value["records"] == {
        "entities": [
            {
                "id": "supplier-order-state:B:e4",
                "type": "SupplierOrderState",
                "properties": {
                    "supplier_order_id": "B",
                    "product_code": "Y",
                    "source_occurrence_id": "e4",
                    "ordered_quantity": quantity,
                },
            }
        ],
        "relations": [],
    }
    assert value["supersessions"] == []
    assert value["valid_time"] == {"kind": "ORDER_ONLY", "value": "e4"}
    assert value["sources"] == [
        {"source_id": SOURCE_ID, "sha256": initial_inputs["source_sha256"]}
    ]
    assert len(value["derivations"]) == 4
    assert {tuple(item["path"]) for item in value["derivations"]} == {
        ("properties", key) for key in before["mapping"]["fields"]
    }
    assert all(item["locator"].startswith("row:0:") for item in value["derivations"])
    assert initial_inputs == before
    assert initial_map(initial_inputs) == result == canonical(value)


@pytest.mark.parametrize(
    "fault,reason",
    [
        ("digest", "STALE_SOURCE"),
        ("missing", "MALFORMED_INPUT"),
        ("boolean", "MALFORMED_INPUT"),
        ("unknown", "MALFORMED_INPUT"),
        ("multiple", "AMBIGUOUS"),
        ("mapping", "UNSUPPORTED_RULE"),
        ("source-id", "MALFORMED_INPUT"),
        ("receipt", "MALFORMED_INPUT"),
    ],
)
def test_initial_mapper_refuses_incomplete_or_invented_inputs(
    initial_inputs, fault, reason
):
    row = json.loads(initial_inputs["source_bytes"])
    if fault == "digest":
        initial_inputs["source_sha256"] = digest(b"other")
    elif fault in {"missing", "boolean", "unknown", "receipt"}:
        if fault == "missing":
            del row["quantity"]
        elif fault == "boolean":
            row["quantity"] = True
        elif fault == "unknown":
            row["authority"] = "claimed"
        else:
            row = {"execution_status": "SUCCEEDED"}
        initial_inputs["source_bytes"] = canonical(row)
        initial_inputs["source_sha256"] = digest(initial_inputs["source_bytes"])
    elif fault == "multiple":
        initial_inputs["source_bytes"] *= 2
        initial_inputs["source_sha256"] = digest(initial_inputs["source_bytes"])
    elif fault == "mapping":
        del initial_inputs["mapping"]["fields"]["product_code"]
    else:
        initial_inputs["source_id"] = ""
    with pytest.raises(import_module(COMPONENT).SupplierInputError) as refused:
        initial_map(initial_inputs)
    assert refused.value.reason == reason


def test_initial_mapper_performs_no_io(initial_inputs, monkeypatch):
    import builtins

    implementation = import_module(COMPONENT)

    def forbidden(*args, **kwargs):
        raise AssertionError("pure initial mapper performed I/O")

    monkeypatch.setattr(builtins, "open", forbidden)
    monkeypatch.setattr(Path, "open", forbidden)
    assert type(implementation.map_initial_source(**initial_inputs)) is bytes


def prepare_plan(history, plan):
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


@pytest.fixture
def complement_owner(tmp_path, compilation):
    import_module(PRODUCER)  # Absent implementation fails before fixture creation.
    history = api.create_structural_history(
        tmp_path / "history.jsonl",
        compilation=compilation,
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    anchors = [
        api.structural_evidence_anchor(
            record_id="artifact:small-shop:baseline-mapping",
            content=(SHOP / "pareto/mapping.json").read_bytes(),
            media_type="application/json",
        )
    ]
    for source_id, artifact_id, path, media in (
        (
            "source:small-shop:warehouse",
            "artifact:source:small-shop:warehouse",
            BASE / "sources/warehouse.jsonl",
            "application/x-ndjson",
        ),
        (
            "source:small-shop:inventory",
            "artifact:source:small-shop:inventory",
            BASE / "sources/inventory-units.csv",
            "text/csv",
        ),
    ):
        anchors.extend(
            api.structural_source_anchors(
                source_id=source_id,
                artifact_id=artifact_id,
                content=path.read_bytes(),
                media_type=media,
            )
        )
    history.append_anchors(
        anchors=tuple(anchors), transaction_time=TIME, actor_id=ACTOR
    )
    plan = json.loads((SHOP / "public_population/plans/ret010.json").read_bytes())
    plan["contract_identity"] = history.partial_contract.identity
    plan["history_profile"]["sha256"] = api.STATE_VERSION_PROFILE.identity
    prepared = prepare_plan(history, plan)
    replay = api.admit_structural_change(
        history=history, preparation=prepared, transaction_time=TIME, actor_id=ACTOR
    )
    assert set(replay.record_history) == {"O1", "X1", "contains:O1:X1"}
    return history


def initial_arguments(history, values):
    return dict(
        history=history,
        source_bytes=values["source_bytes"],
        source_sha256=values["source_sha256"],
        mapping_bytes=canonical(values["mapping"]),
        source_id=values["source_id"],
        source_artifact_id=ARTIFACT_ID,
        mapping_id=MAPPING_ID,
        plan_id=PLAN_ID,
        history_profile=api.STATE_VERSION_PROFILE,
        transaction_time=TIME,
        actor_id=ACTOR,
    )


def prepare_initial(history, values):
    return import_module(PRODUCER).prepare_initial_supplier_change(
        **initial_arguments(history, values)
    )


def test_real_e4_only_source_candidate_admission_reopen_and_lineage(
    complement_owner, initial_inputs, tmp_path, monkeypatch
):
    history = complement_owner
    before = history.replay()
    source = initial_inputs["source_bytes"]
    original_read = Path.read_bytes

    def no_historical_or_oracle_reads(path):
        assert path.name != "supplier-order-history.jsonl"
        assert "oracle" not in path.parts
        return original_read(path)

    monkeypatch.setattr(Path, "read_bytes", no_historical_or_oracle_reads)
    prepared = prepare_initial(history, initial_inputs)
    assert type(prepared) is api.PopulationPreparation
    assert type(prepared.change_set) is api.KnowledgeChangeSet
    assert history.replay().graph.export_records() == before.graph.export_records()
    assert history.replay().change_sets == before.change_sets
    assert prepared.change_set.sources == ((SOURCE_ID, digest(source)),)
    restored = api.KnowledgeChangeSet.from_bytes(prepared.change_set.canonical_bytes)
    assert restored == prepared.change_set
    assert restored.sources == ((SOURCE_ID, digest(source)),)
    assert prepared.change_set.valid_time == api.KnowledgeValidTime("ORDER_ONLY", "e4")
    plan = json.loads(prepared.compilation.canonical_plan_bytes)
    assert plan["adapter"]["version"] == import_module(PRODUCER).ADAPTER_IDENTITY
    assert plan["supersessions"] == []
    final = api.admit_structural_change(
        history=history, preparation=prepared, transaction_time=TIME, actor_id=ACTOR
    )
    assert len(final.change_sets) == len(before.change_sets) + 1
    expected = {
        "id": "supplier-order-state:B:e4",
        "type": "SupplierOrderState",
        "supplier_order_id": "B",
        "product_code": "Y",
        "source_occurrence_id": "e4",
        "ordered_quantity": 1,
    }
    assert final.graph.query("SupplierOrderState", supplier_order_id="B") == [expected]
    for identifier in ("O1", "X1", "contains:O1:X1"):
        assert final.record_history[identifier] == before.record_history[identifier]
    for family, members in before.graph.export_records().items():
        assert [
            r for r in final.graph.export_records()[family] if r["id"] != expected["id"]
        ] == members
    trace = api.trace_population_record(final, expected["id"])
    assert trace.sources[0].record_id == SOURCE_ID
    assert trace.sources[0].content == source
    assert trace.sources[0].identity == digest(source)
    assert json.loads(source)["event_id"] == "e4" and source.count(b"\n") == 1
    assert "supplier-order-state:B:e7" not in final.record_history
    assert set(final.record_history) == {"O1", "X1", "contains:O1:X1", expected["id"]}
    for item in final.retained_inputs:
        assert b'"event_id":"e7"' not in item.content
    isolated = tmp_path / "reopen"
    isolated.mkdir()
    shutil.copyfile(history.path, isolated / "history.jsonl")
    reopened = api.KnowledgeChangeHistory.reopen(isolated / "history.jsonl").replay()
    assert [p.name for p in isolated.iterdir()] == ["history.jsonl"]
    assert reopened.receipt == final.receipt
    assert reopened.graph.export_records() == final.graph.export_records()
    assert (
        api.trace_population_record(reopened, expected["id"]).sources[0].content
        == source
    )


def test_invalid_source_refuses_before_retention(complement_owner, initial_inputs):
    history = complement_owner
    before = history.path.read_bytes()
    initial_inputs["source_sha256"] = digest(b"wrong")
    with pytest.raises(import_module(COMPONENT).SupplierInputError):
        prepare_initial(history, initial_inputs)
    assert history.path.read_bytes() == before


def test_initial_candidate_does_not_rebase_after_an_evidence_append(
    complement_owner, initial_inputs
):
    history = complement_owner
    prepared = prepare_initial(history, initial_inputs)
    history.append_anchors(
        anchors=(
            api.structural_evidence_anchor(
                record_id="artifact:reentry:intervening",
                content=b"explicit next evidence",
                media_type="text/plain",
            ),
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    before = history.path.read_bytes()
    with pytest.raises(api.KnowledgeChangeRefusal) as refused:
        api.admit_structural_change(
            history=history, preparation=prepared, transaction_time=TIME, actor_id=ACTOR
        )
    assert refused.value.reason is api.KnowledgeChangeRefusalReason.STALE_BASE
    assert history.path.read_bytes() == before
    assert (
        history.replay().graph.query("SupplierOrderState", supplier_order_id="B") == []
    )


def test_coordinator_rejects_a_substitute_writer_before_calling_it(initial_inputs):
    calls = []

    class ForeignWriter:
        def append_anchors(self, **kwargs):
            calls.append(kwargs)
            raise AssertionError("foreign writer invoked")

    with pytest.raises(import_module(COMPONENT).SupplierInputError) as refused:
        prepare_initial(ForeignWriter(), initial_inputs)
    assert refused.value.reason == "MALFORMED_INPUT"
    assert calls == []


@pytest.mark.parametrize(
    "field",
    [
        "source_id",
        "source_artifact_id",
        "mapping_id",
        "plan_id",
        "transaction_time",
        "actor_id",
    ],
)
def test_required_metadata_never_gets_a_default(
    complement_owner, initial_inputs, field
):
    before = complement_owner.path.read_bytes()
    values = initial_arguments(complement_owner, initial_inputs)
    values[field] = None
    with pytest.raises(import_module(COMPONENT).SupplierInputError) as refused:
        import_module(PRODUCER).prepare_initial_supplier_change(**values)
    assert refused.value.reason == "MALFORMED_INPUT"
    assert complement_owner.path.read_bytes() == before


@pytest.mark.parametrize("mapping_bytes", [b"{}", b"{", b"[]", b"null"])
def test_malformed_mapping_refuses_before_retention(
    complement_owner, initial_inputs, mapping_bytes
):
    before = complement_owner.path.read_bytes()
    values = initial_arguments(complement_owner, initial_inputs)
    values["mapping_bytes"] = mapping_bytes
    with pytest.raises(import_module(COMPONENT).SupplierInputError):
        import_module(PRODUCER).prepare_initial_supplier_change(**values)
    assert complement_owner.path.read_bytes() == before


def test_missing_profile_refuses_before_retention(complement_owner, initial_inputs):
    before = complement_owner.path.read_bytes()
    values = initial_arguments(complement_owner, initial_inputs)
    values["history_profile"] = None
    with pytest.raises(import_module(COMPONENT).SupplierInputError) as refused:
        import_module(PRODUCER).prepare_initial_supplier_change(**values)
    assert refused.value.reason == "UNSUPPORTED_RULE"
    assert complement_owner.path.read_bytes() == before


@pytest.mark.parametrize("separator", ["\u0085", "\u2028", "\u2029"])
def test_initial_parser_preserves_json_string_separators(initial_inputs, separator):
    row = json.loads(initial_inputs["source_bytes"])
    row["product_code"] = "Y" + separator + "Z"
    initial_inputs["source_bytes"] = canonical(row) + b"\n"
    initial_inputs["source_sha256"] = digest(initial_inputs["source_bytes"])
    assert (
        json.loads(initial_map(initial_inputs))["records"]["entities"][0]["properties"][
            "product_code"
        ]
        == row["product_code"]
    )


def test_initial_boundary_has_no_optional_required_inputs():
    from inspect import Parameter, signature

    parameters = signature(
        import_module(PRODUCER).prepare_initial_supplier_change
    ).parameters.values()
    assert all(
        p.kind is Parameter.KEYWORD_ONLY and p.default is Parameter.empty
        for p in parameters
    )


def test_initial_gate_and_runtime_belong_to_the_selected_checkout():
    gate = json.loads((HERE / "supplier-initial-gate.json").read_bytes())
    assert set(gate) == {"classification", "claim", "tests"}
    assert gate["classification"] == "CONFORMANCE_FIXTURE"
    assert len(gate["tests"]) == len(set(gate["tests"]))
    assert str(Path(__file__).resolve().relative_to(ROOT)) in gate["tests"]
    for name in gate["tests"]:
        path = (ROOT / name).resolve()
        assert path.is_relative_to(ROOT) and path.is_file()
    assert Path(api.__file__).resolve().is_relative_to(ROOT / "src")
    for name in (PRODUCER, COMPONENT):
        assert Path(import_module(name).__file__).resolve().is_relative_to(HERE)

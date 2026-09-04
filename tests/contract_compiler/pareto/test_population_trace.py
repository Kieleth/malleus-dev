"""Public read-only trace from an accepted record back to retained inputs."""

from __future__ import annotations

from hashlib import sha256
from importlib import import_module
from importlib.resources import files
import json
from pathlib import Path

import pytest

from tests.contract_compiler.pareto.test_document_assertion_adapter import _inputs
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    _admit_record_change,
    _anchored_history,
    _record_change,
)
from tests.contract_compiler.pareto.test_public_compiler import (
    ROOT,
    TRANSACTION_TIME,
    _anchor,
    _bootstrap,
    _compiled_shop,
    _event,
    _prepare_and_admit,
    _protocol_events,
    _runtime,
)


EXAMPLES = ROOT / "handover/2026-09-03-core-population-v2/examples"
SHOP_SOURCE = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "small_shop_fulfilment_correction_v1/input/sources"
    / "supplier-order-history.jsonl"
)


def _api():
    return import_module("malleus.compiler")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _small_shop_replay(tmp_path: Path):
    api = _api()
    compiled = _compiled_shop(api)
    history, partial, policy = _runtime(
        api, compiled, tmp_path / "small-shop-trace.jsonl"
    )
    source = SHOP_SOURCE.read_bytes()
    _bootstrap(api, history, compiled, partial, source)
    _prepare_and_admit(api, history, partial, policy, source, "e4")
    _prepare_and_admit(api, history, partial, policy, source, "e7")
    return history, api.KnowledgeChangeHistory.reopen(history.path).replay(), source


def _retain_document_inputs(history, compiled, partial, reading: bytes, capture: bytes):
    anchors = (
        (
            "artifact:validated-contract",
            compiled.artifact.artifact_bytes,
            "VALIDATED_CONTRACT",
        ),
        (
            "artifact:partial-contract",
            partial.canonical_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        (
            "artifact:history-binding",
            history.binding.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        ("capture:inspection-note", capture, "RETAINED_EVIDENCE"),
        ("artifact:inspection-note", reading, "SOURCE_ARTIFACT"),
    )
    for record_id, content, role in anchors:
        _anchor(
            history,
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id=record_id,
                artifact_identity=_digest(content),
            ),
            content,
            role,
        )
    _anchor(
        history,
        _event(
            "SOURCE_REGISTERED",
            artifact_id="artifact:inspection-note",
            source_id="source:inspection-note",
            source_identity=_digest(reading),
        ),
        reading,
        "RETAINED_SOURCE",
    )


def _document_replay(
    tmp_path: Path,
    *,
    first_assertion_modality: str = "STATED",
    assertion_times: dict[str, dict[str, str]] | None = None,
):
    api = _api()
    compiled = api.compile_linkml_contract(
        root_locator="inspection-note",
        sources={
            "inspection-note": (EXAMPLES / "inspection-note.yaml").read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": (
                files("linkml_runtime")
                .joinpath("linkml_model", "model", "schema", "types.yaml")
                .read_bytes()
            ),
        },
    )
    history, partial, policy = _runtime(
        api, compiled, tmp_path / "document-trace.jsonl"
    )
    reading, capture, plan, _ = _inputs()
    capture["assertions"][0]["modality"] = first_assertion_modality
    if assertion_times is not None:
        for assertion in capture["assertions"]:
            assertion.update(assertion_times[assertion["id"]])
    reading_bytes = _canonical(reading)
    capture_bytes = _canonical(capture)
    adapted = api.adapt_document_assertions(
        reading_bytes=reading_bytes,
        capture_bytes=capture_bytes,
        capture_id="capture:inspection-note",
        plan_id=str(plan["plan_id"]),
        contract_identity=partial.identity,
        records=plan["records"],
        supersessions=plan["supersessions"],
    )
    plan = json.loads(adapted.canonical_plan_bytes)
    _retain_document_inputs(history, compiled, partial, reading_bytes, capture_bytes)
    gaps_id = f"{plan['plan_id']}:gaps"
    gaps_bytes = _canonical({"gaps": plan["gaps"], "plan_id": plan["plan_id"]})
    retention_events = {
        "profile:source-assertion": _event(
            "ARTIFACT_REGISTERED",
            artifact_id="profile:source-assertion",
            artifact_identity=api.SOURCE_ASSERTION_PROFILE.identity,
        ),
        plan["plan_id"]: _event(
            "ARTIFACT_REGISTERED",
            artifact_id=plan["plan_id"],
            artifact_identity=_digest(adapted.canonical_plan_bytes),
        ),
        gaps_id: _event(
            "ARTIFACT_REGISTERED",
            artifact_id=gaps_id,
            artifact_identity=_digest(gaps_bytes),
        ),
    }
    prepared = api.prepare_population_change(
        history=history,
        plan=plan,
        profile=json.loads(api.SOURCE_ASSERTION_PROFILE.canonical_bytes),
        retention_events=retention_events,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:public-adopter",
    )
    assert prepared.change_set is not None
    history.admit(
        change_set=prepared.change_set,
        machine_events=_protocol_events(
            policy,
            prepared.change_set,
            prepared.retention_replay.machine_state.identity,
            "inspection-note",
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:public-adopter",
    )
    return history, api.KnowledgeChangeHistory.reopen(history.path).replay()


def test_public_compiler_exposes_the_read_only_population_trace() -> None:
    api = _api()

    assert {
        "PopulationRecordTrace",
        "PopulationTraceRefusal",
        "PopulationTraceRefusalReason",
        "trace_population_record",
    } <= set(api.__all__)


def test_small_shop_trace_reaches_profile_plan_field_and_source_bytes(
    tmp_path: Path,
) -> None:
    api = _api()
    history, replay, source = _small_shop_replay(tmp_path)
    ledger_before = history.path.read_bytes()

    trace = api.trace_population_record(replay, "supplier-order-state:B:e7")

    assert isinstance(trace, api.PopulationRecordTrace)
    assert trace.history_profile == api.STATE_VERSION_PROFILE
    assert trace.change_set.change_set_id == "change:plan:shop:B:e7"
    assert trace.population_plan["plan_id"] == "plan:shop:B:e7"
    assert trace.population_plan_identity == _digest(
        replay.retained_bytes("plan:shop:B:e7")
    )
    assert trace.record_history.supersedes_record_id == ("supplier-order-state:B:e4")
    assert [dict(item) for item in trace.derivations] == [
        {
            "locator": "row:1:supplier_order_id",
            "path": ("properties", "supplier_order_id"),
            "record_id": "supplier-order-state:B:e7",
            "source_id": "source:supplier-order-history",
        },
        {
            "locator": "row:1:product_code",
            "path": ("properties", "product_code"),
            "record_id": "supplier-order-state:B:e7",
            "source_id": "source:supplier-order-history",
        },
        {
            "locator": "row:1:quantity",
            "path": ("properties", "ordered_quantity"),
            "record_id": "supplier-order-state:B:e7",
            "source_id": "source:supplier-order-history",
        },
        {
            "locator": "row:1:event_id",
            "path": ("properties", "source_occurrence_id"),
            "record_id": "supplier-order-state:B:e7",
            "source_id": "source:supplier-order-history",
        },
    ]
    assert [(item.record_id, item.content) for item in trace.sources] == [
        ("source:supplier-order-history", source)
    ]
    assert [item.record_id for item in trace.evidence] == [
        "profile:state-version",
        "plan:shop:B:e7",
    ]
    assert history.path.read_bytes() == ledger_before


def test_document_trace_reaches_assertion_locator_and_retained_capture(
    tmp_path: Path,
) -> None:
    api = _api()
    history, replay = _document_replay(tmp_path)
    ledger_before = history.path.read_bytes()

    trace = api.trace_population_record(replay, "inspection-of:P-7:2026-03-02")

    assert trace.history_profile == api.SOURCE_ASSERTION_PROFILE
    assert {item["locator"] for item in trace.derivations} == {"asr:001"}
    capture_input = next(
        item for item in trace.evidence if item.record_id == "capture:inspection-note"
    )
    capture = json.loads(capture_input.content)
    assertion = next(item for item in capture["assertions"] if item["id"] == "asr:001")
    assert assertion["modality"] == "STATED"
    assert assertion["statement"] == "Pump P-7 was inspected on 2026-03-02."
    assert trace.sources[0].record_id == "source:inspection-note"
    assert history.path.read_bytes() == ledger_before


def test_hypothesised_graph_record_remains_qualified_by_retained_trace(
    tmp_path: Path,
) -> None:
    api = _api()
    history, replay = _document_replay(
        tmp_path,
        first_assertion_modality="HYPOTHESISED",
    )
    ledger_before = history.path.read_bytes()

    trace = api.trace_population_record(replay, "inspection-of:P-7:2026-03-02")
    capture = json.loads(
        next(
            item.content
            for item in trace.evidence
            if item.record_id == "capture:inspection-note"
        )
    )
    assertion = next(item for item in capture["assertions"] if item["id"] == "asr:001")

    assert trace.history_profile.projection_rule_family == (
        "CURRENT_NON_SUPERSEDED_RECORDS_WITH_RETAINED_ASSERTION_TRACE"
    )
    assert assertion["modality"] == "HYPOTHESISED"
    assert "modality" not in replay.graph.get_relation("inspection-of:P-7:2026-03-02")
    assert history.path.read_bytes() == ledger_before


def test_trace_refuses_a_change_without_a_retained_population_plan(
    tmp_path: Path,
) -> None:
    api = _api()
    history, _, partial, _, source_identity, evidence_identity = _anchored_history(
        tmp_path
    )
    change = _record_change(
        history,
        partial,
        source_identity,
        evidence_identity,
        change_set_id="change:direct",
        record_id="left:direct",
        label="direct",
        order="e1",
    )
    _admit_record_change(history, change, suffix="direct")
    replay = history.replay()
    ledger_before = history.path.read_bytes()

    with pytest.raises(api.PopulationTraceRefusal) as refusal:
        api.trace_population_record(replay, "left:direct")

    assert (
        refusal.value.reason
        is api.PopulationTraceRefusalReason.POPULATION_PLAN_NOT_BOUND
    )
    assert history.path.read_bytes() == ledger_before

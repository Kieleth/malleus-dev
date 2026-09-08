"""Current document reproduction cannot silently borrow a historical producer."""

from copy import deepcopy
from importlib.resources import files
import json

import pytest

import malleus.compiler as api
from tests.contract_compiler.pareto import test_population_trace as trace


CURRENT = trace.EXAMPLES.with_name("inspection_note_execution_v2")


@pytest.fixture(scope="module")
def artifact_bytes():
    return api.compile_linkml_contract(
        root_locator="inspection-note",
        sources={
            "inspection-note": (trace.EXAMPLES / "inspection-note.yaml").read_bytes(),
            "malleus": (trace.ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    ).artifact.artifact_bytes


def test_current_example_is_exact_and_preserves_historical_meaning(artifact_bytes):
    current = (CURRENT / "document-change.json").read_bytes()
    trace._assert_current_document_change(artifact_bytes, current)
    historical = json.loads((trace.EXAMPLES / "document-change.json").read_bytes())
    observed = json.loads(current)

    assert set(observed) == set(historical)
    assert {key for key in observed if observed[key] != historical[key]} == {
        "base_ledger_head"
    }
    assert historical["base_ledger_head"] == (
        "sha256:5f52eeecdc80479f6b3a0133fd0390d67f39733c12b88fe0c4946790b405c390"
    )


@pytest.mark.parametrize("field", ["producer", "artifact"])
def test_wrong_compiler_is_refused_before_output_comparison(artifact_bytes, field):
    changed = json.loads(artifact_bytes)
    if field == "producer":
        changed["evidence"]["producer"]["sha256"] = "sha256:" + "0" * 64
    else:
        changed["evidence_sha256"] = "sha256:" + "0" * 64

    with pytest.raises(AssertionError, match="[Pp]roducer|[Aa]rtifact"):
        trace._assert_current_document_change(trace._canonical(changed), b"{}")


@pytest.mark.parametrize(
    "field",
    [
        "operations",
        "sources",
        "evidence",
        "valid_time",
        "base_ledger_head",
        "ordinal_type",
    ],
)
def test_current_comparison_never_discards_changed_fields(artifact_bytes, field):
    changed = json.loads((CURRENT / "document-change.json").read_bytes())
    if field == "ordinal_type":
        changed["operations"][0]["ordinal"] = False
    else:
        changed[field] = None

    with pytest.raises(AssertionError, match="[Cc]hange set"):
        trace._assert_current_document_change(artifact_bytes, trace._canonical(changed))


def test_corrupted_recorded_example_refuses(artifact_bytes, tmp_path, monkeypatch):
    binding = (CURRENT / "binding.json").read_bytes()
    (tmp_path / "binding.json").write_bytes(binding)
    changed = json.loads((CURRENT / "document-change.json").read_bytes())
    changed["operations"][0]["properties"]["name"] = "P-8"
    (tmp_path / "document-change.json").write_bytes(trace._canonical(changed))
    monkeypatch.setattr(trace, "CURRENT_DOCUMENT", tmp_path)

    with pytest.raises(AssertionError, match="[Ee]xample bytes"):
        trace._assert_current_document_change(artifact_bytes, trace._canonical(changed))


def test_reopened_document_preserves_all_records_and_retained_evidence(tmp_path):
    _, replay = trace._document_replay(tmp_path)
    expected_records = deepcopy(
        json.loads((trace.EXAMPLES / "document-plan.json").read_bytes())["records"]
    )
    actual = replay.graph.export_records()
    assert set(actual) >= set(expected_records)
    for family, expected in expected_records.items():
        assert sorted(actual[family], key=lambda item: item["id"]) == sorted(
            expected, key=lambda item: item["id"]
        )
    for family in set(actual) - set(expected_records):
        assert actual[family] == []

    for record in (*actual["entities"], *actual["relations"]):
        traced = api.trace_population_record(replay, record["id"])
        assert (
            traced.sources[0].content == (trace.EXAMPLES / "reading.json").read_bytes()
        )
        capture = next(
            item
            for item in traced.evidence
            if item.record_id == "capture:inspection-note"
        )
        assert (
            capture.content == (trace.EXAMPLES / "document-capture.json").read_bytes()
        )
        assert traced.population_plan_bytes == trace._canonical(
            json.loads((trace.EXAMPLES / "document-plan.json").read_bytes())
        )
        assert traced.change_set.valid_time == api.KnowledgeValidTime(
            "ORDER_ONLY", "capture:inspection-note"
        )

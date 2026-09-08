"""Current evidence must bind the producer without erasing historical results."""

from copy import deepcopy
from dataclasses import replace
from importlib import import_module
import json
from pathlib import Path

import pytest

from research.ontology_driven_kg_realization.experiments.small_shop.object_event.run import (
    run_object_event,
)


HERE = Path(__file__).parent


def helper():
    return import_module(
        "research.ontology_driven_kg_realization.experiments.small_shop"
        ".evidence_assertions"
    )


@pytest.fixture(scope="module")
def occurrence(tmp_path_factory):
    return run_object_event(tmp_path_factory.mktemp("current-evidence-occurrence"))


def test_current_output_is_bound_to_exact_compiler_and_retained_history(occurrence):
    helper().assert_current_evidence(
        "object_event", occurrence.replay, {"evidence.json": occurrence.evidence_bytes}
    )


@pytest.mark.parametrize("change", ["producer", "artifact"])
def test_wrong_compiler_refuses_before_output_comparison(occurrence, change):
    replay = occurrence.replay
    retained = {item.record_id: item for item in replay.retained_inputs}
    artifact = next(
        item for item in retained.values() if item.role == "VALIDATED_CONTRACT"
    )
    value = json.loads(artifact.content)
    if change == "producer":
        value["evidence"]["producer"]["sha256"] = "sha256:" + "0" * 64
    else:
        value["evidence_sha256"] = "sha256:" + "0" * 64
    retained[artifact.record_id] = replace(artifact, content=json.dumps(value).encode())
    changed = replace(replay, _retained=retained)
    with pytest.raises(AssertionError, match="[Cc]ompiler"):
        helper().assert_current_evidence("object_event", changed, {})


@pytest.mark.parametrize("change", ["history", "source", "record", "boolean"])
def test_no_changed_output_field_is_discarded(occurrence, change):
    value = json.loads(occurrence.evidence_bytes)
    if change == "history":
        value["history"]["ledger_head"] = "sha256:" + "0" * 64
    elif change == "source":
        value["source_identity"] = "sha256:" + "0" * 64
    elif change == "record":
        value["observed"]["entities"][0]["id"] = "invented"
    else:
        value["observed"]["relation_count"] = False  # Not the integer zero.
    with pytest.raises(AssertionError, match="[Oo]utput"):
        helper().assert_current_evidence(
            "object_event",
            occurrence.replay,
            {"evidence.json": json.dumps(value).encode()},
        )


@pytest.mark.parametrize("change", ["missing", "extra"])
def test_output_file_set_is_closed(occurrence, change):
    outputs = {"evidence.json": occurrence.evidence_bytes}
    if change == "missing":
        del outputs["evidence.json"]
    else:
        outputs["unbound.json"] = b"{}"
    with pytest.raises(AssertionError, match="[Oo]utput"):
        helper().assert_current_evidence("object_event", occurrence.replay, outputs)


def test_corrupted_expected_bytes_refuse_even_when_the_run_matches_them(
    occurrence, tmp_path, monkeypatch
):
    module = helper()
    binding = (module.CURRENT / "binding.json").read_bytes()
    (tmp_path / "binding.json").write_bytes(binding)
    (tmp_path / "object_event").mkdir()
    corrupt = deepcopy(json.loads(occurrence.evidence_bytes))
    corrupt["history"]["ledger_event_count"] = 0
    content = json.dumps(corrupt).encode()
    (tmp_path / "object_event/evidence.json").write_bytes(content)
    monkeypatch.setattr(module, "CURRENT", tmp_path)
    with pytest.raises(AssertionError, match="[Ee]xpected bytes"):
        module.assert_current_evidence(
            "object_event", occurrence.replay, {"evidence.json": content}
        )


def test_every_predecessor_receipt_remains_byte_identical():
    module = helper()
    binding = json.loads((module.CURRENT / "binding.json").read_bytes())
    assert len(binding["historical_outputs"]) == 10
    for name, identity in binding["historical_outputs"].items():
        assert module.digest((HERE / name).read_bytes()) == identity

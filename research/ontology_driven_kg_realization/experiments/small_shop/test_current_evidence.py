"""Current evidence must bind the producer without erasing historical results."""

from copy import deepcopy
from dataclasses import replace
from importlib import import_module
import json
from pathlib import Path
from types import SimpleNamespace

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


def evidence_bytes(value):
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode()
        + b"\n"
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
    assert evidence_bytes(value) == occurrence.evidence_bytes
    if change == "history":
        value["history"]["ledger_head"] = "sha256:" + "0" * 64
    elif change == "source":
        value["source_identity"] = "sha256:" + "0" * 64
    elif change == "record":
        value["observed"]["entities"][0][0] = "invented"
    else:
        value["observed"]["relation_count"] = False  # Not the integer zero.
    with pytest.raises(AssertionError, match="[Oo]utput"):
        helper().assert_current_evidence(
            "object_event",
            occurrence.replay,
            {"evidence.json": evidence_bytes(value)},
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
    content = evidence_bytes(corrupt)
    (tmp_path / "object_event/evidence.json").write_bytes(content)
    monkeypatch.setattr(module, "CURRENT", tmp_path)
    with pytest.raises(AssertionError, match="[Ee]xpected bytes"):
        module.assert_current_evidence(
            "object_event", occurrence.replay, {"evidence.json": content}
        )


def test_every_predecessor_receipt_remains_byte_identical():
    module = helper()
    binding = json.loads((module.CURRENT / "binding.json").read_bytes())
    assert len(binding["historical_outputs"]) == 20
    for name, identity in binding["historical_outputs"].items():
        assert module.digest((HERE / name).read_bytes()) == identity


def test_changed_historical_receipt_refuses_the_current_comparison(
    occurrence, tmp_path, monkeypatch
):
    module = helper()
    binding = json.loads((module.CURRENT / "binding.json").read_bytes())
    for name in binding["historical_outputs"]:
        destination = tmp_path / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((HERE / name).read_bytes())
    predecessor = tmp_path / "evidence_2026_09_06/object_event/evidence.json"
    predecessor.write_bytes(predecessor.read_bytes() + b" ")
    monkeypatch.setattr(module, "HERE", tmp_path)
    with pytest.raises(AssertionError, match="Historical evidence changed"):
        module.assert_current_evidence(
            "object_event",
            occurrence.replay,
            {"evidence.json": occurrence.evidence_bytes},
        )


def test_a_revision_cannot_introduce_an_unbound_compiler_artifact(occurrence):
    changed = replace(
        occurrence.replay,
        contract_revisions=(
            SimpleNamespace(
                target_validated_contract_bytes=b'{"evidence":{"producer":{"id":"other","sha256":"wrong"}}}'
            ),
        ),
    )
    with pytest.raises(AssertionError, match="[Cc]ompiler"):
        helper().assert_current_evidence("object_event", changed, {})


def test_successor_changes_only_recorded_history_and_artifact_fingerprints():
    module = helper()
    binding = json.loads((module.CURRENT / "binding.json").read_bytes())

    def changes(old, new, path=""):
        assert type(old) is type(new), path
        if isinstance(old, dict):
            assert old.keys() == new.keys(), path
            return [
                p for k in sorted(old) for p in changes(old[k], new[k], path + "/" + k)
            ]
        if isinstance(old, list):
            assert len(old) == len(new), path
            return [
                p
                for i, pair in enumerate(zip(old, new, strict=True))
                for p in changes(*pair, path + "/" + str(i))
            ]
        if old == new:
            return []
        assert isinstance(old, str) and isinstance(new, str), path
        assert old.startswith("sha256:") and new.startswith("sha256:"), path
        assert len(old) == len(new) == 71, path
        return [path]

    for group, scenario in binding["scenarios"].items():
        for name, output in scenario["outputs"].items():
            old = json.loads((HERE / output["predecessor"]).read_bytes())
            new = json.loads((module.CURRENT / group / name).read_bytes())
            assert changes(old, new) == output["changed_paths"]

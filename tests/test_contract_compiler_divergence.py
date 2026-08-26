"""CC-X01 lossless LinkML versus OntologyRegistry measurements."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "contract_compiler_divergence.py"
CASES = (
    ROOT
    / "conformance"
    / "contract_compiler"
    / "v0"
    / "linkml_legacy_divergence"
    / "cases.json"
)
OBSERVATIONS = CASES.with_name("observations.json")
EVIDENCE = ROOT / "conformance" / "contract_compiler" / "v0" / "evidence" / "CC-X01.json"

EXPECTED_CASE_IDS = [
    "simple_parity",
    "parent_mixin_precedence",
    "repeated_mixin",
    "conflicting_mixins_ab",
    "conflicting_mixins_ba",
    "numeric_bounds",
    "explicit_false",
    "default_range",
    "attribute_slot_usage",
]
EXPECTED_ENGINES = ["linkml", "ontology_registry"]
FORBIDDEN_DECISION_KEYS = {
    "classification",
    "comparison",
    "decision",
    "preferred",
    "recommendation",
    "verdict",
    "winner",
}


def _load_runner():
    spec = importlib.util.spec_from_file_location("contract_compiler_divergence", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot load CC-X01 runner: {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


runner = _load_runner()


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def test_cases_are_nine_small_single_module_measurements():
    document = runner.load_cases(CASES)

    assert set(document) == {"schema", "workstream_id", "baseline", "cases"}
    assert document["schema"] == "malleus.contract-compiler.divergence-cases/v1"
    assert document["workstream_id"] == "CC-X01"
    assert document["baseline"] == {
        "linkml": "1.11.1",
        "linkml-runtime": "1.11.1",
    }
    assert [case["case_id"] for case in document["cases"]] == EXPECTED_CASE_IDS
    for case in document["cases"]:
        assert set(case) == {"case_id", "target_class", "source", "probes"}
        assert case["target_class"] in {"Thing", "Child"}
        assert isinstance(case["source"], dict)
        assert "imports" not in case["source"]
        assert case["probes"]


def test_case_corpus_keeps_explicit_false_null_and_absence_distinct():
    document = runner.load_cases(CASES)
    explicit_false = next(
        case for case in document["cases"] if case["case_id"] == "explicit_false"
    )
    default_range = next(
        case for case in document["cases"] if case["case_id"] == "default_range"
    )

    assert explicit_false["source"]["classes"]["Thing"]["slot_usage"]["value"][
        "multivalued"
    ] is False
    assert "range" not in default_range["source"]["slots"]["value"]


def test_wrong_or_extra_baseline_is_rejected():
    document = runner.load_cases(CASES)
    wrong = deepcopy(document)
    wrong["baseline"]["linkml-runtime"] = "1.10.0"
    with pytest.raises(runner.DivergenceError, match="linkml-runtime"):
        runner.validate_cases(wrong)

    extra = deepcopy(document)
    extra["baseline"]["fallback"] = "host"
    with pytest.raises(runner.DivergenceError, match="baseline"):
        runner.validate_cases(extra)


def test_retained_baseline_wheels_are_required_and_hash_checked(tmp_path):
    manifest = _read(
        ROOT
        / "conformance"
        / "contract_compiler"
        / "v0"
        / "compiler_environment"
        / "manifest.json"
    )
    selected = runner.retained_baseline(manifest)
    assert [item.distribution for item in selected] == ["linkml", "linkml-runtime"]
    assert [item.version for item in selected] == ["1.11.1", "1.11.1"]

    corrupt = deepcopy(manifest)
    artifact = next(
        item
        for item in corrupt["wheelhouse"]["artifacts"]
        if item.get("distribution") == "linkml-runtime"
    )
    artifact["sha256"] = "sha256:" + "0" * 64
    with pytest.raises(runner.DivergenceError, match="linkml-runtime"):
        runner.retained_baseline(corrupt)


def test_observations_have_exact_independent_engine_structure_and_no_policy():
    document = _read(OBSERVATIONS)
    runner.validate_observations(document)

    assert set(document) == {
        "schema",
        "workstream_id",
        "cases_sha256",
        "environment_manifest_sha256",
        "baseline",
        "engines",
        "observations",
    }
    assert document["baseline"] == {
        "linkml": "1.11.1",
        "linkml-runtime": "1.11.1",
    }
    assert [engine["engine_id"] for engine in document["engines"]] == EXPECTED_ENGINES
    assert [item["case_id"] for item in document["observations"]] == EXPECTED_CASE_IDS
    for item in document["observations"]:
        assert set(item) == {"case_id", "engines"}
        assert [engine["engine_id"] for engine in item["engines"]] == EXPECTED_ENGINES
        for engine in item["engines"]:
            assert set(engine) == {"engine_id", "construction", "probes"}

    for mapping in _walk(document):
        assert not FORBIDDEN_DECISION_KEYS & set(mapping)


def test_observation_values_use_explicit_absent_null_value_states():
    document = _read(OBSERVATIONS)
    states = set()
    for mapping in _walk(document["observations"]):
        if set(mapping).issubset({"state", "value"}) and "state" in mapping:
            states.add(mapping["state"])
            if mapping["state"] == "VALUE":
                assert set(mapping) == {"state", "value"}
            else:
                assert set(mapping) == {"state"}
    assert states == {"ABSENT", "NULL", "VALUE"}


def test_replay_is_byte_identical_and_matches_retained_observations():
    first = runner.render_observations(runner.load_cases(CASES))
    second = runner.render_observations(runner.load_cases(CASES))
    assert first == second == OBSERVATIONS.read_bytes()


def test_check_detects_any_retained_observation_mutation(tmp_path):
    changed = _read(OBSERVATIONS)
    changed["observations"][0]["engines"][0]["construction"] = {
        "state": "VALUE",
        "value": "MUTATED",
    }
    changed_path = tmp_path / "changed.json"
    changed_path.write_bytes(runner.canonical_json(changed))

    with pytest.raises(runner.DivergenceError, match="do not match"):
        runner.check_observations(CASES, changed_path)


def test_cli_checks_retained_bytes_without_rewriting_them():
    before = OBSERVATIONS.read_bytes()
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout == "CC-X01 observations match retained bytes\n"
    assert OBSERVATIONS.read_bytes() == before


def test_evidence_binds_the_measurements_without_claiming_a_decision():
    evidence = _read(EVIDENCE)
    assert evidence["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert evidence["workstream_id"] == "CC-X01"
    assert evidence["result"] == "PASS"
    assert evidence["case_count"] == 9
    assert evidence["engine_ids"] == EXPECTED_ENGINES
    assert evidence["baseline"] == {
        "linkml": "1.11.1",
        "linkml-runtime": "1.11.1",
    }
    for mapping in _walk(evidence):
        assert not FORBIDDEN_DECISION_KEYS & set(mapping)

"""Execution safeguards, never source meaning or candidate repair."""

from pathlib import Path
import importlib.util
import json

import pytest


@pytest.fixture(scope="module")
def subject():
    path = Path(__file__).with_name("relationship_execute.py")
    spec = importlib.util.spec_from_file_location("relationship_execute", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_method_drift_refuses(subject, tmp_path):
    path = tmp_path / "reader.py"
    path.write_bytes(b"original")
    item = {"path": str(path), "sha256": subject.digest(b"original")}
    assert subject.checked_method(item) == b"original"
    path.write_bytes(b"different")
    with pytest.raises(ValueError, match="identity"):
        subject.checked_method(item)


def test_binding_mutation_refuses(subject):
    binding = {"queries": [{"id": "q", "cases": []}]}
    binding["cases_sha256"] = subject.digest(subject.canonical(binding["queries"]))
    acceptance = {"query_cases_sha256": binding["cases_sha256"]}
    subject.check_binding(binding, acceptance)
    binding["queries"][0]["cases"].append({"record_type": "Changed"})
    with pytest.raises(ValueError, match="binding"):
        subject.check_binding(binding, acceptance)


@pytest.mark.parametrize("arm,attempt", [("a", 1), ("b", 3)])
def test_frozen_queries_repeat_and_review_binds_the_same_output(subject, arm, attempt):
    executed = subject.PAIR / arm / "attempts" / f"attempt-{attempt:02d}"
    outcome = json.loads((executed / "execution-result.json").read_bytes())
    assert outcome["status"] == "ADMITTED_REPLAYED_QUERIED_UNREVIEWED"
    assert (
        subject.digest((executed / "ledger/history.jsonl").read_bytes())
        == outcome["ledger_sha256"]
    )
    for name in ("query-result.json", "trace-summary.json"):
        assert (executed / "query" / name).read_bytes() == (
            executed / "query-repeat" / name
        ).read_bytes()
    source = (executed / "query/query-result.json").read_bytes()
    assert subject.digest(source) == outcome["query_sha256"]
    query = json.loads(source)
    assert len(query["queries"]) == 30
    assert not any(query["forbidden_attempts"].values())
    manifest = json.loads((executed / "review/review-input-manifest.json").read_bytes())
    assert manifest["stage_identities"]["query_result_sha256"] == subject.digest(source)
    assert manifest["authorship"]["deviation"]["to"] == "CODEX_PRELIMINARY"


def test_snapshot_is_exact_and_required(subject, tmp_path):
    live = tmp_path / "document-population.json"
    snapshot = tmp_path / "population-attempt-01.json"
    live.write_bytes(b"{}")
    with pytest.raises(FileNotFoundError):
        subject.submission(snapshot)
    snapshot.write_bytes(b"{}")
    assert subject.submission(snapshot) == b"{}"
    live.write_bytes(b'{"changed":true}')
    with pytest.raises(ValueError, match="snapshot"):
        subject.submission(snapshot)


def test_result_label_is_not_historical(subject):
    source = b'RUN="run-26"\nSCHEMA="run-26-result"\n'
    derived = subject.label_runner(source, "sol-relationship-contrast-01-a")
    assert b"run-26" not in derived
    assert derived.replace(b"sol-relationship-contrast-01-a", b"run-26") == source
    with pytest.raises(ValueError):
        subject.label_runner(source, "run-26")


def test_destination_refuses_overwrite_and_outside_run(subject, tmp_path):
    run = tmp_path / "a"
    run.mkdir()
    target = subject.reserve_attempt(run, 1)
    marker = target / "retained.json"
    marker.write_text(json.dumps({"retained": True}))
    with pytest.raises(FileExistsError):
        subject.reserve_attempt(run, 1)
    assert json.loads(marker.read_text()) == {"retained": True}
    with pytest.raises(ValueError):
        subject.reserve_attempt(run, 4)


@pytest.mark.parametrize("arm,attempt", [("a", 1), ("b", 3)])
def test_admitted_contrast_preserves_submitted_records_and_original_relations(
    subject, arm, attempt
):
    run = subject.PAIR / arm
    executed = run / "attempts" / f"attempt-{attempt:02d}"
    original = json.loads(
        (run / "producer/work/population-attempt-01.json").read_bytes()
    )
    submitted = json.loads((executed / "submitted-population.json").read_bytes())
    exported = json.loads((executed / "public/export-records.json").read_bytes())
    result = json.loads((executed / "public/run-result.json").read_bytes())
    assert result["status"] == "ADMITTED_AND_REPLAYED"
    assert all(result["reopen_matches_admitted"].values())
    assert (
        subject.digest(subject.canonical(exported)) == result["export_records_sha256"]
    )
    for family, records in submitted["records"].items():
        assert {r["id"]: r for r in records} == {r["id"]: r for r in exported[family]}
    assert {r["id"]: r for r in original["records"]["relations"]} == {
        r["id"]: r for r in exported["relations"]
    }
    measured = json.loads((subject.HERE / "relationship-measurement.json").read_bytes())
    assert (
        json.loads((executed / "execution-inputs.json").read_bytes())["method"]
        == measured
    )
    acceptance = json.loads((run / "ontology-acceptance.json").read_bytes())
    binding = json.loads((executed / "query-binding.json").read_bytes())
    subject.check_binding(binding, acceptance)

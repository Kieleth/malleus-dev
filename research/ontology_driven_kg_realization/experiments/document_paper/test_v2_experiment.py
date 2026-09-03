"""Hard guards for the explicit paper-v4 v2 build and query driver."""

from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from research.ontology_driven_kg_realization.experiments.document_paper.experiment_run import (
    PaperExperimentRun,
)
from research.ontology_driven_kg_realization.experiments.document_paper.query_replay import (
    QueryReplayRefusal,
)
from research.ontology_driven_kg_realization.experiments.document_paper import (
    v2_experiment as subject,
)


ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = ROOT / "paper-v4/experiment-v2"
TRANSACTION_TIME = "2026-09-03T09:00:00Z"


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def test_configuration_closes_exact_v2_inputs_without_query_evidence() -> None:
    configuration = subject.experiment_configuration(TRANSACTION_TIME)

    assert configuration.transaction_time == TRANSACTION_TIME
    assert configuration.contract_id == (
        "https://malleus.dev/contracts/paper-v4/experiment-v2"
    )
    assert configuration.ontology_locator == "paper-v4:mid-ocean-ridge-geodynamics"
    assert configuration.population_recipe_profile.record_type_templates == tuple(
        (name, name + "-1.0.0") for name in subject.CONCRETE_RECORD_TYPES
    )
    assert len(configuration.record_type_iris) == 21
    assert not any("query" in name for name in configuration.input_identities())


def test_all_retained_public_inputs_match_the_driver_coordinates() -> None:
    configuration = subject.experiment_configuration(TRANSACTION_TIME)
    inputs = subject.frozen_input_paths(ROOT, Path("private-reading"))

    assert _digest(inputs.selected_ontology) == configuration.ontology_sha256
    assert _digest(inputs.malleus_import) == configuration.malleus_import_sha256
    assert _digest(inputs.linkml_types) == configuration.linkml_types_sha256
    assert _digest(inputs.population) == configuration.population_sha256
    assert _digest(inputs.generic_recipes) == configuration.generic_recipe_sha256
    assert _digest(inputs.ontology_acceptance) == (
        configuration.ontology_acceptance_sha256
    )
    assert _digest(inputs.protocol_machine) == configuration.protocol_machine_sha256
    assert _digest(EXPERIMENT / "native-query-binding.json") == (
        "sha256:922e2c628a86bca22d761ebf6d453c9056ead8bdc5301e3c5dfb193db61368c1"
    )


def test_frozen_population_is_the_first_unmodified_structural_candidate() -> None:
    population = (EXPERIMENT / "population-run/population.json").read_bytes()
    acquisition = json.loads(
        (EXPERIMENT / "population-run/acquisition-record.json").read_bytes()
    )

    assert subject.classify_population_candidate(
        population,
        success_schema="malleus.paper-v4.population/v2",
        refusal_schema="malleus.paper-v4.population-refusal/v2",
        record_id_prefix="urn:malleus:paper-v4:v2:record:",
        ordinal_width=3,
    ) is subject.PopulationCandidateKind.PROPOSAL
    assert acquisition["status"] == "STRUCTURALLY_ACCEPTED"
    assert acquisition["content_review_performed"] is False
    assert acquisition["human_repair"] is False
    assert acquisition["fallback_population"] is False
    assert acquisition["structural_diagnostic_returns"] == 0
    assert acquisition["structural_retries"] == 0
    assert acquisition["attempts"] == [
        {
            "ordinal": 1,
            "population_path": (
                "paper-v4/experiment-v2/population-run/population.json"
            ),
            "population_sha256": subject._POPULATION_SHA256,
            "envelope_status": "PROPOSAL",
            "compiler_status": "ACCEPTED",
            "record_count": 13,
            "operation_count": 13,
            "provenance_assertion_count": 47,
            "plan_sha256": (
                "sha256:fa1194aa705c36ff6ef06bc3d7bcadbeb4297d44c95a3558e5946fb97dbc09e6"
            ),
        }
    ]


def test_driver_recompiles_the_exact_accepted_ontology_coordinate() -> None:
    inputs = subject.frozen_input_paths(ROOT, Path("private-reading"))

    subject._verify_frozen_compilation(inputs)


def test_module_without_required_arguments_exits_two_with_usage() -> None:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-m", subject.__name__],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "usage:" in result.stderr
    assert "--transaction-time" in result.stderr


def test_driver_orders_build_then_replay_query_then_exclusive_write(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    selected_reading = tmp_path / "reading.json"
    private_run = tmp_path / "private-run"
    results = tmp_path / "results"
    configuration = subject.experiment_configuration(TRANSACTION_TIME)
    inputs = subject.frozen_input_paths(ROOT, selected_reading)
    binding = b"binding"
    build = PaperExperimentRun(b"plan", b"provenance", b"receipt", b"result")
    calls: list[tuple[str, object]] = []
    monkeypatch.setattr(
        subject,
        "_preflight",
        lambda *args: (configuration, inputs, binding),
    )

    def frozen(*args, **kwargs) -> PaperExperimentRun:
        calls.append(("build", kwargs))
        return build

    def query(*args, **kwargs) -> bytes:
        calls.append(("query", (args, kwargs)))
        return b"query-result"

    def write(path: Path, source: bytes) -> None:
        calls.append(("write", (path, source)))

    monkeypatch.setattr(subject, "run_frozen_experiment", frozen)
    monkeypatch.setattr(subject, "run_query_replay", query)
    monkeypatch.setattr(subject, "write_query_result", write)

    run = subject.run_v2_experiment(
        ROOT,
        selected_reading=selected_reading,
        private_run_dir=private_run,
        results_dir=results,
        transaction_time=TRANSACTION_TIME,
    )

    assert [name for name, _ in calls] == ["build", "query", "write"]
    build_arguments = calls[0][1]
    assert isinstance(build_arguments, dict)
    assert set(build_arguments) == {
        "configuration",
        "inputs",
        "private_run_dir",
        "results_dir",
    }
    assert calls[1][1][0][:2] == (b"receipt", binding)
    assert calls[2][1] == (results / "query-result.json", b"query-result")
    assert run == subject.V2ExperimentRun(build, b"query-result")


def test_query_refusal_retains_valid_build_and_creates_no_query_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    selected_reading = tmp_path / "reading.json"
    private_run = tmp_path / "private-run"
    results = tmp_path / "results"
    configuration = subject.experiment_configuration(TRANSACTION_TIME)
    inputs = subject.frozen_input_paths(ROOT, selected_reading)
    monkeypatch.setattr(
        subject,
        "_preflight",
        lambda *args: (configuration, inputs, b"binding"),
    )

    def build(*args, **kwargs) -> PaperExperimentRun:
        results.mkdir()
        for name in (
            "experiment-result.json",
            "population-plan.json",
            "population-provenance.json",
            "replay-receipt.json",
        ):
            (results / name).write_bytes(name.encode())
        return PaperExperimentRun(b"plan", b"provenance", b"receipt", b"result")

    monkeypatch.setattr(subject, "run_frozen_experiment", build)
    monkeypatch.setattr(
        subject,
        "run_query_replay",
        lambda *args, **kwargs: (_ for _ in ()).throw(QueryReplayRefusal("injected")),
    )

    with pytest.raises(QueryReplayRefusal, match="injected"):
        subject.run_v2_experiment(
            ROOT,
            selected_reading=selected_reading,
            private_run_dir=private_run,
            results_dir=results,
            transaction_time=TRANSACTION_TIME,
        )

    assert {path.name for path in results.iterdir()} == {
        "experiment-result.json",
        "population-plan.json",
        "population-provenance.json",
        "replay-receipt.json",
    }
    assert not (results / "query-result.json").exists()


def test_binding_drift_refuses_before_build(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    inputs = subject.frozen_input_paths(ROOT, tmp_path / "reading.json")
    monkeypatch.setattr(subject, "_verify_frozen_compilation", lambda value: None)
    expected = {
        inputs.selected_reading: subject._READING_SHA256,
        inputs.population: subject._POPULATION_SHA256,
    }

    def read_exact(path: Path, digest: str, label: str) -> bytes:
        if path in expected:
            if path == inputs.population:
                return (EXPERIMENT / "population-run/population.json").read_bytes()
            return b"reading"
        raise subject.V2ExperimentRefusal("query binding drifted")

    monkeypatch.setattr(subject, "_read_exact", read_exact)

    with pytest.raises(subject.V2ExperimentRefusal, match="query binding drifted"):
        subject._preflight(ROOT, inputs.selected_reading, TRANSACTION_TIME)


def test_transaction_time_change_cannot_change_any_input_identity() -> None:
    first = subject.experiment_configuration(TRANSACTION_TIME)
    second = subject.experiment_configuration("2026-09-03T09:01:00Z")

    assert first.input_identities() == second.input_identities()
    assert replace(first, transaction_time=second.transaction_time) == second

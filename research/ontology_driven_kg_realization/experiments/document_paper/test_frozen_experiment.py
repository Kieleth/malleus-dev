"""Guards for exclusive publication of the frozen paper-v4 run."""

from __future__ import annotations

from pathlib import Path

import pytest

from research.ontology_driven_kg_realization.experiments.document_paper import (
    frozen_experiment as frozen_module,
)
from research.ontology_driven_kg_realization.experiments.document_paper.experiment_run import (
    PaperExperimentRun,
)
from research.ontology_driven_kg_realization.experiments.document_paper.frozen_experiment import (
    FrozenExperimentRefusal,
    main,
    run_frozen_experiment,
)


def _fixture(root: Path) -> Path:
    experiment = root / "paper-v4/experiment"
    for relative, source in {
        "ontology-run/ontology.yaml": b"ontology",
        "ontology-run/inputs/malleus.yaml": b"malleus",
        "population-run/population.json": b"population",
        "generic-recipes.stottr": b"recipes",
        "native-query-binding.json": b"queries",
        "ontology-run/acceptance.jsonl": b"acceptance",
    }.items():
        path = experiment / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(source)
    reading = root / "private/selected-reading.json"
    reading.parent.mkdir()
    reading.write_bytes(b"reading")
    return reading


def _result() -> PaperExperimentRun:
    return PaperExperimentRun(b"plan", b"provenance", b"receipt", b"result")


def test_run_reads_declared_inputs_and_publishes_exact_bundle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reading = _fixture(tmp_path)
    observed = {}

    def run(ledger_path: Path, **inputs: object) -> PaperExperimentRun:
        observed.update(inputs)
        ledger_path.write_bytes(b"private ledger")
        return _result()

    monkeypatch.setattr(frozen_module, "_linkml_types", lambda: b"linkml")
    monkeypatch.setattr(frozen_module, "run_paper_experiment", run)
    private_run = tmp_path / "private/run"
    results = tmp_path / "paper-v4/experiment/results"

    assert (
        run_frozen_experiment(
            tmp_path,
            selected_reading=reading,
            private_run_dir=private_run,
            results_dir=results,
        )
        == _result()
    )
    assert (private_run / "semantic-ledger.jsonl").read_bytes() == b"private ledger"
    assert {path.name: path.read_bytes() for path in results.iterdir()} == {
        "experiment-result.json": b"result",
        "population-plan.json": b"plan",
        "population-provenance.json": b"provenance",
        "replay-receipt.json": b"receipt",
    }
    assert observed["selected_reading_bytes"] == b"reading"
    for role, locator, source in (
        ("selected_ontology", "paper-v4:marine-ontology", b"ontology"),
        ("malleus_import", "malleus", b"malleus"),
        ("linkml_types", "linkml:types", b"linkml"),
    ):
        exact = observed[role]
        assert exact.locator == locator
        assert exact.source_bytes == source
        assert exact.expected_sha256 == frozen_module._digest(source)
    assert observed["population_bytes"] == b"population"
    assert observed["generic_recipe_bytes"] == b"recipes"
    assert observed["query_binding_bytes"] == b"queries"
    assert observed["ontology_acceptance_bytes"] == b"acceptance"


@pytest.mark.parametrize("existing", ("private", "results"))
def test_run_never_overwrites_an_existing_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    existing: str,
) -> None:
    reading = _fixture(tmp_path)
    private_run = tmp_path / "private/run"
    results = tmp_path / "paper-v4/experiment/results"
    target = private_run if existing == "private" else results
    target.mkdir()
    sentinel = target / "sentinel"
    sentinel.write_bytes(b"keep")
    monkeypatch.setattr(
        frozen_module,
        "run_paper_experiment",
        lambda *args, **kwargs: pytest.fail("run reached after target collision"),
    )

    with pytest.raises(FrozenExperimentRefusal, match="already exists"):
        run_frozen_experiment(
            tmp_path,
            selected_reading=reading,
            private_run_dir=private_run,
            results_dir=results,
        )
    assert sentinel.read_bytes() == b"keep"


def test_failed_run_publishes_no_result_bundle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reading = _fixture(tmp_path)
    results = tmp_path / "paper-v4/experiment/results"
    monkeypatch.setattr(frozen_module, "_linkml_types", lambda: b"linkml")

    def refuse(*args: object, **kwargs: object) -> PaperExperimentRun:
        raise ValueError("compiler refusal")

    monkeypatch.setattr(frozen_module, "run_paper_experiment", refuse)
    with pytest.raises(ValueError, match="compiler refusal"):
        run_frozen_experiment(
            tmp_path,
            selected_reading=reading,
            private_run_dir=tmp_path / "private/run",
            results_dir=results,
        )
    assert not results.exists()


def test_run_refuses_a_source_bearing_ledger_outside_private(
    tmp_path: Path,
) -> None:
    reading = _fixture(tmp_path)
    public_run = tmp_path / "paper-v4/experiment/public-run"

    with pytest.raises(FrozenExperimentRefusal, match="must remain beneath"):
        run_frozen_experiment(
            tmp_path,
            selected_reading=reading,
            private_run_dir=public_run,
            results_dir=tmp_path / "paper-v4/experiment/results",
        )
    assert not public_run.exists()


def test_result_target_created_during_run_is_not_replaced(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reading = _fixture(tmp_path)
    results = tmp_path / "paper-v4/experiment/results"

    def race(ledger_path: Path, **inputs: object) -> PaperExperimentRun:
        ledger_path.write_bytes(b"private ledger")
        results.mkdir()
        (results / "sentinel").write_bytes(b"keep")
        return _result()

    monkeypatch.setattr(frozen_module, "_linkml_types", lambda: b"linkml")
    monkeypatch.setattr(frozen_module, "run_paper_experiment", race)
    with pytest.raises(FrozenExperimentRefusal, match="already exists"):
        run_frozen_experiment(
            tmp_path,
            selected_reading=reading,
            private_run_dir=tmp_path / "private/run",
            results_dir=results,
        )
    assert {path.name: path.read_bytes() for path in results.iterdir()} == {
        "sentinel": b"keep"
    }


def test_missing_declared_input_is_typed_and_creates_no_run(
    tmp_path: Path,
) -> None:
    reading = _fixture(tmp_path)
    (tmp_path / "paper-v4/experiment/population-run/population.json").unlink()
    private_run = tmp_path / "private/run"

    with pytest.raises(FrozenExperimentRefusal, match="population proposal"):
        run_frozen_experiment(
            tmp_path,
            selected_reading=reading,
            private_run_dir=private_run,
            results_dir=tmp_path / "paper-v4/experiment/results",
        )
    assert not private_run.exists()


def test_cli_forwards_all_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    observed = {}

    def run(repository_root: Path, **paths: Path) -> PaperExperimentRun:
        observed["repository_root"] = repository_root
        observed.update(paths)
        return _result()

    monkeypatch.setattr(frozen_module, "run_frozen_experiment", run)
    assert (
        main(
            [
                "--repository-root",
                "/repo",
                "--reading",
                "/repo/private/reading.json",
                "--private-run",
                "/repo/private/run",
                "--results",
                "/repo/paper-v4/experiment/results",
            ]
        )
        == 0
    )
    assert observed == {
        "repository_root": Path("/repo"),
        "selected_reading": Path("/repo/private/reading.json"),
        "private_run_dir": Path("/repo/private/run"),
        "results_dir": Path("/repo/paper-v4/experiment/results"),
    }

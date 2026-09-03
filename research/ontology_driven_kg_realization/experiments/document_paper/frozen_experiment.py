"""Run and publish the exact paper-v4 document experiment."""

from __future__ import annotations

import argparse
from hashlib import sha256
from importlib.resources import files
from pathlib import Path
from typing import Sequence

from .experiment_run import PaperExperimentRun, run_paper_experiment
from .ontology_compile import ExactSource


_EXPERIMENT = Path("paper-v4/experiment")
_LEDGER = "semantic-ledger.jsonl"
_RESULTS = {
    "experiment-result.json": "result_bytes",
    "population-plan.json": "canonical_plan_bytes",
    "population-provenance.json": "provenance_bytes",
    "replay-receipt.json": "replay_receipt_bytes",
}


class FrozenExperimentRefusal(ValueError):
    """The exact run inputs or exclusive publication target are unavailable."""


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _read(path: Path, label: str) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise FrozenExperimentRefusal(
            f"cannot read {label} at {path}: {error}"
        ) from error


def _source(locator: str, source: bytes) -> ExactSource:
    return ExactSource(locator, source, _digest(source))


def _linkml_types() -> bytes:
    try:
        return (
            files("linkml_runtime")
            .joinpath("linkml_model", "model", "schema", "types.yaml")
            .read_bytes()
        )
    except (ImportError, OSError) as error:
        raise FrozenExperimentRefusal(
            "cannot read the declared linkml_runtime types.yaml resource"
        ) from error


def _publish(results_dir: Path, run: PaperExperimentRun) -> None:
    if not results_dir.parent.is_dir():
        raise FrozenExperimentRefusal(
            f"results parent directory does not exist: {results_dir.parent}"
        )
    try:
        results_dir.mkdir()
    except FileExistsError as error:
        raise FrozenExperimentRefusal(
            f"results directory already exists: {results_dir}"
        ) from error
    except OSError as error:
        raise FrozenExperimentRefusal(
            f"cannot create result directory at {results_dir}: {error}"
        ) from error

    created: list[Path] = []
    try:
        for name, attribute in _RESULTS.items():
            path = results_dir / name
            with path.open("xb") as stream:
                created.append(path)
                stream.write(getattr(run, attribute))
    except OSError as error:
        for path in reversed(created):
            try:
                path.unlink()
            except OSError:
                pass
        try:
            results_dir.rmdir()
        except OSError:
            pass
        raise FrozenExperimentRefusal(
            f"cannot publish exact result bundle at {results_dir}: {error}"
        ) from error


def run_frozen_experiment(
    repository_root: Path,
    *,
    selected_reading: Path,
    private_run_dir: Path,
    results_dir: Path,
) -> PaperExperimentRun:
    """Execute once, keep the source-bearing ledger private, then publish results."""

    for value, label in (
        (repository_root, "repository_root"),
        (selected_reading, "selected_reading"),
        (private_run_dir, "private_run_dir"),
        (results_dir, "results_dir"),
    ):
        if not isinstance(value, Path):
            raise TypeError(f"{label} must be a Path")
    if private_run_dir.exists():
        raise FrozenExperimentRefusal(
            f"private run directory already exists: {private_run_dir}"
        )
    if results_dir.exists():
        raise FrozenExperimentRefusal(
            f"results directory already exists: {results_dir}"
        )
    private_root = (repository_root / "private").resolve()
    try:
        private_run_dir.resolve().relative_to(private_root)
    except ValueError as error:
        raise FrozenExperimentRefusal(
            f"private run directory must remain beneath {private_root}"
        ) from error
    if not private_run_dir.parent.is_dir():
        raise FrozenExperimentRefusal(
            f"private run parent does not exist: {private_run_dir.parent}"
        )

    experiment = repository_root / _EXPERIMENT
    ontology = _read(experiment / "ontology-run/ontology.yaml", "selected ontology")
    malleus = _read(
        experiment / "ontology-run/inputs/malleus.yaml",
        "retained Malleus import",
    )
    linkml_types = _linkml_types()
    reading = _read(selected_reading, "selected reading")
    population = _read(
        experiment / "population-run/population.json",
        "population proposal",
    )
    recipes = _read(experiment / "generic-recipes.stottr", "generic recipes")
    queries = _read(experiment / "native-query-binding.json", "query binding")
    acceptance = _read(
        experiment / "ontology-run/acceptance.jsonl",
        "ontology acceptance",
    )

    try:
        private_run_dir.mkdir()
    except OSError as error:
        raise FrozenExperimentRefusal(
            f"cannot create private run directory {private_run_dir}: {error}"
        ) from error
    run = run_paper_experiment(
        private_run_dir / _LEDGER,
        selected_ontology=_source("paper-v4:marine-ontology", ontology),
        malleus_import=_source("malleus", malleus),
        linkml_types=_source("linkml:types", linkml_types),
        selected_reading_bytes=reading,
        population_bytes=population,
        generic_recipe_bytes=recipes,
        query_binding_bytes=queries,
        ontology_acceptance_bytes=acceptance,
    )
    _publish(results_dir, run)
    return run


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--reading", required=True, type=Path)
    parser.add_argument("--private-run", required=True, type=Path)
    parser.add_argument("--results", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    run_frozen_experiment(
        args.repository_root,
        selected_reading=args.reading,
        private_run_dir=args.private_run,
        results_dir=args.results,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

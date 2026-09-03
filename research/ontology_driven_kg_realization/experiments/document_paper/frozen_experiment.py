"""Run and publish the exact paper-v4 document experiment."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from .experiment_run import (
    PaperExperimentConfiguration,
    PaperExperimentRun,
    run_paper_experiment,
)
from .ontology_compile import ExactSource


_LEDGER = "semantic-ledger.jsonl"
_RESULTS = {
    "experiment-result.json": "result_bytes",
    "population-plan.json": "canonical_plan_bytes",
    "population-provenance.json": "provenance_bytes",
    "replay-receipt.json": "replay_receipt_bytes",
}


class FrozenExperimentRefusal(ValueError):
    """The exact run inputs or exclusive publication target are unavailable."""


@dataclass(frozen=True, slots=True)
class FrozenExperimentPaths:
    """Every file consumed by one exact knowledge build."""

    selected_ontology: Path
    malleus_import: Path
    linkml_types: Path
    selected_reading: Path
    population: Path
    generic_recipes: Path
    ontology_acceptance: Path
    protocol_machine: Path

    def __post_init__(self) -> None:
        for field in self.__dataclass_fields__:
            if not isinstance(getattr(self, field), Path):
                raise TypeError(f"{field} must be a Path")


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
    configuration: PaperExperimentConfiguration,
    inputs: FrozenExperimentPaths,
    private_run_dir: Path,
    results_dir: Path,
) -> PaperExperimentRun:
    """Execute once, keep the source-bearing ledger private, then publish results."""

    for value, label in (
        (repository_root, "repository_root"),
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
    if type(configuration) is not PaperExperimentConfiguration:
        raise TypeError("configuration must be one PaperExperimentConfiguration")
    if type(inputs) is not FrozenExperimentPaths:
        raise TypeError("inputs must be one FrozenExperimentPaths")
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

    ontology = _read(inputs.selected_ontology, "selected ontology")
    malleus = _read(inputs.malleus_import, "retained Malleus import")
    linkml_types = _read(inputs.linkml_types, "LinkML types import")
    reading = _read(inputs.selected_reading, "selected reading")
    population = _read(inputs.population, "population proposal")
    recipes = _read(inputs.generic_recipes, "generic recipes")
    acceptance = _read(inputs.ontology_acceptance, "ontology acceptance")
    machine = _read(inputs.protocol_machine, "protocol machine")

    try:
        private_run_dir.mkdir()
    except OSError as error:
        raise FrozenExperimentRefusal(
            f"cannot create private run directory {private_run_dir}: {error}"
        ) from error
    run = run_paper_experiment(
        private_run_dir / _LEDGER,
        configuration=configuration,
        selected_ontology=_source(configuration.ontology_locator, ontology),
        malleus_import=_source(configuration.malleus_import_locator, malleus),
        linkml_types=_source(configuration.linkml_types_locator, linkml_types),
        selected_reading_bytes=reading,
        population_bytes=population,
        generic_recipe_bytes=recipes,
        ontology_acceptance_bytes=acceptance,
        protocol_machine_bytes=machine,
    )
    _publish(results_dir, run)
    return run


__all__ = [
    "FrozenExperimentPaths",
    "FrozenExperimentRefusal",
    "run_frozen_experiment",
]

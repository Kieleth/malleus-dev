"""Run the exact paper-v4 v2 knowledge build and replay-derived queries."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Sequence

from .experiment_run import PaperExperimentConfiguration, PaperExperimentRun
from .frozen_experiment import FrozenExperimentPaths, run_frozen_experiment
from .ontology_compile import ExactSource, compile_exact_ontology
from .population_acquisition import (
    PopulationCandidateKind,
    classify_population_candidate,
)
from .population_compile import PopulationRecipeProfile
from .query_replay import run_query_replay, write_query_result


_DOMAIN = "https://malleus.dev/domains/mid-ocean-ridge-geodynamics/"
_ROOT_LOCATOR = "paper-v4:mid-ocean-ridge-geodynamics"
_SOURCE_SHA256 = "sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9"
_ONTOLOGY_SHA256 = "sha256:7c07f94630277edf4aa1be2515e7627e5ebe42c4c9cfddd6c50b867e9c6291ed"
_READING_SHA256 = "sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17"
_MALLEUS_SHA256 = "sha256:5b737c212a5893ceebb22be207a09f3eb09ebab269898d354bb1dacdaad0aff3"
_LINKML_SHA256 = "sha256:1c79b264397bec0eadb404d22e9b163458f1b889809b3b482ecc39c98743fe00"
_POPULATION_SHA256 = "sha256:d4c6fe42c7f96a86c3116c57bccd9c81e53c2ce6e62b421da714a1915ee79964"
_RECIPES_SHA256 = "sha256:7324dbe955a7f0395d878c4e6198704a4fa11c296b79a66c8a30729ab4fbb968"
_ACCEPTANCE_SHA256 = "sha256:5e5120648765083a64d8ec6143c53e80bf856963ac2256b6500f48d5d80903e4"
_MACHINE_SHA256 = "sha256:ad4d7153c34e67f2edf677c53d228b3a277ee68b0088df4ebc19675c0898c9eb"
_BINDING_SHA256 = "sha256:922e2c628a86bca22d761ebf6d453c9056ead8bdc5301e3c5dfb193db61368c1"
_VALIDATED_CONTRACT_SHA256 = "sha256:292f8777ea24ad06de82c70bd87f1c049eb457fd34b742e2d5db12dd0e6233ae"
_COMPILE_RECEIPT_SHA256 = "sha256:d4595bf34eeed2aaa743e18703eadee7324c89bc2f257c88379405279ea62c69"

CONCRETE_RECORD_TYPES = (
    "ObservationMethod",
    "Instrument",
    "GeologicFeature",
    "SeismicPhenomenon",
    "QuantitativeObservation",
    "GeologicMaterial",
    "ChemicalConstituent",
    "GeologicProcess",
    "CategoricalObservation",
    "MethodUsesInstrumentRelation",
    "FeaturePartOfRelation",
    "SeismicPhenomenonOccursAtRelation",
    "ObservationCharacterizesRelation",
    "ObservationConcernsConstituentRelation",
    "MaterialOccursAtRelation",
    "ProcessActsOnMaterialRelation",
    "ProcessReleasesConstituentRelation",
    "ProcessCausesProcessRelation",
    "ProcessTriggersSeismicPhenomenonRelation",
)
CONTRACT_ONLY_RECORD_TYPES = ("GeoscienceObject", "DomainObservation")


class V2ExperimentRefusal(ValueError):
    """The frozen v2 coordinates cannot produce the declared run."""


@dataclass(frozen=True, slots=True)
class V2ExperimentRun:
    """Exact build and query bytes produced by one v2 invocation."""

    build: PaperExperimentRun
    query_result_bytes: bytes


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _read_exact(path: Path, expected_sha256: str, label: str) -> bytes:
    try:
        source = path.read_bytes()
    except OSError as error:
        raise V2ExperimentRefusal(f"cannot read {label} at {path}: {error}") from error
    observed = _digest(source)
    if observed != expected_sha256:
        raise V2ExperimentRefusal(
            f"{label} drifted: expected {expected_sha256}, observed {observed}"
        )
    return source


def population_recipe_profile() -> PopulationRecipeProfile:
    """Return the complete immutable v2 population-to-recipe mapping."""

    return PopulationRecipeProfile(
        population_schema="malleus.paper-v4.population/v2",
        selected_reading_schema="malleus.paper-v4.text-layer-reading/v1",
        provenance_schema="malleus.paper-v4.population-provenance/v2",
        graph_recipe_profile_iri="https://malleus.dev/graph-recipe/profile/v0",
        recipe_namespace="https://malleus.dev/paper-v4/experiment-v2/recipe/",
        member_namespace="https://malleus.dev/paper-v4/experiment-v2/population/member/",
        record_type_templates=tuple(
            (name, name + "-1.0.0") for name in CONCRETE_RECORD_TYPES
        ),
    )


def experiment_configuration(transaction_time: str) -> PaperExperimentConfiguration:
    """Return every frozen build coordinate plus one explicit run time."""

    return PaperExperimentConfiguration(
        result_schema="malleus.paper-v4.knowledge-build-result/v2",
        source_sha256=_SOURCE_SHA256,
        ontology_sha256=_ONTOLOGY_SHA256,
        reading_sha256=_READING_SHA256,
        malleus_import_sha256=_MALLEUS_SHA256,
        linkml_types_sha256=_LINKML_SHA256,
        population_sha256=_POPULATION_SHA256,
        generic_recipe_sha256=_RECIPES_SHA256,
        ontology_acceptance_sha256=_ACCEPTANCE_SHA256,
        protocol_machine_sha256=_MACHINE_SHA256,
        population_recipe_profile=population_recipe_profile(),
        record_type_iris=tuple(
            _DOMAIN + name
            for name in (*CONCRETE_RECORD_TYPES, *CONTRACT_ONLY_RECORD_TYPES)
        ),
        contract_id="https://malleus.dev/contracts/paper-v4/experiment-v2",
        transaction_time=transaction_time,
        ontology_locator=_ROOT_LOCATOR,
        malleus_import_locator="malleus",
        linkml_types_locator="linkml:types",
    )


def frozen_input_paths(
    repository_root: Path, selected_reading: Path
) -> FrozenExperimentPaths:
    """Resolve the exact repository-owned and private v2 input paths."""

    if not isinstance(repository_root, Path) or not isinstance(selected_reading, Path):
        raise TypeError("repository_root and selected_reading must be Paths")
    experiment = repository_root / "paper-v4/experiment-v2"
    return FrozenExperimentPaths(
        selected_ontology=experiment / "ontology-run/ontology-02.yaml",
        malleus_import=experiment / "ontology-run/inputs/malleus.yaml",
        linkml_types=experiment / "run-inputs/linkml-types.yaml",
        selected_reading=selected_reading,
        population=experiment / "population-run/population.json",
        generic_recipes=experiment / "generic-recipes.stottr",
        ontology_acceptance=experiment / "ontology-run/acceptance.jsonl",
        protocol_machine=experiment / "run-inputs/protocol-machine.json",
    )


def _verify_frozen_compilation(inputs: FrozenExperimentPaths) -> None:
    ontology = _read_exact(inputs.selected_ontology, _ONTOLOGY_SHA256, "ontology")
    malleus = _read_exact(inputs.malleus_import, _MALLEUS_SHA256, "Malleus import")
    linkml = _read_exact(inputs.linkml_types, _LINKML_SHA256, "LinkML types")
    result = compile_exact_ontology(
        root=ExactSource(_ROOT_LOCATOR, ontology, _ONTOLOGY_SHA256),
        malleus=ExactSource("malleus", malleus, _MALLEUS_SHA256),
        linkml_types=ExactSource("linkml:types", linkml, _LINKML_SHA256),
    )
    if _digest(result.validated_contract_bytes) != _VALIDATED_CONTRACT_SHA256:
        raise V2ExperimentRefusal("recompiled validated contract differs from acceptance")
    if _digest(result.receipt_bytes) != _COMPILE_RECEIPT_SHA256:
        raise V2ExperimentRefusal("recompiled ontology receipt differs from acceptance")


def _preflight(
    repository_root: Path,
    selected_reading: Path,
    transaction_time: str,
) -> tuple[PaperExperimentConfiguration, FrozenExperimentPaths, bytes]:
    configuration = experiment_configuration(transaction_time)
    inputs = frozen_input_paths(repository_root, selected_reading)
    _verify_frozen_compilation(inputs)
    _read_exact(inputs.selected_reading, _READING_SHA256, "selected reading")
    population = _read_exact(inputs.population, _POPULATION_SHA256, "population")
    kind = classify_population_candidate(
        population,
        success_schema="malleus.paper-v4.population/v2",
        refusal_schema="malleus.paper-v4.population-refusal/v2",
        record_id_prefix="urn:malleus:paper-v4:v2:record:",
        ordinal_width=3,
    )
    if kind is PopulationCandidateKind.MODEL_REFUSAL:
        raise V2ExperimentRefusal("model population refusal is terminal")
    binding_path = repository_root / "paper-v4/experiment-v2/native-query-binding.json"
    binding = _read_exact(binding_path, _BINDING_SHA256, "query binding")
    return configuration, inputs, binding


def run_v2_experiment(
    repository_root: Path,
    *,
    selected_reading: Path,
    private_run_dir: Path,
    results_dir: Path,
    transaction_time: str,
) -> V2ExperimentRun:
    """Build accepted history, then query only its replay receipt."""

    for value, label in (
        (repository_root, "repository_root"),
        (selected_reading, "selected_reading"),
        (private_run_dir, "private_run_dir"),
        (results_dir, "results_dir"),
    ):
        if not isinstance(value, Path):
            raise TypeError(f"{label} must be a Path")
    configuration, inputs, binding = _preflight(
        repository_root,
        selected_reading,
        transaction_time,
    )
    build = run_frozen_experiment(
        repository_root,
        configuration=configuration,
        inputs=inputs,
        private_run_dir=private_run_dir,
        results_dir=results_dir,
    )
    ontology = inputs.selected_ontology.read_bytes()
    malleus = inputs.malleus_import.read_bytes()
    query_result = run_query_replay(
        build.replay_receipt_bytes,
        binding,
        ontology_path=inputs.selected_ontology,
        ontology_source=ontology,
        malleus_path=inputs.malleus_import,
        malleus_source=malleus,
    )
    write_query_result(results_dir / "query-result.json", query_result)
    return V2ExperimentRun(build, query_result)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--selected-reading", required=True, type=Path)
    parser.add_argument("--private-run", required=True, type=Path)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--transaction-time", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    run_v2_experiment(
        args.repository_root,
        selected_reading=args.selected_reading,
        private_run_dir=args.private_run,
        results_dir=args.results,
        transaction_time=args.transaction_time,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())


__all__ = [
    "CONCRETE_RECORD_TYPES",
    "CONTRACT_ONLY_RECORD_TYPES",
    "V2ExperimentRefusal",
    "V2ExperimentRun",
    "experiment_configuration",
    "frozen_input_paths",
    "main",
    "population_recipe_profile",
    "run_v2_experiment",
]

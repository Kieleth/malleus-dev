"""Guards for exclusive publication of the frozen paper-v4 run."""

from __future__ import annotations

from dataclasses import MISSING, fields
from hashlib import sha256
import inspect
from pathlib import Path

import pytest

from research.ontology_driven_kg_realization.experiments.document_paper import (
    frozen_experiment as frozen_module,
)
from research.ontology_driven_kg_realization.experiments.document_paper.experiment_run import (
    PaperExperimentConfiguration,
    PaperExperimentRun,
)
from research.ontology_driven_kg_realization.experiments.document_paper.frozen_experiment import (
    FrozenExperimentPaths,
    FrozenExperimentRefusal,
    run_frozen_experiment,
)
from research.ontology_driven_kg_realization.experiments.document_paper.population_compile import (
    PopulationRecipeProfile,
)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _fixture(root: Path) -> FrozenExperimentPaths:
    input_root = root / "inputs"
    (root / "private").mkdir()
    (root / "paper-v4/experiment").mkdir(parents=True)
    paths = {}
    for role, source in {
        "selected_ontology": b"ontology",
        "malleus_import": b"malleus",
        "linkml_types": b"linkml",
        "selected_reading": b"reading",
        "population": b"population",
        "generic_recipes": b"recipes",
        "ontology_acceptance": b"acceptance",
        "protocol_machine": b"machine",
    }.items():
        path = input_root / role
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(source)
        paths[role] = path
    return FrozenExperimentPaths(**paths)


def _configuration(inputs: FrozenExperimentPaths) -> PaperExperimentConfiguration:
    return PaperExperimentConfiguration(
        result_schema="fiction.knowledge-build-result/v2",
        source_sha256="sha256:" + "1" * 64,
        ontology_sha256=_digest(inputs.selected_ontology.read_bytes()),
        reading_sha256=_digest(inputs.selected_reading.read_bytes()),
        malleus_import_sha256=_digest(inputs.malleus_import.read_bytes()),
        linkml_types_sha256=_digest(inputs.linkml_types.read_bytes()),
        population_sha256=_digest(inputs.population.read_bytes()),
        generic_recipe_sha256=_digest(inputs.generic_recipes.read_bytes()),
        ontology_acceptance_sha256=_digest(inputs.ontology_acceptance.read_bytes()),
        protocol_machine_sha256=_digest(inputs.protocol_machine.read_bytes()),
        population_recipe_profile=PopulationRecipeProfile(
            population_schema="fiction.population/v2",
            selected_reading_schema="fiction.reading/v2",
            provenance_schema="fiction.provenance/v2",
            graph_recipe_profile_iri="https://example.test/profile/v2",
            recipe_namespace="https://example.test/recipe/",
            member_namespace="https://example.test/member/",
            record_type_templates=(("FictionRecord", "FictionRecord-1.0.0"),),
        ),
        record_type_iris=("https://example.test/FictionRecord",),
        contract_id="https://example.test/contract",
        transaction_time="2026-09-02T00:00:00Z",
        ontology_locator="fiction:ontology",
        malleus_import_locator="malleus",
        linkml_types_locator="linkml:types",
    )


def _result() -> PaperExperimentRun:
    return PaperExperimentRun(b"plan", b"provenance", b"receipt", b"result")


def test_run_reads_declared_inputs_and_publishes_exact_bundle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    inputs = _fixture(tmp_path)
    configuration = _configuration(inputs)
    observed = {}

    def run(ledger_path: Path, **inputs: object) -> PaperExperimentRun:
        observed.update(inputs)
        ledger_path.write_bytes(b"private ledger")
        return _result()

    monkeypatch.setattr(frozen_module, "run_paper_experiment", run)
    private_run = tmp_path / "private/run"
    results = tmp_path / "paper-v4/experiment/results"

    assert (
        run_frozen_experiment(
            tmp_path,
            configuration=configuration,
            inputs=inputs,
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
        ("selected_ontology", "fiction:ontology", b"ontology"),
        ("malleus_import", "malleus", b"malleus"),
        ("linkml_types", "linkml:types", b"linkml"),
    ):
        exact = observed[role]
        assert exact.locator == locator
        assert exact.source_bytes == source
        assert exact.expected_sha256 == frozen_module._digest(source)
    assert observed["population_bytes"] == b"population"
    assert observed["generic_recipe_bytes"] == b"recipes"
    assert observed["ontology_acceptance_bytes"] == b"acceptance"
    assert observed["protocol_machine_bytes"] == b"machine"
    assert observed["configuration"] is configuration
    assert "query_binding_bytes" not in observed


@pytest.mark.parametrize("existing", ("private", "results"))
def test_run_never_overwrites_an_existing_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    existing: str,
) -> None:
    inputs = _fixture(tmp_path)
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
            configuration=_configuration(inputs),
            inputs=inputs,
            private_run_dir=private_run,
            results_dir=results,
        )
    assert sentinel.read_bytes() == b"keep"


def test_failed_run_publishes_no_result_bundle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    inputs = _fixture(tmp_path)
    results = tmp_path / "paper-v4/experiment/results"

    def refuse(*args: object, **kwargs: object) -> PaperExperimentRun:
        raise ValueError("compiler refusal")

    monkeypatch.setattr(frozen_module, "run_paper_experiment", refuse)
    with pytest.raises(ValueError, match="compiler refusal"):
        run_frozen_experiment(
            tmp_path,
            configuration=_configuration(inputs),
            inputs=inputs,
            private_run_dir=tmp_path / "private/run",
            results_dir=results,
        )
    assert not results.exists()


def test_run_refuses_a_source_bearing_ledger_outside_private(
    tmp_path: Path,
) -> None:
    inputs = _fixture(tmp_path)
    public_run = tmp_path / "paper-v4/experiment/public-run"

    with pytest.raises(FrozenExperimentRefusal, match="must remain beneath"):
        run_frozen_experiment(
            tmp_path,
            configuration=_configuration(inputs),
            inputs=inputs,
            private_run_dir=public_run,
            results_dir=tmp_path / "paper-v4/experiment/results",
        )
    assert not public_run.exists()


def test_result_target_created_during_run_is_not_replaced(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    inputs = _fixture(tmp_path)
    results = tmp_path / "paper-v4/experiment/results"

    def race(ledger_path: Path, **inputs: object) -> PaperExperimentRun:
        ledger_path.write_bytes(b"private ledger")
        results.mkdir()
        (results / "sentinel").write_bytes(b"keep")
        return _result()

    monkeypatch.setattr(frozen_module, "run_paper_experiment", race)
    with pytest.raises(FrozenExperimentRefusal, match="already exists"):
        run_frozen_experiment(
            tmp_path,
            configuration=_configuration(inputs),
            inputs=inputs,
            private_run_dir=tmp_path / "private/run",
            results_dir=results,
        )
    assert {path.name: path.read_bytes() for path in results.iterdir()} == {
        "sentinel": b"keep"
    }


def test_missing_declared_input_is_typed_and_creates_no_run(
    tmp_path: Path,
) -> None:
    inputs = _fixture(tmp_path)
    configuration = _configuration(inputs)
    inputs.population.unlink()
    private_run = tmp_path / "private/run"

    with pytest.raises(FrozenExperimentRefusal, match="population proposal"):
        run_frozen_experiment(
            tmp_path,
            configuration=configuration,
            inputs=inputs,
            private_run_dir=private_run,
            results_dir=tmp_path / "paper-v4/experiment/results",
        )
    assert not private_run.exists()


def test_paths_have_no_defaults_and_legacy_query_path_is_dead() -> None:
    assert all(
        field.default is MISSING and field.default_factory is MISSING
        for field in fields(FrozenExperimentPaths)
    )
    signature = inspect.signature(run_frozen_experiment)
    assert "selected_reading" not in signature.parameters
    source = inspect.getsource(frozen_module)
    assert "native-query-binding" not in source
    assert "query_binding_bytes" not in source

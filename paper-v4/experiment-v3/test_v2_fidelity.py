"""The manifest-driven harness must reproduce the frozen v2 run byte for byte."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import shutil
import uuid

import pytest

from research.ontology_driven_kg_realization.experiments.document_paper.multimodel import (
    RunManifest,
    acceptance_event,
    binding_closure,
    compile_manifest_ontology,
    contract_only_types,
    derive_run_artifacts,
    extract_delimited,
    render_population_brief,
    run_manifest_experiment,
)


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "paper-v4/experiment-v3/runs/codex-gpt-5.6-v2/run-manifest.json"
V2 = ROOT / "paper-v4/experiment-v2"
V2_TRANSACTION_TIME = "2026-09-03T09:11:42Z"
V2_LEDGER_SHA256 = "df5327be6abfabfb49342a0663185d81b8a8056211108ca759ea7cac2901e828"


def _digest(source: bytes) -> str:
    return sha256(source).hexdigest()


@pytest.fixture(scope="module")
def manifest() -> RunManifest:
    return RunManifest.load(MANIFEST)


def test_binding_closure_is_the_v2_constructible_set(manifest: RunManifest) -> None:
    binding = json.loads((ROOT / manifest.paths["binding"]).read_bytes())
    entities, relations = binding_closure(binding)
    assert set(entities) == set(manifest.entity_types)
    assert set(relations) == set(manifest.relation_types)


def test_contract_only_types_are_the_v2_abstract_ranges(manifest: RunManifest) -> None:
    ontology, _, _, _ = compile_manifest_ontology(ROOT, manifest)
    assert set(contract_only_types(ontology, manifest.constructible)) == set(
        manifest.contract_only_types
    )


def test_derived_recipes_equal_the_frozen_v2_bytes(manifest: RunManifest) -> None:
    derived = derive_run_artifacts(ROOT, manifest)
    assert derived["recipes"] == (V2 / "generic-recipes.stottr").read_bytes()


def test_derived_brief_sections_equal_the_frozen_v2_task_text(
    manifest: RunManifest,
) -> None:
    derived = derive_run_artifacts(ROOT, manifest)["brief_sections"].decode("utf-8")
    task = (V2 / "population-run/task.md").read_text(encoding="utf-8")
    start = task.index("## Constructible entity types")
    end = task.index("Every relation has an empty `properties` object")
    frozen_bullets = [
        line for line in task[start:end].splitlines()
        if line.startswith(("- `", "## "))
    ]
    derived_bullets = [
        line for line in derived.splitlines() if line.startswith(("- `", "## "))
    ]
    assert derived_bullets == frozen_bullets


def test_acceptance_event_equals_the_frozen_v2_bytes(manifest: RunManifest) -> None:
    assert acceptance_event(manifest.sha256["ontology"]) == (
        V2 / "ontology-run/acceptance.jsonl"
    ).read_bytes()


def test_population_brief_renders_the_frozen_v2_task_bytes(
    manifest: RunManifest,
) -> None:
    template = (V2 / "population-run/task.md").read_text(encoding="utf-8")
    sections = derive_run_artifacts(ROOT, manifest)["brief_sections"].decode("utf-8")
    rendered = render_population_brief(
        template,
        ontology_sha256=manifest.sha256["ontology"],
        reading_path=(
            "/Users/luis/Projects/malleus-dev/.claude/worktrees/paper-v4-lean/"
            "private/paper-v4-text-layer/selected-reading.json"
        ),
        sections=sections,
    )
    assert rendered == (V2 / "population-run/task.md").read_bytes()


def test_delimited_extraction_recovers_the_frozen_v2_ontology_bytes() -> None:
    ontology = (V2 / "ontology-run/ontology-02.yaml").read_bytes()
    report = "preamble\n`BEGIN_ONTOLOGY_YAML`\n" + ontology.decode() + "END_ONTOLOGY_YAML\n"
    assert extract_delimited(report, "BEGIN_ONTOLOGY_YAML", "END_ONTOLOGY_YAML") == ontology


def test_manifest_run_reproduces_the_frozen_v2_result_bytes(
    manifest: RunManifest,
) -> None:
    scratch = ROOT / "private" / f"paper-v4-v3-fidelity-{uuid.uuid4().hex[:8]}"
    scratch.mkdir()
    try:
        run_manifest_experiment(
            ROOT,
            MANIFEST,
            private_run_dir=scratch / "run",
            results_dir=scratch / "results",
            transaction_time=V2_TRANSACTION_TIME,
        )
        for name in (
            "experiment-result.json",
            "population-plan.json",
            "population-provenance.json",
            "replay-receipt.json",
            "query-result.json",
        ):
            assert (scratch / "results" / name).read_bytes() == (
                V2 / "results" / name
            ).read_bytes(), name
        ledger = (scratch / "run" / "semantic-ledger.jsonl").read_bytes()
        assert _digest(ledger) == V2_LEDGER_SHA256
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

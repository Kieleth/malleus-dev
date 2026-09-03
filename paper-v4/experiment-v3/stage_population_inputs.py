"""Freeze one run's population-stage inputs from its accepted ontology and binding.

Derives the constructible closure, recipes and brief sections mechanically, renders
the v2 population brief with this run's coordinates, copies the model-visible
inputs, and writes the v2-schema input manifest.

Usage: stage_population_inputs.py --run-dir <run dir> --reading <abs path>
       --write-tool "the Write tool"
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from research.ontology_driven_kg_realization.experiments.document_paper.compiled_graph_recipe_contract import (  # noqa: E402
    derive_compiled_logical_contract,
)
from research.ontology_driven_kg_realization.experiments.document_paper.multimodel import (  # noqa: E402
    binding_closure,
    contract_only_types,
    domain_iri,
    load_ontology,
    population_brief_sections,
    recipe_document,
    render_population_brief,
    run_namespaces,
)
from research.ontology_driven_kg_realization.experiments.document_paper.ontology_compile import (  # noqa: E402
    ExactSource,
    compile_exact_ontology,
)

V2 = ROOT / "paper-v4/experiment-v2"
MALLEUS = V2 / "ontology-run/inputs/malleus.yaml"
LINKML = V2 / "run-inputs/linkml-types.yaml"
QUESTIONS = V2 / "population-run/inputs/competency-questions.json"
TEMPLATE = V2 / "population-run/task.md"


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _write_new(path: Path, source: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(source)


def _source(locator: str, path: Path) -> ExactSource:
    source = path.read_bytes()
    return ExactSource(locator, source, _digest(source))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--reading", required=True, type=Path)
    parser.add_argument("--write-tool", required=True)
    args = parser.parse_args()
    run = args.run_dir
    run_id = run.name
    acceptance = json.loads((run / "ontology-run/acceptance.jsonl").read_bytes())
    ontology_path = next(
        p for p in sorted((run / "ontology-run").glob("ontology-*.yaml"))
        if _digest(p.read_bytes()) == acceptance["ontology_sha256"]
    )
    ontology_bytes = ontology_path.read_bytes()
    ontology = load_ontology(ontology_bytes)
    binding = json.loads((run / "native-query-binding.json").read_bytes())
    entities, relations = binding_closure(binding)
    constructible = (*entities, *relations)
    extra = contract_only_types(ontology, constructible)
    domain = domain_iri(ontology)
    names = run_namespaces(run_id)
    result = compile_exact_ontology(
        root=_source(names["root_locator"], ontology_path),
        malleus=_source("malleus", MALLEUS),
        linkml_types=_source("linkml:types", LINKML),
    )
    contract = derive_compiled_logical_contract(
        result.compilation,
        record_type_iris=tuple(domain + name for name in (*constructible, *extra)),
        contract_id=names["contract_id"],
    )
    recipes = recipe_document(
        ontology, contract, constructible, recipe_namespace=names["recipe_namespace"]
    )
    sections = population_brief_sections(
        ontology, contract, entities, relations,
        root_ontology=yaml.safe_load(MALLEUS.read_bytes()),
    )
    brief = render_population_brief(
        TEMPLATE.read_text(encoding="utf-8"),
        ontology_sha256=acceptance["ontology_sha256"],
        reading_path=str(args.reading),
        sections=sections,
        write_tool=args.write_tool,
    )
    pop = run / "population-run"
    _write_new(run / "generic-recipes.stottr", recipes)
    _write_new(pop / "task.md", brief)
    _write_new(pop / "inputs/ontology.yaml", ontology_bytes)
    _write_new(pop / "inputs/generic-recipes.stottr", recipes)
    shutil.copyfile(QUESTIONS, pop / "inputs/competency-questions.json")
    reading = args.reading.read_bytes()
    files = [
        ("TASK", pop / "task.md"),
        ("SELECTED_ONTOLOGY", pop / "inputs/ontology.yaml"),
        ("GENERIC_RECIPES", pop / "inputs/generic-recipes.stottr"),
        ("COMPETENCY_QUESTIONS", pop / "inputs/competency-questions.json"),
    ]
    v2_manifest = json.loads((V2 / "population-run/input-manifest.json").read_bytes())
    manifest = {
        "schema": v2_manifest["schema"],
        "frozen_at": None,
        "status": v2_manifest["status"],
        "attempt_policy": v2_manifest["attempt_policy"],
        "session_policy": v2_manifest["session_policy"],
        "files": [
            {"role": role, "locator": str(path.relative_to(ROOT)), "sha256": _digest(path.read_bytes())}
            for role, path in files
        ]
        + [{"role": "SELECTED_READING", "locator": str(args.reading), "sha256": _digest(reading)}],
        "success_schema": v2_manifest["success_schema"],
        "refusal_schema": v2_manifest["refusal_schema"],
        "constructible": {
            "entity_types": list(entities),
            "relation_types": list(relations),
            "contract_only_types": list(extra),
        },
    }
    from datetime import datetime, timezone

    manifest["frozen_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _write_new(pop / "input-manifest.json", (json.dumps(manifest, indent=2) + "\n").encode("utf-8"))
    for item in manifest["files"]:
        print(f"{item['role']:22} {item['sha256']}  {item['locator']}")
    print("constructible:", len(entities), "entities,", len(relations), "relations, contract-only", extra)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

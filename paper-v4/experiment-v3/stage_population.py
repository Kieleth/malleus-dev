"""Classify and structurally compile one population attempt before the full run.

On refusal the exact diagnostic bytes are retained as compile-attempt-NN.json and
printed for return to the same producer session (one structural retry allowed).

Usage: stage_population.py --run-dir <run dir> --attempt N [--candidate <path>]
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from malleus.ledger import canonical_json  # noqa: E402

from research.ontology_driven_kg_realization.experiments.document_paper.compiled_graph_recipe_contract import (  # noqa: E402
    derive_compiled_logical_contract,
)
from research.ontology_driven_kg_realization.experiments.document_paper.multimodel import (  # noqa: E402
    domain_iri,
    load_ontology,
    recipe_profile,
    run_namespaces,
)
from research.ontology_driven_kg_realization.experiments.document_paper.ontology_compile import (  # noqa: E402
    ExactSource,
    compile_exact_ontology,
)
from research.ontology_driven_kg_realization.experiments.document_paper.population_acquisition import (  # noqa: E402
    PopulationAcquisitionError,
    PopulationCandidateKind,
    classify_population_candidate,
)
from research.ontology_driven_kg_realization.experiments.document_paper.population_compile import (  # noqa: E402
    PopulationCompileRefusal,
    compile_population,
)

V2 = ROOT / "paper-v4/experiment-v2"


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _source(locator: str, path: Path) -> ExactSource:
    source = path.read_bytes()
    return ExactSource(locator, source, _digest(source))


def _write_new(path: Path, source: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(source)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--attempt", required=True, type=int)
    parser.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    run = args.run_dir.resolve()
    run_id = run.name
    pop = run / "population-run"
    ordinal = f"{args.attempt:02d}"
    candidate = args.candidate or (pop / "population.json")
    retained = pop / f"population-attempt-{ordinal}.json"
    if candidate.resolve() != retained.resolve():
        shutil.copyfile(candidate, retained)
    population = retained.read_bytes()
    print(f"population-attempt-{ordinal}.json {len(population)} bytes {_digest(population)}")

    inputs = json.loads((pop / "input-manifest.json").read_bytes())
    constructible = (
        *inputs["constructible"]["entity_types"],
        *inputs["constructible"]["relation_types"],
    )
    extra = inputs["constructible"]["contract_only_types"]
    reading = Path(
        next(i["locator"] for i in inputs["files"] if i["role"] == "SELECTED_READING")
    ).read_bytes()
    acceptance = json.loads((run / "ontology-run/acceptance.jsonl").read_bytes())
    ontology_path = next(
        p for p in sorted((run / "ontology-run").glob("ontology-*.yaml"))
        if _digest(p.read_bytes()) == acceptance["ontology_sha256"]
    )
    ontology = load_ontology(ontology_path.read_bytes())
    domain = domain_iri(ontology)
    compiled = compile_exact_ontology(
        root=_source(run_namespaces(run_id)["root_locator"], ontology_path),
        malleus=_source("malleus", V2 / "ontology-run/inputs/malleus.yaml"),
        linkml_types=_source("linkml:types", V2 / "run-inputs/linkml-types.yaml"),
    )
    contract = derive_compiled_logical_contract(
        compiled.compilation,
        record_type_iris=tuple(domain + name for name in (*constructible, *extra)),
        contract_id=run_namespaces(run_id)["contract_id"],
    )
    names = run_namespaces(run_id)
    profile = recipe_profile(
        constructible,
        recipe_namespace=names["recipe_namespace"],
        member_namespace=names["member_namespace"],
    )
    try:
        kind = classify_population_candidate(
            population,
            success_schema="malleus.paper-v4.population/v2",
            refusal_schema="malleus.paper-v4.population-refusal/v2",
            record_id_prefix="urn:malleus:paper-v4:v2:record:",
            ordinal_width=3,
        )
        if kind is PopulationCandidateKind.MODEL_REFUSAL:
            print("MODEL_REFUSAL (terminal)")
            return 2
        compilation = compile_population(
            population,
            compiled_ontology=compiled.compilation,
            logical_contract=contract,
            generic_recipe_bytes=(run / "generic-recipes.stottr").read_bytes(),
            selected_reading_bytes=reading,
            recipe_profile=profile,
        )
    except PopulationAcquisitionError as refusal:
        diagnostic = refusal.canonical_diagnostic_bytes()
    except PopulationCompileRefusal as refusal:
        diagnostic = (
            canonical_json(
                {"stage": "POPULATION_COMPILE", "status": "REFUSED", **refusal.as_dict()}
            )
        ).encode("utf-8")
    else:
        records = json.loads(population)["records"]
        entities = sum(1 for r in records if "source" not in r)
        print(
            f"STRUCTURALLY_ACCEPTED records={len(records)} entities={entities} "
            f"relations={len(records) - entities} operations={len(compilation.plan.operations)} "
            f"plan={_digest(compilation.plan.canonical_bytes()) if hasattr(compilation.plan, 'canonical_bytes') else 'n/a'}"
        )
        return 0
    _write_new(pop / f"compile-attempt-{ordinal}.json", diagnostic)
    print(f"REFUSED compile-attempt-{ordinal}.json {_digest(diagnostic)}")
    print(diagnostic.decode("utf-8"))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

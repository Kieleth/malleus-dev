"""Assemble one run manifest from a run directory whose population exists.

Usage: build_run_manifest.py --run-dir <run dir>
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from research.ontology_driven_kg_realization.experiments.document_paper.multimodel import (  # noqa: E402
    MANIFEST_SCHEMA,
    RunManifest,
    run_namespaces,
)

V2 = "paper-v4/experiment-v2"


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    args = parser.parse_args()
    run = args.run_dir.resolve()
    run_id = run.name
    rel = run.relative_to(ROOT)
    inputs = json.loads((run / "population-run/input-manifest.json").read_bytes())
    acceptance = json.loads((run / "ontology-run/acceptance.jsonl").read_bytes())
    ontology = next(
        p for p in sorted((run / "ontology-run").glob("ontology-*.yaml"))
        if _digest(p) == acceptance["ontology_sha256"]
    )
    reading = next(
        item["locator"] for item in inputs["files"] if item["role"] == "SELECTED_READING"
    )
    paths = {
        "source": "paper-v4/source/yu-et-al-2025-mid-atlantic-ridge.pdf",
        "ontology": str(ontology.relative_to(ROOT)),
        "malleus": f"{V2}/ontology-run/inputs/malleus.yaml",
        "linkml": f"{V2}/run-inputs/linkml-types.yaml",
        "reading": str(Path(reading).resolve().relative_to(ROOT)),
        "population": f"{rel}/population-run/population.json",
        "recipes": f"{rel}/generic-recipes.stottr",
        "acceptance": f"{rel}/ontology-run/acceptance.jsonl",
        "machine": f"{V2}/run-inputs/protocol-machine.json",
        "binding": f"{rel}/native-query-binding.json",
    }
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "run_id": run_id,
        **run_namespaces(run_id),
        "entity_types": inputs["constructible"]["entity_types"],
        "relation_types": inputs["constructible"]["relation_types"],
        "contract_only_types": inputs["constructible"]["contract_only_types"],
        "paths": paths,
        "sha256": {role: _digest(ROOT / path) for role, path in paths.items()},
    }
    target = run / "run-manifest.json"
    with target.open("xb") as stream:
        stream.write((json.dumps(manifest, indent=2) + "\n").encode("utf-8"))
    RunManifest.load(target)
    for role, digest in manifest["sha256"].items():
        print(f"{role:11} {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

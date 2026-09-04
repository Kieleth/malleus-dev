"""Print one comparison table over the frozen runs (v2 reference and v3 producers).

Every value is read from retained artifacts; nothing is computed from prose.
Usage: summarize_runs.py [--markdown]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

RUNS = ROOT / "paper-v4/experiment-v3/runs"


def _ontology_shape(path: Path) -> dict[str, int]:
    document = yaml.safe_load(path.read_bytes())
    classes = document.get("classes") or {}
    entities = [n for n, c in classes.items() if (c or {}).get("is_a") != "Relation" and not n.endswith("Relation")]
    relations = [n for n in classes if n not in entities]
    return {
        "entity_classes": len(entities),
        "relation_classes": len(relations),
        "enums": len(document.get("enums") or {}),
    }


def _v2_reference() -> dict[str, object]:
    v2 = ROOT / "paper-v4/experiment-v2"
    ontology = json.loads((v2 / "ontology-run/acquisition-record.json").read_bytes())
    population = json.loads((v2 / "population-run/acquisition-record.json").read_bytes())
    return _row(
        run_id="codex-gpt-5.6-v2",
        producer="gpt-5.6-sol (Codex, effort ultra)",
        ontology_path=v2 / "ontology-run/ontology-02.yaml",
        ontology_attempts=len(ontology["attempts"]),
        facts=ontology["attempts"][-1]["fact_count"],
        binding=v2 / "native-query-binding.json",
        population_attempts=len(population["attempts"]),
        population_records=population["attempts"][-1]["record_count"],
        results=v2 / "results",
    )


def _v3_run(run: Path) -> dict[str, object] | None:
    if not (run / "results/query-result.json").exists():
        return None
    ontology = json.loads((run / "ontology-run/acquisition-record.json").read_bytes())
    population = json.loads((run / "population-run/acquisition-record.json").read_bytes())
    return _row(
        run_id=run.name,
        producer=f"{ontology['producer']['model_family']} (Claude Code, harness default effort)",
        ontology_path=ROOT / ontology["selected_ontology_path"],
        ontology_attempts=len(ontology["attempts"]),
        facts=ontology["attempts"][-1]["fact_count"],
        binding=run / "native-query-binding.json",
        population_attempts=len(population["attempts"]),
        population_records=population["attempts"][-1]["record_count"],
        results=run / "results",
    )


def _row(*, run_id, producer, ontology_path, ontology_attempts, facts, binding, population_attempts, population_records, results) -> dict[str, object]:
    shape = _ontology_shape(ontology_path)
    binding_doc = json.loads(binding.read_bytes())
    result = json.loads((results / "experiment-result.json").read_bytes())
    query = json.loads((results / "query-result.json").read_bytes())
    receipt = json.loads((results / "replay-receipt.json").read_bytes())
    return {
        "run": run_id,
        "producer": producer,
        "ontology attempts": ontology_attempts,
        "entity classes": shape["entity_classes"],
        "relation classes": shape["relation_classes"],
        "enums": shape["enums"],
        "compiled facts": facts,
        "binding cases": [len(q["cases"]) for q in binding_doc["queries"]],
        "population attempts": population_attempts,
        "population records": population_records,
        "graph entities": result["entity_count"],
        "graph relations": result["relation_count"],
        "ledger events": receipt["ledger_event_count"],
        "rows CQ1..CQ4": [len(q["rows"]) for q in query["queries"]],
        "guard attempts": sum(query["forbidden_attempts"].values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()
    rows = [_v2_reference()]
    for run in sorted(RUNS.iterdir()):
        if run.name == "codex-gpt-5.6-v2":
            continue
        row = _v3_run(run)
        if row:
            rows.append(row)
    keys = list(rows[0])
    if args.markdown:
        print("| " + " | ".join(keys) + " |")
        print("|" + "---|" * len(keys))
        for row in rows:
            print("| " + " | ".join(str(row[k]) for k in keys) + " |")
    else:
        for row in rows:
            print(json.dumps(row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

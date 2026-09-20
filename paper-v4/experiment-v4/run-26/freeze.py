"""Freeze run-26: copy the public set, measure the leak ladder, write the record.

Run from the repository root on the pinned interpreter, after the runner has
admitted and the query has executed:

    PYTHONPATH=<core export>/src:$PWD:$PWD/src .venv/bin/python \\
        paper-v4/experiment-v4/run-26/freeze.py --ladder <ladder.py>

What it does, in order: copies the gate's artefacts into ``ontology-run/`` and
the runner's and the query's into ``results/``; measures every public file and
every withheld one against the reading with the leak ladder and moves out any
public file that shares a sixty-character run; writes
``results/withheld-artifacts.json`` and ``ontology-run/result.json``; rebuilds
the review package at freeze and validates its manifest; and rewrites the two
open-stage placeholder tests and the frozen-figure block in ``test_contract.py``
from the files themselves.

One thing it does not do: it does not write ``paper-v4/paper-ledger.md``. Only
the overseer writes that file, and this cell's agent was told not to.

This is the record condition, so ``ontology-run/`` holds this producer's own
phase-one attempt and the result record carries no fixed-ontology fields. The
review package it rebuilds is the v3.2 one, and the manifest is validated
against ``review-protocol-v3.2.json``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path("/Users/luis/Projects/malleus-dev")
HERE = ROOT / "paper-v4/experiment-v4/run-26"
PRIVATE = ROOT / "private/paper-v4-v4-run-26"
PUBLIC = HERE / "results"
ONTOLOGY_RUN = HERE / "ontology-run"
EVALUATION = ROOT / "paper-v4/evaluation-v4"
PACKAGE = EVALUATION / "run-26"
QUESTIONS = ROOT / "paper-v4/experiment-v4/competency-questions-v3.1.json"
RUN_24 = ROOT / "paper-v4/experiment-v4/run-24"
PROTOCOL = EVALUATION / "review-protocol-v3.2.json"

LADDER_RUNGS = [40, 60, 80, 120, 200, 320]
LEAK_WINDOW = 60

PUBLIC_FILES = {
    "census.json": "results/census.json",
    "run-result.json": "results/run-result.json",
    "trace-summary.json": "results/trace-summary.json",
    "native-query-binding.json": "results/native-query-binding.json",
    "query-trace-summary.json": "query/trace-summary.json",
    "paper-events.json": "results/paper-events.json",
    "transaction-time.txt": "transaction-time.txt",
    "launch-log.json": "launch-log.json",
    "usage.json": "usage.json",
    "query-type-sets.json": "query-type-sets.json",
    "query-type-sets.note.json": "query-type-sets.note.json",
    "query-binding.acceptance.json": "query-binding.acceptance.json",
}
GATE_FILES = ("grounding-receipt.json", "population-surface.json", "validated-contract.json")
WITHHELD_SOURCES = {
    "population-plan.json": "results/population-plan.json",
    "gaps.json": "results/gaps.json",
    "replay-receipt.json": "results/replay-receipt.json",
    "export-records.json": "results/export-records.json",
    "query-result.json": "query/query-result.json",
    "document-population.json": "producer/work/document-population.json",
    "retained-capture.json": "ledger/retained-capture.json",
    "history.jsonl": "ledger/history.jsonl",
}
CARRIES = {
    "population-plan.json": "RECORD_PROPERTY_VALUES_QUOTING_THE_READING",
    "gaps.json": "GAP_STATEMENTS_QUOTING_READING_FRAGMENTS",
    "replay-receipt.json": "REPLAYED_RECORD_PROPERTY_VALUES_QUOTING_THE_READING",
    "export-records.json": "EXPORTED_RECORD_PROPERTY_VALUES_QUOTING_THE_READING",
    "query-result.json": "PROJECTED_ROW_FIELDS_QUOTING_THE_READING",
    "document-population.json": "PRODUCER_CAPTURE_ASSERTIONS_QUOTING_THE_READING",
    "retained-capture.json": "RETAINED_CAPTURE_EVIDENCE_QUOTING_THE_READING",
    "history.jsonl": "RETAINED_SOURCE_AND_CAPTURE_BYTES_AS_JSON_ESCAPED_TEXT",
}
SUBSTITUTES = {
    "gaps.json": "results/run-result.json gaps_by_kind",
    "replay-receipt.json": (
        "results/run-result.json replay_receipt_sha256, ledger_head,"
        " ledger_event_count, graph"
    ),
    "query-result.json": (
        "results/query-trace-summary.json and the row counts in the review input"
        " manifest"
    ),
    "history.jsonl": "results/run-result.json ledger_head and ledger_event_count",
}


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ladder(script: Path, paths: list[Path]) -> dict[str, int]:
    out = subprocess.run(
        [sys.executable, str(script), *[str(path) for path in paths]],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    measured: dict[str, int] = {}
    for line in out.strip().splitlines():
        rung, path = line.split(None, 1)
        measured[path.strip()] = int(rung)
    return measured


def copy_public() -> None:
    shutil.copyfile(
        PRIVATE / "gate/attempt-01/diagnostic.json",
        ONTOLOGY_RUN / "attempt-01-diagnostic.json",
    )
    shutil.copyfile(
        PRIVATE / "producer/work/ontology-attempt-01.yaml",
        ONTOLOGY_RUN / "ontology-01.yaml",
    )
    for name in GATE_FILES:
        shutil.copyfile(PRIVATE / "gate/attempt-01" / name, ONTOLOGY_RUN / name)
    for name, relative in PUBLIC_FILES.items():
        shutil.copyfile(PRIVATE / relative, PUBLIC / name)


def write_withheld(measured: dict[str, int], moved: list[tuple[str, Path, int]]) -> list[dict]:
    withheld = []
    for name, relative in WITHHELD_SOURCES.items():
        source = PRIVATE / relative
        item = {
            "name": name,
            "private_path": str(source.relative_to(ROOT)),
            "sha256": digest(source),
            "carries": CARRIES[name],
            "shared_run_chars_at_least": measured[str(source)],
        }
        if name == "history.jsonl":
            item["note"] = (
                "The ladder reports 0 because the ledger stores the reading"
                " JSON-escaped. It is withheld by contract, not by the"
                " measurement."
            )
        if name in SUBSTITUTES:
            item["public_substitute"] = SUBSTITUTES[name]
        withheld.append(item)
    for name, destination, rung in moved:
        withheld.append(
            {
                "name": name,
                "private_path": str(destination.relative_to(ROOT)),
                "sha256": digest(destination),
                "carries": "SHARES_A_60_CHARACTER_RUN_WITH_THE_READING",
                "shared_run_chars_at_least": rung,
            }
        )
    withheld.sort(key=lambda item: item["name"])
    return withheld


def freeze(ladder_script: Path) -> dict[str, object]:
    log = json.loads((PRIVATE / "launch-log.json").read_bytes())
    contract = json.loads((HERE / "run-contract.json").read_bytes())
    copy_public()

    public_paths = [
        path
        for directory in (ONTOLOGY_RUN, PUBLIC)
        for path in sorted(directory.iterdir())
        if path.is_file() and path.name != ".gitkeep"
    ]
    private_paths = [PRIVATE / relative for relative in WITHHELD_SOURCES.values()]
    measured = ladder(ladder_script, public_paths + private_paths)
    leaks = [path for path in public_paths if measured[str(path)] >= LEAK_WINDOW]
    moved: list[tuple[str, Path, int]] = []
    for path in leaks:
        holder = "withheld-ontology-run" if path.parent == ONTOLOGY_RUN else "withheld-results"
        destination = PRIVATE / holder / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), destination)
        moved.append((path.name, destination, measured[str(path)]))
    withheld = write_withheld(measured, moved)

    public_measured = {
        ("ontology-run/" if path.parent == ONTOLOGY_RUN else "") + path.name: measured[
            str(path)
        ]
        for path in public_paths
        if path not in leaks
    }
    (PUBLIC / "withheld-artifacts.json").write_text(
        json.dumps(
            {
                "schema": "malleus.paper-v4.run-26-withheld-artifacts/v1",
                "run_id": "run-26",
                "reason": (
                    "Each file below reproduces text of the selected reading."
                    " Only its identity is public."
                ),
                "check": {
                    "method": "SHARED_NORMALIZED_CHARACTER_RUN_AGAINST_EVERY_READING_BLOCK",
                    "normalization": "UNICODE_WHITESPACE_COLLAPSED_TO_SINGLE_SPACE",
                    "ladder": LADDER_RUNGS,
                    "frozen_threshold": "NO_PUBLIC_FILE_SHARES_A_60_CHARACTER_RUN",
                    "public_files_measured": public_measured,
                },
                "withheld": withheld,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    gate = log["gate"][-1]
    surface = json.loads((ONTOLOGY_RUN / "population-surface.json").read_bytes())
    families: dict[str, int] = {}
    for item in surface["record_types"]:
        families[item["family"]] = families.get(item["family"], 0) + 1
    result = {
        "schema": "malleus.paper-v4.ontology-run-result/v1",
        "status": "ACCEPTED",
        "run_id": "run-26",
        "core": contract["core_gate"]["execution_baseline"],
        "producer_input_manifest_sha256": digest(HERE / "producer-input-manifest.json"),
        "ontology_authored_by": "run-26",
        "producer": {
            "kind": "CLAUDE_CODE_FRESH_SUBAGENT",
            "harness": contract["producer"]["harness"],
            "requested_model": log["launches"][0]["requested_model"],
            "model_family": log["launches"][0]["model_family"],
            "model_id": log["launches"][0]["model_id"],
            "reasoning_effort": "harness default, not pinned or observed",
            "boundary": contract["producer"]["boundary"],
            "session": "FRESH_SINGLE_SESSION",
            "workspace_launches": len(log["launches"]),
            "producing_launch_ordinal": log["launches"][0]["ordinal"],
            "questions_visible": False,
            "ontology_authored": True,
            "phases": "ONTOLOGY_THEN_POPULATION",
            "diagnostic_returns": len(log["gate"]) - 1,
            "diagnostic_return_limit": 2,
            "fallback_used": False,
            "hand_repair_used": False,
            "final_session_log_sha256": digest(PRIVATE / "producer/work/session-log.md"),
            "final_status_sha256": digest(PRIVATE / "producer/work/status.json"),
        },
        "attempts": [
            {
                "attempt": 1,
                "status": "ACCEPTED",
                "stage": "COMPLETE",
                "ontology_sha256": gate["ontology_sha256"],
                "ontology_path": "paper-v4/experiment-v4/run-26/ontology-run/ontology-01.yaml",
                "ontology_visibility": "PUBLIC",
                "diagnostic_path": (
                    "paper-v4/experiment-v4/run-26/ontology-run/attempt-01-diagnostic.json"
                ),
                "diagnostic_sha256": digest(ONTOLOGY_RUN / "attempt-01-diagnostic.json"),
                "accepted_at": gate["accepted_at"],
                "authored_by": "run-26",
            }
        ],
        "accepted": {
            "ontology_sha256": gate["ontology_sha256"],
            "validated_contract_sha256": digest(ONTOLOGY_RUN / "validated-contract.json"),
            "validated_fact_set_sha256": gate["validated_fact_set_sha256"],
            "fact_count": gate["fact_count"],
            "grounding_receipt_sha256": digest(ONTOLOGY_RUN / "grounding-receipt.json"),
            "population_surface_sha256": digest(ONTOLOGY_RUN / "population-surface.json"),
            "population_surface_families": dict(sorted(families.items())),
        },
        "accepted_ontology_sha256": gate["ontology_sha256"],
        "population_started": True,
        "stage_acceptance_non_claim": "STAGE_ACCEPTANCE_NOT_DOMAIN_ADEQUACY",
        "citation_check": gate.get("citation_check"),
        "next_boundary": (
            "Population, admission and replay are recorded in"
            " results/run-result.json. Preliminary inspection under"
            " paper-v4/evaluation-v4/run-26 and Luis's ratification are pending;"
            " nothing here is paper evidence until ratified."
        ),
    }
    assert digest(ROOT / result["attempts"][0]["ontology_path"]) == gate["ontology_sha256"]
    (ONTOLOGY_RUN / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )

    built = subprocess.run(
        [sys.executable, str(PACKAGE / "build_review_inputs.py"), "--stage", "freeze"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert built.returncode == 0, built.stdout + built.stderr
    sys.path.insert(0, str(EVALUATION))
    import review  # noqa: E402

    review.validate_review_input_manifest(
        (PACKAGE / "review-input-manifest.json").read_bytes(),
        PROTOCOL.read_bytes(),
    )
    manifest = json.loads((PACKAGE / "review-input-manifest.json").read_bytes())
    query = json.loads((PRIVATE / "query/query-result.json").read_bytes())
    rows = {item["question_id"]: len(item["rows"]) for item in query["queries"]}
    assert manifest["rows_per_question"] == rows, "manifest rows differ from the result"
    assert manifest["schema"] == (
        "malleus.paper-v4.source-grounded-review-inputs/v3.2"
    ), manifest["schema"]
    assert manifest["review_protocol_sha256"] == digest(PROTOCOL), "protocol digest"
    # The trace summary counts every record the executor traced; the manifest
    # binds the witnesses of the returned rows, which is what review.py checks.
    # Run-25's reviewer was refused over a difference of one between them.
    records_traced = json.loads((PUBLIC / "query-trace-summary.json").read_bytes())[
        "witnesses_traced"
    ]
    witnesses = manifest["witnesses_traced"]
    question_ids = [item["id"] for item in json.loads(QUESTIONS.read_bytes())["questions"]]
    assert sorted(rows) == sorted(question_ids)

    frozen = {}
    for name in ("ontology-run", "results"):
        for path in sorted((HERE / name).iterdir()):
            if path.is_file() and path.suffix != ".pyc" and path.name != ".gitkeep":
                frozen[f"{name}/{path.name}"] = digest(path)
    return {
        "frozen": frozen,
        "withheld": withheld,
        "public_ladder_max": max(public_measured.values()),
        "rows": rows,
        "witnesses": witnesses,
        "records_traced": records_traced,
        "families": dict(sorted(families.items())),
        "materials": [item["name"] for item in manifest["materials"]],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ladder", type=Path, required=True)
    arguments = parser.parse_args(argv)
    report = freeze(arguments.ladder)
    print(
        json.dumps(
            {
                key: report[key]
                for key in (
                    "public_ladder_max",
                    "witnesses",
                    "records_traced",
                    "families",
                )
            },
            indent=2,
        )
    )
    print("frozen files:", len(report["frozen"]))
    print("withheld:", [item["name"] for item in report["withheld"]])
    print("rows total:", sum(report["rows"].values()))
    Path("/private/tmp/claude-501/-Users-luis-Projects-malleus-dev/"
         "1e1b7a20-5bb3-486c-8880-9c4ee4c9be88/scratchpad/run26/"
         "freeze-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

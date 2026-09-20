"""Replay each frozen population through its own runner on a named Core.

One trial is one unmodified ``run-NN/run.py`` process with ``src/malleus``
exported by ``git archive`` from the named repository and commit, first on
``PYTHONPATH`` -- the discipline ``fault-injection-01/run_faults.py`` uses,
with the repository added because the hardened Core lives in a separate clone.
Every other argument comes from the cell's own frozen record, resolved by
``bridge.py``, and the files the runner reads are copied out of the frozen
producer first, so nothing under ``private/paper-v4-v4-run-NN`` is opened for
writing at any point.

Nothing here validates a population or repairs anything. The runner's exit
status, its typed diagnostic and the artifacts it leaves behind are the
observation. Source-bearing outputs stay under ``--private``; ``outcomes.json``
beside this file carries identifiers, digests, reasons and counts.

    .venv/bin/python paper-v4/experiment-v4/bridge-01/replay.py \
        --core FROZEN /Users/luis/Projects/malleus-dev c95dba7b \
        --core CANDIDATE /private/tmp/<candidate>/repo e7937b89 \
        --private private/paper-v4-bridge-01
"""

from __future__ import annotations

import argparse
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "paper-v4/experiment-v4/fault-injection-01"))

import bridge  # noqa: E402
import verify  # noqa: E402


OUTCOME_SCHEMA = "malleus.paper-v4.bridge-01-outcomes/v1"
# The run products compared byte for byte against the frozen ones, and the key
# each is reported under.
PRODUCTS = {
    "replay_receipt": "replay-receipt.json",
    "export_records": "export-records.json",
    "trace_summary": "trace-summary.json",
    "population_plan": "population-plan.json",
    "census": "census.json",
}
IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9_.\-]*:[A-Za-z0-9_.:\-]+")


def export_core(repository: Path, commit: str, into: Path) -> Path:
    archive = subprocess.run(
        ["git", "archive", "--format=tar", commit, "src/malleus"],
        cwd=repository,
        check=True,
        capture_output=True,
    ).stdout
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(into, filter="data")
    return into / "src"


def resolved_commit(repository: Path, commit: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", commit],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def stage_inputs(cell: str, into: Path) -> dict[str, object]:
    """Copy exactly the files the runner reads, at their own relative paths."""

    producer = bridge.producer_root(cell)
    closure = bridge.source_closure(cell)
    reading = bridge.reading_path(cell)
    population = bridge.population_path(cell)
    copied: dict[Path, Path] = {}
    for path in [path for _, path in closure] + [reading, population]:
        destination = into / path.relative_to(producer)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
        copied[path] = destination
    return {
        "closure": [(locator, copied[path]) for locator, path in closure],
        "reading": copied[reading],
        "population": copied[population],
    }


def invoke(
    cell: str,
    staged: dict[str, object],
    *,
    core: Path,
    ledger: Path,
    results: Path,
) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(core)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    names = bridge.identifiers(cell)
    command = [
        sys.executable,
        str(ROOT / f"paper-v4/experiment-v4/{cell}/run.py"),
        "--root",
        bridge.ROOT_LOCATOR,
    ]
    for locator, path in staged["closure"]:
        command += ["--source", locator, str(path)]
    command += [
        "--reading",
        str(staged["reading"]),
        "--population",
        str(staged["population"]),
        "--capture-id",
        names["capture_id"],
        "--plan-id",
        names["plan_id"],
        "--source-id",
        names["source_id"],
        "--artifact-id",
        names["artifact_id"],
        "--ledger",
        str(ledger),
        "--results",
        str(results),
        "--transaction-time",
        names["transaction_time"],
        "--actor-id",
        names["actor_id"],
    ]
    return subprocess.run(
        command, cwd=ROOT, env=environment, capture_output=True, text=True
    )


def diagnostic(cell: str, stderr: str) -> dict[str, str]:
    pattern = re.compile(
        rf"^{re.escape(cell)}: (?P<error>\w+): (?P<reason>[A-Z_]+): (?P<detail>.*)$",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(stderr.strip())
    if match is None:
        return {"error": "", "reason": "", "detail": stderr.strip()}
    return {
        "error": match.group("error"),
        "reason": match.group("reason"),
        "detail": match.group("detail").strip(),
    }


def records_named(cell: str, detail: str) -> list[str]:
    """The record identities a refusal names, filtered by the cell's own plan."""

    population = json.loads(bridge.population_path(cell).read_bytes())
    known = {
        record["id"]
        for family in population["records"].values()
        for record in family
        if isinstance(record, dict) and "id" in record
    }
    return sorted({token for token in IDENTIFIER.findall(detail) if token in known})


def observe(
    cell: str,
    completed: subprocess.CompletedProcess[str],
    *,
    ledger: Path,
    results: Path,
) -> dict[str, object]:
    frozen_result = bridge.frozen_result(cell)
    frozen_results = bridge.frozen_results_dir(cell)
    frozen_ledger = bridge.frozen_ledger(cell)
    record: dict[str, object] = {
        "cell": cell,
        "exit_status": completed.returncode,
        "outcome": "ADMITTED" if completed.returncode == 0 else "REFUSED",
        "diagnostic": diagnostic(cell, completed.stderr),
    }
    record["records_named"] = records_named(cell, str(record["diagnostic"]["detail"]))
    identical = {
        key: (
            (results / name).exists()
            and (results / name).read_bytes() == (frozen_results / name).read_bytes()
        )
        for key, name in sorted(PRODUCTS.items())
    }
    identical["ledger"] = (
        ledger.exists() and ledger.read_bytes() == frozen_ledger.read_bytes()
    )
    record["byte_identical"] = identical
    event_types = verify.ledger_event_types(ledger) if ledger.exists() else []
    record["ledger"] = {
        "sha256": verify.file_digest(ledger) if ledger.exists() else None,
        "event_count": len(event_types),
        "admission_events": [
            item for item in event_types if item in verify.ADMISSION_EVENTS
        ],
    }
    record["frozen"] = {
        "replay_receipt_sha256": frozen_result["replay_receipt_sha256"],
        "export_records_sha256": frozen_result["export_records_sha256"],
        "ledger_sha256": bridge.file_digest(frozen_ledger),
        "graph": frozen_result["graph"],
        "records_traced": frozen_result["records_traced"],
    }
    if (results / "run-result.json").exists():
        observed = json.loads((results / "run-result.json").read_bytes())
        record["observed"] = {
            "status": observed["status"],
            "replay_receipt_sha256": observed["replay_receipt_sha256"],
            "export_records_sha256": observed["export_records_sha256"],
            "ledger_sha256": verify.file_digest(ledger),
            "graph": observed["graph"],
            "records_traced": observed["records_traced"],
            "reopen_matches_admitted": observed["reopen_matches_admitted"],
        }
    else:
        record["observed"] = None
    if event_types:
        record["contract_artifact_differences"] = verify.contract_differences(
            frozen_ledger, ledger
        )
        record["declared_producer_sha256"] = bridge.declared_producer_digest(
            verify.contract_artifact(ledger)
        )
    else:
        record["contract_artifact_differences"] = []
        record["declared_producer_sha256"] = None
    return record


def probe_population(cell: str) -> tuple[dict[str, object], str]:
    """One record's ``statement_sha256`` removed, and nothing else.

    A gate that fires on nothing and a gate that is not reached look the same
    from a table of admissions. This is the one construction none of
    fault-injection-01's eleven classes builds: a record that keeps its
    locator and drops the digest beside it. Both slots are optional on the
    frozen Core, so the same mutation is a before-and-after on one file.

    The record is the sorted-first one carrying both slots, so its type
    declares them and the choice is a function of the population. The
    assertion that formalized the slot drops that entry with it: a
    formalization naming a path the record no longer has is a different fault
    (``UNKNOWN_FORMALIZATION_TARGET``, refused on both Cores) and would measure
    nothing about source binding.
    """

    population = json.loads(bridge.population_path(cell).read_bytes())
    candidates = sorted(
        (record["id"], family)
        for family, records in population["records"].items()
        for record in records
        if isinstance(record.get("properties"), dict)
        and record["properties"].get("assertion_locator")
        and record["properties"].get("statement_sha256")
    )
    if not candidates:
        raise bridge.BridgeRefusal(f"{cell}: no record carries both binding slots")
    record_id, family = candidates[0]
    slot = ["properties", "statement_sha256"]
    for record in population["records"][family]:
        if record["id"] == record_id:
            del record["properties"]["statement_sha256"]
    for assertion in population["capture"]["assertions"]:
        assertion["formalized_by"] = [
            item
            for item in assertion.get("formalized_by", [])
            if not (item.get("record_id") == record_id and item.get("path") == slot)
        ]
    return population, record_id


def run_probe(cell: str, *, core: Path, private: Path, label: str) -> dict[str, object]:
    population, record_id = probe_population(cell)
    root = private / label / f"{cell}-probe"
    shutil.rmtree(root, ignore_errors=True)
    staged = stage_inputs(cell, root / "producer")
    path = root / "producer/probe-population.json"
    path.write_bytes(bridge.canonical(population))
    staged["population"] = path
    completed = invoke(
        cell,
        staged,
        core=core,
        ledger=root / "ledger/history.jsonl",
        results=root / "results",
    )
    reason = diagnostic(cell, completed.stderr)
    return {
        "cell": cell,
        "construction": "REMOVE_STATEMENT_DIGEST_KEEP_LOCATOR",
        "record_id": record_id,
        "exit_status": completed.returncode,
        "outcome": "ADMITTED" if completed.returncode == 0 else "REFUSED",
        "diagnostic": reason,
        "records_named": records_named(cell, str(reason["detail"])),
        "population_sha256": bridge.file_digest(path),
    }


def replay(
    label: str, repository: Path, commit: str, private: Path, cells, probe: str
) -> dict:
    exact = resolved_commit(repository, commit)
    coordinate: dict[str, object] = {
        "label": label,
        "core_repository": str(repository),
        "core_commit": exact,
        "cells": [],
        "probe": None,
    }
    with tempfile.TemporaryDirectory(prefix="malleus-bridge-core-") as temporary:
        core = export_core(repository, exact, Path(temporary))
        coordinate["producer_sha256"] = bridge.producer_digest(core)
        if probe:
            found = run_probe(probe, core=core, private=private, label=label)
            coordinate["probe"] = found
            print(
                f"{label} {probe}-probe {found['outcome']}"
                f" {found['diagnostic']['reason']}",
                flush=True,
            )
        for cell in cells:
            root = private / label / cell
            shutil.rmtree(root, ignore_errors=True)
            staged = stage_inputs(cell, root / "producer")
            completed = invoke(
                cell,
                staged,
                core=core,
                ledger=root / "ledger/history.jsonl",
                results=root / "results",
            )
            record = observe(
                cell,
                completed,
                ledger=root / "ledger/history.jsonl",
                results=root / "results",
            )
            coordinate["cells"].append(record)
            print(
                f"{label} {cell} {record['outcome']} {record['diagnostic']['reason']}",
                flush=True,
            )
    return coordinate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--core",
        action="append",
        nargs=3,
        required=True,
        metavar=("LABEL", "REPOSITORY", "COMMIT"),
        help="one Core coordinate; repeat for a before-and-after pair",
    )
    parser.add_argument("--private", required=True, type=Path)
    parser.add_argument(
        "--only",
        default="",
        help="one cell, for a repair run; 'none' runs the probe by itself",
    )
    parser.add_argument(
        "--probe",
        default="",
        help="one cell to run the source-binding liveness probe against",
    )
    parser.add_argument("--outcomes", default=str(HERE / "outcomes.json"), type=Path)
    arguments = parser.parse_args(argv)

    private = arguments.private.resolve()
    private.mkdir(parents=True, exist_ok=True)
    if arguments.only == "none":
        cells: list[str] = []
    elif arguments.only:
        cells = [arguments.only]
    else:
        cells = list(bridge.CELLS)

    coordinates = {}
    for label, repository, commit in arguments.core:
        coordinates[label] = replay(
            label, Path(repository).resolve(), commit, private, cells, arguments.probe
        )
    outcomes = {
        "schema": OUTCOME_SCHEMA,
        "cells": cells,
        "probe_cell": arguments.probe,
        "coordinates": coordinates,
    }
    Path(arguments.outcomes).write_bytes(
        json.dumps(outcomes, ensure_ascii=False, indent=1, sort_keys=True).encode(
            "utf-8"
        )
        + b"\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Push every faulted population through run-23's own runner and record what happens.

One trial is one ``run-23/run.py`` process, with Core exported from the pinned
commit first on ``PYTHONPATH``, exactly as run-23's own parent-side commands
ran. Only ``--population`` differs between the control and a trial, and only
the injected fault differs inside that file. Nothing in this script validates a
population, decides an outcome or repairs anything: the runner's exit status,
its typed diagnostic and the ledger it leaves behind are the observation.

Source-bearing outputs (the faulted populations, each trial's plan and export)
stay under ``--private``. The public record is ``outcomes.json`` beside this
file: identifiers, digests, refusal reasons and counts, no value from the
reading.

    .venv/bin/python paper-v4/experiment-v4/fault-injection-01/run_faults.py \
        --producer private/paper-v4-v4-run-23/producer \
        --private private/paper-v4-fault-injection-01
"""

from __future__ import annotations

import argparse
import copy
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
RUNNER = ROOT / "paper-v4/experiment-v4/run-23/run.py"

sys.path.insert(0, str(HERE))

import faults  # noqa: E402
import verify  # noqa: E402


CORE_COMMIT = "c95dba7b86bb61487bda9a52458e1ea47cce20ab"
# The Core the frozen cell was run on lives in this checkout. A hardened Core
# under measurement may live in another clone, so the coordinate is a pair and
# both halves are arguments. Their defaults are this cell's own coordinate.
CORE_REPOSITORY = ROOT
# run-23's own ledger, for asking what a different Core moved in the contract.
FROZEN_LEDGER_PATH = ROOT / "private/paper-v4-v4-run-23/ledger/history.jsonl"
OUTCOME_SCHEMA = "malleus.paper-v4.fault-injection-01-outcomes/v1"
CAPTURE_ID = "capture:paper-v4:yu-2025:v4:23"
PLAN_ID = "plan:paper-v4:yu-2025:v4:23"
SOURCE_ID = "source:yu-2025-mid-atlantic-ridge"
ARTIFACT_ID = "artifact:selected-reading:yu-2025:v4:23"
TRANSACTION_TIME = "2026-09-09T22:00:20Z"
ACTOR_ID = "actor:overseer-run-23"
CLOSURE = (
    ("paper-v4-project", "work/ontology-attempt-01.yaml"),
    ("malleus", "inputs/malleus.yaml"),
    ("linkml:types", "inputs/linkml-types.yaml"),
    ("metrology", "inputs/metrology.yaml"),
    ("chronology", "inputs/chronology.yaml"),
    ("research", "inputs/research.yaml"),
)
READING = "inputs/selected-reading.json"
POPULATION = "work/document-population.json"

# run-23's own frozen receipt. The control has to land on it or nothing below
# is a measurement of anything.
FROZEN_RECEIPT = (
    "sha256:a3abceec58dc93692cbdeabf9a95c03551177ba97d9ee4225fe29198f37f1eec"
)
FROZEN_EXPORT = (
    "sha256:0634e0696a34bc2cc736f84dbeadf6b65416ebcd9f84f0e67eeb11bb9a44a286"
)
FROZEN_LEDGER = (
    "sha256:d5ef64c0ca6558967aa664705aa9661d3aec399d73c94aa7a5286ea6a991a908"
)

# The runner names itself before its typed diagnostic. run-23's own runner is
# the default; a runner that selects an adopter policy names itself instead, so
# the prefix is a group rather than a literal. Everything the group captures is
# what it captured before for run-23's output.
DIAGNOSTIC = re.compile(
    r"^(?P<runner>[\w.-]+): (?P<error>\w+): (?P<reason>[A-Z_]+): (?P<detail>.*)$",
    re.DOTALL | re.MULTILINE,
)


def export_core(repository: Path, commit: str, root: Path) -> Path:
    """``src/malleus`` at ``commit``, the way the active-test gate exports it."""

    archive = subprocess.run(
        ["git", "archive", "--format=tar", commit, "src/malleus"],
        cwd=repository,
        check=True,
        capture_output=True,
    ).stdout
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(root, filter="data")
    return root / "src"


def resolved_commit(repository: Path, commit: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", commit],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def invoke(
    *,
    core: Path,
    producer: Path,
    population: Path,
    ledger: Path,
    results: Path,
    runner: Path = RUNNER,
) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(core)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [sys.executable, str(runner), "--root", "paper-v4-project"]
    for locator, relative in CLOSURE:
        command += ["--source", locator, str(producer / relative)]
    command += [
        "--reading",
        str(producer / READING),
        "--population",
        str(population),
        "--capture-id",
        CAPTURE_ID,
        "--plan-id",
        PLAN_ID,
        "--source-id",
        SOURCE_ID,
        "--artifact-id",
        ARTIFACT_ID,
        "--ledger",
        str(ledger),
        "--results",
        str(results),
        "--transaction-time",
        TRANSACTION_TIME,
        "--actor-id",
        ACTOR_ID,
    ]
    return subprocess.run(
        command, cwd=ROOT, env=environment, capture_output=True, text=True
    )


def diagnostic(stderr: str) -> dict[str, str]:
    match = DIAGNOSTIC.search(stderr.strip())
    if match is None:
        return {"error": "", "reason": "", "detail": stderr.strip()}
    return {
        "error": match.group("error"),
        "reason": match.group("reason"),
        "detail": match.group("detail").strip(),
    }


def observe(
    trial: dict[str, object],
    completed: subprocess.CompletedProcess[str],
    *,
    ledger: Path,
    results: Path,
    capture: dict[str, object],
    control_ledger: Path,
    control: dict[str, object],
) -> dict[str, object]:
    """One trial's outcome, read off the runner's own products."""

    record: dict[str, object] = {
        "trial_id": trial["trial_id"],
        "fault_class": trial["fault_class"],
        "letter": trial["letter"],
        "designed_catcher": trial["designed_catcher"],
        "predicted_outcome": trial["predicted_outcome"],
        "target": trial["target"],
        "exit_status": completed.returncode,
    }
    event_types = verify.ledger_event_types(ledger) if ledger.exists() else []
    record["ledger"] = {
        "sha256": verify.file_digest(ledger) if ledger.exists() else None,
        "event_count": len(event_types),
        "event_types": event_types,
        "admission_events": [
            item for item in event_types if item in verify.ADMISSION_EVENTS
        ],
        "opens_the_control_ledger": (
            verify.is_byte_prefix(ledger, control_ledger) if ledger.exists() else False
        ),
    }
    if completed.returncode != 0:
        record["outcome"] = "REFUSED"
        record["diagnostic"] = diagnostic(completed.stderr)
        return record

    result = json.loads((results / "run-result.json").read_bytes())
    export = json.loads((results / "export-records.json").read_bytes())
    trace = json.loads((results / "trace-summary.json").read_bytes())
    witness = verify.fault_witness(trial, export)
    locator_found = verify.locator_disagreements(export, trace)
    digest_found = verify.digest_disagreements(export, capture)
    record["diagnostic"] = {"error": "", "reason": "", "detail": ""}
    record["run"] = {
        "status": result["status"],
        "replay_receipt_sha256": result["replay_receipt_sha256"],
        "export_records_sha256": result["export_records_sha256"],
        "trace_summary_sha256": result["trace_summary_sha256"],
        "ledger_head": result["ledger_head"],
        "records_traced": result["records_traced"],
        "graph": result["graph"],
        "reopen_matches_admitted": result["reopen_matches_admitted"],
        "receipt_equals_frozen": result["replay_receipt_sha256"] == FROZEN_RECEIPT,
        "export_equals_frozen": result["export_records_sha256"] == FROZEN_EXPORT,
        # Against this coordinate's own honest control, which is the comparison
        # that still means something when the Core under measurement is not the
        # one the frozen receipt was taken on.
        "receipt_equals_control": (
            result["replay_receipt_sha256"] == control["replay_receipt_sha256"]
        ),
        "export_equals_control": (
            result["export_records_sha256"] == control["export_records_sha256"]
        ),
    }
    record["fault_in_export"] = witness
    record["post_admission_checks"] = {
        "locator_disagreements": locator_found,
        "digest_disagreements": digest_found,
    }
    exposed = bool(locator_found) or bool(digest_found)
    record["outcome"] = "ADMITTED_EXPOSED" if exposed else "ADMITTED_INVISIBLE"
    return record


def build_parser() -> argparse.ArgumentParser:
    """The command line, separately so its defaults can be asserted."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--producer", required=True, type=Path)
    parser.add_argument("--private", required=True, type=Path)
    parser.add_argument("--only", default="", help="one trial ID, for a repair run")
    parser.add_argument(
        "--core-repo",
        default=str(CORE_REPOSITORY),
        type=Path,
        help="repository the Core export is taken from; default this checkout",
    )
    parser.add_argument(
        "--core-commit",
        default=CORE_COMMIT,
        help="commit the Core export is taken from; default the frozen pin",
    )
    parser.add_argument(
        "--outcomes",
        default=None,
        type=Path,
        help="where the outcome record is written; default beside this file",
    )
    # The admission each trial goes through. run-23's own runner is the
    # default, so this cell's coordinate does not move; a runner that selects
    # an adopter policy before the first record is how the same catalogue is
    # measured with a rule layer on
    # (paper-v4/experiment-v4/content-rules-doc-02).
    parser.add_argument(
        "--runner",
        default=str(RUNNER),
        type=Path,
        help="the admission runner each trial invokes; default run-23's own",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)

    producer = arguments.producer.resolve()
    private = arguments.private.resolve()
    repository = arguments.core_repo.resolve()
    commit = resolved_commit(repository, arguments.core_commit)
    runner = arguments.runner.resolve()
    frozen_coordinate = (
        repository == ROOT and commit == CORE_COMMIT and runner == RUNNER
    )
    trials_root = private / "trials"
    trials_root.mkdir(parents=True, exist_ok=True)

    honest = json.loads((producer / POPULATION).read_bytes())
    catalog = faults.catalog(copy.deepcopy(honest))
    if arguments.only:
        catalog = [item for item in catalog if item["trial_id"] == arguments.only]

    with tempfile.TemporaryDirectory(prefix="malleus-core-pin-") as temporary:
        core = export_core(repository, commit, Path(temporary))

        control_root = private / "control"
        control_ledger = control_root / "ledger/history.jsonl"
        # A control kept from a previous run is only this run's control if it
        # was produced at this run's Core coordinate. Reusing one silently
        # across coordinates would compare trials against the wrong baseline.
        coordinate_path = control_root / "coordinate.json"
        coordinate = {
            "core_repository": str(repository),
            "core_commit": commit,
            "runner": str(runner),
        }
        if control_ledger.exists():
            kept = (
                json.loads(coordinate_path.read_bytes())
                if coordinate_path.exists()
                else {}
            )
            if kept != coordinate:
                raise SystemExit(
                    f"the control under {control_root} was produced at {kept}, not"
                    f" {coordinate}; remove it or point --private elsewhere"
                )
        if not control_ledger.exists():
            shutil.rmtree(control_root, ignore_errors=True)
            completed = invoke(
                core=core,
                producer=producer,
                population=producer / POPULATION,
                ledger=control_ledger,
                results=control_root / "results",
                runner=runner,
            )
            if completed.returncode != 0:
                print(completed.stderr, file=sys.stderr)
                raise SystemExit("the honest control did not admit")
            coordinate_path.write_bytes(
                json.dumps(coordinate, ensure_ascii=False, sort_keys=True).encode(
                    "utf-8"
                )
            )
        control = json.loads((control_root / "results/run-result.json").read_bytes())
        contract_differences: list[dict[str, str]] = []
        if frozen_coordinate:
            if (
                control["replay_receipt_sha256"] != FROZEN_RECEIPT
                or verify.file_digest(control_ledger) != FROZEN_LEDGER
            ):
                raise SystemExit(
                    "the control does not reproduce run-23's frozen receipt"
                )
        else:
            # On another Core the receipt is allowed to move, but only for the
            # producer digest. Anything else is a difference in what Core
            # accepted, and that ends the measurement rather than being noted.
            if control["export_records_sha256"] != FROZEN_EXPORT:
                raise SystemExit(
                    "the control does not reproduce run-23's frozen export on"
                    f" {commit}: {control['export_records_sha256']}"
                )
            contract_differences = verify.contract_differences(
                FROZEN_LEDGER_PATH, control_ledger
            )
            if not verify.is_producer_digest_only(contract_differences):
                moved = ", ".join(item["path"] for item in contract_differences)
                raise SystemExit(
                    "the control's contract moves for more than the producer"
                    f" digest on {commit}: {moved}"
                )

        observations: list[dict[str, object]] = []
        for trial in catalog:
            trial_root = trials_root / str(trial["trial_id"])
            shutil.rmtree(trial_root, ignore_errors=True)
            trial_root.mkdir(parents=True)
            population_path = trial_root / "document-population.json"
            population_path.write_bytes(
                json.dumps(
                    trial["population"],
                    allow_nan=False,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ).encode("utf-8")
            )
            completed = invoke(
                core=core,
                producer=producer,
                population=population_path,
                ledger=trial_root / "ledger/history.jsonl",
                results=trial_root / "results",
                runner=runner,
            )
            observation = observe(
                trial,
                completed,
                ledger=trial_root / "ledger/history.jsonl",
                results=trial_root / "results",
                capture=trial["population"]["capture"],
                control_ledger=control_ledger,
                control=control,
            )
            observation["population_sha256"] = verify.file_digest(population_path)
            observations.append(observation)
            print(
                f"{observation['trial_id']} {observation['outcome']}"
                f" {observation['diagnostic']['reason']}",
                flush=True,
            )

        shutil.rmtree(private / "replay", ignore_errors=True)
        replay = invoke(
            core=core,
            producer=producer,
            population=producer / POPULATION,
            ledger=private / "replay/ledger/history.jsonl",
            results=private / "replay/results",
            runner=runner,
        )

    replayed: dict[str, object] = {}
    if replay.returncode == 0:
        replayed = json.loads((private / "replay/results/run-result.json").read_bytes())
    outcomes = {
        "schema": OUTCOME_SCHEMA,
        "core_commit": commit,
        "core_repository": str(repository),
        "core_is_the_frozen_pin": frozen_coordinate,
        "runner": str(runner),
        "seed": faults.SEED,
        "instances_per_variant": faults.INSTANCES_PER_VARIANT,
        "base_run": "run-23",
        "control": {
            "replay_receipt_sha256": control["replay_receipt_sha256"],
            "export_records_sha256": control["export_records_sha256"],
            "ledger_sha256": verify.file_digest(control_ledger),
            "equals_frozen_run_23": control["replay_receipt_sha256"] == FROZEN_RECEIPT,
            "export_equals_frozen_run_23": (
                control["export_records_sha256"] == FROZEN_EXPORT
            ),
            "contract_differences_from_frozen_run_23": contract_differences,
        },
        "replay_after_trials": {
            "exit_status": replay.returncode,
            "replay_receipt_sha256": replayed.get("replay_receipt_sha256"),
            "equals_frozen_run_23": replayed.get("replay_receipt_sha256")
            == FROZEN_RECEIPT,
            "equals_control": replayed.get("replay_receipt_sha256")
            == control["replay_receipt_sha256"],
        },
        "inputs": {
            "honest_population_sha256": verify.file_digest(producer / POPULATION),
            "reading_sha256": verify.file_digest(producer / READING),
            "ontology_sha256": verify.file_digest(
                producer / "work/ontology-attempt-01.yaml"
            ),
        },
        "trials": observations,
    }
    destination = arguments.outcomes or HERE / (
        "outcomes.json" if not arguments.only else "partial.json"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(
        json.dumps(outcomes, ensure_ascii=False, indent=1, sort_keys=True).encode(
            "utf-8"
        )
        + b"\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

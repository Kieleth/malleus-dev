"""Gate 1: run-23's honest population through the four adopted rules.

Three observations, each separate.

``control`` runs run-23's own ``run.py``, unmodified, on this checkout's Core,
so a refusal by Core's structural gate is never read as a refusal by the rules.

``honest`` rebuilds the same run in a fresh history whose selected policy is
this directory's, executes the pinned Prolog rules over the staged candidate
and submits the real result to the policy. Nothing here invents an outcome.

``equivalence`` runs the shared fixture table, and then every retained sentence
and every string slot value of run-23's population, through both
implementations of the declared normalisation and grammar.

Source-bearing outputs stay under ``--private``. The public record is
``outcomes.json`` beside this file: identities, digests, counts, refused record
identities, slots, rules, mechanisms and classes, and no value from the
reading.

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
        paper-v4/experiment-v4/content-rules-doc-02/gate1.py \
        --producer private/paper-v4-v4-run-23/producer \
        --private private/paper-v4-content-rules-doc-02
"""

from __future__ import annotations

import argparse
from base64 import b64decode
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "paper-v4/experiment-v4/fault-injection-01"))
sys.path.insert(0, str(ROOT / "paper-v4/experiment-v4/rule-census-01"))

import admit  # noqa: E402
import equivalence  # noqa: E402
import verify  # noqa: E402

RUNNER = ROOT / "paper-v4/experiment-v4/run-23/run.py"
CENSUS_OUTCOMES = ROOT / "paper-v4/experiment-v4/rule-census-01/outcomes.json"
FROZEN_LEDGER = ROOT / "private/paper-v4-v4-run-23/ledger/history.jsonl"
OUTCOMES = HERE / "outcomes.json"

OUTCOME_SCHEMA = "malleus.paper-v4.content-rules-doc-02-outcomes/v1"
CORE_COMMIT = "d867c3ab"

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
FROZEN_RECEIPT = (
    "sha256:a3abceec58dc93692cbdeabf9a95c03551177ba97d9ee4225fe29198f37f1eec"
)
FROZEN_EXPORT = (
    "sha256:0634e0696a34bc2cc736f84dbeadf6b65416ebcd9f84f0e67eeb11bb9a44a286"
)

RULE_DEFECT = "RULE_DEFECT"
GRAPH_DEFECT = "GRAPH_DEFECT"
UNDECIDED = "UNDECIDED"

# The census predicts zero refusals here. Nothing is classified in advance: a
# refusal that arrives is read against its record and its cited sentence, one
# line each, and an entry is added here before gate 2 runs. A refusal matching
# no entry stays UNDECIDED and fails the gate.
CLASSIFICATION: tuple[dict, ...] = ()


def classify(row: dict) -> tuple[str, str]:
    for entry in CLASSIFICATION:
        if entry["rule_id"] != row["rule_id"]:
            continue
        if "record_id" in entry and entry["record_id"] not in row["record_ids"]:
            continue
        if (
            "violation_code" in entry
            and entry["violation_code"] != row["violation_code"]
        ):
            continue
        return entry["class"], entry["reason"]
    return (
        UNDECIDED,
        "no entry of the declared classification table matches this refusal",
    )


def retained_artifact(ledger: Path, index: int) -> dict:
    """The artifact one bootstrap event of a history retained.

    Index 0 is the validated contract, which ``verify.contract_differences``
    already reads; index 1 is the partial effective contract, which is where a
    selected policy lives and therefore where a policied history differs from
    the control.
    """

    event = json.loads(ledger.read_text(encoding="utf-8").splitlines()[index])
    if event["event_type"] != "ARTIFACT_REGISTERED":
        raise ValueError(f"{ledger}: event {index} is not an artifact")
    return json.loads(b64decode(event["payload"]["retained_bytes_base64"]))


def private_is_ignored(path: Path) -> bool:
    completed = subprocess.run(
        ["git", "check-ignore", "-q", str(path)], cwd=ROOT, capture_output=True
    )
    return completed.returncode == 0


def control(producer: Path, private: Path) -> dict:
    """Run-23's own runner, unmodified, on this checkout's Core."""

    root = private / "control"
    shutil.rmtree(root, ignore_errors=True)
    command = [sys.executable, str(RUNNER), "--root", "paper-v4-project"]
    for locator, relative in CLOSURE:
        command += ["--source", locator, str(producer / relative)]
    command += [
        "--reading",
        str(producer / READING),
        "--population",
        str(producer / POPULATION),
        "--capture-id",
        CAPTURE_ID,
        "--plan-id",
        PLAN_ID,
        "--source-id",
        SOURCE_ID,
        "--artifact-id",
        ARTIFACT_ID,
        "--ledger",
        str(root / "ledger/history.jsonl"),
        "--results",
        str(root / "results"),
        "--transaction-time",
        TRANSACTION_TIME,
        "--actor-id",
        ACTOR_ID,
    ]
    completed = subprocess.run(
        command, cwd=ROOT, env=dict(os.environ), capture_output=True, text=True
    )
    if completed.returncode != 0:
        return {"exit_status": completed.returncode, "stderr": completed.stderr.strip()}
    result = json.loads((root / "results/run-result.json").read_bytes())
    differences = verify.contract_differences(
        FROZEN_LEDGER, root / "ledger/history.jsonl"
    )
    return {
        "exit_status": 0,
        "status": result["status"],
        "replay_receipt_sha256": result["replay_receipt_sha256"],
        "export_records_sha256": result["export_records_sha256"],
        "equals_frozen_run_23": result["replay_receipt_sha256"] == FROZEN_RECEIPT,
        "export_equals_frozen_run_23": result["export_records_sha256"] == FROZEN_EXPORT,
        "contract_differences_from_frozen_run_23": [
            item["path"] for item in differences
        ],
        "graph": result["graph"],
        "ledger_event_count": result["ledger_event_count"],
    }


def honest(producer: Path, private: Path) -> dict:
    """The same population in a fresh history with this directory's policy."""

    root = private / "honest"
    shutil.rmtree(root, ignore_errors=True)
    arguments = SimpleNamespace(
        root="paper-v4-project",
        source=[[locator, str(producer / relative)] for locator, relative in CLOSURE],
        reading=str(producer / READING),
        population=str(producer / POPULATION),
        capture_id=CAPTURE_ID,
        plan_id=PLAN_ID,
        source_id=SOURCE_ID,
        artifact_id=ARTIFACT_ID,
        ledger=str(root / "ledger/history.jsonl"),
        results=str(root / "results"),
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR_ID,
    )
    ledger = root / "ledger/history.jsonl"
    try:
        result = admit.execute(arguments)
    except admit.RunRefusal as error:
        detail = json.loads(
            (root / "results/content-rule-violations.json").read_bytes()
        )
        rows = []
        for item in detail["violations"]:
            classification, reason = classify(item)
            rows.append(
                {
                    **item,
                    "slot": item["violation_code"].split("/", 1)[-1]
                    if "/" in item["violation_code"]
                    else None,
                    "class": classification,
                    "reason": reason,
                }
            )
        return {
            "outcome": "REFUSED",
            "refusal": str(error),
            "check_outcome": detail["check_outcome"],
            "violated_rule_ids": detail["violated_rule_ids"],
            "admission_events": verify.ledger_admission_events(ledger),
            "refused": rows,
        }
    control_ledger = private / "control/ledger/history.jsonl"
    differences = verify.contract_differences(control_ledger, ledger)
    partial = verify.json_differences(
        retained_artifact(control_ledger, 1), retained_artifact(ledger, 1)
    )
    return {
        "outcome": "ADMITTED",
        "partial_contract_differences_from_the_control": [
            item["path"] for item in partial
        ],
        "check_outcome": result["check_outcome"],
        "checked_rule_ids": result["checked_rule_ids"],
        "violated_rule_ids": result["violated_rule_ids"],
        "fact_count": result["fact_count"],
        "engine": result["engine"],
        "policy_identity": result["policy_identity"],
        "check_contract_identity": result["check_contract_identity"],
        "receipt_identity": result["receipt_identity"],
        "derivations": result["derivations"],
        "retained_sentences": result["retained_sentences"],
        "replay_receipt_sha256": result["replay_receipt_sha256"],
        "export_records_sha256": result["export_records_sha256"],
        "export_equals_frozen_run_23": result["export_records_sha256"] == FROZEN_EXPORT,
        "contract_differences_from_the_control": [item["path"] for item in differences],
        "ledger_event_count": result["ledger_event_count"],
        "accepted_changes": result["accepted_changes"],
        "graph": result["graph"],
        "records_traced": result["records_traced"],
        "refused": [],
    }


def corpus_texts(producer: Path) -> dict[str, str]:
    """Every retained sentence and every string slot value of run-23."""

    population = json.loads((producer / POPULATION).read_bytes())
    texts = {
        f"assertion/{item['id']}": str(item["statement"])
        for item in population["capture"]["assertions"]
    }
    for family in sorted(population["records"]):
        for record in population["records"][family]:
            for slot, value in sorted((record.get("properties") or {}).items()):
                if isinstance(value, str):
                    texts[f"value/{record['id']}/{slot}"] = value
    return texts


def equivalence_block(producer: Path, private: Path) -> dict:
    fixtures = equivalence.compare(equivalence.fixture_texts())
    (private / "equivalence-fixtures.json").write_bytes(
        json.dumps(fixtures, ensure_ascii=False, indent=1, sort_keys=True).encode()
    )
    corpus = equivalence.compare(corpus_texts(producer))
    (private / "equivalence-corpus.json").write_bytes(
        json.dumps(corpus, ensure_ascii=False, indent=1, sort_keys=True).encode()
    )
    return {
        "fixtures": len(fixtures),
        "fixtures_disagreeing": sorted(
            row["label"] for row in fixtures if not row["agrees"]
        ),
        "declared_differences": sorted(equivalence.EXPECTED_EXTRA),
        "corpus_strings": len(corpus),
        "corpus_disagreeing": sorted(
            row["label"] for row in corpus if not row["agrees"]
        ),
        "corpus_disagreeing_count": sum(1 for row in corpus if not row["agrees"]),
        # A corpus row may differ only by the declared production: the text
        # carries a plus-or-minus with no digit before it and every number only
        # the Prolog read is the negation of one the Python read. Anything else
        # is a disagreement between the two implementations.
        "corpus_disagreeing_by_the_declared_production": sum(
            1
            for row in corpus
            if not row["agrees"]
            and row["carries_a_bare_plus_or_minus"]
            and row["surplus_are_negations"]
            and not row["only_in_python"]
        ),
        "corpus_disagreeing_otherwise": sum(
            1
            for row in corpus
            if not row["agrees"]
            and not (
                row["carries_a_bare_plus_or_minus"]
                and row["surplus_are_negations"]
                and not row["only_in_python"]
            )
        ),
        "corpus_normalisation_disagreeing": sum(
            1 for row in corpus if not row["normal_agrees"]
        ),
    }


def census_oracle(observed: list[dict]) -> dict:
    """The four adopted candidates as rule-census-01 measured them on run-23."""

    census = json.loads(CENSUS_OUTCOMES.read_bytes())
    document = census["populations"]["run-23"]
    numbers = sorted(
        {
            row["record_id"]
            for row in census["refusals"]
            if row["population"] == "run-23"
            and row["candidate"] == "NUMBER_IN_CITED_TEXT"
            and row["reading"] == "GLUED_ATTACHED"
            and row["scope"] == "CITED"
        }
    )
    expected = {
        "NO_CONFLICTING_QUANTITY": document["a_no_conflicting_quantity"][
            "with_assertion_modality"
        ]["violations"],
        "INTERVAL_SANITY": document["b_interval_sanity"]["refusals"],
        "NUMBER_IN_CITED_TEXT": document["c_number_in_cited_text"][
            "CITED/GLUED_ATTACHED"
        ]["refusals"],
        "FORMULA_IN_SOURCE": document["e_formula_in_source"]["CITED/GLUED"]["refusals"],
    }
    refused = {record for row in observed for record in row["record_ids"]}
    return {
        "census_refusals_by_candidate": expected,
        "removed_by_the_added_production": numbers,
        "observed_refused_records": sorted(refused),
        "reproduced": sorted(refused) == [],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--producer", required=True, type=Path)
    parser.add_argument("--private", required=True, type=Path)
    parser.add_argument("--steps", default="equivalence,control,honest")
    arguments = parser.parse_args(argv)
    producer = arguments.producer.resolve()
    private = arguments.private.resolve()
    if not private_is_ignored(private):
        raise SystemExit(f"refusing to write an unignored private directory: {private}")
    private.mkdir(parents=True, exist_ok=True)
    steps = [item.strip() for item in arguments.steps.split(",") if item.strip()]

    gate: dict[str, object] = {}
    if "equivalence" in steps:
        gate["equivalence"] = equivalence_block(producer, private)
        print("equivalence", gate["equivalence"], flush=True)
    if "control" in steps:
        gate["control"] = control(producer, private)
        print("control", gate["control"].get("status", "REFUSED"), flush=True)
    if "honest" in steps:
        gate["honest"] = honest(producer, private)
        print("honest", gate["honest"]["outcome"], flush=True)
        refused = gate["honest"]["refused"]
        gate["census_oracle"] = census_oracle(refused)
        gate["acceptance"] = {
            "refusals": len(refused),
            "rule_defects": sum(1 for row in refused if row["class"] == RULE_DEFECT),
            "graph_defects": sum(1 for row in refused if row["class"] == GRAPH_DEFECT),
            "unclassified": sum(1 for row in refused if row["class"] == UNDECIDED),
        }
        print("acceptance", gate["acceptance"], flush=True)

    outcomes = {
        "schema": OUTCOME_SCHEMA,
        "core_commit": CORE_COMMIT,
        "base_run": "run-23",
        "gate_1": gate,
        "gate_2": json.loads(OUTCOMES.read_bytes())["gate_2"]
        if OUTCOMES.exists()
        else None,
    }
    OUTCOMES.write_bytes(
        json.dumps(outcomes, ensure_ascii=False, indent=1, sort_keys=True).encode()
        + b"\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

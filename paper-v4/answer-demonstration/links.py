"""Stage the approved links-only condition; admission stays in repair.py."""

import argparse
import json
from pathlib import Path

from current_adoption import CORE, TREE
from followup import checked_bytes, verify_materials
from input_delivery import verify_delivery
import pilot
import repair
from review_packet import canonical, digest, new_private_directory


HERE = Path(__file__).resolve().parent
BASE = pilot.ROOT / "private/paper-v4-answer-demonstration/sol-calibration-01/b"
HYPOTHESIS = "claim:co2-degassing"


def task(run):
    return f"""# Source-grounded evidence links

Inspect the source's argument for the existing claim:co2-degassing. The graph
currently has no incoming SUPPORTS relation for it. Decide whether the text
justifies explicit source-attributed evidence links involving that hypothesis
and existing entities. Propose only justified ResearchRelation additions, or
refuse. No number of links or particular evidence endpoint is required.

This is finding-guided amendment, not fresh capture. Preserve qualifications:
evidence supporting an author's hypothesis is not independent proof of truth.
SUPPORTS does not mean physical causation. Do not use it to work around an
absent causal predicate. Use only the fixed ontology's legal types and enums.

Read only this task and your producer directory's declared inputs. No questions,
query code, earlier reviews, other runs, network or delegation. You are not alone
in the workspace. Write only producer/work here; never change another file.
The existing graph and baseline capture are context, never a replacement target.
Do not create entities, values, events or ontology edits. Supersessions are empty.
Only new ResearchRelation records involving the hypothesis and existing entity
endpoints are allowed. Do not resubmit existing records or reuse their IDs.

Return producer/work/candidate-01.json with exactly capture, records,
supersessions. Match the baseline-capture.json closed grammar, but include only
new assertion IDs, exact source evidence and formalizations for the proposed
relations. Preserve attribution and reading identity. Every new property and
both endpoints need explicit formalized_by paths. Use fresh record and assertion
IDs prefixed repair:evidence:. Keep the five explicit records arrays: entities,
relations, events, signals, event_participations. Only relations may be nonempty.
Do not manufacture block dispositions: unexamined blocks remain UNTOUCHED.
If no faithful change is possible, write producer/work/refusal.md instead.
Write producer/work/rationale.md with locators, qualifications and limitations.
Do not execute admission. The coordinator may return at most two exact structural
diagnostics, no semantic coaching. Preserve each submitted candidate separately.

Before authoring anything, read every complete declared input frame, including
the skill and complete import closure. First list frame counts with:
`/Users/luis/Projects/malleus-dev/.venv/bin/python {run}/evidence/input_delivery.py --run {run}/evidence --phase initial`
Then invoke it once per part with `--target TARGET --part N`. Use one frame per
tool output, at least 9000 output tokens, and re-read any truncated frame. Read
the skill first, selected reading next, then all remaining inputs. The helper
is the only extra allowed infrastructure path, do not inspect its source.
The coordinator verifies actual tool-output delivery, not a self-reported receipt.
"""


def stage(run):
    run = new_private_directory(run, pilot.ROOT / "private")
    baseline = json.loads((BASE / "manifest.json").read_bytes())
    verify_materials(BASE, baseline["materials"])
    if (baseline["core_commit"], baseline["core_tree"]) != (CORE, TREE):
        raise ValueError("links baseline Core differs")
    pilot.verify_runtime(CORE)
    attempt = BASE / "attempt-01"
    expected = json.loads((attempt / "run-result.json").read_bytes())
    if expected["status"] != "ADMITTED_AND_REPLAYED":
        raise ValueError("links requires an admitted baseline")
    method = json.loads((BASE / "subject-query-01/method.json").read_bytes())
    summary = json.loads((BASE / "subject-query-01/summary.json").read_bytes())
    files = {
        "base-history.jsonl": checked_bytes(
            (attempt / "ledger/history.jsonl").read_bytes(),
            "sha256:7c92d1a6955a7e9e3ef6e80702234bad17df44259060e2e46d4158971bee8d1b",
            "base history",
        ),
        "before-query.json": checked_bytes(
            (BASE / "subject-query-01/query-result.json").read_bytes(),
            summary["query_result_sha256"],
            "subject query",
        ),
        "questions.json": (BASE / "competency-questions.json").read_bytes(),
        "plan.md": (HERE / "LINKS-PLAN.md").read_bytes(),
        "evidence/input_delivery.py": (HERE / "input_delivery.py").read_bytes(),
        "evidence/TASK.md": task(run).encode(),
        "links.py": Path(__file__).read_bytes(),
        "repair.py": (HERE / "repair.py").read_bytes(),
    }
    for name, identity in method["code"].items():
        files[name] = checked_bytes(
            (BASE / "subject-query-01" / name).read_bytes(), identity, name
        )
    for name in baseline["producer_inputs"]:
        files["evidence/producer/" + name] = (BASE / "producer" / name).read_bytes()
    files["evidence/producer/inputs/baseline-records.json"] = checked_bytes(
        (attempt / "export-records.json").read_bytes(),
        expected["export_records_sha256"],
        "base records",
    )
    files["evidence/producer/inputs/baseline-capture.json"] = (
        attempt / "retained-capture.json"
    ).read_bytes()
    submitted = json.loads(
        checked_bytes(
            (attempt / "submitted-population.json").read_bytes(),
            expected["submitted_population_sha256"],
            "base submission",
        )
    )
    if (
        pilot.canonical(submitted["capture"])
        != files["evidence/producer/inputs/baseline-capture.json"]
    ):
        raise ValueError("baseline capture differs from admitted submission")
    declared = [
        {"target": name.removeprefix("evidence/producer/"), "sha256": digest(data)}
        for name, data in files.items()
        if name.startswith("evidence/producer/")
    ]
    files["evidence/producer-input-manifest.json"] = canonical(
        {"declared_inputs": declared}
    )
    for name, data in files.items():
        path = run / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (run / "evidence/producer/work").mkdir()
    manifest = {
        "schema": "malleus.paper-v4.links/v1",
        "decision": "E-0255",
        "status": "FROZEN_BEFORE_DISPATCH",
        "condition": "FINDING_GUIDED_LINKS",
        "core_commit": CORE,
        "core_tree": TREE,
        "base_run": str(BASE.relative_to(pilot.ROOT)),
        "base_receipt_sha256": expected["replay_receipt_sha256"],
        "hypothesis_id": HYPOTHESIS,
        "query_reader": "SubjectGraphReads",
        "producer_model": "gpt-5.6-sol",
        "producer_effort": "ultra",
        "maximum_structural_returns": 2,
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(files.items())
        ],
    }
    (run / "manifest.json").write_bytes(canonical(manifest))
    repair.preflight(run)
    return manifest


def execute(run, candidate, output, transaction_time):
    launch = json.loads((run / "evidence/launch.json").read_bytes())
    if (launch["model"], launch["reasoning_effort"], launch["fork_turns"]) != (
        "gpt-5.6-sol",
        "ultra",
        "none",
    ):
        raise ValueError("links producer differs from frozen condition")
    delivery = verify_delivery(run / "evidence", "initial")
    checked_bytes(
        (HERE / "repair.py").read_bytes(),
        digest((run / "repair.py").read_bytes()),
        "frozen amendment runner",
    )
    result = repair.execute(
        run, "evidence", candidate, output, transaction_time=transaction_time
    )
    (output / "delivery-evidence.json").write_bytes(canonical(delivery))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "execute"))
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--transaction-time")
    args = parser.parse_args()
    print(
        canonical(
            stage(args.run)
            if args.action == "stage"
            else execute(args.run, args.candidate, args.output, args.transaction_time)
        ).decode()
    )

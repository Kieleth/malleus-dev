"""Freeze a task-directed successor; reuse the existing amendment executor."""

import argparse
import json
from pathlib import Path

import malleus.compiler as api
from followup import checked_bytes, verify_materials
from links import execute
import pilot
import repair
from repair_review_packet import check_capture
from review_packet import canonical, digest, new_private_directory


HERE = Path(__file__).resolve().parent
BASE = pilot.ROOT / "private/paper-v4-answer-demonstration/sol-links-01"


def task(run, *, successor=False, qualification=False):
    if successor and qualification:
        raise ValueError("select exactly one amendment condition")
    if qualification:
        return (
            (HERE / "qualification-producer-task.md")
            .read_text()
            .replace("{RUN}", str(run))
        )
    text = f"""# Complete one source-grounded argument

This is task-directed amendment of accepted knowledge. Read competency-question.json
and argument-criteria.json: the question and prospective completion requirements
are intentionally supplied. You have no expected values or suggested endpoints.
Inspect the source and current graph, then propose any justified additions needed
to express that argument, or refuse. Account for each requirement and relevant
qualifications in your rationale. There is no required edge count. Do not force
a complete answer if the source or the fixed representation cannot support one.

Preserve every accepted record, including the existing evidence link. Only new
ResearchRelation records involving claim:co2-degassing and existing entity
endpoints are permitted. No new entities, values, events, ontology edits or
supersessions. Do not resubmit or duplicate existing records. Preserve attribution,
scope and the distinction between observations, estimates, model results and
hypotheses. A supporting argument is not physical causation or independent proof.

Read only this task and declared producer inputs. No other questions, query code,
earlier grades, producer rationales, other runs, network or delegation. You are
not alone in the workspace. Write only producer/work here, preserving others'
files. The baseline-capture.json and prior-amendment-capture.json are separate
retained evidence artifacts for current records, not material to overwrite.

Return producer/work/candidate-01.json with exactly capture, records, supersessions.
The capture uses the same closed grammar as the supplied captures, only fresh
assertion IDs and exact source evidence for your delta. Preserve attribution and
reading identity. Map every new property and both endpoints through formalized_by.
Use fresh record and assertion IDs prefixed argument:evidence:. records has five
explicit arrays: entities, relations, events, signals, event_participations.
Only relations may be nonempty. Supersessions is empty. Unexamined source blocks
remain UNTOUCHED, never invented negative dispositions. Do not execute admission.
Return producer/work/refusal.md if no faithful scoped addition is justified.
Write producer/work/rationale.md with requirement accounting, locators and limits.
The coordinator returns at most two exact structural diagnostics, no semantic
coaching. Retain each submitted candidate separately and stop at your first result.

Before authoring, read every frame of every declared input completely. Read the
skill first, selected reading next, then all remaining inputs. First list counts:
`/Users/luis/Projects/malleus-dev/.venv/bin/python {run}/evidence/input_delivery.py --run {run}/evidence --phase initial`
Invoke once per part with `--target TARGET --part N`, one frame per tool output,
at least 9000 output tokens. Re-read any truncation. The helper is the only extra
allowed infrastructure path; do not inspect its source. Actual tool outputs and
settings are verified, not a self-reported reading receipt. Notify the coordinator
when all frames have been read, before authoring, without waiting for permission.
"""
    if successor:
        text = text.replace("argument:evidence:", "argument-scope:evidence:")
        text = text.replace(
            "including the existing evidence link",
            "including every existing evidence link",
        ).replace(
            "The baseline-capture.json and prior-amendment-capture.json are separate",
            "The baseline-capture.json, prior-amendment-capture.json and\nargument-capture.json are separate",
        )
    return text


def stage(run, *, successor=False, qualification=False):
    if successor and qualification:
        raise ValueError("select exactly one amendment condition")
    run = new_private_directory(run, pilot.ROOT / "private")
    base = (
        BASE.parent / "sol-argument-scope-01"
        if qualification
        else BASE.parent / "sol-argument-01"
        if successor
        else BASE
    )
    previous = json.loads((base / "manifest.json").read_bytes())
    verify_materials(base, previous["materials"])
    pilot.verify_runtime(previous["core_commit"])
    attempt = base / "evidence/attempt-01"
    result = json.loads((attempt / "run-result.json").read_bytes())
    if result["status"] != "ADMITTED_REPLAYED_UNREVIEWED":
        raise ValueError("completion requires the admitted predecessor")
    for name, identity in result["artifacts"].items():
        checked_bytes((attempt / name).read_bytes(), identity, name)
    replay = api.KnowledgeChangeHistory.reopen(
        attempt / "ledger/history.jsonl"
    ).replay()
    checked_bytes(
        replay.receipt.canonical_bytes,
        "sha256:67b7f2ae747ab0f959c05882d1b99f7ef6bb260bf3b97f65c8c6065d3ab2e36b"
        if qualification
        else "sha256:6bc621091ae4918c2079fae7a9a611058fc25fe5c2c29af321e821fadfa9232e"
        if successor
        else "sha256:5339d580b2eaf038b802ee1097318c7c0a558fc5290e62f87a49a1982ccc090e",
        "accepted predecessor receipt",
    )
    checked_bytes(
        pilot.canonical(replay.graph.export_records()),
        result["artifacts"]["export-records.json"],
        "accepted predecessor graph",
    )
    check_capture(
        (attempt / "population-plan.json").read_bytes(),
        (attempt / "retained-capture.json").read_bytes(),
    )
    files = {
        m["path"]: (base / m["path"]).read_bytes()
        for m in previous["materials"]
        if m["path"] != "links.py"
    }
    question = next(
        q
        for q in pilot.load_questions(files["questions.json"])
        if q["id"] == "CQ-T5-01"
    )
    files.update(
        {
            "base-history.jsonl": (attempt / "ledger/history.jsonl").read_bytes(),
            "before-query.json": (attempt / "query-result.json").read_bytes(),
            "plan.md": (
                HERE
                / (
                    "QUALIFICATION-PLAN.md"
                    if qualification
                    else "SCOPED-LINKS-PLAN.md"
                    if successor
                    else "ARGUMENT-PLAN.md"
                )
            ).read_bytes(),
            "repair.py": (HERE / "repair.py").read_bytes(),
            "links.py": (HERE / "links.py").read_bytes(),
            "argument.py": Path(__file__).read_bytes(),
            "evidence/TASK.md": task(
                run, successor=successor, qualification=qualification
            ).encode(),
            "evidence/producer/inputs/baseline-records.json": (
                attempt / "export-records.json"
            ).read_bytes(),
            "evidence/producer/inputs/"
            + (
                "scope-capture.json"
                if qualification
                else "argument-capture.json"
                if successor
                else "prior-amendment-capture.json"
            ): (attempt / "retained-capture.json").read_bytes(),
            "evidence/producer/inputs/competency-question.json": canonical(question),
            "evidence/producer/inputs/argument-criteria.json": (
                HERE
                / (
                    "qualification-criteria.json"
                    if qualification
                    else "argument-criteria.json"
                )
            ).read_bytes(),
        }
    )
    if qualification:
        files["qualification-review-task.md"] = (
            HERE / "qualification-review-task.md"
        ).read_bytes()
    if successor:
        method_folder = base / "scope-method-01"
        method_bytes = checked_bytes(
            (method_folder / "method.json").read_bytes(),
            "sha256:32204e1488aa8113bd6ed24bf2b60c52d64fcb235d8efbcd63c87144d02bf996",
            "accepted scope method",
        )
        method = json.loads(method_bytes)
        verify_materials(method_folder, method["materials"])
        checked_bytes(
            (attempt / "run-result.json").read_bytes(),
            method["base_result_sha256"],
            "scope method accepted baseline",
        )
        files["scope-method.json"] = method_bytes
        for name in ("answers.py", "subject_answers.py", "questions.json"):
            files[name] = (method_folder / name).read_bytes()
        files["before-query.json"] = checked_bytes(
            (base / "scope-query-01/query-result.json").read_bytes(),
            "sha256:2369dbccb0da886b62478a31b99f0890ec82180b1ef409411ae3ac2eb8a4e66c",
            "accepted corrected before query",
        )
    criteria = json.loads(files["evidence/producer/inputs/argument-criteria.json"])
    if (
        criteria["question_id"] != question["id"]
        or [c["semantic"] for c in criteria["criteria"]]
        != question["required_semantics"]
    ):
        raise ValueError("prospective criteria differ from the frozen question")
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
        **previous,
        "schema": "malleus.paper-v4.qualification/v1"
        if qualification
        else "malleus.paper-v4.argument/v1",
        "decision": "E-0272" if qualification else "E-0266" if successor else "E-0259",
        "condition": "FINDING_GUIDED_QUALIFICATION"
        if qualification
        else "TASK_DIRECTED_ARGUMENT_COMPLETION",
        "amendment_id": "qualification-01"
        if qualification
        else "argument-scope-01"
        if successor
        else "argument-01",
        "base_run": str(base.relative_to(pilot.ROOT)),
        "base_receipt_sha256": digest(replay.receipt.canonical_bytes),
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(files.items())
        ],
    }
    if qualification:
        manifest.update(
            observation_id="observation:rc2-deep-depth",
            relation_id="argument-scope:evidence:relation:rc2-deep-depth-supports-co2-degassing",
        )
    (run / "manifest.json").write_bytes(canonical(manifest))
    repair.preflight(run)
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "execute"))
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--transaction-time")
    parser.add_argument("--successor", action="store_true")
    parser.add_argument("--qualification", action="store_true")
    args = parser.parse_args()
    print(
        canonical(
            stage(args.run, successor=args.successor, qualification=args.qualification)
            if args.action == "stage"
            else execute(args.run, args.candidate, args.output, args.transaction_time)
        ).decode()
    )

"""Freeze an independent, source-grounded delta review without supplying judgments."""

import argparse
import json
from pathlib import Path

from followup import verify_materials
from repair import FINDINGS, ROOT, context
from review_packet import canonical, digest, new_private_directory


def check_capture(plan_bytes, capture_bytes):
    evidence = json.loads(plan_bytes)["evidence"]
    if len(evidence) != 1 or evidence[0]["sha256"] != digest(capture_bytes):
        raise ValueError("delta capture differs from its plan evidence binding")


def reassessment(run, case):
    target = new_private_directory(run / case / "reassessment", ROOT / "private")
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    attempt = run / case / "attempt-01"
    result = json.loads((attempt / "run-result.json").read_bytes())
    sources = {
        path.name: path.read_bytes()
        for path in (run / case / "inputs").iterdir()
        if path.name != "TASK.md"
    }
    for name in ("export-records.json", "population-plan.json", "delta-trace.json"):
        source = (attempt / name).read_bytes()
        if digest(source) != result["artifacts"][name]:
            raise ValueError("reassessment artifact drift")
        sources["after-" + name] = source
    capture_bytes = (attempt / "retained-capture.json").read_bytes()
    check_capture(sources["after-population-plan.json"], capture_bytes)
    sources["after-retained-capture.json"] = capture_bytes
    sources["TASK.md"] = (
        "# Reassess the same bounded finding\n\n"
        + FINDINGS[case]
        + "\n\nThe after records and trace are now the accepted state. Read only this packet.\nDo not read questions, query outputs or reviewer judgments. Write only assessment.md\nin this directory. You are not alone in the workspace. Do not modify inputs.\nState whether this same finding is SATISFIED, UNRESOLVED, or needs an\nADDITIONAL_CHANGE_PROPOSAL, with exact evidence and scope limitations.\nDo not equate a duplicate record ID refusal with satisfaction. Do not assume\nsatisfaction because the coordinator ran admission. If another change is needed,\ndescribe it without applying it or expanding scope. No required no-change answer.\n"
    ).encode()
    target.mkdir(parents=True)
    for name, source in sources.items():
        (target / name).write_bytes(source)
    packet = {
        "case": case,
        "status": "FROZEN_BEFORE_REASSESSMENT",
        "materials": [
            {"path": name, "sha256": digest(source)} for name, source in sources.items()
        ],
    }
    (target / "manifest.json").write_bytes(canonical(packet))
    return packet


def prepare(run, output, *, composition=False, attempt_name="attempt-01", links=False):
    target = new_private_directory(output, ROOT / "private")
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    if attempt_name not in {"attempt-01", "attempt-02", "attempt-03"}:
        raise ValueError("review requires one of the three bounded attempts")
    if links and (
        composition
        or manifest["schema"]
        not in {
            "malleus.paper-v4.links/v1",
            "malleus.paper-v4.argument/v1",
            "malleus.paper-v4.qualification/v1",
        }
    ):
        raise ValueError("links review requires its exact finding-guided condition")
    argument = manifest["schema"] == "malleus.paper-v4.argument/v1"
    qualification = manifest["schema"] == "malleus.paper-v4.qualification/v1"
    if qualification and (
        not links or manifest["condition"] != "FINDING_GUIDED_QUALIFICATION"
    ):
        raise ValueError("qualification review requires its exact condition")
    if argument and (
        not links or manifest["condition"] != "TASK_DIRECTED_ARGUMENT_COMPLETION"
    ):
        raise ValueError("argument review requires its exact condition")
    task_name = (
        "argument-review-task.md"
        if argument
        else "links-review-task.md"
        if links
        else "composition-review-task.md"
        if composition
        else "repair-review-task.md"
    )
    sources = {
        "TASK.md": (
            run / "qualification-review-task.md"
            if qualification
            else ROOT / "paper-v4/answer-demonstration" / task_name
        ).read_bytes(),
        "questions.json": (run / "questions.json").read_bytes(),
        "before-query.json": (run / "before-query.json").read_bytes(),
        "review-protocol-v3.json": (
            ROOT / "paper-v4/evaluation-v4/review-protocol-v3.json"
        ).read_bytes(),
    }
    cases = {}
    cases_to_review = ("evidence",) if composition or links else tuple(FINDINGS)
    if composition and manifest["condition"] != "TASK_DIRECTED_COMPOSITION":
        raise ValueError("composition review requires its frozen condition")
    for case in cases_to_review:
        attempt = run / case / attempt_name
        result = json.loads((attempt / "run-result.json").read_bytes())
        if result["status"] != "ADMITTED_REPLAYED_UNREVIEWED":
            raise ValueError("cannot prepare an accepted delta review for " + case)
        for name, identity in result["artifacts"].items():
            value = (attempt / name).read_bytes()
            if digest(value) != identity:
                raise ValueError("attempt artifact drift: " + name)
        check_capture(
            (attempt / "population-plan.json").read_bytes(),
            (attempt / "retained-capture.json").read_bytes(),
        )
        cases[case] = {
            "changed_question_ids": result["changed_question_ids"],
            "run_result_sha256": digest((attempt / "run-result.json").read_bytes()),
        }
        inputs = run / context(manifest)[0] if links else run / case / "inputs"
        for path in inputs.iterdir():
            if path.name != "TASK.md":
                sources[case + "/" + path.name] = path.read_bytes()
        for name in (
            "submitted-population.json",
            "retained-capture.json",
            "population-plan.json",
            "delta-trace.json",
            "query-trace-summary.json",
            "query-result.json",
            "run-result.json",
            "export-records.json",
        ):
            sources[case + "/after-" + name] = (attempt / name).read_bytes()
    target.mkdir(parents=True)
    for name, source in sources.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(source)
    result = {
        "status": "FROZEN_BEFORE_REVIEW",
        "ratification": "PENDING",
        "attempt": attempt_name,
        "cases": cases,
        "materials": [
            {"path": name, "sha256": digest(source)}
            for name, source in sorted(sources.items())
        ],
    }
    (target / "manifest.json").write_bytes(canonical(result))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--composition", action="store_true")
    parser.add_argument("--attempt", default="attempt-01")
    args = parser.parse_args()
    print(
        canonical(
            prepare(
                args.run,
                args.output,
                composition=args.composition,
                attempt_name=args.attempt,
            )
        ).decode()
    )

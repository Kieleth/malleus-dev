"""Read-only structural preflight and independent integration review packets."""

import argparse
import json
from pathlib import Path

import malleus.compiler as api
from followup import checked_bytes, verify_materials
from integration import CONDITION, SCHEMA, check_integration, check_report
import pilot
import repair
from review_packet import canonical, digest, new_private_directory

ROOT = pilot.ROOT / "private"


def inspect_candidate(run, candidate_path):
    manifest, baseline, _ = repair.preflight(run)
    reconciliation = manifest["schema"] == "malleus.paper-v4.reconciliation/v1"
    if not reconciliation and (manifest["schema"], manifest["condition"]) != (
        SCHEMA,
        CONDITION,
    ):
        raise ValueError("integration review requires its exact condition")
    if not reconciliation:
        checked_bytes(
            Path(__file__).with_name("integration.py").read_bytes(),
            digest((run / "integration.py").read_bytes()),
            "integration scope",
        )
    inputs = run / "evidence/producer/inputs"
    reading = (inputs / "selected-reading.json").read_bytes()
    report = json.loads(candidate_path.with_suffix(".report.json").read_bytes())
    base = baseline.graph.export_records()
    ledger_bytes = (run / "base-history.jsonl").read_bytes()
    if reconciliation:
        from reconciliation import load_check

        load_check(run, base, candidate_path)
    if not candidate_path.exists():
        if not reconciliation:
            check_report(base, None, report, json.loads(reading))
        return {"status": "NO_CANDIDATE_REPORTED", "ledger_unchanged": True}
    candidate = json.loads(candidate_path.read_bytes())
    if not reconciliation:
        check_integration(base, candidate, report, json.loads(reading))
    _, capture_id, plan_id = repair.artifact_ids(manifest, "evidence")
    adapted = api.adapt_document_assertions(
        reading_bytes=reading,
        capture_bytes=pilot.canonical(candidate["capture"]),
        capture_id=capture_id,
        plan_id=plan_id,
        contract_identity=baseline.partial_contract.identity,
        records=candidate["records"],
        supersessions=candidate["supersessions"],
        contract_view=baseline.contract_view,
    )
    profile = api.DomainHistoryProfile.from_data(
        json.loads((inputs / "profile-source-assertion.json").read_bytes())
    )
    api.compile_population_plan(
        json.loads(adapted.canonical_plan_bytes),
        partial_contract=baseline.partial_contract,
        contract_view=baseline.contract_view,
        base_state=api.PopulationBaseState.from_replay(baseline),
        history_profile=profile,
    )
    if ledger_bytes != (run / "base-history.jsonl").read_bytes():
        raise ValueError("integration preflight changed the history")
    return {
        "status": "STRUCTURAL_PREFLIGHT_ONLY",
        "ledger_unchanged": True,
        "plan_sha256": digest(adapted.canonical_plan_bytes),
        "limit": "No retention or admission. Exact source witnesses do not establish source meaning.",
    }


def prepare(run, candidate, output):
    target = new_private_directory(output, ROOT)
    manifest = json.loads((run / "manifest.json").read_bytes())
    reconciliation = manifest["schema"] == "malleus.paper-v4.reconciliation/v1"
    if not reconciliation and (manifest["schema"], manifest["condition"]) != (
        SCHEMA,
        CONDITION,
    ):
        raise ValueError("integration review requires its exact condition")
    verify_materials(run, manifest["materials"])
    structural = inspect_candidate(run, candidate)
    report = candidate.with_suffix(".report.json").read_bytes()
    sources = {
        "TASK.md": (
            run
            / (
                "reconciliation-review-task.md"
                if reconciliation
                else "integration-review-task.md"
            )
        ).read_bytes(),
        "evidence/report.json": report,
        "evidence/structural-preflight.json": canonical(structural),
    }
    candidate_bytes = None
    if candidate.exists():
        candidate_bytes = candidate.read_bytes()
        sources["evidence/candidate.json"] = candidate_bytes
    else:
        sources["evidence/refusal.md"] = candidate.with_name("refusal.md").read_bytes()
    for item in manifest["materials"]:
        prefix = "evidence/producer/inputs/"
        if item["path"].startswith(prefix):
            sources["evidence/" + item["path"].removeprefix(prefix)] = (
                run / item["path"]
            ).read_bytes()
    target.mkdir(parents=True)
    for name, data in sources.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    result = {
        "schema": "malleus.paper-v4.reconciliation-source-review/v1"
        if reconciliation
        else "malleus.paper-v4.integration-source-review/v1",
        "status": "FROZEN_BEFORE_INDEPENDENT_REVIEW",
        "ratification": "PENDING",
        "run_manifest_sha256": digest((run / "manifest.json").read_bytes()),
        "candidate_sha256": None
        if candidate_bytes is None
        else digest(candidate_bytes),
        "report_sha256": digest(report),
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(sources.items())
        ],
    }
    (target / "manifest.json").write_bytes(canonical(result))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("inspect", "prepare"))
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print(
        canonical(
            inspect_candidate(args.run, args.candidate)
            if args.action == "inspect"
            else prepare(args.run, args.candidate, args.output)
        ).decode()
    )

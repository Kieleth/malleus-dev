"""Paper-local experiment-context amendment. No source interpretation in code."""

import argparse
import json
from pathlib import Path

import pilot
import repair
from followup import checked_bytes, verify_materials
from reconciliation import require
from review_packet import canonical, digest, new_private_directory

HERE = Path(__file__).resolve().parent
BASE = (
    pilot.ROOT / "private/paper-v4-answer-demonstration/sol-reconciliation-feedback-01"
)
METHOD = BASE.parent / "count-query-01/method"
SCHEMA = "malleus.paper-v4.acquisition/v1"
CONDITION = "SOURCE_GROUNDED_ACQUISITION_RELATIONS"
TARGETS = {
    "campaign:smarties": "Campaign",
    "instrument:obs": "Instrument",
    "count:obs-network": "CountObservation",
    "observation:recording-duration": "Observation",
}
ROUTES = {
    ("PART_OF_CAMPAIGN", "count:obs-network", "campaign:smarties"),
    ("PART_OF_CAMPAIGN", "observation:recording-duration", "campaign:smarties"),
    ("OBSERVED_WITH", "campaign:smarties", "instrument:obs"),
    ("OBSERVED_WITH", "observation:recording-duration", "instrument:obs"),
}


def check_acquisition(base, candidate, report, reading_bytes, source_id):
    """Check exact scope, locators and explanation closure, never entailment."""
    try:
        repair.population_parts(candidate)
        old, new = repair.indexed(base), repair.indexed(candidate["records"])
        require(
            all(
                key in old and old[key][0] == "entities" and old[key][1]["type"] == kind
                for key, kind in TARGETS.items()
            ),
            "missing or retyped acquisition target",
        )
        require(
            bool(new)
            and not new.keys() & old.keys()
            and candidate["supersessions"] == [],
            "only fresh additions, no supersession or reused IDs",
        )
        seen = set()
        existing = {
            (r["type"], r["source_id"], r["target_id"], canonical(r["properties"]))
            for r in base["relations"]
        }
        for key, (family, row) in new.items():
            require(
                family == "relations"
                and row["type"] == "ResearchRelation"
                and key.startswith("acquisition:evidence:"),
                "only acquisition ResearchRelation additions",
            )
            require(
                set(row) == {"id", "type", "source_id", "target_id", "properties"}
                and set(row["properties"]) == {"relation_type"},
                "closed relation shape, no additional properties",
            )
            route = (
                row["properties"]["relation_type"],
                row["source_id"],
                row["target_id"],
            )
            require(
                route in ROUTES and route not in seen,
                "out-of-scope or duplicate relation route",
            )
            require(
                (
                    row["type"],
                    row["source_id"],
                    row["target_id"],
                    canonical(row["properties"]),
                )
                not in existing,
                "relation already present",
            )
            seen.add(route)
        capture = candidate["capture"]
        require(
            capture["reading_sha256"] == digest(reading_bytes)
            and capture["attribution"]["source_id"] == source_id,
            "capture source/reading identity differs",
        )
        blocks = {
            block["id"]: block["text"]
            for page in json.loads(reading_bytes)["pages"]
            for block in page["blocks"]
        }
        assertions = {}
        for assertion in capture["assertions"]:
            require(
                assertion["id"] not in assertions
                and assertion["block"] in blocks
                and bool(assertion["statement"])
                and assertion["statement"] == blocks[assertion["block"]],
                "new evidence must copy a complete known block with unique assertion ID",
            )
            assertions[assertion["id"]] = assertion
        require(
            set(report) == {"schema", "relations", "limitations"}
            and report["schema"] == "malleus.paper-v4.acquisition-report/v1",
            "closed acquisition report required",
        )
        require(
            isinstance(report["limitations"], list)
            and all(isinstance(v, str) and v.strip() for v in report["limitations"]),
            "explicit textual limitations required",
        )
        explained = set()
        for item in report["relations"]:
            require(
                set(item) == {"record_id", "reason", "assertion_ids"}
                and isinstance(item["reason"], str)
                and bool(item["reason"].strip()),
                "explicit relation explanation required",
            )
            require(
                item["record_id"] in new and item["record_id"] not in explained,
                "unknown or duplicated relation explanation",
            )
            require(
                isinstance(item["assertion_ids"], list)
                and bool(item["assertion_ids"])
                and len(item["assertion_ids"]) == len(set(item["assertion_ids"]))
                and set(item["assertion_ids"]) <= assertions.keys(),
                "unknown or duplicate capture-scoped assertion reference",
            )
            explained.add(item["record_id"])
        require(explained == new.keys(), "every relation requires one explanation")
    except (KeyError, TypeError) as error:
        raise ValueError(f"missing or malformed acquisition field: {error}") from error


def load_check(run, base, candidate_path):
    checked_bytes(
        Path(__file__).read_bytes(),
        digest((run / "acquisition.py").read_bytes()),
        "frozen acquisition checks",
    )
    inputs = run / "evidence/producer/inputs"
    report = candidate_path.with_suffix(".report.json").read_bytes()
    check_acquisition(
        base,
        json.loads(candidate_path.read_bytes()),
        json.loads(report),
        (inputs / "selected-reading.json").read_bytes(),
        json.loads((inputs / "coordinates.json").read_bytes())["source_id"],
    )
    return report


def stage(run):
    run = new_private_directory(run, pilot.ROOT / "private")
    previous, _, _ = repair.preflight(BASE)
    outcome = json.loads((BASE / "outcome.json").read_bytes())
    require(
        outcome["status"] == "ADMITTED_REPLAYED_ASSESSED", "accepted baseline required"
    )
    verify_materials(BASE, outcome["materials"])
    method_bytes = checked_bytes(
        (METHOD / "method.json").read_bytes(),
        "sha256:af604ffe7ffe3c8f3bbcadb26a5f68f94dc139e72c7e2ecd6e08f293c9f94c68",
        "current count method",
    )
    method = json.loads(method_bytes)
    verify_materials(METHOD, method["materials"])
    attempt = BASE / "evidence/attempt-01"
    result = json.loads(
        checked_bytes(
            (attempt / "run-result.json").read_bytes(),
            method["base_result_sha256"],
            "accepted result",
        )
    )
    for name, identity in result["artifacts"].items():
        checked_bytes((attempt / name).read_bytes(), identity, name)
    prefix = "evidence/producer/"
    files = {
        item["path"]: (BASE / item["path"]).read_bytes()
        for item in previous["materials"]
        if item["path"].startswith((prefix + "inputs/", prefix + ".claude/"))
        and not item["path"].endswith(
            (
                "reconciliation-context.json",
                "capture-catalog.json",
                "baseline-records.json",
            )
        )
    }
    input_prefix = prefix + "inputs/"
    files[input_prefix + "baseline-records.json"] = (
        attempt / "export-records.json"
    ).read_bytes()
    files[input_prefix + "accepted-reconciliation-capture.json"] = (
        attempt / "retained-capture.json"
    ).read_bytes()
    base = json.loads(files[input_prefix + "baseline-records.json"])
    index = repair.indexed(base)
    files[input_prefix + "acquisition-context.json"] = canonical(
        {
            "targets": {key: index[key][1] for key in TARGETS},
            "read_only_contrast": index["count:useful-obs"][1],
            "allowed_routes": [
                {"predicate": p, "source_id": s, "target_id": t}
                for p, s, t in sorted(ROUTES)
            ],
            "limit": "Permitted scope, not source entailment or mandated edges.",
        }
    )
    captures = {
        name.removeprefix(input_prefix): digest(data)
        for name, data in files.items()
        if name.startswith(input_prefix) and name.endswith("-capture.json")
    }
    require(len(captures) == 6, "six retained captures required")
    files[input_prefix + "capture-catalog.json"] = canonical(captures)
    coordinates = json.loads(files[input_prefix + "coordinates.json"])
    coordinates.update(
        capture_id="capture:paper-v4:acquisition-01:evidence",
        plan_id="plan:paper-v4:acquisition-01:evidence",
    )
    files[input_prefix + "coordinates.json"] = canonical(coordinates)
    files["base-history.jsonl"] = checked_bytes(
        (attempt / "ledger/history.jsonl").read_bytes(),
        "sha256:4a8a4672093ba1b4decd0900a324aa9a728f9d7c625cea3871b1fb95285a19aa",
        "accepted history",
    )
    files["before-query.json"] = checked_bytes(
        (METHOD.parent / "first/query-result.json").read_bytes(),
        "sha256:10f01d53610a3a6ff9f0c2023f5eb6bb7880b9fe60b6c6a19ef9f62d7b00b6e2",
        "current count outputs",
    )
    for name in ("answers.py", "subject_answers.py", "questions.json"):
        files[name] = (METHOD / name).read_bytes()
    files["count-method.json"] = method_bytes
    for name in ("repair.py", "acquisition.py", "acquisition-review-task.md"):
        files[name] = (HERE / name).read_bytes()
    files["plan.md"] = (HERE / "ACQUISITION-PLAN.md").read_bytes()
    files["evidence/input_delivery.py"] = (HERE / "input_delivery.py").read_bytes()
    files["evidence/TASK.md"] = (
        (HERE / "acquisition-producer-task.md")
        .read_text()
        .replace("{RUN}", str(run))
        .encode()
    )
    files["evidence/producer-input-manifest.json"] = canonical(
        {
            "declared_inputs": [
                {"target": name.removeprefix(prefix), "sha256": digest(data)}
                for name, data in sorted(files.items())
                if name.startswith(prefix)
            ]
        }
    )
    manifest = {
        **{
            key: previous[key]
            for key in (
                "core_commit",
                "core_tree",
                "producer_model",
                "producer_effort",
                "maximum_structural_returns",
                "query_reader",
            )
        },
        "schema": SCHEMA,
        "condition": CONDITION,
        "decision": "E-0307",
        "amendment_id": "acquisition-01",
        "status": "FROZEN_BEFORE_DISPATCH",
        "base_run": str(BASE.relative_to(pilot.ROOT)),
        "base_receipt_sha256": result["artifacts"]["replay-receipt.json"],
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(files.items())
        ],
    }
    for name, data in files.items():
        path = run / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (run / "evidence/producer/work").mkdir()
    (run / "manifest.json").write_bytes(canonical(manifest))
    repair.preflight(run)
    return manifest


def structural_check(run, candidate_path):
    """Read-only public adapter and plan compilation, no retention or admission."""
    _, replay, _ = repair.preflight(run)
    load_check(run, replay.graph.export_records(), candidate_path)
    inputs = run / "evidence/producer/inputs"
    candidate = json.loads(candidate_path.read_bytes())
    _, capture_id, plan_id = repair.artifact_ids(
        json.loads((run / "manifest.json").read_bytes()), "evidence"
    )
    adapted = repair.api.adapt_document_assertions(
        reading_bytes=(inputs / "selected-reading.json").read_bytes(),
        capture_bytes=pilot.canonical(candidate["capture"]),
        capture_id=capture_id,
        plan_id=plan_id,
        contract_identity=replay.partial_contract.identity,
        records=candidate["records"],
        supersessions=candidate["supersessions"],
        contract_view=replay.contract_view,
    )
    profile = repair.api.DomainHistoryProfile.from_data(
        json.loads((inputs / "profile-source-assertion.json").read_bytes())
    )
    compiled = repair.api.compile_population_plan(
        json.loads(adapted.canonical_plan_bytes),
        partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=repair.api.PopulationBaseState.from_replay(replay),
        history_profile=profile,
    )
    return {
        "status": str(compiled.status),
        "candidate_sha256": digest(candidate_path.read_bytes()),
        "report_sha256": digest(
            candidate_path.with_suffix(".report.json").read_bytes()
        ),
        "plan_sha256": digest(adapted.canonical_plan_bytes),
    }


def review_packet(run, candidate_path):
    result = structural_check(run, candidate_path)
    packet = new_private_directory(run / "source-review-01", pilot.ROOT / "private")
    inputs = run / "evidence/producer/inputs"
    files = {
        "evidence/" + path.name: path.read_bytes()
        for path in sorted(inputs.iterdir())
        if path.is_file()
    }
    files.update(
        {
            "evidence/candidate.json": candidate_path.read_bytes(),
            "evidence/report.json": candidate_path.with_suffix(
                ".report.json"
            ).read_bytes(),
            "evidence/structural-preflight.json": canonical(result),
            "TASK.md": (run / "acquisition-review-task.md").read_bytes(),
        }
    )
    manifest = {
        "schema": "malleus.paper-v4.acquisition-source-review/v1",
        "run_manifest_sha256": digest((run / "manifest.json").read_bytes()),
        "candidate_sha256": result["candidate_sha256"],
        "report_sha256": result["report_sha256"],
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(files.items())
        ],
    }
    for name, data in files.items():
        path = packet / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (packet / "manifest.json").write_bytes(canonical(manifest))
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--review-packet", action="store_true")
    args = parser.parse_args()
    if args.candidate is None:
        result = stage(args.run)
    elif args.review_packet:
        result = review_packet(args.run, args.candidate)
    else:
        result = structural_check(args.run, args.candidate)
    print(canonical(result).decode())

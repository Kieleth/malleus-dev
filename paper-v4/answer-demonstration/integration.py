"""Question-withheld integration scope and staging; reuse public amendment replay."""

import argparse
import json
from pathlib import Path

import malleus.compiler as api
from followup import checked_bytes, verify_materials
from links import execute
import pilot
import repair
from review_packet import canonical, digest, new_private_directory

HERE = Path(__file__).resolve().parent
BASE = pilot.ROOT / "private/paper-v4-answer-demonstration/sol-qualification-01"
SCHEMA = "malleus.paper-v4.integration/v1"
CONDITION = "QUESTION_WITHHELD_CONTEXT_INTEGRATION"


def quantities(base):
    return {
        row["id"]
        for row in base["entities"]
        if any(
            key in row["properties"] and type(row["properties"][key]) in (int, float)
            for key in ("value_lower", "value_upper", "count", "ratio_value")
        )
    }


def changed_properties(before, after):
    return {
        key
        for key in set(before) | set(after)
        if key not in before
        or key not in after
        or canonical(before[key]) != canonical(after[key])
    }


def check_report(base, candidate, report, reading):
    if (
        set(report) != {"schema", "assessments", "changes"}
        or report["schema"] != "malleus.paper-v4.integration-report/v1"
    ):
        raise ValueError("integration report requires its closed schema")
    blocks = {b["id"]: b["text"] for page in reading["pages"] for b in page["blocks"]}
    eligible = quantities(base)
    seen, amended = set(), set()

    def evidence(entry, required):
        if not isinstance(entry["reason"], str) or not entry["reason"].strip():
            raise ValueError("integration requires an explicit reason")
        if not isinstance(entry["evidence"], list) or (
            required and not entry["evidence"]
        ):
            raise ValueError("integration change requires source evidence")
        for item in entry["evidence"]:
            if (
                set(item) != {"block", "quote"}
                or item["block"] not in blocks
                or not isinstance(item["quote"], str)
                or not item["quote"].strip()
                or item["quote"] not in blocks[item["block"]]
            ):
                raise ValueError(
                    "integration witness must be exact selected-reading text"
                )

    for entry in report["assessments"]:
        if (
            set(entry) != {"record_id", "status", "reason", "evidence"}
            or entry["record_id"] in seen
            or entry["record_id"] not in eligible
            or entry["status"]
            not in {"AMENDMENT", "NO_CHANGE", "UNRESOLVED", "ONTOLOGY_LIMITATION"}
        ):
            raise ValueError("integration assessment identity/status closure differs")
        seen.add(entry["record_id"])
        evidence(entry, entry["status"] == "AMENDMENT")
        if entry["status"] == "AMENDMENT":
            amended.add(entry["record_id"])
    if seen != eligible:
        raise ValueError("integration report must account for every existing quantity")
    expected = set()
    replacement_ids = set()
    if candidate is not None:
        old = repair.indexed(base)
        supersessions = {
            s["record_id"]: s["supersedes_record_id"]
            for s in candidate["supersessions"]
        }
        for row in candidate["records"]["entities"]:
            prior = supersessions[row["id"]]
            replacement_ids.add(prior)
            differences = changed_properties(
                old[prior][1]["properties"], row["properties"]
            )
            if not differences:
                raise ValueError("integration refuses no-op entity replacements")
            expected.update((prior, key) for key in differences)
    if amended != replacement_ids:
        raise ValueError(
            "integration amendment dispositions differ from actual replacements"
        )
    found = set()
    for entry in report["changes"]:
        if set(entry) != {"record_id", "property", "reason", "evidence"}:
            raise ValueError("integration change report fields differ")
        key = (entry["record_id"], entry["property"])
        if key in found:
            raise ValueError("duplicate integration property explanation")
        found.add(key)
        evidence(entry, True)
    if found != expected:
        raise ValueError(
            "integration property explanations must match every exact change"
        )


def check_integration(base, candidate, report, reading):
    repair.population_parts(candidate)
    old, new = repair.indexed(base), repair.indexed(candidate["records"])
    pairs = candidate["supersessions"]
    superseded = {s["supersedes_record_id"]: s["record_id"] for s in pairs}
    if (
        not new
        or set(new) & set(old)
        or len(superseded) != len(pairs)
        or len(set(superseded.values())) != len(pairs)
        or set(superseded.values()) != set(new)
        or not set(superseded) <= set(old)
    ):
        raise ValueError("integration requires unique fresh one-to-one supersessions")
    entities = {
        prior: current
        for prior, current in superseded.items()
        if old[prior][0] == "entities"
    }
    if not entities or not set(entities) <= quantities(base):
        raise ValueError("integration permits existing quantified entities only")
    incident = {
        row["id"]
        for row in base["relations"]
        if row["source_id"] in entities or row["target_id"] in entities
    }
    if set(superseded) != set(entities) | incident:
        raise ValueError("integration requires exact incident-relation closure")
    for prior, current in superseded.items():
        family, previous = old[prior]
        new_family, proposed = new[current]
        if family != new_family or previous["type"] != proposed["type"]:
            raise ValueError(
                "integration replacements must retain family and exact type"
            )
        if family == "entities":
            if {k: v for k, v in previous.items() if k not in {"id", "properties"}} != {
                k: v for k, v in proposed.items() if k not in {"id", "properties"}
            }:
                raise ValueError("integration entity header must be preserved")
        elif family == "relations":
            expected = {**previous, "id": current}
            for endpoint in ("source_id", "target_id"):
                if previous[endpoint] in entities:
                    expected[endpoint] = entities[previous[endpoint]]
            if canonical(proposed) != canonical(expected):
                raise ValueError(
                    "integration relation may only retarget its replaced endpoints"
                )
        else:
            raise ValueError("integration admits no other record family")
    for prior, (family, row) in old.items():
        if (
            family == "entities"
            and "subject" in row["properties"]
            and row["properties"]["subject"] in entities
        ):
            if (
                prior not in entities
                or new[entities[prior]][1]["properties"]["subject"]
                != entities[row["properties"]["subject"]]
            ):
                raise ValueError(
                    "integration would orphan an existing subject dependency"
                )
    check_report(base, candidate, report, reading)


def stage(run):
    run = new_private_directory(run, pilot.ROOT / "private")
    previous = json.loads((BASE / "manifest.json").read_bytes())
    verify_materials(BASE, previous["materials"])
    pilot.verify_runtime(previous["core_commit"])
    attempt = BASE / "evidence/attempt-01"
    result = json.loads((attempt / "run-result.json").read_bytes())
    if result["status"] != "ADMITTED_REPLAYED_UNREVIEWED":
        raise ValueError("integration requires its accepted predecessor")
    for name, identity in result["artifacts"].items():
        checked_bytes((attempt / name).read_bytes(), identity, name)
    replay = api.KnowledgeChangeHistory.reopen(
        attempt / "ledger/history.jsonl"
    ).replay()
    checked_bytes(
        replay.receipt.canonical_bytes,
        "sha256:eb9bcac22da1c1a61912f8b08e2201975d93216c935734b77c110fbbc9f40167",
        "integration base receipt",
    )
    checked_bytes(
        pilot.canonical(replay.graph.export_records()),
        result["artifacts"]["export-records.json"],
        "integration base graph",
    )
    method_root = BASE / "depth-method-01"
    method_bytes = checked_bytes(
        (method_root / "method.json").read_bytes(),
        "sha256:2b3e52b4952b394a10813a426e27efa56ea7891811a0350efcc71e62cc6379a7",
        "depth method",
    )
    verify_materials(method_root, json.loads(method_bytes)["materials"])
    allowed = {
        ".claude/skills/malleus-acolyte/SKILL.md",
        ".claude/skills/malleus-acolyte/agents/openai.yaml",
        *(
            "inputs/" + name
            for name in (
                "argument-capture.json",
                "baseline-capture.json",
                "chronology.yaml",
                "coordinates.json",
                "linkml-types.yaml",
                "malleus.yaml",
                "metrology.yaml",
                "ontology.yaml",
                "population-surface.json",
                "prior-amendment-capture.json",
                "profile-source-assertion.json",
                "research.yaml",
                "selected-reading.json",
                "scope-capture.json",
            )
        ),
    }
    files = {
        "evidence/producer/" + name: (BASE / "evidence/producer" / name).read_bytes()
        for name in sorted(allowed)
    }
    files["evidence/producer/inputs/baseline-records.json"] = (
        attempt / "export-records.json"
    ).read_bytes()
    files["evidence/producer/inputs/qualification-capture.json"] = (
        attempt / "retained-capture.json"
    ).read_bytes()
    files.update(
        {
            "base-history.jsonl": (attempt / "ledger/history.jsonl").read_bytes(),
            "before-query.json": checked_bytes(
                (BASE / "depth-query-01/query-result.json").read_bytes(),
                "sha256:af325d88662ec2aee0fd29fb2cfcd37c5f9bd47e65375a9498fb9c1522e930aa",
                "integration before query",
            ),
            "depth-method.json": method_bytes,
            "plan.md": (HERE / "INTEGRATION-PLAN.md").read_bytes(),
            "integration-review-task.md": (
                HERE / "integration-review-task.md"
            ).read_bytes(),
            "evidence/TASK.md": (HERE / "integration-producer-task.md")
            .read_text()
            .replace("{RUN}", str(run))
            .encode(),
            "evidence/input_delivery.py": (HERE / "input_delivery.py").read_bytes(),
            "repair.py": (HERE / "repair.py").read_bytes(),
            "integration.py": Path(__file__).read_bytes(),
        }
    )
    for name in ("answers.py", "subject_answers.py", "questions.json"):
        files[name] = (method_root / name).read_bytes()
    files["evidence/producer-input-manifest.json"] = canonical(
        {
            "declared_inputs": [
                {
                    "target": name.removeprefix("evidence/producer/"),
                    "sha256": digest(data),
                }
                for name, data in sorted(files.items())
                if name.startswith("evidence/producer/")
            ]
        }
    )
    for name, data in files.items():
        path = run / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (run / "evidence/producer/work").mkdir()
    manifest = {
        **{
            k: previous[k]
            for k in (
                "core_commit",
                "core_tree",
                "producer_model",
                "producer_effort",
                "maximum_structural_returns",
                "query_reader",
            )
        },
        "schema": SCHEMA,
        "decision": "E-0279",
        "condition": CONDITION,
        "status": "FROZEN_BEFORE_DISPATCH",
        "amendment_id": "integration-01",
        "base_run": str(BASE.relative_to(pilot.ROOT)),
        "base_receipt_sha256": digest(replay.receipt.canonical_bytes),
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(files.items())
        ],
    }
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
    args = parser.parse_args()
    print(
        canonical(
            stage(args.run)
            if args.action == "stage"
            else execute(args.run, args.candidate, args.output, args.transaction_time)
        ).decode()
    )

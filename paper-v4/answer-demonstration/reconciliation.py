"""Six-record reconciliation checks and staging. Admission remains in repair.py."""

import argparse
import json
from pathlib import Path

import yaml

from followup import checked_bytes, verify_materials
from integration import changed_properties
import pilot
import repair
from review_packet import canonical, digest, new_private_directory

HERE = Path(__file__).resolve().parent
SCHEMA = "malleus.paper-v4.reconciliation/v1"
CONDITION = "RCA_GUIDED_SIX_RECORD_RECONCILIATION"
TARGETS = frozenset(
    {
        "observation:lab-melt-fraction",
        "observation:lab-water-content",
        "observation:average-depth-uncertainty",
        "observation:abstract-primary-co2",
        "observation:rc2-primary-ba90",
        "qualification:evidence:observation:rc2-deep-depth:v1",
    }
)
PROTECTED = {"value_lower", "value_upper", "count", "ratio_value", "unit"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def build_context(base, documents, *, targets=TARGETS):
    records = repair.indexed(base)
    selected = set(targets)
    require(selected <= records.keys(), "missing reconciliation target")
    for key in targets:
        properties = records[key][1]["properties"]
        if "subject" in properties:
            subject = properties["subject"]
            require(subject in records, f"unresolved subject on {key}: {subject}")
            selected.add(subject)
    return {
        "targets": sorted(targets),
        "records": {key: records[key][1] for key in sorted(selected)},
        "definitions": {
            name: yaml.safe_load(data) for name, data in sorted(documents.items())
        },
        "limit": "Exact records and schema declarations, not generated interpretations.",
    }


def replacements(base, candidate, targets):
    if candidate is None:
        return {}, set()
    repair.population_parts(candidate)
    old, new = repair.indexed(base), repair.indexed(candidate["records"])
    pairs = candidate["supersessions"]
    mapping = {s["supersedes_record_id"]: s["record_id"] for s in pairs}
    require(
        bool(new)
        and not new.keys() & old.keys()
        and len(mapping) == len(pairs) == len(new)
        and set(mapping.values()) == set(new)
        and mapping.keys() <= old.keys(),
        "require fresh one-to-one record replacements",
    )
    entities = {
        key: value for key, value in mapping.items() if old[key][0] == "entities"
    }
    require(
        bool(entities) and entities.keys() <= targets,
        "only six selected entities may change",
    )
    incident = {
        r["id"]
        for r in base["relations"]
        if r["source_id"] in entities or r["target_id"] in entities
    }
    require(
        set(mapping) == entities.keys() | incident,
        "exact incident relation replacements required",
    )
    changes = set()
    for prior, current in mapping.items():
        family, before = old[prior]
        new_family, after = new[current]
        require(
            family == new_family and before["type"] == after["type"],
            "replacement family and exact type must be preserved",
        )
        if family == "entities":
            require(
                {k: v for k, v in before.items() if k not in {"id", "properties"}}
                == {k: v for k, v in after.items() if k not in {"id", "properties"}},
                "entity header changed",
            )
            delta = changed_properties(before["properties"], after["properties"])
            require(
                bool(delta) and not delta & PROTECTED,
                "no-op or protected numerical bounds/units changed",
            )
            changes.update((prior, key) for key in delta)
        elif family == "relations":
            expected = {**before, "id": current}
            for key in ("source_id", "target_id"):
                endpoint = before[key]
                expected[key] = entities[endpoint] if endpoint in entities else endpoint
            require(
                canonical(expected) == canonical(after),
                "relation may only retarget replaced endpoints",
            )
        else:
            raise ValueError("only entities and incident relations may be replaced")
    for key, (family, row) in old.items():
        if family == "entities" and "subject" in row["properties"]:
            subject = row["properties"]["subject"]
            if subject in entities:
                require(
                    key in entities
                    and new[entities[key]][1]["properties"]["subject"]
                    == entities[subject],
                    "replacement would orphan a subject dependency",
                )
    return entities, changes


def check_reconciliation(
    base, candidate, report, reading_bytes, captures, source_id, *, targets=TARGETS
):
    """Check addresses, scope and accounting. Do not assess source meaning."""
    try:
        _check(base, candidate, report, reading_bytes, captures, source_id, targets)
    except (KeyError, TypeError) as error:
        raise ValueError(
            f"missing or malformed reconciliation field: {error}"
        ) from error


def _check(base, candidate, report, reading_bytes, captures, source_id, targets):
    entities, expected_changes = replacements(base, candidate, targets)
    reading = json.loads(reading_bytes)
    blocks = {b["id"]: b["text"] for page in reading["pages"] for b in page["blocks"]}
    catalog = {}
    for identity, data in captures.items():
        checked_bytes(data, identity, "capture identity")
        catalog[identity] = json.loads(data)
    proposed_identity = None
    if candidate is not None:
        proposed_identity = digest(pilot.canonical(candidate["capture"]))
        require(proposed_identity not in catalog, "proposed capture must be new")
        catalog[proposed_identity] = candidate["capture"]
    assertions = {}
    for identity, capture in catalog.items():
        require(
            capture["reading_sha256"] == digest(reading_bytes)
            and capture["attribution"]["source_id"] == source_id,
            "capture source/reading identity differs",
        )
        for assertion in capture["assertions"]:
            key = (identity, assertion["id"])
            require(key not in assertions, "duplicate assertion inside a capture")
            require(assertion["block"] in blocks, "assertion block absent")
            text = blocks[assertion["block"]]
            if identity == proposed_identity:
                require(
                    bool(assertion["statement"]) and assertion["statement"] == text,
                    "new evidence must copy the complete selected block",
                )
            else:
                require(
                    bool(assertion["statement"].strip())
                    and " ".join(assertion["statement"].split())
                    in " ".join(text.split()),
                    "historical assertion fails Core's whitespace-collapse locator rule",
                )
            assertions[key] = assertion

    def evidence(items, required=False):
        require(
            isinstance(items, list) and (not required or bool(items)),
            "source evidence references required",
        )
        for item in items:
            require(
                set(item) == {"capture_sha256", "assertion_id"},
                "evidence uses capture digest and assertion ID only",
            )
            require(
                (item["capture_sha256"], item["assertion_id"]) in assertions,
                "unresolved capture-scoped assertion reference",
            )

    old = repair.indexed(base)
    proposed = {} if candidate is None else repair.indexed(candidate["records"])
    require(
        set(report) == {"schema", "assessments", "changes", "out_of_scope"}
        and report["schema"] == "malleus.paper-v4.reconciliation-report/v1",
        "closed reconciliation report schema required",
    )
    require(
        isinstance(report["out_of_scope"], list)
        and all(
            isinstance(item, str) and item.strip() for item in report["out_of_scope"]
        ),
        "out_of_scope requires explicit textual limitations",
    )
    seen = set()
    for assessment in report["assessments"]:
        require(
            set(assessment) == {"record_id", "status", "contexts"},
            "assessment fields differ",
        )
        key = assessment["record_id"]
        require(key in targets and key not in seen, "assessment target closure differs")
        seen.add(key)
        require(
            assessment["status"] in {"AMENDMENT", "NO_CHANGE", "UNRESOLVED"}
            and (assessment["status"] == "AMENDMENT") == (key in entities),
            "assessment status differs from actual replacement",
        )
        require(
            isinstance(assessment["contexts"], list) and bool(assessment["contexts"]),
            "explicit context account required",
        )
        for context in assessment["contexts"]:
            require(
                set(context) == {"status", "statement", "graph_refs", "evidence"},
                "context fields differ",
            )
            status = context["status"]
            require(
                status in {"REPRESENTED", "MISSING", "PROPOSED", "UNRESOLVED"}
                and isinstance(context["statement"], str)
                and bool(context["statement"].strip()),
                "explicit context status and statement required",
            )
            refs = context["graph_refs"]
            require(
                isinstance(refs, list)
                and (status not in {"REPRESENTED", "PROPOSED"} or bool(refs)),
                "represented/proposed context requires actual graph paths",
            )
            for ref in refs:
                require(
                    set(ref) == {"record_id", "path", "value"}
                    and isinstance(ref["path"], list)
                    and bool(ref["path"]),
                    "graph reference requires record, nonempty path and exact value",
                )
                records = proposed if status == "PROPOSED" else old
                require(
                    ref["record_id"] in records,
                    "graph reference absent in declared existing/proposed state",
                )
                value = records[ref["record_id"]][1]
                for part in ref["path"]:
                    require(
                        isinstance(value, dict)
                        and isinstance(part, str)
                        and part in value,
                        "graph path is absent or misbound",
                    )
                    value = value[part]
                require(
                    canonical(value) == canonical(ref["value"]),
                    "graph reference value differs from actual record",
                )
            evidence(context["evidence"], status == "PROPOSED")
    require(seen == set(targets), "all six target assessments required")
    explained = set()
    for change in report["changes"]:
        require(
            set(change) == {"record_id", "property", "reason", "evidence"}
            and isinstance(change["reason"], str)
            and bool(change["reason"].strip()),
            "explicit changed-property reason required",
        )
        key = (change["record_id"], change["property"])
        require(key not in explained, "duplicate property explanation")
        explained.add(key)
        evidence(change["evidence"], True)
    require(
        explained == expected_changes,
        "explanations must cover every exact property change",
    )


def load_check(run, base, candidate_path):
    checked_bytes(
        Path(__file__).read_bytes(),
        digest((run / "reconciliation.py").read_bytes()),
        "frozen reconciliation checks",
    )
    inputs = run / "evidence/producer/inputs"
    captures = {
        digest(path.read_bytes()): path.read_bytes()
        for path in sorted(inputs.glob("*-capture.json"))
    }
    require(len(captures) == 5, "exactly five retained input captures required")
    report_bytes = candidate_path.with_suffix(".report.json").read_bytes()
    candidate = (
        json.loads(candidate_path.read_bytes()) if candidate_path.exists() else None
    )
    check_reconciliation(
        base,
        candidate,
        json.loads(report_bytes),
        (inputs / "selected-reading.json").read_bytes(),
        captures,
        json.loads((inputs / "coordinates.json").read_bytes())["source_id"],
    )
    return report_bytes


def authorize(run, candidate_path):
    """Paper-owned permission check. An affirmative review is not Core truth."""
    packet = run / "source-review-01"
    try:
        decision = json.loads((packet / "decision.json").read_bytes())
        manifest = json.loads((packet / "manifest.json").read_bytes())
        require(
            set(decision)
            == {
                "status",
                "run_manifest_sha256",
                "candidate_sha256",
                "report_sha256",
                "review_sha256",
                "reviewer_thread_id",
                "ratification",
            },
            "closed source-review decision required",
        )
        require(
            decision["status"] == "ALLOW_SUPPORTED_BATCH"
            and isinstance(decision["reviewer_thread_id"], str)
            and bool(decision["reviewer_thread_id"].strip())
            and decision["ratification"] in {"PENDING_HUMAN", "RATIFIED_BY_LUIS"},
            "affirmative independent source-review decision required",
        )
        expected = {
            "run_manifest_sha256": digest((run / "manifest.json").read_bytes()),
            "candidate_sha256": digest(candidate_path.read_bytes()),
            "report_sha256": digest(
                candidate_path.with_suffix(".report.json").read_bytes()
            ),
        }
        require(
            all(
                decision[key] == value == manifest[key]
                for key, value in expected.items()
            ),
            "stale source-review candidate/report/run binding",
        )
        checked_bytes(
            (packet / "review.md").read_bytes(),
            decision["review_sha256"],
            "source review",
        )
        verify_materials(packet, manifest["materials"])
        return decision
    except (OSError, KeyError, TypeError) as error:
        raise ValueError(f"source-review authorization unavailable: {error}") from error


def stage(run):
    """Reuse the verified accepted baseline packet, never its rejected proposal."""
    from integration import BASE

    run = new_private_directory(run, pilot.ROOT / "private")
    prior = BASE.parent / "sol-integration-01"
    previous, _, _ = repair.preflight(prior)
    files = {
        item["path"]: (prior / item["path"]).read_bytes()
        for item in previous["materials"]
        if item["path"].startswith("evidence/producer/")
        or item["path"]
        in {
            "base-history.jsonl",
            "before-query.json",
            "depth-method.json",
            "answers.py",
            "subject_answers.py",
            "questions.json",
        }
    }
    prefix = "evidence/producer/inputs/"
    base = json.loads(files[prefix + "baseline-records.json"])
    documents = {
        name.removeprefix(prefix): data
        for name, data in files.items()
        if name.startswith(prefix) and name.endswith(".yaml")
    }
    files[prefix + "reconciliation-context.json"] = canonical(
        build_context(base, documents)
    )
    files[prefix + "capture-catalog.json"] = canonical(
        {
            name.removeprefix(prefix): digest(data)
            for name, data in files.items()
            if name.startswith(prefix) and name.endswith("-capture.json")
        }
    )
    for name in ("repair.py", "reconciliation.py", "reconciliation-review-task.md"):
        files[name] = (HERE / name).read_bytes()
    files["plan.md"] = (HERE / "RECONCILIATION-PLAN.md").read_bytes()
    files["evidence/input_delivery.py"] = (HERE / "input_delivery.py").read_bytes()
    files["evidence/TASK.md"] = (
        (HERE / "reconciliation-producer-task.md")
        .read_text()
        .replace("{RUN}", str(run))
        .encode()
    )
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
            key: previous[key]
            for key in (
                "core_commit",
                "core_tree",
                "producer_model",
                "producer_effort",
                "maximum_structural_returns",
                "query_reader",
                "base_run",
                "base_receipt_sha256",
            )
        },
        "schema": SCHEMA,
        "condition": CONDITION,
        "decision": "E-0286",
        "status": "FROZEN_BEFORE_DISPATCH",
        "amendment_id": "reconciliation-01",
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
    parser.add_argument("--stage", type=Path, required=True)
    args = parser.parse_args()
    print(canonical(stage(args.stage)).decode())

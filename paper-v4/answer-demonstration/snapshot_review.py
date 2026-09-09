"""Freeze one current answer view and check review accounting, not semantics."""

import argparse
from datetime import datetime
import json
from pathlib import Path

from review_packet import canonical, digest, docket, new_private_directory

SCHEMA = "malleus.paper-v4.current-snapshot-review/v1"
MODES = {"FRESH_INDEPENDENT", "COORDINATOR_NONINDEPENDENT"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    require(type(value) is str and bool(value.strip()), "nonblank text required")


def locators(values, blocks):
    require(type(values) is list and bool(values), "source locators required")
    require(
        len(set(values)) == len(values) and set(values) <= blocks,
        "invalid source locator",
    )


def check_review(record, index, queries, blocks, identity):
    try:
        _check_review(record, index, queries, blocks, identity)
    except (KeyError, TypeError, IndexError) as error:
        raise ValueError(f"missing or malformed review data: {error}") from error
    return record


def _check_review(record, index, queries, blocks, identity):
    require(record["schema"] == SCHEMA, "wrong review schema")
    require(record["manifest_sha256"] == identity, "wrong review manifest")
    require(record["status"] == "PRELIMINARY_COMPLETE", "review is incomplete")
    require(record["ratification"] == "PENDING_HUMAN", "model cannot ratify")
    reviewer = record["reviewer"]
    text(reviewer["actor_id"])
    require(reviewer["method"] == "MODEL_ASSISTED", "review method must be explicit")
    require(reviewer["independence"] in MODES, "review independence must be explicit")
    require(
        datetime.fromisoformat(reviewer["completed_at"].replace("Z", "+00:00")).tzinfo
        is not None,
        "aware completion time required",
    )
    keys = [w["witness_key"] for w in record["witnesses"]]
    require(
        sorted(keys) == sorted(w["witness_key"] for w in index["witnesses"]),
        "witness closure differs",
    )
    for witness in record["witnesses"]:
        require(
            witness["source_support"]
            in {"SUPPORTED", "PARTIAL", "UNSUPPORTED", "NOT_EVALUABLE"},
            "unknown source support judgment",
        )
        locators(witness["source_locators"], blocks)
        text(witness["rationale"])
    ids = [q["question_id"] for q in index["questions"]]
    require(
        ids
        == [q["question_id"] for q in record["questions"]]
        == [q["question_id"] for q in queries["queries"]],
        "question closure differs",
    )
    for expected, actual, query in zip(
        index["questions"], record["questions"], queries["queries"], strict=True
    ):
        require(
            expected["required_semantics"]
            == [c["semantic"] for c in actual["coverage"]],
            "required semantic closure or order differs",
        )
        covered = 0
        for item in actual["coverage"]:
            text(item["note"])
            locators(item["source_locators"], blocks)
            for key, count in (
                ("row_indices", len(query["rows"])),
                ("path_indices", len(query["paths"])),
            ):
                values = item[key]
                require(
                    type(values) is list
                    and len(set(values)) == len(values)
                    and all(type(i) is int and 0 <= i < count for i in values),
                    "invalid row/path reference",
                )
            has_witness = bool(item["row_indices"] or item["path_indices"])
            if has_witness:
                require(
                    item["absent_reason"] is None,
                    "covered semantic has an absence reason",
                )
                covered += 1
            else:
                require(
                    item["absent_reason"]
                    in {
                        "UNRETURNED",
                        "UNSUPPORTED",
                        "NOT_IN_SOURCE",
                        "LOCATOR_NOT_RESOLVABLE",
                        "NOT_EXPRESSIBLE",
                        "UNRESOLVED",
                    },
                    "absence reason required",
                )
        label = (
            "COVERED"
            if covered == len(actual["coverage"])
            else "PARTIAL"
            if covered
            else "NONE"
        )
        require(
            actual["responsiveness"] == label,
            "responsiveness disagrees with declared coverage",
        )
        require(
            actual["assembly"]
            in {"NO_ANSWER", "ONE_ROW", "LINKED_ROWS", "UNLINKED_ROWS"},
            "unknown assembly descriptor",
        )
        require(
            (actual["assembly"] == "NO_ANSWER") == (covered == 0),
            "assembly disagrees with coverage",
        )
        text(actual["answer"])


def trace_closure(reading_bytes, captures, trace):
    """Resolve capture-scoped locators without deciding source support."""
    reading = json.loads(reading_bytes)
    blocks = {b["id"]: b["text"] for p in reading["pages"] for b in p["blocks"]}
    require(len(blocks) == reading["block_count"], "reading block identity differs")
    catalog = {
        digest(data): (name, json.loads(data)) for name, data in captures.items()
    }
    rows = []
    for entry in trace["records"]:
        require(
            digest(reading_bytes) in entry["sources"].values(), "unbound trace reading"
        )
        require(
            entry["declared_evidence_resolved"] is True, "unresolved declared evidence"
        )
        bound = [
            catalog[entry["evidence"][key]] for key in entry["declared_evidence_ids"]
        ]
        found = []
        for derivation in entry["derivations"]:
            matches = [
                (name, assertion)
                for name, capture in bound
                for assertion in capture["assertions"]
                if assertion["id"] == derivation["locator"]
                and {"record_id": entry["record_id"], "path": derivation["path"]}
                in assertion["formalized_by"]
            ]
            require(len(matches) == 1, "ambiguous or missing capture-scoped derivation")
            name, assertion = matches[0]
            require(
                " ".join(assertion["statement"].split())
                in " ".join(blocks[assertion["block"]].split()),
                "assertion does not occur in selected block",
            )
            found.append(
                {
                    "capture": name,
                    "assertion_id": assertion["id"],
                    "block": assertion["block"],
                    "record_path": derivation["path"],
                    "statement_sha256": digest(assertion["statement"].encode()),
                }
            )
        rows.append({"record_id": entry["record_id"], "resolved_derivations": found})
    return {"records": rows}


def prepare(run, output, *, reviewer_mode):
    import malleus.compiler as api
    import pilot
    import repair
    from followup import checked_bytes, verify_materials

    require(reviewer_mode in MODES, "reviewer mode must be selected")
    target = new_private_directory(output, pilot.ROOT / "private")
    manifest, _, _ = repair.preflight(run)
    require(
        manifest["condition"] == "SOURCE_REVIEW_FEEDBACK_RECONCILIATION",
        "wrong source condition",
    )
    attempt = run / "evidence/attempt-01"
    result = json.loads((attempt / "run-result.json").read_bytes())
    require(
        result["status"] == "ADMITTED_REPLAYED_UNREVIEWED", "accepted result required"
    )
    for name, identity in result["artifacts"].items():
        checked_bytes((attempt / name).read_bytes(), identity, name)
    outcome = json.loads((run / "outcome.json").read_bytes())
    verify_materials(run, outcome["materials"])
    ledger = attempt / "ledger/history.jsonl"
    ledger_bytes = ledger.read_bytes()
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    require(
        replay.receipt.canonical_bytes
        == (attempt / "replay-receipt.json").read_bytes(),
        "receipt does not reproduce",
    )
    require(
        pilot.canonical(replay.graph.export_records())
        == (attempt / "export-records.json").read_bytes(),
        "graph does not reproduce",
    )
    inputs = run / "evidence/producer/inputs"
    query = json.loads((attempt / "query-result.json").read_bytes())
    surface = json.loads((inputs / "population-surface.json").read_bytes())
    fresh, traces, guard_identity, attempts = repair.frozen_queries(
        run, replay, surface, reader=manifest["query_reader"]
    )
    repair.check_read_guard(attempts)
    require(fresh == query["queries"], "current queries do not reproduce")
    trace = json.loads((attempt / "query-trace-summary.json").read_bytes())
    require(
        traces == trace["records"] and guard_identity == query["read_guard_sha256"],
        "trace/read guard differs",
    )
    require(ledger.read_bytes() == ledger_bytes, "read changed ledger")
    sources = {
        name: (run / name).read_bytes()
        for name in (
            "answers.py",
            "subject_answers.py",
            "depth-method.json",
            "qualification-criteria.json",
        )
    }
    for name in (
        "query-result.json",
        "query-trace-summary.json",
        "export-records.json",
        "replay-receipt.json",
    ):
        sources[name] = (attempt / name).read_bytes()
    for name in (
        "selected-reading.json",
        "population-surface.json",
        "profile-source-assertion.json",
    ):
        sources[name] = (inputs / name).read_bytes()
    for path in inputs.glob("*.yaml"):
        sources[path.name] = path.read_bytes()
    capture_catalog = json.loads((inputs / "capture-catalog.json").read_bytes())
    captures = {
        name: checked_bytes((inputs / name).read_bytes(), identity, name)
        for name, identity in capture_catalog.items()
    }
    captures["feedback-capture.json"] = (attempt / "retained-capture.json").read_bytes()
    sources.update(captures)
    sources["capture-catalog.json"] = canonical(
        {name: digest(data) for name, data in captures.items()}
    )
    sources["resolved-trace.json"] = canonical(
        trace_closure(sources["selected-reading.json"], captures, trace)
    )
    questions = json.loads((run / "questions.json").read_bytes())
    index = docket(questions, query, trace)
    sources["review-docket.json"] = canonical(index)
    sources["TASK.md"] = (
        Path(__file__).with_name("snapshot-review-task.md").read_bytes()
    )
    sources["review-criteria.md"] = (
        Path(__file__).with_name("CURRENT-SNAPSHOT-PLAN.md").read_bytes()
    )
    sources["snapshot_review.py"] = Path(__file__).read_bytes()
    sources["review_packet.py"] = (
        Path(__file__).with_name("review_packet.py").read_bytes()
    )
    frozen = {
        "schema": "malleus.paper-v4.current-snapshot-inputs/v1",
        "reviewer_mode": reviewer_mode,
        "condition": "ITERATIVELY_REFINED_SOL_CURRENT_SNAPSHOT",
        "ratification": "PENDING_HUMAN",
        "core_commit": manifest["core_commit"],
        "source_run": run.name,
        "source_run_manifest_sha256": digest((run / "manifest.json").read_bytes()),
        "questions_sha256": digest((run / "questions.json").read_bytes()),
        "source_sha256": json.loads(sources["selected-reading.json"])["source_sha256"],
        "reading_sha256": digest(sources["selected-reading.json"]),
        "ontology_sha256": digest(sources["ontology.yaml"]),
        "ledger_head": replay.ledger_head,
        "ledger_sha256": digest(ledger_bytes),
        "replay_receipt_sha256": digest(replay.receipt.canonical_bytes),
        "query_method_sha256": digest(sources["depth-method.json"]),
        "reproduced_queries_and_traces": True,
        "ledger_unchanged": True,
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(sources.items())
        ],
    }
    target.mkdir(parents=True)
    for name, data in sources.items():
        (target / name).write_bytes(data)
    (target / "manifest.json").write_bytes(canonical(frozen))
    return {
        "packet": str(target),
        "manifest_sha256": digest(canonical(frozen)),
        "questions": len(index["questions"]),
        "central_witnesses": index["distinct_central_witnesses"],
        "traced_records": index["traced_records_including_context"],
    }


def validate(folder, record_path):
    raw = (folder / "manifest.json").read_bytes()
    manifest = json.loads(raw)
    for item in manifest["materials"]:
        path = folder / item["path"]
        require(
            path.resolve().parent == folder.resolve(), "review material escapes packet"
        )
        require(
            digest(path.read_bytes()) == item["sha256"],
            f"review input drift: {item['path']}",
        )
    record = json.loads(record_path.read_bytes())
    require(
        record["reviewer"]["independence"] == manifest["reviewer_mode"],
        "review mode differs from manifest",
    )
    index = json.loads((folder / "review-docket.json").read_bytes())
    queries = json.loads((folder / "query-result.json").read_bytes())
    reading = json.loads((folder / "selected-reading.json").read_bytes())
    blocks = {b["id"] for p in reading["pages"] for b in p["blocks"]}
    return check_review(record, index, queries, blocks, digest(raw))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "validate"))
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--run", type=Path)
    parser.add_argument("--reviewer-mode", choices=sorted(MODES))
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    if args.action == "prepare":
        require(
            args.run is not None and args.reviewer_mode is not None,
            "run and reviewer mode required",
        )
        print(
            json.dumps(prepare(args.run, args.packet, reviewer_mode=args.reviewer_mode))
        )
    else:
        require(args.record is not None, "review record required")
        record = validate(args.packet, args.record)
        print(
            json.dumps(
                {
                    "status": record["status"],
                    "questions": len(record["questions"]),
                    "witnesses": len(record["witnesses"]),
                    "ratification": record["ratification"],
                }
            )
        )

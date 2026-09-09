"""Bounded query-only comparisons using the existing frozen query executor."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path

import malleus.compiler as api

from followup import HERE, ROOT, checked_bytes, verify_materials
import pilot
from repair import check_read_guard, frozen_queries
from review_packet import canonical, digest, docket, new_private_directory


def inputs(run, *, depth=False, count=False, duration=False):
    manifest = json.loads((run / "manifest.json").read_bytes())
    if duration:
        if (
            depth
            or count
            or (manifest["schema"], manifest["condition"])
            != (
                "malleus.paper-v4.acquisition/v1",
                "SOURCE_GROUNDED_ACQUISITION_RELATIONS",
            )
        ):
            raise ValueError(
                "duration comparison requires the exact acquisition condition"
            )
        from repair import preflight
        from reconciliation import authorize

        checked_bytes(
            (run / "manifest.json").read_bytes(),
            "sha256:5060be6e6c6dc2ed6e77eff9f59cd12e6690eabfde5146b3ef0faf2455006830",
            "duration baseline",
        )
        preflight(run)
        authorize(run, run / "evidence/producer/work/candidate-01.json")
    if count:
        if depth or (manifest["schema"], manifest["condition"]) != (
            "malleus.paper-v4.reconciliation/v1",
            "SOURCE_REVIEW_FEEDBACK_RECONCILIATION",
        ):
            raise ValueError("count comparison requires the exact current condition")
        from repair import preflight

        preflight(run)
        verify_materials(
            run, json.loads((run / "outcome.json").read_bytes())["materials"]
        )
    expected_schema = (
        "malleus.paper-v4.acquisition/v1"
        if duration
        else "malleus.paper-v4.reconciliation/v1"
        if count
        else (
            "malleus.paper-v4.qualification/v1"
            if depth
            else "malleus.paper-v4.argument/v1"
        )
    )
    if manifest["schema"] != expected_schema:
        raise ValueError("query comparison requires its exact frozen base condition")
    verify_materials(run, manifest["materials"])
    pilot.verify_runtime(manifest["core_commit"])
    attempt = run / "evidence/attempt-01"
    result = json.loads((attempt / "run-result.json").read_bytes())
    if duration:
        checked_bytes(
            (attempt / "run-result.json").read_bytes(),
            "sha256:0b3513d1010f5270a45e3f0ada051810c6e430ab9e5a6eea0c1ecd5e383b279d",
            "accepted acquisition result",
        )
    if result["status"] != "ADMITTED_REPLAYED_UNREVIEWED":
        raise ValueError("scope comparison requires the admitted argument")
    for name, identity in result["artifacts"].items():
        checked_bytes((attempt / name).read_bytes(), identity, name)
    return manifest, result, attempt


def freeze(run, output, *, depth=False, count=False, duration=False):
    target = new_private_directory(output, ROOT / "private")
    manifest, _, attempt = inputs(run, depth=depth, count=count, duration=duration)
    # The historical projection control is explicitly frozen, not a fallback
    # to a prior selector when the active depth condition fails.
    if duration:
        program = (HERE / "answers.py").read_bytes()
    else:
        historical = (
            ROOT / "private/paper-v4-answer-demonstration/count-query-01/method"
            if count
            else run / ("depth-method-01" if depth else "scope-method-01")
        )
        verify_materials(
            historical,
            json.loads((historical / "method.json").read_bytes())["materials"],
        )
        program = (historical / "answers.py").read_bytes()
    files = {
        "answers.py": program,
        "subject_answers.py": (run / "subject_answers.py").read_bytes(),
        "relation_query.py": Path(__file__).read_bytes(),
        "review_packet.py": (HERE / "review_packet.py").read_bytes(),
        "questions.json": (run / "questions.json").read_bytes(),
        "population-surface.json": (
            run / "evidence/producer/inputs/population-surface.json"
        ).read_bytes(),
    }
    method = {
        "schema": "malleus.paper-v4.duration-query/v1"
        if duration
        else "malleus.paper-v4.count-query/v1"
        if count
        else "malleus.paper-v4.depth-query/v1"
        if depth
        else "malleus.paper-v4.relation-scope-query/v1",
        "decision": "E-0311"
        if duration
        else "E-0304"
        if count
        else "E-0277"
        if depth
        else "E-0263",
        "condition": "QUERY_ONLY_DIRECT_RECORDING_INSTRUMENT"
        if duration
        else "QUERY_ONLY_SCOPED_COUNT_SELECTION"
        if count
        else "QUERY_ONLY_TYPED_DEPTH_SELECTION"
        if depth
        else "QUERY_ONLY_ENDPOINT_SUBJECT_PROJECTION",
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "base_run": str(run.resolve().relative_to(ROOT)),
        "core_commit": manifest["core_commit"],
        "base_result_sha256": digest((attempt / "run-result.json").read_bytes()),
        "materials": [
            {"path": name, "sha256": digest(data)} for name, data in files.items()
        ],
    }
    target.mkdir(parents=True)
    for name, data in files.items():
        (target / name).write_bytes(data)
    (target / "method.json").write_bytes(canonical(method))
    return method


def check_duration_links(before, after, reads):
    """Check the allowed delta against actual graph fields, not answer grading."""
    from answers import HOUSEKEEPING

    for old, new in zip(before, after, strict=True):
        if old["question_id"] != new["question_id"]:
            raise ValueError("duration question identity differs")
        if old["question_id"] != "CQ-T1-05":
            if old != new:
                raise ValueError("duration query changed an unrelated answer")
            continue
        mutable = {"rows", "paths", "witness_ids", "outcome", "note"}
        if old["paths"] or {k: v for k, v in old.items() if k not in mutable} != {
            k: v for k, v in new.items() if k not in mutable
        }:
            raise ValueError("duration query structure differs")
        # The unchanged reader previously returned observations only. Anchor the
        # permitted links in those exact rows, not in the new selector's output.
        selected = {r["witness"]["record_id"] for r in old["rows"]}
        expected_rows, expected_paths = deepcopy(old["rows"]), []
        for edge in sorted(reads.graph.query_relations(), key=lambda e: e["key"]):
            if (
                edge["source_id"] not in selected
                or edge["relation_type"] != "OBSERVED_WITH"
            ):
                continue
            target = reads.graph.get_node(edge["target_id"])
            if target is None:
                raise ValueError("missing duration relation endpoint")
            if target["type"] != "Instrument":
                continue
            source = reads.graph.get_node(edge["source_id"])
            if source is None:
                raise ValueError("missing duration relation endpoint")
            row = {
                "kind": "RELATION",
                "record_type": edge["type"],
                "relation": {
                    k: v
                    for k, v in edge.items()
                    if k not in HOUSEKEEPING | {"key", "source_id", "target_id"}
                },
                "witness": {
                    "relation_id": edge["key"],
                    "source_id": source["id"],
                    "target_id": target["id"],
                },
            }
            for role, node in (("source", source), ("target", target)):
                endpoint = reads.row(node)
                row[role] = endpoint["record"]
                if endpoint["kind"] == "SUBJECT":
                    row[role + "_subject"] = endpoint["subject"]
                    row["witness"][role + "_subject_id"] = endpoint["witness"][
                        "subject_id"
                    ]
            expected_rows.append(row)
            expected_paths.append([source["id"], edge["key"], target["id"]])
        ids = sorted({v for row in expected_rows for v in row["witness"].values()})
        if (
            canonical(new["rows"]) != canonical(expected_rows)
            or new["paths"] != sorted(expected_paths)
            or new["witness_ids"] != ids
        ):
            raise ValueError(
                "duration rows, paths or witnesses differ from permitted graph projection"
            )
        if new["outcome"] != (
            "CANDIDATES_FOR_REVIEW" if expected_rows else "NO_CANDIDATE"
        ):
            raise ValueError("duration outcome differs from returned rows")


def check_count_selection(before, after, reads):
    for old, new in zip(before, after, strict=True):
        if old["question_id"] != new["question_id"]:
            raise ValueError("count comparison question identity differs")
        if old["question_id"] not in {"CQ-T1-02", "CQ-C-04"}:
            if old != new:
                raise ValueError("count selection changed an unrelated question")
            continue
        mutable = {"rows", "witness_ids", "outcome", "note"}
        if (
            {k: v for k, v in old.items() if k not in mutable}
            != {k: v for k, v in new.items() if k not in mutable}
        ) or new["paths"]:
            raise ValueError("count selection changed query structure or paths")
        expected_outcome = "CANDIDATES_FOR_REVIEW" if new["rows"] else "NO_CANDIDATE"
        if new["outcome"] != expected_outcome:
            raise ValueError("count outcome differs from returned rows")
        identities = [row["witness"]["record_id"] for row in new["rows"]]
        if len(identities) != len(set(identities)):
            raise ValueError("duplicate count row")
        witnesses = sorted({v for row in new["rows"] for v in row["witness"].values()})
        if witnesses != new["witness_ids"]:
            raise ValueError("count witness closure differs")
        for row in new["rows"]:
            node = reads.graph.get_node(row["witness"]["record_id"])
            if (
                node is None
                or "count" not in node
                or type(node["count"]) is not int
                or canonical(row) != canonical(reads.row(node))
            ):
                raise ValueError("count projection differs from stored fields")
        if any(
            canonical(row) not in {canonical(r) for r in new["rows"]}
            for row in old["rows"]
        ):
            raise ValueError("count selection lost an existing row")


def check_depth_selection(before, after):
    for old, new in zip(before, after, strict=True):
        if old["question_id"] != new["question_id"]:
            raise ValueError("depth comparison question identity differs")
        if old["question_id"] != "CQ-T3-01":
            if old != new:
                raise ValueError("depth selection changed an unrelated question")
            continue
        if old["paths"] != new["paths"]:
            raise ValueError("depth selection changed paths")
        witnesses = sorted({v for row in new["rows"] for v in row["witness"].values()})
        if witnesses != new["witness_ids"]:
            raise ValueError("depth selection witness closure differs")
        previous = {row["witness"]["record_id"]: row for row in old["rows"]}
        for row in new["rows"]:
            record = row["record"]
            if (
                "quantity_kind_class" not in record
                or record["quantity_kind_class"] != "Length"
                or not any(
                    k in record and type(record[k]) in (int, float)
                    for k in ("value_lower", "value_upper")
                )
            ):
                raise ValueError("depth candidate is not an explicit numeric Length")
            key = row["witness"]["record_id"]
            if key in previous and row != previous[key]:
                raise ValueError("depth selection changed an existing projection")


def check_projection(before, after):
    stripped = deepcopy(after)
    for query in stripped:
        ids = sorted({v for row in query["rows"] for v in row["witness"].values()})
        if ids != query["witness_ids"]:
            raise ValueError("projected witness closure differs")
        for row in query["rows"]:
            if row["kind"] != "RELATION":
                continue
            for role in ("source", "target"):
                context, identity = role + "_subject", role + "_subject_id"
                if "subject" in row[role]:
                    value = row.pop(context)
                    if (
                        not isinstance(value, dict)
                        or row["witness"].pop(identity) != row[role]["subject"]
                    ):
                        raise ValueError("projected subject binding differs")
                elif context in row or identity in row["witness"]:
                    raise ValueError("subject context was invented")
        query["witness_ids"] = sorted(
            {v for row in query["rows"] for v in row["witness"].values()}
        )
    if stripped != before:
        raise ValueError("query changed more than endpoint subject projection")


def execute(run, method_folder, output):
    target = new_private_directory(output, ROOT / "private")
    method = json.loads((method_folder / "method.json").read_bytes())
    verify_materials(method_folder, method["materials"])
    condition = (method["schema"], method["condition"])
    duration = condition == (
        "malleus.paper-v4.duration-query/v1",
        "QUERY_ONLY_DIRECT_RECORDING_INSTRUMENT",
    )
    count = condition == (
        "malleus.paper-v4.count-query/v1",
        "QUERY_ONLY_SCOPED_COUNT_SELECTION",
    )
    if condition == (
        "malleus.paper-v4.depth-query/v1",
        "QUERY_ONLY_TYPED_DEPTH_SELECTION",
    ):
        depth = True
    elif (
        count
        or duration
        or condition
        == (
            "malleus.paper-v4.relation-scope-query/v1",
            "QUERY_ONLY_ENDPOINT_SUBJECT_PROJECTION",
        )
    ):
        depth = False
    else:
        raise ValueError("unknown query comparison condition")
    if method["base_run"] != str(run.resolve().relative_to(ROOT)):
        raise ValueError("scope method belongs to a different run")
    # Query programs execute from the method directory. The orchestration and
    # docket implementation must also match the recorded method, not drift.
    for name in ("relation_query.py", "review_packet.py"):
        checked_bytes(
            (HERE / name).read_bytes(),
            digest((method_folder / name).read_bytes()),
            name,
        )
    manifest, expected, attempt = inputs(
        run, depth=depth, count=count, duration=duration
    )
    checked_bytes(
        (attempt / "run-result.json").read_bytes(),
        method["base_result_sha256"],
        "base result",
    )
    if manifest["core_commit"] != method["core_commit"]:
        raise ValueError("scope method Core binding differs")
    ledger = attempt / "ledger/history.jsonl"
    ledger_identity = digest(ledger.read_bytes())
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    checked_bytes(
        replay.receipt.canonical_bytes,
        expected["artifacts"]["replay-receipt.json"],
        "receipt",
    )
    checked_bytes(
        pilot.canonical(replay.graph.export_records()),
        expected["artifacts"]["export-records.json"],
        "graph",
    )
    surface = json.loads((method_folder / "population-surface.json").read_bytes())
    old = json.loads((attempt / "query-result.json").read_bytes())["queries"]
    baseline, _, old_guard, attempts = frozen_queries(
        run, replay, surface, reader="SubjectGraphReads"
    )
    check_read_guard(attempts)
    if baseline != old:
        raise ValueError("historical query control does not reproduce")
    new, traces, guard, attempts = frozen_queries(
        method_folder, replay, surface, reader="SubjectGraphReads"
    )
    check_read_guard(attempts)
    if old_guard != guard:
        raise ValueError("query guard identity differs")
    if duration:
        from answers import GraphReads

        check_duration_links(old, new, GraphReads(replay.graph, surface))
    elif count:
        from answers import GraphReads

        check_count_selection(old, new, GraphReads(replay.graph, surface))
    elif depth:
        check_depth_selection(old, new)
    else:
        check_projection(old, new)
    checked_bytes(ledger.read_bytes(), ledger_identity, "unchanged ledger")
    checked_bytes(
        pilot.canonical(replay.graph.export_records()),
        expected["artifacts"]["export-records.json"],
        "unchanged graph",
    )
    result = {
        "schema": method["schema"],
        "status": "EXPLORATORY_UNREVIEWED",
        "core_commit": method["core_commit"],
        "method_sha256": digest((method_folder / "method.json").read_bytes()),
        "historical_replay_matches": True,
        "ledger_bytes_unchanged": True,
        "inputs": {
            "ledger_head": replay.ledger_head,
            "replay_receipt_sha256": expected["artifacts"]["replay-receipt.json"],
            "read_guard_sha256": guard,
            "query_program_sha256": digest((method_folder / "answers.py").read_bytes()),
            "reader_sha256": digest(
                (method_folder / "subject_answers.py").read_bytes()
            ),
        },
        "forbidden_attempts": attempts,
        "queries": new,
    }
    trace = {"records": traces}
    review = docket(
        json.loads((method_folder / "questions.json").read_bytes()), result, trace
    )
    summary = {
        "original_queries_reproduced": True,
        "duration_links_only"
        if duration
        else "count_selection_only"
        if count
        else "depth_selection_only"
        if depth
        else "projection_only": True,
        "ledger_bytes_unchanged": True,
        "changed_questions": [
            b["question_id"] for a, b in zip(old, new, strict=True) if a != b
        ],
        "rows": sum(len(q["rows"]) for q in new),
        "paths": sum(len(q["paths"]) for q in new),
        "traced_records": len(traces),
        "query_result_sha256": digest(canonical(result)),
    }
    target.mkdir(parents=True)
    for name, value in (
        ("query-result.json", result),
        ("query-trace-summary.json", trace),
        ("review-docket.json", review),
        ("summary.json", summary),
    ):
        (target / name).write_bytes(canonical(value))
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "execute"))
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--method", type=Path)
    parser.add_argument("--depth", action="store_true")
    parser.add_argument("--count", action="store_true")
    parser.add_argument("--duration", action="store_true")
    args = parser.parse_args()
    if args.action == "execute" and args.method is None:
        parser.error("execute requires --method")
    value = (
        freeze(
            args.run,
            args.output,
            depth=args.depth,
            count=args.count,
            duration=args.duration,
        )
        if args.action == "freeze"
        else execute(args.run, args.method, args.output)
    )
    print(canonical(value).decode())

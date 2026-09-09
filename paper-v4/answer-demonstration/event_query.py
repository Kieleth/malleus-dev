"""Query-only projection of direct causal event references on one frozen history."""

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path

import malleus.compiler as api

from answers import GraphReads
from followup import checked_bytes, verify_materials
import fresh_comparison as fresh
import pilot
from repair import check_read_guard, frozen_queries
from review_packet import canonical, digest, docket, new_private_directory
from snapshot_review import trace_closure

HERE = Path(__file__).resolve().parent
PRIVATE = pilot.ROOT / "private/paper-v4-answer-demonstration"
BASE = PRIVATE / "sol-fresh-comparison-01"
CORE = "160878cf14c0d27b11a440e26688708e9b7a7e2b"
RESULT_ID = "sha256:8224cf24061923e890aec89ee568ca24272d2a8762ca8aa065f711b67bf9a0db"
SURFACE_ID = "sha256:c4c4f39050c2a444767cafef96b2362d83dda9e8d219647693295f3824cf56c8"
QUESTIONS = {"CQ-T4-01", "CQ-T4-02", "CQ-T5-01"}
ROLES = ("cause_event", "effect_event")
IMPLEMENTATION = (
    "event_query.py",
    "review_packet.py",
    "snapshot_review.py",
    "pilot.py",
)


def expand(reads, query):
    """Append referenced events, preserving original rows and real relation paths."""
    result = deepcopy(query)
    if query["question_id"] not in QUESTIONS:
        return result
    present = {
        r["witness"]["record_id"] for r in query["rows"] if r["kind"] != "RELATION"
    }
    events = {}
    for row in query["rows"]:
        if row["kind"] == "RELATION":
            records = [
                (row[role], reads.graph.get_node(row["witness"][role + "_id"]))
                for role in ("source", "target")
            ]
        else:
            records = [
                (row["record"], reads.graph.get_node(row["witness"]["record_id"]))
            ]
        for fields, origin in records:
            for role in ROLES:
                if role not in fields:
                    continue
                if origin is None:
                    raise ValueError("causal event reference has no origin record")
                label = f"causal event reference {origin['id']}.{role}"
                slots = [
                    s for s in reads.types[origin["type"]]["slots"] if s["name"] == role
                ]
                if (
                    len(slots) != 1
                    or not {"range_id", "multivalued"} <= slots[0].keys()
                    or slots[0]["multivalued"] is not False
                ):
                    raise ValueError(label + " requires a declared scalar slot")
                declared = [
                    t
                    for t in reads.types.values()
                    if t["qualified_name"] == slots[0]["range_id"]
                ]
                if len(declared) != 1 or declared[0]["family"] != "EVENT":
                    raise ValueError(label + " must declare an Event range")
                key = fields[role]
                if not isinstance(key, str) or not key or origin[role] != key:
                    raise ValueError(
                        label + " must equal its stored nonempty record ID"
                    )
                event = reads.graph.get_node(key)
                if event is None:
                    raise ValueError(label + f" points to missing record {key}")
                if (
                    event["id"] != key
                    or reads.types[event["type"]]["family"] != "EVENT"
                    or key
                    not in {
                        n["id"]
                        for n in reads.graph.query(entity_type=declared[0]["name"])
                    }
                ):
                    raise ValueError(
                        label + f" target {key} is outside its Event range"
                    )
                if key not in present:
                    events[key] = reads.row(event)
    result["rows"].extend(events[key] for key in sorted(events))
    result["witness_ids"] = sorted(
        {key for row in result["rows"] for key in row["witness"].values()}
    )
    return result


def check_delta(reads, before, after):
    if len(before) != len(after) or any(
        expand(reads, old) != new for old, new in zip(before, after, strict=True)
    ):
        raise ValueError("query changed more than exact direct event projection")


def inputs():
    fresh.verify_packet(BASE)
    checked_bytes(
        (HERE / "answers.py").read_bytes(),
        digest(fresh.method_files()["answers.py"]),
        "event-query projection source",
    )
    attempt = BASE / "attempt-02"
    expected = json.loads(
        checked_bytes(
            (attempt / "run-result.json").read_bytes(),
            RESULT_ID,
            "event-query base result",
        )
    )
    if expected["core_commit"] != CORE or expected["status"] != "ADMITTED_AND_REPLAYED":
        raise ValueError("event-query requires the frozen admitted Core result")
    surface = checked_bytes(
        (BASE / "producer/accepted/population-surface.json").read_bytes(),
        SURFACE_ID,
        "event-query surface",
    )
    old = json.loads(
        checked_bytes(
            (attempt / "query-result.json").read_bytes(),
            expected["query_result_sha256"],
            "event-query original answers",
        )
    )
    return attempt, expected, surface, old


def freeze(output):
    target = new_private_directory(output, PRIVATE)
    _, _, surface, _ = inputs()
    files = {
        **fresh.method_files(),
        **{name: (HERE / name).read_bytes() for name in IMPLEMENTATION},
        "population-surface.json": surface,
    }
    method = {
        "schema": "malleus.paper-v4.causal-event-query/v1",
        "decision": "E-0326",
        "condition": "QUERY_ONLY_DIRECT_CAUSAL_EVENT_RECORDS",
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "core_commit": CORE,
        "base_result_sha256": RESULT_ID,
        "base_query_method_sha256": fresh.METHOD_IDENTITY,
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(files.items())
        ],
    }
    target.mkdir(parents=True)
    for name, data in files.items():
        (target / name).write_bytes(data)
    (target / "method.json").write_bytes(canonical(method))
    return method


def execute(method_folder, output):
    target = new_private_directory(output, PRIVATE)
    method = json.loads((method_folder / "method.json").read_bytes())
    if (
        method["schema"],
        method["condition"],
        method["decision"],
        method["core_commit"],
        method["base_result_sha256"],
        method["base_query_method_sha256"],
    ) != (
        "malleus.paper-v4.causal-event-query/v1",
        "QUERY_ONLY_DIRECT_CAUSAL_EVENT_RECORDS",
        "E-0326",
        CORE,
        RESULT_ID,
        fresh.METHOD_IDENTITY,
    ):
        raise ValueError("event-query method belongs to a different condition")
    verify_materials(method_folder, method["materials"])
    for name in IMPLEMENTATION:
        checked_bytes(
            (HERE / name).read_bytes(),
            digest((method_folder / name).read_bytes()),
            name,
        )
    for name, data in fresh.method_files().items():
        checked_bytes((method_folder / name).read_bytes(), digest(data), name)
    attempt, expected, surface_bytes, old = inputs()
    checked_bytes(
        (method_folder / "population-surface.json").read_bytes(),
        digest(surface_bytes),
        "method surface",
    )
    ledger = attempt / "ledger/history.jsonl"
    ledger_bytes = ledger.read_bytes()
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    checked_bytes(
        replay.receipt.canonical_bytes,
        expected["replay_receipt_sha256"],
        "replay receipt",
    )
    graph = pilot.canonical(replay.graph.export_records())
    checked_bytes(graph, expected["export_records_sha256"], "replayed graph")
    surface = json.loads(surface_bytes)
    before, old_traces, guard_id, counters = frozen_queries(
        method_folder, replay, surface, reader="SubjectGraphReads"
    )
    check_read_guard(counters)
    if before != old["queries"]:
        raise ValueError("event-query original answers do not reproduce")
    native, identity = pilot.load_native()
    if identity != guard_id:
        raise ValueError("event-query read guard differs")
    guard = native._SourceFreeGuard()
    with guard:
        reads = GraphReads(replay.graph, surface)
        after = [expand(reads, q) for q in before]
        check_delta(reads, before, after)
        traces = native.trace_witnesses(
            replay, sorted({key for q in after for key in q["witness_ids"]})
        )
    check_read_guard(guard.attempts)
    if (
        ledger.read_bytes() != ledger_bytes
        or pilot.canonical(replay.graph.export_records()) != graph
    ):
        raise ValueError("event-query changed history or graph")
    reading = checked_bytes(
        (BASE / "producer/inputs/selected-reading.json").read_bytes(),
        expected["reading_sha256"],
        "reading",
    )
    capture = checked_bytes(
        (attempt / "ledger/retained-capture.json").read_bytes(),
        expected["capture"]["capture_sha256"],
        "capture",
    )
    trace = {"records": traces}
    query = {
        "schema": method["schema"],
        "status": "UNREVIEWED",
        "core_commit": CORE,
        "method_sha256": digest((method_folder / "method.json").read_bytes()),
        "base_result_sha256": RESULT_ID,
        "ledger_head": replay.ledger_head,
        "replay_receipt_sha256": expected["replay_receipt_sha256"],
        "read_guard_sha256": guard_id,
        "forbidden_attempts": guard.attempts,
        "queries": after,
    }
    summary = {
        "original_queries_reproduced": True,
        "ledger_bytes_unchanged": True,
        "event_projection_only": True,
        "changed_questions": [
            new["question_id"]
            for prev, new in zip(before, after, strict=True)
            if prev != new
        ],
        "added_record_ids": sorted(
            {t["record_id"] for t in traces} - {t["record_id"] for t in old_traces}
        ),
        "traced_records": len(traces),
        "rows": sum(len(q["rows"]) for q in after),
        "query_result_sha256": digest(canonical(query)),
        "coverage": "NOT_ASSESSED",
    }
    files = {
        "query-result.json": query,
        "query-trace-summary.json": trace,
        "resolved-trace.json": trace_closure(reading, {"capture.json": capture}, trace),
        "review-docket.json": docket(
            json.loads((method_folder / "questions.json").read_bytes()), query, trace
        ),
        "summary.json": summary,
    }
    target.mkdir(parents=True)
    for name, value in files.items():
        (target / name).write_bytes(canonical(value))
    return summary

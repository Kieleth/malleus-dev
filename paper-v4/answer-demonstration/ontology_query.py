"""A separately frozen text-binding condition over an already replayed graph."""

from datetime import datetime, timezone
import json
from pathlib import Path

import malleus.compiler as api

from binding import load_query_program
from followup import checked_bytes, verify_materials
from freeze_review import freeze_sources
import pilot
from ontology_answers import text_binding
from review_packet import (
    canonical,
    digest,
    docket,
    new_private_directory,
    verify_trace_materials,
    vocabulary_sources,
)


HERE = Path(__file__).resolve().parent
CODE_FILES = ("answers.py", "ontology_answers.py", "ontology_query.py", "binding.py")


def freeze(run, output):
    target = new_private_directory(output, pilot.ROOT / "private")
    source = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, source["materials"])
    files = {
        name: ((run / "frozen-code") if name == "answers.py" else HERE)
        .joinpath(name)
        .read_bytes()
        for name in CODE_FILES
    }
    checked_bytes(
        files["answers.py"],
        source["query_program_sha256"],
        "unchanged question programs",
    )
    files["population-surface.json"] = (
        run / "producer/accepted/population-surface.json"
    ).read_bytes()
    files["competency-questions.json"] = (
        run / "competency-questions.json"
    ).read_bytes()
    method = {
        "condition": "EXPLICIT_ONTOLOGY_TEXT_BINDING",
        "decision": "E-0247",
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "core_commit": source["core_commit"],
        "ontology_sha256": source["ontology_sha256"],
        "text_slots": text_binding(json.loads(files["population-surface.json"])),
        "materials": [
            {"path": name, "sha256": digest(data)} for name, data in files.items()
        ],
    }
    target.mkdir(parents=True)
    for name, data in files.items():
        (target / name).write_bytes(data)
    (target / "method.json").write_bytes(canonical(method))
    return method


def method_inputs(folder):
    method = json.loads((folder / "method.json").read_bytes())
    verify_materials(folder, method["materials"])
    for name in CODE_FILES:
        if name == "answers.py":
            continue  # This exact historical module is loaded below, not imported.
        if (folder / name).read_bytes() != (HERE / name).read_bytes():
            raise ValueError(f"loaded query condition differs from frozen code: {name}")
    surface = json.loads((folder / "population-surface.json").read_bytes())
    if text_binding(surface) != method["text_slots"]:
        raise ValueError("explicit text binding changed")
    return method, surface


def execute(run, attempt, method_folder, output, *, compare_original=False):
    target = new_private_directory(output, pilot.ROOT / "private")
    method, surface = method_inputs(method_folder)
    pilot.verify_runtime(method["core_commit"])
    expected = json.loads((attempt / "run-result.json").read_bytes())
    if (
        expected["status"] != "ADMITTED_AND_REPLAYED"
        or expected["ontology_sha256"] != method["ontology_sha256"]
    ):
        raise ValueError("query requires the selected admitted ontology")
    ledger = attempt / "ledger/history.jsonl"
    ledger_before = digest(ledger.read_bytes())
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    checked_bytes(
        replay.receipt.canonical_bytes, expected["replay_receipt_sha256"], "receipt"
    )
    checked_bytes(
        pilot.canonical(replay.graph.export_records()),
        expected["export_records_sha256"],
        "graph",
    )
    program = load_query_program(
        method_folder / "ontology_answers.py",
        digest((method_folder / "ontology_answers.py").read_bytes()),
    )
    base = load_query_program(
        method_folder / "answers.py",
        digest((method_folder / "answers.py").read_bytes()),
    )
    questions_source = (method_folder / "competency-questions.json").read_bytes()
    questions = pilot.load_questions(questions_source)
    old = None
    if compare_original:
        old = json.loads(
            checked_bytes(
                (attempt / "query-result.json").read_bytes(),
                expected["query_result_sha256"],
                "original query",
            )
        )["queries"]
    native, guard_identity = pilot.load_native()
    guard = native._SourceFreeGuard()
    state = replay.graph.state_digest()
    with guard:
        if compare_original:
            control = [
                base.answer(base.GraphReads(replay.graph, surface), q["id"])
                for q in questions
            ]
            if control != old:
                raise ValueError("original query control does not reproduce")
        reads = program.GraphReads(replay.graph, surface, program=base)
        queries = [base.answer(reads, q["id"]) for q in questions]
        traces = native.trace_witnesses(
            replay, sorted({key for q in queries for key in q["witness_ids"]})
        )
    if (
        digest(ledger.read_bytes()) != ledger_before
        or replay.graph.state_digest() != state
    ):
        raise ValueError("query changed accepted state")
    result = {
        "schema": "malleus.paper-v4.ontology-query/v1",
        "status": "EXPLORATORY_UNREVIEWED",
        "run_id": run.name,
        "core_commit": method["core_commit"],
        "historical_replay_matches": True,
        "ledger_bytes_unchanged": True,
        "forbidden_attempts": guard.attempts,
        "inputs": {
            "query_program_sha256": digest(
                (method_folder / "ontology_answers.py").read_bytes()
            ),
            "base_query_program_sha256": digest(
                (method_folder / "answers.py").read_bytes()
            ),
            "runner_sha256": digest((method_folder / "ontology_query.py").read_bytes()),
            "binding_program_sha256": digest(
                (method_folder / "binding.py").read_bytes()
            ),
            "population_surface_sha256": digest(
                (method_folder / "population-surface.json").read_bytes()
            ),
            "question_set_sha256": digest(questions_source),
            "text_binding_sha256": digest((method_folder / "method.json").read_bytes()),
            "read_guard_sha256": guard_identity,
            "ledger_head": replay.ledger_head,
            "replay_receipt_sha256": expected["replay_receipt_sha256"],
        },
        "queries": queries,
    }
    summary = {
        "original_queries_reproduced": compare_original,
        "query_result_sha256": digest(canonical(result)),
        "queries_with_rows": sum(bool(q["rows"]) for q in queries),
        "rows": sum(len(q["rows"]) for q in queries),
        "ledger_bytes_unchanged": True,
    }
    if compare_original:
        summary["changed_questions"] = [
            b["question_id"] for a, b in zip(old, queries, strict=True) if a != b
        ]
    target.mkdir(parents=True)
    (target / "query-result.json").write_bytes(canonical(result))
    (target / "query-trace-summary.json").write_bytes(canonical({"records": traces}))
    (target / "summary.json").write_bytes(canonical(summary))
    return summary


def prepare_review(run, attempt, method_folder, query, output):
    target = new_private_directory(output, pilot.ROOT / "private")
    method_inputs(method_folder)
    manifest = json.loads((run / "manifest.json").read_bytes())
    expected = json.loads((attempt / "run-result.json").read_bytes())
    paths = {
        "selected-reading.json": run / "producer/inputs/selected-reading.json",
        "retained-capture.json": attempt / "ledger/retained-capture.json",
        "population-trace.json": attempt / "public/trace-summary.json",
        "query-result.json": query / "query-result.json",
        "query-trace-summary.json": query / "query-trace-summary.json",
        "population-surface.json": method_folder / "population-surface.json",
        "competency-questions.json": method_folder / "competency-questions.json",
        "text-binding.json": method_folder / "method.json",
        "review.py": pilot.ROOT / "paper-v4/evaluation-v4/review.py",
        "review-protocol-v3.json": pilot.ROOT
        / "paper-v4/evaluation-v4/review-protocol-v3.json",
    }
    sources = {name: path.read_bytes() for name, path in paths.items()}
    sources.update({name: (method_folder / name).read_bytes() for name in CODE_FILES})
    result = json.loads(sources["query-result.json"])
    for key in ("ledger_head", "replay_receipt_sha256"):
        if result["inputs"][key] != expected[key]:
            raise ValueError(f"review query replay binding differs: {key}")
    trace = json.loads(sources["query-trace-summary.json"])
    verify_trace_materials(
        sources["selected-reading.json"], sources["retained-capture.json"], trace
    )
    sources["review-docket.json"] = canonical(
        docket(json.loads(sources["competency-questions.json"]), result, trace)
    )
    sources.update(
        vocabulary_sources(
            manifest["source_closure_sha256"],
            [run / manifest["ontology_path"]]
            + list((run / "producer/inputs").glob("*.yaml")),
            manifest["ontology_sha256"],
        )
    )
    prepared = {
        "accepted_ontology_sha256": manifest["ontology_sha256"],
        "ledger_head": expected["ledger_head"],
        "replay_receipt_sha256": expected["replay_receipt_sha256"],
        "rows_per_question": {
            q["question_id"]: len(q["rows"]) for q in result["queries"]
        },
    }
    return freeze_sources(
        sources, prepared, target, run.name + "-" + query.name + "-review"
    )

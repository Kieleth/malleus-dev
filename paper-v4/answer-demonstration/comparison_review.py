"""Freeze comparable review inputs, not source-support or coverage judgments."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

import malleus.compiler as api

import comparison_reads as reads
from followup import checked_bytes, verify_materials
from review_packet import (
    canonical,
    digest,
    docket,
    new_private_directory,
    vocabulary_sources,
)
from snapshot_review import trace_closure

HERE = Path(__file__).resolve().parent
CRITERIA = reads.PRIVATE / "current-thirty-review-01"
CRITERIA_ID = "sha256:14c11d7c186b34c7ad53b96b266748980fdfb7c201af566f82b337bc96c0484a"
QUALIFICATION_ID = (
    "sha256:ca93de9bdd99d8a5bb527702fd3fb498d586de66f0303d597a4662b0ba67a68d"
)
READING_ID = "sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17"


def load_query(folder):
    return json.loads((folder / "query-result.json").read_bytes())


def freeze(
    output,
    *,
    query,
    trace,
    surface,
    graph,
    reading,
    captures,
    vocabulary,
    query_capacity,
    receipt,
    origin_query_id,
):
    target = new_private_directory(output, reads.PRIVATE)
    checked_bytes(reading, READING_ID, "comparison selected reading")
    criteria = checked_bytes(
        (CRITERIA / "review-criteria.md").read_bytes(),
        CRITERIA_ID,
        "review criteria",
    ).decode()
    interpretation = criteria.split("## Fixed interpretation before assessment\n", 1)[
        1
    ].split(
        "## Deliverables and checks\n",
        1,
    )[0]
    qualification = checked_bytes(
        (CRITERIA / "qualification-criteria.json").read_bytes(),
        QUALIFICATION_ID,
        "qualification criteria",
    )
    question_bytes = (reads.METHOD / "questions.json").read_bytes()
    index = docket(json.loads(question_bytes), query, trace)
    task = (HERE / "snapshot-review-task.md").read_text()
    old = "This is a current snapshot of an iteratively refined history. It is neither\nfirst-pass capture quality nor an assessment of the underlying scientific truth."
    if task.count(old) != 1:
        raise ValueError("review task context changed")
    task = task.replace(
        old,
        "This is one anonymized answer view. Its generation condition is withheld.\nAssess represented source meaning and coverage, not the underlying scientific truth.",
    )
    task += "\nThe declaration audit diagnoses only the fixed reader's schema dependencies.\nA declaration gap is not proof of missing graph content. Inspect graph records\nseparately when diagnosing an absence, never use them to fill a query answer.\nOnly the query envelope is anonymized; all returned rows and paths are unchanged.\nArtifacts may reveal origin, so this is not a claim of perfect blinding.\n"
    files = {
        "TASK.md": task.encode(),
        "review-criteria.md": (
            "## Fixed interpretation before assessment\n" + interpretation
        ).encode(),
        "qualification-criteria.json": qualification,
        "query-result.json": canonical({"queries": query["queries"]}),
        "review-docket.json": canonical(index),
        "query-trace-summary.json": canonical(trace),
        "query-capacity.json": query_capacity,
        "population-surface.json": surface,
        "export-records.json": graph,
        "replay-receipt.json": receipt,
        "selected-reading.json": reading,
        "resolved-trace.json": canonical(trace_closure(reading, captures, trace)),
        "capture-catalog.json": canonical(
            {name: digest(data) for name, data in captures.items()}
        ),
        **captures,
        **vocabulary,
        **{
            name: (HERE / name).read_bytes()
            for name in ("snapshot_review.py", "review_packet.py")
        },
    }
    manifest = {
        "schema": "malleus.paper-v4.comparison-review-inputs/v1",
        "reviewer_mode": "FRESH_INDEPENDENT",
        "ratification": "PENDING_HUMAN",
        "origin_query_sha256": origin_query_id,
        "returned_queries_sha256": digest(canonical(query["queries"])),
        "criteria_origin_sha256": CRITERIA_ID,
        "query_method_sha256": reads.METHOD_IDENTITY,
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(files.items())
        ],
    }
    target.mkdir(parents=True)
    for name, data in files.items():
        (target / name).write_bytes(data)
    (target / "manifest.json").write_bytes(canonical(manifest))
    return {
        "manifest_sha256": digest(canonical(manifest)),
        "questions": len(index["questions"]),
        "witnesses": index["distinct_central_witnesses"],
        "traced_records": index["traced_records_including_context"],
    }


def prepare_reference(case, evidence, output):
    if case not in reads.CASES:
        raise ValueError("reference case was not selected")
    new_private_directory(output, reads.PRIVATE)
    with TemporaryDirectory(
        dir=reads.PRIVATE, prefix="verify-comparison-"
    ) as directory:
        check = Path(directory) / "read"
        reads.execute(case, check)
        for path in check.iterdir():
            if path.read_bytes() != (evidence / path.name).read_bytes():
                raise ValueError("comparison evidence differs: " + path.name)
    query = load_query(evidence)
    trace = json.loads((evidence / "query-trace-summary.json").read_bytes())
    expected = json.loads((evidence / "review-docket.json").read_bytes())
    if (
        docket(json.loads((reads.METHOD / "questions.json").read_bytes()), query, trace)
        != expected
    ):
        raise ValueError("comparison query/docket differs")
    attempt, surface, result_id, _ = reads.CASES[case]
    result = json.loads(
        checked_bytes((attempt / "run-result.json").read_bytes(), result_id, "result")
    )
    inputs = attempt.parent / "producer/inputs"
    if case == "repaired":
        # This reference deliberately uses the exact unchanged calibration ontology.
        fixed_attempt, _, fixed_id, _ = reads.CASES["fixed-ontology"]
        contract_result = json.loads(
            checked_bytes(
                (fixed_attempt / "run-result.json").read_bytes(),
                fixed_id,
                "ontology reference",
            )
        )
        catalog = json.loads((inputs / "capture-catalog.json").read_bytes())
        captures = {
            name: checked_bytes((inputs / name).read_bytes(), identity, name)
            for name, identity in catalog.items()
        }
        captures["new-capture.json"] = (attempt / "retained-capture.json").read_bytes()
        ontology = inputs / "ontology.yaml"
    else:
        contract_result = result
        if case == "earlier-fresh":
            capture_path = attempt / "ledger/retained-capture.json"
            manifest = json.loads((attempt.parent / "manifest.json").read_bytes())
            ontology = attempt.parent / manifest["ontology_path"]
        else:
            capture_path = attempt / "retained-capture.json"
            ontology = inputs / "ontology.yaml"
        captures = {"capture.json": capture_path.read_bytes()}
    captures = {
        f"capture-{number:02d}.json": data
        for number, data in enumerate(captures.values(), 1)
    }
    vocabulary = vocabulary_sources(
        contract_result["source_closure_sha256"],
        [ontology, *inputs.glob("*.yaml")],
        contract_result["ontology_sha256"],
    )
    ledger = attempt / "ledger/history.jsonl"
    ledger_bytes = ledger.read_bytes()
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    graph = reads.pilot.canonical(replay.graph.export_records())
    receipt = replay.receipt.canonical_bytes
    if case == "repaired":
        graph_id = result["artifacts"]["export-records.json"]
        receipt_id = result["artifacts"]["replay-receipt.json"]
    else:
        graph_id = result["export_records_sha256"]
        receipt_id = result["replay_receipt_sha256"]
    checked_bytes(graph, graph_id, "review graph")
    checked_bytes(receipt, receipt_id, "review receipt")
    if ledger.read_bytes() != ledger_bytes:
        raise ValueError("review preparation changed ledger")
    return freeze(
        output,
        query=query,
        trace=trace,
        surface=surface.read_bytes(),
        graph=graph,
        reading=(inputs / "selected-reading.json").read_bytes(),
        captures=captures,
        vocabulary=vocabulary,
        query_capacity=(evidence / "query-capacity.json").read_bytes(),
        receipt=receipt,
        origin_query_id=digest((evidence / "query-result.json").read_bytes()),
    )


def prepare_fresh(run, attempt, output):
    import fresh_comparison as fresh
    from repair import frozen_queries, check_read_guard

    new_private_directory(output, reads.PRIVATE)
    fresh.verify_observed(run, "initial")
    fresh.verify_observed(run, "accepted")
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    result = json.loads((attempt / "run-result.json").read_bytes())
    if (
        attempt.parent != run
        or result["run_id"] != manifest["run_id"]
        or result["status"] != "ADMITTED_AND_REPLAYED"
    ):
        raise ValueError("review requires this run's admitted attempt")
    fresh.check_execution_attempt(
        run,
        run / "reproduction-01",
        attempt / "submitted-population.json",
        result["transaction_time"],
    )
    for name in (
        "ledger/history.jsonl",
        "query-result.json",
        "query-trace-summary.json",
    ):
        if (attempt / name).read_bytes() != (
            run / "reproduction-01" / name
        ).read_bytes():
            raise ValueError("fresh reproduction differs: " + name)
    query_bytes = checked_bytes(
        (attempt / "query-result.json").read_bytes(),
        result["query_result_sha256"],
        "query result",
    )
    query = load_query(attempt)
    trace = json.loads((attempt / "query-trace-summary.json").read_bytes())
    surface = (run / "producer/accepted/population-surface.json").read_bytes()
    ledger = attempt / "ledger/history.jsonl"
    ledger_bytes = ledger.read_bytes()
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    graph = checked_bytes(
        reads.pilot.canonical(replay.graph.export_records()),
        result["export_records_sha256"],
        "fresh graph",
    )
    receipt = checked_bytes(
        replay.receipt.canonical_bytes, result["replay_receipt_sha256"], "fresh receipt"
    )
    queries, traces, guard, counts = frozen_queries(
        run / "frozen-code",
        replay,
        json.loads(surface),
        reader="SubjectGraphReads",
        questions_path=run / "competency-questions.json",
    )
    check_read_guard(counts)
    if (
        query["queries"] != queries
        or trace["records"] != traces
        or query["inputs"]["read_guard_sha256"] != guard
    ):
        raise ValueError("fresh query or traces do not reproduce")
    if ledger.read_bytes() != ledger_bytes:
        raise ValueError("fresh review changed ledger")
    inputs = run / "producer/inputs"
    ontology = run / manifest["ontology_path"]
    vocabulary = vocabulary_sources(
        manifest["source_closure_sha256"],
        [ontology, *inputs.glob("*.yaml")],
        manifest["ontology_sha256"],
    )
    return freeze(
        output,
        query=query,
        trace=trace,
        surface=surface,
        graph=graph,
        reading=(inputs / "selected-reading.json").read_bytes(),
        captures={
            "capture-01.json": (attempt / "ledger/retained-capture.json").read_bytes()
        },
        vocabulary=vocabulary,
        query_capacity=(run / "query-capacity.json").read_bytes(),
        receipt=receipt,
        origin_query_id=digest(query_bytes),
    )

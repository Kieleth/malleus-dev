"""Stage one source-context repair against the frozen fresh graph."""

import json
from pathlib import Path
import subprocess
import sys

import malleus.compiler as api
import event_query as events
from followup import checked_bytes, verify_materials
from input_delivery import verify_delivery
from meaning_audit import inventory
from meaning_repair import check_scope
import pilot
import reconciliation
import repair
from review_packet import canonical, digest, new_private_directory
from snapshot_review import trace_closure

HERE = Path(__file__).resolve().parent
PRIVATE = pilot.ROOT / "private/paper-v4-answer-demonstration"
METHOD = PRIVATE / "event-query-01/method"
METHOD_ID = "sha256:a16f3d5c5b9bb4bbb3a26ddfdccf7e23fffa7500a049133a2d4e970e88b47a6d"
SCHEMA = "malleus.paper-v4.meaning-repair/v1"
TYPES = {
    "ScientificClaim",
    "ScientificObservation",
    "CountObservation",
    "RatioObservation",
}
CHECKS = ("meaning_audit.py", "meaning_repair.py", "reconciliation.py", "repair.py")
LOADED = Path(__file__).read_bytes()


def write_new(folder, files):
    folder.mkdir(parents=True, exist_ok=False)
    for name, data in files.items():
        path = folder / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(data)


def source_files():
    attempt, result, surface, _ = events.inputs()
    source = events.BASE / "producer"
    original = json.loads((events.BASE / "producer-input-manifest.json").read_bytes())
    files = {
        item["target"]: checked_bytes(
            (source / item["target"]).read_bytes(), item["sha256"], item["target"]
        )
        for item in original["declared_inputs"]
    }
    files["inputs/ontology.yaml"] = checked_bytes(
        (source / "work/ontology-attempt-01.yaml").read_bytes(),
        result["ontology_sha256"],
        "ontology",
    )
    files["inputs/baseline-records.json"] = checked_bytes(
        (attempt / "public/export-records.json").read_bytes(),
        result["export_records_sha256"],
        "graph",
    )
    files["inputs/base-capture.json"] = checked_bytes(
        (attempt / "ledger/retained-capture.json").read_bytes(),
        result["capture"]["capture_sha256"],
        "capture",
    )
    files["inputs/population-surface.json"] = surface
    files["inputs/capture-catalog.json"] = canonical(
        {"base-capture.json": result["capture"]["capture_sha256"]}
    )
    files["inputs/coordinates.json"] = canonical(
        {
            "source_id": result["plan"]["source_record_ids"][0],
            "reading_sha256": result["reading_sha256"],
            "capture_id": "capture:paper-v4:meaning-repair-01",
            "plan_id": "plan:paper-v4:meaning-repair-01",
        }
    )
    graph = json.loads(files["inputs/baseline-records.json"])
    targets = {r["id"] for r in graph["entities"] if r["type"] in TYPES}
    inventory(
        graph,
        json.loads(surface),
        json.loads(files["inputs/base-capture.json"]),
        json.loads(files["inputs/selected-reading.json"]),
        targets=targets,
    )
    files["inputs/targets.json"] = canonical(sorted(targets))
    files["inputs/output-format.md"] = (HERE / "meaning-output-format.md").read_bytes()
    return attempt, result, files


def stage(run):
    run = new_private_directory(run, PRIVATE)
    attempt, result, producer = source_files()
    method = json.loads(
        checked_bytes((METHOD / "method.json").read_bytes(), METHOD_ID, "reader")
    )
    verify_materials(METHOD, method["materials"])
    task = (
        (HERE / "meaning-repair-task.md")
        .read_text()
        .replace("prepared task, not yet dispatched", "approved one-proposal task")
        + f"""\n\nYour only output directory is {run}/producer/work.
Read every declared input frame before writing, skill first, complete reading
next, then remaining inputs. List frame counts with:
`{pilot.ROOT}/.venv/bin/python {run}/input_delivery.py --run {run} --phase initial`
For each target and part call that command adding --target TARGET --part N.
Use one frame per tool output, at least 9000 output tokens. Re-read truncation.
The display helper is allowed infrastructure; do not inspect its source.
After all frames, notify the coordinator without waiting, then author.
No structural or semantic return is preauthorized. Stop after your one submission.
"""
    )
    producer["task.md"] = task.encode()
    files = {"producer/" + name: data for name, data in producer.items()}
    files.update(
        {
            "TASK.md": task.encode(),
            "input_delivery.py": (HERE / "input_delivery.py").read_bytes(),
            "producer-input-manifest.json": canonical(
                {
                    "declared_inputs": [
                        {"target": name, "sha256": digest(data)}
                        for name, data in sorted(producer.items())
                    ]
                }
            ),
            "base-history.jsonl": checked_bytes(
                (attempt / "ledger/history.jsonl").read_bytes(),
                "sha256:c02d1a3ca85f74df0fb67e0398c51b0cc4eb9f1da80d88769cd5a483a12e9ddd",
                "ledger",
            ),
            "base-result.json": (attempt / "run-result.json").read_bytes(),
            "before-query.json": checked_bytes(
                (METHOD.parent / "first/query-result.json").read_bytes(),
                "sha256:fbf863e8f86d9902ed42f823b36fe8fbd3be79ee634a0116d0325df62ea3515b",
                "before query",
            ),
            **{"checks/" + name: (HERE / name).read_bytes() for name in CHECKS},
            **{
                "method/" + p.name: p.read_bytes()
                for p in METHOD.iterdir()
                if p.is_file()
            },
        }
    )
    manifest = {
        "schema": SCHEMA,
        "decision": "E-0331",
        "core_commit": events.CORE,
        "producer_model": "gpt-5.6-sol",
        "producer_effort": "ultra",
        "maximum_structural_returns": 0,
        "maximum_semantic_returns": 0,
        "condition": "SOURCE_CONTEXT_AMENDMENT_OF_FRESH_GRAPH",
        "base_result_sha256": digest(files["base-result.json"]),
        "reader_sha256": METHOD_ID,
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(files.items())
        ],
    }
    files["manifest.json"] = canonical(manifest)
    write_new(run, files)
    (run / "producer/work").mkdir()
    preflight(run)
    return manifest


def preflight(run):
    manifest = json.loads((run / "manifest.json").read_bytes())
    if (manifest["schema"], manifest["core_commit"], manifest["reader_sha256"]) != (
        SCHEMA,
        events.CORE,
        METHOD_ID,
    ):
        raise ValueError("wrong repair condition/Core/reader")
    verify_materials(run, manifest["materials"])
    for name in CHECKS:
        checked_bytes(
            (HERE / name).read_bytes(),
            digest((run / "checks" / name).read_bytes()),
            name,
        )
    pilot.verify_runtime(events.CORE)
    expected = json.loads(
        checked_bytes(
            (run / "base-result.json").read_bytes(), events.RESULT_ID, "base result"
        )
    )
    replay = api.KnowledgeChangeHistory.reopen(run / "base-history.jsonl").replay()
    checked_bytes(
        replay.receipt.canonical_bytes,
        expected["replay_receipt_sha256"],
        "base receipt",
    )
    checked_bytes(
        pilot.canonical(replay.graph.export_records()),
        expected["export_records_sha256"],
        "base graph",
    )
    return manifest, replay


def structural_check(run, candidate_path):
    _, replay = preflight(run)
    inputs = run / "producer/inputs"

    def load(name):
        return json.loads((inputs / name).read_bytes())

    candidate = json.loads(candidate_path.read_bytes())
    report = json.loads(candidate_path.with_suffix(".report.json").read_bytes())
    base = replay.graph.export_records()
    targets = set(load("targets.json"))
    check_scope(base, candidate, load("population-surface.json"), targets=targets)
    captures = {
        digest((inputs / "base-capture.json").read_bytes()): (
            inputs / "base-capture.json"
        ).read_bytes()
    }
    coordinates = load("coordinates.json")
    reconciliation.check_reconciliation(
        base,
        candidate,
        report,
        (inputs / "selected-reading.json").read_bytes(),
        captures,
        coordinates["source_id"],
        targets=targets,
    )
    adapted = api.adapt_document_assertions(
        reading_bytes=(inputs / "selected-reading.json").read_bytes(),
        capture_bytes=pilot.canonical(candidate["capture"]),
        capture_id=coordinates["capture_id"],
        plan_id=coordinates["plan_id"],
        contract_identity=replay.partial_contract.identity,
        records=candidate["records"],
        supersessions=candidate["supersessions"],
        contract_view=replay.contract_view,
    )
    profile = api.DomainHistoryProfile.from_data(load("profile-source-assertion.json"))
    compiled = api.compile_population_plan(
        json.loads(adapted.canonical_plan_bytes),
        partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=api.PopulationBaseState.from_replay(replay),
        history_profile=profile,
    )
    return adapted, compiled, profile


def query_view(run, replay):
    """Apply the exact existing reader to a replay, with no source access."""
    surface = json.loads((run / "producer/inputs/population-surface.json").read_bytes())
    for name in ("answers.py", "event_query.py"):
        checked_bytes(
            (HERE / name).read_bytes(),
            digest((run / "method" / name).read_bytes()),
            name,
        )
    queries, _, identity, attempts = repair.frozen_queries(
        run / "method", replay, surface, reader="SubjectGraphReads"
    )
    repair.check_read_guard(attempts)
    native, native_id = pilot.load_native()
    if native_id != identity:
        raise ValueError("read guard changed")
    graph_before = replay.graph.state_digest()
    guard = native._SourceFreeGuard()
    with guard:
        reads = events.GraphReads(replay.graph, surface)
        result = [events.expand(reads, q) for q in queries]
        traces = native.trace_witnesses(
            replay, sorted({key for q in result for key in q["witness_ids"]})
        )
    repair.check_read_guard(guard.attempts)
    if replay.graph.state_digest() != graph_before:
        raise ValueError("query changed the graph")
    return result, traces


def prepare_review(run, candidate_path):
    adapted, compiled, _ = structural_check(run, candidate_path)
    packet = new_private_directory(run / "source-review-01", PRIVATE)
    producer = run / "producer"
    inputs = json.loads((run / "producer-input-manifest.json").read_bytes())
    files = {
        "producer/" + item["target"]: (producer / item["target"]).read_bytes()
        for item in inputs["declared_inputs"]
        if item["target"]
        not in {
            "task.md",
            ".claude/skills/malleus-acolyte/SKILL.md",
            "inputs/population-surface.json",
        }
    }
    files["producer/inputs/proposal-task.md"] = (run / "TASK.md").read_bytes()
    files["producer/inputs/candidate.json"] = candidate_path.read_bytes()
    files["producer/inputs/report.json"] = candidate_path.with_suffix(
        ".report.json"
    ).read_bytes()
    task = (
        (HERE / "meaning-review-task.md").read_text().replace("{PACKET}", str(packet))
    )
    files["producer/task.md"] = task.encode()
    files["TASK.md"] = task.encode()
    files["input_delivery.py"] = (run / "input_delivery.py").read_bytes()
    files["producer-input-manifest.json"] = canonical(
        {
            "declared_inputs": [
                {"target": name.removeprefix("producer/"), "sha256": digest(data)}
                for name, data in sorted(files.items())
                if name.startswith("producer/")
            ]
        }
    )
    manifest = {
        "schema": "malleus.paper-v4.meaning-source-review/v1",
        "run_manifest_sha256": digest((run / "manifest.json").read_bytes()),
        "candidate_sha256": digest(candidate_path.read_bytes()),
        "report_sha256": digest(
            candidate_path.with_suffix(".report.json").read_bytes()
        ),
        "structural_status": str(compiled.status),
        "plan_sha256": digest(adapted.canonical_plan_bytes),
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(files.items())
        ],
    }
    write_new(packet, {**files, "manifest.json": canonical(manifest)})
    return manifest


def authorize_sources(run, candidate_path):
    decision = reconciliation.authorize(run, candidate_path)
    manifest = json.loads((run / "manifest.json").read_bytes())
    producer = verify_delivery(run, "initial")
    reviewer = verify_delivery(run / "source-review-01", "initial")
    if (producer["model"], producer["reasoning_effort"]) != (
        manifest["producer_model"],
        manifest["producer_effort"],
    ):
        raise ValueError("producer differs from the approved model condition")
    if (
        reviewer["thread_id"] == producer["thread_id"]
        or reviewer["thread_id"] != decision["reviewer_thread_id"]
    ):
        raise ValueError("source decision requires its distinct fresh reviewer")
    return {"producer": producer, "reviewer": reviewer}


def execute(run, candidate_path, output, *, transaction_time):
    """Source authorization precedes all new retention and admission."""
    delivery = authorize_sources(run, candidate_path)
    repair.executor_source(Path(__file__), LOADED)
    manifest, baseline = preflight(run)
    adapted, compiled, profile = structural_check(run, candidate_path)
    before, _ = query_view(run, baseline)
    if before != json.loads((run / "before-query.json").read_bytes())["queries"]:
        raise ValueError("before queries do not reproduce")
    target = new_private_directory(output, PRIVATE)
    candidate = json.loads(candidate_path.read_bytes())
    capture_bytes = pilot.canonical(candidate["capture"])
    base_bytes = (run / "base-history.jsonl").read_bytes()
    coordinates = json.loads((run / "producer/inputs/coordinates.json").read_bytes())
    write_new(target, {"executor.py": LOADED, "retained-capture.json": capture_bytes})
    phase = "retention"
    result = {
        "status": "STARTED",
        "transaction_time": transaction_time,
        "candidate_sha256": digest(candidate_path.read_bytes()),
        "core_commit": events.CORE,
    }
    try:
        ledger = target / "ledger/history.jsonl"
        repair.copy_history(run / "base-history.jsonl", ledger, digest(base_bytes))
        actor = "actor:codex:meaning-repair-01"
        command = subprocess.run(
            [
                sys.executable,
                "-m",
                "malleus.compiler_cli",
                "retain",
                "--ledger",
                str(ledger),
                "--evidence",
                coordinates["capture_id"],
                str(target / "retained-capture.json"),
                "application/json",
                "--transaction-time",
                transaction_time,
                "--actor-id",
                actor,
            ],
            capture_output=True,
            text=True,
        )
        if command.returncode:
            raise ValueError(
                "public retention failed: " + command.stdout + command.stderr
            )
        history = api.KnowledgeChangeHistory.reopen(ledger)
        phase = "preparation"
        prepared = api.prepare_population_change(
            history=history,
            plan=json.loads(adapted.canonical_plan_bytes),
            profile=json.loads(profile.canonical_bytes),
            retention_events=api.population_retention_events(
                history=history, compilation=compiled, profile=profile
            ),
            transaction_time=transaction_time,
            actor_id=actor,
        )
        if prepared.change_set is None:
            raise ValueError("scoped amendment produced no change set")
        phase = "admission"
        admitted = api.admit_structural_change(
            history=history,
            preparation=prepared,
            transaction_time=transaction_time,
            actor_id=actor,
        )
        receipt = admitted.receipt.canonical_bytes
        graph = admitted.graph.export_records()
        del admitted, history, prepared
        phase = "replay"
        replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
        repair.verify_replay(
            receipt,
            graph,
            replay.receipt.canonical_bytes,
            replay.graph.export_records(),
            admission_occurred=True,
        )
        repair.check_preservation(
            baseline.graph.export_records(), replay.graph.export_records(), candidate
        )
        repair.check_record_history(
            baseline.record_history, replay.record_history, candidate
        )
        if not ledger.read_bytes().startswith(base_bytes):
            raise ValueError("ledger prefix changed")
        phase = "query"
        ledger_before = ledger.read_bytes()
        queries, traces = query_view(run, replay)
        if ledger.read_bytes() != ledger_before:
            raise ValueError("query changed ledger")
        captures = {
            "base-capture.json": (
                run / "producer/inputs/base-capture.json"
            ).read_bytes(),
            "retained-capture.json": capture_bytes,
        }
        trace = {"records": traces}
        files = {
            "population-plan.json": adapted.canonical_plan_bytes,
            "verified-delivery.json": canonical(delivery),
            "census.json": adapted.canonical_census_bytes,
            "replay-receipt.json": replay.receipt.canonical_bytes,
            "export-records.json": pilot.canonical(replay.graph.export_records()),
            "query-result.json": canonical(
                {
                    "queries": queries,
                    "coverage": "UNREVIEWED",
                    "reader_sha256": METHOD_ID,
                }
            ),
            "query-trace-summary.json": canonical(trace),
            "resolved-trace.json": canonical(
                trace_closure(
                    (run / "producer/inputs/selected-reading.json").read_bytes(),
                    captures,
                    trace,
                )
            ),
        }
        for name, data in files.items():
            with (target / name).open("xb") as stream:
                stream.write(data)
        result.update(
            status="ADMITTED_REPLAYED_UNREVIEWED",
            ledger_head=replay.ledger_head,
            ledger_events=replay.ledger_event_count,
            ledger_prefix_preserved=True,
            exact_delta_preserved=True,
            historical_records_preserved=True,
            graph={
                family: len(rows)
                for family, rows in replay.graph.export_records().items()
            },
            changed_questions=[
                q["question_id"]
                for old, q in zip(before, queries, strict=True)
                if old != q
            ],
            artifacts={name: digest(data) for name, data in files.items()},
        )
    except (ValueError, TypeError, OSError) as error:
        result.update(status="REFUSED_OR_CHECK_FAILED", phase=phase, detail=str(error))
    verify_materials(run, manifest["materials"])
    repair.executor_source(Path(__file__), LOADED)
    with (target / "run-result.json").open("xb") as stream:
        stream.write(canonical(result))
    return result

"""Run a frozen follow-up submission through public Core APIs, then query it."""

import argparse
from datetime import datetime
import json
from pathlib import Path

import malleus.compiler as api

from binding import load_query_program, validate_binding
from followup import HERE, ROOT, checked_bytes, reference_module, verify_materials
import pilot
from review_packet import canonical, digest, new_private_directory

LOADED_EXECUTOR_BYTES = Path(__file__).read_bytes()


def execution_time(value):
    if datetime.fromisoformat(value).tzinfo is None:
        raise ValueError("execution transaction time must include its timezone")
    return value


def population_parts(value):
    if not isinstance(value, dict) or set(value) != {
        "capture",
        "records",
        "supersessions",
    }:
        raise ValueError(
            "population must contain exactly capture, records and supersessions"
        )
    return value


def verify_replay(
    receipt, graph, reopened_receipt, reopened_graph, *, admission_occurred
):
    if receipt != reopened_receipt or graph != reopened_graph:
        raise ValueError("reopened replay differs from pre-close receipt or graph")
    return {
        "replay_matches_preclose": True,
        "admission_occurred": admission_occurred,
    }


def execute(run, population_path, output, *, transaction_time):
    checked_bytes(
        Path(__file__).read_bytes(), digest(LOADED_EXECUTOR_BYTES), "executor"
    )
    clock = execution_time(transaction_time)
    run = run.resolve()
    target = new_private_directory(output, ROOT / "private")
    if not target.is_relative_to(run):
        raise ValueError("attempt must be inside its frozen run directory")
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    pilot.verify_runtime(manifest["core_commit"])
    for path in (run / "frozen-code").glob("*.py"):
        if path.name == "answers.py":
            continue  # Executed from the identified retained bytes below.
        checked_bytes(
            (HERE / path.name).read_bytes(), digest(path.read_bytes()), path.name
        )
    inputs = run / "producer/inputs"
    surface_bytes = (inputs / "population-surface.json").read_bytes()
    question_bytes = (run / "competency-questions.json").read_bytes()
    query_binding_bytes = (run / "query-binding.acceptance.json").read_bytes()
    query_program = load_query_program(
        run / "frozen-code/answers.py",
        json.loads(query_binding_bytes)["query_program_sha256"],
    )
    validate_binding(
        query_binding_bytes,
        surface_bytes,
        question_bytes,
        manifest["core_commit"],
        query_program._source_bytes,
        program=query_program,
    )
    submitted = population_path.read_bytes()
    coordinates = json.loads((inputs / "coordinates.json").read_bytes())
    helpers = reference_module("run.py")
    actor = "actor:codex:" + manifest["run_id"]
    target.mkdir(parents=True)
    (target / "executor.py").write_bytes(LOADED_EXECUTOR_BYTES)
    (target / "submitted-population.json").write_bytes(submitted)
    try:
        population = population_parts(json.loads(submitted))
        sources = {
            locator: (inputs / filename).read_bytes()
            for locator, filename in {
                "paper-v4-project": "ontology.yaml",
                "malleus": "malleus.yaml",
                "linkml:types": "linkml-types.yaml",
                "metrology": "metrology.yaml",
                "chronology": "chronology.yaml",
                "research": "research.yaml",
            }.items()
        }
        compilation = api.compile_linkml_contract(
            root_locator="paper-v4-project", sources=sources
        )
        ledger = target / "ledger/history.jsonl"
        ledger.parent.mkdir()
        history = api.create_structural_history(
            ledger, compilation=compilation, transaction_time=clock, actor_id=actor
        )
        capture_source = pilot.canonical(population["capture"])
        capture_path = target / "retained-capture.json"
        capture_path.write_bytes(capture_source)
        helpers._quiet_cli(
            [
                "retain",
                "--ledger",
                str(ledger),
                "--source",
                coordinates["source_id"],
                coordinates["artifact_id"],
                str(inputs / "selected-reading.json"),
                "application/json",
                "--evidence",
                coordinates["capture_id"],
                str(capture_path),
                "application/json",
                "--transaction-time",
                clock,
                "--actor-id",
                actor,
            ]
        )
        history = api.KnowledgeChangeHistory.reopen(ledger)
        retained = history.replay()
        if retained.partial_contract.identity != manifest["contract_identity"]:
            raise ValueError("created contract differs from acceptance-time binding")
        adapted = api.adapt_document_assertions(
            reading_bytes=(inputs / "selected-reading.json").read_bytes(),
            capture_bytes=capture_source,
            capture_id=coordinates["capture_id"],
            plan_id=coordinates["plan_id"],
            contract_identity=retained.partial_contract.identity,
            records=population["records"],
            supersessions=population["supersessions"],
            contract_view=retained.contract_view,
        )
        plan = json.loads(adapted.canonical_plan_bytes)
        profile = api.DomainHistoryProfile.from_data(
            json.loads((inputs / "profile-source-assertion.json").read_bytes())
        )
        compiled = api.compile_population_plan(
            plan,
            partial_contract=retained.partial_contract,
            contract_view=retained.contract_view,
            base_state=api.PopulationBaseState.from_replay(retained),
            history_profile=profile,
        )
        prepared = api.prepare_population_change(
            history=history,
            plan=plan,
            profile=json.loads(profile.canonical_bytes),
            retention_events=api.population_retention_events(
                history=history, compilation=compiled, profile=profile
            ),
            transaction_time=clock,
            actor_id=actor,
        )
        changed = prepared.change_set is not None
        before = (
            api.admit_structural_change(
                history=history,
                preparation=prepared,
                transaction_time=clock,
                actor_id=actor,
            )
            if changed
            else prepared.retention_replay
        )
        receipt, graph = before.receipt.canonical_bytes, before.graph.export_records()
        del before, history, retained, prepared
        replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
        replay_check = verify_replay(
            receipt,
            graph,
            replay.receipt.canonical_bytes,
            replay.graph.export_records(),
            admission_occurred=changed,
        )
        ledger_digest, graph_digest = (
            digest(ledger.read_bytes()),
            replay.graph.state_digest(),
        )
        questions = pilot.load_questions(question_bytes)
        reads = query_program.GraphReads(replay.graph, json.loads(surface_bytes))
        native, guard_identity = pilot.load_native()
        guard = native._SourceFreeGuard()
        with guard:
            queries = [
                query_program.answer(reads, question["id"]) for question in questions
            ]
            witnesses = sorted(
                {record for query in queries for record in query["witness_ids"]}
            )
            query_traces = native.trace_witnesses(replay, witnesses)
        if (
            ledger_digest != digest(ledger.read_bytes())
            or graph_digest != replay.graph.state_digest()
        ):
            raise ValueError("query changed the graph or ledger")
        query = {
            "schema": "malleus.paper-v4.followup-answers/v1",
            "status": "EXPLORATORY_UNREVIEWED",
            "run_id": manifest["run_id"],
            "core_commit": manifest["core_commit"],
            "execution_mode": "FRESH_FIXED_ONTOLOGY",
            **replay_check,
            "ledger_bytes_unchanged": True,
            "graph_state_digest": graph_digest,
            "inputs": {
                "query_binding_sha256": digest(query_binding_bytes),
                "question_set_sha256": digest(question_bytes),
                "query_program_sha256": digest(query_program._source_bytes),
                "runner_sha256": digest(LOADED_EXECUTOR_BYTES),
                "binding_program_sha256": digest((HERE / "binding.py").read_bytes()),
                "population_surface_sha256": digest(surface_bytes),
                "read_guard_sha256": guard_identity,
                "ledger_head": replay.ledger_head,
                "replay_receipt_sha256": digest(replay.receipt.canonical_bytes),
            },
            "forbidden_attempts": guard.attempts,
            "queries": queries,
        }
        artifacts = {
            "population-plan.json": adapted.canonical_plan_bytes,
            "census.json": adapted.canonical_census_bytes,
            "replay-receipt.json": replay.receipt.canonical_bytes,
            "export-records.json": pilot.canonical(replay.graph.export_records()),
            "trace-summary.json": canonical(
                {
                    "records": [
                        helpers._trace_record(replay, record)
                        for record in sorted(replay.record_history)
                    ]
                }
            ),
            "query-result.json": canonical(query),
            "query-trace-summary.json": canonical({"records": query_traces}),
        }
        for name, value in artifacts.items():
            (target / name).write_bytes(value)
        result = {
            "schema": "malleus.paper-v4.followup-result/v1",
            "run_id": manifest["run_id"],
            "status": "ADMITTED_AND_REPLAYED" if changed else "NO_DOMAIN_CHANGE",
            "core_commit": manifest["core_commit"],
            "transaction_time": clock,
            "submitted_population_sha256": digest(submitted),
            "query_binding_sha256": digest(query_binding_bytes),
            "source_closure_sha256": manifest["source_closure_sha256"],
            "ontology_sha256": manifest["ontology_sha256"],
            "reading_sha256": manifest["reading_sha256"],
            "ledger_head": replay.ledger_head,
            "ledger_event_count": replay.ledger_event_count,
            "replay_receipt_sha256": digest(replay.receipt.canonical_bytes),
            "export_records_sha256": digest(artifacts["export-records.json"]),
            "query_result_sha256": digest(artifacts["query-result.json"]),
            "graph": {
                family: len(rows)
                for family, rows in replay.graph.export_records().items()
            },
            "artifacts": {name: digest(value) for name, value in artifacts.items()},
            **replay_check,
            "forbidden_attempts": guard.attempts,
        }
    except (OSError, TypeError, ValueError) as error:
        result = {
            "status": "REFUSED",
            "run_id": manifest["run_id"],
            "core_commit": manifest["core_commit"],
            "transaction_time": clock,
            "submitted_population_sha256": digest(submitted),
            "cause_chain": reference_module(
                "compile_ontology_candidate.py"
            )._cause_chain(error),
        }
    checked_bytes(
        Path(__file__).read_bytes(), digest(LOADED_EXECUTOR_BYTES), "executor"
    )
    (target / "run-result.json").write_bytes(canonical(result))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--population", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--transaction-time", required=True)
    args = parser.parse_args()
    result = execute(
        args.run, args.population, args.output, transaction_time=args.transaction_time
    )
    print(canonical(result).decode())
    raise SystemExit(2 if result["status"] == "REFUSED" else 0)

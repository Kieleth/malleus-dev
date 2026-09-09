"""Execute the retained public runner, then the prebound thirty graph queries."""

import argparse
import importlib.util
import json
from pathlib import Path
import sys

import malleus.compiler as api

from binding import load_query_program, validate_binding
from followup import checked_bytes, reference_module, verify_materials
import pilot
from review_packet import canonical, digest, new_private_directory


CODE = Path(__file__).read_bytes()


def execute(run, population, output, transaction_time):
    run = run.resolve()
    target = new_private_directory(output, pilot.ROOT / "private")
    if not target.is_relative_to(run):
        raise ValueError("attempt must be inside its run")
    manifest = json.loads((run / "manifest.json").read_bytes())
    if manifest["producer_condition"] != "FRESH_END_TO_END":
        raise ValueError("executor requires the full end-to-end condition")
    if manifest["ontology_agent_id"] != manifest["population_agent_id"]:
        raise ValueError("end-to-end producer session changed")
    verify_materials(run, manifest["materials"])
    pilot.verify_runtime(manifest["core_commit"])
    initial = json.loads((run / "producer-input-manifest.json").read_bytes())
    prospective = initial["schema"] == "malleus.paper-v4.fresh-comparison-inputs/v1"
    if prospective:
        from fresh_comparison import verify_observed, check_execution_attempt
        from query_capacity import audit

        check_execution_attempt(run, target, population, transaction_time)
        verify_observed(run, "initial")
        verify_observed(run, "accepted")
        if manifest["query_reader"] != "SubjectGraphReads":
            raise ValueError("prospective reader differs")
        capacity = checked_bytes(
            (run / "query-capacity.json").read_bytes(),
            manifest["query_capacity_sha256"],
            "capacity audit",
        )
        if capacity != canonical(
            audit(
                json.loads(
                    (run / "producer/accepted/population-surface.json").read_bytes()
                ),
                (run / "method/answers.py").read_bytes(),
                (run / "method/questions.json").read_bytes(),
            )
        ):
            raise ValueError("schema capacity differs from pre-population binding")
    if initial["schema"] == "malleus.paper-v4.current-adoption-inputs/v1":
        from current_adoption import verify_observed

        verify_observed(run, "initial")
        verify_observed(run, "accepted")
    for item in initial["declared_inputs"]:
        checked_bytes(
            (run / "producer" / item["target"]).read_bytes(),
            item["sha256"],
            item["target"],
        )
    ontology = run / manifest["ontology_path"]
    checked_bytes(
        ontology.read_bytes(), manifest["ontology_sha256"], "accepted ontology"
    )
    reference = reference_module("run.py", base_run="run-21")
    runner_bytes = (
        Path(reference.__file__)
        .read_bytes()
        .replace(b"run-21", manifest["run_id"].encode())
    )
    target.mkdir(parents=True)
    runner_path = target / "public-runner.py"
    runner_path.write_bytes(runner_bytes)
    (target / "e2e_execute.py").write_bytes(CODE)
    (target / "submitted-population.json").write_bytes(population.read_bytes())
    spec = importlib.util.spec_from_file_location("e2e_public_runner", runner_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    inputs = run / "producer/inputs"
    coordinates = manifest["interface_coordinates"]
    sources = [["paper-v4-project", str(ontology)]] + [
        [key, str(inputs / name)]
        for key, name in {
            "malleus": "malleus.yaml",
            "linkml:types": "linkml-types.yaml",
            "metrology": "metrology.yaml",
            "chronology": "chronology.yaml",
            "research": "research.yaml",
        }.items()
    ]
    for key, path in sources:
        checked_bytes(
            Path(path).read_bytes(), manifest["source_closure_sha256"][key], key
        )
    ledger = target / "ledger/history.jsonl"
    try:
        public = helper.execute(
            argparse.Namespace(
                root="paper-v4-project",
                source=sources,
                reading=str(inputs / "selected-reading.json"),
                population=str(target / "submitted-population.json"),
                **coordinates,
                artifact_id="artifact:" + manifest["run_id"] + ":reading",
                ledger=str(ledger),
                results=str(target / "public"),
                transaction_time=transaction_time,
                actor_id="actor:codex:" + manifest["run_id"],
            )
        )
    except (OSError, TypeError, ValueError) as error:
        refusal = {
            "status": "REFUSED",
            "run_id": manifest["run_id"],
            "cause_chain": reference_module(
                "compile_ontology_candidate.py", base_run="run-21"
            )._cause_chain(error),
        }
        (target / "run-result.json").write_bytes(canonical(refusal))
        return refusal
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    if digest(replay.receipt.canonical_bytes) != public["replay_receipt_sha256"]:
        raise ValueError("query reopen differs from admitted/replayed receipt")
    if (
        digest(pilot.canonical(replay.graph.export_records()))
        != public["export_records_sha256"]
    ):
        raise ValueError("query reopen differs from admitted/replayed graph")
    surface_bytes = (run / "producer/accepted/population-surface.json").read_bytes()
    questions = (run / "competency-questions.json").read_bytes()
    binding = (run / "query-binding.acceptance.json").read_bytes()
    program = load_query_program(
        run / "frozen-code/answers.py", manifest["query_program_sha256"]
    )
    validate_binding(
        binding,
        surface_bytes,
        questions,
        manifest["core_commit"],
        program._source_bytes,
        program=program,
    )
    reads = program.GraphReads(replay.graph, json.loads(surface_bytes))
    native, guard_identity = pilot.load_native()
    before, state = digest(ledger.read_bytes()), replay.graph.state_digest()
    guard = native._SourceFreeGuard()
    if prospective:
        from repair import frozen_queries, check_read_guard

        queries, traces, guard_identity, attempts = frozen_queries(
            run / "frozen-code",
            replay,
            json.loads(surface_bytes),
            reader="SubjectGraphReads",
            questions_path=run / "competency-questions.json",
        )
        check_read_guard(attempts)
    else:
        with guard:
            queries = [
                program.answer(reads, q["id"]) for q in pilot.load_questions(questions)
            ]
            witness_ids = sorted(
                {key for query in queries for key in query["witness_ids"]}
            )
            traces = native.trace_witnesses(replay, witness_ids)
        attempts = guard.attempts
    if before != digest(ledger.read_bytes()) or state != replay.graph.state_digest():
        raise ValueError("query modified the accepted history or graph")
    query = {
        "schema": "malleus.paper-v4.followup-answers/v1",
        "run_id": manifest["run_id"],
        "status": "EXPLORATORY_UNREVIEWED",
        "core_commit": manifest["core_commit"],
        "execution_mode": "FRESH_END_TO_END",
        "replay_matches_preclose": True,
        "admission_occurred": public["status"] == "ADMITTED_AND_REPLAYED",
        "ledger_bytes_unchanged": True,
        "forbidden_attempts": attempts,
        "inputs": {
            "query_binding_sha256": digest(binding),
            "question_set_sha256": digest(questions),
            "query_program_sha256": digest(program._source_bytes),
            "runner_sha256": digest(CODE),
            "binding_program_sha256": digest(
                (run / "frozen-code/binding.py").read_bytes()
            ),
            "population_surface_sha256": digest(surface_bytes),
            "read_guard_sha256": guard_identity,
            "ledger_head": replay.ledger_head,
            "replay_receipt_sha256": public["replay_receipt_sha256"],
        },
        "queries": queries,
    }
    if prospective:
        query["inputs"].update(
            query_capacity_sha256=digest(capacity),
            reader_class="SubjectGraphReads",
            subject_reader_sha256=digest(
                (run / "frozen-code/subject_answers.py").read_bytes()
            ),
        )
    (target / "query-result.json").write_bytes(canonical(query))
    (target / "query-trace-summary.json").write_bytes(canonical({"records": traces}))
    result = {
        **public,
        "schema": "malleus.paper-v4.end-to-end-result/v1",
        "core_commit": manifest["core_commit"],
        "execution_mode": "FRESH_END_TO_END",
        "query_binding_sha256": digest(binding),
        "query_result_sha256": digest(canonical(query)),
        "public_runner_sha256": digest(runner_bytes),
        "query_runner_sha256": digest(CODE),
        "forbidden_attempts": attempts,
    }
    (target / "run-result.json").write_bytes(canonical(result))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--population", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--transaction-time", required=True)
    args = parser.parse_args()
    result = execute(args.run, args.population, args.output, args.transaction_time)
    print(canonical(result).decode())
    sys.exit(2 if result["status"] == "REFUSED" else 0)

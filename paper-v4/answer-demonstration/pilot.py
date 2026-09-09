"""Read two historical ledgers through their pinned Core. Private outputs only."""

import argparse
from collections import Counter
from hashlib import sha1, sha256
import importlib.util
import json
from pathlib import Path
import re
import subprocess

import malleus.compiler as api

from answers import GraphReads, PROGRAMS, answer
from binding import QUESTION_IDENTITY


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE = "c95dba7b86bb61487bda9a52458e1ea47cce20ab"
PAPER_BASELINE = "8233b771a4f6ae8d248274fdda0185920f99421b"


def canonical(value):
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()


def digest(data):
    return "sha256:" + sha256(data).hexdigest()


def program_sources():
    return {
        name: (HERE / name).read_bytes()
        for name in ("answers.py", "binding.py", "pilot.py")
    }


def verify_runtime(core_commit=CORE):
    """Compare the entire installed source package with the named Git tree."""
    if not re.fullmatch(r"[0-9a-f]{40}", core_commit):
        raise ValueError("Core runtime requires a full commit identity")
    package = Path(api.__file__).resolve().parent
    listing = subprocess.run(
        ["git", "ls-tree", "-r", core_commit, "src/malleus"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    for line in listing.splitlines():
        entry, name = line.split("\t")
        _, kind, expected = entry.split()
        if kind != "blob":
            raise ValueError(f"unexpected Core tree entry: {name}")
        path = package / Path(name).relative_to("src/malleus")
        data = path.read_bytes()
        actual = sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        if actual != expected:
            raise ValueError(f"Core runtime differs from {core_commit}: {path}")
    return str(package)


def load_native():
    # Reuse the existing tested Python-level read guard and provenance join.
    path = ROOT / "paper-v4/experiment-v4/run-20/native_query.py"
    source = path.read_bytes()
    expected = subprocess.run(
        [
            "git",
            "show",
            f"{PAPER_BASELINE}:paper-v4/experiment-v4/run-20/native_query.py",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    if source != expected:
        raise ValueError(
            "historical query guard differs from the fixed reference bytes"
        )
    spec = importlib.util.spec_from_file_location("answer_pilot_native", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, digest(source)


def output_directory(path):
    resolved = path.resolve()
    if not resolved.is_relative_to((ROOT / "private").resolve()):
        raise ValueError("source-bearing pilot outputs must remain under private/")
    if resolved.exists():
        raise ValueError(f"refusing to overwrite pilot output: {resolved}")
    return resolved


def load_questions(source):
    if digest(source) != QUESTION_IDENTITY:
        raise ValueError("frozen question bytes differ from E-0206")
    questions = json.loads(source)["questions"]
    if {q["id"] for q in questions} != set(PROGRAMS) or len(questions) != len(PROGRAMS):
        raise ValueError("query programs must cover each frozen question exactly once")
    return questions


def execute(run_id, output):
    if run_id not in {"run-20", "run-21"}:
        raise ValueError("this pilot consumes only frozen run-20 and run-21")
    target = output_directory(output)
    verify_runtime()
    native, guard_digest = load_native()
    experiment = ROOT / "paper-v4/experiment-v4" / run_id
    expected = json.loads((experiment / "results/run-result.json").read_bytes())
    surface_bytes = (experiment / "ontology-run/population-surface.json").read_bytes()
    surface = json.loads(surface_bytes)
    if surface["validated_fact_set_sha256"] != expected["validated_fact_set_sha256"]:
        raise ValueError("population surface does not bind the selected ontology")
    questions_path = ROOT / "paper-v4/experiment-v4/competency-questions-v3.json"
    questions_bytes = questions_path.read_bytes()
    questions = load_questions(questions_bytes)
    sources = program_sources()
    ledger = ROOT / f"private/paper-v4-v4-{run_id}/ledger/history.jsonl"
    before = digest(ledger.read_bytes())
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    if digest(replay.receipt.canonical_bytes) != expected["replay_receipt_sha256"]:
        raise ValueError("reopen receipt differs from frozen run")
    if (
        digest(canonical(replay.graph.export_records()))
        != expected["export_records_sha256"]
    ):
        raise ValueError("replayed graph differs from frozen run")
    reads = GraphReads(replay.graph, surface)
    graph_before = replay.graph.state_digest()
    guard = native._SourceFreeGuard()
    with guard:
        queries = [answer(reads, q["id"]) for q in questions]
        witness_ids = sorted({w for query in queries for w in query["witness_ids"]})
        traces = native.trace_witnesses(replay, witness_ids)
    if (
        replay.graph.state_digest() != graph_before
        or digest(ledger.read_bytes()) != before
    ):
        raise ValueError("read-only query changed graph or ledger")
    result = {
        "status": "EXPLORATORY_UNREVIEWED",
        "run_id": run_id,
        "core_commit": CORE,
        "inputs": {
            "question_set_sha256": digest(questions_bytes),
            "query_program_sha256": digest(sources["answers.py"]),
            "runner_sha256": digest(sources["pilot.py"]),
            "binding_program_sha256": digest(sources["binding.py"]),
            "population_surface_sha256": digest(surface_bytes),
            "read_guard_sha256": guard_digest,
            "ledger_head": replay.ledger_head,
            "replay_receipt_sha256": expected["replay_receipt_sha256"],
        },
        "historical_replay_matches": True,
        "ledger_bytes_unchanged": True,
        "graph_state_digest": graph_before,
        "forbidden_attempts": guard.attempts,
        "queries": queries,
    }
    # Each run gets a new directory. No historical file is opened for writing.
    target.mkdir(parents=True)
    for name, source in sources.items():
        (target / name).write_bytes(source)
    (target / "query-result.json").write_bytes(canonical(result))
    (target / "trace-summary.json").write_bytes(canonical({"records": traces}))
    summary = {
        "run_id": run_id,
        "status": result["status"],
        "questions": len(queries),
        "outcomes": dict(Counter(q["outcome"] for q in queries)),
        "witnesses": len(witness_ids),
        "forbidden_attempts": guard.attempts,
        "rows_by_question": {q["question_id"]: len(q["rows"]) for q in queries},
        "paths_by_question": {q["question_id"]: len(q["paths"]) for q in queries},
        "query_result_sha256": digest(canonical(result)),
        "ledger_bytes_unchanged": True,
        "historical_replay_matches": True,
    }
    (target / "summary.json").write_bytes(canonical(summary))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, choices=("run-20", "run-21"))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(execute(args.run, args.output), indent=2))


if __name__ == "__main__":
    main()

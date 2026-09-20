"""Execute the frozen contrast with the existing public runner and reader."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PAIR = ROOT / "private/paper-v4-relationship-contrast-01"


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode()


def digest(data):
    return "sha256:" + sha256(data).hexdigest()


def checked_method(item):
    source = (ROOT / item["path"]).read_bytes()
    if digest(source).removeprefix("sha256:") != item["sha256"].removeprefix("sha256:"):
        raise ValueError(f"method identity differs: {item['path']}")
    return source


def check_binding(binding, acceptance):
    actual = digest(canonical(binding["queries"]))
    if actual != binding["cases_sha256"] or actual != acceptance["query_cases_sha256"]:
        raise ValueError("pre-population binding changed")


def submission(snapshot):
    source = snapshot.read_bytes()
    if source != (snapshot.parent / "document-population.json").read_bytes():
        raise ValueError("submitted snapshot and live proposal differ")
    return source


def label_runner(source, run_id):
    if not run_id.startswith("sol-relationship-contrast-01-"):
        raise ValueError("new contrast identity required")
    if b"run-26" not in source:
        raise ValueError("reference runner label absent")
    return source.replace(b"run-26", run_id.encode())


def reserve_attempt(run, number):
    if number not in (1, 2, 3):
        raise ValueError("at most two structural returns after first submission")
    target = run / "attempts" / f"attempt-{number:02d}"
    target.mkdir(parents=True, exist_ok=False)
    return target


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value


def execute(arm, number):
    if arm not in ("a", "b"):
        raise ValueError("choose one frozen arm")
    run = PAIR / arm
    measured = json.loads((HERE / "relationship-measurement.json").read_bytes())
    methods = {
        key: checked_method(value)
        for key, value in measured.items()
        if isinstance(value, dict) and "path" in value
    }
    contrast = module(HERE / "relationship_contrast.py", "contrast_inputs")
    packets = [
        json.loads((PAIR / key / "producer-input-manifest.json").read_bytes())
        for key in ("a", "b")
    ]
    contrast.check_pair(
        *[
            {
                item["target"]: (PAIR / key / "producer" / item["target"]).read_bytes()
                for item in packet["declared_inputs"]
            }
            for key, packet in zip(("a", "b"), packets, strict=True)
        ]
    )
    packet = packets[("a", "b").index(arm)]
    for filename, field in (
        ("task.md", "task_sha256"),
        ("input_delivery.py", "delivery_helper_sha256"),
    ):
        if digest((run / filename).read_bytes()) != packet[field]:
            raise ValueError(f"producer interface identity differs: {filename}")
    sys.path.insert(0, str(ROOT / "paper-v4/answer-demonstration"))
    import input_delivery
    import pilot

    pilot.verify_runtime(measured["core"])
    delivery = [
        input_delivery.verify_delivery(run, phase) for phase in ("initial", "accepted")
    ]
    acceptance = json.loads((run / "ontology-acceptance.json").read_bytes())
    if acceptance["ontology_agent_id"] != acceptance["population_agent_id"]:
        raise ValueError("producer session changed between stages")
    ontology = (
        run
        / "producer/work"
        / f"ontology-attempt-{acceptance['ontology_attempt']:02d}.yaml"
    )
    if digest(ontology.read_bytes()) != acceptance["ontology_sha256"]:
        raise ValueError("accepted ontology identity differs")
    if (
        digest((run / "producer/accepted/population-surface.json").read_bytes())
        != acceptance["population_surface_sha256"]
    ):
        raise ValueError("accepted population surface identity differs")
    binding = json.loads((run / "query-binding.acceptance.json").read_bytes())
    check_binding(binding, acceptance)
    snapshot = run / "producer/work" / f"population-attempt-{number:02d}.json"
    population = submission(snapshot)
    target = reserve_attempt(run, number)
    (target / "submitted-population.json").write_bytes(population)
    runner = label_runner(methods["public_execution_reference"], packet["run_id"])
    (target / "public-runner.py").write_bytes(runner)
    timestamp = datetime.now(timezone.utc).isoformat()
    (target / "execution-inputs.json").write_bytes(
        canonical(
            {
                "run_id": packet["run_id"],
                "attempt": number,
                "population_sha256": digest(population),
                "core": measured["core"],
                "method": measured,
                "runner_sha256": digest(runner),
                "executor_sha256": digest(Path(__file__).read_bytes()),
                "ontology_acceptance_sha256": digest(
                    (run / "ontology-acceptance.json").read_bytes()
                ),
                "binding_acceptance_sha256": digest(
                    (run / "query-binding.acceptance.json").read_bytes()
                ),
                "delivery": delivery,
                "transaction_time": timestamp,
            }
        )
    )
    helper = module(target / "public-runner.py", "contrast_public_runner")
    inputs = run / "producer/inputs"
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
    ledger = target / "ledger/history.jsonl"
    try:
        result = helper.execute(
            argparse.Namespace(
                root="paper-v4-project",
                source=sources,
                reading=str(inputs / "selected-reading.json"),
                population=str(target / "submitted-population.json"),
                **packet["interface_coordinates"],
                artifact_id=f"artifact:{packet['run_id']}:reading",
                ledger=str(ledger),
                results=str(target / "public"),
                transaction_time=timestamp,
                actor_id=f"actor:codex:{packet['run_id']}",
            )
        )
    except (ValueError, TypeError) as error:
        compiler = module(
            ROOT / measured["ontology_compiler"]["path"], "contrast_diagnostic"
        )
        refusal = {
            "status": "REFUSED",
            "attempt": number,
            "cause_chain": compiler._cause_chain(error),
        }
        (target / "diagnostic.json").write_bytes(canonical(refusal))
        return refusal
    binding["bound_after_replay_receipt_sha256"] = result["replay_receipt_sha256"]
    check_binding(binding, acceptance)
    binding_path = target / "query-binding.json"
    binding_path.write_bytes(canonical(binding))
    reader = module(ROOT / measured["reader"]["path"], "contrast_native_reader")
    before = digest(ledger.read_bytes())
    query = reader.execute(
        argparse.Namespace(
            ledger=str(ledger), binding=str(binding_path), results=str(target / "query")
        )
    )
    repeated = reader.execute(
        argparse.Namespace(
            ledger=str(ledger),
            binding=str(binding_path),
            results=str(target / "query-repeat"),
        )
    )
    if query != repeated or before != digest(ledger.read_bytes()):
        raise ValueError("repeated query or history preservation differs")
    if query["inputs"]["replay_receipt_sha256"] != result["replay_receipt_sha256"]:
        raise ValueError("query replay receipt differs from admission")
    if any(query["forbidden_attempts"].values()):
        raise ValueError("query attempted prohibited access")
    outcome = {
        "status": "ADMITTED_REPLAYED_QUERIED_UNREVIEWED",
        "attempt": number,
        "ledger_sha256": before,
        "graph_sha256": result["export_records_sha256"],
        "query_sha256": digest((target / "query/query-result.json").read_bytes()),
        "queries": len(query["queries"]),
        "repeated_queries_equal": True,
        "ledger_unchanged_by_queries": True,
    }
    (target / "execution-result.json").write_bytes(canonical(outcome))
    return outcome


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("arm", choices=("a", "b"))
    parser.add_argument("attempt", type=int)
    args = parser.parse_args()
    print(json.dumps(execute(args.arm, args.attempt), indent=2))

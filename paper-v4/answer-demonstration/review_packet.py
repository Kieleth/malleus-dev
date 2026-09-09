"""Prepare private evidence packets for retrospective review, without grading."""

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL_IDENTITY = (
    "sha256:17b5744a71a1e6a9ab1985f43b3e28d4d683f2d7d369e7decdb375171c2edc21"
)


def canonical(value):
    return (
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, allow_nan=False, indent=2
        ).encode()
        + b"\n"
    )


def digest(source):
    return "sha256:" + sha256(source).hexdigest()


def checked_result(source, result_identity, run):
    if digest(source) != result_identity:
        raise ValueError("selected query result identity differs")
    result = json.loads(source)
    if result["run_id"] != run:
        raise ValueError("selected query result run differs")
    return result


def vocabulary_sources(closure, paths, ontology_identity):
    """Retain every accepted definition, not just projected enum tokens."""
    if not closure or ontology_identity not in closure.values():
        raise ValueError("vocabulary closure omits the accepted ontology")
    available = {}
    for path in paths:
        source = path.read_bytes()
        available[digest(source)] = source
    missing = sorted(set(closure.values()) - set(available))
    if missing:
        raise ValueError(f"missing exact vocabulary bytes: {missing}")
    sources = {}
    entries = []
    for name, identity in sorted(closure.items()):
        filename = "vocabulary-" + identity.removeprefix("sha256:") + ".yaml"
        sources[filename] = available[identity]
        entries.append({"source_id": name, "path": filename, "sha256": identity})
    sources["vocabulary-closure.json"] = canonical(
        {"accepted_ontology_sha256": ontology_identity, "sources": entries}
    )
    return sources


def new_private_directory(path, private):
    path = path.resolve()
    if not path.is_relative_to(private.resolve()):
        raise ValueError("review evidence must remain private")
    if path.exists():
        raise ValueError(f"refusing to overwrite review packet: {path}")
    return path


def central_key(row):
    keys = {
        "ENTITY": {"record_id"},
        "SUBJECT": {"record_id", "subject_id"},
        "RELATION": {"relation_id", "source_id", "target_id"},
    }[row["kind"]]
    if row["kind"] == "RELATION":
        for role in ("source", "target"):
            context, identity = role + "_subject", role + "_subject_id"
            if context in row:
                if (
                    not isinstance(row[context], dict)
                    or identity not in row["witness"]
                    or "subject" not in row[role]
                    or row[role]["subject"] != row["witness"][identity]
                ):
                    raise ValueError("endpoint subject context is unbound")
                keys.add(identity)
    if set(row["witness"]) != keys:
        raise ValueError("required witness identity fields differ")
    return row["witness"]["relation_id" if row["kind"] == "RELATION" else "record_id"]


def docket(questions, result, trace):
    ids = [q["id"] for q in questions["questions"]]
    if len(set(ids)) != len(ids) or ids != [
        q["question_id"] for q in result["queries"]
    ]:
        raise ValueError("question order or closure differs")
    traces = {t["record_id"]: t for t in trace["records"]}
    if len(traces) != len(trace["records"]):
        raise ValueError("duplicate trace identity")
    witnesses, contexts, items = {}, set(), []
    for question, query in zip(questions["questions"], result["queries"], strict=True):
        items.append(
            {
                "question_id": question["id"],
                "question": question["question"],
                "required_semantics": deepcopy(question["required_semantics"]),
                "rows": deepcopy(query["rows"]),
            }
        )
        seen = set()
        for index, row in enumerate(query["rows"]):
            key = central_key(row)
            if key in seen:
                raise ValueError(
                    f"duplicate central witness within {question['id']}: {key}"
                )
            seen.add(key)
            contexts.update(row["witness"].values())
            if key not in witnesses:
                witnesses[key] = {
                    "witness_key": key,
                    "occurrences": [],
                    "projections": [],
                }
            item = witnesses[key]
            item["occurrences"].append(
                {"question_id": question["id"], "row_index": index}
            )
            if row not in item["projections"]:
                item["projections"].append(deepcopy(row))
    if contexts - set(traces):
        raise ValueError(f"missing trace: {sorted(contexts - set(traces))}")
    return {
        "schema": "malleus.paper-v4.review-docket/v1",
        "status": "UNJUDGED",
        "questions": items,
        "witnesses": [witnesses[k] for k in sorted(witnesses)],
        "distinct_central_witnesses": len(witnesses),
        "traced_records_including_context": len(contexts),
    }


def verify_trace_materials(reading_source, capture_source, trace):
    reading, capture = json.loads(reading_source), json.loads(capture_source)
    blocks = {b["id"]: b for p in reading["pages"] for b in p["blocks"]}
    assertions = {a["id"]: a for a in capture["assertions"]}
    if len(blocks) != reading["block_count"] or len(assertions) != len(
        capture["assertions"]
    ):
        raise ValueError("duplicate or missing source/capture identity")
    for record in trace["records"]:
        if digest(reading_source) not in record["sources"].values():
            raise ValueError(f"unbound reading for {record['record_id']}")
        if digest(capture_source) not in record["evidence"].values():
            raise ValueError(f"unbound capture for {record['record_id']}")
        for derivation in record["derivations"]:
            assertion = assertions[derivation["locator"]]
            mapping = {"record_id": record["record_id"], "path": derivation["path"]}
            if mapping not in assertion["formalized_by"]:
                raise ValueError(f"trace path not formalized for {record['record_id']}")
            # The document-capture contract matches spans after whitespace
            # collapse. Keep both retained byte strings unchanged; this checks
            # their location, not source truth or a verbatim-byte equality claim.
            statement = " ".join(assertion["statement"].split())
            block = " ".join(blocks[assertion["block"]]["text"].split())
            if statement not in block:
                raise ValueError(
                    "assertion is not exact selected text after whitespace collapse: "
                    f"{assertion['id']}"
                )


def prepare(run, output, *, pilot, result_identity):
    target = new_private_directory(output, ROOT / "private")
    experiment = ROOT / f"paper-v4/experiment-v4/{run}"
    paths = {
        "selected-reading.json": ROOT
        / "private/paper-v4-text-layer/selected-reading.json",
        "retained-capture.json": ROOT
        / f"private/paper-v4-v4-{run}/ledger/retained-capture.json",
        "competency-questions.json": ROOT
        / "paper-v4/experiment-v4/competency-questions-v3.json",
        "query-result.json": pilot / "query-result.json",
        "query-trace-summary.json": pilot / "trace-summary.json",
        "population-trace.json": experiment / "results/trace-summary.json",
        "population-surface.json": experiment / "ontology-run/population-surface.json",
        "answers.py": pilot / "answers.py",
        "pilot.py": pilot / "pilot.py",
        "binding.py": pilot / "binding.py",
        "review-protocol-v3.json": ROOT
        / "paper-v4/evaluation-v4/review-protocol-v3.json",
        "review.py": ROOT / "paper-v4/evaluation-v4/review.py",
        "review-extension.md": HERE / "REVIEW-EXTENSION.md",
    }
    sources = {name: path.read_bytes() for name, path in paths.items()}
    result = checked_result(sources["query-result.json"], result_identity, run)
    if digest(sources["review-protocol-v3.json"]) != PROTOCOL_IDENTITY:
        raise ValueError("frozen review protocol differs")
    questions = json.loads(sources["competency-questions.json"])
    trace = json.loads(sources["query-trace-summary.json"])
    expected = json.loads((experiment / "results/run-result.json").read_bytes())
    for key in ("ledger_head", "replay_receipt_sha256"):
        if result["inputs"][key] != expected[key]:
            raise ValueError(f"historical run identity differs: {key}")
    for name, key in (
        ("answers.py", "query_program_sha256"),
        ("pilot.py", "runner_sha256"),
        ("binding.py", "binding_program_sha256"),
        ("population-surface.json", "population_surface_sha256"),
        ("competency-questions.json", "question_set_sha256"),
    ):
        if digest(sources[name]) != result["inputs"][key]:
            raise ValueError(f"pilot input differs: {name}")
    if digest(sources["population-trace.json"]) != expected["trace_summary_sha256"]:
        raise ValueError("historical population trace differs")
    verify_trace_materials(
        sources["selected-reading.json"], sources["retained-capture.json"], trace
    )
    index = docket(questions, result, trace)
    sources["review-docket.json"] = canonical(index)
    # This is preparation, not the v3 input manifest or a fabricated completed record.
    manifest = {
        "schema": "malleus.paper-v4.review-preparation/v1",
        "status": "PREPARED_NOT_DISPATCHED",
        "run_id": run,
        "experiment_kind": "RETROSPECTIVE_SELECTIVE_QUERY",
        "core_commit": result["core_commit"],
        "accepted_ontology_sha256": expected["ontology_sha256"],
        "ledger_head": result["inputs"]["ledger_head"],
        "replay_receipt_sha256": result["inputs"]["replay_receipt_sha256"],
        "rows_per_question": {
            q["question_id"]: len(q["rows"]) for q in index["questions"]
        },
        "distinct_central_witnesses": index["distinct_central_witnesses"],
        "traced_records_including_context": index["traced_records_including_context"],
        "materials": [
            {"path": name, "sha256": digest(source)} for name, source in sources.items()
        ],
        "pending": ["INDEPENDENT_REVIEW"],
        "human_ratification": "PENDING",
    }
    target.mkdir(parents=True)
    for name, source in sources.items():
        (target / name).write_bytes(source)
    (target / "preparation.json").write_bytes(canonical(manifest))
    return {
        k: manifest[k]
        for k in (
            "run_id",
            "status",
            "rows_per_question",
            "distinct_central_witnesses",
            "traced_records_including_context",
            "pending",
        )
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", choices=("run-20", "run-21"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pilot", type=Path, required=True)
    parser.add_argument("--result-identity", required=True)
    args = parser.parse_args()
    print(
        canonical(
            prepare(
                args.run,
                args.output,
                pilot=args.pilot,
                result_identity=args.result_identity,
            )
        ).decode()
    )

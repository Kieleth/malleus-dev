"""Bind the approved retrospective review to exact, unmodified pilot outputs."""

import argparse
import json
from pathlib import Path

from review_packet import (
    HERE,
    ROOT,
    canonical,
    digest,
    new_private_directory,
    vocabulary_sources,
)
from selective_review import (
    MANIFEST_SCHEMA,
    RECORD_SCHEMA,
    load_base,
    protocol_bytes,
    replay_mode,
    selective_witnesses,
)


def freeze(run, output, *, preparation, review_id):
    target = new_private_directory(output, ROOT / "private")
    prepared = json.loads((preparation / "preparation.json").read_bytes())
    if prepared["run_id"] != run:
        raise ValueError("preparation belongs to a different run")
    if not isinstance(review_id, str) or not review_id.strip():
        raise ValueError("review identity is required")
    sources = {}
    for item in prepared["materials"]:
        source = (preparation / item["path"]).read_bytes()
        if digest(source) != item["sha256"]:
            raise ValueError(f"prepared input drift: {item['path']}")
        sources[item["path"]] = source
    experiment = ROOT / f"paper-v4/experiment-v4/{run}"
    historical = json.loads((experiment / "results/run-result.json").read_bytes())
    for key in ("ledger_head", "replay_receipt_sha256"):
        if historical[key] != prepared[key]:
            raise ValueError(f"vocabulary run binding differs: {key}")
    if historical["ontology_sha256"] != prepared["accepted_ontology_sha256"]:
        raise ValueError("vocabulary ontology binding differs")
    input_directory = ROOT / f"private/paper-v4-v4-{run}/producer/inputs"
    sources.update(
        vocabulary_sources(
            historical["source_closure_sha256"],
            [experiment / "ontology-run/ontology-01.yaml"]
            + list(input_directory.glob("*.yaml")),
            prepared["accepted_ontology_sha256"],
        )
    )
    return freeze_sources(sources, prepared, target, review_id)


def freeze_sources(sources, prepared, target, review_id):
    result = json.loads(sources["query-result.json"])
    questions = json.loads(sources["competency-questions.json"])
    index = json.loads(sources["review-docket.json"])
    sources["base-review.py"] = sources.pop("review.py")
    sources["review-protocol.json"] = protocol_bytes(sources["review-protocol-v3.json"])
    sources["review-extension.md"] = (HERE / "REVIEW-EXTENSION.md").read_bytes()
    sources["review-task.md"] = (HERE / "REVIEW-TASK.md").read_bytes()
    if replay_mode(result) == "FRESH_FIXED_ONTOLOGY":
        sources["review-task.md"] = sources["review-task.md"].replace(
            b"This is a new retrospective review, not a revision of a historical evaluation.",
            b"This reviews one fresh fixed-ontology capture, not a historical evaluation.",
        )
        sources["review-extension.md"] += (
            b"\n## Fresh fixed-ontology execution\n\n"
            b"For this packet, the historical execution paragraph above is inapplicable. "
            b"The run is FRESH_FIXED_ONTOLOGY, with the acceptance-time query binding "
            b"retained separately. The executed-input summary records this mode. "
            b"No rows, support labels or coverage rules are converted. Review remains "
            b"model-assisted and human ratification remains pending.\n"
        )
    if replay_mode(result) == "FRESH_END_TO_END":
        sources["review-task.md"] = sources["review-task.md"].replace(
            b"This is a new retrospective review, not a revision of a historical evaluation.",
            b"This reviews one fresh end-to-end ontology and capture run, not a historical evaluation.",
        )
        sources["review-extension.md"] += (
            b"\n## Fresh end-to-end execution\n\n"
            b"The historical execution paragraph above is inapplicable. The producer "
            b"constructed its own ontology and populated it in the same session. "
            b"FRESH_END_TO_END preserves the acceptance-time query binding. "
            b"Support, coverage and pending human ratification rules are unchanged.\n"
        )
    for name in ("selective_review.py", "review_packet.py"):
        sources[name] = (HERE / name).read_bytes()
    sources["query-inputs.json"] = canonical(
        {
            "schema": "malleus.paper-v4.selective-review-query-inputs/v1",
            "mode": replay_mode(result),
            "core_commit": result["core_commit"],
            "recorded_query_inputs": result["inputs"],
            "query_result_sha256": digest(sources["query-result.json"]),
            "no_rows_or_judgments_transformed": True,
        }
    )
    names = {
        "selected-reading.json": "selected_reading",
        "retained-capture.json": "retained_capture",
        "competency-questions.json": "competency_questions",
        "query-result.json": "query_result",
        "query-trace-summary.json": "query_trace_summary",
        "population-trace.json": "population_trace",
        "population-surface.json": "population_surface",
        "answers.py": "query_program",
        "pilot.py": "query_runner",
        "capture.py": "query_runner",
        "e2e_execute.py": "query_runner",
        "binding.py": "program_binding_helper",
        "query-inputs.json": "query_binding",
        "review-protocol.json": "review_protocol",
        "query-binding.acceptance.json": "acceptance_query_binding",
    }
    if "subject_answers.py" in sources:
        names.update(
            {
                "answers.py": "base_query_program",
                "subject_answers.py": "query_program",
                "subject_query.py": "query_runner",
            }
        )
    if "ontology_answers.py" in sources:
        names.update(
            {
                "answers.py": "base_query_program",
                "ontology_answers.py": "query_program",
                "ontology_query.py": "query_runner",
            }
        )
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "status": "FROZEN_FOR_REVIEW",
        "run_id": review_id,
        "review_protocol_sha256": digest(sources["review-protocol.json"]),
        "evidence_surface": {
            "kind": "SELECTED_READING_TEXT_LAYER",
            "locator_kind": "SELECTED_READING_BLOCK_ID",
        },
        "fixed_identities": {
            "competency_questions_sha256": digest(sources["competency-questions.json"]),
            "selected_reading_sha256": digest(sources["selected-reading.json"]),
            "source_sha256": json.loads(sources["selected-reading.json"])[
                "source_sha256"
            ],
        },
        "stage_identities": {
            "accepted_ontology_sha256": prepared["accepted_ontology_sha256"],
            "ledger_head": prepared["ledger_head"],
            "replay_receipt_sha256": prepared["replay_receipt_sha256"],
            "population_trace_summary_sha256": digest(sources["population-trace.json"]),
            "query_binding_sha256": digest(sources["query-inputs.json"]),
            "query_result_sha256": digest(sources["query-result.json"]),
            "query_trace_summary_sha256": digest(sources["query-trace-summary.json"]),
        },
        "materials": [
            {
                "name": names[name] if name in names else name,
                "path": name,
                "sha256": digest(source),
                "visibility": "PRIVATE",
            }
            for name, source in sources.items()
        ],
        "question_ids": [q["id"] for q in questions["questions"]],
        "rows_per_question": prepared["rows_per_question"],
        "witnesses_traced": index["distinct_central_witnesses"],
        "authorship": {
            "preliminary_evaluator_kind": "CODEX_PRELIMINARY",
            "ratifier_evaluator_kind": "HUMAN_AUTHOR",
            "ratifier_actor_id": "actor:luis",
            "deviation": {
                "from": "CLAUDE_PRELIMINARY",
                "to": "CODEX_PRELIMINARY",
                "protocol_edited": False,
                "reason": "Luis approved fresh Codex reviewer agents for this separate retrospective arm; the frozen instrument is not changed after dispatch.",
            },
        },
    }
    blank = {
        "schema": RECORD_SCHEMA,
        "status": "BLANK",
        "inputs": {
            "review_protocol_sha256": manifest["review_protocol_sha256"],
            "review_input_manifest_sha256": "",
        },
        "preliminary": {
            "evaluator_kind": "CODEX_PRELIMINARY",
            "actor_id": "",
            "completed_at": "",
        },
        "witnesses": [],
        "questions": [
            {
                "question_id": q["id"],
                "question_responsiveness": "PENDING",
                "responsiveness_rationale": "",
                "assembly": "PENDING",
                "coverage": [],
                "source_locators": [],
                "rows": [],
            }
            for q in questions["questions"]
        ],
        "ratification": {
            "evaluator_kind": "HUMAN_AUTHOR",
            "actor_id": "actor:luis",
            "disposition": "PENDING",
            "completed_at": "",
            "notes": "",
        },
    }
    blank_source = (
        b"# Independent preliminary review\n\n```json\n"
        + canonical(blank).rstrip()
        + b"\n```\n"
    )
    base = load_base(ROOT / "paper-v4/evaluation-v4/review.py")
    base.validate_blank_review(
        blank_source, sources["review-protocol.json"], canonical(manifest)
    )
    selective_witnesses(sources["query-result.json"], manifest)
    target.mkdir(parents=True)
    for name, source in sources.items():
        (target / name).write_bytes(source)
    (target / "review-record.blank.md").write_bytes(blank_source)
    (target / "review-input-manifest.json").write_bytes(canonical(manifest))
    return {
        "packet": str(target),
        "manifest_sha256": digest(canonical(manifest)),
        "questions": len(questions["questions"]),
        "witnesses": manifest["witnesses_traced"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", choices=("run-20", "run-21"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--preparation", type=Path, required=True)
    parser.add_argument("--review-id", required=True)
    args = parser.parse_args()
    print(
        canonical(
            freeze(
                args.run,
                args.output,
                preparation=args.preparation,
                review_id=args.review_id,
            )
        ).decode()
    )

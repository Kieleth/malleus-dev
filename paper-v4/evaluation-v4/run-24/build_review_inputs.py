"""Build run-24's review package from the frozen protocol v3 instruments.

The package is three files and this script writes all three, so that no figure
in any of them is typed by hand. Run-05's task carried run-02's row counts on a
wrapped line into a live review, and the v3 template answers that with one
substitution point per figure; a template with thirty questions has thirty of
them, which is more than a person should be asked to fill by eye.

Two stages, because a cell is opened before its producer runs.

``--stage open`` instantiates what exists at open: the run id, the evidence
surface, the material paths and the thirty question ids of the frozen
competency question file, in that file's order. Every count is a figure of a
producer that has not run, so ``{{ROWS_<question id>}}``, ``{{ROWS_TOTAL}}`` and
``{{WITNESSES_TOTAL}}`` are left standing and this stage refuses if any other
placeholder survives.

``--stage freeze`` reads the cell's own frozen result and run record, fills
those counts, and writes ``review-input-manifest.json``: the v3 manifest
``review.py`` validates, declaring a ``SELECTED_READING_TEXT_LAYER`` surface,
the fixed and stage identities, the seven required materials with their
digests, the cell's question ids and its rows per question. It refuses if a
placeholder survives, if the question ids are not the question file's in order,
or if a declared material is missing from disk.

Nothing here judges anything. The controls in the question file are carried by
the file itself; the validator reports each control outcome as a finding after a
review exists, and this script neither reads nor writes an outcome.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
import textwrap


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN_ID = "run-24"

EVALUATION = ROOT / "paper-v4/evaluation-v4"
PROTOCOL = EVALUATION / "review-protocol-v3.json"
TASK_TEMPLATE = EVALUATION / "review-task-protocol-v3.template.md"
BLANK_TEMPLATE = EVALUATION / "review-record-protocol-v3.blank.md"
TASK = HERE / "review-task.md"
BLANK = HERE / "review-record.blank.md"
MANIFEST = HERE / "review-input-manifest.json"

QUESTIONS = ROOT / "paper-v4/experiment-v4/competency-questions-v3.json"
SELECTED_READING = ROOT / "private/paper-v4-text-layer/selected-reading.json"
SOURCE_PDF_SHA256 = (
    "sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9"
)

RESULTS = ROOT / f"paper-v4/experiment-v4/{RUN_ID}/results"
ONTOLOGY_RUN = ROOT / f"paper-v4/experiment-v4/{RUN_ID}/ontology-run"
PRIVATE = ROOT / f"private/paper-v4-v4-{RUN_ID}"

SURFACE_KIND = "SELECTED_READING_TEXT_LAYER"
LOCATOR_KIND = "SELECTED_READING_BLOCK_ID"
PLACEHOLDER = re.compile(r"\{\{[A-Z_0-9]+\}\}")
COUNT_PLACEHOLDERS = ("ROWS_", "WITNESSES_TOTAL")

# The seven materials protocol v3 requires of a text-layer cell, each with the
# path it takes in this cell. The reading and the two private artefacts stay
# private; the four public ones are this cell's own frozen results.
MATERIALS = (
    ("selected_reading", SELECTED_READING, "PRIVATE"),
    ("competency_questions", QUESTIONS, "PUBLIC"),
    ("query_binding", RESULTS / "native-query-binding.json", "PUBLIC"),
    ("query_result", PRIVATE / "query/query-result.json", "PRIVATE"),
    ("population_trace", RESULTS / "trace-summary.json", "PUBLIC"),
    ("retained_capture", PRIVATE / "ledger/retained-capture.json", "PRIVATE"),
    ("query_trace_summary", RESULTS / "query-trace-summary.json", "PUBLIC"),
)

AUTHORSHIP = {
    "preliminary_evaluator_kind": "CLAUDE_PRELIMINARY",
    "ratifier_evaluator_kind": "HUMAN_AUTHOR",
    "ratifier_actor_id": "actor:luis",
}


class ReviewPackageRefusal(ValueError):
    """The package cannot be written from what is on disk."""


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def question_ids() -> list[str]:
    document = json.loads(QUESTIONS.read_bytes())
    if document["status"] != "FROZEN_BEFORE_V3_CELLS":
        raise ReviewPackageRefusal("the competency question file is not frozen")
    return [str(item["id"]) for item in document["questions"]]


def _row_placeholder(question_id: str) -> str:
    return "{{ROWS_" + question_id.replace("-", "_").upper() + "}}"


def _enumeration(ids: list[str], counts: dict[str, int] | None) -> str:
    """``N rows for `CQ-…`,`` once per question, in the file's order."""

    parts = []
    for index, question_id in enumerate(ids):
        figure = (
            str(counts[question_id])
            if counts is not None
            else _row_placeholder(question_id)
        )
        noun = " rows" if index == 0 else ""
        parts.append(f"{figure}{noun} for `{question_id}`")
    return "\n".join(
        textwrap.wrap(", ".join(parts), width=76, break_long_words=False)
    )


def _record_questions(ids: list[str]) -> str:
    entries = [
        "    {\n"
        f'      "question_id": "{question_id}",\n'
        '      "question_responsiveness": "PENDING",\n'
        '      "responsiveness_rationale": "",\n'
        '      "assembly": "PENDING",\n'
        '      "coverage": [],\n'
        '      "source_locators": [],\n'
        '      "rows": []\n'
        "    }"
        for question_id in ids
    ]
    return ",\n".join(entries)


def _substitute(text: str, table: list[tuple[str, str]], subject: str) -> str:
    for before, after in table:
        if before not in text:
            raise ReviewPackageRefusal(f"{subject} carries no {before}")
        text = text.replace(before, after)
    return text


def _refuse_surviving(text: str, subject: str, counts_allowed: bool) -> None:
    found = sorted(set(PLACEHOLDER.findall(text)))
    if not counts_allowed:
        if found:
            raise ReviewPackageRefusal(f"{subject} still carries {found}")
        return
    stray = [
        name
        for name in found
        if not any(name[2:-2].startswith(prefix) for prefix in COUNT_PLACEHOLDERS)
    ]
    if stray:
        raise ReviewPackageRefusal(f"{subject} still carries {stray}")


def build_task(ids: list[str], counts: dict[str, int] | None, witnesses: int | None) -> str:
    text = TASK_TEMPLATE.read_text(encoding="utf-8")
    text = _substitute(
        text,
        [
            (
                "`{{ROWS_QUESTION_1}}` and its siblings",
                "one row-count placeholder per question",
            ),
            (
                "`{{QUESTION_ID_1}}` and its siblings",
                "one question id per question of the cell's frozen file",
            ),
            (
                "{{ROWS_QUESTION_1}} rows for\n"
                "`{{QUESTION_ID_1}}`, {{ROWS_QUESTION_2}} for `{{QUESTION_ID_2}}`,\n"
                "{{ROWS_TOTAL}} in all",
                _enumeration(ids, counts) + ",\n{{ROWS_TOTAL}} in all",
            ),
            ("{{RUN_ID}}", RUN_ID),
            ("{{SURFACE_KIND}}", SURFACE_KIND),
            ("{{SELECTED_READING_PATH}}", str(SELECTED_READING.relative_to(ROOT))),
            ("{{COMPETENCY_QUESTIONS_PATH}}", str(QUESTIONS.relative_to(ROOT))),
            (
                "{{QUERY_BINDING_PATH}}",
                str((RESULTS / "native-query-binding.json").relative_to(ROOT)),
            ),
            (
                "{{QUERY_RESULT_PATH}}",
                str((PRIVATE / "query/query-result.json").relative_to(ROOT)),
            ),
            (
                "{{POPULATION_TRACE_PATH}}",
                str((RESULTS / "trace-summary.json").relative_to(ROOT)),
            ),
            (
                "{{QUERY_TRACE_SUMMARY_PATH}}",
                str((RESULTS / "query-trace-summary.json").relative_to(ROOT)),
            ),
        ],
        "review task",
    )
    if counts is not None:
        text = text.replace("{{ROWS_TOTAL}}", str(sum(counts.values())))
    if witnesses is not None:
        text = text.replace("{{WITNESSES_TOTAL}}", str(witnesses))
    _refuse_surviving(text, "review task", counts_allowed=counts is None)
    return text


def build_blank(ids: list[str], counts: dict[str, int] | None, witnesses: int | None) -> str:
    text = BLANK_TEMPLATE.read_text(encoding="utf-8")
    text = _substitute(
        text,
        [
            (
                "Template. The question ids, the row counts and the witness count are\n"
                "substituted at freeze, from the frozen cell's own competency question"
                " file and\nquery result, at the same time as\n"
                "`paper-v4/evaluation-v4/review-task-protocol-v3.template.md`. No"
                " placeholder\nmay survive instantiation.",
                f"This is {RUN_ID}'s blank record, written by\n"
                f"`paper-v4/evaluation-v4/{RUN_ID}/build_review_inputs.py` from"
                " the frozen v3\ntemplate. The question ids are this cell's frozen"
                " competency question file's,\nin that file's order. The row and"
                " witness counts are figures of a producer\nthat has not run and are"
                " filled by the same script at freeze; no other\nplaceholder survives"
                " either stage.",
            ),
            (
                "Write one `questions` entry per question in the cell's competency"
                " question\nfile, in that file's order, with the file's own ids: this"
                " template carries two\nas the pattern. Write one `witnesses` entry per"
                " distinct witness the query\nresult returns, {{WITNESSES_TOTAL}} in"
                " all, and reference it from every row\nthat shares it. Rows:"
                " {{ROWS_QUESTION_1}} for `{{QUESTION_ID_1}}`,\n{{ROWS_QUESTION_2}} for"
                " `{{QUESTION_ID_2}}`, {{ROWS_TOTAL}} in all.",
                f"The `questions` block below carries one entry per question of"
                f" the cell's\ncompetency question file, {len(ids)} of them, in that"
                " file's order. Write one\n`witnesses` entry per distinct witness the"
                " query result returns,\n{{WITNESSES_TOTAL}} in all, and reference it"
                " from every row that shares it.\nRows: "
                + _enumeration(ids, counts)
                + ",\n{{ROWS_TOTAL}} in all.",
            ),
            (
                '    {\n'
                '      "question_id": "{{QUESTION_ID_1}}",\n'
                '      "question_responsiveness": "PENDING",\n'
                '      "responsiveness_rationale": "",\n'
                '      "assembly": "PENDING",\n'
                '      "coverage": [],\n'
                '      "source_locators": [],\n'
                '      "rows": []\n'
                '    },\n'
                '    {\n'
                '      "question_id": "{{QUESTION_ID_2}}",\n'
                '      "question_responsiveness": "PENDING",\n'
                '      "responsiveness_rationale": "",\n'
                '      "assembly": "PENDING",\n'
                '      "coverage": [],\n'
                '      "source_locators": [],\n'
                '      "rows": []\n'
                '    }',
                _record_questions(ids),
            ),
        ],
        "blank review record",
    )
    if counts is not None:
        text = text.replace("{{ROWS_TOTAL}}", str(sum(counts.values())))
    if witnesses is not None:
        text = text.replace("{{WITNESSES_TOTAL}}", str(witnesses))
    _refuse_surviving(text, "blank review record", counts_allowed=counts is None)
    return text


def _rows_per_question(ids: list[str]) -> dict[str, int]:
    result = json.loads((PRIVATE / "query/query-result.json").read_bytes())
    counts = {
        str(query["question_id"]): len(query["rows"]) for query in result["queries"]
    }
    if sorted(counts) != sorted(ids):
        raise ReviewPackageRefusal(
            "the query result does not answer this cell's questions"
        )
    return {question_id: counts[question_id] for question_id in ids}


def _witnesses_traced() -> int:
    summary = json.loads((RESULTS / "query-trace-summary.json").read_bytes())
    return int(summary["witnesses_traced"])


def build_manifest(ids: list[str], counts: dict[str, int], witnesses: int) -> dict:
    run_result = json.loads((RESULTS / "run-result.json").read_bytes())
    materials = []
    for name, path, visibility in MATERIALS:
        if not path.is_file():
            raise ReviewPackageRefusal(f"declared material is not on disk: {name}")
        materials.append(
            {
                "name": name,
                "path": str(path.relative_to(ROOT)),
                "sha256": _digest(path.read_bytes()),
                "visibility": visibility,
            }
        )
    by_name = {item["name"]: item for item in materials}
    return {
        "schema": "malleus.paper-v4.source-grounded-review-inputs/v3",
        "status": "FROZEN_FOR_REVIEW",
        "run_id": RUN_ID,
        "review_protocol_sha256": _digest(PROTOCOL.read_bytes()),
        "evidence_surface": {"kind": SURFACE_KIND, "locator_kind": LOCATOR_KIND},
        "fixed_identities": {
            "source_sha256": SOURCE_PDF_SHA256,
            "selected_reading_sha256": by_name["selected_reading"]["sha256"],
            "competency_questions_sha256": by_name["competency_questions"]["sha256"],
        },
        "stage_identities": {
            "accepted_ontology_sha256": run_result["ontology_sha256"],
            "ledger_head": run_result["ledger_head"],
            "replay_receipt_sha256": run_result["replay_receipt_sha256"],
            "query_binding_sha256": by_name["query_binding"]["sha256"],
            "query_result_sha256": by_name["query_result"]["sha256"],
            "query_trace_summary_sha256": by_name["query_trace_summary"]["sha256"],
            "population_trace_summary_sha256": by_name["population_trace"]["sha256"],
        },
        "materials": materials,
        "question_ids": ids,
        "rows_per_question": counts,
        "witnesses_traced": witnesses,
        "authorship": dict(AUTHORSHIP),
    }


def execute(stage: str) -> dict[str, object]:
    ids = question_ids()
    counts = _rows_per_question(ids) if stage == "freeze" else None
    witnesses = _witnesses_traced() if stage == "freeze" else None
    TASK.write_text(build_task(ids, counts, witnesses), encoding="utf-8")
    BLANK.write_text(build_blank(ids, counts, witnesses), encoding="utf-8")
    written = {"stage": stage, "questions": len(ids), "task": str(TASK.name)}
    if stage == "freeze":
        manifest = build_manifest(ids, counts, witnesses)
        MANIFEST.write_bytes(
            json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
        )
        written["rows_total"] = sum(counts.values())
        written["witnesses_traced"] = witnesses
        written["manifest_sha256"] = _digest(MANIFEST.read_bytes())
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--stage", choices=("open", "freeze"), required=True)
    arguments = parser.parse_args(argv)
    try:
        print(json.dumps(execute(arguments.stage), indent=2, sort_keys=True))
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(
            f"review-package: {type(error).__name__}: {error}", file=sys.stderr
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

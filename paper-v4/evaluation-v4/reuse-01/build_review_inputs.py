"""Build reuse-01's review package on the v3.2 instruments.

reuse-01 is not a new graph. It is run-23's accepted, frozen graph asked a
second, independent question set, so the shape of this script is
`paper-v4/evaluation-v4/run-25/build_review_inputs.py` and the three things it
changes are the ones the second set and the newer protocol force:

* the protocol is `review-protocol-v3.2.json`, so the manifest and the record
  carry the v3.2 schemas and the absence vocabulary has six codes, not five;
* the four graph identities the manifest binds come from run-23's own frozen
  ``results/run-result.json``, because run-23's ontology, ledger head and replay
  receipt are what this cell queried and no stage here moved them;
* the task carries three things the v3 template does not: the protocol's own
  checklist, rendered for this surface; the six absence codes with the
  protocol's own definitions; and the subject-tie rule, quoted from the ruled
  clarification with its digest, which every reviewer since 2026-09-12 has been
  handed as an addendum.

Two stages, because a cell is opened before its query runs.

``--stage open`` instantiates what exists at open: the run id, the evidence
surface, the material paths and the thirty question ids of the frozen question
file, in that file's order. Every count is a figure of a query that has not run,
so ``{{ROWS_<question id>}}``, ``{{ROWS_TOTAL}}`` and ``{{WITNESSES_TOTAL}}`` are
left standing and this stage refuses if any other placeholder survives.

``--stage freeze`` reads this cell's own query result, fills those counts, writes
one review block per question, and writes the v3.2 input manifest.

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
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN_ID = "reuse-01"

EVALUATION = ROOT / "paper-v4/evaluation-v4"
PROTOCOL = EVALUATION / "review-protocol-v3.2.json"
TASK_TEMPLATE = EVALUATION / "review-task-protocol-v3.template.md"
BLANK_TEMPLATE = EVALUATION / "review-record-protocol-v3.blank.md"
CLARIFICATION = EVALUATION / "review-task-v3-clarification-2026-09-12.md"
TASK = HERE / "review-task.md"
BLANK = HERE / "review-record.blank.md"
MANIFEST = HERE / "review-input-manifest.json"

QUESTIONS = ROOT / "paper-v4/experiment-v4/competency-questions-set-b.json"
SELECTED_READING = ROOT / "private/paper-v4-text-layer/selected-reading.json"
SOURCE_PDF_SHA256 = (
    "sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9"
)

RESULTS = ROOT / f"paper-v4/experiment-v4/{RUN_ID}/results"
PRIVATE = ROOT / f"private/paper-v4-{RUN_ID}"

# The graph is run-23's and nothing here moved it. Its population trace, its
# retained capture and its run record are read, never written.
RUN_23 = ROOT / "paper-v4/experiment-v4/run-23"
RUN_23_PRIVATE = ROOT / "private/paper-v4-v4-run-23"
RUN_23_RESULT = RUN_23 / "results/run-result.json"

SURFACE_KIND = "SELECTED_READING_TEXT_LAYER"
LOCATOR_KIND = "SELECTED_READING_BLOCK_ID"
PLACEHOLDER = re.compile(r"\{\{[A-Z_0-9]+\}\}")
COUNT_PLACEHOLDERS = ("ROWS_", "WITNESSES_TOTAL")

# The seven materials protocol v3.2 requires of a text-layer cell. Three of them
# are run-23's frozen artefacts, because the graph and its provenance are
# run-23's; three are this cell's own; the reading is the same reading.
MATERIALS = (
    ("selected_reading", SELECTED_READING, "PRIVATE"),
    ("competency_questions", QUESTIONS, "PUBLIC"),
    ("query_binding", RESULTS / "native-query-binding.json", "PUBLIC"),
    ("query_result", PRIVATE / "query/query-result.json", "PRIVATE"),
    ("population_trace", RUN_23 / "results/trace-summary.json", "PUBLIC"),
    ("retained_capture", RUN_23_PRIVATE / "ledger/retained-capture.json", "PRIVATE"),
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


def question_file() -> list[dict[str, Any]]:
    document = json.loads(QUESTIONS.read_bytes())
    if document["status"] != "FROZEN":
        raise ReviewPackageRefusal("the competency question file is not frozen")
    if document.get("set") != "B":
        raise ReviewPackageRefusal("this cell asks the independent second set")
    return list(document["questions"])


def question_ids() -> list[str]:
    return [str(item["id"]) for item in question_file()]


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


def _section(text: str, heading: str) -> tuple[int, int]:
    marker = f"\n## {heading}\n"
    if text.count(marker) != 1:
        raise ReviewPackageRefusal(
            f"the v3 task template does not carry exactly one section {heading!r}"
        )
    start = text.index(marker)
    following = text.find("\n## ", start + len(marker))
    return start, len(text) if following == -1 else following


def _replace_section(text: str, heading: str, replacement: str) -> str:
    start, end = _section(text, heading)
    return text[:start] + replacement + text[end:]


PREAMBLE = """# Malleus paper v4 source-grounded review task, protocol v3.2, second question set

This is {run_id}'s review task, written by
`paper-v4/evaluation-v4/reuse-01/build_review_inputs.py` from the frozen v3
template at `paper-v4/evaluation-v4/review-task-protocol-v3.template.md`. Every
figure below is substituted from this cell's own frozen question file and query
result; no placeholder survives instantiation.

Status: the method was frozen before this cell's query ran, at
`paper-v4/evaluation-v4/review-protocol-v3.2.json`. It is not edited for this
review. That file supersedes `review-protocol-v3.json` for cells opened after it
and changes three things, of which two reach a graph surface:

- A sixth absence code, `NOT_CAPTURED`, for an element the accepted contract has
  a type or a slot for, that no record or field carries and no gap declares.
  Under v3 that fact and "the contract has no place for this at all" shared the
  token `NOT_MODELLED`, so an absence could not be diagnosed from its code.
- Stage identities are declared per surface kind. This cell binds the seven a
  graph surface carries, unchanged from v3.
- A third surface kind for a prose answer set, which is not this cell.

**What this cell is.** It is not a new graph. The graph is run-23's, already
admitted, replayed, reviewed and frozen; no producer ran here, no ontology was
authored, nothing was captured, admitted or replayed for this cell. What is new
is the question set: thirty questions authored from the selected reading alone
by a session that saw no ontology, no graph and no earlier question file, and
put to run-23's untouched ledger. The graph was built question-blind against the
first set and was equally blind to this one.

**One thing to hold on to while you judge.** You are judging run-23's records
against questions run-23's producer never saw, which is the same condition every
graph cell of this experiment was reviewed under. Judge exactly as you would
judge run-23 itself.

You are a fresh Claude session performing the preliminary inspection. Record
your kind as `CLAUDE_PRELIMINARY`, which is the kind the protocol names; if you
are anything else, the substitution is recorded as a deviation in
`paper-v4/evaluation-v4/{run_id}/review-input-manifest.json`, which also binds
every input below by digest. Verify those digests before you begin. This is
AI-assisted preliminary work, not human evidence: Luis ratifies, and only a
record with status `HUMAN_RATIFIED` is evidence for the paper.
"""

JUDGMENTS = """
## Judgments

Per witness, choose one `source_support`:

- `SUPPORTED`: the cited surface supports every material claim in the row.
- `PARTIAL`: it supports some but not all of them, or a needed qualifier is
  absent.
- `UNSUPPORTED`: it contradicts a material claim or supplies no support for it.
- `NOT_EVALUABLE`: the allowed source surface is insufficient to decide.

Per question, you do not choose a label. You fill `coverage`: one entry per item
of that question's `required_semantics`, in the question file's order. For each
item, either name the `row_index` of a row whose witness is `SUPPORTED` and
whose projected fields carry that item; or write `null` there and exactly one
`absent_reason`. These are the protocol's six, each with the protocol's own
definition:

{absence_codes}

Then write the `question_responsiveness` the derivation produces:

- `COVERED`: every required semantic names a row.
- `PARTIAL`: some do and some are absent.
- `NONE`: none does.

The validator recomputes it and refuses a label its derivation does not
produce. Write the reason for the absences in `responsiveness_rationale`, in
your own words.

Also record one `assembly` descriptor per question, which describes how the
answer is assembled and never moves a label:

- `ONE_ROW`: one row carries the whole answer.
- `LINKED_ROWS`: several rows carry it and a relation in the result joins them.
- `UNLINKED_ROWS`: several rows carry it and nothing in the row representation
  joins them.

Judge every returned row exactly once, in order: {enumeration},
{{{{ROWS_TOTAL}}}} in all, over {{{{WITNESSES_TOTAL}}}} distinct witnesses. Cite
at least one locator per witness and per question. Write each reason in your own
words. Copy no source passage into the record beyond the locator, and add no
numerical aggregate.

{subject_tie}"""

CHECKLIST_HEAD = """
## The checklist

The protocol is the rulebook; this is how each rule is verified. Work the list
in order. Reproduce it in your handover note beside the record, with a tick and
one line per entry saying how it came out; the record's own key set is exact and
carries no tick. An entry the validator settles is still yours to read: the
validator refuses when it fails, and a refusal you did not expect is a finding.
"""

RECORDING = """
## Recording

Copy `paper-v4/evaluation-v4/{run_id}/review-record.blank.md`, set `status` to
`PRELIMINARY_COMPLETE`, bind the input manifest digest in
`inputs.review_input_manifest_sha256`, fill `preliminary.actor_id` and
`preliminary.completed_at`, and leave the whole `ratification` block pending.
The per-question review blocks in `paper-v4/evaluation-v4/{run_id}/` carry each
question's rows, their witness keys and its required semantics; fill one and
assemble them into the record's `questions` array in the question file's order.

Then validate your own record with `validate_review` in
`paper-v4/evaluation-v4/review.py`, passing the v3.2 protocol bytes, the input
manifest, the query result, the competency questions and the selected reading.
It checks identities, the declared surface and its locators, witness uniqueness
and row coverage, coverage against `required_semantics` and the derived label.
It never chooses or changes a judgment. Hand the completed record to Luis for
ratification.
"""


def absence_codes() -> str:
    """The six absence codes with the protocol's own definitions, in its order."""

    judgments = json.loads(PROTOCOL.read_bytes())["judgments"]
    definitions = judgments["coverage_absent_reason_definitions"]
    lines = []
    for name in judgments["coverage_absent_reasons"]:
        if name not in definitions:
            raise ReviewPackageRefusal(f"the protocol defines no absence code {name}")
        lines.append(
            "\n".join(
                textwrap.wrap(
                    f"- `{name}`: {definitions[name]}.",
                    width=76,
                    break_long_words=False,
                    break_on_hyphens=False,
                    subsequent_indent="  ",
                )
            )
        )
    return "\n".join(lines)


def subject_tie() -> str:
    """The subject-tie rule, quoted from the ruled clarification with its digest."""

    source = CLARIFICATION.read_bytes()
    text = source.decode("utf-8")
    marker = "## The rule\n"
    if text.count(marker) != 1:
        raise ReviewPackageRefusal("the clarification carries no single rule section")
    start = text.index(marker) + len(marker)
    end = text.find("\n## ", start)
    rule = text[start : len(text) if end == -1 else end].strip()
    quoted = "\n".join("> " + line if line else ">" for line in rule.splitlines())
    return (
        "## The subject-tie rule\n\n"
        "Ruled on 2026-09-12 and handed to every reviewer since, quoted from\n"
        f"`{CLARIFICATION.relative_to(ROOT)}`,\n"
        f"{_digest(source)}:\n\n"
        f"{quoted}\n\n"
        "It binds this cell. A row that carries a same-named element for some\n"
        "other subject does not name the semantic; write `row_index: null` and\n"
        "the absence cause.\n"
    )


def checklist(kind: str = SURFACE_KIND) -> str:
    """The protocol's checklist, numbered, filtered to this surface kind."""

    section = json.loads(PROTOCOL.read_bytes())["checklist"]
    entries = [item for item in section["checks"] if kind in item["applies_to"]]
    if not entries:
        raise ReviewPackageRefusal(f"the protocol lists no check for {kind}")
    lines = [CHECKLIST_HEAD.rstrip("\n"), ""]
    for position, item in enumerate(entries, start=1):
        who = item["verified_by"]
        named = (
            item["validator_function"]
            if who == "VALIDATOR"
            else item["reviewer_judgement"]
        )
        body = (
            f"{position}. **{item['name']}** (`{item['id']}`). "
            f"{item['passes_when']} Reads: {', '.join(item['reads'])}. "
            f"Settled by the {who.lower()} ({named}). "
            f"Outcome: `{item['records_outcome_in']}`."
        )
        lines.append(
            "\n".join(
                textwrap.wrap(
                    body,
                    width=76,
                    break_long_words=False,
                    break_on_hyphens=False,
                    subsequent_indent="   ",
                )
            )
        )
        lines.append("")
    return "\n".join(lines)


def build_task(
    ids: list[str], counts: dict[str, int] | None, witnesses: int | None
) -> str:
    text = TASK_TEMPLATE.read_text(encoding="utf-8")
    start, _ = _section(text, "What you judge")
    text = PREAMBLE.format(run_id=RUN_ID) + text[start:]
    text = _substitute(
        text,
        [
            ("{{RUN_ID}}", RUN_ID),
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
                str((RUN_23 / "results/trace-summary.json").relative_to(ROOT)),
            ),
            (
                "{{QUERY_TRACE_SUMMARY_PATH}}",
                str((RESULTS / "query-trace-summary.json").relative_to(ROOT)),
            ),
        ],
        "review task",
    )
    text = _replace_section(
        text,
        "Judgments",
        JUDGMENTS.format(
            enumeration=_enumeration(ids, counts),
            absence_codes=absence_codes(),
            subject_tie=subject_tie(),
        ),
    )
    text = _replace_section(
        text, "Recording", checklist() + RECORDING.format(run_id=RUN_ID)
    )
    if counts is not None:
        text = text.replace("{{ROWS_TOTAL}}", str(sum(counts.values())))
    if witnesses is not None:
        text = text.replace("{{WITNESSES_TOTAL}}", str(witnesses))
    _refuse_surviving(text, "review task", counts_allowed=counts is None)
    return text


BLANK_PREAMBLE = """# Malleus paper v4 source-grounded review record, protocol v3.2, second question set

This is {run_id}'s blank record, written by
`paper-v4/evaluation-v4/reuse-01/build_review_inputs.py` from the frozen v3
template. The question ids are this cell's frozen competency question file's, in
that file's order. The row and witness counts are this cell's query result's.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Write one `witnesses` entry per distinct witness the query result returns,
{{{{WITNESSES_TOTAL}}}} in all, and reference it from every row that shares it.
Rows: {enumeration},
{{{{ROWS_TOTAL}}}} in all.

Three things the validator derives or forbids, so that writing them wrong is
refused rather than recorded:

- `question_responsiveness` is derived from `coverage`. Write the label the
  derivation produces, `COVERED` when every required semantic names a row,
  `NONE` when none does, `PARTIAL` otherwise. A label the derivation does not
  produce is refused.
- `assembly` is a descriptor, not a grade. It never moves a label.
- A witness is judged once. Two rows with the same key are the same witness.

This is a `SELECTED_READING_TEXT_LAYER` cell: no witness carries `resolution`
and every locator is a reading block id. Copy no source passage into this record
beyond the locator, and add no numerical aggregate.

```json
{record}
```

Each `witnesses` entry has this shape, with the fixed tokens the task defines at
the head of the `rationale`:

```
{{{{
  "witness_key": "obs:instrument-count",
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "source_locators": ["page:2:block:004"],
  "rationale": "DIGEST_OK SUBJECT_IN_BLOCK one or two sentences in your own words"
}}}}
```

Each `rows` entry names a returned row and the witness it shares:

```
{{{{
  "row_index": 0,
  "witness_key": "obs:instrument-count"
}}}}
```

Each `coverage` entry names one required semantic and either the row that
carries it or one typed reason it is absent:

```
{{{{
  "semantic": "instrument_count",
  "row_index": 3,
  "absent_reason": null,
  "note": ""
}}}}

{{{{
  "semantic": "instrument_count",
  "row_index": null,
  "absent_reason": "NOT_MODELLED | NOT_CAPTURED | WITHHELD_STATEMENT | UNREACHED_RECORD | NOT_IN_SOURCE | LOCATOR_NOT_RESOLVABLE",
  "note": "why, in your own words"
}}}}
```
"""


def _blank_record(ids: list[str]) -> dict[str, Any]:
    return {
        "schema": "malleus.paper-v4.source-grounded-review/v3.2",
        "status": "BLANK",
        "inputs": {
            "review_protocol_sha256": _digest(PROTOCOL.read_bytes()),
            "review_input_manifest_sha256": "",
        },
        "preliminary": {
            "evaluator_kind": "CLAUDE_PRELIMINARY",
            "actor_id": "",
            "completed_at": "",
        },
        "witnesses": [],
        "questions": [
            {
                "question_id": question_id,
                "question_responsiveness": "PENDING",
                "responsiveness_rationale": "",
                "assembly": "PENDING",
                "coverage": [],
                "source_locators": [],
                "rows": [],
            }
            for question_id in ids
        ],
        "ratification": {
            "evaluator_kind": "HUMAN_AUTHOR",
            "actor_id": "actor:luis",
            "disposition": "PENDING",
            "completed_at": "",
            "notes": "",
        },
    }


def build_blank(
    ids: list[str], counts: dict[str, int] | None, witnesses: int | None
) -> str:
    # The v3 blank is read so that a template this cell no longer matches is a
    # refusal rather than a silent divergence.
    template = BLANK_TEMPLATE.read_text(encoding="utf-8")
    if '"schema": "malleus.paper-v4.source-grounded-review/v3"' not in template:
        raise ReviewPackageRefusal("the v3 blank template no longer declares its schema")
    text = BLANK_PREAMBLE.format(
        run_id=RUN_ID,
        enumeration=_enumeration(ids, counts),
        record=json.dumps(_blank_record(ids), ensure_ascii=False, indent=2),
    )
    if counts is not None:
        text = text.replace("{{ROWS_TOTAL}}", str(sum(counts.values())))
    if witnesses is not None:
        text = text.replace("{{WITNESSES_TOTAL}}", str(witnesses))
    _refuse_surviving(text, "blank review record", counts_allowed=counts is None)
    return text


def _query_result() -> dict[str, Any]:
    path = PRIVATE / "query/query-result.json"
    if not path.is_file():
        raise ReviewPackageRefusal(f"the query has not run; expected {path}")
    return json.loads(path.read_bytes())


def _rows_per_question(ids: list[str]) -> dict[str, int]:
    result = _query_result()
    counts = {
        str(query["question_id"]): len(query["rows"]) for query in result["queries"]
    }
    if sorted(counts) != sorted(ids):
        raise ReviewPackageRefusal(
            "the query result does not answer this cell's questions"
        )
    return {question_id: counts[question_id] for question_id in ids}


def _witness_key(row: dict[str, Any]) -> str:
    return str(row["witness"].get("relation_id") or row["witness"]["record_id"])


def _witnesses_traced() -> int:
    """The distinct witnesses of the returned rows, which is what v3.2 judges.

    ``review.py`` counts the witness of every returned row and refuses a
    manifest whose figure differs. ``query-trace-summary.json`` counts every
    record the executor traced, which includes a record reached only as another
    row's subject; no row takes it as its witness and no reviewer judges it. The
    two figures need not coincide, so this one is computed from the query result
    and ``_records_traced`` keeps the trace summary's own number.
    """

    result = _query_result()
    return len(
        {
            _witness_key(row)
            for query in result["queries"]
            for row in query["rows"]
        }
    )


def _records_traced() -> int:
    summary = json.loads((RESULTS / "query-trace-summary.json").read_bytes())
    return int(summary["witnesses_traced"])


def build_blocks(result: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    """One working surface per question: its rows, its semantics, no judgment."""

    by_id = {
        str(query["question_id"]): query
        for query in (result or {}).get("queries", [])
    }
    blocks: dict[str, dict[str, Any]] = {}
    for question in question_file():
        question_id = str(question["id"])
        rows = list(by_id[question_id]["rows"]) if question_id in by_id else []
        blocks[question_id] = {
            "question_id": question_id,
            "question": question["question"],
            "required_semantics": list(question["required_semantics"]),
            "question_responsiveness": "PENDING",
            "responsiveness_rationale": "",
            "assembly": "PENDING",
            "coverage": [
                {
                    "semantic": semantic,
                    "row_index": None,
                    "absent_reason": None,
                    "note": "",
                }
                for semantic in question["required_semantics"]
            ],
            "source_locators": [],
            "rows": [
                {"row_index": index, "witness_key": _witness_key(row)}
                for index, row in enumerate(rows)
            ],
        }
    return blocks


def build_manifest(ids: list[str], counts: dict[str, int], witnesses: int) -> dict:
    # The graph's four identities are run-23's, read from its own frozen run
    # record. Nothing in this cell produced them and nothing in it moved them.
    run_result = json.loads(RUN_23_RESULT.read_bytes())
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
    if by_name["population_trace"]["sha256"] != run_result["trace_summary_sha256"]:
        raise ReviewPackageRefusal("run-23's population trace is not its frozen bytes")
    return {
        "schema": "malleus.paper-v4.source-grounded-review-inputs/v3.2",
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
    result = _query_result() if stage == "freeze" else None
    counts = _rows_per_question(ids) if stage == "freeze" else None
    witnesses = _witnesses_traced() if stage == "freeze" else None

    HERE.mkdir(parents=True, exist_ok=True)
    TASK.write_text(build_task(ids, counts, witnesses), encoding="utf-8")
    BLANK.write_text(build_blank(ids, counts, witnesses), encoding="utf-8")
    blocks = build_blocks(result)
    for question_id, block in blocks.items():
        (HERE / f"review-block.{question_id}.json").write_bytes(
            json.dumps(block, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
        )
    written: dict[str, object] = {
        "stage": stage,
        "questions": len(ids),
        "task": str(TASK.relative_to(ROOT)),
        "blocks": len(blocks),
    }
    if stage == "freeze":
        assert counts is not None and witnesses is not None
        manifest = build_manifest(ids, counts, witnesses)
        MANIFEST.write_bytes(
            json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
        )
        written["rows_total"] = sum(counts.values())
        written["witnesses_traced"] = witnesses
        written["records_traced"] = _records_traced()
        written["manifest_sha256"] = _digest(MANIFEST.read_bytes())
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--stage", choices=("open", "freeze"), required=True)
    arguments = parser.parse_args(argv)
    try:
        print(json.dumps(execute(arguments.stage), indent=2, sort_keys=True))
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"review-package: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

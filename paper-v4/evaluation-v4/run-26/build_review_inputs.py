"""Build run-26's review package from the frozen protocol v3.2 instruments.

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
those counts, and writes ``review-input-manifest.json``: the v3.2 manifest
``review.py`` validates, declaring a ``SELECTED_READING_TEXT_LAYER`` surface,
the fixed and stage identities the protocol requires of that kind, the seven
required materials with their digests, the cell's question ids and its rows per
question. It refuses if a placeholder survives, if the question ids are not the
question file's in order, or if a declared material is missing from disk.

What differs from run-25's builder, which is this one's base, and why. The task
is still derived from `review-task-protocol-v3.template.md`, because v3.2 does
not ship a task template of its own, so three sections are replaced section by
section and the script refuses if a section it means to replace is not found:

- the status paragraph, which named v3, becomes a v3.2 preamble stating the
  three declarations that differ and which of them reaches a text-layer cell;
- the absent-reason list inside `Judgments` becomes this protocol's six codes
  with the one-sentence definitions the protocol file itself carries, read from
  it rather than restated here;
- `Recording` gains the protocol's checklist, numbered and filtered to this
  surface kind, and names the v3.2 bytes as what the validator is passed.

Two rules travel inside the task rather than beside it. The subject-tie rule of
`review-task-v3-clarification-2026-09-12.md` is quoted with its path and digest,
where run-25 handed it to its reviewer as an addendum recorded in the launch
log; the clarification says it is to be folded into the task at the next
protocol revision and v3.2 is that revision. And the checklist is worked in
order and reproduced ticked in a handover note beside the record, never in the
record, whose key set is exact under the protocol.

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
RUN_ID = "run-26"

EVALUATION = ROOT / "paper-v4/evaluation-v4"
PROTOCOL = EVALUATION / "review-protocol-v3.2.json"
PRIOR_PROTOCOL = EVALUATION / "review-protocol-v3.json"
TASK_TEMPLATE = EVALUATION / "review-task-protocol-v3.template.md"
BLANK_TEMPLATE = EVALUATION / "review-record-protocol-v3.blank.md"
CLARIFICATION = EVALUATION / "review-task-v3-clarification-2026-09-12.md"
TASK = HERE / "review-task.md"
BLANK = HERE / "review-record.blank.md"
MANIFEST = HERE / "review-input-manifest.json"
CHECKLIST_NOTE = f"paper-v4/evaluation-v4/{RUN_ID}/review-checklist.md"

QUESTIONS = ROOT / "paper-v4/experiment-v4/competency-questions-v3.1.json"
SELECTED_READING = ROOT / "private/paper-v4-text-layer/selected-reading.json"
SOURCE_PDF_SHA256 = (
    "sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9"
)

RESULTS = ROOT / f"paper-v4/experiment-v4/{RUN_ID}/results"
ONTOLOGY_RUN = ROOT / f"paper-v4/experiment-v4/{RUN_ID}/ontology-run"
PRIVATE = ROOT / f"private/paper-v4-v4-{RUN_ID}"

SURFACE_KIND = "SELECTED_READING_TEXT_LAYER"
LOCATOR_KIND = "SELECTED_READING_BLOCK_ID"
MANIFEST_SCHEMA = "malleus.paper-v4.source-grounded-review-inputs/v3.2"
RECORD_SCHEMA = "malleus.paper-v4.source-grounded-review/v3.2"
PLACEHOLDER = re.compile(r"\{\{[A-Z_0-9]+\}\}")
COUNT_PLACEHOLDERS = ("ROWS_", "WITNESSES_TOTAL")

# The seven materials protocol v3.2 requires of a text-layer cell, each with the
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


def protocol() -> dict:
    document = json.loads(PROTOCOL.read_bytes())
    if document["schema"] != "malleus.paper-v4.source-grounded-review-protocol/v3.2":
        raise ReviewPackageRefusal("the bound protocol is not the v3.2 file")
    return document


def question_ids() -> list[str]:
    document = json.loads(QUESTIONS.read_bytes())
    if document["status"] != "FROZEN_BEFORE_V3_1_CELLS":
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


# --------------------------------------------------------------------------
# The three v3.2 differences the task has to state
# --------------------------------------------------------------------------


PREAMBLE = """# Malleus paper v4 source-grounded review task, protocol v3.2

This is {run_id}'s review task, written by
`paper-v4/evaluation-v4/{run_id}/build_review_inputs.py` from the frozen v3
template at `paper-v4/evaluation-v4/review-task-protocol-v3.template.md`. Every
figure below is substituted from this cell's own frozen question file and query
result; no placeholder survives instantiation.

Status: the method was frozen before the producer ran, at
`paper-v4/evaluation-v4/review-protocol-v3.2.json`
(`{protocol_sha256}`). It is not edited for this
review. That file supersedes `review-protocol-v3.json` for cells opened after
it, and this is the first graph cell reviewed under it. Three declarations
differ from v3 and only one of them reaches a cell like this one:

- **A sixth absence code, `NOT_CAPTURED`.** v3's five had no word for plain
  omission, so `NOT_MODELLED` carried both "the accepted contract has no type
  and no slot for this" and "the contract had a place and this record left it
  unset", and an absence could not be diagnosed from its token. The six codes
  and their definitions are in the `Judgments` section below, and choosing
  between `NOT_MODELLED` and `NOT_CAPTURED` is yours, not the validator's.
- **Stage identities are declared per surface kind.** On this surface that is
  the same seven keys v3 fixed, so this cell's manifest keeps its shape. The
  declaration exists because an answer set has no ledger, no replay receipt and
  no query binding.
- **A third evidence surface kind, `IN_CONTEXT_ANSWER_SET`.** This cell does not
  use it. Your surface is `{surface_kind}`, as the manifest declares.

Everything else is v3 unchanged: support judged once per distinct witness, a
locator that does not resolve carrying `NOT_EVALUABLE` by rule, the question
label derived from coverage rather than chosen, and a control reported as a
finding and refusing nothing.

Two rules in this task are not in the v3 template. The subject-tie rule has its
own section below and is quoted from the file that carries it. And the protocol
now ships a checklist, which is rendered in `Recording`: you work it in order
and reproduce it ticked in a handover note, not in the record.

You are a fresh Claude session performing the preliminary inspection. Record
your kind as `CLAUDE_PRELIMINARY`, which is the kind the protocol names; if you
are anything else, the substitution is recorded as a deviation in
`paper-v4/evaluation-v4/{run_id}/review-input-manifest.json`, which also binds
every input below by digest. Verify those digests before you begin. This is
AI-assisted preliminary work, not human evidence: Luis ratifies, and only a
record with status `HUMAN_RATIFIED` is evidence for the paper.
"""

SUBJECT_TIE_HEAD = """
## The subject-tie rule

This rule governs how a coverage entry names a row. It is quoted verbatim from
`{path}`
(`{sha256}`), whose own status line says it
is to be folded into the task template at the next protocol revision. v3.2 is
that revision, so it is part of this task and not an addendum handed to you
beside it. Run-25's reviewer was given the same words in its spawn message and
its launch log records that as an instruction beyond the task; here there is
nothing beyond the task.

"""

CHECKLIST_HEAD = """
## The checklist

The protocol is the rulebook; this is how each rule is verified. Work the list
in order. Reproduce it in `{note}` beside the record, with a tick and one line
per entry saying how it came out; the record's own key set is exact and carries
no tick. An entry the validator settles is still yours to read: the validator
refuses when it fails, and a refusal you did not expect is a finding.

"""

RECORDING = """
## Recording

Copy `paper-v4/evaluation-v4/{run_id}/review-record.blank.md`, set `status` to
`PRELIMINARY_COMPLETE`, bind the input manifest digest in
`inputs.review_input_manifest_sha256`, fill `preliminary.actor_id` and
`preliminary.completed_at`, and leave the whole `ratification` block pending.
The record's schema is `{record_schema}` and its key set is exact: the
checklist ticks go in `{note}`, never in it.

Then run the paper gate:

```
.venv/bin/python paper-v4/run_active_tests.py
```

and validate your own record with `validate_review` in
`paper-v4/evaluation-v4/review.py`, passing the **v3.2** protocol bytes, the
input manifest, the query result, the competency questions and the selected
reading. It checks identities, the declared surface and its locators, witness
uniqueness, row coverage, the unresolvable-locator rule, coverage against
`required_semantics` and the derived label. It never chooses or changes a
judgment. Hand the completed record to Luis for ratification.
"""


def _section(text: str, heading: str) -> tuple[int, int]:
    """The span of one `## heading` section, up to the next heading or the end."""

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


def absence_codes() -> str:
    """The six codes and their definitions, read from the protocol file."""

    document = protocol()
    judgments = document["judgments"]
    order = list(judgments["coverage_absent_reasons"])
    definitions = judgments["coverage_absent_reason_definitions"]
    if sorted(order) != sorted(definitions):
        raise ReviewPackageRefusal(
            "the protocol's absence codes and their definitions do not agree"
        )
    if len(order) != 6:
        raise ReviewPackageRefusal(
            f"protocol v3.2 must declare six absence codes, not {len(order)}"
        )
    lines = []
    for code in order:
        body = f"- `{code}`: {definitions[code]}."
        lines.append(
            "\n".join(
                textwrap.wrap(
                    body,
                    width=76,
                    break_long_words=False,
                    break_on_hyphens=False,
                    subsequent_indent="  ",
                )
            )
        )
    return "\n".join(lines)


def subject_tie_rule() -> str:
    """The clarification's own rule section, quoted, with its path and digest."""

    text = CLARIFICATION.read_text(encoding="utf-8")
    marker = "\n## The rule\n"
    if text.count(marker) != 1:
        raise ReviewPackageRefusal("the clarification carries no single rule section")
    start = text.index(marker) + len(marker)
    following = text.find("\n## ", start)
    quoted = text[start : len(text) if following == -1 else following].strip("\n")
    head = SUBJECT_TIE_HEAD.format(
        path=str(CLARIFICATION.relative_to(ROOT)),
        sha256=_digest(CLARIFICATION.read_bytes()),
    )
    return head + "\n".join(
        ("> " + line) if line else ">" for line in quoted.splitlines()
    ) + "\n"


def checklist(kind: str = SURFACE_KIND) -> str:
    """The protocol's checklist, numbered, filtered to this surface kind."""

    section = protocol()["checklist"]
    entries = [item for item in section["checks"] if kind in item["applies_to"]]
    if not entries:
        raise ReviewPackageRefusal(f"the protocol lists no check for {kind}")
    lines = [CHECKLIST_HEAD.format(note=CHECKLIST_NOTE).rstrip("\n"), ""]
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


V3_ABSENT_REASONS = """- `NOT_MODELLED`: no record or field in the graph carries it.
- `WITHHELD_STATEMENT`: the claim's words carry it and the graph holds them as
  a locator and a digest only.
- `UNREACHED_RECORD`: the graph carries it and no case reaches the record.
- `NOT_IN_SOURCE`: the surface itself does not state it.
- `LOCATOR_NOT_RESOLVABLE`: the row that would carry it cites a locator that
  does not resolve."""


def build_task(ids: list[str], counts: dict[str, int] | None, witnesses: int | None) -> str:
    text = TASK_TEMPLATE.read_text(encoding="utf-8")
    start, _ = _section(text, "What you judge")
    text = PREAMBLE.format(
        run_id=RUN_ID,
        surface_kind=SURFACE_KIND,
        protocol_sha256=_digest(PROTOCOL.read_bytes()),
    ) + text[start:]
    text = _substitute(
        text,
        [
            (V3_ABSENT_REASONS, absence_codes()),
            (
                "{{ROWS_QUESTION_1}} rows for\n"
                "`{{QUESTION_ID_1}}`, {{ROWS_QUESTION_2}} for `{{QUESTION_ID_2}}`,\n"
                "{{ROWS_TOTAL}} in all",
                _enumeration(ids, counts) + ",\n{{ROWS_TOTAL}} in all",
            ),
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
                str((RESULTS / "trace-summary.json").relative_to(ROOT)),
            ),
            (
                "{{QUERY_TRACE_SUMMARY_PATH}}",
                str((RESULTS / "query-trace-summary.json").relative_to(ROOT)),
            ),
        ],
        "review task",
    )
    # The subject-tie rule sits between the judgements it governs and the
    # controls it decides, and the checklist opens the recording section.
    controls_at, _ = _section(text, "Controls")
    text = text[:controls_at] + subject_tie_rule() + text[controls_at:]
    text = _replace_section(
        text,
        "Recording",
        checklist()
        + RECORDING.format(
            run_id=RUN_ID, note=CHECKLIST_NOTE, record_schema=RECORD_SCHEMA
        ),
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
                "# Malleus paper v4 source-grounded review record, protocol v3\n",
                "# Malleus paper v4 source-grounded review record, protocol v3.2\n",
            ),
            (
                "Template. The question ids, the row counts and the witness count are\n"
                "substituted at freeze, from the frozen cell's own competency question"
                " file and\nquery result, at the same time as\n"
                "`paper-v4/evaluation-v4/review-task-protocol-v3.template.md`. No"
                " placeholder\nmay survive instantiation.",
                f"This is {RUN_ID}'s blank record, written by\n"
                f"`paper-v4/evaluation-v4/{RUN_ID}/build_review_inputs.py` from"
                " the frozen v3\ntemplate under protocol v3.2. The question ids are"
                " this cell's frozen\ncompetency question file's, in that file's"
                " order. The row and witness counts\nare figures of a producer that"
                " has not run and are filled by the same script\nat freeze; no other"
                " placeholder survives either stage.",
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
                '  "schema": "malleus.paper-v4.source-grounded-review/v3",',
                f'  "schema": "{RECORD_SCHEMA}",',
            ),
            (
                '    "review_protocol_sha256": "sha256:17b5744a71a1e6a9ab1985f43b3e28d4'
                'd683f2d7d369e7decdb375171c2edc21",',
                '    "review_protocol_sha256": "'
                + _digest(PROTOCOL.read_bytes())
                + '",',
            ),
            (
                '  "absent_reason": "NOT_MODELLED | WITHHELD_STATEMENT |'
                ' UNREACHED_RECORD | NOT_IN_SOURCE | LOCATOR_NOT_RESOLVABLE",',
                '  "absent_reason": "'
                + " | ".join(protocol()["judgments"]["coverage_absent_reasons"])
                + '",',
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
    """The distinct witnesses of the returned rows, which is what v3.2 judges.

    ``review.py`` counts the witness of every returned row and refuses a
    manifest whose figure differs. ``query-trace-summary.json`` counts every
    record the executor traced, and that includes a record reached only as
    another row's subject: the executor traces it so the reviewer has its
    evidence, but no row takes it as its witness and no reviewer judges it. The
    two figures coincided in run-22, run-23 and run-24 and differed by one in
    run-25, whose reviewer was refused for the sixth witness the package
    declared, so the figure is computed from the query result rather than read
    from the trace summary. ``_records_traced`` keeps the trace summary's own
    number, which this cell's launch log records beside this one.
    """

    result = json.loads((PRIVATE / "query/query-result.json").read_bytes())
    return len(
        {
            (row["witness"].get("relation_id") or row["witness"]["record_id"])
            for query in result["queries"]
            for row in query["rows"]
        }
    )


def _records_traced() -> int:
    summary = json.loads((RESULTS / "query-trace-summary.json").read_bytes())
    return int(summary["witnesses_traced"])


def build_manifest(ids: list[str], counts: dict[str, int], witnesses: int) -> dict:
    run_result = json.loads((RESULTS / "run-result.json").read_bytes())
    document = protocol()
    fixed_keys = document["fixed_identities"]["required_keys_by_surface_kind"][
        SURFACE_KIND
    ]
    stage_keys = document["stage_identities"]["required_keys_by_surface_kind"][
        SURFACE_KIND
    ]
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
    required = set(document["review_materials"]["required"][SURFACE_KIND])
    if not required <= set(by_name):
        raise ReviewPackageRefusal(
            f"the protocol requires materials this cell does not stage:"
            f" {sorted(required - set(by_name))}"
        )
    fixed = {
        "source_sha256": SOURCE_PDF_SHA256,
        "selected_reading_sha256": by_name["selected_reading"]["sha256"],
        "competency_questions_sha256": by_name["competency_questions"]["sha256"],
    }
    stage = {
        "accepted_ontology_sha256": run_result["ontology_sha256"],
        "ledger_head": run_result["ledger_head"],
        "replay_receipt_sha256": run_result["replay_receipt_sha256"],
        "query_binding_sha256": by_name["query_binding"]["sha256"],
        "query_result_sha256": by_name["query_result"]["sha256"],
        "query_trace_summary_sha256": by_name["query_trace_summary"]["sha256"],
        "population_trace_summary_sha256": by_name["population_trace"]["sha256"],
    }
    # The key sets are the protocol's for this surface kind, not this script's.
    for declared, expected, subject in (
        (fixed, fixed_keys, "fixed_identities"),
        (stage, stage_keys, "stage_identities"),
    ):
        if set(declared) != set(expected):
            raise ReviewPackageRefusal(
                f"{subject} must carry exactly {sorted(expected)} on {SURFACE_KIND}"
            )
    return {
        "schema": MANIFEST_SCHEMA,
        "status": "FROZEN_FOR_REVIEW",
        "run_id": RUN_ID,
        "review_protocol_sha256": _digest(PROTOCOL.read_bytes()),
        "evidence_surface": {"kind": SURFACE_KIND, "locator_kind": LOCATOR_KIND},
        "fixed_identities": fixed,
        "stage_identities": stage,
        "materials": materials,
        "question_ids": ids,
        # The manifest's key set is exact under review-protocol-v3.2.json, so the
        # executor's own traced-record count is not carried here. It is in
        # results/query-trace-summary.json, in this cell's launch log and in
        # _records_traced above; witnesses_traced is the validator's witness.
        "rows_per_question": counts,
        "witnesses_traced": witnesses,
        "authorship": dict(AUTHORSHIP),
    }


def execute(stage: str) -> dict[str, object]:
    ids = question_ids()
    counts = _rows_per_question(ids) if stage == "freeze" else None
    witnesses = _witnesses_traced() if stage == "freeze" else None
    HERE.mkdir(parents=True, exist_ok=True)
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
        print(
            f"review-package: {type(error).__name__}: {error}", file=sys.stderr
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

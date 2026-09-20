"""Build baseline-01's review package for the IN_CONTEXT_ANSWER_SET surface.

Four files and this script writes all four, so that no figure in any of them is
typed by hand: the v3.2 input manifest, the instantiated review task, the blank
record, and one review block per question. That is the shape
`paper-v4/evaluation-v4/run-25/build_review_inputs.py` uses, and the reason is
the same: run-05's task carried run-02's row counts on a wrapped line into a
live review.

Two stages, because the cell is opened before its producer runs.

``--stage open`` instantiates what exists at open: the run id, the surface, the
material paths and the thirty question ids of the frozen competency question
file, in that file's order. Every count is a figure of a producer that has not
run, so the count placeholders are left standing and this stage refuses if any
other placeholder survives.

``--stage freeze`` reads the producer's answer file, validates it with
``validate_answers.py`` first so that no package is built around a file the
grammar refuses, fills the counts, and writes the manifest.

What differs from a graph cell, and why the task is derived rather than copied:
the answer surface has no query result, no ledger, no replay receipt and no
trace, so seven of the v3 task's sections do not apply to it. They are replaced
here section by section, with the difference stated in the text the reviewer
reads, and the script refuses if a section it means to replace is not found, so
an edit to the v3 template is caught rather than silently ignored.

Nothing here judges anything. The controls in the question file are carried by
the file itself; the validator reports each control outcome as a finding after a
review exists, and this script neither reads nor writes an outcome.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import sys
import textwrap
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN_ID = "baseline-01"

EVALUATION = ROOT / "paper-v4/evaluation-v4"
PROTOCOL = EVALUATION / "review-protocol-v3.2.json"
TASK_TEMPLATE = EVALUATION / "review-task-protocol-v3.template.md"
BLANK_TEMPLATE = EVALUATION / "review-record-protocol-v3.blank.md"
PACKAGE = EVALUATION / RUN_ID
TASK = PACKAGE / "review-task.md"
BLANK = PACKAGE / "review-record.blank.md"
MANIFEST = PACKAGE / "review-input-manifest.json"

QUESTIONS = ROOT / "paper-v4/experiment-v4/competency-questions-v3.1.json"
SELECTED_READING = ROOT / "private/paper-v4-text-layer/selected-reading.json"
SPAWN_MESSAGE = HERE / "spawn-message.md"
ANSWER_FILE = ROOT / "private/paper-v4-baseline-01/producer/work/answers.json"
SOURCE_PDF_SHA256 = (
    "sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9"
)

SURFACE_KIND = "IN_CONTEXT_ANSWER_SET"
LOCATOR_KIND = "SELECTED_READING_BLOCK_ID"
ASSEMBLY = "NOT_APPLICABLE"
PLACEHOLDER = re.compile(r"\{\{[A-Z_0-9]+\}\}")
COUNT_PLACEHOLDERS = ("CLAIMS_", "CLAIMS_TOTAL", "WITNESSES_TOTAL", "MODEL_ID")

# The three materials protocol v3.2 requires of an answer-set cell, plus the
# producer's task, which the protocol permits and which the stage identity
# `producer_task_sha256` is the digest of.
MATERIALS = (
    ("selected_reading", SELECTED_READING, "PRIVATE"),
    ("competency_questions", QUESTIONS, "PUBLIC"),
    ("answer_file", ANSWER_FILE, "PUBLIC"),
    ("producer_task", SPAWN_MESSAGE, "PUBLIC"),
)

AUTHORSHIP = {
    "preliminary_evaluator_kind": "CLAUDE_PRELIMINARY",
    "ratifier_evaluator_kind": "HUMAN_AUTHOR",
    "ratifier_actor_id": "actor:luis",
}


class ReviewPackageRefusal(ValueError):
    """The package cannot be written from what is on disk."""


def _module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:  # pragma: no cover - import plumbing
        raise ReviewPackageRefusal(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


answers_validator = _module(HERE / "validate_answers.py", "baseline_validate_answers")


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def question_file() -> list[dict[str, Any]]:
    document = json.loads(QUESTIONS.read_bytes())
    if document["status"] != "FROZEN_BEFORE_V3_1_CELLS":
        raise ReviewPackageRefusal("the competency question file is not frozen")
    return list(document["questions"])


def question_ids() -> list[str]:
    return [str(item["id"]) for item in question_file()]


# --------------------------------------------------------------------------
# The producer's answer file
# --------------------------------------------------------------------------


def answer_set() -> dict[str, Any]:
    """The validated answer file, refused here rather than at review time."""

    if not ANSWER_FILE.is_file():
        raise ReviewPackageRefusal(
            "the producer has not written an answer file;"
            f" expected {ANSWER_FILE.relative_to(ROOT)}"
        )
    answers_validator.validate_answers(
        ANSWER_FILE.read_bytes(),
        SELECTED_READING.read_bytes(),
        QUESTIONS.read_bytes(),
    )
    return json.loads(ANSWER_FILE.read_bytes())


def _claims_per_question(document: dict[str, Any], ids: list[str]) -> dict[str, int]:
    counts = {
        str(item["question_id"]): len(item["claims"]) for item in document["answers"]
    }
    if sorted(counts) != sorted(ids):
        raise ReviewPackageRefusal("the answer file does not answer this cell's questions")
    return {question_id: counts[question_id] for question_id in ids}


def _witnesses_traced(document: dict[str, Any]) -> int:
    """The distinct claims the answer file cites, which is what v3.2 judges.

    Every claim id is unique by the answer grammar, so this is the claim count.
    It is computed rather than taken from the grammar's report so that the
    manifest's figure comes from the file the reviewer will open.
    """

    return len(
        {
            claim["claim_id"]
            for answer in document["answers"]
            for claim in answer["claims"]
        }
    )


# --------------------------------------------------------------------------
# The review task, derived from the v3 template
# --------------------------------------------------------------------------


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


def _enumeration(ids: list[str], counts: dict[str, int] | None) -> str:
    """``N claims for `CQ-…`,`` once per question, in the file's order."""

    parts = []
    for index, question_id in enumerate(ids):
        figure = (
            str(counts[question_id])
            if counts is not None
            else "{{CLAIMS_" + question_id.replace("-", "_").upper() + "}}"
        )
        noun = " claims" if index == 0 else ""
        parts.append(f"{figure}{noun} for `{question_id}`")
    return "\n".join(
        textwrap.wrap(", ".join(parts), width=76, break_long_words=False)
    )


PREAMBLE = """# Malleus paper v4 source-grounded review task, protocol v3.2, in-context answer set

This is {run_id}'s review task, written by
`paper-v4/experiment-v4/baseline-01/build_review_inputs.py` from the frozen v3
template at `paper-v4/evaluation-v4/review-task-protocol-v3.template.md`. Every
figure below is substituted from this cell's own frozen question file and answer
file; no placeholder survives instantiation.

Status: the method was frozen before the producer ran, at
`paper-v4/evaluation-v4/review-protocol-v3.2.json`. It is not edited for this
review. That file supersedes `review-protocol-v3.json` for cells opened after
it and changes three things:

- A third evidence surface kind, `IN_CONTEXT_ANSWER_SET`, whose locators are
  reading block ids like the text layer's and whose witness is one cited claim,
  keyed by its `claim_id`. There is no ledger, no replay receipt, no query
  binding and no trace on this surface, so there is no query result and the
  material you read in its place is the answer file.
- Stage identities are declared per surface kind. This cell binds three, and
  none of them is a ledger head: the answer file's digest, the producer's model
  id and the digest of the task the producer was given.
- A sixth absence code, `NOT_CAPTURED`, for an element the surface could carry
  and does not. On this surface it reads as "the answer set does not state it
  and declares no `NO_ANSWER_IN_SOURCE` for it".

**What this cell is.** It is not a Malleus cell. One fresh session was given the
selected reading and the thirty questions and asked to answer them in prose with
block citations. It ran no ontology, no compiler, no admission, no ledger and no
query. It is a baseline, and it exists to price what the typed path costs against
plain reading.

**One thing to hold on to while you judge.** This producer saw the questions.
Every graph producer was denied them. The comparison is tilted toward this cell
on purpose, which is what makes the result a price rather than a contest. Judge
this cell exactly as you would judge a graph cell; the tilt is the author's to
report, not yours to correct for.

You are a fresh Claude session performing the preliminary inspection. Record
your kind as `CLAUDE_PRELIMINARY`, which is the kind the protocol names; if you
are anything else, the substitution is recorded as a deviation in
`paper-v4/evaluation-v4/{run_id}/review-input-manifest.json`, which also binds
every input below by digest. Verify those digests before you begin. This is
AI-assisted preliminary work, not human evidence: Luis ratifies, and only a
record with status `HUMAN_RATIFIED` is evidence for the paper.
"""

WHAT_YOU_JUDGE = """
## What you judge

Two properties and nothing else: whether the block a claim cites supports that
claim, and which of each question's required semantics the answer's claims
carry. Do not calculate a score, construct a canonical answer, compare against
an oracle, judge the writing, or judge whether the answer is the one you would
have given.

Support is judged against the cited block and not the article around it. That
rule is unchanged from the graph cells, and it is the rule that makes the two
surfaces comparable on coverage.
"""

INPUTS = """
## Inputs, exactly these

Every one of them is a material in the input manifest, bound by digest.

- `{reading_path}`, the selected reading. You cite its block
  identifiers, and it is the only surface that supports anything here.
- `{questions_path}`, the questions and their `required_semantics`.
- `{answers_path}`, the producer's answer file. This is what
  you read where a graph cell's reviewer reads a query result. Its grammar is
  `paper-v4/experiment-v4/baseline-01/answer-file-schema.json`, and it has
  already been checked against that grammar: every claim cites at least one
  block the reading declares, and no answer or claim reproduces the reading.
- `{task_path}`, the message the producer was given.
- this task, the frozen protocol, the input manifest, the per-question review
  blocks in `paper-v4/evaluation-v4/{run_id}/`, and a copy of
  `paper-v4/evaluation-v4/{run_id}/review-record.blank.md`.

There is no query binding, no query result, no population trace, no query trace
summary and no retained capture in this cell, because no stage that produces one
ran. A manifest on this surface that bound one would be refused.

Do not open an answer oracle, a canonical answer, a prior score, a scorer, a
model transcript, another cell's population file or query result, a session log,
the manuscript, a result-bearing paper ledger entry, or any external source. The
source PDF is optional and may be opened only to cross-check whether the text
layer projected a passage faithfully; it is not a second evidence surface.

You have no network.
"""

WITNESS = """
## What a witness is

One cited claim, keyed by its `claim_id`. The answer file carries, per question,
an answer text and a list of claims; each claim is one sentence-level assertion
with the reading blocks it rests on. The `claim_id` is the witness key you write
in the record, and the rows of a question are its claims in the file's order.

Two differences from a graph cell follow, and both matter:

- **No two claims share an identity.** On a graph surface two rows carrying the
  same `record_id` are one witness, judged once. Here, two answers stating the
  same fact carry two claim ids and are two witnesses. The witness count is
  therefore not comparable with a graph cell's, and the protocol says so. Only
  coverage of the authored elements is comparable.
- **Assembly is not applicable.** A prose answer always assembles, so the
  descriptor would be constant, and a constant token in a comparison table reads
  as a grade. Write `NOT_APPLICABLE` for every question; the validator accepts
  nothing else on this surface.

A question whose answer declares `no_answer_in_source` carries no claim and so
has no row. Its coverage entries all take an absent reason.

## How a witness reaches the surface

Directly. The claim names its own blocks in the answer file, and each of those
is a block id of the selected reading. Open the block, read it, and judge the
claim against it. There is no trace to look a witness up in and no locator to
resolve under a convention, because nothing was derived: the producer wrote a
sentence and named the blocks it read it from.

Cite in the record, for every witness, at least the blocks that claim itself
cites. The validator refuses a witness that omits one of them, because the claim
is judged against the block it rests on. You may cite more, when a neighbouring
block is what decides the judgement, and say so in the rationale.
"""

CHECKS = """
## The checks, and where each applies

There is one check per witness on this surface, and it is the judgement itself.
The graph cells' mechanical checks do not apply here and you do not write their
tokens: there is no `resolution`, because there is no row to open; no statement
digest, because nothing binds a statement by digest; no derivation locality,
because no relation was derived; and no subject-present token, because there is
no subject slot.

Begin each `rationale` with the fact that decides it, in your own words, and
then the reason. Where a claim is broader than the block it cites, say which
part the block carries and which it does not; that is what separates `PARTIAL`
from `SUPPORTED` here.

One thing this cell cannot establish, and it is worth holding while you judge:
a prose answer can cite a block and still have been composed from the model's
memory of the article. Nothing in this cell excludes that. You judge whether the
cited block supports the claim, which is a different and smaller question, and
zero `UNSUPPORTED` here would not mean the answers were grounded.
"""

JUDGMENTS = """
## Judgments

Per witness, choose one `source_support`:

- `SUPPORTED`: the cited block supports every material claim in the statement.
- `PARTIAL`: it supports some but not all of it, or a needed qualifier is
  absent.
- `UNSUPPORTED`: it contradicts the statement or supplies no support for it.
- `NOT_EVALUABLE`: the allowed source surface is insufficient to decide.

Per question, you do not choose a label. You fill `coverage`: one entry per item
of that question's `required_semantics`, in the question file's order. For each
item, either name the `row_index` of a claim whose witness is `SUPPORTED` and
whose statement carries that item; or write `null` there and one
`absent_reason`:

- `NOT_CAPTURED`: the answer could have stated it and does not, and the answer
  declares no `NO_ANSWER_IN_SOURCE` for that question.
- `NOT_IN_SOURCE`: the reading itself does not state it.
- `NOT_MODELLED`: reserved for a surface with a contract; it does not arise
  here, since a prose answer has no type and no slot.
- `WITHHELD_STATEMENT`: the element is inside the answer's prose and no claim
  states it, so no witness carries it.
- `UNREACHED_RECORD` and `LOCATOR_NOT_RESOLVABLE` do not arise on this surface.

Then write the `question_responsiveness` the derivation produces:

- `COVERED`: every required semantic names a row.
- `PARTIAL`: some do and some are absent.
- `NONE`: none does.

The validator recomputes it and refuses a label its derivation does not produce.
Write the reason for the absences in `responsiveness_rationale`, in your own
words. Write `NOT_APPLICABLE` for `assembly` on every question.

Judge every claim exactly once, in order: {enumeration},
{{{{CLAIMS_TOTAL}}}} in all, over {{{{WITNESSES_TOTAL}}}} distinct claims. Cite at
least one locator per witness and per question. Write each reason in your own
words. Copy no source passage into the record beyond the locator, and add no
numerical aggregate.
"""

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
question's claims and its required semantics; fill one and assemble them into
the record's `questions` array in the question file's order.

Then run the paper gate:

```
.venv/bin/python paper-v4/run_active_tests.py
```

and validate your own record with `validate_review` in
`paper-v4/evaluation-v4/review.py`, passing the v3.2 protocol bytes, the input
manifest, the competency questions, the selected reading, and the answer file as
`answer_set_source`. There is no `query_result_source` on this surface. It
checks identities, the claims against the reading, witness uniqueness and row
coverage, that every witness cites the blocks its claim cites, coverage against
`required_semantics` and the derived label. It never chooses or changes a
judgment. Hand the completed record to Luis for ratification.
"""


def checklist(kind: str = SURFACE_KIND) -> str:
    """The protocol's checklist, numbered, filtered to this surface kind."""

    protocol = json.loads(PROTOCOL.read_bytes())
    section = protocol["checklist"]
    entries = [
        item for item in section["checks"] if kind in item["applies_to"]
    ]
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


def build_task(ids: list[str], counts: dict[str, int] | None, witnesses: int | None) -> str:
    text = TASK_TEMPLATE.read_text(encoding="utf-8")
    start, _ = _section(text, "What you judge")
    text = PREAMBLE.format(run_id=RUN_ID) + text[start:]
    text = _replace_section(text, "What you judge", WHAT_YOU_JUDGE)
    text = _replace_section(
        text,
        "Inputs, exactly these",
        INPUTS.format(
            run_id=RUN_ID,
            reading_path=SELECTED_READING.relative_to(ROOT),
            questions_path=QUESTIONS.relative_to(ROOT),
            answers_path=ANSWER_FILE.relative_to(ROOT),
            task_path=SPAWN_MESSAGE.relative_to(ROOT),
        ),
    )
    # "How a witness reaches the surface" first: WITNESS carries a section of
    # that name, and replacing it earlier would leave two and refuse.
    text = _replace_section(text, "How a witness reaches the surface", "")
    text = _replace_section(text, "The three kinds of row", WITNESS)
    text = _replace_section(text, "The checks, and where each applies", CHECKS)
    text = _replace_section(
        text, "Judgments", JUDGMENTS.format(enumeration=_enumeration(ids, counts))
    )
    text = _replace_section(
        text, "Recording", checklist() + RECORDING.format(run_id=RUN_ID)
    )
    if counts is not None:
        text = text.replace("{{CLAIMS_TOTAL}}", str(sum(counts.values())))
    if witnesses is not None:
        text = text.replace("{{WITNESSES_TOTAL}}", str(witnesses))
    _refuse_surviving(text, "review task", counts_allowed=counts is None)
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
# The blank record, derived from the v3 blank
# --------------------------------------------------------------------------


BLANK_PREAMBLE = """# Malleus paper v4 source-grounded review record, protocol v3.2, in-context answer set

This is {run_id}'s blank record, written by
`paper-v4/experiment-v4/baseline-01/build_review_inputs.py` from the frozen v3
template. The question ids are this cell's frozen competency question file's, in
that file's order. The claim counts are the producer's answer file's.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Write one `witnesses` entry per claim the answer file cites,
{{{{WITNESSES_TOTAL}}}} in all. Claim ids are unique, so no witness is shared and
none is judged twice. Claims: {enumeration},
{{{{CLAIMS_TOTAL}}}} in all.

Three things the validator derives or forbids, so that writing them wrong is
refused rather than recorded:

- `question_responsiveness` is derived from `coverage`. Write the label the
  derivation produces, `COVERED` when every required semantic names a row,
  `NONE` when none does, `PARTIAL` otherwise. A label the derivation does not
  produce is refused.
- `assembly` is `NOT_APPLICABLE` on this surface, on every question. A prose
  answer always assembles, so the descriptor would be constant, and a constant
  token in a comparison table reads as a grade.
- A witness must cite every block its claim cites in the answer file. Support is
  judged against the cited block, not the article around it.

No witness carries `resolution` on this surface and every locator is a reading
block id. Copy no source passage into this record beyond the locator, and add no
numerical aggregate.

```json
{record}
```

Each `witnesses` entry has this shape:

```
{{
  "witness_key": "CQ-T1-01:c1",
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "source_locators": ["page:2:block:004"],
  "rationale": "one or two sentences in your own words"
}}
```

Each `rows` entry names one claim of that question and the witness it is:

```
{{
  "row_index": 0,
  "witness_key": "CQ-T1-01:c1"
}}
```

Each `coverage` entry names one required semantic and either the claim that
carries it or one typed reason it is absent:

```
{{
  "semantic": "instrument_count",
  "row_index": 3,
  "absent_reason": null,
  "note": ""
}}

{{
  "semantic": "instrument_count",
  "row_index": null,
  "absent_reason": "NOT_CAPTURED | NOT_IN_SOURCE | WITHHELD_STATEMENT | NOT_MODELLED",
  "note": "why, in your own words"
}}
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


def build_blank(ids: list[str], counts: dict[str, int] | None, witnesses: int | None) -> str:
    # The v3 blank is read so that a template this cell no longer matches is a
    # refusal rather than a silent divergence: its JSON block is the shape this
    # record keeps, minus the schema, the assembly token and the absent reasons.
    template = BLANK_TEMPLATE.read_text(encoding="utf-8")
    if '"schema": "malleus.paper-v4.source-grounded-review/v3"' not in template:
        raise ReviewPackageRefusal("the v3 blank template no longer declares its schema")
    text = BLANK_PREAMBLE.format(
        run_id=RUN_ID,
        enumeration=_enumeration(ids, counts),
        record=json.dumps(_blank_record(ids), ensure_ascii=False, indent=2),
    )
    if counts is not None:
        text = text.replace("{{CLAIMS_TOTAL}}", str(sum(counts.values())))
    if witnesses is not None:
        text = text.replace("{{WITNESSES_TOTAL}}", str(witnesses))
    _refuse_surviving(text, "blank review record", counts_allowed=counts is None)
    return text


# --------------------------------------------------------------------------
# The per-question review blocks
# --------------------------------------------------------------------------


def build_blocks(document: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    """One working surface per question: its claims, its semantics, no judgment."""

    by_id = {str(item["question_id"]): item for item in (document or {}).get("answers", [])}
    blocks: dict[str, dict[str, Any]] = {}
    for question in question_file():
        question_id = str(question["id"])
        answer = by_id.get(question_id)
        claims = list(answer["claims"]) if answer is not None else []
        blocks[question_id] = {
            "question_id": question_id,
            "question": question["question"],
            "required_semantics": list(question["required_semantics"]),
            "no_answer_in_source": (
                bool(answer["no_answer_in_source"]) if answer is not None else None
            ),
            "claims": [
                {"claim_id": claim["claim_id"], "blocks": list(claim["blocks"])}
                for claim in claims
            ],
            "question_responsiveness": "PENDING",
            "responsiveness_rationale": "",
            "assembly": ASSEMBLY,
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
                {"row_index": index, "witness_key": claim["claim_id"]}
                for index, claim in enumerate(claims)
            ],
        }
    return blocks


# --------------------------------------------------------------------------
# The v3.2 input manifest
# --------------------------------------------------------------------------


def build_manifest(
    ids: list[str], counts: dict[str, int], witnesses: int, document: dict[str, Any]
) -> dict[str, Any]:
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
        # No ledger head, no replay receipt, no query binding and no trace: the
        # baseline ran no stage that produces one, and protocol v3.2 declares
        # this surface's three identities instead of the graph surfaces' seven.
        "stage_identities": {
            "answer_file_sha256": by_name["answer_file"]["sha256"],
            "producer_model_id": str(document["producer_model_id"]),
            "producer_task_sha256": by_name["producer_task"]["sha256"],
        },
        "materials": materials,
        "question_ids": ids,
        "rows_per_question": counts,
        "witnesses_traced": witnesses,
        "authorship": dict(AUTHORSHIP),
    }


# --------------------------------------------------------------------------


def execute(stage: str) -> dict[str, object]:
    ids = question_ids()
    document = answer_set() if stage == "freeze" else None
    counts = _claims_per_question(document, ids) if document is not None else None
    witnesses = _witnesses_traced(document) if document is not None else None

    PACKAGE.mkdir(parents=True, exist_ok=True)
    TASK.write_text(build_task(ids, counts, witnesses), encoding="utf-8")
    BLANK.write_text(build_blank(ids, counts, witnesses), encoding="utf-8")
    blocks = build_blocks(document)
    for question_id, block in blocks.items():
        (PACKAGE / f"review-block.{question_id}.json").write_bytes(
            json.dumps(block, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
        )
    written: dict[str, object] = {
        "stage": stage,
        "questions": len(ids),
        "task": str(TASK.relative_to(ROOT)),
        "blocks": len(blocks),
    }
    if document is not None:
        assert counts is not None and witnesses is not None
        manifest = build_manifest(ids, counts, witnesses, document)
        MANIFEST.write_bytes(
            json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
        )
        written["claims_total"] = sum(counts.values())
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
        print(f"review-package: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

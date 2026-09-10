"""Drive the run-24 harness end to end on the neutral inspection-note fixture.

The fixture is Core's own synthetic document-capture conformance corpus. No paper
reading, ontology, capture or result enters this test, and no model runs.

Neither the producer condition nor the harness has a delta of any kind, and the
question file has one. Run-24's producer block is run-23's key for key, the
three model fields included, its spawn message is run-23's with the run id
moved, and its eight declared inputs are the same bytes staged the same way at
the same Core commit. v4.13 does not move: the binder, the executor and the
offline validation are run-23's bytes. What moves is the question file, and it
moves in one place, ``paper-v4/evaluation-v4/run-24/build_review_inputs.py``,
which binds ``competency-questions-v3.1.json`` where run-23's bound v3.

Eight files and the spawn message are run-23's with the run id substituted and
nothing else, and ``pin.py`` is too once its reference cell moves. Every one of
them is read through a table stated once here and reversed, so everything
outside a stated table must reach run-23's bytes exactly and an edit riding
inside a run id move fails here rather than travelling with the cell.

Core-19 and Core-20 are carried from run-23 and are not carried unread: the pin
still reads them at the commit run-23 pinned, against the same v4.8 baseline,
and both must come back LANDED. Their evidence is a commit and not a file in
this directory, so this file checks only that the pin can still refuse either
and that a pre-flight paragraph missing one refusal reason reads PENDING rather
than LANDED; what the adapter and the skill carry at the pinned commit is
``test_contract.py``'s.

``bind_from_surface.py`` is exercised end to end on a fixture that carries a
``subject`` reference, and that fixture is where the carried reachability rules
are driven twice. With both types listed, the bearing type still gets no plain
ENTITY case, a record of it that carries no subject comes back as one ENTITY row
from the ENTITY_NO_SUBJECT case, and the record that does carry one comes back
as a single SUBJECT row with two ordinals, because the typed SUBJECT case and
the SUBJECT_ANY case both reach it. With the bearing type listed alone, which is
the shape run-22's CQ-T4-01 had, the subject's type is nowhere in the set and
the record is returned anyway. The fixture's subject entity carries ``tags``, so
v4.7's carried SUBJECT_TAGS_PROJECTED delta is exercised on the same run as
everything else. All of it is run-23's behaviour, driven here so that carrying
the binder is carrying what it does and not only its bytes.

The question file is read as a file: v3.1 is v3 with CQ-C-03's required
semantics reduced to three, the other twenty-nine questions byte-identical, and
the contract pins its digest.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from hashlib import sha256
from importlib.resources import files
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Iterator

import pytest
import yaml


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN_02 = HERE.parent / "run-02"
RUN_03 = HERE.parent / "run-03"
RUN_04 = HERE.parent / "run-04"
RUN_05 = HERE.parent / "run-05"
RUN_06 = HERE.parent / "run-06"
RUN_07 = HERE.parent / "run-07"
RUN_08 = HERE.parent / "run-08"
RUN_09 = HERE.parent / "run-09"
RUN_22 = HERE.parent / "run-22"
RUN_23 = HERE.parent / "run-23"
PRIVATE = ROOT / "private"
QUESTIONS_V3_1 = HERE.parent / "competency-questions-v3.1.json"
QUESTIONS_V3 = HERE.parent / "competency-questions-v3.json"
REVIEW_PACKAGE = ROOT / "paper-v4/evaluation-v4/run-24"
PRIOR_REVIEW_PACKAGE = ROOT / "paper-v4/evaluation-v4/run-23"
FIXTURE = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "inspection_note_capture_v1"
)
LINKML_TYPES = Path(
    str(
        files("linkml_runtime").joinpath(
            "linkml_model", "model", "schema", "types.yaml"
        )
    )
)
TRANSACTION_TIME = "2026-09-04T00:00:00Z"
ACTOR = "actor:paper-v4-run-24"
SPAWN_MESSAGE = HERE / "spawn-message.md"
CONTRACT_PATH = HERE / "run-contract.json"
OFFLINE_VALIDATION = HERE / "offline-validation.json"

# The one sentence STOP_RULE_CLARIFIED adds to run-04's message.
STOP_RULE_SENTENCE = (
    "Reviewing the next block is not invention; stop only when every block is"
    " REVIEWED or listed in `nothing_assertable`, or when the next addition"
    " would require invention."
)

# The ten changes Core owns. Their evidence is a commit, not a file in this
# directory, so ``pin.py`` records what landed and test_contract recomputes it;
# there is nothing here to grep for. All ten are carried from run-23. Eight of
# them stop at the coordinate run-23 pinned Core-18 at and read
# CARRIED_FROM_RUN_23 and nothing else; Core-19 and Core-20 are carried too but
# are still read, at the commit run-23 pinned and against the same v4.8
# baseline, so those two read LANDED or PENDING_AT_PIN.
CORE_CHANGE_IDS = (
    "CORE_12_DERIVATION_CHECKS",
    "CORE_14_MODALITY_SOURCE_OF_TRUTH",
    "CORE_15_SUBJECT_ALIASES",
    "CORE_16_PROJECTED_SUBJECT",
    "CORE_17_PROJECTION_WITHDRAWN",
    "CORE_18_NAME_AS_WORD",
    "CORE_19_HONEST_REPORTING",
    "CORE_20_REFUSAL_LIST_PREFLIGHT",
    "PACKS_0_3_0",
    "SUBJECT_ELEMENT",
)
# The two the pin still reads rather than carries unread. They are run-18's
# entries, carried through run-19, run-20, run-21, run-22 and run-23, and carry
# ``carried_from: run-23``; what is not carried is the status, which the pin
# recomputes from the bytes at the pinned commit.
READ_AT_THE_PIN_CORE_CHANGE_IDS = (
    "CORE_19_HONEST_REPORTING",
    "CORE_20_REFUSAL_LIST_PREFLIGHT",
)
CARRIED_PIN_STATUS = "CARRIED_FROM_RUN_23"
READ_AT_THE_PIN_STATUSES = {"LANDED", "PENDING_AT_PIN"}
CORE_PIN_STATUSES = {CARRIED_PIN_STATUS} | READ_AT_THE_PIN_STATUSES

# The eight files this cell carries with the run id moved and nothing else,
# read through RUN_ID_SUBSTITUTIONS, which reverse. v4.13 does not move under
# this cell, so the three files run-23 changed are carried the way the five it
# carried are, and the list of files that carry a change of their own is empty.
RUN_ID_SUBSTITUTIONS = (
    (
        "run-23",
        "run-24",
    ),
    (
        "Run-23",
        "Run-24",
    ),
    (
        "run_23",
        "run_24",
    ),
)
CARRIED_WITH_THE_RUN_ID = (
    "bind_from_surface.py",
    "compile_ontology_candidate.py",
    "native_query.py",
    "offline_validation.py",
    "prepare_producer.py",
    "run.py",
    "spawn-message.md",
    "usage_from_launch_log.py",
)


# ``pin.py`` names the cell it carries from, so it takes two tables after the
# run id move. The first steps the reference cell from run-22 to run-23, the
# carried status with it, and the interface ordinal from 23 to 24, and repairs
# the three passages the blanket move would otherwise make untrue; the protocol
# version is not in it, because v4.13 does not move under this cell. The second
# gives run-22's own marked blocks their markers back: a marker names the cell
# that wrote the block, the reference-cell move would put run-23's name on
# run-22's four, and this cell adds no block of its own.
PIN_REFERENCE_CELL = (
    (
        "run-22",
        "run-23",
    ),
    (
        "RUN_22",
        "RUN_23",
    ),
    (
        'INTERFACE_ORDINAL = "23"',
        'INTERFACE_ORDINAL = "24"',
    ),
    (
        "Core does not move under this cell and the harness does: v4.13 is where it moves\n"
        "to. This pins the commit run-23 pinned, so its thirty-four carried entries still\n"
        "read at fixed coordinates, the v4.1 baseline\n",
        "Core does not move under this cell and neither does the harness: v4.13 stays\n"
        "where run-23 took it. This pins the commit run-23 pinned, so its thirty-five\n"
        "carried entries still read at fixed coordinates, the v4.1 baseline\n",
    ),
    (
        "# through run-19, run-20, run-21 and run-23 and read again at the commit\n"
        "# run-23 pinned.\n",
        "# through run-19, run-20, run-21, run-22 and run-23 and read again at the\n"
        "# commit run-23 pinned.\n",
    ),
    (
        "    # Carried from run-23, and before that from run-21, run-20, run-19,\n"
        "    # run-18, run-17, run-16, run-15 and run-14, where it was the change\n"
        "    # under test.",
        "    # Carried from run-23, and before that from run-22, run-21, run-20,\n"
        "    # run-19, run-18, run-17, run-16, run-15 and run-14, where it was the\n"
        "    # change under test.",
    ),
)
PIN_RUN_22_ADDITION_MARKERS = (
    "the canonical-staging table",
    "the canonical bytes beside the canonical digest",
    "the cause of every moved input",
    "the staged bytes beside the source bytes",
)
PIN_MARKERS_KEPT = tuple(
    (f"# run-23 addition {edge}: {label}\n", f"# run-22 addition {edge}: {label}\n")
    for label in PIN_RUN_22_ADDITION_MARKERS
    for edge in ("begins", "ends")
)


# ``build_review_inputs.py`` is the one file this cell changes, and it takes
# one table after the run id move: the question file it binds, and the frozen
# status string that file carries. The table reverses, so undo it and then the
# run id table and run-23's builder comes back byte for byte; an edit in
# neither fails here rather than travelling with the cell.
BUILDER_V3_1 = (
    (
        'QUESTIONS = ROOT / "paper-v4/experiment-v4/competency-questions-v3.json"',
        'QUESTIONS = ROOT / "paper-v4/experiment-v4/competency-questions-v3.1.json"',
    ),
    (
        '    if document["status"] != "FROZEN_BEFORE_V3_CELLS":\n',
        '    if document["status"] != "FROZEN_BEFORE_V3_1_CELLS":\n',
    ),
)


# The one change this cell states, and the file it lands in. The list is closed:
# a second change, or a change in a file no entry names, fails the statement
# below rather than arriving unannounced. Nothing in this directory is in it:
# the harness is run-23's and the change is which question file the cell binds.
RUN_24_CHANGES = {
    "QUESTIONS_V3_1_CQ_C_03_EXCLUDED_SURFACE_ONLY": (
        "paper-v4/evaluation-v4/run-24/build_review_inputs.py",
    ),
}
ENTITY_NO_SUBJECT = "ENTITY_NO_SUBJECT"
SUBJECT_ANY = "SUBJECT_ANY"
BINDING_SCHEMA_V6 = "malleus.paper-v4.native-query-binding/v6"
BINDING_SCHEMA_V5 = "malleus.paper-v4.native-query-binding/v5"

# The five blocks run-18 added to run-17's pin and the four run-22 added to
# run-21's, each still delimited in ``pin.py`` by its own marker pair. This cell
# adds none: a marker names the cell that wrote the block, so run-18's still say
# run-18 and run-22's still say run-22 after the two moves, which is what
# PIN_MARKERS_KEPT puts back.
PIN_ADDITION_MARKERS = (
    "the Core-19 and Core-20 constants",
    "the readers Core-19 and Core-20 are pinned by",
    "the Core-19 and Core-20 entries",
    "this cell's own entries in the gate status",
    "the Core-19 and Core-20 report keys",
)
ADDITION_BEGINS = "# run-18 addition begins: "
ADDITION_ENDS = "# run-18 addition ends: "
RUN_22_ADDITION_BEGINS = "# run-22 addition begins: "
RUN_22_ADDITION_ENDS = "# run-22 addition ends: "

# The Core coordinate run-17 pinned, which is the baseline the two carried
# Core-19 and Core-20 entries are read against and the commit every other
# carried Core entry still stops at.
V4_9_COORDINATE = "dc5254795a78648591d3a1b0bcf602af8d443dc1"
# The producer block's three model fields. This cell moves none of them, and it
# moves no other key either: test_contract.py compares run-24's producer block
# to run-23's key by key and requires no difference at all. Run-23's own model
# entry, run-21's, run-19's, run-18's and run-17's are carried beside this
# cell's as the closed cells' records, their subjects those cells' producer
# blocks and not this one's, so none is a harness marker and none is this cell's
# change.
MODEL_CHANGE_ID = "OPUS_5_REPLICATE_AT_V4_13"
PRIOR_MODEL_CHANGE_IDS = (
    "HAIKU_4_5_PRODUCER_AT_V4_9",
    "HAIKU_4_5_PRODUCER_AT_V4_10",
    "OPUS_5_PRODUCER_AT_V4_10",
    "OPUS_5_REPLICATE_AT_V4_10",
    "OPUS_5_REPLICATE_AT_V4_12",
    "SONNET_5_PRODUCER_AT_V4_9",
    "SONNET_5_PRODUCER_AT_V4_10",
)
MODEL_FIELDS = {
    "requested_model": "opus",
    "model_family": "Claude Opus 5",
    "model_id": "claude-opus-5",
}
# Run-23's, and they are the same three. A replicate that moved one of them
# would be a matrix cell, not a replicate, and the equality below is where that
# would fail. Neither the producer condition nor the harness moves under this
# cell, which is what makes its rows comparable with run-23's on every side and
# with run-20's, run-21's and run-22's on the producer side.
PRIOR_MODEL_FIELDS = {
    "requested_model": "opus",
    "model_family": "Claude Opus 5",
    "model_id": "claude-opus-5",
}

# The nineteen changes the instruments own, each with the file that carries it
# and one string that cannot be there unless the change is. Eighteen are carried
# from run-23 and their markers are in bytes this cell copied; the last is this
# cell's own and its marker is in the review package builder, which is the one
# file where binding v3.1 rather than v3 is written down. The producer sees none
# of them.
DELTA_MARKERS = {
    "BINDING_FROZEN_AT_ACCEPTANCE": (
        "paper-v4/experiment-v4/run-24/bind_from_surface.py",
        '"bound_at_stage": BOUND_AT_STAGE,',
    ),
    "GATE_SURFACES_CHAINED_CAUSE": (
        "paper-v4/experiment-v4/run-24/compile_ontology_candidate.py",
        '"cause_chain": chain,',
    ),
    "INTERPRETER_PREFLIGHT": (
        "paper-v4/experiment-v4/run-24/prepare_producer.py",
        "def preflight() -> dict[str, object]:",
    ),
    "LAUNCH_LOG_V2": (
        "paper-v4/experiment-v4/run-24/usage_from_launch_log.py",
        'LOG_SCHEMA = "malleus.paper-v4.producer-launch-log/v2"',
    ),
    "PUBLIC_COST_RECORD": (
        "paper-v4/experiment-v4/run-24/usage_from_launch_log.py",
        'USAGE_SCHEMA = "malleus.paper-v4.producer-usage/v1"',
    ),
    "QUERY_CASE_KINDS_V3": (
        "paper-v4/experiment-v4/run-24/native_query.py",
        "_ROWS_BY_KIND = {",
    ),
    "REVIEW_PROTOCOL_V2": (
        "paper-v4/evaluation-v4/review-protocol-v2.json",
        '"query_trace_summary"',
    ),
    "REVIEW_TASK_V2": (
        "paper-v4/evaluation-v4/review-task.template.md",
        "{{WITNESS_COUNT}}",
    ),
    "REVIEW_TASK_V3": (
        "paper-v4/evaluation-v4/review-task-v3.template.md",
        "SUBJECT_IN_BLOCK",
    ),
    "REVIEW_TASK_V4": (
        "paper-v4/evaluation-v4/review-task-v4.template.md",
        "**Derivation locality, `RELATION` rows only.**",
    ),
    "STOP_RULE_CLARIFIED": (
        "paper-v4/experiment-v4/run-24/spawn-message.md",
        "Reviewing the next block is",
    ),
    "SUBJECT_TAGS_PROJECTED": (
        "paper-v4/experiment-v4/run-24/native_query.py",
        'SUBJECT_TAGS_SLOT = "tags"',
    ),
    "ENTITY_KIND_RESTRICTED": (
        "paper-v4/experiment-v4/run-24/bind_from_surface.py",
        "unattached = [name for name in types if name not in set(bearing)]",
    ),
    "ONE_ROW_PER_WITNESS_OWN_TYPE_PROJECTION": (
        "paper-v4/experiment-v4/run-24/native_query.py",
        "def surface_projections(binding: dict[str, object])"
        " -> dict[str, list[str]]:",
    ),
    "ENTITY_NO_SUBJECT_REACHABILITY": (
        "paper-v4/experiment-v4/run-24/native_query.py",
        "def _entity_no_subject_rows(",
    ),
    "TYPE_SET_CLOSURE_AT_BIND_TIME": (
        "paper-v4/experiment-v4/run-24/bind_from_surface.py",
        "def refuse_unclosed(",
    ),
    "CANONICAL_PROFILE_STAGING": (
        "paper-v4/experiment-v4/run-24/prepare_producer.py",
        "def staged_bytes(item: dict[str, object], data: bytes) -> bytes:",
    ),
    "SUBJECT_ANY_REACHABILITY": (
        "paper-v4/experiment-v4/run-24/bind_from_surface.py",
        '                    "kind": SUBJECT_ANY,',
    ),
    "QUESTIONS_V3_1_CQ_C_03_EXCLUDED_SURFACE_ONLY": (
        "paper-v4/evaluation-v4/run-24/build_review_inputs.py",
        'QUESTIONS = ROOT / "paper-v4/experiment-v4/competency-questions-v3.1.json"',
    ),
}

CAPTURE_ID = "capture:inspection-note"
PLAN_ID = "plan:inspection-note:1"
SOURCE_ID = "source:inspection-note"
ARTIFACT_ID = "artifact:inspection-note"

# Core owns the governed-history machine, its policy, its binding, its check
# outcome and its event bytes. Paper code that names any of them has stopped
# being an adopter and started hand-assembling Core's protocol. The tokens are
# spelled in halves so this guard cannot match itself.
FORBIDDEN_SYMBOLS = (
    "Protocol" + "MachineProgram",
    "Policy" + "Program",
    "KnowledgeChange" + "HistoryBinding",
    "CHECK_" + "RECORDED",
    "machine_" + "events",
)

# The Event half of this test. The shared fixture declares no Event type, so the
# test adds one to its own ontology bytes and never edits the fixture.
EVENT_TYPE = "MaintenanceEvent"
EVENT_RECORD_ID = "maintenance-event:P-7:2026-03-02"

# The SUBJECT half. The fixture declares no subject reference, so the test adds
# one to its own ontology bytes and never edits the fixture.
SUBJECT_SLOT = "subject"
# The closure half. The fixture declares no subclass of a project class, so the
# test declares one on its own copy of the ontology and never edits the fixture.
SUBTYPE = "ProbeInspection"
SUBJECT_RECORD_ID = "inspection:P-7:2026-03-02"
# The reachability half. A second record of the same bearing type that names no
# subject: v4.4 reached it with no case at all and v4.12 reaches it once, as an
# ENTITY row of its own type.
UNATTACHED_RECORD_ID = "inspection:P-9:2026-03-04"
UNATTACHED_INSPECTED_ON = "2026-03-04"
SUBJECT_TARGET_ID = "asset:P-7"
# The carried v4.7 delta needs a subject that carries ``tags``. The fixture's asset does
# not, and the fixture is Core's and is read, never written, so the test writes
# the slot on its own copy of the records exactly as it writes the subject.
SUBJECT_TAGS_SLOT = "tags"
SUBJECT_TARGET_TAGS = ["P-7", "Pump 7"]
ROOT_PARENTS = ("Entity", "Event", "Relation", "Signal")
GROUNDING = {
    "tag": "grounding",
    "value": {
        "area": "Industrial maintenance and reliability",
        "taxonomy": "DDC 620.0046",
        "vocabularies": [
            {
                "vocabulary": (
                    "ISO 14224:2016 Collection and exchange of reliability and"
                    " maintenance data for equipment"
                ),
                "vocabulary_url": "https://www.iso.org/standard/64076.html",
                "borrowed_terms": ["equipment unit", "maintenance action"],
            }
        ],
        "invented_terms": [],
    },
}


def _module(name: str):
    path = HERE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"paper_v4_run_24_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _binder_of(cell: Path, name: str, module: str = "bind_from_surface"):
    """An earlier cell's module, read and never written."""
    path = cell / f"{module}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_23_binder():
    """Run-23's binder: this cell has no delta, so it is the same expansion."""
    return _binder_of(RUN_23, "paper_v4_run_23_binder")


def _run_09_binder():
    """Run-09's binder, the cell before the carried ENTITY restriction."""
    return _binder_of(RUN_09, "paper_v4_run_09_binder")


def _identity(case: dict) -> tuple[str, ...]:
    """A case's kind and its types, which is all a type-only case is."""
    if case["kind"] in {"ENTITY", ENTITY_NO_SUBJECT}:
        return (case["kind"], case["record_type"])
    if case["kind"] == "RELATION":
        return (
            "RELATION",
            case["source_record_type"],
            case["relation_record_type"],
            case["target_record_type"],
        )
    return (case["kind"], case["record_type"], case["subject_record_type"])


def _identities(cases: list[dict]) -> set[tuple[str, ...]]:
    return {_identity(case) for case in cases}


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _plain(text: str) -> str:
    return " ".join(text.split())


def _span(text: str, start: str, end: str) -> str:
    """The inclusive span from ``start`` to the first ``end`` after it."""
    assert text.count(start) == 1, start
    begin = text.index(start)
    return text[begin : text.index(end, begin) + len(end)]


def _carried(name: str) -> tuple[str, str]:
    """This cell's copy of a run-23 file, beside run-23's with the run id moved."""
    return (
        (HERE / name).read_text(encoding="utf-8"),
        (RUN_23 / name).read_text(encoding="utf-8")
        .replace("run-23", "run-24")
        .replace("Run-23", "Run-24")
        .replace("run_23", "run_24"),
    )


@pytest.fixture()
def private_workspace() -> Iterator[Path]:
    PRIVATE.mkdir(exist_ok=True)
    path = Path(tempfile.mkdtemp(dir=PRIVATE, prefix="run-24-test-"))
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _source_arguments(ontology: Path | None = None) -> list[str]:
    return [
        "--root",
        "inspection-note",
        "--source",
        "inspection-note",
        str(ontology if ontology is not None else FIXTURE / "inspection-note.yaml"),
        "--source",
        "malleus",
        str(ROOT / "ontology/malleus.yaml"),
        "--source",
        "linkml:types",
        str(LINKML_TYPES),
    ]


def _population_file(directory: Path) -> Path:
    plan = json.loads((FIXTURE / "document-plan.json").read_bytes())
    path = directory / "document-population.json"
    path.write_bytes(
        _canonical(
            {
                "capture": json.loads((FIXTURE / "document-capture.json").read_bytes()),
                "records": plan["records"],
                "supersessions": plan["supersessions"],
            }
        )
    )
    return path


def _event_ontology(directory: Path) -> Path:
    """The neutral fixture ontology plus one grounded Event subclass.

    The fixture is Core's and is read, never written. It declares no Event type
    and carries no grounding block, and the PROJECT rite needs one on every class
    whose ``is_a`` is a Malleus root, so the test writes its own bytes.
    """
    document = yaml.safe_load((FIXTURE / "inspection-note.yaml").read_bytes())
    document["classes"][EVENT_TYPE] = {"is_a": "Event"}
    for body in document["classes"].values():
        if body.get("is_a") in ROOT_PARENTS:
            body["annotations"] = {"grounding": deepcopy(GROUNDING)}
    path = directory / "inspection-note-with-event.yaml"
    path.write_bytes(yaml.safe_dump(document, sort_keys=True).encode("utf-8"))
    return path


def _event_population_file(directory: Path) -> Path:
    """The fixture capture and records with one Event record and its derivation.

    Every ``properties`` key needs a formalization target, so the event's
    ``event_type`` is named by the same assertion that already carries the
    inspection.
    """
    plan = json.loads((FIXTURE / "document-plan.json").read_bytes())
    capture = json.loads((FIXTURE / "document-capture.json").read_bytes())
    capture["assertions"][0]["formalized_by"].append(
        {"path": ["properties", "event_type"], "record_id": EVENT_RECORD_ID}
    )
    records = dict(plan["records"])
    records["events"] = [
        {
            "id": EVENT_RECORD_ID,
            "properties": {"event_type": "INSPECTION"},
            "type": EVENT_TYPE,
        }
    ]
    path = directory / "document-population-with-event.json"
    path.write_bytes(
        _canonical(
            {
                "capture": capture,
                "records": records,
                "supersessions": plan["supersessions"],
            }
        )
    )
    return path


def _binding_file(directory: Path) -> Path:
    path = directory / "native-query-binding.json"
    path.write_bytes(
        _canonical(
            {
                "schema": "malleus.paper-v4.native-query-binding/v6",
                "status": "FROZEN_AFTER_REPLAY",
                "queries": [
                    {
                        "id": "NQ-FIXTURE-01",
                        "question_id": "FIXTURE-01",
                        "cases": [
                            {
                                "kind": "RELATION",
                                "ordinal": 1,
                                "source_record_type": "Inspection",
                                "relation_record_type": "InspectionOfRelation",
                                "target_record_type": "Asset",
                                "output_fields": {
                                    "source": ["inspected_on"],
                                    "relation": ["relation_type"],
                                    "target": ["name"],
                                },
                            }
                        ],
                    }
                ],
            }
        )
    )
    return path


def _subject_ontology(directory: Path) -> Path:
    """The neutral fixture ontology plus a grounded ``subject`` reference.

    Core-13 puts ``subject`` on the research pack's SourceAsserted mixin, single,
    optional and Entity-ranged. The fixture is Core's and is read, never written,
    and it imports no pack, so the test declares the same shape on its own bytes:
    one entity type carries an entity-ranged ``subject`` slot, which is what a
    SUBJECT case binds against.
    """
    document = yaml.safe_load((FIXTURE / "inspection-note.yaml").read_bytes())
    document["slots"][SUBJECT_SLOT] = {"range": "Asset"}
    document["classes"]["Inspection"]["slots"].append(SUBJECT_SLOT)
    for body in document["classes"].values():
        if body.get("is_a") in ROOT_PARENTS:
            body["annotations"] = {"grounding": deepcopy(GROUNDING)}
    path = directory / "inspection-note-with-subject.yaml"
    path.write_bytes(yaml.safe_dump(document, sort_keys=True).encode("utf-8"))
    return path


def _subtype_ontology(directory: Path) -> Path:
    """The neutral fixture ontology plus one subtype of an entity type.

    The fixture declares no subclass of a project class, and the closure rule
    is about exactly that: the facade's typed query returns a type's records
    and its subtypes', so a set that lists the parent and not the child binds a
    query the executor refuses after the rows exist (E-0196). The fixture is
    Core's and is read, never written, so the subtype is declared on the test's
    own bytes.
    """

    document = yaml.safe_load((FIXTURE / "inspection-note.yaml").read_bytes())
    for body in document["classes"].values():
        if body.get("is_a") in ROOT_PARENTS:
            body["annotations"] = {"grounding": deepcopy(GROUNDING)}
    document["classes"][SUBTYPE] = {"is_a": "Inspection"}
    path = directory / "inspection-note-with-subtype.yaml"
    path.write_bytes(yaml.safe_dump(document, sort_keys=True).encode("utf-8"))
    return path


def _subtype_gate_surface(workspace: Path) -> Path:
    """Compile the fixture-plus-subtype ontology and return its accepted surface."""

    producer = workspace / "producer"
    if not producer.exists():
        _module("prepare_producer").prepare(
            ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
        )
    gate = workspace / "gate-subtype"
    assert _module("compile_ontology_candidate").compile_candidate(
        ontology_path=_subtype_ontology(workspace),
        producer_root=producer,
        output=gate,
        attempt=1,
    )
    return gate / "population-surface.json"


def _subject_population_file(directory: Path) -> Path:
    """The fixture records with one naming its subject and one naming none.

    Both are of the bearing type. The first is what the v4.4 restriction was
    written for and is reached through its subject and, from v4.13, through
    SUBJECT_ANY as well; the second is what E-0197 found run-21 carrying 237
    of and what v4.12's fourth case kind reaches.
    """

    plan = json.loads((FIXTURE / "document-plan.json").read_bytes())
    capture = json.loads((FIXTURE / "document-capture.json").read_bytes())
    capture["assertions"][0]["formalized_by"].extend(
        (
            {"path": ["properties", SUBJECT_SLOT], "record_id": SUBJECT_RECORD_ID},
            {
                "path": ["properties", SUBJECT_TAGS_SLOT],
                "record_id": SUBJECT_TARGET_ID,
            },
            {
                "path": ["properties", "inspected_on"],
                "record_id": UNATTACHED_RECORD_ID,
            },
        )
    )
    records = deepcopy(plan["records"])
    records["entities"].append(
        {
            "id": UNATTACHED_RECORD_ID,
            "properties": {"inspected_on": UNATTACHED_INSPECTED_ON},
            "type": "Inspection",
        }
    )
    for entity in records["entities"]:
        if entity["id"] == SUBJECT_RECORD_ID:
            entity["properties"][SUBJECT_SLOT] = SUBJECT_TARGET_ID
        if entity["id"] == SUBJECT_TARGET_ID:
            entity["properties"][SUBJECT_TAGS_SLOT] = list(SUBJECT_TARGET_TAGS)
    path = directory / "document-population-with-subject.json"
    path.write_bytes(
        _canonical(
            {
                "capture": capture,
                "records": records,
                "supersessions": plan["supersessions"],
            }
        )
    )
    return path


def _run(script: str, arguments: list[str]) -> subprocess.CompletedProcess[str]:
    environment = {
        "PATH": "/usr/bin:/bin",
        "PYTHONPATH": f"{ROOT}:{ROOT / 'src'}",
    }
    return subprocess.run(
        [sys.executable, str(HERE / f"{script}.py"), *arguments],
        capture_output=True,
        cwd=ROOT,
        env=environment,
        text=True,
    )


def _executed(workspace: Path) -> tuple[Path, dict[str, object]]:
    results = workspace / "results"
    completed = _run(
        "run",
        [
            *_source_arguments(),
            "--reading",
            str(FIXTURE / "reading.json"),
            "--population",
            str(_population_file(workspace)),
            "--capture-id",
            CAPTURE_ID,
            "--plan-id",
            PLAN_ID,
            "--source-id",
            SOURCE_ID,
            "--artifact-id",
            ARTIFACT_ID,
            "--ledger",
            str(workspace / "history.jsonl"),
            "--results",
            str(results),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )
    assert completed.returncode == 0, completed.stderr
    return results, json.loads((results / "run-result.json").read_bytes())


def test_no_paper_module_names_a_core_protocol_internal() -> None:
    scripts = sorted(path.name for path in HERE.glob("*.py"))

    assert scripts == [
        "bind_from_surface.py",
        "compile_ontology_candidate.py",
        "native_query.py",
        "offline_validation.py",
        "pin.py",
        "prepare_producer.py",
        "run.py",
        "test_contract.py",
        "test_pipeline.py",
        "usage_from_launch_log.py",
    ]
    for name in scripts:
        text = (HERE / name).read_text(encoding="utf-8")
        for symbol in FORBIDDEN_SYMBOLS:
            assert symbol not in text, f"{name} names {symbol}"


def test_the_eight_carried_harness_files_are_run_23s_bytes() -> None:
    """Every instrument in this directory but the pin, carried byte for byte.

    Run-23 changed three of these files and carried five; this cell changes
    none, so all eight are read the same way: run-23's file with the run id
    substituted and nothing else. Neither the binder, nor the executor, nor the
    offline validation, nor how the run executes, nor how the gate refuses, nor
    how a declared input is staged, nor what the producer is told moves. The
    file list is closed against the directory, so a ninth file, or any edit
    inside one of the eight, fails here rather than travelling with the cell.
    """

    assert set(CARRIED_WITH_THE_RUN_ID) == {
        "bind_from_surface.py",
        "compile_ontology_candidate.py",
        "native_query.py",
        "offline_validation.py",
        "prepare_producer.py",
        "run.py",
        "spawn-message.md",
        "usage_from_launch_log.py",
    }
    # No file of this directory carries a change of this cell's. The one change
    # it states lands in the review package builder, which lives elsewhere.
    named = {name for files in RUN_24_CHANGES.values() for name in files}
    assert set(RUN_24_CHANGES) == {"QUESTIONS_V3_1_CQ_C_03_EXCLUDED_SURFACE_ONLY"}
    assert named == {"paper-v4/evaluation-v4/run-24/build_review_inputs.py"}
    assert not named & {f"paper-v4/experiment-v4/run-24/{name}" for name in
                        CARRIED_WITH_THE_RUN_ID}
    assert sorted(
        path.name
        for path in HERE.iterdir()
        if path.suffix in {".py", ".md"} and not path.name.startswith("test_")
    ) == sorted(CARRIED_WITH_THE_RUN_ID + ("pin.py",))
    for name in CARRIED_WITH_THE_RUN_ID:
        here, expected = _carried(name)
        assert here == expected, name
        assert "run-24" in here or name == "native_query.py", name
        # The table reverses: undo the substitutions and run-23's file comes
        # back, so an edit cannot ride along inside the run id move.
        reversed_text = here
        for before, after in RUN_ID_SUBSTITUTIONS:
            reversed_text = reversed_text.replace(after, before)
        assert reversed_text == (RUN_23 / name).read_text(encoding="utf-8"), name

    # The executor names no cell at all, so its bytes are run-23's untouched.
    assert (HERE / "native_query.py").read_bytes() == (
        RUN_23 / "native_query.py"
    ).read_bytes()

    runner = (HERE / "run.py").read_text(encoding="utf-8")
    # Once for the plan compiler and once for the document adapter, so Core-12's
    # evaluative-slot check stays in force; a runner that dropped the second
    # would skip EVALUATIVE_SLOT_NOT_EVALUATED in silence.
    assert runner.count("contract_view=retention.contract_view") == 2
    assert STOP_RULE_SENTENCE in _plain(SPAWN_MESSAGE.read_text(encoding="utf-8"))
    assert STOP_RULE_SENTENCE not in _plain(
        (RUN_04 / "spawn-message.md").read_text(encoding="utf-8")
    )
    # The spawn message is run-23's with the run id moved and nothing else, so
    # the producer is told exactly what run-23's producer was told, which is
    # what run-22's and run-21's were told. This is the producer-side half of
    # the replicate claim and it is byte-exact through the chain.
    message, expected_message = _carried("spawn-message.md")
    assert message == expected_message
    assert message == (
        (RUN_23 / "spawn-message.md")
        .read_text(encoding="utf-8")
        .replace("run-23", "run-24")
    )
    assert message == (
        (RUN_22 / "spawn-message.md")
        .read_text(encoding="utf-8")
        .replace("run-22", "run-24")
    )


def test_the_binder_and_the_offline_validation_are_run_23s_apart_from_the_run_id() -> None:
    """The three files run-23 changed, read as carried and nothing more.

    Run-23 stated its edit to each of these as a table and reversed it. This
    cell states no table for them, so the claim is stronger and simpler: strip
    the run id from this cell's copy and run-23's file comes back, and the only
    lines that differ at all are the ones that spell the run id. Anything else
    is a harness change arriving inside a replicate.
    """

    for name in ("bind_from_surface.py", "native_query.py", "offline_validation.py"):
        here = (HERE / name).read_text(encoding="utf-8").splitlines()
        prior = (RUN_23 / name).read_text(encoding="utf-8").splitlines()
        assert len(here) == len(prior), name
        for mine, theirs in zip(here, prior):
            if mine == theirs:
                continue
            assert "run-24" in mine or "run_24" in mine, (name, mine)
            assert mine.replace("run-24", "run-23").replace(
                "run_24", "run_23"
            ) == theirs, (name, mine)

    # What v4.13 put in them is still there, read off the modules rather than
    # the text: the fifth case kind, its binding schema, and its row builder.
    binder = _module("bind_from_surface")
    executor = _module("native_query")
    assert binder.BINDING_SCHEMA == BINDING_SCHEMA_V6
    assert binder.CASE_KINDS == (
        "ENTITY",
        ENTITY_NO_SUBJECT,
        "RELATION",
        "SUBJECT",
        SUBJECT_ANY,
    )
    assert executor.CASE_KINDS == binder.CASE_KINDS
    assert executor._ROWS_BY_KIND[SUBJECT_ANY] is executor._ROWS_BY_KIND["SUBJECT"]
    assert binder.CASE_KINDS == _run_23_binder().CASE_KINDS


def test_the_review_package_builder_is_run_23s_with_the_question_file_moved() -> None:
    """The whole of this cell's edit surface, stated as one table and reversed.

    A cell that changes a file has to say what it changed in it, and saying it
    in prose is what lets a second edit ride along. The builder is read as
    run-23's bytes with the run id moved and then this table applied; reversing
    both must give run-23's builder back byte for byte. Every entry is required
    to appear exactly once, so an anchor that matched twice, or a change made
    outside the table, fails here.
    """

    here = (REVIEW_PACKAGE / "build_review_inputs.py").read_text(encoding="utf-8")
    prior = (PRIOR_REVIEW_PACKAGE / "build_review_inputs.py").read_text(
        encoding="utf-8"
    )

    assert here != prior
    carried = prior
    for before, after in RUN_ID_SUBSTITUTIONS:
        carried = carried.replace(before, after)
    built = carried
    for before, after in BUILDER_V3_1:
        assert built.count(before) == 1, before[:60]
        built = built.replace(before, after)
    assert built == here
    reversed_text = here
    for before, after in reversed(BUILDER_V3_1):
        assert here.count(after) == 1, after[:60]
        reversed_text = reversed_text.replace(after, before)
    for before, after in RUN_ID_SUBSTITUTIONS:
        reversed_text = reversed_text.replace(after, before)
    assert reversed_text == prior

    # What the table is for, read off the module rather than the text: the
    # builder binds v3.1 and the file it binds is the one the contract pins.
    builder = _binder_of(
        REVIEW_PACKAGE, "paper_v4_run_24_review_builder", "build_review_inputs"
    )
    prior_builder = _binder_of(
        PRIOR_REVIEW_PACKAGE, "paper_v4_run_23_review_builder", "build_review_inputs"
    )
    assert builder.RUN_ID == "run-24"
    assert prior_builder.RUN_ID == "run-23"
    assert builder.QUESTIONS == QUESTIONS_V3_1
    assert prior_builder.QUESTIONS == QUESTIONS_V3
    assert builder.QUESTIONS.is_file()
    contract = json.loads(CONTRACT_PATH.read_bytes())["evaluation"]
    assert contract["competency_questions"]["path"] == str(
        builder.QUESTIONS.relative_to(ROOT)
    )
    assert contract["competency_questions"]["sha256"] == _digest(
        builder.QUESTIONS.read_bytes()
    )
    assert contract["review_task"]["carried_from"] == "run-23"
    assert contract["review_task"]["carried_bytes"] == (
        "RUN_23S_BUILDER_WITH_THE_RUN_ID_MOVED_AND_THE_QUESTION_FILE_MOVED_TO_V3_1"
    )
    # The thirty ids it reads are v3.1's, in that file's order, and they are the
    # same thirty ids run-23's builder read from v3.
    assert builder.question_ids() == [
        item["id"] for item in json.loads(QUESTIONS_V3_1.read_bytes())["questions"]
    ]
    assert builder.question_ids() == prior_builder.question_ids()
    assert len(builder.question_ids()) == 30


def test_the_bound_question_file_reduces_cq_c_03_to_three_semantics() -> None:
    """v3.1 against v3, read as two files: one question moved and no other.

    The digest the contract pins is recomputed here from the bytes on disk, and
    the two files are compared question by question, so a second amendment
    riding inside the CQ-C-03 change fails here.
    """

    subject = json.loads(QUESTIONS_V3_1.read_bytes())
    prior = json.loads(QUESTIONS_V3.read_bytes())
    contract = json.loads(CONTRACT_PATH.read_bytes())["evaluation"]

    assert subject["schema"] == prior["schema"]
    assert [item["id"] for item in subject["questions"]] == [
        item["id"] for item in prior["questions"]
    ]
    by_id = {item["id"]: item for item in subject["questions"]}
    prior_by_id = {item["id"]: item for item in prior["questions"]}
    assert [
        question_id
        for question_id in by_id
        if by_id[question_id] != prior_by_id[question_id]
    ] == ["CQ-C-03"]
    assert by_id["CQ-C-03"]["required_semantics"] == [
        "site_set",
        "maximum_depth_quantity",
        "spreading_rate_quantity",
    ]
    assert prior_by_id["CQ-C-03"]["required_semantics"] == [
        "site_set",
        "maximum_depth_quantity",
        "spreading_rate_quantity",
        "compilation_source",
    ]
    assert by_id["CQ-C-03"]["expected_outcome"]["kind"] == "EXCLUDED_SURFACE"
    assert by_id["CQ-C-03"]["expected_outcome"]["expected_coverage"] == "NONE"
    assert contract["competency_questions"]["sha256"] == _digest(
        QUESTIONS_V3_1.read_bytes()
    )
    assert contract["competency_questions"]["supersedes"]["sha256"] == _digest(
        QUESTIONS_V3.read_bytes()
    )


def test_native_query_is_run_23s_executor_unchanged() -> None:
    """Five case kinds, three row kinds, four builders, and not one byte moved.

    The executor names no cell of its own, so carrying it with the run id moved
    leaves run-23's bytes exactly. What this holds is that the shape v4.13 left
    is still there: a fifth case kind in every one of the four maps that key on
    a kind, no fifth row builder, and three row kinds, because SUBJECT_ANY
    writes a SUBJECT row out of the builder that already wrote one. The spans
    hold the rest of the file against run-08's bytes, so it cannot drift away
    from the executor every cell from run-02 onward ran.
    """

    text = (HERE / "native_query.py").read_text(encoding="utf-8")
    prior = (RUN_23 / "native_query.py").read_text(encoding="utf-8")

    # Nothing moved at all: the file names no cell, so there was nothing for the
    # run id table to substitute.
    assert text == prior
    assert "run-24" not in text
    assert "run_24" not in text
    assert text.count("Run-13's 515 rows") == 1
    assert text.count("run-14's 919 carried 44") == 1
    assert text.count("Run-21 populated 237") == 1
    assert text.count(BINDING_SCHEMA_V6) == 1
    assert BINDING_SCHEMA_V5 not in text
    # The cell before v4.13 is where the fifth kind is absent, which is what
    # makes it identifiable as a kind this instrument has and an earlier one
    # did not.
    assert (RUN_22 / "native_query.py").read_text(encoding="utf-8").count(
        BINDING_SCHEMA_V5
    ) == 1
    assert SUBJECT_ANY not in (RUN_22 / "native_query.py").read_text(encoding="utf-8")
    assert text.count('RESULT_SCHEMA = "malleus.paper-v4.query-result/v3"') == 1
    assert "malleus.paper-v4.query-result/v2" not in text
    # The carried v4.7 delta is still exactly one edit, on the own-type fields.
    assert text.count('SUBJECT_TAGS_SLOT = "tags"') == 1
    assert (
        text.count(
            '                "subject": _project(\n'
            "                    subject,\n"
            "                    [*_own_fields(subject, projections),"
            " SUBJECT_TAGS_SLOT],\n"
            "                ),\n"
        )
        == 1
    )
    assert "SUBJECT_TAGS_SLOT" not in (
        RUN_09 / "native_query.py"
    ).read_text(encoding="utf-8")
    # No row carries the singular field, at any kind. There are still four
    # builders and so still four places an ordinal is written: the fifth kind
    # adds no builder, it reuses the SUBJECT one.
    assert '"case_ordinal":' not in text
    assert text.count('"case_ordinals": [case["ordinal"]],') == 4
    assert text.count("def _subject_rows(") == 1

    # The bytes every cell from run-02 to run-08 ran are still one file.
    for prior_cell in (RUN_02, RUN_03, RUN_04, RUN_05, RUN_06, RUN_07):
        assert (prior_cell / "native_query.py").read_bytes() == (
            RUN_08 / "native_query.py"
        ).read_bytes(), prior_cell.name
    # Every region run-08 already had and neither the carried removal nor this
    # cell's addition touches is still run-08's, ``_project`` included.
    for start, end in (
        ("class _SourceFreeGuard:", "        self._stack.close()\n"),
        (
            "def trace_witnesses(",
            "    return [traced[record_id] for record_id in sorted(traced)]\n",
        ),
        ("def execute(arguments: argparse.Namespace)", "    return result\n"),
        ("def _project(", "    return {name: record[name] for name in fields if name in record}\n"),
        ("FORBIDDEN_ATTEMPTS = ", "    }\n)\n"),
    ):
        assert _span(text, start, end) == _span(
            (RUN_08 / "native_query.py").read_text(encoding="utf-8"), start, end
        ), start

    subject = _module("native_query")
    prior_module = _binder_of(
        RUN_23, "paper_v4_run_23_native_query", "native_query"
    )
    assert subject.RESULT_SCHEMA == "malleus.paper-v4.query-result/v3"
    assert subject.BINDING_SCHEMA == BINDING_SCHEMA_V6
    assert subject.SUBJECT_TAGS_SLOT == "tags"
    assert subject.SUBJECT_SLOT == "subject"
    assert subject.RECORD_TYPE_SLOT == "type"
    assert subject.ENTITY_NO_SUBJECT == ENTITY_NO_SUBJECT
    assert subject.SUBJECT_ANY == SUBJECT_ANY
    # The row kind the carried case writes is the one an ENTITY case already
    # wrote; the new kind's is the one a SUBJECT case already wrote.
    assert subject.ENTITY_ROW_KIND == "ENTITY"
    assert subject.CASE_KINDS == (
        "ENTITY",
        ENTITY_NO_SUBJECT,
        "RELATION",
        "SUBJECT",
        SUBJECT_ANY,
    )
    assert subject.CASE_KINDS == tuple(sorted(subject.CASE_KINDS))
    assert prior_module.CASE_KINDS == subject.CASE_KINDS
    assert set(subject.CASE_KINDS) - set(prior_module.CASE_KINDS) == set()
    # Run-22's executor, one cell further back, is where the fifth kind is not.
    before_v4_13 = _binder_of(
        RUN_22, "paper_v4_run_22_native_query", "native_query"
    )
    assert set(subject.CASE_KINDS) - set(before_v4_13.CASE_KINDS) == {SUBJECT_ANY}
    assert sorted(subject._ROWS_BY_KIND) == list(subject.CASE_KINDS)
    assert sorted(subject._CASE_FIELDS) == sorted(subject._OUTPUT_FIELDS)
    assert sorted(subject._CASE_FIELDS) == list(subject.CASE_KINDS)
    # The new kind's grammar is the SUBJECT kind's and it is answered by the
    # SUBJECT kind's builder, which is what makes its row a SUBJECT row rather
    # than a fourth shape the reviewer has to learn. The carried kind's grammar
    # is the ENTITY kind's for the same reason.
    for mapping in (
        subject._CASE_FIELDS,
        subject._OUTPUT_FIELDS,
        subject._TYPE_FIELDS,
        subject._PROJECTED_TYPES,
    ):
        assert mapping[ENTITY_NO_SUBJECT] == mapping["ENTITY"]
        assert mapping[SUBJECT_ANY] == mapping["SUBJECT"]
    assert subject._ROWS_BY_KIND[SUBJECT_ANY] is subject._ROWS_BY_KIND["SUBJECT"]
    assert (
        subject._ROWS_BY_KIND[ENTITY_NO_SUBJECT]
        is not subject._ROWS_BY_KIND["ENTITY"]
    )
    # The four carried kinds do not move at all.
    for kind in prior_module.CASE_KINDS:
        assert subject._CASE_FIELDS[kind] == prior_module._CASE_FIELDS[kind], kind
        assert subject._OUTPUT_FIELDS[kind] == prior_module._OUTPUT_FIELDS[kind], kind
        assert subject._TYPE_FIELDS[kind] == prior_module._TYPE_FIELDS[kind], kind
        assert (
            subject._PROJECTED_TYPES[kind] == prior_module._PROJECTED_TYPES[kind]
        ), kind
    assert subject.RESULT_SCHEMA == prior_module.RESULT_SCHEMA
    # The carried removal reads a case's projected fields per declared type, so
    # every kind's output fields are covered and no key outside the grammar is.
    assert sorted(subject._PROJECTED_TYPES) == list(subject.CASE_KINDS)
    for kind, pairs in subject._PROJECTED_TYPES.items():
        assert {field for _, field in pairs} == subject._OUTPUT_FIELDS[kind], kind
        assert {key for key, _ in pairs} <= subject._CASE_FIELDS[kind], kind


def test_pin_is_run_23s_bytes_with_the_reference_cell_and_the_markers_kept() -> None:
    """The one file that names the cell it carries from, and gains no code here.

    ``pin.py`` writes ``pin_status`` on every Core entry and reads the declared
    inputs against a reference run, so carrying it means moving two things: the
    run id, and the cell of record. Run-18 had to move a third because Core did
    not stand still under it, run-22 a fourth because it changed the staging and
    run-23 a fifth because it moved the protocol version; this cell moves none
    of the three, because Core is held, the staging is run-22's and v4.13 is
    run-23's. What it does have to do is give the marked blocks their markers
    back: a marker names the cell that wrote the block, and the reference-cell
    move would otherwise put run-23's name on run-22's four. Run-18's five and
    run-22's four are here as bytes with their own markers, this cell adds none,
    and the file reverses through both tables to run-23's byte for byte with
    nothing removed first. An edit in no table fails.
    """

    here = (HERE / "pin.py").read_text(encoding="utf-8")
    prior = (RUN_23 / "pin.py").read_text(encoding="utf-8")

    assert here != prior
    reversed_text = here
    for before, after in reversed(PIN_MARKERS_KEPT):
        assert here.count(after) == 1, after[:60]
        reversed_text = reversed_text.replace(after, before)
    for before, after in reversed(PIN_REFERENCE_CELL):
        assert here.count(after) >= 1, after[:60]
        reversed_text = reversed_text.replace(after, before)
    for before, after in RUN_ID_SUBSTITUTIONS:
        reversed_text = reversed_text.replace(after, before)
    assert reversed_text == prior
    # Run-18's five marked blocks are carried whole, markers included, and both
    # files carry every one of them exactly once.
    for label in PIN_ADDITION_MARKERS:
        for text, name in ((here, "run-24"), (prior, "run-23")):
            assert text.count(f"{ADDITION_BEGINS}{label}\n") == 1, (label, name)
            assert text.count(f"{ADDITION_ENDS}{label}\n") == 1, (label, name)
    assert here.count(ADDITION_BEGINS) == len(PIN_ADDITION_MARKERS)
    assert here.count(ADDITION_ENDS) == len(PIN_ADDITION_MARKERS)
    assert here.count(ADDITION_BEGINS) == prior.count(ADDITION_BEGINS)
    # Run-22's four are still marked with run-22's run id in both files: the
    # cell that wrote a block keeps its name on it, and this cell wrote none.
    for label in PIN_RUN_22_ADDITION_MARKERS:
        for text, name in ((here, "run-24"), (prior, "run-23")):
            assert text.count(f"{RUN_22_ADDITION_BEGINS}{label}\n") == 1, (label, name)
            assert text.count(f"{RUN_22_ADDITION_ENDS}{label}\n") == 1, (label, name)
    assert here.count(RUN_22_ADDITION_BEGINS) == len(PIN_RUN_22_ADDITION_MARKERS)
    assert here.count(RUN_22_ADDITION_ENDS) == len(PIN_RUN_22_ADDITION_MARKERS)
    assert here.count(RUN_22_ADDITION_BEGINS) == prior.count(RUN_22_ADDITION_BEGINS)
    for absent in ("run-23", "run-24"):
        assert f"# {absent} addition begins: " not in here
        assert f"# {absent} addition ends: " not in here

    # What the two tables are for, read off the module rather than the text.
    pin = _module("pin")
    assert pin.RUN_ID == "run-24"
    assert pin.PROTOCOL_VERSION == "v4.13"
    assert pin.INTERFACE_ORDINAL == "24"
    assert pin.CARRIED == CARRIED_PIN_STATUS
    assert pin.REFERENCE_RUN == "run-23"
    assert pin.REFERENCE_MANIFEST == (
        "paper-v4/experiment-v4/run-23/producer-input-manifest.json"
    )
    assert (ROOT / pin.REFERENCE_MANIFEST).is_file()
    assert pin.CARRIED in CORE_PIN_STATUSES
    # Neither the protocol version nor Core moves: this cell is the second of
    # v4.13 at the coordinate run-23 pinned, and the ordinal is the only thing
    # of the four that steps.
    prior_pin = _binder_of(RUN_23, "paper_v4_run_23_pin", "pin")
    assert prior_pin.PROTOCOL_VERSION == "v4.13"
    assert pin.PROTOCOL_VERSION == prior_pin.PROTOCOL_VERSION
    assert prior_pin.INTERFACE_ORDINAL == "23"
    assert prior_pin.CARRIED == "CARRIED_FROM_RUN_22"
    assert prior_pin.REFERENCE_RUN == "run-22"
    # The staging table is carried unchanged, so the profile is still staged as
    # canonical JSON and the cause of a moved input is still named rather than
    # left to be guessed at. Nothing is expected to have moved this cell.
    assert pin.CANONICAL_JSON_INPUTS == frozenset({"SOURCE_ASSERTION_PROFILE"})
    assert pin.CANONICAL_JSON == "CANONICAL_JSON"
    assert pin.SOURCE_BYTES == "SOURCE_BYTES"
    assert pin.MOVED_BY_THE_HARNESS == {
        "SOURCE_ASSERTION_PROFILE": "STAGED_AS_CANONICAL_JSON_FROM_V4_12"
    }
    assert pin.CANONICAL_JSON_INPUTS == prior_pin.CANONICAL_JSON_INPUTS
    assert pin.MOVED_BY_THE_HARNESS == prior_pin.MOVED_BY_THE_HARNESS
    # Both statuses exist at run-23 too, because the two entries they belong to
    # are run-18's and are carried through it rather than rewritten.
    assert pin.LANDED == "LANDED"
    assert pin.PENDING == "PENDING_AT_PIN"
    assert {pin.LANDED, pin.PENDING} == READ_AT_THE_PIN_STATUSES
    assert prior_pin.LANDED == pin.LANDED
    assert prior_pin.PENDING == pin.PENDING
    # The baseline the two carried entries are read against is the coordinate
    # run-17 pinned, which is still where every other carried entry stops.
    assert pin.V4_8_COMMIT == prior_pin.V4_8_COMMIT == V4_9_COORDINATE


def test_the_pin_refuses_landed_for_core_20_unless_the_paragraph_carries_every_reason() -> None:
    """The guard the carried Core-20 entry needs, driven on synthetic text.

    Core-20's whole content is that the skill's pre-flight paragraph carries the
    two enums' refusal reasons, each of them and no other. A pin that recorded
    LANDED off a paragraph missing one would say a producer had a list to check
    against when it did not, and this cell's whole subject is what that list
    does for a producer that reads it. The decision is a pure function of three
    strings, so it is driven here with a paragraph built to be wrong in one way
    at a time; no commit is read.
    """

    pin = _module("pin")
    reasons = ["ALPHA_ONE", "BETA_TWO", "GAMMA_THREE"]
    marker = pin.PREFLIGHT_MARKER
    guard = (
        "DocumentAssertionRefusalReason PopulationPlanRefusalReason"
        f" {marker}"
    )

    def skill(body: str) -> str:
        return (
            "before\n"
            f"<!-- {marker}:start -->\n{body}\n<!-- {marker}:end -->\n"
            "after\n"
        )

    complete = skill("\n".join(f"- {reason}: check it." for reason in reasons))
    observed = pin.preflight_observation(complete, guard, reasons)
    assert observed["paragraph_present"] is True
    assert observed["reasons_absent_from_the_paragraph"] == []
    assert observed["reasons_the_paragraph_invents"] == []
    assert pin.preflight_status(observed) == pin.LANDED

    # One reason missing: PENDING, and the entry names which one.
    short = skill("\n".join(f"- {reason}: check it." for reason in reasons[:-1]))
    observed = pin.preflight_observation(short, guard, reasons)
    assert observed["reasons_absent_from_the_paragraph"] == ["GAMMA_THREE"]
    assert observed["every_reason_named"] is False
    assert pin.preflight_status(observed) == pin.PENDING

    # One reason neither enum carries: PENDING too, because a producer told to
    # check for a refusal that cannot happen is being told something untrue.
    invented = skill(
        "\n".join(f"- {reason}: check it." for reason in [*reasons, "DELTA_FOUR"])
    )
    observed = pin.preflight_observation(invented, guard, reasons)
    assert observed["reasons_the_paragraph_invents"] == ["DELTA_FOUR"]
    assert pin.preflight_status(observed) == pin.PENDING

    # No markers at all: PENDING, and no reason counted as named.
    observed = pin.preflight_observation("no paragraph here", guard, reasons)
    assert observed["paragraph_present"] is False
    assert observed["reasons_named_in_the_paragraph"] == []
    assert pin.preflight_status(observed) == pin.PENDING

    # The paragraph is complete but the guard does not derive it from the enums:
    # PENDING, because a hand-written list is what drifts.
    for weak in ("", "DocumentAssertionRefusalReason", f"{marker} only"):
        observed = pin.preflight_observation(complete, weak, reasons)
        assert observed["every_reason_named"] is True
        assert pin.preflight_status(observed) == pin.PENDING, weak


def test_the_carried_delta_projects_tags_only_on_the_subject_side_and_only_when_present() -> None:
    """The carried v4.7 delta at the row level, on rows built in isolation.

    A subject that carries ``tags`` projects them beside its own type's fields;
    one that does not projects exactly what run-09 projected. The record side
    never gains the field and the two other kinds are untouched. Run-09's
    executor is the comparison because it is the last one without the tags
    delta, and it is driven with the same projections the case names, so the
    only difference the comparison can show is the delta itself.
    """

    subject = _module("native_query")
    prior = _binder_of(
        RUN_09, "paper_v4_run_09_native_query_rows", "native_query"
    )
    assert "SUBJECT_TAGS_SLOT" not in (
        RUN_09 / "native_query.py"
    ).read_text(encoding="utf-8")

    class _Graph:
        def __init__(self, records: dict[str, list[dict]]) -> None:
            self._records = records

        def query(self, record_type: str) -> list[dict]:
            return list(self._records.get(record_type, ()))

    tagged = {
        "id": "asset:P-7",
        "type": "Asset",
        "name": "Pump P-7",
        "tags": ["P-7", "P7"],
    }
    bare = {"id": "asset:P-8", "type": "Asset", "name": "Pump P-8"}
    records = [
        {
            "id": "inspection:1",
            "type": "Inspection",
            "inspected_on": "2026-03-02",
            "subject": "asset:P-7",
        },
        {
            "id": "inspection:2",
            "type": "Inspection",
            "inspected_on": "2026-03-03",
            "subject": "asset:P-8",
        },
    ]
    graph = _Graph({"Asset": [tagged, bare], "Inspection": records})
    case = {
        "kind": "SUBJECT",
        "ordinal": 1,
        "output_fields": {"record": ["inspected_on", "subject"], "subject": ["name"]},
        "record_type": "Inspection",
        "subject_record_type": "Asset",
    }
    projections = {"Asset": ["name"], "Inspection": ["inspected_on", "subject"]}

    witnesses: list[str] = []
    rows = subject._subject_rows(graph, case, witnesses, projections)
    prior_rows = prior._subject_rows(graph, dict(case), [])

    assert [row["subject"] for row in rows] == [
        {"name": "Pump P-7", "tags": ["P-7", "P7"]},
        {"name": "Pump P-8"},
    ]
    # Run-09's executor on the same graph and the same projection: the tagged
    # subject is the only difference, and it is an addition.
    assert [row["subject"] for row in prior_rows] == [
        {"name": "Pump P-7"},
        {"name": "Pump P-8"},
    ]
    # The record side, the witnesses and the row order are untouched.
    assert [row["record"] for row in rows] == [row["record"] for row in prior_rows]
    assert [row["witness"] for row in rows] == [row["witness"] for row in prior_rows]
    assert witnesses == ["inspection:1", "asset:P-7", "inspection:2", "asset:P-8"]
    for row in rows:
        assert "tags" not in row["record"]
        assert "type" not in row["record"]
        assert row["case_ordinals"] == [1]

    # The other two kinds project the same fields either way; only the ordinal
    # field's name moves, which is this cell's delta and not the tags one.
    entity_case = {
        "kind": "ENTITY",
        "ordinal": 1,
        "output_fields": {"record": ["name"]},
        "record_type": "Asset",
    }
    here_rows = subject._entity_rows(graph, entity_case, [], projections)
    there_rows = prior._entity_rows(graph, dict(entity_case), [])
    assert [row["record"] for row in here_rows] == [
        {"name": "Pump P-7"},
        {"name": "Pump P-8"},
    ]
    assert [row["record"] for row in here_rows] == [
        row["record"] for row in there_rows
    ]
    assert [row["witness"] for row in here_rows] == [
        row["witness"] for row in there_rows
    ]
    assert [row["case_ordinals"] for row in here_rows] == [[1], [1]]
    assert [row["case_ordinal"] for row in there_rows] == [1, 1]


def test_two_cases_reaching_one_witness_are_one_row_of_the_records_own_type() -> None:
    """The v4.9 removal at the row level, and the two refusals that guard it.

    A question whose type set names a type and one of its ancestors expands to
    an ENTITY case for each, and the graph returns the same record under both.
    Run-14, the last executor without the removal, wrote two rows, the
    ancestor's with fewer fields; this writes one,
    projected through the record's own type and carrying both ordinals. The
    projections come out of the binding, so a type the binding projects two ways
    and a record whose own type it never names are both refused rather than
    guessed past.
    """

    subject = _module("native_query")

    class _Graph:
        """A two-level hierarchy: ``query`` on the parent returns the child."""

        def __init__(self, records: list[dict], subtypes: dict[str, list[str]]):
            self._records = records
            self._subtypes = subtypes

        def query(self, record_type: str) -> list[dict]:
            wanted = {record_type, *self._subtypes.get(record_type, ())}
            return [item for item in self._records if item["type"] in wanted]

        def query_relations(self, relation_type: str | None = None) -> list[dict]:
            return []

    class _Replay:
        def __init__(self, graph) -> None:
            self.graph = graph

    pump = {
        "id": "asset:P-7",
        "type": "Pump",
        "name": "Pump P-7",
        "serial": "SN-7",
    }
    graph = _Graph([pump], {"Asset": ["Pump"]})
    binding = {
        "queries": [
            {
                "id": "NQ-CQ-01",
                "question_id": "CQ-01",
                "cases": [
                    {
                        "kind": "ENTITY",
                        "ordinal": 1,
                        "output_fields": {"record": ["name"]},
                        "record_type": "Asset",
                    },
                    {
                        "kind": "ENTITY",
                        "ordinal": 2,
                        "output_fields": {"record": ["name", "serial"]},
                        "record_type": "Pump",
                    },
                ],
            }
        ]
    }

    results, witnesses = subject.run_queries(_Replay(graph), binding)
    rows = results[0]["rows"]

    assert len(rows) == 1
    assert rows[0]["case_ordinals"] == [1, 2]
    # The own type's fields, not the ancestor case's fewer ones. Run-14, before
    # the removal, returned {"name": "Pump P-7"} here as well as this, in that
    # order.
    assert rows[0]["record"] == {"name": "Pump P-7", "serial": "SN-7"}
    assert rows[0]["witness"] == {"record_id": "asset:P-7"}
    assert "case_ordinal" not in rows[0]
    # The witness list is unchanged: it is what the tracer dedupes by id.
    assert witnesses == ["asset:P-7", "asset:P-7"]

    # The map the projection comes from is the binding's own per-type fields.
    assert subject.surface_projections(binding) == {
        "Asset": ["name"],
        "Pump": ["name", "serial"],
    }

    # A type projected two ways is refused rather than chosen between.
    conflicting = deepcopy(binding)
    conflicting["queries"][0]["cases"][1]["record_type"] = "Asset"
    with pytest.raises(subject.NativeQueryRefusal) as refusal:
        subject.surface_projections(conflicting)
    assert "projects Asset two ways" in str(refusal.value)

    # A record whose own type the binding never names is refused too: the
    # executor does not fall back to the case's type.
    orphan = {"id": "asset:P-9", "type": "Valve", "name": "Valve P-9"}
    with pytest.raises(subject.NativeQueryRefusal) as refusal:
        subject.run_queries(
            _Replay(_Graph([orphan], {"Asset": ["Valve"]})), binding
        )
    assert "no projection for the record's own type: Valve" in str(refusal.value)


def test_bind_from_surface_carries_all_five_kinds_and_adds_none() -> None:
    """Every rule the binder has, still there, and no rule of this cell's.

    The reversal test above already holds every byte of this file against
    run-23's; what this one holds is what those bytes mean. The v4.4
    restriction is read against run-09's pre-restriction bytes: a
    subject-bearing type gets no plain ENTITY case. v4.12's ENTITY_NO_SUBJECT
    case and its closure refusal are here. v4.13's SUBJECT_ANY case is here,
    one per bearing type in the set and entity type on the surface, and run-22's
    binder is where it is not, which is what makes it a rule this instrument has
    and the cell before v4.13 did not. v4.7's tags delta is in the executor, not
    here, so the binder's housekeeping set still drops ``tags`` from every
    projection it writes.
    """

    here = (HERE / "bind_from_surface.py").read_text(encoding="utf-8")
    prior = (RUN_09 / "bind_from_surface.py").read_text(encoding="utf-8")
    run_23 = (RUN_23 / "bind_from_surface.py").read_text(encoding="utf-8")
    run_22 = (RUN_22 / "bind_from_surface.py").read_text(encoding="utf-8")

    assert here != prior
    for start, end in (
        ("class BindingRefusal(ValueError):", "def _cases(\n"),
        ("    if len(cases) != expected:", "    return cases\n"),
        (
            '        "population_surface_sha256": _digest(surface_source),',
            "def execute(arguments: argparse.Namespace) -> dict[str, object]:\n",
        ),
        (
            "    type_sets = json.loads(Path(arguments.type_sets).read_bytes())",
            "    binding = build(\n",
        ),
        (
            "    output.parent.mkdir(parents=True, exist_ok=True)",
            '    parser.add_argument("--surface", required=True,'
            ' help="accepted population surface")\n',
        ),
        (
            '    parser.add_argument(\n        "--type-sets", required=True,'
            ' help="question id to surface type list"\n    )',
            "raise SystemExit(main())\n",
        ),
        ("HOUSEKEEPING_SLOTS = frozenset(", "BOUND_BY = ("),
    ):
        assert _span(here, start, end) == _span(prior, start, end), start

    # The carried v4.4 delta, line for line, against the cell before it.
    assert "unattached = [name for name in types if name not in set(bearing)]" in here
    assert "unattached = " not in prior
    assert "    for record_type in unattached:\n" in here
    assert "    for record_type in types:\n" in prior
    assert "    for record_type in types:\n" not in here
    assert "        len(unattached)\n" in here
    assert "entity_case_scope" in here
    assert "entity_case_scope" not in prior
    # The typed SUBJECT loop is untouched: subject-bearing types are still
    # reached through the subject types the set lists, and the v4.13 addition
    # is a second loop beside it rather than a replacement of it.
    assert _span(
        here,
        "    for record_type in bearing:\n        for subject_type in entities:",
        "    for record_type in bearing:\n        for subject_type in entities_on_surface:",
    ).replace(
        "    for record_type in bearing:\n        for subject_type in entities_on_surface:",
        "    expected = (\n",
    ) == _span(
        prior,
        "    for record_type in bearing:\n        for subject_type in entities:",
        "    expected = (\n",
    )

    # The carried v4.12 changes: the fourth kind, emitted for the bearing types
    # alone, and the closure refusal before the binding is written.
    assert here.count('"kind": ENTITY_NO_SUBJECT,') == 1
    assert run_23.count('"kind": ENTITY_NO_SUBJECT,') == 1
    assert run_22.count('"kind": ENTITY_NO_SUBJECT,') == 1
    assert "        + len(bearing)\n" in here
    assert "entity_no_subject_case_scope" in here
    assert "def refuse_unclosed(" in here
    assert here.index("    refuse_unclosed(") < here.index('        "schema": BINDING_SCHEMA,')
    assert "type_set_closure.py" in here
    assert _span(here, "def refuse_unclosed(", "def build(\n") == _span(
        run_23, "def refuse_unclosed(", "def build(\n"
    )

    # The carried v4.13 kind, paired off the surface's entity types and not off
    # the question's set, and its term in the exhaustive count. Run-23's binder
    # carries it identically and run-22's carries it not at all.
    assert here.count('"kind": SUBJECT_ANY,') == 1
    assert run_23.count('"kind": SUBJECT_ANY,') == 1
    assert "SUBJECT_ANY" not in run_22
    assert "    entities_on_surface = entity_types(by_name)\n" in here
    assert "entities_on_surface" in run_23
    assert "entities_on_surface" not in run_22
    assert "        + len(bearing) * len(entities_on_surface)\n" in here
    assert "subject_any_case_scope" in here
    assert "subject_any_case_scope" not in run_22

    binder = _module("bind_from_surface")
    run_22_binder = _binder_of(RUN_22, "paper_v4_run_22_binder")
    assert binder.BINDING_SCHEMA == BINDING_SCHEMA_V6
    assert _run_23_binder().BINDING_SCHEMA == BINDING_SCHEMA_V6
    assert run_22_binder.BINDING_SCHEMA == BINDING_SCHEMA_V5
    assert binder.CASE_KINDS == (
        "ENTITY",
        ENTITY_NO_SUBJECT,
        "RELATION",
        "SUBJECT",
        SUBJECT_ANY,
    )
    assert binder.CASE_KINDS == tuple(sorted(binder.CASE_KINDS))
    assert _run_23_binder().CASE_KINDS == binder.CASE_KINDS
    assert run_22_binder.CASE_KINDS == (
        "ENTITY",
        ENTITY_NO_SUBJECT,
        "RELATION",
        "SUBJECT",
    )
    assert set(binder.CASE_KINDS) - set(_run_23_binder().CASE_KINDS) == set()
    assert set(binder.CASE_KINDS) - set(run_22_binder.CASE_KINDS) == {SUBJECT_ANY}
    assert binder.ENTITY_NO_SUBJECT == ENTITY_NO_SUBJECT
    assert binder.SUBJECT_ANY == SUBJECT_ANY
    assert binder.SUBJECT_SLOT == "subject"
    assert binder.CLOSURE_CHECK == (
        "TYPE_SET_CLOSED_UNDER_THE_SURFACES_SUBTYPES_AT_BIND_TIME"
    )
    # The closure reader is the shared file every cell from v4.11 reads, loaded
    # by path and not copied into the cell.
    closure = binder._type_set_closure()
    assert closure.REASON == "TYPE_SET_NOT_CLOSED_UNDER_SUBTYPES"
    assert (HERE.parent / "type_set_closure.py").is_file()
    # The shared reader is read by path and never copied into the cell, and
    # this cell does not touch it: it guards a listed type's surface subtypes,
    # which is a different rule from the one v4.13 adds.
    assert "def omissions(" not in here
    assert closure.__file__ is None or "type_set_closure" in str(
        HERE.parent / "type_set_closure.py"
    )
    # The v4.7 delta is not here: the binder still calls ``tags`` housekeeping
    # and names it in no projection it writes.
    assert "https://malleus.dev/schema/tags" in binder.HOUSEKEEPING_SLOTS
    assert binder.HOUSEKEEPING_SLOTS == _run_23_binder().HOUSEKEEPING_SLOTS
    assert "SUBJECT_TAGS_SLOT" not in here


def test_the_binder_refuses_a_type_set_that_omits_a_surface_subtype(
    private_workspace: Path,
) -> None:
    """v4.12, change two, driven on a surface that carries a subtype.

    Run-23's first binding listed a parent and not its surface subtype; the
    facade returned the subtype's records and the executor refused a type the
    binding never named, after the rows existed (E-0196). v4.11 answered that
    with a reader the procedure ran by hand between writing the sets and binding
    them. Here the binder runs it, so the refusal happens where the evaluator
    can still correct the set and there is no binding file to skip it with.
    """

    subject = _module("bind_from_surface")
    surface_path = _subtype_gate_surface(private_workspace)
    contract_path = _gate_contract(surface_path)
    output = private_workspace / "binding-unclosed.json"

    # The parent alone: the surface carries a subtype of it, so the set is not
    # closed and no binding is written.
    with pytest.raises(subject.BindingRefusal) as refusal:
        subject.build(
            surface_source=surface_path.read_bytes(),
            type_sets={"CQ-01": ["Asset", "Inspection"]},
            replay_receipt="PENDING",
            contract_source=contract_path.read_bytes(),
        )
    assert "TYPE_SET_NOT_CLOSED_UNDER_SUBTYPES" in str(refusal.value)
    assert "CQ-01 omits ProbeInspection" in str(refusal.value)

    completed = _run(
        "bind_from_surface",
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(contract_path),
            "--type-sets",
            str(
                _type_set_file(
                    private_workspace, {"CQ-01": ["Asset", "Inspection"]}
                )
            ),
            "--replay-receipt",
            "PENDING",
            "--output",
            str(output),
        ],
    )
    assert completed.returncode == 2
    assert "TYPE_SET_NOT_CLOSED_UNDER_SUBTYPES" in completed.stderr
    assert not output.exists()

    # The closed set binds, and the binding it writes is the one the executor
    # can project: every reached record's own type is named.
    closed = subject.build(
        surface_source=surface_path.read_bytes(),
        type_sets={"CQ-01": ["Asset", "Inspection", "ProbeInspection"]},
        replay_receipt="PENDING",
        contract_source=contract_path.read_bytes(),
    )
    assert closed["type_sets"]["CQ-01"] == ["Asset", "Inspection", "ProbeInspection"]
    assert closed["expansion"]["closure_checked"] == subject.CLOSURE_CHECK
    # The contract is required: a binding cannot be written without one.
    assert _run(
        "bind_from_surface",
        [
            "--surface",
            str(surface_path),
            "--type-sets",
            str(_type_set_file(private_workspace, {"CQ-02": ["Asset"]})),
            "--replay-receipt",
            "PENDING",
            "--output",
            str(private_workspace / "binding-no-contract.json"),
        ],
    ).returncode == 2
    assert not (private_workspace / "binding-no-contract.json").exists()


def test_offline_validation_is_run_23s_with_the_run_id_moved() -> None:
    """Carried whole, and all four stages still run-23's numbers.

    ``offline_validation.py`` computes the v4.4 restriction, the v4.9 collapse,
    the v4.12 restoration and v4.13's SUBJECT_ANY reachability on run-09's
    frozen record. None of the four moves under this cell, so all four stages
    must return run-23's numbers exactly, key for key; a rule that returns other
    numbers is a different rule and this test fails rather than the record being
    adjusted to match. The record differs from run-23's in three strings and
    nothing else: the run id, the schema string and the digest of the binder it
    read, which moves because the binder's own docstring names the cell.
    """

    here = (HERE / "offline_validation.py").read_text(encoding="utf-8")
    prior = (RUN_23 / "offline_validation.py").read_text(encoding="utf-8")

    for carried in (
        "def witness_identity(",
        '"rows_one_per_witness"',
        '"rows_re_projected"',
        '"rows_re_projected_under_another_label"',
        '"and_change_id": "ONE_ROW_PER_WITNESS_OWN_TYPE_PROJECTION"',
    ):
        assert carried in here, carried
        assert carried in prior, carried

    record = json.loads(OFFLINE_VALIDATION.read_bytes())
    prior_record = json.loads((RUN_23 / "offline-validation.json").read_bytes())
    contract = json.loads(CONTRACT_PATH.read_bytes())["offline_validation"]
    totals = record["totals"]
    prior_totals = prior_record["totals"]

    assert record["run_id"] == "run-24"
    assert prior_record["run_id"] == "run-23"
    assert record["schema"] == "malleus.paper-v4.run-24-offline-validation/v3"
    assert prior_record["schema"] == "malleus.paper-v4.run-23-offline-validation/v3"
    assert record["change_id"] == "ENTITY_KIND_RESTRICTED"
    assert record["and_change_id"] == "ONE_ROW_PER_WITNESS_OWN_TYPE_PROJECTION"
    assert record["third_change_id"] == "ENTITY_NO_SUBJECT_REACHABILITY"
    assert record["fourth_change_id"] == "SUBJECT_ANY_REACHABILITY"
    assert record["fourth_change_id"] == prior_record["fourth_change_id"]
    assert record["measured_on"] == "run-09"

    # All four stages, unchanged against run-23's record, key by key, question
    # by question. Nothing is filtered out of the comparison, because nothing
    # was added.
    assert totals == prior_totals
    assert record["questions"] == prior_record["questions"]
    # The whole record equals run-23's but for the three strings the run id
    # reaches, so a stage that moved would have to move a count and there is no
    # count here that is not run-23's.
    assert {
        name: value
        for name, value in record.items()
        if name not in {"run_id", "schema", "inputs", "non_claim"}
    } == {
        name: value
        for name, value in prior_record.items()
        if name not in {"run_id", "schema", "inputs", "non_claim"}
    }
    assert record["inputs"]["binder"]["sha256"] != (
        prior_record["inputs"]["binder"]["sha256"]
    )
    assert {
        name: value
        for name, value in record["inputs"].items()
        if name != "binder"
    } == {
        name: value
        for name, value in prior_record["inputs"].items()
        if name != "binder"
    }
    assert totals["rows_reached_by_subject_any"] == 407
    assert totals["rows_reached_by_subject_any_witnesses"] == 387
    assert totals["rows_reached_by_subject_any_beyond_typed_subject"] == 156
    assert (
        totals["rows_reached_by_subject_any_beyond_typed_subject_witnesses"] == 143
    )
    assert totals["rows_reached_by_subject_any_by_label"] == {
        "PARTIAL": 2,
        "SUPPORTED": 405,
    }
    assert sum(totals["rows_reached_by_subject_any_by_label"].values()) == (
        totals["rows_reached_by_subject_any"]
    )
    # The rows beyond the typed pairing are a proper part of what the kind
    # reaches, and they are what the change is for: a record of a listed
    # bearing type whose subject's type the set does not list.
    assert 0 < totals["rows_reached_by_subject_any_beyond_typed_subject"] < (
        totals["rows_reached_by_subject_any"]
    )
    assert totals["rows_reached_by_subject_any_beyond_typed_subject_witnesses"] <= (
        totals["rows_reached_by_subject_any_witnesses"]
    )
    assert sum(
        question["rows_reached_by_subject_any"] for question in record["questions"]
    ) == totals["rows_reached_by_subject_any"]
    # The two additions do not overlap: a record either carries a subject or it
    # does not, so no row is counted by both stages.
    assert totals["rows_restored_by_entity_no_subject"] + (
        totals["rows_reached_by_subject_any"]
    ) <= totals["rows_v3"]
    # The carried third stage, unchanged.
    assert totals["rows_restored_by_entity_no_subject"] == 429
    assert totals["rows_restored_witnesses"] == 373
    assert totals["rows_restored_new_witnesses"] == 373
    assert totals["rows_restored_by_label"] == {"PARTIAL": 2, "SUPPORTED": 427}
    assert sum(totals["rows_restored_by_label"].values()) == (
        totals["rows_restored_by_entity_no_subject"]
    )
    # Every restored row is a row the v4.4 restriction removed, and every
    # restored witness is one no kept case reaches: the addition gives back
    # what that removal took and reaches nothing the other kinds already did.
    assert totals["rows_restored_by_entity_no_subject"] <= totals["rows_removed"]
    assert totals["rows_restored_new_witnesses"] == (
        totals["rows_restored_witnesses"]
    )
    assert sum(
        question["rows_restored_by_entity_no_subject"]
        for question in record["questions"]
    ) == totals["rows_restored_by_entity_no_subject"]
    assert totals["rows_v3"] == 1466
    assert totals["rows_kept"] == 630
    assert totals["rows_kept_by_label"] == {"PARTIAL": 12, "SUPPORTED": 618}
    assert totals["rows_one_per_witness"] == 463
    assert totals["rows_re_projected"] == 167
    assert totals["rows_one_per_witness"] + totals["rows_re_projected"] == (
        totals["rows_kept"]
    )
    assert totals["rows_re_projected_under_another_label"] == 0
    assert sum(totals["rows_one_per_witness_by_kind"].values()) == (
        totals["rows_one_per_witness"]
    )
    assert sum(totals["rows_one_per_witness_by_label"].values()) == (
        totals["rows_one_per_witness"]
    )
    for question in record["questions"]:
        assert question["rows_one_per_witness"] + question["rows_re_projected"] == (
            question["rows_kept"]
        )
    assert sum(
        question["rows_one_per_witness"] for question in record["questions"]
    ) == totals["rows_one_per_witness"]

    # The record is what the script returns today, not a copy of run-23's.
    assert _module("offline_validation").validate() == record
    assert record["inputs"]["binder"]["path"] == (
        "paper-v4/experiment-v4/run-24/bind_from_surface.py"
    )
    assert record["inputs"]["binder"]["sha256"] == _digest(
        (HERE / "bind_from_surface.py").read_bytes()
    )

    # The contract carries the same four numbers, so neither can drift alone.
    assert contract["rows_kept"] == totals["rows_kept"]
    assert contract["rows_one_per_witness"] == totals["rows_one_per_witness"]
    assert contract["rows_re_projected"] == totals["rows_re_projected"]
    assert contract["rows_re_projected_under_another_label"] == 0
    assert contract["and_change_id"] == record["and_change_id"]
    assert contract["third_change_id"] == record["third_change_id"]
    assert contract["fourth_change_id"] == record["fourth_change_id"]
    assert contract["rows_reached_by_subject_any"] == (
        totals["rows_reached_by_subject_any"]
    )
    assert contract["rows_reached_by_subject_any_witnesses"] == (
        totals["rows_reached_by_subject_any_witnesses"]
    )
    assert contract["rows_reached_by_subject_any_beyond_typed_subject"] == (
        totals["rows_reached_by_subject_any_beyond_typed_subject"]
    )
    assert contract[
        "rows_reached_by_subject_any_beyond_typed_subject_witnesses"
    ] == totals["rows_reached_by_subject_any_beyond_typed_subject_witnesses"]
    assert contract["rows_restored_by_entity_no_subject"] == (
        totals["rows_restored_by_entity_no_subject"]
    )
    assert contract["rows_restored_witnesses"] == totals["rows_restored_witnesses"]
    assert contract["rows_restored_new_witnesses"] == (
        totals["rows_restored_new_witnesses"]
    )
    assert contract["carried_from"] == "run-23"
    assert contract["record"] == "paper-v4/experiment-v4/run-24/offline-validation.json"
    assert contract["schema"] == record["schema"]


def test_every_stated_change_is_present_in_the_file_that_carries_it() -> None:
    """One marker per instrument change id, read from the contract, found in its
    subject.

    Every one of the thirty-six entries run-23 closed with is carried, the
    eighteen instrument ones included, except that this cell's producer record
    keeps the id run-23's had and moves its subject here; one entry is added,
    the question file's. That leaves eight entries with no instrument file to
    grep for, the seven closed cells' producer records and this cell's own. The
    two Core entries the pin still reads are carried too, and their evidence is
    the pinned commit rather than a file here. The sets are disjoint and
    together they are the whole change list, so an entry added or dropped fails
    here.
    """

    changes = {
        str(item["id"]): item
        for item in json.loads(CONTRACT_PATH.read_bytes())["protocol"]["changes"]
    }

    assert set(changes) == set(DELTA_MARKERS) | set(CORE_CHANGE_IDS) | {
        MODEL_CHANGE_ID,
        *PRIOR_MODEL_CHANGE_IDS,
    }
    assert set(DELTA_MARKERS) & set(CORE_CHANGE_IDS) == set()
    for change_id in (MODEL_CHANGE_ID, *PRIOR_MODEL_CHANGE_IDS):
        assert change_id not in set(DELTA_MARKERS) | set(CORE_CHANGE_IDS)
    assert set(READ_AT_THE_PIN_CORE_CHANGE_IDS) <= set(CORE_CHANGE_IDS)
    assert len(changes) == 37
    prior_changes = {
        str(item["id"]): item
        for item in json.loads(
            (RUN_23 / "run-contract.json").read_bytes()
        )["protocol"]["changes"]
    }
    assert len(prior_changes) == 36
    assert set(changes) - set(prior_changes) == set(RUN_24_CHANGES)
    assert set(prior_changes) - set(changes) == set()
    # The one entry this cell adds is the only entry that is not carried apart
    # from its own producer record, and it is the entry the table above
    # declares.
    own = {
        change_id
        for change_id, entry in changes.items()
        if "carried_from" not in entry
    }
    assert own == set(RUN_24_CHANGES) | {MODEL_CHANGE_ID}
    stated = set(RUN_24_CHANGES)
    for change_id, (relative, marker) in DELTA_MARKERS.items():
        text_of = (ROOT / relative).read_text(encoding="utf-8")
        assert marker in text_of, change_id
        entry = json.dumps(changes[change_id])
        assert Path(relative).name in entry, change_id
        assert changes[change_id]["detail"].strip()
        assert changes[change_id]["why"].strip()
        if change_id in stated:
            assert "carried_from" not in changes[change_id], change_id
            assert changes[change_id]["carried_since"] == "run-24", change_id
            # Every file the entry names is the file the table names, and the
            # entry's subject is the question file the change is about.
            for name in RUN_24_CHANGES[change_id]:
                assert (ROOT / name).is_file(), (change_id, name)
        else:
            assert changes[change_id]["carried_from"] == "run-23", change_id
    for change_id in CORE_CHANGE_IDS:
        entry = changes[change_id]
        assert entry["pin_status"] in CORE_PIN_STATUSES
        assert entry["core_task"].startswith("Core-")
        # Every Core entry is carried this cell, the two the pin still reads
        # included: Core does not move, so no entry here is this cell's own.
        assert entry["carried_from"] == "run-23", change_id
        if change_id in READ_AT_THE_PIN_CORE_CHANGE_IDS:
            # Carried, and still read: the pin recomputes the status at the
            # commit run-23 pinned against the same v4.8 baseline. Both were
            # written at run-18 and carried since, so ``carried_since`` stays
            # there and only ``carried_from`` steps.
            assert entry["pin_status"] in READ_AT_THE_PIN_STATUSES, change_id
            assert entry["carried_since"] == "run-18", change_id
            assert entry["baseline_commit"] == V4_9_COORDINATE, change_id
            assert entry["carried"] == (
                "READ_AGAIN_AT_THE_SAME_COMMIT_NOT_CARRIED_UNREAD"
            ), change_id
        else:
            assert entry["pin_status"] == CARRIED_PIN_STATUS, change_id
    # This cell's own producer entry has no instrument file at all. Core does
    # not move, the producer condition does not move and the harness does not
    # move; the question file does, and the entry says so and points at the
    # entry that carries it rather than restating it.
    model = changes[MODEL_CHANGE_ID]
    assert "carried_from" not in model
    assert model["kind"] == "MODEL_CELL"
    assert model["core_delta"] == "NONE"
    assert model["harness_delta"] == "NONE_THE_INSTRUMENTS_ARE_RUN_23S"
    assert model["producer_delta"] == "NONE"
    assert model["question_file_delta"] == "ONE_CHANGE_STATED_AS_ITS_OWN_ENTRY"
    assert model["replicates"] == ["run-20", "run-21", "run-22", "run-23"]
    assert model["producer_matched_cells"] == ["run-20", "run-21", "run-22", "run-23"]
    assert model["harness_matched_cell"] == "run-23"
    assert model["review_protocol_matched_cell"] == "run-23"
    assert model["model_fields_moved"] == []
    assert model["subject_block"] == "producer"
    # The id is run-23's, because this cell replicates at the same protocol
    # version. What moves is the subject, and the entry says that in one field
    # rather than leaving two cells to be read off one id.
    assert model["carried_since"] == "run-23"
    assert model["restated_at"] == "run-24"
    assert model["restated_note"].strip()
    assert model["subject"] == (
        "paper-v4/experiment-v4/run-24/run-contract.json#producer"
    )
    assert prior_changes[MODEL_CHANGE_ID]["subject"] == (
        "paper-v4/experiment-v4/run-23/run-contract.json#producer"
    )
    assert "core_task" not in model
    # The comparability statement, which is the one thing this cell must not
    # leave to a reader's inference: every side with run-23, the producer side
    # and the review protocol with run-22, the producer side alone with run-20
    # and run-21.
    assert model["comparability"] == (
        "ROWS_AND_REVIEWS_ARE_COMPARABLE_WITH_RUN_23_ON_THE_PRODUCER_SIDE_THE"
        "_QUERY_SIDE_AND_THE_REVIEW_PROTOCOL_WITH_CQ_C_03_READ_AGAINST_THREE"
        "_SEMANTICS_WITH_RUN_22_ON_THE_PRODUCER_SIDE_AND_THE_REVIEW_PROTOCOL"
        "_AND_WITH_RUN_20_AND_RUN_21_ON_THE_PRODUCER_SIDE_ONLY"
    )
    assert model["comparability"] == (
        json.loads(CONTRACT_PATH.read_bytes())["scope"]["comparability"]
    )
    assert "five draws of one condition" in model["comparability_detail"]
    assert "three required semantics here and four there" in (
        model["comparability_detail"]
    )
    for name in (*CARRIED_WITH_THE_RUN_ID, "pin.py"):
        assert name not in model["subject"], name
    # The seven closed cells' records keep their own subjects and their own
    # model fields; none may be read as this cell's producer. Run-20's,
    # run-21's and run-22's are among them and carry the same three model
    # fields this cell runs, which is what makes this a replicate on the
    # producer side: the entries that name them are those cells', and this
    # cell's own is the one above.
    for change_id, cell in (
        ("HAIKU_4_5_PRODUCER_AT_V4_9", "run-17"),
        ("HAIKU_4_5_PRODUCER_AT_V4_10", "run-18"),
        ("OPUS_5_PRODUCER_AT_V4_10", "run-20"),
        ("OPUS_5_REPLICATE_AT_V4_10", "run-21"),
        ("OPUS_5_REPLICATE_AT_V4_12", "run-22"),
        ("SONNET_5_PRODUCER_AT_V4_9", "run-16"),
        ("SONNET_5_PRODUCER_AT_V4_10", "run-19"),
    ):
        entry = changes[change_id]
        assert entry["kind"] == "MODEL_CELL"
        assert entry["carried_from"] == "run-23", change_id
        assert entry["subject_cell"] == cell, change_id
        assert entry["subject"] == (
            f"paper-v4/experiment-v4/{cell}/run-contract.json#producer"
        ), change_id


def test_the_producer_block_is_run_23s_key_for_key_with_nothing_moved() -> None:
    """The whole of what a replicate is, read off the contract and the manifest.

    Run-24 moves nothing. The producer block is run-23's key for key, the three
    model fields included, and the comparison below is the whole guard: one key
    that differed would make this a matrix cell and would be read later as the
    cause of whatever the two cells do not share. Run-23 moved these three
    fields off run-19's and was admitted at its second runner attempt after one
    defect; holding them here is what makes the pair two draws of one condition.
    """

    contract = json.loads(CONTRACT_PATH.read_bytes())
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())
    producer = contract["producer"]
    prior = json.loads((RUN_23 / "run-contract.json").read_bytes())["producer"]

    assert set(producer) == set(prior)
    assert {
        key: value for key, value in producer.items() if prior[key] != value
    } == {}
    assert producer == prior
    assert {key: producer[key] for key in MODEL_FIELDS} == MODEL_FIELDS
    assert {key: prior[key] for key in MODEL_FIELDS} == PRIOR_MODEL_FIELDS
    assert MODEL_FIELDS == PRIOR_MODEL_FIELDS
    assert manifest["producer"] == producer
    # The manifest is the file the workspace is built from, so the model fields
    # have to be the same three there too.
    assert {key: manifest["producer"][key] for key in MODEL_FIELDS} == MODEL_FIELDS
    # And the harness the model runs under is the same harness.
    assert producer["harness"] == prior["harness"]
    assert producer["kind"] == prior["kind"] == "CLAUDE_CODE_FRESH_SUBAGENT"
    assert producer["session"] == prior["session"] == "FRESH_SINGLE_SESSION"
    assert producer["reasoning_effort"] == prior["reasoning_effort"]
    assert producer["max_compiler_diagnostic_returns"] == 2
    assert producer["max_ontology_revision_rounds"] == 2
    assert producer["fallback"] == "FORBIDDEN"
    assert producer["network"] == "FORBIDDEN"
    assert producer["delegation"] == "FORBIDDEN"


def test_producer_preparation_refuses_output_outside_private() -> None:
    subject = _module("prepare_producer")

    with pytest.raises(subject.ProducerPreparationRefusal):
        subject.prepare(ROOT / "ontology/malleus.yaml", ROOT / "tmp-producer")


def test_producer_preparation_installs_the_claude_layout_and_exact_closure(
    private_workspace: Path,
) -> None:
    subject = _module("prepare_producer")
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())
    output = private_workspace / "producer"

    receipt = subject.prepare(ROOT / manifest["declared_inputs"][1]["source"], output)

    installed = {
        str(path.relative_to(output))
        for path in output.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    assert installed == {item["target"] for item in manifest["declared_inputs"]}
    assert len(installed) == 8
    assert ".claude/skills/malleus-acolyte/SKILL.md" in installed
    assert not (output / ".codex").exists()
    assert receipt["status"] == "FROZEN"
    assert receipt["core"] == manifest["core"]
    assert (private_workspace / "producer-input-receipt.json").exists()


def test_the_history_profile_is_staged_as_its_canonical_bytes(
    private_workspace: Path,
) -> None:
    """The carried v4.12 staging: the staged file's digest is the profile identity.

    shop-01's producer wrote the staged profile file's digest into four
    population plans, as the parent's phase-two message told it to, and the
    compiler refused every one with IDENTITY_MISMATCH because it digests the
    profile's canonical bytes and not the file's (E-0203, cause B). Run-23
    answered that and this cell carries it unchanged, so the staging is exactly
    run-23's and no declared input moves against run-23's manifest at all.
    """

    subject = _module("prepare_producer")
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())
    contract = json.loads(CONTRACT_PATH.read_bytes())
    declared = {item["name"]: item for item in manifest["declared_inputs"]}
    profile = declared["SOURCE_ASSERTION_PROFILE"]
    output = private_workspace / "producer"

    # The manifest states a staging per input, and exactly one is canonical.
    assert subject.CANONICAL_JSON_INPUTS == {"SOURCE_ASSERTION_PROFILE"}
    assert {
        name: item["staged_as"] for name, item in declared.items()
    } == {
        name: (
            subject.CANONICAL_JSON
            if name in subject.CANONICAL_JSON_INPUTS
            else subject.SOURCE_BYTES
        )
        for name in declared
    }
    # The source bytes and the staged bytes are stated separately, and they
    # differ for the profile and for nothing else.
    for name, item in declared.items():
        moved = item["sha256"] != item["source_sha256"]
        assert moved == (name in subject.CANONICAL_JSON_INPUTS), name

    receipt = subject.prepare(ROOT / declared["SELECTED_READING"]["source"], output)
    staged = (output / profile["target"]).read_bytes()
    source = subject._git_show(manifest["core"]["commit"], profile["source"])

    assert staged != source
    assert staged == subject._canonical(source)
    assert json.loads(staged) == json.loads(source)
    assert not staged.endswith(b"\n")
    assert staged == json.dumps(
        json.loads(source),
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    # The staged file's digest is the profile identity the manifest, the
    # contract and the pin all record, and it is not the file's own.
    assert _digest(staged) == profile["sha256"]
    assert _digest(source) == profile["source_sha256"]
    assert _digest(staged) == manifest["history_profile"]["profile_identity"]
    assert _digest(staged) == contract["history"]["profile_sha256"]
    assert _digest(source) == contract["history"]["profile_file_sha256"]
    assert contract["history"]["profile_staging"] == (
        "CANONICAL_JSON_THE_STAGED_FILES_DIGEST_IS_THE_IDENTITY"
    )
    assert {
        item["name"]: item["sha256"] for item in receipt["files"]
    }["SOURCE_ASSERTION_PROFILE"] == profile["sha256"]
    # Run-23 staged the profile the same way, so nothing moved against its
    # manifest: the staging is carried and the cause table has nothing to say.
    prior = {
        item["name"]: (item["sha256"], item["staged_as"])
        for item in json.loads(
            (RUN_23 / "producer-input-manifest.json").read_bytes()
        )["declared_inputs"]
    }
    assert prior["SOURCE_ASSERTION_PROFILE"] == (
        profile["sha256"],
        subject.CANONICAL_JSON,
    )
    assert manifest["moved_since"]["moved"] == []
    assert manifest["moved_since"]["moved_cause"] == {}
    assert manifest["moved_since"]["reference_run"] == "run-23"
    assert sorted(manifest["moved_since"]["unchanged"]) == sorted(declared)
    # Every other declared input is staged as the bytes the commit carries.
    for name, item in declared.items():
        if name in subject.CANONICAL_JSON_INPUTS or name == "SELECTED_READING":
            continue
        assert (output / item["target"]).read_bytes() == subject._git_show(
            manifest["core"]["commit"], item["source"]
        ), name


def test_producer_preparation_refuses_a_staging_the_manifest_does_not_declare(
    monkeypatch: pytest.MonkeyPatch, private_workspace: Path
) -> None:
    """The builder and the manifest have to agree on what is staged how.

    A manifest that stages another input canonical, or none, is a manifest this
    builder did not write, and staging bytes nobody declared is exactly the
    class of defect E-0203 turned up. The check is on the set, so both
    directions refuse.
    """

    subject = _module("prepare_producer")
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())
    reading = ROOT / "private/paper-v4-text-layer/selected-reading.json"

    for name, staging in (
        ("SOURCE_ASSERTION_PROFILE", subject.SOURCE_BYTES),
        ("RESEARCH_PACK", subject.CANONICAL_JSON),
    ):
        drifted = deepcopy(manifest)
        for item in drifted["declared_inputs"]:
            if item["name"] == name:
                item["staged_as"] = staging
        path = private_workspace / f"manifest-{name}.json"
        path.write_bytes(_canonical(drifted))
        monkeypatch.setattr(subject, "MANIFEST", path)
        with pytest.raises(subject.ProducerPreparationRefusal) as refusal:
            subject.prepare(reading, private_workspace / f"producer-{name}")
        assert "canonical JSON" in str(refusal.value), name

    # An unknown staging name is refused by the writer rather than guessed at.
    with pytest.raises(subject.ProducerPreparationRefusal) as refusal:
        subject.staged_bytes({"name": "X", "staged_as": "RAW"}, b"{}")
    assert "unknown staging" in str(refusal.value)


def test_producer_preparation_refuses_a_drifted_declared_input(
    private_workspace: Path,
) -> None:
    subject = _module("prepare_producer")

    with pytest.raises(subject.ProducerPreparationRefusal):
        subject.prepare(FIXTURE / "reading.json", private_workspace / "producer")


def test_producer_preparation_reads_every_tracked_input_from_the_commit(
    private_workspace: Path,
) -> None:
    subject = _module("prepare_producer")
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())
    commit = manifest["core"]["commit"]
    seen: list[tuple[str, str]] = []
    real = subject._git_show

    def recording(requested: str, path: str) -> bytes:
        seen.append((requested, path))
        return real(requested, path)

    subject._git_show = recording
    receipt = subject.prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json",
        private_workspace / "producer",
    )

    tracked = [
        item["source"]
        for item in manifest["declared_inputs"]
        if item["name"] != "SELECTED_READING"
    ]
    assert sorted(seen) == sorted((commit, source) for source in tracked)
    assert len(tracked) == 7
    assert receipt["core"]["commit"] == commit


def test_the_installed_skill_is_the_bytes_at_the_commit_not_the_live_tree(
    private_workspace: Path,
) -> None:
    subject = _module("prepare_producer")
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())
    output = private_workspace / "producer"

    subject.prepare(ROOT / "private/paper-v4-text-layer/selected-reading.json", output)

    skill = output / ".claude/skills/malleus-acolyte/SKILL.md"
    frozen = subprocess.run(
        ["git", "show", f"{manifest['core']['commit']}:{skill.relative_to(output)}"],
        capture_output=True,
        check=True,
        cwd=ROOT,
    ).stdout
    assert skill.read_bytes() == frozen
    assert _digest(frozen) == next(
        item["sha256"]
        for item in manifest["declared_inputs"]
        if item["name"] == "MALLEUS_NASCENT_PROJECT_SKILL"
    )
    assert "install-skills" not in (HERE / "prepare_producer.py").read_text(
        encoding="utf-8"
    )


def test_producer_preparation_refuses_an_input_absent_at_the_recorded_commit() -> None:
    subject = _module("prepare_producer")
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())

    with pytest.raises(subject.ProducerPreparationRefusal):
        subject._git_show(manifest["core"]["commit"], "ontology/no-such-pack.yaml")


def test_ontology_gate_returns_one_aggregate_grounding_diagnostic(
    private_workspace: Path,
) -> None:
    subject = _module("compile_ontology_candidate")
    producer = private_workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    output = private_workspace / "gate-01"

    assert not subject.compile_candidate(
        ontology_path=FIXTURE / "inspection-note.yaml",
        producer_root=producer,
        output=output,
        attempt=1,
    )

    diagnostic = json.loads((output / "diagnostic.json").read_bytes())
    assert diagnostic["status"] == "REFUSED"
    assert diagnostic["stage"] == "PACK_GROUNDING"
    assert diagnostic["reason"] == "DIRECT_ROOT_GROUNDING_REQUIRED"
    assert diagnostic["detail"] == (
        "DIRECT_ROOT_GROUNDING_REQUIRED: project classes extend Malleus roots"
        " without grounding: Asset extends Entity; Inspection extends Entity;"
        " InspectionOfRelation extends Relation; VibrationReading extends Entity"
    )
    assert {path.name for path in output.iterdir()} == {"diagnostic.json"}


def test_ontology_gate_accepts_a_pack_derived_project(
    private_workspace: Path,
) -> None:
    subject = _module("compile_ontology_candidate")
    producer = private_workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    ontology = private_workspace / "candidate.yaml"
    ontology.write_text(
        """id: https://example.org/gate-probe
name: gate_probe
imports: [linkml:types, malleus, research]
classes:
  ProbeObservation:
    is_a: Observation
""",
        encoding="utf-8",
    )
    output = private_workspace / "gate-02"

    assert subject.compile_candidate(
        ontology_path=ontology,
        producer_root=producer,
        output=output,
        attempt=2,
    )

    diagnostic = json.loads((output / "diagnostic.json").read_bytes())
    surface = json.loads((output / "population-surface.json").read_bytes())
    assert diagnostic["status"] == "ACCEPTED"
    assert diagnostic["stage"] == "COMPLETE"
    assert surface["schema"] == "malleus.paper-v4.population-surface/v2"
    assert surface["families_admitted"] == ["entities", "events", "relations"]
    assert any(
        item["name"] == "ProbeObservation" and item["family"] == "ENTITY"
        for item in surface["record_types"]
    )
    assert {path.name for path in output.iterdir()} == {
        "diagnostic.json",
        "grounding-receipt.json",
        "population-surface.json",
        "validated-contract.json",
    }


def test_an_event_type_reaches_the_surface_and_one_event_record_is_admitted(
    private_workspace: Path,
) -> None:
    """The run-02 defect, closed at both ends.

    Run-02's surface listed no Event type although the bound profile admits
    events and the accepted ontology declared one, so the producer wrote typed
    gaps instead of Event records (E-0122 finding 3). Here the surface lists the
    Event subclass under family EVENT, and a capture whose ``records`` carry an
    ``events`` envelope with a full derivation admits, replays and exports it.
    """
    producer = private_workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    ontology = _event_ontology(private_workspace)
    gate = private_workspace / "gate-event"

    assert _module("compile_ontology_candidate").compile_candidate(
        ontology_path=ontology,
        producer_root=producer,
        output=gate,
        attempt=1,
    )

    surface = json.loads((gate / "population-surface.json").read_bytes())
    families = {item["name"]: item["family"] for item in surface["record_types"]}
    assert surface["schema"] == "malleus.paper-v4.population-surface/v2"
    assert surface["families_admitted"] == ["entities", "events", "relations"]
    assert families[EVENT_TYPE] == "EVENT"
    assert families["Event"] == "EVENT"
    assert families["Asset"] == "ENTITY"
    assert families["InspectionOfRelation"] == "RELATION"
    assert "EVENT_PARTICIPATION" not in set(families.values())
    event_type = next(
        item for item in surface["record_types"] if item["name"] == EVENT_TYPE
    )
    assert "event_type" in {slot["name"] for slot in event_type["slots"]}

    results = private_workspace / "event-results"
    completed = _run(
        "run",
        [
            *_source_arguments(ontology),
            "--reading",
            str(FIXTURE / "reading.json"),
            "--population",
            str(_event_population_file(private_workspace)),
            "--capture-id",
            CAPTURE_ID,
            "--plan-id",
            PLAN_ID,
            "--source-id",
            SOURCE_ID,
            "--artifact-id",
            ARTIFACT_ID,
            "--ledger",
            str(private_workspace / "event-history.jsonl"),
            "--results",
            str(results),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )
    assert completed.returncode == 0, completed.stderr

    result = json.loads((results / "run-result.json").read_bytes())
    export = json.loads((results / "export-records.json").read_bytes())
    summary = json.loads((results / "trace-summary.json").read_bytes())
    traces = {item["record_id"]: item for item in summary["records"]}

    assert result["status"] == "ADMITTED_AND_REPLAYED"
    assert result["reopen_matches_admitted"] == {
        "receipt": True,
        "export_records": True,
    }
    assert result["graph"]["events"] == 1
    assert result["graph"]["entities"] == 2
    assert result["graph"]["relations"] == 1
    assert result["graph"]["event_participations"] == 0
    assert result["records_traced"] == 4
    assert export["events"] == [
        {
            "id": EVENT_RECORD_ID,
            "properties": {"event_type": "INSPECTION"},
            "type": EVENT_TYPE,
        }
    ]
    assert traces[EVENT_RECORD_ID]["record_type"] == EVENT_TYPE
    assert [item["path"] for item in traces[EVENT_RECORD_ID]["derivations"]] == [
        ["properties", "event_type"]
    ]


def test_run_admits_replays_and_reproduces_the_same_receipt(
    private_workspace: Path,
) -> None:
    results, result = _executed(private_workspace)

    assert result["schema"] == "malleus.paper-v4.run-24-result/v1"
    assert result["run_id"] == "run-24"
    assert result["status"] == "ADMITTED_AND_REPLAYED"
    assert result["reopen_matches_admitted"] == {
        "receipt": True,
        "export_records": True,
    }
    assert result["replay_receipt_sha256"] == _digest(
        (results / "replay-receipt.json").read_bytes()
    )
    assert result["capture"]["capture_id"] == CAPTURE_ID
    assert result["capture"]["capture_sha256"] == _digest(
        (FIXTURE / "document-capture.json").read_bytes()
    )
    assert result["reading_sha256"] == _digest((FIXTURE / "reading.json").read_bytes())
    assert result["plan"]["plan_id"] == PLAN_ID
    assert result["plan"]["status"] == "CHANGE_SET"
    assert result["graph"]["entities"] == 2
    assert result["graph"]["relations"] == 1
    assert result["graph"]["events"] == 0
    assert result["gaps_by_kind"] == {
        "INTERVAL_NOT_EXPRESSIBLE": 1,
        "MODALITY_NOT_EXPRESSIBLE": 1,
        "TYPE_ABSENT": 1,
    }
    assert sorted(path.name for path in results.iterdir()) == [
        "census.json",
        "export-records.json",
        "gaps.json",
        "paper-events.json",
        "population-plan.json",
        "replay-receipt.json",
        "run-result.json",
        "trace-summary.json",
    ]


def test_run_records_exactly_one_paper_owned_stage_acceptance(
    private_workspace: Path,
) -> None:
    results, result = _executed(private_workspace)
    events = json.loads((results / "paper-events.json").read_bytes())

    assert [event["event"] for event in events["events"]] == [
        "ONTOLOGY_ACCEPTED_FOR_POPULATION"
    ]
    event = events["events"][0]
    assert event["ontology_sha256"] == _digest(
        (FIXTURE / "inspection-note.yaml").read_bytes()
    )
    assert event["non_claim"] == "STAGE_ACCEPTANCE_NOT_DOMAIN_ADEQUACY"
    assert event["actor_id"] == ACTOR
    assert event["transaction_time"] == TRANSACTION_TIME
    assert event["ontology_sha256"] == result["ontology_sha256"]


def test_run_traces_every_admitted_record_to_retained_inputs(
    private_workspace: Path,
) -> None:
    results, _ = _executed(private_workspace)
    summary = json.loads((results / "trace-summary.json").read_bytes())
    traces = {item["record_id"]: item for item in summary["records"]}

    assert set(traces) == {
        "asset:P-7",
        "inspection:P-7:2026-03-02",
        "inspection-of:P-7:2026-03-02",
    }
    for trace in traces.values():
        assert trace["plan_id"] == PLAN_ID
        assert trace["history_profile"]["profile_id"] == "source-assertion"
        assert isinstance(trace["evidence"], dict)
        assert trace["evidence"][CAPTURE_ID] == _digest(
            (FIXTURE / "document-capture.json").read_bytes()
        )
        assert trace["sources"][SOURCE_ID] == _digest(
            (FIXTURE / "reading.json").read_bytes()
        )
    assert "statement" not in json.dumps(summary)


def test_native_query_reads_only_the_replayed_graph(
    private_workspace: Path,
) -> None:
    _executed(private_workspace)
    binding = _binding_file(private_workspace)
    query_results = private_workspace / "query"

    completed = _run(
        "native_query",
        [
            "--ledger",
            str(private_workspace / "history.jsonl"),
            "--binding",
            str(binding),
            "--results",
            str(query_results),
        ],
    )
    assert completed.returncode == 0, completed.stderr

    result = json.loads((query_results / "query-result.json").read_bytes())
    assert result["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    assert result["inputs"]["query_binding_sha256"] == _digest(binding.read_bytes())
    rows = result["queries"][0]["rows"]
    assert len(rows) == 1
    assert rows[0]["source"] == {"inspected_on": "2026-03-02"}
    assert rows[0]["target"] == {"name": "P-7"}
    assert rows[0]["relation"] == {"relation_type": "INSPECTION_OF"}
    assert rows[0]["witness"] == {
        "relation_id": "inspection-of:P-7:2026-03-02",
        "source_id": "inspection:P-7:2026-03-02",
        "target_id": "asset:P-7",
    }


def test_native_query_traces_every_witness_and_selects_evidence_by_id(
    private_workspace: Path,
) -> None:
    _executed(private_workspace)
    query_results = private_workspace / "query"
    completed = _run(
        "native_query",
        [
            "--ledger",
            str(private_workspace / "history.jsonl"),
            "--binding",
            str(_binding_file(private_workspace)),
            "--results",
            str(query_results),
        ],
    )
    assert completed.returncode == 0, completed.stderr

    summary = json.loads((query_results / "trace-summary.json").read_bytes())
    traced = {item["record_id"]: item for item in summary["records"]}

    assert set(traced) == {
        "asset:P-7",
        "inspection:P-7:2026-03-02",
        "inspection-of:P-7:2026-03-02",
    }
    assert summary["witnesses_traced"] == 3
    assert summary["evidence_selection"] == "BY_RECORD_ID_NEVER_BY_POSITION"
    for trace in traced.values():
        assert trace["declared_evidence_resolved"] is True
        assert trace["evidence"][CAPTURE_ID] == _digest(
            (FIXTURE / "document-capture.json").read_bytes()
        )


def test_the_source_free_guard_refuses_and_counts_a_file_read() -> None:
    subject = _module("native_query")
    guard = subject._SourceFreeGuard()

    with pytest.raises(subject.NativeQueryRefusal):
        with guard:
            open(FIXTURE / "reading.json", "rb")

    assert guard.attempts == {"embedding_import": 0, "file_read": 1, "network": 0}


def test_native_query_refuses_a_binding_naming_an_absent_type(
    private_workspace: Path,
) -> None:
    _executed(private_workspace)
    binding = private_workspace / "bad-binding.json"
    binding.write_bytes(
        _canonical(
            {
                "schema": "malleus.paper-v4.native-query-binding/v6",
                "status": "FROZEN_AFTER_REPLAY",
                "queries": [
                    {
                        "id": "NQ-FIXTURE-02",
                        "question_id": "FIXTURE-02",
                        "cases": [
                            {
                                "kind": "RELATION",
                                "ordinal": 1,
                                "source_record_type": "Inspection",
                                "relation_record_type": "AbsentRelation",
                                "target_record_type": "Asset",
                                "output_fields": {
                                    "source": [],
                                    "relation": [],
                                    "target": [],
                                },
                            }
                        ],
                    }
                ],
            }
        )
    )

    completed = _run(
        "native_query",
        [
            "--ledger",
            str(private_workspace / "history.jsonl"),
            "--binding",
            str(binding),
            "--results",
            str(private_workspace / "query-refused"),
        ],
    )

    assert completed.returncode == 2
    assert "AbsentRelation" in completed.stderr
    assert not (private_workspace / "query-refused").exists()


# ---------------------------------------------------------------------------
# The carried v4.2 and v4.3 deltas, exercised rather than asserted.
# ---------------------------------------------------------------------------


LAUNCH_LOG = {
    "schema": "malleus.paper-v4.producer-launch-log/v2",
    "run": "run-24",
    "protocol": "v4.9",
    "launches": [
        {
            "ordinal": 1,
            "role": "PRODUCER",
            "phase": "ONTOLOGY",
            "first_stage": "ONTOLOGY_ATTEMPT_01",
            "harness": "Claude Code Agent tool, subagent_type general-purpose",
            "requested_model": "opus",
            "model_family": "Claude Opus 5",
            "model_id": "claude-opus-5",
            "usage_cumulative": {
                "tokens": 185877,
                "tool_uses": 17,
                "duration_ms": 1007660,
            },
            "usage_by_resume": [
                {
                    "after": "ONTOLOGY_ATTEMPT_02",
                    "tokens": 203752,
                    "tool_uses": 23,
                    "duration_ms": 1194022,
                },
                {
                    "after": "POPULATION",
                    "tokens": 371026,
                    "tool_uses": 72,
                    "duration_ms": 2696310,
                },
            ],
        }
    ],
    "gate": [{"attempt": 1, "status": "ACCEPTED"}],
    "runner": [
        {
            "attempt": 1,
            "status": "ADMITTED_AND_REPLAYED",
            "execution_commit": "0000000",
            "structural_diagnostic_returns_used": 0,
        }
    ],
    "query": {"rows_by_question": {}},
    "review": {"model_id": "claude-opus-5", "tokens": 322049},
}


def _gate_contract(surface: Path) -> Path:
    """The validated contract the gate wrote beside the surface it accepted.

    v4.12's binder reads it: the surface carries no ancestry and the closure
    check needs the contract's ``rdfs:subClassOf`` facts.
    """

    return surface.parent / "validated-contract.json"


def _gate_surface(workspace: Path) -> Path:
    """Compile the fixture-plus-Event ontology and return its accepted surface."""

    producer = workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    gate = workspace / "gate-binding"
    assert _module("compile_ontology_candidate").compile_candidate(
        ontology_path=_event_ontology(workspace),
        producer_root=producer,
        output=gate,
        attempt=1,
    )
    return gate / "population-surface.json"


def _subject_gate_surface(workspace: Path) -> Path:
    """Compile the fixture-plus-subject ontology and return its accepted surface."""

    producer = workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    gate = workspace / "gate-subject"
    assert _module("compile_ontology_candidate").compile_candidate(
        ontology_path=_subject_ontology(workspace),
        producer_root=producer,
        output=gate,
        attempt=1,
    )
    return gate / "population-surface.json"


def _type_set_file(directory: Path, type_sets: dict[str, list[str]]) -> Path:
    path = directory / "query-type-sets.json"
    path.write_bytes(_canonical(type_sets))
    return path


def test_the_gate_records_every_link_of_a_chained_cause(
    private_workspace: Path,
) -> None:
    """Run-05's attempt 01, with the cause in the file instead of beside it."""

    subject = _module("compile_ontology_candidate")
    producer = private_workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    ontology = private_workspace / "rejected-field.yaml"
    ontology.write_text(
        """id: https://example.org/gate-probe
name: gate_probe
comments: [a note the source boundary rejects]
imports: [linkml:types, malleus, research]
classes:
  ProbeObservation:
    is_a: Observation
""",
        encoding="utf-8",
    )
    output = private_workspace / "gate-chained"

    assert not subject.compile_candidate(
        ontology_path=ontology,
        producer_root=producer,
        output=output,
        attempt=1,
    )

    diagnostic = json.loads((output / "diagnostic.json").read_bytes())
    chain = diagnostic["cause_chain"]

    assert diagnostic["status"] == "REFUSED"
    assert diagnostic["reason"] == "IMPORT_READER_REFUSED"
    assert diagnostic["detail"] == "IMPORT_READER_REFUSED"
    assert len(chain) >= 2
    assert chain[0]["reason"] == diagnostic["reason"]
    assert chain[0]["detail"] == diagnostic["detail"]
    assert "rejected field 'comments'" in json.dumps(chain[1:])
    assert "rejected field 'comments'" in diagnostic["chained_cause"]
    assert all(set(link) == {"detail", "error_type", "reason"} for link in chain)


def test_an_unchained_refusal_records_one_link_and_no_chained_cause(
    private_workspace: Path,
) -> None:
    subject = _module("compile_ontology_candidate")
    producer = private_workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    output = private_workspace / "gate-unchained"

    assert not subject.compile_candidate(
        ontology_path=FIXTURE / "inspection-note.yaml",
        producer_root=producer,
        output=output,
        attempt=1,
    )

    diagnostic = json.loads((output / "diagnostic.json").read_bytes())

    assert diagnostic["reason"] == "DIRECT_ROOT_GROUNDING_REQUIRED"
    assert len(diagnostic["cause_chain"]) == 1
    assert diagnostic["chained_cause"] is None


def test_the_preflight_records_the_interpreter_and_the_locked_versions(
    private_workspace: Path,
) -> None:
    subject = _module("prepare_producer")

    receipt = subject.prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json",
        private_workspace / "producer",
    )
    interpreter = receipt["interpreter"]

    assert interpreter["status"] == "VERIFIED"
    assert interpreter["checked"] == "INTERPRETER_AND_LOCKED_COMPILER_VERSIONS"
    assert interpreter["prefix"] == interpreter["required_prefix"]
    assert interpreter["prefix"] == str((ROOT / ".venv").resolve())
    assert interpreter["locked_versions"] == interpreter["installed_versions"]
    assert set(interpreter["locked_versions"]) == {"linkml", "linkml-runtime"}
    assert interpreter["environment_lock_sha256"] == _digest(
        (ROOT / interpreter["environment_lock"]).read_bytes()
    )


def test_the_preflight_refuses_an_interpreter_that_is_not_the_repository_venv(
    monkeypatch: pytest.MonkeyPatch, private_workspace: Path
) -> None:
    subject = _module("prepare_producer")
    monkeypatch.setattr(subject.sys, "prefix", "/usr")

    with pytest.raises(subject.ProducerPreparationRefusal, match="interpreter is"):
        subject.prepare(
            ROOT / "private/paper-v4-text-layer/selected-reading.json",
            private_workspace / "producer",
        )

    assert not (private_workspace / "producer").exists()


def test_the_preflight_refuses_a_version_the_environment_lock_does_not_name(
    monkeypatch: pytest.MonkeyPatch, private_workspace: Path
) -> None:
    subject = _module("prepare_producer")
    monkeypatch.setattr(subject.metadata, "version", lambda name: "1.10.0")

    with pytest.raises(subject.ProducerPreparationRefusal, match="1.10.0"):
        subject.prepare(
            ROOT / "private/paper-v4-text-layer/selected-reading.json",
            private_workspace / "producer",
        )

    assert not (private_workspace / "producer").exists()


def test_the_binding_is_the_exhaustive_expansion_of_the_surface(
    private_workspace: Path,
) -> None:
    """One ENTITY case per type, the RELATION cross product, no SUBJECT case.

    This surface carries no subject reference, so no type is restricted and the
    three subject kinds expand to nothing and say so rather than being absent:
    SUBJECT, v4.12's ENTITY_NO_SUBJECT and v4.13's SUBJECT_ANY are all emitted
    for the subject-bearing types of a set and this set has none. The expansion
    is v4.3's for this surface.
    """

    subject = _module("bind_from_surface")
    surface_path = _gate_surface(private_workspace)
    surface = json.loads(surface_path.read_bytes())
    relations = sorted(
        item["name"] for item in surface["record_types"] if item["family"] == "RELATION"
    )
    types = ["Asset", "Inspection"]
    output = private_workspace / "binding-acceptance.json"

    subject.main(
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(_gate_contract(surface_path)),
            "--type-sets",
            str(_type_set_file(private_workspace, {"CQ-01": types})),
            "--replay-receipt",
            "PENDING",
            "--output",
            str(output),
        ]
    )

    binding = json.loads(output.read_bytes())
    query = binding["queries"][0]
    kinds = Counter(case["kind"] for case in query["cases"])
    asset = next(
        item for item in surface["record_types"] if item["name"] == "Asset"
    )
    expected_projection = [
        slot["name"]
        for slot in asset["slots"]
        if slot["qualified_name"] not in subject.HOUSEKEEPING_SLOTS
    ]

    assert binding["schema"] == "malleus.paper-v4.native-query-binding/v6"
    assert binding["bound_at_stage"] == "ONTOLOGY_ACCEPTANCE"
    assert binding["bound_after_replay_receipt_sha256"] == "PENDING"
    assert binding["population_surface_sha256"] == _digest(surface_path.read_bytes())
    assert binding["type_sets"] == {"CQ-01": types}
    assert binding["expansion"]["case_kinds"] == [
        "ENTITY",
        ENTITY_NO_SUBJECT,
        "RELATION",
        "SUBJECT",
        SUBJECT_ANY,
    ]
    assert binding["expansion"]["subject_bearing_record_types"] == []
    assert binding["expansion"]["closure_checked"] == subject.CLOSURE_CHECK
    assert binding["expansion"]["subject_slot"] == SUBJECT_SLOT
    assert binding["expansion"]["entity_case_scope"] == (
        "TYPES_IN_THE_SET_THAT_CARRY_NO_SUBJECT"
    )
    assert binding["expansion"]["entity_no_subject_case_scope"] == (
        "TYPES_IN_THE_SET_THAT_CARRY_SUBJECT_RESTRICTED_TO_RECORDS"
        "_WHOSE_SUBJECT_SLOT_IS_ABSENT"
    )
    assert binding["expansion"]["subject_any_case_scope"] == (
        "TYPES_IN_THE_SET_THAT_CARRY_SUBJECT_PAIRED_WITH_EVERY_ENTITY"
        "_TYPE_THE_SURFACE_DECLARES_AND_NOT_ONLY_THE_SETS"
    )
    assert ENTITY_NO_SUBJECT not in kinds
    assert SUBJECT_ANY not in kinds
    assert query["id"] == "NQ-CQ-01"
    assert query["question_id"] == "CQ-01"
    assert kinds == Counter(
        {"ENTITY": len(types), "RELATION": len(types) * len(types) * len(relations)}
    )
    assert len(query["cases"]) == len(types) + len(types) * len(types) * len(relations)
    assert [case["ordinal"] for case in query["cases"]] == list(
        range(1, len(query["cases"]) + 1)
    )
    relation_cases = [case for case in query["cases"] if case["kind"] == "RELATION"]
    entity_cases = [case for case in query["cases"] if case["kind"] == "ENTITY"]
    assert {case["relation_record_type"] for case in relation_cases} == set(relations)
    assert [case["record_type"] for case in entity_cases] == types
    assert expected_projection
    assert "id" not in expected_projection
    for case in entity_cases:
        if case["record_type"] == "Asset":
            assert case["output_fields"]["record"] == expected_projection
    for case in relation_cases:
        if case["source_record_type"] == "Asset":
            assert case["output_fields"]["source"] == expected_projection
        assert not set(case["output_fields"]["relation"]) & {
            "id",
            "source_id",
            "target_id",
        }

    # The binding the query executes is the binding the launch log pinned.
    _module("native_query").load_binding(output.read_bytes())


def test_a_subject_bearing_surface_gets_no_entity_case_for_the_bearing_type(
    private_workspace: Path,
) -> None:
    """The carried restrictions and v4.13's addition beside them.

    ``Inspection`` bears ``subject`` and ``Asset`` does not, so the expansion
    emits one plain ENTITY case for ``Asset`` and none for ``Inspection``, and
    reaches an attached ``Inspection`` through its SUBJECT cases. v4.12's
    ENTITY_NO_SUBJECT case for ``Inspection`` is carried. What v4.13 adds is one
    SUBJECT_ANY case for ``Inspection`` against every entity type the surface
    declares, and not against the two the set lists: the typed pairing stands
    and the new one is a superset of it, so a record whose subject's type the
    set leaves out is reached anyway.
    """

    binder = _module("bind_from_surface")
    surface_path = _subject_gate_surface(private_workspace)
    surface = json.loads(surface_path.read_bytes())
    relations = sorted(
        item["name"] for item in surface["record_types"] if item["family"] == "RELATION"
    )
    entities_on_surface = sorted(
        item["name"] for item in surface["record_types"] if item["family"] == "ENTITY"
    )
    types = ["Asset", "Inspection"]
    output = private_workspace / "binding-subject.json"

    binder.main(
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(_gate_contract(surface_path)),
            "--type-sets",
            str(_type_set_file(private_workspace, {"CQ-01": types})),
            "--replay-receipt",
            "PENDING",
            "--output",
            str(output),
        ]
    )

    binding = json.loads(output.read_bytes())
    query = binding["queries"][0]
    kinds = Counter(case["kind"] for case in query["cases"])
    subject_cases = [case for case in query["cases"] if case["kind"] == "SUBJECT"]
    entity_cases = [case for case in query["cases"] if case["kind"] == "ENTITY"]
    inspection = next(
        item for item in surface["record_types"] if item["name"] == "Inspection"
    )
    bearing = ["Inspection"]
    unattached = ["Asset"]

    assert SUBJECT_SLOT in {slot["name"] for slot in inspection["slots"]}
    assert binding["expansion"]["subject_bearing_record_types"] == bearing
    assert binding["expansion"]["entity_case_scope"] == (
        "TYPES_IN_THE_SET_THAT_CARRY_NO_SUBJECT"
    )
    assert [case["record_type"] for case in entity_cases] == unattached
    assert "Inspection" not in {case["record_type"] for case in entity_cases}
    # The surface declares entity types the question's set does not list, which
    # is the whole point of the new kind: the typed SUBJECT pairing is read off
    # the set and the SUBJECT_ANY pairing off the surface.
    assert set(types) < set(entities_on_surface)
    assert kinds == Counter(
        {
            "ENTITY": len(unattached),
            ENTITY_NO_SUBJECT: len(bearing),
            "RELATION": len(types) * len(types) * len(relations),
            "SUBJECT": len(types),
            SUBJECT_ANY: len(bearing) * len(entities_on_surface),
        }
    )
    # v4.12's kind is emitted for the bearing types and for nothing else, and
    # it is emitted directly after the ENTITY cases, so the ordinals keep the
    # two entity kinds first.
    no_subject_cases = [
        case for case in query["cases"] if case["kind"] == ENTITY_NO_SUBJECT
    ]
    assert [case["record_type"] for case in no_subject_cases] == bearing
    assert [case["ordinal"] for case in no_subject_cases] == [2]
    for case in no_subject_cases:
        assert set(case["output_fields"]) == {"record"}
        assert set(case) == {"kind", "ordinal", "output_fields", "record_type"}
        # The projection is the type's own, the same list its SUBJECT case
        # projects for the same type: the kind selects, it does not project.
        assert case["output_fields"]["record"] == (
            subject_cases[0]["output_fields"]["record"]
        )
    # v4.13's kind is emitted for the bearing types against every entity type
    # the surface declares, last, so the ordinals keep the carried kinds where
    # they were and the new cases come after the typed SUBJECT ones.
    any_cases = [case for case in query["cases"] if case["kind"] == SUBJECT_ANY]
    assert [case["record_type"] for case in any_cases] == bearing * len(
        entities_on_surface
    )
    assert [case["subject_record_type"] for case in any_cases] == entities_on_surface
    assert min(case["ordinal"] for case in any_cases) > max(
        case["ordinal"] for case in subject_cases
    )
    for case in any_cases:
        assert set(case["output_fields"]) == {"record", "subject"}
        assert set(case) == {
            "kind",
            "ordinal",
            "output_fields",
            "record_type",
            "subject_record_type",
        }
        assert SUBJECT_SLOT in case["output_fields"]["record"]
    # The typed pairs are a subset of the new ones, type for type, and where a
    # pair is in both the projection is the same: the kind selects, it does not
    # project.
    typed = {
        (case["record_type"], case["subject_record_type"]): case["output_fields"]
        for case in subject_cases
    }
    widened = {
        (case["record_type"], case["subject_record_type"]): case["output_fields"]
        for case in any_cases
    }
    assert set(typed) < set(widened)
    for pair, fields in typed.items():
        assert widened[pair] == fields, pair
    # The declared count rule, recomputed here rather than restated.
    assert len(query["cases"]) == (
        len(unattached)
        + len(bearing)
        + len(types) * len(types) * len(relations)
        + len(bearing) * len(types)
        + len(bearing) * len(entities_on_surface)
    )
    assert [
        (case["record_type"], case["subject_record_type"]) for case in subject_cases
    ] == [("Inspection", "Asset"), ("Inspection", "Inspection")]
    for case in subject_cases:
        assert SUBJECT_SLOT in case["output_fields"]["record"]
        assert set(case["output_fields"]) == {"record", "subject"}
    assert [case["ordinal"] for case in query["cases"]] == list(
        range(1, len(query["cases"]) + 1)
    )
    _module("native_query").load_binding(output.read_bytes())

    # Against run-23's binder on the same surface: the same expansion, case for
    # case and digest for digest, because this cell carries that binder. The
    # instrument is unchanged and the equality is where a silent edit would
    # show.
    run_23 = _run_23_binder()
    same_binding = run_23.build(
        surface_source=surface_path.read_bytes(),
        type_sets={"CQ-01": types},
        replay_receipt="PENDING",
        contract_source=_gate_contract(surface_path).read_bytes(),
    )
    assert same_binding["queries"][0]["cases"] == query["cases"]
    assert same_binding["cases_sha256"] == binding["cases_sha256"]
    assert same_binding["schema"] == BINDING_SCHEMA_V6 == binding["schema"]

    # And against run-22's, the cell before the fifth kind: exactly one case
    # more per bearing type and surface entity type, and every case run-22
    # emitted still emitted, in the same order and with the same types. The
    # digest moves because cases were added and for no other reason, which is
    # what the v6 schema step was for.
    run_22 = _binder_of(RUN_22, "paper_v4_run_22_binder")
    prior_binding = run_22.build(
        surface_source=surface_path.read_bytes(),
        type_sets={"CQ-01": types},
        replay_receipt="PENDING",
        contract_source=_gate_contract(surface_path).read_bytes(),
    )
    prior = prior_binding["queries"][0]["cases"]
    assert len(query["cases"]) == len(prior) + len(bearing) * len(entities_on_surface)
    assert _identities(prior) < _identities(query["cases"])
    assert _identities(query["cases"]) - _identities(prior) == {
        (SUBJECT_ANY, "Inspection", name) for name in entities_on_surface
    }
    # Case for case, ignoring the ordinals: the new cases are appended, so the
    # carried ones do not even shift.
    assert [
        case
        for case in query["cases"]
        if case["kind"] != SUBJECT_ANY
    ] == prior
    assert binding["cases_sha256"] != prior_binding["cases_sha256"]
    assert prior_binding["schema"] == BINDING_SCHEMA_V5
    assert binding["schema"] == BINDING_SCHEMA_V6

    # And against run-09's, the cell before the restriction: the same type is
    # reached, and it is reached by a case that selects on the absent slot
    # instead of by one that returns every record of the type.
    before = _run_09_binder().build(
        surface_source=surface_path.read_bytes(),
        type_sets={"CQ-01": types},
        replay_receipt="PENDING",
    )["queries"][0]["cases"]
    assert Counter(case["kind"] for case in before) == Counter(
        {
            "ENTITY": len(types),
            "RELATION": len(types) * len(types) * len(relations),
            "SUBJECT": len(types),
        }
    )
    assert ("ENTITY", "Inspection") in _identities(before)
    assert ("ENTITY", "Inspection") not in _identities(query["cases"])
    assert (ENTITY_NO_SUBJECT, "Inspection") not in _identities(before)


def test_a_type_set_listing_a_bearing_type_alone_still_returns_its_attached_records(
    private_workspace: Path,
) -> None:
    """v4.13's change on the shape that produced run-23's one NONE.

    Run-23's CQ-T4-01 listed the claim type alone. Under v4.12 the only entity
    case for a subject-bearing type returns the records whose subject slot is
    absent, and the typed SUBJECT case pairs the type with the entity types the
    set lists, so a claim whose subject is a geologic feature was returned by
    nothing: 61 subject-less claims of 124 came back and none of the 63 that
    carry a subject (E-0342, the run-23 RCA's cause 1). Here that set is written
    against the fixture: ``Inspection`` alone, with ``Asset`` nowhere in it. The
    binder emits a SUBJECT_ANY case for every entity type the surface declares,
    the attached inspection comes back through the one for ``Asset``, and
    run-23's binder on the same set emits no case that reaches it.
    """

    binder = _module("bind_from_surface")
    surface_path = _subject_gate_surface(private_workspace)
    surface = json.loads(surface_path.read_bytes())
    entities_on_surface = sorted(
        item["name"] for item in surface["record_types"] if item["family"] == "ENTITY"
    )
    ontology = private_workspace / "inspection-note-with-subject.yaml"
    alone = {"CQ-01": ["Inspection"]}

    # The set the evaluator writes when the question is about inspections: the
    # subject's type is not in it, and under v4.12 that is what lost the record.
    assert "Asset" not in alone["CQ-01"]
    assert "Asset" in entities_on_surface

    results = private_workspace / "alone-results"
    completed = _run(
        "run",
        [
            *_source_arguments(ontology),
            "--reading",
            str(FIXTURE / "reading.json"),
            "--population",
            str(_subject_population_file(private_workspace)),
            "--capture-id",
            CAPTURE_ID,
            "--plan-id",
            PLAN_ID,
            "--source-id",
            SOURCE_ID,
            "--artifact-id",
            ARTIFACT_ID,
            "--ledger",
            str(private_workspace / "alone-history.jsonl"),
            "--results",
            str(results),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )
    assert completed.returncode == 0, completed.stderr
    result = json.loads((results / "run-result.json").read_bytes())

    binding_path = private_workspace / "binding-alone.json"
    binder.main(
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(_gate_contract(surface_path)),
            "--type-sets",
            str(_type_set_file(private_workspace, alone)),
            "--replay-receipt",
            result["replay_receipt_sha256"],
            "--output",
            str(binding_path),
        ]
    )
    cases = json.loads(binding_path.read_bytes())["queries"][0]["cases"]
    kinds = Counter(case["kind"] for case in cases)

    # The new case is present, once per entity type the surface declares, and
    # the typed SUBJECT case can only pair the bearing type with itself.
    assert kinds[SUBJECT_ANY] == len(entities_on_surface)
    assert kinds["ENTITY"] == 0
    assert kinds[ENTITY_NO_SUBJECT] == 1
    assert kinds["SUBJECT"] == 1
    assert [
        case["subject_record_type"] for case in cases if case["kind"] == SUBJECT_ANY
    ] == entities_on_surface
    assert [
        case["subject_record_type"] for case in cases if case["kind"] == "SUBJECT"
    ] == ["Inspection"]
    assert any(
        case["kind"] == SUBJECT_ANY and case["subject_record_type"] == "Asset"
        for case in cases
    )

    query_results = private_workspace / "alone-query"
    completed = _run(
        "native_query",
        [
            "--ledger",
            str(private_workspace / "alone-history.jsonl"),
            "--binding",
            str(binding_path),
            "--results",
            str(query_results),
        ],
    )
    assert completed.returncode == 0, completed.stderr
    rows = json.loads((query_results / "query-result.json").read_bytes())["queries"][
        0
    ]["rows"]
    by_kind: dict[str, list[dict]] = {}
    for row in rows:
        by_kind.setdefault(row["kind"], []).append(row)

    # Both records of the bearing type come back, once each: the subject-less
    # one as an ENTITY row and the attached one as a SUBJECT row projecting the
    # asset it is about, whose type the question never named.
    assert sorted(by_kind) == ["ENTITY", "SUBJECT"]
    assert [row["witness"]["record_id"] for row in by_kind["ENTITY"]] == [
        UNATTACHED_RECORD_ID
    ]
    assert [row["witness"] for row in by_kind["SUBJECT"]] == [
        {"record_id": SUBJECT_RECORD_ID, "subject_id": SUBJECT_TARGET_ID}
    ]
    attached = by_kind["SUBJECT"][0]
    assert attached["record"][SUBJECT_SLOT] == SUBJECT_TARGET_ID
    assert attached["subject"] == {
        "name": "P-7",
        SUBJECT_TAGS_SLOT: list(SUBJECT_TARGET_TAGS),
    }
    # One row per witness still: ``Asset`` and ``Entity`` both reach it and it
    # is one row with two ordinals.
    assert len(rows) == 2
    assert attached["case_ordinals"] == sorted(
        case["ordinal"]
        for case in cases
        if case["kind"] == SUBJECT_ANY
        and case["subject_record_type"] in {"Asset", "Entity"}
    )

    # Run-23's binder on the same set returns the same cases: this cell carries
    # it, so the reachability the rest of this test drives is run-23's.
    assert _run_23_binder().build(
        surface_source=surface_path.read_bytes(),
        type_sets=alone,
        replay_receipt="PENDING",
        contract_source=_gate_contract(surface_path).read_bytes(),
    )["queries"][0]["cases"] == cases

    # Run-22's binder on the same set: no case of its four kinds returns the
    # attached record, which is exactly what CQ-T4-01 hit.
    prior_cases = _binder_of(RUN_22, "paper_v4_run_22_binder").build(
        surface_source=surface_path.read_bytes(),
        type_sets=alone,
        replay_receipt="PENDING",
        contract_source=_gate_contract(surface_path).read_bytes(),
    )["queries"][0]["cases"]
    assert SUBJECT_ANY not in {case["kind"] for case in prior_cases}
    assert [
        case["subject_record_type"]
        for case in prior_cases
        if case["kind"] == "SUBJECT"
    ] == ["Inspection"]
    prior_binding = private_workspace / "binding-alone-v412.json"
    prior_binding.write_bytes(
        _canonical(
            {
                "schema": BINDING_SCHEMA_V5,
                "queries": [
                    {"id": "NQ-CQ-01", "question_id": "CQ-01", "cases": prior_cases}
                ],
            }
        )
    )
    prior_results = private_workspace / "alone-query-v412"
    prior_executor = _binder_of(
        RUN_22, "paper_v4_run_22_native_query_alone", "native_query"
    )
    assert (
        prior_executor.main(
            [
                "--ledger",
                str(private_workspace / "alone-history.jsonl"),
                "--binding",
                str(prior_binding),
                "--results",
                str(prior_results),
            ]
        )
        == 0
    )
    prior_rows = json.loads((prior_results / "query-result.json").read_bytes())[
        "queries"
    ][0]["rows"]
    assert [row["witness"]["record_id"] for row in prior_rows] == [
        UNATTACHED_RECORD_ID
    ]
    assert SUBJECT_RECORD_ID not in {
        row["witness"]["record_id"] for row in prior_rows
    }

def test_all_five_case_kinds_execute_against_the_replayed_graph(
    private_workspace: Path,
) -> None:
    """The carried change and v4.12's, end to end, on one replayed graph.

    Run-08's binding could return the RELATION row and nothing else. Run-09
    returned both records as ENTITY rows and the subject link as a SUBJECT row,
    so the inspection came back twice. Under the v4.4 restriction the attached
    inspection arrives only through its subject and the asset still arrives as
    an ENTITY row because it bears no subject. What that restriction left
    unreachable is the second inspection, which names no subject: v4.12's fourth
    case kind returns it, once, as an ENTITY row of its own type. v4.13's fifth
    kind reaches the attached one a second way, through the surface's entity
    types rather than the set's, and the row it builds is the row the typed
    SUBJECT case builds, so the witness is one row carrying both ordinals.
    Every row is witnessed and traced and the row kinds are still three.
    """

    binder = _module("bind_from_surface")
    surface_path = _subject_gate_surface(private_workspace)
    ontology = private_workspace / "inspection-note-with-subject.yaml"
    results = private_workspace / "subject-results"
    completed = _run(
        "run",
        [
            *_source_arguments(ontology),
            "--reading",
            str(FIXTURE / "reading.json"),
            "--population",
            str(_subject_population_file(private_workspace)),
            "--capture-id",
            CAPTURE_ID,
            "--plan-id",
            PLAN_ID,
            "--source-id",
            SOURCE_ID,
            "--artifact-id",
            ARTIFACT_ID,
            "--ledger",
            str(private_workspace / "subject-history.jsonl"),
            "--results",
            str(results),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )
    assert completed.returncode == 0, completed.stderr
    result = json.loads((results / "run-result.json").read_bytes())

    binding = private_workspace / "binding-executed.json"
    binder.main(
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(_gate_contract(surface_path)),
            "--type-sets",
            str(_type_set_file(private_workspace, {"CQ-01": ["Asset", "Inspection"]})),
            "--replay-receipt",
            result["replay_receipt_sha256"],
            "--output",
            str(binding),
        ]
    )
    query_results = private_workspace / "subject-query"
    completed = _run(
        "native_query",
        [
            "--ledger",
            str(private_workspace / "subject-history.jsonl"),
            "--binding",
            str(binding),
            "--results",
            str(query_results),
        ],
    )
    assert completed.returncode == 0, completed.stderr

    query_result = json.loads((query_results / "query-result.json").read_bytes())
    summary = json.loads((query_results / "trace-summary.json").read_bytes())
    rows = query_result["queries"][0]["rows"]
    by_kind: dict[str, list[dict]] = {}
    for row in rows:
        by_kind.setdefault(row["kind"], []).append(row)

    assert query_result["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    # Five case kinds and three row kinds: the fourth writes ENTITY rows and
    # the fifth writes SUBJECT rows.
    assert sorted(by_kind) == ["ENTITY", "RELATION", "SUBJECT"]
    binding_cases = [
        case
        for query in json.loads(binding.read_bytes())["queries"]
        for case in query["cases"]
    ]
    assert sorted({case["kind"] for case in binding_cases}) == [
        "ENTITY",
        ENTITY_NO_SUBJECT,
        "RELATION",
        "SUBJECT",
        SUBJECT_ANY,
    ]
    # The asset through its own ENTITY case, ordinal 1, and the subject-less
    # inspection through the ENTITY_NO_SUBJECT case, ordinal 2. The attached
    # inspection is in neither: the v4.4 restriction still holds for it.
    assert [row["witness"]["record_id"] for row in by_kind["ENTITY"]] == [
        SUBJECT_TARGET_ID,
        UNATTACHED_RECORD_ID,
    ]
    assert SUBJECT_RECORD_ID not in {
        row["witness"]["record_id"] for row in by_kind["ENTITY"]
    }
    unattached_row = by_kind["ENTITY"][1]
    assert unattached_row["case_ordinals"] == [
        next(
            case["ordinal"]
            for case in binding_cases
            if case["kind"] == ENTITY_NO_SUBJECT
        )
    ]
    # Projected by its own type, and the absent slot is simply not there.
    assert unattached_row["record"] == {"inspected_on": UNATTACHED_INSPECTED_ON}
    assert SUBJECT_SLOT not in unattached_row["record"]
    assert len(by_kind["RELATION"]) == 1
    assert by_kind["RELATION"][0]["witness"] == {
        "relation_id": "inspection-of:P-7:2026-03-02",
        "source_id": SUBJECT_RECORD_ID,
        "target_id": SUBJECT_TARGET_ID,
    }
    assert len(by_kind["SUBJECT"]) == 1
    subject_row = by_kind["SUBJECT"][0]
    assert subject_row["witness"] == {
        "record_id": SUBJECT_RECORD_ID,
        "subject_id": SUBJECT_TARGET_ID,
    }
    assert subject_row["record"][SUBJECT_SLOT] == SUBJECT_TARGET_ID
    # The typed SUBJECT case and v4.13's SUBJECT_ANY cases all reach the
    # attached inspection through the same asset: the typed pair, the widened
    # pair, and the widened pair against ``Entity``, because the facade's typed
    # query returns a type's records and its subtypes'. That is one witness in
    # the question and so one row, carrying all three ordinals: the dedupe rule
    # v4.9 landed is what makes the widened pairing cost no row at all.
    reaching = sorted(
        case["ordinal"]
        for case in binding_cases
        if case["kind"] in {"SUBJECT", SUBJECT_ANY}
        and case["record_type"] == "Inspection"
        and case["subject_record_type"] in {"Asset", "Entity"}
    )
    assert len(reaching) == 3
    assert (
        sum(
            1
            for case in binding_cases
            if case["kind"] == "SUBJECT"
            and case["subject_record_type"] == "Asset"
        )
        == 1
    )
    assert subject_row["case_ordinals"] == reaching
    # The carried v4.7 delta, end to end: the binder called ``tags`` housekeeping and
    # named only ``name`` for the subject side, and the executor projected the
    # subject's tags beside it because the record carries them.
    assert subject_row["subject"] == {
        "name": "P-7",
        SUBJECT_TAGS_SLOT: list(SUBJECT_TARGET_TAGS),
    }
    subject_case = next(
        case
        for query in json.loads(binding.read_bytes())["queries"]
        for case in query["cases"]
        if case["kind"] == "SUBJECT"
    )
    assert subject_case["output_fields"]["subject"] == ["description", "name"]
    assert SUBJECT_TAGS_SLOT not in subject_case["output_fields"]["subject"]
    # The record side never gains the field, and the ENTITY row of the same
    # entity is what run-23 returned.
    assert SUBJECT_TAGS_SLOT not in subject_row["record"]
    assert by_kind["ENTITY"][0]["record"] == {"name": "P-7"}
    # v4.9, end to end on the fixture: the rows of a question are ordered by the
    # first case that produced them, no witness appears twice, and every key a
    # row projects is a slot the witness record's own type declares on the
    # accepted surface. The surface is the file the binder read, so this reads
    # the projection against its source rather than against the case.
    assert [row["case_ordinals"][0] for row in rows] == sorted(
        row["case_ordinals"][0] for row in rows
    )
    for row in rows:
        assert row["case_ordinals"] == sorted(row["case_ordinals"])
        assert row["case_ordinals"]
        assert "case_ordinal" not in row
    seen = [(row["kind"], _canonical(row["witness"])) for row in rows]
    assert len(seen) == len(set(seen))
    surface_slots = {
        str(record_type["name"]): {
            str(slot["name"]) for slot in record_type["slots"]
        }
        for record_type in json.loads(surface_path.read_bytes())["record_types"]
    }
    population = json.loads(
        (private_workspace / "document-population-with-subject.json").read_bytes()
    )
    own_type = {
        item["id"]: item["type"]
        for group in population["records"].values()
        for item in group
    }
    assert own_type[SUBJECT_RECORD_ID] == "Inspection"
    assert own_type[UNATTACHED_RECORD_ID] == "Inspection"
    assert own_type[SUBJECT_TARGET_ID] == "Asset"
    for row in rows:
        if row["kind"] == "ENTITY":
            sides = [(row["record"], own_type[row["witness"]["record_id"]])]
        elif row["kind"] == "SUBJECT":
            sides = [
                (row["record"], own_type[row["witness"]["record_id"]]),
                (row["subject"], own_type[row["witness"]["subject_id"]]),
            ]
        else:
            sides = [
                (row["source"], own_type[row["witness"]["source_id"]]),
                (row["target"], own_type[row["witness"]["target_id"]]),
                (row["relation"], own_type[row["witness"]["relation_id"]]),
            ]
        for projected, type_name in sides:
            assert set(projected) <= surface_slots[type_name] | {
                SUBJECT_TAGS_SLOT
            }, (row["kind"], type_name)

    # Every witness of every kind resolves to a retained input, by record id.
    traced = {item["record_id"] for item in summary["records"]}
    assert traced == {
        SUBJECT_RECORD_ID,
        SUBJECT_TARGET_ID,
        UNATTACHED_RECORD_ID,
        "inspection-of:P-7:2026-03-02",
    }
    assert summary["evidence_selection"] == "BY_RECORD_ID_NEVER_BY_POSITION"


def test_the_binding_refuses_a_case_of_an_unknown_kind_or_open_fields() -> None:
    subject = _module("native_query")
    case = {
        "kind": "ENTITY",
        "ordinal": 1,
        "record_type": "Asset",
        "output_fields": {"record": ["name"]},
    }

    def binding(mutated: dict[str, object]) -> bytes:
        return _canonical(
            {
                "schema": "malleus.paper-v4.native-query-binding/v6",
                "queries": [
                    {"id": "NQ-X", "question_id": "X", "cases": [mutated]}
                ],
            }
        )

    assert subject.load_binding(binding(dict(case)))
    for mutate, expected in (
        (lambda item: item.__setitem__("kind", "SUMMARY"), "kind is unknown"),
        (lambda item: item.__setitem__("relation_record_type", "R"), "not closed"),
        (
            lambda item: item.__setitem__("output_fields", {"source": []}),
            "output_fields must name",
        ),
    ):
        mutated = dict(case)
        mutate(mutated)
        with pytest.raises(subject.NativeQueryRefusal, match=expected):
            subject.load_binding(binding(mutated))


def test_only_the_receipt_field_moves_between_acceptance_and_query(
    private_workspace: Path,
) -> None:
    subject = _module("bind_from_surface")
    surface_path = _gate_surface(private_workspace)
    type_sets = _type_set_file(private_workspace, {"CQ-01": ["Asset", "Inspection"]})
    at_acceptance = private_workspace / "binding-acceptance.json"
    after_replay = private_workspace / "binding-query.json"
    receipt = "sha256:" + "0" * 64

    for output, value in ((at_acceptance, "PENDING"), (after_replay, receipt)):
        subject.main(
            [
                "--surface",
                str(surface_path),
                "--contract",
                str(_gate_contract(surface_path)),
                "--type-sets",
                str(type_sets),
                "--replay-receipt",
                value,
                "--output",
                str(output),
            ]
        )

    first = json.loads(at_acceptance.read_bytes())
    second = json.loads(after_replay.read_bytes())

    assert first["cases_sha256"] == second["cases_sha256"]
    assert first["queries"] == second["queries"]
    assert {
        key for key in first if first[key] != second.get(key)
    } == {"bound_after_replay_receipt_sha256"}
    assert second["bound_after_replay_receipt_sha256"] == receipt


def test_the_binding_refuses_a_type_the_surface_does_not_carry(
    private_workspace: Path,
) -> None:
    subject = _module("bind_from_surface")
    surface_path = _gate_surface(private_workspace)

    with pytest.raises(subject.BindingRefusal, match="AbsentType"):
        subject.build(
            surface_source=surface_path.read_bytes(),
            type_sets={"CQ-01": ["Asset", "AbsentType"]},
            replay_receipt="PENDING",
            contract_source=_gate_contract(surface_path).read_bytes(),
        )


def test_the_binding_frozen_at_acceptance_executes_after_the_replay(
    private_workspace: Path,
) -> None:
    """The whole point of the change: bound before rows, run after them."""

    binder = _module("bind_from_surface")
    surface_path = _gate_surface(private_workspace)
    type_sets = _type_set_file(private_workspace, {"CQ-01": ["Asset", "Inspection"]})
    at_acceptance = private_workspace / "binding-acceptance.json"
    binder.main(
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(_gate_contract(surface_path)),
            "--type-sets",
            str(type_sets),
            "--replay-receipt",
            "PENDING",
            "--output",
            str(at_acceptance),
        ]
    )
    frozen_cases = json.loads(at_acceptance.read_bytes())["cases_sha256"]

    results, result = _executed(private_workspace)
    after_replay = private_workspace / "binding-query.json"
    binder.main(
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(_gate_contract(surface_path)),
            "--type-sets",
            str(type_sets),
            "--replay-receipt",
            result["replay_receipt_sha256"],
            "--output",
            str(after_replay),
        ]
    )

    assert json.loads(after_replay.read_bytes())["cases_sha256"] == frozen_cases

    query_results = private_workspace / "query"
    completed = _run(
        "native_query",
        [
            "--ledger",
            str(private_workspace / "history.jsonl"),
            "--binding",
            str(after_replay),
            "--results",
            str(query_results),
        ],
    )
    assert completed.returncode == 0, completed.stderr

    query_result = json.loads((query_results / "query-result.json").read_bytes())
    rows = query_result["queries"][0]["rows"]

    assert query_result["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    assert query_result["inputs"]["query_binding_sha256"] == _digest(
        after_replay.read_bytes()
    )
    relation_rows = [row for row in rows if row["kind"] == "RELATION"]
    assert Counter(row["kind"] for row in rows) == Counter(
        {"ENTITY": 2, "RELATION": 1}
    )
    assert len(relation_rows) == 1
    assert relation_rows[0]["witness"] == {
        "relation_id": "inspection-of:P-7:2026-03-02",
        "source_id": "inspection:P-7:2026-03-02",
        "target_id": "asset:P-7",
    }
    assert relation_rows[0]["target"]["name"] == "P-7"


def test_usage_is_differenced_from_the_cumulative_launch_log_figures() -> None:
    subject = _module("usage_from_launch_log")

    usage = subject.derive(deepcopy(LAUNCH_LOG))

    assert usage["schema"] == "malleus.paper-v4.producer-usage/v1"
    assert usage["run"] == "run-24"
    assert usage["model_id"] == "claude-opus-5"
    assert [item["stage"] for item in usage["stages"]] == [
        "ONTOLOGY_ATTEMPT_01",
        "ONTOLOGY_ATTEMPT_02",
        "POPULATION",
    ]
    assert [item["tokens"] for item in usage["stages"]] == [185877, 17875, 167274]
    assert sum(item["tokens"] for item in usage["stages"]) == 371026
    assert usage["producer_total_tokens"] == 371026
    assert usage["review"] == {"model_id": "claude-opus-5", "tokens": 322049}
    assert "ADMITTED_AND_REPLAYED at runner attempt 1" in usage["population"]
    assert "0000000" in usage["population"]


def test_the_usage_record_refuses_a_launch_log_of_another_shape() -> None:
    subject = _module("usage_from_launch_log")

    for mutate, expected in (
        (lambda log: log.__setitem__("schema", "malleus.paper-v4.producer-launch-log/v1"), "v2"),
        (lambda log: log.pop("review"), "review"),
        (lambda log: log["runner"][0].pop("execution_commit"), "execution_commit"),
        (lambda log: log["launches"][0].pop("first_stage"), "first_stage"),
        (lambda log: log.__setitem__("drafts", []), "undeclared"),
    ):
        log = deepcopy(LAUNCH_LOG)
        mutate(log)
        with pytest.raises(subject.UsageRefusal, match=expected):
            subject.derive(log)


def test_the_usage_record_refuses_a_cumulative_figure_that_decreases() -> None:
    subject = _module("usage_from_launch_log")
    log = deepcopy(LAUNCH_LOG)
    log["launches"][0]["usage_by_resume"][0]["tokens"] = 1

    with pytest.raises(subject.UsageRefusal, match="decreases"):
        subject.derive(log)

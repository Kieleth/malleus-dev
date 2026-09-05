"""Drive the run-14 harness end to end on the neutral inspection-note fixture.

The fixture is Core's own synthetic document-capture conformance corpus. No paper
reading, ontology, capture or result enters this test, and no model runs.

v4.8 has no harness delta. Every executable file and the spawn message are
run-13's bytes: seven carry the run id and are reconstructed from run-13's text
by the substitution table below, which reverses back to run-13's bytes, and
``native_query.py`` carries no run id at all and is byte for byte run-13's file.
A ninth file, or an edit to any of the eight, fails the first group of tests
rather than travelling with the cell. The Core change under test narrows one
comparison in the adapter and is as absent from this directory as the seven
before it.

``bind_from_surface.py`` is still exercised end to end on a fixture that carries
a ``subject`` reference, because a carried delta that quietly stopped working
would otherwise be found by a row count nobody reads: the bearing type gets no
ENTITY case, its record is reached through its subject or not at all, and the
expansion is run-13's binder's, case for case. The fixture's subject entity
carries ``tags``, so v4.7's carried SUBJECT_TAGS_PROJECTED delta is exercised on
the same run as everything else.
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
RUN_13 = HERE.parent / "run-13"
PRIVATE = ROOT / "private"
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
ACTOR = "actor:paper-v4-run-14"
SPAWN_MESSAGE = HERE / "spawn-message.md"
CONTRACT_PATH = HERE / "run-contract.json"

# The one sentence STOP_RULE_CLARIFIED adds to run-04's message.
STOP_RULE_SENTENCE = (
    "Reviewing the next block is not invention; stop only when every block is"
    " REVIEWED or listed in `nothing_assertable`, or when the next addition"
    " would require invention."
)

# The eight changes Core owns. Their evidence is a commit, not a file in this
# directory, so ``pin.py`` records what landed and test_contract recomputes it;
# there is nothing here to grep for. CORE_18_NAME_AS_WORD is this cell's, and it
# is as absent from this directory as the other seven.
CORE_CHANGE_IDS = (
    "CORE_12_DERIVATION_CHECKS",
    "CORE_14_MODALITY_SOURCE_OF_TRUTH",
    "CORE_15_SUBJECT_ALIASES",
    "CORE_16_PROJECTED_SUBJECT",
    "CORE_17_PROJECTION_WITHDRAWN",
    "CORE_18_NAME_AS_WORD",
    "PACKS_0_3_0",
    "SUBJECT_ELEMENT",
)
CORE_PIN_STATUSES = {"LANDED", "PENDING_AT_PIN", "CARRIED_FROM_RUN_13"}

# The eight harness files and how each is reconstructed from run-13's. Seven
# carry the run id and are read through RUN_ID_SUBSTITUTIONS, which reverse;
# ``native_query.py`` carries none and is compared byte for byte. This table is
# the whole statement of v4.8's harness delta, which is that there is none.
RUN_ID_SUBSTITUTIONS = (
    ("run-13", "run-14"),
    ("Run-13", "Run-14"),
    ("run_13", "run_14"),
)
CARRIED_WITH_THE_RUN_ID = (
    "run.py",
    "compile_ontology_candidate.py",
    "prepare_producer.py",
    "usage_from_launch_log.py",
    "spawn-message.md",
    "bind_from_surface.py",
    "offline_validation.py",
)
CARRIED_BYTE_FOR_BYTE = ("native_query.py",)

# The thirteen changes the harness owns, each with the file that carries it
# and one string that cannot be there unless the change is. All thirteen are
# carried from run-13 and point at this cell's copy of the file. v4.8 adds none,
# so every marker below is found in bytes this cell did not write, and the
# producer sees none of them either.
DELTA_MARKERS = {
    "BINDING_FROZEN_AT_ACCEPTANCE": (
        "paper-v4/experiment-v4/run-14/bind_from_surface.py",
        '"bound_at_stage": BOUND_AT_STAGE,',
    ),
    "GATE_SURFACES_CHAINED_CAUSE": (
        "paper-v4/experiment-v4/run-14/compile_ontology_candidate.py",
        '"cause_chain": chain,',
    ),
    "INTERPRETER_PREFLIGHT": (
        "paper-v4/experiment-v4/run-14/prepare_producer.py",
        "def preflight() -> dict[str, object]:",
    ),
    "LAUNCH_LOG_V2": (
        "paper-v4/experiment-v4/run-14/usage_from_launch_log.py",
        'LOG_SCHEMA = "malleus.paper-v4.producer-launch-log/v2"',
    ),
    "PUBLIC_COST_RECORD": (
        "paper-v4/experiment-v4/run-14/usage_from_launch_log.py",
        'USAGE_SCHEMA = "malleus.paper-v4.producer-usage/v1"',
    ),
    "QUERY_CASE_KINDS_V3": (
        "paper-v4/experiment-v4/run-14/native_query.py",
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
        "paper-v4/experiment-v4/run-14/spawn-message.md",
        "Reviewing the next block is",
    ),
    "SUBJECT_TAGS_PROJECTED": (
        "paper-v4/experiment-v4/run-14/native_query.py",
        'SUBJECT_TAGS_SLOT = "tags"',
    ),
    "ENTITY_KIND_RESTRICTED": (
        "paper-v4/experiment-v4/run-14/bind_from_surface.py",
        "unattached = [name for name in types if name not in set(bearing)]",
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
SUBJECT_RECORD_ID = "inspection:P-7:2026-03-02"
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
    spec = importlib.util.spec_from_file_location(f"paper_v4_run_14_{name}", path)
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


def _run_13_binder():
    """Run-13's binder: this cell has no delta, so it is the same expansion."""
    return _binder_of(RUN_13, "paper_v4_run_13_binder")


def _run_09_binder():
    """Run-09's binder, the cell before the carried ENTITY restriction."""
    return _binder_of(RUN_09, "paper_v4_run_09_binder")


def _identity(case: dict) -> tuple[str, ...]:
    """A case's types, which is all a type-only case is."""
    if case["kind"] == "ENTITY":
        return ("ENTITY", case["record_type"])
    if case["kind"] == "RELATION":
        return (
            "RELATION",
            case["source_record_type"],
            case["relation_record_type"],
            case["target_record_type"],
        )
    return ("SUBJECT", case["record_type"], case["subject_record_type"])


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
    """This cell's copy of a run-13 file, beside run-13's with the run id moved."""
    return (
        (HERE / name).read_text(encoding="utf-8"),
        (RUN_13 / name).read_text(encoding="utf-8")
        .replace("run-13", "run-14")
        .replace("Run-13", "Run-14")
        .replace("run_13", "run_14"),
    )


@pytest.fixture()
def private_workspace() -> Iterator[Path]:
    PRIVATE.mkdir(exist_ok=True)
    path = Path(tempfile.mkdtemp(dir=PRIVATE, prefix="run-14-test-"))
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
                "schema": "malleus.paper-v4.native-query-binding/v4",
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


def _subject_population_file(directory: Path) -> Path:
    """The fixture capture and records with one record naming its subject."""

    plan = json.loads((FIXTURE / "document-plan.json").read_bytes())
    capture = json.loads((FIXTURE / "document-capture.json").read_bytes())
    capture["assertions"][0]["formalized_by"].extend(
        (
            {"path": ["properties", SUBJECT_SLOT], "record_id": SUBJECT_RECORD_ID},
            {
                "path": ["properties", SUBJECT_TAGS_SLOT],
                "record_id": SUBJECT_TARGET_ID,
            },
        )
    )
    records = deepcopy(plan["records"])
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


def test_the_eight_harness_files_are_run_13s_bytes_with_no_delta() -> None:
    """The runner, the gate, the builder, the deriver, the message, the binder,
    the offline validation and the executor.

    v4.8's harness is run-13's harness. Seven of the eight carry the run id and
    are stated here as three exact substitutions that reverse back to run-13's
    bytes; the executor carries no run id and is compared byte for byte. The
    Core change under test narrows a comparison inside the adapter, which
    changes neither how the run executes, nor which rows the query binding
    reaches, nor what the producer is told, so an edit to any of the eight fails
    this test rather than travelling with the cell.
    """

    assert set(CARRIED_WITH_THE_RUN_ID) | set(CARRIED_BYTE_FOR_BYTE) == {
        "bind_from_surface.py",
        "compile_ontology_candidate.py",
        "native_query.py",
        "offline_validation.py",
        "prepare_producer.py",
        "run.py",
        "spawn-message.md",
        "usage_from_launch_log.py",
    }
    for name in CARRIED_WITH_THE_RUN_ID:
        here, expected = _carried(name)
        assert here == expected, name
        assert "run-13" not in here, name
        assert "run_13" not in here, name
        # The table reverses: undo the substitutions and run-13's file comes
        # back, so a fourth edit cannot ride along inside the run id move.
        reversed_text = here
        for before, after in RUN_ID_SUBSTITUTIONS:
            reversed_text = reversed_text.replace(after, before)
        assert reversed_text == (RUN_13 / name).read_text(encoding="utf-8"), name
    for name in CARRIED_BYTE_FOR_BYTE:
        assert (HERE / name).read_bytes() == (RUN_13 / name).read_bytes(), name
        assert "run-13" not in (HERE / name).read_text(encoding="utf-8"), name

    runner = (HERE / "run.py").read_text(encoding="utf-8")
    # Once for the plan compiler and once for the document adapter, so Core-12's
    # evaluative-slot check stays in force; a runner that dropped the second
    # would skip EVALUATIVE_SLOT_NOT_EVALUATED in silence.
    assert runner.count("contract_view=retention.contract_view") == 2
    assert STOP_RULE_SENTENCE in _plain(SPAWN_MESSAGE.read_text(encoding="utf-8"))
    assert STOP_RULE_SENTENCE not in _plain(
        (RUN_04 / "spawn-message.md").read_text(encoding="utf-8")
    )


def test_native_query_is_run_13s_bytes_and_the_chain_back_to_run_08_holds() -> None:
    """The executor does not move, and v4.7's delta is still the only one in it.

    This cell's executor is run-13's file byte for byte, which the previous test
    also states. What this one adds is the chain: the carried
    SUBJECT_TAGS_PROJECTED delta is still exactly two edits, both present once,
    and every region run-08 already had is still run-08's, including ``_project``
    itself. A cell that quietly rewrote the executor and moved run-13's copy with
    it would pass the byte comparison and fail here.
    """

    here = (HERE / "native_query.py").read_text(encoding="utf-8")

    assert here == (RUN_13 / "native_query.py").read_text(encoding="utf-8")
    assert "run-13" not in here
    assert "run-14" not in here
    assert here.count("malleus.paper-v4.native-query-binding/v4") == 1
    # v4.7's delta, still two edits and still only in the executor.
    assert here.count('SUBJECT_TAGS_SLOT = "tags"') == 1
    assert (
        here.count(
            '                "subject": _project(\n'
            '                    subject, [*fields["subject"], SUBJECT_TAGS_SLOT]\n'
            "                ),\n"
        )
        == 1
    )
    assert '"subject": _project(subject, fields["subject"]),' not in here
    assert "SUBJECT_TAGS_SLOT" not in (
        RUN_09 / "native_query.py"
    ).read_text(encoding="utf-8")
    # The bytes every cell from run-02 to run-08 ran are still one file.
    for prior_cell in (RUN_02, RUN_03, RUN_04, RUN_05, RUN_06, RUN_07):
        assert (prior_cell / "native_query.py").read_bytes() == (
            RUN_08 / "native_query.py"
        ).read_bytes(), prior_cell.name
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
        assert _span(here, start, end) == _span(
            (RUN_08 / "native_query.py").read_text(encoding="utf-8"), start, end
        ), start

    subject = _module("native_query")
    assert subject.RESULT_SCHEMA == "malleus.paper-v4.query-result/v2"
    assert subject.BINDING_SCHEMA == "malleus.paper-v4.native-query-binding/v4"
    assert subject.SUBJECT_TAGS_SLOT == "tags"
    assert sorted(subject._ROWS_BY_KIND) == ["ENTITY", "RELATION", "SUBJECT"]
    assert sorted(subject._CASE_FIELDS) == sorted(subject._OUTPUT_FIELDS)
    assert sorted(subject._CASE_FIELDS) == list(subject.CASE_KINDS)
    # The case grammar does not move: no kind, field or output field is added.
    prior_module = _binder_of(
        RUN_13, "paper_v4_run_13_native_query", "native_query"
    )
    assert subject._CASE_FIELDS == prior_module._CASE_FIELDS
    assert subject._OUTPUT_FIELDS == prior_module._OUTPUT_FIELDS
    assert subject.CASE_KINDS == prior_module.CASE_KINDS
    assert subject.BINDING_SCHEMA == prior_module.BINDING_SCHEMA


def test_the_carried_delta_projects_tags_only_on_the_subject_side_and_only_when_present() -> None:
    """The carried delta at the row level, on rows the executor builds in isolation.

    A subject that carries ``tags`` projects them beside its binder-named
    fields; one that does not projects exactly what run-09 projected. The
    record side of the same row never gains the field, and the two other kinds
    are untouched. Run-09's executor is the comparison because it is the last
    one without the delta: run-13's carries it and this cell's is run-13's.
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

    tagged = {"id": "asset:P-7", "name": "Pump P-7", "tags": ["P-7", "P7"]}
    bare = {"id": "asset:P-8", "name": "Pump P-8"}
    records = [
        {"id": "inspection:1", "inspected_on": "2026-03-02", "subject": "asset:P-7"},
        {"id": "inspection:2", "inspected_on": "2026-03-03", "subject": "asset:P-8"},
    ]
    graph = _Graph({"Asset": [tagged, bare], "Inspection": records})
    case = {
        "kind": "SUBJECT",
        "ordinal": 1,
        "output_fields": {"record": ["inspected_on", "subject"], "subject": ["name"]},
        "record_type": "Inspection",
        "subject_record_type": "Asset",
    }

    witnesses: list[str] = []
    rows = subject._subject_rows(graph, case, witnesses)
    prior_rows = prior._subject_rows(graph, dict(case), [])

    assert [row["subject"] for row in rows] == [
        {"name": "Pump P-7", "tags": ["P-7", "P7"]},
        {"name": "Pump P-8"},
    ]
    # Run-09's executor on the same graph and the same case: the tagged subject
    # is the only difference, and it is an addition.
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

    # The other two kinds are the same function object's output either way.
    entity_case = {
        "kind": "ENTITY",
        "ordinal": 1,
        "output_fields": {"record": ["name"]},
        "record_type": "Asset",
    }
    assert subject._entity_rows(graph, entity_case, []) == prior._entity_rows(
        graph, dict(entity_case), []
    )
    assert [row["record"] for row in subject._entity_rows(graph, entity_case, [])] == [
        {"name": "Pump P-7"},
        {"name": "Pump P-8"},
    ]


def test_bind_from_surface_is_run_13s_bytes_and_keeps_the_v4_4_restriction() -> None:
    """No delta this cell, and the carried ones are still line for line in place.

    The first assertion is the whole guard: run-13's file with the run id moved
    is this one. v4.7's tags delta is in the executor, not here, so the binder's
    housekeeping set still drops ``tags`` from every projection it writes. The
    rest is the v4.4 restriction, held against run-09's pre-restriction bytes
    exactly as run-13 held it, so a carried delta that quietly came undone
    fails here rather than in a row count nobody reads.
    """

    here = (HERE / "bind_from_surface.py").read_text(encoding="utf-8")
    prior = (RUN_09 / "bind_from_surface.py").read_text(encoding="utf-8")
    carried, expected = _carried("bind_from_surface.py")

    assert carried == expected
    assert here != prior
    for start, end in (
        ("class BindingRefusal(ValueError):", "def _cases(\n"),
        ("    for source_type in types:", "    expected = (\n"),
        ("    if len(cases) != expected:", "def build(\n"),
        ("def build(", '        "cases_sha256": _digest(_canonical(queries)),\n'),
        (
            '        "population_surface_sha256": _digest(surface_source),',
            "raise SystemExit(main())\n",
        ),
        ("SURFACE_SCHEMA = ", "CASE_KINDS = (\"ENTITY\", \"RELATION\", \"SUBJECT\")\n"),
        ("HOUSEKEEPING_SLOTS = frozenset(", "BOUND_BY = ("),
    ):
        assert _span(here, start, end) == _span(prior, start, end), start

    # The carried delta, line for line.
    assert 'BINDING_SCHEMA = "malleus.paper-v4.native-query-binding/v4"' in here
    assert 'BINDING_SCHEMA = "malleus.paper-v4.native-query-binding/v3"' in prior
    assert "unattached = [name for name in types if name not in set(bearing)]" in here
    assert "unattached = " not in prior
    assert "    for record_type in unattached:\n" in here
    assert "    for record_type in types:\n" in prior
    assert "    for record_type in types:\n" not in here
    assert "        len(unattached)\n" in here
    assert "entity_case_scope" in here
    assert "entity_case_scope" not in prior
    # The SUBJECT loop is untouched: subject-bearing types are still reached.
    assert "    for record_type in bearing:\n" in here
    assert _span(here, "    for record_type in bearing:", "    expected = (\n") == _span(
        prior, "    for record_type in bearing:", "    expected = (\n"
    )

    binder = _module("bind_from_surface")
    assert binder.BINDING_SCHEMA == "malleus.paper-v4.native-query-binding/v4"
    assert binder.CASE_KINDS == ("ENTITY", "RELATION", "SUBJECT")
    assert binder.SUBJECT_SLOT == "subject"
    assert binder.BINDING_SCHEMA == _run_13_binder().BINDING_SCHEMA
    # The delta is not here: the binder still calls ``tags`` housekeeping and
    # names it in no projection it writes.
    assert "https://malleus.dev/schema/tags" in binder.HOUSEKEEPING_SLOTS
    assert binder.HOUSEKEEPING_SLOTS == _run_13_binder().HOUSEKEEPING_SLOTS
    assert "SUBJECT_TAGS_SLOT" not in here


def test_every_v4_8_change_is_present_in_the_file_that_carries_it() -> None:
    """One marker per change id, read from the contract, found in its subject.

    Thirteen of the twenty-one are the harness's and all thirteen are carried.
    Eight are Core's, and this cell's is one of those, so nothing here can
    report Core-18 landing.
    """

    changes = {
        str(item["id"]): item
        for item in json.loads(CONTRACT_PATH.read_bytes())["protocol"]["changes"]
    }

    assert set(changes) == set(DELTA_MARKERS) | set(CORE_CHANGE_IDS)
    for change_id, (relative, marker) in DELTA_MARKERS.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert marker in text, change_id
        entry = json.dumps(changes[change_id])
        assert Path(relative).name in entry, change_id
        assert changes[change_id]["detail"].strip()
        assert changes[change_id]["why"].strip()
    for change_id in CORE_CHANGE_IDS:
        assert changes[change_id]["pin_status"] in CORE_PIN_STATUSES
        assert changes[change_id]["core_task"].startswith("Core-")


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

    assert result["schema"] == "malleus.paper-v4.run-14-result/v1"
    assert result["run_id"] == "run-14"
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
                "schema": "malleus.paper-v4.native-query-binding/v4",
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
    "run": "run-14",
    "protocol": "v4.8",
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

    This surface carries no subject reference, so no type is restricted, the
    third kind expands to nothing and says so rather than being absent, and the
    expansion is v4.3's for this surface.
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

    assert binding["schema"] == "malleus.paper-v4.native-query-binding/v4"
    assert binding["bound_at_stage"] == "ONTOLOGY_ACCEPTANCE"
    assert binding["bound_after_replay_receipt_sha256"] == "PENDING"
    assert binding["population_surface_sha256"] == _digest(surface_path.read_bytes())
    assert binding["type_sets"] == {"CQ-01": types}
    assert binding["expansion"]["case_kinds"] == ["ENTITY", "RELATION", "SUBJECT"]
    assert binding["expansion"]["subject_bearing_record_types"] == []
    assert binding["expansion"]["subject_slot"] == SUBJECT_SLOT
    assert binding["expansion"]["entity_case_scope"] == (
        "TYPES_IN_THE_SET_THAT_CARRY_NO_SUBJECT"
    )
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
    """The carried v4.4 restriction, on a surface that carries a subject
    reference.

    ``Inspection`` bears ``subject`` and ``Asset`` does not, so the expansion
    emits one ENTITY case for ``Asset`` and none for ``Inspection``, and reaches
    ``Inspection`` through its SUBJECT cases instead. Run-14's delta is in the
    executor, so the expansion is run-13's binder's, case for case.
    """

    binder = _module("bind_from_surface")
    surface_path = _subject_gate_surface(private_workspace)
    surface = json.loads(surface_path.read_bytes())
    relations = sorted(
        item["name"] for item in surface["record_types"] if item["family"] == "RELATION"
    )
    types = ["Asset", "Inspection"]
    output = private_workspace / "binding-subject.json"

    binder.main(
        [
            "--surface",
            str(surface_path),
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
    assert kinds == Counter(
        {
            "ENTITY": len(unattached),
            "RELATION": len(types) * len(types) * len(relations),
            "SUBJECT": len(types),
        }
    )
    # The declared count rule, recomputed here rather than restated.
    assert len(query["cases"]) == (
        len(unattached)
        + len(types) * len(types) * len(relations)
        + len(bearing) * len(types)
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

    # Against run-13's binder on the same surface: the same cases, in the same
    # order, with the same digest. v4.8 moves the binding nowhere.
    run_13 = _run_13_binder()
    prior_binding = run_13.build(
        surface_source=surface_path.read_bytes(),
        type_sets={"CQ-01": types},
        replay_receipt="PENDING",
    )
    prior = prior_binding["queries"][0]["cases"]
    assert query["cases"] == prior
    assert _identities(query["cases"]) == _identities(prior)
    assert binding["cases_sha256"] == prior_binding["cases_sha256"]

    # And against run-09's, the cell before the restriction: one ENTITY case
    # fewer, and every RELATION and SUBJECT case identical.
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
    assert _identities(query["cases"]) < _identities(before)
    assert _identities(before) - _identities(query["cases"]) == {
        ("ENTITY", "Inspection")
    }


def test_all_three_case_kinds_execute_against_the_replayed_graph(
    private_workspace: Path,
) -> None:
    """The change, end to end: the subject-bearing record arrives once.

    Run-08's binding could return the RELATION row and nothing else. Run-09
    returned both records as ENTITY rows and the subject link as a SUBJECT row,
    so the inspection came back twice. Under the restriction the inspection
    arrives only through its subject, the asset still arrives as an ENTITY row
    because it bears no subject, and every row is witnessed and traced.
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
    assert sorted(by_kind) == ["ENTITY", "RELATION", "SUBJECT"]
    # Run-09 returned both records here. The bearing type has no ENTITY case.
    assert [row["witness"]["record_id"] for row in by_kind["ENTITY"]] == [
        SUBJECT_TARGET_ID
    ]
    assert SUBJECT_RECORD_ID not in {
        row["witness"]["record_id"] for row in by_kind["ENTITY"]
    }
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
    # entity is what run-13 returned.
    assert SUBJECT_TAGS_SLOT not in subject_row["record"]
    assert by_kind["ENTITY"][0]["record"] == {"name": "P-7"}
    assert [row["case_ordinal"] for row in rows] == sorted(
        row["case_ordinal"] for row in rows
    )
    # Every witness of every kind resolves to a retained input, by record id.
    traced = {item["record_id"] for item in summary["records"]}
    assert traced == {SUBJECT_RECORD_ID, SUBJECT_TARGET_ID, "inspection-of:P-7:2026-03-02"}
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
                "schema": "malleus.paper-v4.native-query-binding/v4",
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
    assert usage["run"] == "run-14"
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

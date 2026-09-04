"""Drive the run-02 harness end to end on the neutral inspection-note fixture.

The fixture is Core's own synthetic document-capture conformance corpus. No paper
reading, ontology, capture or result enters this test, and no model runs.
"""

from __future__ import annotations

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


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
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
ACTOR = "actor:paper-v4-run-02"
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


def _module(name: str):
    path = HERE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"paper_v4_run_02_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


@pytest.fixture()
def private_workspace() -> Iterator[Path]:
    PRIVATE.mkdir(exist_ok=True)
    path = Path(tempfile.mkdtemp(dir=PRIVATE, prefix="run-02-test-"))
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _source_arguments() -> list[str]:
    return [
        "--root",
        "inspection-note",
        "--source",
        "inspection-note",
        str(FIXTURE / "inspection-note.yaml"),
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


def _binding_file(directory: Path) -> Path:
    path = directory / "native-query-binding.json"
    path.write_bytes(
        _canonical(
            {
                "schema": "malleus.paper-v4.native-query-binding/v2",
                "status": "FROZEN_AFTER_REPLAY",
                "queries": [
                    {
                        "id": "NQ-FIXTURE-01",
                        "question_id": "FIXTURE-01",
                        "cases": [
                            {
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
        "compile_ontology_candidate.py",
        "native_query.py",
        "prepare_producer.py",
        "run.py",
        "test_contract.py",
        "test_pipeline.py",
    ]
    for name in scripts:
        text = (HERE / name).read_text(encoding="utf-8")
        for symbol in FORBIDDEN_SYMBOLS:
            assert symbol not in text, f"{name} names {symbol}"


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


def test_run_admits_replays_and_reproduces_the_same_receipt(
    private_workspace: Path,
) -> None:
    results, result = _executed(private_workspace)

    assert result["schema"] == "malleus.paper-v4.run-02-result/v1"
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
                "schema": "malleus.paper-v4.native-query-binding/v2",
                "status": "FROZEN_AFTER_REPLAY",
                "queries": [
                    {
                        "id": "NQ-FIXTURE-02",
                        "question_id": "FIXTURE-02",
                        "cases": [
                            {
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

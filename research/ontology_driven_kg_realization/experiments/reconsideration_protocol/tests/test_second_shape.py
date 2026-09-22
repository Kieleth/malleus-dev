"""The interface under a document shape, which the row shape cannot exercise.

Two adapters exist and both are private, so neither can be a test here. Four
properties of the interface are reachable only from the document shape, and
each has cost a real run something:

1. **A branching stage graph.** Two stages continue one predecessor, which is
   what a control arm is. A chain cannot show that ``predecessors`` is a graph
   rather than a list.
2. **A stage with no evidence to retain.** A control is handed the graph and the
   obligations and no new document, so it declares no source id, and its
   procedure must then carry no anchor line; a record and a procedure that
   disagree about whether there is evidence is the refusal.
3. **A packet of several files with different roles.** A row-shaped packet is
   one file; a document-shaped one is a reading, a schema closure, a skill, a
   capability declaration and a purpose note.
4. **A differential window measure.** When the two documents are two versions
   of one work, a substring test refuses every honest input and a run of a
   fixed width that only the later one carries is the leak.

The fixture below is invented, in full: two tiny readings of a made-up
document, written here. No byte of any real consumer's evidence is in this
file, which is the point of testing the shape rather than the run.
"""

from __future__ import annotations

import json

import pytest

from .. import archive, digests, exposure, freeze, launch, packets, pin, producer
from .. import windows
from ..adapter import Adapter, Layout, RuntimePin, Schemas, Stage


STAGES = (
    Stage(
        name="A",
        workspace="workspace-stage-a",
        harness="stage-a",
        export_file="stage-a-export.json",
        packet="stage-a",
        packet_target="inputs/selected-reading.json",
        packet_source_id="source:almanac-2019-preprint",
        predecessor=None,
    ),
    Stage(
        name="B",
        workspace="workspace-stage-b",
        harness="stage-b",
        export_file="stage-b-export.json",
        packet="stage-b",
        packet_target="inputs/later-reading.json",
        packet_source_id="source:almanac-2021-published",
        predecessor="A",
    ),
    # No packet, no source id, no new document. Its predecessor is A, not B.
    Stage(
        name="CONTROL",
        workspace="workspace-control",
        harness="control",
        export_file="control-export.json",
        predecessor="A",
    ),
)


def _reading(sentence):
    """One invented reading, in the shape a page-and-block reader produces."""
    return (
        json.dumps(
            {
                "pages": [
                    {
                        "page": 1,
                        "blocks": [
                            {
                                "id": "page:1:block:0",
                                "ordinal": 0,
                                "text": "The almanac opens with a note on its method"
                                " and the years it covers.",
                            },
                            {"id": "page:1:block:1", "ordinal": 1, "text": sentence},
                        ],
                    }
                ]
            },
            indent=2,
            sort_keys=True,
        ).encode()
        + b"\n"
    )


EARLIER = _reading(
    "The northern basin is described as quiet through the whole of the period."
)
LATER = _reading(
    "The northern basin is reported as active for a part of the later period."
)
PURPOSE = (
    b"# What this graph is for\nA later session will hold only this graph and"
    b" new evidence about the same material.\n"
)
SCHEMA_CLOSURE = b"classes:\n  AlmanacReading:\n    is_a: Entity\n"
SKILL = b"# The adopter's operating manual\nRead the schema before the code.\n"


def _adapter(root):
    return Adapter(
        run_id="SECOND-SHAPE",
        stages=STAGES,
        layout=Layout(
            root=root,
            producer=root / "producer",
            packets=root / "packets",
            obligations=root / "obligations",
            assessment=root / "assessment",
            manifest=root / "HARNESS-MANIFEST.json",
        ),
        schemas=Schemas(
            producer_manifest="second-shape.manifest/v0",
            receipt="second-shape.receipt/v0",
            archive="second-shape.archive/v0",
            exposure_report="second-shape.report/v0",
        ),
        pin=RuntimePin(
            core_commit="a" * 40,
            runtime=root / "runtime-aaaaaaaa",
            package=root / "package",
            markers=("runtime-aaaaaaaa/RUNTIME.md",),
        ),
    )


# --------------------------------------------------------- the stage graph


def test_two_stages_continue_one_predecessor():
    adapter = _adapter_only()
    assert adapter.names == ("A", "B", "CONTROL")
    assert adapter.predecessors == {"A": None, "B": "A", "CONTROL": "A"}
    from .. import handoff

    assert handoff.predecessor_of("B", adapter.predecessors) == "A"
    assert handoff.predecessor_of("CONTROL", adapter.predecessors) == "A"
    assert handoff.predecessor_of("A", adapter.predecessors) is None


def _adapter_only():
    from pathlib import Path

    return _adapter(Path("/nowhere"))


def test_a_stage_may_carry_no_packet_and_no_source_id():
    adapter = _adapter_only()
    assert adapter.stage("CONTROL").packet is None
    assert adapter.stage("CONTROL").packet_source_id is None
    assert adapter.stage("B").packet_source_id == "source:almanac-2021-published"


# -------------------------------------------- a packet of several files


def _packet_files():
    return {
        "stage-a": [
            ("stage-a/selected-reading.json", "DATA", EARLIER, "reading"),
            ("stage-a/closure.yaml", "TEXT", SCHEMA_CLOSURE, "the pinned export"),
            ("stage-a/SKILL.md", "TEXT", SKILL, "the tracked skill"),
            ("stage-a/PURPOSE.md", "TEXT", PURPOSE, "this test"),
        ],
        "stage-b": [("stage-b/later-reading.json", "DATA", LATER, "reading")],
        "control": [],
    }


def test_one_packet_stages_several_files_each_with_its_own_role(tmp_path):
    records = {}
    for name, entries in _packet_files().items():
        records[name] = packets.stage_files(
            tmp_path, [(relative, data) for relative, _role, data, _from in entries]
        )
    assert len(records["stage-a"]) == 4
    assert records["control"] == []
    assert (tmp_path / "stage-a/SKILL.md").read_bytes() == SKILL
    # The role and where the bytes came from are the adapter's fields and ride
    # beside the three the mechanism records.
    declaration = {
        name: {
            "files": [
                {**record, "role": role, "read_from": read_from}
                for record, (_relative, role, _data, read_from) in zip(
                    records[name], entries
                )
            ],
            "source_id": {"stage-a": "source:almanac-2019-preprint"}.get(name),
        }
        for name, entries in _packet_files().items()
    }
    assert declaration["stage-a"]["files"][2]["role"] == "TEXT"
    assert declaration["control"]["source_id"] is None
    for name in declaration:
        packets.verify_files(tmp_path, declaration[name]["files"])


def test_a_moved_packet_file_is_named_before_a_later_stage_is_built(tmp_path):
    entries = _packet_files()["stage-a"]
    records = packets.stage_files(
        tmp_path, [(relative, data) for relative, _r, data, _f in entries]
    )
    current = [(relative, data) for relative, _r, data, _f in entries]
    assert packets.would_move(tmp_path, records, current) == []
    poisoned = [
        (
            relative,
            SKILL + b"one more line\n" if relative.endswith("SKILL.md") else data,
        )
        for relative, _r, data, _f in entries
    ]
    assert packets.would_move(tmp_path, records, poisoned) == ["stage-a/SKILL.md"]


# ------------------------------------------- the differential window measure


def _measure(where, role, data, stage):
    """A leak is a run only the later reading carries. Stage B's DATA is it."""
    if role == "DATA" and stage == "B":
        return
    later_only = windows.windows_only_in(LATER.decode(), EARLIER.decode(), width=40)
    normalised = windows.plain(data.decode("utf-8", errors="replace"))
    for start, piece in windows.runs(normalised, width=40):
        if piece in later_only:
            raise exposure.ExposureRefusal(
                f"{where}: a 40-character run of the later document at normalised"
                f" offset {start}, which the earlier document does not carry:"
                f" {piece!r}"
            )


def test_the_two_readings_share_most_of_their_runs_and_differ_in_some():
    shared = windows.shared_windows(EARLIER.decode(), LATER.decode(), width=40)
    only = windows.windows_only_in(LATER.decode(), EARLIER.decode(), width=40)
    assert shared, "a substring test would refuse every honest input"
    assert only, "the two readings would be indistinguishable"


def test_the_earlier_reading_passes_and_the_later_one_does_not(tmp_path):
    workspace = tmp_path / "workspace-stage-a"
    (workspace / "inputs").mkdir(parents=True)
    (workspace / "inputs/selected-reading.json").write_bytes(EARLIER)
    declared = {"inputs/selected-reading.json": "DATA"}
    report = exposure.check(
        workspace,
        declared,
        "A",
        stages=("A", "B", "CONTROL"),
        frozen_digests={digests.digest(EARLIER)},
        measure=_measure,
        report_schema="second-shape.report/v0",
        report_extras={"window": 40},
    )
    assert report["status"] == "CLEAN" and report["window"] == 40

    (workspace / "inputs/selected-reading.json").write_bytes(LATER)
    with pytest.raises(exposure.ExposureRefusal, match="40-character run"):
        exposure.check(
            workspace,
            declared,
            "A",
            stages=("A", "B", "CONTROL"),
            frozen_digests={digests.digest(LATER)},
            measure=_measure,
            report_schema="second-shape.report/v0",
        )


def test_stage_b_may_carry_the_later_document_because_it_is_its_evidence(tmp_path):
    workspace = tmp_path / "workspace-stage-b"
    (workspace / "inputs").mkdir(parents=True)
    (workspace / "inputs/later-reading.json").write_bytes(LATER)
    report = exposure.check(
        workspace,
        {"inputs/later-reading.json": "DATA"},
        "B",
        stages=("A", "B", "CONTROL"),
        frozen_digests={digests.digest(LATER)},
        measure=_measure,
        report_schema="second-shape.report/v0",
    )
    assert report["status"] == "CLEAN"


def test_the_control_may_not_carry_it(tmp_path):
    workspace = tmp_path / "workspace-control"
    (workspace / "inputs").mkdir(parents=True)
    (workspace / "inputs/later-reading.json").write_bytes(LATER)
    with pytest.raises(exposure.ExposureRefusal, match="40-character run"):
        exposure.check(
            workspace,
            {"inputs/later-reading.json": "DATA"},
            "CONTROL",
            stages=("A", "B", "CONTROL"),
            frozen_digests={digests.digest(LATER)},
            measure=_measure,
            report_schema="second-shape.report/v0",
        )


# ------------------------------- a stage with no evidence, end to end


def _build(root, stage, files, status="FROZEN"):
    adapter = _adapter(root)
    declaration = adapter.stage(stage)
    workspace = adapter.workspace_of(stage)
    harness = adapter.harness_of(stage)
    producer.write_workspace(workspace, files)
    (workspace / "work").mkdir(parents=True, exist_ok=True)
    procedure = producer.procedure_for(
        stage,
        (workspace / "PROCEDURE.md").read_bytes().decode(),
        {},
    )
    message = b"own <PRODUCER_WORKSPACE>/work/ and nothing else.\n"
    report = exposure.check(
        workspace,
        {relative: role for relative, (role, _) in files.items()},
        stage,
        stages=adapter.names,
        frozen_digests={digests.digest(data) for _role, data in files.values()},
        measure=_measure,
        report_schema=adapter.schemas.exposure_report,
        extra={"spawn-message.md": ("TEXT", message)},
    )
    manifest, _ = producer.build(
        stage,
        run_id=adapter.run_id,
        schema=adapter.schemas.producer_manifest,
        harness=harness,
        harness_name=declaration.harness,
        workspace=workspace,
        root=root,
        report=report,
        status=status,
        packet_target=declaration.packet_target,
        packet_source_id=declaration.packet_source_id,
        message=message,
        procedure=procedure,
        extras={
            "producer": {
                "model_id": "m",
                "model_family": "f",
                "requested_model": "r",
                "reasoning_effort": "e",
            }
        },
    )
    return adapter, manifest, workspace, harness


CONTROL_PROCEDURE = (
    b"# Review procedure\nYou receive the graph you exported and the"
    b" obligations over it. There is no new document and nothing to anchor.\n"
)
STAGE_A_PROCEDURE = (
    b"# Population procedure\nRun:\n\n    runner.py anchor --history"
    b" work/history.jsonl --packet inputs/selected-reading.json --source-id"
    b" source:almanac-2019-preprint\n"
)


def test_a_stage_with_no_source_id_and_no_anchor_line_launches(tmp_path):
    files = {
        "PROCEDURE.md": ("TEXT", CONTROL_PROCEDURE),
        "inputs/stage-a-export.json": ("PRODUCER_OWN", b'{"entities":[]}\n'),
    }
    adapter, manifest, workspace, harness = _build(tmp_path, "CONTROL", files)
    assert manifest["status"] == "FROZEN"
    assert launch.declared_source_id(manifest) is None
    (harness / "spawn-message.md").write_bytes(
        b"own <PRODUCER_WORKSPACE>/work/ and nothing else.\n"
    )
    rows, declared = launch.checked_inputs(manifest, workspace, harness)
    launch.refuse_undeclared_files(workspace, declared, work_dir="work")
    launch.refuse_procedure_disagreement(
        CONTROL_PROCEDURE.decode(), None, refuse_extra=True
    )
    assert len(rows) == 3
    assert launch.dispatch_of(harness, workspace).endswith("/work/ and nothing else.\n")


def test_a_control_whose_procedure_carries_an_anchor_line_refuses(tmp_path):
    files = {
        "PROCEDURE.md": ("TEXT", STAGE_A_PROCEDURE),
        "inputs/stage-a-export.json": ("PRODUCER_OWN", b'{"entities":[]}\n'),
    }
    _adapter_, manifest, _workspace, _harness = _build(tmp_path, "CONTROL", files)
    assert launch.declared_source_id(manifest) is None
    with pytest.raises(launch.LaunchRefusal, match="declares no source id"):
        launch.refuse_procedure_disagreement(
            STAGE_A_PROCEDURE.decode(), None, refuse_extra=True
        )


def test_a_stage_with_a_source_id_must_carry_its_anchor_line(tmp_path):
    files = {
        "PROCEDURE.md": ("TEXT", STAGE_A_PROCEDURE),
        "inputs/selected-reading.json": ("DATA", EARLIER),
    }
    _adapter_, manifest, _workspace, _harness = _build(tmp_path, "A", files)
    found = launch.declared_source_id(manifest)
    assert found == "source:almanac-2019-preprint"
    launch.refuse_procedure_disagreement(STAGE_A_PROCEDURE.decode(), found)
    with pytest.raises(launch.LaunchRefusal, match="source-id"):
        launch.refuse_procedure_disagreement(CONTROL_PROCEDURE.decode(), found)


def test_the_packet_record_carries_the_source_id_and_the_control_none(tmp_path):
    files = {
        "PROCEDURE.md": ("TEXT", STAGE_A_PROCEDURE),
        "inputs/selected-reading.json": ("DATA", EARLIER),
    }
    _adapter_, manifest, _w, _h = _build(tmp_path, "A", files)
    carrying = [item for item in manifest["declared_inputs"] if item.get("source_id")]
    assert [item["path"] for item in carrying] == ["inputs/selected-reading.json"]


# ------------------------------------------- the guard and the archive


def test_the_guard_and_the_archive_work_over_a_branching_graph(tmp_path):
    files = {
        "PROCEDURE.md": ("TEXT", STAGE_A_PROCEDURE),
        "inputs/selected-reading.json": ("DATA", EARLIER),
    }
    adapter, manifest, workspace, harness = _build(tmp_path, "A", files)
    harnesses = {stage.name: stage.harness for stage in STAGES}
    assert (
        freeze.launch_records(tmp_path, stages=adapter.names, harnesses=harnesses) == []
    )
    stamped = json.loads((harness / "producer-input-manifest.json").read_bytes())
    stamped["launch"] = {"launched": True, "launched_at": "2026-09-21T00:00:00Z"}
    (harness / "producer-input-manifest.json").write_bytes(digests.indented(stamped))
    assert freeze.launch_records(
        tmp_path, stages=adapter.names, harnesses=harnesses
    ) == ["A"]
    with pytest.raises(freeze.FreezeRefusal, match="LAUNCH_RECORDED"):
        freeze.refuse_if_launched(adapter.names, ["A"])
    # Rebuilding the two stages that branch off A is exactly what stays legal.
    freeze.refuse_if_launched(("B", "CONTROL"), ["A"])

    (workspace / "work/stage-a-export.json").write_bytes(b'{"entities":[]}\n')
    result = archive.archive("A", adapter=adapter, root=tmp_path)
    assert result["files"] == 1
    from .. import handoff

    found = handoff.archived_export("A", adapter=adapter, root=tmp_path)
    assert found.name == "stage-a-export.json"
    with pytest.raises(handoff.HandoffRefusal, match="not launched"):
        handoff.archived_export("B", adapter=adapter, root=tmp_path)


def test_the_package_pin_is_the_same_mechanism_for_both_shapes():
    from .. import census

    first = pin.package_pin(census.PACKAGE)
    second = pin.package_pin(census.PACKAGE)
    assert first == second
    assert first["sha256"].startswith("sha256:")

"""The generic mechanisms, each against the smallest thing that shows it holds."""

from __future__ import annotations

import json

import pytest

from .. import archive, assessment, digests, exposure, freeze, launch, packets, pin
from .. import obligations, producer, windows
from ..adapter import Adapter, Layout, RuntimePin, Schemas, Stage


# ------------------------------------------------------------------ digests


def test_canonical_bytes_are_sorted_and_tight():
    assert digests.canonical({"b": 1, "a": [2, 3]}) == b'{"a":[2,3],"b":1}'


def test_a_digest_is_over_the_exact_bytes():
    assert digests.digest(b"") == (
        "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )


def test_artifact_digests_are_keyed_relative_to_the_root(tmp_path):
    (tmp_path / "one").mkdir()
    (tmp_path / "one/a.txt").write_bytes(b"a")
    (tmp_path / "one/nested").mkdir()
    (tmp_path / "one/nested/b.txt").write_bytes(b"b")
    found = digests.artifact_digests(tmp_path, (tmp_path / "one",))
    assert sorted(found) == ["one/a.txt", "one/nested/b.txt"]
    assert found["one/a.txt"] == digests.digest(b"a")


# ------------------------------------------------------------------ packets


def test_staging_writes_the_bytes_and_records_three_things(tmp_path):
    records = packets.stage_files(
        tmp_path, [("a/one.jsonl", b'{"x":1}\n'), ("b/two.txt", b"two")]
    )
    assert (tmp_path / "a/one.jsonl").read_bytes() == b'{"x":1}\n'
    assert records[0] == {
        "path": "a/one.jsonl",
        "sha256": digests.digest(b'{"x":1}\n'),
        "bytes": 8,
    }


def test_verify_refuses_an_absent_a_moved_and_a_resized_file(tmp_path):
    records = packets.stage_files(tmp_path, [("one.txt", b"one")])
    packets.verify_files(tmp_path, records)
    (tmp_path / "one.txt").write_bytes(b"two")
    with pytest.raises(packets.PacketRefusal, match="is not the frozen"):
        packets.verify_files(tmp_path, records)
    (tmp_path / "one.txt").unlink()
    with pytest.raises(packets.PacketRefusal, match="declared and not present"):
        packets.verify_files(tmp_path, records)


def test_would_move_names_what_a_second_freeze_would_change(tmp_path):
    records = packets.stage_files(tmp_path, [("one.txt", b"one")])
    assert packets.would_move(tmp_path, records, [("one.txt", b"one")]) == []
    assert packets.would_move(tmp_path, records, [("one.txt", b"other")]) == ["one.txt"]


# -------------------------------------------------------------- obligations


def _obligation(identifier, subject):
    return {
        "id": identifier,
        "subject": subject,
        "permitted_outcomes": ["CORRECTION", "NO_CHANGE", "CONFLICT", "UNRESOLVED"],
    }


def _declaration(items):
    return {"boundary_id": "reading:fixture", "obligations": items}


def test_the_freeze_record_holds_the_body_and_every_obligation():
    items = [_obligation("obligation:one", {"pick": ["a"]})]
    body = digests.indented(_declaration(items))
    record = obligations.freeze_record(
        body, items, schema="fixture.freeze/v0", path="obligations.json"
    )
    assert obligations.load_frozen(body, record, per_obligation=True)["obligations"]
    with pytest.raises(obligations.BindingRefusal, match="not the bytes they declare"):
        obligations.load_frozen(body + b"\n", record)


def test_a_single_edited_obligation_is_caught_only_per_obligation():
    items = [_obligation("obligation:one", {"pick": ["a"]})]
    body = digests.indented(_declaration(items))
    record = obligations.freeze_record(
        body, items, schema="fixture.freeze/v0", path="obligations.json"
    )
    moved = [_obligation("obligation:one", {"pick": ["b"]})]
    rebuilt = digests.indented(_declaration(moved))
    record["sha256"] = digests.digest(rebuilt)
    obligations.load_frozen(rebuilt, record)
    with pytest.raises(obligations.BindingRefusal, match="not the bytes it declares"):
        obligations.load_frozen(rebuilt, record, per_obligation=True)


EMPTY_EXPORT = {group: [] for group in obligations.EXPORT_GROUPS}


def test_an_export_of_the_wrong_shape_refuses():
    with pytest.raises(obligations.BindingRefusal, match="not a graph export"):
        obligations.check_export({"entities": []})
    with pytest.raises(obligations.BindingRefusal, match="not a list"):
        obligations.check_export({**EMPTY_EXPORT, "entities": {}})


def test_a_withheld_record_id_in_the_export_refuses():
    export = {**EMPTY_EXPORT, "entities": [{"id": "withheld:one", "properties": {}}]}
    with pytest.raises(obligations.BindingRefusal, match="withheld:one"):
        obligations.check_export(
            export, forbidden_record_ids=("withheld:one",), noun="the answer"
        )


def test_an_obligation_that_binds_nothing_is_still_an_interpretation():
    items = [_obligation("obligation:empty", {"pick": []})]
    body = digests.indented(_declaration(items))
    record = obligations.freeze_record(
        body, items, schema="fixture.freeze/v0", path="o.json"
    )
    bound = obligations.bind(
        EMPTY_EXPORT,
        {"id": "knowledge:fixture", "sha256": digests.digest(b"k")},
        declared=obligations.load_frozen(body, record),
        select=lambda subject: [],
        evidence=[digests.reference("evidence:fixture", b"e")],
        ontology=digests.reference("ontology:fixture", b"o"),
        bound_schema="fixture.bound/v0",
        carry_identity=False,
    )
    assert bound["bindings"][0]["matched"] == 0
    assert bound["bindings"][0]["must_review"] is True
    assert len(bound["boundary"]["interpretations"]) == 1


def test_the_identity_sits_beside_the_boundary_and_not_inside_it():
    items = [_obligation("obligation:one", {"pick": []})]
    body = digests.indented(_declaration(items))
    record = obligations.freeze_record(
        body, items, schema="fixture.freeze/v0", path="o.json"
    )
    arguments = dict(
        declared=obligations.load_frozen(body, record),
        select=lambda subject: [],
        evidence=[digests.reference("evidence:fixture", b"e")],
        ontology=digests.reference("ontology:fixture", b"o"),
        bound_schema="fixture.bound/v0",
    )
    knowledge = {"id": "knowledge:fixture", "sha256": digests.digest(b"k")}
    without = obligations.bind(
        EMPTY_EXPORT, knowledge, carry_identity=False, **arguments
    )
    with_it = obligations.bind(EMPTY_EXPORT, knowledge, **arguments)
    assert with_it["boundary"] == without["boundary"]
    assert "boundary_identity" not in with_it["boundary"]
    assert with_it["boundary_identity"].startswith("sha256:")


def test_binding_extras_carry_the_question_beside_the_ids():
    items = [{**_obligation("obligation:one", {"pick": []}), "asks": "what changed"}]
    body = digests.indented(_declaration(items))
    record = obligations.freeze_record(
        body, items, schema="fixture.freeze/v0", path="o.json"
    )
    bound = obligations.bind(
        EMPTY_EXPORT,
        {"id": "knowledge:fixture", "sha256": digests.digest(b"k")},
        declared=obligations.load_frozen(body, record),
        select=lambda subject: [],
        evidence=[digests.reference("evidence:fixture", b"e")],
        ontology=digests.reference("ontology:fixture", b"o"),
        bound_schema="fixture.bound/v0",
        binding_extras=("asks",),
        carry_identity=False,
    )
    assert bound["bindings"][0]["asks"] == "what changed"


# ----------------------------------------------------------------- exposure


def _clean(where, role, data, stage):
    return None


def test_the_closure_check_runs_both_ways(tmp_path):
    (tmp_path / "one.txt").write_bytes(b"one")
    with pytest.raises(exposure.ExposureRefusal, match="not declared"):
        exposure.check(
            tmp_path,
            {},
            "A",
            stages=("A",),
            frozen_digests=set(),
            measure=_clean,
            report_schema="fixture.report/v0",
        )
    with pytest.raises(exposure.ExposureRefusal, match="absent.txt"):
        exposure.check(
            tmp_path,
            {"one.txt": "TEXT", "absent.txt": "TEXT"},
            "A",
            stages=("A",),
            frozen_digests=set(),
            measure=_clean,
            report_schema="fixture.report/v0",
        )


def test_data_must_be_a_frozen_packet(tmp_path):
    (tmp_path / "one.jsonl").write_bytes(b"one")
    with pytest.raises(exposure.ExposureRefusal, match="frozen packet"):
        exposure.check(
            tmp_path,
            {"one.jsonl": "DATA"},
            "A",
            stages=("A",),
            frozen_digests={digests.digest(b"other")},
            measure=_clean,
            report_schema="fixture.report/v0",
        )
    report = exposure.check(
        tmp_path,
        {"one.jsonl": "DATA"},
        "A",
        stages=("A",),
        frozen_digests={digests.digest(b"one")},
        measure=_clean,
        report_schema="fixture.report/v0",
    )
    assert report["status"] == "CLEAN"
    assert report["total_bytes"] == 3


def test_the_measure_sees_every_file_and_every_extra(tmp_path):
    (tmp_path / "one.txt").write_bytes(b"one")
    seen = []

    def measure(where, role, data, stage):
        seen.append((where, role, stage))

    report = exposure.check(
        tmp_path,
        {"one.txt": "TEXT"},
        "B",
        stages=("A", "B"),
        frozen_digests=set(),
        measure=measure,
        report_schema="fixture.report/v0",
        extra={"spawn-message.md": ("TEXT", b"spawn")},
    )
    assert seen == [("one.txt", "TEXT", "B"), ("spawn-message.md", "TEXT", "B")]
    assert [item["in_workspace"] for item in report["files"]] == [True, False]


def test_an_undeclared_role_refuses_in_the_workspace_and_in_the_extra(tmp_path):
    (tmp_path / "one.txt").write_bytes(b"one")
    with pytest.raises(exposure.ExposureRefusal, match="undeclared role: WRONG"):
        exposure.check(
            tmp_path,
            {"one.txt": "WRONG"},
            "A",
            stages=("A",),
            frozen_digests=set(),
            measure=_clean,
            report_schema="fixture.report/v0",
        )


def test_an_unknown_stage_refuses_before_anything_is_read(tmp_path):
    with pytest.raises(exposure.ExposureRefusal, match="unknown stage"):
        exposure.check(
            tmp_path,
            {},
            "Z",
            stages=("A",),
            frozen_digests=set(),
            measure=_clean,
            report_schema="fixture.report/v0",
        )


def test_the_report_carries_the_adapters_own_extras(tmp_path):
    report = exposure.check(
        tmp_path,
        {},
        "A",
        stages=("A",),
        frozen_digests=set(),
        measure=_clean,
        report_schema="fixture.report/v0",
        report_extras={"window": 60, "checked": ["ONE"]},
    )
    assert report["window"] == 60 and report["checked"] == ["ONE"]
    assert list(report)[-1] == "status"


# ------------------------------------------------------------------ windows


def test_a_shared_run_is_not_a_leak_and_a_later_only_run_is():
    earlier = "The valley narrows here. A second sentence follows it closely."
    later = "The valley narrows here. A different sentence follows it closely."
    only = windows.windows_only_in(later, earlier, width=20)
    assert only
    assert all(
        piece not in windows.windows(windows.plain(earlier), 20) for piece in only
    )
    assert windows.shared_windows(earlier, later, width=20)


def test_normalisation_collapses_whitespace_and_nothing_else():
    assert windows.plain("  a\n b\tc  ") == "a b c"


def test_a_run_straddling_a_block_join_is_found_over_the_joined_text():
    blocks = ["first half of one sentence", "and the second half of it"]
    joined = windows.plain(" ".join(blocks))
    straddling = joined[20:50]
    assert len(straddling) == 30
    assert straddling in windows.windows(joined, 30)
    per_block = set()
    for block in blocks:
        per_block |= windows.windows(windows.plain(block), 30)
    assert straddling not in per_block


# --------------------------------------------------------------- assessment


def _record(status="DRAFT", ratification=None):
    return {
        "schema": "fixture.record/v0",
        "status": status,
        "inputs": {},
        "counts": {"kept": 1, "changed": 0},
        "obligations": [
            {
                "obligation_id": "obligation:one",
                "assessed_as": "kept",
                "producer_outcome": "NO_CHANGE",
                "rationale": "it still stands",
                "source_locators": ["row:0:a"],
            }
        ],
        "ratification": ratification or {"status": "PENDING"},
    }


TALLY = dict(
    obligation_keys=(
        "obligation_id",
        "assessed_as",
        "producer_outcome",
        "rationale",
        "source_locators",
    ),
    assessment_outcomes=("kept", "changed"),
    producer_outcomes=("NO_CHANGE", "CORRECTION"),
    outcome_counts=("kept", "changed"),
)


def test_the_tally_counts_the_judgements():
    counts, seen = assessment.tally(_record(), **TALLY)
    assert counts == {"kept": 1, "changed": 0}
    assert seen == {"obligation:one"}


def test_counts_that_do_not_tally_refuse():
    record = _record()
    record["counts"] = {"kept": 2, "changed": 0}
    with pytest.raises(assessment.AssessmentRefusal, match="tally"):
        assessment.tally(record, **TALLY)


def test_one_obligation_judged_twice_refuses():
    record = _record()
    record["obligations"] = record["obligations"] * 2
    record["counts"] = {"kept": 2, "changed": 0}
    with pytest.raises(assessment.AssessmentRefusal, match="judged twice"):
        assessment.tally(record, **TALLY)


def test_a_blank_rationale_and_an_empty_locator_list_refuse():
    record = _record()
    record["obligations"][0]["rationale"] = "  "
    with pytest.raises(assessment.AssessmentRefusal, match="blank rationale"):
        assessment.tally(record, **TALLY)
    record = _record()
    record["obligations"][0]["source_locators"] = []
    with pytest.raises(assessment.AssessmentRefusal, match="source_locators"):
        assessment.tally(record, **TALLY)


def test_a_forbidden_field_refuses():
    record = _record()
    record["obligations"][0]["score"] = 1
    with pytest.raises(assessment.AssessmentRefusal, match="score"):
        assessment.tally(record, forbidden_fields=("score",), **TALLY)


def test_an_unratified_record_must_say_pending():
    assert assessment.check_ratification(_record(), ratifier="actor:human") == "PENDING"
    record = _record(ratification={"status": "RATIFIED"})
    with pytest.raises(assessment.AssessmentRefusal, match="PENDING"):
        assessment.check_ratification(record, ratifier="actor:human")


def test_ratifying_cannot_alter_a_judgement():
    record = _record(status="HUMAN_RATIFIED")
    naked = {key: value for key, value in record.items() if key != "ratification"}
    block = {
        "status": "RATIFIED",
        "actor_id": "actor:human",
        "at": "2026-09-21T00:00:00Z",
        "binding_file": "protocol.json",
        "binding_file_sha256": digests.digest(b"p"),
        "record_sha256": digests.digest(digests.canonical(naked)),
        "scope": "one record",
    }
    record["ratification"] = block
    assert assessment.check_ratification(record, ratifier="actor:human") == "RATIFIED"
    record["obligations"][0]["rationale"] = "changed after ratifying"
    with pytest.raises(assessment.AssessmentRefusal, match="record_sha256"):
        assessment.check_ratification(record, ratifier="actor:human")


def test_another_actor_cannot_ratify():
    record = _record(status="HUMAN_RATIFIED")
    naked = {key: value for key, value in record.items() if key != "ratification"}
    record["ratification"] = {
        "status": "RATIFIED",
        "actor_id": "actor:someone-else",
        "at": "2026-09-21T00:00:00Z",
        "binding_file": "protocol.json",
        "binding_file_sha256": digests.digest(b"p"),
        "record_sha256": digests.digest(digests.canonical(naked)),
        "scope": "one record",
    }
    with pytest.raises(assessment.AssessmentRefusal, match="ratifier"):
        assessment.check_ratification(record, ratifier="actor:human")


def test_containment_catches_a_rename_and_an_embedding(tmp_path):
    forbidden = {"answers.json": b'{"answer": 1}'}
    assessment.contained(tmp_path, forbidden)
    (tmp_path / "answers.json").write_bytes(b"anything")
    with pytest.raises(assessment.AssessmentRefusal, match="answers.json"):
        assessment.contained(tmp_path, forbidden)
    (tmp_path / "answers.json").unlink()
    (tmp_path / "renamed.json").write_bytes(b'{"answer": 1}')
    with pytest.raises(assessment.AssessmentRefusal, match="renamed"):
        assessment.contained(tmp_path, forbidden)
    (tmp_path / "renamed.json").unlink()
    (tmp_path / "notes.md").write_bytes(b'before {"answer": 1} after')
    with pytest.raises(assessment.AssessmentRefusal, match="embeds"):
        assessment.contained(tmp_path, forbidden)


# -------------------------------------------------------------------- pin


def test_the_package_pin_is_over_its_own_modules():
    from .. import census

    found = pin.package_pin(census.PACKAGE)
    assert found["module_count"] == len(list(census.PACKAGE.glob("*.py")))
    assert found["sha256"] == digests.digest(digests.canonical(found["modules"]))
    assert "census.py" in found["modules"]
    pin.verify_package(census.PACKAGE, found)


def test_a_moved_module_fails_verification(tmp_path):
    from .. import census
    import shutil as _shutil

    copy = tmp_path / "reconsideration_protocol"
    _shutil.copytree(census.PACKAGE, copy)
    recorded = pin.package_pin(copy)
    (copy / "digests.py").write_bytes((copy / "digests.py").read_bytes() + b"\n")
    with pytest.raises(pin.PinRefusal, match="not the recorded"):
        pin.verify_package(copy, recorded)


def test_a_directory_with_no_module_cannot_be_pinned(tmp_path):
    (tmp_path / "empty").mkdir()
    with pytest.raises(pin.PinRefusal, match="nothing to pin"):
        pin.package_pin(tmp_path / "empty")


# ------------------------------------------------------------------- freeze


def _tree(root, stages, launched=()):
    for stage in stages:
        harness = root / "producer" / f"stage-{stage.lower()}"
        harness.mkdir(parents=True)
        (harness / "producer-input-manifest.json").write_bytes(
            digests.indented(
                {
                    "launch": {
                        "launched": stage in launched,
                        "launched_at": "2026-09-21T00:00:00Z"
                        if stage in launched
                        else None,
                    }
                }
            )
        )
    return {stage: f"stage-{stage.lower()}" for stage in stages}


def test_the_guard_reads_each_stages_own_manifest(tmp_path):
    harnesses = _tree(tmp_path, ("A", "B"), launched=("A",))
    assert freeze.launch_records(tmp_path, stages=("A", "B"), harnesses=harnesses) == [
        "A"
    ]


def test_the_guard_reads_the_index_copy_too(tmp_path):
    harnesses = _tree(tmp_path, ("A", "B"))
    (tmp_path / "INDEX.json").write_bytes(
        digests.indented({"producer": {"B": {"launched": True}}})
    )
    assert freeze.launch_records(
        tmp_path, stages=("A", "B"), harnesses=harnesses, manifest_name="INDEX.json"
    ) == ["B"]


def test_a_rebuild_of_a_launched_stage_refuses_and_names_it():
    with pytest.raises(freeze.FreezeRefusal, match="LAUNCH_RECORDED"):
        freeze.refuse_if_launched(("A", "B"), ["A"])
    freeze.refuse_if_launched(("B",), ["A"])


def test_the_refusal_report_is_typed():
    try:
        freeze.refuse_if_launched(("A",), ["A"])
    except freeze.FreezeRefusal as refusal:
        report = freeze.refusal_report(refusal, recorded=["A"], requested=("A",))
    assert report["reason"] == "LAUNCH_RECORDED"
    assert report["stages"] == ["A"] and report["rebuild_requested"] == ["A"]


# ----------------------------------------------------------------- producer


def test_a_procedure_with_an_unfilled_token_refuses():
    with pytest.raises(ValueError, match="__EXPORT__"):
        producer.procedure_for("A", "write __EXPORT__", {"__PACKET__": "p"})
    assert (
        producer.procedure_for("A", "write __EXPORT__", {"__EXPORT__": "a.json"})
        == "write a.json"
    )


def test_a_placeholder_says_so_in_its_own_bytes():
    data = producer.placeholder("the export", filled_after="STAGE_A")
    assert json.loads(data) == {
        "PLACEHOLDER": True,
        "filled_after": "STAGE_A",
        "fill_with": "the export",
    }


def test_a_rebuild_carries_a_recorded_launch_forward(tmp_path):
    harness = tmp_path / "stage-a"
    harness.mkdir()
    fresh = producer.launch_seed(harness, "producer/stage-a/spawn-message.md")
    assert fresh["launched"] is False
    (harness / "producer-input-manifest.json").write_bytes(
        digests.indented(
            {"launch": {"launched": True, "launched_at": "2026-09-21T00:00:00Z"}}
        )
    )
    carried = producer.launch_seed(harness, "producer/stage-a/spawn-message.md")
    assert carried == {"launched": True, "launched_at": "2026-09-21T00:00:00Z"}


def test_the_packet_record_is_the_one_that_carries_the_source_id():
    report = {
        "files": [
            {
                "path": "inputs/evidence.jsonl",
                "role": "DATA",
                "bytes": 3,
                "sha256": digests.digest(b"one"),
                "in_workspace": True,
            },
            {
                "path": "PROCEDURE.md",
                "role": "TEXT",
                "bytes": 3,
                "sha256": digests.digest(b"two"),
                "in_workspace": True,
            },
        ]
    }
    rows = producer.declared_inputs(
        report,
        packet_target="inputs/evidence.jsonl",
        packet_source_id="source:fixture",
    )
    assert [item.get("source_id") for item in rows] == ["source:fixture", None]


def test_a_stage_with_no_source_id_declares_none():
    report = {
        "files": [
            {
                "path": "PROCEDURE.md",
                "role": "TEXT",
                "bytes": 3,
                "sha256": digests.digest(b"two"),
                "in_workspace": True,
            }
        ]
    }
    rows = producer.declared_inputs(report, packet_target=None, packet_source_id=None)
    assert "source_id" not in rows[0]


# ------------------------------------------------------------------- launch


def _adapter(root, stages):
    return Adapter(
        run_id="FIXTURE",
        stages=stages,
        layout=Layout(
            root=root,
            producer=root / "producer",
            packets=root / "packets",
            obligations=root / "obligations",
            assessment=root / "assessment",
            manifest=root / "INDEX.json",
        ),
        schemas=Schemas(
            producer_manifest="fixture.manifest/v0",
            receipt="fixture.receipt/v0",
            archive="fixture.archive/v0",
            exposure_report="fixture.report/v0",
        ),
        pin=RuntimePin(
            core_commit="0" * 40, runtime=root / "runtime", package=root / "package"
        ),
    )


def test_a_template_and_a_launched_stage_both_refuse():
    with pytest.raises(launch.LaunchRefusal, match="TEMPLATE"):
        launch.refuse_not_launchable("A", {"status": "TEMPLATE_PENDING"})
    launch.refuse_not_launchable("A", {"status": "FROZEN"})
    launch.refuse_not_launchable(
        "A", {"status": "FROZEN_REHEARSAL"}, statuses=("FROZEN", "FROZEN_REHEARSAL")
    )
    with pytest.raises(launch.LaunchRefusal, match="already recorded"):
        launch.refuse_already_launched(
            "A", {"launch": {"launched": True, "launched_at": "now"}}
        )


def test_a_drifted_input_refuses_and_an_absent_one_too(tmp_path):
    workspace = tmp_path / "workspace"
    harness = tmp_path / "harness"
    workspace.mkdir()
    harness.mkdir()
    (workspace / "one.txt").write_bytes(b"one")
    manifest = {
        "declared_inputs": [
            {
                "path": "one.txt",
                "role": "TEXT",
                "sha256": digests.digest(b"one"),
                "in_workspace": True,
            }
        ]
    }
    rows, declared = launch.checked_inputs(manifest, workspace, harness)
    assert rows[0]["sha256"] == digests.digest(b"one")
    launch.refuse_undeclared_files(workspace, declared, work_dir="work")
    (workspace / "one.txt").write_bytes(b"two")
    with pytest.raises(launch.LaunchRefusal, match="is not the frozen"):
        launch.checked_inputs(manifest, workspace, harness)
    (workspace / "one.txt").unlink()
    with pytest.raises(launch.LaunchRefusal, match="declared and not present"):
        launch.checked_inputs(manifest, workspace, harness)


def test_the_producers_own_directory_is_outside_the_closure(tmp_path):
    workspace = tmp_path / "workspace"
    (workspace / "work").mkdir(parents=True)
    (workspace / "work/history.jsonl").write_bytes(b"{}")
    (workspace / "extra.json").write_bytes(b"{}")
    declared = {(workspace / "extra.json").resolve()}
    launch.refuse_undeclared_files(workspace, declared, work_dir="work")
    with pytest.raises(launch.LaunchRefusal, match="history.jsonl"):
        launch.refuse_undeclared_files(workspace, declared, work_dir="nothing")
    with pytest.raises(launch.LaunchRefusal, match="extra.json"):
        launch.refuse_undeclared_files(workspace, set(), work_dir="work")


def test_two_declared_source_ids_refuse_and_none_returns_none():
    assert launch.declared_source_id({"declared_inputs": []}) is None
    manifest = {
        "declared_inputs": [
            {"source_id": "source:one"},
            {"source_id": "source:two"},
        ]
    }
    with pytest.raises(launch.LaunchRefusal, match="2 declared inputs"):
        launch.declared_source_id(manifest)


def test_the_record_and_the_procedure_must_agree():
    launch.refuse_procedure_disagreement(
        "anchor --source-id source:one --packet p", "source:one"
    )
    with pytest.raises(launch.LaunchRefusal, match="source-id"):
        launch.refuse_procedure_disagreement("anchor --packet p", "source:one")
    launch.refuse_procedure_disagreement("no anchor line", None)
    with pytest.raises(launch.LaunchRefusal, match="declares no source id"):
        launch.refuse_procedure_disagreement(
            "anchor --source-id source:one", None, refuse_extra=True
        )


def test_the_spawn_message_must_carry_its_one_token(tmp_path):
    (tmp_path / "spawn-message.md").write_bytes(b"no token here")
    with pytest.raises(launch.LaunchRefusal, match="PRODUCER_WORKSPACE"):
        launch.dispatch_of(tmp_path, "/somewhere")
    (tmp_path / "spawn-message.md").write_bytes(b"own <PRODUCER_WORKSPACE>/work/")
    assert launch.dispatch_of(tmp_path, "/somewhere") == "own /somewhere/work/"


# ------------------------------------------------------------------ archive


def test_an_archive_is_read_only_and_never_replaced(tmp_path):
    stages = (Stage(name="A", workspace="workspace-a", harness="stage-a"),)
    adapter = _adapter(tmp_path, stages)
    harness = tmp_path / "producer/stage-a"
    work = tmp_path / "producer/workspace-a/work"
    work.mkdir(parents=True)
    harness.mkdir(parents=True)
    (work / "export.json").write_bytes(b"{}")
    (harness / "producer-input-manifest.json").write_bytes(
        digests.indented(
            {
                "run_id": "FIXTURE",
                "workspace": "producer/workspace-a",
                "launch": {"launched": True, "launched_at": "2026-09-21T00:00:00Z"},
            }
        )
    )
    result = archive.archive("A", adapter=adapter, root=tmp_path)
    assert result["files"] == 1
    copied = harness / "archive/2026-09-21T00:00:00Z/work/export.json"
    assert copied.read_bytes() == b"{}"
    assert copied.stat().st_mode & 0o777 == archive.READ_ONLY
    record = json.loads(
        (harness / "archive/2026-09-21T00:00:00Z/ARCHIVE.json").read_bytes()
    )
    assert record["schema"] == "fixture.archive/v0"
    with pytest.raises(archive.ArchiveRefusal, match="already"):
        archive.archive("A", adapter=adapter, root=tmp_path)


def test_an_unlaunched_stage_and_an_empty_work_both_refuse(tmp_path):
    stages = (Stage(name="A", workspace="workspace-a", harness="stage-a"),)
    adapter = _adapter(tmp_path, stages)
    harness = tmp_path / "producer/stage-a"
    harness.mkdir(parents=True)
    (tmp_path / "producer/workspace-a/work").mkdir(parents=True)
    (harness / "producer-input-manifest.json").write_bytes(
        digests.indented(
            {
                "run_id": "FIXTURE",
                "workspace": "producer/workspace-a",
                "launch": {"launched": False, "launched_at": None},
            }
        )
    )
    with pytest.raises(archive.ArchiveRefusal, match="not launched"):
        archive.archive("A", adapter=adapter, root=tmp_path)
    (harness / "producer-input-manifest.json").write_bytes(
        digests.indented(
            {
                "run_id": "FIXTURE",
                "workspace": "producer/workspace-a",
                "launch": {"launched": True, "launched_at": "2026-09-21T00:00:00Z"},
            }
        )
    )
    with pytest.raises(archive.ArchiveRefusal, match="no files"):
        archive.archive("A", adapter=adapter, root=tmp_path)
    with pytest.raises(archive.ArchiveRefusal, match="unknown stage"):
        archive.archive("Z", adapter=adapter, root=tmp_path)

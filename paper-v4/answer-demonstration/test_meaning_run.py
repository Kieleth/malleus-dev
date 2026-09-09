"""The amendment packet keeps producer inputs separate from query evidence."""

import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    "fault",
    [None, "same_session", "different_reviewer", "wrong_model", "missing_frames"],
)
def test_execution_requires_two_verified_fresh_deliveries(tmp_path, monkeypatch, fault):
    import meaning_run as run

    folder = tmp_path / "run"
    folder.mkdir()
    (folder / "manifest.json").write_bytes(
        run.canonical({"producer_model": "gpt-5.6-sol", "producer_effort": "ultra"})
    )
    monkeypatch.setattr(
        run.reconciliation, "authorize", lambda *_: {"reviewer_thread_id": "reviewer"}
    )
    calls = []

    def delivery(path, phase):
        calls.append((path, phase))
        if fault == "missing_frames":
            raise ValueError("incomplete model-visible delivery")
        producer = path == folder
        thread = "proposer" if producer else "reviewer"
        if not producer and fault == "same_session":
            thread = "proposer"
        if not producer and fault == "different_reviewer":
            thread = "unbound-reviewer"
        return {
            "thread_id": thread,
            "model": "different" if fault == "wrong_model" else "gpt-5.6-sol",
            "reasoning_effort": "ultra",
        }

    monkeypatch.setattr(run, "verify_delivery", delivery)
    if fault:
        with pytest.raises(ValueError):
            run.authorize_sources(folder, folder / "candidate.json")
    else:
        evidence = run.authorize_sources(folder, folder / "candidate.json")
        assert evidence["reviewer"]["thread_id"] == "reviewer"
        assert calls == [(folder, "initial"), (folder / "source-review-01", "initial")]


def test_frozen_packet_and_public_preflight():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_meaning_run import check_packet; check_packet()",
        ],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_frozen_withheld_candidate_never_creates_a_ledger():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_meaning_run import check_withheld; check_withheld()",
        ],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_withheld():
    import json
    from tempfile import TemporaryDirectory
    import meaning_run as run

    folder = run.PRIVATE / "sol-meaning-repair-01"
    candidate = folder / "producer/work/candidate-01.json"
    packet = folder / "source-review-01"
    decision = json.loads((packet / "decision.json").read_bytes())
    assert decision["status"] == "WITHHOLD_BATCH"
    assert decision["candidate_sha256"] == run.digest(candidate.read_bytes())
    assert decision["review_sha256"] == run.digest((packet / "review.md").read_bytes())
    assert decision["ratification"] == "PENDING_HUMAN"
    run.verify_materials(
        packet, json.loads((packet / "manifest.json").read_bytes())["materials"]
    )
    _, baseline = run.preflight(folder)
    _, compiled, _ = run.structural_check(folder, candidate)
    assert compiled.status == run.api.PopulationPlanStatus.CHANGE_SET
    before = (folder / "base-history.jsonl").read_bytes()
    with TemporaryDirectory(prefix="meaning-refusal-", dir=run.PRIVATE) as temp:
        output = run.Path(temp) / "must-not-exist"
        with pytest.raises(ValueError, match="affirmative independent source-review"):
            run.execute(
                folder, candidate, output, transaction_time="2026-09-09T02:00:00Z"
            )
        assert not output.exists()
    assert (folder / "base-history.jsonl").read_bytes() == before
    _, current = run.preflight(folder)
    assert current.receipt.canonical_bytes == baseline.receipt.canonical_bytes
    assert current.graph.export_records() == baseline.graph.export_records()
    queries, _ = run.query_view(folder, current)
    assert queries == json.loads((folder / "before-query.json").read_bytes())["queries"]


def check_packet():
    import json
    from tempfile import TemporaryDirectory
    from types import SimpleNamespace
    import pytest
    import meaning_run as run
    from input_delivery import input_frames

    with TemporaryDirectory(prefix="meaning-stage-", dir=run.PRIVATE) as temp:
        folder = run.Path(temp) / "run"
        manifest = run.stage(folder)
        assert manifest["producer_model"] == "gpt-5.6-sol"
        assert manifest["producer_effort"] == "ultra"
        assert manifest["maximum_structural_returns"] == 0
        assert manifest["decision"] == "E-0331"
        assert (
            len(json.loads((folder / "producer/inputs/targets.json").read_bytes()))
            == 76
        )
        frames = input_frames(folder, "initial")
        assert len(frames) >= 12
        assert all(
            "question" not in name and "query" not in name and "review" not in name
            for name in frames
        )
        assert set(frames) == {
            p.relative_to(folder / "producer").as_posix()
            for p in (folder / "producer").rglob("*")
            if p.is_file()
        }
        run.preflight(folder)
        before = json.loads((folder / "before-query.json").read_bytes())
        _, replay = run.preflight(folder)
        queries, traces = run.query_view(folder, replay)
        assert queries == before["queries"]
        assert len(traces) == 26
        candidate = folder / "producer/work/synthetic-packet-test.json"
        candidate.write_bytes(b'{"synthetic":"packet bytes only, not a population"}')
        candidate.with_suffix(".report.json").write_bytes(b'{"synthetic":"report"}')
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(
                run,
                "structural_check",
                lambda *_: (
                    SimpleNamespace(canonical_plan_bytes=b"{}"),
                    SimpleNamespace(status="SYNTHETIC_TEST"),
                    None,
                ),
            )
            review = run.prepare_review(folder, candidate)
        packet = folder / "source-review-01"
        review_frames = input_frames(packet, "initial")
        assert "inputs/population-surface.json" not in review_frames
        assert ".claude/skills/malleus-acolyte/SKILL.md" not in review_frames
        assert {
            "inputs/candidate.json",
            "inputs/report.json",
            "inputs/selected-reading.json",
            "inputs/ontology.yaml",
            "inputs/base-capture.json",
            "inputs/baseline-records.json",
        } <= review_frames.keys()
        assert review["candidate_sha256"] == run.digest(candidate.read_bytes())
        run.verify_materials(packet, review["materials"])
        assert (
            packet / "producer/inputs/candidate.json"
        ).read_bytes() == candidate.read_bytes()
        output = folder / "not-authorized"
        with pytest.raises(ValueError, match="source-review"):
            run.execute(
                folder,
                folder / "producer/work/absent.json",
                output,
                transaction_time="2026-09-09T02:00:00Z",
            )
        assert not output.exists()
        with pytest.raises(ValueError, match="overwrite"):
            run.stage(folder)
        reading = folder / "producer/inputs/selected-reading.json"
        old = reading.read_bytes()
        reading.write_bytes(old + b" ")
        with pytest.raises(ValueError):
            run.preflight(folder)
        reading.write_bytes(old)
        ledger = folder / "base-history.jsonl"
        ledger.write_bytes(ledger.read_bytes() + b"\n")
        with pytest.raises(ValueError):
            run.preflight(folder)

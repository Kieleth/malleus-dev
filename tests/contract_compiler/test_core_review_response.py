"""Mechanical contract for the 2026-09-01 core-review response journal."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HANDOVER = ROOT / "handover" / "2026-09-01-malleus-core-review.md"
JOURNAL = HANDOVER.with_name("2026-09-01-malleus-core-review-response.jsonl")
SCHEMA = "malleus.handover-review-response/v0"
REVIEW_ID = "core-review:2026-09-01"
FINDING_IDS = tuple([f"D{number}" for number in range(1, 13)] + ["W1"])
DISPOSITIONS = {
    "D1": "ADOPT",
    "D2": "ADOPT",
    "D3": "ADOPT",
    "D4": "DEFER",
    "D5": "ADOPT",
    "D6": "DEFER",
    "D7": "ADOPT",
    "D8": "ADOPT",
    "D9": "ADOPT",
    "D10": "RETURN",
    "D11": "ADOPT",
    "D12": "DEFER",
    "W1": "ADOPT",
}
ENVELOPE_FIELDS = {
    "schema",
    "sequence",
    "event_id",
    "event_type",
    "generated_at",
    "responsible_actor_id",
    "source_event_ids",
    "payload",
}
PAYLOAD_FIELDS = {
    "REVIEW_BOUND": {
        "review_id",
        "reviewed_target_commit",
        "reviewed_target_tree",
        "review_evidence_commit",
        "review_evidence_tree",
        "review_evidence_path",
        "review_evidence_blob",
        "review_evidence_sha256",
        "finding_ids",
    },
    "FINDING_DISPOSITIONED": {
        "review_id",
        "finding_id",
        "review_disposition",
        "rationale",
    },
    "CORRECTION_EVIDENCED": {
        "correction_id",
        "finding_ids",
        "target_commit",
        "target_tree",
        "files",
        "checks",
        "rationale",
    },
    "REREVIEW_REQUESTED": {
        "request_id",
        "prior_review_id",
        "target_commit",
        "target_tree",
        "finding_ids",
        "correction_event_ids",
        "intended_recipient_id",
        "review_question",
    },
}


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, member in pairs:
        if key in value:
            raise AssertionError(f"duplicate JSON member {key!r}")
        value[key] = member
    return value


def _events() -> list[dict[str, object]]:
    events = []
    for line_number, line in enumerate(JOURNAL.read_text(encoding="utf-8").splitlines(), 1):
        assert line, f"blank journal line {line_number}"
        event = json.loads(line, object_pairs_hook=_strict_object)
        assert isinstance(event, dict)
        events.append(event)
    return events


def _git(*arguments: str) -> bytes:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stderr.decode("utf-8")
    return completed.stdout


def _tree(commit: str) -> str:
    return _git("rev-parse", f"{commit}^{{tree}}").decode("ascii").strip()


def _blob(commit: str, path: str) -> str:
    return _git("rev-parse", f"{commit}:{path}").decode("ascii").strip()


def _sha256_at(commit: str, path: str) -> str:
    return "sha256:" + hashlib.sha256(_git("show", f"{commit}:{path}")).hexdigest()


def test_review_response_journal_is_closed_ordered_and_source_linked() -> None:
    events = _events()
    assert events
    assert [event["sequence"] for event in events] == list(range(len(events)))
    event_ids = [event["event_id"] for event in events]
    assert len(event_ids) == len(set(event_ids))

    seen: set[str] = set()
    for event in events:
        assert set(event) == ENVELOPE_FIELDS
        assert event["schema"] == SCHEMA
        assert isinstance(event["event_id"], str) and event["event_id"]
        assert event["generated_at"].endswith("Z")
        assert event["responsible_actor_id"] in {"actor:operator", "actor:overseer"}
        assert event["event_type"] in PAYLOAD_FIELDS
        assert set(event["payload"]) == PAYLOAD_FIELDS[event["event_type"]]
        assert len(event["source_event_ids"]) == len(set(event["source_event_ids"]))
        assert set(event["source_event_ids"]) <= seen
        seen.add(event["event_id"])


def test_review_binding_preserves_the_exact_original_review_evidence() -> None:
    events = _events()
    bound = events[0]
    assert bound["event_type"] == "REVIEW_BOUND"
    assert bound["source_event_ids"] == []
    payload = bound["payload"]
    assert payload == {
        "review_id": REVIEW_ID,
        "reviewed_target_commit": "bb56848a1ec711de7a90d362cb92c60ac11656e9",
        "reviewed_target_tree": "e21cb387c3544514acf30679598f03aeac9aa665",
        "review_evidence_commit": "ecc56d6453963759cfbdf38c9d6c510520a46a39",
        "review_evidence_tree": "8e9a1a3bce82ac0299e2465d509a0b4024571cfc",
        "review_evidence_path": "handover/2026-09-01-malleus-core-review.md",
        "review_evidence_blob": "c4fad398ea79c4c3429296e97ddc06dfb1b1854e",
        "review_evidence_sha256": (
            "sha256:dad7e090b0269a6260d3e85faac80da9b8b257ced4ceeea278df15c0f9c0758d"
        ),
        "finding_ids": list(FINDING_IDS),
    }
    assert _tree(payload["reviewed_target_commit"]) == payload["reviewed_target_tree"]
    assert _tree(payload["review_evidence_commit"]) == payload["review_evidence_tree"]
    assert _blob(payload["review_evidence_commit"], payload["review_evidence_path"]) == (
        payload["review_evidence_blob"]
    )
    assert _sha256_at(
        payload["review_evidence_commit"], payload["review_evidence_path"]
    ) == payload["review_evidence_sha256"]


def test_every_finding_has_one_immutable_operator_disposition() -> None:
    events = _events()
    dispositions = [
        event for event in events if event["event_type"] == "FINDING_DISPOSITIONED"
    ]
    assert [event["payload"]["finding_id"] for event in dispositions] == list(
        FINDING_IDS
    )
    assert {
        event["payload"]["finding_id"]: event["payload"]["review_disposition"]
        for event in dispositions
    } == DISPOSITIONS
    review_event_id = events[0]["event_id"]
    for event in dispositions:
        assert event["responsible_actor_id"] == "actor:operator"
        assert event["source_event_ids"] == [review_event_id]
        assert event["payload"]["review_id"] == REVIEW_ID
        assert event["payload"]["rationale"]


def test_correction_evidence_resolves_only_committed_exact_bytes() -> None:
    events = _events()
    corrections = [
        event for event in events if event["event_type"] == "CORRECTION_EVIDENCED"
    ]
    assert corrections
    disposition_ids = {
        event["payload"]["finding_id"]
        for event in events
        if event["event_type"] == "FINDING_DISPOSITIONED"
        and event["payload"]["review_disposition"] == "ADOPT"
    }
    for event in corrections:
        payload = event["payload"]
        assert set(payload["finding_ids"]) <= disposition_ids
        assert payload["target_tree"] == _tree(payload["target_commit"])
        assert payload["files"]
        for artifact in payload["files"]:
            assert set(artifact) == {"path", "git_blob", "sha256"}
            assert artifact["path"] and ".." not in Path(artifact["path"]).parts
            assert artifact["git_blob"] == _blob(
                payload["target_commit"], artifact["path"]
            )
            assert artifact["sha256"] == _sha256_at(
                payload["target_commit"], artifact["path"]
            )
        assert payload["checks"]
        for check in payload["checks"]:
            assert set(check) == {"argv", "exit_code", "result"}
            assert check["argv"] and all(
                isinstance(argument, str) and argument for argument in check["argv"]
            )
            assert check["exit_code"] == 0
            assert check["result"] == "PASS"
        assert payload["rationale"]


def test_fresh_rereview_targets_the_corrected_commit_not_a_review_record() -> None:
    events = _events()
    requests = [event for event in events if event["event_type"] == "REREVIEW_REQUESTED"]
    assert len(requests) == 1
    request = requests[0]
    assert request is events[-1]
    payload = request["payload"]
    assert payload["request_id"] == "rereview-request:core:1"
    assert payload["prior_review_id"] == REVIEW_ID
    assert payload["target_tree"] == _tree(payload["target_commit"])
    assert payload["target_commit"] not in {
        "bb56848a1ec711de7a90d362cb92c60ac11656e9",
        "ecc56d6453963759cfbdf38c9d6c510520a46a39",
    }
    correction_by_id = {
        event["event_id"]: event
        for event in events
        if event["event_type"] == "CORRECTION_EVIDENCED"
    }
    assert set(payload["correction_event_ids"]) <= set(correction_by_id)
    covered = {
        finding_id
        for event_id in payload["correction_event_ids"]
        for finding_id in correction_by_id[event_id]["payload"]["finding_ids"]
    }
    assert set(payload["finding_ids"]) == covered
    assert request["source_event_ids"] == payload["correction_event_ids"]
    assert payload["intended_recipient_id"] == "actor:independent-reviewer"
    assert payload["review_question"]


def test_handover_points_to_the_response_without_rewriting_historical_evidence() -> None:
    current = HANDOVER.read_text(encoding="utf-8")
    assert "## 9. Operator response and re-review" in current
    assert "2026-09-01-malleus-core-review-response.jsonl" in current
    historical = _git(
        "show",
        "ecc56d6453963759cfbdf38c9d6c510520a46a39:"
        "handover/2026-09-01-malleus-core-review.md",
    )
    assert hashlib.sha256(historical).hexdigest() == (
        "dad7e090b0269a6260d3e85faac80da9b8b257ced4ceeea278df15c0f9c0758d"
    )

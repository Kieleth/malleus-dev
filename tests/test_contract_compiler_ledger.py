from __future__ import annotations

import hashlib
import json
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.contract_compiler_ledger import (  # noqa: E402
    LedgerValidationError,
    canonical_json,
    entry_hash,
    load_ledger,
    render_status,
    verify_evidence_snapshot,
)


OVERSEER = ROOT / "design" / "contract_compiler" / "overseer"


def _copy_ledger(tmp_path: Path) -> Path:
    copied = tmp_path / "overseer"
    shutil.copytree(OVERSEER, copied)
    return copied


def _rewrite_entry(path: Path, mutate, *, rehash: bool) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    mutate(value)
    if rehash:
        value["entry_hash"] = entry_hash(value)
    path.write_text(canonical_json(value, indent=2) + "\n", encoding="utf-8")


def _reseal(root: Path) -> None:
    previous = "GENESIS"
    paths = sorted((root / "entries").glob("*.json"))
    for sequence, path in enumerate(paths, start=1):
        value = json.loads(path.read_text(encoding="utf-8"))
        value["sequence"] = sequence
        value["entry_id"] = f"OVR-{sequence:06d}"
        value["previous_entry_hash"] = previous
        value["entry_hash"] = entry_hash(value)
        path.write_text(canonical_json(value, indent=2) + "\n", encoding="utf-8")
        previous = value["entry_hash"]
    head = json.loads((root / "head.json").read_text(encoding="utf-8"))
    head.update(
        entry_count=len(paths),
        head_entry_id=f"OVR-{len(paths):06d}",
        head_hash=previous,
    )
    (root / "head.json").write_text(
        canonical_json(head, indent=2) + "\n",
        encoding="utf-8",
    )


def _append_correction(
    root: Path,
    *,
    target_id: str,
    actor_type: str,
    replacement_required: bool,
) -> str:
    paths = sorted((root / "entries").glob("*.json"))
    sequence = len(paths) + 1
    entry_id = f"OVR-{sequence:06d}"
    target = json.loads(
        (root / "entries" / f"{target_id}.json").read_text(encoding="utf-8")
    )
    prior = json.loads(paths[-1].read_text(encoding="utf-8"))["recorded_at"]
    recorded_at = (
        datetime.fromisoformat(prior.removesuffix("Z") + "+00:00")
        + timedelta(minutes=1)
    ).isoformat().replace("+00:00", "Z")
    subject = target["subject"]
    references = [{"relation": "SUPERSEDES", "target": target_id, "type": "ENTRY"}]
    if subject["type"] != "PROGRAM":
        references.append(
            {"relation": "AFFECTS", "target": subject["id"], "type": subject["type"]}
        )
    entry = {
        "actor": {
            "id": "operator" if actor_type == "OPERATOR" else "overseer",
            "type": actor_type,
        },
        "data": {
            "affected_subject_ids": [subject["id"]],
            "replacement_required": replacement_required,
            "supersedes_entry_id": target_id,
        },
        "entry_hash": "sha256:" + "0" * 64,
        "entry_id": entry_id,
        "entry_type": "CORRECTION",
        "ledger": "overseer",
        "previous_entry_hash": "sha256:" + "0" * 64,
        "recorded_at": recorded_at,
        "references": references,
        "schema": "malleus.contract-compiler.ledger-entry/v1",
        "sequence": sequence,
        "subject": subject,
        "summary": f"Correct the recorded {subject['id']} entry.",
        "why": "Synthetic validation case for append-only correction authority.",
    }
    path = root / "entries" / f"{entry_id}.json"
    path.write_text(canonical_json(entry, indent=2) + "\n", encoding="utf-8")
    _reseal(root)
    return entry_id


def _append_replacement_workstream(root: Path, source_id: str) -> str:
    paths = sorted((root / "entries").glob("*.json"))
    sequence = len(paths) + 1
    entry_id = f"OVR-{sequence:06d}"
    source = json.loads(
        (root / "entries" / f"{source_id}.json").read_text(encoding="utf-8")
    )
    prior = json.loads(paths[-1].read_text(encoding="utf-8"))["recorded_at"]
    recorded_at = (
        datetime.fromisoformat(prior.removesuffix("Z") + "+00:00")
        + timedelta(minutes=1)
    ).isoformat().replace("+00:00", "Z")
    source.update(
        entry_id=entry_id,
        sequence=sequence,
        recorded_at=recorded_at,
        summary="Replace the corrected workstream state.",
        why="Synthetic positive case for an active typed replacement.",
    )
    path = root / "entries" / f"{entry_id}.json"
    path.write_text(canonical_json(source, indent=2) + "\n", encoding="utf-8")
    _reseal(root)
    return entry_id


def test_overseer_ledger_and_projection_are_current() -> None:
    state = load_ledger(OVERSEER)

    assert state.head["entry_count"] == len(state.entries)
    assert state.head["head_entry_id"] == state.entries[-1]["entry_id"]
    assert state.head["head_hash"] == state.entries[-1]["entry_hash"]
    rendered = render_status(state)
    assert rendered == (OVERSEER / "status.md").read_text(encoding="utf-8")
    assert all(not line.endswith(" ") for line in rendered.splitlines())


def test_suffix_truncation_is_caught_by_separate_local_head(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    (copied / "entries" / "OVR-000006.json").unlink()

    with pytest.raises(LedgerValidationError, match="entry_count"):
        load_ledger(copied)


def test_entry_tampering_breaks_the_hash_chain(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000003.json"
    _rewrite_entry(target, lambda value: value.update(summary="tampered"), rehash=False)

    with pytest.raises(LedgerValidationError, match="entry_hash"):
        load_ledger(copied)


def test_duplicate_json_keys_fail_closed(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000001.json"
    text = target.read_text(encoding="utf-8")
    target.write_text(
        text.replace(
            '"ledger": "overseer"', '"ledger": "overseer",\n  "ledger": "overseer"'
        ),
        encoding="utf-8",
    )

    with pytest.raises(LedgerValidationError, match="duplicate JSON key"):
        load_ledger(copied)


def test_unknown_fields_fail_schema_validation(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000001.json"
    _rewrite_entry(
        target, lambda value: value.update(notes="unbounded escape hatch"), rehash=True
    )

    with pytest.raises(LedgerValidationError, match="schema"):
        load_ledger(copied)


def test_only_the_operator_can_record_a_decision(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000002.json"
    _rewrite_entry(
        target,
        lambda value: value["actor"].update(type="WORKER", id="worker:test"),
        rehash=True,
    )

    with pytest.raises(LedgerValidationError, match="schema"):
        load_ledger(copied)


def test_completed_workstream_requires_decision_evidence(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000003.json"
    _rewrite_entry(
        target,
        lambda value: value["data"].update(evidence_entry_ids=[]),
        rehash=True,
    )

    with pytest.raises(LedgerValidationError, match="schema"):
        load_ledger(copied)


def test_entry_type_and_payload_are_discriminated(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000004.json"
    _rewrite_entry(
        target, lambda value: value.update(entry_type="OBSERVATION"), rehash=True
    )

    with pytest.raises(LedgerValidationError, match="schema"):
        load_ledger(copied)


def test_workstream_subject_must_match_payload(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000005.json"
    _rewrite_entry(
        target,
        lambda value: value["subject"].update(id="CC-X03"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="workstream subject and payload"):
        load_ledger(copied, repository=ROOT)


def test_decision_subject_must_match_payload(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000002.json"
    _rewrite_entry(
        target,
        lambda value: value["subject"].update(id="OD-002"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="decision subject and payload"):
        load_ledger(copied, repository=ROOT)


def test_document_reference_cannot_escape_repository(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000001.json"
    _rewrite_entry(
        target,
        lambda value: value["references"][0].update(target="/etc/hosts"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="repository-relative"):
        load_ledger(copied, repository=ROOT)


def test_canonical_reference_must_exist_in_graph(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000002.json"
    _rewrite_entry(
        target,
        lambda value: value["references"][1].update(
            target="https://malleus.dev/not-a-canonical-record"
        ),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="absent from the canonical graph"):
        load_ledger(copied, repository=ROOT)


def test_entry_reference_must_point_backward(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000003.json"
    _rewrite_entry(
        target,
        lambda value: value["references"][0].update(target="OVR-000003"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="point backward"):
        load_ledger(copied, repository=ROOT)


def test_observation_cannot_complete_a_workstream(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000004.json"

    def make_observation(value: dict) -> None:
        value["entry_type"] = "OBSERVATION"
        value["data"] = {
            "as_of": value["recorded_at"],
            "basis": ["Unverified reviewer observation."],
            "limitations": ["No retained mechanical evidence."],
        }

    _rewrite_entry(target, make_observation, rehash=False)
    _reseal(copied)

    with pytest.raises(
        LedgerValidationError, match="OBSERVATION cannot satisfy a gate"
    ):
        load_ledger(copied, repository=ROOT)


def test_nonbootstrap_transition_requires_projected_prior_state(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000006.json"
    _rewrite_entry(
        target,
        lambda value: value["data"].update(bootstrap=False),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="previous_state"):
        load_ledger(copied, repository=ROOT)


def test_only_operator_can_correct_a_decision(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000002",
        actor_type="OVERSEER",
        replacement_required=False,
    )

    with pytest.raises(LedgerValidationError, match="only the operator"):
        load_ledger(copied, repository=ROOT)


def test_only_operator_can_correct_the_program_decision(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000001",
        actor_type="OVERSEER",
        replacement_required=False,
    )

    with pytest.raises(LedgerValidationError, match="only the operator"):
        load_ledger(copied, repository=ROOT)


def test_decision_correction_requires_operator_identity(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    correction_id = _append_correction(
        copied,
        target_id="OVR-000002",
        actor_type="OPERATOR",
        replacement_required=False,
    )
    _rewrite_entry(
        copied / "entries" / f"{correction_id}.json",
        lambda value: value["actor"].update(id="overseer"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="only the operator"):
        load_ledger(copied, repository=ROOT)


def test_correction_subject_must_equal_target_subject(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    correction_id = _append_correction(
        copied,
        target_id="OVR-000002",
        actor_type="OPERATOR",
        replacement_required=False,
    )
    _rewrite_entry(
        copied / "entries" / f"{correction_id}.json",
        lambda value: value.update(subject={"id": "CC-X03", "type": "WORKSTREAM"}),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="same subject"):
        load_ledger(copied, repository=ROOT)


def test_correction_that_requires_replacement_fails_without_one(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000002",
        actor_type="OPERATOR",
        replacement_required=True,
    )

    with pytest.raises(LedgerValidationError, match="replacement entry is absent"):
        load_ledger(copied, repository=ROOT)


def test_projected_state_correction_cannot_waive_replacement(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000006",
        actor_type="OVERSEER",
        replacement_required=False,
    )

    with pytest.raises(
        LedgerValidationError, match="projected state requires a replacement"
    ):
        load_ledger(copied, repository=ROOT)


def test_required_replacement_must_remain_active(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000006",
        actor_type="OVERSEER",
        replacement_required=True,
    )
    replacement_id = _append_replacement_workstream(copied, "OVR-000006")
    _append_correction(
        copied,
        target_id=replacement_id,
        actor_type="OVERSEER",
        replacement_required=True,
    )

    with pytest.raises(LedgerValidationError, match="replacement entry is absent"):
        load_ledger(copied, repository=ROOT)


def test_correction_of_correction_restores_the_original_projection(
    tmp_path: Path,
) -> None:
    copied = _copy_ledger(tmp_path)
    correction_id = _append_correction(
        copied,
        target_id="OVR-000006",
        actor_type="OVERSEER",
        replacement_required=True,
    )
    _append_correction(
        copied,
        target_id=correction_id,
        actor_type="OVERSEER",
        replacement_required=False,
    )

    state = load_ledger(copied, repository=ROOT)

    assert "| `CC-X03` | `PAUSED` |" in render_status(state)


def test_active_typed_replacement_projects_normally(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000006",
        actor_type="OVERSEER",
        replacement_required=True,
    )
    _append_replacement_workstream(copied, "OVR-000006")

    state = load_ledger(copied, repository=ROOT)

    assert "| `CC-X03` | `PAUSED` |" in render_status(state)


def test_evidence_reference_must_target_immutable_evidence_area(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000004.json"
    _rewrite_entry(
        target,
        lambda value: value["references"][0].update(
            target="design/PROTOCOL_FOUNDATION_GRAPH.ttl"
        ),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="immutable evidence"):
        load_ledger(copied, repository=ROOT)


def test_verified_fact_requires_immutable_evidence(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000004.json"
    _rewrite_entry(
        target,
        lambda value: value["references"].pop(0),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="requires immutable EVIDENCE"):
        load_ledger(copied, repository=ROOT)


def test_failed_verification_report_cannot_satisfy_a_gate(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    copied = repository / "design" / "contract_compiler" / "overseer"
    shutil.copytree(OVERSEER, copied)
    for relative in (
        "design/contract_compiler/program.md",
        "design/contract_compiler/decisions.md",
        "design/PROTOCOL_FOUNDATION_GRAPH.ttl",
    ):
        target = repository / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    for path in sorted((copied / "entries").glob("OVR-*.json"))[6:]:
        path.unlink()
    report_path = copied / "evidence" / "CC-D01.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["checks"][0]["result"] = "FAIL"
    report_path.write_text(canonical_json(report, indent=2) + "\n", encoding="utf-8")
    report_digest = "sha256:" + hashlib.sha256(report_path.read_bytes()).hexdigest()
    _rewrite_entry(
        copied / "entries" / "OVR-000004.json",
        lambda value: value["references"][0].update(digest=report_digest),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(
        LedgerValidationError, match="failed check cannot satisfy a gate"
    ):
        load_ledger(copied, repository=repository)


def test_evidence_sealing_checks_source_bytes(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("verified bytes\n", encoding="utf-8")
    digest = "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest()
    report = {
        "artifacts": [
            {
                "byte_length": len(artifact.read_bytes()),
                "path": "artifact.txt",
                "sha256": digest,
            }
        ],
        "base_commit": "0" * 40,
        "checks": [
            {
                "check_id": "fixture",
                "method": "Compare exact source bytes.",
                "observed": "Fixture matched.",
                "result": "PASS",
            }
        ],
        "limitations": [],
        "recorded_at": "2026-08-24T19:30:00Z",
        "schema": "malleus.contract-compiler.verification-report/v1",
        "workstream_id": "CC-D01",
    }
    report_path = tmp_path / "report.json"
    report_path.write_text(canonical_json(report, indent=2) + "\n", encoding="utf-8")

    verify_evidence_snapshot(
        report_path,
        tmp_path,
        schema_path=OVERSEER / "ledger.schema.json",
    )
    artifact.write_text("tampered bytes\n", encoding="utf-8")
    with pytest.raises(
        LedgerValidationError, match="byte length mismatch|digest mismatch"
    ):
        verify_evidence_snapshot(
            report_path,
            tmp_path,
            schema_path=OVERSEER / "ledger.schema.json",
        )


def test_latest_document_revision_must_match_current_bytes(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000009.json"
    _rewrite_entry(
        target,
        lambda value: value["data"]["documents"][0].update(
            after_digest="sha256:" + "0" * 64
        ),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="latest document digest mismatch"):
        load_ledger(copied, repository=ROOT)


def test_document_revision_path_cannot_escape_repository(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000007.json"
    _rewrite_entry(
        target,
        lambda value: value["data"]["documents"][0].update(path="../../etc/hosts"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="schema violation"):
        load_ledger(copied, repository=ROOT)

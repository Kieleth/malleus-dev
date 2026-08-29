from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType

import pytest

from malleus.ledger import canonical_json


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CHARTER = HERE / "CHARTER.md"
JOURNAL_MODULE = HERE / "journal.py"
SEED = HERE / "journal.jsonl"


def _load_journal() -> ModuleType:
    spec = importlib.util.spec_from_file_location("small_shop_journal", JOURNAL_MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("small-shop journal module cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(root: Path, *argv: str) -> bytes:
    result = subprocess.run(
        ("git", *argv),
        cwd=root,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    return result.stdout


def _new_repository(path: Path, *, symlink: bool = False) -> dict[str, object]:
    path.mkdir()
    _git(path, "init", "--quiet")
    _git(path, "config", "user.email", "small-shop@example.invalid")
    _git(path, "config", "user.name", "Small Shop Test")
    evidence_path = path / "design" / "evidence.md"
    evidence_path.parent.mkdir()
    evidence_path.write_bytes(b"committed evidence\n")
    relative = "design/evidence.md"
    if symlink:
        link = path / "design" / "evidence-link.md"
        link.symlink_to("evidence.md")
        relative = "design/evidence-link.md"
    _git(path, "add", "design")
    _git(path, "commit", "--quiet", "-m", "fixture")
    commit = _git(path, "rev-parse", "HEAD^{commit}").decode().strip()
    tree = _git(path, "rev-parse", "HEAD^{tree}").decode().strip()
    source = (
        (path / relative).read_bytes()
        if not symlink
        else b"evidence.md"
    )
    return {
        "root": path,
        "commit": commit,
        "tree": tree,
        "path": relative,
        "source": source,
    }


@pytest.fixture(scope="module")
def repository(tmp_path_factory: pytest.TempPathFactory) -> dict[str, object]:
    return _new_repository(tmp_path_factory.mktemp("small-shop-git") / "repository")


def _evidence(repository: dict[str, object]) -> list[dict[str, object]]:
    source = repository["source"]
    assert isinstance(source, bytes)
    return [
        {
            "role": "ONTOLOGY_REALIZATION_DESIGN",
            "path": repository["path"],
            "sha256": "sha256:" + hashlib.sha256(source).hexdigest(),
            "byte_length": len(source),
        }
    ]


def _intent_payload(journal: ModuleType, repository: dict[str, object]) -> dict:
    return {
        "series_id": journal.SERIES_ID,
        "fixture_id": journal.FIXTURE_ID,
        "checkpoint_id": journal.CHECKPOINT_ID,
        "ret_sequence": list(journal.RET_SEQUENCE),
        "claims_under_test": list(journal.CLAIMS_UNDER_TEST),
        "excluded_claims": list(journal.EXCLUDED_CLAIMS),
        "repository": {
            "commit": repository["commit"],
            "tree": repository["tree"],
        },
        "evidence": _evidence(repository),
    }


def _record(
    journal: ModuleType,
    repository: dict[str, object],
    *,
    sequence: int = 1,
    recorded_at: str = "2026-08-29T04:00:00Z",
    previous_record_hash: str = "GENESIS",
    kind: str = "INTENT_RECORDED",
    payload: dict | None = None,
) -> dict:
    record = {
        "schema_version": "1",
        "sequence": sequence,
        "kind": kind,
        "recorded_at": recorded_at,
        "responsible_actor": "test:operator",
        "previous_record_hash": previous_record_hash,
        "payload": payload if payload is not None else _intent_payload(journal, repository),
    }
    record["record_hash"] = journal._record_hash(record)
    return record


def _rehash(journal: ModuleType, record: dict) -> dict:
    record["record_hash"] = journal._record_hash(record)
    return record


def _write(path: Path, records: list[dict]) -> None:
    path.write_bytes(
        "".join(canonical_json(record) + "\n" for record in records).encode("utf-8")
    )


def _assert_refused(
    journal: ModuleType,
    path: Path,
    repository: dict[str, object],
    expected: str,
) -> None:
    with pytest.raises(journal.JournalError) as caught:
        journal.read_journal(path, root=repository["root"])
    assert expected in str(caught.value)


def test_charter_freezes_the_exact_ret_ladder_and_green_boundary() -> None:
    text = CHARTER.read_text(encoding="utf-8")
    ordered = [text.index(f"### RET-{number:03d}") for number in range(0, 70, 10)]

    assert ordered == sorted(ordered)
    for required in (
        "zero ABox population and produces zero `ProposedOperation` values",
        "`OrderContainsUnit(O1, X1)`",
        "After `I1` and `I2` exist",
        "supplier-order `B` correction from `1Y` at `e4` to `2Y` at `e7`",
        "bounded `I2` correction at `e9`",
        "`EVENT_ENTITY_CORRELATION_REPRESENTATION_UNSELECTED`",
        "Per-entity Event ordering remains a typed gap",
        "same declared accepted projection",
        "Direct GraphRecipe materialization is not GREEN",
    ):
        assert required in text


def test_charter_freezes_identity_compiler_skill_and_authority_guards() -> None:
    text = CHARTER.read_text(encoding="utf-8")

    for required in (
        "`Y1` and `Y2` are distinct physical items",
        "deterministic partial function over exact, closed inputs",
        "external, untrusted proposal producer",
        "Only accepted exact bytes become compiler input",
        "Compiler execution and replay never invoke the skill",
        "Independent oracle bytes are test evidence and are never execution input",
        "It cannot accept a proposal or change a projection",
        "public ABox encoding profile",
        "Event-endpoint expansion",
    ):
        assert required in text


def test_charter_leaves_exactly_six_fixture_choices_deferred() -> None:
    text = CHARTER.read_text(encoding="utf-8")
    deferred = text.split("## Deferred fixture choices", 1)[1].split(
        "## Journal staging", 1
    )[0]

    assert deferred.count("DEFERRED") == 1
    for choice in (
        "`RET-010` source occurrence",
        "`X1` to `X` transformation",
        "Relation-type literal",
        "Valid-time, calendar, and timezone policy",
        "Passive versus gating review",
        "Evidence-sufficiency rule",
    ):
        assert choice in deferred


def test_charter_defers_unconsumed_journal_kinds_tdd_first() -> None:
    text = CHARTER.read_text(encoding="utf-8")

    for kind in (
        "INPUT_SET_FROZEN",
        "ORACLE_FROZEN",
        "RUN_RECORDED",
        "MUTATION_RECORDED",
        "VERIFICATION_RECORDED",
        "REPLAY_RECORDED",
        "FINDING_RECORDED",
    ):
        assert f"`{kind}`" in text
    assert "must be added TDD-first" in text


@pytest.mark.parametrize("field", [
    "schema_version",
    "sequence",
    "kind",
    "recorded_at",
    "responsible_actor",
    "previous_record_hash",
    "payload",
    "record_hash",
])
def test_missing_envelope_field_refuses(
    tmp_path: Path,
    repository: dict[str, object],
    field: str,
) -> None:
    journal = _load_journal()
    record = _record(journal, repository)
    del record[field]
    path = tmp_path / "journal.jsonl"
    _write(path, [record])

    _assert_refused(journal, path, repository, "missing fields")


def test_unknown_envelope_field_refuses(
    tmp_path: Path,
    repository: dict[str, object],
) -> None:
    journal = _load_journal()
    record = _record(journal, repository)
    record["surprise"] = True
    _rehash(journal, record)
    path = tmp_path / "journal.jsonl"
    _write(path, [record])

    _assert_refused(journal, path, repository, "unknown fields")


def test_unknown_kind_refuses(tmp_path: Path, repository: dict[str, object]) -> None:
    journal = _load_journal()
    record = _record(journal, repository)
    record["kind"] = "RUN_RECORDED"
    _rehash(journal, record)
    path = tmp_path / "journal.jsonl"
    _write(path, [record])

    _assert_refused(journal, path, repository, "unsupported kind")


def test_duplicate_json_key_refuses(
    tmp_path: Path,
    repository: dict[str, object],
) -> None:
    journal = _load_journal()
    record = _record(journal, repository)
    encoded = canonical_json(record)
    duplicate = encoded.replace(
        '"kind":"INTENT_RECORDED",',
        '"kind":"INTENT_RECORDED","kind":"INTENT_RECORDED",',
        1,
    )
    path = tmp_path / "journal.jsonl"
    path.write_bytes((duplicate + "\n").encode("utf-8"))

    _assert_refused(journal, path, repository, "duplicate JSON key")


@pytest.mark.parametrize(
    ("wire", "expected"),
    [
        (b"\xff\n", "UTF-8"),
        (b"\n", "blank line"),
        (b"[]\n", "JSON object"),
        (b"{}", "terminal LF"),
    ],
)
def test_invalid_wire_refuses(
    tmp_path: Path,
    repository: dict[str, object],
    wire: bytes,
    expected: str,
) -> None:
    journal = _load_journal()
    path = tmp_path / "journal.jsonl"
    path.write_bytes(wire)

    _assert_refused(journal, path, repository, expected)


def test_embedded_blank_line_refuses(
    tmp_path: Path,
    repository: dict[str, object],
) -> None:
    journal = _load_journal()
    record = _record(journal, repository)
    path = tmp_path / "journal.jsonl"
    path.write_bytes((canonical_json(record) + "\n\n").encode("utf-8"))

    _assert_refused(journal, path, repository, "blank line")


def test_nonfinite_number_refuses(
    tmp_path: Path,
    repository: dict[str, object],
) -> None:
    journal = _load_journal()
    record = _record(journal, repository)
    record["sequence"] = float("nan")
    path = tmp_path / "journal.jsonl"
    path.write_bytes(
        (json.dumps(record, allow_nan=True, separators=(",", ":")) + "\n").encode()
    )

    _assert_refused(journal, path, repository, "non-finite")


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("schema_version", "2", "schema_version"),
        ("sequence", True, "sequence"),
        ("sequence", 2, "sequence"),
        ("recorded_at", "2026-08-29T04:00:00+00:00", "UTC Z"),
        ("recorded_at", "2026-8-29T04:00:00Z", "canonical"),
        ("responsible_actor", "  ", "responsible_actor"),
        ("previous_record_hash", "sha256:" + "0" * 64, "GENESIS"),
        ("record_hash", "sha256:" + "0" * 64, "record_hash mismatch"),
    ],
)
def test_invalid_envelope_value_refuses(
    tmp_path: Path,
    repository: dict[str, object],
    field: str,
    value: object,
    expected: str,
) -> None:
    journal = _load_journal()
    record = _record(journal, repository)
    record[field] = value
    if field != "record_hash":
        _rehash(journal, record)
    path = tmp_path / "journal.jsonl"
    _write(path, [record])

    _assert_refused(journal, path, repository, expected)


def test_timestamp_must_be_nondecreasing(
    tmp_path: Path,
    repository: dict[str, object],
) -> None:
    journal = _load_journal()
    first = _record(journal, repository, recorded_at="2026-08-29T04:00:01Z")
    second = _record(
        journal,
        repository,
        sequence=2,
        recorded_at="2026-08-29T04:00:00Z",
        previous_record_hash=first["record_hash"],
    )
    path = tmp_path / "journal.jsonl"
    _write(path, [first, second])

    _assert_refused(journal, path, repository, "nondecreasing")


def test_exact_predecessor_hash_is_required(
    tmp_path: Path,
    repository: dict[str, object],
) -> None:
    journal = _load_journal()
    first = _record(journal, repository)
    second = _record(
        journal,
        repository,
        sequence=2,
        recorded_at="2026-08-29T04:00:01Z",
        previous_record_hash="sha256:" + "0" * 64,
    )
    path = tmp_path / "journal.jsonl"
    _write(path, [first, second])

    _assert_refused(journal, path, repository, "previous_record_hash")


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (lambda payload: payload.pop("series_id"), "missing fields"),
        (lambda payload: payload.__setitem__("surprise", True), "unknown fields"),
        (lambda payload: payload.__setitem__("claims_under_test", "claim"), "claims_under_test"),
        (lambda payload: payload.__setitem__("evidence", {}), "evidence"),
        (lambda payload: payload.__setitem__("repository", []), "repository"),
    ],
)
def test_wrong_intent_payload_fields_or_types_refuse(
    tmp_path: Path,
    repository: dict[str, object],
    mutation,
    expected: str,
) -> None:
    journal = _load_journal()
    payload = _intent_payload(journal, repository)
    mutation(payload)
    record = _record(journal, repository, payload=payload)
    path = tmp_path / "journal.jsonl"
    _write(path, [record])

    _assert_refused(journal, path, repository, expected)


def test_operator_decision_payload_is_exact_and_typed(
    tmp_path: Path,
    repository: dict[str, object],
) -> None:
    journal = _load_journal()
    payload = {
        "decision_key": "compiler_authority_boundary",
        "formal_decision_refs": ["OKG-D013"],
        "selected_values": deepcopy(
            journal.OPERATOR_DECISIONS["compiler_authority_boundary"]["selected_values"]
        ),
        "deferred_values": deepcopy(
            journal.OPERATOR_DECISIONS["compiler_authority_boundary"]["deferred_values"]
        ),
        "repository": {
            "commit": repository["commit"],
            "tree": repository["tree"],
        },
        "evidence": _evidence(repository),
    }
    payload["deferred_values"]["ret_010_source_occurrence"] = "SELECTED"
    record = _record(
        journal,
        repository,
        kind="OPERATOR_DECISION_RECORDED",
        payload=payload,
    )
    path = tmp_path / "journal.jsonl"
    _write(path, [record])

    _assert_refused(journal, path, repository, "deferred_values")


def test_bad_or_mismatched_git_coordinates_refuse(
    tmp_path: Path,
    repository: dict[str, object],
) -> None:
    journal = _load_journal()
    for field, value, expected in (
        ("commit", "0" * 40, "commit does not exist"),
        ("tree", "1" * 40, "tree mismatch"),
    ):
        payload = _intent_payload(journal, repository)
        payload["repository"][field] = value
        record = _record(journal, repository, payload=payload)
        path = tmp_path / f"{field}.jsonl"
        _write(path, [record])
        _assert_refused(journal, path, repository, expected)


@pytest.mark.parametrize(
    ("artifact_path", "expected"),
    [
        ("/tmp/evidence.md", "repository-relative"),
        ("../evidence.md", "parent escape"),
        ("design/missing.md", "not a committed file"),
    ],
)
def test_invalid_evidence_path_refuses(
    tmp_path: Path,
    repository: dict[str, object],
    artifact_path: str,
    expected: str,
) -> None:
    journal = _load_journal()
    payload = _intent_payload(journal, repository)
    payload["evidence"][0]["path"] = artifact_path
    record = _record(journal, repository, payload=payload)
    path = tmp_path / "journal.jsonl"
    _write(path, [record])

    _assert_refused(journal, path, repository, expected)


def test_committed_symlink_evidence_refuses(tmp_path: Path) -> None:
    journal = _load_journal()
    repository = _new_repository(tmp_path / "repository", symlink=True)
    payload = _intent_payload(journal, repository)
    record = _record(journal, repository, payload=payload)
    path = tmp_path / "journal.jsonl"
    _write(path, [record])

    _assert_refused(journal, path, repository, "symlink")


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("sha256", "sha256:" + "0" * 64, "sha256 mismatch"),
        ("byte_length", 999, "byte_length mismatch"),
        ("sha256", "sha256:" + "A" * 64, "lowercase"),
    ],
)
def test_mismatched_evidence_artifact_refuses(
    tmp_path: Path,
    repository: dict[str, object],
    field: str,
    value: object,
    expected: str,
) -> None:
    journal = _load_journal()
    payload = _intent_payload(journal, repository)
    payload["evidence"][0][field] = value
    record = _record(journal, repository, payload=payload)
    path = tmp_path / "journal.jsonl"
    _write(path, [record])

    _assert_refused(journal, path, repository, expected)


def test_payment_first_ret_ordering_refuses(
    tmp_path: Path,
    repository: dict[str, object],
) -> None:
    journal = _load_journal()
    payload = _intent_payload(journal, repository)
    payload["ret_sequence"][1:3] = ["RET-020", "RET-010"]
    record = _record(journal, repository, payload=payload)
    path = tmp_path / "journal.jsonl"
    _write(path, [record])

    _assert_refused(journal, path, repository, "RET ladder")


@pytest.mark.parametrize(
    "claim",
    [
        "Y1_Y2_REVISION_CHAIN",
        "COMPILER_INVOKES_ONTOLOGY_CORRECTOR_SKILL",
        "REPLAY_INVOKES_ONTOLOGY_CORRECTOR_SKILL",
    ],
)
def test_unaccepted_identity_or_skill_authority_claim_refuses(
    tmp_path: Path,
    repository: dict[str, object],
    claim: str,
) -> None:
    journal = _load_journal()
    payload = _intent_payload(journal, repository)
    payload["claims_under_test"].append(claim)
    record = _record(journal, repository, payload=payload)
    path = tmp_path / "journal.jsonl"
    _write(path, [record])

    _assert_refused(journal, path, repository, "claims_under_test")


def test_committed_seed_has_exact_records_and_cli_check() -> None:
    journal = _load_journal()
    records = journal.read_journal(
        SEED,
        root=ROOT,
        expected_count=3,
        expected_head_hash=journal.EXPECTED_HEAD_HASH,
    )

    assert [record["kind"] for record in records] == [
        "OPERATOR_DECISION_RECORDED",
        "OPERATOR_DECISION_RECORDED",
        "INTENT_RECORDED",
    ]
    assert [record["payload"].get("decision_key") for record in records[:2]] == [
        "canonical_running_domain",
        "compiler_authority_boundary",
    ]
    assert records[2]["payload"]["ret_sequence"] == list(journal.RET_SEQUENCE)
    assert records[2]["payload"]["claims_under_test"] == list(
        journal.CLAIMS_UNDER_TEST
    )
    assert records[2]["payload"]["excluded_claims"] == list(
        journal.EXCLUDED_CLAIMS
    )
    assert all(
        record["payload"]["repository"]
        == {
            "commit": "37cf69d57ee85f8a5f936661f1cf5fbdb975573b",
            "tree": "00251ce0809e5240cfa08fc4e192811d30de8380",
        }
        for record in records
    )
    assert records[1]["payload"]["deferred_values"] == {
        "ret_010_source_occurrence": "DEFERRED",
        "x1_to_x_transform": "DEFERRED",
        "relation_type_literal": "DEFERRED",
        "valid_time_calendar_timezone": "DEFERRED",
        "passive_or_gating_review": "DEFERRED",
        "evidence_sufficiency_rule": "DEFERRED",
    }
    assert all(record["recorded_at"] > "2026-08-29T03:37:14Z" for record in records)
    completed = subprocess.run(
        (sys.executable, str(JOURNAL_MODULE), "check"),
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert f"3 records, head {journal.EXPECTED_HEAD_HASH}" in completed.stdout

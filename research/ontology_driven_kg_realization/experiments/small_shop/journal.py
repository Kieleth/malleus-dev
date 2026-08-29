#!/usr/bin/env python3
"""Validate the private Small Shop research-evidence journal."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import Any, Sequence

from malleus.ledger import canonical_json, content_digest


ROOT = Path(__file__).resolve().parents[4]
JOURNAL = Path(__file__).with_name("journal.jsonl")
SCHEMA_VERSION = "1"
GENESIS = "GENESIS"
RECORD_HASH_DOMAIN = "malleus:research:small-shop-journal:v1"
EXPECTED_HEAD_HASH = (
    "sha256:a1d5d89be132c05fac585fd269aec5b5c9790f16971138e68a4c158738dc6cc2"
)

SERIES_ID = "SMALL_SHOP_GRAPH_REALIZATION"
FIXTURE_ID = "OKG-FX001"
CHECKPOINT_ID = "OKG-CP002"
RET_SEQUENCE = (
    "RET-000",
    "RET-010",
    "RET-020",
    "RET-030",
    "RET-040",
    "RET-050",
    "RET-060",
)
CLAIMS_UNDER_TEST = (
    "RET_000_EFFECTIVE_CONTRACT_WITH_ZERO_POPULATION",
    "RET_010_PROTOCOL_ACCEPTED_ORDER_UNIT_RELATION",
    "RET_020_PROTOCOL_ACCEPTED_FIXED_ARITY_SETTLEMENT",
    "RET_030_PROTOCOL_ACCEPTED_B_AND_I2_CORRECTIONS",
    "RET_040_OD_010_EVENT_ENTITY_TYPED_REFUSAL",
    "RET_050_PER_ENTITY_EVENT_ORDER_TYPED_GAP",
    "RET_060_EXACT_REPLAY_PROJECTION_CONVERGENCE",
    "Y1_Y2_DISTINCT_PHYSICAL_ITEMS",
    "DETERMINISTIC_CLOSED_INPUT_COMPILER",
    "OPTIONAL_EXTERNAL_PROPOSAL_SKILL",
    "PROTOCOL_REVIEWED_EXACT_BYTES",
    "MODEL_FREE_REPLAY",
)
EXCLUDED_CLAIMS = (
    "Y1_Y2_REVISION_OR_SUPERSESSION",
    "DIRECT_GRAPH_RECIPE_ACCEPTANCE",
    "PUBLIC_ABOX_ENCODING_PROFILE",
    "EVENT_ENDPOINT_EXPANSION",
    "SKILL_INSIDE_COMPILER_OR_REPLAY",
    "INDEPENDENT_ORACLE_EXECUTION_INPUT",
    "JOURNAL_ACCEPTANCE_AUTHORITY",
)

OPERATOR_DECISIONS = {
    "canonical_running_domain": {
        "formal_decision_refs": ["OKG-D013"],
        "selected_values": {
            "canonical_fixture": "OKG-FX001",
            "later_stress_domains": "physics, chemistry",
        },
        "deferred_values": {},
    },
    "compiler_authority_boundary": {
        "formal_decision_refs": [],
        "selected_values": {
            "compiler": "DETERMINISTIC_CLOSED_INPUT",
            "ontology_builder_corrector": "OPTIONAL_EXTERNAL_PROPOSAL_PRODUCER",
            "candidate_admission": "PROTOCOL_REVIEW_BEFORE_ACCEPTED_INPUT",
            "replay": "RETAINED_BYTES_AND_RECORDED_ARTIFACTS_ONLY",
        },
        "deferred_values": {
            "ret_010_source_occurrence": "DEFERRED",
            "x1_to_x_transform": "DEFERRED",
            "relation_type_literal": "DEFERRED",
            "valid_time_calendar_timezone": "DEFERRED",
            "passive_or_gating_review": "DEFERRED",
            "evidence_sufficiency_rule": "DEFERRED",
        },
    },
    "ret_010_fixture_bundle": {
        "formal_decision_refs": [],
        "selected_values": {
            "source_occurrence": "RETAIN_E27_DERIVE_ENTITY_PAIRS_SELECT_O1_X1",
            "x1_to_x_transform": "EXPLICIT_TOTAL_LOOKUP_X1_TO_X",
            "relation_type_literal": "ORDER_CONTAINS_UNIT",
            "source_time_grammar": "%d-%m %H:%M",
            "normalized_valid_time": "2000-05-07T17:00:00Z",
            "temporal_provenance": "FIXTURE_DERIVED_SYNTHETIC_YEAR_AND_UTC",
            "review_semantics": "PASSIVE_EXACT_REVIEW_NOT_ACCEPT_AUTHORITY",
            "evidence_sufficiency": "CLOSED_DERIVATION_PACKAGE",
            "event_correlation_support": "RET_040_REMAINS_TYPED_RED",
        },
        "deferred_values": {},
    },
}

ENVELOPE_FIELDS = {
    "schema_version",
    "sequence",
    "kind",
    "recorded_at",
    "responsible_actor",
    "previous_record_hash",
    "payload",
    "record_hash",
}
DECISION_FIELDS = {
    "decision_key",
    "formal_decision_refs",
    "selected_values",
    "deferred_values",
    "repository",
    "evidence",
}
INTENT_FIELDS = {
    "series_id",
    "fixture_id",
    "checkpoint_id",
    "ret_sequence",
    "claims_under_test",
    "excluded_claims",
    "repository",
    "evidence",
}
REPOSITORY_FIELDS = {"commit", "tree"}
EVIDENCE_FIELDS = {"role", "path", "sha256", "byte_length"}
KINDS = {"OPERATOR_DECISION_RECORDED", "INTENT_RECORDED"}
EVIDENCE_ROLE_PATHS = {
    "RUNNING_DOMAIN_CHECKPOINT": (
        "design/GRAPH_REALIZATION_RUNNING_DOMAIN_CHECKPOINT.md"
    ),
    "ONTOLOGY_REALIZATION_DESIGN": "design/ONTOLOGY_DRIVEN_KG_REALIZATION.md",
}


class JournalError(ValueError):
    """The private research journal is malformed or cannot be verified."""


def _exact_fields(value: Any, expected: set[str], context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise JournalError(f"{context} must be a JSON object")
    missing = sorted(expected - value.keys())
    unknown = sorted(value.keys() - expected)
    if missing:
        raise JournalError(f"{context} has missing fields: {missing}")
    if unknown:
        raise JournalError(f"{context} has unknown fields: {unknown}")
    return value


def _nonblank_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise JournalError(f"{context} must be a nonblank canonical string")
    return value


def _sha256(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.startswith("sha256:"):
        raise JournalError(f"{context} must start with sha256:")
    encoded = value.removeprefix("sha256:")
    if encoded != encoded.lower():
        raise JournalError(f"{context} must use lowercase hexadecimal")
    if len(encoded) != 64:
        raise JournalError(f"{context} must contain 64 hexadecimal characters")
    try:
        decoded = bytes.fromhex(encoded)
    except ValueError as error:
        raise JournalError(f"{context} must contain hexadecimal characters") from error
    if len(decoded) != 32:
        raise JournalError(f"{context} must encode 32 bytes")
    return value


def _object_id(value: Any, context: str) -> str:
    if not isinstance(value, str):
        raise JournalError(f"{context} must be a 40-character Git object ID")
    if value != value.lower():
        raise JournalError(f"{context} must use lowercase hexadecimal")
    if len(value) != 40:
        raise JournalError(f"{context} must be a 40-character Git object ID")
    try:
        decoded = bytes.fromhex(value)
    except ValueError as error:
        raise JournalError(f"{context} must contain hexadecimal characters") from error
    if len(decoded) != 20:
        raise JournalError(f"{context} must encode 20 bytes")
    return value


def _timestamp(value: Any, context: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise JournalError(f"{context} must be a UTC Z timestamp")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as error:
        raise JournalError(f"{context} must be a canonical UTC Z timestamp") from error
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise JournalError(f"{context} must be a canonical UTC Z timestamp")
    return parsed


def _record_hash(record: dict[str, Any]) -> str:
    body = {
        key: deepcopy(value)
        for key, value in record.items()
        if key != "record_hash"
    }
    return content_digest(
        {"domain_separator": RECORD_HASH_DOMAIN, "record": body}
    )


def _git(root: Path, argv: tuple[str, ...], context: str) -> bytes:
    try:
        result = subprocess.run(
            argv,
            cwd=root,
            capture_output=True,
            check=False,
        )
    except OSError as error:
        raise JournalError(f"{context}: cannot run git: {error}") from error
    if result.returncode:
        detail = result.stderr.decode(errors="replace").strip()
        suffix = f": {detail}" if detail else ""
        raise JournalError(f"{context}{suffix}")
    return result.stdout


def _validate_repository(value: Any, root: Path) -> tuple[str, str]:
    repository = _exact_fields(value, REPOSITORY_FIELDS, "repository")
    commit = _object_id(repository["commit"], "repository.commit")
    tree = _object_id(repository["tree"], "repository.tree")
    _git(
        root,
        ("git", "cat-file", "-e", f"{commit}^{{commit}}"),
        f"repository commit does not exist: {commit}",
    )
    observed_tree = _git(
        root,
        ("git", "rev-parse", f"{commit}^{{tree}}"),
        f"cannot resolve tree for repository commit {commit}",
    ).decode("ascii").strip()
    if observed_tree != tree:
        raise JournalError(
            f"repository tree mismatch: expected {tree}, observed {observed_tree}"
        )
    return commit, tree


def _repository_path(value: Any) -> str:
    path = _nonblank_string(value, "evidence.path")
    if path.startswith("/"):
        raise JournalError("evidence.path must be repository-relative")
    if "\\" in path:
        raise JournalError("evidence.path must use repository-relative POSIX syntax")
    parts = path.split("/")
    if ".." in parts:
        raise JournalError("evidence.path contains a parent escape")
    if any(not part or part == "." for part in parts):
        raise JournalError("evidence.path must be canonical repository-relative syntax")
    if any(any(ord(character) < 32 for character in part) for part in parts):
        raise JournalError("evidence.path contains a control character")
    return path


def _committed_artifact(root: Path, commit: str, path: str) -> bytes:
    entry = _git(
        root,
        ("git", "ls-tree", "-z", commit, "--", path),
        f"cannot inspect committed evidence path {path}",
    )
    if not entry:
        raise JournalError(f"evidence.path is not a committed file: {path}")
    entries = [item for item in entry.split(b"\0") if item]
    if len(entries) != 1 or b"\t" not in entries[0]:
        raise JournalError(f"evidence.path does not resolve to one committed file: {path}")
    header, encoded_path = entries[0].split(b"\t", 1)
    fields = header.split(b" ")
    if len(fields) != 3:
        raise JournalError(f"evidence.path has an invalid Git tree entry: {path}")
    mode, kind, _object = fields
    if mode == b"120000":
        raise JournalError(f"evidence.path must not be a symlink: {path}")
    if mode not in {b"100644", b"100755"} or kind != b"blob":
        raise JournalError(f"evidence.path must be a committed regular file: {path}")
    try:
        observed_path = encoded_path.decode("utf-8")
    except UnicodeDecodeError as error:
        raise JournalError("evidence.path Git entry is not UTF-8") from error
    if observed_path != path:
        raise JournalError(f"evidence.path resolved to a different Git path: {path}")
    return _git(
        root,
        ("git", "cat-file", "blob", f"{commit}:{path}"),
        f"cannot read committed evidence path {path}",
    )


def _validate_evidence(value: Any, root: Path, commit: str) -> None:
    if not isinstance(value, list) or not value:
        raise JournalError("evidence must be a nonempty JSON array")
    seen: set[tuple[str, str]] = set()
    for position, item in enumerate(value, start=1):
        artifact = _exact_fields(item, EVIDENCE_FIELDS, f"evidence[{position}]")
        role = _nonblank_string(artifact["role"], f"evidence[{position}].role")
        required_path = EVIDENCE_ROLE_PATHS.get(role)
        if required_path is None:
            raise JournalError(f"evidence[{position}].role is unsupported: {role}")
        path = _repository_path(artifact["path"])
        if path != required_path:
            raise JournalError(
                f"evidence role {role} must bind {required_path}, got {path}"
            )
        identity = (role, path)
        if identity in seen:
            raise JournalError(f"evidence contains duplicate role/path: {role} {path}")
        seen.add(identity)
        expected_digest = _sha256(
            artifact["sha256"], f"evidence[{position}].sha256"
        )
        expected_length = artifact["byte_length"]
        if isinstance(expected_length, bool) or not isinstance(expected_length, int):
            raise JournalError(f"evidence[{position}].byte_length must be an integer")
        if expected_length < 0:
            raise JournalError(f"evidence[{position}].byte_length must be nonnegative")
        source = _committed_artifact(root, commit, path)
        observed_digest = "sha256:" + hashlib.sha256(source).hexdigest()
        if expected_digest != observed_digest:
            raise JournalError(
                f"evidence[{position}].sha256 mismatch: "
                f"expected {expected_digest}, observed {observed_digest}"
            )
        if expected_length != len(source):
            raise JournalError(
                f"evidence[{position}].byte_length mismatch: "
                f"expected {expected_length}, observed {len(source)}"
            )
    if seen != set(EVIDENCE_ROLE_PATHS.items()):
        raise JournalError("evidence must contain the exact v1 role/path set once")


def _validate_common_payload(payload: dict[str, Any], root: Path) -> None:
    commit, _tree = _validate_repository(payload["repository"], root)
    _validate_evidence(payload["evidence"], root, commit)


def _validate_decision(value: Any, root: Path) -> None:
    payload = _exact_fields(
        value, DECISION_FIELDS, "OPERATOR_DECISION_RECORDED payload"
    )
    decision_key = _nonblank_string(payload["decision_key"], "decision_key")
    specification = OPERATOR_DECISIONS.get(decision_key)
    if specification is None:
        raise JournalError(f"decision_key is unsupported: {decision_key}")
    for field in ("formal_decision_refs", "selected_values", "deferred_values"):
        if payload[field] != specification[field]:
            raise JournalError(
                f"{decision_key}.{field} does not match the frozen decision"
            )
    _validate_common_payload(payload, root)


def _validate_intent(value: Any, root: Path) -> None:
    payload = _exact_fields(value, INTENT_FIELDS, "INTENT_RECORDED payload")
    for field, expected in (
        ("series_id", SERIES_ID),
        ("fixture_id", FIXTURE_ID),
        ("checkpoint_id", CHECKPOINT_ID),
    ):
        observed = _nonblank_string(payload[field], field)
        if observed != expected:
            raise JournalError(f"{field} must be {expected}")
    if payload["ret_sequence"] != list(RET_SEQUENCE):
        raise JournalError("ret_sequence must match the frozen RET ladder")
    if payload["claims_under_test"] != list(CLAIMS_UNDER_TEST):
        raise JournalError("claims_under_test must match the frozen claim set")
    if payload["excluded_claims"] != list(EXCLUDED_CLAIMS):
        raise JournalError("excluded_claims must match the frozen exclusion set")
    _validate_common_payload(payload, root)


def _duplicate_safe_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise JournalError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_nonfinite(token: str) -> None:
    raise JournalError(f"non-finite JSON number is forbidden: {token}")


def _require_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise JournalError("non-finite JSON number is forbidden")
    if isinstance(value, dict):
        for nested in value.values():
            _require_finite(nested)
    elif isinstance(value, list):
        for nested in value:
            _require_finite(nested)


def _decode(path: Path) -> list[dict[str, Any]]:
    try:
        source = path.read_bytes()
    except OSError as error:
        raise JournalError(f"cannot read journal {path}: {error}") from error
    if not source.endswith(b"\n"):
        raise JournalError("journal must end with one terminal LF")
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as error:
        raise JournalError("journal must be valid UTF-8") from error
    lines = text[:-1].split("\n")
    if any(not line for line in lines):
        raise JournalError("journal contains a blank line")
    records = []
    for line_number, line in enumerate(lines, start=1):
        try:
            value = json.loads(
                line,
                object_pairs_hook=_duplicate_safe_object,
                parse_constant=_reject_nonfinite,
            )
        except JournalError:
            raise
        except json.JSONDecodeError as error:
            raise JournalError(
                f"journal line {line_number} is invalid JSON: {error.msg}"
            ) from error
        if not isinstance(value, dict):
            raise JournalError(f"journal line {line_number} must be a JSON object")
        _require_finite(value)
        try:
            canonical = canonical_json(value)
        except ValueError as error:
            raise JournalError(
                f"journal line {line_number} is not canonical JSON: {error}"
            ) from error
        if line != canonical:
            raise JournalError(f"journal line {line_number} is not canonical JSON")
        records.append(value)
    return records


def read_journal(
    path: Path = JOURNAL,
    *,
    root: Path = ROOT,
    expected_count: int | None = None,
    expected_head_hash: str | None = None,
) -> list[dict[str, Any]]:
    """Read and verify one immutable Small Shop research journal."""
    records = _decode(Path(path))
    expected_previous = GENESIS
    previous_time: datetime | None = None
    for expected_sequence, record in enumerate(records, start=1):
        _exact_fields(record, ENVELOPE_FIELDS, f"record {expected_sequence}")
        if record["schema_version"] != SCHEMA_VERSION:
            raise JournalError(
                f"record {expected_sequence} schema_version must be {SCHEMA_VERSION}"
            )
        sequence = record["sequence"]
        if isinstance(sequence, bool) or not isinstance(sequence, int):
            raise JournalError(f"record {expected_sequence} sequence must be an integer")
        if sequence != expected_sequence:
            raise JournalError(
                f"record sequence mismatch: expected {expected_sequence}, got {sequence}"
            )
        kind = _nonblank_string(record["kind"], f"record {sequence} kind")
        if kind not in KINDS:
            raise JournalError(f"record {sequence} has unsupported kind: {kind}")
        recorded_at = _timestamp(
            record["recorded_at"], f"record {sequence} recorded_at"
        )
        if previous_time is not None and recorded_at < previous_time:
            raise JournalError("recorded_at values must be nondecreasing")
        previous_time = recorded_at
        _nonblank_string(
            record["responsible_actor"], f"record {sequence} responsible_actor"
        )
        predecessor = record["previous_record_hash"]
        if expected_previous == GENESIS:
            if predecessor != GENESIS:
                raise JournalError("record 1 previous_record_hash must be GENESIS")
        else:
            _sha256(predecessor, f"record {sequence} previous_record_hash")
            if predecessor != expected_previous:
                raise JournalError(
                    f"record {sequence} previous_record_hash does not match record "
                    f"{sequence - 1}"
                )
        if kind == "OPERATOR_DECISION_RECORDED":
            _validate_decision(record["payload"], Path(root))
        else:
            _validate_intent(record["payload"], Path(root))
        observed_hash = _sha256(record["record_hash"], f"record {sequence} record_hash")
        calculated_hash = _record_hash(record)
        if observed_hash != calculated_hash:
            raise JournalError(
                f"record {sequence} record_hash mismatch: "
                f"expected {calculated_hash}, observed {observed_hash}"
            )
        expected_previous = observed_hash
    if expected_count is not None and len(records) != expected_count:
        raise JournalError(
            f"journal count mismatch: expected {expected_count}, got {len(records)}"
        )
    head = records[-1]["record_hash"] if records else GENESIS
    if expected_head_hash is not None and head != expected_head_hash:
        raise JournalError(
            f"journal head mismatch: expected {expected_head_hash}, got {head}"
        )
    return deepcopy(records)


def check() -> tuple[int, str]:
    records = read_journal(
        JOURNAL,
        root=ROOT,
        expected_count=4,
        expected_head_hash=EXPECTED_HEAD_HASH,
    )
    return len(records), records[-1]["record_hash"]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check",))
    arguments = parser.parse_args(argv)
    try:
        count, head = check()
    except JournalError as error:
        print(f"small-shop journal invalid: {error}", file=sys.stderr)
        return 1
    if arguments.command == "check":
        print(f"small-shop journal OK: {count} records, head {head}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate and render the contract-compiler overseer ledger.

The ledger is repository governance data, not a Malleus protocol ledger. It
therefore has no ontology identity. Each event is an immutable JSON block whose
canonical content participates in a hash chain. ``head.json`` supplies a
separate local count and head anchor. CC-000 will bind that head externally.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


ENTRY_ID = re.compile(r"^OVR-[0-9]{6}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
GENESIS = "GENESIS"
TASK_ID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
ALLOWED_TRANSITIONS = {
    "UNRECORDED": {"PLANNED"},
    "PLANNED": {"ACTIVE", "PAUSED", "COMPLETE", "REJECTED"},
    "ACTIVE": {"PAUSED", "COMPLETE", "REJECTED"},
    "PAUSED": {"ACTIVE", "REJECTED"},
    "COMPLETE": set(),
    "REJECTED": set(),
}
RELATION_TYPES = {
    "DEFINES": {"DOCUMENT"},
    "DECIDES": {"DOCUMENT", "DECISION"},
    "SATISFIES": {"WORKSTREAM"},
    "EVIDENCES": {"ENTRY", "EVIDENCE", "COMMIT"},
    "IMPLEMENTS": {"WORKSTREAM", "DOCUMENT"},
    "SUPERSEDES": {"ENTRY"},
    "COORDINATES": {"TASK"},
    "CANONICALIZES": {"CANONICAL_URI"},
    "AFFECTS": {"WORKSTREAM", "DECISION", "DOCUMENT", "TASK"},
}


class LedgerValidationError(ValueError):
    """The overseer ledger or its projection is malformed or inconsistent."""


@dataclass(frozen=True)
class LedgerState:
    root: Path
    entries: tuple[dict[str, Any], ...]
    head: dict[str, Any]


def canonical_json(value: Any, *, indent: int | None = None) -> str:
    """Encode the ledger's named canonical JSON grammar."""
    try:
        if indent is None:
            encoded = json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
        else:
            encoded = json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                indent=indent,
                allow_nan=False,
            )
        encoded.encode("utf-8")
        return encoded
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        raise LedgerValidationError(f"value is not canonical JSON: {error}") from error


def entry_hash(entry: Mapping[str, Any]) -> str:
    """Hash one entry, excluding only its generated ``entry_hash`` field."""
    body = {key: value for key, value in entry.items() if key != "entry_hash"}
    return "sha256:" + hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise LedgerValidationError(f"duplicate JSON key '{key}'")
        result[key] = value
    return result


def _reject_nonfinite(value: str) -> None:
    raise LedgerValidationError(f"nonfinite JSON number '{value}' is not allowed")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_nonfinite,
        )
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        LedgerValidationError,
    ) as error:
        raise LedgerValidationError(f"{path}: invalid JSON: {error}") from error
    if not isinstance(value, dict):
        raise LedgerValidationError(f"{path}: root must be an object")
    _reject_nonfinite_tree(value, str(path))
    return value


def _reject_nonfinite_tree(value: Any, context: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise LedgerValidationError(f"{context}: object keys must be strings")
            _reject_nonfinite_tree(item, f"{context}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_nonfinite_tree(item, f"{context}[{index}]")
    elif isinstance(value, float) and not math.isfinite(value):
        raise LedgerValidationError(f"{context}: nonfinite numbers are not allowed")


def _validate_schema(
    value: dict[str, Any], validator: Draft202012Validator, context: str
) -> None:
    errors = sorted(
        validator.iter_errors(value), key=lambda error: list(error.absolute_path)
    )
    if not errors:
        return
    first = errors[0]
    location = ".".join(str(part) for part in first.absolute_path) or "root"
    raise LedgerValidationError(
        f"{context}: schema violation at {location}: {first.message}"
    )


def verify_evidence_snapshot(
    report_path: Path,
    repository: Path,
    *,
    schema_path: Path | None = None,
) -> dict[str, Any]:
    """Seal-time check that a verification report describes current bytes."""
    repository = repository.resolve()
    schema_path = schema_path or (
        repository / "design" / "contract_compiler" / "overseer" / "ledger.schema.json"
    )
    schema = _read_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    report = _read_json(report_path)
    _validate_schema(report, validator, str(report_path))
    if report.get("schema") != "malleus.contract-compiler.verification-report/v1":
        raise LedgerValidationError(f"{report_path}: not a verification report")
    for artifact in report["artifacts"]:
        context = f"{report_path} artifact {artifact['path']}"
        path = _repository_path(repository, artifact["path"], context)
        if not path.is_file():
            raise LedgerValidationError(f"{context}: target does not exist")
        source = path.read_bytes()
        actual_length = len(source)
        if artifact["byte_length"] != actual_length:
            raise LedgerValidationError(
                f"{context}: byte length mismatch, expected "
                f"{artifact['byte_length']}, got {actual_length}"
            )
        actual_digest = "sha256:" + hashlib.sha256(source).hexdigest()
        if artifact["sha256"] != actual_digest:
            raise LedgerValidationError(
                f"{context}: digest mismatch, expected {artifact['sha256']}, "
                f"got {actual_digest}"
            )
    return report


def _parse_utc(value: str, context: str) -> datetime:
    if not value.endswith("Z"):
        raise LedgerValidationError(f"{context}: timestamp must use UTC Z form")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise LedgerValidationError(
            f"{context}: invalid timestamp '{value}'"
        ) from error
    return parsed


def _heading_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    for line in text.splitlines():
        if not line.startswith("#"):
            continue
        heading = line.lstrip("#").strip().lower()
        slug = re.sub(r"[^a-z0-9 _-]", "", heading)
        anchors.add(re.sub(r"[ _]+", "-", slug).strip("-"))
    return anchors


def _repository_path(repository: Path, relative: str, context: str) -> Path:
    relative_path = Path(relative)
    if (
        relative_path.is_absolute()
        or ".." in relative_path.parts
        or re.match(r"^[A-Za-z]:", relative) is not None
    ):
        raise LedgerValidationError(f"{context}: path must stay repository-relative")
    path = (repository / relative_path).resolve()
    if repository.resolve() not in path.parents:
        raise LedgerValidationError(f"{context}: path escapes the repository")
    return path


def _commit_has_durable_reference(repository: Path, commit: str) -> bool:
    if (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
            cwd=repository,
            capture_output=True,
            check=False,
        ).returncode
        == 0
    ):
        return True
    tags = subprocess.run(
        ["git", "tag", "--contains", commit, "--format=%(refname:short)"],
        cwd=repository,
        capture_output=True,
        check=False,
        text=True,
    )
    return tags.returncode == 0 and any(
        tag.startswith("evidence/") for tag in tags.stdout.splitlines()
    )


def _validate_references(
    entries: Sequence[dict[str, Any]],
    repository: Path,
    validator: Draft202012Validator,
) -> tuple[set[str], set[str], str]:
    positions = {entry["entry_id"]: index for index, entry in enumerate(entries)}
    program = (repository / "design" / "contract_compiler" / "program.md").read_text(
        encoding="utf-8"
    )
    decisions = (
        repository / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    canonical = (repository / "design" / "PROTOCOL_FOUNDATION_GRAPH.ttl").read_text(
        encoding="utf-8"
    )
    workstream_ids = set(re.findall(r"(?m)^\|\s*(CC-[A-Z0-9]+)\s*\|", program))
    decision_ids = set(
        re.findall(r"\b(?:AD|OD)-[0-9]{3}\b", program + "\n" + decisions)
    )
    evidence_root = (
        repository / "design" / "contract_compiler" / "overseer" / "evidence"
    ).resolve()

    for position, entry in enumerate(entries):
        for reference in entry["references"]:
            kind = reference["type"]
            target = reference["target"]
            relation = reference["relation"]
            context = f"{entry['entry_id']} reference {kind}:{target}"
            if kind not in RELATION_TYPES[relation]:
                raise LedgerValidationError(
                    f"{context}: relation {relation} cannot target {kind}"
                )
            if kind in {"DOCUMENT", "EVIDENCE"}:
                relative, separator, anchor = target.partition("#")
                path = _repository_path(repository, relative, context)
                if not path.is_file():
                    raise LedgerValidationError(f"{context}: target does not exist")
                if separator and anchor not in _heading_anchors(
                    path.read_text(encoding="utf-8")
                ):
                    raise LedgerValidationError(
                        f"{context}: heading anchor does not resolve"
                    )
                if kind == "DOCUMENT" and "digest" in reference:
                    raise LedgerValidationError(
                        f"{context}: mutable document references cannot carry a digest"
                    )
                if kind == "EVIDENCE":
                    if separator or evidence_root not in path.parents:
                        raise LedgerValidationError(
                            f"{context}: immutable evidence must be an unanchored overseer evidence file"
                        )
                    report = _read_json(path)
                    _validate_schema(report, validator, context)
                    digest = reference["digest"]
                    actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
                    if digest != actual:
                        raise LedgerValidationError(
                            f"{context}: digest mismatch, expected {digest}, got {actual}"
                        )
            elif kind == "WORKSTREAM" and target not in workstream_ids:
                raise LedgerValidationError(f"{context}: workstream does not resolve")
            elif kind == "DECISION" and target not in decision_ids:
                raise LedgerValidationError(f"{context}: decision does not resolve")
            elif kind == "ENTRY":
                if target not in positions:
                    raise LedgerValidationError(f"{context}: entry does not resolve")
                if positions[target] >= position:
                    raise LedgerValidationError(
                        f"{context}: entry references must point backward"
                    )
            elif kind == "TASK" and TASK_ID.fullmatch(target) is None:
                raise LedgerValidationError(f"{context}: task must be a canonical UUID")
            elif kind == "CANONICAL_URI" and f"<{target}>" not in canonical:
                raise LedgerValidationError(
                    f"{context}: URI is absent from the canonical graph"
                )
            elif kind == "COMMIT":
                if COMMIT.fullmatch(target) is None:
                    raise LedgerValidationError(
                        f"{context}: commit must be a full Git object ID"
                    )
                result = subprocess.run(
                    ["git", "cat-file", "-e", f"{target}^{{commit}}"],
                    cwd=repository,
                    capture_output=True,
                    check=False,
                )
                if result.returncode:
                    raise LedgerValidationError(f"{context}: commit does not resolve")
                if not _commit_has_durable_reference(repository, target):
                    raise LedgerValidationError(
                        f"{context}: commit must be reachable from HEAD or an "
                        "evidence/* tag"
                    )
    return workstream_ids, decision_ids, canonical


def _superseded_entries(entries: Sequence[dict[str, Any]]) -> set[str]:
    positions = {entry["entry_id"]: index for index, entry in enumerate(entries)}
    by_id = {entry["entry_id"]: entry for entry in entries}
    corrections: list[dict[str, Any]] = []
    for position, entry in enumerate(entries):
        if entry["entry_type"] != "CORRECTION":
            continue
        target_id = entry["data"]["supersedes_entry_id"]
        if target_id not in positions or positions[target_id] >= position:
            raise LedgerValidationError(
                f"{entry['entry_id']}: correction target must be an earlier entry"
            )
        target = by_id[target_id]
        if entry["subject"] != target["subject"]:
            raise LedgerValidationError(
                f"{entry['entry_id']}: correction and target must have the same subject"
            )
        if target["subject"]["id"] not in entry["data"]["affected_subject_ids"]:
            raise LedgerValidationError(
                f"{entry['entry_id']}: correction must name the target subject"
            )
        if target["subject"]["type"] in {"PROGRAM", "DECISION"} and entry["actor"] != {
            "id": "operator",
            "type": "OPERATOR",
        }:
            raise LedgerValidationError(
                f"{entry['entry_id']}: only the operator can correct a decision"
            )
        if (
            target["entry_type"] in {"DECISION", "WORKSTREAM_STATE"}
            and not entry["data"]["replacement_required"]
        ):
            raise LedgerValidationError(
                f"{entry['entry_id']}: correcting projected state requires a replacement"
            )
        expected_ref = {
            "relation": "SUPERSEDES",
            "type": "ENTRY",
            "target": target_id,
        }
        if not any(
            all(reference.get(key) == value for key, value in expected_ref.items())
            for reference in entry["references"]
        ):
            raise LedgerValidationError(
                f"{entry['entry_id']}: correction must reference the superseded entry"
            )
        corrections.append(entry)

    superseded: set[str] = set()
    for entry in reversed(entries):
        if entry["entry_id"] in superseded or entry["entry_type"] != "CORRECTION":
            continue
        superseded.add(entry["data"]["supersedes_entry_id"])

    for entry in corrections:
        if entry["entry_id"] in superseded:
            continue
        target = by_id[entry["data"]["supersedes_entry_id"]]
        if entry["data"]["replacement_required"]:
            position = positions[entry["entry_id"]]
            replacement = any(
                later["entry_type"] == target["entry_type"]
                and later["subject"] == target["subject"]
                and later["entry_id"] not in superseded
                for later in entries[position + 1 :]
            )
            if not replacement:
                raise LedgerValidationError(
                    f"{entry['entry_id']}: required replacement entry is absent"
                )
    return superseded


def _verified_fact_passes(entry: dict[str, Any], repository: Path) -> bool:
    evidence = [
        reference
        for reference in entry["references"]
        if reference["type"] == "EVIDENCE"
    ]
    return bool(evidence) and all(
        all(
            check["result"] == "PASS"
            for check in _read_json(
                _repository_path(
                    repository,
                    reference["target"],
                    f"{entry['entry_id']} gate evidence",
                )
            )["checks"]
        )
        for reference in evidence
    )


def _validate_semantics(
    entries: Sequence[dict[str, Any]],
    workstream_ids: set[str],
    decision_ids: set[str],
    canonical: str,
    repository: Path,
) -> set[str]:
    superseded = _superseded_entries(entries)
    active = [entry for entry in entries if entry["entry_id"] not in superseded]
    by_id = {entry["entry_id"]: entry for entry in active}
    positions = {entry["entry_id"]: index for index, entry in enumerate(entries)}
    workstream_state: dict[str, str] = {}
    document_history: dict[str, tuple[str, str]] = {}

    for entry in active:
        entry_type = entry["entry_type"]
        data = entry["data"]
        context = entry["entry_id"]
        if entry_type == "DECISION":
            decision_id = data["decision_id"]
            if entry["subject"]["type"] == "PROGRAM":
                if decision_id != "CC-PROGRAM-001":
                    raise LedgerValidationError(
                        f"{context}: program decision ID must be CC-PROGRAM-001"
                    )
            elif (
                entry["subject"]["id"] != decision_id or decision_id not in decision_ids
            ):
                raise LedgerValidationError(
                    f"{context}: decision subject and payload must resolve to the same ID"
                )
            for uri in data["canonical_record_uris"]:
                if f"<{uri}>" not in canonical:
                    raise LedgerValidationError(
                        f"{context}: canonical decision URI does not resolve: {uri}"
                    )
                if not any(
                    reference["relation"] == "CANONICALIZES"
                    and reference["type"] == "CANONICAL_URI"
                    and reference["target"] == uri
                    for reference in entry["references"]
                ):
                    raise LedgerValidationError(
                        f"{context}: canonical decision URI is absent from references: {uri}"
                    )
            unknown = set(data["satisfies_workstreams"]) - workstream_ids
            if unknown:
                raise LedgerValidationError(
                    f"{context}: unknown satisfied workstream: {sorted(unknown)[0]}"
                )
            for workstream_id in data["satisfies_workstreams"]:
                if not any(
                    reference["relation"] == "SATISFIES"
                    and reference["type"] == "WORKSTREAM"
                    and reference["target"] == workstream_id
                    for reference in entry["references"]
                ):
                    raise LedgerValidationError(
                        f"{context}: satisfied workstream is absent from references: "
                        f"{workstream_id}"
                    )
        elif entry_type == "VERIFIED_FACT":
            if not any(
                reference["type"] == "EVIDENCE" for reference in entry["references"]
            ):
                raise LedgerValidationError(
                    f"{context}: verified fact requires immutable EVIDENCE"
                )
        elif entry_type == "WORKSTREAM_STATE":
            workstream_id = data["workstream_id"]
            if (
                entry["subject"]["id"] != workstream_id
                or workstream_id not in workstream_ids
            ):
                raise LedgerValidationError(
                    f"{context}: workstream subject and payload must resolve to the same ID"
                )
            prior = workstream_state.get(workstream_id)
            if data["bootstrap"]:
                if prior is not None:
                    raise LedgerValidationError(
                        f"{context}: bootstrap is allowed only for the first recorded state"
                    )
            elif prior is None or data["previous_state"] != prior:
                raise LedgerValidationError(
                    f"{context}: previous_state does not match the projected state"
                )
            transition = (data["previous_state"], data["new_state"])
            if transition[1] not in ALLOWED_TRANSITIONS[transition[0]]:
                raise LedgerValidationError(
                    f"{context}: transition {transition[0]} -> {transition[1]} is not allowed"
                )
            for evidence_id in data["evidence_entry_ids"]:
                if (
                    evidence_id not in by_id
                    or positions[evidence_id] >= positions[context]
                ):
                    raise LedgerValidationError(
                        f"{context}: evidence entry must be active and earlier: {evidence_id}"
                    )
                if by_id[evidence_id]["entry_type"] not in {
                    "DECISION",
                    "VERIFIED_FACT",
                    "DOCUMENT_REVISION",
                }:
                    raise LedgerValidationError(
                        f"{context}: {by_id[evidence_id]['entry_type']} cannot satisfy a gate"
                    )
                if by_id[evidence_id][
                    "entry_type"
                ] == "VERIFIED_FACT" and not _verified_fact_passes(
                    by_id[evidence_id], repository
                ):
                    raise LedgerValidationError(
                        f"{context}: VERIFIED_FACT with a failed check cannot satisfy a gate"
                    )
                if not any(
                    reference["relation"] == "EVIDENCES"
                    and reference["type"] == "ENTRY"
                    and reference["target"] == evidence_id
                    for reference in entry["references"]
                ):
                    raise LedgerValidationError(
                        f"{context}: evidence entry is absent from references: {evidence_id}"
                    )
            workstream_state[workstream_id] = data["new_state"]
        elif entry_type == "DOCUMENT_REVISION":
            seen_paths: set[str] = set()
            for document in data["documents"]:
                relative = document["path"]
                if relative in seen_paths:
                    raise LedgerValidationError(
                        f"{context}: duplicate document path in one revision: {relative}"
                    )
                seen_paths.add(relative)
                _repository_path(repository, relative, context)
                previous = document_history.get(relative)
                if previous is not None:
                    if document["change"] == "CREATED":
                        raise LedgerValidationError(
                            f"{context}: previously recorded document cannot be CREATED"
                        )
                    if document["before_digest"] != previous[0]:
                        raise LedgerValidationError(
                            f"{context}: before_digest does not match prior revision for {relative}"
                        )
                document_history[relative] = (document["after_digest"], context)

    for relative, (expected, context) in document_history.items():
        path = _repository_path(repository, relative, context)
        if not path.is_file():
            raise LedgerValidationError(
                f"{context}: revised document does not exist: {relative}"
            )
        actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise LedgerValidationError(
                f"{context}: latest document digest mismatch for {relative}, "
                f"expected {expected}, got {actual}"
            )
    return superseded


def load_ledger(root: Path, *, repository: Path | None = None) -> LedgerState:
    """Load every immutable block plus the separate local head anchor."""
    root = root.resolve()
    repository = repository.resolve() if repository is not None else root.parents[2]
    schema = _read_json(root / "ledger.schema.json")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        raise LedgerValidationError(
            f"ledger.schema.json is invalid: {error.message}"
        ) from error
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    head = _read_json(root / "head.json")
    _validate_schema(head, validator, "head.json")
    paths = sorted((root / "entries").glob("*.json"))
    if len(paths) != head["entry_count"]:
        raise LedgerValidationError(
            f"head entry_count is {head['entry_count']}, found {len(paths)} entry files"
        )

    entries: list[dict[str, Any]] = []
    previous_hash = GENESIS
    previous_time: datetime | None = None
    for sequence, path in enumerate(paths, start=1):
        entry = _read_json(path)
        context = path.name
        _validate_schema(entry, validator, context)
        expected_id = f"OVR-{sequence:06d}"
        if path.stem != expected_id or entry["entry_id"] != expected_id:
            raise LedgerValidationError(
                f"{context}: entry ID and filename must be {expected_id}"
            )
        if entry["sequence"] != sequence:
            raise LedgerValidationError(f"{context}: sequence must be {sequence}")
        recorded_at = _parse_utc(entry["recorded_at"], f"{context} recorded_at")
        if previous_time is not None and recorded_at < previous_time:
            raise LedgerValidationError(f"{context}: recorded_at decreased")
        if entry["previous_entry_hash"] != previous_hash:
            raise LedgerValidationError(f"{context}: previous_entry_hash mismatch")
        actual_hash = entry_hash(entry)
        if entry["entry_hash"] != actual_hash:
            raise LedgerValidationError(
                f"{context}: entry_hash mismatch, expected {actual_hash}"
            )
        entries.append(entry)
        previous_hash = entry["entry_hash"]
        previous_time = recorded_at

    if not entries:
        raise LedgerValidationError("the overseer ledger must not be empty")
    if head["head_entry_id"] != entries[-1]["entry_id"]:
        raise LedgerValidationError("head_entry_id does not match the final entry")
    if head["head_hash"] != entries[-1]["entry_hash"]:
        raise LedgerValidationError("head_hash does not match the final entry")

    workstreams, decisions, canonical = _validate_references(
        entries,
        repository,
        validator,
    )
    _validate_semantics(entries, workstreams, decisions, canonical, repository)
    return LedgerState(root=root, entries=tuple(entries), head=head)


def _cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_status(state: LedgerState) -> str:
    """Render the bounded current-state projection from validated entries."""
    decisions: dict[str, dict[str, Any]] = {}
    workstreams: dict[str, dict[str, Any]] = {}
    superseded = _superseded_entries(state.entries)
    for entry in state.entries:
        if entry["entry_id"] in superseded:
            continue
        if entry["entry_type"] == "DECISION":
            decisions[entry["data"]["decision_id"]] = entry
        elif entry["entry_type"] == "WORKSTREAM_STATE":
            workstreams[entry["data"]["workstream_id"]] = entry

    lines = [
        "# Contract compiler overseer status",
        "",
        "Generated from validated immutable ledger blocks. Do not edit this file by hand.",
        "",
        f"Ledger entries: `{state.head['entry_count']}`",
        f"Ledger head: `{state.head['head_entry_id']}` / `{state.head['head_hash']}`",
        "Schema: [`ledger.schema.json`](ledger.schema.json)",
        "History: [`entries/`](entries/)",
        "",
        "## Accepted decisions",
        "",
        "| Decision | Selection | Constraint | Block |",
        "|---|---|---|---|",
    ]
    for decision_id, entry in sorted(decisions.items()):
        data = entry["data"]
        if data["state"] != "ACCEPTED":
            continue
        constraint = (
            "; ".join(item.rstrip(".") for item in data["constraints"])
            or "None recorded"
        )
        lines.append(
            f"| `{decision_id}` | {_cell(data['selected_option'])} | "
            f"{_cell(constraint)} | [`{entry['entry_id']}`](entries/{entry['entry_id']}.json) |"
        )

    lines.extend(
        [
            "",
            "Open choices remain in the [decision workbook](../decisions.md).",
            "",
            "## Workstream state",
            "",
            "| Workstream | State | Current result | Block |",
            "|---|---|---|---|",
        ]
    )
    for workstream_id, entry in sorted(workstreams.items()):
        data = entry["data"]
        result = "; ".join(item.rstrip(".") for item in data["deliverables"])
        lines.append(
            f"| `{workstream_id}` | `{data['new_state']}` | {_cell(result)} | "
            f"[`{entry['entry_id']}`](entries/{entry['entry_id']}.json) |"
        )

    blockers = [
        (workstream_id, blocker)
        for workstream_id, entry in sorted(workstreams.items())
        for blocker in entry["data"]["blockers"]
    ]
    lines.extend(["", "## Active blockers", ""])
    if blockers:
        lines.extend(f"- `{workstream}`: {blocker}" for workstream, blocker in blockers)
    else:
        lines.append("None recorded.")

    lines.extend(
        [
            "",
            "## Latest blocks",
            "",
            "| Recorded at | Type | Subject | Summary |",
            "|---|---|---|---|",
        ]
    )
    for entry in state.entries[-10:]:
        lines.append(
            f"| `{entry['recorded_at']}` | `{entry['entry_type']}` | "
            f"`{entry['subject']['id']}` | "
            f"[{_cell(entry['summary'])}](entries/{entry['entry_id']}.json) |"
        )
    return "\n".join(lines) + "\n"


def _write_atomic(path: Path, text: str) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = ""
    finally:
        if temporary:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=("check", "render", "hash", "verify-evidence"),
        help="validate, render, hash one draft, or verify evidence source bytes",
    )
    parser.add_argument("path", nargs="?", type=Path)
    arguments = parser.parse_args(argv)
    default_root = (
        Path(__file__).resolve().parents[1]
        / "design"
        / "contract_compiler"
        / "overseer"
    )

    if arguments.command == "hash":
        if arguments.path is None:
            parser.error("hash requires an entry path")
        print(entry_hash(_read_json(arguments.path)))
        return 0

    if arguments.command == "verify-evidence":
        if arguments.path is None:
            parser.error("verify-evidence requires a report path")
        repository = Path(__file__).resolve().parents[1]
        report = verify_evidence_snapshot(arguments.path, repository)
        print(
            f"verified {len(report['artifacts'])} artifacts and "
            f"{len(report['checks'])} recorded checks for {report['workstream_id']}"
        )
        return 0

    root = arguments.path or default_root
    state = load_ledger(root)
    rendered = render_status(state)
    status = root / "status.md"
    if arguments.command == "render":
        _write_atomic(status, rendered)
        return 0
    if not status.is_file() or status.read_text(encoding="utf-8") != rendered:
        raise LedgerValidationError("status.md is not the exact generated projection")
    print(
        f"validated {state.head['entry_count']} entries; "
        f"head {state.head['head_entry_id']} {state.head['head_hash']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

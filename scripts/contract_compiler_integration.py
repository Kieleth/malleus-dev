#!/usr/bin/env python3
"""Validate CC-000 workstream registration and integration handoffs.

The validator never executes commands found in governance data. It performs a
fixed set of JSON Schema, file, ledger, and Git object checks. The integration
manifest grants repository permissions; it is not an ontology or a runtime
consumer-bundle manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError, ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.contract_compiler_ledger import load_ledger
from scripts.contract_compiler_ledger import _superseded_entries as superseded_entries


COMMIT = re.compile(r"^[0-9a-f]{40}$")
WORKSTREAM = re.compile(r"^CC-[A-Z0-9]+$")
GLOB_CHARACTERS = frozenset("*?[")
EXPECTED_OWNER_SEPARATIONS = frozenset(
    {
        ("CC-011", "CC-012"),
        ("CC-013", "CC-014"),
        ("CC-015", "CC-016"),
        ("CC-019", "CC-020"),
    }
)
TDD_PHASES = (
    "RED",
    "GREEN",
    "SLICE",
    "DISPROOF",
    "REGRESSION",
    "PACKAGE",
    "ATTEST",
)


class IntegrationValidationError(ValueError):
    """CC-000 refused a malformed or unauthorized integration state."""


@dataclass(frozen=True)
class IntegrationState:
    """Validated registry, active cards, and selected candidates."""

    manifest: dict[str, Any]
    workstreams: Mapping[str, tuple[str, ...]]
    cards: Mapping[str, dict[str, Any]]
    selections: tuple[str, ...]


def _fail(code: str, message: str) -> None:
    raise IntegrationValidationError(f"[{code}] {message}")


def canonical_json(value: Any, *, indent: int | None = None) -> str:
    """Return the one named canonical JSON representation used by CC-000."""
    try:
        if indent is None:
            return json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=indent,
            allow_nan=False,
        )
    except (TypeError, ValueError, UnicodeError) as error:
        _fail("CC000_JSON", f"value is not canonical JSON: {error}")


def _digest(source: bytes) -> str:
    return "sha256:" + hashlib.sha256(source).hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            _fail("CC000_JSON_DUPLICATE_KEY", f"duplicate JSON key '{key}'")
        value[key] = item
    return value


def _reject_constant(value: str) -> None:
    _fail("CC000_JSON_NONFINITE", f"nonfinite JSON number '{value}' is forbidden")


def _reject_nonfinite(value: Any, context: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_nonfinite(item, f"{context}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_nonfinite(item, f"{context}[{index}]")
    elif isinstance(value, float) and not math.isfinite(value):
        _fail("CC000_JSON_NONFINITE", f"{context} contains a nonfinite number")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except IntegrationValidationError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        _fail("CC000_JSON", f"{path}: invalid JSON: {error}")
    if not isinstance(value, dict):
        _fail("CC000_JSON", f"{path}: root must be an object")
    _reject_nonfinite(value, str(path))
    return value


def _schema(repository: Path) -> dict[str, Any]:
    schema = _read_json(
        repository / "design" / "contract_compiler" / "integration.schema.json"
    )
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        _fail("CC000_SCHEMA_INVALID", error.message)
    return schema


def _walk_errors(error: ValidationError) -> Sequence[ValidationError]:
    return (error, *(child for item in error.context for child in _walk_errors(item)))


def _validate_schema(
    value: dict[str, Any],
    schema: dict[str, Any],
    definition: str,
    context: str,
) -> None:
    validator = Draft202012Validator(
        {
            "$ref": f"#/$defs/{definition}",
            "$defs": schema["$defs"],
        },
        format_checker=FormatChecker(),
    )
    errors = sorted(
        validator.iter_errors(value), key=lambda error: list(error.absolute_path)
    )
    if not errors:
        return
    flattened = [item for error in errors for item in _walk_errors(error)]
    unknown = next(
        (error for error in flattened if error.validator == "additionalProperties"),
        None,
    )
    selected = unknown or errors[0]
    location = ".".join(str(part) for part in selected.absolute_path) or "root"
    if unknown is not None:
        code = "CC000_SCHEMA_UNKNOWN_FIELD"
    elif selected.validator in {"minItems", "maxItems"} and location == "workstreams":
        code = "CC000_REGISTRY_COUNT"
    else:
        code = "CC000_SCHEMA"
    _fail(code, f"{context}: schema violation at {location}: {selected.message}")


def _table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def load_program_registry(program_path: Path) -> dict[str, tuple[str, ...]]:
    """Read the approved Markdown workstream tables without a second DAG copy."""
    try:
        lines = program_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        _fail("CC000_PROGRAM", f"cannot read {program_path}: {error}")
    registry: dict[str, tuple[str, ...]] = {}
    dependency_column: int | None = None
    for line in lines:
        if not line.startswith("|"):
            dependency_column = None
            continue
        cells = _table_cells(line)
        if cells and cells[0] == "ID":
            labels = {label.lower(): index for index, label in enumerate(cells)}
            dependency_column = labels.get("depends on")
            continue
        if not cells or WORKSTREAM.fullmatch(cells[0]) is None:
            continue
        if dependency_column is None or dependency_column >= len(cells):
            _fail(
                "CC000_PROGRAM",
                f"{cells[0]} appears outside a table with a Depends on column",
            )
        workstream_id = cells[0]
        if workstream_id in registry:
            _fail("CC000_PROGRAM", f"duplicate program workstream {workstream_id}")
        raw = cells[dependency_column]
        dependencies = () if raw == "none" else tuple(
            item.strip() for item in raw.split(",")
        )
        if any(WORKSTREAM.fullmatch(item) is None for item in dependencies):
            _fail(
                "CC000_PROGRAM",
                f"{workstream_id} has malformed dependencies: {raw}",
            )
        registry[workstream_id] = dependencies
    if not registry:
        _fail("CC000_PROGRAM", "the approved program contains no workstreams")
    return registry


def _safe_path(value: str, context: str) -> str:
    if "\\" in value or any(character in value for character in GLOB_CHARACTERS):
        _fail("CC000_PATH_UNSAFE", f"{context}: paths are exact and cannot use globs")
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or value.endswith("/")
        or "." in path.parts
        or ".." in path.parts
        or re.match(r"^[A-Za-z]:", value) is not None
    ):
        _fail("CC000_PATH_UNSAFE", f"{context}: path must stay repository-relative")
    return path.as_posix()


def _bundle_path(root: Path, value: str, context: str) -> Path:
    relative = _safe_path(value, context)
    root = root.resolve()
    path = (root / relative).resolve()
    if root != path and root not in path.parents:
        _fail("CC000_PATH_UNSAFE", f"{context}: symlink escapes the manifest bundle")
    return path


def _scope_contains(scope: Mapping[str, str], path: str) -> bool:
    root = scope["path"]
    return path == root or (scope["kind"] == "TREE" and path.startswith(root + "/"))


def _scopes_overlap(left: Mapping[str, str], right: Mapping[str, str]) -> bool:
    return _scope_contains(left, right["path"]) or _scope_contains(right, left["path"])


def _git(
    repository: Path,
    *arguments: str,
    text: bool = True,
) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", *arguments],
        cwd=repository,
        capture_output=True,
        check=False,
        text=text,
    )


def _require_git_object(repository: Path, object_id: str, kind: str) -> None:
    if COMMIT.fullmatch(object_id) is None:
        _fail("CC000_GIT_COMMIT_ID", f"{kind} must be a full 40-character object ID")
    result = _git(repository, "cat-file", "-e", f"{object_id}^{{commit}}")
    if result.returncode:
        _fail("CC000_GIT_OBJECT_MISSING", f"{kind} does not resolve: {object_id}")


def _git_bytes(repository: Path, commit: str, path: str, context: str) -> bytes:
    result = _git(repository, "show", f"{commit}:{path}", text=False)
    if result.returncode:
        _fail("CC000_ARTIFACT_MISSING", f"{context}: {path} is absent at {commit}")
    return result.stdout


def _verify_artifact_bytes(
    artifact: Mapping[str, Any], source: bytes, context: str
) -> None:
    if artifact["byte_length"] != len(source):
        _fail(
            "CC000_ARTIFACT_LENGTH",
            f"{context}: expected {artifact['byte_length']} bytes, got {len(source)}",
        )
    actual = _digest(source)
    if artifact["sha256"] != actual:
        _fail(
            "CC000_ARTIFACT_DIGEST",
            f"{context}: expected {artifact['sha256']}, got {actual}",
        )


def _touched_paths(repository: Path, commits: Sequence[str]) -> tuple[str, ...]:
    touched: set[str] = set()
    for commit in commits:
        result = _git(
            repository,
            "diff-tree",
            "--root",
            "--no-commit-id",
            "--name-status",
            "-r",
            "-M",
            "-z",
            commit,
            text=False,
        )
        if result.returncode:
            _fail("CC000_GIT_HISTORY", f"cannot inspect commit {commit}")
        tokens = [token.decode("utf-8") for token in result.stdout.split(b"\0") if token]
        index = 0
        while index < len(tokens):
            status = tokens[index]
            index += 1
            path_count = 2 if status.startswith(("R", "C")) else 1
            if index + path_count > len(tokens):
                _fail("CC000_GIT_HISTORY", f"malformed path record in {commit}")
            for path in tokens[index : index + path_count]:
                touched.add(_safe_path(path, f"commit {commit}"))
            index += path_count
    return tuple(sorted(touched))


def _passing_evidence_report(source: bytes, context: str) -> dict[str, Any]:
    try:
        report = json.loads(
            source.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except IntegrationValidationError:
        raise
    except (UnicodeError, json.JSONDecodeError) as error:
        _fail("CC000_EVIDENCE_INVALID", f"{context}: invalid JSON evidence: {error}")
    if not isinstance(report, dict):
        _fail("CC000_EVIDENCE_INVALID", f"{context}: evidence root must be an object")
    ledger_schema = _read_json(
        Path(__file__).resolve().parents[1]
        / "design"
        / "contract_compiler"
        / "overseer"
        / "ledger.schema.json"
    )
    validator = Draft202012Validator(
        {
            "$ref": "#/$defs/verificationReport",
            "$defs": ledger_schema["$defs"],
        },
        format_checker=FormatChecker(),
    )
    errors = sorted(
        validator.iter_errors(report), key=lambda error: list(error.absolute_path)
    )
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "root"
        _fail(
            "CC000_EVIDENCE_INVALID",
            f"{context}: schema violation at {location}: {first.message}",
        )
    if any(check["result"] != "PASS" for check in report["checks"]):
        _fail("CC000_EVIDENCE_FAILED", f"{context}: evidence is not all PASS")
    return report


def validate_candidate_history(
    repository: Path,
    candidate: Mapping[str, Any],
    *,
    allowed_scopes: Sequence[Mapping[str, str]],
    workstream_id: str | None = None,
) -> tuple[str, ...]:
    """Validate exact commits and every path touched, including later deletions."""
    repository = repository.resolve()
    if candidate.get("state") not in {"ELIGIBLE", "INTEGRATED"}:
        _fail("CC000_CANDIDATE_STATE", "only ELIGIBLE or INTEGRATED can gate work")
    for scope in allowed_scopes:
        _safe_path(scope["path"], "candidate scope")
    base = candidate.get("base_commit", "")
    head = candidate.get("head_commit", "")
    _require_git_object(repository, base, "base_commit")
    _require_git_object(repository, head, "head_commit")
    ancestry = _git(repository, "merge-base", "--is-ancestor", base, head)
    if ancestry.returncode:
        _fail("CC000_GIT_ANCESTRY", f"{head} does not descend from {base}")
    history = _git(repository, "rev-list", "--reverse", "--parents", f"{base}..{head}")
    if history.returncode:
        _fail("CC000_GIT_HISTORY", f"cannot enumerate {base}..{head}")
    commits: list[str] = []
    expected_parent = base
    for line in history.stdout.splitlines():
        fields = line.split()
        if len(fields) != 2 or fields[1] != expected_parent:
            _fail("CC000_GIT_NONLINEAR", "candidate history must be one linear chain")
        commits.append(fields[0])
        expected_parent = fields[0]
    if not commits or commits[-1] != head:
        _fail("CC000_GIT_HISTORY", "candidate range contains no head commit")
    actual_tree = _git(repository, "rev-parse", f"{head}^{{tree}}")
    if actual_tree.returncode or candidate.get("head_tree") != actual_tree.stdout.strip():
        _fail("CC000_CANDIDATE_TREE", "head_tree does not bind the candidate tree")
    touched = _touched_paths(repository, commits)
    outside = [
        path
        for path in touched
        if not any(_scope_contains(scope, path) for scope in allowed_scopes)
    ]
    if outside:
        _fail(
            "CC000_SCOPE_VIOLATION",
            "candidate history touched unauthorized paths: " + ", ".join(outside),
        )
    candidate_artifacts: dict[str, Mapping[str, Any]] = {}
    for kind in ("artifacts", "evidence"):
        records = candidate.get(kind)
        if not isinstance(records, list) or not records:
            _fail("CC000_CANDIDATE", f"candidate requires nonempty {kind}")
        for record in records:
            path = _safe_path(record["path"], f"candidate {kind}")
            source = _git_bytes(repository, head, path, f"candidate {kind}")
            _verify_artifact_bytes(record, source, f"candidate {kind} {path}")
            if kind == "artifacts":
                if path in candidate_artifacts:
                    _fail("CC000_CANDIDATE", f"duplicate candidate artifact {path}")
                candidate_artifacts[path] = record
                continue
            if record.get("result") != "PASS":
                _fail("CC000_EVIDENCE_FAILED", f"{path}: gate result is not PASS")
            report = _passing_evidence_report(source, path)
            if report["base_commit"] != base:
                _fail("CC000_EVIDENCE_INVALID", f"{path}: base_commit is stale")
            if workstream_id is not None and report["workstream_id"] != workstream_id:
                _fail("CC000_EVIDENCE_INVALID", f"{path}: workstream_id is stale")
            report_artifacts = {item["path"]: item for item in report["artifacts"]}
            if (
                len(report_artifacts) != len(report["artifacts"])
                or report_artifacts != candidate_artifacts
            ):
                _fail(
                    "CC000_EVIDENCE_INVALID",
                    f"{path}: report artifacts do not equal candidate artifacts",
                )
    return touched


def worker_entry_hash(entry: Mapping[str, Any]) -> str:
    body = {key: value for key, value in entry.items() if key != "entry_hash"}
    return _digest(canonical_json(body).encode("utf-8"))


def _validate_worker_ledger(
    bundle: Path,
    card: dict[str, Any],
    schema: dict[str, Any],
) -> dict[str, dict[str, str]]:
    pointer = card["ledger"]
    if pointer["state"] == "NOT_STARTED":
        return {}
    root = _bundle_path(bundle, pointer["path"], f"{card['workstream_id']} ledger")
    head = _read_json(root / "head.json")
    _validate_schema(head, schema, "workerLedgerHead", f"{root}/head.json")
    workstream_id = card["workstream_id"]
    if head["workstream_id"] != workstream_id:
        _fail("CC000_WORKER_LEDGER", f"{workstream_id}: ledger head ID mismatch")
    paths = sorted((root / "entries").glob("*.json"))
    if len(paths) != head["entry_count"]:
        _fail("CC000_WORKER_LEDGER", f"{workstream_id}: entry count mismatch")
    previous = "GENESIS"
    prior_time: datetime | None = None
    entries: list[dict[str, Any]] = []
    entry_ids: set[str] = set()
    owner = card["assignment"].get("owner_id")
    for sequence, path in enumerate(paths, start=1):
        entry = _read_json(path)
        _validate_schema(entry, schema, "workerLedgerEntry", str(path))
        expected_id = f"{workstream_id}-WRK-{sequence:06d}"
        if path.stem != expected_id or entry["entry_id"] != expected_id:
            _fail("CC000_WORKER_LEDGER", f"{path.name}: expected {expected_id}")
        if entry["workstream_id"] != workstream_id or entry["sequence"] != sequence:
            _fail("CC000_WORKER_LEDGER", f"{path.name}: namespace or sequence mismatch")
        if owner is None or entry["actor_id"] != owner:
            _fail("CC000_WORKER_AUTHORITY", f"{path.name}: actor is not the card owner")
        if entry["previous_entry_hash"] != previous:
            _fail("CC000_WORKER_LEDGER", f"{path.name}: previous hash mismatch")
        actual_hash = worker_entry_hash(entry)
        if entry["entry_hash"] != actual_hash:
            _fail("CC000_WORKER_LEDGER", f"{path.name}: entry hash mismatch")
        recorded = datetime.fromisoformat(entry["recorded_at"].removesuffix("Z") + "+00:00")
        if prior_time is not None and recorded < prior_time:
            _fail("CC000_WORKER_LEDGER", f"{path.name}: time moved backwards")
        prior_time = recorded
        previous = actual_hash
        if entry["entry_type"] == "CORRECTION":
            target = entry["data"]["supersedes_entry_id"]
            if target not in entry_ids:
                _fail(
                    "CC000_WORKER_LEDGER",
                    f"{path.name}: correction target must be an earlier entry",
                )
        entries.append(entry)
        entry_ids.add(entry["entry_id"])
    expected_pointer = {
        "entry_count": head["entry_count"],
        "head_entry_id": head["head_entry_id"],
        "head_hash": head["head_hash"],
    }
    for key, value in expected_pointer.items():
        if pointer[key] != value:
            _fail("CC000_WORKER_LEDGER", f"{workstream_id}: card {key} is stale")
    if not paths or head["head_entry_id"] != paths[-1].stem or head["head_hash"] != previous:
        _fail("CC000_WORKER_LEDGER", f"{workstream_id}: head is stale")
    superseded: set[str] = set()
    for entry in reversed(entries):
        if entry["entry_id"] in superseded or entry["entry_type"] != "CORRECTION":
            continue
        superseded.add(entry["data"]["supersedes_entry_id"])
    phases = {
        entry["data"]["phase"]: entry["data"]
        for entry in entries
        if entry["entry_id"] not in superseded and entry["entry_type"] == "TDD_RESULT"
    }
    return phases


def _cycle(registry: Mapping[str, Sequence[str]]) -> tuple[str, ...] | None:
    visiting: list[str] = []
    visited: set[str] = set()

    def visit(node: str) -> tuple[str, ...] | None:
        if node in visiting:
            start = visiting.index(node)
            return tuple(visiting[start:] + [node])
        if node in visited:
            return None
        visiting.append(node)
        for dependency in registry[node]:
            found = visit(dependency)
            if found is not None:
                return found
        visiting.pop()
        visited.add(node)
        return None

    for node in registry:
        found = visit(node)
        if found is not None:
            return found
    return None


def _workstream_states(ledger_state: Any) -> tuple[dict[str, str], dict[str, dict[str, Any]]]:
    superseded = superseded_entries(ledger_state.entries)
    states: dict[str, str] = {}
    entries: dict[str, dict[str, Any]] = {}
    for entry in ledger_state.entries:
        if entry["entry_id"] in superseded or entry["entry_type"] != "WORKSTREAM_STATE":
            continue
        workstream_id = entry["data"]["workstream_id"]
        states[workstream_id] = entry["data"]["new_state"]
        entries[workstream_id] = entry
    return states, entries


def _verify_current_file(path: Path, record: Mapping[str, Any], context: str) -> None:
    if not path.is_file():
        _fail("CC000_ARTIFACT_MISSING", f"{context}: {path} does not exist")
    _verify_artifact_bytes(record, path.read_bytes(), context)


def validate_integration(
    repository: Path,
    manifest_path: Path | None = None,
    *,
    require_sealed: bool = False,
) -> IntegrationState:
    """Validate the complete program registry and every registered active card."""
    repository = repository.resolve()
    manifest_path = manifest_path or (
        repository / "design" / "contract_compiler" / "integration.json"
    )
    manifest_path = manifest_path.resolve()
    bundle = manifest_path.parent
    schema = _schema(repository)
    manifest = _read_json(manifest_path)
    _validate_schema(manifest, schema, "integrationManifest", str(manifest_path))
    program = load_program_registry(repository / "design" / "contract_compiler" / "program.md")

    rows = manifest["workstreams"]
    ids = [row["workstream_id"] for row in rows]
    if len(ids) != len(set(ids)):
        _fail("CC000_REGISTRY_COUNT", "workstream IDs must be unique")
    supplied = {row["workstream_id"]: tuple(row["depends_on"]) for row in rows}
    known = set(supplied)
    for workstream_id, dependencies in supplied.items():
        unknown = [dependency for dependency in dependencies if dependency not in known]
        if unknown:
            _fail(
                "CC000_DEPENDENCY_UNKNOWN",
                f"{workstream_id} names unknown dependency {unknown[0]}",
            )
        if workstream_id in dependencies:
            _fail("CC000_DEPENDENCY_SELF", f"{workstream_id} depends on itself")
    found_cycle = _cycle(supplied)
    if found_cycle is not None:
        _fail("CC000_DEPENDENCY_CYCLE", " -> ".join(found_cycle))
    if len(rows) != len(program) or set(supplied) != set(program):
        _fail(
            "CC000_REGISTRY_COUNT",
            f"manifest has {len(rows)} workstreams, approved program has {len(program)}",
        )
    for workstream_id, dependencies in supplied.items():
        if dependencies != program[workstream_id]:
            _fail(
                "CC000_REGISTRY_DRIFT",
                f"{workstream_id}: {dependencies!r} != {program[workstream_id]!r}",
            )

    owner_pairs = frozenset(
        (item["left"], item["right"]) for item in manifest["owner_separations"]
    )
    if owner_pairs != EXPECTED_OWNER_SEPARATIONS:
        _fail("CC000_OWNER_POLICY_DRIFT", "owner-separation pairs differ from the program")
    reserved = []
    for item in manifest["reserved_scopes"]:
        scope = item["scope"]
        _safe_path(scope["path"], "reserved scope")
        reserved.append(item)

    cards: dict[str, dict[str, Any]] = {}
    card_digests: dict[str, str] = {}
    for row in rows:
        reference = row["card"]
        if reference["state"] == "ABSENT":
            continue
        path = _bundle_path(bundle, reference["path"], f"{row['workstream_id']} card")
        _verify_current_file(path, reference, f"{row['workstream_id']} card")
        card = _read_json(path)
        _validate_schema(card, schema, "workstreamCard", str(path))
        workstream_id = row["workstream_id"]
        if card["workstream_id"] != workstream_id:
            _fail("CC000_CARD_ID", f"{path}: card ID does not match registry row")
        assignment = card["assignment"]
        authorization = card["authorization"]
        actor = authorization["authorized_by"]
        owner = assignment.get("owner_id")
        if actor["type"] == "WORKER" and actor["id"] == owner:
            _fail("CC000_SELF_AUTHORIZATION", f"{workstream_id}: worker authorized itself")
        if actor["type"] not in {"OPERATOR", "OVERSEER"}:
            _fail("CC000_AUTHORITY", f"{workstream_id}: authorization lacks authority")
        if assignment["state"] == "UNASSIGNED" and authorization["class"] not in {
            "PLANNING_ONLY",
            "BLOCKED",
        }:
            _fail("CC000_ASSIGNMENT", f"{workstream_id}: active authorization needs an owner")
        for scope in card["scopes"]:
            _safe_path(scope["path"], f"{workstream_id} scope")
            if owner != "overseer" and any(
                _scopes_overlap(scope, item["scope"]) for item in reserved
            ):
                _fail(
                    "CC000_SCOPE_RESERVED",
                    f"{workstream_id}: {scope['path']} is reserved to the overseer",
                )
        cards[workstream_id] = card
        card_digests[workstream_id] = reference["sha256"]

    active = {
        workstream_id: card
        for workstream_id, card in cards.items()
        if card["authorization"]["class"] in {"FORMAL", "EXPLORATION_ONLY"}
    }
    active_ids = sorted(active)
    for index, left_id in enumerate(active_ids):
        for right_id in active_ids[index + 1 :]:
            if any(
                _scopes_overlap(left, right)
                for left in active[left_id]["scopes"]
                for right in active[right_id]["scopes"]
            ):
                _fail(
                    "CC000_SCOPE_OVERLAP",
                    f"{left_id} and {right_id} hold overlapping active scopes",
                )
    for left_id, right_id in EXPECTED_OWNER_SEPARATIONS:
        if left_id not in cards or right_id not in cards:
            continue
        left_owner = cards[left_id]["assignment"].get("owner_id")
        right_owner = cards[right_id]["assignment"].get("owner_id")
        if left_owner is not None and left_owner == right_owner:
            _fail(
                "CC000_OWNER_SEPARATION",
                f"{left_id} and {right_id} must have different owners",
            )

    anchor = manifest["authority"]["overseer_ledger"]
    ledger_root = _bundle_path(repository, anchor["path"], "overseer ledger")
    ledger_state = load_ledger(ledger_root, repository=repository)
    if anchor["entry_count"] > len(ledger_state.entries):
        _fail("CC000_LEDGER_ANCHOR", "overseer checkpoint is beyond the ledger head")
    checkpoint = ledger_state.entries[anchor["entry_count"] - 1]
    expected_checkpoint = {
        "head_entry_id": checkpoint["entry_id"],
        "head_hash": checkpoint["entry_hash"],
    }
    for field, expected in expected_checkpoint.items():
        if anchor[field] != expected:
            _fail("CC000_LEDGER_ANCHOR", f"overseer checkpoint {field} is stale")
    states, state_entries = _workstream_states(ledger_state)

    phase_results: dict[str, dict[str, dict[str, str]]] = {}
    for workstream_id, card in cards.items():
        phase_results[workstream_id] = _validate_worker_ledger(bundle, card, schema)
        if card["authorization"]["class"] != "FORMAL":
            continue
        dependencies = supplied[workstream_id]
        incomplete = [dependency for dependency in dependencies if states.get(dependency) != "COMPLETE"]
        if incomplete:
            _fail(
                "CC000_DEPENDENCY_INCOMPLETE",
                f"{workstream_id} waits for: {', '.join(incomplete)}",
            )
        if states.get(workstream_id) not in {"ACTIVE", "COMPLETE"}:
            _fail("CC000_WORKSTREAM_STATE", f"{workstream_id} is not ACTIVE or COMPLETE")
        bindings = {
            binding["workstream_id"]: binding
            for binding in card["authorization"]["dependency_bindings"]
        }
        if set(bindings) != set(dependencies):
            _fail("CC000_DEPENDENCY_BINDING", f"{workstream_id}: binding set is stale")
        for dependency, binding in bindings.items():
            entry = state_entries[dependency]
            if (
                binding["completion_entry_id"] != entry["entry_id"]
                or binding["completion_entry_hash"] != entry["entry_hash"]
                or binding["card_sha256"] != card_digests.get(dependency)
            ):
                _fail("CC000_DEPENDENCY_BINDING", f"{workstream_id}: {dependency} binding is stale")

    snapshot = manifest["authority"]["snapshot"]
    if require_sealed and snapshot["state"] != "SEALED":
        _fail("CC000_UNSEALED", "integration manifest has no result-commit seal")
    if snapshot["state"] == "SEALED":
        result_commit = snapshot["result_commit"]
        _require_git_object(repository, result_commit, "result_commit")
        for artifact in snapshot["artifacts"]:
            path = _safe_path(artifact["path"], "authority snapshot")
            source = _git_bytes(repository, result_commit, path, "authority snapshot")
            _verify_artifact_bytes(artifact, source, f"authority snapshot {path}")

    selections = tuple(manifest["selections"])
    for workstream_id in selections:
        if workstream_id not in cards:
            _fail("CC000_SELECTION", f"{workstream_id} has no registered card")
        card = cards[workstream_id]
        if card["authorization"]["class"] != "FORMAL":
            _fail(
                "CC000_SELECTION_AUTHORIZATION",
                f"{workstream_id}: only FORMAL work may be selected",
            )
        if states.get(workstream_id) != "COMPLETE":
            _fail(
                "CC000_SELECTION_STATE",
                f"{workstream_id}: only a COMPLETE workstream may be selected",
            )
        if card["candidate"]["state"] != "INTEGRATED":
            _fail("CC000_CANDIDATE_STATE", f"{workstream_id} is not INTEGRATED")
        validate_candidate_history(
            repository,
            card["candidate"],
            allowed_scopes=tuple(card["scopes"]),
            workstream_id=workstream_id,
        )
        phases = phase_results[workstream_id]
        missing = [phase for phase in TDD_PHASES if phase not in phases]
        failed = [
            phase
            for phase, data in phases.items()
            if data["result"] not in {"PASS", "EXPECTED_FAILURE", "NOT_APPLICABLE"}
            or (phase == "RED" and data["result"] != "EXPECTED_FAILURE")
            or (phase not in {"RED", "PACKAGE"} and data["result"] != "PASS")
        ]
        if missing or failed:
            _fail(
                "CC000_TDD_INCOMPLETE",
                f"{workstream_id}: missing {missing}, failed {failed}",
            )
    return IntegrationState(
        manifest=manifest,
        workstreams=supplied,
        cards=cards,
        selections=selections,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "check-draft"))
    parser.add_argument("manifest", nargs="?", type=Path)
    arguments = parser.parse_args(argv)
    repository = Path(__file__).resolve().parents[1]
    state = validate_integration(
        repository,
        arguments.manifest,
        require_sealed=arguments.command == "check",
    )
    print(
        f"validated {len(state.workstreams)} workstreams, "
        f"{len(state.cards)} cards, {len(state.selections)} selections"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

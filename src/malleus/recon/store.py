"""Typed, replayable storage for bounded literature reviews."""

from __future__ import annotations

import json
import os
import re
import tempfile
from copy import deepcopy
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping
from urllib.parse import urlparse

from malleus.kg import KnowledgeGraph, OpStatus
from malleus.ledger import JsonlLedger, LedgerError, canonical_json, record_hash
from malleus.ontology import OntologyRegistry, bundled_ontology_path


PROJECT_FILE = "project.json"
LEDGER_FILE = "ledger.jsonl"
BUILD_DIRECTORY = "build"
PROJECT_SCHEMA_VERSION = "1"
RECORD_EVENT = "RECON_RECORD"
RECORDED = "RECORDED"
REJECTED = "REJECTED"
_PAYLOAD_FIELDS = {
    "decision",
    "record_type",
    "record",
    "candidate_hash",
    "supersedes_event_id",
    "errors",
}
_PROJECT_FIELDS = {
    "schema_version",
    "title",
    "target_id",
    "created_at",
    "creator_id",
    "ontology_hash",
}
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_EVIDENCE_REQUIRED = frozenset({"Work", "Claim", "Result"})


class ReconError(ValueError):
    """The Recon project or candidate cannot be interpreted safely."""


@dataclass(frozen=True)
class StoredRecord:
    """The latest recorded value for one stable record identifier."""

    record_type: str
    record: dict[str, Any]
    event_id: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _nonblank(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReconError(f"{label} must be a nonblank string")
    return value


def _exact_fields(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing:
        raise ReconError(f"{label} missing required fields: {', '.join(missing)}")
    if unknown:
        raise ReconError(f"{label} has unknown fields: {', '.join(unknown)}")


def _atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        stream = os.fdopen(descriptor, "wb", closefd=True)
        descriptor = -1
        with stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        Path(temporary_name).replace(path)
        temporary_name = ""
    except OSError as error:
        raise ReconError(f"Could not write {path} without partial replacement: {error}") from error
    finally:
        if descriptor >= 0:
            try:
                os.close(descriptor)
            except OSError:
                pass
        if temporary_name:
            Path(temporary_name).unlink(missing_ok=True)


class ReconProject:
    """One local Recon project backed by the shared Malleus JSONL ledger."""

    def __init__(
        self,
        root: str | Path,
        *,
        clock: Callable[[], str] | None = None,
    ):
        self.root = Path(root)
        self._clock = clock or _utc_now
        self.registry = OntologyRegistry(bundled_ontology_path("domains", "recon.yaml"))
        self.ontology_hash = f"sha256:{self.registry.content_hash()}"
        self.config = self._read_config()
        self.ledger = JsonlLedger(self.root / LEDGER_FILE, self.ontology_hash)

    @classmethod
    def initialize(
        cls,
        root: str | Path,
        *,
        title: str,
        target_id: str,
        creator_id: str,
        clock: Callable[[], str] | None = None,
    ) -> "ReconProject":
        destination = Path(root)
        title = _nonblank(title, "title")
        target_id = _nonblank(target_id, "target_id")
        creator_id = _nonblank(creator_id, "creator_id")
        if destination.exists() and not destination.is_dir():
            raise ReconError(f"Recon project path is not a directory: {destination}")
        if destination.exists() and any(destination.iterdir()):
            raise ReconError(f"Recon project directory is not empty: {destination}")
        destination.mkdir(parents=True, exist_ok=True)
        registry = OntologyRegistry(bundled_ontology_path("domains", "recon.yaml"))
        now = (clock or _utc_now)()
        try:
            parsed = datetime.fromisoformat(now.replace("Z", "+00:00"))
        except (AttributeError, ValueError) as error:
            raise ReconError("Project clock must return an ISO 8601 datetime") from error
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ReconError("Project clock must include a timezone offset")
        config = {
            "schema_version": PROJECT_SCHEMA_VERSION,
            "title": title,
            "target_id": target_id,
            "created_at": now,
            "creator_id": creator_id,
            "ontology_hash": f"sha256:{registry.content_hash()}",
        }
        _atomic_json(destination / PROJECT_FILE, config)
        return cls(destination, clock=clock)

    def _read_config(self) -> dict[str, Any]:
        path = self.root / PROJECT_FILE
        if not path.is_file():
            raise ReconError(f"Recon project is missing {PROJECT_FILE}: {self.root}")
        try:
            value = json.loads(
                path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ReconError(f"Cannot read {path}: {error}") from error
        if not isinstance(value, dict):
            raise ReconError(f"{path} must contain one JSON object")
        _exact_fields(value, _PROJECT_FIELDS, PROJECT_FILE)
        if value["schema_version"] != PROJECT_SCHEMA_VERSION:
            raise ReconError(
                f"Unsupported Recon project schema_version: {value['schema_version']}"
            )
        for field in ("title", "target_id", "creator_id"):
            _nonblank(value[field], f"{PROJECT_FILE} {field}")
        try:
            created_at = datetime.fromisoformat(value["created_at"].replace("Z", "+00:00"))
        except (AttributeError, ValueError) as error:
            raise ReconError(f"{PROJECT_FILE} created_at must be an ISO 8601 datetime") from error
        if created_at.tzinfo is None or created_at.utcoffset() is None:
            raise ReconError(f"{PROJECT_FILE} created_at must include a timezone offset")
        if not isinstance(value["ontology_hash"], str) or _DIGEST.fullmatch(
            value["ontology_hash"]
        ) is None:
            raise ReconError(f"{PROJECT_FILE} ontology_hash must be sha256:<64 hex>")
        if value["ontology_hash"] != self.ontology_hash:
            raise ReconError(
                "Recon ontology hash differs from this project; run an explicit migration "
                "instead of replaying under changed types"
            )
        return value

    def events(self) -> list[dict[str, Any]]:
        events = self.ledger.read()
        self._replay(events)
        return events

    def current_records(self) -> dict[str, StoredRecord]:
        return self._replay(self.ledger.read())

    def record(
        self,
        record_type: str,
        record: Mapping[str, Any],
        *,
        actor_id: str,
        supersedes_event_id: str | None = None,
    ) -> dict[str, Any]:
        _nonblank(record_type, "record_type")
        _nonblank(actor_id, "actor_id")
        if supersedes_event_id is not None:
            _nonblank(supersedes_event_id, "supersedes_event_id")
        if not isinstance(record, Mapping):
            raise ReconError("record must be a JSON object")
        candidate = deepcopy(dict(record))
        try:
            candidate_hash = record_hash(record_type, candidate)
        except LedgerError as error:
            raise ReconError(f"record cannot be represented as canonical JSON: {error}") from error
        events = self.ledger.read()
        state = self._replay(events)
        latest = {identifier: item.event_id for identifier, item in state.items()}
        errors = self._candidate_errors(
            state,
            latest,
            record_type,
            candidate,
            supersedes_event_id,
        )
        payload = {
            "decision": RECORDED if not errors else REJECTED,
            "record_type": record_type,
            "record": candidate,
            "candidate_hash": candidate_hash,
            "supersedes_event_id": supersedes_event_id,
            "errors": errors,
        }
        event = self.ledger.append(
            event_id=f"recon-event:{len(events) + 1:06d}",
            event_type=RECORD_EVENT,
            transaction_time=self._clock(),
            actor_id=actor_id,
            payload=payload,
            validate=self._validate_history,
        )
        return event

    def validate(self) -> list[str]:
        state = self.current_records()
        errors = []
        target = state.get(self.config["target_id"])
        if target is None:
            errors.append(
                f"Project target '{self.config['target_id']}' has not been recorded"
            )
        elif target.record_type != "ReviewTarget":
            errors.append(
                f"Project target '{self.config['target_id']}' is {target.record_type}, "
                "expected ReviewTarget"
            )
        return errors

    def _validate_history(self, events: list[dict[str, Any]]) -> None:
        self._replay(events)

    def _replay(self, events: list[dict[str, Any]]) -> dict[str, StoredRecord]:
        state: dict[str, StoredRecord] = {}
        latest: dict[str, str] = {}
        for position, event in enumerate(events, start=1):
            if event["event_type"] != RECORD_EVENT:
                raise ReconError(
                    f"event {position} has unsupported event_type '{event['event_type']}'"
                )
            payload = event["payload"]
            if not isinstance(payload, dict):
                raise ReconError(f"event {position} payload must be an object")
            _exact_fields(payload, _PAYLOAD_FIELDS, f"event {position} payload")
            record_type = _nonblank(payload["record_type"], f"event {position} record_type")
            record = payload["record"]
            if not isinstance(record, dict):
                raise ReconError(f"event {position} record must be an object")
            try:
                expected_hash = record_hash(record_type, record)
            except LedgerError as error:
                raise ReconError(f"event {position} record is not canonical: {error}") from error
            if payload["candidate_hash"] != expected_hash:
                raise ReconError(f"event {position} candidate_hash mismatch")
            supplied_errors = payload["errors"]
            if not isinstance(supplied_errors, list) or any(
                not isinstance(error, str) for error in supplied_errors
            ):
                raise ReconError(f"event {position} errors must be a list of strings")
            supersedes = payload["supersedes_event_id"]
            if supersedes is not None and (
                not isinstance(supersedes, str) or not supersedes.strip()
            ):
                raise ReconError(
                    f"event {position} supersedes_event_id must be null or a nonblank string"
                )
            errors = self._candidate_errors(
                state,
                latest,
                record_type,
                record,
                supersedes,
            )
            expected_decision = RECORDED if not errors else REJECTED
            if payload["decision"] != expected_decision:
                raise ReconError(
                    f"event {position} decision is {payload['decision']}, "
                    f"replay requires {expected_decision}"
                )
            if supplied_errors != errors:
                raise ReconError(f"event {position} validation errors do not replay exactly")
            if not errors:
                identifier = record["id"]
                state[identifier] = StoredRecord(
                    record_type=record_type,
                    record=deepcopy(record),
                    event_id=event["event_id"],
                )
                latest[identifier] = event["event_id"]
        return state

    def _candidate_errors(
        self,
        state: Mapping[str, StoredRecord],
        latest: Mapping[str, str],
        record_type: str,
        record: Mapping[str, Any],
        supersedes_event_id: str | None,
    ) -> list[str]:
        errors = []
        if not self.registry.has_type(record_type):
            return [f"Unknown Recon record type: '{record_type}'"]
        if self.registry.get_type(record_type).abstract:
            return [f"Recon record type '{record_type}' is abstract"]
        identifier = record.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            return ["Record requires a nonblank string id"]
        existing = state.get(identifier)
        if existing is None:
            if supersedes_event_id is not None:
                errors.append(
                    f"Record '{identifier}' is new and cannot supersede event "
                    f"'{supersedes_event_id}'"
                )
        else:
            if existing.record_type != record_type:
                errors.append(
                    f"Record '{identifier}' is already typed {existing.record_type}, "
                    f"not {record_type}"
                )
            expected = latest[identifier]
            if supersedes_event_id != expected:
                errors.append(
                    f"Revision of '{identifier}' must supersede latest event '{expected}'"
                )
        if errors:
            return errors
        candidate = dict(state)
        candidate[identifier] = StoredRecord(record_type, deepcopy(dict(record)), "candidate")
        errors = self._state_errors(candidate)
        if record_type == "CoversAxisRelation":
            profile = (record.get("source_id"), record.get("target_id"))
            for existing_id, existing_record in sorted(state.items()):
                if existing_id == identifier or existing_record.record_type != record_type:
                    continue
                existing_profile = (
                    existing_record.record.get("source_id"),
                    existing_record.record.get("target_id"),
                )
                if profile == existing_profile:
                    errors.append(
                        f"CoversAxisRelation '{identifier}' duplicates subject-axis profile "
                        f"already recorded by '{existing_id}'"
                    )
                    break
        return errors

    def _state_errors(self, state: Mapping[str, StoredRecord]) -> list[str]:
        errors, _ = self._materialize(state)
        errors.extend(self._semantic_errors(state))
        return errors

    def _materialize(
        self,
        state: Mapping[str, StoredRecord],
    ) -> tuple[list[str], KnowledgeGraph]:
        graph = KnowledgeGraph(self.registry)
        errors = []
        categories = ("Entity", "Relation", "Event")
        for category in categories:
            for identifier, stored in sorted(state.items()):
                record_type = stored.record_type
                if not self.registry.is_subtype_of(record_type, category):
                    continue
                record = stored.record
                properties = {
                    key: deepcopy(value)
                    for key, value in record.items()
                    if key not in {"id", "source_id", "target_id"}
                }
                if category == "Entity":
                    operation = graph.create_entity(record_type, identifier, properties)
                elif category == "Relation":
                    operation = graph.create_relation(
                        record_type,
                        identifier,
                        record.get("source_id"),
                        record.get("target_id"),
                        properties,
                    )
                else:
                    operation = graph.create_event(record_type, identifier, properties)
                if operation.op_status == OpStatus.REJECTED:
                    errors.append(
                        f"{record_type} '{identifier}': {operation.rejection_reason}"
                    )
        recognized = {
            identifier
            for identifier, stored in state.items()
            if any(self.registry.is_subtype_of(stored.record_type, root) for root in categories)
        }
        for identifier in sorted(set(state) - recognized):
            errors.append(
                f"{state[identifier].record_type} '{identifier}' is not an Entity, Relation, or Event"
            )
        return errors, graph

    def _semantic_errors(self, state: Mapping[str, StoredRecord]) -> list[str]:
        errors = []
        for identifier, stored in sorted(state.items()):
            record = stored.record
            evidence_ids = record.get("evidence_ids", [])
            if isinstance(evidence_ids, list):
                for evidence_id in evidence_ids:
                    evidence = state.get(evidence_id)
                    if evidence is None:
                        errors.append(
                            f"{stored.record_type} '{identifier}' references missing evidence "
                            f"'{evidence_id}'"
                        )
                    elif evidence.record_type != "EvidenceAttachment":
                        errors.append(
                            f"{stored.record_type} '{identifier}' evidence '{evidence_id}' is "
                            f"{evidence.record_type}, expected EvidenceAttachment"
                        )
                    elif evidence.record.get("review_state") == "RETIRED":
                        errors.append(
                            f"{stored.record_type} '{identifier}' references retired evidence "
                            f"'{evidence_id}'"
                        )
            if (
                stored.record_type in _EVIDENCE_REQUIRED
                and record.get("review_state") in {"REVIEWED", "CONTESTED"}
                and not evidence_ids
            ):
                errors.append(
                    f"Reviewed {stored.record_type} '{identifier}' requires evidence_ids"
                )
            if stored.record_type == "EvidenceAttachment":
                errors.extend(self._evidence_errors(identifier, record))
            for field in ("priority_date", "cutoff_date", "accessed_on"):
                if field in record:
                    try:
                        date.fromisoformat(record[field])
                    except (TypeError, ValueError):
                        errors.append(
                            f"{stored.record_type} '{identifier}' {field} must be YYYY-MM-DD"
                        )

        return errors

    @staticmethod
    def _evidence_errors(identifier: str, record: Mapping[str, Any]) -> list[str]:
        errors = []
        source_uri = record.get("source_uri")
        local_path = record.get("local_path")
        usable_uri = isinstance(source_uri, str) and bool(source_uri.strip())
        usable_path = isinstance(local_path, str) and bool(local_path.strip())
        if not usable_uri and not usable_path:
            errors.append(
                f"EvidenceAttachment '{identifier}' requires source_uri or local_path"
            )
        if source_uri is not None and not usable_uri:
            errors.append(
                f"EvidenceAttachment '{identifier}' source_uri must be a nonblank string"
            )
        if local_path is not None and not usable_path:
            errors.append(
                f"EvidenceAttachment '{identifier}' local_path must be a nonblank string"
            )
        if usable_uri:
            parsed = urlparse(source_uri) if isinstance(source_uri, str) else None
            if parsed is None or not parsed.scheme:
                errors.append(
                    f"EvidenceAttachment '{identifier}' source_uri requires a URI scheme"
                )
        digest = record.get("artifact_sha256")
        length = record.get("artifact_byte_length")
        if (digest is None) != (length is None):
            errors.append(
                f"EvidenceAttachment '{identifier}' artifact_sha256 and "
                "artifact_byte_length must be supplied together"
            )
        if digest is not None and (
            not isinstance(digest, str) or _DIGEST.fullmatch(digest) is None
        ):
            errors.append(
                f"EvidenceAttachment '{identifier}' artifact_sha256 must be sha256:<64 hex>"
            )
        return errors


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ReconError(f"duplicate JSON key '{key}'")
        result[key] = value
    return result


def load_record_file(path: str | Path) -> dict[str, Any]:
    """Load one JSON object while refusing duplicate object keys."""

    source = Path(path)
    try:
        value = json.loads(source.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReconError(f"Cannot read record file {source}: {error}") from error
    if not isinstance(value, dict):
        raise ReconError(f"Record file {source} must contain one JSON object")
    try:
        canonical_json(value)
    except LedgerError as error:
        raise ReconError(f"Record file {source} is not canonical JSON: {error}") from error
    return value

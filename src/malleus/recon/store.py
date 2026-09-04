"""Typed, replayable storage for bounded literature reviews."""

from __future__ import annotations

import errno
import json
import os
import re
import stat
import tempfile
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping
from urllib.parse import urlparse

from malleus.kg import KnowledgeGraph, OpStatus
from malleus.ledger import LedgerError, canonical_json, record_hash
from malleus.migration import (
    MigrationAwareJsonlLedger,
    MigrationError,
    MigrationVerification,
    MigrationVerifier,
    migration_chain,
)
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
_WRITER_LOCK_FILE = ".recon-writer.lock"
_LOCK_CONTENTION_ERRNOS = frozenset({errno.EACCES, errno.EAGAIN, errno.EWOULDBLOCK})
_LOCK_CONTENTION_WINERRORS = frozenset({33})


class ReconError(ValueError):
    """The Recon project or candidate cannot be interpreted safely."""


@dataclass(frozen=True)
class StoredRecord:
    """The latest recorded value for one stable record identifier."""

    record_type: str
    record: dict[str, Any]
    event_id: str


@dataclass(frozen=True)
class RecordCandidate:
    """One typed candidate for an atomic Recon ledger batch."""

    record_type: str
    record: Mapping[str, Any]
    supersedes_event_id: str | None = None


@dataclass
class _ReplayIndex:
    """Current replay state plus reverse indexes for affected-record checks."""

    registry: OntologyRegistry
    records: dict[str, StoredRecord]
    latest: dict[str, str]
    relations_by_endpoint: dict[str, set[str]]
    records_by_evidence: dict[str, set[str]]
    coverage_profiles: dict[tuple[str, str], set[str]]

    @classmethod
    def from_records(
        cls,
        registry: OntologyRegistry,
        records: Mapping[str, StoredRecord],
    ) -> "_ReplayIndex":
        index = cls(registry, {}, {}, {}, {}, {})
        for stored in records.values():
            index.replace(stored)
        return index

    def replace(self, stored: StoredRecord) -> None:
        identifier = stored.record["id"]
        previous = self.records.get(identifier)
        if previous is not None:
            self._remove(previous)
        self.records[identifier] = stored
        self.latest[identifier] = stored.event_id
        self._add(stored)

    def _add(self, stored: StoredRecord) -> None:
        identifier = stored.record["id"]
        evidence_ids = stored.record.get("evidence_ids", [])
        if isinstance(evidence_ids, list):
            for evidence_id in evidence_ids:
                if isinstance(evidence_id, str):
                    self.records_by_evidence.setdefault(evidence_id, set()).add(identifier)
        if self.registry.is_subtype_of(stored.record_type, "Relation"):
            for endpoint in (stored.record.get("source_id"), stored.record.get("target_id")):
                if isinstance(endpoint, str):
                    self.relations_by_endpoint.setdefault(endpoint, set()).add(identifier)
        if stored.record_type == "CoversAxisRelation":
            source = stored.record.get("source_id")
            target = stored.record.get("target_id")
            if isinstance(source, str) and isinstance(target, str):
                self.coverage_profiles.setdefault((source, target), set()).add(identifier)

    def _remove(self, stored: StoredRecord) -> None:
        identifier = stored.record["id"]
        evidence_ids = stored.record.get("evidence_ids", [])
        if isinstance(evidence_ids, list):
            for evidence_id in evidence_ids:
                if isinstance(evidence_id, str):
                    self._discard(self.records_by_evidence, evidence_id, identifier)
        if self.registry.is_subtype_of(stored.record_type, "Relation"):
            for endpoint in (stored.record.get("source_id"), stored.record.get("target_id")):
                if isinstance(endpoint, str):
                    self._discard(self.relations_by_endpoint, endpoint, identifier)
        if stored.record_type == "CoversAxisRelation":
            source = stored.record.get("source_id")
            target = stored.record.get("target_id")
            if isinstance(source, str) and isinstance(target, str):
                self._discard(self.coverage_profiles, (source, target), identifier)

    @staticmethod
    def _discard(index: dict[Any, set[str]], key: Any, identifier: str) -> None:
        identifiers = index.get(key)
        if identifiers is None:
            return
        identifiers.discard(identifier)
        if not identifiers:
            del index[key]


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
    try:
        encoded = (
            json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ReconError(f"Could not encode {path} as canonical UTF-8 JSON: {error}") from error
    descriptor = -1
    temporary_name = ""
    replace_started = False
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
        )
        stream = os.fdopen(descriptor, "wb", closefd=True)
        descriptor = -1
        with stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        replace_started = True
        Path(temporary_name).replace(path)
        temporary_name = ""
        replace_started = False
    except BaseException as error:
        if replace_started:
            rollback_error = None
            try:
                path.unlink(missing_ok=True)
            except BaseException as failure:
                rollback_error = failure
            if rollback_error is not None:
                try:
                    marker_remains = path.exists()
                except OSError:
                    marker_remains = True
                if marker_remains:
                    raise ReconError(
                        f"Project initialization outcome is indeterminate: {path} remains "
                        "after replacement and rollback both failed"
                    ) from error
        if isinstance(error, OSError):
            raise ReconError(
                f"Could not write {path} without partial replacement: {error}"
            ) from error
        raise
    finally:
        if descriptor >= 0:
            try:
                os.close(descriptor)
            except BaseException:
                pass
        if temporary_name:
            try:
                Path(temporary_name).unlink(missing_ok=True)
            except BaseException:
                pass


def _acquire_writer_lock(stream: Any) -> None:
    if os.name == "nt":
        import msvcrt

        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b"\0")
            stream.flush()
        stream.seek(0)
        msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        return

    import fcntl

    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)


def _release_writer_lock(stream: Any) -> None:
    if os.name == "nt":
        import msvcrt

        stream.seek(0)
        msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        return

    import fcntl

    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _is_lock_contention(error: OSError) -> bool:
    return error.errno in _LOCK_CONTENTION_ERRNOS or getattr(
        error, "winerror", None
    ) in _LOCK_CONTENTION_WINERRORS


def _precheck_reserved_lock(path: Path, subject: str) -> None:
    try:
        status = path.lstat()
    except FileNotFoundError:
        return
    except OSError as error:
        raise ReconError(f"Could not inspect {subject} {path}: {error}") from error
    if not stat.S_ISREG(status.st_mode) or status.st_nlink != 1:
        raise ReconError(
            f"Reserved {subject} must be a single-link regular file: {path}"
        )


def _assert_reserved_lock_identity(path: Path, descriptor: int, subject: str) -> None:
    try:
        path_status = path.lstat()
        descriptor_status = os.fstat(descriptor)
    except OSError as error:
        raise ReconError(f"Could not verify {subject} {path}: {error}") from error
    if (
        not stat.S_ISREG(path_status.st_mode)
        or not stat.S_ISREG(descriptor_status.st_mode)
        or path_status.st_nlink != 1
        or descriptor_status.st_nlink != 1
        or not os.path.samestat(path_status, descriptor_status)
    ):
        raise ReconError(
            f"Reserved {subject} changed identity, has aliases, or is not a "
            f"regular file: {path}"
        )


@contextmanager
def _exclusive_writer(path: Path) -> Iterator[None]:
    """Fail closed when another cooperating ReconProject writer is active."""

    _precheck_reserved_lock(path, "Recon writer lock")
    try:
        descriptor = os.open(
            path,
            os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
    except OSError as error:
        raise ReconError(f"Could not open Recon writer lock {path}: {error}") from error
    try:
        # The context owns the raw descriptor. Keeping it separate from the
        # stream makes cleanup exact even when stream.close() raises after
        # closing its own wrapper state.
        stream = os.fdopen(descriptor, "r+b", closefd=False)
    except OSError as error:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise ReconError(
            f"Could not initialize Recon writer lock {path}: {error}"
        ) from error
    try:
        _assert_reserved_lock_identity(path, descriptor, "Recon writer lock")
    except BaseException:
        try:
            stream.close()
        except BaseException:
            pass
        try:
            os.close(descriptor)
        except BaseException:
            pass
        raise

    acquired = False
    body_failed = False
    try:
        try:
            _acquire_writer_lock(stream)
            acquired = True
        except OSError as error:
            if _is_lock_contention(error):
                raise ReconError(
                    f"Recon project already has an active writer: {path.parent}"
                ) from error
            raise ReconError(
                f"Could not acquire Recon writer lock {path}: {error}"
            ) from error
        _assert_reserved_lock_identity(path, descriptor, "Recon writer lock")
        yield
    except BaseException:
        body_failed = True
        raise
    finally:
        cleanup_interrupt = None
        if acquired:
            try:
                _release_writer_lock(stream)
            except Exception:
                # Closing the descriptor releases the process lock as the
                # final guard even if an explicit unlock is interrupted.
                pass
            except BaseException as error:
                cleanup_interrupt = error
        try:
            stream.close()
        except Exception:
            pass
        except BaseException as error:
            if cleanup_interrupt is None:
                cleanup_interrupt = error
        try:
            os.close(descriptor)
        except Exception:
            pass
        except BaseException as error:
            if cleanup_interrupt is None:
                cleanup_interrupt = error
        if not body_failed and cleanup_interrupt is not None:
            raise cleanup_interrupt


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
        self._configure_registry(
            OntologyRegistry(bundled_ontology_path("domains", "recon.yaml"))
        )
        self.config = self._read_config()
        self._configure_ledger()

    def _configure_registry(self, registry: OntologyRegistry) -> None:
        self.registry = registry
        self.ontology_hash = f"sha256:{self.registry.content_hash()}"
        self.migrations = migration_chain(self.registry)
        self.migration_verifier = MigrationVerifier(self.registry, self.migrations)
        # Compatibility surface for callers that inspect grammar history. It
        # contains only alternate hashes of the current bytes. Migration
        # identities are deliberately absent and require the verifier above.
        self.historical_ontology_hashes = tuple(
            identity
            for identity in self.migration_verifier.grammar_ontology_hashes
            if identity != self.ontology_hash
        )

    def _configure_ledger(self) -> None:
        self._ledger = MigrationAwareJsonlLedger(
            self.root / LEDGER_FILE,
            self.migration_verifier,
        )

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
        destination.mkdir(parents=True, exist_ok=True)
        registry = OntologyRegistry(bundled_ontology_path("domains", "recon.yaml"))
        with _exclusive_writer(destination / _WRITER_LOCK_FILE):
            existing = [
                path for path in destination.iterdir() if path.name != _WRITER_LOCK_FILE
            ]
            if existing:
                raise ReconError(f"Recon project directory is not empty: {destination}")
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
            project = cls.__new__(cls)
            project.root = destination
            project._clock = clock or _utc_now
            project._configure_registry(registry)
            project.config = config
            project._configure_ledger()
            _atomic_json(destination / PROJECT_FILE, config)
            return project

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
        try:
            self.migration_verifier.verify((value["ontology_hash"],))
        except MigrationError as error:
            raise ReconError(
                f"Recon ontology hash cannot be replayed by this project: {error}"
            ) from error
        return value

    def events(self) -> list[dict[str, Any]]:
        return self.snapshot()[0]

    def current_records(self) -> dict[str, StoredRecord]:
        return self.snapshot()[1]

    def snapshot(self) -> tuple[list[dict[str, Any]], dict[str, StoredRecord]]:
        """Read and verify one ledger snapshot for a complete derived build."""
        events, records, _verification = self.snapshot_verified()
        return events, records

    def snapshot_verified(
        self,
    ) -> tuple[
        list[dict[str, Any]],
        dict[str, StoredRecord],
        MigrationVerification,
    ]:
        """Read one snapshot with exact grammar and migration evidence."""
        events, verification = self._ledger.read_verified(
            additional_ontology_hashes=(self.config["ontology_hash"],)
        )
        return events, self._replay(events), verification

    def record(
        self,
        record_type: str,
        record: Mapping[str, Any],
        *,
        actor_id: str,
        supersedes_event_id: str | None = None,
    ) -> dict[str, Any]:
        return self.record_many(
            [RecordCandidate(record_type, record, supersedes_event_id)],
            actor_id=actor_id,
        )[0]

    def record_many(
        self,
        candidates: list[RecordCandidate],
        *,
        actor_id: str,
        require_all_recorded: bool = False,
    ) -> tuple[dict[str, Any], ...]:
        """Record one failure-atomic batch, optionally refusing any rejection."""

        _nonblank(actor_id, "actor_id")
        if not isinstance(candidates, list) or not candidates:
            raise ReconError("record batch must be a nonempty list")
        with _exclusive_writer(self.root / _WRITER_LOCK_FILE):
            if require_all_recorded:
                return self._record_required_batch(candidates, actor_id=actor_id)
            return self._record_decision_batch(candidates, actor_id=actor_id)

    def _record_decision_batch(
        self,
        candidates: list[RecordCandidate],
        *,
        actor_id: str,
    ) -> tuple[dict[str, Any], ...]:
        events = self._ledger.read()
        original_state = self._replay(events)
        index = _ReplayIndex.from_records(self.registry, original_state)
        transaction_time = self._clock()
        entries = []
        for offset, item in enumerate(candidates, start=1):
            record_type, candidate, candidate_hash = self._prepare_candidate(item, offset)
            errors = self._candidate_errors(
                index,
                record_type,
                candidate,
                item.supersedes_event_id,
            )
            event_id = f"recon-event:{len(events) + offset:06d}"
            payload = {
                "decision": RECORDED if not errors else REJECTED,
                "record_type": record_type,
                "record": candidate,
                "candidate_hash": candidate_hash,
                "supersedes_event_id": item.supersedes_event_id,
                "errors": errors,
            }
            entries.append(
                {
                    "event_id": event_id,
                    "event_type": RECORD_EVENT,
                    "transaction_time": transaction_time,
                    "actor_id": actor_id,
                    "payload": payload,
                }
            )
            if not errors:
                index.replace(StoredRecord(record_type, candidate, event_id))

        def validate_suffix(candidate_events: list[dict[str, Any]]) -> None:
            self._validate_decision_suffix(
                candidate_events,
                prefix=events,
                original_state=original_state,
                suffix_length=len(entries),
            )

        return self._ledger.append_many(
            entries,
            validate=validate_suffix,
        )

    def _prepare_candidate(
        self,
        item: RecordCandidate,
        offset: int,
    ) -> tuple[str, dict[str, Any], str]:
        if not isinstance(item, RecordCandidate):
            raise ReconError(f"record batch item {offset} must be a RecordCandidate")
        record_type = _nonblank(item.record_type, f"record batch item {offset} type")
        if item.supersedes_event_id is not None:
            _nonblank(
                item.supersedes_event_id,
                f"record batch item {offset} supersedes_event_id",
            )
        if not isinstance(item.record, Mapping):
            raise ReconError(f"record batch item {offset} record must be a JSON object")
        candidate = deepcopy(dict(item.record))
        try:
            candidate_hash = record_hash(record_type, candidate)
        except LedgerError as error:
            raise ReconError(
                f"record batch item {offset} is not canonical JSON: {error}"
            ) from error
        return record_type, candidate, candidate_hash

    def _record_required_batch(
        self,
        candidates: list[RecordCandidate],
        *,
        actor_id: str,
    ) -> tuple[dict[str, Any], ...]:
        events = self._ledger.read()
        original_state = self._replay(events)
        original_latest = {
            identifier: item.event_id for identifier, item in original_state.items()
        }
        state = dict(original_state)
        latest = dict(original_latest)
        transaction_time = self._clock()
        entries = []
        for offset, item in enumerate(candidates, start=1):
            record_type, candidate, candidate_hash = self._prepare_candidate(item, offset)
            errors = self._identity_errors(
                state,
                latest,
                record_type,
                candidate,
                item.supersedes_event_id,
            )
            if errors:
                raise ReconError(
                    f"record batch item {offset} would be rejected: {'; '.join(errors)}"
                )
            event_id = f"recon-event:{len(events) + offset:06d}"
            entries.append(
                {
                    "event_id": event_id,
                    "event_type": RECORD_EVENT,
                    "transaction_time": transaction_time,
                    "actor_id": actor_id,
                    "payload": {
                        "decision": RECORDED,
                        "record_type": record_type,
                        "record": candidate,
                        "candidate_hash": candidate_hash,
                        "supersedes_event_id": item.supersedes_event_id,
                        "errors": [],
                    },
                }
            )
            identifier = candidate["id"]
            state[identifier] = StoredRecord(record_type, candidate, event_id)
            latest[identifier] = event_id
        final_errors = [*self._state_errors(state), *self._duplicate_profile_errors(state)]
        if final_errors:
            raise ReconError(
                "record batch final state is invalid: " + "; ".join(final_errors)
            )
        replay_index = _ReplayIndex.from_records(self.registry, original_state)
        for offset, entry in enumerate(entries, start=1):
            payload = entry["payload"]
            replay_errors = self._candidate_errors(
                replay_index,
                payload["record_type"],
                payload["record"],
                payload["supersedes_event_id"],
            )
            if replay_errors:
                raise ReconError(
                    f"record batch item {offset} is not replay-valid in caller order: "
                    + "; ".join(replay_errors)
                )
            replay_index.replace(
                StoredRecord(
                    payload["record_type"],
                    payload["record"],
                    entry["event_id"],
                )
            )

        def validate_suffix(candidate_events: list[dict[str, Any]]) -> None:
            self._validate_required_suffix(
                candidate_events,
                prefix=events,
                original_state=original_state,
                suffix_length=len(entries),
            )

        return self._ledger.append_many(entries, validate=validate_suffix)

    def validate(
        self,
        state: Mapping[str, StoredRecord] | None = None,
    ) -> list[str]:
        state = self.current_records() if state is None else state
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

    def _replay(self, events: list[dict[str, Any]]) -> dict[str, StoredRecord]:
        index = _ReplayIndex.from_records(self.registry, {})
        for position, event in enumerate(events, start=1):
            payload, record_type, record, supersedes = self._event_payload(
                event, position
            )
            supplied_errors = payload["errors"]
            errors = self._candidate_errors(
                index,
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
                index.replace(
                    StoredRecord(
                        record_type=record_type,
                        record=deepcopy(record),
                        event_id=event["event_id"],
                    )
                )
        return index.records

    def _event_payload(
        self,
        event: Mapping[str, Any],
        position: int,
    ) -> tuple[dict[str, Any], str, dict[str, Any], str | None]:
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
        return payload, record_type, record, supersedes

    @staticmethod
    def _require_unchanged_prefix(
        events: list[dict[str, Any]],
        prefix: list[dict[str, Any]],
        suffix_length: int,
    ) -> int:
        prefix_length = len(prefix)
        if len(events) != prefix_length + suffix_length:
            raise ReconError(
                "ledger changed while the Recon record batch was being prepared"
            )
        if prefix_length and (
            events[prefix_length - 1]["event_hash"]
            != prefix[prefix_length - 1]["event_hash"]
        ):
            raise ReconError(
                "ledger changed while the Recon record batch was being prepared"
            )
        return prefix_length

    def _validate_decision_suffix(
        self,
        events: list[dict[str, Any]],
        *,
        prefix: list[dict[str, Any]],
        original_state: Mapping[str, StoredRecord],
        suffix_length: int,
    ) -> None:
        prefix_length = self._require_unchanged_prefix(
            events, prefix, suffix_length
        )
        index = _ReplayIndex.from_records(self.registry, original_state)
        for position, event in enumerate(events[prefix_length:], start=prefix_length + 1):
            payload, record_type, record, supersedes = self._event_payload(event, position)
            errors = self._candidate_errors(index, record_type, record, supersedes)
            expected_decision = RECORDED if not errors else REJECTED
            if payload["decision"] != expected_decision:
                raise ReconError(
                    f"event {position} decision is {payload['decision']}, "
                    f"replay requires {expected_decision}"
                )
            if payload["errors"] != errors:
                raise ReconError(f"event {position} validation errors do not replay exactly")
            if not errors:
                index.replace(
                    StoredRecord(record_type, deepcopy(record), event["event_id"])
                )

    def _validate_required_suffix(
        self,
        events: list[dict[str, Any]],
        *,
        prefix: list[dict[str, Any]],
        original_state: Mapping[str, StoredRecord],
        suffix_length: int,
    ) -> None:
        prefix_length = self._require_unchanged_prefix(
            events, prefix, suffix_length
        )
        index = _ReplayIndex.from_records(self.registry, original_state)
        for position, event in enumerate(events[prefix_length:], start=prefix_length + 1):
            payload, record_type, record, supersedes = self._event_payload(event, position)
            if payload["decision"] != RECORDED or payload["errors"] != []:
                raise ReconError(
                    f"event {position} in a required batch must be RECORDED without errors"
                )
            errors = self._candidate_errors(index, record_type, record, supersedes)
            if errors:
                raise ReconError(
                    f"event {position} required batch does not replay in order: "
                    + "; ".join(errors)
                )
            index.replace(
                StoredRecord(record_type, deepcopy(record), event["event_id"])
            )
        errors = [
            *self._state_errors(index.records),
            *self._duplicate_profile_errors(index.records),
        ]
        if errors:
            raise ReconError(
                "required batch final state does not replay: " + "; ".join(errors)
            )

    def _candidate_errors(
        self,
        index: _ReplayIndex,
        record_type: str,
        record: Mapping[str, Any],
        supersedes_event_id: str | None,
    ) -> list[str]:
        errors = self._identity_errors(
            index.records,
            index.latest,
            record_type,
            record,
            supersedes_event_id,
        )
        if errors:
            return errors
        identifier = record["id"]
        candidate = StoredRecord(record_type, deepcopy(dict(record)), "candidate")
        errors = self._transition_materialization_errors(index, candidate)

        affected = {identifier}
        if record_type == "EvidenceAttachment":
            previous = index.records.get(identifier)
            was_retired = (
                previous is not None
                and previous.record.get("review_state") == "RETIRED"
            )
            is_retired = candidate.record.get("review_state") == "RETIRED"
            if was_retired != is_retired:
                affected.update(index.records_by_evidence.get(identifier, ()))

        def lookup(record_id: str) -> StoredRecord | None:
            if record_id == identifier:
                return candidate
            return index.records.get(record_id)

        for affected_id in sorted(affected):
            stored = candidate if affected_id == identifier else index.records[affected_id]
            errors.extend(self._record_semantic_errors(affected_id, stored, lookup))

        if record_type == "CoversAxisRelation":
            source = record.get("source_id")
            target = record.get("target_id")
            if isinstance(source, str) and isinstance(target, str):
                duplicates = index.coverage_profiles.get((source, target), set()) - {
                    identifier
                }
                if duplicates:
                    existing_id = min(duplicates)
                    errors.append(
                        f"CoversAxisRelation '{identifier}' duplicates subject-axis profile "
                        f"already recorded by '{existing_id}'"
                    )
        return errors

    def _transition_materialization_errors(
        self,
        index: _ReplayIndex,
        candidate: StoredRecord,
    ) -> list[str]:
        identifier = candidate.record["id"]
        categories = tuple(
            category
            for category in ("Entity", "Relation", "Event")
            if self.registry.is_subtype_of(candidate.record_type, category)
        )
        if not categories:
            return [
                f"{candidate.record_type} '{identifier}' is not an Entity, Relation, or Event"
            ]

        errors = []
        for category in categories:
            operation = self._validate_record_operation(
                candidate,
                index.records,
                category,
            )
            if operation.op_status == OpStatus.REJECTED:
                errors.append(
                    f"{candidate.record_type} '{identifier}': "
                    f"{operation.rejection_reason}"
                )
                if category == "Entity":
                    for relation_id in sorted(
                        index.relations_by_endpoint.get(identifier, ())
                    ):
                        relation = index.records[relation_id]
                        dependent = self._validate_record_operation(
                            relation,
                            index.records,
                            "Relation",
                            excluded_entity_id=identifier,
                        )
                        if dependent.op_status == OpStatus.REJECTED:
                            errors.append(
                                f"{relation.record_type} '{relation_id}': "
                                f"{dependent.rejection_reason}"
                            )
        return errors

    def _validate_record_operation(
        self,
        stored: StoredRecord,
        state: Mapping[str, StoredRecord],
        category: str,
        *,
        excluded_entity_id: str | None = None,
    ):
        record = stored.record
        identifier = record["id"]
        properties = {
            key: deepcopy(value)
            for key, value in record.items()
            if key not in {"id", "source_id", "target_id"}
        }
        graph = KnowledgeGraph(self.registry)
        if category == "Entity":
            return graph.create_entity(stored.record_type, identifier, properties)
        if category == "Event":
            return graph.create_event(stored.record_type, identifier, properties)

        materialized_endpoints = set()
        for endpoint in (record.get("source_id"), record.get("target_id")):
            if (
                not isinstance(endpoint, str)
                or endpoint == excluded_entity_id
                or endpoint in materialized_endpoints
            ):
                continue
            endpoint_record = state.get(endpoint)
            if endpoint_record is None or not self.registry.is_subtype_of(
                endpoint_record.record_type, "Entity"
            ):
                continue
            endpoint_properties = {
                key: deepcopy(value)
                for key, value in endpoint_record.record.items()
                if key not in {"id", "source_id", "target_id"}
            }
            graph.create_entity(
                endpoint_record.record_type,
                endpoint,
                endpoint_properties,
            )
            materialized_endpoints.add(endpoint)
        return graph.create_relation(
            stored.record_type,
            identifier,
            record.get("source_id"),
            record.get("target_id"),
            properties,
        )

    def _identity_errors(
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
        return []

    def _state_errors(self, state: Mapping[str, StoredRecord]) -> list[str]:
        errors, _ = self._materialize(state)
        errors.extend(self._semantic_errors(state))
        return errors

    @staticmethod
    def _duplicate_profile_errors(state: Mapping[str, StoredRecord]) -> list[str]:
        profiles: dict[tuple[str, str], str] = {}
        errors = []
        for identifier, stored in sorted(state.items()):
            if stored.record_type != "CoversAxisRelation":
                continue
            key = (stored.record.get("source_id"), stored.record.get("target_id"))
            prior = profiles.get(key)
            if prior is not None:
                errors.append(
                    f"CoversAxisRelation profile {key[0]!r} -> {key[1]!r} is duplicated "
                    f"by '{prior}' and '{identifier}'"
                )
            else:
                profiles[key] = identifier
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
            errors.extend(self._record_semantic_errors(identifier, stored, state.get))
        return errors

    def _record_semantic_errors(
        self,
        identifier: str,
        stored: StoredRecord,
        lookup: Callable[[Any], StoredRecord | None],
    ) -> list[str]:
        record = stored.record
        errors = []
        evidence_ids = record.get("evidence_ids", [])
        if isinstance(evidence_ids, list):
            for evidence_id in evidence_ids:
                evidence = lookup(evidence_id)
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

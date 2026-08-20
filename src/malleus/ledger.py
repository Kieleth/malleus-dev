"""Strict single-writer hash-linked JSONL storage for protocol events."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import tempfile
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping


SCHEMA_VERSION = "1"
GENESIS = "GENESIS"
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
EVENT_FIELDS = {
    "schema_version",
    "sequence",
    "event_id",
    "event_type",
    "transaction_time",
    "actor_id",
    "ontology_hash",
    "payload",
    "previous_event_hash",
    "event_hash",
}


class LedgerError(ValueError):
    """The event ledger is malformed, inconsistent, or cannot be verified."""


def canonical_json(value: Any) -> str:
    try:
        blob = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        # Lone surrogates survive json.dumps but not the wire. Encode here,
        # inside the typed handler (UnicodeEncodeError is a ValueError), so
        # every digest, append, and read failure is a LedgerError, never an
        # untyped crash.
        blob.encode("utf-8")
        return blob
    except (TypeError, ValueError) as error:
        raise LedgerError(f"Value is not canonical JSON: {error}") from error


def content_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def event_hash(event: Mapping[str, Any]) -> str:
    return content_digest({key: deepcopy(value) for key, value in event.items() if key != "event_hash"})


def record_hash(record_type: str, record: Mapping[str, Any]) -> str:
    if not isinstance(record_type, str) or not record_type.strip():
        raise LedgerError("record_type must be a nonblank string")
    if not isinstance(record, Mapping):
        raise LedgerError("record must be a mapping")
    body = {key: deepcopy(value) for key, value in record.items() if key != "content_hash"}
    return content_digest({"record_type": record_type, "record": body})


def with_content_hash(record_type: str, record: Mapping[str, Any]) -> dict[str, Any]:
    if "content_hash" in record:
        raise LedgerError("content_hash is generated and must not be supplied")
    result = deepcopy(dict(record))
    result["content_hash"] = record_hash(record_type, result)
    return result


def require_digest(value: Any, context: str) -> None:
    if not isinstance(value, str) or DIGEST_PATTERN.fullmatch(value) is None:
        raise LedgerError(f"{context} must be a sha256 digest")


def aware_datetime(value: Any, context: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise LedgerError(f"{context} must be an ISO 8601 datetime string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise LedgerError(f"{context} is invalid: {value}") from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise LedgerError(f"{context} must include a timezone offset")
    return parsed


class JsonlLedger:
    """Persistence envelope with no domain transition policy."""

    def __init__(
        self,
        path: str | Path,
        ontology_hash: str,
        historical_ontology_hashes: tuple[str, ...] = (),
    ):
        """`historical_ontology_hashes` are the same ontology's identity under
        earlier payload grammars.

        A hash written into an accepted append-only ledger is a public
        contract. The ledger cannot be rewritten to match a new hashing rule,
        so the rule must be able to verify what the ledger already holds. Every
        accepted hash names the same bytes; declaring one that does not is the
        caller's error and this envelope cannot detect it.
        """
        self.path = Path(path)
        require_digest(ontology_hash, "ontology_hash")
        for historical in historical_ontology_hashes:
            require_digest(historical, "historical ontology_hash")
        self.ontology_hash = ontology_hash
        self.historical_ontology_hashes = tuple(historical_ontology_hashes)
        self.accepted_ontology_hashes = (ontology_hash, *self.historical_ontology_hashes)
        # Which of them the last read actually encountered. A ledger replaying
        # under an earlier grammar is a fact the caller may act on, so it is
        # reported rather than absorbed.
        self.verified_ontology_hashes: tuple[str, ...] = ()

    def append(
        self,
        *,
        event_id: str,
        event_type: str,
        transaction_time: str,
        actor_id: str,
        payload: Mapping[str, Any],
        validate: Callable[[list[dict[str, Any]]], None],
    ) -> dict[str, Any]:
        """Validate history, then commit one line by failure-atomic replacement."""
        return self.append_many(
            (
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "transaction_time": transaction_time,
                    "actor_id": actor_id,
                    "payload": payload,
                },
            ),
            validate=validate,
        )[0]

    def append_many(
        self,
        entries: Iterable[Mapping[str, Any]],
        *,
        validate: Callable[[list[dict[str, Any]]], None],
    ) -> tuple[dict[str, Any], ...]:
        """Validate and commit one or more events by one atomic replacement."""
        pending = list(entries)
        if not pending:
            raise LedgerError("Ledger event batch must not be empty")
        events = self.read()
        appended = []
        previous_hash = events[-1]["event_hash"] if events else GENESIS
        expected = {
            "event_id",
            "event_type",
            "transaction_time",
            "actor_id",
            "payload",
        }
        for offset, entry in enumerate(pending, start=1):
            if not isinstance(entry, Mapping):
                raise LedgerError(f"Ledger batch entry {offset} must be a mapping")
            _exact_fields(entry, expected, f"Ledger batch entry {offset}")
            payload = entry["payload"]
            event = {
                "schema_version": SCHEMA_VERSION,
                "sequence": len(events) + offset,
                "event_id": entry["event_id"],
                "event_type": entry["event_type"],
                "transaction_time": entry["transaction_time"],
                "actor_id": entry["actor_id"],
                "ontology_hash": self.ontology_hash,
                "payload": (
                    deepcopy(dict(payload)) if isinstance(payload, Mapping) else payload
                ),
                "previous_event_hash": previous_hash,
            }
            event["event_hash"] = event_hash(event)
            appended.append(event)
            previous_hash = event["event_hash"]
        candidate = [*events, *appended]
        self._validate_envelopes(candidate)
        validate(deepcopy(candidate))
        encoded = "".join(
            canonical_json(event) + "\n" for event in appended
        ).encode("utf-8")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        current = self.path.read_bytes() if self.path.exists() else b""
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{self.path.name}.",
            suffix=".tmp",
            dir=self.path.parent,
        )
        try:
            view = memoryview(current + encoded)
            while view:
                written = os.write(descriptor, view)
                if written <= 0:
                    raise LedgerError("Ledger append made no progress")
                view = view[written:]
            os.fsync(descriptor)
            os.close(descriptor)
            descriptor = -1
            os.replace(temporary_name, self.path)
            temporary_name = ""
        except (OSError, LedgerError) as error:
            raise LedgerError(f"Ledger append failed without changing the ledger: {error}") from error
        finally:
            if descriptor >= 0:
                os.close(descriptor)
            if temporary_name:
                try:
                    os.unlink(temporary_name)
                except FileNotFoundError:
                    pass
        return tuple(deepcopy(appended))

    def read(
        self,
        *,
        expected_head_hash: str | None = None,
        expected_event_count: int | None = None,
    ) -> list[dict[str, Any]]:
        events = self._decode()
        self._validate_envelopes(events)
        if expected_event_count is not None and len(events) != expected_event_count:
            raise LedgerError(
                f"Ledger event count mismatch: expected {expected_event_count}, got {len(events)}"
            )
        head = events[-1]["event_hash"] if events else GENESIS
        if expected_head_hash is not None and head != expected_head_hash:
            raise LedgerError(f"Ledger head mismatch: expected {expected_head_hash}, got {head}")
        return deepcopy(events)

    def _decode(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        raw = self.path.read_bytes()
        if not raw:
            return []
        if not raw.endswith(b"\n"):
            raise LedgerError("Ledger has a truncated final record")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise LedgerError(f"Ledger is not valid UTF-8: {error}") from error
        events = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line:
                raise LedgerError(f"line {line_number}: blank lines are not allowed")
            try:
                event = json.loads(
                    line,
                    object_pairs_hook=_unique_object,
                    parse_constant=_reject_nonfinite,
                )
            except (json.JSONDecodeError, LedgerError) as error:
                raise LedgerError(f"line {line_number}: invalid JSON: {error}") from error
            if not isinstance(event, dict):
                raise LedgerError(f"line {line_number}: event must be an object")
            events.append(event)
        return events

    def _validate_envelopes(self, events: list[dict[str, Any]]) -> None:
        prior_hash = GENESIS
        prior_time = None
        event_ids = set()
        seen: set[str] = set()
        for index, event in enumerate(events, start=1):
            context = f"event {index}"
            _string_keys(event, context)
            _exact_fields(event, EVENT_FIELDS, context)
            if event["schema_version"] != SCHEMA_VERSION:
                raise LedgerError(
                    f"{context}: unsupported schema_version: {event['schema_version']}"
                )
            if (
                not isinstance(event["sequence"], int)
                or isinstance(event["sequence"], bool)
                or event["sequence"] != index
            ):
                raise LedgerError(f"{context}: sequence must be {index}")
            for name in ("event_id", "event_type", "actor_id"):
                if not isinstance(event[name], str) or not event[name].strip():
                    raise LedgerError(f"{context}: {name} must be a nonblank string")
            if event["event_id"] in event_ids:
                raise LedgerError(f"{context}: duplicate event_id '{event['event_id']}'")
            transaction_time = aware_datetime(
                event["transaction_time"],
                f"{context} transaction_time",
            )
            if prior_time is not None and transaction_time < prior_time:
                raise LedgerError(f"{context}: transaction_time decreased")
            if event["ontology_hash"] not in self.accepted_ontology_hashes:
                raise LedgerError(
                    f"{context}: ontology_hash does not match this ledger under any "
                    f"payload grammar it accepts"
                )
            seen.add(event["ontology_hash"])
            require_digest(event["ontology_hash"], f"{context} ontology_hash")
            if event["previous_event_hash"] != prior_hash:
                raise LedgerError(f"{context}: previous_event_hash mismatch")
            if prior_hash != GENESIS:
                require_digest(prior_hash, f"{context} previous_event_hash")
            require_digest(event["event_hash"], f"{context} event_hash")
            if event["event_hash"] != event_hash(event):
                raise LedgerError(f"{context}: event_hash mismatch")
            if not isinstance(event["payload"], dict):
                raise LedgerError(f"{context}: payload must be an object")
            _reject_nonfinite_tree(event["payload"], f"{context} payload")
            event_ids.add(event["event_id"])
            prior_hash = event["event_hash"]
            prior_time = transaction_time
        self.verified_ontology_hashes = tuple(
            h for h in self.accepted_ontology_hashes if h in seen
        )


def _string_keys(value: Mapping[Any, Any], context: str) -> None:
    invalid = [repr(key) for key in value if not isinstance(key, str)]
    if invalid:
        raise LedgerError(f"{context}: object keys must be strings: {', '.join(invalid)}")


def _exact_fields(value: Mapping[str, Any], expected: set[str], context: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing:
        raise LedgerError(f"{context}: missing required fields: {', '.join(missing)}")
    if unknown:
        raise LedgerError(f"{context}: unknown fields: {', '.join(unknown)}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise LedgerError(f"duplicate JSON key '{key}'")
        result[key] = value
    return result


def _reject_nonfinite(value: str) -> None:
    raise LedgerError(f"nonfinite JSON number '{value}' is not allowed")


def _reject_nonfinite_tree(value: Any, context: str) -> None:
    if isinstance(value, dict):
        _string_keys(value, context)
        for name, item in value.items():
            _reject_nonfinite_tree(item, f"{context}.{name}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_nonfinite_tree(item, f"{context}[{index}]")
    elif isinstance(value, float) and not math.isfinite(value):
        raise LedgerError(f"{context}: nonfinite numbers are not allowed")

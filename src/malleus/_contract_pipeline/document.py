"""Optional document-assertion adapter for neutral population plans."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from types import MappingProxyType
from typing import Any

from malleus._contract_pipeline.population import (
    SOURCE_ASSERTION_PROFILE,
    _GAP_KINDS,
    _GRAMMAR as _POPULATION_PLAN_GRAMMAR,
)


DOCUMENT_CAPTURE_GRAMMAR = "malleus.document-capture/private-v0"
DOCUMENT_ASSERTION_ADAPTER = MappingProxyType(
    {"adapter_id": "document-assertion", "version": "0"}
)

_CAPTURE_FIELDS = {
    "assertions",
    "attribution",
    "nothing_assertable",
    "reading_sha256",
    "schema",
}
_ATTRIBUTION_FIELDS = {"author", "date", "source_id"}
_ASSERTION_FIELDS = {
    "block",
    "formalized_by",
    "gaps",
    "id",
    "modality",
    "statement",
}
_FORMALIZATION_FIELDS = {"path", "record_id"}
_GAP_FIELDS = {"kind", "statement"}
_MODALITIES = {
    "CALCULATED",
    "CONTESTED",
    "HYPOTHESISED",
    "MEASURED",
    "NEGATED",
    "STATED",
}


class DocumentAssertionRefusalReason(str, Enum):
    FIELDS_NOT_CLOSED = "FIELDS_NOT_CLOSED"
    GAP_REQUIRED = "GAP_REQUIRED"
    MALFORMED_CAPTURE = "MALFORMED_CAPTURE"
    MALFORMED_READING = "MALFORMED_READING"
    NOT_VERBATIM = "NOT_VERBATIM"
    READING_MISMATCH = "READING_MISMATCH"
    UNKNOWN_BLOCK = "UNKNOWN_BLOCK"
    UNKNOWN_FORMALIZATION_TARGET = "UNKNOWN_FORMALIZATION_TARGET"
    UNKNOWN_GAP_KIND = "UNKNOWN_GAP_KIND"
    UNKNOWN_MODALITY = "UNKNOWN_MODALITY"
    UNSUPPORTED_GRAMMAR = "UNSUPPORTED_GRAMMAR"


class DocumentAssertionRefusal(ValueError):
    def __init__(self, reason: DocumentAssertionRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


@dataclass(frozen=True, slots=True)
class DocumentAssertionCompilation:
    """Exact evidence and deterministic products of one document capture."""

    capture_id: str
    capture_bytes: bytes
    capture_identity: str
    reading_identity: str
    canonical_plan_bytes: bytes
    canonical_census_bytes: bytes


def _fail(
    reason: DocumentAssertionRefusalReason, detail: str
) -> DocumentAssertionRefusal:
    return DocumentAssertionRefusal(reason, detail)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key: {key}")
        result[key] = value
    return result


def _load(
    source: bytes, label: str, reason: DocumentAssertionRefusalReason
) -> dict[str, object]:
    if type(source) is not bytes:
        raise _fail(reason, f"{label} must be exact bytes")
    try:
        value = json.loads(source, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, TypeError, UnicodeDecodeError, ValueError) as error:
        raise _fail(reason, f"{label} is not unambiguous JSON") from error
    return _obj(value, label, reason)


def _canonical(value: object, label: str) -> bytes:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode()
    except (TypeError, UnicodeError, ValueError) as error:
        raise _fail(
            DocumentAssertionRefusalReason.MALFORMED_CAPTURE,
            f"{label} is not JSON data",
        ) from error


def _obj(
    value: object,
    label: str,
    reason: DocumentAssertionRefusalReason = (
        DocumentAssertionRefusalReason.MALFORMED_CAPTURE
    ),
) -> dict[str, object]:
    if not isinstance(value, dict):
        raise _fail(reason, f"{label} must be an object")
    return value


def _items(
    value: object,
    label: str,
    reason: DocumentAssertionRefusalReason = (
        DocumentAssertionRefusalReason.MALFORMED_CAPTURE
    ),
) -> list[object]:
    if not isinstance(value, list):
        raise _fail(reason, f"{label} must be an array")
    return value


def _word(
    value: object,
    label: str,
    reason: DocumentAssertionRefusalReason = (
        DocumentAssertionRefusalReason.MALFORMED_CAPTURE
    ),
) -> str:
    if not isinstance(value, str) or not value:
        raise _fail(reason, f"{label} is required")
    return value


def _closed(value: dict[str, object], fields: set[str], label: str) -> None:
    if set(value) != fields:
        raise _fail(
            DocumentAssertionRefusalReason.FIELDS_NOT_CLOSED,
            f"{label} fields are not closed",
        )


def _reading_blocks(reading: dict[str, object]) -> tuple[tuple[str, str], ...]:
    reason = DocumentAssertionRefusalReason.MALFORMED_READING
    pages = _items(reading.get("pages"), "reading pages", reason)
    blocks: list[tuple[str, str]] = []
    seen: set[str] = set()
    for raw_page in pages:
        page = _obj(raw_page, "reading page", reason)
        for raw_block in _items(page.get("blocks"), "reading page blocks", reason):
            block = _obj(raw_block, "reading block", reason)
            block_id = _word(block.get("id"), "reading block ID", reason)
            ordinal = block.get("ordinal")
            text = block.get("text")
            if (
                isinstance(ordinal, bool)
                or not isinstance(ordinal, int)
                or not isinstance(text, str)
            ):
                raise _fail(reason, f"malformed block ordinal or text: {block_id}")
            if block_id in seen:
                raise _fail(reason, f"repeated block ID: {block_id}")
            seen.add(block_id)
            blocks.append((block_id, text))
    return tuple(blocks)


def _record_snapshot(
    records: object,
) -> tuple[dict[str, object], dict[str, dict[str, object]]]:
    root = _obj(json.loads(_canonical(records, "records")), "records")
    by_id: dict[str, dict[str, object]] = {}
    for raw_family in root.values():
        for raw_record in _items(raw_family, "record family"):
            record = _obj(raw_record, "record")
            record_id = _word(record.get("id"), "record ID")
            if record_id in by_id:
                raise _fail(
                    DocumentAssertionRefusalReason.MALFORMED_CAPTURE,
                    f"repeated record ID: {record_id}",
                )
            by_id[record_id] = record
    return root, by_id


def _path_exists(record: dict[str, object], path: list[object]) -> bool:
    if not path or not all(isinstance(step, str) and step for step in path):
        return False
    node: object = record
    for step in path:
        if not isinstance(node, dict) or step not in node:
            return False
        node = node[step]
    return True


def _normalise(text: str) -> str:
    return " ".join(text.split())


def adapt_document_assertions(
    *,
    reading_bytes: bytes,
    capture_bytes: bytes,
    capture_id: str,
    plan_id: str,
    contract_identity: str,
    records: object,
    supersessions: object,
    valid_time: object,
) -> DocumentAssertionCompilation:
    """Turn one checked document capture into one neutral population plan."""

    reading = _load(
        reading_bytes,
        "reading",
        DocumentAssertionRefusalReason.MALFORMED_READING,
    )
    capture = _load(
        capture_bytes,
        "capture",
        DocumentAssertionRefusalReason.MALFORMED_CAPTURE,
    )
    _closed(capture, _CAPTURE_FIELDS, "capture")
    if capture["schema"] != DOCUMENT_CAPTURE_GRAMMAR:
        raise _fail(
            DocumentAssertionRefusalReason.UNSUPPORTED_GRAMMAR,
            "document-capture grammar is unsupported",
        )

    reading_identity = _digest(reading_bytes)
    if capture["reading_sha256"] != reading_identity:
        raise _fail(
            DocumentAssertionRefusalReason.READING_MISMATCH,
            "capture does not name the supplied reading bytes",
        )
    blocks = _reading_blocks(reading)
    block_text = dict(blocks)

    attribution = _obj(capture["attribution"], "capture attribution")
    _closed(attribution, _ATTRIBUTION_FIELDS, "capture attribution")
    source_id = _word(attribution["source_id"], "capture source ID")
    _word(attribution["author"], "capture author")
    _word(attribution["date"], "capture date")

    record_data, records_by_id = _record_snapshot(records)
    assertions = _items(capture["assertions"], "capture assertions")
    reviewed = _reviewed_blocks(capture, block_text)
    derivations: list[dict[str, object]] = []
    gaps: list[dict[str, object]] = []
    counts = {
        "FULLY_FORMALIZED": 0,
        "PARTLY_FORMALIZED": 0,
        "UNFORMALIZED": 0,
    }
    gaps_by_kind: dict[str, int] = {}
    seen_assertions: set[str] = set()

    for raw_assertion in assertions:
        assertion = _obj(raw_assertion, "assertion")
        _closed(assertion, _ASSERTION_FIELDS, "assertion")
        assertion_id = _word(assertion["id"], "assertion ID")
        if assertion_id in seen_assertions:
            raise _fail(
                DocumentAssertionRefusalReason.MALFORMED_CAPTURE,
                f"repeated assertion ID: {assertion_id}",
            )
        seen_assertions.add(assertion_id)
        block_id = _word(assertion["block"], "assertion block")
        if block_id not in block_text:
            raise _fail(
                DocumentAssertionRefusalReason.UNKNOWN_BLOCK,
                f"unknown assertion block: {block_id}",
            )
        reviewed.add(block_id)
        statement = _word(assertion["statement"], "assertion statement")
        if _normalise(statement) not in _normalise(block_text[block_id]):
            raise _fail(
                DocumentAssertionRefusalReason.NOT_VERBATIM,
                f"assertion is not verbatim: {assertion_id}",
            )
        modality = _word(assertion["modality"], "assertion modality")
        if modality not in _MODALITIES:
            raise _fail(
                DocumentAssertionRefusalReason.UNKNOWN_MODALITY,
                f"unsupported assertion modality: {modality}",
            )

        formalizations = _items(assertion["formalized_by"], "formalized_by")
        assertion_gaps = _items(assertion["gaps"], "assertion gaps")
        if not formalizations and not assertion_gaps:
            raise _fail(
                DocumentAssertionRefusalReason.GAP_REQUIRED,
                f"assertion has no formalization or gap: {assertion_id}",
            )
        _append_formalizations(
            formalizations,
            assertion_id,
            source_id,
            records_by_id,
            derivations,
        )
        _append_gaps(
            assertion_gaps,
            assertion_id,
            source_id,
            gaps,
            gaps_by_kind,
        )
        key = (
            "PARTLY_FORMALIZED"
            if formalizations and assertion_gaps
            else "FULLY_FORMALIZED"
            if formalizations
            else "UNFORMALIZED"
        )
        counts[key] += 1

    capture_id = _word(capture_id, "capture ID")
    plan_id = _word(plan_id, "plan ID")
    contract_identity = _word(contract_identity, "contract identity")
    capture_identity = _digest(capture_bytes)
    plan = {
        "adapter": dict(DOCUMENT_ASSERTION_ADAPTER),
        "contract_identity": contract_identity,
        "derivations": derivations,
        "evidence": [{"evidence_id": capture_id, "sha256": capture_identity}],
        "gaps": gaps,
        "grammar": _POPULATION_PLAN_GRAMMAR,
        "history_profile": {
            "profile_id": SOURCE_ASSERTION_PROFILE.profile_id,
            "sha256": SOURCE_ASSERTION_PROFILE.identity,
        },
        "plan_id": plan_id,
        "records": record_data,
        "sources": [{"sha256": reading_identity, "source_id": source_id}],
        "supersessions": json.loads(_canonical(supersessions, "supersessions")),
        "valid_time": json.loads(_canonical(valid_time, "valid time")),
    }
    census = {
        "assertions": counts,
        "blocks": {
            block_id: "REVIEWED" if block_id in reviewed else "UNTOUCHED"
            for block_id, _ in blocks
        },
        "blocks_reviewed": len(reviewed),
        "blocks_total": len(blocks),
        "capture_sha256": capture_identity,
        "gaps_by_kind": dict(sorted(gaps_by_kind.items())),
    }
    return DocumentAssertionCompilation(
        capture_id=capture_id,
        capture_bytes=capture_bytes,
        capture_identity=capture_identity,
        reading_identity=reading_identity,
        canonical_plan_bytes=_canonical(plan, "population plan"),
        canonical_census_bytes=_canonical(census, "capture census"),
    )


def _reviewed_blocks(
    capture: dict[str, object], block_text: dict[str, str]
) -> set[str]:
    reviewed: set[str] = set()
    for value in _items(capture["nothing_assertable"], "nothing_assertable"):
        block_id = _word(value, "nothing_assertable block ID")
        if block_id not in block_text:
            raise _fail(
                DocumentAssertionRefusalReason.UNKNOWN_BLOCK,
                f"unknown nothing_assertable block: {block_id}",
            )
        reviewed.add(block_id)
    return reviewed


def _append_formalizations(
    values: list[object],
    assertion_id: str,
    source_id: str,
    records: dict[str, dict[str, object]],
    output: list[dict[str, object]],
) -> None:
    for value in values:
        formalization = _obj(value, "formalization")
        _closed(formalization, _FORMALIZATION_FIELDS, "formalization")
        record_id = _word(
            formalization["record_id"],
            "formalization record ID",
            DocumentAssertionRefusalReason.UNKNOWN_FORMALIZATION_TARGET,
        )
        path = _items(
            formalization["path"],
            "formalization path",
            DocumentAssertionRefusalReason.UNKNOWN_FORMALIZATION_TARGET,
        )
        record = records.get(record_id)
        if record is None or not _path_exists(record, path):
            raise _fail(
                DocumentAssertionRefusalReason.UNKNOWN_FORMALIZATION_TARGET,
                f"missing formalization target: {record_id}:{path}",
            )
        output.append(
            {
                "locator": assertion_id,
                "path": path,
                "record_id": record_id,
                "source_id": source_id,
            }
        )


def _append_gaps(
    values: list[object],
    assertion_id: str,
    source_id: str,
    output: list[dict[str, object]],
    counts: dict[str, int],
) -> None:
    for value in values:
        gap = _obj(value, "assertion gap")
        _closed(gap, _GAP_FIELDS, "assertion gap")
        kind = _word(
            gap["kind"],
            "assertion gap kind",
            DocumentAssertionRefusalReason.UNKNOWN_GAP_KIND,
        )
        if kind not in _GAP_KINDS:
            raise _fail(
                DocumentAssertionRefusalReason.UNKNOWN_GAP_KIND,
                f"unsupported assertion gap kind: {kind}",
            )
        output.append(
            {
                "kind": kind,
                "locator": assertion_id,
                "source_id": source_id,
                "statement": _word(gap["statement"], "assertion gap statement"),
            }
        )
        counts[kind] = counts.get(kind, 0) + 1


__all__ = (
    "DOCUMENT_ASSERTION_ADAPTER",
    "DOCUMENT_CAPTURE_GRAMMAR",
    "DocumentAssertionCompilation",
    "DocumentAssertionRefusal",
    "DocumentAssertionRefusalReason",
    "adapt_document_assertions",
)

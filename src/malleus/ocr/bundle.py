"""The portable object model for a document evidence bundle.

Every object here is one identity plane. The planes exist so that a change in
one cannot silently rewrite another: correcting a reading must not move the
region it read, and a retry must not overwrite the attempt before it.

These dataclasses are a carrier, never the authority. The authority is
`ontology/domains/ocr.yaml`, and every object here answers `record()` with the
graph record the registry validates. A field that does not reach a record is
governed by nothing, which is the defect this profile spent a release
committing before its own rubric caught it.

Nested structures do not become graph records. A selector, a config identity
and transport metadata are content-addressed artifacts (decision 2), so the
coordinate contract stays the selector specification's and this schema does
not fork it.

Digests reuse `malleus.ledger.canonical_json`, so a bundle object hashes the
same way a protocol record does. Nothing in this module writes to a ledger.
"""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import MISSING, asdict, dataclass, field, fields, is_dataclass
from typing import Any, Mapping

from malleus.ledger import canonical_json

# The portable identity of this profile. A document that does not name all
# three is not refused for tidiness: a reader that guesses which profile and
# version produced a bundle is a reader that will one day guess wrong.
PROFILE_ID = "malleus.ocr.evidence_integrity"
PROFILE_VERSION = "v0"
DOCUMENT_VERSION = 1


class BundleError(ValueError):
    """A document cannot be read as a bundle. Refuse; never repair."""


# Full, algorithm-tagged digests only. A truncated digest may be displayed and
# may never be stored as an integrity value (decision C6 and OCR-090).
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")

# Material that must never reach a bundle. Credentials are excluded by
# construction, not by redaction after the fact (decision C6).
SECRET_KEYS = frozenset({
    "authorization", "api_key", "apikey", "x-api-key", "token",
    "access_token", "refresh_token", "secret", "password", "cookie",
    "set-cookie", "private_key", "client_secret",
})


def canonical_digest(value: Any) -> str:
    """Digest a bundle object the way the protocol digests a record.

    Dataclasses are converted to plain mappings first, so an object and the
    mapping it serializes to produce the same digest. A bundle that travels
    as JSON and one held in memory must not disagree about their identity.
    """
    if is_dataclass(value) and not isinstance(value, type):
        value = asdict(value)
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


# Fields carried as tuples in Python and as arrays in a document.
_TUPLE_FIELDS = frozenset({
    "required_units", "candidate_ids", "observed_units",
    "sources", "rasters", "regions", "attempts", "hypotheses",
    "corrections", "selections",
})

_STRING_FIELDS = frozenset({
    "id", "temporal_policy", "frozen_at", "inventory_basis", "digest",
    "media_type", "locator", "source_id", "unit", "render_contract",
    "raster_id", "selector_profile", "region_id", "request_digest", "status",
    "response_digest", "unavailable_reason", "text_digest", "attempt_id",
    "correction_id", "reviewed_hypothesis_id", "reviewer_id", "verdict",
    "corrected_text_digest", "predecessor_id", "selected_id", "reason", "kind",
    "data_handling_policy_id", "hostile_content_policy_id",
})

_STRING_ARRAY_FIELDS = frozenset({"required_units", "candidate_ids", "observed_units"})


def _validate_document_field(cls: type, name: str, value: Any, where: str) -> None:
    """Refuse JSON shapes the carrier annotations cannot represent safely."""
    field_path = f"{where}.{name}"
    if name in _TUPLE_FIELDS and not isinstance(value, (list, tuple)):
        raise BundleError(f"{field_path} must be an array")
    if name in _STRING_ARRAY_FIELDS:
        invalid = next(
            ((index, item) for index, item in enumerate(value) if not isinstance(item, str)),
            None,
        )
        if invalid is not None:
            index, item = invalid
            raise BundleError(
                f"{field_path}[{index}] must be a string, got {type(item).__name__}"
            )
    if name in _STRING_FIELDS and value is not None and not isinstance(value, str):
        raise BundleError(f"{field_path} must be a string, got {type(value).__name__}")
    if name == "byte_length" and (
        not isinstance(value, int) or isinstance(value, bool)
    ):
        raise BundleError(f"{field_path} must be an integer, got {type(value).__name__}")
    if name == "confidence" and value is not None and (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(float(value))
    ):
        raise BundleError(f"{field_path} must be a finite number")
    if name == "human_verified" and not isinstance(value, bool):
        raise BundleError(f"{field_path} must be a boolean, got {type(value).__name__}")
    if name in {"selector", "config_identity", "metric_families", "transport_metadata"}:
        if not isinstance(value, Mapping):
            raise BundleError(f"{field_path} must be a mapping, got {type(value).__name__}")
    if cls is OCRAttempt and name == "config_identity":
        invalid = next(
            (
                (key, item)
                for key, item in value.items()
                if not isinstance(key, str) or not isinstance(item, str)
            ),
            None,
        )
        if invalid is not None:
            key, item = invalid
            raise BundleError(
                f"{field_path}[{key!r}] must have a string key and value, "
                f"got {type(item).__name__} value"
            )
    if cls is SourceClass and name == "metric_families":
        for family, declaration in value.items():
            if not isinstance(family, str):
                raise BundleError(f"{field_path} names must be strings")
            if not isinstance(declaration, Mapping):
                raise BundleError(f"{field_path}[{family!r}] must be a mapping")
            denominator = declaration.get("denominator")
            if denominator is not None and not isinstance(denominator, str):
                raise BundleError(
                    f"{field_path}[{family!r}].denominator must be a string"
                )
            threshold = declaration.get("threshold")
            if threshold is not None and (
                not isinstance(threshold, (int, float))
                or isinstance(threshold, bool)
                or not math.isfinite(float(threshold))
            ):
                raise BundleError(
                    f"{field_path}[{family!r}].threshold must be a finite number"
                )


def _construct(cls: type, data: Any, where: str) -> Any:
    """Build one plane from a document fragment, or refuse and say why.

    Closed to undeclared keys. A document carrying a field this version does
    not know is a document from a profile this version cannot verify, and
    dropping it silently would let the unknown part travel unexamined.
    """
    if not isinstance(data, Mapping):
        raise BundleError(f"{where} must be a mapping, got {type(data).__name__}")
    declared = {f.name for f in fields(cls)}
    unknown = sorted(set(data) - declared)
    if unknown:
        raise BundleError(f"{where} carries undeclared keys: {', '.join(unknown)}")
    required = _DOCUMENT_REQUIRED_FIELDS.get(cls, frozenset({
        f.name for f in fields(cls)
        if f.default is MISSING and f.default_factory is MISSING
    }))
    absent = sorted(name for name in required if name not in data or data[name] is None)
    if absent:
        raise BundleError(f"{where} is missing required keys: {', '.join(absent)}")
    for name, value in data.items():
        _validate_document_field(cls, name, value, where)
    payload = {
        name: tuple(value) if name in _TUPLE_FIELDS else value
        for name, value in data.items()
    }
    try:
        return cls(**payload)
    except (TypeError, ValueError) as error:
        raise BundleError(f"{where} cannot be constructed: {error}") from error


def _present(record: dict[str, Any]) -> dict[str, Any]:
    """Drop unset optional slots. An absent optional slot is not a null one."""
    return {key: value for key, value in record.items() if value is not None}


@dataclass(frozen=True)
class SourceClass:
    """Declared before ingest and frozen at it (decision C8).

    Carries the three per-class declarations that decisions C2, C3 and C4 each
    needed separately: the required-unit inventory, the coverage metric
    families with their denominators and thresholds, and the temporal policy.
    Freezing matters: a metric family chosen after seeing the scan is a metric
    family chosen to flatter it.
    """

    id: str
    required_units: tuple[str, ...]
    metric_families: Mapping[str, Mapping[str, Any]]
    temporal_policy: str
    frozen_at: str
    inventory_basis: str = "derived_then_confirmed"

    def record(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "required_units": list(self.required_units),
            "metric_family_names": sorted(self.metric_families),
            "metric_families_digest": canonical_digest(self.metric_families),
            "temporal_policy": self.temporal_policy,
            "frozen_at": self.frozen_at,
            "inventory_basis": self.inventory_basis,
        }


@dataclass(frozen=True)
class SourceRepresentation:
    """Exact original bytes. Never replaced by a normalized derivative."""

    id: str
    digest: str
    byte_length: int
    media_type: str
    locator: str

    def record(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "digest": self.digest,
            "byte_length": self.byte_length,
            "media_type": self.media_type,
            "locator": self.locator,
        }


@dataclass(frozen=True)
class Raster:
    """A rendering derived from a source. Derived, never a replacement."""

    id: str
    source_id: str
    unit: str
    digest: str
    render_contract: str

    def record(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source_representation_id": self.source_id,
            "unit": self.unit,
            "digest": self.digest,
            "render_contract": self.render_contract,
        }


@dataclass(frozen=True)
class Region:
    """A stable spatial identity over a raster.

    The selector is governed by a declared profile. W3C Web Annotation and
    IIIF are the first-party default and hold no privilege: any profile that
    passes the selector conformance suite replaces them (decision C1).
    """

    id: str
    raster_id: str
    selector: Mapping[str, Any]
    selector_profile: str = "w3c-web-annotation+iiif"

    def record(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "raster_id": self.raster_id,
            "selector_digest": canonical_digest(self.selector),
            "selector_profile": self.selector_profile,
        }


@dataclass(frozen=True)
class OCRAttempt:
    """One execution attempt. Attempts never collapse, including retries."""

    id: str
    region_id: str
    request_digest: str
    config_identity: Mapping[str, str]
    status: str
    response_digest: str | None = None
    unavailable_reason: str | None = None

    def record(self) -> dict[str, Any]:
        return _present({
            "id": self.id,
            "event_type": "OCR_ATTEMPT",
            "region_id": self.region_id,
            "request_digest": self.request_digest,
            "config_identity_digest": canonical_digest(self.config_identity),
            "attempt_status": self.status,
            "response_digest": self.response_digest,
            "unavailable_reason": self.unavailable_reason,
        })


@dataclass(frozen=True)
class Hypothesis:
    """One reading of one region, from exactly one origin.

    A machine reading names its attempt; a human correction names its review.
    Never both, so the provenance of a reading is never ambiguous.
    """

    id: str
    region_id: str
    text_digest: str
    attempt_id: str | None = None
    correction_id: str | None = None
    confidence: float | None = None

    def record(self) -> dict[str, Any]:
        return _present({
            "id": self.id,
            "region_id": self.region_id,
            "text_digest": self.text_digest,
            "attempt_id": self.attempt_id,
            "correction_id": self.correction_id,
            "confidence": self.confidence,
        })


@dataclass(frozen=True)
class ReviewCorrection:
    """Append-only human review. Overwrites nothing."""

    id: str
    reviewed_hypothesis_id: str
    reviewer_id: str
    verdict: str
    corrected_text_digest: str | None = None
    predecessor_id: str | None = None

    def record(self) -> dict[str, Any]:
        return _present({
            "id": self.id,
            "event_type": "REVIEW_CORRECTION",
            "reviewed_hypothesis_id": self.reviewed_hypothesis_id,
            "reviewer_id": self.reviewer_id,
            "review_verdict": self.verdict,
            "corrected_text_digest": self.corrected_text_digest,
            "predecessor_id": self.predecessor_id,
        })


@dataclass(frozen=True)
class Selection:
    """Which reading is current, and why.

    Currency is not validity (decision C7). A demoted hypothesis remains a
    valid observation of the same bytes; it is simply not the selected one.
    """

    id: str
    region_id: str
    candidate_ids: tuple[str, ...]
    selected_id: str
    reason: str
    human_verified: bool = False

    def record(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "region_id": self.region_id,
            "candidate_ids": list(self.candidate_ids),
            "selected_id": self.selected_id,
            "reason": self.reason,
            "human_verified": self.human_verified,
        }


@dataclass(frozen=True)
class Bundle:
    """A portable document evidence bundle at capability AUDIT_ONLY."""

    id: str
    source_class: SourceClass
    kind: str = "FINISHED_READING"
    sources: tuple[SourceRepresentation, ...] = ()
    rasters: tuple[Raster, ...] = ()
    regions: tuple[Region, ...] = ()
    attempts: tuple[OCRAttempt, ...] = ()
    hypotheses: tuple[Hypothesis, ...] = ()
    corrections: tuple[ReviewCorrection, ...] = ()
    selections: tuple[Selection, ...] = ()
    observed_units: tuple[str, ...] = ()
    data_handling_policy_id: str | None = None
    hostile_content_policy_id: str | None = None
    transport_metadata: Mapping[str, Any] = field(default_factory=dict)

    def record(self) -> dict[str, Any]:
        return _present({
            "id": self.id,
            "bundle_kind": self.kind,
            "source_class_id": self.source_class.id,
            "member_ids": [item.id for item in self._members()],
            "data_handling_policy_id": self.data_handling_policy_id,
            "hostile_content_policy_id": self.hostile_content_policy_id,
            "observed_units": list(self.observed_units),
            "transport_metadata_digest": canonical_digest(self.transport_metadata),
        })

    def document(self) -> dict[str, Any]:
        """The portable form. This, not the Python object, is the artifact.

        An adapter conforms by emitting one of these. It may be written in any
        language: the dataclasses in this module are one carrier for the
        records, never the contract.
        """
        return {
            "profile": PROFILE_ID,
            "profile_version": PROFILE_VERSION,
            "document_version": DOCUMENT_VERSION,
            "bundle": asdict(self),
        }

    @classmethod
    def from_document(cls, document: Any) -> "Bundle":
        """Read a document, or refuse. Never partially read one."""
        if not isinstance(document, Mapping):
            raise BundleError(f"a bundle document must be a mapping, got {type(document).__name__}")
        expected = {
            "profile": PROFILE_ID,
            "profile_version": PROFILE_VERSION,
            "document_version": DOCUMENT_VERSION,
        }
        unknown = sorted(set(document) - set(expected) - {"bundle"})
        if unknown:
            raise BundleError(f"document carries undeclared keys: {', '.join(unknown)}")
        for key, value in expected.items():
            if key not in document:
                raise BundleError(f"document does not declare '{key}'")
            if document[key] != value:
                raise BundleError(
                    f"document declares {key}={document[key]!r}; this reader verifies "
                    f"{value!r} and will not guess at the difference"
                )
        if not isinstance(document["document_version"], int) or isinstance(
            document["document_version"], bool
        ):
            raise BundleError("document_version must be an integer")
        if "bundle" not in document:
            raise BundleError("document carries no bundle")
        payload = document["bundle"]
        if not isinstance(payload, Mapping):
            raise BundleError("document bundle must be a mapping")
        declared = {f.name for f in fields(cls)}
        unknown = sorted(set(payload) - declared)
        if unknown:
            raise BundleError(f"bundle carries undeclared keys: {', '.join(unknown)}")
        if "source_class" not in payload:
            raise BundleError("bundle declares no source class")
        built: dict[str, Any] = {
            "source_class": _construct(SourceClass, payload["source_class"], "source_class"),
        }
        for name, plane in _PLANES.items():
            if name not in payload:
                continue
            items = payload[name]
            if not isinstance(items, (list, tuple)):
                raise BundleError(f"{name} must be an array")
            built[name] = tuple(
                _construct(plane, item, f"{name}[{index}]")
                for index, item in enumerate(items)
            )
        for name in set(payload) - set(built):
            built[name] = (
                tuple(payload[name])
                if name in _TUPLE_FIELDS and isinstance(payload[name], list)
                else payload[name]
            )
        return _construct(cls, built, "bundle")

    def _members(self) -> tuple[Any, ...]:
        return (
            *self.sources, *self.rasters, *self.regions, *self.attempts,
            *self.hypotheses, *self.corrections, *self.selections,
        )

    def by_id(self, kind: str) -> dict[str, Any]:
        return {item.id: item for item in getattr(self, kind)}


# Plane name to carrier, read by `Bundle.from_document`. Declared after the
# classes it names, and after Bundle, so the module has one reading order.
_PLANES: dict[str, type] = {
    "sources": SourceRepresentation,
    "rasters": Raster,
    "regions": Region,
    "attempts": OCRAttempt,
    "hypotheses": Hypothesis,
    "corrections": ReviewCorrection,
    "selections": Selection,
}


# Required here means required at the portable-document boundary. Some fields
# map to required ontology slots. The collection fields also stay explicit so
# an author-declared empty collection remains distinguishable from an omitted
# collection the reader invented. Carrier defaults are only an ergonomic path
# for constructing a new in-memory bundle.
_DOCUMENT_REQUIRED_FIELDS: dict[type, frozenset[str]] = {
    SourceClass: frozenset({
        "id", "required_units", "metric_families", "temporal_policy", "frozen_at",
        "inventory_basis",
    }),
    SourceRepresentation: frozenset({"id", "digest", "byte_length", "media_type", "locator"}),
    Raster: frozenset({"id", "source_id", "unit", "digest", "render_contract"}),
    Region: frozenset({"id", "raster_id", "selector", "selector_profile"}),
    OCRAttempt: frozenset({"id", "region_id", "request_digest", "config_identity", "status"}),
    Hypothesis: frozenset({"id", "region_id", "text_digest"}),
    ReviewCorrection: frozenset({"id", "reviewed_hypothesis_id", "reviewer_id", "verdict"}),
    Selection: frozenset({
        "id", "region_id", "candidate_ids", "selected_id", "reason", "human_verified",
    }),
    Bundle: frozenset({
        "id", "source_class", "kind", "sources", "rasters", "regions", "attempts",
        "hypotheses", "corrections", "selections", "observed_units",
        "data_handling_policy_id", "hostile_content_policy_id", "transport_metadata",
    }),
}

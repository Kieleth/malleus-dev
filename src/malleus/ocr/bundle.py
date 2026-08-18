"""The portable object model for a document evidence bundle.

Every object here is one identity plane. The planes exist so that a change in
one cannot silently rewrite another: correcting a reading must not move the
region it read, and a retry must not overwrite the attempt before it.

Digests reuse `malleus.ledger.canonical_json`, so a bundle object hashes the
same way a protocol record does. Nothing in this module writes to a ledger.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Mapping

from malleus.ledger import canonical_json

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


@dataclass(frozen=True)
class SourceRepresentation:
    """Exact original bytes. Never replaced by a normalized derivative."""

    id: str
    digest: str
    byte_length: int
    media_type: str
    locator: str


@dataclass(frozen=True)
class Raster:
    """A rendering derived from a source. Derived, never a replacement."""

    id: str
    source_id: str
    digest: str
    render_contract: str


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


@dataclass(frozen=True)
class ReviewCorrection:
    """Append-only human review. Overwrites nothing."""

    id: str
    reviewed_hypothesis_id: str
    reviewer_id: str
    verdict: str
    corrected_text_digest: str | None = None
    predecessor_id: str | None = None


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


@dataclass(frozen=True)
class Bundle:
    """A portable document evidence bundle at capability AUDIT_ONLY."""

    id: str
    source_class: SourceClass
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

    def by_id(self, kind: str) -> dict[str, Any]:
        return {item.id: item for item in getattr(self, kind)}

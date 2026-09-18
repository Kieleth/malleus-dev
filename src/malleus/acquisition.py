"""Read-only coverage of explicitly declared interpretation reviews.

This optional experimental profile checks identities and supplied dispositions,
not whether a reviewer understood evidence correctly. It neither reads a graph
nor writes a ledger. Consumers must explicitly gate completion with
``check_review_coverage(...).require_complete()`` and supply the actual current
boundary. The input grammar is exposed in ``REVIEW_COVERAGE_PROFILE``; it is not
a stable wire or a replacement for Assent review, policy or admission.
"""

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path
from typing import Sequence

from malleus.ledger import LedgerError, canonical_json


class ReviewCoverageRefusalReason(str, Enum):
    """Input refusal versus an explicit incomplete-review assertion."""

    MALFORMED_INPUT = "MALFORMED_INPUT"
    UNSUPPORTED_GRAMMAR = "UNSUPPORTED_GRAMMAR"
    DUPLICATE_ID = "DUPLICATE_ID"
    UNKNOWN_INTERPRETATION = "UNKNOWN_INTERPRETATION"
    UNDECLARED_REFERENCE = "UNDECLARED_REFERENCE"
    INCOMPLETE_REVIEW = "INCOMPLETE_REVIEW"


class ReviewCoverageRefusal(ValueError):
    """A malformed request or a refused review-completion claim."""

    def __init__(self, reason: ReviewCoverageRefusalReason, detail: str):
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.value}: {detail}")


def _malformed(detail):
    return ReviewCoverageRefusal(ReviewCoverageRefusalReason.MALFORMED_INPUT, detail)


def _canonical(value):
    try:
        return canonical_json(value).encode("utf-8")
    except (LedgerError, RecursionError) as error:
        raise _malformed(f"canonical JSON required: {error}") from error


def _identity(value):
    return "sha256:" + sha256(_canonical(value)).hexdigest()


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise _malformed(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _nonfinite(value):
    raise _malformed(f"non-finite JSON number: {value}")


def _decode(data):
    if type(data) is not bytes:
        raise _malformed("exact JSON bytes required")
    try:
        value = json.loads(
            data, object_pairs_hook=_unique_object, parse_constant=_nonfinite
        )
        _canonical(value)
    except (ValueError, RecursionError) as error:
        if isinstance(error, ReviewCoverageRefusal):
            raise
        raise _malformed(f"invalid JSON: {error}") from error
    if type(value) is not dict:
        raise _malformed("JSON object required")
    return value


_PROFILE = _decode(
    Path(__file__)
    .with_name("profiles")
    .joinpath("interpretation-review.json")
    .read_bytes()
)
REVIEW_COVERAGE_PROFILE = _canonical(_PROFILE)
"""Canonical installed profile bytes, including input shapes and outcome rules."""
REVIEW_COVERAGE_PROFILE_IDENTITY = _identity(_PROFILE)


_BOUNDARY_IDENTITY_ROUTE = (
    "; it is the boundary's identity digest, never its id: read it from "
    "malleus.acquisition.review_boundary_identity(boundary_bytes=...)"
)


def _object(value, kind, where):
    fields = _PROFILE["objects"][kind]
    if type(value) is not dict or set(value) != set(fields):
        raise _malformed(f"{where}: expected exactly {sorted(fields)}")
    return {
        key: _typed(value[key], rule, f"{where}.{key}") for key, rule in fields.items()
    }


def _typed(value, kind, where):
    if kind.endswith("?"):
        return None if value is None else _typed(value, kind[:-1], where)
    if kind in {"text", "digest"}:
        if type(value) is not str or not value.strip():
            raise _malformed(f"{where}: nonblank text required")
        if kind == "digest" and not (
            value.startswith("sha256:")
            and len(value) == 71
            and all(char in "0123456789abcdef" for char in value[7:])
        ):
            route = (
                _BOUNDARY_IDENTITY_ROUTE if where.endswith("boundary_identity") else ""
            )
            raise _malformed(f"{where}: lowercase SHA-256 identity required{route}")
        return value
    if kind in {"refs", "refs+"}:
        if type(value) is not list or (kind == "refs+" and not value):
            raise _malformed(f"{where}: {kind} requires a reference list")
        refs = [_object(item, "reference", where) for item in value]
        if len({item["id"] for item in refs}) != len(refs):
            raise ReviewCoverageRefusal(
                ReviewCoverageRefusalReason.DUPLICATE_ID,
                f"{where}: repeated reference ID",
            )
        return sorted(refs, key=lambda item: item["id"])
    return _object(value, kind, where)


def _parse(data, kind):
    value = _object(_decode(data), kind, kind)
    if value["schema"] != _PROFILE["grammars"][kind]:
        raise ReviewCoverageRefusal(
            ReviewCoverageRefusalReason.UNSUPPORTED_GRAMMAR,
            f"{kind}: expected {_PROFILE['grammars'][kind]}",
        )
    return value


def _context(boundary):
    refs = [
        *boundary["evidence"],
        *boundary["dependencies"],
        *boundary["interpretations"],
        *(
            item
            for item in (boundary["ontology"], boundary["knowledge"])
            if item is not None
        ),
    ]
    context = {}
    for item in refs:
        if item["id"] in context and context[item["id"]] != item["sha256"]:
            raise _malformed(f"conflicting reference identity: {item['id']}")
        context[item["id"]] = item["sha256"]
    return context


@dataclass(frozen=True, slots=True)
class ReviewCoverage:
    """Immutable accounting receipt, not an attestation of semantic correctness.

    ``document`` returns a defensive JSON value. Its ``groups`` preserve current
    review rationales, open issues and proposed changes. Missing/stale reviews
    are separate. The receipt binds inputs, but does not authenticate them.
    """

    canonical_bytes: bytes

    @property
    def document(self) -> dict:
        return json.loads(self.canonical_bytes)

    @property
    def identity(self) -> str:
        return "sha256:" + sha256(self.canonical_bytes).hexdigest()

    @property
    def boundary_identity(self) -> str:
        return self.document["boundary_identity"]

    @property
    def profile_identity(self) -> str:
        return self.document["profile_identity"]

    @property
    def missing(self) -> tuple[str, ...]:
        return tuple(self.document["missing"])

    @property
    def stale(self) -> tuple[str, ...]:
        return tuple(self.document["stale"])

    @property
    def complete(self) -> bool:
        return self.document["complete"]

    def require_complete(self) -> "ReviewCoverage":
        """Refuse an incomplete declared review boundary, without writing."""
        if not self.complete:
            raise ReviewCoverageRefusal(
                ReviewCoverageRefusalReason.INCOMPLETE_REVIEW,
                f"missing={list(self.missing)}; stale={list(self.stale)}",
            )
        return self


def check_review_coverage(
    *, boundary_bytes: bytes, review_bytes: Sequence[bytes]
) -> ReviewCoverage:
    """Check one declared boundary and its explicit selection of review bytes.

    Use an empty tuple of reviews to obtain the normalized boundary identity
    before authoring reviews. ``review_bytes`` must be a list or tuple, not a
    history to search for a preferred outcome. Unknown/duplicate subjects refuse;
    missing/stale reviews return incomplete coverage. Call ``require_complete``
    before asserting this selected review boundary is complete.

    No source fetching, truth evaluation, policy selection, graph access, or
    persistence occurs. A caller supplying an obsolete boundary will obtain
    coverage relative to that obsolete declaration, not detection of new evidence.
    """
    boundary = _parse(boundary_bytes, "boundary")
    context = _context(boundary)
    boundary_identity = _identity(boundary)
    expected = {item["id"]: item["sha256"] for item in boundary["interpretations"]}
    if type(review_bytes) not in (list, tuple):
        raise _malformed("review_bytes must be an explicit list or tuple of bytes")
    reviews = sorted(
        (_parse(raw, "review") for raw in review_bytes), key=lambda r: r["id"]
    )
    seen_ids, seen_targets = set(), set()
    stale = []
    groups = {rule["group"]: [] for rule in _PROFILE["outcomes"].values()}
    for item in reviews:
        target = item["interpretation"]["id"]
        if item["id"] in seen_ids or target in seen_targets:
            raise ReviewCoverageRefusal(
                ReviewCoverageRefusalReason.DUPLICATE_ID,
                f"one review ID and one review per interpretation required: {item['id']}, {target}",
            )
        seen_ids.add(item["id"])
        seen_targets.add(target)
        if target not in expected:
            raise ReviewCoverageRefusal(
                ReviewCoverageRefusalReason.UNKNOWN_INTERPRETATION, target
            )
        if item["outcome"] not in _PROFILE["outcomes"]:
            raise _malformed(f"unknown review outcome: {item['outcome']}")
        rule = _PROFILE["outcomes"][item["outcome"]]
        if any(item[field] is None for field in rule["requires"]) or any(
            item[field] is not None for field in rule["forbids"]
        ):
            raise _malformed(
                f"{item['id']}: outcome requires {rule['requires']}, forbids {rule['forbids']}"
            )
        if (
            item["boundary_identity"] != boundary_identity
            or item["interpretation"]["sha256"] != expected[target]
        ):
            stale.append(target)
            continue
        for reference in (*item["supporting_references"], *item["affected_uses"]):
            if (
                reference["id"] not in context
                or context[reference["id"]] != reference["sha256"]
            ):
                raise ReviewCoverageRefusal(
                    ReviewCoverageRefusalReason.UNDECLARED_REFERENCE,
                    f"{item['id']}: reference not in current boundary: {reference['id']}",
                )
        groups[rule["group"]].append(item)
    missing = sorted(set(expected) - seen_targets)
    return ReviewCoverage(
        _canonical(
            {
                "schema": _PROFILE["grammars"]["receipt"],
                "profile_identity": REVIEW_COVERAGE_PROFILE_IDENTITY,
                "boundary_identity": boundary_identity,
                "review_identities": [
                    {"id": item["id"], "sha256": _identity(item)} for item in reviews
                ],
                "complete": not missing and not stale,
                "missing": missing,
                "stale": sorted(stale),
                "groups": groups,
            }
        )
    )


def review_boundary_identity(*, boundary_bytes: bytes) -> str:
    """Return the identity every review of this boundary must carry.

    A review's ``boundary_identity`` is the digest of the normalized boundary,
    never the boundary's own ``id``. Authoring a review requires the digest
    first, so this names the route that was previously reachable only by calling
    ``check_review_coverage`` with an empty review tuple and reading the receipt.

    It normalizes and refuses exactly as the checker does, reads no source and
    writes nothing. An obsolete boundary yields that obsolete boundary's
    identity; it does not detect later evidence.
    """
    return check_review_coverage(
        boundary_bytes=boundary_bytes, review_bytes=()
    ).boundary_identity


__all__ = [
    "REVIEW_COVERAGE_PROFILE",
    "REVIEW_COVERAGE_PROFILE_IDENTITY",
    "ReviewCoverage",
    "ReviewCoverageRefusal",
    "ReviewCoverageRefusalReason",
    "check_review_coverage",
    "review_boundary_identity",
]

"""OCR evidence-integrity profile: verification, not perception.

This package does not perform OCR. It renders nothing, calls no provider and
selects no engine. It verifies that a document evidence bundle produced by
somebody else's OCR stack preserves the lineage from an accepted reading back
to the exact source bytes, and refuses when it does not.

The name says `ocr` because that is the first profile. Only one plane here is
OCR-specific: the region selector, and decision C1 makes that swappable. Bring
audio and you replace the selector profile while the identity planes, digest
rules, staleness semantics and coverage declarations stand unchanged.

The artifact is the bundle document, not the Python object. `Bundle.document()`
and `Bundle.from_document()` are the boundary, `malleus-ocr` verifies one from
the command line, and `malleus-ocr --conformance` runs the packaged cases. An
adapter conforms by emitting a document; it may be written in any language.

The authority for this vocabulary is `ontology/domains/ocr.yaml`. Every plane
is a typed record under a root primitive, and `verify_bundle` validates each
one through `KnowledgeGraph` before it runs a profile check. The dataclasses
here are a carrier: they answer `record()` and hold no meaning the schema does
not declare.

Decisions governing this package are recorded in
`design/OCR_EVIDENCE_INTEGRITY_DECISIONS.md` (`OCR-D001`). Capability level is
`AUDIT_ONLY`: nothing here writes to a protocol ledger, because human review
has no ledger event door and `review-report-recording` remains unimplemented.
"""

from malleus.ocr.bundle import (
    Bundle,
    Hypothesis,
    OCRAttempt,
    Raster,
    Region,
    ReviewCorrection,
    Selection,
    SourceClass,
    SourceRepresentation,
    canonical_digest,
)
from malleus.ocr.verify import (
    CAPABILITY,
    Diagnostic,
    VerificationResult,
    profile_registry,
    verify_bundle,
)

__all__ = [
    "Bundle",
    "CAPABILITY",
    "Diagnostic",
    "Hypothesis",
    "OCRAttempt",
    "Raster",
    "Region",
    "ReviewCorrection",
    "Selection",
    "SourceClass",
    "SourceRepresentation",
    "VerificationResult",
    "canonical_digest",
    "profile_registry",
    "verify_bundle",
]

"""Verify a document evidence bundle. Refuse rather than repair.

Every check here traces to a decision in
`design/OCR_EVIDENCE_INTEGRITY_DECISIONS.md`. A check that cannot be traced to
a decision does not belong in the profile, and a decision with no check is
prose.

The verifier proves source-to-reading lineage and the separation of identity
planes. It does not prove source authenticity, factual truth, quote fairness,
or that a reading is correct. Those need separate evidence and the profile
says so rather than implying otherwise.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from malleus.kg import KnowledgeGraph, OpStatus
from malleus.ocr.bundle import DIGEST, SECRET_KEYS, Bundle
from malleus.ontology import OntologyRegistry, bundled_ontology_path

CAPABILITY = "AUDIT_ONLY"

# Profile-local diagnostics. Deliberately NOT core MonitorErrorCode values:
# the core vocabulary is closed and a profile may map into it only through an
# explicit adapter contract, which AUDIT_ONLY does not have.
CODES = {
    "OCR-D001": "an integrity value is not a full algorithm-tagged digest",
    "OCR-D002": "credential-shaped material is present in the bundle",
    "OCR-D003": "a reading has no resolvable path to source bytes",
    "OCR-D004": "a corrected reading moved the region identity",
    "OCR-D005": "two attempts share an identity",
    "OCR-D006": "a correction reviews a hypothesis the bundle does not retain",
    "OCR-D007": "a hypothesis origin is ambiguous or absent",
    "OCR-D008": "a selection claims human verification with no review record",
    "OCR-D009": "the source class is not frozen before ingest",
    "OCR-D010": "a required policy declaration is unbound",
    "OCR-D011": "a selection names a hypothesis it did not consider",
    "OCR-D012": "no coverage metric family is declared",
    "OCR-D013": "a bundle record violates the profile ontology",
}

ONTOLOGY = ("domains", "ocr.yaml")

# Entities before events, the order KnowledgeGraph replays record families in.
PLANES: tuple[tuple[str, str, str], ...] = (
    ("source_class", "SourceClass", "entity"),
    ("sources", "SourceRepresentation", "entity"),
    ("rasters", "Raster", "entity"),
    ("regions", "Region", "entity"),
    ("hypotheses", "Hypothesis", "entity"),
    ("selections", "Selection", "entity"),
    ("bundle", "EvidenceBundle", "entity"),
    ("attempts", "OCRAttempt", "event"),
    ("corrections", "ReviewCorrection", "event"),
)


def profile_registry() -> OntologyRegistry:
    """The ontology that governs this profile.

    Constructed from the schema shipped with the package, the way
    `malleus.recon` constructs its own. Pass a different registry to
    `verify_bundle` to run a bundle against a different profile version; the
    default receives no privilege the replacement lacks.
    """
    return OntologyRegistry(bundled_ontology_path(*ONTOLOGY))


@dataclass(frozen=True)
class Diagnostic:
    code: str
    subject: str
    detail: str

    def __str__(self) -> str:
        return f"{self.code} [{self.subject}] {CODES[self.code]}: {self.detail}"


@dataclass(frozen=True)
class VerificationResult:
    bundle_id: str
    capability: str
    diagnostics: tuple[Diagnostic, ...]

    @property
    def conforms(self) -> bool:
        return not self.diagnostics

    def codes(self) -> tuple[str, ...]:
        return tuple(d.code for d in self.diagnostics)


def _walk(value: Any, path: str = ""):
    if isinstance(value, Mapping):
        for key, item in value.items():
            yield path, str(key), item
            yield from _walk(item, f"{path}.{key}" if path else str(key))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            yield from _walk(item, f"{path}[{index}]")


def verify_bundle(
    bundle: Bundle,
    registry: OntologyRegistry | None = None,
) -> VerificationResult:
    """Run every profile check. Collect all diagnostics; never stop at the first."""
    out: list[Diagnostic] = []

    def add(code: str, subject: str, detail: str) -> None:
        out.append(Diagnostic(code, subject, detail))

    # Write-time validation first. Every plane is a typed record under the
    # root primitives, and the registry refuses an unknown property, a missing
    # required slot, a value outside a closed enum or a range violation. The
    # checks below it are the cross-plane questions a schema cannot ask.
    graph = KnowledgeGraph(registry if registry is not None else profile_registry())
    for attribute, type_name, family in PLANES:
        if attribute == "bundle":
            objects: tuple[Any, ...] = (bundle,)
        else:
            value = getattr(bundle, attribute)
            objects = value if isinstance(value, tuple) else (value,)
        create = graph.create_entity if family == "entity" else graph.create_event
        for item in objects:
            record = item.record()
            operation = create(type_name, record["id"], {
                key: value for key, value in record.items() if key != "id"
            })
            if operation.op_status is OpStatus.REJECTED:
                add("OCR-D013", record["id"], f"{type_name}: {operation.rejection_reason}")

    sources = bundle.by_id("sources")
    rasters = bundle.by_id("rasters")
    regions = bundle.by_id("regions")
    attempts = bundle.by_id("attempts")
    hypotheses = bundle.by_id("hypotheses")
    corrections = bundle.by_id("corrections")

    # C6: full algorithm-tagged digests. A truncated value may be displayed and
    # may never be an integrity value.
    for kind, items in (("sources", bundle.sources), ("rasters", bundle.rasters)):
        for item in items:
            if not DIGEST.fullmatch(item.digest):
                add("OCR-D001", item.id, f"{kind} digest {item.digest!r}")
    for attempt in bundle.attempts:
        for label, value in (("request", attempt.request_digest),
                             ("response", attempt.response_digest)):
            if value is not None and not DIGEST.fullmatch(value):
                add("OCR-D001", attempt.id, f"{label} digest {value!r}")
    for hypothesis in bundle.hypotheses:
        if not DIGEST.fullmatch(hypothesis.text_digest):
            add("OCR-D001", hypothesis.id, f"text digest {hypothesis.text_digest!r}")

    # C6: credentials never enter the bundle, detected rather than trusted.
    for scope, blob in (("transport_metadata", bundle.transport_metadata),
                        *((a.id, a.config_identity) for a in bundle.attempts)):
        for _, key, _ in _walk(blob):
            if key.lower() in SECRET_KEYS:
                add("OCR-D002", scope, f"key {key!r}")

    # Identity planes: a reading must reach the pixels it claims to have read.
    for hypothesis in bundle.hypotheses:
        region = regions.get(hypothesis.region_id)
        if region is None:
            add("OCR-D003", hypothesis.id, f"unknown region {hypothesis.region_id!r}")
            continue
        raster = rasters.get(region.raster_id)
        if raster is None:
            add("OCR-D003", hypothesis.id, f"unknown raster {region.raster_id!r}")
            continue
        if raster.source_id not in sources:
            add("OCR-D003", hypothesis.id, f"unknown source {raster.source_id!r}")

    # A hypothesis has exactly one origin, so provenance is never ambiguous.
    for hypothesis in bundle.hypotheses:
        origins = [o for o in (hypothesis.attempt_id, hypothesis.correction_id) if o]
        if len(origins) != 1:
            add("OCR-D007", hypothesis.id, f"{len(origins)} origins declared")
            continue
        if hypothesis.attempt_id and hypothesis.attempt_id not in attempts:
            add("OCR-D003", hypothesis.id, f"unknown attempt {hypothesis.attempt_id!r}")
        if hypothesis.correction_id and hypothesis.correction_id not in corrections:
            add("OCR-D003", hypothesis.id, f"unknown correction {hypothesis.correction_id!r}")

    # Attempts never collapse. Retries are separate records, not overwrites.
    seen: set[str] = set()
    for attempt in bundle.attempts:
        if attempt.id in seen:
            add("OCR-D005", attempt.id, "duplicate attempt identity")
        seen.add(attempt.id)

    # A correction preserves what it reviewed, and does not move the region.
    for correction in bundle.corrections:
        reviewed = hypotheses.get(correction.reviewed_hypothesis_id)
        if reviewed is None:
            add("OCR-D006", correction.id,
                f"reviewed hypothesis {correction.reviewed_hypothesis_id!r} absent")
            continue
        for child in bundle.hypotheses:
            if child.correction_id == correction.id and child.region_id != reviewed.region_id:
                add("OCR-D004", child.id,
                    f"region moved {reviewed.region_id!r} -> {child.region_id!r}")

    # Selections consider what they select, and cannot invent human review.
    reviewed_hypotheses = {c.reviewed_hypothesis_id for c in bundle.corrections}
    corrected = {h.id for h in bundle.hypotheses if h.correction_id}
    for selection in bundle.selections:
        if selection.selected_id not in selection.candidate_ids:
            add("OCR-D011", selection.id,
                f"selected {selection.selected_id!r} not among candidates")
        for candidate in selection.candidate_ids:
            if candidate not in hypotheses:
                add("OCR-D011", selection.id, f"unknown candidate {candidate!r}")
        if selection.human_verified and not (
            selection.selected_id in corrected or selection.selected_id in reviewed_hypotheses
        ):
            add("OCR-D008", selection.id,
                f"{selection.selected_id!r} carries no review record")

    # C8 and the declaration half of C3 and C4: the source class is frozen
    # before ingest and names its metric families. This is NOT C3. C3 measures
    # coverage against those families and their thresholds, and no code here
    # does that. Citing a decision beside a check that does not perform it is
    # how C3 came to look discharged.
    source_class = bundle.source_class
    if not source_class.frozen_at.strip():
        add("OCR-D009", source_class.id, "no frozen_at recorded")
    if not source_class.metric_families:
        add("OCR-D012", source_class.id, "coverage metric families empty")

    # C5: policy declarations are mandatory and bound. Their content is the
    # adopter's; their existence is the profile's.
    for label, value in (("data_handling", bundle.data_handling_policy_id),
                         ("hostile_content", bundle.hostile_content_policy_id)):
        if not value:
            add("OCR-D010", bundle.id, f"{label} policy unbound")

    return VerificationResult(bundle.id, CAPABILITY, tuple(out))


# C7: staleness is two properties. Invalidation follows bytes; currency
# follows configuration. Collapsing them would make engine comparison
# impossible, because the older reading would be stale by definition.
INVALIDATING = ("source_digest", "raster_digest")
DEMOTING = ("prompt", "model", "ontology", "mapping", "policy")


def currency_verdict(before: Mapping[str, str], after: Mapping[str, str]) -> str:
    """Compare two reading configurations.

    INVALIDATED: the bytes changed, so prior readings describe pixels that no
    longer exist and are void. DEMOTED: the configuration changed, so prior
    readings remain valid observations of the same bytes and are no longer
    current, which triggers re-review without destroying anything. CURRENT:
    nothing relevant moved.
    """
    changed = {key for key in set(before) | set(after) if before.get(key) != after.get(key)}
    if changed & set(INVALIDATING):
        return "INVALIDATED"
    if changed & set(DEMOTING):
        return "DEMOTED"
    return "CURRENT"


def profile_projection() -> dict:
    """The published projection of this profile.

    Derived from CODES above, which is the authority. The JSON under
    `conformance/ocr/v0/` is generated from this and is not shipped in the
    distribution: an adopter reads the registry from the module, never from a
    projection that could drift.
    """
    return {
        "profile_id": "malleus.ocr.evidence_integrity",
        "profile_version": "v0",
        "capability": CAPABILITY,
        "ontology": "ontology/domains/ocr.yaml",
        "decision_record": "design/OCR_EVIDENCE_INTEGRITY_DECISIONS.md",
        "selector_profile_default": "w3c-web-annotation+iiif",
        "selector_profile_replaceable": True,
        "diagnostics": dict(sorted(CODES.items())),
        "proves": [
            "source-to-reading lineage",
            "separation of identity planes",
            "declared coverage and policy precommitment",
            "every plane typed under the malleus root primitives",
        ],
        "does_not_prove": [
            "source authenticity",
            "factual truth of a reading",
            "quote fairness or representativeness",
            "downstream consequence",
        ],
    }

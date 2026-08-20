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
from malleus.ontology import OntologyError, OntologyRegistry, bundled_ontology_path

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
    "OCR-D014": "a rendering claims a unit the bundle does not observe",
    "OCR-D015": "a declared state and the detail it requires disagree",
}

# Every reference one plane makes to another, walked regardless of what points
# at the holder. Lineage used to be traced from readings outward, so a plane
# nothing referenced was never examined: a region over a missing raster and a
# raster over a missing source both took a purity seal. An unexamined record is
# not thereby sound, and the bundle is the unit of verification, not the
# reading. `optional` references are skipped when unset rather than refused.
REFERENCES: tuple[tuple[str, str, str, bool], ...] = (
    ("rasters", "source_id", "sources", False),
    ("regions", "raster_id", "rasters", False),
    ("attempts", "region_id", "regions", False),
    ("hypotheses", "region_id", "regions", False),
    ("hypotheses", "attempt_id", "attempts", True),
    ("hypotheses", "correction_id", "corrections", True),
    ("selections", "region_id", "regions", False),
    ("selections", "selected_id", "hypotheses", False),
    ("corrections", "predecessor_id", "corrections", True),
)

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


# What happened to one declared unit. Mandate B2: verified blank, unreadable,
# unavailable, failed, excluded and absent stay distinct, and none may be
# padded, snapped or converted into another. NOT_OBSERVED, NOT_RENDERED and
# NOT_ATTEMPTED are the three ways a unit goes unaccounted for, kept apart for
# the same reason: "we never fetched it", "we have it and never rendered it"
# and "we rendered it and never looked" are different failures with different
# fixes.
#
# The vocabulary itself is NOT declared here. It used to be, as a module tuple
# that nothing read, and the cost was exact: ABSENT sat in that tuple for a
# release while `_unit_outcome` could not produce it, so a reviewer stating a
# page is not in the source got the page reported READ. A vocabulary no code
# consults cannot notice that one of its values is unreachable. The enums in
# `ontology/domains/ocr.yaml` are the authority now and `outcome_dispositions`
# reads them.
READ = "READ"

# The three-valued answer. Not a bool: "we looked and can say what we found",
# "nobody looked" and "somebody looked and the look failed" are three answers,
# and a boolean makes two of them share a word.
ACCOUNTED = "ACCOUNTED"
NOT_CHECKED = "NOT_CHECKED"
CHECK_FAILED = "CHECK_FAILED"

DISPOSITION_ENUM = "UnitDisposition"

# The closed-world mapping, one enum per disposition. Declared in the schema
# and read back, rather than assumed by whoever wrote the last branch.
OUTCOME_ENUMS = {
    ACCOUNTED: "AccountedUnitOutcome",
    NOT_CHECKED: "NotCheckedUnitOutcome",
    CHECK_FAILED: "CheckFailedUnitOutcome",
}

# Denominators this profile can compute. A family naming anything else is
# reported UNMEASURED rather than quietly passing, because an unmeasured
# metric that reads as a pass is worse than a missing one.
DENOMINATORS = {"declared_units"}


def outcome_dispositions(registry: OntologyRegistry | None = None) -> dict[str, str]:
    """The declared mapping from a unit outcome to its disposition.

    Read from the ontology, never assumed here. Refuses rather than repairs: a
    disposition with no outcome enum, an outcome claimed by two dispositions,
    or a disposition the schema does not declare are all schema errors, and
    guessing which one was meant is how a census acquires a value nobody
    declared.
    """
    registry = registry if registry is not None else profile_registry()
    declared = registry.get_enum_values(DISPOSITION_ENUM)
    unmapped = sorted(set(declared) - set(OUTCOME_ENUMS))
    if unmapped:
        raise OntologyError(
            f"{DISPOSITION_ENUM} declares {unmapped} with no outcome enum to fill them"
        )
    mapping: dict[str, str] = {}
    for disposition, enum_name in OUTCOME_ENUMS.items():
        if disposition not in declared:
            raise OntologyError(
                f"'{disposition}' is not a value of {DISPOSITION_ENUM}"
            )
        for outcome in registry.get_enum_values(enum_name):
            if outcome in mapping:
                raise OntologyError(
                    f"outcome '{outcome}' carries two dispositions: "
                    f"{mapping[outcome]} and {disposition}"
                )
            mapping[outcome] = disposition
    return mapping


@dataclass(frozen=True)
class UnitAccount:
    """One declared unit, what became of it, and which of the three that is."""

    unit: str
    outcome: str
    disposition: str

    @property
    def accounted(self) -> bool:
        """Accounted means somebody looked and can say what they found.

        A blank page that was read and found blank is accounted for. So is one
        ruled out of scope, and so is one a reviewer states is not in the
        source at all. A page nobody opened is not, however sound the
        paperwork around it, and neither is one whose only attempt failed.

        Kept as a bit because the coverage numerator is a count. It is derived
        from the disposition and is not the authority: a caller asking why a
        unit is unaccounted reads `disposition`, which distinguishes the unit
        nobody fetched from the one whose call died.
        """
        return self.disposition == ACCOUNTED


@dataclass(frozen=True)
class MetricResult:
    """One precommitted measure, its value, and whether it met its own bar."""

    family: str
    denominator: str
    value: float | None
    threshold: float | None
    verdict: str  # MET, UNMET, or UNMEASURED

    def __str__(self) -> str:
        if self.value is None:
            return f"{self.family}: UNMEASURED (denominator {self.denominator!r} is not computable here)"
        return (f"{self.family}: {self.value:.3f} against {self.threshold} "
                f"over {self.denominator} -> {self.verdict}")


@dataclass(frozen=True)
class Account:
    """What was covered. Separate from whether the paperwork holds together.

    Integrity is a bit: a reading either reaches its pixels or it does not.
    Coverage is a census and cannot be one, which is why they are two answers.
    A bundle passing integrity while accounting for nothing was taking a seal
    that meant only "nothing in here is wrong".
    """

    kind: str
    units: tuple[UnitAccount, ...]
    metrics: tuple[MetricResult, ...]

    @property
    def unaccounted(self) -> tuple[str, ...]:
        return tuple(u.unit for u in self.units if not u.accounted)

    def units_with(self, disposition: str) -> tuple[str, ...]:
        """The units carrying one disposition.

        `unaccounted` is the union of the two negative dispositions and cannot
        say which. A caller acting on the answer needs to: an unfetched unit is
        fetched, a failed call is retried, and reporting both as "unaccounted"
        hands the operator one word for two jobs.
        """
        return tuple(u.unit for u in self.units if u.disposition == disposition)

    @property
    def complete(self) -> bool:
        """Every declared bar met, judged against the adopter's own thresholds.

        Deliberately not "every unit accounted for". An adopter who froze a
        coverage threshold of 0.5 said half is enough for their purpose, and
        adding an all-units rule on top would make their declaration
        decorative and put our bar back over theirs. That substitution is the
        error this whole design replaced.

        A source class declaring no measure cannot be complete: with nothing
        declared there is no bar to meet, and an empty `all()` would otherwise
        certify a bundle nobody measured. OCR-D012 refuses that source class
        anyway; this does not rely on it.

        A registration is never complete. It claims no reading, so there is
        nothing for completeness to be true of, and it may never stand as
        evidence that an adapter conforms.
        """
        if self.kind != "FINISHED_READING" or not self.metrics:
            return False
        return all(m.verdict == "MET" for m in self.metrics)


@dataclass(frozen=True)
class VerificationResult:
    bundle_id: str
    capability: str
    diagnostics: tuple[Diagnostic, ...]
    account: Account

    @property
    def conforms(self) -> bool:
        """The paperwork holds together. Says nothing about what was read."""
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
    registry = registry if registry is not None else profile_registry()
    graph = KnowledgeGraph(registry)
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

    # Identity planes: every reference resolves, whoever made it. A reading
    # must reach the pixels it claims to have read, and a plane no reading
    # touches must still point at something that exists.
    by_plane = {
        "sources": sources, "rasters": rasters, "regions": regions,
        "attempts": attempts, "hypotheses": hypotheses, "corrections": corrections,
        "selections": bundle.by_id("selections"),
    }
    for plane, attribute, target, optional in REFERENCES:
        known = by_plane[target]
        for item in getattr(bundle, plane):
            referenced = getattr(item, attribute)
            if referenced is None and optional:
                continue
            if referenced not in known:
                add("OCR-D003", item.id,
                    f"{attribute} names {referenced!r}, absent from {target}")

    # A rendering names the unit it renders, and a unit the bundle does not
    # observe cannot have been rendered from bytes the bundle holds. Without
    # this a typo in a unit name silently reports the page as never rendered.
    for raster in bundle.rasters:
        if raster.unit not in bundle.observed_units:
            add("OCR-D014", raster.id,
                f"unit {raster.unit!r} is not among the observed units")

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

    # C1 (roadmap): a state and the detail it requires must agree. The schema
    # can say a slot is required; it cannot say "required when the status is
    # UNAVAILABLE", and LinkML's exactly_one_of cannot express that implication
    # without also accepting the case it exists to refuse. So it lives here,
    # beside the check, rather than in a slot description nothing performs.
    for attempt in bundle.attempts:
        stated = bool(attempt.unavailable_reason and attempt.unavailable_reason.strip())
        if attempt.status == "UNAVAILABLE" and not stated:
            add("OCR-D015", attempt.id,
                "status is UNAVAILABLE and no unavailable_reason is given")
        if attempt.status != "UNAVAILABLE" and stated:
            add("OCR-D015", attempt.id,
                f"status is {attempt.status} and carries an unavailable_reason")

    # A correction that says it produced a different reading must carry it, and
    # what it carries must be what the hypothesis plane holds. Mandate B2 keeps
    # the verdicts distinct; this keeps the two planes agreeing about what the
    # corrected text actually is.
    for correction in bundle.corrections:
        produced = [h for h in bundle.hypotheses if h.correction_id == correction.id]
        if correction.verdict == "CORRECTED":
            if not correction.corrected_text_digest:
                add("OCR-D015", correction.id,
                    "verdict is CORRECTED and no corrected text is carried")
            elif len(produced) != 1:
                add("OCR-D015", correction.id,
                    f"verdict is CORRECTED and produced {len(produced)} readings, not one")
            elif produced[0].text_digest != correction.corrected_text_digest:
                add("OCR-D015", correction.id,
                    f"corrected text {correction.corrected_text_digest} disagrees with "
                    f"the reading it produced, {produced[0].text_digest}")
        elif correction.corrected_text_digest:
            add("OCR-D015", correction.id,
                f"verdict is {correction.verdict} and carries a corrected text")

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

    return VerificationResult(
        bundle.id, CAPABILITY, tuple(out), account_for(bundle, registry)
    )


def _unit_outcome(bundle: Bundle, unit: str) -> str:
    """What became of one declared unit, in mandate B2's vocabulary."""
    if unit not in bundle.observed_units:
        return "NOT_OBSERVED"
    rasters = [r for r in bundle.rasters if r.unit == unit]
    if not rasters:
        return "NOT_RENDERED"
    raster_ids = {r.id for r in rasters}
    regions = {r.id for r in bundle.regions if r.raster_id in raster_ids}
    if not regions:
        return "NOT_ATTEMPTED"

    # A human verdict outranks the machine: a reviewer who looked and found the
    # region blank has accounted for it, and no attempt status may overwrite
    # that. Mandate B2 forbids converting one state into another, so the order
    # is fixed here rather than left to whichever record is read last.
    #
    # ABSENT leads because it is the only verdict that speaks about the unit
    # rather than about one region of it: "this page is not in the source" is
    # not outranked by a reading of something else on the same page. It was
    # missing from this list for a release, and the consequence was not a
    # missing row, it was the wrong row: the fall-through below reported the
    # unit READ, converting a reviewer's statement of absence into a reading.
    # That is the exact substitution mandate B2 exists to forbid.
    reviewed = {h.id for h in bundle.hypotheses if h.region_id in regions}
    verdicts = [c.verdict for c in bundle.corrections if c.reviewed_hypothesis_id in reviewed]
    for verdict in ("ABSENT", "UNREADABLE", "EXCLUDED", "VERIFIED_BLANK"):
        if verdict in verdicts:
            return verdict
    if any(h.region_id in regions for h in bundle.hypotheses):
        return READ

    attempts = [a for a in bundle.attempts if a.region_id in regions]
    if not attempts:
        return "NOT_ATTEMPTED"
    for status in ("UNAVAILABLE", "FAILED"):
        if any(a.status == status for a in attempts):
            return status
    return "NOT_ATTEMPTED"


def account_for(bundle: Bundle, registry: OntologyRegistry | None = None) -> Account:
    """Census every declared unit, then measure what the source class precommitted.

    The declaration was frozen before ingest precisely so this cannot be graded
    against a bar chosen after seeing the scan.

    Takes the same registry the record validation ran under, so a caller who
    replaces the profile ontology replaces the census vocabulary with it. A
    replacement that governed which records are legal while the outcome
    vocabulary stayed hardcoded here would be half a replacement.
    """
    dispositions = outcome_dispositions(registry)
    units = []
    for unit in bundle.source_class.required_units:
        outcome = _unit_outcome(bundle, unit)
        if outcome not in dispositions:
            raise OntologyError(
                f"unit outcome '{outcome}' is produced by this verifier and "
                f"declared by no outcome enum in the profile ontology"
            )
        units.append(UnitAccount(unit, outcome, dispositions[outcome]))
    units = tuple(units)
    accounted = sum(1 for u in units if u.accounted)
    metrics = []
    for family, declaration in sorted(bundle.source_class.metric_families.items()):
        denominator = str(declaration.get("denominator", ""))
        threshold = declaration.get("threshold")
        if denominator not in DENOMINATORS or not isinstance(threshold, (int, float)):
            metrics.append(MetricResult(family, denominator, None, None, "UNMEASURED"))
            continue
        total = len(units)
        if total == 0:
            # A ratio over an empty denominator is undefined, not perfect. This
            # read 1.0 and therefore MET, so a source class requiring nothing
            # scored full coverage on a census of nothing. The schema refuses an
            # empty required_units today and that made the branch unreachable,
            # which is a neighbouring gate holding a door this arithmetic left
            # open. Fail closed here too, on its own.
            metrics.append(MetricResult(family, denominator, None, None, "UNMEASURED"))
            continue
        value = accounted / total
        metrics.append(MetricResult(
            family, denominator, value, float(threshold),
            "MET" if value >= threshold else "UNMET",
        ))
    return Account(bundle.kind, units, tuple(metrics))


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
        # The census vocabulary, published because an adopter reading only this
        # projection must be able to tell which outcomes count as looked-at.
        # Derived from the ontology, so the projection cannot claim a mapping
        # the schema does not declare.
        "unit_dispositions": {
            outcome: disposition
            for outcome, disposition in sorted(outcome_dispositions().items())
        },
        "proves": [
            "source-to-reading lineage",
            "separation of identity planes",
            "declared coverage and policy precommitment",
            "every plane typed under the malleus root primitives",
            "a three-valued unit census: looked-at, never looked at, look failed",
        ],
        "does_not_prove": [
            "source authenticity",
            "factual truth of a reading",
            "quote fairness or representativeness",
            "downstream consequence",
        ],
    }

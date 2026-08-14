"""The Ordo Malleus: mechanical rites for inspecting a malleus-derived schema.

(An ontology named after a hammer attracts inquisitors. We keep them
useful.)

This module runs the rites that a machine can judge without taste: the
schema constructs, the root is current, the tongues are constrained, the
endpoints are bound, the signals are derived, the formulas are not inert
strings pretending to be knowledge. The rites that need judgment (write-path
enforcement, reader/writer census, provenance quality) belong to the
malleus-inquisitor skill and are declared, not implemented, in rubric.yaml.

Every rite exists because a real adoption paid for its absence. The rubric
records the lesson; no project is named.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from malleus.ontology import OntologyError, OntologyRegistry, bundled_ontology_path

HERESY = "HERESY"          # the rule is explicit and the schema breaks it
SUSPICION = "SUSPICION"    # probably a defect; a deliberate design may survive it
NOTE = "NOTE"              # information the inquisitor would want
COMMENDATION = "COMMENDATION"  # discipline worth keeping

_PRIMITIVES = ("Entity", "Event", "Signal", "Relation")
_TYPE_SLOTS = {"Event": "event_type", "Relation": "relation_type", "Signal": "signal_type"}


def _rubric_config() -> dict:
    data = yaml.safe_load((Path(__file__).parent / "rubric.yaml").read_text(encoding="utf-8"))
    return data.get("config", {}) if isinstance(data, dict) else {}


def _formula_tokens() -> tuple[str, ...]:
    tokens = _rubric_config().get("formula_slot_tokens") or [
        "formula", "formal_expression", "expression",
    ]
    return tuple(str(token).lower() for token in tokens)


@dataclass(frozen=True)
class Finding:
    rite: str
    severity: str
    subject: str
    message: str


@dataclass
class Report:
    schema_path: str
    findings: list[Finding] = field(default_factory=list)

    def add(self, rite: str, severity: str, subject: str, message: str) -> None:
        self.findings.append(Finding(rite, severity, subject, message))

    @property
    def heresies(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == HERESY]

    @property
    def purity(self) -> bool:
        return not self.heresies

    def to_json(self) -> str:
        return json.dumps(
            {
                "schema": self.schema_path,
                "purity": self.purity,
                "findings": [f.__dict__ for f in self.findings],
            },
            indent=2,
        )


def _concrete_subtypes(registry: OntologyRegistry, root: str) -> list[str]:
    out = []
    for name in registry.type_names():
        if name == root:
            continue
        typedef = registry.get_type(name)
        if typedef.abstract or typedef.is_mixin:
            continue
        if registry.is_subtype_of(name, root):
            out.append(name)
    return sorted(out)


def run_rites(
    schema_path: str | Path,
    import_map: dict[str, str] | None = None,
    root_path: str | Path | None = None,
) -> Report:
    """Run every mechanical rite against one schema. Returns the full Report."""
    report = Report(schema_path=str(schema_path))

    # Rite of Construction: the schema must load, imports resolved, or nothing
    # else can be judged.
    try:
        registry = OntologyRegistry(str(schema_path), import_map=import_map or None)
    except (OntologyError, OSError, ValueError) as exc:
        report.add("construction", HERESY, str(schema_path), f"schema does not construct: {exc}")
        return report
    report.add("construction", COMMENDATION, str(schema_path),
               f"constructs; version {registry.schema_version or 'undeclared'}, "
               f"content hash {registry.content_hash()[:12]}…, "
               f"{len(registry.type_names())} types")

    # Rite of the Root: the five primitives must be present, and unused
    # primitives are worth knowing about (in the field, Signal is the most
    # distinctive primitive and the least adopted).
    missing = [p for p in _PRIMITIVES if not registry.has_type(p)]
    if missing:
        report.add("root", HERESY, ",".join(missing),
                   "root primitives absent: the schema does not import the malleus root")
        return report
    for primitive in _PRIMITIVES:
        subtypes = _concrete_subtypes(registry, primitive)
        if not subtypes and primitive != "Entity":
            report.add("root", NOTE, primitive,
                       f"no concrete subtype extends {primitive}; declared vocabulary "
                       "with no speaker is how drift begins")
    agents = registry.types_with_mixin("Agent")
    if not agents:
        report.add("root", NOTE, "Agent",
                   "no type carries the Agent mixin; if the domain has actors who "
                   "decide or authorize, they are currently unmodeled")

    # Rite of Root Currency: compare against the installed root. A vendored
    # copy that drifted from the installed malleus is the single most repeated
    # adoption failure observed in the field.
    # Currency is a consumer question: does this schema still validate like
    # the installed root? So the STRICT check, which sees required-constraint
    # drift. The producer-side check certified a root that had silently
    # dropped a required line; never again.
    root = Path(root_path) if root_path else bundled_ontology_path("malleus.yaml")
    try:
        root_registry = OntologyRegistry(str(root))
        verdict = registry.check_compatibility_strict(
            root_registry.content_hash(), root_registry.strict_fingerprint()
        )
        if verdict in ("superset", "identical"):
            phrase = ("is identical to" if verdict == "identical"
                      else "is a superset of")
            report.add("root_currency", COMMENDATION, str(root),
                       f"schema {phrase} the installed root (strict): root is current")
        else:
            report.add("root_currency", HERESY, str(root),
                       f"schema is {verdict} against the installed root under the "
                       "strict (consumer-side) check: the imported root has drifted "
                       "from the installed malleus. Re-vendor or fix the import map, "
                       "then regenerate all artifacts.")
            producer = registry.check_compatibility(
                root_registry.content_hash(), root_registry.fingerprint()
            )
            if producer in ("superset", "identical"):
                report.add("root_currency", NOTE, str(root),
                           "producer-compatible but consumer-divergent: the drift is "
                           "in required constraints, the most silent kind")
    except (OntologyError, OSError) as exc:
        report.add("root_currency", SUSPICION, str(root), f"root not comparable: {exc}")

    # Rite of Constrained Tongues: every concrete Event/Relation/Signal
    # subtype must narrow its type-slot to an enum or pin it with
    # equals_string. A loose string slot is a hole in the fence.
    for primitive, slot_name in _TYPE_SLOTS.items():
        for name in _concrete_subtypes(registry, primitive):
            constraint = registry.get_slot_constraint(name, slot_name)
            rng = constraint.range if constraint else None
            pinned = bool(constraint and constraint.equals_string)
            if pinned or (rng and registry.has_enum(rng)):
                continue
            report.add("constrained_tongues", HERESY, name,
                       f"{slot_name} is not constrained to an enum or pinned with "
                       "equals_string; any string will validate")

    # Rite of Bound Endpoints: a concrete Relation narrows both endpoints.
    # (Predicate pinning via equals_string is enforced at construction since
    # 0.6.0, so only endpoint width is left to judge.) Endpoints left at
    # Entity make domain/range checking vacuous: 'does this relation name
    # exist' is not a contract.
    for name in _concrete_subtypes(registry, "Relation"):
        for endpoint in ("source_id", "target_id"):
            c = registry.get_slot_constraint(name, endpoint)
            rng = c.range if c else None
            if rng in (None, "string", "Entity"):
                report.add("bound_endpoints", SUSPICION, name,
                           f"{endpoint} range is {rng or 'undeclared'}; the endpoint "
                           "contract is vacuous, narrow it to a domain class")

    # Rite of the Derived: a Signal is a computed quality. It must name its
    # bearer, and should carry its algorithm and computation time, or it is an
    # assertion wearing a Signal's clothes.
    for name in _concrete_subtypes(registry, "Signal"):
        slots = registry.effective_slots(name)
        bearer = slots.get("bearer_id")
        if not (bearer and bearer.required):
            report.add("derived_signals", SUSPICION, name,
                       "bearer_id is not required; a quality with no bearer is "
                       "not a derived quality")
        for expected in ("algorithm", "computed_at"):
            if expected not in slots:
                report.add("derived_signals", NOTE, name,
                           f"{expected} not among effective slots; a Signal that "
                           "cannot say how or when it was computed cannot be recomputed")

    # Rite Against Inert Formulas: a slot shaped like a formula, with nothing
    # declaring an executor, is documentation pretending to be knowledge. In
    # the field, five systems wrote the formula down and none executed it.
    tokens = _formula_tokens()
    for name in registry.type_names():
        typedef = registry.get_type(name)
        if typedef.is_mixin or typedef.abstract:
            continue
        for slot_name in registry.effective_slots(name):
            lowered = slot_name.lower()
            if any(token in lowered for token in tokens):
                report.add("inert_formula", SUSPICION, f"{name}.{slot_name}",
                           "formula-shaped slot; either wire an executor for it or "
                           "mark it inert in its description (see docs/RECIPES.md, "
                           "recipe 4)")
    return report

"""Mechanical rites for the Malleus root ontology profile.

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

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from malleus.inquisition.pack_grounding import (
    PACK_GROUNDING_RITE_IDENTITY,
    PackConformanceReceipt,
    PackGroundingReceipt,
    PackGroundingRefusal,
    PackGroundingRefusalReason,
    validate_pack_conformance,
    validate_pack_grounding,
)
from malleus.ontology import OntologyError, OntologyRegistry, bundled_ontology_path

HERESY = "HERESY"          # the rule is explicit and the schema breaks it
SUSPICION = "SUSPICION"    # probably a defect; a deliberate design may survive it
NOTE = "NOTE"              # information the inquisitor would want
COMMENDATION = "COMMENDATION"  # discipline worth keeping

_PRIMITIVES = ("Entity", "Event", "Signal", "Relation")
_TYPE_SLOTS = {"Event": "event_type", "Relation": "relation_type", "Signal": "signal_type"}


RUBRIC_PATH = Path(__file__).parent / "rubric.yaml"
REPORT_SCOPE = "root-ontology-profile"


class RubricError(RuntimeError):
    """The rubric is missing, unparseable, or malformed.

    The rubric is the instrument, not the subject. A malformed schema becomes
    a finding; a malformed rubric refuses, because a tuning error that
    degrades to built-in defaults ignores the operator in silence.
    """


class RiteContractError(AssertionError):
    """A rite call site broke the contract. A bug here, never the operator's
    rubric: distinct from RubricError so the CLI cannot blame the wrong file."""


_DECLARABLE = (HERESY, SUSPICION, NOTE)
_NOTE_REASONS = ("open_question", "low_stakes")

# Every rite id the mechanical rites can emit. The rubric must declare all of
# them, checked when the rubric loads rather than when a rite happens to fire:
# a lazy check means a deleted entry is only noticed if that rite would have
# spoken, so a schema tripping nothing gets a seal from a rubric with holes.
EMITTED_RITES = (
    "construction",
    "root",
    "root_has_speakers",
    "root_currency",
    "root_currency_answerable",
    "constrained_tongues",
    "bound_endpoints",
    "derived_signals",
    "inert_formula",
)

# Rites that may never be switched off. `construction` is the precondition for
# judging anything at all: with it disabled, a document that does not even
# parse would collect no findings and take the seal.
UNDISABLABLE_RITES = ("construction",)

if not set(UNDISABLABLE_RITES) <= set(EMITTED_RITES):  # pragma: no cover - import-time guard
    raise RuntimeError(
        "UNDISABLABLE_RITES names a rite the code never emits: the two constants "
        f"drifted ({sorted(set(UNDISABLABLE_RITES) - set(EMITTED_RITES))}). The "
        "floor would then be enforced against an entry nothing checks."
    )


def _rubric(path: Path | None = None) -> dict:
    """Load and structurally validate the rubric. Nothing is assumed away."""
    path = path or RUBRIC_PATH
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise RubricError(f"rubric at {path} could not be read: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("config"), dict):
        raise RubricError(
            f"rubric at {path} has no `config:` mapping. This is the inquisitor's "
            "instrument, not the schema under inspection: fix or reinstall the rubric."
        )
    if not isinstance(data.get("version"), (int, str)):
        raise RubricError(
            f"rubric at {path} must declare a scalar `version:`; got "
            f"{data.get('version')!r}. It is reported with every verdict, so a "
            "consumer parses it."
        )
    seen: set[str] = set()
    for section in ("mechanical", "judgment"):
        entries = data.get(section)
        if not isinstance(entries, list) or not entries:
            raise RubricError(f"rubric at {path}: `{section}:` must be a non-empty list of rites")
        for entry in entries:
            _validate_rite(path, section, entry)
            if entry["id"] in seen:
                raise RubricError(
                    f"rubric at {path}: rite {entry['id']!r} is declared twice. A duplicate "
                    "silently last-wins, so the losing entry's severity is a setting the "
                    "operator can read and the instrument ignores."
                )
            seen.add(entry["id"])
    _validate_rite_table(path, data, seen)
    return data


def _validate_rite_table(path: Path, data: dict, declared: set[str]) -> None:
    """The rite table as a whole, not one rite at a time."""
    missing = [rite for rite in EMITTED_RITES if rite not in declared]
    if missing:
        raise RubricError(
            f"rubric at {path} declares no entry for {missing}, which the rites emit. "
            "Disable a rite with `enabled: false`; deleting its entry leaves the "
            "instrument unable to say how loud the finding should be."
        )
    by_id = {entry["id"]: entry for section in ("mechanical", "judgment")
             for entry in data[section]}
    for rite in UNDISABLABLE_RITES:
        if by_id[rite].get("enabled", True) is False:
            raise RubricError(
                f"rubric at {path}: rite {rite!r} cannot be disabled. It is the "
                "precondition for judging anything, and an instrument that skips it "
                "would grant the seal to a document that does not parse."
            )


def _validate_rite(path: Path, section: str, entry: object) -> None:
    if not isinstance(entry, dict):
        raise RubricError(f"rubric at {path}: every {section} rite must be a mapping, got {entry!r}")
    rite = entry.get("id")
    if not isinstance(rite, str) or not rite.strip():
        raise RubricError(f"rubric at {path}: a {section} rite has no `id:`")
    for key in ("question", "lesson"):
        if not isinstance(entry.get(key), str) or not entry[key].strip():
            raise RubricError(f"rubric at {path}: rite {rite!r} has no `{key}:`")
    if entry.get("severity") not in _DECLARABLE:
        raise RubricError(
            f"rubric at {path}: rite {rite!r} declares severity "
            f"{entry.get('severity')!r}; expected one of {_DECLARABLE}"
        )
    if not isinstance(entry.get("enabled", True), bool):
        raise RubricError(f"rubric at {path}: rite {rite!r} has a non-boolean `enabled:`")
    if entry["severity"] == NOTE and entry.get("status") not in _NOTE_REASONS:
        raise RubricError(
            f"rubric at {path}: rite {rite!r} is NOTE and must say why in `status:` "
            f"(one of {_NOTE_REASONS}). A low severity because the underlying property "
            "is unestablished reads identically to one softened for convenience, and "
            "the difference must be data, not an argument a reader reconstructs."
        )
    if entry.get("status") == "low_stakes" and not str(entry.get("status_reason", "")).strip():
        # `low_stakes` on its own is an unverifiable self-assertion, and a
        # sanctioned field is exactly where a severity softened to keep a
        # build green would hide. Make the claim carry its argument.
        raise RubricError(
            f"rubric at {path}: rite {rite!r} claims `status: low_stakes` and must say "
            "why in `status_reason:`. Nobody can check the claim itself; the reason is "
            "what a reviewer reads to catch a severity softened for convenience."
        )


class Rites:
    """The rite table exactly as the rubric declares it.

    The rubric governs each rite's PRIMARY verdict and whether it runs at all.
    Secondary findings (commendations, graded sub-findings below the primary
    condition) carry their own severity at the call site and say so.
    """

    def __init__(self, rubric: dict, path: Path | None = None,
                 digest: str = "", baseline: dict[str, str] | None = None) -> None:
        self.path = str(path or RUBRIC_PATH)
        self.version = rubric.get("version")
        # The version is the operator's own word. The digest is not, so a CI
        # reader keyed on "which instrument granted this" has one handle that
        # a copy cannot forge for free.
        self.digest = digest
        self._baseline = baseline or {}
        self._severity: dict[str, str] = {}
        self._enabled: dict[str, bool] = {}
        self._order: list[str] = []
        for section in ("mechanical", "judgment"):
            for entry in rubric[section]:
                self._severity[entry["id"]] = entry["severity"]
                self._enabled[entry["id"]] = entry.get("enabled", True)
                self._order.append(entry["id"])

    @property
    def disabled(self) -> tuple[str, ...]:
        """EVERY rite the rubric switched off, mechanical and judgment.

        A seal is only as wide as the rubric that granted it, so this travels
        with every report: the record of what was not judged belongs beside
        the record of what was. Counting only the mechanical tier let all 24
        judgment rites be switched off under a header reading "0 rites
        disabled", which is the disclosure lying about its own coverage.
        """
        return tuple(r for r in self._order if not self._enabled[r])

    @property
    def disabled_mechanical(self) -> tuple[str, ...]:
        return tuple(r for r in self.disabled if r in EMITTED_RITES)

    @property
    def disabled_judgment(self) -> tuple[str, ...]:
        return tuple(r for r in self.disabled if r not in EMITTED_RITES)

    @property
    def downgraded(self) -> tuple[str, ...]:
        """Rites the operator lowered below the packaged severity.

        A downgrade narrows the gate exactly as much as a disable: a heresy
        tuned to NOTE is visible, inert, and still seals. Reporting one and
        not the other discloses one of the two dimensions along which the
        instrument can be narrowed.
        """
        order = {NOTE: 0, SUSPICION: 1, HERESY: 2}
        return tuple(r for r in self._order
                     if r in self._baseline
                     and order.get(self._severity[r], 0) < order.get(self._baseline[r], 0))

    @property
    def narrowed(self) -> bool:
        return bool(self.disabled or self.downgraded)

    def _known(self, rite: str) -> None:
        if rite not in self._severity:
            raise RubricError(
                f"rite {rite!r} is emitted by the rites and absent from the rubric. "
                "Disable a rite with `enabled: false`; deleting its entry leaves the "
                "instrument unable to say how loud the finding should be."
            )

    def enabled(self, rite: str) -> bool:
        self._known(rite)
        return self._enabled[rite]

    def severity(self, rite: str) -> str:
        self._known(rite)
        return self._severity[rite]


def _packaged_severities(path: Path | None) -> dict[str, str]:
    """The shipped severities, to measure a tuned rubric against.

    Empty when the packaged rubric is the one in use (nothing to compare) or
    when it cannot be read (a broken install is already reported elsewhere;
    it must not turn a tuned run into a crash).
    """
    if path is None:
        return {}
    try:
        packaged = _rubric(RUBRIC_PATH)
    except RubricError:
        return {}
    return {entry["id"]: entry["severity"]
            for section in ("mechanical", "judgment")
            for entry in packaged[section]}


def _tokens(rubric: dict) -> tuple[str, ...]:
    tokens = rubric["config"].get("formula_slot_tokens")
    if not isinstance(tokens, list):
        raise RubricError(
            "rubric `config.formula_slot_tokens` must be a list. "
            "An empty list disables the inert_formula rite; a missing or "
            "mistyped key is a broken rubric and is not assumed away."
        )
    return tuple(str(token).lower() for token in tokens)


def _formula_tokens(path: Path | None = None) -> tuple[str, ...]:
    return _tokens(_rubric(path))


@dataclass(frozen=True)
class Finding:
    rite: str
    severity: str
    subject: str
    message: str


@dataclass
class Report:
    schema_path: str
    rites: Rites
    findings: list[Finding] = field(default_factory=list)

    def verdict(self, rite: str, subject: str, message: str) -> None:
        """Emit a rite's PRIMARY finding at the severity the rubric declares."""
        if self.rites.enabled(rite):
            self.findings.append(Finding(rite, self.rites.severity(rite), subject, message))

    def add(self, rite: str, severity: str, subject: str, message: str) -> None:
        """Emit a secondary finding: a commendation, or a graded sub-finding
        below the rite's primary condition, at an explicit severity.

        Never a heresy. Only a rite's primary verdict may deny the seal, and
        primary verdicts take their severity from the rubric; a heresy raised
        here would be a severity the rubric can neither see nor tune.
        """
        if severity == HERESY:
            # Not a RubricError: the operator's rubric is fine, this is a bug
            # in a call site, and telling them their rubric is broken would
            # send them to fix the one file that is not at fault.
            raise RiteContractError(
                f"rite {rite!r} tried to raise a heresy through add(); only verdict() "
                "may, because only verdict() reads its severity from the rubric"
            )
        if self.rites.enabled(rite):
            self.findings.append(Finding(rite, severity, subject, message))

    @property
    def heresies(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == HERESY]

    @property
    def unconstructed(self) -> list[Finding]:
        """Anything `construction` said that was not a commendation."""
        return [f for f in self.findings
                if f.rite == "construction" and f.severity != COMMENDATION]

    @property
    def purity(self) -> bool:
        """The seal, with one floor the rubric cannot lower.

        A document that did not construct is never sealed, whatever severity
        the rubric puts on saying so. The rubric governs how loud a finding
        is; it may not govern whether an unjudgeable document can pass.
        Round 4 closed this on `enabled:` and left it open on `severity:`,
        which is one word in the same entry: a half-closed gate.
        """
        return not self.heresies and not self.unconstructed

    def to_json(self) -> str:
        return json.dumps(
            {
                "schema": self.schema_path,
                "scope": REPORT_SCOPE,
                "purity": self.purity,
                "rubric": Path(self.rites.path).name,
                "rubric_version": self.rites.version,
                "rubric_sha256": self.rites.digest,
                "disabled": list(self.rites.disabled),
                "downgraded": list(self.rites.downgraded),
                "findings": [f.__dict__ for f in self.findings],
            },
            indent=2,
        )


def _skipped_after(report: "Report", reached: str) -> None:
    """Name the rites an early return prevented from running.

    A report showing one heresy and nothing else invites the reader to
    conclude the rest passed. Observed in the field: a construction failure
    left seven of eight rites unexecuted across a whole repository and the
    report said nothing about it.
    """
    remaining = [r for r in EMITTED_RITES[EMITTED_RITES.index(reached) + 1:]
                 if report.rites.enabled(r)]
    if remaining:
        report.add(reached, NOTE, "coverage",
                   f"{len(remaining)} rites did not run, because nothing past "
                   f"`{reached}` could be judged: {', '.join(remaining)}. "
                   "Their silence is not a pass.")


class _ReferenceUnusable(Exception):
    """Internal: the reference root cannot answer the currency question.

    Not an error the caller sees. The finding is already recorded; this only
    skips the comparison, because the fault is in the reference and every
    other rite still has a perfectly good subject to judge.
    """


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
    rubric_path: str | Path | None = None,
) -> Report:
    """Run every mechanical rite against one schema. Returns the full Report.

    Severities and enablement come from the rubric, loaded and validated
    before any work is done, so a broken instrument refuses before it can
    throw away a half-finished report.
    """
    path = Path(rubric_path) if rubric_path else None
    rubric = _rubric(path)
    digest = hashlib.sha256((path or RUBRIC_PATH).read_bytes()).hexdigest()
    report = Report(schema_path=str(schema_path),
                    rites=Rites(rubric, path, digest, _packaged_severities(path)))

    # Rite of Construction: the schema must load, imports resolved, or nothing
    # else can be judged.
    try:
        registry = OntologyRegistry(str(schema_path), import_map=import_map or None)
    except (OntologyError, OSError, ValueError) as exc:
        report.verdict("construction", str(schema_path), f"schema does not construct: {exc}")
        # A schema written against an old root often fails under current
        # rules. Compare the mapped root to the installed one anyway, so the
        # report explains the failure instead of hiding its likely cause.
        mapped_root = (import_map or {}).get("malleus")
        if mapped_root:
            try:
                vendored = OntologyRegistry(mapped_root)
                installed = OntologyRegistry(
                    str(Path(root_path) if root_path else bundled_ontology_path("malleus.yaml"))
                )
                verdict = vendored.check_compatibility_strict(
                    installed.content_hash(), installed.strict_fingerprint()
                )
                if verdict not in ("identical", "superset"):
                    report.add("root_currency", NOTE, mapped_root,
                               f"the imported root is {verdict} against the installed "
                               "malleus; the construction failure above likely follows "
                               "from version skew, judged under current-malleus rules")
            except (OntologyError, OSError, ValueError) as diag_exc:
                # The likeliest reason the mapped root will not load is that
                # the mapped root is itself broken, which is exactly when the
                # operator needs to be told the tool tried and failed.
                report.add("root_currency", NOTE, mapped_root,
                           f"could not compare the mapped root to the installed malleus "
                           f"({diag_exc}); the construction failure above could not be "
                           "attributed to version skew")
        _skipped_after(report, "construction")
        return report
    if not registry.type_names():
        # JSON is valid YAML, so a wrong-format ontology parses into an
        # empty registry. Judging it would certify a non-schema as an empty
        # schema; refuse with the right diagnosis instead.
        report.verdict("construction", str(schema_path),
                       "document parses but declares no LinkML classes; this is "
                       "not a schema the rites can judge (wrong format?)")
        _skipped_after(report, "construction")
        return report
    report.add("construction", COMMENDATION, str(schema_path),
               f"constructs; version {registry.schema_version or 'undeclared'}, "
               f"content hash {registry.content_hash()[:12]}…, "
               f"{len(registry.type_names())} types")

    # The other reader a retirement needs. The loader refuses a name past its
    # boundary; without this, the ones still inside their window are visible
    # only on the day they bite, which is a wall wearing a plan's clothes.
    for retirement in registry.retirements():
        successor = (
            f"use '{retirement.replaced_by}'" if retirement.replaced_by
            else "no replacement is offered"
        )
        report.add("construction", NOTE, retirement.slot,
                   f"retires at version {retirement.stops_at_text} ({retirement.reason}); "
                   f"{successor}")

    # Rite of the Root: the primitives must be present. A schema that never
    # imported the root cannot be judged at all, which is why this is the
    # rite's primary condition and why it denies the seal.
    missing = [p for p in _PRIMITIVES if not registry.has_type(p)]
    if missing:
        report.verdict("root", ",".join(missing),
                       "root primitives absent: the schema does not import the malleus root")
        _skipped_after(report, "root")
        return report

    # Rite of Speakers: a declared primitive nobody extends is vocabulary with
    # no speaker. Separate from the root rite because it is a different
    # question at a different volume (in the field, Signal is the most
    # distinctive primitive and the least adopted).
    for primitive in _PRIMITIVES:
        subtypes = _concrete_subtypes(registry, primitive)
        if not subtypes and primitive != "Entity":
            report.verdict("root_has_speakers", primitive,
                           f"no concrete subtype extends {primitive}; declared vocabulary "
                           "with no speaker is how drift begins")
    agents = registry.types_with_mixin("Agent")
    if not agents:
        report.verdict("root_has_speakers", "Agent",
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
        # The reference gets the same wrong-format refusal the subject got
        # fourteen lines up. An empty or non-malleus reference has an empty
        # fingerprint, which makes every subject a trivial superset, so the
        # rite would answer "root is current" precisely when it knows least.
        absent = [p for p in _PRIMITIVES if not root_registry.has_type(p)]
        if absent:
            # Only the currency question is unanswerable. The subject is fine,
            # so the rites below still run.
            report.verdict("root_currency_answerable", str(root),
                           f"the reference root declares no {', '.join(absent)}; this is not "
                           "a malleus root, and currency cannot be asked against it "
                           "(an empty reference makes every schema a superset)")
            raise _ReferenceUnusable
        verdict = registry.check_compatibility_strict(
            root_registry.content_hash(), root_registry.strict_fingerprint()
        )
        if verdict in ("superset", "identical"):
            phrase = ("is identical to" if verdict == "identical"
                      else "is a superset of")
            report.add("root_currency", COMMENDATION, str(root),
                       f"schema {phrase} the installed root (strict): root is current")
            # The grammar version is excluded from the structural comparison,
            # so say it here rather than let it vanish. It used to be compared
            # as an ordinary fact, which made this commendation unreachable for
            # any schema using a conditional feature the root does not.
            grammar = registry.fingerprint_grammar(root_registry.strict_fingerprint())
            if grammar == "newer":
                report.add("root_currency", NOTE, str(root),
                           "the root declares a newer fingerprint grammar than this "
                           "schema produces; the structural comparison above answered a "
                           "narrower question than it appears to")
        else:
            report.verdict("root_currency", str(root),
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
    except _ReferenceUnusable:
        pass  # already recorded above; the remaining rites still apply
    except (OntologyError, OSError) as exc:
        # "I could not determine whether your root is current" is an unknown
        # condition, and an unknown condition refuses. Its own rite, because
        # "the root drifted" and "the root could not be read" are two
        # questions at two volumes.
        report.verdict("root_currency_answerable", str(root),
                       f"the reference root could not be read, so currency could not be "
                       f"judged at all: {exc}")

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
            report.verdict("constrained_tongues", name,
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
                report.verdict("bound_endpoints", name,
                               f"{endpoint} range is {rng or 'undeclared'}; the endpoint "
                               "contract is vacuous, narrow it to a domain class")

    # Rite of the Derived: a Signal is a computed quality. It must name its
    # bearer, and should carry its algorithm and computation time, or it is an
    # assertion wearing a Signal's clothes.
    for name in _concrete_subtypes(registry, "Signal"):
        slots = registry.effective_slots(name)
        bearer = slots.get("bearer_id")
        if not (bearer and bearer.required):
            report.verdict("derived_signals", name,
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
    tokens = _tokens(rubric)
    for name in registry.type_names():
        typedef = registry.get_type(name)
        if typedef.is_mixin or typedef.abstract:
            continue
        for slot_name in registry.effective_slots(name):
            lowered = slot_name.lower()
            if any(token in lowered for token in tokens):
                report.verdict("inert_formula", f"{name}.{slot_name}",
                               "formula-shaped slot; either wire an executor for it or "
                               "mark it inert in its description (see docs/RECIPES.md, "
                               "recipe 4)")
    return report


__all__ = (
    "COMMENDATION",
    "EMITTED_RITES",
    "Finding",
    "HERESY",
    "NOTE",
    "PACK_GROUNDING_RITE_IDENTITY",
    "PackConformanceReceipt",
    "PackGroundingReceipt",
    "PackGroundingRefusal",
    "PackGroundingRefusalReason",
    "REPORT_SCOPE",
    "Report",
    "RiteContractError",
    "Rites",
    "RubricError",
    "SUSPICION",
    "UNDISABLABLE_RITES",
    "run_rites",
    "validate_pack_conformance",
    "validate_pack_grounding",
)

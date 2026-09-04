"""Strict LinkML-backed structural validation for Malleus graphs."""

from __future__ import annotations

import hashlib
import json
import math
import sysconfig
from copy import deepcopy
from dataclasses import dataclass, field, fields
from datetime import datetime
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path
from typing import Any, Literal, Mapping

import yaml


# The five kinds the validator enforces directly.
BASE_RANGES = frozenset({"string", "integer", "float", "boolean", "datetime"})

# The rest of LinkML's built-in types, each mapped to the base kind that is
# actually checked. Declaring `uri` or `double` is legal in the schema
# language, and refusing it punished adopters for using their tools
# correctly: two independent projects lost a schema to this in one week, one
# on `uri` and one on `double`.
#
# The mapping is honest about its limit. `uri` is checked as a string, not
# parsed as a URI; `date` is checked as a string, not parsed as a date. The
# lexical form is NOT enforced, and that boundary is
# `lexical-format-validation` in IMPLEMENTATION_STATUS.md. Accepting the
# declaration and checking the base kind is strictly more than refusing the
# schema, and it is stated rather than implied.
LEXICAL_RANGES = {
    "double": "float",
    "decimal": "float",
    "date": "string",
    "time": "string",
    "date_or_datetime": "string",
    "uri": "string",
    "uriorcurie": "string",
    "curie": "string",
    "ncname": "string",
    "objectidentifier": "string",
    "nodeidentifier": "string",
    "jsonpointer": "string",
    "jsonpath": "string",
    "sparqlpath": "string",
}

BUILTIN_RANGES = frozenset(BASE_RANGES | set(LEXICAL_RANGES))
LEGACY_FINGERPRINT_VERSION = 3
FINGERPRINT_VERSION = 4
FINGERPRINT_VERSION_PREFIX = "fingerprint_version:"

# Every payload grammar a recorded content hash may have been written under,
# newest first. The grammar version sits inside the hashed payload, and 0.11.0
# made it conditional: 3 unconditionally before, 4 afterwards for a schema
# using exactly_one_of, inlined or value_presence. So a feature-using schema's
# content hash changed between releases without one ontology byte changing,
# and a ledger anchored under the old hash could not replay.
#
# A hash written into an accepted append-only ledger is a public contract. The
# ledger cannot be rewritten to match a new rule, so the rule must be able to
# verify what the ledger already holds. Verify a recorded hash under its own
# grammar, say which one verified it, and never silently recompute and reject.
KNOWN_PAYLOAD_GRAMMARS: tuple[int, ...] = (FINGERPRINT_VERSION, LEGACY_FINGERPRINT_VERSION)


def _structural_facts(facts: frozenset[str]) -> frozenset[str]:
    """The facts that describe the schema, without the one that describes the grammar.

    `fingerprint_version:N` says which fact grammar produced this set. It is
    not a property of the schema, and comparing it as though it were makes
    "superset" unreachable for exactly the pair that most needs the answer: a
    root that uses none of the conditional features against a project that
    uses one. They then differ by one fact in each direction, neither set
    contains the other, and a correct schema is reported divergent.

    Reported by an adopting project whose release pipeline this blocked, and
    reproduced here against our own shipped ontologies: `assent.yaml` carries
    every fact `malleus.yaml` has, zero missing, and answered divergent.
    """
    return frozenset(f for f in facts if not f.startswith(FINGERPRINT_VERSION_PREFIX))


def _fingerprint_grammar(facts: frozenset[str]) -> int | None:
    """The grammar version a fact set declares, or None when it declares none."""
    declared = {
        f[len(FINGERPRINT_VERSION_PREFIX):]
        for f in facts
        if f.startswith(FINGERPRINT_VERSION_PREFIX)
    }
    if len(declared) != 1:
        return None
    try:
        return int(next(iter(declared)))
    except ValueError:
        return None


def _compare_structure(mine: frozenset[str], foreign: frozenset[str]) -> str:
    mine, foreign = _structural_facts(mine), _structural_facts(foreign)
    if foreign.issubset(mine):
        return "superset"
    if mine.issubset(foreign):
        return "subset"
    return "divergent"


_CLASS_EXPRESSION_KEYS = frozenset({"slot_conditions"})
_SLOT_CONDITION_KEYS = frozenset({"required", "equals_string", "value_presence"})
_VALUE_PRESENCE_VALUES = frozenset({"PRESENT", "ABSENT"})


def bundled_ontology_path(*parts: str) -> Path:
    """Resolve one ontology shipped with the installed package or source tree."""
    if not parts:
        raise OntologyError("bundled ontology path requires at least one component")
    if any(
        not isinstance(part, str)
        or not part.strip()
        or Path(part).is_absolute()
        or Path(part).parts != (part,)
        or part in {".", ".."}
        for part in parts
    ):
        raise OntologyError("bundled ontology path components must be relative names")
    source_root = Path(__file__).resolve().parents[2] / "ontology"
    source_candidate = source_root.joinpath(*parts)
    if source_candidate.is_file():
        return source_candidate
    try:
        installed = distribution("malleus-dev")
    except PackageNotFoundError:
        installed = None
    if installed is not None:
        suffix = "/".join(("share", "malleus", "ontology", *parts))
        for installed_file in installed.files or ():
            if installed_file.as_posix().endswith(suffix):
                candidate = Path(installed.locate_file(installed_file))
                if candidate.is_file():
                    return candidate
    installed_root = Path(sysconfig.get_path("data")) / "share" / "malleus" / "ontology"
    installed_candidate = installed_root.joinpath(*parts)
    if installed_candidate.is_file():
        return installed_candidate
    raise OntologyError(f"Bundled ontology does not exist: {'/'.join(parts)}")


class OntologyError(ValueError):
    """Raised when an ontology cannot be loaded without ambiguity."""


@dataclass(frozen=True, slots=True)
class OntologySource:
    """One exact byte-bearing source retained by an ontology registry."""

    source_role: Literal["entry", "import"]
    resolved_locator: str
    source_bytes: bytes

    @property
    def byte_length(self) -> int:
        return len(self.source_bytes)

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.source_bytes).hexdigest()


@dataclass(frozen=True, slots=True)
class OntologyImportResolution:
    """One authored import edge and the target selected by the loader."""

    parent_locator: str
    ordinal: int
    literal: str
    target_role: Literal["ontology", "builtin"]
    resolved_locator: str


@dataclass(frozen=True, slots=True)
class OntologyDefinitionSource:
    """The retained source that owns one resolved ontology definition."""

    kind: Literal["type", "enum", "slot", "class"]
    name: str
    source_locator: str


@dataclass(frozen=True, slots=True)
class OntologySourceClosure:
    """Immutable provenance for every source used to construct a registry."""

    sources: tuple[OntologySource, ...]
    imports: tuple[OntologyImportResolution, ...]
    definitions: tuple[OntologyDefinitionSource, ...]


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise OntologyError(
                f"Unhashable YAML mapping key at line {key_node.start_mark.line + 1}"
            ) from error
        if duplicate:
            raise OntologyError(
                f"Duplicate YAML key '{key}' at line {key_node.start_mark.line + 1}"
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


@dataclass(frozen=True)
class SlotConstraint:
    """Structural constraints declared for a slot or a class slot usage."""

    required: bool | None = None
    range: str | None = None
    multivalued: bool | None = None
    identifier: bool | None = None
    equals_string: str | None = None
    minimum_value: int | float | None = None
    maximum_value: int | float | None = None
    inlined: bool | None = None
    value_presence: str | None = None


@dataclass(frozen=True)
class ClassExpression:
    """One supported flat LinkML class expression."""

    slot_conditions: tuple[tuple[str, SlotConstraint], ...]


@dataclass(frozen=True)
class TypeDef:
    """A registered class, including its direct slots and mixins."""

    name: str
    parent: str | None
    slots: list[str] = field(default_factory=list)
    slot_usage: dict[str, SlotConstraint] = field(default_factory=dict)
    is_mixin: bool = False
    abstract: bool = False
    mixins: tuple[str, ...] = ()
    exactly_one_of: tuple[ClassExpression, ...] = ()


@dataclass(frozen=True)
class EnumDef:
    """A registered enum with its permissible values."""

    name: str
    values: frozenset[str]


def _constraint(data: Mapping[str, Any]) -> SlotConstraint:
    return SlotConstraint(
        required=data.get("required") if "required" in data else None,
        range=data.get("range"),
        multivalued=data.get("multivalued") if "multivalued" in data else None,
        inlined=data.get("inlined") if "inlined" in data else None,
        identifier=data.get("identifier") if "identifier" in data else None,
        equals_string=data.get("equals_string"),
        minimum_value=data.get("minimum_value"),
        maximum_value=data.get("maximum_value"),
        value_presence=data.get("value_presence"),
    )


@dataclass(frozen=True)
class Retirement:
    """A declared plan to remove a name, with the boundary where it stops working."""

    slot: str
    schema: str
    stops_at: tuple[int, ...]
    stops_at_text: str
    reason: str
    replaced_by: str | None = None

    def __str__(self) -> str:
        successor = f"; use '{self.replaced_by}'" if self.replaced_by else "; no replacement"
        return f"'{self.slot}' retires at {self.schema} {self.stops_at_text}{successor}: {self.reason}"


def _version_tuple(subject: str, text: Any) -> tuple[int, ...]:
    """Parse a dotted numeric version, or refuse.

    Deliberately strict. A boundary nobody can compare is a boundary that never
    arrives, which is the whole failure mode a retirement exists to avoid.
    """
    if not isinstance(text, str) or not text.strip():
        raise OntologyError(f"{subject} must be a dotted version string")
    parts = text.strip().split(".")
    if not all(part.isdigit() for part in parts):
        raise OntologyError(
            f"{subject} must be a dotted version of integers, got {text!r}"
        )
    return tuple(int(part) for part in parts)


def _read_retirement(
    slot: str,
    definition: Mapping[str, Any] | None,
    schema_version: str | None,
    source: Path,
) -> Retirement | None:
    """Read a declared retirement, or refuse a malformed one.

    A retirement without a boundary is the "deprecated forever" state: a marker
    that changes nothing, which is the same defect as a value declared and
    produced by nothing. The boundary is therefore required, and it is compared
    against the version of the schema that DECLARES the retirement, so the
    artifact carries both halves and no reader's clock decides the answer.
    """
    if not isinstance(definition, Mapping):
        return None
    annotations = definition.get("annotations")
    if not isinstance(annotations, Mapping):
        return None
    declared = annotations.get("retires")
    if declared is None:
        return None
    if not isinstance(declared, Mapping):
        raise OntologyError(f"Slot '{slot}' in '{source}': `retires` must be a mapping")
    unknown = sorted(set(declared) - {"stops_at", "reason", "replaced_by"})
    if unknown:
        raise OntologyError(
            f"Slot '{slot}' in '{source}': `retires` carries undeclared keys: "
            f"{', '.join(unknown)}"
        )
    reason = declared.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise OntologyError(
            f"Slot '{slot}' in '{source}': a retirement states its reason. A name "
            f"removed without one leaves the next reader guessing why"
        )
    if "stops_at" not in declared:
        raise OntologyError(
            f"Slot '{slot}' in '{source}': a retirement declares `stops_at`. Without a "
            f"boundary the marker never bites and nothing changes, which is a note "
            f"pretending to be a plan"
        )
    stops_at = _version_tuple(f"Slot '{slot}' in '{source}': `stops_at`", declared["stops_at"])
    replaced_by = declared.get("replaced_by")
    if replaced_by is not None and (not isinstance(replaced_by, str) or not replaced_by.strip()):
        raise OntologyError(f"Slot '{slot}' in '{source}': `replaced_by` must be a slot name")
    if schema_version is None:
        raise OntologyError(
            f"Slot '{slot}' in '{source}': a retirement needs the schema to declare its "
            f"own `version`, because the boundary is compared against it"
        )
    current = _version_tuple(f"Schema '{source}' version", schema_version)
    if current >= stops_at:
        successor = (
            f" Use '{replaced_by}'." if replaced_by else " It has no replacement."
        )
        raise OntologyError(
            f"Slot '{slot}' in '{source}' retired at version {declared['stops_at']} and "
            f"this schema is {schema_version}: {reason}.{successor}"
        )
    return Retirement(
        slot=slot,
        schema=str(source),
        stops_at=stops_at,
        stops_at_text=str(declared["stops_at"]),
        reason=reason,
        replaced_by=replaced_by,
    )


def _declares_adoption(definition: Mapping[str, Any] | None) -> bool:
    """Whether a definition says it adopts an existing name rather than claiming it.

    Carried in LinkML's own `annotations`, so the declaration travels with the
    slot and other LinkML tooling ignores it rather than choking. Deliberately
    NOT part of the content-hash payload: adopting a name changes no structural
    fact, and if it did, declaring an adoption would re-anchor every ledger,
    which is absurd for a statement that two definitions already agree.
    """
    if not isinstance(definition, Mapping):
        return False
    annotations = definition.get("annotations")
    if not isinstance(annotations, Mapping):
        return False
    return annotations.get("adopts") is True


def _constraint_difference(
    existing: Mapping[str, Any] | None,
    adopting: Mapping[str, Any] | None,
) -> str:
    """Name every enforced field on which two slot definitions disagree.

    Compares what the validator enforces, not the prose. Description and
    annotations are excluded on purpose: they carry meaning a machine cannot
    check, which is why the adoption has to be declared by a human as well.
    """
    if existing is None or adopting is None:
        return "one of the definitions was not retained for comparison"
    mine, theirs = _constraint(existing), _constraint(adopting)
    differences = [
        f"{field.name} {getattr(mine, field.name)!r} vs {getattr(theirs, field.name)!r}"
        for field in fields(SlotConstraint)
        if getattr(mine, field.name) != getattr(theirs, field.name)
    ]
    return ", ".join(differences)


def _require_optional_type(subject: str, name: str, value: Any, expected: type) -> None:
    if value is not None and not isinstance(value, expected):
        raise OntologyError(f"{subject} {name} must be {expected.__name__}")


def _validate_constraint_definition(subject: str, constraint: SlotConstraint) -> None:
    for name in ("required", "multivalued", "inlined", "identifier"):
        _require_optional_type(subject, name, getattr(constraint, name), bool)
    for name in ("range", "equals_string", "value_presence"):
        _require_optional_type(subject, name, getattr(constraint, name), str)
    for name in ("minimum_value", "maximum_value"):
        value = getattr(constraint, name)
        if value is not None and (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(float(value))
        ):
            raise OntologyError(f"{subject} {name} must be a finite number")
    if (
        constraint.value_presence is not None
        and constraint.value_presence not in _VALUE_PRESENCE_VALUES
    ):
        raise OntologyError(
            f"{subject} value_presence must be one of "
            f"{sorted(_VALUE_PRESENCE_VALUES)}"
        )
    if constraint.required and constraint.value_presence == "ABSENT":
        raise OntologyError(
            f"{subject} cannot be required and have value_presence ABSENT"
        )
    if constraint.equals_string is not None and constraint.value_presence == "ABSENT":
        raise OntologyError(
            f"{subject} cannot declare equals_string and have value_presence ABSENT"
        )


def _merge_constraint(base: SlotConstraint, override: SlotConstraint) -> SlotConstraint:
    values = {}
    for item in fields(SlotConstraint):
        value = getattr(override, item.name)
        values[item.name] = getattr(base, item.name) if value is None else value
    return SlotConstraint(**values)


def _conjoin_expression_constraint(
    base: SlotConstraint,
    condition: SlotConstraint,
    subject: str,
) -> SlotConstraint:
    if (
        base.equals_string is not None
        and condition.equals_string is not None
        and base.equals_string != condition.equals_string
    ):
        raise OntologyError(
            f"{subject} has conflicting equals_string values "
            f"'{base.equals_string}' and '{condition.equals_string}'"
        )

    base_presence = base.value_presence
    condition_presence = condition.value_presence
    if (
        base_presence is not None
        and condition_presence is not None
        and base_presence != condition_presence
    ):
        raise OntologyError(
            f"{subject} has conflicting value_presence values "
            f"'{base_presence}' and '{condition_presence}'"
        )

    values = {item.name: getattr(base, item.name) for item in fields(SlotConstraint)}
    if base.required is True or condition.required is True:
        values["required"] = True
    elif condition.required is not None:
        values["required"] = condition.required
    values["equals_string"] = (
        condition.equals_string
        if condition.equals_string is not None
        else base.equals_string
    )
    values["value_presence"] = (
        condition_presence
        or base_presence
    )
    result = SlotConstraint(**values)
    _validate_constraint_definition(subject, result)
    return result


def _utf8_encodable(value: str) -> bool:
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _canonical_constraint_value(value: Any) -> Any:
    # 0 and 0.0 enforce the same bound; identity must not distinguish them.
    if isinstance(value, float) and not isinstance(value, bool) and value.is_integer():
        return int(value)
    return value


def _constraint_dict(value: SlotConstraint) -> dict[str, Any]:
    result = {}
    for item in fields(SlotConstraint):
        field_value = getattr(value, item.name)
        # `inlined` was added after fingerprint version 3. Omitting its absent
        # value preserves every ontology identity whose enforced behavior did
        # not change.
        if item.name in {"inlined", "value_presence"} and field_value is None:
            continue
        result[item.name] = _canonical_constraint_value(field_value)
    return result


_ABSENT_EQUALS_FALSE = ("required", "multivalued", "inlined", "identifier")


def _normalized_global_slot(constraint: SlotConstraint) -> SlotConstraint:
    """At global-slot level an explicit False enforces exactly like absence;
    identity must not distinguish them. (In slot_usage a False can override a
    True base, so usage constraints stay raw.)"""
    values = {item.name: getattr(constraint, item.name) for item in fields(SlotConstraint)}
    for name in _ABSENT_EQUALS_FALSE:
        if values[name] is False:
            values[name] = None
    return SlotConstraint(**values)


def _inert_usage(typedef: TypeDef, slot_name: str, constraint: SlotConstraint) -> bool:
    """An all-None slot_usage entry for a slot the class already lists in
    slots: neither attaches nor constrains anything; identity skips it."""
    return slot_name in typedef.slots and all(
        getattr(constraint, item.name) is None for item in fields(SlotConstraint)
    )


def _sparse_constraint_dict(value: SlotConstraint) -> dict[str, Any]:
    return {
        item.name: _canonical_constraint_value(field_value)
        for item in fields(SlotConstraint)
        if (field_value := getattr(value, item.name)) is not None
    }


def _expression_dict(expression: ClassExpression) -> dict[str, Any]:
    return {
        "slot_conditions": {
            name: _sparse_constraint_dict(constraint)
            for name, constraint in expression.slot_conditions
        }
    }


def _expression_blob(expression: ClassExpression) -> str:
    return json.dumps(_expression_dict(expression), sort_keys=True, separators=(",", ":"))


def _parse_exactly_one_of(
    subject: str,
    definition: Mapping[str, Any],
) -> tuple[ClassExpression, ...]:
    for key in ("any_of", "all_of", "none_of"):
        if key in definition:
            raise OntologyError(
                f"{subject} uses unsupported class expression key '{key}'"
            )
    if "exactly_one_of" not in definition:
        return ()
    raw_expressions = definition["exactly_one_of"]
    if not isinstance(raw_expressions, list) or not raw_expressions:
        raise OntologyError(f"{subject} exactly_one_of must be a nonempty list")
    expressions = []
    for index, raw_expression in enumerate(raw_expressions):
        expression_subject = f"{subject} exactly_one_of[{index}]"
        if not isinstance(raw_expression, Mapping):
            raise OntologyError(f"{expression_subject} must be a mapping")
        unsupported = sorted(set(raw_expression) - _CLASS_EXPRESSION_KEYS)
        if unsupported:
            raise OntologyError(
                f"{expression_subject} uses unsupported expression keys: {unsupported}"
            )
        conditions = raw_expression.get("slot_conditions")
        if not isinstance(conditions, Mapping) or not conditions:
            raise OntologyError(
                f"{expression_subject} slot_conditions must be a nonempty mapping"
            )
        parsed_conditions = []
        for slot_name, raw_condition in conditions.items():
            condition_subject = f"{expression_subject} slot '{slot_name}'"
            if not isinstance(slot_name, str):
                raise OntologyError(
                    f"{expression_subject} slot condition names must be strings"
                )
            if not isinstance(raw_condition, Mapping):
                raise OntologyError(f"{condition_subject} must be a mapping")
            unsupported = sorted(set(raw_condition) - _SLOT_CONDITION_KEYS)
            if unsupported:
                raise OntologyError(
                    f"{condition_subject} uses unsupported condition keys: {unsupported}"
                )
            condition = _constraint(raw_condition)
            _validate_constraint_definition(condition_subject, condition)
            if all(
                getattr(condition, item.name) is None
                for item in fields(SlotConstraint)
            ):
                raise OntologyError(f"{condition_subject} must declare a constraint")
            parsed_conditions.append((slot_name, condition))
        expressions.append(
            ClassExpression(tuple(sorted(parsed_conditions, key=lambda item: item[0])))
        )
    return tuple(sorted(expressions, key=_expression_blob))


class OntologyRegistry:
    """Resolved ontology registry and closed-world structural validator."""

    def __init__(
        self,
        schema_path: str | Path,
        import_map: Mapping[str, str | Path] | None = None,
    ):
        self._schema_path = Path(schema_path)
        self._entry_path = self._schema_path.resolve()
        self._import_map = {
            name: self._mapped_path(path) for name, path in (import_map or {}).items()
        }
        self._types: dict[str, TypeDef] = {}
        self._enums: dict[str, EnumDef] = {}
        self._slots: dict[str, SlotConstraint] = {}
        self._slot_ranges: dict[str, str] = {}
        self._scalar_types: dict[str, str] = {}
        self._inheritance: dict[str, str | None] = {}
        self._definition_sources: dict[tuple[str, str], Path] = {}
        # Kept so a declared adoption can be checked against what it adopts.
        self._claimed_definitions: dict[tuple[str, str], Any] = {}
        self._retirements: dict[str, Retirement] = {}
        self._loaded_sources: dict[Path, bytes] = {}
        self._import_resolutions: list[OntologyImportResolution] = []
        self._effective_slot_cache: dict[str, dict[str, SlotConstraint]] = {}
        self._schema_name: str | None = None
        self._schema_version: str | None = None
        self._load_schema(self._entry_path)
        self._validate_retirement_successors()
        self._validate_schema()
        self._source_closure = self._build_source_closure()

    def _validate_retirement_successors(self) -> None:
        """A retirement that points nowhere sends the reader to a dead end.

        Checked after the whole closure loads, because the replacement is
        commonly the promoted name in an upstream schema that had not been read
        when the retiring slot was.
        """
        for retirement in self._retirements.values():
            successor = retirement.replaced_by
            if successor is not None and successor not in self._slots:
                raise OntologyError(
                    f"Slot '{retirement.slot}' in '{retirement.schema}' retires in favour "
                    f"of '{successor}', which no schema in this closure declares"
                )

    def _mapped_path(self, path: str | Path) -> Path:
        mapped = Path(path)
        if not mapped.is_absolute():
            mapped = self._schema_path.parent / mapped
        return mapped

    def _claim_name(
        self,
        kind: str,
        name: str,
        source: Path,
        definition: Mapping[str, Any] | None = None,
    ) -> bool:
        """Claim one name, or accept a declared adoption of an existing one.

        Returns True when the caller owns the name and should record its
        definition, False when the name was adopted and the existing definition
        stands.

        A duplicate is a collision by default and stays one. It is an adoption
        only when the second occurrence says so and the two definitions already
        agree. Both halves are load-bearing. Structural agreement alone is not
        enough: two slots can share a range and mean opposite things, which is
        the case that made this necessary, so a human declares the adoption and
        the loader checks the structure. Silence remains an error.

        Without this a promotion is an outage. Pushing a concept up into the
        root, which `ONTOLOGY_PROTOCOL.md` rule 2 asks for once two projects
        need it independently, made every domain that already named it stop
        loading. Not degrade: stop.
        """
        key = (kind, name)
        prior = self._definition_sources.get(key)
        if prior is None:
            self._definition_sources[key] = source
            self._claimed_definitions[key] = definition
            return True
        if not _declares_adoption(definition):
            raise OntologyError(
                f"Duplicate {kind} '{name}' in '{source}' conflicts with '{prior}'. "
                f"If '{source}' adopts the definition in '{prior}', declare it with "
                f"`annotations: {{adopts: true}}` on that {kind}; silence is a collision."
            )
        if kind != "slot":
            raise OntologyError(
                f"{kind.capitalize()} '{name}' in '{source}' declares adoption, which is "
                f"supported for slots only. A {kind} that already exists upstream is "
                f"reused by importing it, not by redeclaring it."
            )
        difference = _constraint_difference(
            self._claimed_definitions.get(key), definition
        )
        if difference:
            raise OntologyError(
                f"Slot '{name}' in '{source}' declares adoption of '{prior}' and differs "
                f"from it: {difference}. Adoption is for a definition that already "
                f"agrees. A different definition is a different concept and needs its "
                f"own name."
            )
        return False

    def _load_schema(self, path: Path) -> None:
        path = path.resolve()
        if path in self._loaded_sources:
            return
        if not path.is_file():
            raise OntologyError(f"Ontology file does not exist: '{path}'")

        try:
            source_bytes = path.read_bytes()
            source_text = source_bytes.decode("utf-8")
            schema = yaml.load(source_text, Loader=UniqueKeyLoader)
        except yaml.YAMLError as error:
            # Malformed YAML is the most common way a schema fails to load;
            # it must be a typed refusal every caller already catches, not a
            # parser traceback.
            raise OntologyError(f"Ontology is not valid YAML: '{path}': {error}") from error
        except UnicodeDecodeError as error:
            raise OntologyError(f"Ontology is not UTF-8: '{path}': {error}") from error
        except OSError as error:
            raise OntologyError(f"Cannot read ontology file '{path}': {error}") from error
        if not isinstance(schema, dict):
            raise OntologyError(f"Ontology must be a YAML mapping: '{path}'")
        locator = str(path)
        if not _utf8_encodable(locator):
            raise OntologyError(
                f"Ontology resolved locator is not UTF-8 encodable: {locator!r}"
            )
        # This mapping is the visited set as well as the retained evidence.
        # Record before descending so cyclic imports terminate without a
        # second loading mechanism or a second read of the same source.
        self._loaded_sources[path] = source_bytes
        declared_version = schema.get("version")
        this_version = None if declared_version is None else str(declared_version)
        if path == self._entry_path:
            declared_name = schema.get("name")
            if declared_name is not None and (
                not isinstance(declared_name, str) or not declared_name.strip()
            ):
                raise OntologyError(
                    f"Ontology name must be a nonblank string: '{path}'"
                )
            self._schema_name = declared_name
            self._schema_version = this_version

        imports = schema.get("imports", [])
        if not isinstance(imports, list) or not all(isinstance(item, str) for item in imports):
            raise OntologyError(f"Ontology imports must be a list of strings: '{path}'")
        for ordinal, imported_name in enumerate(imports):
            if imported_name == "linkml:types":
                self._import_resolutions.append(
                    OntologyImportResolution(
                        parent_locator=locator,
                        ordinal=ordinal,
                        literal=imported_name,
                        target_role="builtin",
                        resolved_locator=imported_name,
                    )
                )
                continue
            imported_path = self._resolve_import(path.parent, imported_name)
            if imported_path is None:
                raise OntologyError(
                    f"Cannot resolve import '{imported_name}' required by '{path}'. "
                    "Provide a local file or an explicit import_map entry."
                )
            imported_path = imported_path.resolve()
            imported_locator = str(imported_path)
            if not _utf8_encodable(imported_locator):
                raise OntologyError(
                    "Ontology import resolved locator is not UTF-8 encodable: "
                    f"{imported_locator!r}"
                )
            self._import_resolutions.append(
                OntologyImportResolution(
                    parent_locator=locator,
                    ordinal=ordinal,
                    literal=imported_name,
                    target_role="ontology",
                    resolved_locator=imported_locator,
                )
            )
            self._load_schema(imported_path)

        for name, definition in self._mapping(schema, "types", path).items():
            if not isinstance(name, str):
                raise OntologyError(f"Type names in '{path}' must be strings")
            self._claim_name("type", name, path, definition if isinstance(definition, dict) else None)
            if not isinstance(definition, dict) or not definition.get("typeof"):
                raise OntologyError(f"Type '{name}' in '{path}' requires typeof")
            if not isinstance(definition["typeof"], str):
                raise OntologyError(f"Type '{name}' typeof in '{path}' must be string")
            self._scalar_types[name] = definition["typeof"]

        for name, definition in self._mapping(schema, "enums", path).items():
            if not isinstance(name, str):
                raise OntologyError(f"Enum names in '{path}' must be strings")
            self._claim_name("enum", name, path, definition if isinstance(definition, dict) else None)
            if not isinstance(definition, dict):
                raise OntologyError(f"Enum '{name}' in '{path}' must be a mapping")
            permissible = definition.get("permissible_values", {})
            if not isinstance(permissible, dict):
                raise OntologyError(
                    f"Enum '{name}' permissible_values in '{path}' must be a mapping"
                )
            if not all(isinstance(value, str) for value in permissible):
                raise OntologyError(f"Enum '{name}' permissible value names must be strings")
            self._enums[name] = EnumDef(name, frozenset(permissible))

        for name, definition in self._mapping(schema, "slots", path).items():
            if not isinstance(name, str):
                raise OntologyError(f"Slot names in '{path}' must be strings")
            if not isinstance(definition, dict):
                raise OntologyError(f"Slot '{name}' in '{path}' must be a mapping")
            slot = _constraint(definition)
            _validate_constraint_definition(f"Slot '{name}'", slot)
            retirement = _read_retirement(name, definition, this_version, path)
            if retirement is not None:
                self._retirements[name] = retirement
            if not self._claim_name("slot", name, path, definition):
                continue  # adopted: the existing definition stands, unchanged
            self._slots[name] = slot
            if slot.range:
                self._slot_ranges[name] = slot.range

        for name, definition in self._mapping(schema, "classes", path).items():
            if not isinstance(name, str):
                raise OntologyError(f"Class names in '{path}' must be strings")
            self._claim_name("class", name, path, definition if isinstance(definition, dict) else None)
            if not isinstance(definition, dict):
                raise OntologyError(f"Class '{name}' in '{path}' must be a mapping")
            direct_slots = definition.get("slots", []) or []
            mixins = definition.get("mixins", []) or []
            usage_data = definition.get("slot_usage", {}) or {}
            if not isinstance(direct_slots, list) or not all(
                isinstance(slot, str) for slot in direct_slots
            ):
                raise OntologyError(f"Class '{name}' slots in '{path}' must be strings")
            if not isinstance(mixins, list) or not all(isinstance(mixin, str) for mixin in mixins):
                raise OntologyError(f"Class '{name}' mixins in '{path}' must be strings")
            if not isinstance(usage_data, dict):
                raise OntologyError(f"Class '{name}' slot_usage in '{path}' must be a mapping")
            slot_usage = {}
            for slot_name, usage in usage_data.items():
                if not isinstance(usage, dict):
                    raise OntologyError(
                        f"Class '{name}' usage for '{slot_name}' in '{path}' must be a mapping"
                    )
                slot_usage[slot_name] = _constraint(usage)
                _validate_constraint_definition(
                    f"Class '{name}' slot '{slot_name}'",
                    slot_usage[slot_name],
                )
            parent = definition.get("is_a")
            _require_optional_type(f"Class '{name}'", "is_a", parent, str)
            for boolean_name in ("mixin", "abstract"):
                if boolean_name in definition and not isinstance(definition[boolean_name], bool):
                    raise OntologyError(
                        f"Class '{name}' {boolean_name} must be bool"
                    )
            typedef = TypeDef(
                name=name,
                parent=parent,
                slots=list(direct_slots),
                slot_usage=slot_usage,
                is_mixin=bool(definition.get("mixin", False)),
                abstract=bool(definition.get("abstract", False)),
                mixins=tuple(dict.fromkeys(mixins)),
                exactly_one_of=_parse_exactly_one_of(
                    f"Class '{name}'",
                    definition,
                ),
            )
            self._types[name] = typedef
            self._inheritance[name] = typedef.parent

    @staticmethod
    def _mapping(schema: Mapping[str, Any], key: str, path: Path) -> Mapping[str, Any]:
        value = schema.get(key, {}) or {}
        if not isinstance(value, dict):
            raise OntologyError(f"Ontology '{key}' must be a mapping: '{path}'")
        return value

    def _resolve_import(self, start_dir: Path, name: str) -> Path | None:
        mapped = self._import_map.get(name)
        if mapped is not None:
            if not mapped.is_file():
                # An explicit map entry that misses must be diagnosed as
                # itself, not as the absence of a map entry.
                raise OntologyError(
                    f"import_map entry '{name}' resolves to '{mapped.resolve()}', "
                    "which is not a file. Relative map paths resolve against the "
                    "schema file's directory, not the working directory."
                )
            return mapped.resolve()

        explicit = Path(name)
        if explicit.suffix in {".yaml", ".yml"} or "/" in name:
            candidate = explicit if explicit.is_absolute() else start_dir / explicit
            return candidate.resolve() if candidate.is_file() else None
        if ":" in name:
            return None

        current = start_dir.resolve()
        while True:
            for suffix in (".yaml", ".yml"):
                candidate = current / f"{name}{suffix}"
                if candidate.is_file():
                    return candidate.resolve()
            if current.parent == current:
                break
            current = current.parent

        # Last resort: an ontology this package ships. `imports: [malleus]`
        # with malleus installed is the commonest adoption shape there is,
        # and refusing it made the inspector report correct schemas as
        # construction heresies on an adopter's first run. A vendored or
        # local copy still wins, above, so root-currency drift stays visible.
        try:
            bundled = bundled_ontology_path(f"{name}.yaml")
        except (OntologyError, OSError):
            return None
        return bundled.resolve() if bundled.is_file() else None

    def _validate_schema(self) -> None:
        range_names = [set(self._types), set(self._enums), set(self._scalar_types)]
        for left_index, left in enumerate(range_names):
            for right in range_names[left_index + 1 :]:
                overlap = left & right
                if overlap:
                    raise OntologyError(
                        f"Ambiguous range name declared in multiple namespaces: '{sorted(overlap)[0]}'"
                    )

        for name, typedef in self._types.items():
            if typedef.parent and typedef.parent not in self._types:
                raise OntologyError(f"Class '{name}' has unknown parent '{typedef.parent}'")
            for mixin in typedef.mixins:
                if mixin not in self._types:
                    raise OntologyError(f"Class '{name}' has unknown mixin '{mixin}'")
            for slot_name in [*typedef.slots, *typedef.slot_usage]:
                if slot_name not in self._slots:
                    raise OntologyError(f"Class '{name}' uses unknown slot '{slot_name}'")

        for name, slot in self._slots.items():
            self._validate_slot_range(f"Slot '{name}'", slot)
        for name, typedef in self._types.items():
            for slot_name, slot in typedef.slot_usage.items():
                self._validate_slot_range(f"Class '{name}' slot '{slot_name}'", slot)
            for slot_name, slot in self.effective_slots(name).items():
                subject = f"Class '{name}' effective slot '{slot_name}'"
                _validate_constraint_definition(subject, slot)
                self._validate_slot_range(subject, slot)

        for name, typedef in self._types.items():
            if name != "Relation" and self.is_subtype_of(name, "Relation") and not typedef.abstract:
                slots = self.effective_slots(name)
                predicate = slots.get("relation_type")
                source = slots.get("source_id")
                target = slots.get("target_id")
                if not predicate or not predicate.equals_string:
                    raise OntologyError(
                        f"Concrete relation '{name}' must fix relation_type with equals_string"
                    )
                for role, endpoint in (("source_id", source), ("target_id", target)):
                    if not endpoint or endpoint.range not in self._types:
                        raise OntologyError(
                            f"Concrete relation '{name}' must declare class-valued {role} range"
                        )
                    if not self.is_subtype_of(endpoint.range, "Entity"):
                        raise OntologyError(
                            f"Concrete relation '{name}' {role} range '{endpoint.range}' "
                            "must be an Entity subtype"
                        )

        for name in self._scalar_types:
            self._resolve_scalar_range(name, set())
        # Force full constraint resolution now. Cyclic inheritance and
        # order-dependent mixin conflicts are construction failures, not
        # surprises at first use; identity can then treat mixin sets as
        # unordered because order is unobservable.
        for name in self._types:
            self.effective_slots(name)
        for name in self._types:
            slots = self.effective_slots(name)
            for group_index, group in enumerate(
                self._class_expression_groups(name, ())
            ):
                for expression_index, expression in enumerate(group):
                    for slot_name, override in expression.slot_conditions:
                        if slot_name not in slots:
                            raise OntologyError(
                                f"Class '{name}' exactly_one_of[{group_index}]"
                                f"[{expression_index}] references unknown slot "
                                f"'{slot_name}'"
                            )
                        subject = (
                            f"Class '{name}' exactly_one_of[{group_index}]"
                            f"[{expression_index}] slot '{slot_name}'"
                        )
                        constraint = _conjoin_expression_constraint(
                            slots[slot_name],
                            override,
                            subject,
                        )
                        self._validate_slot_range(subject, constraint)

    def _validate_slot_range(self, subject: str, slot: SlotConstraint) -> None:
        if slot.range and not self._known_range(slot.range):
            raise OntologyError(f"{subject} has unknown range '{slot.range}'")
        if slot.minimum_value is not None and slot.maximum_value is not None:
            if slot.minimum_value > slot.maximum_value:
                raise OntologyError(f"{subject} has minimum_value above maximum_value")
        if slot.equals_string is not None and slot.range in self._enums:
            if slot.equals_string not in self._enums[slot.range].values:
                raise OntologyError(
                    f"{subject} equals_string '{slot.equals_string}' is not in enum '{slot.range}'"
                )

    def _known_range(self, name: str) -> bool:
        return name in BUILTIN_RANGES or name in self._scalar_types or name in self._enums or name in self._types

    def _resolve_scalar_range(self, name: str, seen: set[str]) -> str:
        if name in LEXICAL_RANGES:
            return LEXICAL_RANGES[name]
        if name in BASE_RANGES:
            return name
        if name not in self._scalar_types:
            raise OntologyError(f"Scalar type chain terminates in unsupported range '{name}'")
        if name in seen:
            raise OntologyError(f"Cyclic scalar type definition at '{name}'")
        return self._resolve_scalar_range(self._scalar_types[name], seen | {name})

    @property
    def schema_path(self) -> Path:
        """The file this registry was built from."""
        return self._schema_path

    def source_closure(self) -> OntologySourceClosure:
        """Return the immutable exact source closure used to build this registry."""
        return self._source_closure

    def _build_source_closure(self) -> OntologySourceClosure:
        entry = OntologySource(
            source_role="entry",
            resolved_locator=str(self._entry_path),
            source_bytes=self._loaded_sources[self._entry_path],
        )
        imported = tuple(
            OntologySource(
                source_role="import",
                resolved_locator=str(path),
                source_bytes=source_bytes,
            )
            for path, source_bytes in sorted(
                self._loaded_sources.items(), key=lambda item: str(item[0])
            )
            if path != self._entry_path
        )
        definitions = tuple(
            OntologyDefinitionSource(
                kind=kind,
                name=name,
                source_locator=str(source),
            )
            for (kind, name), source in sorted(
                self._definition_sources.items(),
                key=lambda item: (item[0][0], item[0][1], str(item[1])),
            )
        )
        imports = tuple(
            sorted(
                self._import_resolutions,
                key=lambda item: (
                    item.parent_locator,
                    item.ordinal,
                    item.literal,
                    item.target_role,
                    item.resolved_locator,
                ),
            )
        )
        return OntologySourceClosure(
            sources=(entry, *imported),
            imports=imports,
            definitions=definitions,
        )

    @property
    def schema_name(self) -> str | None:
        """The entry schema's declared ``name:``, or None if absent."""
        return self._schema_name

    @property
    def schema_version(self) -> str | None:
        """The entry schema's declared `version:`, or None if it declares none."""
        return self._schema_version

    def has_type(self, type_name: str) -> bool:
        return type_name in self._types

    def type_names(self) -> tuple[str, ...]:
        """Return every resolved ontology class name in deterministic order."""
        return tuple(sorted(self._types))

    def has_enum(self, enum_name: str) -> bool:
        return enum_name in self._enums

    def is_valid_enum_value(self, enum_name: str, value: str) -> bool:
        return enum_name in self._enums and value in self._enums[enum_name].values

    def get_enum_values(self, enum_name: str) -> frozenset[str]:
        if enum_name not in self._enums:
            raise KeyError(f"Unknown enum: {enum_name}")
        return self._enums[enum_name].values

    def is_subtype_of(self, child: str, ancestor: str) -> bool:
        current = child
        visited = set()
        while current is not None and current not in visited:
            if current == ancestor:
                return True
            visited.add(current)
            current = self._inheritance.get(current)
        return False

    def has_mixin(self, type_name: str, mixin_name: str) -> bool:
        current = type_name
        visited = set()
        while current is not None and current not in visited:
            visited.add(current)
            typedef = self._types.get(current)
            if typedef and mixin_name in typedef.mixins:
                return True
            current = self._inheritance.get(current)
        return False

    def types_with_mixin(self, mixin_name: str) -> list[str]:
        return sorted(
            name
            for name in self._types
            if name != mixin_name and self.has_mixin(name, mixin_name)
        )

    def get_type(self, type_name: str) -> TypeDef:
        if type_name not in self._types:
            raise KeyError(f"Unknown type: {type_name}")
        return deepcopy(self._types[type_name])

    def effective_slots(self, type_name: str) -> dict[str, SlotConstraint]:
        """Return inherited and mixin slots with the most specific constraints."""
        if type_name not in self._types:
            raise KeyError(f"Unknown type: {type_name}")
        if type_name not in self._effective_slot_cache:
            self._effective_slot_cache[type_name] = self._build_effective_slots(type_name, ())
        return dict(self._effective_slot_cache[type_name])

    def _build_effective_slots(
        self,
        type_name: str,
        trail: tuple[str, ...],
    ) -> dict[str, SlotConstraint]:
        if type_name in trail:
            path = " -> ".join((*trail, type_name))
            raise OntologyError(f"Cyclic class inheritance or mixin path: {path}")
        typedef = self._types[type_name]
        result: dict[str, SlotConstraint] = {}
        next_trail = (*trail, type_name)
        if typedef.parent:
            result.update(self._build_effective_slots(typedef.parent, next_trail))
        mixin_origin: dict[str, str] = {}
        for mixin in typedef.mixins:
            for slot_name, constraint in self._build_effective_slots(mixin, next_trail).items():
                prior = mixin_origin.get(slot_name)
                if prior is not None and result[slot_name] != constraint:
                    raise OntologyError(
                        f"Type '{type_name}': mixins '{prior}' and '{mixin}' declare "
                        f"conflicting constraints for slot '{slot_name}'. Mixin "
                        "resolution must not depend on declaration order; resolve "
                        "the conflict in the mixins themselves (a class's own "
                        "slot_usage is applied after the mixin merge and cannot "
                        "repair it)."
                    )
                mixin_origin[slot_name] = mixin
                result[slot_name] = constraint
        for slot_name in typedef.slots:
            result.setdefault(slot_name, self._slots[slot_name])
        for slot_name, override in typedef.slot_usage.items():
            base = result.get(slot_name, self._slots[slot_name])
            result[slot_name] = _merge_constraint(base, override)
        return result

    def get_slot_constraint(self, type_name: str, slot_name: str) -> SlotConstraint | None:
        if type_name not in self._types:
            return None
        return self.effective_slots(type_name).get(slot_name)

    def validate_enum_field(self, type_name: str, slot_name: str, value: str) -> str | None:
        constraint = self.get_slot_constraint(type_name, slot_name)
        if constraint and constraint.range in self._enums:
            if not self.is_valid_enum_value(constraint.range, value):
                valid = sorted(self.get_enum_values(constraint.range))
                return f"Invalid value '{value}' for {slot_name}. Valid: {valid}"
        return None

    def validate_instance(self, type_name: str, data: Mapping[str, Any]) -> list[str]:
        """Return every closed-world structural violation for one typed record."""
        if type_name not in self._types:
            return [f"Unknown type: '{type_name}'"]
        if not isinstance(data, Mapping):
            return [f"Properties for '{type_name}' must be a mapping"]

        non_string_keys = [
            repr(name)
            for name in data
            if not isinstance(name, str) or not _utf8_encodable(name)
        ]
        if non_string_keys:
            return [
                "Property names must be UTF-8 encodable strings, got: "
                + ", ".join(non_string_keys)
            ]

        slots = self.effective_slots(type_name)
        errors = [
            f"Unknown property '{name}' for {type_name}"
            for name in sorted(set(data) - set(slots))
        ]
        for name, slot in slots.items():
            if (
                slot.required or slot.value_presence == "PRESENT"
            ) and self._missing_required(name, data):
                errors.append(f"Required slot '{name}' missing for {type_name}")
            if slot.value_presence == "ABSENT" and name in data:
                errors.append(f"Property '{name}' must be absent for {type_name}")
        for name, value in data.items():
            slot = slots.get(name)
            if (
                slot is not None
                and slot.value_presence != "ABSENT"
                and value is not None
            ):
                errors.extend(self._validate_value(name, value, slot))
        errors.extend(self._validate_class_expressions(type_name, data, slots))
        return errors

    def _validate_class_expressions(
        self,
        type_name: str,
        data: Mapping[str, Any],
        slots: Mapping[str, SlotConstraint],
    ) -> list[str]:
        errors = []
        for group in self._class_expression_groups(type_name, ()):
            results = [
                self._class_expression_errors(expression, data, slots)
                for expression in group
            ]
            matches = [index for index, result in enumerate(results) if not result]
            if len(matches) == 1:
                continue
            if matches:
                detail = f"matched alternatives {matches}"
            else:
                _, nearest = min(
                    enumerate(results),
                    key=lambda item: (len(item[1]), _expression_blob(group[item[0]])),
                )
                detail = "nearest alternative: " + "; ".join(nearest)
            errors.append(
                f"Class '{type_name}' must satisfy exactly one declared "
                f"alternative; matched {len(matches)}; {detail}"
            )
        return errors

    def _class_expression_groups(
        self,
        type_name: str,
        trail: tuple[str, ...],
    ) -> tuple[tuple[ClassExpression, ...], ...]:
        if type_name in trail:
            return ()
        typedef = self._types[type_name]
        next_trail = (*trail, type_name)
        groups = []
        if typedef.parent:
            groups.extend(self._class_expression_groups(typedef.parent, next_trail))
        for mixin in typedef.mixins:
            groups.extend(self._class_expression_groups(mixin, next_trail))
        if typedef.exactly_one_of:
            groups.append(typedef.exactly_one_of)
        return tuple(dict.fromkeys(groups))

    def _class_expression_errors(
        self,
        expression: ClassExpression,
        data: Mapping[str, Any],
        slots: Mapping[str, SlotConstraint],
    ) -> list[str]:
        errors = []
        for name, override in expression.slot_conditions:
            constraint = _conjoin_expression_constraint(
                slots[name],
                override,
                f"Expression slot '{name}'",
            )
            if constraint.value_presence == "ABSENT":
                if name in data:
                    errors.append(f"Property '{name}' must be absent")
                continue
            if (
                constraint.required or constraint.value_presence == "PRESENT"
            ) and self._missing_required(name, data):
                errors.append(f"missing {name} (required slot '{name}')")
                continue
            if name not in data or data[name] is None:
                if constraint.equals_string is not None:
                    errors.append(
                        f"Property '{name}' must equal '{constraint.equals_string}'"
                    )
                continue
            errors.extend(self._validate_value(name, data[name], constraint))
        return errors

    @staticmethod
    def _missing_required(name: str, data: Mapping[str, Any]) -> bool:
        if name not in data:
            return True
        value = data[name]
        return value is None or value == "" or value == []

    def _validate_value(self, name: str, value: Any, slot: SlotConstraint) -> list[str]:
        if slot.multivalued:
            if not isinstance(value, list):
                return [f"Property '{name}' must be a list"]
            errors = []
            scalar_slot = _merge_constraint(slot, SlotConstraint(multivalued=False))
            for index, item in enumerate(value):
                errors.extend(self._validate_scalar(f"{name}[{index}]", item, scalar_slot))
            return errors
        if isinstance(value, list):
            return [f"Property '{name}' must be singular"]
        return self._validate_scalar(name, value, slot)

    def _validate_scalar(self, name: str, value: Any, slot: SlotConstraint) -> list[str]:
        errors = []
        if isinstance(value, str):
            # The identity layer hashes UTF-8; a value the validator accepts
            # must survive the serialization identity performs. Lone
            # surrogates pass isinstance(str) and json.dumps, then crash the
            # digest. Reject them here so the write is a refusal, not a
            # KeyError three layers down.
            try:
                value.encode("utf-8")
            except UnicodeEncodeError:
                return [f"Property '{name}' must be valid UTF-8 (no lone surrogates)"]
        range_name = slot.range or "string"
        scalar_range = (
            self._resolve_scalar_range(range_name, set())
            if range_name in BUILTIN_RANGES or range_name in self._scalar_types
            else range_name
        )

        if slot.identifier and (not isinstance(value, str) or not value.strip()):
            errors.append(f"Identifier '{name}' must be a nonblank string")
        elif scalar_range == "string" and not isinstance(value, str):
            errors.append(f"Property '{name}' must be a string")
        elif scalar_range == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
            errors.append(f"Property '{name}' must be an integer")
        elif scalar_range == "float" and (
            not isinstance(value, (int, float)) or isinstance(value, bool)
        ):
            errors.append(f"Property '{name}' must be a number")
        elif scalar_range == "float" and not math.isfinite(float(value)):
            errors.append(f"Property '{name}' must be a finite number")
        elif scalar_range == "boolean" and not isinstance(value, bool):
            errors.append(f"Property '{name}' must be a boolean")
        elif scalar_range == "datetime" and not self._valid_datetime(value):
            errors.append(f"Property '{name}' must be an ISO 8601 datetime string")
        elif range_name in self._enums:
            if not isinstance(value, str) or value not in self._enums[range_name].values:
                valid = sorted(self._enums[range_name].values)
                errors.append(f"Invalid value '{value}' for {name}. Valid: {valid}")
        elif range_name in self._types:
            if slot.inlined:
                if not isinstance(value, Mapping):
                    errors.append(f"Inlined property '{name}' must be a mapping")
                else:
                    errors.extend(
                        f"Inlined property '{name}': {error}"
                        for error in self.validate_instance(range_name, value)
                    )
            elif not isinstance(value, str) or not value.strip():
                errors.append(f"Reference '{name}' must be a nonblank identifier")

        if slot.equals_string is not None and value != slot.equals_string:
            errors.append(
                f"Property '{name}' must equal '{slot.equals_string}', got '{value}'"
            )
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if slot.minimum_value is not None and value < slot.minimum_value:
                errors.append(f"Property '{name}' must be at least {slot.minimum_value}")
            if slot.maximum_value is not None and value > slot.maximum_value:
                errors.append(f"Property '{name}' must be at most {slot.maximum_value}")
        return errors

    @staticmethod
    def _valid_datetime(value: Any) -> bool:
        if not isinstance(value, str) or not value.strip():
            return False
        if "T" not in value and "t" not in value and " " not in value:
            return False
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return False
        return True

    def content_hash(self) -> str:
        """Return the versioned hash of every enforced structural fact."""
        return self.content_hash_under(self._fingerprint_version())

    def content_hashes(self) -> dict[int, str]:
        """This schema's content hash under every payload grammar it may carry.

        One schema, several legitimate identities, because the grammar version
        is part of the hashed payload and the rule for choosing it changed. All
        of them describe the same bytes.
        """
        return {g: self.content_hash_under(g) for g in KNOWN_PAYLOAD_GRAMMARS}

    def verifying_grammar(self, recorded_hash: str) -> int | None:
        """Which payload grammar makes a recorded hash match, or None.

        None means the recorded hash does not describe this schema under any
        grammar this release knows, which is a real mismatch and must refuse.
        A returned grammar older than the current one means the record is
        sound and was written by an earlier release; the caller decides whether
        to re-anchor and is told, rather than the hash being quietly redone.
        """
        digest = recorded_hash.split(":", 1)[1] if ":" in recorded_hash else recorded_hash
        for grammar, candidate in self.content_hashes().items():
            if candidate == digest:
                return grammar
        return None

    def retirements(self) -> tuple[Retirement, ...]:
        """Every name declared as retiring, in slot order.

        The loader refuses a name past its boundary. This is the other reader:
        the ones still inside their window, so a retirement is visible before
        it bites rather than only when it does.
        """
        return tuple(self._retirements[name] for name in sorted(self._retirements))

    def verifies(self, *recorded_hashes: str) -> bool:
        """Whether every recorded hash names this schema under some known grammar.

        Use this wherever a hash read back from a record is compared. Equality
        is the wrong question there: the same schema has one identity per
        payload grammar, so a value written by an earlier release compares
        unequal while naming exactly these bytes. Where both sides are computed
        now by the running code they share a grammar by construction, and
        equality is the right question; widening those would accept two
        genuinely different ontologies as one.
        """
        return all(self.verifying_grammar(h) is not None for h in recorded_hashes)

    def content_hash_under(self, grammar: int) -> str:
        """The hash this schema would carry under one payload grammar."""
        if not hasattr(self, "_cached_hashes"):
            self._cached_hashes: dict[int, str] = {}
        if grammar not in self._cached_hashes:
            canonical = {
                "fingerprint_version": grammar,
                "types": {
                    name: {
                        "parent": typedef.parent,
                        "slots": sorted(typedef.slots),
                        "slot_usage": {
                            slot: _constraint_dict(constraint)
                            for slot, constraint in sorted(typedef.slot_usage.items())
                            if not _inert_usage(typedef, slot, constraint)
                        },
                        "is_mixin": typedef.is_mixin,
                        "abstract": typedef.abstract,
                        "mixins": sorted(typedef.mixins),
                        **(
                            {
                                "exactly_one_of": [
                                    _expression_dict(expression)
                                    for expression in typedef.exactly_one_of
                                ]
                            }
                            if typedef.exactly_one_of
                            else {}
                        ),
                    }
                    for name, typedef in sorted(self._types.items())
                },
                "enums": {
                    name: sorted(definition.values)
                    for name, definition in sorted(self._enums.items())
                },
                "slots": {
                    name: _constraint_dict(_normalized_global_slot(definition))
                    for name, definition in sorted(self._slots.items())
                },
                "scalar_types": dict(sorted(self._scalar_types.items())),
            }
            blob = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
            self._cached_hashes[grammar] = hashlib.sha256(blob.encode()).hexdigest()
        return self._cached_hashes[grammar]

    def fingerprint(self) -> frozenset[str]:
        """Return producer-side structural facts, excluding required constraints."""
        if not hasattr(self, "_cached_fingerprint"):
            facts = {f"fingerprint_version:{self._fingerprint_version()}"}
            for name, typedef in self._types.items():
                facts.add(f"type:{name}")
                if typedef.parent:
                    facts.add(f"type:{name}:parent:{typedef.parent}")
                if typedef.is_mixin:
                    facts.add(f"type:{name}:mixin")
                if typedef.abstract:
                    facts.add(f"type:{name}:abstract")
                for mixin in typedef.mixins:
                    facts.add(f"type:{name}:uses_mixin:{mixin}")
                for slot in typedef.slots:
                    facts.add(f"type:{name}:slot:{slot}")
                for slot_name, constraint in typedef.slot_usage.items():
                    if _inert_usage(typedef, slot_name, constraint):
                        continue
                    facts.update(self._constraint_facts(f"type:{name}:usage:{slot_name}", constraint))
                # Membership is an enforced constraint: it decides
                # unknown-property rejection. Walk the same resolved slot
                # table the validator walks, so a slot attached by ANY route
                # (slots:, slot_usage:, parent, mixin) is a fact.
                for slot_name in self.effective_slots(name):
                    facts.add(f"type:{name}:effective_slot:{slot_name}")
                if typedef.exactly_one_of:
                    expressions = [
                        _expression_dict(expression)
                        for expression in typedef.exactly_one_of
                    ]
                    facts.add(
                        f"type:{name}:exactly_one_of:"
                        + json.dumps(expressions, sort_keys=True, separators=(",", ":"))
                    )
            for name, definition in self._enums.items():
                facts.add(f"enum:{name}")
                facts.update(f"enum:{name}:{value}" for value in definition.values)
            for name, definition in self._slots.items():
                facts.add(f"slot:{name}")
                facts.update(
                    self._constraint_facts(f"slot:{name}", _normalized_global_slot(definition))
                )
            for name, base in self._scalar_types.items():
                facts.add(f"scalar_type:{name}:{base}")
            self._cached_fingerprint = frozenset(facts)
        return self._cached_fingerprint

    def _fingerprint_version(self) -> int:
        if any(typedef.exactly_one_of for typedef in self._types.values()):
            return FINGERPRINT_VERSION
        if any(
            constraint.inlined is True or constraint.value_presence is not None
            for constraint in self._slots.values()
        ):
            return FINGERPRINT_VERSION
        if any(
            constraint.inlined is not None or constraint.value_presence is not None
            for typedef in self._types.values()
            for constraint in typedef.slot_usage.values()
        ):
            return FINGERPRINT_VERSION
        return LEGACY_FINGERPRINT_VERSION

    @staticmethod
    def _constraint_facts(prefix: str, constraint: SlotConstraint) -> set[str]:
        facts = set()
        for name in (
            "range",
            "multivalued",
            "inlined",
            "identifier",
            "equals_string",
            "minimum_value",
            "maximum_value",
            "value_presence",
        ):
            value = getattr(constraint, name)
            if value is not None:
                facts.add(f"{prefix}:{name}:{_canonical_constraint_value(value)}")
        return facts

    def fingerprint_serializable(self) -> list[str]:
        return sorted(self.fingerprint())

    def strict_fingerprint(self) -> frozenset[str]:
        """Return structural facts including required constraints."""
        if not hasattr(self, "_cached_strict_fingerprint"):
            facts = set(self.fingerprint())
            for name, definition in self._slots.items():
                if definition.required:
                    facts.add(f"slot:{name}:required")
            for name, typedef in self._types.items():
                for slot_name, constraint in typedef.slot_usage.items():
                    if constraint.required:
                        facts.add(f"type:{name}:usage:{slot_name}:required")
                for slot_name, constraint in self.effective_slots(name).items():
                    if constraint.required:
                        facts.add(f"type:{name}:effective:{slot_name}:required")
            self._cached_strict_fingerprint = frozenset(facts)
        return self._cached_strict_fingerprint

    def strict_fingerprint_serializable(self) -> list[str]:
        return sorted(self.strict_fingerprint())

    def check_compatibility(
        self,
        foreign_hash: str,
        foreign_fingerprint: frozenset[str],
    ) -> str:
        if self.content_hash() == foreign_hash:
            return "identical"
        return _compare_structure(self.fingerprint(), foreign_fingerprint)

    def check_compatibility_strict(
        self,
        foreign_hash: str,
        foreign_strict_fingerprint: frozenset[str],
    ) -> str:
        if self.content_hash() == foreign_hash:
            return "identical"
        return _compare_structure(self.strict_fingerprint(), foreign_strict_fingerprint)

    def fingerprint_grammar(self, foreign_fingerprint: frozenset[str]) -> str:
        """How the foreign fact grammar relates to this one.

        The version is excluded from the structural comparison and answered
        here instead, so it is qualified rather than dropped. `newer` is the
        direction that warrants care: a set produced by a grammar this reader
        does not know may carry fact kinds it cannot interpret, so a structural
        subset test against it is answering a narrower question than it looks.
        """
        theirs = _fingerprint_grammar(foreign_fingerprint)
        if theirs is None:
            return "unknown"
        mine = self._fingerprint_version()
        if theirs == mine:
            return "same"
        return "older" if theirs < mine else "newer"

    @property
    def entity_types(self) -> list[str]:
        return [
            name
            for name in self._types
            if name != "Entity" and self.is_subtype_of(name, "Entity")
        ]

    @property
    def relation_types(self) -> list[str]:
        return [
            name
            for name in self._types
            if name != "Relation" and self.is_subtype_of(name, "Relation")
        ]

    @property
    def signal_types(self) -> list[str]:
        return [
            name
            for name in self._types
            if name != "Signal" and self.is_subtype_of(name, "Signal")
        ]

    @property
    def event_types(self) -> list[str]:
        return [
            name
            for name in self._types
            if name != "Event" and self.is_subtype_of(name, "Event")
        ]

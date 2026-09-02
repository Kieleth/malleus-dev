"""Validated fact artifact reader and LinkML-free structural view."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from hashlib import sha256
import json
import math
from types import MappingProxyType
from typing import Any, Mapping

from malleus._contract_compiler import ContractFact

from .model import (
    ARTIFACT_CAPABILITY,
    ARTIFACT_GRAMMAR,
    CANONICALIZATION,
    CANONICALIZATION_ID,
    EXPRESSION_METAMODEL_ID,
    FACT_NAMESPACE,
    RDF_TYPE,
    RDFS_SUBCLASS,
    SEED_METAMODEL_ID,
    SYMBOL_POLICY,
    SYMBOL_POLICY_ID,
    ArtifactRefusal,
    ArtifactRefusalReason,
    EffectiveConstraints,
    canonical_json,
    metamodel,
)


_KINDS = {
    "Class",
    "Enum",
    "ExactlyOneAlternative",
    "ExactlyOneGroup",
    "Scalar",
    "Slot",
    "SlotCondition",
    "SlotUse",
}
_SEEDS = {
    FACT_NAMESPACE + name
    for name in ("Boolean", "DateTime", "Float", "Integer", "String")
}
_P = {name: FACT_NAMESPACE + name for name in (
    "abstract",
    "enumValue",
    "equalsString",
    "identifier",
    "inAlternative",
    "inGroup",
    "inlined",
    "isMixin",
    "maximum",
    "minimum",
    "multivalued",
    "onClass",
    "required",
    "typeof",
    "usesMixin",
    "usesSlot",
    "valuePresence",
    "valueRange",
)}
_ALLOWED = {
    "Class": {RDF_TYPE, RDFS_SUBCLASS, _P["abstract"], _P["isMixin"], _P["usesMixin"]},
    "Enum": {RDF_TYPE, _P["enumValue"]},
    "Scalar": {RDF_TYPE, _P["typeof"]},
    "Slot": {
        RDF_TYPE,
        _P["equalsString"],
        _P["identifier"],
        _P["inlined"],
        _P["maximum"],
        _P["minimum"],
        _P["multivalued"],
        _P["required"],
        _P["valuePresence"],
        _P["valueRange"],
    },
    "SlotUse": {
        RDF_TYPE,
        _P["equalsString"],
        _P["identifier"],
        _P["inlined"],
        _P["maximum"],
        _P["minimum"],
        _P["multivalued"],
        _P["onClass"],
        _P["required"],
        _P["usesSlot"],
        _P["valuePresence"],
        _P["valueRange"],
    },
    "ExactlyOneGroup": {RDF_TYPE, _P["onClass"]},
    "ExactlyOneAlternative": {RDF_TYPE, _P["inGroup"]},
    "SlotCondition": {
        RDF_TYPE,
        _P["equalsString"],
        _P["inAlternative"],
        _P["required"],
        _P["usesSlot"],
        _P["valuePresence"],
    },
}
_REQUIRED_ONE = {
    "Class": {RDF_TYPE, _P["abstract"], _P["isMixin"]},
    "Enum": {RDF_TYPE},
    "Scalar": {RDF_TYPE, _P["typeof"]},
    "Slot": {
        RDF_TYPE,
        _P["identifier"],
        _P["inlined"],
        _P["multivalued"],
        _P["required"],
        _P["valueRange"],
    },
    "SlotUse": {
        RDF_TYPE,
        _P["identifier"],
        _P["inlined"],
        _P["multivalued"],
        _P["onClass"],
        _P["required"],
        _P["usesSlot"],
        _P["valueRange"],
    },
    "ExactlyOneGroup": {RDF_TYPE, _P["onClass"]},
    "ExactlyOneAlternative": {RDF_TYPE, _P["inGroup"]},
    "SlotCondition": {RDF_TYPE, _P["inAlternative"], _P["usesSlot"]},
}
_MAX_ONE = {
    kind: predicates - ({_P["usesMixin"]} if kind == "Class" else set())
    for kind, predicates in _ALLOWED.items()
}
_MAX_ONE["Enum"] = {RDF_TYPE}


def _refuse(reason: ArtifactRefusalReason, detail: str) -> ArtifactRefusal:
    return ArtifactRefusal(reason, detail)


def _fact_set_digest(facts_sha256: str, metamodel_id: str) -> str:
    envelope = {
        "canonicalization_profile": CANONICALIZATION_ID,
        "domain": "malleus.contract-fact-set/candidate-v0",
        "facts_sha256": facts_sha256.removeprefix("sha256:"),
        "metamodel": metamodel_id,
        "symbol_policy": SYMBOL_POLICY_ID,
    }
    return "sha256:" + sha256(canonical_json(envelope)).hexdigest()


def _acyclic(edges: Mapping[str, tuple[str, ...]]) -> bool:
    state: dict[str, int] = {}
    for root in edges:
        if state.get(root) == 2:
            continue
        stack: list[tuple[str, int]] = [(root, 0)]
        while stack:
            node, index = stack[-1]
            if state.get(node, 0) == 0:
                state[node] = 1
            children = edges.get(node, ())
            if index == len(children):
                state[node] = 2
                stack.pop()
                continue
            child = children[index]
            stack[-1] = (node, index + 1)
            if state.get(child, 0) == 1:
                return False
            if state.get(child, 0) == 0:
                stack.append((child, 0))
    return True


@dataclass(frozen=True, slots=True)
class ContractType:
    name: str
    parent: str | None
    slots: tuple[str, ...]
    is_mixin: bool
    abstract: bool
    mixins: tuple[str, ...]


class ContractView:
    """A fact-backed structural reader with no source or LinkML dependency."""

    __slots__ = (
        "_classes",
        "_content_hash",
        "_enums",
        "_facts",
        "_kinds",
        "_scalars",
        "_sealed",
        "_slot_uses",
        "_slots",
        "_values",
        "artifact_bytes",
    )

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "_sealed", False):
            raise AttributeError("ContractView is immutable")
        object.__setattr__(self, name, value)

    def __init__(
        self,
        facts: tuple[ContractFact, ...],
        *,
        content_hash: str,
        artifact_bytes: bytes,
        metamodel_id: str,
        schema_authorities: tuple[tuple[str, bool], ...],
    ) -> None:
        self._facts = facts
        self._content_hash = content_hash.removeprefix("sha256:")
        self.artifact_bytes = artifact_bytes
        values = _validate_fact_set(facts, metamodel_id)
        _validate_qualified_subjects(values, schema_authorities)
        self._values = MappingProxyType(
            {
                subject: MappingProxyType(dict(predicates))
                for subject, predicates in values.items()
            }
        )
        self._kinds = MappingProxyType({
            subject: str(values[RDF_TYPE][0]).removeprefix(FACT_NAMESPACE)
            for subject, values in self._values.items()
        })
        self._classes = MappingProxyType({
            subject: ContractType(
                name=subject,
                parent=_optional(values, RDFS_SUBCLASS),
                slots=(),
                is_mixin=_boolean(values, _P["isMixin"]),
                abstract=_boolean(values, _P["abstract"]),
                mixins=tuple(str(value) for value in values.get(_P["usesMixin"], ())),
            )
            for subject, values in self._values.items()
            if self._kinds[subject] == "Class"
        })
        self._enums = MappingProxyType({
            subject: frozenset(str(value) for value in values.get(_P["enumValue"], ()))
            for subject, values in self._values.items()
            if self._kinds[subject] == "Enum"
        })
        self._scalars = MappingProxyType({
            subject: str(values[_P["typeof"]][0])
            for subject, values in self._values.items()
            if self._kinds[subject] == "Scalar"
        })
        slot_uses: dict[str, dict[str, EffectiveConstraints]] = defaultdict(dict)
        for subject, values in self._values.items():
            if self._kinds[subject] != "SlotUse":
                continue
            class_id = str(values[_P["onClass"]][0])
            slot_id = str(values[_P["usesSlot"]][0])
            slot_uses[class_id][slot_id] = _constraints(values)
        self._slot_uses = MappingProxyType(
            {
                class_id: MappingProxyType(dict(slots))
                for class_id, slots in slot_uses.items()
            }
        )
        self._slots = MappingProxyType({
            subject: _constraints(values)
            for subject, values in self._values.items()
            if self._kinds[subject] == "Slot"
        })
        self._sealed = True

    @property
    def facts(self) -> tuple[ContractFact, ...]:
        return self._facts

    def content_hash(self) -> str:
        return self._content_hash

    def _resolve(self, value: str, candidates: Mapping[str, object], label: str) -> str:
        if not isinstance(value, str) or not value:
            raise KeyError(f"{label} must be a nonempty string")
        if value in candidates:
            return value
        matches = tuple(sorted(key for key in candidates if key.rsplit("/", 1)[-1] == value))
        if not matches:
            raise KeyError(f"Unknown {label}: {value}")
        if len(matches) != 1:
            raise ValueError(f"Ambiguous {label}: {value}")
        return matches[0]

    def has_type(self, type_name: str) -> bool:
        try:
            self._resolve(type_name, self._classes, "type")
        except (KeyError, ValueError):
            return False
        return True

    def type_names(self) -> tuple[str, ...]:
        return tuple(sorted(self._classes))

    def get_type(self, type_name: str) -> ContractType:
        return self._classes[self._resolve(type_name, self._classes, "type")]

    def has_enum(self, enum_name: str) -> bool:
        try:
            self._resolve(enum_name, self._enums, "enum")
        except (KeyError, ValueError):
            return False
        return True

    def get_enum_values(self, enum_name: str) -> frozenset[str]:
        return self._enums[self._resolve(enum_name, self._enums, "enum")]

    def is_valid_enum_value(self, enum_name: str, value: str) -> bool:
        try:
            return value in self.get_enum_values(enum_name)
        except (KeyError, ValueError):
            return False

    def is_subtype_of(self, child: str, ancestor: str) -> bool:
        try:
            current = self._resolve(child, self._classes, "type")
            target = self._resolve(ancestor, self._classes, "type")
        except (KeyError, ValueError):
            return False
        seen: set[str] = set()
        while current not in seen:
            if current == target:
                return True
            seen.add(current)
            parent = self._classes[current].parent
            if parent is None:
                return False
            current = parent
        return False

    def has_mixin(self, type_name: str, mixin_name: str) -> bool:
        try:
            current = self._resolve(type_name, self._classes, "type")
            target = self._resolve(mixin_name, self._classes, "type")
        except (KeyError, ValueError):
            return False
        seen: set[str] = set()
        pending = [current]
        while pending:
            item = pending.pop()
            if item in seen:
                continue
            seen.add(item)
            definition = self._classes[item]
            if target in definition.mixins:
                return True
            pending.extend(definition.mixins)
            if definition.parent is not None:
                pending.append(definition.parent)
        return False

    def effective_slots(self, type_name: str) -> dict[str, EffectiveConstraints]:
        exact = type_name in self._classes
        class_id = self._resolve(type_name, self._classes, "type")
        qualified = dict(sorted(self._slot_uses.get(class_id, {}).items()))
        if exact:
            return qualified
        local: dict[str, EffectiveConstraints] = {}
        for slot_id, constraint in qualified.items():
            name = slot_id.rsplit("/", 1)[-1]
            if name in local:
                raise ValueError(f"Ambiguous slot: {name}")
            local[name] = constraint
        return local

    def get_slot_constraint(
        self, type_name: str, slot_name: str
    ) -> EffectiveConstraints | None:
        try:
            class_id = self._resolve(type_name, self._classes, "type")
        except (KeyError, ValueError):
            return None
        uses = self._slot_uses.get(class_id, {})
        try:
            slot_id = self._resolve(slot_name, uses, "slot")
        except (KeyError, ValueError):
            return None
        return uses[slot_id]

    def validate_instance(self, type_name: str, data: Mapping[str, Any]) -> list[str]:
        try:
            class_id = self._resolve(type_name, self._classes, "type")
        except (KeyError, ValueError):
            return [f"Unknown type: '{type_name}'"]
        if not isinstance(data, Mapping):
            return [f"Properties for '{type_name}' must be a mapping"]
        uses = self._slot_uses.get(class_id, {})
        normalized: dict[str, Any] = {}
        errors: list[str] = []
        for name, value in data.items():
            if not isinstance(name, str):
                errors.append(f"Property name must be a string: {name!r}")
                continue
            try:
                slot_id = self._resolve(name, uses, "property")
            except (KeyError, ValueError):
                errors.append(f"Unknown property '{name}' for {type_name}")
                continue
            normalized[slot_id] = value
        for slot_id, constraint in uses.items():
            name = slot_id.rsplit("/", 1)[-1]
            value = normalized.get(slot_id)
            if (constraint.required or constraint.value_presence == "PRESENT") and (
                slot_id not in normalized or value is None or value == ""
            ):
                errors.append(f"Required slot '{name}' missing for {type_name}")
            if constraint.value_presence == "ABSENT" and slot_id in normalized:
                errors.append(f"Property '{name}' must be absent for {type_name}")
            if slot_id in normalized and normalized[slot_id] is not None:
                errors.extend(self._validate_value(name, normalized[slot_id], constraint))
        return errors

    def _validate_value(
        self, name: str, value: Any, constraint: EffectiveConstraints
    ) -> list[str]:
        if constraint.multivalued:
            if not isinstance(value, list):
                return [f"Property '{name}' must be a list"]
            errors: list[str] = []
            for index, item in enumerate(value):
                errors.extend(self._validate_scalar(f"{name}[{index}]", item, constraint))
            return errors
        if isinstance(value, list):
            return [f"Property '{name}' must be singular"]
        return self._validate_scalar(name, value, constraint)

    def _validate_scalar(
        self, name: str, value: Any, constraint: EffectiveConstraints
    ) -> list[str]:
        errors: list[str] = []
        terminal = self._terminal(constraint.range_id)
        if constraint.identifier and (not isinstance(value, str) or not value.strip()):
            errors.append(f"Identifier '{name}' must be a nonblank string")
        elif terminal == FACT_NAMESPACE + "String" and not isinstance(value, str):
            errors.append(f"Property '{name}' must be a string")
        elif terminal == FACT_NAMESPACE + "Integer" and (
            not isinstance(value, int) or isinstance(value, bool)
        ):
            errors.append(f"Property '{name}' must be an integer")
        elif terminal == FACT_NAMESPACE + "Float" and (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(float(value))
        ):
            errors.append(f"Property '{name}' must be a finite number")
        elif terminal == FACT_NAMESPACE + "Boolean" and not isinstance(value, bool):
            errors.append(f"Property '{name}' must be a boolean")
        elif terminal == FACT_NAMESPACE + "DateTime" and not _valid_datetime(value):
            errors.append(f"Property '{name}' must be an ISO 8601 datetime string")
        elif constraint.range_id in self._enums:
            if not isinstance(value, str) or value not in self._enums[constraint.range_id]:
                errors.append(f"Invalid value '{value}' for {name}")
        elif constraint.range_id in self._classes:
            if constraint.inlined:
                if not isinstance(value, Mapping):
                    errors.append(f"Inlined property '{name}' must be a mapping")
                else:
                    errors.extend(self.validate_instance(constraint.range_id, value))
            elif not isinstance(value, str) or not value.strip():
                errors.append(f"Reference '{name}' must be a nonblank identifier")
        if constraint.equals_string is not None and value != constraint.equals_string:
            errors.append(f"Property '{name}' must equal '{constraint.equals_string}'")
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if constraint.minimum is not None and Decimal(str(value)) < Decimal(constraint.minimum):
                errors.append(f"Property '{name}' must be at least {constraint.minimum}")
            if constraint.maximum is not None and Decimal(str(value)) > Decimal(constraint.maximum):
                errors.append(f"Property '{name}' must be at most {constraint.maximum}")
        return errors

    def _terminal(self, range_id: str) -> str:
        seen: set[str] = set()
        current = range_id
        while current in self._scalars and current not in seen:
            seen.add(current)
            current = self._scalars[current]
        return current


def _optional(values: Mapping[str, tuple[object, ...]], predicate: str) -> str | None:
    found = values.get(predicate, ())
    return None if not found else str(found[0])


def _boolean(values: Mapping[str, tuple[object, ...]], predicate: str) -> bool:
    value = values[predicate][0]
    if type(value) is not bool:
        raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, f"{predicate} is not Boolean")
    return value


def _constraints(values: Mapping[str, tuple[object, ...]]) -> EffectiveConstraints:
    return EffectiveConstraints(
        range_id=str(values[_P["valueRange"]][0]),
        required=_boolean(values, _P["required"]),
        multivalued=_boolean(values, _P["multivalued"]),
        identifier=_boolean(values, _P["identifier"]),
        inlined=_boolean(values, _P["inlined"]),
        equals_string=_optional(values, _P["equalsString"]),
        minimum=_optional(values, _P["minimum"]),
        maximum=_optional(values, _P["maximum"]),
        value_presence=_optional(values, _P["valuePresence"]),
    )


def _canonical_decimal_lexeme(value: str) -> str:
    try:
        number = Decimal(value)
    except Exception as error:
        raise _refuse(
            ArtifactRefusalReason.INVALID_FACT_SET,
            "numeric predicate object is not decimal",
        ) from error
    if not number.is_finite():
        raise _refuse(
            ArtifactRefusalReason.INVALID_FACT_SET,
            "numeric predicate object is not finite",
        )
    if number.is_zero():
        return "0"
    fixed = format(number, "f")
    return fixed.rstrip("0").rstrip(".") if "." in fixed else fixed


def _terminal_range(
    identifier: str,
    kinds: Mapping[str, str],
    values: Mapping[str, Mapping[str, tuple[object, ...]]],
) -> str:
    current = identifier
    seen: set[str] = set()
    while kinds.get(current) == "Scalar":
        if current in seen:
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "scalar graph is cyclic")
        seen.add(current)
        current = str(values[current][_P["typeof"]][0])
    if current in _SEEDS or kinds.get(current) in {"Class", "Enum"}:
        return current
    raise _refuse(
        ArtifactRefusalReason.INVALID_FACT_SET,
        "scalar or range chain does not terminate in a seed primitive",
    )


def _structural_id(name: str, values: Mapping[str, object]) -> str:
    profiles = {
        "slot_use": (
            "malleus.contract-structure.slot-use/v0",
            "urn:malleus:contract-structure:slot-use:v0:sha256:",
        ),
        "group": (
            "malleus.contract-structure.exactly-one-group/v0",
            "urn:malleus:contract-structure:exactly-one-group:v0:sha256:",
        ),
        "alternative": (
            "malleus.contract-structure.exactly-one-alternative/v0",
            "urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:",
        ),
        "condition": (
            "malleus.contract-structure.slot-condition/v0",
            "urn:malleus:contract-structure:slot-condition:v0:sha256:",
        ),
        "semantics": ("malleus.exactly-one-alternative-semantics/v0", "sha256:"),
    }
    domain, prefix = profiles[name]
    return prefix + sha256(canonical_json({**values, "domain": domain})).hexdigest()


def _validate_expressions(
    kinds: Mapping[str, str],
    values: Mapping[str, Mapping[str, tuple[object, ...]]],
) -> None:
    groups = {subject for subject, kind in kinds.items() if kind == "ExactlyOneGroup"}
    alternatives = {
        subject for subject, kind in kinds.items() if kind == "ExactlyOneAlternative"
    }
    conditions = {subject for subject, kind in kinds.items() if kind == "SlotCondition"}
    uses = {
        (
            str(item[_P["onClass"]][0]),
            str(item[_P["usesSlot"]][0]),
        ): _constraints(item)
        for subject, item in values.items()
        if kinds[subject] == "SlotUse"
    }
    group_members: dict[str, list[str]] = defaultdict(list)
    alternative_members: dict[str, list[str]] = defaultdict(list)
    groups_by_class: dict[str, list[str]] = defaultdict(list)
    for alternative in alternatives:
        group = str(values[alternative][_P["inGroup"]][0])
        if group not in groups:
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "alternative group target invalid")
        group_members[group].append(alternative)
    for condition in conditions:
        alternative = str(values[condition][_P["inAlternative"]][0])
        if alternative not in alternatives:
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "condition alternative target invalid")
        alternative_members[alternative].append(condition)
    for group in groups:
        class_id = str(values[group][_P["onClass"]][0])
        if kinds.get(class_id) != "Class":
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "expression class target invalid")
        groups_by_class[class_id].append(group)
        if not group_members[group]:
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "expression group is empty")
        semantic_digests: list[str] = []
        for alternative in group_members[group]:
            members = alternative_members[alternative]
            if not members:
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "expression alternative is empty")
            semantic_conditions: list[dict[str, object]] = []
            slots: set[str] = set()
            for condition in members:
                item = values[condition]
                slot_id = str(item[_P["usesSlot"]][0])
                if kinds.get(slot_id) != "Slot" or slot_id in slots:
                    raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "condition slot invalid or repeated")
                slots.add(slot_id)
                applicable = uses.get((class_id, slot_id))
                if applicable is None:
                    raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "condition slot is not applicable")
                semantic: dict[str, object] = {"slot": slot_id}
                if _P["required"] in item:
                    semantic["required"] = _boolean(item, _P["required"])
                if _P["equalsString"] in item:
                    value = item[_P["equalsString"]][0]
                    if type(value) is not str:
                        raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "condition equalsString invalid")
                    terminal = _terminal_range(applicable.range_id, kinds, values)
                    if terminal != FACT_NAMESPACE + "String" and kinds.get(applicable.range_id) != "Enum":
                        raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "condition equalsString range invalid")
                    semantic["equalsString"] = value
                if _P["valuePresence"] in item:
                    presence = item[_P["valuePresence"]][0]
                    if presence not in {"PRESENT", "ABSENT"}:
                        raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "condition valuePresence invalid")
                    semantic["valuePresence"] = presence
                if len(semantic) == 1:
                    raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "condition has no enforcing member")
                if semantic.get("valuePresence") == "ABSENT" and (
                    semantic.get("required") is True or "equalsString" in semantic
                ):
                    raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "condition ABSENT conflict")
                expected_condition = _structural_id(
                    "condition", {"alternative": alternative, "slot": slot_id}
                )
                if condition != expected_condition:
                    raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "condition identity mismatch")
                semantic_conditions.append(semantic)
            semantic_conditions.sort(key=canonical_json)
            semantic_digest = _structural_id(
                "semantics", {"conditions": semantic_conditions}
            )
            expected_alternative = _structural_id(
                "alternative",
                {"alternative_semantic_digest": semantic_digest, "group": group},
            )
            if alternative != expected_alternative:
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "alternative identity mismatch")
            semantic_digests.append(semantic_digest)
        if len(semantic_digests) != len(set(semantic_digests)):
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "duplicate semantic alternative")
        expected_group = _structural_id(
            "group",
            {
                "alternative_semantic_digests": sorted(semantic_digests),
                "class": class_id,
            },
        )
        if group != expected_group:
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "group identity mismatch")
    if any(len(items) > 1 for items in groups_by_class.values()):
        raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "class has multiple expression groups")


def _validate_fact_set(
    facts: tuple[ContractFact, ...],
    metamodel_id: str,
) -> dict[str, dict[str, tuple[object, ...]]]:
    if len(set(facts)) != len(facts):
        raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "duplicate fact")
    grouped: dict[str, dict[str, list[object]]] = defaultdict(lambda: defaultdict(list))
    for fact in facts:
        if type(fact.subject) is not str or type(fact.predicate) is not str:
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "fact identifiers must be strings")
        if type(fact.object) not in {bool, str}:
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "invalid fact object")
        grouped[fact.subject][fact.predicate].append(fact.object)
    frozen = {
        subject: {predicate: tuple(objects) for predicate, objects in predicates.items()}
        for subject, predicates in grouped.items()
    }
    kinds: dict[str, str] = {}
    for subject, values in frozen.items():
        if subject in _SEEDS:
            raise _refuse(
                ArtifactRefusalReason.INVALID_FACT_SET,
                "seed primitives cannot be fact subjects",
            )
        type_values = values.get(RDF_TYPE, ())
        if len(type_values) != 1 or type(type_values[0]) is not str:
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, f"{subject} needs one kind")
        kind_iri = str(type_values[0])
        if not kind_iri.startswith(FACT_NAMESPACE):
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, f"{subject} has unknown kind")
        kind = kind_iri.removeprefix(FACT_NAMESPACE)
        if kind not in _KINDS:
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, f"{subject} has unknown kind")
        kinds[subject] = kind
        identifier_predicates = {
            RDFS_SUBCLASS,
            _P["inAlternative"],
            _P["inGroup"],
            _P["onClass"],
            _P["typeof"],
            _P["usesMixin"],
            _P["usesSlot"],
            _P["valueRange"],
        }
        boolean_predicates = {
            _P["abstract"],
            _P["identifier"],
            _P["inlined"],
            _P["isMixin"],
            _P["multivalued"],
            _P["required"],
        }
        for predicate in identifier_predicates & set(values):
            if any(type(value) is not str for value in values[predicate]):
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "identifier object is not a string")
        for predicate in boolean_predicates & set(values):
            if any(type(value) is not bool for value in values[predicate]):
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "Boolean object has wrong type")
        for predicate in {
            _P["enumValue"],
            _P["equalsString"],
            _P["maximum"],
            _P["minimum"],
            _P["valuePresence"],
        } & set(values):
            if any(type(value) is not str for value in values[predicate]):
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "string object has wrong type")
        unknown = set(values) - _ALLOWED[kind]
        if unknown:
            raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, f"{subject} has unknown predicate")
        for predicate in _REQUIRED_ONE[kind]:
            if len(values.get(predicate, ())) != 1:
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, f"{subject} misses {predicate}")
        for predicate in _MAX_ONE[kind]:
            if len(values.get(predicate, ())) > 1:
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, f"{subject} repeats {predicate}")
    expression_present = any(kind in {
        "ExactlyOneAlternative", "ExactlyOneGroup", "SlotCondition"
    } for kind in kinds.values())
    expected_metamodel = (
        EXPRESSION_METAMODEL_ID if expression_present else SEED_METAMODEL_ID
    )
    if metamodel_id != expected_metamodel:
        raise _refuse(
            ArtifactRefusalReason.INVALID_FACT_SET,
            "fact kinds do not match the bound metamodel",
        )
    class_edges: dict[str, tuple[str, ...]] = {}
    for subject, kind in kinds.items():
        values = frozen[subject]
        if kind == "Class":
            targets = tuple(str(value) for value in values.get(RDFS_SUBCLASS, ())) + tuple(
                str(value) for value in values.get(_P["usesMixin"], ())
            )
            if any(kinds.get(target) != "Class" for target in targets):
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "class edge target is not a Class")
            for target in values.get(_P["usesMixin"], ()):
                if frozen[str(target)][_P["isMixin"]] != (True,):
                    raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "mixin target is not a mixin")
            class_edges[subject] = targets
        elif kind == "Scalar":
            target = str(values[_P["typeof"]][0])
            if target not in _SEEDS and kinds.get(target) != "Scalar":
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "invalid scalar target")
        elif kind in {"Slot", "SlotUse"}:
            range_id = str(values[_P["valueRange"]][0])
            if range_id not in _SEEDS and kinds.get(range_id) not in {"Class", "Enum", "Scalar"}:
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "invalid range target")
            constraints = _constraints(values)
            if constraints.value_presence not in {None, "PRESENT", "ABSENT"}:
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "invalid valuePresence")
            terminal = _terminal_range(range_id, kinds, frozen)
            if constraints.inlined and kinds.get(range_id) != "Class":
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "inlined range is not a Class")
            if constraints.equals_string is not None and not (
                terminal == FACT_NAMESPACE + "String" or kinds.get(range_id) == "Enum"
            ):
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "equalsString range is invalid")
            for decimal in (constraints.minimum, constraints.maximum):
                if decimal is not None and _canonical_decimal_lexeme(decimal) != decimal:
                    raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "numeric lexical form is not canonical")
            if (constraints.minimum is not None or constraints.maximum is not None) and terminal not in {
                FACT_NAMESPACE + "Integer", FACT_NAMESPACE + "Float"
            }:
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "numeric bound range is invalid")
            if constraints.minimum is not None and constraints.maximum is not None:
                if Decimal(constraints.minimum) > Decimal(constraints.maximum):
                    raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "minimum exceeds maximum")
            if constraints.value_presence == "ABSENT" and (
                constraints.required or constraints.equals_string is not None
            ):
                raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "ABSENT constraint conflict")
            if kind == "SlotUse":
                if kinds.get(str(values[_P["onClass"]][0])) != "Class":
                    raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "SlotUse class target invalid")
                if kinds.get(str(values[_P["usesSlot"]][0])) != "Slot":
                    raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "SlotUse slot target invalid")
                expected = _structural_id(
                    "slot_use",
                    {
                        "class": str(values[_P["onClass"]][0]),
                        "slot": str(values[_P["usesSlot"]][0]),
                    },
                )
                if subject != expected:
                    raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "SlotUse identity mismatch")
                if constraints.identifier and not constraints.required:
                    raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "identifier SlotUse is not required")
    if not _acyclic(class_edges):
        raise _refuse(ArtifactRefusalReason.INVALID_FACT_SET, "class graph is cyclic")
    for subject, kind in kinds.items():
        if kind == "Scalar":
            _terminal_range(subject, kinds, frozen)
    if expression_present:
        _validate_expressions(kinds, frozen)
    return frozen


def _validate_qualified_subjects(
    values: Mapping[str, Mapping[str, tuple[object, ...]]],
    schema_authorities: tuple[tuple[str, bool], ...],
) -> None:
    structural = {
        "ExactlyOneAlternative": "urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:",
        "ExactlyOneGroup": "urn:malleus:contract-structure:exactly-one-group:v0:sha256:",
        "SlotCondition": "urn:malleus:contract-structure:slot-condition:v0:sha256:",
        "SlotUse": "urn:malleus:contract-structure:slot-use:v0:sha256:",
    }
    for subject, predicates in values.items():
        kind = str(predicates[RDF_TYPE][0]).removeprefix(FACT_NAMESPACE)
        if kind in structural:
            if not subject.startswith(structural[kind]):
                raise _refuse(
                    ArtifactRefusalReason.INVALID_FACT_SET,
                    "structural subject violates the bound symbol policy",
                )
            continue
        owners = [
            (schema_id, trusted)
            for schema_id, trusted in schema_authorities
            if subject.startswith(schema_id + "/")
            and len(subject) > len(schema_id) + 1
        ]
        if not owners or max(owners, key=lambda owner: len(owner[0]))[1]:
            raise _refuse(
                ArtifactRefusalReason.INVALID_FACT_SET,
                "declaration subject has no nontrusted evidenced owner",
            )


def _exact_object(value: object, keys: set[str], label: str) -> dict[str, object]:
    if type(value) is not dict or set(value) != keys:
        raise _refuse(
            ArtifactRefusalReason.MALFORMED_ARTIFACT,
            f"{label} members are not exact",
        )
    return value


def _nonempty_string(value: object, label: str) -> str:
    if type(value) is not str or not value:
        raise _refuse(
            ArtifactRefusalReason.MALFORMED_ARTIFACT,
            f"{label} must be a nonempty string",
        )
    return value


def _sha256_string(value: object, label: str) -> str:
    digest = _nonempty_string(value, label)
    if (
        not digest.startswith("sha256:")
        or len(digest) != 71
        or any(character not in "0123456789abcdef" for character in digest[7:])
    ):
        raise _refuse(
            ArtifactRefusalReason.MALFORMED_ARTIFACT,
            f"{label} is not a SHA-256 identity",
        )
    return digest


def _resolver_evidence(value: object, label: str) -> dict[str, object]:
    result = _exact_object(
        value,
        {"configuration_id", "profile_version", "resolver_id"},
        label,
    )
    for field in result:
        _nonempty_string(result[field], f"{label}.{field}")
    return result


def _identity_evidence(value: object, label: str) -> None:
    result = _exact_object(value, {"id", "sha256"}, label)
    _nonempty_string(result["id"], f"{label}.id")
    _sha256_string(result["sha256"], f"{label}.sha256")


def _validate_evidence(value: object) -> tuple[tuple[str, bool], ...]:
    evidence = _exact_object(
        value,
        {
            "adapter",
            "annotations",
            "binder",
            "imports",
            "producer",
            "root",
            "selection",
            "sources",
        },
        "evidence",
    )
    for identity in ("adapter", "binder", "producer"):
        _identity_evidence(evidence[identity], f"evidence.{identity}")
    selection = _resolver_evidence(evidence["selection"], "evidence.selection")
    root = _exact_object(
        evidence["root"],
        {"requested_locator", "resolved_locator", "resolver", "source_sha256"},
        "evidence.root",
    )
    _nonempty_string(root["requested_locator"], "evidence.root.requested_locator")
    resolved_root = _nonempty_string(
        root["resolved_locator"], "evidence.root.resolved_locator"
    )
    root_sha256 = _sha256_string(
        root["source_sha256"], "evidence.root.source_sha256"
    )
    if _resolver_evidence(root["resolver"], "evidence.root.resolver") != selection:
        raise _refuse(
            ArtifactRefusalReason.MALFORMED_ARTIFACT,
            "root resolver differs from closure selection",
        )
    sources = evidence["sources"]
    if type(sources) is not list or not sources:
        raise _refuse(
            ArtifactRefusalReason.MALFORMED_ARTIFACT,
            "evidence.sources must be a nonempty array",
        )
    source_by_id: dict[str, tuple[str, str, bool]] = {}
    schema_authorities: list[tuple[str, bool]] = []
    seen_schema_ids: set[str] = set()
    for index, raw in enumerate(sources):
        source = _exact_object(
            raw,
            {
                "byte_length",
                "media_type",
                "module_id",
                "resolver",
                "schema_id",
                "sha256",
                "trusted",
            },
            f"evidence.sources[{index}]",
        )
        module_id = _nonempty_string(
            source["module_id"], f"evidence.sources[{index}].module_id"
        )
        schema_id = _nonempty_string(
            source["schema_id"], f"evidence.sources[{index}].schema_id"
        )
        byte_length = source["byte_length"]
        if type(byte_length) is not int or byte_length < 0:
            raise _refuse(
                ArtifactRefusalReason.MALFORMED_ARTIFACT,
                "source byte_length must be a nonnegative integer",
            )
        _nonempty_string(source["media_type"], "source media_type")
        source_sha256 = _sha256_string(source["sha256"], "source sha256")
        trusted = source["trusted"]
        if type(trusted) is not bool:
            raise _refuse(
                ArtifactRefusalReason.MALFORMED_ARTIFACT,
                "source trusted flag must be Boolean",
            )
        if _resolver_evidence(source["resolver"], "source resolver") != selection:
            raise _refuse(
                ArtifactRefusalReason.MALFORMED_ARTIFACT,
                "source resolver differs from closure selection",
            )
        if module_id in source_by_id or schema_id in seen_schema_ids:
            raise _refuse(
                ArtifactRefusalReason.MALFORMED_ARTIFACT,
                "evidence repeats a source module or schema",
            )
        source_by_id[module_id] = (schema_id, source_sha256, trusted)
        seen_schema_ids.add(schema_id)
        schema_authorities.append((schema_id, trusted))
    if source_by_id.get(resolved_root, (None, None))[1] != root_sha256:
        raise _refuse(
            ArtifactRefusalReason.MALFORMED_ARTIFACT,
            "root source does not resolve in evidence.sources",
        )
    annotations = evidence["annotations"]
    if type(annotations) is not list:
        raise _refuse(
            ArtifactRefusalReason.MALFORMED_ARTIFACT,
            "evidence.annotations must be an array",
        )
    for index, raw in enumerate(annotations):
        annotation = _exact_object(
            raw,
            {"module_id", "path", "value"},
            f"evidence.annotations[{index}]",
        )
        if annotation["module_id"] not in source_by_id:
            raise _refuse(
                ArtifactRefusalReason.MALFORMED_ARTIFACT,
                "annotation names an unknown source module",
            )
        path = annotation["path"]
        if type(path) is not list or any(
            type(member) not in {str, int}
            or (type(member) is str and not member)
            or (type(member) is int and member < 0)
            for member in path
        ):
            raise _refuse(
                ArtifactRefusalReason.MALFORMED_ARTIFACT,
                "annotation path is malformed",
            )
    imports = evidence["imports"]
    if type(imports) is not list:
        raise _refuse(
            ArtifactRefusalReason.MALFORMED_ARTIFACT,
            "evidence.imports must be an array",
        )
    edges: set[tuple[str, int]] = set()
    adjacency: dict[str, list[str]] = {module_id: [] for module_id in source_by_id}
    ordinals_by_parent: dict[str, list[int]] = defaultdict(list)
    for index, raw in enumerate(imports):
        edge = _exact_object(
            raw,
            {
                "child_module_id",
                "literal",
                "ordinal",
                "parent_module_id",
                "resolver",
            },
            f"evidence.imports[{index}]",
        )
        parent = _nonempty_string(edge["parent_module_id"], "import parent")
        child = _nonempty_string(edge["child_module_id"], "import child")
        _nonempty_string(edge["literal"], "import literal")
        ordinal = edge["ordinal"]
        if (
            parent not in source_by_id
            or child not in source_by_id
            or type(ordinal) is not int
            or ordinal < 0
            or (parent, ordinal) in edges
            or _resolver_evidence(edge["resolver"], "import resolver") != selection
        ):
            raise _refuse(
                ArtifactRefusalReason.MALFORMED_ARTIFACT,
                "import edge is malformed",
            )
        edges.add((parent, ordinal))
        adjacency[parent].append(child)
        ordinals_by_parent[parent].append(ordinal)
    if any(
        sorted(ordinals) != list(range(len(ordinals)))
        for ordinals in ordinals_by_parent.values()
    ):
        raise _refuse(
            ArtifactRefusalReason.MALFORMED_ARTIFACT,
            "import ordinals are not contiguous and zero-based",
        )
    if not _acyclic({
        module_id: tuple(children) for module_id, children in adjacency.items()
    }):
        raise _refuse(
            ArtifactRefusalReason.MALFORMED_ARTIFACT,
            "evidenced import graph is cyclic",
        )
    reachable: set[str] = set()
    pending = [resolved_root]
    while pending:
        module_id = pending.pop()
        if module_id in reachable:
            continue
        reachable.add(module_id)
        pending.extend(adjacency[module_id])
    if reachable != set(source_by_id):
        raise _refuse(
            ArtifactRefusalReason.MALFORMED_ARTIFACT,
            "evidenced sources do not form one rooted import closure",
        )
    return tuple(sorted(schema_authorities))


def _valid_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return "T" in value or "t" in value or " " in value


def _reject_nonfinite_json(value: str) -> None:
    raise ValueError(f"non-finite JSON value {value}")


def load_validated_contract_artifact(artifact_bytes: bytes) -> ContractView:
    """Load exact artifact bytes without touching source, LinkML, or a registry."""

    if type(artifact_bytes) is not bytes:
        raise _refuse(ArtifactRefusalReason.MALFORMED_ARTIFACT, "artifact must be bytes")
    try:
        payload = json.loads(
            artifact_bytes.decode("utf-8"),
            parse_constant=_reject_nonfinite_json,
        )
    except (UnicodeDecodeError, ValueError) as error:
        raise _refuse(ArtifactRefusalReason.MALFORMED_ARTIFACT, "invalid canonical JSON") from error
    if not isinstance(payload, dict):
        raise _refuse(ArtifactRefusalReason.MALFORMED_ARTIFACT, "artifact root must be an object")
    try:
        canonical = canonical_json(payload)
    except (TypeError, UnicodeEncodeError, ValueError) as error:
        raise _refuse(
            ArtifactRefusalReason.MALFORMED_ARTIFACT,
            "artifact contains a non-canonical JSON value",
        ) from error
    if canonical != artifact_bytes:
        raise _refuse(ArtifactRefusalReason.ARTIFACT_INTEGRITY_MISMATCH, "artifact bytes are not canonical")
    if payload.get("grammar") != ARTIFACT_GRAMMAR:
        raise _refuse(
            ArtifactRefusalReason.UNSUPPORTED_ARTIFACT_GRAMMAR,
            "unknown validated artifact grammar",
        )
    expected_keys = {
        "canonicalization",
        "capability",
        "evidence",
        "evidence_sha256",
        "fact_count",
        "facts",
        "facts_sha256",
        "grammar",
        "metamodel",
        "symbol_policy",
        "validated_fact_set_sha256",
    }
    if set(payload) != expected_keys or payload.get("capability") != ARTIFACT_CAPABILITY:
        raise _refuse(ArtifactRefusalReason.MALFORMED_ARTIFACT, "artifact members are not exact")
    evidence = payload["evidence"]
    evidence_sha256 = "sha256:" + sha256(canonical_json(evidence)).hexdigest()
    if payload["evidence_sha256"] != evidence_sha256:
        raise _refuse(
            ArtifactRefusalReason.ARTIFACT_INTEGRITY_MISMATCH,
            "evidence digest mismatch",
        )
    schema_authorities = _validate_evidence(evidence)
    declared_metamodel = payload["metamodel"]
    known_metamodels = {
        identity: metamodel(identity)
        for identity in (SEED_METAMODEL_ID, EXPRESSION_METAMODEL_ID)
    }
    if (
        not isinstance(declared_metamodel, dict)
        or declared_metamodel not in known_metamodels.values()
        or payload["canonicalization"] != CANONICALIZATION
        or payload["symbol_policy"] != SYMBOL_POLICY
    ):
        raise _refuse(ArtifactRefusalReason.ARTIFACT_INTEGRITY_MISMATCH, "bound semantic identity mismatch")
    metamodel_id = str(declared_metamodel["id"])
    records = payload["facts"]
    if not isinstance(records, list):
        raise _refuse(ArtifactRefusalReason.MALFORMED_ARTIFACT, "facts must be an array")
    facts: list[ContractFact] = []
    for record in records:
        if not isinstance(record, dict) or set(record) != {"object", "predicate", "subject"}:
            raise _refuse(ArtifactRefusalReason.MALFORMED_ARTIFACT, "fact record is not exact")
        facts.append(ContractFact(record["subject"], record["predicate"], record["object"]))
    ordered = sorted(facts, key=lambda fact: canonical_json(fact.as_dict()))
    if facts != ordered:
        raise _refuse(
            ArtifactRefusalReason.ARTIFACT_INTEGRITY_MISMATCH,
            "fact array is not in canonical order",
        )
    canonical_facts = canonical_json([fact.as_dict() for fact in facts])
    facts_sha256 = "sha256:" + sha256(canonical_facts).hexdigest()
    if (
        type(payload["fact_count"]) is not int
        or payload["fact_count"] != len(facts)
        or payload["facts_sha256"] != facts_sha256
    ):
        raise _refuse(ArtifactRefusalReason.ARTIFACT_INTEGRITY_MISMATCH, "fact array digest mismatch")
    validated = _fact_set_digest(facts_sha256, metamodel_id)
    if payload["validated_fact_set_sha256"] != validated:
        raise _refuse(ArtifactRefusalReason.ARTIFACT_INTEGRITY_MISMATCH, "validated fact-set digest mismatch")
    return ContractView(
        tuple(facts),
        content_hash=validated,
        artifact_bytes=artifact_bytes,
        metamodel_id=metamodel_id,
        schema_authorities=schema_authorities,
    )


__all__ = ["ContractType", "ContractView", "load_validated_contract_artifact"]

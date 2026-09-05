"""Elaborate one qualified binding into validated canonical contract facts."""

from __future__ import annotations

from dataclasses import dataclass, fields, replace
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping

from malleus._contract_binder import ContractBinding, QualifiedDeclaration
from malleus._contract_compiler import (
    CompilerImplementation,
    ContractFact,
    NeutralContract,
    SourceAttestation,
    _ContractBuilder,
    _canonical_decimal,
    _encode_facts,
    _load_profile,
)
from malleus._contract_linkml_adapter import (
    AuthoredMapping,
    AuthoredScalar,
    AuthoredSequence,
    AuthoredValue,
)

from .model import (
    ARTIFACT_CAPABILITY,
    ARTIFACT_GRAMMAR,
    CANONICALIZATION,
    EXPRESSION_METAMODEL_ID,
    FACT_NAMESPACE,
    PRODUCER_ID,
    RDFS_SUBCLASS,
    SEED_METAMODEL_ID,
    SYMBOL_POLICY,
    SYMBOL_POLICY_ID,
    AnnotationEvidence,
    ArtifactEvidence,
    EffectiveConstraints,
    ElaboratedAlternative,
    ElaboratedClass,
    ElaboratedCondition,
    ElaboratedContract,
    ElaboratedEnum,
    ElaboratedExpressionGroup,
    ElaboratedScalar,
    ElaboratedSlot,
    ElaboratedSlotUse,
    ElaborationRefusal,
    ElaborationRefusalReason,
    ImportEvidence,
    ResolverEvidence,
    RootEvidence,
    SourceEvidence,
    ValidatedContractArtifact,
    ValidatedContractCompilation,
    canonical_json,
    metamodel,
)
from .view import _fact_set_digest, load_validated_contract_artifact


_MISSING = object()
_SEED_SCALARS = ("Boolean", "DateTime", "Float", "Integer", "String")
_SEED_SCALAR_NAMES = ", ".join(name.lower() for name in _SEED_SCALARS)
_BOOLEAN_FIELDS = ("required", "multivalued", "identifier", "inlined")
_OPTIONAL_FIELDS = ("equals_string", "minimum", "maximum", "value_presence")
_CONSTRAINT_FIELDS = ("range_id", *_BOOLEAN_FIELDS, *_OPTIONAL_FIELDS)
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
_KIND = {name: FACT_NAMESPACE + name for name in (
    "Class",
    "Enum",
    "ExactlyOneAlternative",
    "ExactlyOneGroup",
    "Scalar",
    "Slot",
    "SlotCondition",
    "SlotUse",
)}


def _refuse(reason: ElaborationRefusalReason, detail: str) -> ElaborationRefusal:
    return ElaborationRefusal(reason, detail)


def _fields(value: AuthoredMapping) -> dict[str, AuthoredValue]:
    return {field.name: field.value for field in value.fields}


def _field(value: AuthoredMapping, name: str) -> AuthoredValue | object:
    return _fields(value).get(name, _MISSING)


def _scalar(value: AuthoredValue | object, label: str) -> bool | str | None:
    if not isinstance(value, AuthoredScalar):
        raise _refuse(
            ElaborationRefusalReason.MALFORMED_BINDING,
            f"{label} is not a bound scalar",
        )
    return value.value


def _mapping(value: AuthoredValue | object, label: str) -> AuthoredMapping:
    if not isinstance(value, AuthoredMapping):
        raise _refuse(
            ElaborationRefusalReason.MALFORMED_BINDING,
            f"{label} is not a bound mapping",
        )
    return value


def _sequence(value: AuthoredValue | object, label: str) -> AuthoredSequence:
    if not isinstance(value, AuthoredSequence):
        raise _refuse(
            ElaborationRefusalReason.MALFORMED_BINDING,
            f"{label} is not a bound sequence",
        )
    return value


def _authored_plain(value: AuthoredValue) -> object:
    if isinstance(value, AuthoredScalar):
        return {"kind": value.kind, "lexeme": value.lexeme, "value": value.value}
    if isinstance(value, AuthoredSequence):
        return [_authored_plain(item.value) for item in value.items]
    return {field.name: _authored_plain(field.value) for field in value.fields}


@dataclass(frozen=True, slots=True)
class _UseState:
    constraints: EffectiveConstraints
    explicit: frozenset[str]


class _Elaborator:
    def __init__(self, binding: ContractBinding) -> None:
        if type(binding) is not ContractBinding:
            raise _refuse(
                ElaborationRefusalReason.MALFORMED_BINDING,
                "input must be one exact ContractBinding",
            )
        self.binding = binding
        authoritative = [
            declaration
            for declaration in binding.declarations
            if not declaration.trusted
            and declaration.identifier == declaration.authoritative_identifier
        ]
        self.declarations = {item.identifier: item for item in authoritative}
        if len(self.declarations) != len(authoritative):
            raise _refuse(
                ElaborationRefusalReason.MALFORMED_BINDING,
                "authoritative declaration identifiers are not unique",
            )
        self.references = {
            (item.source_identifier, item.path): item.target_identifier
            for item in binding.references
        }
        if len(self.references) != len(binding.references):
            raise _refuse(
                ElaborationRefusalReason.MALFORMED_BINDING,
                "binding repeats one reference site",
            )
        self.module_schema = {
            module.module_id: module.schema_id
            for module in binding.declared_closure.modules
        }
        self.classes_by_id = {
            item.identifier: item for item in authoritative if item.kind == "Class"
        }
        self.slots_by_id = {
            item.identifier: item for item in authoritative if item.kind == "Slot"
        }
        self.enums_by_id = {
            item.identifier: item for item in authoritative if item.kind == "Enum"
        }
        self.scalars_by_id = {
            item.identifier: item for item in authoritative if item.kind == "Scalar"
        }
        self.class_direct_slots: dict[str, tuple[str, ...]] = {}
        self.class_usage: dict[str, dict[str, dict[str, object]]] = {}
        self.class_parent: dict[str, str | None] = {}
        self.class_mixins: dict[str, tuple[str, ...]] = {}
        self.class_flags: dict[str, tuple[bool, bool]] = {}
        self.slot_constraints: dict[str, EffectiveConstraints] = {}
        self.slot_authored_fields: dict[str, frozenset[str]] = {}
        self._effective_cache: dict[str, dict[str, _UseState]] = {}

    def _reference(
        self,
        source_identifier: str,
        path: tuple[str | int, ...],
        *,
        required: bool = True,
    ) -> str | None:
        result = self.references.get((source_identifier, path))
        if result is None and required:
            raise _refuse(
                ElaborationRefusalReason.MALFORMED_BINDING,
                f"binding omits resolved reference {source_identifier} {path}",
            )
        return result

    def _module_default_range(self, declaration: QualifiedDeclaration) -> str:
        schema_id = self.module_schema[declaration.module_id]
        return self._reference(schema_id, ("default_range",), required=False) or (
            FACT_NAMESPACE + "String"
        )

    def _partial_constraints(
        self,
        body: AuthoredMapping,
        source_identifier: str,
        path: tuple[str | int, ...] = (),
    ) -> dict[str, object]:
        authored = _fields(body)
        result: dict[str, object] = {}
        if "range" in authored:
            result["range_id"] = self._reference(
                source_identifier, path + ("range",)
            )
        for name in _BOOLEAN_FIELDS:
            if name in authored:
                value = _scalar(authored[name], name)
                if type(value) is not bool:
                    raise _refuse(
                        ElaborationRefusalReason.MALFORMED_BINDING,
                        f"{name} is not Boolean",
                    )
                result[name] = value
        if "equals_string" in authored:
            value = _scalar(authored["equals_string"], "equals_string")
            if type(value) is not str:
                raise _refuse(
                    ElaborationRefusalReason.MALFORMED_BINDING,
                    "equals_string is not a string",
                )
            result["equals_string"] = value
        for source_name, target_name in (
            ("minimum_value", "minimum"),
            ("maximum_value", "maximum"),
        ):
            if source_name in authored:
                value = _scalar(authored[source_name], source_name)
                if type(value) is not str:
                    raise _refuse(
                        ElaborationRefusalReason.MALFORMED_BINDING,
                        f"{source_name} is not a decimal lexeme",
                    )
                result[target_name] = _canonical_decimal(value)
        if "value_presence" in authored:
            value = _scalar(authored["value_presence"], "value_presence")
            if value not in {"PRESENT", "ABSENT"}:
                raise _refuse(
                    ElaborationRefusalReason.CONTRADICTORY_CONSTRAINT,
                    "value_presence is outside the closed vocabulary",
                )
            result["value_presence"] = value
        return result

    @staticmethod
    def _merge(
        base: EffectiveConstraints,
        changes: Mapping[str, object],
    ) -> EffectiveConstraints:
        values = {field.name: getattr(base, field.name) for field in fields(base)}
        for name, value in changes.items():
            if name == "minimum" and values[name] is not None:
                value = str(max(Decimal(str(values[name])), Decimal(str(value))))
                value = _canonical_decimal(value)
            elif name == "maximum" and values[name] is not None:
                value = str(min(Decimal(str(values[name])), Decimal(str(value))))
                value = _canonical_decimal(value)
            values[name] = value
        return EffectiveConstraints(**values)

    def _base_constraints(self, declaration: QualifiedDeclaration) -> _UseState:
        partial = self._partial_constraints(declaration.body, declaration.identifier)
        constraint = EffectiveConstraints(
            range_id=str(
                partial.pop("range_id", self._module_default_range(declaration))
            ),
            required=bool(partial.pop("required", False)),
            multivalued=bool(partial.pop("multivalued", False)),
            identifier=bool(partial.pop("identifier", False)),
            inlined=bool(partial.pop("inlined", False)),
            **partial,
        )
        self._validate_constraint(constraint, declaration.identifier, slot_use=False)
        explicit = frozenset(self._partial_constraints(
            declaration.body, declaration.identifier
        ))
        return _UseState(constraint, explicit)

    def _validate_constraint(
        self,
        constraint: EffectiveConstraints,
        subject: str,
        *,
        slot_use: bool,
    ) -> None:
        target = self.declarations.get(constraint.range_id)
        is_seed = constraint.range_id in {
            FACT_NAMESPACE + name for name in _SEED_SCALARS
        }
        if not is_seed and target is None:
            raise _refuse(
                ElaborationRefusalReason.INVALID_RANGE,
                f"{subject} has an unbound range {constraint.range_id}; a "
                f"range binds as one of the seed scalars {_SEED_SCALAR_NAMES}"
                ", or a class or enum declared in the closure",
            )
        target_kind = None if target is None else target.kind
        if constraint.inlined and target_kind != "Class":
            raise _refuse(
                ElaborationRefusalReason.CONTRADICTORY_CONSTRAINT,
                f"{subject} inlines a non-Class range",
            )
        terminal = self._terminal_range(constraint.range_id)
        if (constraint.minimum is not None or constraint.maximum is not None) and terminal not in {
            FACT_NAMESPACE + "Integer",
            FACT_NAMESPACE + "Float",
        }:
            raise _refuse(
                ElaborationRefusalReason.CONTRADICTORY_CONSTRAINT,
                f"{subject} applies numeric bounds to a nonnumeric range",
            )
        if (
            constraint.minimum is not None
            and constraint.maximum is not None
            and Decimal(constraint.minimum) > Decimal(constraint.maximum)
        ):
            raise _refuse(
                ElaborationRefusalReason.CONTRADICTORY_CONSTRAINT,
                f"{subject} minimum exceeds maximum",
            )
        if constraint.equals_string is not None and not (
            terminal == FACT_NAMESPACE + "String" or target_kind == "Enum"
        ):
            raise _refuse(
                ElaborationRefusalReason.CONTRADICTORY_CONSTRAINT,
                f"{subject} equals_string requires a String or Enum range",
            )
        if constraint.value_presence == "ABSENT" and (
            constraint.required or constraint.equals_string is not None
        ):
            raise _refuse(
                ElaborationRefusalReason.CONTRADICTORY_CONSTRAINT,
                f"{subject} ABSENT conflicts with another constraint",
            )
        if slot_use and constraint.identifier and not constraint.required:
            raise _refuse(
                ElaborationRefusalReason.CONTRADICTORY_CONSTRAINT,
                f"{subject} identifier conflicts with required false",
            )

    def _terminal_range(self, identifier: str) -> str:
        current = identifier
        seen: set[str] = set()
        while current in self.scalars_by_id:
            if current in seen:
                raise _refuse(
                    ElaborationRefusalReason.INVALID_RANGE,
                    "scalar range graph is cyclic",
                )
            seen.add(current)
            target = self._reference(current, ("typeof",))
            assert target is not None
            current = target
        return current

    def _prepare_slots(self) -> tuple[ElaboratedSlot, ...]:
        output: list[ElaboratedSlot] = []
        for identifier, declaration in sorted(self.slots_by_id.items()):
            state = self._base_constraints(declaration)
            self.slot_constraints[identifier] = state.constraints
            self.slot_authored_fields[identifier] = state.explicit
            output.append(ElaboratedSlot(identifier, state.constraints))
        return tuple(output)

    def _class_reference_sequence(
        self,
        declaration: QualifiedDeclaration,
        field_name: str,
    ) -> tuple[str, ...]:
        value = _field(declaration.body, field_name)
        if value is _MISSING:
            return ()
        sequence = _sequence(value, field_name)
        return tuple(
            str(self._reference(declaration.identifier, (field_name, item.ordinal)))
            for item in sequence.items
        )

    def _prepare_classes(self) -> tuple[ElaboratedClass, ...]:
        output: list[ElaboratedClass] = []
        for identifier, declaration in sorted(self.classes_by_id.items()):
            body = _fields(declaration.body)
            parent = (
                self._reference(identifier, ("is_a",))
                if "is_a" in body
                else None
            )
            mixins = self._class_reference_sequence(declaration, "mixins")
            if len(mixins) != len(set(mixins)):
                raise _refuse(
                    ElaborationRefusalReason.REPEATED_MIXIN,
                    f"{identifier} repeats a mixin",
                )
            is_mixin = bool(
                _scalar(body["mixin"], "mixin") if "mixin" in body else False
            )
            abstract = bool(
                _scalar(body["abstract"], "abstract")
                if "abstract" in body
                else False
            )
            self.class_parent[identifier] = parent
            self.class_mixins[identifier] = mixins
            self.class_flags[identifier] = (is_mixin, abstract)
            direct = list(self._class_reference_sequence(declaration, "slots"))
            attributes = body.get("attributes")
            if attributes is not None:
                for field in _mapping(attributes, "attributes").fields:
                    local_id = f"{identifier}/{field.name}"
                    if local_id not in self.slots_by_id:
                        raise _refuse(
                            ElaborationRefusalReason.MALFORMED_BINDING,
                            f"{identifier} local slot is absent from binding",
                        )
                    direct.append(local_id)
            if len(direct) != len(set(direct)):
                raise _refuse(
                    ElaborationRefusalReason.AMBIGUOUS_APPLICABLE_SLOT,
                    f"{identifier} repeats one direct slot",
                )
            self.class_direct_slots[identifier] = tuple(direct)
            usage: dict[str, dict[str, object]] = {}
            slot_usage = body.get("slot_usage")
            if slot_usage is not None:
                for field in _mapping(slot_usage, "slot_usage").fields:
                    slot_id = self._reference(
                        identifier, ("slot_usage", field.name)
                    )
                    assert slot_id is not None
                    usage[slot_id] = self._partial_constraints(
                        _mapping(field.value, "slot_usage member"),
                        identifier,
                        ("slot_usage", field.name),
                    )
            self.class_usage[identifier] = usage
            output.append(
                ElaboratedClass(identifier, parent, mixins, is_mixin, abstract)
            )
        self._validate_class_graph()
        return tuple(output)

    def _validate_class_graph(self) -> None:
        edges = {
            identifier: tuple(
                item
                for item in (self.class_parent[identifier], *self.class_mixins[identifier])
                if item is not None
            )
            for identifier in self.classes_by_id
        }
        state: dict[str, int] = {}
        for root in edges:
            if state.get(root) == 2:
                continue
            stack: list[tuple[str, int]] = [(root, 0)]
            while stack:
                node, index = stack[-1]
                state.setdefault(node, 1)
                children = edges.get(node, ())
                if index == len(children):
                    state[node] = 2
                    stack.pop()
                    continue
                child = children[index]
                stack[-1] = (node, index + 1)
                if child not in edges:
                    raise _refuse(
                        ElaborationRefusalReason.MALFORMED_BINDING,
                        f"class edge target {child} is absent",
                    )
                if state.get(child) == 1:
                    raise _refuse(
                        ElaborationRefusalReason.INHERITANCE_CYCLE,
                        f"class graph cycles at {child}",
                    )
                if state.get(child, 0) == 0:
                    stack.append((child, 0))
        for identifier, mixins in self.class_mixins.items():
            for mixin in mixins:
                if not self.class_flags[mixin][0]:
                    raise _refuse(
                        ElaborationRefusalReason.MIXIN_TARGET_NOT_MIXIN,
                        f"{identifier} uses non-mixin {mixin}",
                    )

    def _effective(self, identifier: str) -> dict[str, _UseState]:
        if identifier in self._effective_cache:
            return self._effective_cache[identifier]
        result: dict[str, _UseState] = {}
        parent = self.class_parent[identifier]
        if parent is not None:
            result = dict(self._effective(parent))
        mixin_values: dict[tuple[str, str], object] = {}
        for mixin in self.class_mixins[identifier]:
            for slot_id, state in self._effective(mixin).items():
                changes = {
                    name: getattr(state.constraints, name)
                    for name in state.explicit
                }
                for name, value in changes.items():
                    key = (slot_id, name)
                    prior = mixin_values.get(key, _MISSING)
                    if prior is not _MISSING and prior != value:
                        raise _refuse(
                            ElaborationRefusalReason.MIXIN_CONFLICT,
                            f"{identifier} mixins conflict on {slot_id} {name}",
                        )
                    mixin_values[key] = value
                if slot_id not in result:
                    result[slot_id] = state
                    continue
                prior_state = result[slot_id]
                result[slot_id] = _UseState(
                    self._merge(prior_state.constraints, changes),
                    prior_state.explicit | state.explicit,
                )
        for slot_id in self.class_direct_slots[identifier]:
            result.setdefault(
                slot_id,
                _UseState(
                    self.slot_constraints[slot_id],
                    self.slot_authored_fields[slot_id],
                ),
            )
        for slot_id, changes in self.class_usage[identifier].items():
            if slot_id not in result:
                raise _refuse(
                    ElaborationRefusalReason.SLOT_USAGE_NOT_APPLICABLE,
                    f"{identifier} narrows non-applicable slot {slot_id}",
                )
            prior = result[slot_id]
            result[slot_id] = _UseState(
                self._merge(prior.constraints, changes),
                prior.explicit | frozenset(changes),
            )
        identifiers = 0
        for slot_id, state in result.items():
            constraints = state.constraints
            if constraints.identifier:
                if constraints.required is False and "required" in state.explicit:
                    raise _refuse(
                        ElaborationRefusalReason.CONTRADICTORY_CONSTRAINT,
                        f"{identifier} identifier {slot_id} explicitly refuses required",
                    )
                constraints = replace(constraints, required=True)
                identifiers += 1
            self._validate_constraint(
                constraints,
                f"{identifier} {slot_id}",
                slot_use=True,
            )
            result[slot_id] = _UseState(constraints, state.explicit)
        if identifiers > 1:
            raise _refuse(
                ElaborationRefusalReason.MULTIPLE_IDENTIFIER_SLOTS,
                f"{identifier} has multiple identifier slots",
            )
        self._effective_cache[identifier] = result
        return result

    def _slot_use_id(self, class_id: str, slot_id: str) -> str:
        envelope = {
            "class": class_id,
            "domain": "malleus.contract-structure.slot-use/v0",
            "slot": slot_id,
        }
        return (
            "urn:malleus:contract-structure:slot-use:v0:sha256:"
            + sha256(canonical_json(envelope)).hexdigest()
        )

    def _prepare_slot_uses(self) -> tuple[ElaboratedSlotUse, ...]:
        output = [
            ElaboratedSlotUse(
                self._slot_use_id(class_id, slot_id),
                class_id,
                slot_id,
                state.constraints,
            )
            for class_id in sorted(self.classes_by_id)
            for slot_id, state in sorted(self._effective(class_id).items())
        ]
        return tuple(output)

    def _prepare_enums(self) -> tuple[ElaboratedEnum, ...]:
        output = []
        for identifier, declaration in sorted(self.enums_by_id.items()):
            value = _field(declaration.body, "permissible_values")
            values = () if value is _MISSING else tuple(
                sorted(field.name for field in _mapping(value, "permissible_values").fields)
            )
            output.append(ElaboratedEnum(identifier, values))
        return tuple(output)

    def _prepare_scalars(self) -> tuple[ElaboratedScalar, ...]:
        return tuple(
            ElaboratedScalar(identifier, str(self._reference(identifier, ("typeof",))))
            for identifier in sorted(self.scalars_by_id)
        )

    def _prepare_expressions(self) -> tuple[ElaboratedExpressionGroup, ...]:
        groups: list[ElaboratedExpressionGroup] = []
        for identifier, declaration in sorted(self.classes_by_id.items()):
            value = _field(declaration.body, "exactly_one_of")
            if value is _MISSING:
                continue
            alternatives: list[ElaboratedAlternative] = []
            sequence = _sequence(value, "exactly_one_of")
            for item in sequence.items:
                alternative = _mapping(item.value, "exactly_one_of alternative")
                conditions_value = _field(alternative, "slot_conditions")
                conditions_map = _mapping(conditions_value, "slot_conditions")
                conditions: list[ElaboratedCondition] = []
                seen: set[str] = set()
                for condition_field in conditions_map.fields:
                    slot_id = self._reference(
                        identifier,
                        (
                            "exactly_one_of",
                            item.ordinal,
                            "slot_conditions",
                            condition_field.name,
                        ),
                    )
                    assert slot_id is not None
                    if slot_id in seen or slot_id not in self._effective(identifier):
                        raise _refuse(
                            ElaborationRefusalReason.INVALID_EXPRESSION,
                            f"{identifier} expression slot is repeated or inapplicable",
                        )
                    seen.add(slot_id)
                    body = _fields(_mapping(condition_field.value, "slot condition"))
                    required = (
                        _scalar(body["required"], "required")
                        if "required" in body
                        else None
                    )
                    equals_string = (
                        _scalar(body["equals_string"], "equals_string")
                        if "equals_string" in body
                        else None
                    )
                    value_presence = (
                        _scalar(body["value_presence"], "value_presence")
                        if "value_presence" in body
                        else None
                    )
                    if required is None and equals_string is None and value_presence is None:
                        raise _refuse(
                            ElaborationRefusalReason.INVALID_EXPRESSION,
                            "slot condition is empty",
                        )
                    if value_presence == "ABSENT" and (
                        required is True or equals_string is not None
                    ):
                        raise _refuse(
                            ElaborationRefusalReason.INVALID_EXPRESSION,
                            "ABSENT condition conflicts",
                        )
                    slot_range = self._effective(identifier)[slot_id].constraints
                    if equals_string is not None:
                        target = self.declarations.get(slot_range.range_id)
                        if not (
                            self._terminal_range(slot_range.range_id)
                            == FACT_NAMESPACE + "String"
                            or (target is not None and target.kind == "Enum")
                        ):
                            raise _refuse(
                                ElaborationRefusalReason.INVALID_EXPRESSION,
                                "equals_string condition has a non-string range",
                            )
                    conditions.append(
                        ElaboratedCondition(
                            slot_id,
                            required if type(required) is bool else None,
                            equals_string if type(equals_string) is str else None,
                            value_presence if type(value_presence) is str else None,
                        )
                    )
                ordered = tuple(
                    sorted(conditions, key=lambda value: canonical_json(_condition_dict(value)))
                )
                alternatives.append(ElaboratedAlternative(ordered))
            semantic = [
                canonical_json([_condition_dict(condition) for condition in alternative.conditions])
                for alternative in alternatives
            ]
            if len(semantic) != len(set(semantic)):
                raise _refuse(
                    ElaborationRefusalReason.INVALID_EXPRESSION,
                    "exactly_one_of repeats an alternative",
                )
            groups.append(
                ElaboratedExpressionGroup(
                    identifier,
                    tuple(sorted(alternatives, key=lambda value: canonical_json([
                        _condition_dict(condition) for condition in value.conditions
                    ]))),
                )
            )
        return tuple(groups)

    def elaborate(self) -> ElaboratedContract:
        slots = self._prepare_slots()
        classes = self._prepare_classes()
        slot_uses = self._prepare_slot_uses()
        enums = self._prepare_enums()
        scalars = self._prepare_scalars()
        expressions = self._prepare_expressions()
        adapter_profiles = {
            (module.support_profile, module.profile_sha256)
            for module in self.binding.declared_closure.modules
        }
        if len(adapter_profiles) != 1:
            raise _refuse(
                ElaborationRefusalReason.MALFORMED_BINDING,
                "closure does not bind one adapter profile",
            )
        adapter_id, adapter_hash = next(iter(adapter_profiles))
        return ElaboratedContract(
            classes=classes,
            slots=slots,
            slot_uses=slot_uses,
            enums=enums,
            scalars=scalars,
            expression_groups=expressions,
            adapter_profile_id=adapter_id,
            adapter_profile_sha256=adapter_hash,
            binder_profile_id=self.binding.profile_id,
            binder_profile_sha256=self.binding.profile_sha256,
            metamodel_id=(
                EXPRESSION_METAMODEL_ID if expressions else SEED_METAMODEL_ID
            ),
            symbol_policy_id=SYMBOL_POLICY_ID,
        )


def _condition_dict(value: ElaboratedCondition) -> dict[str, object]:
    result: dict[str, object] = {"slot": value.slot_id}
    if value.required is not None:
        result["required"] = value.required
    if value.equals_string is not None:
        result["equalsString"] = value.equals_string
    if value.value_presence is not None:
        result["valuePresence"] = value.value_presence
    return result


def _emit_constraints(
    builder: _ContractBuilder,
    subject: str,
    constraints: EffectiveConstraints,
) -> None:
    builder.add(subject, _P["valueRange"], constraints.range_id)
    builder.add(subject, _P["required"], constraints.required)
    builder.add(subject, _P["multivalued"], constraints.multivalued)
    builder.add(subject, _P["identifier"], constraints.identifier)
    builder.add(subject, _P["inlined"], constraints.inlined)
    for name, predicate in (
        ("equals_string", _P["equalsString"]),
        ("minimum", _P["minimum"]),
        ("maximum", _P["maximum"]),
        ("value_presence", _P["valuePresence"]),
    ):
        value = getattr(constraints, name)
        if value is not None:
            builder.add(subject, predicate, value)


def _structural(
    name: str,
    role_values: Mapping[str, object],
) -> str:
    profiles = {
        "alternative": (
            "malleus.contract-structure.exactly-one-alternative/v0",
            "urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:",
        ),
        "group": (
            "malleus.contract-structure.exactly-one-group/v0",
            "urn:malleus:contract-structure:exactly-one-group:v0:sha256:",
        ),
        "condition": (
            "malleus.contract-structure.slot-condition/v0",
            "urn:malleus:contract-structure:slot-condition:v0:sha256:",
        ),
        "semantics": ("malleus.exactly-one-alternative-semantics/v0", "sha256:"),
    }
    domain, prefix = profiles[name]
    return prefix + sha256(canonical_json({**role_values, "domain": domain})).hexdigest()


def _facts(elaborated: ElaboratedContract) -> tuple[NeutralContract, tuple[ContractFact, ...]]:
    builder = _ContractBuilder()
    for scalar in elaborated.scalars:
        builder.declare(scalar.identifier, _KIND["Scalar"])
        builder.add(scalar.identifier, _P["typeof"], scalar.typeof_id)
    for enum in elaborated.enums:
        builder.declare(enum.identifier, _KIND["Enum"])
        for value in enum.values:
            builder.add(enum.identifier, _P["enumValue"], value)
    for slot in elaborated.slots:
        builder.declare(slot.identifier, _KIND["Slot"])
        _emit_constraints(builder, slot.identifier, slot.constraints)
    for class_ in elaborated.classes:
        builder.declare(class_.identifier, _KIND["Class"])
        builder.add(class_.identifier, _P["abstract"], class_.abstract)
        builder.add(class_.identifier, _P["isMixin"], class_.is_mixin)
        if class_.parent_id is not None:
            builder.add(class_.identifier, RDFS_SUBCLASS, class_.parent_id)
        for mixin in class_.mixin_ids:
            builder.add(class_.identifier, _P["usesMixin"], mixin)
    for use in elaborated.slot_uses:
        builder.declare(use.identifier, _KIND["SlotUse"])
        builder.add(use.identifier, _P["onClass"], use.class_id)
        builder.add(use.identifier, _P["usesSlot"], use.slot_id)
        _emit_constraints(builder, use.identifier, use.constraints)
    for group in elaborated.expression_groups:
        prepared = []
        for alternative in group.alternatives:
            conditions = [_condition_dict(item) for item in alternative.conditions]
            digest = _structural("semantics", {"conditions": conditions})
            prepared.append((digest, alternative))
        group_id = _structural(
            "group",
            {
                "alternative_semantic_digests": sorted(item[0] for item in prepared),
                "class": group.class_id,
            },
        )
        builder.declare(group_id, _KIND["ExactlyOneGroup"])
        builder.add(group_id, _P["onClass"], group.class_id)
        for semantic_digest, alternative in prepared:
            alternative_id = _structural(
                "alternative",
                {
                    "alternative_semantic_digest": semantic_digest,
                    "group": group_id,
                },
            )
            builder.declare(alternative_id, _KIND["ExactlyOneAlternative"])
            builder.add(alternative_id, _P["inGroup"], group_id)
            for condition in alternative.conditions:
                condition_id = _structural(
                    "condition",
                    {"alternative": alternative_id, "slot": condition.slot_id},
                )
                builder.declare(condition_id, _KIND["SlotCondition"])
                builder.add(condition_id, _P["inAlternative"], alternative_id)
                builder.add(condition_id, _P["usesSlot"], condition.slot_id)
                if condition.required is not None:
                    builder.add(condition_id, _P["required"], condition.required)
                if condition.equals_string is not None:
                    builder.add(condition_id, _P["equalsString"], condition.equals_string)
                if condition.value_presence is not None:
                    builder.add(condition_id, _P["valuePresence"], condition.value_presence)
    contract = builder.finish()
    return contract, _encode_facts(contract, _load_profile(None))


def _evidence(binding: ContractBinding) -> ArtifactEvidence:
    declared = binding.declared_closure
    closure = declared.source_closure

    def resolver(value) -> ResolverEvidence:
        return ResolverEvidence(
            value.resolver_id,
            value.profile_version,
            value.configuration_id,
        )

    annotations = tuple(
        sorted(
            (
                AnnotationEvidence(
                    module.module_id,
                    occurrence.path,
                    canonical_json(_authored_plain(occurrence.value)),
                )
                for module in declared.modules
                for occurrence in module.occurrences
                if occurrence.classification == "ANNOTATION_ONLY"
            ),
            key=lambda item: (
                item.module_id,
                tuple(
                    (0, value) if type(value) is int else (1, value)
                    for value in item.path
                ),
            ),
        )
    )
    producer_inputs = []
    source_root = Path(__file__).parents[1]
    for relative in (
        "_contract_compiler.py",
        "_contract_pipeline/__init__.py",
        "_contract_pipeline/elaborate.py",
        "_contract_pipeline/model.py",
        "_contract_pipeline/view.py",
    ):
        source = source_root.joinpath(relative).read_bytes()
        producer_inputs.append(
            {"path": relative, "sha256": "sha256:" + sha256(source).hexdigest()}
        )
    producer_sha256 = "sha256:" + sha256(canonical_json(producer_inputs)).hexdigest()
    return ArtifactEvidence(
        selection=resolver(closure.selection),
        root=RootEvidence(
            closure.root.requested_locator,
            closure.root.resolved_locator,
            closure.root.source_sha256,
            resolver(closure.root.resolver_selection),
        ),
        sources=tuple(
            sorted(
                (
                    SourceEvidence(
                        module.module_id,
                        module.schema_id,
                        module.source.byte_length,
                        module.source.sha256,
                        module.source.media_type,
                        module.trusted,
                        resolver(module.source.resolver_selection),
                    )
                    for module in declared.modules
                ),
                key=lambda item: item.module_id,
            )
        ),
        annotations=annotations,
        imports=tuple(
            ImportEvidence(
                edge.parent_module_id,
                edge.parent_import_ordinal,
                edge.literal_import,
                edge.child_module_id,
                resolver(edge.resolver_selection),
            )
            for edge in closure.import_edges
        ),
        adapter_profile_id=declared.modules[0].support_profile,
        adapter_profile_sha256=(
            "sha256:" + declared.modules[0].profile_sha256.removeprefix("sha256:")
        ),
        binder_profile_id=binding.profile_id,
        binder_profile_sha256=(
            "sha256:" + binding.profile_sha256.removeprefix("sha256:")
        ),
        producer_id=PRODUCER_ID,
        producer_sha256=producer_sha256,
    )


def _evidence_dict(evidence: ArtifactEvidence) -> dict[str, object]:
    def resolver(value: ResolverEvidence) -> dict[str, str]:
        return {
            "configuration_id": value.configuration_id,
            "profile_version": value.profile_version,
            "resolver_id": value.resolver_id,
        }

    return {
        "adapter": {
            "id": evidence.adapter_profile_id,
            "sha256": evidence.adapter_profile_sha256,
        },
        "annotations": [
            {
                "module_id": item.module_id,
                "path": list(item.path),
                "value": json.loads(item.canonical_value),
            }
            for item in evidence.annotations
        ],
        "binder": {
            "id": evidence.binder_profile_id,
            "sha256": evidence.binder_profile_sha256,
        },
        "imports": [
            {
                "child_module_id": item.child_module_id,
                "literal": item.literal,
                "ordinal": item.ordinal,
                "parent_module_id": item.parent_module_id,
                "resolver": resolver(item.resolver),
            }
            for item in evidence.imports
        ],
        "producer": {
            "id": evidence.producer_id,
            "sha256": evidence.producer_sha256,
        },
        "root": {
            "requested_locator": evidence.root.requested_locator,
            "resolved_locator": evidence.root.resolved_locator,
            "resolver": resolver(evidence.root.resolver),
            "source_sha256": evidence.root.source_sha256,
        },
        "selection": resolver(evidence.selection),
        "sources": [
            {
                "byte_length": item.byte_length,
                "media_type": item.media_type,
                "module_id": item.module_id,
                "schema_id": item.schema_id,
                "sha256": item.sha256,
                "trusted": item.trusted,
                "resolver": resolver(item.resolver),
            }
            for item in evidence.sources
        ],
    }


def compile_binding(binding: ContractBinding) -> ValidatedContractCompilation:
    """Compile one exact qualified binding without reparsing or re-resolving."""

    elaborated = _Elaborator(binding).elaborate()
    contract, facts = _facts(elaborated)
    canonical_facts = canonical_json([fact.as_dict() for fact in facts])
    facts_sha256 = "sha256:" + sha256(canonical_facts).hexdigest()
    validated_sha256 = _fact_set_digest(facts_sha256, elaborated.metamodel_id)
    evidence = _evidence(binding)
    evidence_payload = _evidence_dict(evidence)
    evidence_sha256 = "sha256:" + sha256(canonical_json(evidence_payload)).hexdigest()
    payload = {
        "canonicalization": CANONICALIZATION,
        "capability": ARTIFACT_CAPABILITY,
        "evidence": evidence_payload,
        "evidence_sha256": evidence_sha256,
        "fact_count": len(facts),
        "facts": [fact.as_dict() for fact in facts],
        "facts_sha256": facts_sha256,
        "grammar": ARTIFACT_GRAMMAR,
        "metamodel": metamodel(elaborated.metamodel_id),
        "symbol_policy": SYMBOL_POLICY,
        "validated_fact_set_sha256": validated_sha256,
    }
    artifact_bytes = canonical_json(payload)
    artifact = ValidatedContractArtifact(
        grammar=ARTIFACT_GRAMMAR,
        capability=ARTIFACT_CAPABILITY,
        canonical_facts=canonical_facts,
        facts_sha256=facts_sha256,
        validated_fact_set_sha256=validated_sha256,
        fact_count=len(facts),
        evidence=evidence,
        evidence_sha256=evidence_sha256,
        artifact_bytes=artifact_bytes,
    )
    view = load_validated_contract_artifact(artifact_bytes)
    root = binding.declared_closure.source_closure.root
    root_module = next(
        module
        for module in binding.declared_closure.modules
        if module.module_id == root.resolved_locator
    )
    profile = _load_profile(None)
    return ValidatedContractCompilation(
        elaborated=elaborated,
        contract=contract,
        facts=facts,
        canonical_facts=canonical_facts,
        facts_sha256=facts_sha256.removeprefix("sha256:"),
        content_hash=validated_sha256.removeprefix("sha256:"),
        artifact=artifact,
        view=view,
        source=SourceAttestation(
            locator=root.requested_locator,
            byte_length=root_module.source.byte_length,
            sha256=root_module.source.sha256.removeprefix("sha256:"),
        ),
        implementation=CompilerImplementation(
            adapter=str(profile.data["adapter"]),
            linkml_version=str(profile.data["linkml_version"]),
            linkml_runtime_version=str(profile.data["linkml_runtime_version"]),
            support_profile=str(profile.data["support_profile"]),
            profile_sha256=profile.digest,
            executor_sha256=sha256(
                Path(__file__).parents[1].joinpath("_contract_compiler.py").read_bytes()
            ).hexdigest(),
            adapter_executor_sha256=sha256(
                Path(__file__).parents[1]
                .joinpath("_contract_linkml_adapter.py")
                .read_bytes()
            ).hexdigest(),
        ),
    )

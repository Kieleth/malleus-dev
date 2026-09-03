"""Project validated contract IR into the paper's GraphRecipe contract.

This adapter reads only the compiler's frontend-neutral elaboration and its
fact-backed ``ContractView``.  The caller supplies the exact domain record
types in scope; imported protocol roots are used only to classify those types.
"""

from __future__ import annotations

from decimal import Decimal
from hashlib import sha256
import json
import math
from typing import Any

from malleus._contract_pipeline import (
    ContractView,
    ElaboratedContract,
    ValidatedContractCompilation,
)

from ..graph_recipe.assembly import AssemblyPlan
from ..graph_recipe.model import (
    GraphRecipeDiagnostic,
    GraphRecipeFailure,
    LogicalGraphContract,
    LogicalRecordType,
    LogicalSlot,
    LogicalSlotConstraints,
    OntologySymbolBindings,
    RelationEndpointConstraints,
    SymbolBinding,
)


XSD = "http://www.w3.org/2001/XMLSchema#"
FACTS = "https://malleus.dev/contract-facts/"
BASE = "https://malleus.dev/graph-recipe/base/"
FOUNDATION = "https://malleus.dev/schema/"

_SCHEMA_VERSION = "malleus.compiled-graph-recipe-contract/paper-v0"
_BINDING_DERIVATION = "compiled-frontend-neutral-ir"
_SEED_RANGES = {
    FACTS + "String": XSD + "string",
    FACTS + "Integer": XSD + "integer",
    FACTS + "Float": XSD + "float",
    FACTS + "Boolean": XSD + "boolean",
    FACTS + "DateTime": XSD + "dateTime",
}
_ROLES = {
    FOUNDATION + "Entity": ("ENTITY", BASE + "CreateEntity"),
    FOUNDATION + "Relation": ("RELATION", BASE + "CreateRelation"),
}
_EXCLUDED_ROLE_ROOTS = frozenset(
    {
        FOUNDATION + "Entity",
        FOUNDATION + "Relation",
        FOUNDATION + "Signal",
        FOUNDATION + "Event",
    }
)


def _failure(
    subject: str,
    message: str,
    *,
    code: str = "COMPILED_LOGICAL_CONTRACT_DERIVATION_FAILED",
    phase: str = "logical-contract",
    **evidence: Any,
) -> GraphRecipeFailure:
    return GraphRecipeFailure(
        GraphRecipeDiagnostic(
            code,
            phase,
            subject,
            {"message": message},
            evidence,
        )
    )


def _validated_view(compilation: ValidatedContractCompilation) -> ContractView:
    if type(compilation) is not ValidatedContractCompilation:
        raise TypeError("compilation must be one exact ValidatedContractCompilation")
    if type(compilation.elaborated) is not ElaboratedContract:
        raise _failure(
            "compilation.elaborated",
            "Compilation does not contain one exact frontend-neutral elaboration.",
        )
    if type(compilation.view) is not ContractView:
        raise _failure(
            "compilation.view",
            "Compilation does not contain one exact fact-backed ContractView.",
        )

    artifact_hash = compilation.artifact.validated_fact_set_sha256
    expected_content_hash = artifact_hash.removeprefix("sha256:")
    mismatches = []
    if compilation.content_hash != expected_content_hash:
        mismatches.append("compilation.content_hash")
    if compilation.view.content_hash() != expected_content_hash:
        mismatches.append("view.content_hash")
    if compilation.view.facts != compilation.facts:
        mismatches.append("view.facts")
    if compilation.view.artifact_bytes != compilation.artifact.artifact_bytes:
        mismatches.append("view.artifact_bytes")
    if mismatches:
        raise _failure(
            artifact_hash,
            "Compilation and fact-backed view identities disagree.",
            mismatches=mismatches,
        )
    return compilation.view


def _suffix(identifier: str, *, kind: str) -> str:
    suffix = identifier.rsplit("/", 1)[-1]
    if not suffix or suffix == identifier:
        raise _failure(
            identifier,
            f"Compiled {kind} IRI has no slash-qualified runtime symbol.",
            kind=kind,
        )
    return suffix


def _reject_suffix_collisions(identifiers: set[str], *, kind: str) -> None:
    by_suffix: dict[str, list[str]] = {}
    for identifier in sorted(identifiers):
        by_suffix.setdefault(_suffix(identifier, kind=kind), []).append(identifier)
    collisions = {
        suffix: values for suffix, values in by_suffix.items() if len(values) > 1
    }
    if collisions:
        raise _failure(
            kind,
            f"Compiled {kind} IRIs collide after runtime-symbol derivation.",
            collisions=collisions,
        )


def _selected_classes(
    view: ContractView,
    record_type_iris: tuple[str, ...],
) -> tuple[str, ...]:
    if not isinstance(record_type_iris, tuple):
        raise TypeError("record_type_iris must be an ordered tuple")
    if not record_type_iris:
        raise _failure(
            "record_type_iris",
            "The compiled paper contract requires at least one selected record type.",
        )
    if not all(isinstance(item, str) and item.strip() for item in record_type_iris):
        raise _failure(
            "record_type_iris",
            "Every selected record type must be a nonblank qualified IRI.",
        )
    if len(set(record_type_iris)) != len(record_type_iris):
        raise _failure(
            "record_type_iris",
            "The selected record type tuple contains duplicates.",
            record_type_iris=list(record_type_iris),
        )

    known = set(view.type_names())
    unknown = sorted(set(record_type_iris) - known)
    if unknown:
        raise _failure(
            "record_type_iris",
            "The selected record type tuple contains unknown compiled classes.",
            unknown_record_types=unknown,
        )
    roots = sorted(set(record_type_iris) & _EXCLUDED_ROLE_ROOTS)
    if roots:
        raise _failure(
            "record_type_iris",
            "Imported protocol role roots cannot be selected as domain records.",
            imported_role_roots=roots,
        )
    mixins = sorted(item for item in record_type_iris if view.get_type(item).is_mixin)
    if mixins:
        raise _failure(
            "record_type_iris",
            "Mixin classes cannot be selected as GraphRecipe records.",
            mixin_record_types=mixins,
        )
    _reject_suffix_collisions(set(record_type_iris), kind="record type")
    return tuple(sorted(record_type_iris))


def _role(view: ContractView, type_iri: str) -> tuple[str, str]:
    matches = [
        value
        for root, value in _ROLES.items()
        if view.has_type(root) and view.is_subtype_of(type_iri, root)
    ]
    if len(matches) != 1:
        raise _failure(
            type_iri,
            "Selected type must resolve to exactly one Entity or Relation role.",
            matching_roles=[item[0] for item in matches],
        )
    return matches[0]


def _scalar_terminals(compilation: ValidatedContractCompilation) -> dict[str, str]:
    scalars = {
        item.identifier: item.typeof_id for item in compilation.elaborated.scalars
    }
    if len(scalars) != len(compilation.elaborated.scalars):
        raise _failure(
            "compilation.elaborated.scalars",
            "Compiled scalar identifiers are not unique.",
        )
    terminals: dict[str, str] = {}
    for scalar in sorted(scalars):
        seen: set[str] = set()
        current = scalar
        while current in scalars:
            if current in seen:
                raise _failure(
                    scalar,
                    "Compiled scalar ancestry contains a cycle.",
                    cycle=sorted((*seen, current)),
                )
            seen.add(current)
            current = scalars[current]
        try:
            terminals[scalar] = _SEED_RANGES[current]
        except KeyError as error:
            raise _failure(
                scalar,
                "Compiled scalar does not terminate at a supported seed scalar.",
                terminal=current,
            ) from error
    return terminals


def _bound_number(value: str | None, *, subject: str) -> int | float | None:
    if value is None:
        return None
    number = Decimal(value)
    if not number.is_finite():
        raise _failure(subject, "Compiled numeric bound is not finite.", bound=value)
    if number == number.to_integral_value():
        return int(number)
    projected = float(number)
    if not math.isfinite(projected) or Decimal(str(projected)) != number:
        raise _failure(
            subject,
            "Compiled numeric bound cannot be represented exactly by GraphRecipe.",
            bound=value,
        )
    return projected


def _range_iri(
    range_id: str,
    *,
    subject: str,
    classes: set[str],
    selected: set[str],
    enums: set[str],
    scalar_terminals: dict[str, str],
    allow_entity_root: bool = False,
) -> str:
    if range_id in _SEED_RANGES:
        return _SEED_RANGES[range_id]
    if range_id in scalar_terminals:
        return scalar_terminals[range_id]
    if range_id in enums:
        return range_id
    if range_id in classes:
        if range_id not in selected and not (
            allow_entity_root and range_id == FOUNDATION + "Entity"
        ):
            raise _failure(
                subject,
                "Class-valued slot range is outside the frozen record selection.",
                range=range_id,
            )
        return range_id
    raise _failure(
        subject,
        "Compiled slot range is unresolved or unsupported by GraphRecipe.",
        range=range_id,
    )


def _project_slots(
    view: ContractView,
    type_iri: str,
    *,
    role: str,
    selected: set[str],
    classes: set[str],
    enums: set[str],
    scalar_terminals: dict[str, str],
) -> tuple[LogicalSlot, ...]:
    effective = view.effective_slots(type_iri)
    _reject_suffix_collisions(set(effective), kind=f"property on {type_iri}")
    projected = []
    for position, (slot_iri, constraint) in enumerate(sorted(effective.items())):
        subject = f"{type_iri} {slot_iri}"
        runtime_symbol = _suffix(slot_iri, kind="property")
        if constraint.value_presence is not None:
            raise _failure(
                subject,
                "GraphRecipe has no value_presence representation.",
                value_presence=constraint.value_presence,
            )
        projected.append(
            LogicalSlot(
                property_iri=slot_iri,
                runtime_symbol=_suffix(slot_iri, kind="property"),
                position=position,
                constraints=LogicalSlotConstraints(
                    required=constraint.required,
                    range=_range_iri(
                        constraint.range_id,
                        subject=subject,
                        classes=classes,
                        selected=selected,
                        enums=enums,
                        scalar_terminals=scalar_terminals,
                        allow_entity_root=(
                            role == "RELATION"
                            and runtime_symbol in {"source_id", "target_id"}
                        ),
                    ),
                    multivalued=constraint.multivalued,
                    inlined=constraint.inlined,
                    identifier=constraint.identifier,
                    equals_string=constraint.equals_string,
                    minimum_value=_bound_number(
                        constraint.minimum,
                        subject=subject,
                    ),
                    maximum_value=_bound_number(
                        constraint.maximum,
                        subject=subject,
                    ),
                ),
            )
        )
    return tuple(projected)


def _require_positional_slots(
    type_iri: str,
    role: str,
    slots: tuple[LogicalSlot, ...],
) -> None:
    by_symbol = {item.runtime_symbol: item for item in slots}
    required = {"id"} | ({"source_id", "target_id"} if role == "RELATION" else set())
    missing = sorted(required - set(by_symbol))
    optional = sorted(
        symbol
        for symbol in required & set(by_symbol)
        if not by_symbol[symbol].constraints.required
    )
    if missing or optional:
        raise _failure(
            type_iri,
            "Selected record lacks required positional GraphRecipe slots.",
            missing_positional_slots=missing,
            optional_positional_slots=optional,
        )


def _bindings(
    compilation: ValidatedContractCompilation,
    selected: tuple[str, ...],
    property_iris: set[str],
) -> OntologySymbolBindings:
    _reject_suffix_collisions(property_iris, kind="property")
    artifact_hash = compilation.artifact.validated_fact_set_sha256
    identity_payload = {
        "artifact": artifact_hash,
        "record_type_iris": list(selected),
        "property_iris": sorted(property_iris),
    }
    identity = sha256(
        json.dumps(
            identity_payload,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    return OntologySymbolBindings(
        schema_version=_SCHEMA_VERSION,
        binding_id=f"urn:malleus:compiled-graph-recipe-bindings:{identity}",
        ontology_artifact=artifact_hash,
        derivation=_BINDING_DERIVATION,
        types=tuple(
            SymbolBinding(type_iri, _suffix(type_iri, kind="record type"))
            for type_iri in selected
        ),
        properties=tuple(
            SymbolBinding(property_iri, _suffix(property_iri, kind="property"))
            for property_iri in sorted(property_iris)
        ),
    )


def derive_compiled_logical_contract(
    compilation: ValidatedContractCompilation,
    *,
    record_type_iris: tuple[str, ...],
    contract_id: str,
) -> LogicalGraphContract:
    """Derive the frozen paper slice from one validated compilation."""

    view = _validated_view(compilation)
    selected = _selected_classes(view, record_type_iris)
    selected_set = set(selected)
    classes = {item.identifier for item in compilation.elaborated.classes}
    enums = {item.identifier for item in compilation.elaborated.enums}
    if len(classes) != len(compilation.elaborated.classes):
        raise _failure(
            "compilation.elaborated.classes",
            "Compiled class identifiers are not unique.",
        )
    if len(enums) != len(compilation.elaborated.enums):
        raise _failure(
            "compilation.elaborated.enums",
            "Compiled enum identifiers are not unique.",
        )
    expressions = {item.class_id for item in compilation.elaborated.expression_groups}
    unsupported_expressions = sorted(selected_set & expressions)
    if unsupported_expressions:
        raise _failure(
            "record_type_iris",
            "Selected records use conditional expressions unavailable in GraphRecipe.",
            expression_record_types=unsupported_expressions,
        )
    scalar_terminals = _scalar_terminals(compilation)

    records = []
    property_iris: set[str] = set()
    for type_iri in selected:
        role, operation = _role(view, type_iri)
        slots = _project_slots(
            view,
            type_iri,
            role=role,
            selected=selected_set,
            classes=classes,
            enums=enums,
            scalar_terminals=scalar_terminals,
        )
        _require_positional_slots(type_iri, role, slots)
        property_iris.update(item.property_iri for item in slots)
        by_symbol = {item.runtime_symbol: item for item in slots}
        endpoints = None
        if role == "RELATION":
            source = by_symbol["source_id"].constraints.range
            target = by_symbol["target_id"].constraints.range
            if source not in classes or target not in classes:
                raise _failure(
                    type_iri,
                    "Relation endpoint ranges must be compiled class IRIs.",
                    source_range=source,
                    target_range=target,
                )
            endpoints = RelationEndpointConstraints(source=source, target=target)
        abstract = view.get_type(type_iri).abstract
        records.append(
            LogicalRecordType(
                type_iri=type_iri,
                runtime_symbol=_suffix(type_iri, kind="record type"),
                role=role,
                abstract=abstract,
                required_properties=tuple(
                    item for item in slots if item.constraints.required
                ),
                optional_properties=tuple(
                    item for item in slots if not item.constraints.required
                ),
                endpoint_constraints=endpoints,
                legal_operation_kind=None if abstract else operation,
            )
        )

    bindings = _bindings(compilation, selected, property_iris)
    artifact_hash = compilation.artifact.validated_fact_set_sha256
    try:
        return LogicalGraphContract(
            schema_version=_SCHEMA_VERSION,
            status="complete",
            contract_id=contract_id,
            record_types=tuple(records),
            constructible_record_types=tuple(
                item.type_iri for item in records if not item.abstract
            ),
            registry_hash=artifact_hash,
            symbol_bindings=bindings,
        )
    except GraphRecipeFailure:
        raise
    except (TypeError, ValueError) as error:
        raise _failure(contract_id, str(error)) from error


def require_plan_contract_alignment(
    plan: AssemblyPlan,
    logical_contract: LogicalGraphContract,
    compilation: ValidatedContractCompilation,
) -> AssemblyPlan:
    """Refuse plan, logical-contract, or runtime-symbol identity drift."""

    if type(plan) is not AssemblyPlan:
        raise TypeError("plan must be one exact AssemblyPlan")
    if type(logical_contract) is not LogicalGraphContract:
        raise TypeError("logical_contract must be one exact LogicalGraphContract")
    _validated_view(compilation)
    compiled_hash = compilation.artifact.validated_fact_set_sha256
    if logical_contract.registry_hash != compiled_hash:
        raise _failure(
            logical_contract.contract_id,
            "Logical contract is not bound to the supplied validated compilation.",
            code="COMPILED_LOGICAL_CONTRACT_DRIFT",
            phase="plan-contract",
            logical_registry_hash=logical_contract.registry_hash,
            compiled_contract_hash=compiled_hash,
        )
    if plan.contract_digest != logical_contract.contract_digest:
        raise _failure(
            logical_contract.contract_id,
            "AssemblyPlan contract digest does not match the logical contract.",
            code="COMPILED_LOGICAL_CONTRACT_DRIFT",
            phase="plan-contract",
            plan_contract_digest=plan.contract_digest,
            logical_contract_digest=logical_contract.contract_digest,
        )

    members = {item.member: item for item in plan.members}
    if len(members) != len(plan.members) or set(members) != set(plan.operation_members):
        raise _failure(
            logical_contract.contract_id,
            "AssemblyPlan members and paired operations do not align.",
            code="COMPILED_LOGICAL_CONTRACT_DRIFT",
            phase="plan-contract",
            members=sorted(members),
            operation_members=list(plan.operation_members),
        )
    for member_iri, operation in zip(
        plan.operation_members,
        plan.operations,
        strict=True,
    ):
        member = members[member_iri]
        try:
            runtime_symbol = logical_contract.record_for_iri(
                member.record_type
            ).runtime_symbol
        except GraphRecipeFailure as error:
            raise _failure(
                member_iri,
                "AssemblyPlan member record type is absent from the logical contract.",
                code="COMPILED_LOGICAL_CONTRACT_DRIFT",
                phase="plan-contract",
                member_record_type=member.record_type,
            ) from error
        if operation.record_type != runtime_symbol:
            raise _failure(
                member_iri,
                "Paired operation record type does not match the compiled runtime symbol.",
                code="COMPILED_LOGICAL_CONTRACT_DRIFT",
                phase="plan-contract",
                member_record_type=member.record_type,
                logical_runtime_symbol=runtime_symbol,
                operation_record_type=operation.record_type,
            )
    return plan


compile_logical_contract = derive_compiled_logical_contract

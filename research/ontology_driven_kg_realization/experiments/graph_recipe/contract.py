"""Project an ``OntologyRegistry`` into the frozen logical graph contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from malleus.ontology import OntologyRegistry

from .model import (
    GraphRecipeDiagnostic,
    GraphRecipeFailure,
    LogicalGraphContract,
    LogicalRecordType,
    LogicalSlot,
    LogicalSlotConstraints,
    OntologySymbolBindings,
    RelationEndpointConstraints,
)


XSD = "http://www.w3.org/2001/XMLSchema#"
BASE = "https://malleus.dev/graph-recipe/base/"

_BUILTIN_RANGE_IRIS = {
    "string": XSD + "string",
    "integer": XSD + "integer",
    "float": XSD + "float",
    "boolean": XSD + "boolean",
    "datetime": XSD + "dateTime",
    "double": XSD + "double",
    "decimal": XSD + "decimal",
    "date": XSD + "date",
    "time": XSD + "time",
    "date_or_datetime": XSD + "dateTime",
    "uri": XSD + "anyURI",
    "uriorcurie": XSD + "string",
    "curie": XSD + "string",
    "ncname": XSD + "NCName",
    "objectidentifier": XSD + "string",
    "nodeidentifier": XSD + "string",
    "jsonpointer": XSD + "string",
    "jsonpath": XSD + "string",
    "sparqlpath": XSD + "string",
}

_ROLE_ROOTS = (
    ("Entity", "ENTITY", BASE + "CreateEntity"),
    ("Relation", "RELATION", BASE + "CreateRelation"),
    ("Signal", "SIGNAL", BASE + "CreateSignal"),
    ("Event", "EVENT", BASE + "CreateEvent"),
)


def _failure(subject: str, message: str, **evidence: Any) -> GraphRecipeFailure:
    return GraphRecipeFailure(
        GraphRecipeDiagnostic(
            "LOGICAL_CONTRACT_DERIVATION_FAILED",
            "logical-contract",
            subject,
            {"message": message},
            evidence,
        )
    )


def load_ontology_symbol_bindings(path: str | Path) -> OntologySymbolBindings:
    return OntologySymbolBindings.load(path)


def _validate_binding_coverage(
    registry: OntologyRegistry,
    bindings: OntologySymbolBindings,
) -> None:
    if bindings.derivation != "explicit-validated-input":
        raise _failure(
            bindings.binding_id,
            "Ontology symbol bindings must declare derivation 'explicit-validated-input'.",
            derivation=bindings.derivation,
        )

    registry_types = set(registry.type_names())
    bound_types = {item.local_symbol for item in bindings.types}
    effective_properties = {
        slot_name
        for type_name in registry.type_names()
        for slot_name in registry.effective_slots(type_name)
    }
    bound_properties = {item.local_symbol for item in bindings.properties}
    missing_types = sorted(registry_types - bound_types)
    unknown_types = sorted(bound_types - registry_types)
    missing_properties = sorted(effective_properties - bound_properties)
    unknown_properties = sorted(bound_properties - effective_properties)
    if missing_types or unknown_types or missing_properties or unknown_properties:
        raise _failure(
            bindings.binding_id,
            "Ontology symbol bindings do not bijectively cover the effective ontology symbols.",
            missing_types=missing_types,
            unknown_types=unknown_types,
            missing_properties=missing_properties,
            unknown_properties=unknown_properties,
        )


def _role(
    registry: OntologyRegistry,
    type_name: str,
) -> tuple[str, str]:
    matches = [
        (role, operation)
        for root, role, operation in _ROLE_ROOTS
        if registry.has_type(root) and registry.is_subtype_of(type_name, root)
    ]
    if len(matches) != 1:
        raise _failure(
            type_name,
            f"Ontology type '{type_name}' must resolve to exactly one graph record role.",
            matching_roles=[item[0] for item in matches],
        )
    return matches[0]


def _range_iri(
    registry: OntologyRegistry,
    bindings: OntologySymbolBindings,
    type_name: str,
    slot_name: str,
    range_name: str | None,
) -> str:
    if range_name is None:
        raise _failure(
            f"{type_name}.{slot_name}",
            f"Effective slot '{type_name}.{slot_name}' has no declared range.",
            record_type=type_name,
            property=slot_name,
        )
    if range_name in _BUILTIN_RANGE_IRIS:
        return _BUILTIN_RANGE_IRIS[range_name]
    if registry.has_type(range_name):
        return bindings.type_iri(range_name)
    if registry.has_enum(range_name):
        raise _failure(
            f"{type_name}.{slot_name}",
            f"Enum range '{range_name}' has no explicit IRI binding in this experiment profile.",
            record_type=type_name,
            property=slot_name,
            range=range_name,
        )
    raise _failure(
        f"{type_name}.{slot_name}",
        f"Scalar range '{range_name}' cannot be projected through the public registry API.",
        record_type=type_name,
        property=slot_name,
        range=range_name,
    )


def _project_slots(
    registry: OntologyRegistry,
    bindings: OntologySymbolBindings,
    type_name: str,
) -> tuple[LogicalSlot, ...]:
    projected = []
    effective = registry.effective_slots(type_name)
    ordered = sorted(effective.items(), key=lambda item: bindings.property_iri(item[0]))
    for position, (slot_name, constraint) in enumerate(ordered):
        projected.append(
            LogicalSlot(
                property_iri=bindings.property_iri(slot_name),
                runtime_symbol=slot_name,
                position=position,
                constraints=LogicalSlotConstraints(
                    required=bool(constraint.required),
                    range=_range_iri(registry, bindings, type_name, slot_name, constraint.range),
                    multivalued=bool(constraint.multivalued),
                    inlined=bool(constraint.inlined),
                    identifier=bool(constraint.identifier),
                    equals_string=constraint.equals_string,
                    minimum_value=constraint.minimum_value,
                    maximum_value=constraint.maximum_value,
                ),
            )
        )
    return tuple(projected)


def _require_positional_slots(
    type_name: str,
    role: str,
    slots: tuple[LogicalSlot, ...],
) -> None:
    by_symbol = {item.runtime_symbol: item for item in slots}
    required = {"id"} | ({"source_id", "target_id"} if role == "RELATION" else set())
    missing = sorted(required - set(by_symbol))
    nonrequired = sorted(name for name in required & set(by_symbol) if not by_symbol[name].constraints.required)
    if missing or nonrequired:
        raise _failure(
            type_name,
            f"Record type '{type_name}' lacks required positional contract slots.",
            missing_positional_slots=missing,
            optional_positional_slots=nonrequired,
        )


def _project_record(
    registry: OntologyRegistry,
    bindings: OntologySymbolBindings,
    type_name: str,
) -> LogicalRecordType:
    definition = registry.get_type(type_name)
    role, operation = _role(registry, type_name)
    slots = _project_slots(registry, bindings, type_name)
    _require_positional_slots(type_name, role, slots)
    by_symbol = {item.runtime_symbol: item for item in slots}
    endpoints = None
    if role == "RELATION":
        endpoints = RelationEndpointConstraints(
            source=by_symbol["source_id"].constraints.range,
            target=by_symbol["target_id"].constraints.range,
        )
    return LogicalRecordType(
        type_iri=bindings.type_iri(type_name),
        runtime_symbol=type_name,
        role=role,
        abstract=definition.abstract,
        required_properties=tuple(item for item in slots if item.constraints.required),
        optional_properties=tuple(item for item in slots if not item.constraints.required),
        endpoint_constraints=endpoints,
        legal_operation_kind=None if definition.abstract else operation,
    )


def derive_logical_contract(
    registry: OntologyRegistry,
    bindings: OntologySymbolBindings,
    contract_id: str,
) -> LogicalGraphContract:
    """Derive the complete target-neutral contract for the accepted slice.

    ``contract_id`` is caller-supplied protocol identity.  It is never guessed
    from a filename or ontology IRI.
    """

    if not isinstance(registry, OntologyRegistry):
        raise TypeError("registry must be an OntologyRegistry")
    if not isinstance(bindings, OntologySymbolBindings):
        raise TypeError("bindings must be OntologySymbolBindings")
    _validate_binding_coverage(registry, bindings)

    records = []
    for binding in bindings.types:
        definition = registry.get_type(binding.local_symbol)
        if definition.is_mixin:
            continue
        records.append(_project_record(registry, bindings, binding.local_symbol))

    if not records:
        raise _failure(contract_id, "The ontology projects no graph record types.")
    registry_hash = f"sha256:{registry.content_hash()}"
    try:
        return LogicalGraphContract(
            schema_version=bindings.schema_version,
            status="complete",
            contract_id=contract_id,
            record_types=tuple(records),
            constructible_record_types=tuple(item.type_iri for item in records if not item.abstract),
            registry_hash=registry_hash,
            symbol_bindings=bindings,
        )
    except GraphRecipeFailure:
        raise
    except (TypeError, ValueError) as error:
        raise _failure(contract_id, str(error)) from error


compile_logical_contract = derive_logical_contract


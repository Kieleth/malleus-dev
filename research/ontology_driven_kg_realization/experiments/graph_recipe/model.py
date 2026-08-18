"""Immutable values shared by the research-local GraphRecipe experiment.

The models deliberately mirror the frozen JSON artifacts.  Mutable mappings
enter only through strict loaders and leave only through defensive
``as_dict`` projections.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping, Sequence, TypeAlias
from urllib.parse import urlsplit


JsonValue: TypeAlias = type(None) | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]


def _require_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonblank string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ValueError(f"{name} must be valid UTF-8") from error
    return value


def _require_iri(value: Any, name: str) -> str:
    iri = _require_text(value, name)
    parsed = urlsplit(iri)
    if not parsed.scheme or any(character.isspace() for character in iri):
        raise ValueError(f"{name} must be an absolute IRI")
    return iri


def _validate_json(value: Any, path: str = "value") -> None:
    if value is None or isinstance(value, (str, bool)):
        if isinstance(value, str):
            try:
                value.encode("utf-8")
            except UnicodeEncodeError as error:
                raise ValueError(f"{path} must be valid UTF-8") from error
        return
    if isinstance(value, int) and not isinstance(value, bool):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{path} must be a finite JSON number")
        return
    if isinstance(value, Mapping):
        for key, member in value.items():
            if not isinstance(key, str):
                raise ValueError(f"{path} object keys must be strings")
            _validate_json(member, f"{path}.{key}")
        return
    if isinstance(value, (list, tuple)):
        for index, member in enumerate(value):
            _validate_json(member, f"{path}[{index}]")
        return
    raise ValueError(f"{path} is not a JSON value")


def _canonical_json(value: Any) -> str:
    _validate_json(value)
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _json_copy(value: Any) -> Any:
    return json.loads(_canonical_json(value))


@dataclass(frozen=True, init=False)
class GraphRecipeDiagnostic:
    """One stable refusal with JSON evidence."""

    code: str
    phase: str
    subject: str
    _details_json: str = field(repr=False)
    _evidence_json: str = field(repr=False)

    def __init__(
        self,
        code: str,
        phase: str,
        subject: str,
        details: Mapping[str, Any],
        evidence: Mapping[str, Any],
    ) -> None:
        object.__setattr__(self, "code", _require_text(code, "diagnostic code"))
        object.__setattr__(self, "phase", _require_text(phase, "diagnostic phase"))
        object.__setattr__(self, "subject", _require_text(subject, "diagnostic subject"))
        if not isinstance(details, Mapping):
            raise ValueError("diagnostic details must be a mapping")
        if not isinstance(evidence, Mapping):
            raise ValueError("diagnostic evidence must be a mapping")
        object.__setattr__(self, "_details_json", _canonical_json(dict(details)))
        object.__setattr__(self, "_evidence_json", _canonical_json(dict(evidence)))

    @property
    def details(self) -> dict[str, Any]:
        return json.loads(self._details_json)

    @property
    def evidence(self) -> dict[str, Any]:
        return json.loads(self._evidence_json)

    @property
    def message(self) -> str:
        message = self.details.get("message")
        return message if isinstance(message, str) else self.code

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "phase": self.phase,
            "subject": self.subject,
            "details": self.details,
            "evidence": self.evidence,
        }

    @classmethod
    def from_dict(
        cls,
        value: Mapping[str, Any],
        *,
        subject: str = "GraphRecipeDiagnostic",
    ) -> "GraphRecipeDiagnostic":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("code", "phase", "subject", "details", "evidence"), subject)
        return cls(
            data["code"],
            data["phase"],
            data["subject"],
            data["details"],
            data["evidence"],
        )


class GraphRecipeFailure(ValueError):
    """A deterministic, evidence-preserving GraphRecipe refusal."""

    def __init__(
        self,
        diagnostics: GraphRecipeDiagnostic | Sequence[GraphRecipeDiagnostic],
    ) -> None:
        if isinstance(diagnostics, GraphRecipeDiagnostic):
            values = (diagnostics,)
        elif isinstance(diagnostics, Sequence) and not isinstance(diagnostics, (str, bytes)):
            values = tuple(diagnostics)
        else:
            raise TypeError("diagnostics must be a diagnostic or a sequence of diagnostics")
        if not values or not all(isinstance(item, GraphRecipeDiagnostic) for item in values):
            raise TypeError("diagnostics must contain at least one GraphRecipeDiagnostic")
        self.diagnostics = tuple(sorted(values, key=lambda item: _canonical_json(item.as_dict())))
        super().__init__("; ".join(item.message for item in self.diagnostics))

    def as_dict(self) -> dict[str, Any]:
        return {"diagnostics": [item.as_dict() for item in self.diagnostics]}


def _model_failure(subject: str, message: str, **evidence: Any) -> GraphRecipeFailure:
    return GraphRecipeFailure(
        GraphRecipeDiagnostic(
            "GRAPH_RECIPE_MODEL_INVALID",
            "artifact-loading",
            subject,
            {"message": message},
            evidence,
        )
    )


def _require_object(value: Any, subject: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise _model_failure(subject, f"{subject} must be a JSON object.", actual_type=type(value).__name__)
    if not all(isinstance(key, str) for key in value):
        raise _model_failure(subject, f"{subject} object keys must be strings.")
    return value


def _require_exact_fields(
    value: Mapping[str, Any],
    required: Sequence[str],
    subject: str,
) -> None:
    required_set = set(required)
    missing = sorted(required_set - set(value))
    unknown = sorted(set(value) - required_set)
    if missing or unknown:
        parts = []
        if missing:
            parts.append(f"missing required fields: {', '.join(missing)}")
        if unknown:
            parts.append(f"unknown fields: {', '.join(unknown)}")
        raise _model_failure(
            subject,
            f"{subject} has {'; '.join(parts)}.",
            missing_fields=missing,
            unknown_fields=unknown,
        )


def _require_array(value: Any, subject: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise _model_failure(subject, f"{subject} must be a JSON array.", actual_type=type(value).__name__)
    return value


def _duplicate_rejecting_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json_object(path: str | Path) -> Mapping[str, Any]:
    """Load one strict UTF-8 JSON object without accepting duplicate keys."""

    artifact = Path(path)
    subject = str(artifact)
    try:
        text = artifact.read_text(encoding="utf-8")
        value = json.loads(text, object_pairs_hook=_duplicate_rejecting_object)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise _model_failure(subject, f"Cannot load GraphRecipe JSON artifact: {error}.") from error
    return _require_object(value, subject)


@dataclass(frozen=True)
class SymbolBinding:
    iri: str
    local_symbol: str

    def __post_init__(self) -> None:
        _require_iri(self.iri, "binding IRI")
        _require_text(self.local_symbol, "binding local_symbol")

    def as_dict(self) -> dict[str, str]:
        return {"iri": self.iri, "local_symbol": self.local_symbol}

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "SymbolBinding":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("iri", "local_symbol"), subject)
        try:
            return cls(data["iri"], data["local_symbol"])
        except ValueError as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class OntologySymbolBindings:
    schema_version: str
    binding_id: str
    ontology_artifact: str
    derivation: str
    types: tuple[SymbolBinding, ...]
    properties: tuple[SymbolBinding, ...]

    def __post_init__(self) -> None:
        _require_text(self.schema_version, "bindings schema_version")
        _require_iri(self.binding_id, "binding_id")
        _require_text(self.ontology_artifact, "ontology_artifact")
        _require_text(self.derivation, "binding derivation")
        if not self.types:
            raise ValueError("type bindings cannot be empty")
        if not all(isinstance(item, SymbolBinding) for item in (*self.types, *self.properties)):
            raise TypeError("types and properties must contain SymbolBinding values")
        object.__setattr__(self, "types", tuple(sorted(self.types, key=lambda item: item.iri)))
        object.__setattr__(self, "properties", tuple(sorted(self.properties, key=lambda item: item.iri)))
        self._validate_bijection("type", self.types)
        self._validate_bijection("property", self.properties)

    @staticmethod
    def _validate_bijection(kind: str, bindings: tuple[SymbolBinding, ...]) -> None:
        iris = [item.iri for item in bindings]
        symbols = [item.local_symbol for item in bindings]
        duplicate_iris = sorted({item for item in iris if iris.count(item) > 1})
        duplicate_symbols = sorted({item for item in symbols if symbols.count(item) > 1})
        if duplicate_iris or duplicate_symbols:
            raise ValueError(
                f"{kind} bindings are not bijective; duplicate IRIs={duplicate_iris}, "
                f"duplicate local symbols={duplicate_symbols}"
            )

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "binding_id": self.binding_id,
            "ontology_artifact": self.ontology_artifact,
            "derivation": self.derivation,
            "types": [item.as_dict() for item in self.types],
            "properties": [item.as_dict() for item in self.properties],
        }

    @classmethod
    def from_dict(
        cls,
        value: Mapping[str, Any],
        *,
        subject: str = "OntologySymbolBindings",
    ) -> "OntologySymbolBindings":
        data = _require_object(value, subject)
        _require_exact_fields(
            data,
            ("schema_version", "binding_id", "ontology_artifact", "derivation", "types", "properties"),
            subject,
        )
        type_values = _require_array(data["types"], f"{subject}.types")
        property_values = _require_array(data["properties"], f"{subject}.properties")
        try:
            return cls(
                data["schema_version"],
                data["binding_id"],
                data["ontology_artifact"],
                data["derivation"],
                tuple(
                    SymbolBinding.from_dict(item, subject=f"{subject}.types[{index}]")
                    for index, item in enumerate(type_values)
                ),
                tuple(
                    SymbolBinding.from_dict(item, subject=f"{subject}.properties[{index}]")
                    for index, item in enumerate(property_values)
                ),
            )
        except GraphRecipeFailure:
            raise
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error

    @classmethod
    def load(cls, path: str | Path) -> "OntologySymbolBindings":
        return cls.from_dict(load_json_object(path), subject=str(Path(path)))

    def _lookup(self, values: tuple[SymbolBinding, ...], attribute: str, needle: str, kind: str) -> str:
        for binding in values:
            if getattr(binding, attribute) == needle:
                return binding.local_symbol if attribute == "iri" else binding.iri
        raise GraphRecipeFailure(
            GraphRecipeDiagnostic(
                "ONTOLOGY_SYMBOL_UNBOUND",
                "logical-contract",
                needle,
                {"message": f"No explicit {kind} binding exists for '{needle}'."},
                {"kind": kind, "symbol": needle, "binding_id": self.binding_id},
            )
        )

    def type_symbol(self, iri: str) -> str:
        return self._lookup(self.types, "iri", iri, "type")

    def type_iri(self, local_symbol: str) -> str:
        return self._lookup(self.types, "local_symbol", local_symbol, "type")

    def property_symbol(self, iri: str) -> str:
        return self._lookup(self.properties, "iri", iri, "property")

    def property_iri(self, local_symbol: str) -> str:
        return self._lookup(self.properties, "local_symbol", local_symbol, "property")


@dataclass(frozen=True)
class LogicalSlotConstraints:
    required: bool
    range: str
    multivalued: bool
    inlined: bool
    identifier: bool
    equals_string: str | None
    minimum_value: int | float | None
    maximum_value: int | float | None

    def __post_init__(self) -> None:
        for name in ("required", "multivalued", "inlined", "identifier"):
            if not isinstance(getattr(self, name), bool):
                raise TypeError(f"slot constraint {name} must be bool")
        _require_iri(self.range, "slot constraint range")
        if self.equals_string is not None and not isinstance(self.equals_string, str):
            raise TypeError("slot constraint equals_string must be string or None")
        for name in ("minimum_value", "maximum_value"):
            value = getattr(self, name)
            if value is not None and (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not math.isfinite(float(value))
            ):
                raise TypeError(f"slot constraint {name} must be a finite number or None")
        if (
            self.minimum_value is not None
            and self.maximum_value is not None
            and self.minimum_value > self.maximum_value
        ):
            raise ValueError("slot constraint minimum_value exceeds maximum_value")

    def as_dict(self) -> dict[str, Any]:
        return {
            "required": self.required,
            "range": self.range,
            "multivalued": self.multivalued,
            "inlined": self.inlined,
            "identifier": self.identifier,
            "equals_string": self.equals_string,
            "minimum_value": self.minimum_value,
            "maximum_value": self.maximum_value,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "LogicalSlotConstraints":
        data = _require_object(value, subject)
        fields = (
            "required",
            "range",
            "multivalued",
            "inlined",
            "identifier",
            "equals_string",
            "minimum_value",
            "maximum_value",
        )
        _require_exact_fields(data, fields, subject)
        try:
            return cls(*(data[name] for name in fields))
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class LogicalSlot:
    property_iri: str
    runtime_symbol: str
    position: int
    constraints: LogicalSlotConstraints

    def __post_init__(self) -> None:
        _require_iri(self.property_iri, "property_iri")
        _require_text(self.runtime_symbol, "property runtime_symbol")
        if not isinstance(self.position, int) or isinstance(self.position, bool) or self.position < 0:
            raise ValueError("logical slot position must be a nonnegative integer")
        if not isinstance(self.constraints, LogicalSlotConstraints):
            raise TypeError("logical slot constraints must be LogicalSlotConstraints")

    @property
    def positional(self) -> bool:
        return self.runtime_symbol in {"id", "source_id", "target_id"}

    def as_dict(self) -> dict[str, Any]:
        return {
            "property_iri": self.property_iri,
            "runtime_symbol": self.runtime_symbol,
            "position": self.position,
            "constraints": self.constraints.as_dict(),
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "LogicalSlot":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("property_iri", "runtime_symbol", "position", "constraints"), subject)
        try:
            return cls(
                data["property_iri"],
                data["runtime_symbol"],
                data["position"],
                LogicalSlotConstraints.from_dict(data["constraints"], subject=f"{subject}.constraints"),
            )
        except GraphRecipeFailure:
            raise
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class RelationEndpointConstraints:
    source: str
    target: str

    def __post_init__(self) -> None:
        _require_iri(self.source, "relation source range")
        _require_iri(self.target, "relation target range")

    def as_dict(self) -> dict[str, str]:
        return {"source": self.source, "target": self.target}

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "RelationEndpointConstraints":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("source", "target"), subject)
        try:
            return cls(data["source"], data["target"])
        except ValueError as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class LogicalRecordType:
    type_iri: str
    runtime_symbol: str
    role: str
    abstract: bool
    required_properties: tuple[LogicalSlot, ...]
    optional_properties: tuple[LogicalSlot, ...]
    endpoint_constraints: RelationEndpointConstraints | None
    legal_operation_kind: str | None

    def __post_init__(self) -> None:
        _require_iri(self.type_iri, "type_iri")
        _require_text(self.runtime_symbol, "type runtime_symbol")
        if self.role not in {"ENTITY", "RELATION", "SIGNAL", "EVENT"}:
            raise ValueError(f"unknown logical record role: {self.role!r}")
        if not isinstance(self.abstract, bool):
            raise TypeError("logical record abstract must be bool")
        slots = (*self.required_properties, *self.optional_properties)
        if not all(isinstance(item, LogicalSlot) for item in slots):
            raise TypeError("logical record properties must be LogicalSlot values")
        if any(not item.constraints.required for item in self.required_properties):
            raise ValueError("required_properties contains an optional slot")
        if any(item.constraints.required for item in self.optional_properties):
            raise ValueError("optional_properties contains a required slot")
        positions = [item.position for item in slots]
        if sorted(positions) != list(range(len(slots))):
            raise ValueError("logical slot positions must be unique and contiguous from zero")
        if len({item.property_iri for item in slots}) != len(slots):
            raise ValueError("logical record repeats a property IRI")
        if len({item.runtime_symbol for item in slots}) != len(slots):
            raise ValueError("logical record repeats a property runtime symbol")
        if self.role == "RELATION":
            if not isinstance(self.endpoint_constraints, RelationEndpointConstraints):
                raise ValueError("relation records require endpoint_constraints")
        elif self.endpoint_constraints is not None:
            raise ValueError("only relation records may declare endpoint_constraints")
        if self.abstract:
            if self.legal_operation_kind is not None:
                raise ValueError("abstract records cannot declare a legal operation kind")
        else:
            _require_iri(self.legal_operation_kind, "legal_operation_kind")
        object.__setattr__(
            self,
            "required_properties",
            tuple(sorted(self.required_properties, key=lambda item: item.property_iri)),
        )
        object.__setattr__(
            self,
            "optional_properties",
            tuple(sorted(self.optional_properties, key=lambda item: item.property_iri)),
        )

    @property
    def slots(self) -> tuple[LogicalSlot, ...]:
        return tuple(sorted((*self.required_properties, *self.optional_properties), key=lambda item: item.position))

    @property
    def operation_properties(self) -> tuple[LogicalSlot, ...]:
        return tuple(item for item in self.slots if not item.positional)

    def slot_for_iri(self, property_iri: str) -> LogicalSlot:
        for slot in self.slots:
            if slot.property_iri == property_iri:
                return slot
        raise GraphRecipeFailure(
            GraphRecipeDiagnostic(
                "LOGICAL_PROPERTY_UNKNOWN",
                "assembly",
                property_iri,
                {"message": f"Property '{property_iri}' is not legal for '{self.type_iri}'."},
                {"record_type": self.type_iri, "property": property_iri},
            )
        )

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type_iri": self.type_iri,
            "runtime_symbol": self.runtime_symbol,
            "role": self.role,
            "abstract": self.abstract,
            "required_properties": [item.as_dict() for item in self.required_properties],
            "optional_properties": [item.as_dict() for item in self.optional_properties],
        }
        if self.endpoint_constraints is not None:
            result["endpoint_constraints"] = self.endpoint_constraints.as_dict()
        result["legal_operation_kind"] = self.legal_operation_kind
        return result

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "LogicalRecordType":
        data = _require_object(value, subject)
        common = {
            "type_iri",
            "runtime_symbol",
            "role",
            "abstract",
            "required_properties",
            "optional_properties",
            "legal_operation_kind",
        }
        allowed = common | ({"endpoint_constraints"} if data.get("role") == "RELATION" else set())
        _require_exact_fields(data, tuple(allowed), subject)
        required = _require_array(data["required_properties"], f"{subject}.required_properties")
        optional = _require_array(data["optional_properties"], f"{subject}.optional_properties")
        try:
            return cls(
                data["type_iri"],
                data["runtime_symbol"],
                data["role"],
                data["abstract"],
                tuple(
                    LogicalSlot.from_dict(item, subject=f"{subject}.required_properties[{index}]")
                    for index, item in enumerate(required)
                ),
                tuple(
                    LogicalSlot.from_dict(item, subject=f"{subject}.optional_properties[{index}]")
                    for index, item in enumerate(optional)
                ),
                RelationEndpointConstraints.from_dict(
                    data["endpoint_constraints"], subject=f"{subject}.endpoint_constraints"
                )
                if "endpoint_constraints" in data
                else None,
                data["legal_operation_kind"],
            )
        except GraphRecipeFailure:
            raise
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class LogicalGraphContract:
    schema_version: str
    status: str
    contract_id: str
    record_types: tuple[LogicalRecordType, ...]
    constructible_record_types: tuple[str, ...]
    registry_hash: str = field(repr=False)
    symbol_bindings: OntologySymbolBindings = field(repr=False)

    def __post_init__(self) -> None:
        _require_text(self.schema_version, "contract schema_version")
        if self.status != "complete":
            raise ValueError("logical contract status must be 'complete'")
        _require_iri(self.contract_id, "contract_id")
        if not all(isinstance(item, LogicalRecordType) for item in self.record_types):
            raise TypeError("record_types must contain LogicalRecordType values")
        if not self.registry_hash.startswith("sha256:") or len(self.registry_hash) != 71:
            raise ValueError("registry_hash must be a sha256 digest")
        if not isinstance(self.symbol_bindings, OntologySymbolBindings):
            raise TypeError("symbol_bindings must be OntologySymbolBindings")
        records = tuple(sorted(self.record_types, key=lambda item: item.type_iri))
        if len({item.type_iri for item in records}) != len(records):
            raise ValueError("logical contract repeats a record type IRI")
        constructible = tuple(sorted(self.constructible_record_types))
        expected = tuple(item.type_iri for item in records if not item.abstract)
        if constructible != expected:
            raise ValueError("constructible_record_types must name every and only concrete record type")
        object.__setattr__(self, "record_types", records)
        object.__setattr__(self, "constructible_record_types", constructible)

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "contract_id": self.contract_id,
            "record_types": [item.as_dict() for item in self.record_types],
            "constructible_record_types": list(self.constructible_record_types),
        }

    def identity_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "registry_hash": self.registry_hash,
            "symbol_bindings": self.symbol_bindings.as_dict(),
            "record_types": [item.as_dict() for item in self.record_types],
            "constructible_record_types": list(self.constructible_record_types),
        }

    @property
    def contract_digest(self) -> str:
        return "sha256:" + sha256(_canonical_json(self.identity_payload()).encode("utf-8")).hexdigest()

    def record_for_iri(self, type_iri: str) -> LogicalRecordType:
        for record in self.record_types:
            if record.type_iri == type_iri:
                return record
        raise GraphRecipeFailure(
            GraphRecipeDiagnostic(
                "LOGICAL_RECORD_TYPE_UNKNOWN",
                "assembly",
                type_iri,
                {"message": f"Record type '{type_iri}' is not in the logical contract."},
                {"record_type": type_iri, "contract_id": self.contract_id},
            )
        )

    def record_for_symbol(self, runtime_symbol: str) -> LogicalRecordType:
        for record in self.record_types:
            if record.runtime_symbol == runtime_symbol:
                return record
        raise GraphRecipeFailure(
            GraphRecipeDiagnostic(
                "LOGICAL_RECORD_TYPE_UNKNOWN",
                "assembly",
                runtime_symbol,
                {"message": f"Runtime record type '{runtime_symbol}' is not in the logical contract."},
                {"runtime_symbol": runtime_symbol, "contract_id": self.contract_id},
            )
        )

    @classmethod
    def from_dict(
        cls,
        value: Mapping[str, Any],
        *,
        registry_hash: str,
        symbol_bindings: OntologySymbolBindings,
        subject: str = "LogicalGraphContract",
    ) -> "LogicalGraphContract":
        data = _require_object(value, subject)
        _require_exact_fields(
            data,
            ("schema_version", "status", "contract_id", "record_types", "constructible_record_types"),
            subject,
        )
        records = _require_array(data["record_types"], f"{subject}.record_types")
        constructible = _require_array(
            data["constructible_record_types"], f"{subject}.constructible_record_types"
        )
        try:
            return cls(
                data["schema_version"],
                data["status"],
                data["contract_id"],
                tuple(
                    LogicalRecordType.from_dict(item, subject=f"{subject}.record_types[{index}]")
                    for index, item in enumerate(records)
                ),
                tuple(constructible),
                registry_hash,
                symbol_bindings,
            )
        except GraphRecipeFailure:
            raise
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class RdfTerm:
    """The closed RDF-term encoding admitted by GraphRecipe Profile v0."""

    kind: str
    value: str | None = None
    datatype: str | None = None
    lexical_form: str | None = None

    def __post_init__(self) -> None:
        if self.kind == "iri":
            _require_iri(self.value, "RDF IRI value")
            if self.datatype is not None or self.lexical_form is not None:
                raise ValueError("an RDF IRI term cannot carry literal fields")
        elif self.kind == "literal":
            _require_iri(self.datatype, "RDF literal datatype")
            if not isinstance(self.lexical_form, str):
                raise ValueError("an RDF literal requires lexical_form")
            try:
                self.lexical_form.encode("utf-8")
            except UnicodeEncodeError as error:
                raise ValueError("RDF literal lexical_form must be valid UTF-8") from error
            if self.value is not None:
                raise ValueError("an RDF literal cannot carry an IRI value")
        elif self.kind == "none":
            if self.value is not None or self.datatype is not None or self.lexical_form is not None:
                raise ValueError("an RDF none term cannot carry a value")
        else:
            raise ValueError(f"unsupported RDF term kind: {self.kind!r}")

    @classmethod
    def iri(cls, value: str) -> "RdfTerm":
        return cls("iri", value=value)

    @classmethod
    def literal(cls, datatype: str, lexical_form: str) -> "RdfTerm":
        return cls("literal", datatype=datatype, lexical_form=lexical_form)

    @classmethod
    def none(cls) -> "RdfTerm":
        return cls("none")

    def as_dict(self) -> dict[str, Any]:
        if self.kind == "iri":
            return {"kind": "iri", "value": self.value}
        if self.kind == "literal":
            return {
                "kind": "literal",
                "datatype": self.datatype,
                "lexical_form": self.lexical_form,
            }
        return {"kind": "none"}

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str = "RdfTerm") -> "RdfTerm":
        data = _require_object(value, subject)
        kind = data.get("kind")
        fields_by_kind = {
            "iri": ("kind", "value"),
            "literal": ("kind", "datatype", "lexical_form"),
            "none": ("kind",),
        }
        if kind not in fields_by_kind:
            raise _model_failure(subject, f"{subject} has unsupported kind {kind!r}.", kind=kind)
        _require_exact_fields(data, fields_by_kind[kind], subject)
        try:
            if kind == "iri":
                return cls.iri(data["value"])
            if kind == "literal":
                return cls.literal(data["datatype"], data["lexical_form"])
            return cls.none()
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


RDFTerm = RdfTerm


@dataclass(frozen=True)
class PrefixBinding:
    prefix: str
    iri: str

    def __post_init__(self) -> None:
        if not isinstance(self.prefix, str):
            raise TypeError("prefix must be a string")
        _require_iri(self.iri, "prefix IRI")

    def as_dict(self) -> dict[str, str]:
        return {"prefix": self.prefix, "iri": self.iri}


@dataclass(frozen=True)
class RecipeParameter:
    name: str
    type_iri: str | None
    mandatory: bool

    def __post_init__(self) -> None:
        _require_text(self.name, "recipe parameter name")
        if self.type_iri is not None:
            _require_iri(self.type_iri, "recipe parameter type_iri")
        if not isinstance(self.mandatory, bool):
            raise TypeError("recipe parameter mandatory must be bool")

    def as_dict(self) -> dict[str, Any]:
        return {"name": self.name, "type_iri": self.type_iri, "mandatory": self.mandatory}


@dataclass(frozen=True)
class RecipeArgument:
    """One template argument, either a variable or an RDF constant."""

    variable: str | None
    term: RdfTerm | None

    def __post_init__(self) -> None:
        if (self.variable is None) == (self.term is None):
            raise ValueError("recipe argument requires exactly one of variable or term")
        if self.variable is not None:
            _require_text(self.variable, "recipe argument variable")
        if self.term is not None and not isinstance(self.term, RdfTerm):
            raise TypeError("recipe argument term must be RdfTerm")

    @classmethod
    def variable_reference(cls, variable: str) -> "RecipeArgument":
        return cls(variable, None)

    @classmethod
    def constant(cls, term: RdfTerm) -> "RecipeArgument":
        return cls(None, term)

    def as_dict(self) -> dict[str, Any]:
        if self.variable is not None:
            return {"kind": "variable", "variable": self.variable}
        return {"kind": "term", "term": self.term.as_dict()}


@dataclass(frozen=True)
class RecipePattern:
    template_iri: str
    arguments: tuple[RecipeArgument, ...]
    source_pattern_index: int

    def __post_init__(self) -> None:
        _require_iri(self.template_iri, "pattern template_iri")
        if not all(isinstance(item, RecipeArgument) for item in self.arguments):
            raise TypeError("pattern arguments must be RecipeArgument values")
        if (
            not isinstance(self.source_pattern_index, int)
            or isinstance(self.source_pattern_index, bool)
            or self.source_pattern_index < 0
        ):
            raise ValueError("source_pattern_index must be a nonnegative integer")

    def as_dict(self) -> dict[str, Any]:
        return {
            "template_iri": self.template_iri,
            "arguments": [item.as_dict() for item in self.arguments],
            "source_pattern_index": self.source_pattern_index,
        }


@dataclass(frozen=True)
class RecipeTemplate:
    template_iri: str
    parameters: tuple[RecipeParameter, ...]
    patterns: tuple[RecipePattern, ...]
    base: bool

    def __post_init__(self) -> None:
        _require_iri(self.template_iri, "recipe template_iri")
        if not all(isinstance(item, RecipeParameter) for item in self.parameters):
            raise TypeError("template parameters must be RecipeParameter values")
        if not all(isinstance(item, RecipePattern) for item in self.patterns):
            raise TypeError("template patterns must be RecipePattern values")
        if not isinstance(self.base, bool):
            raise TypeError("template base must be bool")
        names = [item.name for item in self.parameters]
        if len(set(names)) != len(names):
            raise ValueError("template parameter names must be unique")
        if self.base and self.patterns:
            raise ValueError("BASE templates cannot carry patterns")

    def as_dict(self) -> dict[str, Any]:
        return {
            "template_iri": self.template_iri,
            "parameters": [item.as_dict() for item in self.parameters],
            "patterns": [item.as_dict() for item in self.patterns],
            "base": self.base,
        }


@dataclass(frozen=True)
class ParsedRecipe:
    """One parsed stOTTR document, including BASE and public templates."""

    source_digest: str
    prefixes: tuple[PrefixBinding, ...]
    templates: tuple[RecipeTemplate, ...]

    def __post_init__(self) -> None:
        if not self.source_digest.startswith("sha256:") or len(self.source_digest) != 71:
            raise ValueError("source_digest must be a sha256 digest")
        if not all(isinstance(item, PrefixBinding) for item in self.prefixes):
            raise TypeError("prefixes must contain PrefixBinding values")
        if not all(isinstance(item, RecipeTemplate) for item in self.templates):
            raise TypeError("templates must contain RecipeTemplate values")
        if len({item.prefix for item in self.prefixes}) != len(self.prefixes):
            raise ValueError("prefix declarations must be unique")
        if len({item.template_iri for item in self.templates}) != len(self.templates):
            raise ValueError("template declarations must be unique")
        object.__setattr__(self, "prefixes", tuple(sorted(self.prefixes, key=lambda item: item.prefix)))
        object.__setattr__(self, "templates", tuple(sorted(self.templates, key=lambda item: item.template_iri)))

    @property
    def base_templates(self) -> tuple[RecipeTemplate, ...]:
        return tuple(item for item in self.templates if item.base)

    @property
    def public_templates(self) -> tuple[RecipeTemplate, ...]:
        return tuple(item for item in self.templates if not item.base)

    def template(self, template_iri: str) -> RecipeTemplate:
        for item in self.templates:
            if item.template_iri == template_iri:
                return item
        raise GraphRecipeFailure(
            GraphRecipeDiagnostic(
                "RECIPE_TEMPLATE_UNDECLARED",
                "profile-validation",
                template_iri,
                {"message": f"Template '{template_iri}' is not declared."},
                {"template": template_iri, "source_digest": self.source_digest},
            )
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_digest": self.source_digest,
            "prefixes": [item.as_dict() for item in self.prefixes],
            "templates": [item.as_dict() for item in self.templates],
        }


ParsedRecipeDocument = ParsedRecipe
ParsedTemplate = RecipeTemplate


@dataclass(frozen=True)
class IdentityBinding:
    identity_key: str
    field: str

    def __post_init__(self) -> None:
        _require_text(self.identity_key, "identity_key")
        if self.field not in {"member_iri", "record_id"}:
            raise ValueError("identity binding field must be member_iri or record_id")

    def as_dict(self) -> dict[str, str]:
        return {"identity_key": self.identity_key, "field": self.field}

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "IdentityBinding":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("identity_key", "field"), subject)
        try:
            return cls(data["identity_key"], data["field"])
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class InvocationArgument:
    parameter: str
    identity_binding: IdentityBinding | None
    term: RdfTerm | None

    def __post_init__(self) -> None:
        _require_text(self.parameter, "invocation parameter")
        if (self.identity_binding is None) == (self.term is None):
            raise ValueError("invocation argument requires exactly one binding or term")
        if self.identity_binding is not None and not isinstance(self.identity_binding, IdentityBinding):
            raise TypeError("identity_binding must be IdentityBinding")
        if self.term is not None and not isinstance(self.term, RdfTerm):
            raise TypeError("term must be RdfTerm")

    def as_dict(self) -> dict[str, Any]:
        if self.identity_binding is not None:
            return {"parameter": self.parameter, "identity_binding": self.identity_binding.as_dict()}
        return {"parameter": self.parameter, "term": self.term.as_dict()}

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "InvocationArgument":
        data = _require_object(value, subject)
        present = tuple(name for name in ("identity_binding", "term") if name in data)
        if len(present) != 1:
            raise _model_failure(subject, f"{subject} requires exactly one identity_binding or term.")
        _require_exact_fields(data, ("parameter", present[0]), subject)
        try:
            return cls(
                data["parameter"],
                IdentityBinding.from_dict(data["identity_binding"], subject=f"{subject}.identity_binding")
                if present[0] == "identity_binding"
                else None,
                RdfTerm.from_dict(data["term"], subject=f"{subject}.term")
                if present[0] == "term"
                else None,
            )
        except GraphRecipeFailure:
            raise
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class RecipeInvocation:
    invocation_id: str
    template: str
    arguments: tuple[InvocationArgument, ...]

    def __post_init__(self) -> None:
        _require_iri(self.invocation_id, "invocation_id")
        _require_iri(self.template, "invocation template")
        if not all(isinstance(item, InvocationArgument) for item in self.arguments):
            raise TypeError("arguments must contain InvocationArgument values")
        names = [item.parameter for item in self.arguments]
        if len(set(names)) != len(names):
            raise ValueError("invocation arguments repeat a parameter")

    def as_dict(self) -> dict[str, Any]:
        return {
            "invocation_id": self.invocation_id,
            "template": self.template,
            "arguments": [item.as_dict() for item in self.arguments],
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "RecipeInvocation":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("invocation_id", "template", "arguments"), subject)
        arguments = _require_array(data["arguments"], f"{subject}.arguments")
        try:
            return cls(
                data["invocation_id"],
                data["template"],
                tuple(
                    InvocationArgument.from_dict(item, subject=f"{subject}.arguments[{index}]")
                    for index, item in enumerate(arguments)
                ),
            )
        except GraphRecipeFailure:
            raise
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class InvocationPlan:
    schema_version: str
    plan_id: str
    invocations: tuple[RecipeInvocation, ...]

    def __post_init__(self) -> None:
        _require_text(self.schema_version, "invocation schema_version")
        _require_iri(self.plan_id, "plan_id")
        if not self.invocations:
            raise ValueError("invocation plan cannot be empty")
        if not all(isinstance(item, RecipeInvocation) for item in self.invocations):
            raise TypeError("invocations must contain RecipeInvocation values")
        object.__setattr__(self, "invocations", tuple(sorted(self.invocations, key=lambda item: item.invocation_id)))
        if len({item.invocation_id for item in self.invocations}) != len(self.invocations):
            raise ValueError("invocation IDs must be unique")

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "plan_id": self.plan_id,
            "invocations": [item.as_dict() for item in self.invocations],
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str = "InvocationPlan") -> "InvocationPlan":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("schema_version", "plan_id", "invocations"), subject)
        invocations = _require_array(data["invocations"], f"{subject}.invocations")
        try:
            return cls(
                data["schema_version"],
                data["plan_id"],
                tuple(
                    RecipeInvocation.from_dict(item, subject=f"{subject}.invocations[{index}]")
                    for index, item in enumerate(invocations)
                ),
            )
        except GraphRecipeFailure:
            raise
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error

    @classmethod
    def load(cls, path: str | Path) -> "InvocationPlan":
        return cls.from_dict(load_json_object(path), subject=str(Path(path)))


@dataclass(frozen=True)
class ResolvedIdentity:
    identity_key: str
    member_iri: str
    record_id: str

    def __post_init__(self) -> None:
        _require_text(self.identity_key, "identity_key")
        _require_iri(self.member_iri, "member_iri")
        _require_text(self.record_id, "record_id")

    def as_dict(self) -> dict[str, str]:
        return {
            "identity_key": self.identity_key,
            "member_iri": self.member_iri,
            "record_id": self.record_id,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "ResolvedIdentity":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("identity_key", "member_iri", "record_id"), subject)
        try:
            return cls(data["identity_key"], data["member_iri"], data["record_id"])
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class IdentityPolicy:
    schema_version: str
    policy_id: str
    collision_policy: str
    identities: tuple[ResolvedIdentity, ...]

    def __post_init__(self) -> None:
        _require_text(self.schema_version, "identity policy schema_version")
        _require_iri(self.policy_id, "policy_id")
        if self.collision_policy != "reject":
            raise ValueError("this experiment slice requires collision_policy 'reject'")
        if not all(isinstance(item, ResolvedIdentity) for item in self.identities):
            raise TypeError("identities must contain ResolvedIdentity values")
        object.__setattr__(self, "identities", tuple(sorted(self.identities, key=lambda item: item.identity_key)))
        for attribute in ("identity_key", "member_iri", "record_id"):
            values = [getattr(item, attribute) for item in self.identities]
            if len(set(values)) != len(values):
                raise ValueError(f"identity policy repeats {attribute}")

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "policy_id": self.policy_id,
            "collision_policy": self.collision_policy,
            "identities": [item.as_dict() for item in self.identities],
        }

    def resolve(self, binding: IdentityBinding) -> str:
        for identity in self.identities:
            if identity.identity_key == binding.identity_key:
                return getattr(identity, binding.field)
        raise GraphRecipeFailure(
            GraphRecipeDiagnostic(
                "IDENTITY_BINDING_UNRESOLVED",
                "invocation-binding",
                binding.identity_key,
                {"message": f"Identity key '{binding.identity_key}' is not declared."},
                {"identity_key": binding.identity_key, "policy_id": self.policy_id},
            )
        )

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str = "IdentityPolicy") -> "IdentityPolicy":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("schema_version", "policy_id", "collision_policy", "identities"), subject)
        identities = _require_array(data["identities"], f"{subject}.identities")
        try:
            return cls(
                data["schema_version"],
                data["policy_id"],
                data["collision_policy"],
                tuple(
                    ResolvedIdentity.from_dict(item, subject=f"{subject}.identities[{index}]")
                    for index, item in enumerate(identities)
                ),
            )
        except GraphRecipeFailure:
            raise
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error

    @classmethod
    def load(cls, path: str | Path) -> "IdentityPolicy":
        return cls.from_dict(load_json_object(path), subject=str(Path(path)))


@dataclass(frozen=True)
class RecordFact:
    member: str
    operation_kind: str
    record_type: str
    record_id: str

    kind = "Record"

    def __post_init__(self) -> None:
        _require_iri(self.member, "Record member")
        _require_iri(self.operation_kind, "Record operation_kind")
        _require_iri(self.record_type, "Record record_type")
        _require_text(self.record_id, "Record record_id")

    def as_dict(self) -> dict[str, str]:
        return {
            "kind": self.kind,
            "member": self.member,
            "operation_kind": self.operation_kind,
            "record_type": self.record_type,
            "record_id": self.record_id,
        }


@dataclass(frozen=True)
class PropertyFact:
    member: str
    property: str
    value: RdfTerm

    kind = "Property"

    def __post_init__(self) -> None:
        _require_iri(self.member, "Property member")
        _require_iri(self.property, "Property property")
        if not isinstance(self.value, RdfTerm):
            raise TypeError("Property value must be RdfTerm")

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "member": self.member,
            "property": self.property,
            "value": self.value.as_dict(),
        }


@dataclass(frozen=True)
class RelationSourceFact:
    member: str
    record_id: str

    kind = "RelationSource"

    def __post_init__(self) -> None:
        _require_iri(self.member, "RelationSource member")
        _require_text(self.record_id, "RelationSource record_id")

    def as_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "member": self.member, "record_id": self.record_id}


@dataclass(frozen=True)
class RelationTargetFact:
    member: str
    record_id: str

    kind = "RelationTarget"

    def __post_init__(self) -> None:
        _require_iri(self.member, "RelationTarget member")
        _require_text(self.record_id, "RelationTarget record_id")

    def as_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "member": self.member, "record_id": self.record_id}


@dataclass(frozen=True)
class DependsOnFact:
    member: str
    prerequisite_member: str

    kind = "DependsOn"

    def __post_init__(self) -> None:
        _require_iri(self.member, "DependsOn member")
        _require_iri(self.prerequisite_member, "DependsOn prerequisite_member")

    def as_dict(self) -> dict[str, str]:
        return {
            "kind": self.kind,
            "member": self.member,
            "prerequisite_member": self.prerequisite_member,
        }


TerminalFact: TypeAlias = RecordFact | PropertyFact | RelationSourceFact | RelationTargetFact | DependsOnFact


def terminal_fact_from_dict(value: Mapping[str, Any], *, subject: str = "TerminalFact") -> TerminalFact:
    data = _require_object(value, subject)
    kind = data.get("kind")
    fields_by_kind = {
        "Record": ("kind", "member", "operation_kind", "record_type", "record_id"),
        "Property": ("kind", "member", "property", "value"),
        "RelationSource": ("kind", "member", "record_id"),
        "RelationTarget": ("kind", "member", "record_id"),
        "DependsOn": ("kind", "member", "prerequisite_member"),
    }
    if kind not in fields_by_kind:
        raise _model_failure(subject, f"{subject} has unsupported terminal fact kind {kind!r}.", kind=kind)
    _require_exact_fields(data, fields_by_kind[kind], subject)
    try:
        if kind == "Record":
            return RecordFact(
                data["member"], data["operation_kind"], data["record_type"], data["record_id"]
            )
        if kind == "Property":
            return PropertyFact(
                data["member"],
                data["property"],
                RdfTerm.from_dict(data["value"], subject=f"{subject}.value"),
            )
        if kind == "RelationSource":
            return RelationSourceFact(data["member"], data["record_id"])
        if kind == "RelationTarget":
            return RelationTargetFact(data["member"], data["record_id"])
        return DependsOnFact(data["member"], data["prerequisite_member"])
    except GraphRecipeFailure:
        raise
    except (TypeError, ValueError) as error:
        raise _model_failure(subject, str(error)) from error


_FACT_ORDER = {
    "Record": 0,
    "Property": 1,
    "RelationSource": 2,
    "RelationTarget": 3,
    "DependsOn": 4,
}


def terminal_fact_sort_key(fact: TerminalFact) -> tuple[str, int, str]:
    return fact.member, _FACT_ORDER[fact.kind], _canonical_json(fact.as_dict())


@dataclass(frozen=True)
class ExpansionEmission:
    emission_id: str
    fact: TerminalFact
    expansion_path_id: str

    def __post_init__(self) -> None:
        _require_text(self.emission_id, "emission_id")
        if not isinstance(
            self.fact,
            (RecordFact, PropertyFact, RelationSourceFact, RelationTargetFact, DependsOnFact),
        ):
            raise TypeError("emission fact is not a terminal fact")
        _require_text(self.expansion_path_id, "expansion_path_id")

    def as_dict(self) -> dict[str, Any]:
        return {
            "emission_id": self.emission_id,
            "fact": self.fact.as_dict(),
            "expansion_path_id": self.expansion_path_id,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "ExpansionEmission":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("emission_id", "fact", "expansion_path_id"), subject)
        try:
            return cls(
                data["emission_id"],
                terminal_fact_from_dict(data["fact"], subject=f"{subject}.fact"),
                data["expansion_path_id"],
            )
        except GraphRecipeFailure:
            raise
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True, init=False)
class DigestValue:
    """A digest field whose status-specific JSON shape remains explicit."""

    status: str
    _payload_json: str = field(repr=False)

    def __init__(self, status: str, payload: Mapping[str, Any]) -> None:
        _require_text(status, "digest status")
        if not isinstance(payload, Mapping):
            raise TypeError("digest payload must be a mapping")
        if "status" in payload:
            raise ValueError("digest payload must not repeat status")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "_payload_json", _canonical_json(dict(payload)))

    @property
    def payload(self) -> dict[str, Any]:
        return json.loads(self._payload_json)

    def as_dict(self) -> dict[str, Any]:
        return {"status": self.status, **self.payload}

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "DigestValue":
        data = dict(_require_object(value, subject))
        if "status" not in data:
            raise _model_failure(subject, f"{subject} is missing required field: status.", missing_fields=["status"])
        status = data.pop("status")
        try:
            return cls(status, data)
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class TerminalFactsArtifact:
    schema_version: str
    status: str
    invocation_digest: DigestValue
    emissions: tuple[ExpansionEmission, ...]

    def __post_init__(self) -> None:
        _require_text(self.schema_version, "terminal facts schema_version")
        _require_text(self.status, "terminal facts status")
        if not isinstance(self.invocation_digest, DigestValue):
            raise TypeError("invocation_digest must be DigestValue")
        if not all(isinstance(item, ExpansionEmission) for item in self.emissions):
            raise TypeError("emissions must contain ExpansionEmission values")
        object.__setattr__(
            self,
            "emissions",
            tuple(sorted(self.emissions, key=lambda item: (*terminal_fact_sort_key(item.fact), item.emission_id))),
        )
        if len({item.emission_id for item in self.emissions}) != len(self.emissions):
            raise ValueError("emission IDs must be unique")

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "invocation_digest": self.invocation_digest.as_dict(),
            "emissions": [item.as_dict() for item in self.emissions],
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str = "TerminalFactsArtifact") -> "TerminalFactsArtifact":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("schema_version", "status", "invocation_digest", "emissions"), subject)
        emissions = _require_array(data["emissions"], f"{subject}.emissions")
        try:
            return cls(
                data["schema_version"],
                data["status"],
                DigestValue.from_dict(data["invocation_digest"], subject=f"{subject}.invocation_digest"),
                tuple(
                    ExpansionEmission.from_dict(item, subject=f"{subject}.emissions[{index}]")
                    for index, item in enumerate(emissions)
                ),
            )
        except GraphRecipeFailure:
            raise
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class ConstructionMember:
    member: str
    operation_kind: str
    record_type: str
    record_id: str

    def __post_init__(self) -> None:
        RecordFact(self.member, self.operation_kind, self.record_type, self.record_id)

    @classmethod
    def from_record(cls, fact: RecordFact) -> "ConstructionMember":
        if not isinstance(fact, RecordFact):
            raise TypeError("construction member requires a RecordFact")
        return cls(fact.member, fact.operation_kind, fact.record_type, fact.record_id)

    def as_dict(self) -> dict[str, str]:
        return {
            "member": self.member,
            "operation_kind": self.operation_kind,
            "record_type": self.record_type,
            "record_id": self.record_id,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "ConstructionMember":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("member", "operation_kind", "record_type", "record_id"), subject)
        try:
            return cls(data["member"], data["operation_kind"], data["record_type"], data["record_id"])
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class MemberDependency:
    prerequisite_member: str
    member: str

    def __post_init__(self) -> None:
        _require_iri(self.prerequisite_member, "prerequisite_member")
        _require_iri(self.member, "dependency member")

    def as_dict(self) -> dict[str, str]:
        return {"prerequisite_member": self.prerequisite_member, "member": self.member}

    @classmethod
    def from_dict(cls, value: Mapping[str, Any], *, subject: str) -> "MemberDependency":
        data = _require_object(value, subject)
        _require_exact_fields(data, ("prerequisite_member", "member"), subject)
        try:
            return cls(data["prerequisite_member"], data["member"])
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error


@dataclass(frozen=True)
class ConstructionMemberGraph:
    schema_version: str
    status: str
    members: tuple[ConstructionMember, ...]
    dependencies: tuple[MemberDependency, ...]
    acyclic: bool
    topological_order: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.schema_version, "member graph schema_version")
        _require_text(self.status, "member graph status")
        if not all(isinstance(item, ConstructionMember) for item in self.members):
            raise TypeError("members must contain ConstructionMember values")
        if not all(isinstance(item, MemberDependency) for item in self.dependencies):
            raise TypeError("dependencies must contain MemberDependency values")
        if not isinstance(self.acyclic, bool):
            raise TypeError("acyclic must be bool")
        object.__setattr__(self, "members", tuple(sorted(self.members, key=lambda item: item.member)))
        object.__setattr__(
            self,
            "dependencies",
            tuple(sorted(self.dependencies, key=lambda item: (item.prerequisite_member, item.member))),
        )
        names = tuple(item.member for item in self.members)
        if len(set(names)) != len(names):
            raise ValueError("construction member IRIs must be unique")
        if self.acyclic and (len(self.topological_order) != len(names) or set(self.topological_order) != set(names)):
            raise ValueError("acyclic member graph topological_order must contain every member exactly once")

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "members": [item.as_dict() for item in self.members],
            "dependencies": [item.as_dict() for item in self.dependencies],
            "acyclic": self.acyclic,
            "topological_order": list(self.topological_order),
        }

    @classmethod
    def from_dict(
        cls,
        value: Mapping[str, Any],
        *,
        subject: str = "ConstructionMemberGraph",
    ) -> "ConstructionMemberGraph":
        data = _require_object(value, subject)
        fields = ("schema_version", "status", "members", "dependencies", "acyclic", "topological_order")
        _require_exact_fields(data, fields, subject)
        members = _require_array(data["members"], f"{subject}.members")
        dependencies = _require_array(data["dependencies"], f"{subject}.dependencies")
        order = _require_array(data["topological_order"], f"{subject}.topological_order")
        try:
            return cls(
                data["schema_version"],
                data["status"],
                tuple(
                    ConstructionMember.from_dict(item, subject=f"{subject}.members[{index}]")
                    for index, item in enumerate(members)
                ),
                tuple(
                    MemberDependency.from_dict(item, subject=f"{subject}.dependencies[{index}]")
                    for index, item in enumerate(dependencies)
                ),
                data["acyclic"],
                tuple(order),
            )
        except GraphRecipeFailure:
            raise
        except (TypeError, ValueError) as error:
            raise _model_failure(subject, str(error)) from error

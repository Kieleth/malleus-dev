"""Private LinkML adapter for a small, explicit neutral-contract subset.

The adjacent profile owns the accepted source shapes and semantic policy. This
module supplies generic parsing, validation, identity, and fact-encoding
mechanisms. It performs no source or network resolution.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
from typing import Any, Mapping
from unicodedata import category
from urllib.parse import urlsplit

from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.loaders import yaml_loader
import yaml
from yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode
from yaml.tokens import (
    AliasToken,
    AnchorToken,
    DirectiveToken,
    DocumentEndToken,
    DocumentStartToken,
    TagToken,
)


class ContractCompileError(ValueError):
    """The complete source cannot be compiled under the active profile."""


FactObject = bool | str


@dataclass(frozen=True, slots=True)
class ContractProperty:
    """One predicate and value in a neutral declaration."""

    predicate: str
    object: FactObject


@dataclass(frozen=True, slots=True)
class ContractDeclaration:
    """One frontend-neutral declaration before fact encoding."""

    identifier: str
    kind: str
    properties: tuple[ContractProperty, ...]


@dataclass(frozen=True, slots=True)
class NeutralContract:
    """The adapter result consumed by the generic fact encoder."""

    declarations: tuple[ContractDeclaration, ...]


@dataclass(frozen=True, slots=True)
class ContractFact:
    """One immutable canonical contract fact."""

    subject: str
    predicate: str
    object: FactObject

    def as_dict(self) -> dict[str, FactObject]:
        """Return the exact three-member logical record."""

        return {
            "object": self.object,
            "predicate": self.predicate,
            "subject": self.subject,
        }


@dataclass(frozen=True, slots=True)
class SourceAttestation:
    """Identity of the exact caller-supplied source."""

    locator: str
    byte_length: int
    sha256: str


@dataclass(frozen=True, slots=True)
class CompilerImplementation:
    """Exact profile and executor coordinates used for the result."""

    adapter: str
    linkml_version: str
    linkml_runtime_version: str
    support_profile: str
    profile_sha256: str
    executor_sha256: str


@dataclass(frozen=True, slots=True)
class ContractCompilation:
    """Immutable result of compiling one exact source blob."""

    contract: NeutralContract
    facts: tuple[ContractFact, ...]
    canonical_facts: bytes
    facts_sha256: str
    source: SourceAttestation
    implementation: CompilerImplementation


@dataclass(frozen=True, slots=True)
class _Profile:
    data: Mapping[str, Any]
    digest: str

    def mapping(self, key: str) -> Mapping[str, Any]:
        value = self.data[key]
        if not isinstance(value, Mapping):
            raise RuntimeError(f"validated profile member {key!r} is not a mapping")
        return value

    def shape(self, name: str) -> Mapping[str, Any]:
        value = self.mapping("node_shapes")[name]
        if not isinstance(value, Mapping):
            raise RuntimeError(f"validated node shape {name!r} is not a mapping")
        return value

    def fields(self, shape: str) -> Mapping[str, Mapping[str, Any]]:
        raw = self.shape(shape)["fields"]
        if not isinstance(raw, Mapping):
            raise RuntimeError(f"validated fields for {shape!r} are not a mapping")
        return raw

    def field(self, shape: str, name: str) -> Mapping[str, Any]:
        return self.fields(shape)[name]

    def default(self, reference: str) -> object:
        group, field = reference.split(".", 1)
        return self.mapping("defaults")[group][field]


@dataclass(frozen=True, slots=True)
class _Slot:
    name: str
    identifier: str
    authored: Mapping[str, object]
    shape: str


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _plain_json(value: object) -> object:
    if isinstance(value, Mapping):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("profile mapping keys must be strings")
        return {key: _plain_json(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_plain_json(item) for item in value]
    if isinstance(value, tuple):
        raise TypeError("profile sequences must be lists")
    return value


_PROFILE_PATH = Path(__file__).with_name("_contract_compiler_profile.json")
_SCHEMA_ID = "malleus.contract-compiler.linkml-profile/v0"
_CANONICALIZERS = {"malleus.canonical-json/compact-sorted-key-utf8-no-newline/v0"}
_CLASSIFICATIONS = (
    "ANNOTATION_ONLY",
    "ENFORCED",
    "IDENTITY_ONLY",
    "UNSUPPORTED",
)
_PARSERS = {
    "boolean",
    "decimal",
    "enum_values",
    "items",
    "mapping",
    "module_iri",
    "named",
    "nonempty_string",
    "string",
    "string_list",
}
_RESOLVERS = {"class", "mixin_list", "range", "seed"}
_ROOT_KEYS = {
    "adapter",
    "builtins",
    "canonicalization",
    "defaults",
    "kinds",
    "linkml_runtime_version",
    "linkml_version",
    "lowering_plan",
    "namespace",
    "node_shapes",
    "predicates",
    "range_resolution",
    "schema",
    "seed_primitives",
    "structural_identities",
    "support_profile",
    "symbol_policy",
    "trusted_import",
}
_SHAPE_KEYS = {
    "constraints",
    "fields",
    "kind",
    "label",
    "max_fields",
    "min_fields",
    "rules",
    "use_identity",
}
_FIELD_KEYS = {
    "classification",
    "default",
    "identity_role",
    "item_shape",
    "max_items",
    "member",
    "min_items",
    "parser",
    "predicate",
    "required",
    "resolver",
    "schema_default",
    "values",
}
_KIND_NAMES = {
    "class",
    "enum",
    "exactly_one_alternative",
    "exactly_one_group",
    "scalar",
    "slot",
    "slot_condition",
    "slot_use",
}
_PREDICATE_NAMES = {
    "abstract",
    "enum_value",
    "equals_string",
    "identifier",
    "in_alternative",
    "in_group",
    "inlined",
    "is_mixin",
    "maximum_value",
    "minimum_value",
    "multivalued",
    "on_class",
    "required",
    "subclass_of",
    "type",
    "typeof",
    "uses_mixin",
    "uses_slot",
    "value_presence",
    "value_range",
}
_SHAPE_NAMES = {
    "alternative",
    "attribute",
    "class",
    "condition",
    "enum",
    "permissible_value",
    "schema",
    "slot",
    "type",
}
_IDENTITY_NAMES = {
    "alternative_semantics",
    "exactly_one_alternative",
    "exactly_one_group",
    "slot_condition",
    "slot_use",
}
_PLAN_KEYS = {
    "validate_imports": {"field", "op"},
    "validate_shared_namespace": {"collections", "op"},
    "declare_direct_seed_scalars": {"base_field", "collection", "op", "shape"},
    "declare_enums": {"collection", "op", "shape", "values_field"},
    "declare_slots": {
        "attribute_field",
        "attribute_shape",
        "classes_collection",
        "op",
        "slot_shape",
        "slots_collection",
    },
    "declare_shallow_classes": {
        "collection",
        "derived_mixin_forbidden_fields",
        "mixin_field",
        "mixins_field",
        "op",
        "parent_field",
        "parent_semantic_fields",
        "shape",
    },
    "lower_slot_uses": {
        "attributes_field",
        "classes_collection",
        "kind",
        "on_class_predicate",
        "op",
        "slots_field",
        "uses_slot_predicate",
    },
    "lower_flat_exactly_one": {
        "alternative_identity",
        "alternative_kind",
        "alternatives_field",
        "classes_collection",
        "condition_identity",
        "condition_slot_member",
        "condition_value_field",
        "condition_shape",
        "conditions_field",
        "enum_collection",
        "group_identity",
        "group_kind",
        "group_on_class_predicate",
        "alternative_in_group_predicate",
        "condition_in_alternative_predicate",
        "condition_uses_slot_predicate",
        "op",
        "range_field",
        "semantic_identity",
        "string_builtin",
    },
}
_PLAN_ORDER = tuple(_PLAN_KEYS)


def _profile_mapping(value: object, where: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractCompileError(f"profile {where} must be a mapping")
    return value


def _profile_string(value: object, where: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContractCompileError(f"profile {where} must be a nonempty string")
    return value


def _exact_keys(value: Mapping[str, Any], expected: set[str], where: str) -> None:
    if set(value) != expected:
        delta = sorted(set(value).symmetric_difference(expected))
        raise ContractCompileError(
            f"profile {where} has unexpected member {delta[0]!r}"
        )


def _string_list(value: object, where: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ContractCompileError(f"profile {where} must be a string list")
    if len(value) != len(set(value)):
        raise ContractCompileError(f"profile {where} repeats a value")
    return value


def _nonnegative(value: object, where: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ContractCompileError(f"profile {where} must be a nonnegative integer")
    return value


def _absolute_identifier(value: str, where: str) -> str:
    if any(
        character.isspace() or category(character) in {"Cc", "Cs"}
        for character in value
    ):
        raise ContractCompileError(f"profile {where} contains a forbidden code point")
    try:
        parts = urlsplit(value)
    except ValueError as error:
        raise ContractCompileError(
            f"profile {where} is not an absolute identifier"
        ) from error
    if (
        not parts.scheme
        or not parts.scheme[0].isalpha()
        or not all(
            character.isalnum() or character in {"+", "-", "."}
            for character in parts.scheme
        )
    ):
        raise ContractCompileError(f"profile {where} is not an absolute identifier")
    return value


def _local_identifier(value: str, where: str) -> str:
    valid_start = value and (value[0] == "_" or value[0].isalpha())
    valid_rest = all(character == "_" or character.isalnum() for character in value)
    if not valid_start or not valid_rest or not value.isascii():
        raise ContractCompileError(f"profile {where} is not an ASCII identifier")
    return value


def _term_spec(value: object, where: str) -> Mapping[str, Any]:
    term = _profile_mapping(value, where)
    _exact_keys(term, {"form", "value"}, where)
    form = term["form"]
    text = _profile_string(term["value"], f"{where}.value")
    if form not in {"ABSOLUTE", "LOCAL"}:
        raise ContractCompileError(f"profile {where}.form is not supported")
    if form == "ABSOLUTE":
        _absolute_identifier(text, f"{where}.value")
    else:
        _local_identifier(text, f"{where}.value")
    return term


def _default_compatible(parser: str, value: object) -> bool:
    if parser == "boolean":
        return isinstance(value, bool)
    if parser in {"module_iri", "nonempty_string", "string"}:
        return isinstance(value, str) and (parser == "string" or bool(value))
    return False


def _validate_field(
    shape_name: str,
    field_name: str,
    value: object,
    shapes: Mapping[str, Any],
    defaults: Mapping[str, Any],
    predicates: Mapping[str, Any],
) -> None:
    where = f"node_shapes.{shape_name}.fields.{field_name}"
    field = _profile_mapping(value, where)
    if not {"classification", "parser"}.issubset(field):
        raise ContractCompileError(f"profile {where} lacks classification or parser")
    if not set(field).issubset(_FIELD_KEYS):
        extra = sorted(set(field).difference(_FIELD_KEYS))[0]
        raise ContractCompileError(f"profile {where} has unread member {extra!r}")
    classification = field["classification"]
    parser = field["parser"]
    for member in (
        "classification",
        "default",
        "identity_role",
        "item_shape",
        "member",
        "parser",
        "predicate",
        "resolver",
        "schema_default",
    ):
        if member in field:
            _profile_string(field[member], f"{where}.{member}")
    if classification not in _CLASSIFICATIONS or parser not in _PARSERS:
        raise ContractCompileError(f"profile {where} has an unknown operation")
    if parser == "mapping" and classification != "UNSUPPORTED":
        raise ContractCompileError(f"profile {where}.parser is not executable")
    if "required" in field and not isinstance(field["required"], bool):
        raise ContractCompileError(f"profile {where}.required must be boolean")
    if classification == "UNSUPPORTED" and set(field) != {
        "classification",
        "parser",
    }:
        raise ContractCompileError(f"profile {where} has unread unsupported policy")
    for cardinality in ("min_items", "max_items"):
        if cardinality in field:
            _nonnegative(field[cardinality], f"{where}.{cardinality}")
    if field.get("min_items", 0) > field.get("max_items", float("inf")):
        raise ContractCompileError(f"profile {where} has inverted cardinality")
    if "item_shape" in field:
        if parser not in {"enum_values", "items", "named"}:
            raise ContractCompileError(f"profile {where}.item_shape is unread")
        if field["item_shape"] not in shapes:
            raise ContractCompileError(f"profile {where}.item_shape is unknown")
    if parser in {"enum_values", "items", "named"} and "item_shape" not in field:
        raise ContractCompileError(f"profile {where} lacks item_shape")
    if "predicate" in field:
        if field["predicate"] not in predicates:
            raise ContractCompileError(f"profile {where}.predicate is unknown")
        if classification != "ENFORCED":
            raise ContractCompileError(f"profile {where}.predicate is unread")
        if parser not in {
            "boolean",
            "decimal",
            "enum_values",
            "nonempty_string",
            "string",
            "string_list",
        }:
            raise ContractCompileError(
                f"profile {where}.predicate has a non-scalar parser"
            )
    if "resolver" in field:
        if field["resolver"] not in _RESOLVERS:
            raise ContractCompileError(f"profile {where}.resolver is unknown")
        if classification != "ENFORCED":
            raise ContractCompileError(f"profile {where}.resolver is unread")
        expected_parser = {
            "class": "nonempty_string",
            "mixin_list": "string_list",
            "range": "nonempty_string",
            "seed": "nonempty_string",
        }[field["resolver"]]
        if parser != expected_parser:
            raise ContractCompileError(
                f"profile {where}.resolver has an incompatible parser"
            )
    if "identity_role" in field and (
        classification != "IDENTITY_ONLY" or field["identity_role"] != "module"
    ):
        raise ContractCompileError(f"profile {where}.identity_role is invalid")
    if "identity_role" in field and (
        parser != "module_iri" or field.get("required") is not True
    ):
        raise ContractCompileError(f"profile {where}.identity_role is not executable")
    if classification == "IDENTITY_ONLY" and shape_name != "schema":
        raise ContractCompileError(f"profile {where}.identity_role is outside schema")
    if classification == "IDENTITY_ONLY" and "identity_role" not in field:
        raise ContractCompileError(f"profile {where} lacks an identity_role")
    if "values" in field:
        _string_list(field["values"], f"{where}.values")
        if parser not in {"nonempty_string", "string"}:
            raise ContractCompileError(f"profile {where}.values is unread")
    if ("min_items" in field or "max_items" in field) and parser not in {
        "enum_values",
        "items",
        "named",
        "string_list",
    }:
        raise ContractCompileError(f"profile {where} item cardinality is unread")
    if "member" in field and (classification != "ENFORCED" or "predicate" not in field):
        raise ContractCompileError(f"profile {where}.member is unread")
    if "default" in field:
        if classification != "ENFORCED":
            raise ContractCompileError(f"profile {where}.default is unread")
        reference = _profile_string(field["default"], f"{where}.default")
        try:
            group, member = reference.split(".", 1)
            default = _profile_mapping(defaults[group], group)[member]
        except (KeyError, ValueError) as error:
            raise ContractCompileError(f"profile {where}.default is unknown") from error
        if not _default_compatible(parser, default):
            raise ContractCompileError(f"profile {where}.default has wrong type")
    if "schema_default" in field:
        if classification != "ENFORCED":
            raise ContractCompileError(f"profile {where}.schema_default is unread")
        schema_fields = _profile_mapping(shapes["schema"], "schema")["fields"]
        if field["schema_default"] not in schema_fields:
            raise ContractCompileError(f"profile {where}.schema_default is unknown")
        source = schema_fields[field["schema_default"]]
        if source["classification"] != "ENFORCED" or source["parser"] not in {
            "nonempty_string",
            "string",
        }:
            raise ContractCompileError(
                f"profile {where}.schema_default is incompatible"
            )
        if parser != source["parser"]:
            raise ContractCompileError(
                f"profile {where}.schema_default has incompatible parsers"
            )


def _validate_rules_constraints(
    shape_name: str, shape: Mapping[str, Any], fields: Mapping[str, Any]
) -> None:
    rules = shape.get("rules", [])
    if not isinstance(rules, list):
        raise ContractCompileError(f"profile {shape_name}.rules must be a list")
    rule_keys = {
        "applies_to",
        "if_field",
        "if_value",
        "op",
        "refuse_explicit_conflict",
        "then_field",
        "then_value",
    }
    for index, value in enumerate(rules):
        rule = _profile_mapping(value, f"{shape_name}.rules[{index}]")
        _exact_keys(rule, rule_keys, f"{shape_name}.rules[{index}]")
        if rule["op"] != "implies" or rule["applies_to"] != "slot_use":
            raise ContractCompileError(f"profile {shape_name} has unknown rule")
        if rule["if_field"] not in fields or rule["then_field"] not in fields:
            raise ContractCompileError(f"profile {shape_name} rule field is unknown")
        if any(
            fields[rule[member]]["classification"] != "ENFORCED"
            for member in ("if_field", "then_field")
        ):
            raise ContractCompileError(
                f"profile {shape_name} rule field is not enforced"
            )
        if any(
            fields[rule[member]]["parser"] != "boolean"
            for member in ("if_field", "then_field")
        ):
            raise ContractCompileError(
                f"profile {shape_name} rule operands must be boolean"
            )
        if not isinstance(rule["refuse_explicit_conflict"], bool):
            raise ContractCompileError(f"profile {shape_name} rule flag is invalid")
        for field_member, value_member in (
            ("if_field", "if_value"),
            ("then_field", "then_value"),
        ):
            parser = fields[rule[field_member]]["parser"]
            if not _default_compatible(parser, rule[value_member]):
                raise ContractCompileError(
                    f"profile {shape_name} rule value has wrong type"
                )
    constraints = shape.get("constraints", [])
    if not isinstance(constraints, list):
        raise ContractCompileError(f"profile {shape_name}.constraints must be a list")
    schemas = {
        "equals": {"field", "op", "value"},
        "ordered_bounds": {
            "allowed_builtin_ranges",
            "maximum",
            "minimum",
            "op",
            "range",
        },
    }
    for index, value in enumerate(constraints):
        constraint = _profile_mapping(value, f"{shape_name}.constraints[{index}]")
        operation = constraint.get("op")
        if operation not in schemas:
            raise ContractCompileError(f"profile {shape_name} has unknown constraint")
        _exact_keys(
            constraint, schemas[operation], f"{shape_name}.constraints[{index}]"
        )
        operands = (
            [constraint["field"]]
            if operation == "equals"
            else [constraint[name] for name in ("minimum", "maximum", "range")]
        )
        if any(field not in fields for field in operands):
            raise ContractCompileError(
                f"profile {shape_name} constraint field is unknown"
            )
        if any(fields[field]["classification"] != "ENFORCED" for field in operands):
            raise ContractCompileError(
                f"profile {shape_name} constraint field is not enforced"
            )
        if operation == "equals":
            parser = fields[constraint["field"]]["parser"]
            if not _default_compatible(parser, constraint["value"]):
                raise ContractCompileError(
                    f"profile {shape_name} constraint value has wrong type"
                )
        if operation == "ordered_bounds":
            minimum = fields[constraint["minimum"]]
            maximum = fields[constraint["maximum"]]
            range_field = fields[constraint["range"]]
            if any(
                field["parser"] != "decimal" or "predicate" not in field
                for field in (minimum, maximum)
            ):
                raise ContractCompileError(
                    f"profile {shape_name} bound operand is not decimal"
                )
            if (
                range_field["parser"] != "nonempty_string"
                or range_field.get("resolver") != "range"
                or "predicate" not in range_field
            ):
                raise ContractCompileError(
                    f"profile {shape_name} bound range is not executable"
                )
            allowed = _string_list(
                constraint["allowed_builtin_ranges"],
                f"{shape_name}.allowed_builtin_ranges",
            )
            if not allowed:
                raise ContractCompileError(
                    f"profile {shape_name} numeric ranges must not be empty"
                )


def _validate_plan(
    value: object,
    shapes: Mapping[str, Any],
    kinds: Mapping[str, Any],
    identities: Mapping[str, Any],
    builtins: Mapping[str, Any],
    range_resolution: Mapping[str, Any],
) -> None:
    if not isinstance(value, list):
        raise ContractCompileError("profile lowering_plan must be a list")
    operations = []
    for index, record_value in enumerate(value):
        record = _profile_mapping(record_value, f"lowering_plan[{index}]")
        operation = record.get("op")
        if operation not in _PLAN_KEYS:
            raise ContractCompileError(
                f"profile lowering plan opcode {operation!r} is unknown"
            )
        _exact_keys(record, _PLAN_KEYS[operation], f"lowering_plan[{index}]")
        list_members = {
            "collections",
            "derived_mixin_forbidden_fields",
            "parent_semantic_fields",
        }
        for member, operand in record.items():
            if member in list_members:
                _string_list(operand, f"lowering_plan[{index}].{member}")
            else:
                _profile_string(operand, f"lowering_plan[{index}].{member}")
        operations.append(operation)
    if tuple(operations) != _PLAN_ORDER:
        raise ContractCompileError("profile lowering_plan has unsupported order")
    schema_fields = shapes["schema"]["fields"]
    class_fields = shapes["class"]["fields"]
    alternative_fields = shapes["alternative"]["fields"]
    for record in value:
        operation = record["op"]
        for member, item in record.items():
            if member == "op":
                continue
            if (member.endswith("_shape") or member == "shape") and item not in shapes:
                raise ContractCompileError(f"profile lowering {member} is unknown")
            if member.endswith("_kind") or member == "kind":
                if item not in kinds:
                    raise ContractCompileError(f"profile lowering {member} is unknown")
            if member.endswith("_predicate"):
                if item not in _PREDICATE_NAMES:
                    raise ContractCompileError(f"profile lowering {member} is unknown")
            if member.endswith("_identity") and item not in identities:
                raise ContractCompileError(f"profile lowering {member} is unknown")
            if member.endswith("_collection") or member == "collection":
                if item not in schema_fields:
                    raise ContractCompileError(f"profile lowering {member} is unknown")
        if operation == "validate_shared_namespace":
            collections = _string_list(record["collections"], "plan.collections")
            if any(name not in schema_fields for name in collections):
                raise ContractCompileError("profile lowering collection is unknown")
            if any(
                schema_fields[name]["classification"] != "ENFORCED"
                or schema_fields[name]["parser"] != "named"
                for name in collections
            ):
                raise ContractCompileError(
                    "profile namespace validation operand is not a collection"
                )
        if operation == "declare_shallow_classes":
            for member in (
                "derived_mixin_forbidden_fields",
                "parent_semantic_fields",
            ):
                names = _string_list(record[member], f"plan.{member}")
                if any(name not in class_fields for name in names):
                    raise ContractCompileError(f"profile lowering {member} is unknown")
        if operation == "lower_flat_exactly_one":
            if record["conditions_field"] not in alternative_fields:
                raise ContractCompileError(
                    "profile lowering conditions_field is unknown"
                )
    by_operation = {record["op"]: record for record in value}

    def require_kind(shape_name: str) -> None:
        if shapes[shape_name].get("kind") not in kinds:
            raise ContractCompileError(
                f"profile executable shape {shape_name!r} lacks a kind"
            )

    def require_field(
        shape_name: str,
        field_name: str,
        *,
        parser: str | None = None,
        resolver: str | None = None,
        predicate: bool = False,
    ) -> Mapping[str, Any]:
        field = shapes[shape_name]["fields"].get(field_name)
        if not field or field["classification"] != "ENFORCED":
            raise ContractCompileError(
                f"profile executable field {shape_name}.{field_name} is not enforced"
            )
        if parser is not None and field["parser"] != parser:
            raise ContractCompileError(
                f"profile executable field {shape_name}.{field_name} has wrong parser"
            )
        if resolver is not None and field.get("resolver") != resolver:
            raise ContractCompileError(
                f"profile executable field {shape_name}.{field_name} has wrong resolver"
            )
        if predicate and "predicate" not in field:
            raise ContractCompileError(
                f"profile executable field {shape_name}.{field_name} lacks a predicate"
            )
        return field

    def require_identity(name: str, roles: set[str]) -> None:
        identity = identities[name]
        if set(identity["member_roles"]) != roles:
            raise ContractCompileError(
                f"profile structural identity {name!r} has wrong roles"
            )

    def collection_shape(name: str) -> str:
        field = schema_fields[name]
        if field["classification"] != "ENFORCED" or field["parser"] != "named":
            raise ContractCompileError(
                f"profile lowering collection {name!r} is not named"
            )
        return str(field["item_shape"])

    imports = by_operation["validate_imports"]
    if imports["field"] not in schema_fields:
        raise ContractCompileError("profile lowering imports field is unknown")
    import_field = schema_fields[imports["field"]]
    if (
        import_field["classification"] != "ENFORCED"
        or import_field["parser"] != "string_list"
    ):
        raise ContractCompileError("profile lowering imports field is incompatible")
    scalars = by_operation["declare_direct_seed_scalars"]
    if collection_shape(str(scalars["collection"])) != scalars["shape"]:
        raise ContractCompileError("profile scalar lowering shape does not match")
    require_kind(str(scalars["shape"]))
    require_field(
        str(scalars["shape"]),
        str(scalars["base_field"]),
        parser="nonempty_string",
        resolver="seed",
        predicate=True,
    )
    enums = by_operation["declare_enums"]
    if collection_shape(str(enums["collection"])) != enums["shape"]:
        raise ContractCompileError("profile enum lowering shape does not match")
    require_kind(str(enums["shape"]))
    enum_values = require_field(
        str(enums["shape"]),
        str(enums["values_field"]),
        parser="enum_values",
        predicate=True,
    )
    enum_value_shape = shapes[str(enum_values["item_shape"])]
    if enum_value_shape.get("min_fields", 0) != 0 or any(
        field["classification"] != "ANNOTATION_ONLY" or field.get("required") is True
        for field in enum_value_shape["fields"].values()
    ):
        raise ContractCompileError(
            "profile enum value body contains executable semantic policy"
        )
    enum_value_emitters = {
        (shape_name, field_name)
        for shape_name, shape in shapes.items()
        for field_name, field in shape["fields"].items()
        if field["parser"] == "enum_values" and "predicate" in field
    }
    if enum_value_emitters != {(str(enums["shape"]), str(enums["values_field"]))}:
        raise ContractCompileError(
            "profile enum-values predicate lacks the dedicated emitter"
        )
    slots = by_operation["declare_slots"]
    if collection_shape(str(slots["slots_collection"])) != slots["slot_shape"]:
        raise ContractCompileError("profile slot lowering shape does not match")
    slot_shapes = {str(slots["slot_shape"]), str(slots["attribute_shape"])}
    for shape_name in slot_shapes:
        require_kind(shape_name)
        identity_name = shapes[shape_name].get("use_identity")
        if identity_name not in identities:
            raise ContractCompileError(
                f"profile executable shape {shape_name!r} lacks slot-use identity"
            )
        require_identity(str(identity_name), {"class", "domain", "slot"})
    class_shape = collection_shape(str(slots["classes_collection"]))
    attribute = require_field(
        class_shape, str(slots["attribute_field"]), parser="named"
    )
    if attribute.get("item_shape") != slots["attribute_shape"]:
        raise ContractCompileError("profile attribute lowering shape does not match")
    classes = by_operation["declare_shallow_classes"]
    if collection_shape(str(classes["collection"])) != classes["shape"]:
        raise ContractCompileError("profile class lowering shape does not match")
    declared_class_shape = str(classes["shape"])
    require_kind(declared_class_shape)
    require_field(
        declared_class_shape,
        str(classes["parent_field"]),
        parser="nonempty_string",
        resolver="class",
        predicate=True,
    )
    require_field(
        declared_class_shape,
        str(classes["mixins_field"]),
        parser="string_list",
        resolver="mixin_list",
        predicate=True,
    )
    require_field(
        declared_class_shape,
        str(classes["mixin_field"]),
        parser="boolean",
        predicate=True,
    )
    for member in ("derived_mixin_forbidden_fields", "parent_semantic_fields"):
        for field in classes[member]:
            require_field(declared_class_shape, str(field))
    uses = by_operation["lower_slot_uses"]
    uses_shape = collection_shape(str(uses["classes_collection"]))
    require_field(uses_shape, str(uses["attributes_field"]), parser="named")
    require_field(uses_shape, str(uses["slots_field"]), parser="string_list")
    expressions = by_operation["lower_flat_exactly_one"]
    expression_shape = collection_shape(str(expressions["classes_collection"]))
    alternative = require_field(
        expression_shape, str(expressions["alternatives_field"]), parser="items"
    )
    conditions = require_field(
        str(alternative["item_shape"]),
        str(expressions["conditions_field"]),
        parser="named",
    )
    if conditions.get("item_shape") != expressions["condition_shape"]:
        raise ContractCompileError("profile conditions field is not executable")
    if (
        conditions.get("min_items") != 1
        or conditions.get("max_items") != 1
        or conditions.get("required") is not True
    ):
        raise ContractCompileError(
            "profile conditions field must select exactly one condition"
        )
    condition_shape_name = str(expressions["condition_shape"])
    require_kind(condition_shape_name)
    require_field(
        condition_shape_name,
        str(expressions["condition_value_field"]),
        predicate=True,
    )
    condition_fields = [
        field
        for field in shapes[condition_shape_name]["fields"].values()
        if field["classification"] == "ENFORCED"
    ]
    if any("member" not in field for field in condition_fields):
        raise ContractCompileError("profile condition field lacks a semantic member")
    condition_members = [str(field["member"]) for field in condition_fields]
    for member in [*condition_members, str(expressions["condition_slot_member"])]:
        _local_identifier(member, "condition semantic member")
    if len(condition_members) != len(set(condition_members)):
        raise ContractCompileError("profile condition fields alias a semantic member")
    if expressions["condition_slot_member"] in condition_members:
        raise ContractCompileError("profile condition slot aliases a semantic member")
    if expressions["string_builtin"] not in builtins:
        raise ContractCompileError("profile condition builtin is unknown")
    if expressions["enum_collection"] != by_operation["declare_enums"]["collection"]:
        raise ContractCompileError("profile condition enum collection is inconsistent")
    for shape_name in slot_shapes:
        require_field(
            shape_name,
            str(expressions["range_field"]),
            parser="nonempty_string",
            resolver="range",
            predicate=True,
        )
    require_identity(str(expressions["semantic_identity"]), {"conditions", "domain"})
    require_identity(
        str(expressions["group_identity"]),
        {"alternative_semantic_digests", "class", "domain"},
    )
    require_identity(
        str(expressions["alternative_identity"]),
        {"alternative_semantic_digest", "domain", "group"},
    )
    require_identity(
        str(expressions["condition_identity"]),
        {"alternative", "domain", "slot"},
    )
    expected_range_spaces = [str(scalars["collection"]), str(enums["collection"])]
    if range_resolution["declaration_collections"] != expected_range_spaces:
        raise ContractCompileError("profile range declaration spaces are inconsistent")

    declaration_shapes = {
        str(scalars["shape"]),
        str(enums["shape"]),
        *slot_shapes,
        declared_class_shape,
        condition_shape_name,
    }
    if (
        shapes[str(slots["slot_shape"])]["kind"]
        != shapes[str(slots["attribute_shape"])]["kind"]
    ):
        raise ContractCompileError("profile slot shapes disagree on their kind")
    node_role_kinds = [
        shapes[str(scalars["shape"])]["kind"],
        shapes[str(enums["shape"])]["kind"],
        shapes[str(slots["slot_shape"])]["kind"],
        shapes[declared_class_shape]["kind"],
        shapes[condition_shape_name]["kind"],
        uses["kind"],
        expressions["group_kind"],
        expressions["alternative_kind"],
    ]
    if len(node_role_kinds) != len(set(node_role_kinds)):
        raise ContractCompileError("profile node roles alias a kind")

    def require_distinct_predicates(names: list[str], where: str) -> None:
        if len(names) != len(set(names)):
            raise ContractCompileError(f"profile {where} aliases a predicate role")

    for shape_name in declaration_shapes:
        require_distinct_predicates(
            ["type"]
            + [
                str(field["predicate"])
                for field in shapes[shape_name]["fields"].values()
                if field["classification"] == "ENFORCED" and "predicate" in field
            ],
            f"shape {shape_name!r}",
        )
    for shape_name in slot_shapes:
        require_distinct_predicates(
            [
                "type",
                str(uses["on_class_predicate"]),
                str(uses["uses_slot_predicate"]),
            ]
            + [
                str(field["predicate"])
                for field in shapes[shape_name]["fields"].values()
                if field["classification"] == "ENFORCED" and "predicate" in field
            ],
            "slot-use node",
        )
    require_distinct_predicates(
        ["type", str(expressions["group_on_class_predicate"])], "group node"
    )
    require_distinct_predicates(
        ["type", str(expressions["alternative_in_group_predicate"])],
        "alternative node",
    )
    require_distinct_predicates(
        [
            "type",
            str(expressions["condition_in_alternative_predicate"]),
            str(expressions["condition_uses_slot_predicate"]),
        ]
        + [
            str(field["predicate"])
            for field in shapes[condition_shape_name]["fields"].values()
            if field["classification"] == "ENFORCED" and "predicate" in field
        ],
        "condition node",
    )
    effective_shapes = {*slot_shapes, declared_class_shape, condition_shape_name}
    consumed_fields: set[tuple[str, str]] = set()

    def consume(shape_name: str, *field_names: object) -> None:
        consumed_fields.update((shape_name, str(field)) for field in field_names)

    consume("schema", imports["field"])
    consume("schema", *by_operation["validate_shared_namespace"]["collections"])
    consume(
        "schema",
        scalars["collection"],
        enums["collection"],
        slots["slots_collection"],
        slots["classes_collection"],
        classes["collection"],
        uses["classes_collection"],
        expressions["classes_collection"],
        expressions["enum_collection"],
        *range_resolution["declaration_collections"],
    )
    consume(str(scalars["shape"]), scalars["base_field"])
    consume(str(enums["shape"]), enums["values_field"])
    consume(class_shape, slots["attribute_field"])
    consume(
        declared_class_shape,
        classes["mixin_field"],
        classes["mixins_field"],
        classes["parent_field"],
        *classes["derived_mixin_forbidden_fields"],
        *classes["parent_semantic_fields"],
        uses["attributes_field"],
        uses["slots_field"],
        expressions["alternatives_field"],
    )
    consume(str(alternative["item_shape"]), expressions["conditions_field"])
    consume(condition_shape_name, expressions["condition_value_field"])
    for shape_name in slot_shapes:
        consume(shape_name, expressions["range_field"])
    for shape_name in effective_shapes:
        consume(
            shape_name,
            *(
                field_name
                for field_name, field in shapes[shape_name]["fields"].items()
                if field["classification"] == "ENFORCED" and "predicate" in field
            ),
        )
    for shape in shapes.values():
        for field in shape["fields"].values():
            if "schema_default" in field:
                consume("schema", field["schema_default"])
    for shape_name, shape in shapes.items():
        for field_name, field in shape["fields"].items():
            if (
                field["classification"] == "ENFORCED"
                and (shape_name, field_name) not in consumed_fields
            ):
                raise ContractCompileError(
                    f"profile field {shape_name}.{field_name} has no semantic consumer"
                )
    for shape_name, shape in shapes.items():
        if "kind" in shape and shape_name not in declaration_shapes:
            raise ContractCompileError(
                f"profile shape {shape_name!r} has unread kind policy"
            )
        if "use_identity" in shape and shape_name not in slot_shapes:
            raise ContractCompileError(
                f"profile shape {shape_name!r} has unread identity policy"
            )
        if "rules" in shape and shape_name not in slot_shapes:
            raise ContractCompileError(
                f"profile shape {shape_name!r} has unread rule policy"
            )
        if "constraints" in shape and shape_name not in effective_shapes:
            raise ContractCompileError(
                f"profile shape {shape_name!r} has unread constraint policy"
            )
        for field_name, field in shape["fields"].items():
            if "member" in field and shape_name != condition_shape_name:
                raise ContractCompileError(
                    f"profile field {shape_name}.{field_name} has unread member policy"
                )
            if (
                "default" in field or "schema_default" in field
            ) and shape_name not in effective_shapes:
                raise ContractCompileError(
                    f"profile field {shape_name}.{field_name} has unread default policy"
                )


def _validate_profile(data: Mapping[str, Any]) -> None:
    _exact_keys(data, _ROOT_KEYS, "root")
    if data["schema"] != _SCHEMA_ID or data["adapter"] != "linkml":
        raise ContractCompileError("profile schema or adapter is not supported")
    if data["canonicalization"] not in _CANONICALIZERS:
        raise ContractCompileError("profile canonicalization is not supported")
    for member in (
        "linkml_runtime_version",
        "linkml_version",
        "namespace",
        "support_profile",
        "trusted_import",
    ):
        _profile_string(data[member], member)
    if data["linkml_version"] != "1.11.1" or data["linkml_runtime_version"] != "1.11.1":
        raise ContractCompileError("profile LinkML versions are not supported")
    _absolute_identifier(str(data["namespace"]), "namespace")
    if not str(data["namespace"]).endswith("/"):
        raise ContractCompileError("profile namespace must be an absolute IRI base")
    defaults = _profile_mapping(data["defaults"], "defaults")
    _exact_keys(defaults, {"class", "slot"}, "defaults")
    _exact_keys(
        _profile_mapping(defaults["class"], "defaults.class"),
        {"abstract", "mixin"},
        "defaults.class",
    )
    _exact_keys(
        _profile_mapping(defaults["slot"], "defaults.slot"),
        {"identifier", "inlined", "multivalued", "range", "required"},
        "defaults.slot",
    )
    builtins = _profile_mapping(data["builtins"], "builtins")
    seeds = _string_list(data["seed_primitives"], "seed_primitives")
    if set(builtins) != set(seeds):
        raise ContractCompileError("profile builtins and seed primitives differ")
    kinds = _profile_mapping(data["kinds"], "kinds")
    predicates = _profile_mapping(data["predicates"], "predicates")
    _exact_keys(kinds, _KIND_NAMES, "kinds")
    _exact_keys(predicates, _PREDICATE_NAMES, "predicates")
    resolved_resources: list[str] = []
    for registry_name, registry in (
        ("builtins", builtins),
        ("kinds", kinds),
        ("predicates", predicates),
    ):
        for name, term in registry.items():
            _term_spec(term, f"{registry_name}.{name}")
        resolved = [
            (
                str(term["value"])
                if term["form"] == "ABSOLUTE"
                else str(data["namespace"]) + str(term["value"])
            )
            for term in registry.values()
        ]
        if len(resolved) != len(set(resolved)):
            raise ContractCompileError(f"profile {registry_name} resolves a collision")
        resolved_resources.extend(resolved)
    if len(resolved_resources) != len(set(resolved_resources)):
        raise ContractCompileError("profile semantic registries resolve a collision")
    shapes = _profile_mapping(data["node_shapes"], "node_shapes")
    _exact_keys(shapes, _SHAPE_NAMES, "node_shapes")
    identities = _profile_mapping(
        data["structural_identities"], "structural_identities"
    )
    _exact_keys(identities, _IDENTITY_NAMES, "structural_identities")
    for shape_name, shape_value in shapes.items():
        shape = _profile_mapping(shape_value, f"node_shapes.{shape_name}")
        if not {"fields", "label"}.issubset(shape) or not set(shape).issubset(
            _SHAPE_KEYS
        ):
            raise ContractCompileError(
                f"profile node shape {shape_name!r} is not closed"
            )
        _profile_string(shape["label"], f"node_shapes.{shape_name}.label")
        fields = _profile_mapping(shape["fields"], f"node_shapes.{shape_name}.fields")
        if "kind" in shape and shape["kind"] not in kinds:
            raise ContractCompileError(
                f"profile node shape {shape_name!r} kind is unknown"
            )
        if "use_identity" in shape and shape["use_identity"] not in identities:
            raise ContractCompileError(
                f"profile node shape {shape_name!r} identity is unknown"
            )
        for cardinality in ("min_fields", "max_fields"):
            if cardinality in shape:
                _nonnegative(shape[cardinality], f"{shape_name}.{cardinality}")
        if shape.get("min_fields", 0) > shape.get("max_fields", float("inf")):
            raise ContractCompileError(
                f"profile node shape {shape_name!r} cardinality is inverted"
            )
        for field_name, field in fields.items():
            _validate_field(shape_name, field_name, field, shapes, defaults, predicates)
        _validate_rules_constraints(shape_name, shape, fields)
        for constraint in shape.get("constraints", ()):
            if constraint["op"] == "ordered_bounds" and not set(
                constraint["allowed_builtin_ranges"]
            ).issubset(builtins):
                raise ContractCompileError(
                    f"profile node shape {shape_name!r} names unknown numeric seeds"
                )
    for name, identity_value in identities.items():
        identity = _profile_mapping(identity_value, f"structural_identities.{name}")
        _exact_keys(
            identity,
            {"domain", "member_roles", "prefix"},
            f"structural_identities.{name}",
        )
        _profile_string(identity["domain"], f"{name}.domain")
        prefix = _profile_string(identity["prefix"], f"{name}.prefix")
        _absolute_identifier(prefix, f"structural_identities.{name}.prefix")
        roles = _profile_mapping(
            identity["member_roles"], f"structural_identities.{name}.member_roles"
        )
        if not roles:
            raise ContractCompileError(
                f"profile structural identity {name!r} has no member roles"
            )
        for role, member in roles.items():
            _local_identifier(role, f"structural_identities.{name}.role")
            _local_identifier(member, f"structural_identities.{name}.member")
        if len(roles) != len(set(roles.values())):
            raise ContractCompileError(
                f"profile structural identity {name!r} repeats a member"
            )
    symbol_policy = _profile_mapping(data["symbol_policy"], "symbol_policy")
    _exact_keys(
        symbol_policy,
        {"identity", "join_operation", "key_parser", "separator"},
        "symbol_policy",
    )
    _absolute_identifier(
        _profile_string(symbol_policy["identity"], "symbol_policy.identity"),
        "symbol_policy.identity",
    )
    if symbol_policy["join_operation"] != "delimiter_join":
        raise ContractCompileError("profile symbol join operation is unsupported")
    if symbol_policy["key_parser"] != "ascii_identifier":
        raise ContractCompileError("profile symbol key parser is unsupported")
    if symbol_policy["separator"] != "/":
        raise ContractCompileError("profile symbol separator is unsupported")
    range_resolution = _profile_mapping(data["range_resolution"], "range_resolution")
    _exact_keys(
        range_resolution,
        {"builtin_registry", "declaration_collections", "op"},
        "range_resolution",
    )
    if range_resolution["op"] != "ordered_spaces":
        raise ContractCompileError("profile range resolution operation is unsupported")
    if range_resolution["builtin_registry"] != "builtins":
        raise ContractCompileError("profile range builtin registry is unknown")
    declaration_collections = _string_list(
        range_resolution["declaration_collections"],
        "range_resolution.declaration_collections",
    )
    if not declaration_collections:
        raise ContractCompileError("profile range declaration spaces are empty")
    module_identities = [
        field
        for field in shapes["schema"]["fields"].values()
        if field.get("identity_role") == "module"
    ]
    if len(module_identities) != 1:
        raise ContractCompileError("profile schema must declare one module identity")
    _validate_plan(
        data["lowering_plan"],
        shapes,
        kinds,
        identities,
        builtins,
        range_resolution,
    )


def _load_profile(injected: Mapping[str, object] | None) -> _Profile:
    try:
        if injected is None:
            raw = _PROFILE_PATH.read_bytes()
            data = json.loads(raw)
            digest = sha256(raw).hexdigest()
        else:
            plain = _plain_json(injected)
            raw = _canonical_json(plain)
            data = json.loads(raw)
            digest = sha256(raw).hexdigest()
    except (OSError, TypeError, ValueError) as error:
        raise ContractCompileError(f"profile cannot be loaded: {error}") from error
    if not isinstance(data, Mapping):
        raise ContractCompileError("profile root must be a mapping")
    try:
        _validate_profile(data)
    except ContractCompileError:
        raise
    except (KeyError, RuntimeError, TypeError, ValueError) as error:
        raise ContractCompileError(
            f"profile validation refused malformed state: {error}"
        ) from error
    return _Profile(data, digest)


_YAML_STRING = "tag:yaml.org,2002:str"
_YAML_BOOLEAN = "tag:yaml.org,2002:bool"
_YAML_NULL = "tag:yaml.org,2002:null"


def _mapping_items(node: Node, where: str) -> list[tuple[str, Node]]:
    if not isinstance(node, MappingNode):
        raise ContractCompileError(f"{where} must be a mapping")
    result: list[tuple[str, Node]] = []
    seen: set[str] = set()
    for key_node, value_node in node.value:
        if not isinstance(key_node, ScalarNode) or key_node.tag != _YAML_STRING:
            raise ContractCompileError(f"{where} has a non-string mapping key")
        key = key_node.value
        if key == "<<":
            raise ContractCompileError(f"{where} contains a YAML merge key")
        if key in seen:
            raise ContractCompileError(f"{where} repeats field {key!r}")
        seen.add(key)
        result.append((key, value_node))
    return result


def _string(node: Node, where: str, *, nonempty: bool = False) -> str:
    if not isinstance(node, ScalarNode) or node.tag != _YAML_STRING:
        raise ContractCompileError(f"{where} must be a string")
    if nonempty and not node.value:
        raise ContractCompileError(f"{where} must be a nonempty string")
    return node.value


def _boolean(node: Node, where: str) -> bool:
    if (
        not isinstance(node, ScalarNode)
        or node.style is not None
        or node.tag != _YAML_BOOLEAN
        or node.value not in {"true", "false"}
    ):
        raise ContractCompileError(f"{where} must be raw lowercase true or false")
    return node.value == "true"


def _decimal(node: Node, where: str) -> str:
    if not isinstance(node, ScalarNode) or node.style is not None:
        raise ContractCompileError(f"{where} must be an unquoted JSON number")
    text = node.value
    index = 1 if text.startswith("-") else 0
    if index >= len(text):
        raise ContractCompileError(f"{where} has an invalid numeric lexeme")
    if text[index] == "0":
        index += 1
        if index < len(text) and text[index].isdigit():
            raise ContractCompileError(f"{where} has a leading zero")
    elif "1" <= text[index] <= "9":
        while index < len(text) and text[index].isdigit():
            index += 1
    else:
        raise ContractCompileError(f"{where} has an invalid integer part")
    if index < len(text) and text[index] == ".":
        index += 1
        start = index
        while index < len(text) and text[index].isdigit():
            index += 1
        if index == start:
            raise ContractCompileError(f"{where} has an empty fraction")
    if index < len(text) and text[index] in {"e", "E"}:
        index += 1
        if index < len(text) and text[index] in {"+", "-"}:
            index += 1
        start = index
        while index < len(text) and text[index].isdigit():
            index += 1
        if index == start:
            raise ContractCompileError(f"{where} has an empty exponent")
    if index != len(text):
        raise ContractCompileError(f"{where} has an invalid numeric lexeme")
    try:
        value = Decimal(text)
    except InvalidOperation as error:
        raise ContractCompileError(f"{where} is not a finite decimal") from error
    if not value.is_finite():
        raise ContractCompileError(f"{where} is not a finite decimal")
    if value.is_zero():
        return "0"
    fixed = format(value, "f")
    return fixed.rstrip("0").rstrip(".") if "." in fixed else fixed


def _identifier(value: str, where: str) -> str:
    try:
        _local_identifier(value, where)
    except ContractCompileError:
        raise ContractCompileError(f"{where} has invalid declaration key {value!r}")
    return value


def _module_iri(node: Node, where: str) -> str:
    value = _string(node, where, nonempty=True)
    try:
        _absolute_identifier(value, where)
        parts = urlsplit(value)
    except ContractCompileError as error:
        raise ContractCompileError(f"{where} must be an absolute IRI") from error
    if parts.query or parts.fragment or value.endswith("/"):
        raise ContractCompileError(
            f"{where} must be an absolute module IRI without query or fragment"
        )
    return value


class _RawParser:
    def __init__(self, profile: _Profile) -> None:
        self.profile = profile

    @staticmethod
    def _cardinality(values: object, spec: Mapping[str, Any], where: str) -> None:
        if not isinstance(values, (list, tuple, dict)):
            return
        if "min_items" in spec and len(values) < spec["min_items"]:
            raise ContractCompileError(f"{where} has too few items")
        if "max_items" in spec and len(values) > spec["max_items"]:
            raise ContractCompileError(f"{where} has too many items")

    def _value(self, node: Node, spec: Mapping[str, Any], where: str) -> object:
        operation = spec["parser"]
        if operation == "string":
            result: object = _string(node, where)
        elif operation == "nonempty_string":
            result = _string(node, where, nonempty=True)
        elif operation == "module_iri":
            result = _module_iri(node, where)
        elif operation == "boolean":
            result = _boolean(node, where)
        elif operation == "decimal":
            result = _decimal(node, where)
        elif operation == "string_list":
            if not isinstance(node, SequenceNode):
                raise ContractCompileError(f"{where} must be a sequence")
            result = tuple(
                _string(item, f"{where} item", nonempty=True) for item in node.value
            )
            if len(result) != len(set(result)):
                raise ContractCompileError(f"{where} repeats an item")
        elif operation == "items":
            if not isinstance(node, SequenceNode):
                raise ContractCompileError(f"{where} must be a sequence")
            result = tuple(
                self._shape(item, spec["item_shape"], f"{where}[{index}]")
                for index, item in enumerate(node.value)
            )
        elif operation == "named":
            result = {}
            for key, item in _mapping_items(node, where):
                if (
                    self.profile.mapping("symbol_policy")["key_parser"]
                    != "ascii_identifier"
                ):
                    raise ContractCompileError(
                        "profile symbol key parser is not executable"
                    )
                name = _identifier(key, where)
                result[name] = self._shape(item, spec["item_shape"], f"{where}.{name}")
        elif operation == "enum_values":
            result = {}
            for key, item in _mapping_items(node, where):
                if not key:
                    raise ContractCompileError(f"{where} has an empty value")
                if isinstance(item, ScalarNode) and item.tag == _YAML_NULL:
                    if item.style is not None or item.value not in {"", "null"}:
                        raise ContractCompileError(
                            f"{where}.{key} has unsupported null syntax"
                        )
                    result[key] = {}
                else:
                    result[key] = self._shape(
                        item, spec["item_shape"], f"{where}.{key}"
                    )
        else:
            raise ContractCompileError(
                f"profile parser operation {operation!r} is not executable"
            )
        self._cardinality(result, spec, where)
        if "values" in spec and result not in spec["values"]:
            raise ContractCompileError(f"{where} has an unsupported value")
        return result

    def _shape(self, node: Node, shape_name: str, where: str) -> dict[str, object]:
        shape = self.profile.shape(shape_name)
        fields = self.profile.fields(shape_name)
        values = _mapping_items(node, where)
        unknown = [name for name, _ in values if name not in fields]
        if unknown:
            raise ContractCompileError(
                f"{where} contains unsupported field {unknown[0]!r}"
            )
        result: dict[str, object] = {}
        for name, value in values:
            spec = fields[name]
            if spec["classification"] == "UNSUPPORTED":
                raise ContractCompileError(
                    f"{where} contains unsupported field {name!r}"
                )
            result[name] = self._value(value, spec, f"{where}.{name}")
        missing = [
            name
            for name, spec in fields.items()
            if spec.get("required") is True and name not in result
        ]
        if missing:
            raise ContractCompileError(
                f"{where} is missing required field {sorted(missing)[0]!r}"
            )
        if len(result) < shape.get("min_fields", 0):
            raise ContractCompileError(f"{where} has too few fields")
        if len(result) > shape.get("max_fields", float("inf")):
            raise ContractCompileError(f"{where} has too many fields")
        return result

    def parse(self, text: str) -> dict[str, object]:
        try:
            forbidden = (
                AliasToken,
                AnchorToken,
                DirectiveToken,
                DocumentEndToken,
                DocumentStartToken,
                TagToken,
            )
            for token in yaml.scan(text, Loader=yaml.SafeLoader):
                if isinstance(token, forbidden):
                    raise ContractCompileError(
                        f"source contains unsupported YAML token {type(token).__name__}"
                    )
            documents = list(yaml.compose_all(text, Loader=yaml.SafeLoader))
        except yaml.YAMLError as error:
            raise ContractCompileError(f"source is not valid YAML: {error}") from error
        if len(documents) != 1 or documents[0] is None:
            raise ContractCompileError(
                "source must contain exactly one mapping document"
            )
        return self._shape(documents[0], "schema", "schema root")


class _ContractBuilder:
    def __init__(self) -> None:
        self._declarations: dict[str, tuple[str, list[ContractProperty]]] = {}

    def declare(self, identifier: str, kind: str) -> None:
        _absolute_identifier(identifier, "neutral declaration identifier")
        _absolute_identifier(kind, "neutral declaration kind")
        if identifier in self._declarations:
            raise ContractCompileError(
                f"neutral declaration {identifier!r} is emitted more than once"
            )
        self._declarations[identifier] = (kind, [])

    def add(self, identifier: str, predicate: str, object_: FactObject) -> None:
        _absolute_identifier(predicate, "neutral property predicate")
        if identifier not in self._declarations:
            raise RuntimeError(f"property emitted before declaration {identifier!r}")
        if type(object_) not in {bool, str}:
            raise ContractCompileError(
                "neutral contract objects must be bool or string"
            )
        property_ = ContractProperty(predicate, object_)
        properties = self._declarations[identifier][1]
        if property_ in properties:
            raise ContractCompileError(
                f"duplicate property emitted for declaration {identifier!r}"
            )
        properties.append(property_)

    def finish(self) -> NeutralContract:
        declarations = []
        for identifier, (kind, properties) in self._declarations.items():
            ordered = tuple(
                sorted(
                    properties,
                    key=lambda item: _canonical_json(
                        {"object": item.object, "predicate": item.predicate}
                    ),
                )
            )
            declarations.append(ContractDeclaration(identifier, kind, ordered))
        declarations.sort(key=lambda item: item.identifier)
        return NeutralContract(tuple(declarations))


_MISSING = object()


def _resolved_term(namespace: str, value: object) -> str:
    spec = _profile_mapping(value, "validated term")
    return (
        str(spec["value"])
        if spec["form"] == "ABSOLUTE"
        else namespace + str(spec["value"])
    )


class _LinkMLAdapter:
    def __init__(self, schema: Mapping[str, object], profile: _Profile) -> None:
        self.schema = schema
        self.profile = profile
        self.namespace = str(profile.data["namespace"])
        self.builder = _ContractBuilder()
        module_field = self._identity_field("schema", "module")
        self.module = str(
            self._read(
                "schema",
                schema,
                module_field,
                purpose="identity",
                identity_role="module",
            )
        )
        self.imports: tuple[str, ...] = ()
        self.types: Mapping[str, Mapping[str, object]] = {}
        self.enums: Mapping[str, Mapping[str, object]] = {}
        self.slots: Mapping[str, Mapping[str, object]] = {}
        self.classes: Mapping[str, Mapping[str, object]] = {}
        self.local: dict[tuple[str, str], _Slot] = {}
        self.uses: dict[str, Mapping[str, tuple[_Slot, Mapping[str, object]]]] = {}
        self.slot_shape = ""
        self.scalar_shape = ""
        self.scalar_base_field = ""

    def _identity_field(self, shape: str, role: str) -> str:
        matches = [
            field
            for field, spec in self.profile.fields(shape).items()
            if spec.get("identity_role") == role
        ]
        if len(matches) != 1:
            raise ContractCompileError(
                f"profile shape {shape!r} must declare one {role!r} identity"
            )
        return matches[0]

    def _read(
        self,
        shape: str,
        source: Mapping[str, object],
        field: str,
        *,
        purpose: str = "semantic",
        identity_role: str | None = None,
        default: object = _MISSING,
    ) -> object:
        spec = self.profile.field(shape, field)
        classification = spec["classification"]
        if purpose == "identity":
            if (
                classification != "IDENTITY_ONLY"
                or spec.get("identity_role") != identity_role
            ):
                raise ContractCompileError(
                    f"profile field {shape}.{field} cannot serve identity role "
                    f"{identity_role!r}"
                )
        elif purpose == "semantic":
            if classification == "IDENTITY_ONLY":
                if "identity_role" in spec:
                    raise ContractCompileError(
                        f"identity field {shape}.{field} cannot be read as semantics"
                    )
                return default
            if classification != "ENFORCED":
                return default
        else:
            raise ContractCompileError(f"unknown profile read purpose {purpose!r}")
        if field in source:
            return source[field]
        return default

    def _collection(self, name: str) -> Mapping[str, Mapping[str, object]]:
        value = self._read("schema", self.schema, name, default={})
        if not isinstance(value, Mapping):
            raise ContractCompileError(f"parsed collection {name!r} is not a mapping")
        return value

    def _collection_shape(self, name: str) -> str:
        return str(self.profile.field("schema", name)["item_shape"])

    def _validate_imports(self, field: str) -> None:
        trusted = self.profile.data["trusted_import"]
        imports = tuple(self._read("schema", self.schema, field, default=()))
        unsupported = [reference for reference in imports if reference != trusted]
        if unsupported:
            raise ContractCompileError(
                f"bytes-only adapter cannot resolve import {unsupported[0]!r}"
            )
        self.imports = imports

    def _validate_namespaces(self, collections: list[str]) -> None:
        seen: set[str] = set()
        for name in collections:
            declarations = self._collection(name)
            overlap = seen.intersection(declarations)
            if overlap:
                raise ContractCompileError(
                    f"declaration namespace collision at {sorted(overlap)[0]!r}"
                )
            seen.update(declarations)

    def _run_validate_imports(self, operation: Mapping[str, object]) -> None:
        self._validate_imports(str(operation["field"]))

    def _run_validate_namespace(self, operation: Mapping[str, object]) -> None:
        self._validate_namespaces(list(operation["collections"]))

    def _term(self, name: str) -> str:
        return _resolved_term(self.namespace, self.profile.mapping("predicates")[name])

    def _kind(self, name: str) -> tuple[str, str]:
        spec = self.profile.mapping("kinds")[name]
        return str(spec["value"]), _resolved_term(self.namespace, spec)

    def _symbol(self, name: str) -> str:
        return self._join(self.module, name)

    def _join(self, *members: str) -> str:
        policy = self.profile.mapping("symbol_policy")
        if policy["join_operation"] != "delimiter_join":
            raise ContractCompileError(
                "profile symbol join operation is not executable"
            )
        return str(policy["separator"]).join(members)

    def _declare(self, identifier: str, shape: str) -> None:
        self._declare_kind(identifier, str(self.profile.shape(shape)["kind"]))

    def _declare_kind(self, identifier: str, kind_name: str) -> None:
        _, kind_iri = self._kind(kind_name)
        self.builder.declare(identifier, kind_iri)

    def _property(
        self, identifier: str, predicate_name: str, object_: FactObject
    ) -> None:
        self.builder.add(identifier, self._term(predicate_name), object_)

    def _builtin(self, reference: str) -> str | None:
        if self.profile.data["trusted_import"] not in self.imports:
            return None
        builtins = self.profile.mapping("builtins")
        if reference not in builtins:
            return None
        return _resolved_term(self.namespace, builtins[reference])

    def _range(self, reference: str) -> str:
        policy = self.profile.mapping("range_resolution")
        if policy["op"] != "ordered_spaces":
            raise ContractCompileError("profile range resolution is not executable")
        builtin = self._builtin(reference)
        if builtin is not None:
            return builtin
        for collection in policy["declaration_collections"]:
            if reference in self._collection(str(collection)):
                return self._symbol(reference)
        raise ContractCompileError(f"unsupported range reference {reference!r}")

    def _seed(self, reference: str) -> str:
        if reference not in self.profile.data["seed_primitives"]:
            raise ContractCompileError(
                "custom scalar must directly name one supported seed primitive"
            )
        target = self._builtin(reference)
        if target is None:
            raise ContractCompileError(
                f"seed primitive {reference!r} requires the trusted import"
            )
        return target

    def _class(self, reference: str) -> str:
        if reference not in self.classes:
            raise ContractCompileError(f"unknown class reference {reference!r}")
        return self._symbol(reference)

    def _terminal_range(self, identifier: object) -> str:
        value = str(identifier)
        prefix = self._join(self.module, "")
        if value.startswith(prefix):
            name = value.removeprefix(prefix)
            if name in self.types:
                base = self._read(
                    self.scalar_shape,
                    self.types[name],
                    self.scalar_base_field,
                )
                return self._seed(str(base))
        return value

    def _resolve(self, spec: Mapping[str, Any], value: object) -> object:
        resolver = spec.get("resolver")
        if resolver == "range":
            return self._range(str(value))
        if resolver == "seed":
            return self._seed(str(value))
        if resolver == "class":
            return self._class(str(value))
        if resolver == "mixin_list":
            return tuple(self._class(str(item)) for item in value)
        return value

    def _apply_rules(
        self,
        shape_name: str,
        authored: Mapping[str, object],
        effective: dict[str, object],
        context: str,
    ) -> None:
        for rule in self.profile.shape(shape_name).get("rules", ()):
            if rule.get("applies_to") not in {None, context}:
                continue
            if effective.get(rule["if_field"]) != rule["if_value"]:
                continue
            target = str(rule["then_field"])
            expected = rule["then_value"]
            authored_target = self._read(shape_name, authored, target, default=_MISSING)
            if (
                rule["refuse_explicit_conflict"] is True
                and authored_target is not _MISSING
                and authored_target != expected
            ):
                raise ContractCompileError(
                    f"explicit {target!r} conflicts with an active profile rule"
                )
            effective[target] = expected

    def _apply_constraints(
        self, shape_name: str, effective: Mapping[str, object]
    ) -> None:
        for constraint in self.profile.shape(shape_name).get("constraints", ()):
            operation = constraint["op"]
            if operation == "equals":
                field = str(constraint["field"])
                if effective.get(field) != constraint["value"]:
                    raise ContractCompileError(
                        f"{shape_name}.{field} is outside the active profile"
                    )
            if operation == "ordered_bounds":
                minimum = str(constraint["minimum"])
                maximum = str(constraint["maximum"])
                present = minimum in effective or maximum in effective
                allowed = {
                    self._builtin(str(name))
                    for name in constraint["allowed_builtin_ranges"]
                }
                terminal = self._terminal_range(effective[str(constraint["range"])])
                if present and terminal not in allowed:
                    raise ContractCompileError(
                        "numeric bounds require a supported numeric range"
                    )
                if (
                    minimum in effective
                    and maximum in effective
                    and Decimal(str(effective[minimum]))
                    > Decimal(str(effective[maximum]))
                ):
                    raise ContractCompileError("minimum value exceeds maximum value")

    def _effective(
        self,
        shape_name: str,
        authored: Mapping[str, object],
        *,
        context: str,
    ) -> dict[str, object]:
        effective: dict[str, object] = {}
        for field, spec in self.profile.fields(shape_name).items():
            if spec["classification"] != "ENFORCED" or "predicate" not in spec:
                continue
            value = self._read(shape_name, authored, field, default=_MISSING)
            if value is _MISSING and "schema_default" in spec:
                value = self._read(
                    "schema",
                    self.schema,
                    str(spec["schema_default"]),
                    default=_MISSING,
                )
            if value is _MISSING and "default" in spec:
                value = self.profile.default(str(spec["default"]))
            if value is _MISSING:
                continue
            effective[field] = self._resolve(spec, value)
        self._apply_rules(shape_name, authored, effective, context)
        self._apply_constraints(shape_name, effective)
        return effective

    def _emit_effective(
        self, identifier: str, shape_name: str, effective: Mapping[str, object]
    ) -> None:
        for field, value in effective.items():
            spec = self.profile.field(shape_name, field)
            if spec["classification"] != "ENFORCED":
                raise ContractCompileError(
                    f"non-enforced field {shape_name}.{field} reached fact emission"
                )
            predicate = str(spec["predicate"])
            if isinstance(value, tuple):
                for item in value:
                    if type(item) is not str:
                        raise ContractCompileError(
                            f"field {shape_name}.{field} emitted a non-string sequence"
                        )
                    self._property(identifier, predicate, item)
            else:
                if type(value) not in {bool, str}:
                    raise ContractCompileError(
                        f"field {shape_name}.{field} emitted a non-scalar value"
                    )
                self._property(identifier, predicate, value)

    def _slot(self, name: str) -> _Slot:
        if name not in self.slots:
            raise ContractCompileError(f"unknown slot reference {name!r}")
        return _Slot(name, self._symbol(name), self.slots[name], self.slot_shape)

    def _validate_class_edges(self, operation: Mapping[str, object]) -> None:
        shape = str(operation["shape"])
        parent_field = str(operation["parent_field"])
        mixins_field = str(operation["mixins_field"])
        mixin_field = str(operation["mixin_field"])
        for body in self.classes.values():
            parent_value = self._read(shape, body, parent_field, default=_MISSING)
            if parent_value is not _MISSING:
                parent_name = str(parent_value)
                self._class(parent_name)
                parent = self.classes[parent_name]
                for field in operation["parent_semantic_fields"]:
                    if (
                        self._read(shape, parent, str(field), default=_MISSING)
                        is not _MISSING
                    ):
                        raise ContractCompileError(
                            "semantic parent is outside the active profile"
                        )
            mixins = self._read(shape, body, mixins_field, default=())
            for mixin_name in mixins:
                self._class(str(mixin_name))
                mixin = self.classes[str(mixin_name)]
                mixin_semantics = self._effective(shape, mixin, context="declaration")
                if mixin_semantics[mixin_field] is not True:
                    raise ContractCompileError(
                        "mixin reference does not target a mixin"
                    )
                for field in operation["derived_mixin_forbidden_fields"]:
                    if (
                        self._read(shape, mixin, str(field), default=_MISSING)
                        is not _MISSING
                    ):
                        raise ContractCompileError(
                            "derived or semantic mixin is outside the active profile"
                        )

    def _emit_types(self, operation: Mapping[str, object]) -> None:
        collection = str(operation["collection"])
        shape = str(operation["shape"])
        base_field = str(operation["base_field"])
        self.types = self._collection(collection)
        self.scalar_shape = shape
        self.scalar_base_field = base_field
        spec = self.profile.field(shape, base_field)
        for name in sorted(self.types):
            identifier = self._symbol(name)
            self._declare(identifier, shape)
            source = self._read(shape, self.types[name], base_field)
            target = self._resolve(spec, source)
            self._property(identifier, str(spec["predicate"]), str(target))

    def _emit_enums(self, operation: Mapping[str, object]) -> None:
        collection = str(operation["collection"])
        shape = str(operation["shape"])
        values_field = str(operation["values_field"])
        self.enums = self._collection(collection)
        spec = self.profile.field(shape, values_field)
        for name in sorted(self.enums):
            identifier = self._symbol(name)
            self._declare(identifier, shape)
            values = self._read(shape, self.enums[name], values_field, default={})
            for value in sorted(values):
                self._property(identifier, str(spec["predicate"]), value)

    def _emit_slots(self, operation: Mapping[str, object]) -> None:
        slot_shape = str(operation["slot_shape"])
        attribute_shape = str(operation["attribute_shape"])
        attribute_field = str(operation["attribute_field"])
        slots_collection = str(operation["slots_collection"])
        classes_collection = str(operation["classes_collection"])
        class_shape = self._collection_shape(classes_collection)
        self.slots = self._collection(slots_collection)
        self.slot_shape = slot_shape
        self.classes = self._collection(classes_collection)
        for name in sorted(self.slots):
            slot = self._slot(name)
            self._declare(slot.identifier, slot.shape)
            effective = self._effective(
                slot.shape, slot.authored, context="declaration"
            )
            self._emit_effective(slot.identifier, slot.shape, effective)
        for class_name, body in self.classes.items():
            attributes = self._read(class_shape, body, attribute_field, default={})
            for name, authored in attributes.items():
                identifier = self._join(self._symbol(class_name), name)
                slot = _Slot(name, identifier, authored, attribute_shape)
                self.local[(class_name, name)] = slot
                self._declare(identifier, slot.shape)
                effective = self._effective(
                    slot.shape, slot.authored, context="declaration"
                )
                self._emit_effective(identifier, slot.shape, effective)

    def _emit_classes(self, operation: Mapping[str, object]) -> None:
        shape = str(operation["shape"])
        self.classes = self._collection(str(operation["collection"]))
        self._validate_class_edges(operation)
        for name in sorted(self.classes):
            identifier = self._symbol(name)
            self._declare(identifier, shape)
            effective = self._effective(
                shape, self.classes[name], context="declaration"
            )
            self._emit_effective(identifier, shape, effective)

    def _structural(self, name: str, role_values: Mapping[str, object]) -> str:
        profile = self.profile.mapping("structural_identities")[name]
        roles = profile["member_roles"]
        supplied = {**role_values, "domain": profile["domain"]}
        if set(supplied) != set(roles):
            raise RuntimeError(f"wrong structural roles for {name}")
        members = {roles[role]: value for role, value in supplied.items()}
        return str(profile["prefix"]) + sha256(_canonical_json(members)).hexdigest()

    def _slot_use_id(self, class_id: str, slot: _Slot) -> str:
        identity_name = str(self.profile.shape(slot.shape)["use_identity"])
        return self._structural(
            identity_name,
            {
                "class": class_id,
                "slot": slot.identifier,
            },
        )

    def _emit_uses(self, operation: Mapping[str, object]) -> None:
        classes_collection = str(operation["classes_collection"])
        slots_field = str(operation["slots_field"])
        attributes_field = str(operation["attributes_field"])
        kind = str(operation["kind"])
        class_shape = self._collection_shape(classes_collection)
        self.classes = self._collection(classes_collection)
        result: dict[str, Mapping[str, tuple[_Slot, Mapping[str, object]]]] = {}
        for class_name in sorted(self.classes):
            body = self.classes[class_name]
            uses: dict[str, tuple[_Slot, Mapping[str, object]]] = {}
            slots = self._read(class_shape, body, slots_field, default=())
            for name in slots:
                slot = self._slot(str(name))
                uses[slot.name] = (
                    slot,
                    self._effective(slot.shape, slot.authored, context="slot_use"),
                )
            attributes = self._read(class_shape, body, attributes_field, default={})
            for name in attributes:
                slot = self.local[(class_name, name)]
                if name in uses:
                    raise ContractCompileError(
                        f"class {class_name!r} has an ambiguous slot {name!r}"
                    )
                uses[name] = (
                    slot,
                    self._effective(slot.shape, slot.authored, context="slot_use"),
                )
            result[class_name] = uses
            class_id = self._symbol(class_name)
            for slot, effective in uses.values():
                identifier = self._slot_use_id(class_id, slot)
                self._declare_kind(identifier, kind)
                self._property(
                    identifier, str(operation["on_class_predicate"]), class_id
                )
                self._property(
                    identifier,
                    str(operation["uses_slot_predicate"]),
                    slot.identifier,
                )
                self._emit_effective(identifier, slot.shape, effective)
        self.uses = result

    def _condition_slot(
        self,
        reference: str,
        uses: Mapping[str, tuple[_Slot, Mapping[str, object]]],
    ) -> tuple[_Slot, Mapping[str, object]]:
        if reference not in uses:
            raise ContractCompileError(
                f"condition references non-applicable slot {reference!r}"
            )
        return uses[reference]

    def _validate_condition_range(
        self,
        condition: Mapping[str, object],
        slot: Mapping[str, object],
        operation: Mapping[str, object],
    ) -> None:
        if str(operation["condition_value_field"]) not in condition:
            return
        string_range = self._builtin(str(operation["string_builtin"]))
        enum_ranges = {
            self._symbol(name)
            for name in self._collection(str(operation["enum_collection"]))
        }
        range_value = slot[str(operation["range_field"])]
        if range_value != string_range and range_value not in enum_ranges:
            raise ContractCompileError(
                "equals_string condition requires a string or enum range"
            )

    def _emit_expressions(self, operation: Mapping[str, object]) -> None:
        classes_collection = str(operation["classes_collection"])
        alternatives_field = str(operation["alternatives_field"])
        conditions_field = str(operation["conditions_field"])
        condition_shape = str(operation["condition_shape"])
        class_shape = self._collection_shape(classes_collection)
        alternative_shape = str(
            self.profile.field(class_shape, alternatives_field)["item_shape"]
        )
        self.classes = self._collection(classes_collection)
        for class_name, body in self.classes.items():
            alternatives = self._read(class_shape, body, alternatives_field, default=())
            if not alternatives:
                continue
            prepared: list[tuple[str, str, Mapping[str, object]]] = []
            for alternative in alternatives:
                conditions = self._read(
                    alternative_shape, alternative, conditions_field
                )
                reference, condition = next(iter(conditions.items()))
                slot, slot_effective = self._condition_slot(
                    reference, self.uses[class_name]
                )
                condition_effective = self._effective(
                    condition_shape, condition, context="condition"
                )
                self._validate_condition_range(
                    condition_effective, slot_effective, operation
                )
                semantic = {str(operation["condition_slot_member"]): slot.identifier}
                for field, value in condition_effective.items():
                    semantic[
                        str(self.profile.field(condition_shape, field)["member"])
                    ] = value
                semantic_name = str(operation["semantic_identity"])
                digest = self._structural(
                    semantic_name,
                    {
                        "conditions": [semantic],
                    },
                )
                prepared.append((digest, slot.identifier, condition_effective))
            digests = [digest for digest, _, _ in prepared]
            if len(digests) != len(set(digests)):
                raise ContractCompileError("exactly_one_of repeats an alternative")
            class_id = self._symbol(class_name)
            group_name = str(operation["group_identity"])
            group_id = self._structural(
                group_name,
                {
                    "alternative_semantic_digests": sorted(digests),
                    "class": class_id,
                },
            )
            self._declare_kind(group_id, str(operation["group_kind"]))
            self._property(
                group_id, str(operation["group_on_class_predicate"]), class_id
            )
            for digest, slot_id, condition in prepared:
                alternative_name = str(operation["alternative_identity"])
                alternative_id = self._structural(
                    alternative_name,
                    {
                        "alternative_semantic_digest": digest,
                        "group": group_id,
                    },
                )
                self._declare_kind(alternative_id, str(operation["alternative_kind"]))
                self._property(
                    alternative_id,
                    str(operation["alternative_in_group_predicate"]),
                    group_id,
                )
                condition_name = str(operation["condition_identity"])
                condition_id = self._structural(
                    condition_name,
                    {
                        "alternative": alternative_id,
                        "slot": slot_id,
                    },
                )
                self._declare(condition_id, condition_shape)
                self._property(
                    condition_id,
                    str(operation["condition_in_alternative_predicate"]),
                    alternative_id,
                )
                self._property(
                    condition_id,
                    str(operation["condition_uses_slot_predicate"]),
                    slot_id,
                )
                self._emit_effective(condition_id, condition_shape, condition)

    def adapt(self) -> NeutralContract:
        handlers = {
            "validate_imports": self._run_validate_imports,
            "validate_shared_namespace": self._run_validate_namespace,
            "declare_direct_seed_scalars": self._emit_types,
            "declare_enums": self._emit_enums,
            "declare_slots": self._emit_slots,
            "declare_shallow_classes": self._emit_classes,
            "lower_slot_uses": self._emit_uses,
            "lower_flat_exactly_one": self._emit_expressions,
        }
        for operation in self.profile.data["lowering_plan"]:
            handlers[str(operation["op"])](operation)
        return self.builder.finish()


def _encode_facts(
    contract: NeutralContract, profile: _Profile
) -> tuple[ContractFact, ...]:
    namespace = str(profile.data["namespace"])
    semantic_resources = {
        _resolved_term(namespace, term)
        for registry_name in ("builtins", "kinds", "predicates")
        for term in profile.mapping(registry_name).values()
    }
    aliases = sorted(
        declaration.identifier
        for declaration in contract.declarations
        if declaration.identifier in semantic_resources
    )
    if aliases:
        raise ContractCompileError(
            f"neutral declaration identifier aliases semantic resource {aliases[0]!r}"
        )
    type_predicate = _resolved_term(namespace, profile.mapping("predicates")["type"])
    facts: list[ContractFact] = []
    seen: set[ContractFact] = set()
    for declaration in contract.declarations:
        emitted = [
            ContractFact(declaration.identifier, type_predicate, declaration.kind)
        ]
        emitted.extend(
            ContractFact(declaration.identifier, property_.predicate, property_.object)
            for property_ in declaration.properties
        )
        for fact in emitted:
            if fact in seen:
                raise ContractCompileError("neutral contract emits a duplicate fact")
            seen.add(fact)
            facts.append(fact)
    return tuple(sorted(facts, key=lambda fact: _canonical_json(fact.as_dict())))


def _decode_source(source: bytes) -> str:
    if not isinstance(source, bytes):
        raise TypeError("source must be bytes")
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ContractCompileError("source is not valid UTF-8") from error
    if text.startswith("\ufeff"):
        raise ContractCompileError("source must not contain a byte-order mark")
    return text


def _validate_versions(profile: _Profile) -> None:
    expected = {
        "linkml": profile.data["linkml_version"],
        "linkml-runtime": profile.data["linkml_runtime_version"],
    }
    for distribution, required in expected.items():
        try:
            installed = version(distribution)
        except PackageNotFoundError as error:
            raise ContractCompileError(
                f"required adapter distribution {distribution!r} is absent"
            ) from error
        if installed != required:
            raise ContractCompileError(
                f"{distribution} must be exactly {required}, found {installed}"
            )


def _validate_linkml(text: str, profile: _Profile) -> None:
    try:
        yaml_loader.loads(text, target_class=SchemaDefinition)
    except Exception as error:
        required = profile.data["linkml_runtime_version"]
        raise ContractCompileError(
            f"LinkML Runtime {required} rejected the source: {error}"
        ) from error


def compile_linkml_contract(
    source: bytes,
    *,
    locator: str,
    profile: Mapping[str, object] | None = None,
) -> ContractCompilation:
    """Adapt exact LinkML bytes into declarations, then encode neutral facts."""

    if not isinstance(locator, str) or not locator:
        raise TypeError("locator must be a nonempty string")
    active = _load_profile(profile)
    text = _decode_source(source)
    try:
        schema = _RawParser(active).parse(text)
        _validate_versions(active)
        _validate_linkml(text, active)
        contract = _LinkMLAdapter(schema, active).adapt()
        facts = _encode_facts(contract, active)
        canonical = _canonical_json([fact.as_dict() for fact in facts])
    except ContractCompileError:
        raise
    except (KeyError, RuntimeError, TypeError, ValueError) as error:
        raise ContractCompileError(
            f"profile execution refused malformed state: {error}"
        ) from error
    return ContractCompilation(
        contract=contract,
        facts=facts,
        canonical_facts=canonical,
        facts_sha256=sha256(canonical).hexdigest(),
        source=SourceAttestation(
            locator=locator,
            byte_length=len(source),
            sha256=sha256(source).hexdigest(),
        ),
        implementation=CompilerImplementation(
            adapter=str(active.data["adapter"]),
            linkml_version=str(active.data["linkml_version"]),
            linkml_runtime_version=str(active.data["linkml_runtime_version"]),
            support_profile=str(active.data["support_profile"]),
            profile_sha256=active.digest,
            executor_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        ),
    )

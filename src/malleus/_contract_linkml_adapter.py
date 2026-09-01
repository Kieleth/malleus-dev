"""Private LinkML retained-source parser and declaration adapter."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum, auto
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, TypeAlias
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

from ._contract_source import (
    CollaboratorRefusal,
    ModuleObservation,
    ResolvedImportEdge,
    ResolverSelection,
    RetainedSource,
    RootResolution,
    SourceClosure,
)


class LinkMLRefusalReason(Enum):
    """Closed failure classes for the private adapter boundary."""

    INVALID_PROFILE = auto()
    MALFORMED_OBSERVATION = auto()
    MALFORMED_SOURCE = auto()
    REJECTED_SOURCE = auto()
    LINKML_RUNTIME_REJECTED = auto()
    OBSERVATION_IMPORT_MISMATCH = auto()
    CLOSURE_IMPORT_MISMATCH = auto()
    TRUSTED_MODULE_MISMATCH = auto()


class LinkMLAdapterRefusal(ValueError):
    """One typed atomic refusal with no partial adapter result."""

    def __init__(
        self,
        reason: LinkMLRefusalReason,
        detail: str,
        *,
        module_id: str | None = None,
        path: tuple[str | int, ...] = (),
    ) -> None:
        self.reason = reason
        self.module_id = module_id
        self.path = path
        super().__init__(f"{reason.name}: {detail}")


@dataclass(frozen=True, slots=True)
class AuthoredScalar:
    """One scalar with both its source lexeme and parsed value."""

    kind: str
    lexeme: str
    value: bool | str | None


@dataclass(frozen=True, slots=True)
class AuthoredSequenceItem:
    """One zero-based authored sequence member."""

    ordinal: int
    value: AuthoredValue


@dataclass(frozen=True, slots=True)
class AuthoredSequence:
    """An authored sequence whose order and repetitions are retained."""

    items: tuple[AuthoredSequenceItem, ...]


@dataclass(frozen=True, slots=True)
class AuthoredField:
    """One structured mapping member backed by the exact retained source bytes."""

    name: str
    ordinal: int
    classification: str
    value: AuthoredValue
    value_classification: str | None = None


@dataclass(frozen=True, slots=True)
class AuthoredMapping:
    """Structured authored mapping evidence in exact member order."""

    fields: tuple[AuthoredField, ...]


AuthoredValue: TypeAlias = AuthoredScalar | AuthoredSequence | AuthoredMapping


@dataclass(frozen=True, slots=True)
class ClassifiedOccurrence:
    """One present source location under the selected support profile."""

    path: tuple[str | int, ...]
    ordinal_path: tuple[int, ...]
    classification: str
    value: AuthoredValue
    value_classification: str | None = None


@dataclass(frozen=True, slots=True)
class DeclaredDeclaration:
    """One module-local declaration before binding or elaboration."""

    name: str
    identifier: str
    kind: str
    ordinal: int
    path: tuple[str, ...]
    body: AuthoredMapping


@dataclass(frozen=True, slots=True)
class DeclaredModule:
    """Lossless authored evidence for one retained module."""

    module_id: str
    schema_id: str
    source: RetainedSource
    authored_imports: tuple[str, ...]
    root: AuthoredMapping
    declarations: tuple[DeclaredDeclaration, ...]
    occurrences: tuple[ClassifiedOccurrence, ...]
    trusted: bool
    support_profile: str
    profile_sha256: str


@dataclass(frozen=True, slots=True)
class DeclaredContractClosure:
    """Complete declared evidence for one exact retained source closure."""

    source_closure: SourceClosure
    modules: tuple[DeclaredModule, ...]


@dataclass(frozen=True, slots=True)
class _ParsedDocument:
    plain: Mapping[str, object]
    root: AuthoredMapping
    occurrences: tuple[ClassifiedOccurrence, ...]


@dataclass(frozen=True, slots=True)
class _AdapterProfile:
    data: Mapping[str, Any]
    digest: str


_PROFILE_PATH = Path(__file__).with_name("_contract_compiler_profile.json")
_YAML_STRING = "tag:yaml.org,2002:str"
_YAML_BOOLEAN = "tag:yaml.org,2002:bool"
_YAML_NULL = "tag:yaml.org,2002:null"
_CLASSIFICATIONS = {
    "ANNOTATION_ONLY",
    "ENFORCED",
    "IDENTITY_ONLY",
    "REJECTED",
}
_PARSERS = {
    "adoption_annotations",
    "boolean",
    "decimal",
    "enum_values",
    "items",
    "mapping",
    "module_iri",
    "named",
    "nonempty_string",
    "prefixes",
    "string",
    "string_list",
}
_KEY_PARSERS = {"ascii_identifier", "nonempty_string", "reference"}
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
    "source_ordering",
    "structural_identities",
    "support_profile",
    "symbol_policy",
    "trusted_import",
    "trusted_module",
}
_SHAPE_NAMES = {
    "adoption_annotations",
    "alternative",
    "attribute",
    "class",
    "condition",
    "enum",
    "permissible_value",
    "schema",
    "slot",
    "slot_usage",
    "type",
}
_SHAPE_KEYS = {
    "bootstrap",
    "constraints",
    "declaration_kind",
    "fields",
    "kind",
    "label",
    "max_fields",
    "min_fields",
    "rules",
    "use_identity",
}
_FIELD_KEYS = {
    "bootstrap",
    "bootstrap_max_items",
    "classification",
    "default",
    "identity_role",
    "item_classification",
    "item_shape",
    "key_classification",
    "key_parser",
    "max_items",
    "member",
    "min_items",
    "parser",
    "predicate",
    "required",
    "resolver",
    "schema_default",
    "value_classification",
    "values",
}
_ADAPTER_SHAPE_POLICY_KEYS = {"declaration_kind", "max_fields", "min_fields"}
_ADAPTER_FIELD_POLICY_KEYS = {
    "classification",
    "item_classification",
    "item_shape",
    "key_classification",
    "key_parser",
    "max_items",
    "min_items",
    "parser",
    "required",
    "value_classification",
    "values",
}


def _refusal(
    reason: LinkMLRefusalReason,
    detail: str,
    *,
    module_id: str | None = None,
    path: tuple[str | int, ...] = (),
) -> LinkMLAdapterRefusal:
    return LinkMLAdapterRefusal(reason, detail, module_id=module_id, path=path)


def _profile_mapping(value: object, where: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            f"profile {where} must be a mapping",
        )
    return value


def _profile_string(value: object, where: str) -> str:
    if not isinstance(value, str) or not value:
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            f"profile {where} must be a nonempty string",
        )
    return value


def _plain_profile(value: object) -> object:
    if isinstance(value, Mapping):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("profile mapping keys must be strings")
        return {key: _plain_profile(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_plain_profile(item) for item in value]
    if isinstance(value, tuple):
        raise TypeError("profile sequences must be lists")
    return value


def _exact_profile_keys(
    value: Mapping[str, Any], expected: set[str], where: str
) -> None:
    if set(value) != expected:
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            f"profile {where} is not closed",
        )


def _validate_term(spec: object, where: str) -> None:
    term = _profile_mapping(spec, where)
    _exact_profile_keys(term, {"form", "value"}, where)
    if term["form"] not in {"ABSOLUTE", "LOCAL"}:
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            f"profile {where} has an unsupported term form",
        )
    _profile_string(term["value"], f"{where}.value")


def _validate_adapter_profile(
    root: Mapping[str, Any], authority: Mapping[str, Any]
) -> None:
    _exact_profile_keys(root, _ROOT_KEYS, "root")
    _exact_profile_keys(authority, _ROOT_KEYS, "packaged root")
    if root["schema"] != "malleus.contract-compiler.linkml-profile/v0":
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            "profile schema is not supported",
        )
    if root["adapter"] != "linkml":
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            "profile adapter is not supported",
        )
    if root["linkml_version"] != "1.11.1" or root["linkml_runtime_version"] != "1.11.1":
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            "profile LinkML versions are not supported",
        )
    if authority["support_profile"] != "malleus.linkml/private-v0":
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            "packaged adapter profile identity is not supported",
        )
    for member in (
        "support_profile",
        "namespace",
        "trusted_import",
        "trusted_module",
        "builtins",
        "seed_primitives",
    ):
        if root[member] != authority[member]:
            raise _refusal(
                LinkMLRefusalReason.INVALID_PROFILE,
                f"profile {member} differs from the private adapter authority",
            )
    ordering = _profile_mapping(root["source_ordering"], "source_ordering")
    if ordering != {
        "field_order": "PRESERVE_AUTHORED",
        "module_order": "PRESERVE_SOURCE_CLOSURE",
        "ordinal_base": 0,
    }:
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            "profile source ordering is not executable",
        )
    trusted = _profile_mapping(root["trusted_module"], "trusted_module")
    _exact_profile_keys(
        trusted,
        {"byte_length", "module_id", "schema_id", "sha256"},
        "trusted_module",
    )
    if (
        type(trusted["byte_length"]) is not int
        or trusted["byte_length"] < 0
        or trusted["module_id"] != root["trusted_import"]
    ):
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            "profile trusted module identity is invalid",
        )
    for member in ("module_id", "schema_id", "sha256"):
        _profile_string(trusted[member], f"trusted_module.{member}")
    digest = str(trusted["sha256"])
    if (
        not digest.startswith("sha256:")
        or len(digest) != 71
        or any(character not in "0123456789abcdef" for character in digest[7:])
    ):
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            "profile trusted module digest is invalid",
        )
    namespace = _profile_string(root["namespace"], "namespace")
    _absolute_iri(namespace, "profile namespace")
    if not namespace.endswith("/"):
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            "profile namespace is not an absolute IRI base",
        )
    builtins = _profile_mapping(root["builtins"], "builtins")
    seeds = root["seed_primitives"]
    if (
        not isinstance(seeds, list)
        or any(type(seed) is not str or not seed for seed in seeds)
        or len(seeds) != len(set(seeds))
        or set(builtins) != set(seeds)
    ):
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            "profile trusted builtin order differs from its map",
        )
    for name, term in builtins.items():
        _profile_string(name, "builtins key")
        _validate_term(term, f"builtins.{name}")
    shapes = _profile_mapping(root["node_shapes"], "node_shapes")
    authority_shapes = _profile_mapping(authority["node_shapes"], "node_shapes")
    _exact_profile_keys(shapes, _SHAPE_NAMES, "node_shapes")
    _exact_profile_keys(authority_shapes, _SHAPE_NAMES, "packaged node_shapes")
    for shape_name in _SHAPE_NAMES:
        shape = _profile_mapping(shapes[shape_name], f"node_shapes.{shape_name}")
        authority_shape = _profile_mapping(
            authority_shapes[shape_name], f"packaged node_shapes.{shape_name}"
        )
        if not {"fields", "label"}.issubset(shape) or not set(shape).issubset(
            _SHAPE_KEYS
        ):
            raise _refusal(
                LinkMLRefusalReason.INVALID_PROFILE,
                f"profile shape {shape_name} is not closed",
            )
        for member in _ADAPTER_SHAPE_POLICY_KEYS:
            if (member in shape) != (member in authority_shape) or shape.get(
                member
            ) != authority_shape.get(member):
                raise _refusal(
                    LinkMLRefusalReason.INVALID_PROFILE,
                    f"profile shape {shape_name} changes adapter policy {member}",
                )
        _profile_string(shape["label"], f"node_shapes.{shape_name}.label")
        fields = _profile_mapping(shape["fields"], f"node_shapes.{shape_name}.fields")
        authority_fields = _profile_mapping(
            authority_shape["fields"], f"packaged node_shapes.{shape_name}.fields"
        )
        if set(fields) != set(authority_fields):
            raise _refusal(
                LinkMLRefusalReason.INVALID_PROFILE,
                f"profile shape {shape_name} changes the private grammar",
            )
        for field_name, raw_field in fields.items():
            field = _profile_mapping(
                raw_field, f"node_shapes.{shape_name}.fields.{field_name}"
            )
            if not set(field).issubset(_FIELD_KEYS):
                raise _refusal(
                    LinkMLRefusalReason.INVALID_PROFILE,
                    f"profile field {shape_name}.{field_name} is not closed",
                )
            authority_field = _profile_mapping(
                authority_fields[field_name],
                f"packaged node_shapes.{shape_name}.fields.{field_name}",
            )
            for member in _ADAPTER_FIELD_POLICY_KEYS:
                if (member in field) != (member in authority_field) or field.get(
                    member
                ) != authority_field.get(member):
                    raise _refusal(
                        LinkMLRefusalReason.INVALID_PROFILE,
                        f"profile field {shape_name}.{field_name} changes adapter "
                        f"policy {member}",
                    )
            classification = field.get("classification")
            parser = field.get("parser")
            if classification not in _CLASSIFICATIONS or parser not in _PARSERS:
                raise _refusal(
                    LinkMLRefusalReason.INVALID_PROFILE,
                    f"profile field {shape_name}.{field_name} is not executable",
                )
            item_shape = field.get("item_shape")
            if item_shape is not None and item_shape not in shapes:
                raise _refusal(
                    LinkMLRefusalReason.INVALID_PROFILE,
                    f"profile field {shape_name}.{field_name} has unknown shape",
                )
            for member in (
                "item_classification",
                "key_classification",
                "value_classification",
            ):
                if member in field and field[member] not in _CLASSIFICATIONS - {
                    "REJECTED"
                }:
                    raise _refusal(
                        LinkMLRefusalReason.INVALID_PROFILE,
                        f"profile field {shape_name}.{field_name} has invalid {member}",
                    )
            if "value_classification" in field and parser not in {
                "module_iri",
                "nonempty_string",
                "prefixes",
                "string",
            }:
                raise _refusal(
                    LinkMLRefusalReason.INVALID_PROFILE,
                    f"profile field {shape_name}.{field_name} has unread value "
                    "classification",
                )
            if (
                parser in {"items", "string_list"}
                and "item_classification" not in field
            ):
                raise _refusal(
                    LinkMLRefusalReason.INVALID_PROFILE,
                    f"profile field {shape_name}.{field_name} lacks item classification",
                )
            if parser in {"adoption_annotations", "enum_values", "items", "named"} and (
                "item_shape" not in field
            ):
                raise _refusal(
                    LinkMLRefusalReason.INVALID_PROFILE,
                    f"profile field {shape_name}.{field_name} lacks item shape",
                )
            if parser == "mapping" and classification != "REJECTED":
                raise _refusal(
                    LinkMLRefusalReason.INVALID_PROFILE,
                    f"profile field {shape_name}.{field_name} exposes raw mapping",
                )
            if parser in {"enum_values", "named", "prefixes"}:
                if (
                    "key_classification" not in field
                    or field.get("key_parser") not in _KEY_PARSERS
                ):
                    raise _refusal(
                        LinkMLRefusalReason.INVALID_PROFILE,
                        f"profile field {shape_name}.{field_name} lacks key policy",
                    )
            elif "key_parser" in field:
                raise _refusal(
                    LinkMLRefusalReason.INVALID_PROFILE,
                    f"profile field {shape_name}.{field_name} has unread key parser",
                )


def _load_adapter_profile(
    injected: Mapping[str, object] | _AdapterProfile | None,
) -> _AdapterProfile:
    if isinstance(injected, _AdapterProfile):
        return injected
    try:
        authority_raw = _PROFILE_PATH.read_bytes()
        authority = _profile_mapping(json.loads(authority_raw), "packaged root")
        if injected is None:
            raw = authority_raw
            data = authority
        else:
            raw = json.dumps(
                _plain_profile(injected),
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            data = _profile_mapping(json.loads(raw), "root")
        _validate_adapter_profile(data, authority)
    except LinkMLAdapterRefusal:
        raise
    except (KeyError, OSError, RuntimeError, TypeError, ValueError) as error:
        raise _refusal(
            LinkMLRefusalReason.INVALID_PROFILE,
            f"profile validation refused malformed state: {error}",
        ) from error
    return _AdapterProfile(data, sha256(raw).hexdigest())


def _absolute_iri(value: str, where: str) -> str:
    if any(
        character.isspace() or category(character) in {"Cc", "Cs"}
        for character in value
    ):
        raise ValueError(f"{where} contains a forbidden code point")
    parts = urlsplit(value)
    if (
        not parts.scheme
        or not parts.scheme[0].isalpha()
        or not all(
            character.isalnum() or character in {"+", "-", "."}
            for character in parts.scheme
        )
    ):
        raise ValueError(f"{where} must be an absolute IRI")
    return value


def _ascii_identifier(value: str, where: str) -> str:
    valid_start = value and (value[0] == "_" or value[0].isalpha())
    valid_rest = all(character == "_" or character.isalnum() for character in value)
    if not valid_start or not valid_rest or not value.isascii():
        raise ValueError(f"{where} is not an ASCII identifier")
    return value


def _reference(value: str, where: str) -> str:
    prefix, separator, local = value.partition(":")
    if separator:
        _ascii_identifier(prefix, where)
        _ascii_identifier(local, where)
    else:
        _ascii_identifier(value, where)
    return value


def _decimal_lexeme(text: str, where: str) -> str:
    index = 1 if text.startswith("-") else 0
    if index >= len(text):
        raise ValueError(f"{where} has an invalid numeric lexeme")
    if text[index] == "0":
        index += 1
        if index < len(text) and text[index].isdigit():
            raise ValueError(f"{where} has a leading zero")
    elif "1" <= text[index] <= "9":
        while index < len(text) and text[index].isdigit():
            index += 1
    else:
        raise ValueError(f"{where} has an invalid integer part")
    if index < len(text) and text[index] == ".":
        index += 1
        start = index
        while index < len(text) and text[index].isdigit():
            index += 1
        if index == start:
            raise ValueError(f"{where} has an empty fraction")
    if index < len(text) and text[index] in {"e", "E"}:
        index += 1
        if index < len(text) and text[index] in {"+", "-"}:
            index += 1
        start = index
        while index < len(text) and text[index].isdigit():
            index += 1
        if index == start:
            raise ValueError(f"{where} has an empty exponent")
    if index != len(text):
        raise ValueError(f"{where} has an invalid numeric lexeme")
    try:
        value = Decimal(text)
    except InvalidOperation as error:
        raise ValueError(f"{where} is not a finite decimal") from error
    if not value.is_finite():
        raise ValueError(f"{where} is not a finite decimal")
    return text


class _RawParser:
    def __init__(
        self,
        *,
        text: str,
        module_id: str,
        profile: Mapping[str, Any],
    ) -> None:
        self.text = text
        self.module_id = module_id
        self.profile = profile
        self.occurrences: list[ClassifiedOccurrence] = []

    def _raw(self, node: Node) -> str:
        return self.text[node.start_mark.index : node.end_mark.index]

    def _mapping_items(self, node: Node, where: str) -> list[tuple[str, Node, int]]:
        if not isinstance(node, MappingNode):
            raise ValueError(f"{where} must be a mapping")
        result: list[tuple[str, Node, int]] = []
        seen: set[str] = set()
        for ordinal, (key_node, value_node) in enumerate(node.value):
            if not isinstance(key_node, ScalarNode) or key_node.tag != _YAML_STRING:
                raise ValueError(f"{where} has a non-string mapping key")
            key = key_node.value
            if key == "<<":
                raise ValueError(f"{where} contains a YAML merge key")
            if key in seen:
                raise ValueError(f"{where} repeats field {key!r}")
            seen.add(key)
            result.append((key, value_node, ordinal))
        return result

    def _scalar_string(
        self, node: Node, where: str, *, nonempty: bool = False
    ) -> tuple[str, AuthoredScalar]:
        if not isinstance(node, ScalarNode) or node.tag != _YAML_STRING:
            raise ValueError(f"{where} must be a string")
        if nonempty and not node.value:
            raise ValueError(f"{where} must be a nonempty string")
        return node.value, AuthoredScalar("STRING", self._raw(node), node.value)

    def _scalar_boolean(self, node: Node, where: str) -> tuple[bool, AuthoredScalar]:
        if (
            not isinstance(node, ScalarNode)
            or node.style is not None
            or node.tag != _YAML_BOOLEAN
            or node.value not in {"true", "false"}
        ):
            raise ValueError(f"{where} must be raw lowercase true or false")
        value = node.value == "true"
        return value, AuthoredScalar("BOOLEAN", node.value, value)

    def _scalar_decimal(self, node: Node, where: str) -> tuple[str, AuthoredScalar]:
        if not isinstance(node, ScalarNode) or node.style is not None:
            raise ValueError(f"{where} must be an unquoted JSON number")
        lexeme = self._raw(node)
        value = _decimal_lexeme(lexeme, where)
        return value, AuthoredScalar("NUMBER", lexeme, value)

    def _record(
        self,
        path: tuple[str | int, ...],
        ordinal_path: tuple[int, ...],
        classification: str,
        value: AuthoredValue,
        value_classification: str | None = None,
    ) -> None:
        self.occurrences.append(
            ClassifiedOccurrence(
                path,
                ordinal_path,
                classification,
                value,
                value_classification,
            )
        )

    def _shape_spec(self, name: str) -> Mapping[str, Any]:
        return _profile_mapping(
            _profile_mapping(self.profile["node_shapes"], "node_shapes")[name],
            f"node_shapes.{name}",
        )

    def _field_specs(self, shape_name: str) -> Mapping[str, Any]:
        return _profile_mapping(
            self._shape_spec(shape_name)["fields"],
            f"node_shapes.{shape_name}.fields",
        )

    def _value(
        self,
        node: Node,
        spec: Mapping[str, Any],
        path: tuple[str | int, ...],
        ordinal_path: tuple[int, ...],
    ) -> tuple[object, AuthoredValue]:
        operation = spec["parser"]
        where = ".".join(str(part) for part in path)
        if operation in {"string", "nonempty_string", "module_iri"}:
            plain, authored = self._scalar_string(
                node, where, nonempty=operation != "string"
            )
            if operation == "module_iri":
                _absolute_iri(plain, where)
                parts = urlsplit(plain)
                if parts.query or parts.fragment or plain.endswith("/"):
                    raise ValueError(
                        f"{where} must omit query, fragment, and trailing slash"
                    )
            result: tuple[object, AuthoredValue] = plain, authored
        elif operation == "boolean":
            result = self._scalar_boolean(node, where)
        elif operation == "decimal":
            result = self._scalar_decimal(node, where)
        elif operation == "string_list":
            if not isinstance(node, SequenceNode):
                raise ValueError(f"{where} must be a sequence")
            values: list[str] = []
            items: list[AuthoredSequenceItem] = []
            classification = spec["item_classification"]
            for ordinal, item in enumerate(node.value):
                value, authored = self._scalar_string(
                    item, f"{where}[{ordinal}]", nonempty=True
                )
                values.append(value)
                items.append(AuthoredSequenceItem(ordinal, authored))
                self._record(
                    path + (ordinal,),
                    ordinal_path + (ordinal,),
                    classification,
                    authored,
                )
            result = tuple(values), AuthoredSequence(tuple(items))
        elif operation == "items":
            if not isinstance(node, SequenceNode):
                raise ValueError(f"{where} must be a sequence")
            values = []
            items = []
            classification = spec["item_classification"]
            for ordinal, item in enumerate(node.value):
                plain, authored = self._shape(
                    item,
                    str(spec["item_shape"]),
                    path + (ordinal,),
                    ordinal_path + (ordinal,),
                )
                values.append(plain)
                items.append(AuthoredSequenceItem(ordinal, authored))
                self._record(
                    path + (ordinal,),
                    ordinal_path + (ordinal,),
                    classification,
                    authored,
                )
            result = tuple(values), AuthoredSequence(tuple(items))
        elif operation in {"named", "enum_values", "prefixes"}:
            values: dict[str, object] = {}
            fields: list[AuthoredField] = []
            key_classification = spec["key_classification"]
            key_parser = spec["key_parser"]
            for key, item, ordinal in self._mapping_items(node, where):
                if key_parser == "ascii_identifier":
                    _ascii_identifier(key, where)
                elif key_parser == "reference":
                    _reference(key, where)
                elif key_parser == "nonempty_string" and not key:
                    raise ValueError(f"{where} has an empty value")
                item_path = path + (key,)
                item_ordinals = ordinal_path + (ordinal,)
                if operation == "prefixes":
                    plain, authored = self._scalar_string(
                        item, f"{where}.{key}", nonempty=True
                    )
                    _absolute_iri(plain, f"{where}.{key}")
                elif (
                    operation == "enum_values"
                    and isinstance(item, ScalarNode)
                    and item.tag == _YAML_NULL
                ):
                    raw = self._raw(item)
                    if item.style is not None or raw not in {"", "null"}:
                        raise ValueError(f"{where}.{key} has unsupported null syntax")
                    plain = {}
                    authored = AuthoredMapping(())
                else:
                    plain, authored = self._shape(
                        item,
                        str(spec["item_shape"]),
                        item_path,
                        item_ordinals,
                    )
                values[key] = plain
                value_classification = spec.get("value_classification")
                fields.append(
                    AuthoredField(
                        key,
                        ordinal,
                        key_classification,
                        authored,
                        value_classification,
                    )
                )
                self._record(
                    item_path,
                    item_ordinals,
                    key_classification,
                    authored,
                    value_classification,
                )
            result = values, AuthoredMapping(tuple(fields))
        elif operation == "adoption_annotations":
            result = self._shape(
                node,
                str(spec["item_shape"]),
                path,
                ordinal_path,
            )
        else:
            raise RuntimeError(f"parser operation {operation!r} is not executable")
        plain, authored = result
        size = len(plain) if isinstance(plain, (tuple, dict)) else None
        if "min_items" in spec and size is not None and size < spec["min_items"]:
            raise ValueError(f"{where} has too few items")
        if "max_items" in spec and size is not None and size > spec["max_items"]:
            raise ValueError(f"{where} has too many items")
        if "values" in spec and plain not in spec["values"]:
            raise ValueError(f"{where} has a rejected value")
        return plain, authored

    def _shape(
        self,
        node: Node,
        shape_name: str,
        path: tuple[str | int, ...],
        ordinal_path: tuple[int, ...],
    ) -> tuple[dict[str, object], AuthoredMapping]:
        shape = self._shape_spec(shape_name)
        specs = self._field_specs(shape_name)
        where = ".".join(str(part) for part in path) or "schema root"
        values = self._mapping_items(node, where)
        unknown = [name for name, _, _ in values if name not in specs]
        if unknown:
            raise _refusal(
                LinkMLRefusalReason.REJECTED_SOURCE,
                f"{where} contains rejected field {unknown[0]!r}",
                module_id=self.module_id,
                path=path + (unknown[0],),
            )
        plain: dict[str, object] = {}
        fields: list[AuthoredField] = []
        for name, node_value, ordinal in values:
            spec = _profile_mapping(specs[name], f"{shape_name}.{name}")
            classification = str(spec["classification"])
            field_path = path + (name,)
            field_ordinals = ordinal_path + (ordinal,)
            if classification == "REJECTED":
                raise _refusal(
                    LinkMLRefusalReason.REJECTED_SOURCE,
                    f"{where} contains rejected field {name!r}",
                    module_id=self.module_id,
                    path=field_path,
                )
            parsed, authored = self._value(node_value, spec, field_path, field_ordinals)
            plain[name] = parsed
            value_classification = spec.get("value_classification")
            if spec["parser"] == "prefixes":
                value_classification = None
            fields.append(
                AuthoredField(
                    name,
                    ordinal,
                    classification,
                    authored,
                    value_classification,
                )
            )
            self._record(
                field_path,
                field_ordinals,
                classification,
                authored,
                value_classification,
            )
        missing = [
            name
            for name, raw_spec in specs.items()
            if _profile_mapping(raw_spec, f"{shape_name}.{name}").get("required")
            is True
            and name not in plain
        ]
        if missing:
            raise ValueError(
                f"{where} is missing required field {sorted(missing)[0]!r}"
            )
        if len(plain) < shape.get("min_fields", 0):
            raise ValueError(f"{where} has too few fields")
        if len(plain) > shape.get("max_fields", float("inf")):
            raise ValueError(f"{where} has too many fields")
        return plain, AuthoredMapping(tuple(fields))

    def parse(self) -> _ParsedDocument:
        try:
            forbidden = (
                AliasToken,
                AnchorToken,
                DirectiveToken,
                DocumentEndToken,
                DocumentStartToken,
                TagToken,
            )
            for token in yaml.scan(self.text, Loader=yaml.SafeLoader):
                if isinstance(token, forbidden):
                    raise ValueError(
                        f"source contains rejected YAML token {type(token).__name__}"
                    )
            documents = list(yaml.compose_all(self.text, Loader=yaml.SafeLoader))
        except (ValueError, yaml.YAMLError) as error:
            raise _refusal(
                LinkMLRefusalReason.MALFORMED_SOURCE,
                f"source is not valid under the raw grammar: {error}",
                module_id=self.module_id,
            ) from error
        if len(documents) != 1 or documents[0] is None:
            raise _refusal(
                LinkMLRefusalReason.MALFORMED_SOURCE,
                "source must contain exactly one mapping document",
                module_id=self.module_id,
            )
        try:
            plain, root = self._shape(documents[0], "schema", (), ())
        except LinkMLAdapterRefusal:
            raise
        except (KeyError, RuntimeError, TypeError, ValueError) as error:
            raise _refusal(
                LinkMLRefusalReason.MALFORMED_SOURCE,
                str(error),
                module_id=self.module_id,
            ) from error
        return _ParsedDocument(plain, root, tuple(self.occurrences))


def _decode_source(source: bytes, module_id: str) -> str:
    if type(source) is not bytes:
        raise _refusal(
            LinkMLRefusalReason.MALFORMED_OBSERVATION,
            "retained source bytes are malformed",
            module_id=module_id,
        )
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as error:
        raise _refusal(
            LinkMLRefusalReason.MALFORMED_SOURCE,
            "source is not valid UTF-8",
            module_id=module_id,
        ) from error
    if text.startswith("\ufeff"):
        raise _refusal(
            LinkMLRefusalReason.MALFORMED_SOURCE,
            "source must not contain a byte-order mark",
            module_id=module_id,
        )
    return text


def _parse_linkml_source(
    source: bytes,
    *,
    module_id: str,
    profile: Mapping[str, object] | None = None,
) -> _ParsedDocument:
    """Parse one ordinary exact source for this adapter and the old bootstrap."""

    active = _load_adapter_profile(profile)
    text = _decode_source(source, module_id)
    parsed = _RawParser(text=text, module_id=module_id, profile=active.data).parse()
    try:
        yaml_loader.loads(text, target_class=SchemaDefinition)
    except Exception as error:
        raise _refusal(
            LinkMLRefusalReason.LINKML_RUNTIME_REJECTED,
            f"LinkML Runtime 1.11.1 rejected the source: {error}",
            module_id=module_id,
        ) from error
    return parsed


def _validate_selection(value: object, where: str) -> ResolverSelection:
    if (
        type(value) is not ResolverSelection
        or type(value.resolver_id) is not str
        or not value.resolver_id
        or type(value.profile_version) is not str
        or not value.profile_version
        or type(value.configuration_id) is not str
        or not value.configuration_id
    ):
        raise _refusal(
            LinkMLRefusalReason.MALFORMED_OBSERVATION,
            f"{where} has a malformed resolver selection",
        )
    return value


def _validate_observation(observation: object) -> ModuleObservation:
    if type(observation) is not ModuleObservation:
        raise _refusal(
            LinkMLRefusalReason.MALFORMED_OBSERVATION,
            "adapter input must be one exact ModuleObservation",
        )
    source = observation.source
    if (
        type(observation.module_id) is not str
        or not observation.module_id
        or type(source) is not RetainedSource
        or type(source.resolved_locator) is not str
        or not source.resolved_locator
        or source.resolved_locator != observation.module_id
        or type(source.source_bytes) is not bytes
        or type(source.byte_length) is not int
        or source.byte_length < 0
        or source.byte_length != len(source.source_bytes)
        or type(source.sha256) is not str
        or source.sha256 != f"sha256:{sha256(source.source_bytes).hexdigest()}"
        or type(source.media_type) is not str
        or not source.media_type
        or type(observation.authored_imports) is not tuple
        or any(
            type(item) is not str or not item for item in observation.authored_imports
        )
    ):
        raise _refusal(
            LinkMLRefusalReason.MALFORMED_OBSERVATION,
            "module observation does not attest its exact source",
            module_id=getattr(observation, "module_id", None),
        )
    _validate_selection(source.resolver_selection, "retained source")
    return observation


def _resolved_term(namespace: str, spec: object) -> str:
    term = _profile_mapping(spec, "builtin term")
    return (
        str(term["value"])
        if term["form"] == "ABSOLUTE"
        else namespace + str(term["value"])
    )


def _trusted_module(
    observation: ModuleObservation, profile: _AdapterProfile
) -> DeclaredModule:
    data = profile.data
    trusted = _profile_mapping(data["trusted_module"], "trusted_module")
    source = observation.source
    if (
        source.byte_length != trusted["byte_length"]
        or source.sha256 != trusted["sha256"]
        or observation.authored_imports
    ):
        raise _refusal(
            LinkMLRefusalReason.TRUSTED_MODULE_MISMATCH,
            "trusted LinkML module bytes or imports differ from the profile",
            module_id=observation.module_id,
        )
    namespace = str(data["namespace"])
    builtins = _profile_mapping(data["builtins"], "builtins")
    declarations = tuple(
        DeclaredDeclaration(
            name=name,
            identifier=_resolved_term(namespace, builtins[name]),
            kind="Scalar",
            ordinal=ordinal,
            path=("trusted_builtins", name),
            body=AuthoredMapping(()),
        )
        for ordinal, name in enumerate(data["seed_primitives"])
    )
    return DeclaredModule(
        module_id=observation.module_id,
        schema_id=str(trusted["schema_id"]),
        source=source,
        authored_imports=(),
        root=AuthoredMapping(()),
        declarations=declarations,
        occurrences=tuple(
            ClassifiedOccurrence(
                ("trusted_builtins", declaration.name),
                (declaration.ordinal,),
                "IDENTITY_ONLY",
                AuthoredScalar("STRING", declaration.name, declaration.name),
            )
            for declaration in declarations
        ),
        trusted=True,
        support_profile=str(data["support_profile"]),
        profile_sha256=profile.digest,
    )


def _mapping_field(mapping: AuthoredMapping, name: str) -> AuthoredField | None:
    return next((field for field in mapping.fields if field.name == name), None)


def _declarations(
    parsed: _ParsedDocument, profile: Mapping[str, Any]
) -> tuple[DeclaredDeclaration, ...]:
    schema_id = str(parsed.plain["id"])
    shapes = _profile_mapping(profile["node_shapes"], "node_shapes")
    declarations: list[DeclaredDeclaration] = []

    def append_collection(root_field: AuthoredField) -> None:
        root_spec = _profile_mapping(
            _profile_mapping(shapes["schema"], "schema")["fields"][root_field.name],
            root_field.name,
        )
        shape_name = str(root_spec["item_shape"])
        shape = _profile_mapping(shapes[shape_name], shape_name)
        kind = shape.get("declaration_kind")
        if kind is None:
            return
        if not isinstance(root_field.value, AuthoredMapping):
            raise RuntimeError("validated declaration collection is not a mapping")
        for item in root_field.value.fields:
            if not isinstance(item.value, AuthoredMapping):
                raise RuntimeError("validated declaration body is not a mapping")
            declarations.append(
                DeclaredDeclaration(
                    name=item.name,
                    identifier=f"{schema_id}/{item.name}",
                    kind=str(kind),
                    ordinal=len(declarations),
                    path=(root_field.name, item.name),
                    body=item.value,
                )
            )

    for root_field in parsed.root.fields:
        if root_field.name in {"types", "enums", "slots", "classes"}:
            append_collection(root_field)
        if root_field.name != "classes" or not isinstance(
            root_field.value, AuthoredMapping
        ):
            continue
        attribute_shape = _profile_mapping(shapes["attribute"], "attribute")
        kind = str(attribute_shape["declaration_kind"])
        for class_field in root_field.value.fields:
            if not isinstance(class_field.value, AuthoredMapping):
                continue
            attributes = _mapping_field(class_field.value, "attributes")
            if attributes is None or not isinstance(attributes.value, AuthoredMapping):
                continue
            class_id = f"{schema_id}/{class_field.name}"
            for attribute in attributes.value.fields:
                if not isinstance(attribute.value, AuthoredMapping):
                    raise RuntimeError("validated attribute body is not a mapping")
                declarations.append(
                    DeclaredDeclaration(
                        name=attribute.name,
                        identifier=f"{class_id}/{attribute.name}",
                        kind=kind,
                        ordinal=len(declarations),
                        path=(
                            "classes",
                            class_field.name,
                            "attributes",
                            attribute.name,
                        ),
                        body=attribute.value,
                    )
                )
    return tuple(declarations)


def _parse_observation(
    observation: object,
    *,
    profile: Mapping[str, object] | None,
) -> DeclaredModule:
    module = _validate_observation(observation)
    active = _load_adapter_profile(profile)
    trusted_id = str(
        _profile_mapping(active.data["trusted_module"], "trusted_module")["module_id"]
    )
    if module.module_id == trusted_id:
        return _trusted_module(module, active)
    parsed = _parse_linkml_source(
        module.source.source_bytes,
        module_id=module.module_id,
        profile=active.data,
    )
    imports = tuple(str(item) for item in parsed.plain.get("imports", ()))
    if imports != module.authored_imports:
        mismatch = next(
            (
                index
                for index, pair in enumerate(
                    zip(imports, module.authored_imports, strict=False)
                )
                if pair[0] != pair[1]
            ),
            min(len(imports), len(module.authored_imports)),
        )
        raise _refusal(
            LinkMLRefusalReason.OBSERVATION_IMPORT_MISMATCH,
            "parsed imports differ from retained authored imports",
            module_id=module.module_id,
            path=("imports", mismatch),
        )
    return DeclaredModule(
        module_id=module.module_id,
        schema_id=str(parsed.plain["id"]),
        source=module.source,
        authored_imports=imports,
        root=parsed.root,
        declarations=_declarations(parsed, active.data),
        occurrences=parsed.occurrences,
        trusted=False,
        support_profile=str(active.data["support_profile"]),
        profile_sha256=active.digest,
    )


def parse_linkml_module(
    module: ModuleObservation,
    *,
    profile: Mapping[str, object] | None = None,
) -> DeclaredModule:
    """Parse one retained module without resolving or binding anything."""

    return _parse_observation(module, profile=profile)


@dataclass(frozen=True, slots=True)
class LinkMLImportReader:
    """Read ordered LinkML imports from retained bytes for source closure."""

    profile: Mapping[str, object] | None = None

    def read_imports(self, source: RetainedSource) -> tuple[str, ...]:
        if type(source) is not RetainedSource:
            raise CollaboratorRefusal("input is not a retained source")
        try:
            active = _load_adapter_profile(self.profile)
            trusted_id = str(
                _profile_mapping(active.data["trusted_module"], "trusted_module")[
                    "module_id"
                ]
            )
            if source.resolved_locator == trusted_id:
                observation = ModuleObservation(trusted_id, source, ())
                _trusted_module(observation, active)
                return ()
            parsed = _parse_linkml_source(
                source.source_bytes,
                module_id=source.resolved_locator,
                profile=active.data,
            )
            return tuple(str(item) for item in parsed.plain.get("imports", ()))
        except LinkMLAdapterRefusal as error:
            raise CollaboratorRefusal(str(error)) from error


def _edge_index(
    edges: tuple[ResolvedImportEdge, ...],
) -> dict[tuple[str, int], ResolvedImportEdge]:
    indexed: dict[tuple[str, int], ResolvedImportEdge] = {}
    for edge in edges:
        if type(edge) is not ResolvedImportEdge:
            raise _refusal(
                LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH,
                "closure contains a malformed import edge",
            )
        if (
            type(edge.parent_module_id) is not str
            or not edge.parent_module_id
            or type(edge.parent_import_ordinal) is not int
            or edge.parent_import_ordinal < 0
            or type(edge.literal_import) is not str
            or not edge.literal_import
            or type(edge.child_module_id) is not str
            or not edge.child_module_id
        ):
            raise _refusal(
                LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH,
                "closure contains a malformed import edge",
            )
        try:
            _validate_selection(edge.resolver_selection, "import edge")
        except LinkMLAdapterRefusal as error:
            raise _refusal(
                LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH,
                "closure contains a malformed import edge resolver selection",
                module_id=edge.parent_module_id,
                path=("imports", edge.parent_import_ordinal),
            ) from error
        key = (edge.parent_module_id, edge.parent_import_ordinal)
        if key in indexed:
            raise _refusal(
                LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH,
                "closure repeats an import edge ordinal",
                module_id=edge.parent_module_id,
                path=("imports", edge.parent_import_ordinal),
            )
        indexed[key] = edge
    return indexed


def adapt_linkml_closure(
    closure: SourceClosure,
    *,
    profile: Mapping[str, object] | None = None,
) -> DeclaredContractClosure:
    """Adapt one complete retained closure or refuse without partial output."""

    if type(closure) is not SourceClosure:
        raise _refusal(
            LinkMLRefusalReason.MALFORMED_OBSERVATION,
            "adapter input must be one exact SourceClosure",
        )
    if type(closure.modules) is not tuple or type(closure.import_edges) is not tuple:
        raise _refusal(
            LinkMLRefusalReason.MALFORMED_OBSERVATION,
            "closure members and import edges must be immutable tuples",
        )
    selection = _validate_selection(closure.selection, "closure")
    root = closure.root
    if (
        type(root) is not RootResolution
        or type(root.requested_locator) is not str
        or not root.requested_locator
        or type(root.resolved_locator) is not str
        or not root.resolved_locator
        or type(root.source_sha256) is not str
    ):
        raise _refusal(
            LinkMLRefusalReason.MALFORMED_OBSERVATION,
            "closure root resolution is malformed",
        )
    _validate_selection(root.resolver_selection, "closure root")
    active = _load_adapter_profile(profile)
    trusted_literal = str(active.data["trusted_import"])
    trusted_id = str(
        _profile_mapping(active.data["trusted_module"], "trusted_module")["module_id"]
    )
    edges = _edge_index(closure.import_edges)
    observations = tuple(_validate_observation(module) for module in closure.modules)
    if any(module.source.resolver_selection != selection for module in observations):
        raise _refusal(
            LinkMLRefusalReason.MALFORMED_OBSERVATION,
            "closure module was retained under a different resolver selection",
        )
    module_ids = tuple(module.module_id for module in observations)
    if len(module_ids) != len(set(module_ids)):
        raise _refusal(
            LinkMLRefusalReason.MALFORMED_OBSERVATION,
            "closure repeats a module identifier",
        )
    available = set(module_ids)
    mismatched_trusted = next(
        (
            edge
            for edge in closure.import_edges
            if edge.literal_import == trusted_literal
            and edge.child_module_id != trusted_id
        ),
        None,
    )
    if mismatched_trusted is not None:
        raise _refusal(
            LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH,
            "trusted LinkML import resolves to the wrong module identity",
            module_id=mismatched_trusted.parent_module_id,
            path=("imports", mismatched_trusted.parent_import_ordinal),
        )
    declared = tuple(
        _parse_observation(module, profile=active) for module in observations
    )
    consumed: set[tuple[str, int]] = set()
    for module in declared:
        for ordinal, literal in enumerate(module.authored_imports):
            key = (module.module_id, ordinal)
            edge = edges.get(key)
            if (
                edge is None
                or edge.literal_import != literal
                or edge.child_module_id not in available
                or edge.resolver_selection != closure.selection
            ):
                raise _refusal(
                    LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH,
                    f"closure does not resolve authored import {literal!r}",
                    module_id=module.module_id,
                    path=("imports", ordinal),
                )
            consumed.add(key)
    extra = next(
        (
            edge
            for edge in closure.import_edges
            if (edge.parent_module_id, edge.parent_import_ordinal) not in consumed
        ),
        None,
    )
    if extra is not None:
        raise _refusal(
            LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH,
            "closure contains an unauthored import edge",
            module_id=extra.parent_module_id,
            path=("imports", extra.parent_import_ordinal),
        )
    if (
        closure.root.resolved_locator not in available
        or closure.root.source_sha256
        != next(
            module.source.sha256
            for module in observations
            if module.module_id == closure.root.resolved_locator
        )
        or closure.root.resolver_selection != closure.selection
    ):
        raise _refusal(
            LinkMLRefusalReason.MALFORMED_OBSERVATION,
            "closure root does not match its retained module",
        )
    children: dict[str, list[str]] = {}
    for edge in closure.import_edges:
        children.setdefault(edge.parent_module_id, []).append(edge.child_module_id)
    reachable: set[str] = set()
    pending = [closure.root.resolved_locator]
    while pending:
        module_id = pending.pop()
        if module_id in reachable:
            continue
        reachable.add(module_id)
        pending.extend(reversed(children.get(module_id, ())))
    orphan = next(
        (
            module.module_id
            for module in observations
            if module.module_id not in reachable
        ),
        None,
    )
    if orphan is not None:
        raise _refusal(
            LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH,
            "closure contains a module not reachable from its exact root",
            module_id=orphan,
        )
    return DeclaredContractClosure(source_closure=closure, modules=declared)

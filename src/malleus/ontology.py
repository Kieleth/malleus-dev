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
from typing import Any, Mapping

import yaml


BUILTIN_RANGES = frozenset({"string", "integer", "float", "boolean", "datetime"})
FINGERPRINT_VERSION = 2


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
        identifier=data.get("identifier") if "identifier" in data else None,
        equals_string=data.get("equals_string"),
        minimum_value=data.get("minimum_value"),
        maximum_value=data.get("maximum_value"),
    )


def _require_optional_type(subject: str, name: str, value: Any, expected: type) -> None:
    if value is not None and not isinstance(value, expected):
        raise OntologyError(f"{subject} {name} must be {expected.__name__}")


def _validate_constraint_definition(subject: str, constraint: SlotConstraint) -> None:
    for name in ("required", "multivalued", "identifier"):
        _require_optional_type(subject, name, getattr(constraint, name), bool)
    for name in ("range", "equals_string"):
        _require_optional_type(subject, name, getattr(constraint, name), str)
    for name in ("minimum_value", "maximum_value"):
        value = getattr(constraint, name)
        if value is not None and (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(float(value))
        ):
            raise OntologyError(f"{subject} {name} must be a finite number")


def _merge_constraint(base: SlotConstraint, override: SlotConstraint) -> SlotConstraint:
    values = {}
    for item in fields(SlotConstraint):
        value = getattr(override, item.name)
        values[item.name] = getattr(base, item.name) if value is None else value
    return SlotConstraint(**values)


def _constraint_dict(value: SlotConstraint) -> dict[str, Any]:
    return {item.name: getattr(value, item.name) for item in fields(SlotConstraint)}


class OntologyRegistry:
    """Resolved ontology registry and closed-world structural validator."""

    def __init__(
        self,
        schema_path: str | Path,
        import_map: Mapping[str, str | Path] | None = None,
    ):
        self._schema_path = Path(schema_path)
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
        self._loaded_paths: set[Path] = set()
        self._effective_slot_cache: dict[str, dict[str, SlotConstraint]] = {}
        self._load_schema(self._schema_path)
        self._validate_schema()

    def _mapped_path(self, path: str | Path) -> Path:
        mapped = Path(path)
        if not mapped.is_absolute():
            mapped = self._schema_path.parent / mapped
        return mapped

    def _claim_name(self, kind: str, name: str, source: Path) -> None:
        key = (kind, name)
        prior = self._definition_sources.get(key)
        if prior is not None:
            raise OntologyError(
                f"Duplicate {kind} '{name}' in '{source}' conflicts with '{prior}'"
            )
        self._definition_sources[key] = source

    def _load_schema(self, path: Path) -> None:
        path = path.resolve()
        if path in self._loaded_paths:
            return
        if not path.is_file():
            raise OntologyError(f"Ontology file does not exist: '{path}'")
        self._loaded_paths.add(path)

        with path.open(encoding="utf-8") as stream:
            schema = yaml.load(stream, Loader=UniqueKeyLoader)
        if not isinstance(schema, dict):
            raise OntologyError(f"Ontology must be a YAML mapping: '{path}'")

        imports = schema.get("imports", [])
        if not isinstance(imports, list) or not all(isinstance(item, str) for item in imports):
            raise OntologyError(f"Ontology imports must be a list of strings: '{path}'")
        for imported_name in imports:
            if imported_name == "linkml:types":
                continue
            imported_path = self._resolve_import(path.parent, imported_name)
            if imported_path is None:
                raise OntologyError(
                    f"Cannot resolve import '{imported_name}' required by '{path}'. "
                    "Provide a local file or an explicit import_map entry."
                )
            self._load_schema(imported_path)

        for name, definition in self._mapping(schema, "types", path).items():
            if not isinstance(name, str):
                raise OntologyError(f"Type names in '{path}' must be strings")
            self._claim_name("type", name, path)
            if not isinstance(definition, dict) or not definition.get("typeof"):
                raise OntologyError(f"Type '{name}' in '{path}' requires typeof")
            if not isinstance(definition["typeof"], str):
                raise OntologyError(f"Type '{name}' typeof in '{path}' must be string")
            self._scalar_types[name] = definition["typeof"]

        for name, definition in self._mapping(schema, "enums", path).items():
            if not isinstance(name, str):
                raise OntologyError(f"Enum names in '{path}' must be strings")
            self._claim_name("enum", name, path)
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
            self._claim_name("slot", name, path)
            if not isinstance(definition, dict):
                raise OntologyError(f"Slot '{name}' in '{path}' must be a mapping")
            slot = _constraint(definition)
            _validate_constraint_definition(f"Slot '{name}'", slot)
            self._slots[name] = slot
            if slot.range:
                self._slot_ranges[name] = slot.range

        for name, definition in self._mapping(schema, "classes", path).items():
            if not isinstance(name, str):
                raise OntologyError(f"Class names in '{path}' must be strings")
            self._claim_name("class", name, path)
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
                mixins=tuple(mixins),
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
            return mapped.resolve() if mapped.is_file() else None

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
                return None
            current = current.parent

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
            self.effective_slots(name)

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
        if name in BUILTIN_RANGES:
            return name
        if name not in self._scalar_types:
            raise OntologyError(f"Scalar type chain terminates in unsupported range '{name}'")
        if name in seen:
            raise OntologyError(f"Cyclic scalar type definition at '{name}'")
        return self._resolve_scalar_range(self._scalar_types[name], seen | {name})

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
        for mixin in typedef.mixins:
            for slot_name, constraint in self._build_effective_slots(mixin, next_trail).items():
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

        non_string_keys = [repr(name) for name in data if not isinstance(name, str)]
        if non_string_keys:
            return [f"Property names must be strings, got: {', '.join(non_string_keys)}"]

        slots = self.effective_slots(type_name)
        errors = [
            f"Unknown property '{name}' for {type_name}"
            for name in sorted(set(data) - set(slots))
        ]
        for name, slot in slots.items():
            if slot.required and self._missing_required(name, data):
                errors.append(f"Required slot '{name}' missing for {type_name}")
        for name, value in data.items():
            slot = slots.get(name)
            if slot is not None and value is not None:
                errors.extend(self._validate_value(name, value, slot))
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
        elif range_name in self._types and (not isinstance(value, str) or not value.strip()):
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
        if not hasattr(self, "_cached_hash"):
            canonical = {
                "fingerprint_version": FINGERPRINT_VERSION,
                "types": {
                    name: {
                        "parent": typedef.parent,
                        "slots": sorted(typedef.slots),
                        "slot_usage": {
                            slot: _constraint_dict(constraint)
                            for slot, constraint in sorted(typedef.slot_usage.items())
                        },
                        "is_mixin": typedef.is_mixin,
                        "abstract": typedef.abstract,
                        "mixins": sorted(typedef.mixins),
                    }
                    for name, typedef in sorted(self._types.items())
                },
                "enums": {
                    name: sorted(definition.values)
                    for name, definition in sorted(self._enums.items())
                },
                "slots": {
                    name: _constraint_dict(definition)
                    for name, definition in sorted(self._slots.items())
                },
                "scalar_types": dict(sorted(self._scalar_types.items())),
            }
            blob = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
            self._cached_hash = hashlib.sha256(blob.encode()).hexdigest()
        return self._cached_hash

    def fingerprint(self) -> frozenset[str]:
        """Return producer-side structural facts, excluding required constraints."""
        if not hasattr(self, "_cached_fingerprint"):
            facts = {f"fingerprint_version:{FINGERPRINT_VERSION}"}
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
                    facts.update(self._constraint_facts(f"type:{name}:usage:{slot_name}", constraint))
            for name, definition in self._enums.items():
                facts.add(f"enum:{name}")
                facts.update(f"enum:{name}:{value}" for value in definition.values)
            for name, definition in self._slots.items():
                facts.add(f"slot:{name}")
                facts.update(self._constraint_facts(f"slot:{name}", definition))
            for name, base in self._scalar_types.items():
                facts.add(f"scalar_type:{name}:{base}")
            self._cached_fingerprint = frozenset(facts)
        return self._cached_fingerprint

    @staticmethod
    def _constraint_facts(prefix: str, constraint: SlotConstraint) -> set[str]:
        facts = set()
        for name in (
            "range",
            "multivalued",
            "identifier",
            "equals_string",
            "minimum_value",
            "maximum_value",
        ):
            value = getattr(constraint, name)
            if value is not None:
                facts.add(f"{prefix}:{name}:{value}")
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
        mine = self.fingerprint()
        if foreign_fingerprint.issubset(mine):
            return "superset"
        if mine.issubset(foreign_fingerprint):
            return "subset"
        return "divergent"

    def check_compatibility_strict(
        self,
        foreign_hash: str,
        foreign_strict_fingerprint: frozenset[str],
    ) -> str:
        if self.content_hash() == foreign_hash:
            return "identical"
        mine = self.strict_fingerprint()
        if foreign_strict_fingerprint.issubset(mine):
            return "superset"
        if mine.issubset(foreign_strict_fingerprint):
            return "subset"
        return "divergent"

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

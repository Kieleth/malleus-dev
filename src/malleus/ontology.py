"""Ontology registry: loads a LinkML schema and provides runtime type validation.

The registry is the constructor parameter for the KG. It defines what CAN exist:
which entity types, relation types, signal types, event types, and their constraints.

Content-addressable hashing and fingerprinting enable distributed ontology
convergence: two instances can verify compatibility (identical, superset,
subset, or divergent) without exchanging full schemas.
"""

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass(frozen=True)
class SlotConstraint:
    """A constraint on a slot from slot_usage."""
    required: bool = False
    range: str | None = None


@dataclass(frozen=True)
class TypeDef:
    """A registered type (entity, relation, signal, event class)."""
    name: str
    parent: str | None
    slots: list[str] = field(default_factory=list)
    slot_usage: dict[str, SlotConstraint] = field(default_factory=dict)
    is_mixin: bool = False


@dataclass(frozen=True)
class EnumDef:
    """A registered enum with its permissible values."""
    name: str
    values: frozenset[str]


class OntologyRegistry:
    """Runtime type registry built from a LinkML schema.

    This is the ontology-as-constructor-parameter: the KG cannot be
    instantiated without it, and every write is validated against it.
    """

    def __init__(self, schema_path: str | Path):
        self._schema_path = Path(schema_path)
        self._types: dict[str, TypeDef] = {}
        self._enums: dict[str, EnumDef] = {}
        self._slot_ranges: dict[str, str] = {}  # slot_name -> range (from slots: section)
        self._inheritance: dict[str, str | None] = {}
        self._load()

    def _load(self):
        """Load schema and all its imports recursively."""
        self._load_schema(self._schema_path)

    @property
    def _loaded_paths(self) -> set[str]:
        if not hasattr(self, "__loaded"):
            self.__loaded: set[str] = set()
        return self.__loaded

    def _load_schema(self, path: Path):
        resolved = str(path.resolve())
        if resolved in self._loaded_paths:
            return
        self._loaded_paths.add(resolved)

        with open(path) as f:
            schema = yaml.safe_load(f)

        for imp in schema.get("imports", []):
            if imp == "linkml:types":
                continue
            imp_path = self._resolve_import(path.parent, imp)
            if imp_path is not None:
                self._load_schema(imp_path)

        for name, defn in schema.get("enums", {}).items():
            values = frozenset(defn.get("permissible_values", {}).keys())
            self._enums[name] = EnumDef(name=name, values=values)

        for name, defn in schema.get("slots", {}).items():
            slot_range = defn.get("range")
            if slot_range:
                self._slot_ranges[name] = slot_range

        for name, defn in schema.get("classes", {}).items():
            parent = defn.get("is_a")
            is_mixin = defn.get("mixin", False)
            slots = defn.get("slots", [])
            slot_usage = {}
            for slot_name, usage in defn.get("slot_usage", {}).items():
                slot_usage[slot_name] = SlotConstraint(
                    required=usage.get("required", False),
                    range=usage.get("range"),
                )
            self._types[name] = TypeDef(
                name=name,
                parent=parent,
                slots=slots,
                slot_usage=slot_usage,
                is_mixin=is_mixin,
            )
            self._inheritance[name] = parent

    def _resolve_import(self, start_dir: Path, name: str) -> Path | None:
        """Resolve an import name to a YAML file path.

        Walks upward from start_dir looking for {name}.yaml. Allows domain
        extensions to import a root ontology that lives a directory above.
        Returns None if not found at any level.
        """
        current = start_dir.resolve()
        while True:
            candidate = current / f"{name}.yaml"
            if candidate.exists():
                return candidate
            if current.parent == current:  # filesystem root
                return None
            current = current.parent

    def has_type(self, type_name: str) -> bool:
        return type_name in self._types

    def has_enum(self, enum_name: str) -> bool:
        return enum_name in self._enums

    def is_valid_enum_value(self, enum_name: str, value: str) -> bool:
        if enum_name not in self._enums:
            return False
        return value in self._enums[enum_name].values

    def get_enum_values(self, enum_name: str) -> frozenset[str]:
        if enum_name not in self._enums:
            raise KeyError(f"Unknown enum: {enum_name}")
        return self._enums[enum_name].values

    def is_subtype_of(self, child: str, ancestor: str) -> bool:
        """Check if child is a subtype of ancestor (walks the is_a chain)."""
        current = child
        while current is not None:
            if current == ancestor:
                return True
            current = self._inheritance.get(current)
        return False

    def get_type(self, type_name: str) -> TypeDef:
        if type_name not in self._types:
            raise KeyError(f"Unknown type: {type_name}")
        return self._types[type_name]

    def get_slot_constraint(self, type_name: str, slot_name: str) -> SlotConstraint | None:
        """Get the most specific slot constraint for a type, walking up the hierarchy."""
        current = type_name
        while current is not None:
            typedef = self._types.get(current)
            if typedef and slot_name in typedef.slot_usage:
                return typedef.slot_usage[slot_name]
            current = self._inheritance.get(current)
        return None

    def validate_enum_field(self, type_name: str, slot_name: str, value: str) -> str | None:
        """Validate a field value against its enum constraint. Returns error message or None.

        Checks two sources:
        1. slot_usage on the class (or ancestors): most specific constraint
        2. slot-level range from the slots: section: fallback
        """
        constraint = self.get_slot_constraint(type_name, slot_name)
        if constraint and constraint.range and self.has_enum(constraint.range):
            if not self.is_valid_enum_value(constraint.range, value):
                valid = self.get_enum_values(constraint.range)
                return f"Invalid value '{value}' for {slot_name}. Valid: {sorted(valid)}"
            return None

        slot_range = self._slot_ranges.get(slot_name)
        if slot_range and self.has_enum(slot_range):
            if not self.is_valid_enum_value(slot_range, value):
                valid = self.get_enum_values(slot_range)
                return f"Invalid value '{value}' for {slot_name}. Valid: {sorted(valid)}"

        return None

    # --- Content-addressable hashing ---

    def content_hash(self) -> str:
        """Compute deterministic SHA-256 hash of the resolved ontology.

        Two registries with identical resolved state produce the same hash,
        regardless of file paths or load order. The hash covers all types,
        enums, slot ranges, and inheritance in canonical (sorted) form.

        This is the ontology identity for distributed sync: include it in
        every graph write so receivers can verify compatibility.
        """
        if not hasattr(self, "_cached_hash"):
            canonical = {
                "types": {
                    name: {
                        "parent": td.parent,
                        "slots": sorted(td.slots),
                        "slot_usage": {
                            k: {"required": v.required, "range": v.range}
                            for k, v in sorted(td.slot_usage.items())
                        },
                        "is_mixin": td.is_mixin,
                    }
                    for name, td in sorted(self._types.items())
                },
                "enums": {
                    name: sorted(ed.values)
                    for name, ed in sorted(self._enums.items())
                },
                "slot_ranges": dict(sorted(self._slot_ranges.items())),
                "inheritance": dict(sorted(self._inheritance.items())),
            }
            blob = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
            self._cached_hash = hashlib.sha256(blob.encode("utf-8")).hexdigest()
        return self._cached_hash

    def fingerprint(self) -> frozenset[str]:
        """Compute atomic facts about this ontology for superset checking.

        Each element is one fact: type exists, enum value exists, inheritance
        link, slot range, etc. Under additive-only evolution, a newer ontology's
        fingerprint is a strict superset of an older one's.

        Required/optional constraints are excluded from the fingerprint because
        additive-only allows relaxation (required -> optional), which is a valid
        superset change that doesn't affect data compatibility.
        """
        if not hasattr(self, "_cached_fingerprint"):
            facts: set[str] = set()

            for name, td in self._types.items():
                facts.add(f"type:{name}")
                if td.parent:
                    facts.add(f"type:{name}:parent:{td.parent}")
                if td.is_mixin:
                    facts.add(f"type:{name}:mixin")
                for slot in td.slots:
                    facts.add(f"type:{name}:slot:{slot}")
                for slot_name, constraint in td.slot_usage.items():
                    if constraint.range:
                        facts.add(f"type:{name}:usage:{slot_name}:range:{constraint.range}")

            for name, ed in self._enums.items():
                facts.add(f"enum:{name}")
                for value in ed.values:
                    facts.add(f"enum:{name}:{value}")

            for slot_name, range_type in self._slot_ranges.items():
                facts.add(f"slot_range:{slot_name}:{range_type}")

            self._cached_fingerprint = frozenset(facts)
        return self._cached_fingerprint

    def fingerprint_serializable(self) -> list[str]:
        """Return fingerprint as a sorted list for JSON serialization."""
        return sorted(self.fingerprint())

    def check_compatibility(
        self,
        foreign_hash: str,
        foreign_fingerprint: frozenset[str],
    ) -> str:
        """Check compatibility with a foreign ontology.

        Returns one of:
        - "identical": same resolved ontology
        - "superset": this ontology contains everything foreign does (I'm newer)
        - "subset": foreign contains everything this does (they're newer)
        - "divergent": neither is a superset (incompatible fork)
        """
        if self.content_hash() == foreign_hash:
            return "identical"

        my_fp = self.fingerprint()
        if foreign_fingerprint.issubset(my_fp):
            return "superset"
        if my_fp.issubset(foreign_fingerprint):
            return "subset"
        return "divergent"

    @property
    def entity_types(self) -> list[str]:
        return [n for n, t in self._types.items() if self.is_subtype_of(n, "Entity") and n != "Entity"]

    @property
    def relation_types(self) -> list[str]:
        return [n for n, t in self._types.items() if self.is_subtype_of(n, "Relation") and n != "Relation"]

    @property
    def signal_types(self) -> list[str]:
        return [n for n, t in self._types.items() if self.is_subtype_of(n, "Signal") and n != "Signal"]

    @property
    def event_types(self) -> list[str]:
        return [n for n, t in self._types.items() if self.is_subtype_of(n, "Event") and n != "Event"]

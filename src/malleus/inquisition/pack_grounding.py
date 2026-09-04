"""Mechanical grounding check for optional knowledge packs and adopters."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from hashlib import sha256
import json
from pathlib import Path
from types import MappingProxyType
from typing import Mapping
from urllib.parse import urlsplit

import yaml

from malleus.ontology import OntologyError, UniqueKeyLoader


_RITE_PATH = Path(__file__).with_name("pack-grounding.json")


class PackGroundingRefusalReason(Enum):
    """Closed reasons the pack-grounding rite can refuse exact source bytes."""

    MALFORMED_SOURCE = auto()
    UNKNOWN_ROLE = auto()
    GROUNDING_REQUIRED = auto()
    GROUNDING_NOT_CLOSED = auto()
    GROUNDING_INCOMPLETE = auto()
    DIRECT_ROOT_GROUNDING_REQUIRED = auto()
    PACK_SURFACE_NOT_PRESERVED = auto()


class PackGroundingRefusal(ValueError):
    """Typed refusal from the pack-grounding rite."""

    def __init__(self, reason: PackGroundingRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest_bytes(value: bytes) -> str:
    return "sha256:" + sha256(value).hexdigest()


def _mapping(value: object, where: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.MALFORMED_SOURCE,
            f"{where} must be a mapping with string keys",
        )
    return value


def _load_rite() -> tuple[Mapping[str, object], str]:
    try:
        raw = _RITE_PATH.read_bytes()
        value = json.loads(raw)
        rite = _mapping(value, "pack-grounding rite")
        expected = {
            "schema",
            "roles",
            "root_parents",
            "annotation_key",
            "annotation_tag",
            "cited_fields",
            "cited_with_inventions_fields",
            "vocabulary_fields",
            "none_found_fields",
        }
        if set(rite) != expected:
            raise ValueError("root fields are not closed")
        if rite["schema"] != "malleus.pack-grounding-rite/v0":
            raise ValueError("schema is not supported")
        for field in (
            "roles",
            "root_parents",
            "cited_fields",
            "cited_with_inventions_fields",
            "vocabulary_fields",
            "none_found_fields",
        ):
            items = rite[field]
            if (
                not isinstance(items, list)
                or not items
                or any(not isinstance(item, str) or not item for item in items)
                or len(items) != len(set(items))
            ):
                raise ValueError(f"{field} must be a nonempty unique string list")
        if rite["roles"] != ["PACK", "PROJECT"]:
            raise ValueError("roles differ from the executable boundary")
        if rite["root_parents"] != ["Entity", "Event", "Signal", "Relation"]:
            raise ValueError("root parents differ from the Malleus primitives")
        for field in ("annotation_key", "annotation_tag"):
            if not isinstance(rite[field], str) or not rite[field]:
                raise ValueError(f"{field} must be nonempty text")
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise RuntimeError(f"pack-grounding rite is invalid: {error}") from error
    return MappingProxyType(dict(rite)), _digest_bytes(raw)


_RITE, PACK_GROUNDING_RITE_IDENTITY = _load_rite()
_ROLES = frozenset(_RITE["roles"])
_ROOT_PARENTS = frozenset(_RITE["root_parents"])
_CITED_FIELDS = frozenset(_RITE["cited_fields"])
_CITED_WITH_INVENTIONS_FIELDS = frozenset(_RITE["cited_with_inventions_fields"])
_VOCABULARY_FIELDS = frozenset(_RITE["vocabulary_fields"])
_NONE_FOUND_FIELDS = frozenset(_RITE["none_found_fields"])


@dataclass(frozen=True, slots=True)
class PackGroundingReceipt:
    """Identity and covered subjects of one successful grounding check."""

    role: str
    source_id: str
    source_sha256: str
    rite_identity: str
    grounded_subjects: tuple[str, ...]

    @property
    def canonical_bytes(self) -> bytes:
        return _canonical(
            {
                "grounded_subjects": list(self.grounded_subjects),
                "rite_identity": self.rite_identity,
                "role": self.role,
                "source_id": self.source_id,
                "source_sha256": self.source_sha256,
            }
        )

    def to_json(self) -> str:
        return json.dumps(json.loads(self.canonical_bytes), indent=2, sort_keys=True)


@dataclass(frozen=True, slots=True)
class PackConformanceReceipt:
    """Exact candidate and reference identities for one compatible pack edit."""

    source_id: str
    source_sha256: str
    reference_id: str
    reference_sha256: str

    @property
    def canonical_bytes(self) -> bytes:
        return _canonical(
            {
                "reference_id": self.reference_id,
                "reference_sha256": self.reference_sha256,
                "source_id": self.source_id,
                "source_sha256": self.source_sha256,
            }
        )

    def to_json(self) -> str:
        return json.dumps(json.loads(self.canonical_bytes), indent=2, sort_keys=True)


def _nonblank(value: object, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
            f"{where} must be nonblank text",
        )
    return value


def _terms(value: object, where: str, *, nonempty: bool) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or any(not isinstance(item, str) or not item.strip() for item in value)
        or len(value) != len(set(value))
        or (nonempty and not value)
    ):
        qualifier = "nonempty " if nonempty else ""
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
            f"{where} must be a {qualifier}unique string list",
        )
    return tuple(value)


def _vocabularies(value: object, subject: str) -> None:
    where = f"{subject}.grounding.vocabularies"
    if not isinstance(value, list) or not value:
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
            f"{where} must be a nonempty list",
        )
    seen: set[tuple[str, str]] = set()
    for ordinal, raw_vocabulary in enumerate(value):
        vocabulary = _mapping(raw_vocabulary, f"{where}[{ordinal}]")
        if set(vocabulary) != _VOCABULARY_FIELDS:
            raise PackGroundingRefusal(
                PackGroundingRefusalReason.GROUNDING_NOT_CLOSED,
                f"{where}[{ordinal}] fields are not closed",
            )
        name = _nonblank(vocabulary["vocabulary"], f"{where}[{ordinal}].vocabulary")
        url = _nonblank(
            vocabulary["vocabulary_url"],
            f"{where}[{ordinal}].vocabulary_url",
        )
        if not urlsplit(url).scheme:
            raise PackGroundingRefusal(
                PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
                f"{where}[{ordinal}].vocabulary_url must be an absolute locator",
            )
        identity = (name, url)
        if identity in seen:
            raise PackGroundingRefusal(
                PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
                f"{where} repeats one vocabulary identity",
            )
        seen.add(identity)
        _terms(
            vocabulary["borrowed_terms"],
            f"{where}[{ordinal}].borrowed_terms",
            nonempty=True,
        )


def _grounding(annotations: object, subject: str) -> None:
    if annotations is None:
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.GROUNDING_REQUIRED,
            f"{subject} has no grounding annotation",
        )
    values = _mapping(annotations, f"{subject}.annotations")
    key = str(_RITE["annotation_key"])
    if key not in values:
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.GROUNDING_REQUIRED,
            f"{subject} has no grounding annotation",
        )
    annotation = _mapping(values[key], f"{subject}.annotations.{key}")
    if set(annotation) != {"tag", "value"}:
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.GROUNDING_NOT_CLOSED,
            f"{subject} grounding annotation must contain exactly tag and value",
        )
    if annotation["tag"] != _RITE["annotation_tag"]:
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
            f"{subject} grounding annotation has the wrong tag",
        )
    grounding = _mapping(annotation["value"], f"{subject}.grounding.value")
    fields = set(grounding)
    if fields in {_CITED_FIELDS, _CITED_WITH_INVENTIONS_FIELDS}:
        _nonblank(grounding["area"], f"{subject}.grounding.area")
        _nonblank(grounding["taxonomy"], f"{subject}.grounding.taxonomy")
        _vocabularies(grounding["vocabularies"], subject)
        invented = _terms(
            grounding["invented_terms"],
            f"{subject}.grounding.invented_terms",
            nonempty=False,
        )
        has_search = fields == _CITED_WITH_INVENTIONS_FIELDS
        if bool(invented) != has_search:
            raise PackGroundingRefusal(
                PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
                f"{subject} must pair invented terms with invention_search",
            )
        if has_search:
            _nonblank(
                grounding["invention_search"],
                f"{subject}.grounding.invention_search",
            )
        return
    if fields == _NONE_FOUND_FIELDS:
        _nonblank(grounding["area"], f"{subject}.grounding.area")
        _nonblank(grounding["taxonomy"], f"{subject}.grounding.taxonomy")
        if grounding["none_found"] is not True:
            raise PackGroundingRefusal(
                PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
                f"{subject}.grounding.none_found must be literal true",
            )
        _nonblank(grounding["search"], f"{subject}.grounding.search")
        _terms(
            grounding["invented_terms"],
            f"{subject}.grounding.invented_terms",
            nonempty=True,
        )
        return
    raise PackGroundingRefusal(
        PackGroundingRefusalReason.GROUNDING_NOT_CLOSED,
        f"{subject} grounding fields are not one supported closed form",
    )


def _document(source: bytes) -> Mapping[str, object]:
    if type(source) is not bytes:
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.MALFORMED_SOURCE,
            "source must be exact bytes",
        )
    try:
        decoded = source.decode("utf-8")
        root = yaml.load(decoded, Loader=UniqueKeyLoader)
    except (UnicodeDecodeError, yaml.YAMLError, OntologyError) as error:
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.MALFORMED_SOURCE,
            f"source is not unique-key UTF-8 YAML: {error}",
        ) from error
    return _mapping(root, "schema")


_DOCUMENTATION_FIELDS = frozenset(
    {"annotations", "comments", "description", "examples", "notes", "title"}
)


def _missing_surface(reference: object, candidate: object, path: str) -> list[str]:
    if isinstance(reference, Mapping):
        if not isinstance(candidate, Mapping):
            return [path]
        missing: list[str] = []
        reference_fields = {
            key: value
            for key, value in reference.items()
            if key not in _DOCUMENTATION_FIELDS
        }
        candidate_fields = {
            key: value
            for key, value in candidate.items()
            if key not in _DOCUMENTATION_FIELDS
        }
        for key, value in reference_fields.items():
            child = f"{path}.{key}"
            if key not in candidate_fields:
                missing.append(child)
                continue
            missing.extend(_missing_surface(value, candidate_fields[key], child))
        if not path.endswith(".permissible_values"):
            missing.extend(
                f"{path}.{key}" for key in candidate_fields.keys() - reference_fields
            )
        return missing
    if isinstance(reference, list):
        if not isinstance(candidate, list):
            return [path]
        duplicates = [
            item
            for ordinal, item in enumerate(candidate)
            if item in candidate[:ordinal]
        ]
        return [f"{path}[{item!r}]" for item in duplicates] + [
            f"{path}[{item!r}]"
            for item in (*reference, *candidate)
            if (item in reference) != (item in candidate)
        ]
    return [] if candidate == reference else [path]


def validate_pack_conformance(
    source: bytes,
    *,
    reference: bytes,
) -> PackConformanceReceipt:
    """Check that an edited pack preserves one exact reference pack's surface.

    Documentation may change and declarations may be added. Existing class,
    slot, and enum declarations may not be removed or weakened.
    """

    source_receipt = validate_pack_grounding(source, role="PACK")
    reference_receipt = validate_pack_grounding(reference, role="PACK")
    source_document = _document(source)
    reference_document = _document(reference)
    missing: list[str] = []
    for section in ("classes", "slots", "enums"):
        reference_declarations = _mapping(
            reference_document.get(section, {}), f"reference.{section}"
        )
        source_declarations = _mapping(
            source_document.get(section, {}), f"source.{section}"
        )
        for name, declaration in reference_declarations.items():
            path = f"{section}.{name}"
            if name not in source_declarations:
                missing.append(path)
                continue
            missing.extend(
                _missing_surface(declaration, source_declarations[name], path)
            )
    if missing:
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.PACK_SURFACE_NOT_PRESERVED,
            "reference surface is not preserved: " + ", ".join(sorted(missing)),
        )
    return PackConformanceReceipt(
        source_id=source_receipt.source_id,
        source_sha256=source_receipt.source_sha256,
        reference_id=reference_receipt.source_id,
        reference_sha256=reference_receipt.source_sha256,
    )


def validate_pack_grounding(source: bytes, *, role: str) -> PackGroundingReceipt:
    """Check grounding metadata without judging whether the citation is apt."""

    if type(source) is not bytes:
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.MALFORMED_SOURCE,
            "source must be exact bytes",
        )
    if role not in _ROLES:
        raise PackGroundingRefusal(
            PackGroundingRefusalReason.UNKNOWN_ROLE,
            f"unknown grounding role: {role!r}",
        )
    document = _document(source)
    source_id = _nonblank(document.get("id"), "schema.id")
    grounded: list[str] = []
    if role == "PACK":
        _grounding(document.get("annotations"), source_id)
        grounded.append(source_id)
    else:
        classes = _mapping(document.get("classes", {}), "schema.classes")
        for name, raw_class in classes.items():
            body = _mapping(raw_class, f"classes.{name}")
            if body.get("is_a") not in _ROOT_PARENTS:
                continue
            try:
                _grounding(body.get("annotations"), str(name))
            except PackGroundingRefusal as error:
                if error.reason is PackGroundingRefusalReason.GROUNDING_REQUIRED:
                    raise PackGroundingRefusal(
                        PackGroundingRefusalReason.DIRECT_ROOT_GROUNDING_REQUIRED,
                        f"project class {name} extends {body['is_a']} directly",
                    ) from error
                raise
            grounded.append(str(name))
    return PackGroundingReceipt(
        role=role,
        source_id=source_id,
        source_sha256=_digest_bytes(source),
        rite_identity=PACK_GROUNDING_RITE_IDENTITY,
        grounded_subjects=tuple(sorted(grounded)),
    )


__all__ = (
    "PACK_GROUNDING_RITE_IDENTITY",
    "PackConformanceReceipt",
    "PackGroundingReceipt",
    "PackGroundingRefusal",
    "PackGroundingRefusalReason",
    "validate_pack_conformance",
    "validate_pack_grounding",
)

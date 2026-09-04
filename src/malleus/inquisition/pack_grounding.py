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
            "root_namespace",
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
        for field in ("root_namespace", "annotation_key", "annotation_tag"):
            if not isinstance(rite[field], str) or not rite[field]:
                raise ValueError(f"{field} must be nonempty text")
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise RuntimeError(f"pack-grounding rite is invalid: {error}") from error
    return MappingProxyType(dict(rite)), _digest_bytes(raw)


_RITE, PACK_GROUNDING_RITE_IDENTITY = _load_rite()
_ROLES = frozenset(_RITE["roles"])
_ROOT_PARENTS = frozenset(_RITE["root_parents"])
_ROOT_NAMESPACE = str(_RITE["root_namespace"])
_CITED_FIELDS = frozenset(_RITE["cited_fields"])
_CITED_WITH_INVENTIONS_FIELDS = frozenset(_RITE["cited_with_inventions_fields"])
_VOCABULARY_FIELDS = frozenset(_RITE["vocabulary_fields"])
_NONE_FOUND_FIELDS = frozenset(_RITE["none_found_fields"])
_ROOT_FORMS = "closed forms: " + " | ".join(
    "+".join(str(field) for field in _RITE[name])
    for name in ("cited_fields", "cited_with_inventions_fields", "none_found_fields")
)
_ENTRY_FORM = "closed form: " + "+".join(
    str(field) for field in _RITE["vocabulary_fields"]
)
_ANNOTATION_FORM = "closed form: tag+value"


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


@dataclass(frozen=True, slots=True)
class _Defect:
    """One ill-formed grounding position, its reason, and the form it must take."""

    subject: str
    ordinal: int
    reason: PackGroundingRefusalReason
    message: str
    expected: str

    @property
    def order(self) -> tuple[str, int, str]:
        return (self.subject, self.ordinal, self.message)

    def render(self) -> str:
        return f"{self.message} [{self.reason.name}] {self.expected}"


def _note(
    defects: list[_Defect],
    subject: str,
    ordinal: int,
    reason: PackGroundingRefusalReason,
    message: str,
    expected: str,
) -> None:
    defects.append(_Defect(subject, ordinal, reason, message, expected))


def _refuse_defects(defects: list[_Defect]) -> PackGroundingRefusal:
    ordered = sorted(defects, key=lambda defect: defect.order)
    return PackGroundingRefusal(
        ordered[0].reason,
        "grounding blocks are not accepted: "
        + "; ".join(defect.render() for defect in ordered),
    )


def _string_mapping(value: object) -> Mapping[str, object] | None:
    if not isinstance(value, Mapping) or not all(
        isinstance(key, str) for key in value
    ):
        return None
    return value


def _check_text(
    value: object,
    where: str,
    *,
    subject: str,
    ordinal: int,
    expected: str,
    defects: list[_Defect],
) -> bool:
    if not isinstance(value, str) or not value.strip():
        _note(
            defects,
            subject,
            ordinal,
            PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
            f"{where} must be nonblank text",
            expected,
        )
        return False
    return True


def _check_terms(
    value: object,
    where: str,
    *,
    nonempty: bool,
    subject: str,
    ordinal: int,
    expected: str,
    defects: list[_Defect],
) -> tuple[str, ...] | None:
    if (
        not isinstance(value, list)
        or any(not isinstance(item, str) or not item.strip() for item in value)
        or len(value) != len(set(value))
        or (nonempty and not value)
    ):
        qualifier = "nonempty " if nonempty else ""
        _note(
            defects,
            subject,
            ordinal,
            PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
            f"{where} must be a {qualifier}unique string list",
            expected,
        )
        return None
    return tuple(value)


def _check_vocabularies(
    value: object,
    subject: str,
    defects: list[_Defect],
) -> None:
    where = f"{subject}.grounding.vocabularies"
    if not isinstance(value, list) or not value:
        _note(
            defects,
            subject,
            -1,
            PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
            f"{where} must be a nonempty list",
            _ENTRY_FORM,
        )
        return
    seen: dict[tuple[str, str], int] = {}
    for ordinal, raw_vocabulary in enumerate(value):
        position = f"{where}[{ordinal}]"
        vocabulary = _string_mapping(raw_vocabulary)
        if vocabulary is None:
            _note(
                defects,
                subject,
                ordinal,
                PackGroundingRefusalReason.MALFORMED_SOURCE,
                f"{position} must be a mapping with string keys",
                _ENTRY_FORM,
            )
            continue
        if set(vocabulary) != _VOCABULARY_FIELDS:
            _note(
                defects,
                subject,
                ordinal,
                PackGroundingRefusalReason.GROUNDING_NOT_CLOSED,
                f"{position} fields are not closed",
                _ENTRY_FORM,
            )
            continue
        named = _check_text(
            vocabulary["vocabulary"],
            f"{position}.vocabulary",
            subject=subject,
            ordinal=ordinal,
            expected=_ENTRY_FORM,
            defects=defects,
        )
        located = _check_text(
            vocabulary["vocabulary_url"],
            f"{position}.vocabulary_url",
            subject=subject,
            ordinal=ordinal,
            expected=_ENTRY_FORM,
            defects=defects,
        )
        if located and not urlsplit(str(vocabulary["vocabulary_url"])).scheme:
            _note(
                defects,
                subject,
                ordinal,
                PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
                f"{position}.vocabulary_url must be an absolute locator",
                _ENTRY_FORM,
            )
            located = False
        if named and located:
            identity = (
                str(vocabulary["vocabulary"]),
                str(vocabulary["vocabulary_url"]),
            )
            if identity in seen:
                _note(
                    defects,
                    subject,
                    ordinal,
                    PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
                    f"{position} repeats the vocabulary identity of "
                    f"{where}[{seen[identity]}]",
                    _ENTRY_FORM,
                )
            else:
                seen[identity] = ordinal
        _check_terms(
            vocabulary["borrowed_terms"],
            f"{position}.borrowed_terms",
            nonempty=True,
            subject=subject,
            ordinal=ordinal,
            expected=_ENTRY_FORM,
            defects=defects,
        )


def _grounding_defects(annotations: object, subject: str) -> list[_Defect] | None:
    """Collect every defect in one subject's grounding block.

    ``None`` means the block is absent, which the caller reports as its own
    reason. An empty list means the block is well formed.
    """

    if annotations is None:
        return None
    defects: list[_Defect] = []
    values = _string_mapping(annotations)
    if values is None:
        _note(
            defects,
            subject,
            -1,
            PackGroundingRefusalReason.MALFORMED_SOURCE,
            f"{subject}.annotations must be a mapping with string keys",
            _ANNOTATION_FORM,
        )
        return defects
    key = str(_RITE["annotation_key"])
    if key not in values:
        return None
    annotation = _string_mapping(values[key])
    if annotation is None:
        _note(
            defects,
            subject,
            -1,
            PackGroundingRefusalReason.MALFORMED_SOURCE,
            f"{subject}.annotations.{key} must be a mapping with string keys",
            _ANNOTATION_FORM,
        )
        return defects
    if set(annotation) != {"tag", "value"}:
        _note(
            defects,
            subject,
            -1,
            PackGroundingRefusalReason.GROUNDING_NOT_CLOSED,
            f"{subject} grounding annotation must contain exactly tag and value",
            _ANNOTATION_FORM,
        )
        return defects
    if annotation["tag"] != _RITE["annotation_tag"]:
        _note(
            defects,
            subject,
            -1,
            PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
            f"{subject} grounding annotation has the wrong tag",
            _ANNOTATION_FORM,
        )
    grounding = _string_mapping(annotation["value"])
    if grounding is None:
        _note(
            defects,
            subject,
            -1,
            PackGroundingRefusalReason.MALFORMED_SOURCE,
            f"{subject}.grounding.value must be a mapping with string keys",
            _ROOT_FORMS,
        )
        return defects
    fields = set(grounding)
    if fields in {_CITED_FIELDS, _CITED_WITH_INVENTIONS_FIELDS}:
        _check_text(
            grounding["area"],
            f"{subject}.grounding.area",
            subject=subject,
            ordinal=-1,
            expected=_ROOT_FORMS,
            defects=defects,
        )
        _check_text(
            grounding["taxonomy"],
            f"{subject}.grounding.taxonomy",
            subject=subject,
            ordinal=-1,
            expected=_ROOT_FORMS,
            defects=defects,
        )
        _check_vocabularies(grounding["vocabularies"], subject, defects)
        invented = _check_terms(
            grounding["invented_terms"],
            f"{subject}.grounding.invented_terms",
            nonempty=False,
            subject=subject,
            ordinal=-1,
            expected=_ROOT_FORMS,
            defects=defects,
        )
        has_search = fields == _CITED_WITH_INVENTIONS_FIELDS
        if invented is not None and bool(invented) != has_search:
            _note(
                defects,
                subject,
                -1,
                PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
                f"{subject} must pair invented terms with invention_search",
                _ROOT_FORMS,
            )
        if has_search:
            _check_text(
                grounding["invention_search"],
                f"{subject}.grounding.invention_search",
                subject=subject,
                ordinal=-1,
                expected=_ROOT_FORMS,
                defects=defects,
            )
        return defects
    if fields == _NONE_FOUND_FIELDS:
        _check_text(
            grounding["area"],
            f"{subject}.grounding.area",
            subject=subject,
            ordinal=-1,
            expected=_ROOT_FORMS,
            defects=defects,
        )
        _check_text(
            grounding["taxonomy"],
            f"{subject}.grounding.taxonomy",
            subject=subject,
            ordinal=-1,
            expected=_ROOT_FORMS,
            defects=defects,
        )
        if grounding["none_found"] is not True:
            _note(
                defects,
                subject,
                -1,
                PackGroundingRefusalReason.GROUNDING_INCOMPLETE,
                f"{subject}.grounding.none_found must be literal true",
                _ROOT_FORMS,
            )
        _check_text(
            grounding["search"],
            f"{subject}.grounding.search",
            subject=subject,
            ordinal=-1,
            expected=_ROOT_FORMS,
            defects=defects,
        )
        _check_terms(
            grounding["invented_terms"],
            f"{subject}.grounding.invented_terms",
            nonempty=True,
            subject=subject,
            ordinal=-1,
            expected=_ROOT_FORMS,
            defects=defects,
        )
        return defects
    _note(
        defects,
        subject,
        -1,
        PackGroundingRefusalReason.GROUNDING_NOT_CLOSED,
        f"{subject} grounding fields are not one supported closed form",
        _ROOT_FORMS,
    )
    return defects


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


def _direct_root_parent(
    value: object,
    prefixes: Mapping[str, object],
) -> str | None:
    if not isinstance(value, str):
        return None
    if value in _ROOT_PARENTS:
        return value
    prefix, separator, local = value.partition(":")
    if not separator or local not in _ROOT_PARENTS:
        return None
    return local if prefixes.get(prefix) == _ROOT_NAMESPACE else None


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

    Documentation may change and declarations may be added. Reference imports
    remain one unique set. Existing class, slot, and enum declarations may not
    be removed or weakened.
    """

    source_receipt = validate_pack_grounding(source, role="PACK")
    reference_receipt = validate_pack_grounding(reference, role="PACK")
    source_document = _document(source)
    reference_document = _document(reference)
    missing = _missing_surface(
        reference_document.get("imports", []),
        source_document.get("imports", []),
        "imports",
    )
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
        defects = _grounding_defects(document.get("annotations"), source_id)
        if defects is None:
            raise PackGroundingRefusal(
                PackGroundingRefusalReason.GROUNDING_REQUIRED,
                f"{source_id} has no grounding annotation",
            )
        if defects:
            raise _refuse_defects(defects)
        grounded.append(source_id)
    else:
        classes = _mapping(document.get("classes", {}), "schema.classes")
        prefixes = _mapping(document.get("prefixes", {}), "schema.prefixes")
        missing: list[tuple[str, str]] = []
        defects = []
        for name, raw_class in classes.items():
            body = _mapping(raw_class, f"classes.{name}")
            root_parent = _direct_root_parent(body.get("is_a"), prefixes)
            if root_parent is None:
                continue
            found = _grounding_defects(body.get("annotations"), str(name))
            if found is None:
                missing.append((str(name), root_parent))
                continue
            if found:
                defects.extend(found)
                continue
            grounded.append(str(name))
        if defects:
            raise _refuse_defects(defects)
        if missing:
            detail = "; ".join(
                f"{name} extends {parent}" for name, parent in sorted(missing)
            )
            raise PackGroundingRefusal(
                PackGroundingRefusalReason.DIRECT_ROOT_GROUNDING_REQUIRED,
                "project classes extend Malleus roots without grounding: " + detail,
            )
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

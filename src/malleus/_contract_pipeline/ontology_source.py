"""The LinkML source a compiled contract was compiled from, held explicitly.

A history holds its validated contract and never the source behind it. That is
enough to admit knowledge and to replay, and it is not enough to compose an
addition: composing needs the root the contract came from. This module gives the
source set a grammar, an identity derived from its own bytes, and a place in the
ledger, and it gives one proposal's Core-derived compilation the same.

Two closed grammars:

``malleus.ontology-source-set/v1``
    The root locator, every module's locator, media type, byte length and
    sha256, the compiler execution that produced the contract, and the validated
    contract identity the set reproduces. The module bytes themselves are
    retained as ordinary artifacts and the fold checks that every digest the set
    names is in the history.

``malleus.ontology-revision-target/v1``
    What Core derived for one proposal: the composed root's digest, the source
    set it composed onto, and the two exact contract artifacts the revision
    would install. The proposer supplies none of it, which is what lets a
    proposer hold no compiler, and acceptance reads it instead of compiling,
    which is what lets acceptance hold none either.

Both records carry their identity in their record ID, so a record cannot be
retained under a name that is not its own bytes (architectural law 8).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from hashlib import sha256
import json
from typing import Mapping

from malleus._contract_pipeline.model import canonical_json


ONTOLOGY_SOURCE_SET_GRAMMAR = "malleus.ontology-source-set/v1"
ONTOLOGY_REVISION_TARGET_GRAMMAR = "malleus.ontology-revision-target/v1"
ONTOLOGY_SOURCE_MEDIA_TYPE = "application/yaml"

ONTOLOGY_SOURCE_RECORD_PREFIX = "ontology-source:"
ONTOLOGY_SOURCE_SET_RECORD_PREFIX = "ontology-source-set:"
ONTOLOGY_REVISION_TARGET_RECORD_PREFIX = "ontology-revision-target:"

_SOURCE_SET_FIELDS = frozenset(
    {
        "compiler_execution_identity",
        "grammar",
        "modules",
        "root_locator",
        "validated_contract_identity",
    }
)
_MODULE_FIELDS = frozenset({"byte_length", "locator", "media_type", "sha256"})
_TARGET_FIELDS = frozenset(
    {
        "composed_root_sha256",
        "grammar",
        "partial_contract",
        "proposal_identity",
        "source_set_identity",
        "validated_contract",
    }
)
_SOURCE_SET_MARKER = ONTOLOGY_SOURCE_SET_GRAMMAR.encode("utf-8")
_TARGET_MARKER = ONTOLOGY_REVISION_TARGET_GRAMMAR.encode("utf-8")


class OntologySourceRefusalReason(Enum):
    """Every way holding or reading the ontology source fails closed."""

    MALFORMED_SOURCE_SET = auto()
    MALFORMED_REVISION_TARGET = auto()
    ONTOLOGY_SOURCE_NOT_RETAINED = auto()
    ONTOLOGY_SOURCE_ALREADY_RETAINED = auto()
    ONTOLOGY_SOURCE_BYTES_NOT_RETAINED = auto()
    ONTOLOGY_SOURCE_DOES_NOT_REPRODUCE_CONTRACT = auto()
    REVISION_TARGET_SOURCE_SET_NOT_CURRENT = auto()


class OntologySourceRefusal(ValueError):
    def __init__(self, reason: OntologySourceRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


def refuse(reason: OntologySourceRefusalReason, detail: str) -> OntologySourceRefusal:
    return OntologySourceRefusal(reason, detail)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _is_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 71
        and value.startswith("sha256:")
        and all(character in "0123456789abcdef" for character in value[7:])
    )


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} is required")
    return value


def _identity(value: object, label: str) -> str:
    if not _is_digest(value):
        raise ValueError(f"{label} must be a SHA-256 digest")
    assert isinstance(value, str)
    return value


@dataclass(frozen=True, slots=True)
class OntologySourceModule:
    """One module of a compiled source set, named by its own bytes."""

    byte_length: int
    locator: str
    media_type: str
    sha256: str


@dataclass(frozen=True, slots=True)
class OntologySourceSet:
    """The exact LinkML source set one validated contract was compiled from."""

    canonical_bytes: bytes
    identity: str
    record_id: str
    root_locator: str
    modules: tuple[OntologySourceModule, ...]
    compiler_execution_identity: str
    validated_contract_identity: str

    @property
    def root_sha256(self) -> str:
        for module in self.modules:
            if module.locator == self.root_locator:
                return module.sha256
        raise refuse(
            OntologySourceRefusalReason.MALFORMED_SOURCE_SET,
            "a source set names its own root module",
        )

    @classmethod
    def compose(
        cls,
        *,
        root_locator: str,
        sources: Mapping[str, bytes],
        compiler_execution_identity: str,
        validated_contract_identity: str,
    ) -> OntologySourceSet:
        if root_locator not in sources:
            raise refuse(
                OntologySourceRefusalReason.MALFORMED_SOURCE_SET,
                f"the source map does not carry the root locator: {root_locator}",
            )
        return cls.from_bytes(
            canonical_json(
                {
                    "compiler_execution_identity": compiler_execution_identity,
                    "grammar": ONTOLOGY_SOURCE_SET_GRAMMAR,
                    "modules": [
                        {
                            "byte_length": len(content),
                            "locator": locator,
                            "media_type": ONTOLOGY_SOURCE_MEDIA_TYPE,
                            "sha256": _digest(content),
                        }
                        for locator, content in sorted(sources.items())
                    ],
                    "root_locator": root_locator,
                    "validated_contract_identity": validated_contract_identity,
                }
            )
        )

    @classmethod
    def from_bytes(cls, source: bytes) -> OntologySourceSet:
        if type(source) is not bytes:
            raise refuse(
                OntologySourceRefusalReason.MALFORMED_SOURCE_SET,
                "source set input must be exact bytes",
            )
        try:
            data = json.loads(source)
            if not isinstance(data, dict):
                raise ValueError("source set root must be an object")
            if canonical_json(data) != source:
                raise ValueError("source set bytes are not canonical")
            if set(data) != _SOURCE_SET_FIELDS:
                raise ValueError("source set fields are not closed")
            if data["grammar"] != ONTOLOGY_SOURCE_SET_GRAMMAR:
                raise ValueError("source set grammar is unsupported")
            raw_modules = data["modules"]
            if not isinstance(raw_modules, list) or not raw_modules:
                raise ValueError("a source set holds at least one module")
            modules: list[OntologySourceModule] = []
            for entry in raw_modules:
                if not isinstance(entry, dict) or set(entry) != _MODULE_FIELDS:
                    raise ValueError("module fields are not closed")
                length = entry["byte_length"]
                if (
                    not isinstance(length, int)
                    or isinstance(length, bool)
                    or length < 0
                ):
                    raise ValueError("module byte length must be a whole number")
                modules.append(
                    OntologySourceModule(
                        length,
                        _text(entry["locator"], "module locator"),
                        _text(entry["media_type"], "module media type"),
                        _identity(entry["sha256"], "module digest"),
                    )
                )
            locators = [module.locator for module in modules]
            if locators != sorted(set(locators)):
                raise ValueError("modules must be sorted by locator and unique")
            root_locator = _text(data["root_locator"], "root locator")
            if root_locator not in locators:
                raise ValueError("the root locator must name one of the modules")
            digest = _digest(source)
            return cls(
                source,
                digest,
                ONTOLOGY_SOURCE_SET_RECORD_PREFIX + digest,
                root_locator,
                tuple(modules),
                _identity(
                    data["compiler_execution_identity"], "compiler execution identity"
                ),
                _identity(
                    data["validated_contract_identity"], "validated contract identity"
                ),
            )
        except OntologySourceRefusal:
            raise
        except (TypeError, ValueError) as error:
            raise refuse(
                OntologySourceRefusalReason.MALFORMED_SOURCE_SET, str(error)
            ) from error


@dataclass(frozen=True, slots=True)
class OntologyRevisionTarget:
    """What Core derived for one proposal, so nobody else needs a compiler."""

    canonical_bytes: bytes
    identity: str
    record_id: str
    proposal_identity: str
    source_set_identity: str
    composed_root_sha256: str
    validated_contract_bytes: bytes
    partial_contract_bytes: bytes

    @classmethod
    def compose(
        cls,
        *,
        proposal_identity: str,
        source_set_identity: str,
        composed_root_sha256: str,
        validated_contract_bytes: bytes,
        partial_contract_bytes: bytes,
    ) -> OntologyRevisionTarget:
        try:
            validated = json.loads(validated_contract_bytes)
            partial = json.loads(partial_contract_bytes)
        except (TypeError, ValueError) as error:
            raise refuse(
                OntologySourceRefusalReason.MALFORMED_REVISION_TARGET,
                "the derived contract artifacts must be canonical JSON objects",
            ) from error
        return cls.from_bytes(
            canonical_json(
                {
                    "composed_root_sha256": composed_root_sha256,
                    "grammar": ONTOLOGY_REVISION_TARGET_GRAMMAR,
                    "partial_contract": partial,
                    "proposal_identity": proposal_identity,
                    "source_set_identity": source_set_identity,
                    "validated_contract": validated,
                }
            )
        )

    @classmethod
    def from_bytes(cls, source: bytes) -> OntologyRevisionTarget:
        if type(source) is not bytes:
            raise refuse(
                OntologySourceRefusalReason.MALFORMED_REVISION_TARGET,
                "revision target input must be exact bytes",
            )
        try:
            data = json.loads(source)
            if not isinstance(data, dict):
                raise ValueError("revision target root must be an object")
            if canonical_json(data) != source:
                raise ValueError("revision target bytes are not canonical")
            if set(data) != _TARGET_FIELDS:
                raise ValueError("revision target fields are not closed")
            if data["grammar"] != ONTOLOGY_REVISION_TARGET_GRAMMAR:
                raise ValueError("revision target grammar is unsupported")
            validated = data["validated_contract"]
            partial = data["partial_contract"]
            if not isinstance(validated, dict) or not isinstance(partial, dict):
                raise ValueError("derived contract artifacts must be objects")
            digest = _digest(source)
            return cls(
                source,
                digest,
                ONTOLOGY_REVISION_TARGET_RECORD_PREFIX + digest,
                _identity(data["proposal_identity"], "proposal identity"),
                _identity(data["source_set_identity"], "source set identity"),
                _identity(data["composed_root_sha256"], "composed root digest"),
                canonical_json(validated),
                canonical_json(partial),
            )
        except OntologySourceRefusal:
            raise
        except (TypeError, ValueError) as error:
            raise refuse(
                OntologySourceRefusalReason.MALFORMED_REVISION_TARGET, str(error)
            ) from error


def _claims(content: bytes, marker: bytes, grammar: str) -> bool:
    if marker not in content:
        return False
    try:
        data = json.loads(content)
    except (UnicodeDecodeError, ValueError):
        return False
    return isinstance(data, dict) and data.get("grammar") == grammar


def read_source_set(record_id: str, content: bytes) -> OntologySourceSet | None:
    """The source set one retained input declares, or ``None``.

    Bytes that claim the grammar are read as a source set and refused if they
    are not one, so a malformed record never hides behind its own malformation.
    """

    if not _claims(content, _SOURCE_SET_MARKER, ONTOLOGY_SOURCE_SET_GRAMMAR):
        return None
    source_set = OntologySourceSet.from_bytes(content)
    if source_set.record_id != record_id:
        raise refuse(
            OntologySourceRefusalReason.MALFORMED_SOURCE_SET,
            "a source set's record ID is its own digest: "
            f"{record_id} holds {source_set.record_id}",
        )
    return source_set


def read_revision_target(
    record_id: str, content: bytes
) -> OntologyRevisionTarget | None:
    """The derived revision target one retained input declares, or ``None``."""

    if not _claims(content, _TARGET_MARKER, ONTOLOGY_REVISION_TARGET_GRAMMAR):
        return None
    target = OntologyRevisionTarget.from_bytes(content)
    if target.record_id != record_id:
        raise refuse(
            OntologySourceRefusalReason.MALFORMED_REVISION_TARGET,
            "a revision target's record ID is its own digest: "
            f"{record_id} holds {target.record_id}",
        )
    return target


__all__ = (
    "ONTOLOGY_REVISION_TARGET_GRAMMAR",
    "ONTOLOGY_REVISION_TARGET_RECORD_PREFIX",
    "ONTOLOGY_SOURCE_MEDIA_TYPE",
    "ONTOLOGY_SOURCE_RECORD_PREFIX",
    "ONTOLOGY_SOURCE_SET_GRAMMAR",
    "ONTOLOGY_SOURCE_SET_RECORD_PREFIX",
    "OntologyRevisionTarget",
    "OntologySourceModule",
    "OntologySourceRefusal",
    "OntologySourceRefusalReason",
    "OntologySourceSet",
    "read_revision_target",
    "read_source_set",
)

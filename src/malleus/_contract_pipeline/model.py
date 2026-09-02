"""Frozen values for the private validated-contract pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto
from hashlib import sha256
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from malleus._contract_compiler import ContractFact, NeutralContract


FACT_NAMESPACE = "https://malleus.dev/contract-facts/"
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
RDFS_SUBCLASS = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
ARTIFACT_GRAMMAR = "malleus.validated-contract-artifact/private-v0"
ARTIFACT_CAPABILITY = "VALIDATED_FACTS_AND_STRUCTURAL_VIEW_ONLY"
SEED_METAMODEL_ID = (
    "urn:malleus:contract-metamodel:non-expression-seed:v0:sha256:"
    "1c68a612f3e7a0f80c31965aa5525954921dfbee60d151552d10d61cb0aac71b"
)
EXPRESSION_METAMODEL_ID = (
    "urn:malleus:contract-metamodel:expression-capable:v0:sha256:"
    "65aae23b7a0892a4d2ae2b5adc6888f1ddd39c94ce03f412d50a6a5ccd5d0964"
)
CANONICALIZATION_ID = (
    "malleus.canonical-json/d05-compact-sorted-key-utf8-no-newline/v0"
)
SYMBOL_POLICY_ID = (
    "urn:malleus:contract-symbol-policy:linkml-v0-slash-qualified:v0"
)
PRODUCER_ID = "malleus.contract-pipeline/python-private-v0"


def canonical_json(value: object) -> bytes:
    """Encode the exact compact sorted-key UTF-8 grammar."""

    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def digest(value: object) -> str:
    return "sha256:" + sha256(canonical_json(value)).hexdigest()


_CANONICALIZATION_DESCRIPTOR = {
    "encoding": "utf-8",
    "fact_array_order": "canonical-record-bytes-ascending",
    "id": CANONICALIZATION_ID,
    "json": "compact-sorted-keys-no-newline",
}
_SYMBOL_POLICY_DESCRIPTOR = {
    "authoritative_resolution": "exact-retained-closure",
    "declaration_join": "slash",
    "id": SYMBOL_POLICY_ID,
    "ownership_exception": "explicit-imported-global-slot-adoption",
}
def metamodel(identity: str) -> dict[str, str]:
    if identity not in {SEED_METAMODEL_ID, EXPRESSION_METAMODEL_ID}:
        raise ValueError("unknown internal contract metamodel")
    return {"id": identity, "sha256": "sha256:" + identity.rsplit(":", 1)[-1]}
CANONICALIZATION = {
    "id": CANONICALIZATION_ID,
    "sha256": digest(_CANONICALIZATION_DESCRIPTOR),
}
SYMBOL_POLICY = {
    "id": SYMBOL_POLICY_ID,
    "sha256": digest(_SYMBOL_POLICY_DESCRIPTOR),
}


class ElaborationRefusalReason(Enum):
    """Closed refusal classes for the measured elaboration subset."""

    MALFORMED_BINDING = auto()
    UNSUPPORTED_CONSTRUCT = auto()
    INHERITANCE_CYCLE = auto()
    REPEATED_MIXIN = auto()
    MIXIN_TARGET_NOT_MIXIN = auto()
    MIXIN_CONFLICT = auto()
    AMBIGUOUS_APPLICABLE_SLOT = auto()
    SLOT_USAGE_NOT_APPLICABLE = auto()
    INVALID_RANGE = auto()
    MULTIPLE_IDENTIFIER_SLOTS = auto()
    CONTRADICTORY_CONSTRAINT = auto()
    INVALID_EXPRESSION = auto()
    INVALID_FACT_SET = auto()


class ElaborationRefusal(ValueError):
    def __init__(self, reason: ElaborationRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


class ArtifactRefusalReason(Enum):
    """Closed refusal classes for the private validated-fact artifact."""

    MALFORMED_ARTIFACT = auto()
    UNSUPPORTED_ARTIFACT_GRAMMAR = auto()
    ARTIFACT_INTEGRITY_MISMATCH = auto()
    INVALID_FACT_SET = auto()


class ArtifactRefusal(ValueError):
    def __init__(self, reason: ArtifactRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


@dataclass(frozen=True, slots=True)
class EffectiveConstraints:
    """One fully resolved Slot or SlotUse constraint set."""

    range_id: str
    required: bool
    multivalued: bool
    identifier: bool
    inlined: bool
    equals_string: str | None = None
    minimum: str | None = None
    maximum: str | None = None
    value_presence: str | None = None

    @property
    def range(self) -> str:
        return self.range_id

    @property
    def minimum_value(self) -> Decimal | None:
        return None if self.minimum is None else Decimal(self.minimum)

    @property
    def maximum_value(self) -> Decimal | None:
        return None if self.maximum is None else Decimal(self.maximum)


@dataclass(frozen=True, slots=True)
class ElaboratedClass:
    identifier: str
    parent_id: str | None
    mixin_ids: tuple[str, ...]
    is_mixin: bool
    abstract: bool


@dataclass(frozen=True, slots=True)
class ElaboratedSlot:
    identifier: str
    constraints: EffectiveConstraints


@dataclass(frozen=True, slots=True)
class ElaboratedSlotUse:
    identifier: str
    class_id: str
    slot_id: str
    constraints: EffectiveConstraints


@dataclass(frozen=True, slots=True)
class ElaboratedEnum:
    identifier: str
    values: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ElaboratedScalar:
    identifier: str
    typeof_id: str


@dataclass(frozen=True, slots=True)
class ElaboratedCondition:
    slot_id: str
    required: bool | None
    equals_string: str | None
    value_presence: str | None


@dataclass(frozen=True, slots=True)
class ElaboratedAlternative:
    conditions: tuple[ElaboratedCondition, ...]


@dataclass(frozen=True, slots=True)
class ElaboratedExpressionGroup:
    class_id: str
    alternatives: tuple[ElaboratedAlternative, ...]


@dataclass(frozen=True, slots=True)
class ElaboratedContract:
    """Frontend-neutral measured subset before canonical fact encoding."""

    classes: tuple[ElaboratedClass, ...]
    slots: tuple[ElaboratedSlot, ...]
    slot_uses: tuple[ElaboratedSlotUse, ...]
    enums: tuple[ElaboratedEnum, ...]
    scalars: tuple[ElaboratedScalar, ...]
    expression_groups: tuple[ElaboratedExpressionGroup, ...]
    adapter_profile_id: str
    adapter_profile_sha256: str
    binder_profile_id: str
    binder_profile_sha256: str
    metamodel_id: str
    symbol_policy_id: str


@dataclass(frozen=True, slots=True)
class ResolverEvidence:
    resolver_id: str
    profile_version: str
    configuration_id: str


@dataclass(frozen=True, slots=True)
class RootEvidence:
    requested_locator: str
    resolved_locator: str
    source_sha256: str
    resolver: ResolverEvidence


@dataclass(frozen=True, slots=True)
class SourceEvidence:
    module_id: str
    schema_id: str
    byte_length: int
    sha256: str
    media_type: str
    trusted: bool
    resolver: ResolverEvidence


@dataclass(frozen=True, slots=True)
class AnnotationEvidence:
    module_id: str
    path: tuple[str | int, ...]
    canonical_value: bytes


@dataclass(frozen=True, slots=True)
class ImportEvidence:
    parent_module_id: str
    ordinal: int
    literal: str
    child_module_id: str
    resolver: ResolverEvidence


@dataclass(frozen=True, slots=True)
class ArtifactEvidence:
    selection: ResolverEvidence
    root: RootEvidence
    sources: tuple[SourceEvidence, ...]
    annotations: tuple[AnnotationEvidence, ...]
    imports: tuple[ImportEvidence, ...]
    adapter_profile_id: str
    adapter_profile_sha256: str
    binder_profile_id: str
    binder_profile_sha256: str
    producer_id: str
    producer_sha256: str


@dataclass(frozen=True, slots=True)
class ValidatedContractArtifact:
    grammar: str
    capability: str
    canonical_facts: bytes
    facts_sha256: str
    validated_fact_set_sha256: str
    fact_count: int
    evidence: ArtifactEvidence
    evidence_sha256: str
    artifact_bytes: bytes

    @property
    def content_hash(self) -> str:
        return self.validated_fact_set_sha256.removeprefix("sha256:")


@dataclass(frozen=True, slots=True)
class ValidatedContractCompilation:
    elaborated: ElaboratedContract
    contract: NeutralContract
    facts: tuple[ContractFact, ...]
    canonical_facts: bytes
    facts_sha256: str
    content_hash: str
    artifact: ValidatedContractArtifact
    view: object
    source: object
    implementation: object

    @staticmethod
    def fact_bytes(fact: ContractFact) -> bytes:
        return canonical_json(fact.as_dict())

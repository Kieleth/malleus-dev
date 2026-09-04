"""Strict paper-local bridge from GraphRecipe plans to knowledge changes."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from malleus._contract_pipeline.knowledge import (
    KnowledgeChangeSet,
    KnowledgeOperation,
    KnowledgeValidTime,
)
from malleus.ledger import GENESIS, canonical_json

from ..graph_recipe.assembly import AssemblyPlan


_DIGEST_PREFIX = "sha256:"
_HEX = frozenset("0123456789abcdef")
_CHANGE_GRAMMAR = "malleus.knowledge-change-set/private-v0"
_CONTRACT_KIND = "PRIVATE_PARTIAL_EFFECTIVE_CONTRACT_V0"
_MEMBER_OPERATION_TYPES = {
    "https://malleus.dev/graph-recipe/base/CreateEntity": "CREATE_ENTITY",
    "https://malleus.dev/graph-recipe/base/CreateRelation": "CREATE_RELATION",
    "https://malleus.dev/graph-recipe/base/CreateSignal": "CREATE_SIGNAL",
    "https://malleus.dev/graph-recipe/base/CreateEvent": "CREATE_EVENT",
}
_SUPPORTED_OPERATION_TYPES = frozenset({"CREATE_ENTITY", "CREATE_RELATION"})


class GraphRecipeChangeSetError(ValueError):
    """The GraphRecipe plan cannot enter the private knowledge history."""


def _is_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and value.startswith(_DIGEST_PREFIX)
        and len(value) == 71
        and all(character in _HEX for character in value[7:])
    )


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GraphRecipeChangeSetError(f"{label} must be nonblank text")
    return value


def _require_digest(value: object, label: str) -> str:
    if not _is_digest(value):
        raise GraphRecipeChangeSetError(f"{label} must be a sha256 digest")
    assert isinstance(value, str)
    return value


def _require_head(value: object, label: str) -> str:
    if value != GENESIS and not _is_digest(value):
        raise GraphRecipeChangeSetError(f"{label} must be GENESIS or a sha256 digest")
    assert isinstance(value, str)
    return value


@dataclass(frozen=True, slots=True)
class RetainedReference:
    """One retained source or evidence artifact named by exact bytes."""

    record_id: str
    sha256: str

    def __post_init__(self) -> None:
        _require_text(self.record_id, "retained record_id")
        _require_digest(self.sha256, "retained sha256")


@dataclass(frozen=True, slots=True)
class HistoryBaseCoordinates:
    """The exact accepted-history position against which a change is proposed."""

    ledger_head: str
    ledger_event_count: int
    acceptance_head: str
    materialization_head: str
    accepted_state_digest: str

    def __post_init__(self) -> None:
        _require_head(self.ledger_head, "base ledger_head")
        if type(self.ledger_event_count) is not int or self.ledger_event_count < 0:
            raise GraphRecipeChangeSetError(
                "base ledger_event_count must be a nonnegative integer"
            )
        if (self.ledger_event_count == 0) != (self.ledger_head == GENESIS):
            raise GraphRecipeChangeSetError(
                "base ledger_head and ledger_event_count disagree"
            )
        _require_head(self.acceptance_head, "base acceptance_head")
        _require_head(self.materialization_head, "base materialization_head")
        _require_digest(
            self.accepted_state_digest,
            "base accepted_state_digest",
        )


def canonical_assembly_plan_bytes(plan: AssemblyPlan) -> bytes:
    """Return the exact retained bytes whose digest is ``plan.plan_digest``."""

    if not isinstance(plan, AssemblyPlan):
        raise GraphRecipeChangeSetError("plan must be an AssemblyPlan")
    value = {
        "schema_version": "graph-recipe-plan-v0",
        "contract_digest": plan.contract_digest,
        "invocation_digests": list(plan.invocation_digests),
        "member_graph": plan.member_graph_artifact(),
        "proposed_operations": plan.proposed_operations_artifact(),
    }
    source = canonical_json(value).encode("utf-8")
    actual = _DIGEST_PREFIX + sha256(source).hexdigest()
    if actual != plan.plan_digest:
        raise GraphRecipeChangeSetError("plan fields do not reproduce plan.plan_digest")
    return source


def _closure(
    values: tuple[RetainedReference, ...],
    *,
    id_field: str,
    label: str,
) -> list[dict[str, str]]:
    if not isinstance(values, tuple) or not values:
        raise GraphRecipeChangeSetError(
            f"{label} must be an ordered nonempty tuple of RetainedReference values"
        )
    if not all(isinstance(value, RetainedReference) for value in values):
        raise GraphRecipeChangeSetError(
            f"{label} must contain only RetainedReference values"
        )
    identifiers = [value.record_id for value in values]
    if len(identifiers) != len(set(identifiers)):
        raise GraphRecipeChangeSetError(f"{label} record IDs must be unique")
    return [{id_field: value.record_id, "sha256": value.sha256} for value in values]


def _operations(plan: AssemblyPlan) -> list[dict[str, object]]:
    if not plan.operations:
        raise GraphRecipeChangeSetError(
            "an accepted knowledge change requires at least one GraphRecipe operation"
        )
    members_by_id = {item.member: item for item in plan.members}
    if len(members_by_id) != len(plan.members) or set(members_by_id) != set(
        plan.operation_members
    ):
        raise GraphRecipeChangeSetError(
            "plan members and operation_members must name the same members"
        )

    dependencies: dict[str, list[str]] = {
        member: [] for member in plan.operation_members
    }
    for dependency in plan.dependencies:
        if (
            dependency.member not in dependencies
            or dependency.prerequisite_member not in dependencies
        ):
            raise GraphRecipeChangeSetError(
                "plan dependency references an unknown operation member"
            )
        dependencies[dependency.member].append(dependency.prerequisite_member)

    result: list[dict[str, object]] = []
    for ordinal, (member, operation) in enumerate(
        zip(plan.operation_members, plan.operations, strict=True)
    ):
        operation_type = operation.op_type.value
        if operation_type not in _SUPPORTED_OPERATION_TYPES:
            raise GraphRecipeChangeSetError(
                f"unsupported GraphRecipe operation type: {operation_type}"
            )
        declared = members_by_id[member]
        declared_operation_type = _MEMBER_OPERATION_TYPES.get(declared.operation_kind)
        if declared_operation_type is None:
            raise GraphRecipeChangeSetError(
                f"unsupported construction member operation kind: {declared.operation_kind}"
            )
        if declared_operation_type != operation_type:
            raise GraphRecipeChangeSetError(
                f"operation {ordinal} type does not match member {member}"
            )
        if declared.record_id != operation.record_id:
            raise GraphRecipeChangeSetError(
                f"operation {ordinal} record_id does not match member {member}"
            )
        # The member retains an ontology type IRI while the operation retains its
        # runtime symbol. AssemblyPlan does not retain their symbol binding, so
        # record type alignment cannot be checked here without inventing a rule.
        item: dict[str, object] = {
            "depends_on": dependencies[member],
            "operation_id": member,
            "operation_type": operation_type,
            "ordinal": ordinal,
            "properties": operation.properties,
            "record_id": operation.record_id,
            "record_type": operation.record_type,
        }
        if operation_type == "CREATE_RELATION":
            item["source_id"] = operation.source_id
            item["target_id"] = operation.target_id
        result.append(item)
    return result


def assembly_plan_to_operations(plan: AssemblyPlan) -> tuple[KnowledgeOperation, ...]:
    """Lower one aligned create-only plan for the private history composer."""

    return tuple(
        KnowledgeOperation(
            ordinal=item["ordinal"],
            operation_id=item["operation_id"],
            operation_type=item["operation_type"],
            record_type=item["record_type"],
            record_id=item["record_id"],
            properties=item["properties"],
            depends_on=tuple(item["depends_on"]),
            source_id=item.get("source_id"),
            target_id=item.get("target_id"),
        )
        for item in _operations(plan)
    )


def assembly_plan_to_change_set(
    plan: AssemblyPlan,
    *,
    change_set_id: str,
    contract_identity: str,
    base: HistoryBaseCoordinates,
    sources: tuple[RetainedReference, ...],
    evidence: tuple[RetainedReference, ...],
    valid_time: KnowledgeValidTime,
    supersedes: tuple[str, ...],
) -> KnowledgeChangeSet:
    """Map one complete GraphRecipe plan into canonical history input bytes."""

    plan_bytes = canonical_assembly_plan_bytes(plan)
    _require_text(change_set_id, "change_set_id")
    _require_digest(contract_identity, "contract_identity")
    if not isinstance(base, HistoryBaseCoordinates):
        raise GraphRecipeChangeSetError("base must be HistoryBaseCoordinates")
    if not isinstance(valid_time, KnowledgeValidTime):
        raise GraphRecipeChangeSetError("valid_time must be KnowledgeValidTime")
    if not isinstance(supersedes, tuple):
        raise GraphRecipeChangeSetError("supersedes must be an ordered tuple")
    source_closure = _closure(sources, id_field="source_id", label="sources")
    evidence_closure = _closure(
        evidence,
        id_field="evidence_id",
        label="evidence",
    )
    plan_identity = _DIGEST_PREFIX + sha256(plan_bytes).hexdigest()
    if not any(item.sha256 == plan_identity for item in evidence):
        raise GraphRecipeChangeSetError(
            "evidence must include the retained canonical AssemblyPlan digest"
        )

    payload = {
        "base_acceptance_head": base.acceptance_head,
        "base_accepted_state_digest": base.accepted_state_digest,
        "base_ledger_event_count": base.ledger_event_count,
        "base_ledger_head": base.ledger_head,
        "base_materialization_head": base.materialization_head,
        "change_set_id": change_set_id,
        "contract_identity": contract_identity,
        "contract_kind": _CONTRACT_KIND,
        "evidence": evidence_closure,
        "grammar": _CHANGE_GRAMMAR,
        "operations": _operations(plan),
        "sources": source_closure,
        "supersedes": list(supersedes),
        "valid_time": {
            "kind": valid_time.kind,
            "value": valid_time.value,
        },
    }
    return KnowledgeChangeSet.from_bytes(canonical_json(payload).encode("utf-8"))


__all__ = [
    "GraphRecipeChangeSetError",
    "HistoryBaseCoordinates",
    "RetainedReference",
    "assembly_plan_to_operations",
    "assembly_plan_to_change_set",
    "canonical_assembly_plan_bytes",
]

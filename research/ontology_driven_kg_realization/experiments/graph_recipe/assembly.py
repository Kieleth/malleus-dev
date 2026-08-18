"""Deterministic GraphRecipe terminal assembly and atomic graph admission."""

from __future__ import annotations

import heapq
import json
import math
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from malleus.kg import KnowledgeGraph, OpStatus, OpType
from malleus.ledger import canonical_json, content_digest
from malleus.staging import CandidateSubgraph, ProposedOperation, stage_subgraph

from .model import (
    ConstructionMember,
    DependsOnFact,
    ExpansionEmission,
    GraphRecipeDiagnostic,
    GraphRecipeFailure,
    LogicalGraphContract,
    MemberDependency,
    PropertyFact,
    RecordFact,
    RelationSourceFact,
    RelationTargetFact,
    RdfTerm,
    TerminalFact,
)


BASE = "https://malleus.dev/graph-recipe/base/"
XSD = "http://www.w3.org/2001/XMLSchema#"

_OPERATION_TYPES = {
    BASE + "CreateEntity": OpType.CREATE_ENTITY,
    BASE + "CreateRelation": OpType.CREATE_RELATION,
    BASE + "CreateSignal": OpType.CREATE_SIGNAL,
    BASE + "CreateEvent": OpType.CREATE_EVENT,
}


def _diagnostic(
    code: str,
    phase: str,
    subject: str,
    message: str,
    evidence: Mapping[str, Any],
) -> GraphRecipeDiagnostic:
    return GraphRecipeDiagnostic(code, phase, subject, {"message": message}, evidence)


def _json_copy(value: Any) -> Any:
    return json.loads(canonical_json(value))


class AssemblyFailure(GraphRecipeFailure):
    """Assembly refusal retaining every completed layer artifact."""

    def __init__(
        self,
        diagnostics: Sequence[GraphRecipeDiagnostic],
        *,
        member_graph_artifact: Mapping[str, Any],
    ) -> None:
        super().__init__(diagnostics)
        self._member_graph_artifact = canonical_json(member_graph_artifact)

    @property
    def member_graph_artifact(self) -> dict[str, Any]:
        return json.loads(self._member_graph_artifact)

    @property
    def proposed_operations_artifact(self) -> dict[str, Any]:
        return {
            "schema_version": "1",
            "status": "not-produced",
            "blocked_by": self.diagnostics[0].code,
            "operations": [],
        }


class StagingFailure(GraphRecipeFailure):
    """Structural-gate refusal over an unchanged materialized graph."""

    def __init__(
        self,
        diagnostics: Sequence[GraphRecipeDiagnostic],
        *,
        graph_artifact: Mapping[str, Any],
        candidate_digest: str,
        plan: "AssemblyPlan",
    ) -> None:
        super().__init__(diagnostics)
        self._graph_artifact = canonical_json(graph_artifact)
        self.candidate_digest = candidate_digest
        self.plan = plan

    @property
    def graph_artifact(self) -> dict[str, Any]:
        return json.loads(self._graph_artifact)

    @property
    def member_graph_artifact(self) -> dict[str, Any]:
        return self.plan.member_graph_artifact(include_valid=True)

    @property
    def proposed_operations_artifact(self) -> dict[str, Any]:
        return self.plan.proposed_operations_artifact()


@dataclass(frozen=True)
class AssemblyPlan:
    """A complete, ordered, target-neutral construction plan."""

    contract_digest: str
    invocation_digests: tuple[str, ...]
    members: tuple[ConstructionMember, ...]
    dependencies: tuple[MemberDependency, ...]
    topological_order: tuple[str, ...]
    operations: tuple[ProposedOperation, ...]
    operation_members: tuple[str, ...]
    member_emissions: tuple[tuple[str, tuple[tuple[str, str], ...]], ...]
    plan_digest: str

    def __post_init__(self) -> None:
        if len(self.operations) != len(self.operation_members):
            raise ValueError("operations and operation_members must align")
        if tuple(item.member for item in self.members) != tuple(
            sorted(item.member for item in self.members)
        ):
            raise ValueError("members must be ordered by member IRI")
        if self.operation_members != self.topological_order:
            raise ValueError("operation_members must equal topological_order")
        for name, value in (
            ("contract_digest", self.contract_digest),
            ("plan_digest", self.plan_digest),
            *(("invocation_digest", value) for value in self.invocation_digests),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ValueError(f"{name} must be a sha256 digest")

    def member_graph_artifact(self, *, include_valid: bool = False) -> dict[str, Any]:
        artifact: dict[str, Any] = {
            "schema_version": "1",
            "status": "complete",
        }
        if include_valid:
            artifact["valid"] = True
        artifact.update(
            {
                "members": [item.as_dict() for item in self.members],
                "dependencies": [item.as_dict() for item in self.dependencies],
                "acyclic": True,
                "topological_order": list(self.topological_order),
            }
        )
        return artifact

    def proposed_operations_artifact(self) -> dict[str, Any]:
        return {
            "schema_version": "1",
            "status": "complete",
            "operations": [item.as_dict() for item in self.operations],
        }

    def operation_lineage(self) -> list[dict[str, Any]]:
        by_member = dict(self.member_emissions)
        result = []
        for index, member in enumerate(self.operation_members):
            emissions = by_member[member]
            result.append(
                {
                    "member": member,
                    "operation_index": index,
                    "emission_ids": [emission_id for emission_id, _ in emissions],
                    "expansion_path_ids": [path_id for _, path_id in emissions],
                }
            )
        return result


@dataclass(frozen=True)
class RealizationResult:
    staging: str
    materialization: str
    snapshot: Mapping[str, Any]
    canonical_operations: tuple[Mapping[str, Any], ...]
    state_digest: str
    candidate_digest: str | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1",
            "status": "complete",
            "staging": self.staging,
            "materialization": self.materialization,
            "snapshot": _json_copy(self.snapshot),
            "canonical_operations": _json_copy(self.canonical_operations),
            "state_digest": self.state_digest,
        }


def _emissions(
    values: Sequence[ExpansionEmission | Mapping[str, Any]],
) -> tuple[ExpansionEmission, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise TypeError("emissions must be a sequence")
    result = []
    for index, value in enumerate(values):
        if isinstance(value, ExpansionEmission):
            emission = value
        elif isinstance(value, Mapping):
            emission = ExpansionEmission.from_dict(value, subject=f"emissions[{index}]")
        else:
            raise TypeError(f"emissions[{index}] must be ExpansionEmission or a mapping")
        result.append(emission)
    result.sort(key=lambda item: item.emission_id)
    ids = [item.emission_id for item in result]
    if len(set(ids)) != len(ids):
        raise GraphRecipeFailure(
            _diagnostic(
                "DUPLICATE_TERMINAL_EMISSION",
                "member-graph",
                next(item for item in ids if ids.count(item) > 1),
                "Terminal emission IDs must be unique across the atomic plan.",
                {"duplicate_emission_ids": sorted({item for item in ids if ids.count(item) > 1})},
            )
        )
    return tuple(result)


def _member_graph_artifact(
    members: Sequence[ConstructionMember],
    dependencies: Sequence[MemberDependency],
    *,
    blocked_by: str,
    acyclic: bool,
    cycle: Sequence[str] = (),
) -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "schema_version": "1",
        "status": "complete",
        "valid": False,
        "members": [item.as_dict() for item in sorted(members, key=lambda item: item.member)],
        "dependencies": [
            item.as_dict()
            for item in sorted(
                dependencies,
                key=lambda item: (item.prerequisite_member, item.member),
            )
        ],
        "acyclic": acyclic,
    }
    if cycle:
        artifact["cycle"] = list(cycle)
    artifact["topological_order"] = []
    artifact["blocked_by"] = blocked_by
    return artifact


def _raise_assembly(
    diagnostics: Sequence[GraphRecipeDiagnostic],
    members: Sequence[ConstructionMember],
    dependencies: Sequence[MemberDependency],
    *,
    acyclic: bool = True,
    cycle: Sequence[str] = (),
) -> None:
    ordered = tuple(sorted(diagnostics, key=lambda item: canonical_json(item.as_dict())))
    raise AssemblyFailure(
        ordered,
        member_graph_artifact=_member_graph_artifact(
            members,
            dependencies,
            blocked_by=ordered[0].code,
            acyclic=acyclic,
            cycle=cycle,
        ),
    )


def _collect(
    emissions: tuple[ExpansionEmission, ...],
) -> tuple[
    dict[str, list[tuple[TerminalFact, ExpansionEmission]]],
    tuple[ConstructionMember, ...],
    tuple[MemberDependency, ...],
]:
    grouped: dict[str, list[tuple[TerminalFact, ExpansionEmission]]] = {}
    for emission in emissions:
        grouped.setdefault(emission.fact.member, []).append((emission.fact, emission))

    members = []
    diagnostics = []
    for member in sorted(grouped):
        records = [fact for fact, _ in grouped[member] if isinstance(fact, RecordFact)]
        if len(records) != 1:
            diagnostics.append(
                _diagnostic(
                    "MEMBER_RECORD_CARDINALITY_VIOLATION",
                    "member-graph",
                    member,
                    f"Member '{member}' requires exactly one Record fact, received {len(records)}.",
                    {"member": member, "record_count": len(records)},
                )
            )
            continue
        members.append(ConstructionMember.from_record(records[0]))

    dependencies = tuple(
        sorted(
            {
                MemberDependency(fact.prerequisite_member, fact.member)
                for values in grouped.values()
                for fact, _ in values
                if isinstance(fact, DependsOnFact)
            },
            key=lambda item: (item.prerequisite_member, item.member),
        )
    )
    if diagnostics:
        _raise_assembly(diagnostics, members, dependencies)
    return grouped, tuple(sorted(members, key=lambda item: item.member)), dependencies


def _validate_dependencies(
    grouped: Mapping[str, Sequence[tuple[TerminalFact, ExpansionEmission]]],
    members: tuple[ConstructionMember, ...],
    dependencies: tuple[MemberDependency, ...],
    contract: LogicalGraphContract,
) -> None:
    member_names = {item.member for item in members}
    diagnostics = []
    for dependency in dependencies:
        unknown = [
            value
            for value in (dependency.prerequisite_member, dependency.member)
            if value not in member_names
        ]
        if unknown:
            diagnostics.append(
                _diagnostic(
                    "CONSTRUCTION_DEPENDENCY_MEMBER_UNKNOWN",
                    "member-graph",
                    dependency.member,
                    "DependsOn references a member without exactly one Record fact.",
                    {
                        "member": dependency.member,
                        "prerequisite_member": dependency.prerequisite_member,
                        "unknown_members": sorted(unknown),
                    },
                )
            )

    record_ids: dict[str, str] = {}
    duplicate_ids: dict[str, list[str]] = {}
    for item in members:
        if item.record_id in record_ids:
            duplicate_ids.setdefault(item.record_id, [record_ids[item.record_id]]).append(item.member)
        else:
            record_ids[item.record_id] = item.member
    for record_id, owners in sorted(duplicate_ids.items()):
        diagnostics.append(
            _diagnostic(
                "PLAN_RECORD_ID_COLLISION",
                "member-graph",
                record_id,
                f"Graph record ID '{record_id}' is anchored by multiple members.",
                {"record_id": record_id, "members": sorted(owners)},
            )
        )
    if diagnostics:
        _raise_assembly(diagnostics, members, dependencies)

    dependency_pairs = {(item.prerequisite_member, item.member) for item in dependencies}
    record_types = {item.type_iri for item in contract.record_types}
    missing = []
    for member in sorted(grouped):
        record = next(item for item in members if item.member == member)
        record_contract = contract.record_for_iri(record.record_type)
        references: list[tuple[str, str]] = []
        for fact, _ in grouped[member]:
            if isinstance(fact, RelationSourceFact):
                references.append(("RelationSource", fact.record_id))
            elif isinstance(fact, RelationTargetFact):
                references.append(("RelationTarget", fact.record_id))
            elif isinstance(fact, PropertyFact):
                slot = record_contract.slot_for_iri(fact.property)
                if slot.constraints.range in record_types:
                    references.append(("Property", _reference_value(fact.value)))
        for reference_kind, record_id in sorted(references):
            prerequisite = record_ids.get(record_id)
            if prerequisite is None or (prerequisite, member) in dependency_pairs:
                continue
            message = (
                f"Member '{member}' references local record '{record_id}' through "
                f"'{reference_kind}' without DependsOn('{member}', '{prerequisite}')."
            )
            missing.append(
                _diagnostic(
                    "LOCAL_REFERENCE_DEPENDENCY_MISSING",
                    "member-graph",
                    member,
                    message,
                    {
                        "member": member,
                        "record_id": record_id,
                        "reference_kind": reference_kind,
                        "required_prerequisite_member": prerequisite,
                    },
                )
            )
    if missing:
        _raise_assembly(missing, members, dependencies)


def _reference_value(term: RdfTerm) -> str:
    if term.kind == "iri":
        return term.value
    if term.kind == "literal":
        return term.lexical_form
    raise GraphRecipeFailure(
        _diagnostic(
            "REFERENCE_TERM_INVALID",
            "member-graph",
            term.kind,
            "A record reference must be an IRI or literal graph record ID.",
            {"term": term.as_dict()},
        )
    )


def _topological_order(
    members: tuple[ConstructionMember, ...],
    dependencies: tuple[MemberDependency, ...],
) -> tuple[str, ...]:
    names = tuple(item.member for item in members)
    indegree = {name: 0 for name in names}
    successors = {name: set() for name in names}
    for dependency in dependencies:
        if dependency.member not in indegree or dependency.prerequisite_member not in indegree:
            continue
        if dependency.member not in successors[dependency.prerequisite_member]:
            successors[dependency.prerequisite_member].add(dependency.member)
            indegree[dependency.member] += 1

    ready = [name for name, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        member = heapq.heappop(ready)
        order.append(member)
        for successor in sorted(successors[member]):
            indegree[successor] -= 1
            if indegree[successor] == 0:
                heapq.heappush(ready, successor)
    if len(order) == len(names):
        return tuple(order)

    remaining = {name for name, degree in indegree.items() if degree > 0}
    cycle = _cycle_witness(successors, remaining)
    diagnostic = _diagnostic(
        "CONSTRUCTION_DEPENDENCY_CYCLE",
        "member-graph",
        cycle[0],
        f"Construction dependency cycle: {' -> '.join(cycle)}.",
        {"cycle": list(cycle)},
    )
    _raise_assembly(
        (diagnostic,),
        members,
        dependencies,
        acyclic=False,
        cycle=cycle,
    )
    raise AssertionError("unreachable")


def _cycle_witness(
    successors: Mapping[str, set[str]],
    remaining: set[str],
) -> tuple[str, ...]:
    state: dict[str, int] = {}
    stack: list[str] = []
    positions: dict[str, int] = {}

    def visit(member: str) -> tuple[str, ...] | None:
        state[member] = 1
        positions[member] = len(stack)
        stack.append(member)
        for successor in sorted(successors[member] & remaining):
            if state.get(successor, 0) == 0:
                found = visit(successor)
                if found is not None:
                    return found
            elif state[successor] == 1:
                raw = tuple((*stack[positions[successor] :], successor))
                return _canonical_cycle(raw)
        stack.pop()
        positions.pop(member)
        state[member] = 2
        return None

    for member in sorted(remaining):
        if state.get(member, 0) == 0:
            found = visit(member)
            if found is not None:
                return found
    raise ValueError("cyclic remainder produced no cycle witness")


def _canonical_cycle(cycle: tuple[str, ...]) -> tuple[str, ...]:
    body = cycle[:-1]
    rotations = [body[index:] + body[:index] for index in range(len(body))]
    smallest = min(rotations)
    return (*smallest, smallest[0])


def _python_value(term: RdfTerm) -> Any:
    if term.kind == "iri":
        return term.value
    if term.kind != "literal":
        raise GraphRecipeFailure(
            _diagnostic(
                "TERMINAL_PROPERTY_VALUE_INVALID",
                "assembly",
                term.kind,
                "Property lowering requires an IRI or literal value.",
                {"term": term.as_dict()},
            )
        )
    value = term.lexical_form
    if term.datatype == XSD + "integer":
        try:
            return int(value)
        except ValueError as error:
            raise GraphRecipeFailure(
                _diagnostic(
                    "TERMINAL_PROPERTY_VALUE_INVALID",
                    "assembly",
                    value,
                    f"Literal '{value}' is not an xsd:integer lexical form.",
                    {"term": term.as_dict()},
                )
            ) from error
    if term.datatype in {XSD + "float", XSD + "double", XSD + "decimal"}:
        try:
            number = float(value)
        except ValueError as error:
            raise GraphRecipeFailure(
                _diagnostic(
                    "TERMINAL_PROPERTY_VALUE_INVALID",
                    "assembly",
                    value,
                    f"Literal '{value}' is not a numeric lexical form.",
                    {"term": term.as_dict()},
                )
            ) from error
        if not math.isfinite(number):
            raise GraphRecipeFailure(
                _diagnostic(
                    "TERMINAL_PROPERTY_VALUE_INVALID",
                    "assembly",
                    value,
                    "Numeric property values must be finite.",
                    {"term": term.as_dict()},
                )
            )
        return number
    if term.datatype == XSD + "boolean":
        if value in {"true", "1"}:
            return True
        if value in {"false", "0"}:
            return False
        raise GraphRecipeFailure(
            _diagnostic(
                "TERMINAL_PROPERTY_VALUE_INVALID",
                "assembly",
                value,
                f"Literal '{value}' is not an xsd:boolean lexical form.",
                {"term": term.as_dict()},
            )
        )
    return value


def _lower_member(
    record: ConstructionMember,
    facts: Sequence[tuple[TerminalFact, ExpansionEmission]],
    contract: LogicalGraphContract,
) -> ProposedOperation:
    record_contract = contract.record_for_iri(record.record_type)
    expected_operation = record_contract.legal_operation_kind
    if expected_operation is None or record.operation_kind != expected_operation:
        raise GraphRecipeFailure(
            _diagnostic(
                "RECORD_OPERATION_KIND_MISMATCH",
                "assembly",
                record.member,
                f"Record member '{record.member}' operation kind does not match its logical record type.",
                {
                    "member": record.member,
                    "record_type": record.record_type,
                    "expected_operation_kind": expected_operation,
                    "actual_operation_kind": record.operation_kind,
                },
            )
        )

    properties: dict[str, Any] = {}
    sources = []
    targets = []
    diagnostics = []
    property_facts: dict[str, list[PropertyFact]] = {}
    for fact, _ in facts:
        if isinstance(fact, PropertyFact):
            property_facts.setdefault(fact.property, []).append(fact)
        elif isinstance(fact, RelationSourceFact):
            sources.append(fact.record_id)
        elif isinstance(fact, RelationTargetFact):
            targets.append(fact.record_id)

    for property_iri in sorted(property_facts):
        values = property_facts[property_iri]
        slot = record_contract.slot_for_iri(property_iri)
        if slot.positional:
            diagnostics.append(
                _diagnostic(
                    "POSITIONAL_PROPERTY_BINDING_FORBIDDEN",
                    "assembly",
                    record.member,
                    f"Positional property '{slot.runtime_symbol}' cannot be repeated in ProposedOperation.properties.",
                    {"member": record.member, "property": property_iri},
                )
            )
            continue
        if len(values) != 1:
            diagnostics.append(
                _diagnostic(
                    "MEMBER_PROPERTY_CARDINALITY_VIOLATION",
                    "assembly",
                    record.member,
                    f"Member '{record.member}' property '{property_iri}' requires exactly one value in this slice.",
                    {"member": record.member, "property": property_iri, "value_count": len(values)},
                )
            )
            continue
        properties[slot.runtime_symbol] = _python_value(values[0].value)

    missing = [
        slot
        for slot in record_contract.operation_properties
        if slot.constraints.required and slot.runtime_symbol not in properties
    ]
    for slot in missing:
        diagnostics.append(
            _diagnostic(
                "MEMBER_REQUIRED_PROPERTY_MISSING",
                "assembly",
                record.member,
                f"Member '{record.member}' is missing required property '{slot.property_iri}'.",
                {"member": record.member, "property": slot.property_iri},
            )
        )

    if record_contract.role == "RELATION":
        if len(sources) != 1 or len(targets) != 1:
            diagnostics.append(
                _diagnostic(
                    "RELATION_ENDPOINT_CARDINALITY_VIOLATION",
                    "assembly",
                    record.member,
                    f"Relation member '{record.member}' requires exactly one source and one target.",
                    {"member": record.member, "source_count": len(sources), "target_count": len(targets)},
                )
            )
    elif sources or targets:
        diagnostics.append(
            _diagnostic(
                "NON_RELATION_ENDPOINT_FORBIDDEN",
                "assembly",
                record.member,
                f"Non-relation member '{record.member}' cannot declare relation endpoints.",
                {"member": record.member, "source_count": len(sources), "target_count": len(targets)},
            )
        )
    if diagnostics:
        raise GraphRecipeFailure(diagnostics)

    operation_type = _OPERATION_TYPES.get(record.operation_kind)
    if operation_type is None:
        raise GraphRecipeFailure(
            _diagnostic(
                "RECORD_OPERATION_KIND_UNKNOWN",
                "assembly",
                record.member,
                f"Operation kind '{record.operation_kind}' is not in the closed terminal ABI.",
                {"member": record.member, "operation_kind": record.operation_kind},
            )
        )
    return ProposedOperation(
        operation_type,
        record_contract.runtime_symbol,
        record.record_id,
        properties,
        sources[0] if sources else None,
        targets[0] if targets else None,
    )


def assemble_plan(
    contract: LogicalGraphContract,
    emissions: Sequence[ExpansionEmission | Mapping[str, Any]],
    *,
    invocation_digests: Sequence[str],
) -> AssemblyPlan:
    """Aggregate, validate, order, and lower one atomic PopulationPlan."""

    if not isinstance(contract, LogicalGraphContract):
        raise TypeError("contract must be a LogicalGraphContract")
    if isinstance(invocation_digests, (str, bytes)) or not isinstance(invocation_digests, Sequence):
        raise TypeError("invocation_digests must be a sequence")
    digests = tuple(sorted(invocation_digests))
    for digest in digests:
        if not isinstance(digest, str) or not digest.startswith("sha256:") or len(digest) != 71:
            raise ValueError("invocation_digests must contain sha256 digests")

    values = _emissions(emissions)
    grouped, members, dependencies = _collect(values)
    _validate_dependencies(grouped, members, dependencies, contract)
    order = _topological_order(members, dependencies)
    by_member = {item.member: item for item in members}
    operations = tuple(_lower_member(by_member[member], grouped[member], contract) for member in order)
    member_emissions = tuple(
        (
            member,
            tuple(
                sorted(
                    ((emission.emission_id, emission.expansion_path_id) for _, emission in grouped[member]),
                    key=lambda item: item[0],
                )
            ),
        )
        for member in order
    )
    graph_artifact = {
        "schema_version": "1",
        "status": "complete",
        "members": [item.as_dict() for item in members],
        "dependencies": [item.as_dict() for item in dependencies],
        "acyclic": True,
        "topological_order": list(order),
    }
    operations_artifact = {
        "schema_version": "1",
        "status": "complete",
        "operations": [item.as_dict() for item in operations],
    }
    plan_digest = content_digest(
        {
            "schema_version": "graph-recipe-plan-v0",
            "contract_digest": contract.contract_digest,
            "invocation_digests": list(digests),
            "member_graph": graph_artifact,
            "proposed_operations": operations_artifact,
        }
    )
    return AssemblyPlan(
        contract.contract_digest,
        digests,
        members,
        dependencies,
        order,
        operations,
        order,
        member_emissions,
        plan_digest,
    )


def _graph_artifact(
    graph: KnowledgeGraph,
    *,
    staging: str,
    materialization: str,
) -> dict[str, Any]:
    return {
        "schema_version": "1",
        "status": "complete",
        "staging": staging,
        "materialization": materialization,
        "snapshot": graph.snapshot(),
        "canonical_operations": list(graph.canonical_operations()),
        "state_digest": graph.state_digest(),
    }


def _result(
    graph: KnowledgeGraph,
    *,
    staging: str,
    materialization: str,
    candidate_digest: str | None,
) -> RealizationResult:
    return RealizationResult(
        staging,
        materialization,
        _json_copy(graph.snapshot()),
        tuple(_json_copy(graph.canonical_operations())),
        graph.state_digest(),
        candidate_digest,
    )


def _staging_diagnostics(
    candidate: CandidateSubgraph,
    plan: AssemblyPlan,
) -> tuple[GraphRecipeDiagnostic, ...]:
    diagnostics = []
    for index, operation in enumerate(candidate.operations):
        if operation.op_status != OpStatus.REJECTED:
            continue
        reason = operation.rejection_reason or "Structural validation rejected the operation"
        member = plan.operation_members[index]
        diagnostics.append(
            _diagnostic(
                "PLAN_GATE_REJECTION",
                "staging",
                member,
                f"The structural plan gate rejected proposed operation {index}: {reason}",
                {
                    "operation_index": index,
                    "recipe_member": member,
                    "endpoint_diagnostic": reason,
                },
            )
        )
    return tuple(diagnostics)


def stage_and_materialize(
    graph: KnowledgeGraph,
    plan: AssemblyPlan,
    *,
    turn: int | None = None,
) -> RealizationResult:
    """Stage the whole plan in isolation and materialize it only if valid."""

    if not isinstance(graph, KnowledgeGraph):
        raise TypeError("graph must be a KnowledgeGraph")
    if not isinstance(plan, AssemblyPlan):
        raise TypeError("plan must be an AssemblyPlan")
    if not plan.operations:
        return _result(
            graph,
            staging="skipped-empty-operation-sequence",
            materialization="skipped-empty-operation-sequence",
            candidate_digest=None,
        )

    candidate = stage_subgraph(graph, plan.operations, turn=turn)
    if not candidate.valid:
        diagnostics = _staging_diagnostics(candidate, plan)
        if not diagnostics:
            diagnostics = (
                _diagnostic(
                    "PLAN_GATE_REJECTION",
                    "staging",
                    plan.operation_members[0],
                    "The structural plan gate rejected the candidate without operation evidence.",
                    {
                        "operation_index": 0,
                        "recipe_member": plan.operation_members[0],
                        "endpoint_diagnostic": "Structural validation rejected the candidate",
                    },
                ),
            )
        raise StagingFailure(
            diagnostics,
            graph_artifact=_graph_artifact(
                graph,
                staging="rejected-atomically",
                materialization="not-entered",
            ),
            candidate_digest=candidate.candidate_digest,
            plan=plan,
        )

    candidate.materialize_into(graph)
    return _result(
        graph,
        staging="accepted",
        materialization="committed-atomically",
        candidate_digest=candidate.candidate_digest,
    )

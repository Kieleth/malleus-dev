"""Shared write path for the three Gedanken toys.

Every graph in this directory is built the same way and no other way: an empty
registry-gated `KnowledgeGraph`, one `stage_subgraph` batch through the real
validators, then `PrologVerifier.verify_candidate_subgraph` over the resulting
candidate. A refused write is a crash carrying the registry's own reason, never
a silently smaller graph.
"""

from __future__ import annotations

from pathlib import Path

from malleus.kg import KnowledgeGraph
from malleus.logic import GraphFactCompiler, LogicCheckResult, LogicContract
from malleus.ontology import OntologyRegistry
from malleus.prolog_verifier import PrologVerifier
from malleus.staging import CandidateSubgraph, ProposedOperation, stage_subgraph

HERE = Path(__file__).resolve().parent.parent
ONTOLOGIES = HERE / "ontologies"
CONTRACTS = HERE / "contracts"


def registry_for(toy: str) -> OntologyRegistry:
    return OntologyRegistry(ONTOLOGIES / f"{toy}.yaml")


def contract_for(toy: str) -> LogicContract:
    return LogicContract.load(CONTRACTS / f"{toy}_logic.yaml")


def stage(toy: str, writes: list[ProposedOperation]) -> CandidateSubgraph:
    """Stage one whole toy graph as a single candidate on an empty base."""
    graph = KnowledgeGraph(registry_for(toy))
    candidate = stage_subgraph(graph, writes)
    if not candidate.valid:
        raise AssertionError(f"{toy} candidate refused: {candidate.rejection_reason}")
    return candidate


def materialize(toy: str, writes: list[ProposedOperation]) -> KnowledgeGraph:
    """Stage and structurally materialize, so the graph exists as graph state."""
    graph = KnowledgeGraph(registry_for(toy))
    candidate = stage_subgraph(graph, writes)
    if not candidate.valid:
        raise AssertionError(f"{toy} candidate refused: {candidate.rejection_reason}")
    candidate.materialize_into(graph)
    return graph


def check(toy: str, writes: list[ProposedOperation]) -> LogicCheckResult:
    """Run the pinned contract over one toy graph and return the verdict."""
    return PrologVerifier(contract_for(toy)).verify_candidate_subgraph(stage(toy, writes))


def facts(toy: str, *graphs: KnowledgeGraph):
    return GraphFactCompiler().compile(*graphs)


def findings(result: LogicCheckResult) -> tuple[tuple[str, str, tuple[str, ...]], ...]:
    """The verdict as comparable tuples: rule, code, witnesses."""
    return tuple(
        (violation.rule_id, violation.violation_code, violation.witness_record_ids)
        for violation in result.violations
    )


def codes(result: LogicCheckResult) -> tuple[str, ...]:
    return tuple(sorted({violation.violation_code for violation in result.violations}))


def report(label: str, result: LogicCheckResult) -> None:
    print(f"\n--- {label} ---")
    print(f"outcome        {result.outcome}")
    print(f"facts          {result.fact_count} facts, {len(result.translated_record_ids)} records")
    print(f"checked rules  {', '.join(result.checked_rule_ids)}")
    if not result.violations:
        print("violations     none")
        return
    for violation in result.violations:
        witnesses = ", ".join(violation.witness_record_ids)
        print(f"violation      {violation.rule_id} / {violation.violation_code} [{witnesses}]")

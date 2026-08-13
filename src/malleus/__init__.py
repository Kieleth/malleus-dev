"""Malleus: root ontology + ontology-typed knowledge graph with distributed convergence.

Public API:
    OntologyRegistry  — load LinkML schemas, validate types/enums, hash, fingerprint.
    KnowledgeGraph    — write-time validated typed KG with operation log.
    PrologVerifier    — optional domain rule verification via SWI-Prolog.

Example:
    from malleus import OntologyRegistry, KnowledgeGraph
    reg = OntologyRegistry("path/to/schema.yaml")
    kg = KnowledgeGraph(reg)
    op = kg.create_entity("Drug", "drug-001", {"name": "Simvastatin"})
"""

from malleus.ontology import (
    EnumDef,
    OntologyError,
    OntologyRegistry,
    SlotConstraint,
    TypeDef,
    bundled_ontology_path,
)
from malleus.kg import (
    KnowledgeGraph,
    Operation,
    OpStatus,
    OpType,
    ValidationResult,
)
from malleus.protocol import (
    AcceptedGraphError,
    AcceptedGraphProjector,
    AcceptedGraphView,
    AuthorizationState,
    EventType,
    LedgerError,
    ProposalState,
    ProtocolError,
    ProtocolLedger,
    ProtocolProjection,
    TemporalWrite,
    acceptance_result_head,
    accepted_application_record,
    candidate_artifact_digest,
    candidate_artifact_fields,
    candidate_manifest,
    candidate_manifest_hash,
    graph_base_artifact_digest,
    graph_base_metadata,
    make_record,
    temporal_write,
)
from malleus.staging import (
    CandidateSubgraph,
    ProposedOperation,
    StagingError,
    StaleCandidateError,
    stage_subgraph,
)
from malleus.status import IMPLEMENTATION_STATUS, ImplementationStatus
from malleus.control import (
    AuthorizationEvaluation,
    ControlError,
    MonitoringError,
    PolicyEvaluation,
    authority_monitor_failure_records,
    authorization_policy_digest,
    authorization_policy_requirements,
    epistemic_policy_digest,
    evaluate_authorization_policy,
    evaluate_epistemic_policy,
    monitor_failure_records,
    monitor_specification_digest,
)
from malleus.logic import (
    CompiledFacts,
    GraphFactCompiler,
    LogicCheckResult,
    LogicContract,
    LogicError,
    LogicExecutionError,
    Violation,
    logic_monitor_failure_records,
)
from malleus.prolog_verifier import PrologVerifier

__version__ = IMPLEMENTATION_STATUS.package_version

__all__ = [
    "OntologyRegistry",
    "OntologyError",
    "TypeDef",
    "EnumDef",
    "SlotConstraint",
    "bundled_ontology_path",
    "KnowledgeGraph",
    "Operation",
    "OpStatus",
    "OpType",
    "ValidationResult",
    "ProtocolLedger",
    "ProtocolProjection",
    "ProtocolError",
    "LedgerError",
    "EventType",
    "ProposalState",
    "AuthorizationState",
    "make_record",
    "AcceptedGraphError",
    "AcceptedGraphProjector",
    "AcceptedGraphView",
    "TemporalWrite",
    "acceptance_result_head",
    "accepted_application_record",
    "candidate_artifact_digest",
    "candidate_artifact_fields",
    "candidate_manifest",
    "candidate_manifest_hash",
    "graph_base_artifact_digest",
    "graph_base_metadata",
    "temporal_write",
    "CandidateSubgraph",
    "ProposedOperation",
    "StagingError",
    "StaleCandidateError",
    "stage_subgraph",
    "ControlError",
    "AuthorizationEvaluation",
    "MonitoringError",
    "PolicyEvaluation",
    "authority_monitor_failure_records",
    "authorization_policy_digest",
    "authorization_policy_requirements",
    "monitor_specification_digest",
    "epistemic_policy_digest",
    "evaluate_authorization_policy",
    "evaluate_epistemic_policy",
    "monitor_failure_records",
    "CompiledFacts",
    "GraphFactCompiler",
    "LogicCheckResult",
    "LogicContract",
    "LogicError",
    "LogicExecutionError",
    "Violation",
    "logic_monitor_failure_records",
    "PrologVerifier",
    "IMPLEMENTATION_STATUS",
    "ImplementationStatus",
    "__version__",
]

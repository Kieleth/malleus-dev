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
)
from malleus.kg import (
    KnowledgeGraph,
    Operation,
    OpStatus,
    OpType,
    ValidationResult,
)
from malleus.protocol import (
    AuthorizationState,
    EventType,
    LedgerError,
    ProposalState,
    ProtocolError,
    ProtocolLedger,
    ProtocolProjection,
    make_record,
)

try:
    from malleus.prolog_verifier import PrologVerifier, VerificationResult
    _prolog_available = True
except ImportError:
    _prolog_available = False

__version__ = "0.1.0"

__all__ = [
    "OntologyRegistry",
    "OntologyError",
    "TypeDef",
    "EnumDef",
    "SlotConstraint",
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
    "__version__",
]

if _prolog_available:
    __all__.extend(["PrologVerifier", "VerificationResult"])

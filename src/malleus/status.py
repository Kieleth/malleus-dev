"""Machine-readable boundary for the implemented Malleus capability set."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ImplementationStatus:
    package_version: str
    current_stage: str
    boundary: str
    completed_stages: tuple[str, ...]
    implemented_capabilities: tuple[str, ...]
    pending_capabilities: tuple[str, ...]
    root_ontology_version: str
    assent_ontology_version: str


IMPLEMENTATION_STATUS = ImplementationStatus(
    package_version="0.2.0",
    current_stage="4",
    boundary="stage-4-structural-staging",
    completed_stages=("2", "3", "7a", "4"),
    implemented_capabilities=(
        "closed-world-ontology-validation",
        "typed-graph-write-validation",
        "assent-state-machines",
        "hash-linked-protocol-ledger",
        "isolated-proposed-subgraph-staging",
        "domain-specific-candidate-verification",
    ),
    pending_capabilities=(
        "general-graph-to-prolog-compilation",
        "policy-selected-monitoring-control",
        "assent-gated-materialization",
        "accepted-graph-projection",
        "bitemporal-as-of-replay",
        "action-execution",
    ),
    root_ontology_version="0.4.0",
    assent_ontology_version="0.1.0",
)

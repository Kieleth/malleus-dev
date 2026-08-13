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
    package_version="0.3.0",
    current_stage="5",
    boundary="stage-5-general-logic-monitoring",
    completed_stages=("2", "3", "7a", "4", "5"),
    implemented_capabilities=(
        "closed-world-ontology-validation",
        "typed-graph-write-validation",
        "assent-state-machines",
        "hash-linked-protocol-ledger",
        "isolated-proposed-subgraph-staging",
        "general-graph-to-prolog-compilation",
        "pinned-logic-contracts",
        "process-isolated-logic-checks",
        "exhaustive-violation-witnesses",
        "immutable-logic-check-records",
        "logic-monitor-failure-to-unknown",
    ),
    pending_capabilities=(
        "policy-selected-monitoring-control",
        "proposal-candidate-semantic-binding",
        "assent-gated-materialization",
        "accepted-graph-projection",
        "bitemporal-as-of-replay",
        "action-execution",
        "untrusted-rule-program-sandboxing",
    ),
    root_ontology_version="0.4.0",
    assent_ontology_version="0.2.0",
)

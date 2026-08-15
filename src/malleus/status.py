"""Machine-readable boundary for the implemented Malleus capability set."""

from dataclasses import dataclass

import yaml

from malleus.ontology import bundled_ontology_path


def _declared_schema_version(*parts: str) -> str:
    with open(bundled_ontology_path(*parts), encoding="utf-8") as stream:
        return str(yaml.safe_load(stream)["version"])


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
    package_version="0.6.0",
    current_stage="7c",
    boundary="stage-7c-policy-selected-authorization-control",
    completed_stages=("2", "3", "7a", "4", "5", "6", "7b", "7c"),
    implemented_capabilities=(
        "closed-world-ontology-validation",
        "typed-graph-write-validation",
        "assent-state-machines",
        "hash-linked-protocol-ledger",
        "failure-atomic-ledger-replacement",
        "isolated-proposed-subgraph-staging",
        "general-graph-to-prolog-compilation",
        "pinned-logic-contracts",
        "process-isolated-logic-checks",
        "exhaustive-violation-witnesses",
        "immutable-logic-check-records",
        "logic-monitor-failure-to-unknown",
        "typed-monitor-specifications",
        "typed-epistemic-policies",
        "proposal-bound-epistemic-policy",
        "exact-required-monitor-coverage",
        "single-output-per-monitor-context",
        "single-logic-check-per-monitor-context",
        "closed-core-assessment-contracts",
        "deterministic-epistemic-control-selection",
        "atomic-unavailable-monitor-assessments",
        "content-addressed-external-graph-base",
        "replayable-temporal-candidate-manifests",
        "proposal-candidate-semantic-binding",
        "decision-candidate-semantic-binding",
        "atomic-assent-gated-materialization",
        "accepted-graph-projection",
        "bitemporal-as-of-replay",
        "half-open-valid-time-intervals",
        "explicit-record-supersession",
        "accepted-graph-materialization-head",
        "typed-authorization-policies",
        "action-bound-authorization-policy",
        "exact-required-authority-monitor-coverage",
        "deterministic-authorization-control-selection",
        "authority-monitor-failure-to-clarify",
        "verdict-scoped-authority-grant-validation",
    ),
    pending_capabilities=(
        "monitor-execution-orchestration",
        "epistemic-policy-authority-and-scope",
        "authorization-policy-authority-and-scope",
        "portable-graph-base-resolution",
        "typed-retraction-semantics",
        "multi-writer-ledger-serialization",
        "action-execution",
        "review-report-recording",
        "outcome-observation-recording",
        "protocol-actor-registration",
        "evidence-assertion-recording",
        "untrusted-rule-program-sandboxing",
        "citation-byte-verification",
        "deferral-queue-aging",
    ),
    root_ontology_version=_declared_schema_version("malleus.yaml"),
    assent_ontology_version=_declared_schema_version("assent.yaml"),
)

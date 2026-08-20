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
    package_version="0.12.0",
    current_stage="8c",
    boundary="stage-8c-executable-provenance-and-effect-closure",
    completed_stages=(
        "2",
        "3",
        "7a",
        "4",
        "5",
        "6",
        "7b",
        "7c",
        "8a",
        "8b",
        "8c",
    ),
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
        "evidence-assertion-recording",
        "content-addressed-source-artifacts",
        "exact-evidence-source-binding",
        "failure-atomic-event-batches",
        "epistemic-monitor-adapter-orchestration",
        "adapter-failure-to-unknown",
        "content-addressed-external-graph-base",
        "replayable-temporal-candidate-manifests",
        "proposal-candidate-semantic-binding",
        "decision-candidate-semantic-binding",
        "atomic-assent-gated-materialization",
        "accepted-graph-projection",
        "bitemporal-as-of-replay",
        "half-open-valid-time-intervals",
        "precision-aware-valid-time-boundaries",
        "iana-timezone-calendar-day-enforcement",
        "three-valued-valid-time-projection",
        "indeterminacy-reason-commitments",
        "explicit-record-supersession",
        "accepted-graph-materialization-head",
        "typed-authorization-policies",
        "action-bound-authorization-policy",
        "exact-required-authority-monitor-coverage",
        "deterministic-authorization-control-selection",
        "authority-monitor-failure-to-clarify",
        "verdict-scoped-authority-grant-validation",
        "content-addressed-outcome-contracts",
        "authorized-action-dispatch-recording",
        "terminal-execution-receipts",
        "independent-outcome-observation-recording",
        "typed-literature-review-ledger",
        "evidence-linked-literature-comparison",
        "deterministic-recon-artifact-builds",
        "legacy-literature-kg-v1-import",
    ),
    pending_capabilities=(
        "monitor-execution-orchestration",
        "epistemic-policy-authority-and-scope",
        "authorization-policy-authority-and-scope",
        "portable-graph-base-resolution",
        "typed-retraction-semantics",
        "historical-timezone-database-migration",
        "dependency-closed-valid-time-projection",
        "multi-writer-ledger-serialization",
        "lexical-format-validation",
        "action-execution",
        "review-report-recording",
        "protocol-actor-registration",
        "untrusted-rule-program-sandboxing",
        "citation-byte-verification",
        "deferral-queue-aging",
        "exactly-once-effect-delivery-profile",
    ),
    root_ontology_version=_declared_schema_version("malleus.yaml"),
    assent_ontology_version=_declared_schema_version("assent.yaml"),
)

"""Adversarial tests for assent transitions and their JSONL envelope."""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

from malleus.ledger import JsonlLedger
from malleus.ontology import OntologyRegistry
from malleus.control import (
    MonitoringError,
    authority_monitor_failure_records,
    authorization_policy_digest,
    evaluate_authorization_policy,
    epistemic_policy_digest,
    evaluate_epistemic_policy,
    monitor_failure_records,
    monitor_specification_digest,
)
from malleus.logic import (
    LogicCheckResult,
    LogicExecutionError,
    Violation,
    logic_contract_digest,
    logic_monitor_failure_records,
)
from malleus.protocol import (
    AssentPlan,
    AssentPlanError,
    AuthorizationState,
    EventType,
    LedgerError,
    ProposalState,
    ProtocolError,
    ProtocolLedger,
    canonical_json,
    content_digest,
    event_hash,
    make_record,
    MonitorEvent,
    MonitorFailurePlan,
    MonitorStep,
    outcome_contract_digest,
    record_hash,
    source_artifact_digest,
    source_artifact_fields,
    source_bytes_digest,
    ValidTime,
)


ASSENT_SCHEMA = Path(__file__).parent.parent / "ontology" / "assent.yaml"
T0 = "2026-08-12T08:00:00Z"
SNAPSHOT = "sha256:" + "1" * 64
ARTIFACT_BODY = "sha256:" + "2" * 64


def time_at(minute: int) -> str:
    return f"2026-08-12T08:{minute:02d}:00Z"


def valid_time_at(value: str) -> dict:
    return ValidTime.exact(value.replace("Z", "+00:00")).as_dict()


@pytest.fixture
def registry(tmp_path):
    domain = tmp_path / "assent_test.yaml"
    domain.write_text(
        """id: https://malleus.dev/schema/assent-test
name: assent_test
version: 0.1.0
imports:
  - assent
classes:
  TestActionProposal:
    is_a: ActionProposal
    slots:
      - test_parameter
  ForgedLogicalAssessment:
    is_a: Assessment
slots:
  test_parameter:
    range: string
    required: true
""",
        encoding="utf-8",
    )
    return OntologyRegistry(domain, import_map={"assent": ASSENT_SCHEMA})


@pytest.fixture
def ledger(tmp_path, registry):
    return ProtocolLedger(tmp_path / "protocol.jsonl", registry)


def anchor(ledger: ProtocolLedger) -> dict:
    return ledger.append_event(
        event_id="event:anchor",
        event_type=EventType.EXTERNAL_SNAPSHOT_ANCHORED,
        transaction_time=T0,
        actor_id="actor:system",
        payload={
            "snapshot_id": "snapshot:stage-1",
            "snapshot_hash": SNAPSHOT,
            "source": "malleus-moving/research_graph/research.jsonl",
            "record_count": 200,
            "opaque": True,
        },
    )


def add_artifact(
    ledger: ProtocolLedger,
    artifact_id: str,
    kind: str,
    minute: int,
    *,
    record_type: str = "ProtocolArtifact",
    artifact_hash: str = ARTIFACT_BODY,
    **fields,
) -> dict:
    event_id = f"event:{artifact_id}"
    timestamp = time_at(minute)
    record = make_record(
        record_type,
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:system",
        role="registrar",
        id=artifact_id,
        artifact_kind=kind,
        artifact_version="1",
        artifact_hash=artifact_hash,
        **fields,
    )
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.ARTIFACT_RECORDED,
        transaction_time=timestamp,
        actor_id="actor:system",
        payload={"artifact_type": record_type, "artifact": record},
    )
    return record


def add_source_artifact(
    ledger: ProtocolLedger,
    *,
    artifact_id: str = "artifact:source:invoice",
    minute: int = 5,
    source_bytes: bytes = b"invoice INV-104 amount 42000",
) -> dict:
    fields = source_artifact_fields(
        artifact_id=artifact_id,
        artifact_version="1",
        source_bytes=source_bytes,
        media_type="application/pdf",
        locator="documents/INV-104.pdf",
    )
    return add_artifact(
        ledger,
        artifact_id,
        "SOURCE",
        minute,
        record_type="SourceArtifact",
        **fields,
    )


def add_outcome_contract(
    ledger: ProtocolLedger,
    *,
    artifact_id: str = "artifact:outcome-contract:effect-present",
    minute: int = 5,
) -> dict:
    fields = {
        "outcome_contract_schema_version": "1",
        "observation_type": "EXPECTED_EFFECT_PRESENT",
        "observer_implementation_hash": "sha256:" + "b" * 64,
    }
    return add_artifact(
        ledger,
        artifact_id,
        "OUTCOME_CONTRACT",
        minute,
        record_type="OutcomeContractArtifact",
        artifact_hash=outcome_contract_digest(
            schema_version=fields["outcome_contract_schema_version"],
            contract_id=artifact_id,
            contract_version="1",
            observation_type=fields["observation_type"],
            observer_implementation_hash=fields["observer_implementation_hash"],
        ),
        **fields,
    )


# kind -> (dependency artifact kind, dependency id, assessment type, id slot, hash slot)
KIND_CONTRACTS = {
    "CONFLICT": (
        "CONFLICT_RULE",
        "artifact:conflict-rule",
        "ConflictAssessment",
        "conflict_rule_id",
        "conflict_rule_hash",
    ),
    "UNCERTAINTY": (
        "UNCERTAINTY_CONTRACT",
        "artifact:uncertainty-contract",
        "UncertaintyAssessment",
        "uncertainty_contract_id",
        "uncertainty_contract_hash",
    ),
    "TEMPORAL": (
        "TEMPORAL_CONTRACT",
        "artifact:temporal-contract",
        "TemporalAssessment",
        "temporal_contract_id",
        "temporal_contract_hash",
    ),
}


def add_monitor(
    ledger: ProtocolLedger,
    monitor_id: str,
    assessment_kind: str,
    minute: int,
    *,
    input_artifacts: list[dict] | None = None,
) -> dict:
    inputs = sorted(input_artifacts or [], key=lambda artifact: artifact["id"])
    fields = {
        "monitor_schema_version": "1",
        "assessment_kind": assessment_kind,
        "monitor_implementation_hash": "sha256:" + "a" * 64,
        "input_artifact_ids": [artifact["id"] for artifact in inputs],
        "input_artifact_record_hashes": [artifact["content_hash"] for artifact in inputs],
        "source_record_ids": [artifact["id"] for artifact in inputs],
    }
    return add_artifact(
        ledger,
        monitor_id,
        "MONITOR_SPECIFICATION",
        minute,
        record_type="MonitorSpecificationArtifact",
        artifact_hash=monitor_specification_digest(
            schema_version="1",
            monitor_id=monitor_id,
            monitor_version="1",
            assessment_kind=assessment_kind,
            implementation_hash=fields["monitor_implementation_hash"],
            input_artifact_ids=fields["input_artifact_ids"],
            input_artifact_record_hashes=fields["input_artifact_record_hashes"],
        ),
        **fields,
    )


def add_kind_monitor(
    ledger: ProtocolLedger,
    kind: str,
    minute: int = 5,
) -> tuple[dict, dict]:
    """Register the pinned dependency artifact and the monitor that reads it."""
    artifact_kind, artifact_id, _, _, _ = KIND_CONTRACTS[kind]
    dependency = add_artifact(ledger, artifact_id, artifact_kind, minute)
    monitor = add_monitor(
        ledger,
        f"artifact:{kind.lower()}-monitor",
        kind,
        minute,
        input_artifacts=[dependency],
    )
    return dependency, monitor


def add_epistemic_policy(
    ledger: ProtocolLedger,
    rules: dict,
    requirements: list[tuple[dict, str, str]],
    minute: int,
    *,
    policy_id: str = "artifact:epistemic-policy",
) -> dict:
    ordered = sorted(requirements, key=lambda item: item[0]["id"])
    fields = {
        "policy_schema_version": "1",
        "ruleset_id": rules["id"],
        "ruleset_record_hash": rules["content_hash"],
        "ruleset_artifact_hash": rules["artifact_hash"],
        "required_monitor_ids": [item[0]["id"] for item in ordered],
        "required_monitor_record_hashes": [item[0]["content_hash"] for item in ordered],
        "violation_verdicts": [item[1] for item in ordered],
        "unknown_verdicts": [item[2] for item in ordered],
        "control_precedence": ["REJECT", "CONTEST", "DEFER"],
        "source_record_ids": [rules["id"], *(item[0]["id"] for item in ordered)],
    }
    return add_artifact(
        ledger,
        policy_id,
        "EPISTEMIC_POLICY",
        minute,
        record_type="EpistemicPolicyArtifact",
        artifact_hash=epistemic_policy_digest(
            schema_version="1",
            policy_id=policy_id,
            policy_version="1",
            ruleset_id=rules["id"],
            ruleset_record_hash=rules["content_hash"],
            ruleset_artifact_hash=rules["artifact_hash"],
            required_monitor_ids=fields["required_monitor_ids"],
            required_monitor_record_hashes=fields["required_monitor_record_hashes"],
            violation_verdicts=fields["violation_verdicts"],
            unknown_verdicts=fields["unknown_verdicts"],
            control_precedence=fields["control_precedence"],
        ),
        **fields,
    )


def add_authorization_policy(
    ledger: ProtocolLedger,
    monitors: list[dict],
    minute: int,
    *,
    policy_id: str = "artifact:authorization-policy",
) -> dict:
    ordered = sorted(monitors, key=lambda item: item["id"])
    fields = {
        "policy_schema_version": "1",
        "required_monitor_ids": [item["id"] for item in ordered],
        "required_monitor_record_hashes": [item["content_hash"] for item in ordered],
        "source_record_ids": [item["id"] for item in ordered],
    }
    return add_artifact(
        ledger,
        policy_id,
        "AUTHORIZATION_POLICY",
        minute,
        record_type="AuthorizationPolicyArtifact",
        artifact_hash=authorization_policy_digest(
            schema_version="1",
            policy_id=policy_id,
            policy_version="1",
            required_monitor_ids=fields["required_monitor_ids"],
            required_monitor_record_hashes=fields["required_monitor_record_hashes"],
        ),
        **fields,
    )


def setup_artifacts(
    ledger: ProtocolLedger,
    *,
    violation_verdict: str = "REJECT",
    unknown_verdict: str = "DEFER",
    include_grant: bool = True,
    extra_kinds: tuple[str, ...] = (),
) -> dict[str, dict]:
    rules = add_artifact(ledger, "artifact:rules", "RULE_SET", 1)
    contract_fields = {
        "logic_contract_schema_version": "1",
        "ontology_hash": "sha256:" + "6" * 64,
        "fact_contract_version": "2",
        "ruleset_id": rules["id"],
        "ruleset_version": "1",
        "ruleset_record_hash": rules["content_hash"],
        "ruleset_artifact_hash": rules["artifact_hash"],
        "rule_ids": ["RULE_ONE"],
        "timeout_seconds": 5,
        "source_record_ids": [rules["id"]],
    }
    logic_contract = add_artifact(
        ledger,
        "artifact:logic-contract",
        "LOGIC_CONTRACT",
        2,
        record_type="LogicContractArtifact",
        artifact_hash=logic_contract_digest(
            schema_version=contract_fields["logic_contract_schema_version"],
            contract_id="artifact:logic-contract",
            contract_version="1",
            ontology_hash=contract_fields["ontology_hash"],
            fact_contract_version=contract_fields["fact_contract_version"],
            ruleset_id=contract_fields["ruleset_id"],
            ruleset_version=contract_fields["ruleset_version"],
            rule_ids=contract_fields["rule_ids"],
            timeout_seconds=contract_fields["timeout_seconds"],
            ruleset_hash=contract_fields["ruleset_artifact_hash"],
        ),
        **contract_fields,
    )
    monitor = add_monitor(ledger, "artifact:monitor", "TYPE", 2)
    logic_monitor = add_monitor(
        ledger,
        "artifact:logic-monitor",
        "LOGICAL",
        3,
        input_artifacts=[logic_contract],
    )
    authority_monitor = add_monitor(
        ledger,
        "artifact:authority-monitor",
        "AUTHORITY",
        3,
    )
    authorization_policy = add_authorization_policy(
        ledger,
        [authority_monitor],
        4,
    )
    epistemic_policy = add_epistemic_policy(
        ledger,
        rules,
        [(monitor, violation_verdict, unknown_verdict)],
        4,
    )
    grant = add_artifact(
            ledger,
            "artifact:grant",
            "AUTHORITY_GRANT",
            5,
            record_type="AuthorityGrant",
            grantor_actor_id="actor:system",
            grantee_actor_id="actor:executor",
            permitted_action_types=["TEST"],
            grant_valid_from=time_at(5),
            grant_valid_to=time_at(20),
        ) if include_grant else None
    artifacts = {
        "monitor": monitor,
        "logic_monitor": logic_monitor,
        "authority_monitor": authority_monitor,
        "epistemic_policy": epistemic_policy,
        "rules": rules,
        "logic_contract": logic_contract,
        "authorization_policy": authorization_policy,
        "grant": grant,
    }
    for kind in extra_kinds:
        dependency, kind_monitor = add_kind_monitor(ledger, kind, 5)
        artifacts[f"{kind.lower()}_dependency"] = dependency
        artifacts[f"{kind.lower()}_monitor"] = kind_monitor
    return artifacts


def record_proposal(
    ledger: ProtocolLedger,
    *,
    epistemic_policy: dict | None = None,
    authorization_policy: dict | None = None,
    include_action: bool = False,
    minute: int = 6,
    proposal_id: str = "proposal:1",
    proposal_revision: int = 1,
    revises_proposal_id: str | None = None,
    proposal_key: str = "proposal-key",
    claim_id: str = "claim:1",
    claim_key: str = "claim-key",
    claim_revision: int = 1,
    revises_claim_version_id: str | None = None,
    claim_valid_from=None,
    evidence_count: int = 0,
    source_artifact: dict | None = None,
    assertion_claim_id: str | None = None,
    assertion_evidence_id: str | None = None,
    action_id: str = "action:1",
    action_revision: int = 1,
    revises_action_id: str | None = None,
) -> tuple[dict, dict, dict | None]:
    if evidence_count and source_artifact is None:
        raise ValueError("source_artifact is required when evidence_count is nonzero")
    projection = ledger.replay()
    if epistemic_policy is None:
        policies = [
            item["record"]
            for item in projection.objects.values()
            if item["record_type"] == "EpistemicPolicyArtifact"
        ]
        if len(policies) != 1:
            raise AssertionError("record_proposal requires exactly one epistemic policy")
        epistemic_policy = policies[0]
    if include_action and authorization_policy is None:
        policies = [
            item["record"]
            for item in projection.objects.values()
            if item["record_type"] == "AuthorizationPolicyArtifact"
        ]
        if len(policies) != 1:
            raise AssertionError("record_proposal requires exactly one authorization policy")
        authorization_policy = policies[0]
    event_id = f"event:{proposal_id}"
    timestamp = time_at(minute)
    claim = make_record(
        "ClaimVersion",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:proposer",
        role="proposer",
        id=claim_id,
        claim_key=claim_key,
        revision=claim_revision,
        revises_claim_version_id=revises_claim_version_id,
        statement="The declared relation is structurally valid.",
        domain_valid_from=(
            valid_time_at(timestamp) if claim_valid_from is None else claim_valid_from
        ),
        domain_valid_to=None,
        dependency_ids=[],
    )
    action = None
    members = [("ClaimVersion", claim)]
    for index in range(1, evidence_count + 1):
        evidence = make_record(
            "Evidence",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:proposer",
            role="proposer",
            source_record_ids=[source_artifact["id"]],
            id=f"{proposal_id}:evidence:{index}",
            evidence_kind="PUBLISHED_SOURCE",
            source_artifact_id=source_artifact["id"],
            source_artifact_hash=source_artifact["content_hash"],
            locator=f"malleus-moving/research_graph/source-{index}.json",
            request_id=None,
        )
        assertion = make_record(
            "EvidenceAssertion",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:proposer",
            role="proposer",
            source_record_ids=[claim["id"], evidence["id"]],
            id=f"{proposal_id}:assertion:{index}",
            claim_version_id=assertion_claim_id or claim["id"],
            evidence_id=assertion_evidence_id or evidence["id"],
            evidence_polarity="SUPPORTS",
            rationale="The cited source states the claim verbatim.",
        )
        members.append(("Evidence", evidence))
        members.append(("EvidenceAssertion", assertion))
    if include_action:
        action = make_record(
            "TestActionProposal",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:proposer",
            role="proposer",
            source_record_ids=[authorization_policy["id"]],
            id=action_id,
            action_type="TEST",
            action_payload_hash="sha256:" + "6" * 64,
            action_key="action-key",
            revision=action_revision,
            revises_action_proposal_id=revises_action_id,
            authorization_policy_id=authorization_policy["id"],
            authorization_policy_hash=authorization_policy["content_hash"],
            test_parameter="value",
        )
        members.append(("TestActionProposal", action))
    proposal = make_record(
        "ProposedSubgraph",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:proposer",
        role="proposer",
        source_record_ids=[epistemic_policy["id"]],
        id=proposal_id,
        proposal_key=proposal_key,
        revision=proposal_revision,
        revises_proposal_id=revises_proposal_id,
        base_acceptance_head=projection.acceptance_head,
        epistemic_policy_id=epistemic_policy["id"],
        epistemic_policy_hash=epistemic_policy["content_hash"],
        member_content_hashes=[record["content_hash"] for _, record in members],
        claim_version_ids=[claim["id"]],
        evidence_ids=[
            record["id"] for record_type, record in members if record_type == "Evidence"
        ],
        evidence_assertion_ids=[
            record["id"]
            for record_type, record in members
            if record_type == "EvidenceAssertion"
        ],
        action_proposal_ids=[action["id"]] if action else [],
    )
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.PROPOSAL_RECORDED,
        transaction_time=timestamp,
        actor_id="actor:proposer",
        payload={
            "proposal": proposal,
            "members": [
                {"record_type": record_type, "record": record}
                for record_type, record in members
            ],
        },
    )
    return proposal, claim, action


def record_type_assessment(
    ledger: ProtocolLedger,
    proposal: dict,
    monitor: dict,
    *,
    outcome: str = "SATISFIED",
    minute: int = 7,
    input_record_ids: list[str] | None = None,
    assessment_id: str | None = None,
) -> dict:
    assessment_id = assessment_id or f"assessment:{outcome.lower()}"
    event_id = f"event:{assessment_id}"
    timestamp = time_at(minute)
    assessment = make_record(
        "TypeAssessment",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:monitor",
        role="type-monitor",
        source_record_ids=[proposal["id"], monitor["id"]],
        id=assessment_id,
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
        assessment_kind="TYPE",
        assessment_outcome=outcome,
        monitor_id=monitor["id"],
        monitor_version="1",
        monitor_hash=monitor["content_hash"],
        monitor_failure_id=None,
        input_record_ids=input_record_ids or [proposal["id"]],
        reason_codes=["TYPE_RESULT"],
        rationale="The structural monitor completed.",
    )
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.ASSESSMENT_RECORDED,
        transaction_time=timestamp,
        actor_id="actor:monitor",
        payload={"assessment_type": "TypeAssessment", "assessment": assessment},
    )
    return assessment


def record_kind_assessment(
    ledger: ProtocolLedger,
    proposal: dict,
    artifacts: dict[str, dict],
    kind: str,
    *,
    outcome: str = "SATISFIED",
    minute: int = 7,
    assessment_id: str | None = None,
    conflicting_assertion_ids: list[str] | None = None,
    input_record_ids: list[str] | None = None,
) -> dict:
    """Record a CONFLICT, UNCERTAINTY, or TEMPORAL assessment with its pinned
    dependency artifact."""
    _, _, assessment_type, id_slot, hash_slot = KIND_CONTRACTS[kind]
    monitor = artifacts[f"{kind.lower()}_monitor"]
    dependency = artifacts[f"{kind.lower()}_dependency"]
    assessment_id = assessment_id or f"assessment:{kind.lower()}:1"
    event_id = f"event:{assessment_id}"
    timestamp = time_at(minute)
    extra = {id_slot: dependency["id"], hash_slot: dependency["content_hash"]}
    if kind == "CONFLICT":
        extra["conflicting_assertion_ids"] = list(conflicting_assertion_ids or [])
    assessment = make_record(
        assessment_type,
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:monitor",
        role=f"{kind.lower()}-monitor",
        source_record_ids=[proposal["id"], monitor["id"], dependency["id"]],
        id=assessment_id,
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
        assessment_kind=kind,
        assessment_outcome=outcome,
        monitor_id=monitor["id"],
        monitor_version="1",
        monitor_hash=monitor["content_hash"],
        monitor_failure_id=None,
        input_record_ids=(
            input_record_ids if input_record_ids is not None else [proposal["id"]]
        ),
        reason_codes=[f"{kind}_RESULT"],
        rationale=f"The pinned {kind.lower()} monitor completed.",
        **extra,
    )
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.ASSESSMENT_RECORDED,
        transaction_time=timestamp,
        actor_id="actor:monitor",
        payload={"assessment_type": assessment_type, "assessment": assessment},
    )
    return assessment


def record_logic_check(
    ledger: ProtocolLedger,
    proposal: dict,
    artifacts: dict[str, dict],
    *,
    violated: bool = False,
    minute: int = 7,
    check_id: str = "logic-check:1",
    event_id: str = "event:logic-check",
    context_state_digests: tuple[str, ...] = (),
    mutate=None,
) -> tuple[dict, tuple[dict, ...]]:
    result = LogicCheckResult(
        candidate_digest="sha256:" + "3" * 64,
        base_state_digest="sha256:" + "4" * 64,
        candidate_state_digest="sha256:" + "5" * 64,
        context_state_digests=tuple(context_state_digests),
        ontology_hash="sha256:" + "6" * 64,
        fact_contract_version="2",
        contract_id=artifacts["logic_contract"]["id"],
        contract_version="1",
        contract_hash=artifacts["logic_contract"]["artifact_hash"],
        ruleset_id=artifacts["rules"]["id"],
        ruleset_version="1",
        ruleset_hash=artifacts["rules"]["artifact_hash"],
        engine_name="SWI-Prolog",
        engine_version="100002",
        timeout_seconds=5,
        facts_hash="sha256:" + "7" * 64,
        fact_count=4,
        translated_record_ids=("graph:1",),
        checked_rule_ids=("RULE_ONE",),
        violations=(Violation("RULE_ONE", "CONFLICT", ("graph:1",)),) if violated else (),
    )
    timestamp = time_at(minute)
    check, witnesses = result.to_protocol_records(
        check_id=check_id,
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:monitor",
        role="logic-monitor",
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
        monitor_id=artifacts["logic_monitor"]["id"],
        monitor_version="1",
        monitor_hash=artifacts["logic_monitor"]["content_hash"],
        logic_contract_record_hash=artifacts["logic_contract"]["content_hash"],
        ruleset_record_hash=artifacts["rules"]["content_hash"],
    )
    witnesses = list(witnesses)
    if mutate is not None:
        mutate(check, witnesses)
        check["content_hash"] = record_hash("LogicCheckRecord", check)
        for witness in witnesses:
            witness["content_hash"] = record_hash("ViolationWitness", witness)
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.LOGIC_CHECK_RECORDED,
        transaction_time=timestamp,
        actor_id="actor:monitor",
        payload={"check": check, "witnesses": witnesses},
    )
    return check, tuple(witnesses)


def record_logical_assessment(
    ledger: ProtocolLedger,
    proposal: dict,
    check: dict,
    artifacts: dict[str, dict],
    *,
    minute: int = 8,
    mutate=None,
) -> dict:
    event_id = "event:logical-assessment"
    timestamp = time_at(minute)
    assessment = make_record(
        "LogicalAssessment",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:monitor",
        role="logic-monitor",
        source_record_ids=[
            proposal["id"],
            artifacts["logic_monitor"]["id"],
            check["id"],
            artifacts["logic_contract"]["id"],
            artifacts["rules"]["id"],
        ],
        id="assessment:logical:1",
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
        assessment_kind="LOGICAL",
        assessment_outcome=check["check_outcome"],
        monitor_id=artifacts["logic_monitor"]["id"],
        monitor_version="1",
        monitor_hash=artifacts["logic_monitor"]["content_hash"],
        monitor_failure_id=None,
        input_record_ids=[proposal["id"], check["id"]],
        reason_codes=["LOGIC_CHECK_COMPLETED"],
        rationale="The pinned logic check completed.",
        checked_rule_ids=check["checked_rule_ids"],
        violated_rule_ids=check["violated_rule_ids"],
        logic_check_record_ids=[check["id"]],
        logic_contract_id=artifacts["logic_contract"]["id"],
        logic_contract_record_hash=artifacts["logic_contract"]["content_hash"],
        ruleset_id=artifacts["rules"]["id"],
        ruleset_hash=artifacts["rules"]["content_hash"],
    )
    if mutate is not None:
        mutate(assessment)
        assessment["content_hash"] = record_hash("LogicalAssessment", assessment)
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.ASSESSMENT_RECORDED,
        transaction_time=timestamp,
        actor_id="actor:monitor",
        payload={"assessment_type": "LogicalAssessment", "assessment": assessment},
    )
    return assessment


def record_authority_assessment(
    ledger: ProtocolLedger,
    proposal: dict,
    action: dict,
    artifacts: dict[str, dict],
    *,
    outcome: str = "SATISFIED",
    checked: list[str] | None = None,
    violated: list[str] | None = None,
    evaluated_actor_id: str = "actor:executor",
    grant: dict | None = None,
    include_grant: bool = True,
    minute: int = 9,
    assessment_id: str = "assessment:authority:1",
    mutate=None,
) -> dict:
    event_id = f"event:{assessment_id}"
    timestamp = time_at(minute)
    evaluated_grant = (artifacts["grant"] if grant is None else grant) if include_grant else None
    sources = [
        proposal["id"],
        action["id"],
        artifacts["authority_monitor"]["id"],
        artifacts["authorization_policy"]["id"],
    ]
    if evaluated_grant is not None:
        sources.append(evaluated_grant["id"])
    authority = make_record(
        "AuthorityAssessment",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:authority-monitor",
        role="authority-monitor",
        source_record_ids=sources,
        id=assessment_id,
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=ledger.replay().acceptance_head,
        assessment_kind="AUTHORITY",
        assessment_outcome=outcome,
        monitor_id=artifacts["authority_monitor"]["id"],
        monitor_version="1",
        monitor_hash=artifacts["authority_monitor"]["content_hash"],
        monitor_failure_id=None,
        input_record_ids=[
            proposal["id"],
            action["id"],
            *([evaluated_grant["id"]] if evaluated_grant is not None else []),
        ],
        reason_codes=["GRANT_RESULT"],
        rationale="The versioned authority policy was evaluated.",
        action_proposal_id=action["id"],
        action_content_hash=action["content_hash"],
        evaluated_actor_id=evaluated_actor_id,
        authority_policy_id=artifacts["authorization_policy"]["id"],
        authority_policy_hash=artifacts["authorization_policy"]["content_hash"],
        evaluated_authority_grant_id=(
            evaluated_grant["id"] if evaluated_grant is not None else None
        ),
        evaluated_authority_grant_hash=(
            evaluated_grant["content_hash"] if evaluated_grant is not None else None
        ),
        checked_policy_predicates=checked if checked is not None else ["actor_in_scope"],
        violated_policy_predicates=violated if violated is not None else [],
    )
    if mutate is not None:
        mutate(authority)
        authority["content_hash"] = record_hash("AuthorityAssessment", authority)
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.ASSESSMENT_RECORDED,
        transaction_time=timestamp,
        actor_id="actor:authority-monitor",
        payload={"assessment_type": "AuthorityAssessment", "assessment": authority},
    )
    return authority


def record_authority_failure(
    ledger: ProtocolLedger,
    proposal: dict,
    action: dict,
    artifacts: dict[str, dict],
    *,
    evaluated_actor_id: str = "actor:executor",
    evaluated_grant: dict | None = None,
    minute: int = 9,
    assessment_id: str = "assessment:authority:unknown",
    mutate=None,
) -> dict:
    event_id = f"event:{assessment_id}"
    timestamp = time_at(minute)
    failure, unknown = authority_monitor_failure_records(
        error=MonitoringError("authority dependency unavailable"),
        failure_id=f"failure:{assessment_id}",
        assessment_id=assessment_id,
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:authority-monitor",
        role="authority-monitor",
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=ledger.replay().acceptance_head,
        action_proposal_id=action["id"],
        action_content_hash=action["content_hash"],
        evaluated_actor_id=evaluated_actor_id,
        authority_policy_id=artifacts["authorization_policy"]["id"],
        authority_policy_hash=artifacts["authorization_policy"]["content_hash"],
        monitor_id=artifacts["authority_monitor"]["id"],
        monitor_version="1",
        monitor_hash=artifacts["authority_monitor"]["content_hash"],
        failure_category="DEPENDENCY",
        error_code="AUTHORITY_SOURCE_UNAVAILABLE",
        evaluated_authority_grant_id=(
            evaluated_grant["id"] if evaluated_grant is not None else None
        ),
        evaluated_authority_grant_hash=(
            evaluated_grant["content_hash"] if evaluated_grant is not None else None
        ),
    )
    if mutate is not None:
        mutate(failure, unknown)
        failure["content_hash"] = record_hash("MonitorFailure", failure)
        unknown["content_hash"] = record_hash("UnavailableAuthorityAssessment", unknown)
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.MONITOR_FAILED,
        transaction_time=timestamp,
        actor_id="actor:authority-monitor",
        payload={
            "failure": failure,
            "assessment_type": "UnavailableAuthorityAssessment",
            "assessment": unknown,
        },
    )
    return unknown


def transition(
    *,
    event_id: str,
    timestamp: str,
    actor_id: str,
    transition_id: str,
    subject: str,
    from_state: str,
    to_state: str,
    trigger: str,
    sequence: int,
) -> dict:
    return make_record(
        "TransitionRecord",
        event_id=event_id,
        generated_at=timestamp,
        actor_id=actor_id,
        role="state-controller",
        source_record_ids=[trigger],
        id=transition_id,
        transition_subject_id=subject,
        from_state=from_state,
        to_state=to_state,
        triggering_record_id=trigger,
        ledger_event_id=event_id,
        sequence=sequence,
        transition_time=timestamp,
    )


def decide_authorization(
    ledger: ProtocolLedger,
    proposal: dict,
    action: dict,
    claim: dict,
    epistemic: dict,
    assessments: list[dict],
    artifacts: dict[str, dict],
    *,
    authorized_actor_id: str = "actor:executor",
    cite_grant: bool | None = None,
    minute: int = 10,
    decision_id: str = "decision:authorization:1",
    mutate=None,
) -> dict:
    base = ledger.replay().acceptance_head
    policy = artifacts["authorization_policy"]
    projection = ledger.replay()
    monitors = {
        monitor_id: projection.objects[monitor_id]["record"]
        for monitor_id in policy["required_monitor_ids"]
    }
    evaluation = evaluate_authorization_policy(
        policy,
        monitors,
        assessments,
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        action_id=action["id"],
        action_content_hash=action["content_hash"],
        evaluated_actor_id=authorized_actor_id,
        base_acceptance_head=base,
    )
    if cite_grant is None:
        cite_grant = evaluation.verdict == "AUTHORIZE"
    grant = artifacts["grant"] if cite_grant else None
    event_id = f"event:{decision_id}"
    timestamp = time_at(minute)
    sources = {
        action["id"],
        claim["id"],
        epistemic["id"],
        policy["id"],
        *(item["id"] for item in assessments),
    }
    if grant is not None:
        sources.add(grant["id"])
    decision = make_record(
        "AuthorizationDecision",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:authorizer",
        role="authorizer",
        source_record_ids=sorted(sources),
        id=decision_id,
        base_acceptance_head=base,
        policy_id=policy["id"],
        policy_hash=policy["content_hash"],
        rationale_codes=[f"AUTHORIZATION_{evaluation.verdict}"],
        rationale="The deterministic authorization policy selected this control.",
        action_proposal_id=action["id"],
        action_content_hash=action["content_hash"],
        authorization_verdict=evaluation.verdict,
        epistemic_decision_ids=[epistemic["id"]],
        relied_on_claim_version_ids=[claim["id"]],
        authority_assessment_ids=list(evaluation.assessment_ids),
        triggered_assessment_ids=list(evaluation.triggered_assessment_ids),
        policy_evaluation_hash=evaluation.evaluation_hash,
        authority_grant_id=grant["id"] if grant is not None else None,
        authority_grant_hash=grant["content_hash"] if grant is not None else None,
        authorized_actor_id=authorized_actor_id,
        authorization_valid_from=timestamp if evaluation.verdict == "AUTHORIZE" else None,
        authorization_valid_to=time_at(minute + 1) if evaluation.verdict == "AUTHORIZE" else None,
    )
    if mutate is not None:
        mutate(decision)
        decision["content_hash"] = record_hash("AuthorizationDecision", decision)
    target = {
        "AUTHORIZE": "AUTHORIZED",
        "BLOCK": "BLOCKED",
        "CLARIFY": "CLARIFICATION_REQUIRED",
    }[decision["authorization_verdict"]]
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.AUTHORIZATION_DECIDED,
        transaction_time=timestamp,
        actor_id="actor:authorizer",
        payload={
            "decision": decision,
            "transition": transition(
                event_id=event_id,
                timestamp=timestamp,
                actor_id="actor:authorizer",
                transition_id=f"transition:{decision_id}",
                subject=action["id"],
                from_state="PENDING",
                to_state=target,
                trigger=decision["id"],
                sequence=ledger.replay().event_count + 1,
            ),
        },
    )
    return decision


def decide_epistemically(
    ledger: ProtocolLedger,
    proposal: dict,
    assessment: dict,
    artifacts: dict[str, dict],
    *,
    verdict: str | None = None,
    minute: int = 8,
    mutate=None,
    transition_id: str = "transition:proposal:1",
    decision_id: str = "decision:epistemic:1",
    event_id: str = "event:epistemic:1",
    requests: list[tuple[str, dict]] | None = None,
    revisions: list[dict] | None = None,
    evidence_assertion_ids: list[str] | None = None,
) -> dict:
    requests = requests or []
    revisions = revisions or []
    timestamp = time_at(minute)
    policy = artifacts["epistemic_policy"]
    monitors = {
        artifact["id"]: artifact
        for artifact in artifacts.values()
        if artifact is not None
        and artifact.get("artifact_kind") == "MONITOR_SPECIFICATION"
    }
    evaluation = evaluate_epistemic_policy(
        policy,
        monitors,
        [assessment],
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
    )
    selected_verdict = verdict or evaluation.verdict
    decision = make_record(
        "EpistemicDecision",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:reviewer",
        role="epistemic-controller",
        source_record_ids=[
            proposal["id"],
            assessment["id"],
            artifacts["epistemic_policy"]["id"],
            artifacts["rules"]["id"],
        ],
        id=decision_id,
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
        epistemic_verdict=selected_verdict,
        assessment_ids=list(evaluation.assessment_ids),
        triggered_assessment_ids=list(evaluation.triggered_assessment_ids),
        policy_evaluation_hash=evaluation.evaluation_hash,
        evidence_assertion_ids=list(evidence_assertion_ids or []),
        request_ids=[record["id"] for _, record in requests],
        claim_revision_ids=[record["id"] for record in revisions],
        policy_id=artifacts["epistemic_policy"]["id"],
        policy_hash=artifacts["epistemic_policy"]["content_hash"],
        ruleset_id=artifacts["rules"]["id"],
        ruleset_hash=artifacts["rules"]["content_hash"],
        rationale_codes=["POLICY_RESULT"],
        rationale="The versioned policy selected a verdict.",
    )
    if mutate is not None:
        mutate(decision)
        decision["content_hash"] = record_hash("EpistemicDecision", decision)
    target = {
        "ACCEPT": "ACCEPTED",
        "REJECT": "REJECTED",
        "DEFER": "DEFERRED",
        "CONTEST": "CONTESTED",
    }[decision["epistemic_verdict"]]
    sequence = ledger.replay().event_count + 1
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.EPISTEMIC_DECIDED,
        transaction_time=timestamp,
        actor_id="actor:reviewer",
        payload={
            "decision": decision,
            "requests": [
                {"record_type": record_type, "record": record}
                for record_type, record in requests
            ],
            "revisions": [
                {"record_type": "ClaimRevision", "record": record}
                for record in revisions
            ],
            "application": None,
            "transition": transition(
                event_id=event_id,
                timestamp=timestamp,
                actor_id="actor:reviewer",
                transition_id=transition_id,
                subject=proposal["id"],
                from_state="PROPOSED",
                to_state=target,
                trigger=decision["id"],
                sequence=sequence,
            ),
        },
    )
    return decision


class TestEnvelope:
    def test_external_snapshot_is_explicitly_opaque_and_anchored(self, ledger):
        event = anchor(ledger)
        projection = ledger.replay(
            expected_head_hash=event["event_hash"],
            expected_event_count=1,
        )
        assert projection.snapshot_hash == SNAPSHOT
        assert projection.acceptance_head != SNAPSHOT

    def test_first_event_must_be_anchor(self, ledger):
        with pytest.raises(ProtocolError, match="first event must anchor"):
            ledger.append_event(
                event_id="event:artifact",
                event_type=EventType.ARTIFACT_RECORDED,
                transaction_time=T0,
                actor_id="actor:system",
                payload={"artifact_type": "ProtocolArtifact", "artifact": {}},
            )
        assert not ledger.path.exists()

    @pytest.mark.parametrize(
        "kind,required_type",
        [
            ("SOURCE", "SourceArtifact"),
            ("OUTCOME_CONTRACT", "OutcomeContractArtifact"),
            ("MONITOR_SPECIFICATION", "MonitorSpecificationArtifact"),
            ("EPISTEMIC_POLICY", "EpistemicPolicyArtifact"),
        ],
    )
    def test_typed_artifact_kinds_refuse_generic_records(self, ledger, kind, required_type):
        anchor(ledger)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match=required_type):
            add_artifact(ledger, f"artifact:opaque:{kind}", kind, 1)
        assert ledger.path.read_bytes() == before


class TestContentAddressedSources:
    def test_source_builder_binds_exact_bytes(self):
        first = source_artifact_fields(
            artifact_id="artifact:source:1",
            artifact_version="1",
            source_bytes=b"invoice amount 42000",
            media_type="application/pdf",
            locator="documents/invoice.pdf",
        )
        changed = source_artifact_fields(
            artifact_id="artifact:source:1",
            artifact_version="1",
            source_bytes=b"invoice amount 42001",
            media_type="application/pdf",
            locator="documents/invoice.pdf",
        )
        assert first["source_content_digest"] == source_bytes_digest(
            b"invoice amount 42000"
        )
        assert first["source_byte_length"] == len(b"invoice amount 42000")
        assert first["source_content_digest"] != changed["source_content_digest"]
        assert first["artifact_hash"] != changed["artifact_hash"]

    def test_the_builder_is_optional_and_a_fabricated_digest_is_accepted(self):
        """R6 H3. `source_artifact_fields` is the only function in the package
        that touches a `bytes` object, and it is a caller-side convenience
        with no callers in `src/`. Everything downstream reads
        `source_content_digest` as a given, so a digest and a length that
        describe no file anywhere commit and replay.

        This is not a defect to fix at this stage; it is the boundary. The
        record makes a caller's assertion immutable and attributable, which is
        worth having, and it verifies nothing. The test exists so that the
        boundary is proven rather than described, and so that any future claim
        that the artifact 'proves byte identity' has something to fail
        against.
        """
        fabricated = source_artifact_digest(
            schema_version="1",
            artifact_id="artifact:source:phantom",
            artifact_version="1",
            source_content_digest="sha256:" + "b1" * 32,
            source_byte_length=999999,          # no such file
            source_media_type="application/pdf",
            source_locator="documents/never-existed.pdf",
        )
        assert fabricated.startswith("sha256:")
        honest = source_artifact_fields(
            artifact_id="artifact:source:phantom",
            artifact_version="1",
            source_bytes=b"31 bytes of entirely real data.",
            media_type="application/pdf",
            locator="documents/never-existed.pdf",
        )
        # Same identity function, and it cannot tell the two apart: nothing
        # in the package ever compares a declared length to real bytes.
        assert honest["source_byte_length"] == 31
        assert fabricated != honest["artifact_hash"]

    def test_source_artifact_is_replay_visible(self, ledger):
        anchor(ledger)
        source = add_source_artifact(ledger)
        replayed = ledger.replay().objects[source["id"]]
        assert replayed["record_type"] == "SourceArtifact"
        assert replayed["record"]["source_content_digest"] == source_bytes_digest(
            b"invoice INV-104 amount 42000"
        )

    @pytest.mark.parametrize(
        "field,value",
        [
            ("source_content_digest", "sha256:" + "0" * 64),
            ("source_byte_length", 1),
            ("source_media_type", "text/plain"),
            ("source_locator", "documents/other.pdf"),
        ],
    )
    def test_source_semantic_tampering_is_atomic(self, ledger, field, value):
        anchor(ledger)
        fields = source_artifact_fields(
            artifact_id="artifact:source:tampered",
            artifact_version="1",
            source_bytes=b"original bytes",
            media_type="application/pdf",
            locator="documents/original.pdf",
        )
        fields[field] = value
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="source artifact semantic hash mismatch"):
            add_artifact(
                ledger,
                "artifact:source:tampered",
                "SOURCE",
                4,
                record_type="SourceArtifact",
                **fields,
            )
        assert ledger.path.read_bytes() == before

    def test_evidence_cannot_reuse_a_different_source_record_hash(self, ledger):
        anchor(ledger)
        setup_artifacts(ledger)
        source = add_source_artifact(ledger)
        mismatched = deepcopy(source)
        mismatched["content_hash"] = "sha256:" + "0" * 64
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="Artifact hash mismatch"):
            record_proposal(
                ledger,
                evidence_count=1,
                source_artifact=mismatched,
            )
        assert ledger.path.read_bytes() == before


class TestAtomicEventBatches:
    def test_empty_batch_fails_without_change(self, ledger):
        anchor(ledger)
        before = ledger.path.read_bytes()
        with pytest.raises(LedgerError, match="batch must not be empty"):
            ledger.append_events(())
        assert ledger.path.read_bytes() == before

    def test_invalid_second_event_leaves_neither_event(self, ledger):
        anchor(ledger)
        timestamp = time_at(1)
        first = make_record(
            "ProtocolArtifact",
            event_id="event:batch:1",
            generated_at=timestamp,
            actor_id="actor:system",
            role="registrar",
            id="artifact:batch:1",
            artifact_kind="RULE_SET",
            artifact_version="1",
            artifact_hash=ARTIFACT_BODY,
        )
        second = make_record(
            "ProtocolArtifact",
            event_id="event:batch:2",
            generated_at=timestamp,
            actor_id="actor:system",
            role="registrar",
            id="artifact:batch:2",
            artifact_kind="SOURCE",
            artifact_version="1",
            artifact_hash=ARTIFACT_BODY,
        )
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="SOURCE requires SourceArtifact"):
            ledger.append_events((
                {
                    "event_id": "event:batch:1",
                    "event_type": EventType.ARTIFACT_RECORDED,
                    "transaction_time": timestamp,
                    "actor_id": "actor:system",
                    "payload": {
                        "artifact_type": "ProtocolArtifact",
                        "artifact": first,
                    },
                },
                {
                    "event_id": "event:batch:2",
                    "event_type": EventType.ARTIFACT_RECORDED,
                    "transaction_time": timestamp,
                    "actor_id": "actor:system",
                    "payload": {
                        "artifact_type": "ProtocolArtifact",
                        "artifact": second,
                    },
                },
            ))
        assert ledger.path.read_bytes() == before


class TestThinAssentPlan:
    @staticmethod
    def failure_plan(
        *,
        suffix: str = "type",
        role: str = "type-monitor",
    ) -> MonitorFailurePlan:
        return MonitorFailurePlan(
            event_id=f"event:plan:{suffix}:failed",
            failure_id=f"failure:plan:{suffix}",
            assessment_id=f"assessment:plan:{suffix}:unknown",
            transaction_time=time_at(7),
            actor_id="actor:monitor",
            role=role,
            failure_category="EXECUTION",
            error_code="FAILED",
        )

    @staticmethod
    def completed_type_event(context, *, missing_source: bool = False) -> MonitorEvent:
        event_id = "event:plan:type:satisfied"
        timestamp = time_at(7)
        sources = [context.proposal["id"], context.monitor["id"]]
        if missing_source:
            sources.append("record:does-not-exist")
        assessment = make_record(
            "TypeAssessment",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:monitor",
            role="type-monitor",
            source_record_ids=sources,
            id="assessment:plan:type:satisfied",
            proposal_id=context.proposal["id"],
            proposal_content_hash=context.proposal["content_hash"],
            base_acceptance_head=context.proposal["base_acceptance_head"],
            assessment_kind="TYPE",
            assessment_outcome="SATISFIED",
            monitor_id=context.monitor["id"],
            monitor_version=context.monitor["artifact_version"],
            monitor_hash=context.monitor["content_hash"],
            monitor_failure_id=None,
            input_record_ids=[context.proposal["id"]],
            reason_codes=["TYPE_RESULT"],
            rationale="The declared type adapter completed.",
        )
        return MonitorEvent(
            event_id=event_id,
            event_type=EventType.ASSESSMENT_RECORDED,
            transaction_time=timestamp,
            actor_id="actor:monitor",
            payload={"assessment_type": "TypeAssessment", "assessment": assessment},
        )

    def plan(self, proposal, monitor, adapter) -> AssentPlan:
        return AssentPlan(
            proposal_id=proposal["id"],
            proposal_record_hash=proposal["content_hash"],
            steps=(MonitorStep(
                monitor_id=monitor["id"],
                monitor_record_hash=monitor["content_hash"],
                adapter=adapter,
                failure=self.failure_plan(),
            ),),
        )

    def test_runs_exact_declared_adapter_once_and_replays(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        calls = []

        def adapter(context):
            calls.append(context.monitor["id"])
            with pytest.raises(TypeError):
                context.proposal["id"] = "proposal:mutated"
            return self.completed_type_event(context)

        results = self.plan(proposal, artifacts["monitor"], adapter).run(ledger)
        assert calls == [artifacts["monitor"]["id"]]
        assert results[0].assessment_outcome == "SATISFIED"
        reopened = ProtocolLedger(ledger.path, ledger.registry).replay()
        assert results[0].assessment_id in reopened.assessment_ids
        assert reopened.proposal_states[proposal["id"]] == ProposalState.PROPOSED

    def test_adapter_exception_records_unknown_without_retry(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        calls = 0

        def adapter(_context):
            nonlocal calls
            calls += 1
            raise RuntimeError("adapter dependency failed")

        result = self.plan(proposal, artifacts["monitor"], adapter).run(ledger)[0]
        projection = ledger.replay()
        assert calls == 1
        assert result.assessment_outcome == "UNKNOWN"
        assert result.assessment_id in projection.assessment_ids
        failure = projection.objects["failure:plan:type"]["record"]
        assert failure["error_message"] == "adapter dependency failed"

    def test_invalid_adapter_record_becomes_unknown_atomically(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        before_count = ledger.replay().event_count

        def adapter(context):
            return self.completed_type_event(context, missing_source=True)

        result = self.plan(proposal, artifacts["monitor"], adapter).run(ledger)[0]
        projection = ledger.replay()
        assert result.assessment_outcome == "UNKNOWN"
        assert projection.event_count == before_count + 1
        assert "assessment:plan:type:satisfied" not in projection.objects
        assert result.assessment_id in projection.assessment_ids

    def test_hash_drift_fails_before_call_or_append(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        calls = []
        plan = AssentPlan(
            proposal_id=proposal["id"],
            proposal_record_hash=proposal["content_hash"],
            steps=(MonitorStep(
                monitor_id=artifacts["monitor"]["id"],
                monitor_record_hash="sha256:" + "0" * 64,
                adapter=lambda context: calls.append(context),
                failure=self.failure_plan(),
            ),),
        )
        before = ledger.path.read_bytes()
        with pytest.raises(AssentPlanError, match="record hash differs from policy"):
            plan.run(ledger)
        assert calls == []
        assert ledger.path.read_bytes() == before

    def test_policy_coverage_mismatch_fails_before_call(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        calls = []
        plan = AssentPlan(
            proposal_id=proposal["id"],
            proposal_record_hash=proposal["content_hash"],
            steps=(MonitorStep(
                monitor_id=artifacts["logic_monitor"]["id"],
                monitor_record_hash=artifacts["logic_monitor"]["content_hash"],
                adapter=lambda context: calls.append(context),
                failure=self.failure_plan(),
            ),),
        )
        before = ledger.path.read_bytes()
        with pytest.raises(AssentPlanError, match="policy's exact monitors"):
            plan.run(ledger)
        assert calls == []
        assert ledger.path.read_bytes() == before

    def test_logical_check_and_assessment_commit_as_one_batch(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        policy = add_epistemic_policy(
            ledger,
            artifacts["rules"],
            [(artifacts["logic_monitor"], "REJECT", "DEFER")],
            5,
            policy_id="artifact:logic-only-policy",
        )
        proposal, _, _ = record_proposal(ledger, epistemic_policy=policy)

        def adapter(context):
            contract = context.input_artifacts[0]
            result = LogicCheckResult(
                candidate_digest="sha256:" + "3" * 64,
                base_state_digest="sha256:" + "4" * 64,
                candidate_state_digest="sha256:" + "5" * 64,
                context_state_digests=(),
                ontology_hash="sha256:" + "6" * 64,
                fact_contract_version="2",
                contract_id=contract["id"],
                contract_version=contract["artifact_version"],
                contract_hash=contract["artifact_hash"],
                ruleset_id=contract["ruleset_id"],
                ruleset_version=contract["ruleset_version"],
                ruleset_hash=contract["ruleset_artifact_hash"],
                engine_name="SWI-Prolog",
                engine_version="100002",
                timeout_seconds=contract["timeout_seconds"],
                facts_hash="sha256:" + "7" * 64,
                fact_count=4,
                translated_record_ids=("graph:1",),
                checked_rule_ids=tuple(contract["rule_ids"]),
                violations=(),
            )
            check_event_id = "event:plan:logic:check"
            check_time = time_at(7)
            check, witnesses = result.to_protocol_records(
                check_id="logic-check:plan:1",
                event_id=check_event_id,
                generated_at=check_time,
                actor_id="actor:monitor",
                role="logic-monitor",
                proposal_id=context.proposal["id"],
                proposal_content_hash=context.proposal["content_hash"],
                base_acceptance_head=context.proposal["base_acceptance_head"],
                monitor_id=context.monitor["id"],
                monitor_version=context.monitor["artifact_version"],
                monitor_hash=context.monitor["content_hash"],
                logic_contract_record_hash=contract["content_hash"],
                ruleset_record_hash=contract["ruleset_record_hash"],
            )
            assessment_event_id = "event:plan:logic:assessment"
            assessment_time = time_at(8)
            assessment = make_record(
                "LogicalAssessment",
                event_id=assessment_event_id,
                generated_at=assessment_time,
                actor_id="actor:monitor",
                role="logic-monitor",
                source_record_ids=[
                    context.proposal["id"],
                    context.monitor["id"],
                    check["id"],
                    contract["id"],
                    contract["ruleset_id"],
                ],
                id="assessment:plan:logic:satisfied",
                proposal_id=context.proposal["id"],
                proposal_content_hash=context.proposal["content_hash"],
                base_acceptance_head=context.proposal["base_acceptance_head"],
                assessment_kind="LOGICAL",
                assessment_outcome="SATISFIED",
                monitor_id=context.monitor["id"],
                monitor_version=context.monitor["artifact_version"],
                monitor_hash=context.monitor["content_hash"],
                monitor_failure_id=None,
                input_record_ids=[context.proposal["id"], check["id"]],
                reason_codes=["LOGIC_CHECK_COMPLETED"],
                rationale="The declared logic adapter completed.",
                checked_rule_ids=check["checked_rule_ids"],
                violated_rule_ids=check["violated_rule_ids"],
                logic_check_record_ids=[check["id"]],
                logic_contract_id=contract["id"],
                logic_contract_record_hash=contract["content_hash"],
                ruleset_id=contract["ruleset_id"],
                ruleset_hash=contract["ruleset_record_hash"],
            )
            return (
                MonitorEvent(
                    event_id=check_event_id,
                    event_type=EventType.LOGIC_CHECK_RECORDED,
                    transaction_time=check_time,
                    actor_id="actor:monitor",
                    payload={"check": check, "witnesses": list(witnesses)},
                ),
                MonitorEvent(
                    event_id=assessment_event_id,
                    event_type=EventType.ASSESSMENT_RECORDED,
                    transaction_time=assessment_time,
                    actor_id="actor:monitor",
                    payload={
                        "assessment_type": "LogicalAssessment",
                        "assessment": assessment,
                    },
                ),
            )

        plan = AssentPlan(
            proposal_id=proposal["id"],
            proposal_record_hash=proposal["content_hash"],
            steps=(MonitorStep(
                monitor_id=artifacts["logic_monitor"]["id"],
                monitor_record_hash=artifacts["logic_monitor"]["content_hash"],
                adapter=adapter,
                failure=self.failure_plan(suffix="logic", role="logic-monitor"),
            ),),
        )
        before_count = ledger.replay().event_count
        result = plan.run(ledger)[0]
        projection = ProtocolLedger(ledger.path, ledger.registry).replay()
        assert result.assessment_outcome == "SATISFIED"
        assert result.event_ids == (
            "event:plan:logic:check",
            "event:plan:logic:assessment",
        )
        assert projection.event_count == before_count + 2
        assert "logic-check:plan:1" in projection.logic_check_ids
        assert result.assessment_id in projection.assessment_ids

    def test_logical_adapter_exception_records_bound_unknown(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        policy = add_epistemic_policy(
            ledger,
            artifacts["rules"],
            [(artifacts["logic_monitor"], "REJECT", "DEFER")],
            5,
            policy_id="artifact:logic-failure-policy",
        )
        proposal, _, _ = record_proposal(ledger, epistemic_policy=policy)
        plan = AssentPlan(
            proposal_id=proposal["id"],
            proposal_record_hash=proposal["content_hash"],
            steps=(MonitorStep(
                monitor_id=artifacts["logic_monitor"]["id"],
                monitor_record_hash=artifacts["logic_monitor"]["content_hash"],
                adapter=lambda _context: (_ for _ in ()).throw(
                    LogicExecutionError("Prolog process unavailable")
                ),
                failure=self.failure_plan(suffix="logic", role="logic-monitor"),
            ),),
        )
        result = plan.run(ledger)[0]
        unknown = ledger.replay().objects[result.assessment_id]["record"]
        assert result.assessment_outcome == "UNKNOWN"
        assert unknown["logic_contract_id"] == artifacts["logic_contract"]["id"]
        assert unknown["ruleset_id"] == artifacts["rules"]["id"]


class TestGenericEffectLifecycle:
    @staticmethod
    def authorized_action(ledger, *, authority_outcome: str = "SATISFIED"):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        outcome_contract = add_outcome_contract(ledger)
        proposal, claim, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        epistemic = decide_epistemically(ledger, proposal, assessment, artifacts)
        authority = record_authority_assessment(
            ledger,
            proposal,
            action,
            artifacts,
            outcome=authority_outcome,
            violated=(
                ["actor_in_scope"] if authority_outcome == "VIOLATED" else []
            ),
        )
        authorization = decide_authorization(
            ledger,
            proposal,
            action,
            claim,
            epistemic,
            [authority],
            artifacts,
        )
        return artifacts, outcome_contract, proposal, action, authorization

    @staticmethod
    def dispatch(
        ledger,
        action,
        authorization,
        *,
        suffix: str = "1",
        minute: int = 10,
        mutate=None,
    ):
        event_id = f"event:dispatch:{suffix}"
        timestamp = time_at(minute)
        record = make_record(
            "ActionDispatch",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:dispatcher",
            role="dispatcher",
            source_record_ids=[action["id"], authorization["id"]],
            id=f"dispatch:{suffix}",
            action_proposal_id=action["id"],
            action_content_hash=action["content_hash"],
            authorization_decision_id=authorization["id"],
            authorization_decision_hash=authorization["content_hash"],
            executor_id="actor:executor",
            dispatch_adapter_id="adapter:research-effect-store:v1",
            base_acceptance_head=authorization["base_acceptance_head"],
            dispatched_at=timestamp,
        )
        if mutate is not None:
            mutate(record)
            record["content_hash"] = record_hash("ActionDispatch", record)
        ledger.append_event(
            event_id=event_id,
            event_type=EventType.ACTION_DISPATCHED,
            transaction_time=timestamp,
            actor_id="actor:dispatcher",
            payload={"dispatch": record},
        )
        return record

    @staticmethod
    def execute(ledger, dispatch, *, mutate=None):
        event_id = "event:execution:1"
        timestamp = time_at(11)
        record = make_record(
            "ActionExecution",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:executor",
            role="executor",
            source_record_ids=[dispatch["id"]],
            id="execution:1",
            dispatch_id=dispatch["id"],
            dispatch_hash=dispatch["content_hash"],
            executor_id="actor:executor",
            execution_started_at=time_at(10),
            execution_ended_at=timestamp,
            execution_status="SUCCEEDED",
            execution_result_hash="sha256:" + "c" * 64,
        )
        if mutate is not None:
            mutate(record)
            record["content_hash"] = record_hash("ActionExecution", record)
        ledger.append_event(
            event_id=event_id,
            event_type=EventType.ACTION_EXECUTED,
            transaction_time=timestamp,
            actor_id="actor:executor",
            payload={"execution": record},
        )
        return record

    @staticmethod
    def observe(
        ledger,
        execution,
        contract,
        *,
        observer_id: str = "actor:external-observer",
        mutate=None,
    ):
        fields = source_artifact_fields(
            artifact_id="artifact:source:effect-store",
            artifact_version="1",
            source_bytes=b'{"action_id":"action:1","status":"written"}\n',
            media_type="application/x-ndjson",
            locator="effects/payments.jsonl",
        )
        source = add_artifact(
            ledger,
            "artifact:source:effect-store",
            "SOURCE",
            11,
            record_type="SourceArtifact",
            **fields,
        )
        event_id = "event:outcome:1"
        timestamp = time_at(12)
        record = make_record(
            "OutcomeObservation",
            event_id=event_id,
            generated_at=timestamp,
            actor_id=observer_id,
            role="outcome-observer",
            source_record_ids=[execution["id"], contract["id"], source["id"]],
            id="outcome:1",
            execution_id=execution["id"],
            execution_hash=execution["content_hash"],
            outcome_contract_id=contract["id"],
            outcome_contract_hash=contract["content_hash"],
            observer_id=observer_id,
            observation_type=contract["observation_type"],
            observation_result="CONFIRMED",
            observed_at=timestamp,
            observed_source_artifact_id=source["id"],
            observed_source_artifact_hash=source["content_hash"],
        )
        if mutate is not None:
            mutate(record)
            record["content_hash"] = record_hash("OutcomeObservation", record)
        ledger.append_event(
            event_id=event_id,
            event_type=EventType.OUTCOME_OBSERVED,
            transaction_time=timestamp,
            actor_id=observer_id,
            payload={"observation": record},
        )
        return source, record

    def test_authorized_effect_lifecycle_reopens_with_complete_trace(self, ledger):
        _, contract, _, action, authorization = self.authorized_action(ledger)
        dispatch = self.dispatch(ledger, action, authorization)
        execution = self.execute(ledger, dispatch)
        source, observation = self.observe(ledger, execution, contract)
        projection = ProtocolLedger(ledger.path, ledger.registry).replay()
        assert projection.dispatch_by_action[action["id"]] == dispatch["id"]
        assert projection.execution_by_dispatch[dispatch["id"]] == execution["id"]
        assert projection.observation_by_execution_contract[
            (execution["id"], contract["id"])
        ] == observation["id"]
        assert source["id"] in projection.artifact_ids
        assert observation["id"] in projection.outcome_observation_ids

    def test_blocked_action_cannot_create_dispatch(self, ledger):
        _, _, _, action, authorization = self.authorized_action(
            ledger,
            authority_outcome="VIOLATED",
        )
        assert authorization["authorization_verdict"] == "BLOCK"
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="not authorized for dispatch"):
            self.dispatch(ledger, action, authorization)
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize(
        "mutate,message",
        [
            (
                lambda record: record.update(
                    authorization_decision_hash="sha256:" + "0" * 64
                ),
                "dispatch authorization hash mismatch",
            ),
            (
                lambda record: record.update(executor_id="actor:someone-else"),
                "dispatch executor mismatch",
            ),
            (
                lambda record: record.update(dispatched_at=time_at(11)),
                "dispatched_at must equal event time",
            ),
        ],
    )
    def test_dispatch_is_bound_to_exact_authorization(self, ledger, mutate, message):
        _, _, _, action, authorization = self.authorized_action(ledger)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match=message):
            self.dispatch(ledger, action, authorization, mutate=mutate)
        assert ledger.path.read_bytes() == before

    def test_expired_authorization_cannot_dispatch(self, ledger):
        _, _, _, action, authorization = self.authorized_action(ledger)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="outside authorization validity"):
            self.dispatch(ledger, action, authorization, minute=11)
        assert ledger.path.read_bytes() == before

    def test_changed_accepted_state_makes_authorization_stale(self, ledger):
        artifacts, _, _, action, authorization = self.authorized_action(ledger)
        other, _, _ = record_proposal(
            ledger,
            minute=10,
            proposal_id="proposal:other",
            proposal_key="proposal-key:other",
            claim_id="claim:other",
            claim_key="claim-key:other",
        )
        other_assessment = record_type_assessment(
            ledger,
            other,
            artifacts["monitor"],
            minute=10,
            assessment_id="assessment:other",
        )
        decide_epistemically(
            ledger,
            other,
            other_assessment,
            artifacts,
            minute=10,
            decision_id="decision:epistemic:other",
            event_id="event:epistemic:other",
            transition_id="transition:proposal:other",
        )
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="dispatch authorization is stale"):
            self.dispatch(ledger, action, authorization)
        assert ledger.path.read_bytes() == before

    def test_second_dispatch_is_refused_without_claiming_external_exactly_once(self, ledger):
        _, _, _, action, authorization = self.authorized_action(ledger)
        self.dispatch(ledger, action, authorization)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="already has a recorded dispatch"):
            self.dispatch(ledger, action, authorization, suffix="2")
        assert ledger.path.read_bytes() == before

    def test_execution_must_bind_dispatch_and_executor(self, ledger):
        _, _, _, action, authorization = self.authorized_action(ledger)
        dispatch = self.dispatch(ledger, action, authorization)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="execution actor mismatch"):
            self.execute(
                ledger,
                dispatch,
                mutate=lambda record: record.update(executor_id="actor:other"),
            )
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize(
        "mutate,message",
        [
            (
                lambda record: record.update(observer_id="actor:executor"),
                "observer must record its own observation",
            ),
            (
                lambda record: record.update(
                    observed_source_artifact_hash="sha256:" + "0" * 64
                ),
                "Artifact hash mismatch",
            ),
        ],
    )
    def test_outcome_requires_independent_observer_and_exact_state_source(
        self,
        ledger,
        mutate,
        message,
    ):
        _, contract, _, action, authorization = self.authorized_action(ledger)
        dispatch = self.dispatch(ledger, action, authorization)
        execution = self.execute(ledger, dispatch)
        before_count = ledger.replay().event_count
        with pytest.raises(ProtocolError, match=message):
            self.observe(ledger, execution, contract, mutate=mutate)
        projection = ledger.replay()
        assert projection.event_count == before_count + 1
        assert "outcome:1" not in projection.objects

    def test_executor_cannot_certify_its_own_outcome(self, ledger):
        _, contract, _, action, authorization = self.authorized_action(ledger)
        dispatch = self.dispatch(ledger, action, authorization)
        execution = self.execute(ledger, dispatch)
        before_count = ledger.replay().event_count
        with pytest.raises(ProtocolError, match="observer must differ from executor"):
            self.observe(
                ledger,
                execution,
                contract,
                observer_id="actor:executor",
            )
        assert ledger.replay().event_count == before_count + 1

    def test_outcome_contract_semantic_tampering_is_atomic(self, ledger):
        anchor(ledger)
        fields = {
            "outcome_contract_schema_version": "1",
            "observation_type": "EXPECTED_EFFECT_PRESENT",
            "observer_implementation_hash": "sha256:" + "b" * 64,
        }
        artifact_hash = outcome_contract_digest(
            schema_version="1",
            contract_id="artifact:outcome-contract:tampered",
            contract_version="1",
            observation_type=fields["observation_type"],
            observer_implementation_hash=fields["observer_implementation_hash"],
        )
        fields["observation_type"] = "DIFFERENT_CHECK"
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="outcome contract semantic hash mismatch"):
            add_artifact(
                ledger,
                "artifact:outcome-contract:tampered",
                "OUTCOME_CONTRACT",
                1,
                record_type="OutcomeContractArtifact",
                artifact_hash=artifact_hash,
                **fields,
            )
        assert ledger.path.read_bytes() == before


class TestArtifactContracts:
    @pytest.mark.parametrize(
        "case,message",
        [
            ("input_hash", "input artifact hash mismatch"),
            ("semantic_hash", "monitor semantic hash mismatch"),
            ("sources", "source_record_ids missing required records"),
        ],
    )
    def test_monitor_specification_replay_binds_inputs_and_semantics(
        self,
        ledger,
        case,
        message,
    ):
        anchor(ledger)
        contract = add_artifact(ledger, "artifact:contract", "EVIDENCE_CONTRACT", 1)
        input_hash = contract["content_hash"]
        sources = [contract["id"]]
        if case == "input_hash":
            input_hash = "sha256:" + "0" * 64
        elif case == "sources":
            sources = []
        semantic_hash = monitor_specification_digest(
            schema_version="1",
            monitor_id="artifact:evidence-monitor",
            monitor_version="1",
            assessment_kind="EVIDENCE_COMPLETENESS",
            implementation_hash="sha256:" + "a" * 64,
            input_artifact_ids=[contract["id"]],
            input_artifact_record_hashes=[input_hash],
        )
        if case == "semantic_hash":
            semantic_hash = "sha256:" + "0" * 64

        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match=message):
            add_artifact(
                ledger,
                "artifact:evidence-monitor",
                "MONITOR_SPECIFICATION",
                2,
                record_type="MonitorSpecificationArtifact",
                artifact_hash=semantic_hash,
                monitor_schema_version="1",
                assessment_kind="EVIDENCE_COMPLETENESS",
                monitor_implementation_hash="sha256:" + "a" * 64,
                input_artifact_ids=[contract["id"]],
                input_artifact_record_hashes=[input_hash],
                source_record_ids=sources,
            )
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize(
        "case,message",
        [
            ("monitor_hash", "Artifact hash mismatch"),
            ("semantic_hash", "policy semantic hash mismatch"),
            ("authority_monitor", "cannot require AUTHORITY monitor"),
            ("sources", "source_record_ids missing required records"),
        ],
    )
    def test_epistemic_policy_replay_binds_exact_monitors_and_semantics(
        self,
        ledger,
        case,
        message,
    ):
        anchor(ledger)
        rules = add_artifact(ledger, "artifact:rules", "RULE_SET", 1)
        monitor = add_monitor(
            ledger,
            "artifact:policy-monitor",
            "AUTHORITY" if case == "authority_monitor" else "TYPE",
            2,
        )
        monitor_hash = monitor["content_hash"]
        sources = [rules["id"], monitor["id"]]
        if case == "monitor_hash":
            monitor_hash = "sha256:" + "0" * 64
        elif case == "sources":
            sources = [rules["id"]]
        fields = {
            "policy_schema_version": "1",
            "ruleset_id": rules["id"],
            "ruleset_record_hash": rules["content_hash"],
            "ruleset_artifact_hash": rules["artifact_hash"],
            "required_monitor_ids": [monitor["id"]],
            "required_monitor_record_hashes": [monitor_hash],
            "violation_verdicts": ["REJECT"],
            "unknown_verdicts": ["DEFER"],
            "control_precedence": ["REJECT", "CONTEST", "DEFER"],
            "source_record_ids": sources,
        }
        semantic_hash = epistemic_policy_digest(
            schema_version="1",
            policy_id="artifact:epistemic-policy",
            policy_version="1",
            ruleset_id=fields["ruleset_id"],
            ruleset_record_hash=fields["ruleset_record_hash"],
            ruleset_artifact_hash=fields["ruleset_artifact_hash"],
            required_monitor_ids=fields["required_monitor_ids"],
            required_monitor_record_hashes=fields["required_monitor_record_hashes"],
            violation_verdicts=fields["violation_verdicts"],
            unknown_verdicts=fields["unknown_verdicts"],
            control_precedence=fields["control_precedence"],
        )
        if case == "semantic_hash":
            semantic_hash = "sha256:" + "0" * 64

        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match=message):
            add_artifact(
                ledger,
                "artifact:epistemic-policy",
                "EPISTEMIC_POLICY",
                3,
                record_type="EpistemicPolicyArtifact",
                artifact_hash=semantic_hash,
                **fields,
            )
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize(
        "mutate,message",
        [
            (lambda event: event.update(sequence=2), "sequence must be 1"),
            (lambda event: event.update(transaction_time="2026-08-12T08:00:00"), "timezone"),
            (lambda event: event["payload"].update(extra=True), "unknown fields"),
        ],
    )
    def test_corrupt_envelope_fails_closed(self, ledger, mutate, message):
        event = anchor(ledger)
        mutate(event)
        event["event_hash"] = event_hash(event)
        ledger.path.write_text(canonical_json(event) + "\n", encoding="utf-8")
        with pytest.raises(LedgerError, match=message):
            ledger.replay()

    def test_duplicate_key_nonfinite_and_truncation_fail_closed(self, ledger):
        event = anchor(ledger)
        raw = canonical_json(event)
        duplicate = raw.replace('"schema_version":"1"', '"schema_version":"1","schema_version":"1"')
        ledger.path.write_text(duplicate + "\n", encoding="utf-8")
        with pytest.raises(LedgerError, match="duplicate JSON key"):
            ledger.replay()
        nonfinite = raw.replace('"record_count":200', '"record_count":NaN')
        ledger.path.write_text(nonfinite + "\n", encoding="utf-8")
        with pytest.raises(LedgerError, match="nonfinite JSON number"):
            ledger.replay()
        ledger.path.write_text(raw, encoding="utf-8")
        with pytest.raises(LedgerError, match="truncated final record"):
            ledger.replay()

    def test_interrupted_append_preserves_last_valid_ledger(self, ledger, monkeypatch):
        anchor(ledger)
        before = ledger.path.read_bytes()
        real_write = __import__("os").write
        writes = 0

        def interrupted_write(descriptor, value):
            nonlocal writes
            writes += 1
            if writes == 1:
                return real_write(descriptor, value[:17])
            raise OSError("injected append failure")

        monkeypatch.setattr("malleus.ledger.os.write", interrupted_write)
        with pytest.raises(LedgerError, match="failed without changing the ledger"):
            add_artifact(ledger, "artifact:interrupted", "RULE_SET", 1)
        assert ledger.path.read_bytes() == before
        assert ledger.replay().event_count == 1
        assert list(ledger.path.parent.glob(f".{ledger.path.name}.*.tmp")) == []

    @pytest.mark.parametrize("operation", ["fsync", "replace"])
    def test_failed_ledger_commit_preserves_last_valid_file(
        self,
        ledger,
        monkeypatch,
        operation,
    ):
        anchor(ledger)
        before = ledger.path.read_bytes()

        def fail(*_args):
            raise OSError(f"injected {operation} failure")

        monkeypatch.setattr(f"malleus.ledger.os.{operation}", fail)
        with pytest.raises(LedgerError, match="failed without changing the ledger"):
            add_artifact(ledger, f"artifact:{operation}", "RULE_SET", 1)
        assert ledger.path.read_bytes() == before
        assert ledger.replay().event_count == 1
        assert list(ledger.path.parent.glob(f".{ledger.path.name}.*.tmp")) == []

    def test_protocol_ledger_has_no_public_raw_storage_mutator(self, ledger):
        assert not hasattr(ledger, "storage")

    def test_hash_chain_and_external_anchor_checks_detect_corruption(self, ledger):
        first = anchor(ledger)
        add_monitor(ledger, "artifact:monitor", "TYPE", 1)
        events = [json.loads(line) for line in ledger.path.read_text(encoding="utf-8").splitlines()]
        events[0]["actor_id"] = "actor:tampered"
        ledger.path.write_text(
            "\n".join(canonical_json(event) for event in events) + "\n",
            encoding="utf-8",
        )
        with pytest.raises(LedgerError, match="event_hash mismatch"):
            ledger.replay()

        ledger.path.write_text(canonical_json(first) + "\n", encoding="utf-8")
        with pytest.raises(LedgerError, match="Ledger event count mismatch"):
            ledger.replay(expected_event_count=2)
        with pytest.raises(LedgerError, match="Ledger head mismatch"):
            ledger.replay(expected_head_hash="sha256:" + "9" * 64)

    def test_broken_previous_hash_is_rejected(self, ledger):
        anchor(ledger)
        add_monitor(ledger, "artifact:monitor", "TYPE", 1)
        events = [json.loads(line) for line in ledger.path.read_text(encoding="utf-8").splitlines()]
        events[1]["previous_event_hash"] = "sha256:" + "9" * 64
        events[1]["event_hash"] = event_hash(events[1])
        ledger.path.write_text(
            "\n".join(canonical_json(event) for event in events) + "\n",
            encoding="utf-8",
        )
        with pytest.raises(LedgerError, match="previous_event_hash mismatch"):
            ledger.replay()

    def test_boolean_sequence_is_not_an_integer(self, ledger):
        event = anchor(ledger)
        event["sequence"] = True
        event["event_hash"] = event_hash(event)
        ledger.path.write_text(canonical_json(event) + "\n", encoding="utf-8")
        with pytest.raises(LedgerError, match="sequence must be 1"):
            ledger.replay()


class TestProposalAndEpistemicState:
    def test_acceptance_is_replay_derived(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, claim, _ = record_proposal(ledger)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        monitored = ledger.replay()
        assert monitored.proposal_states[proposal["id"]] == ProposalState.PROPOSED
        assert not monitored.epistemic_decision_ids
        decide_epistemically(ledger, proposal, assessment, artifacts)
        first = ledger.replay()
        second = ledger.replay()
        assert first.proposal_states[proposal["id"]] == ProposalState.ACCEPTED
        assert first.current_claim_by_key[claim["claim_key"]] == claim["id"]
        assert first.acceptance_head == second.acceptance_head
        assert "state" not in proposal

    @pytest.mark.parametrize(
        "claim_valid_from,message",
        [
            (
                "2026-01-27T12:00:00-08:00",
                "Inlined property 'domain_valid_from' must be a mapping",
            ),
            (
                {
                    "valid_time_precision": "CALENDAR_DAY",
                    "calendar_date": "2026-01-27",
                    "timezone_database_version": "2026c",
                    "indeterminacy_reason": "The source establishes only the day.",
                },
                "missing timezone",
            ),
            (
                {
                    "valid_time_precision": "CALENDAR_DAY",
                    "calendar_date": "2026-01-27",
                    "timezone": "PST",
                    "timezone_database_version": "2026c",
                    "indeterminacy_reason": "The source establishes only the day.",
                },
                "installed IANA zone",
            ),
            (
                {
                    "valid_time_precision": "CALENDAR_DAY",
                    "calendar_date": "2026-01-27",
                    "timezone": "America/Los_Angeles",
                    "timezone_database_version": "2026c",
                },
                "missing indeterminacy_reason",
            ),
        ],
    )
    def test_claim_valid_time_old_path_and_unexplained_uncertainty_fail_closed(
        self,
        ledger,
        claim_valid_from,
        message,
    ):
        anchor(ledger)
        setup_artifacts(ledger)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match=message):
            record_proposal(ledger, claim_valid_from=claim_valid_from)
        assert ledger.path.read_bytes() == before

    def test_claim_calendar_day_preserves_zone_and_extracted_reason(self, ledger):
        anchor(ledger)
        setup_artifacts(ledger)
        valid_time = ValidTime.calendar_day(
            "2026-01-27",
            timezone="America/Los_Angeles",
            indeterminacy_reason="The invoice states the day but no installation time.",
        ).as_dict()
        _, claim, _ = record_proposal(ledger, claim_valid_from=valid_time)
        replayed = ledger.replay().objects[claim["id"]]["record"]
        assert replayed["domain_valid_from"] == valid_time

    @pytest.mark.parametrize(
        "verdict,state",
        [
            ("REJECT", ProposalState.REJECTED),
            ("DEFER", ProposalState.DEFERRED),
            ("CONTEST", ProposalState.CONTESTED),
        ],
    )
    def test_nonacceptance_does_not_advance_acceptance_head(self, ledger, verdict, state):
        anchor(ledger)
        artifacts = setup_artifacts(ledger, violation_verdict=verdict)
        proposal, _, _ = record_proposal(ledger)
        assessment = record_type_assessment(
            ledger,
            proposal,
            artifacts["monitor"],
            outcome="VIOLATED",
        )
        before = ledger.replay().acceptance_head
        decide_epistemically(ledger, proposal, assessment, artifacts)
        projection = ledger.replay()
        assert projection.proposal_states[proposal["id"]] == state
        assert projection.acceptance_head == before

    def test_violated_assessment_cannot_support_accept(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        assessment = record_type_assessment(
            ledger,
            proposal,
            artifacts["monitor"],
            outcome="VIOLATED",
        )
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="verdict differs from deterministic policy"):
            decide_epistemically(ledger, proposal, assessment, artifacts, verdict="ACCEPT")
        assert ledger.path.read_bytes() == before

    def test_exact_monitor_can_produce_only_one_output_per_proposal(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        first = record_type_assessment(ledger, proposal, artifacts["monitor"])
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="monitor already produced assessment"):
            record_type_assessment(
                ledger,
                proposal,
                artifacts["monitor"],
                outcome="VIOLATED",
                minute=8,
            )
        assert ledger.path.read_bytes() == before
        assert ledger.replay().monitor_output_ids[
            (proposal["id"], artifacts["monitor"]["id"])
        ] == first["id"]

    def test_proposal_policy_cannot_be_replaced_after_monitoring(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        late_policy = add_epistemic_policy(
            ledger,
            artifacts["rules"],
            [(artifacts["monitor"], "CONTEST", "CONTEST")],
            8,
            policy_id="artifact:late-policy",
        )
        late_artifacts = {**artifacts, "epistemic_policy": late_policy}
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="decision policy differs from proposal"):
            decide_epistemically(
                ledger,
                proposal,
                assessment,
                late_artifacts,
                minute=9,
            )
        assert ledger.path.read_bytes() == before

    def test_custom_assessment_subclass_cannot_bypass_kind_contract(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        event_id = "event:forged-logical-assessment"
        timestamp = time_at(7)
        assessment = make_record(
            "ForgedLogicalAssessment",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:monitor",
            role="logic-monitor",
            source_record_ids=[proposal["id"], artifacts["logic_monitor"]["id"]],
            id="assessment:forged-logical",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            assessment_kind="LOGICAL",
            assessment_outcome="SATISFIED",
            monitor_id=artifacts["logic_monitor"]["id"],
            monitor_version="1",
            monitor_hash=artifacts["logic_monitor"]["content_hash"],
            monitor_failure_id=None,
            input_record_ids=[proposal["id"]],
            reason_codes=["FORGED"],
            rationale="Attempted to bypass the logical assessment contract.",
        )
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="LOGICAL monitor requires LogicalAssessment"):
            ledger.append_event(
                event_id=event_id,
                event_type=EventType.ASSESSMENT_RECORDED,
                transaction_time=timestamp,
                actor_id="actor:monitor",
                payload={
                    "assessment_type": "ForgedLogicalAssessment",
                    "assessment": assessment,
                },
            )
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize(
        "outcome,missing_requirements,error",
        [
            ("SATISFIED", [], None),
            ("VIOLATED", ["requirement:citation"], None),
            ("SATISFIED", ["requirement:citation"], "has missing requirements"),
            ("VIOLATED", [], "has no missing requirement"),
        ],
    )
    def test_evidence_completeness_outcome_matches_missing_requirements(
        self,
        ledger,
        outcome,
        missing_requirements,
        error,
    ):
        anchor(ledger)
        rules = add_artifact(ledger, "artifact:rules", "RULE_SET", 1)
        contract = add_artifact(ledger, "artifact:evidence-contract", "EVIDENCE_CONTRACT", 1)
        monitor = add_monitor(
            ledger,
            "artifact:evidence-monitor",
            "EVIDENCE_COMPLETENESS",
            2,
            input_artifacts=[contract],
        )
        add_epistemic_policy(
            ledger,
            rules,
            [(monitor, "REJECT", "DEFER")],
            3,
        )
        proposal, _, _ = record_proposal(ledger)
        event_id = "event:evidence-assessment"
        timestamp = time_at(7)
        assessment = make_record(
            "EvidenceCompletenessAssessment",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:monitor",
            role="evidence-monitor",
            source_record_ids=[proposal["id"], monitor["id"], contract["id"]],
            id="assessment:evidence",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            assessment_kind="EVIDENCE_COMPLETENESS",
            assessment_outcome=outcome,
            monitor_id=monitor["id"],
            monitor_version="1",
            monitor_hash=monitor["content_hash"],
            monitor_failure_id=None,
            input_record_ids=[proposal["id"]],
            reason_codes=["EVIDENCE_RESULT"],
            rationale="The evidence contract was evaluated.",
            evidence_contract_id=contract["id"],
            evidence_contract_hash=contract["content_hash"],
            missing_requirement_ids=missing_requirements,
        )
        def append():
            return ledger.append_event(
                event_id=event_id,
                event_type=EventType.ASSESSMENT_RECORDED,
                transaction_time=timestamp,
                actor_id="actor:monitor",
                payload={
                    "assessment_type": "EvidenceCompletenessAssessment",
                    "assessment": assessment,
                },
            )
        if error is None:
            append()
            assert assessment["id"] in ledger.replay().assessment_ids
        else:
            before = ledger.path.read_bytes()
            with pytest.raises(ProtocolError, match=error):
                append()
            assert ledger.path.read_bytes() == before

    def test_decision_requires_every_policy_selected_monitor(self, ledger):
        anchor(ledger)
        rules = add_artifact(ledger, "artifact:rules", "RULE_SET", 1)
        type_monitor = add_monitor(ledger, "artifact:type-monitor", "TYPE", 2)
        conflict_monitor = add_monitor(ledger, "artifact:conflict-monitor", "CONFLICT", 2)
        policy = add_epistemic_policy(
            ledger,
            rules,
            [
                (type_monitor, "REJECT", "DEFER"),
                (conflict_monitor, "CONTEST", "DEFER"),
            ],
            3,
        )
        proposal, _, _ = record_proposal(ledger)
        assessment = record_type_assessment(ledger, proposal, type_monitor)
        event_id = "event:missing-monitor-decision"
        timestamp = time_at(8)
        decision = make_record(
            "EpistemicDecision",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:reviewer",
            role="epistemic-controller",
            source_record_ids=[proposal["id"], assessment["id"], policy["id"], rules["id"]],
            id="decision:missing-monitor",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            epistemic_verdict="ACCEPT",
            assessment_ids=[assessment["id"]],
            triggered_assessment_ids=[],
            policy_evaluation_hash="sha256:" + "9" * 64,
            evidence_assertion_ids=[],
            request_ids=[],
            claim_revision_ids=[],
            policy_id=policy["id"],
            policy_hash=policy["content_hash"],
            ruleset_id=rules["id"],
            ruleset_hash=rules["content_hash"],
            rationale_codes=["POLICY_RESULT"],
            rationale="Attempted decision with incomplete monitor coverage.",
        )
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="has no assessment"):
            ledger.append_event(
                event_id=event_id,
                event_type=EventType.EPISTEMIC_DECIDED,
                transaction_time=timestamp,
                actor_id="actor:reviewer",
                payload={
                    "decision": decision,
                    "requests": [],
                    "revisions": [],
                    "application": None,
                    "transition": transition(
                        event_id=event_id,
                        timestamp=timestamp,
                        actor_id="actor:reviewer",
                        transition_id="transition:missing-monitor",
                        subject=proposal["id"],
                        from_state="PROPOSED",
                        to_state="ACCEPTED",
                        trigger=decision["id"],
                        sequence=ledger.replay().event_count + 1,
                    ),
                },
            )
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize(
        "mutate,message",
        [
            (
                lambda decision: decision.update(triggered_assessment_ids=[]),
                "triggered assessments differ",
            ),
            (
                lambda decision: decision.update(policy_evaluation_hash="sha256:" + "0" * 64),
                "policy evaluation hash mismatch",
            ),
            (
                lambda decision: decision.update(source_record_ids=[]),
                "source_record_ids missing required records",
            ),
        ],
    )
    def test_policy_control_record_is_replay_bound(self, ledger, mutate, message):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        assessment = record_type_assessment(
            ledger,
            proposal,
            artifacts["monitor"],
            outcome="VIOLATED",
        )
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match=message):
            decide_epistemically(
                ledger,
                proposal,
                assessment,
                artifacts,
                mutate=mutate,
            )
        assert ledger.path.read_bytes() == before

    def test_decision_and_transition_ids_must_be_distinct(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="introduced record IDs contain duplicates"):
            decide_epistemically(
                ledger,
                proposal,
                assessment,
                artifacts,
                transition_id="decision:epistemic:1",
            )
        assert ledger.path.read_bytes() == before

    def test_state_outputs_cannot_be_smuggled_as_proposal_members(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal = make_record(
            "ProposedSubgraph",
            event_id="event:proposal:1",
            generated_at=time_at(6),
            actor_id="actor:proposer",
            role="proposer",
            source_record_ids=[artifacts["epistemic_policy"]["id"]],
            id="proposal:1",
            proposal_key="proposal-key",
            revision=1,
            revises_proposal_id=None,
            base_acceptance_head=ledger.replay().acceptance_head,
            epistemic_policy_id=artifacts["epistemic_policy"]["id"],
            epistemic_policy_hash=artifacts["epistemic_policy"]["content_hash"],
            member_content_hashes=["sha256:" + "9" * 64],
            claim_version_ids=[],
            evidence_ids=[],
            evidence_assertion_ids=[],
            action_proposal_ids=[],
        )
        with pytest.raises(ProtocolError, match="not an allowed proposed content type"):
            ledger.append_event(
                event_id="event:proposal:1",
                event_type=EventType.PROPOSAL_RECORDED,
                transaction_time=time_at(6),
                actor_id="actor:proposer",
                payload={
                    "proposal": proposal,
                    "members": [{"record_type": "TransitionRecord", "record": {}}],
                },
            )

    def test_record_attribution_must_match_event(self, ledger):
        anchor(ledger)
        artifact = make_record(
            "ProtocolArtifact",
            event_id="event:wrong",
            generated_at=time_at(1),
            actor_id="actor:system",
            role="registrar",
            id="artifact:monitor",
            artifact_kind="MONITOR_SPECIFICATION",
            artifact_version="1",
            artifact_hash=ARTIFACT_BODY,
        )
        with pytest.raises(ProtocolError, match="generation_event_id mismatch"):
            ledger.append_event(
                event_id="event:artifact",
                event_type=EventType.ARTIFACT_RECORDED,
                transaction_time=time_at(1),
                actor_id="actor:system",
                payload={"artifact_type": "ProtocolArtifact", "artifact": artifact},
            )

    def test_runtime_required_list_presence_fails_with_protocol_error(self, ledger):
        anchor(ledger)
        event_id = "event:proposal:1"
        timestamp = time_at(1)
        claim = make_record(
            "ClaimVersion",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:proposer",
            role="proposer",
            id="claim:1",
            claim_key="claim-key",
            revision=1,
            revises_claim_version_id=None,
            statement="test",
            domain_valid_from=valid_time_at(timestamp),
            domain_valid_to=None,
            dependency_ids=[],
        )
        proposal = make_record(
            "ProposedSubgraph",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:proposer",
            role="proposer",
            id="proposal:1",
            proposal_key="proposal-key",
            revision=1,
            revises_proposal_id=None,
            base_acceptance_head=ledger.replay().acceptance_head,
            epistemic_policy_id="artifact:policy",
            epistemic_policy_hash="sha256:" + "8" * 64,
            member_content_hashes=[claim["content_hash"]],
            claim_version_ids=[claim["id"]],
            evidence_ids=[],
            evidence_assertion_ids=[],
            action_proposal_ids=[],
        )
        del proposal["evidence_ids"]
        proposal["content_hash"] = record_hash("ProposedSubgraph", proposal)
        with pytest.raises(ProtocolError, match="missing required fields: evidence_ids"):
            ledger.append_event(
                event_id=event_id,
                event_type=EventType.PROPOSAL_RECORDED,
                transaction_time=timestamp,
                actor_id="actor:proposer",
                payload={
                    "proposal": proposal,
                    "members": [{"record_type": "ClaimVersion", "record": claim}],
                },
            )

    def test_assessment_inputs_must_resolve_and_include_proposal(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="must include proposal|unknown assessment input"):
            record_type_assessment(
                ledger,
                proposal,
                artifacts["monitor"],
                input_record_ids=["record:phantom"],
            )
        assert ledger.path.read_bytes() == before


class TestMonitorFailureAndAuthorization:
    def test_authorization_policy_kind_requires_typed_artifact(self, ledger):
        anchor(ledger)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="requires AuthorizationPolicyArtifact"):
            add_artifact(
                ledger,
                "artifact:opaque-authorization-policy",
                "AUTHORIZATION_POLICY",
                1,
            )
        assert ledger.path.read_bytes() == before

    def test_authority_grant_cannot_name_another_grantor(self, ledger):
        anchor(ledger)
        with pytest.raises(ProtocolError, match="grantor must be the generating actor"):
            add_artifact(
                ledger,
                "artifact:forged-grant",
                "AUTHORITY_GRANT",
                1,
                record_type="AuthorityGrant",
                grantor_actor_id="actor:someone-else",
                grantee_actor_id="actor:system",
                permitted_action_types=["TEST"],
                grant_valid_from=time_at(1),
                grant_valid_to=time_at(2),
            )

    def test_monitor_failure_is_separate_and_forces_unknown(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        event_id = "event:monitor-failed"
        timestamp = time_at(7)
        failure, unknown = monitor_failure_records(
            error=MonitoringError("The monitor exceeded its deadline."),
            failure_id="failure:1",
            assessment_id="assessment:unknown",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:monitor",
            role="type-monitor",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            monitor_id=artifacts["monitor"]["id"],
            monitor_version="1",
            monitor_hash=artifacts["monitor"]["content_hash"],
            assessment_kind="TYPE",
            failure_category="TIMEOUT",
            error_code="DEADLINE",
        )
        ledger.append_event(
            event_id=event_id,
            event_type=EventType.MONITOR_FAILED,
            transaction_time=timestamp,
            actor_id="actor:monitor",
            payload={
                "failure": failure,
                "assessment_type": "UnavailableAssessment",
                "assessment": unknown,
            },
        )
        projection = ledger.replay()
        assert failure["id"] in projection.monitor_failure_ids
        assert unknown["id"] in projection.assessment_ids
        with pytest.raises(ProtocolError, match="verdict differs from deterministic policy"):
            decide_epistemically(ledger, proposal, unknown, artifacts, verdict="ACCEPT")
        decision = decide_epistemically(ledger, proposal, unknown, artifacts)
        assert decision["epistemic_verdict"] == "DEFER"
        assert decision["triggered_assessment_ids"] == [unknown["id"]]
        assert ledger.replay().proposal_states[proposal["id"]] == ProposalState.DEFERRED

    def test_generic_unknown_cannot_impersonate_authority_output(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        event_id = "event:authority-monitor-failed"
        timestamp = time_at(7)
        failure, unknown = monitor_failure_records(
            error=MonitoringError("The monitor exceeded its deadline."),
            failure_id="failure:authority",
            assessment_id="assessment:authority:unknown",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:monitor",
            role="authority-monitor",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            monitor_id=artifacts["monitor"]["id"],
            monitor_version="1",
            monitor_hash=artifacts["monitor"]["content_hash"],
            assessment_kind="TYPE",
            failure_category="TIMEOUT",
            error_code="DEADLINE",
        )
        authority_monitor = artifacts["authority_monitor"]
        for record in (failure, unknown):
            record["assessment_kind" if record is unknown else "failed_assessment_kind"] = (
                "AUTHORITY"
            )
            record["monitor_id"] = authority_monitor["id"]
            record["monitor_hash"] = authority_monitor["content_hash"]
            record["source_record_ids"] = [proposal["id"], authority_monitor["id"]]
        unknown["source_record_ids"].append(failure["id"])
        failure["content_hash"] = record_hash("MonitorFailure", failure)
        unknown["content_hash"] = record_hash("UnavailableAssessment", unknown)

        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="requires UnavailableAuthorityAssessment"):
            ledger.append_event(
                event_id=event_id,
                event_type=EventType.MONITOR_FAILED,
                transaction_time=timestamp,
                actor_id="actor:monitor",
                payload={
                    "failure": failure,
                    "assessment_type": "UnavailableAssessment",
                    "assessment": unknown,
                },
            )
        assert ledger.path.read_bytes() == before

    def test_epistemic_monitor_failure_cannot_carry_authority_context(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        event_id = "event:type-monitor-with-authority-context"
        failure, unknown = monitor_failure_records(
            error=MonitoringError("monitor failed"),
            failure_id="failure:type-with-authority",
            assessment_id="assessment:type-with-authority",
            event_id=event_id,
            generated_at=time_at(7),
            actor_id="actor:monitor",
            role="type-monitor",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            monitor_id=artifacts["monitor"]["id"],
            monitor_version="1",
            monitor_hash=artifacts["monitor"]["content_hash"],
            assessment_kind="TYPE",
            failure_category="EXECUTION",
            error_code="FAILED",
        )
        failure["action_proposal_id"] = "action:smuggled"
        failure["content_hash"] = record_hash("MonitorFailure", failure)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="non-authority failure contains authority fields"):
            ledger.append_event(
                event_id=event_id,
                event_type=EventType.MONITOR_FAILED,
                transaction_time=time_at(7),
                actor_id="actor:monitor",
                payload={
                    "failure": failure,
                    "assessment_type": "UnavailableAssessment",
                    "assessment": unknown,
                },
            )
        assert ledger.path.read_bytes() == before

    def test_monitor_failure_and_unavailable_assessment_cannot_share_id(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        event_id = "event:monitor-id-collision"
        timestamp = time_at(7)
        failure, unknown = monitor_failure_records(
            error=MonitoringError("The monitor failed."),
            failure_id="record:collision",
            assessment_id="assessment:temporary",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:monitor",
            role="type-monitor",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            monitor_id=artifacts["monitor"]["id"],
            monitor_version="1",
            monitor_hash=artifacts["monitor"]["content_hash"],
            assessment_kind="TYPE",
            failure_category="EXECUTION",
            error_code="FAILED",
        )
        unknown["id"] = failure["id"]
        unknown["content_hash"] = record_hash("UnavailableAssessment", unknown)

        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="IDs must differ"):
            ledger.append_event(
                event_id=event_id,
                event_type=EventType.MONITOR_FAILED,
                transaction_time=timestamp,
                actor_id="actor:monitor",
                payload={
                    "failure": failure,
                    "assessment_type": "UnavailableAssessment",
                    "assessment": unknown,
                },
            )
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize("reuse_same_context", [True, False])
    def test_standalone_unknown_cannot_reuse_monitor_failure(self, ledger, reuse_same_context):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        event_id = "event:monitor-failed"
        timestamp = time_at(7)
        failure, unknown = monitor_failure_records(
            error=MonitoringError("The monitor exceeded its deadline."),
            failure_id="failure:reused",
            assessment_id="assessment:original-unknown",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:monitor",
            role="type-monitor",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            monitor_id=artifacts["monitor"]["id"],
            monitor_version="1",
            monitor_hash=artifacts["monitor"]["content_hash"],
            assessment_kind="TYPE",
            failure_category="TIMEOUT",
            error_code="DEADLINE",
        )
        ledger.append_event(
            event_id=event_id,
            event_type=EventType.MONITOR_FAILED,
            transaction_time=timestamp,
            actor_id="actor:monitor",
            payload={
                "failure": failure,
                "assessment_type": "UnavailableAssessment",
                "assessment": unknown,
            },
        )

        reuse_event_id = f"event:reuse-failure:{reuse_same_context}"
        context = {
            "proposal_id": proposal["id"] if reuse_same_context else "proposal:other",
            "proposal_content_hash": (
                proposal["content_hash"] if reuse_same_context else "sha256:" + "9" * 64
            ),
            "base_acceptance_head": (
                proposal["base_acceptance_head"]
                if reuse_same_context
                else "sha256:" + "8" * 64
            ),
            "monitor_id": (
                artifacts["monitor"]["id"] if reuse_same_context else "artifact:monitor:other"
            ),
            "monitor_version": "1",
            "monitor_hash": (
                artifacts["monitor"]["content_hash"]
                if reuse_same_context
                else "sha256:" + "7" * 64
            ),
        }
        reused = make_record(
            "UnavailableAssessment",
            event_id=reuse_event_id,
            generated_at=time_at(8),
            actor_id="actor:other",
            role="type-monitor",
            source_record_ids=[failure["id"]],
            id=f"assessment:reused:{reuse_same_context}",
            assessment_kind="TYPE",
            assessment_outcome="UNKNOWN",
            monitor_failure_id=failure["id"],
            input_record_ids=[context["proposal_id"]],
            # A valid MonitorErrorCode on purpose: the record must be
            # structurally sound so that the protocol invariant below is what
            # rejects it, not the schema catching a placeholder first.
            reason_codes=["FAILED"],
            rationale="Attempted reuse of an earlier monitor failure.",
            **context,
        )
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="atomic MONITOR_FAILED"):
            ledger.append_event(
                event_id=reuse_event_id,
                event_type=EventType.ASSESSMENT_RECORDED,
                transaction_time=time_at(8),
                actor_id="actor:other",
                payload={"assessment_type": "UnavailableAssessment", "assessment": reused},
            )
        assert ledger.path.read_bytes() == before

    def test_authorization_requires_action_bound_actor_and_satisfied_authority(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, claim, action = record_proposal(ledger, include_action=True)
        type_assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        epistemic = decide_epistemically(ledger, proposal, type_assessment, artifacts)
        base = ledger.replay().acceptance_head
        authority = record_authority_assessment(ledger, proposal, action, artifacts)
        evaluation = evaluate_authorization_policy(
            artifacts["authorization_policy"],
            {artifacts["authority_monitor"]["id"]: artifacts["authority_monitor"]},
            [authority],
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            action_id=action["id"],
            action_content_hash=action["content_hash"],
            evaluated_actor_id="actor:executor",
            base_acceptance_head=base,
        )
        event_id = "event:authorization:1"
        timestamp = time_at(10)
        decision = make_record(
            "AuthorizationDecision",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:authorizer",
            role="authorizer",
            source_record_ids=[
                action["id"],
                claim["id"],
                epistemic["id"],
                authority["id"],
                artifacts["authorization_policy"]["id"],
                artifacts["grant"]["id"],
            ],
            id="decision:authorization:1",
            base_acceptance_head=base,
            policy_id=artifacts["authorization_policy"]["id"],
            policy_hash=artifacts["authorization_policy"]["content_hash"],
            rationale_codes=["AUTHORIZED_BY_GRANT"],
            rationale="The exact action and actor are in scope.",
            action_proposal_id=action["id"],
            action_content_hash=action["content_hash"],
            authorization_verdict="AUTHORIZE",
            epistemic_decision_ids=[epistemic["id"]],
            relied_on_claim_version_ids=[claim["id"]],
            authority_assessment_ids=[authority["id"]],
            triggered_assessment_ids=list(evaluation.triggered_assessment_ids),
            policy_evaluation_hash=evaluation.evaluation_hash,
            authority_grant_id=artifacts["grant"]["id"],
            authority_grant_hash=artifacts["grant"]["content_hash"],
            authorized_actor_id="actor:executor",
            authorization_valid_from=timestamp,
            authorization_valid_to=time_at(11),
        )
        sequence = ledger.replay().event_count + 1
        ledger.append_event(
            event_id=event_id,
            event_type=EventType.AUTHORIZATION_DECIDED,
            transaction_time=timestamp,
            actor_id="actor:authorizer",
            payload={
                "decision": decision,
                "transition": transition(
                    event_id=event_id,
                    timestamp=timestamp,
                    actor_id="actor:authorizer",
                    transition_id="transition:action:1",
                    subject=action["id"],
                    from_state="PENDING",
                    to_state="AUTHORIZED",
                    trigger=decision["id"],
                    sequence=sequence,
                ),
            },
        )
        assert ledger.replay().authorization_states[action["id"]] == AuthorizationState.AUTHORIZED

    def test_satisfied_authority_assessment_cannot_contain_violations(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        decide_epistemically(ledger, proposal, assessment, artifacts)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="SATISFIED authority assessment has violations"):
            record_authority_assessment(
                ledger,
                proposal,
                action,
                artifacts,
                checked=["actor_in_scope"],
                violated=["actor_in_scope"],
            )
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize("field", ["checked_policy_predicates", "violated_policy_predicates"])
    def test_authority_predicate_lists_are_present_or_fail_with_protocol_error(self, ledger, field):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        decide_epistemically(ledger, proposal, assessment, artifacts)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match=f"missing required fields|Required slot '{field}'"):
            record_authority_assessment(
                ledger,
                proposal,
                action,
                artifacts,
                mutate=lambda value: value.pop(field),
            )
        assert ledger.path.read_bytes() == before

    def test_violated_authority_output_deterministically_blocks_and_may_cite_grant(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, claim, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        epistemic = decide_epistemically(ledger, proposal, assessment, artifacts)
        authority = record_authority_assessment(
            ledger,
            proposal,
            action,
            artifacts,
            outcome="VIOLATED",
            violated=["actor_in_scope"],
        )
        decision = decide_authorization(
            ledger,
            proposal,
            action,
            claim,
            epistemic,
            [authority],
            artifacts,
            cite_grant=True,
        )
        assert decision["authorization_verdict"] == "BLOCK"
        assert decision["authority_grant_id"] == artifacts["grant"]["id"]
        assert decision["authorization_valid_from"] is None
        assert ledger.replay().authorization_states[action["id"]] == AuthorizationState.BLOCKED

    def test_missing_grant_can_be_assessed_as_violated_and_blocked(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger, include_grant=False)
        proposal, claim, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        epistemic = decide_epistemically(ledger, proposal, assessment, artifacts)
        authority = record_authority_assessment(
            ledger,
            proposal,
            action,
            artifacts,
            outcome="VIOLATED",
            checked=["grant_present"],
            violated=["grant_present"],
            include_grant=False,
        )
        decision = decide_authorization(
            ledger,
            proposal,
            action,
            claim,
            epistemic,
            [authority],
            artifacts,
        )
        assert decision["authorization_verdict"] == "BLOCK"
        assert decision["authority_grant_id"] is None

    @pytest.mark.parametrize("failure_first", [False, True])
    def test_completed_and_unavailable_authority_outputs_are_mutually_exclusive(
        self,
        ledger,
        failure_first,
    ):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        decide_epistemically(ledger, proposal, assessment, artifacts)
        if failure_first:
            record_authority_failure(
                ledger,
                proposal,
                action,
                artifacts,
                evaluated_grant=artifacts["grant"],
            )
        else:
            record_authority_assessment(ledger, proposal, action, artifacts)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="monitor already produced assessment"):
            if failure_first:
                record_authority_assessment(ledger, proposal, action, artifacts)
            else:
                record_authority_failure(
                    ledger,
                    proposal,
                    action,
                    artifacts,
                    evaluated_grant=artifacts["grant"],
                )
        assert ledger.path.read_bytes() == before

    def test_authority_output_can_refresh_after_acceptance_head_advances(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        decide_epistemically(ledger, proposal, assessment, artifacts)
        first = record_authority_assessment(
            ledger,
            proposal,
            action,
            artifacts,
            assessment_id="assessment:authority:head-1",
        )

        other, _, _ = record_proposal(
            ledger,
            minute=10,
            proposal_id="proposal:other",
            claim_id="claim:other",
            claim_key="claim-key-other",
        )
        other_assessment = record_type_assessment(
            ledger,
            other,
            artifacts["monitor"],
            minute=11,
            assessment_id="assessment:other",
        )
        decide_epistemically(
            ledger,
            other,
            other_assessment,
            artifacts,
            minute=12,
            decision_id="decision:epistemic:other",
            event_id="event:epistemic:other",
            transition_id="transition:proposal:other",
        )
        second = record_authority_assessment(
            ledger,
            proposal,
            action,
            artifacts,
            minute=13,
            assessment_id="assessment:authority:head-2",
        )
        assert first["base_acceptance_head"] != second["base_acceptance_head"]
        assert {
            first["id"],
            second["id"],
        }.issubset(ledger.replay().assessment_ids)

    def test_authority_outputs_are_distinct_for_evaluated_actors(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        decide_epistemically(ledger, proposal, assessment, artifacts)
        first = record_authority_assessment(
            ledger,
            proposal,
            action,
            artifacts,
            evaluated_actor_id="actor:executor",
            assessment_id="assessment:authority:executor",
        )
        second = record_authority_assessment(
            ledger,
            proposal,
            action,
            artifacts,
            outcome="VIOLATED",
            evaluated_actor_id="actor:other",
            violated=["actor_in_scope"],
            minute=10,
            assessment_id="assessment:authority:other",
        )
        assert first["evaluated_actor_id"] != second["evaluated_actor_id"]
        assert {first["id"], second["id"]}.issubset(ledger.replay().assessment_ids)

    def test_authority_output_can_reevaluate_a_new_exact_grant(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        decide_epistemically(ledger, proposal, assessment, artifacts)
        first = record_authority_assessment(
            ledger,
            proposal,
            action,
            artifacts,
            assessment_id="assessment:authority:grant-1",
        )
        second_grant = add_artifact(
            ledger,
            "artifact:grant:second",
            "AUTHORITY_GRANT",
            10,
            record_type="AuthorityGrant",
            grantor_actor_id="actor:system",
            grantee_actor_id="actor:executor",
            permitted_action_types=["TEST"],
            grant_valid_from=time_at(5),
            grant_valid_to=time_at(20),
        )
        second = record_authority_assessment(
            ledger,
            proposal,
            action,
            artifacts,
            grant=second_grant,
            minute=11,
            assessment_id="assessment:authority:grant-2",
        )
        assert first["base_acceptance_head"] == second["base_acceptance_head"]
        assert first["evaluated_authority_grant_id"] != second["evaluated_authority_grant_id"]
        assert {first["id"], second["id"]}.issubset(ledger.replay().assessment_ids)

    def test_unavailable_authority_output_deterministically_requires_clarification(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, claim, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        epistemic = decide_epistemically(ledger, proposal, assessment, artifacts)
        unknown = record_authority_failure(ledger, proposal, action, artifacts)
        decision = decide_authorization(
            ledger,
            proposal,
            action,
            claim,
            epistemic,
            [unknown],
            artifacts,
        )
        assert decision["authorization_verdict"] == "CLARIFY"
        assert decision["authority_grant_id"] is None
        assert ledger.replay().authorization_states[action["id"]] == (
            AuthorizationState.CLARIFICATION_REQUIRED
        )

    def test_block_cannot_cite_grant_from_unknown_output(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        second_monitor = add_monitor(
            ledger,
            "artifact:authority-monitor:second",
            "AUTHORITY",
            6,
        )
        multi_policy = add_authorization_policy(
            ledger,
            [artifacts["authority_monitor"], second_monitor],
            6,
            policy_id="artifact:authorization-policy:multi",
        )
        second_grant = add_artifact(
            ledger,
            "artifact:grant:unknown-path",
            "AUTHORITY_GRANT",
            6,
            record_type="AuthorityGrant",
            grantor_actor_id="actor:system",
            grantee_actor_id="actor:executor",
            permitted_action_types=["TEST"],
            grant_valid_from=time_at(5),
            grant_valid_to=time_at(20),
        )
        proposal, claim, action = record_proposal(
            ledger,
            authorization_policy=multi_policy,
            include_action=True,
            minute=7,
        )
        type_assessment = record_type_assessment(
            ledger,
            proposal,
            artifacts["monitor"],
            minute=8,
        )
        epistemic = decide_epistemically(
            ledger,
            proposal,
            type_assessment,
            artifacts,
            minute=9,
        )
        multi_artifacts = {
            **artifacts,
            "authorization_policy": multi_policy,
        }
        violated = record_authority_assessment(
            ledger,
            proposal,
            action,
            multi_artifacts,
            outcome="VIOLATED",
            violated=["actor_in_scope"],
            minute=10,
            assessment_id="assessment:authority:violated",
        )
        unknown = record_authority_failure(
            ledger,
            proposal,
            action,
            {
                **multi_artifacts,
                "authority_monitor": second_monitor,
            },
            evaluated_grant=second_grant,
            minute=11,
            assessment_id="assessment:authority:unknown-second",
        )
        before = ledger.path.read_bytes()

        def cite_unknown_grant(value):
            value["authority_grant_id"] = second_grant["id"]
            value["authority_grant_hash"] = second_grant["content_hash"]
            value["source_record_ids"].append(second_grant["id"])

        with pytest.raises(
            ProtocolError,
            match="triggering VIOLATED authority assessment",
        ):
            decide_authorization(
                ledger,
                proposal,
                action,
                claim,
                epistemic,
                [violated, unknown],
                multi_artifacts,
                minute=12,
                mutate=cite_unknown_grant,
            )
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize(
        "mutate,message",
        [
            (
                lambda value: value.update({"authorization_verdict": "BLOCK"}),
                "verdict differs from deterministic authorization policy",
            ),
            (
                lambda value: value.update({"policy_evaluation_hash": "sha256:" + "9" * 64}),
                "authorization policy evaluation hash mismatch",
            ),
            (
                lambda value: value["triggered_assessment_ids"].append(
                    "assessment:authority:1"
                ),
                "triggered authority assessments differ from policy",
            ),
        ],
    )
    def test_authorization_control_record_cannot_override_replay(self, ledger, mutate, message):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, claim, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        epistemic = decide_epistemically(ledger, proposal, assessment, artifacts)
        authority = record_authority_assessment(ledger, proposal, action, artifacts)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match=message):
            decide_authorization(
                ledger,
                proposal,
                action,
                claim,
                epistemic,
                [authority],
                artifacts,
                mutate=mutate,
            )
        assert ledger.path.read_bytes() == before

    def test_late_valid_authorization_policy_cannot_replace_action_binding(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, claim, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        epistemic = decide_epistemically(ledger, proposal, assessment, artifacts)
        replacement = add_authorization_policy(
            ledger,
            [artifacts["authority_monitor"]],
            9,
            policy_id="artifact:authorization-policy:replacement",
        )
        authority = record_authority_assessment(
            ledger,
            proposal,
            action,
            artifacts,
            minute=10,
        )
        before = ledger.path.read_bytes()

        def replace_policy(value):
            value["policy_id"] = replacement["id"]
            value["policy_hash"] = replacement["content_hash"]
            value["source_record_ids"].append(replacement["id"])

        with pytest.raises(ProtocolError, match="decision policy differs from action"):
            decide_authorization(
                ledger,
                proposal,
                action,
                claim,
                epistemic,
                [authority],
                artifacts,
                minute=11,
                mutate=replace_policy,
            )
        assert ledger.path.read_bytes() == before

    def test_authority_failure_context_mismatch_is_atomic(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        decide_epistemically(ledger, proposal, assessment, artifacts)
        before = ledger.path.read_bytes()

        def drift_action_hash(_failure, unknown):
            unknown["action_content_hash"] = "sha256:" + "9" * 64

        with pytest.raises(ProtocolError, match="failure and assessment action_content_hash differ"):
            record_authority_failure(
                ledger,
                proposal,
                action,
                artifacts,
                mutate=drift_action_hash,
            )
        assert ledger.path.read_bytes() == before

    def test_violated_authority_predicate_must_have_been_checked(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        decide_epistemically(ledger, proposal, assessment, artifacts)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="violated authority predicates were not checked"):
            record_authority_assessment(
                ledger,
                proposal,
                action,
                artifacts,
                outcome="VIOLATED",
                checked=["actor_in_scope"],
                violated=["action_in_scope"],
            )
        assert ledger.path.read_bytes() == before

    def test_authorize_cannot_substitute_a_different_sufficient_grant(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, claim, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        epistemic = decide_epistemically(ledger, proposal, assessment, artifacts)
        authority = record_authority_assessment(ledger, proposal, action, artifacts)
        replacement_grant = add_artifact(
            ledger,
            "artifact:grant:replacement",
            "AUTHORITY_GRANT",
            10,
            record_type="AuthorityGrant",
            grantor_actor_id="actor:system",
            grantee_actor_id="actor:executor",
            permitted_action_types=["TEST"],
            grant_valid_from=time_at(5),
            grant_valid_to=time_at(20),
        )
        before = ledger.path.read_bytes()

        def replace_grant(value):
            value["authority_grant_id"] = replacement_grant["id"]
            value["authority_grant_hash"] = replacement_grant["content_hash"]
            value["source_record_ids"].append(replacement_grant["id"])

        with pytest.raises(ProtocolError, match="AUTHORIZE grant differs from assessed grant"):
            decide_authorization(
                ledger,
                proposal,
                action,
                claim,
                epistemic,
                [authority],
                artifacts,
                minute=11,
                mutate=replace_grant,
            )
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize(
        "mutation,message",
        [
            (
                lambda value: value.update({
                    "authority_grant_id": None,
                    "authority_grant_hash": None,
                }),
                "AUTHORIZE requires grant and validity start",
            ),
            (
                lambda value: value.update({"authorization_valid_from": time_at(4)}),
                "authorization begins before its grant",
            ),
            (
                lambda value: value.update({"authorization_valid_to": time_at(21)}),
                "authorization exceeds its grant",
            ),
        ],
    )
    def test_authorize_grant_preconditions_fail_atomically(self, ledger, mutation, message):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, claim, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        epistemic = decide_epistemically(ledger, proposal, assessment, artifacts)
        authority = record_authority_assessment(ledger, proposal, action, artifacts)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match=message):
            decide_authorization(
                ledger,
                proposal,
                action,
                claim,
                epistemic,
                [authority],
                artifacts,
                mutate=mutation,
            )
        assert ledger.path.read_bytes() == before

    def test_non_authorizing_decision_cannot_smuggle_validity(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, claim, action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        epistemic = decide_epistemically(ledger, proposal, assessment, artifacts)
        authority = record_authority_assessment(
            ledger,
            proposal,
            action,
            artifacts,
            outcome="VIOLATED",
            violated=["actor_in_scope"],
        )
        before = ledger.path.read_bytes()

        def add_validity(value):
            value["authorization_valid_from"] = time_at(10)
            value["authorization_valid_to"] = time_at(11)

        with pytest.raises(ProtocolError, match="non-AUTHORIZE decision cannot grant validity"):
            decide_authorization(
                ledger,
                proposal,
                action,
                claim,
                epistemic,
                [authority],
                artifacts,
                mutate=add_validity,
            )
        assert ledger.path.read_bytes() == before

    def test_action_revision_cannot_fork_from_nonlatest_revision(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        first_proposal, _, first_action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(
            ledger,
            first_proposal,
            artifacts["monitor"],
            outcome="VIOLATED",
        )
        decide_epistemically(ledger, first_proposal, assessment, artifacts)
        record_proposal(
            ledger,
            include_action=True,
            minute=9,
            proposal_id="proposal:2",
            proposal_revision=2,
            revises_proposal_id=first_proposal["id"],
            claim_id="claim:2",
            action_id="action:2",
            action_revision=2,
            revises_action_id=first_action["id"],
        )
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="action revision must extend latest revision"):
            record_proposal(
                ledger,
                include_action=True,
                minute=10,
                proposal_id="proposal:3",
                proposal_revision=2,
                revises_proposal_id=first_proposal["id"],
                claim_id="claim:3",
                action_id="action:3",
                action_revision=2,
                revises_action_id=first_action["id"],
            )
        assert ledger.path.read_bytes() == before

    def test_unknown_schema_registry_fails_at_construction(self, tmp_path):
        registry = OntologyRegistry(Path(__file__).parent.parent / "ontology" / "malleus.yaml")
        with pytest.raises(ProtocolError, match="missing required classes"):
            ProtocolLedger(tmp_path / "bad.jsonl", registry)

    def test_registry_category_contract_fails_at_construction(self, tmp_path, registry):
        wrong = deepcopy(registry)
        wrong._types["MonitorFailure"] = replace(
            wrong._types["MonitorFailure"],
            parent="Assessment",
        )
        wrong._inheritance["MonitorFailure"] = "Assessment"
        with pytest.raises(ProtocolError, match="must not be an Assessment"):
            ProtocolLedger(tmp_path / "wrong.jsonl", wrong)

    @pytest.mark.parametrize(
        "type_name,parent,expected",
        [
            ("Decision", "Entity", "Decision.*inherit.*ProtocolRecord"),
            ("AuthorityAssessment", "ProtocolRecord", "AuthorityAssessment.*inherit.*Assessment"),
        ],
    )
    def test_registry_preflight_rejects_broken_protocol_hierarchy(
        self,
        tmp_path,
        registry,
        type_name,
        parent,
        expected,
    ):
        wrong = deepcopy(registry)
        wrong._types[type_name] = replace(wrong._types[type_name], parent=parent)
        wrong._inheritance[type_name] = parent
        with pytest.raises(ProtocolError, match=expected):
            ProtocolLedger(tmp_path / f"wrong-{type_name}.jsonl", wrong)


class TestLogicCheckProtocol:
    @pytest.mark.parametrize(
        "case, message",
        [
            ("record_hash", "Artifact hash mismatch"),
            ("artifact_hash", "ruleset artifact hash mismatch"),
            ("semantic_hash", "semantic hash mismatch"),
            ("sources", "sources must include ruleset"),
        ],
    )
    def test_logic_contract_artifact_separates_record_raw_and_semantic_hashes(
        self,
        ledger,
        case,
        message,
    ):
        anchor(ledger)
        rules = add_artifact(ledger, "artifact:rules", "RULE_SET", 1)
        fields = {
            "logic_contract_schema_version": "1",
            "ontology_hash": "sha256:" + "6" * 64,
            "fact_contract_version": "2",
            "ruleset_id": rules["id"],
            "ruleset_version": "1",
            "ruleset_record_hash": rules["content_hash"],
            "ruleset_artifact_hash": rules["artifact_hash"],
            "rule_ids": ["RULE_ONE"],
            "timeout_seconds": 5,
            "source_record_ids": [rules["id"]],
        }
        if case == "record_hash":
            fields["ruleset_record_hash"] = "sha256:" + "0" * 64
        elif case == "artifact_hash":
            fields["ruleset_artifact_hash"] = "sha256:" + "0" * 64
        elif case == "sources":
            fields["source_record_ids"] = []
        semantic_hash = logic_contract_digest(
            schema_version=fields["logic_contract_schema_version"],
            contract_id="artifact:logic-contract",
            contract_version="1",
            ontology_hash=fields["ontology_hash"],
            fact_contract_version=fields["fact_contract_version"],
            ruleset_id=fields["ruleset_id"],
            ruleset_version=fields["ruleset_version"],
            rule_ids=fields["rule_ids"],
            timeout_seconds=fields["timeout_seconds"],
            ruleset_hash=fields["ruleset_artifact_hash"],
        )
        if case == "semantic_hash":
            semantic_hash = "sha256:" + "0" * 64
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match=message):
            add_artifact(
                ledger,
                "artifact:logic-contract",
                "LOGIC_CONTRACT",
                2,
                record_type="LogicContractArtifact",
                artifact_hash=semantic_hash,
                **fields,
            )
        assert ledger.path.read_bytes() == before

    def test_logic_check_rejects_stale_accepted_context(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        stale, _, _ = record_proposal(
            ledger,
            proposal_id="proposal:stale",
            claim_id="claim:stale",
        )
        fresh, _, _ = record_proposal(
            ledger,
            proposal_id="proposal:fresh",
            claim_id="claim:fresh",
            minute=7,
        )
        assessment = record_type_assessment(
            ledger,
            fresh,
            artifacts["monitor"],
            minute=8,
        )
        decide_epistemically(ledger, fresh, assessment, artifacts, minute=9)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="stale acceptance head"):
            record_logic_check(ledger, stale, artifacts, minute=10)
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize("violated", [False, True])
    def test_completed_logic_check_and_assessment_replay(self, ledger, violated):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        check, witnesses = record_logic_check(
            ledger,
            proposal,
            artifacts,
            violated=violated,
        )
        assessment = record_logical_assessment(ledger, proposal, check, artifacts)

        projection = ledger.replay()
        assert check["id"] in projection.logic_check_ids
        assert set(check["violation_witness_ids"]) == projection.violation_witness_ids
        assert assessment["id"] in projection.assessment_ids
        assert check["check_outcome"] == ("VIOLATED" if violated else "SATISFIED")
        assert len(witnesses) == (1 if violated else 0)

    def test_exact_logical_monitor_can_record_only_one_check_per_proposal(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        first, _ = record_logic_check(ledger, proposal, artifacts)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="logical monitor already produced check"):
            record_logic_check(
                ledger,
                proposal,
                artifacts,
                violated=True,
                minute=8,
                check_id="logic-check:2",
                event_id="event:logic-check:2",
            )
        assert ledger.path.read_bytes() == before
        assert ledger.replay().logic_check_by_monitor_context[
            (proposal["id"], artifacts["logic_monitor"]["id"])
        ] == first["id"]

    @pytest.mark.parametrize("failure_first", [False, True])
    def test_completed_and_unavailable_logic_paths_are_mutually_exclusive(
        self,
        ledger,
        failure_first,
    ):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        failure_event_id = "event:exclusive-logic-failure"
        failure, unavailable = logic_monitor_failure_records(
            error=LogicExecutionError("The pinned logic engine did not complete."),
            failure_id="failure:logic:exclusive",
            assessment_id="assessment:logic:unavailable",
            event_id=failure_event_id,
            generated_at=time_at(7),
            actor_id="actor:monitor",
            role="logic-monitor",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            monitor_id=artifacts["logic_monitor"]["id"],
            monitor_version="1",
            monitor_hash=artifacts["logic_monitor"]["content_hash"],
            logic_contract_id=artifacts["logic_contract"]["id"],
            logic_contract_record_hash=artifacts["logic_contract"]["content_hash"],
            ruleset_id=artifacts["rules"]["id"],
            ruleset_record_hash=artifacts["rules"]["content_hash"],
            failure_category="EXECUTION",
            error_code="ENGINE_FAILED",
        )

        def record_failure():
            return ledger.append_event(
                event_id=failure_event_id,
                event_type=EventType.MONITOR_FAILED,
                transaction_time=time_at(7),
                actor_id="actor:monitor",
                payload={
                    "failure": failure,
                    "assessment_type": "UnavailableAssessment",
                    "assessment": unavailable,
                },
            )

        if failure_first:
            record_failure()
            before = ledger.path.read_bytes()
            with pytest.raises(ProtocolError, match="already produced unavailable output"):
                record_logic_check(
                    ledger,
                    proposal,
                    artifacts,
                    violated=True,
                    minute=8,
                    event_id="event:exclusive-logic-check",
                )
        else:
            record_logic_check(ledger, proposal, artifacts, violated=True)
            before = ledger.path.read_bytes()
            with pytest.raises(ProtocolError, match="completed logical check already exists"):
                record_failure()
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize(
        "case, message",
        [
            ("no_rules", "checked no rules"),
            ("unchecked_violation", "violated rules were not checked"),
            ("satisfied_with_violation", "SATISFIED logic check has violations"),
            ("wrong_rules_hash", "Artifact hash mismatch"),
            ("blank_rule", "nonblank strings"),
            ("fact_contract", "fact_contract_version"),
            ("ontology", "ontology hash differs from contract"),
            ("timeout", "timeout differs from contract"),
            ("sources", "source_record_ids missing required records"),
        ],
    )
    def test_logic_check_rejects_inconsistent_or_unpinned_results(
        self,
        ledger,
        case,
        message,
    ):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        before = ledger.path.read_bytes()

        def mutate(check, _witnesses):
            if case == "no_rules":
                check["checked_rule_ids"] = []
            elif case == "unchecked_violation":
                check["violated_rule_ids"] = ["RULE_OTHER"]
                check["check_outcome"] = "VIOLATED"
            elif case == "satisfied_with_violation":
                check["violated_rule_ids"] = ["RULE_ONE"]
            elif case == "wrong_rules_hash":
                check["ruleset_record_hash"] = "sha256:" + "0" * 64
            elif case == "blank_rule":
                check["checked_rule_ids"] = [""]
            elif case == "fact_contract":
                check["fact_contract_version"] = "99"
            elif case == "ontology":
                check["ontology_hash"] = "sha256:" + "0" * 64
            elif case == "sources":
                check["source_record_ids"] = []
            else:
                check["timeout_seconds"] = 6

        with pytest.raises(ProtocolError, match=message):
            record_logic_check(ledger, proposal, artifacts, mutate=mutate)
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize(
        "case, message",
        [
            ("unknown_record", "untranslated record"),
            ("binding_hash", "binding hash mismatch"),
            ("wrong_check", "logic_check_id mismatch"),
            ("sources", "source_record_ids missing required records"),
        ],
    )
    def test_violation_witness_is_bound_to_check_rule_and_translated_scope(
        self,
        ledger,
        case,
        message,
    ):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        before = ledger.path.read_bytes()

        def mutate(_check, witnesses):
            witness = witnesses[0]
            if case == "unknown_record":
                witness["witness_record_ids"] = ["graph:unknown"]
                witness["witness_binding_hash"] = content_digest({
                    "rule_id": witness["rule_id"],
                    "violation_code": witness["violation_code"],
                    "witness_record_ids": witness["witness_record_ids"],
                })
            elif case == "binding_hash":
                witness["witness_binding_hash"] = "sha256:" + "0" * 64
            elif case == "wrong_check":
                witness["logic_check_id"] = "logic-check:other"
            else:
                witness["source_record_ids"] = []

        with pytest.raises(ProtocolError, match=message):
            record_logic_check(
                ledger,
                proposal,
                artifacts,
                violated=True,
                mutate=mutate,
            )
        assert ledger.path.read_bytes() == before

    @pytest.mark.parametrize(
        "case, message",
        [
            ("rules", "checked rules differ"),
            ("sources", "source_record_ids missing required records"),
        ],
    )
    def test_logical_assessment_must_exactly_match_applied_check(
        self,
        ledger,
        case,
        message,
    ):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        check, _ = record_logic_check(ledger, proposal, artifacts)
        before = ledger.path.read_bytes()

        def mutate(assessment):
            if case == "rules":
                assessment["checked_rule_ids"] = ["RULE_OTHER"]
            else:
                assessment["source_record_ids"] = []

        with pytest.raises(ProtocolError, match=message):
            record_logical_assessment(
                ledger,
                proposal,
                check,
                artifacts,
                mutate=mutate,
            )
        assert ledger.path.read_bytes() == before

    def test_unknown_logical_assessment_has_failure_and_no_completed_check(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        event_id = "event:logic-monitor-failed"
        timestamp = time_at(7)
        failure, assessment = logic_monitor_failure_records(
            error=LogicExecutionError("The pinned logic engine did not complete."),
            failure_id="failure:logic:1",
            assessment_id="assessment:logical:unknown",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:monitor",
            role="logic-monitor",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            monitor_id=artifacts["logic_monitor"]["id"],
            monitor_version="1",
            monitor_hash=artifacts["logic_monitor"]["content_hash"],
            logic_contract_id=artifacts["logic_contract"]["id"],
            logic_contract_record_hash=artifacts["logic_contract"]["content_hash"],
            failure_category="EXECUTION",
            error_code="ENGINE_FAILED",
            ruleset_id=artifacts["rules"]["id"],
            ruleset_record_hash=artifacts["rules"]["content_hash"],
        )
        ledger.append_event(
            event_id=event_id,
            event_type=EventType.MONITOR_FAILED,
            transaction_time=timestamp,
            actor_id="actor:monitor",
            payload={
                "failure": failure,
                "assessment_type": "UnavailableAssessment",
                "assessment": assessment,
            },
        )
        projection = ledger.replay()
        assert assessment["id"] in projection.assessment_ids
        assert not projection.logic_check_ids

    @pytest.mark.parametrize(
        "case, message",
        [
            ("failure_sources", "source_record_ids missing required records"),
            ("assessment_sources", "source_record_ids missing required records"),
            ("contract_hash", "failure and assessment logic_contract_record_hash differ"),
        ],
    )
    def test_failed_logic_monitor_requires_exact_atomic_provenance(
        self,
        ledger,
        case,
        message,
    ):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        event_id = "event:logic-monitor-provenance-failed"
        timestamp = time_at(7)
        failure, assessment = logic_monitor_failure_records(
            error=LogicExecutionError("The pinned logic engine did not complete."),
            failure_id="failure:logic:provenance",
            assessment_id="assessment:logical:provenance",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:monitor",
            role="logic-monitor",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            monitor_id=artifacts["logic_monitor"]["id"],
            monitor_version="1",
            monitor_hash=artifacts["logic_monitor"]["content_hash"],
            logic_contract_id=artifacts["logic_contract"]["id"],
            logic_contract_record_hash=artifacts["logic_contract"]["content_hash"],
            failure_category="EXECUTION",
            error_code="ENGINE_FAILED",
            ruleset_id=artifacts["rules"]["id"],
            ruleset_record_hash=artifacts["rules"]["content_hash"],
        )
        if case == "failure_sources":
            failure["source_record_ids"] = []
            failure["content_hash"] = record_hash("MonitorFailure", failure)
        elif case == "assessment_sources":
            assessment["source_record_ids"] = []
            assessment["content_hash"] = record_hash("UnavailableAssessment", assessment)
        else:
            failure["logic_contract_record_hash"] = "sha256:" + "0" * 64
            failure["content_hash"] = record_hash("MonitorFailure", failure)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match=message):
            ledger.append_event(
                event_id=event_id,
                event_type=EventType.MONITOR_FAILED,
                transaction_time=timestamp,
                actor_id="actor:monitor",
                payload={
                    "failure": failure,
                    "assessment_type": "UnavailableAssessment",
                    "assessment": assessment,
                },
            )
        assert ledger.path.read_bytes() == before

    def test_old_proof_field_is_not_in_schema(self, registry):
        slots = registry.effective_slots("LogicalAssessment")
        assert "proof_record_ids" not in slots
        assert "logic_check_record_ids" in slots


class TestRequestAndRevisionArm:
    """The Request/Revision validation arm executed with content, not empty
    lists (self-inquisition S6)."""

    def test_accept_with_review_request_and_claim_revision(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal_one, claim_one, _ = record_proposal(ledger)
        assessment_one = record_type_assessment(ledger, proposal_one, artifacts["monitor"])
        decide_epistemically(ledger, proposal_one, assessment_one, artifacts)

        replacement_time = ValidTime.calendar_day(
            "2026-08-13",
            timezone="UTC",
            indeterminacy_reason="The source establishes the revision day only.",
        ).as_dict()
        proposal_two, claim_two, _ = record_proposal(
            ledger,
            minute=10,
            proposal_id="proposal:2",
            claim_id="claim:2",
            claim_revision=2,
            revises_claim_version_id=claim_one["id"],
            claim_valid_from=replacement_time,
        )
        assessment_two = record_type_assessment(
            ledger,
            proposal_two,
            artifacts["monitor"],
            minute=11,
            assessment_id="assessment:satisfied:2",
        )
        decision_id = "decision:epistemic:2"
        event_id = "event:epistemic:2"
        timestamp = time_at(12)
        revision = make_record(
            "ClaimRevision",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:reviewer",
            role="epistemic-controller",
            source_record_ids=[claim_one["id"]],
            id="revision:1",
            replaced_claim_version_id=claim_one["id"],
            replacement_claim_version_id=claim_two["id"],
            triggering_decision_id=decision_id,
            revision_justification="Replacing the accepted claim with its successor.",
            dependency_ids=[],
            replacement_valid_from=claim_two["domain_valid_from"],
            replaced_valid_to=claim_two["domain_valid_from"],
        )
        request = make_record(
            "HumanReviewRequest",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:reviewer",
            role="reviewer",
            source_record_ids=[proposal_two["id"]],
            id="request:review:1",
            triggering_decision_id=decision_id,
            target_proposal_id=proposal_two["id"],
            request_contract_id="contract:review:1",
            request_contract_hash="sha256:" + "7" * 64,
            requested_by_actor_id="actor:reviewer",
            intended_recipient_id=None,
            intended_role="reviewer",
            issued_at=timestamp,
            expires_at=None,
            request_state="OPEN",
            review_question="Does the successor claim reflect the reviewed evidence?",
            reviewer_authority_requirement="reviewer",
        )
        decide_epistemically(
            ledger,
            proposal_two,
            assessment_two,
            artifacts,
            minute=12,
            transition_id="transition:proposal:2",
            decision_id=decision_id,
            event_id=event_id,
            requests=[("HumanReviewRequest", request)],
            revisions=[revision],
        )
        projection = ledger.replay()
        assert projection.proposal_states[proposal_two["id"]] == ProposalState.ACCEPTED
        assert projection.current_claim_by_key[claim_one["claim_key"]] == claim_two["id"]
        assert claim_one["id"] in projection.superseded_claim_ids
        assert projection.objects["revision:1"]["record_type"] == "ClaimRevision"
        assert projection.objects["revision:1"]["record"]["replacement_valid_from"] == replacement_time
        assert projection.objects["request:review:1"]["record_type"] == "HumanReviewRequest"


class TestSurrogatesInTheLedgerAreDiagnosed:
    """Every encoding failure in the identity layer is a LedgerError, on the
    write path AND the read path (second self-inquisition H2)."""

    @pytest.mark.parametrize("value", ["\ud800", "\udc00", "\ud800\udc00"])
    def test_content_digest_raises_ledger_error(self, value):
        with pytest.raises(LedgerError):
            content_digest({"p": value})

    def test_append_raises_ledger_error(self, tmp_path):
        jsonl = JsonlLedger(tmp_path / "l.jsonl", "sha256:" + "1" * 64)
        with pytest.raises(LedgerError):
            jsonl.append(
                event_id="e1",
                event_type="X",
                transaction_time="2026-08-13T00:00:00+00:00",
                actor_id="a",
                payload={"p": "\ud800"},
                validate=lambda events: None,
            )
        assert not (tmp_path / "l.jsonl").exists()

    def test_read_of_surrogate_bearing_line_raises_ledger_error(self, tmp_path):
        path = tmp_path / "l.jsonl"
        path.write_text('{"payload": "\\ud800"}\n', encoding="utf-8")
        jsonl = JsonlLedger(path, "sha256:" + "1" * 64)
        with pytest.raises(LedgerError):
            jsonl.read()


class TestAssessmentKindContractIsPinned:
    """The one enum duplicated in Python twice is pinned by the ledger
    contract (second self-inquisition S1)."""

    def test_widened_assessment_kind_is_refused_by_the_ledger(self, tmp_path):
        source = Path(__file__).parent.parent / "ontology" / "assent.yaml"
        widened = tmp_path / "assent.yaml"
        widened.write_text(
            source.read_text().replace(
                "      AUTHORITY:\n", "      AUTHORITY:\n      EXTRA:\n", 1
            )
        )
        registry = OntologyRegistry(
            widened,
            import_map={"malleus": str((source.parent / "malleus.yaml").resolve())},
        )
        with pytest.raises(ProtocolError, match="AssessmentKind"):
            ProtocolLedger(tmp_path / "ledger.jsonl", registry)


class TestEvidenceMembersInProposals:
    """EvidenceAssertion members resolve their ClaimVersion and their Evidence
    (second self-inquisition S2, src/malleus/assent.py:811-813)."""

    def test_proposal_carries_evidence_and_assertions_with_content(self, ledger):
        anchor(ledger)
        setup_artifacts(ledger)
        source = add_source_artifact(ledger)
        proposal, claim, _ = record_proposal(
            ledger,
            evidence_count=2,
            source_artifact=source,
        )
        projection = ledger.replay()
        assert len(proposal["evidence_ids"]) == 2
        assert len(proposal["evidence_assertion_ids"]) == 2
        for evidence_id in proposal["evidence_ids"]:
            assert projection.objects[evidence_id]["record_type"] == "Evidence"
            assert projection.objects[evidence_id]["record"]["evidence_kind"]
        for assertion_id in proposal["evidence_assertion_ids"]:
            item = projection.objects[assertion_id]
            assert item["record_type"] == "EvidenceAssertion"
            assert item["record"]["claim_version_id"] == claim["id"]
            assert item["record"]["evidence_id"] in proposal["evidence_ids"]
            assert item["record"]["evidence_polarity"] == "SUPPORTS"

    def test_assertion_citing_unknown_evidence_is_refused(self, ledger):
        anchor(ledger)
        setup_artifacts(ledger)
        source = add_source_artifact(ledger)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="Unknown referenced object"):
            record_proposal(
                ledger,
                evidence_count=1,
                source_artifact=source,
                assertion_evidence_id="evidence:absent",
            )
        assert ledger.path.read_bytes() == before

    def test_assertion_whose_claim_reference_is_evidence_is_refused(self, ledger):
        anchor(ledger)
        setup_artifacts(ledger)
        source = add_source_artifact(ledger)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="expected ClaimVersion"):
            record_proposal(
                ledger,
                evidence_count=1,
                source_artifact=source,
                assertion_claim_id="proposal:1:evidence:1",
            )
        assert ledger.path.read_bytes() == before


class TestCoreAssessmentKindsAreRecorded:
    """The ConflictAssessment arm of _validate_completed_assessment runs with
    content, and every core AssessmentKind has one recorded instance
    (second self-inquisition S2, src/malleus/assent.py:2026-2045)."""

    def test_conflict_uncertainty_and_temporal_assessments_are_recorded(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(
            ledger,
            extra_kinds=("CONFLICT", "UNCERTAINTY", "TEMPORAL"),
        )
        source = add_source_artifact(ledger)
        proposal, _, _ = record_proposal(
            ledger,
            evidence_count=2,
            source_artifact=source,
        )
        conflicts = sorted(proposal["evidence_assertion_ids"])
        conflict = record_kind_assessment(
            ledger,
            proposal,
            artifacts,
            "CONFLICT",
            outcome="VIOLATED",
            conflicting_assertion_ids=conflicts,
            input_record_ids=[proposal["id"], *conflicts],
        )
        uncertainty = record_kind_assessment(
            ledger,
            proposal,
            artifacts,
            "UNCERTAINTY",
            minute=8,
        )
        temporal = record_kind_assessment(
            ledger,
            proposal,
            artifacts,
            "TEMPORAL",
            minute=9,
        )
        projection = ledger.replay()
        recorded = {
            identifier: projection.objects[identifier]["record_type"]
            for identifier in (conflict["id"], uncertainty["id"], temporal["id"])
        }
        assert recorded == {
            conflict["id"]: "ConflictAssessment",
            uncertainty["id"]: "UncertaintyAssessment",
            temporal["id"]: "TemporalAssessment",
        }
        assert projection.objects[conflict["id"]]["record"][
            "conflicting_assertion_ids"
        ] == conflicts
        assert conflict["id"] in projection.assessment_ids

    def test_satisfied_conflict_assessment_names_no_conflicts(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger, extra_kinds=("CONFLICT",))
        source = add_source_artifact(ledger)
        proposal, _, _ = record_proposal(
            ledger,
            evidence_count=2,
            source_artifact=source,
        )
        conflict = record_kind_assessment(
            ledger,
            proposal,
            artifacts,
            "CONFLICT",
            outcome="SATISFIED",
            conflicting_assertion_ids=[],
        )
        assert ledger.replay().objects[conflict["id"]]["record"][
            "conflicting_assertion_ids"
        ] == []

    @pytest.mark.parametrize(
        "case,message",
        [
            ("satisfied_with_conflicts", "SATISFIED conflict assessment names conflicts"),
            ("violated_with_one", "VIOLATED conflict assessment requires two assertions"),
            ("outside_proposal", "conflict assertion is outside proposal"),
            ("not_an_input", "conflict assertions must be assessment inputs"),
            ("unsorted", "conflicting_assertion_ids must be in canonical sorted order"),
        ],
    )
    def test_conflict_assessment_binds_its_assertions(self, ledger, case, message):
        anchor(ledger)
        artifacts = setup_artifacts(ledger, extra_kinds=("CONFLICT",))
        source = add_source_artifact(ledger)
        first, _, _ = record_proposal(
            ledger,
            evidence_count=2,
            source_artifact=source,
        )
        second, _, _ = record_proposal(
            ledger,
            minute=6,
            proposal_id="proposal:2",
            proposal_key="proposal-key:2",
            claim_id="claim:2",
            claim_key="claim-key:2",
            evidence_count=2,
            source_artifact=source,
        )
        own = sorted(second["evidence_assertion_ids"])
        outcome = "VIOLATED"
        conflicts = own
        inputs = [second["id"], *own]
        if case == "satisfied_with_conflicts":
            outcome = "SATISFIED"
        elif case == "violated_with_one":
            conflicts = own[:1]
            inputs = [second["id"], own[0]]
        elif case == "outside_proposal":
            conflicts = sorted([own[0], sorted(first["evidence_assertion_ids"])[0]])
            inputs = [second["id"], *conflicts]
        elif case == "not_an_input":
            inputs = [second["id"]]
        else:
            conflicts = list(reversed(own))
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match=message):
            record_kind_assessment(
                ledger,
                second,
                artifacts,
                "CONFLICT",
                outcome=outcome,
                conflicting_assertion_ids=conflicts,
                input_record_ids=inputs,
            )
        assert ledger.path.read_bytes() == before


class TestDecisionEvidenceLiesInsideTheProposal:
    """A decision may only cite evidence assertions carried by its own proposal
    (second self-inquisition S2, src/malleus/assent.py:1318-1321)."""

    def test_accept_cites_its_own_evidence_assertions(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        source = add_source_artifact(ledger)
        proposal, _, _ = record_proposal(
            ledger,
            evidence_count=2,
            source_artifact=source,
        )
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        decision = decide_epistemically(
            ledger,
            proposal,
            assessment,
            artifacts,
            evidence_assertion_ids=list(proposal["evidence_assertion_ids"]),
        )
        projection = ledger.replay()
        assert decision["evidence_assertion_ids"] == proposal["evidence_assertion_ids"]
        assert projection.proposal_states[proposal["id"]] == ProposalState.ACCEPTED

    def test_decision_citing_another_proposals_evidence_is_refused(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        source = add_source_artifact(ledger)
        first, _, _ = record_proposal(
            ledger,
            evidence_count=1,
            source_artifact=source,
        )
        second, _, _ = record_proposal(
            ledger,
            minute=6,
            proposal_id="proposal:2",
            proposal_key="proposal-key:2",
            claim_id="claim:2",
            claim_key="claim-key:2",
            evidence_count=1,
            source_artifact=source,
        )
        assessment = record_type_assessment(
            ledger,
            second,
            artifacts["monitor"],
            assessment_id="assessment:satisfied:2",
        )
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="evidence is outside proposal"):
            decide_epistemically(
                ledger,
                second,
                assessment,
                artifacts,
                evidence_assertion_ids=list(first["evidence_assertion_ids"]),
            )
        assert ledger.path.read_bytes() == before


class TestContextStateDigestsAreValidated:
    """Every context state digest a logic check names is checked for digest
    format (second self-inquisition S2, src/malleus/assent.py:967-968)."""

    def test_logic_check_records_context_state_digests(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        digests = ("sha256:" + "8" * 64, "sha256:" + "9" * 64)
        check, _ = record_logic_check(
            ledger,
            proposal,
            artifacts,
            context_state_digests=digests,
        )
        recorded = ledger.replay().objects[check["id"]]["record"]
        assert recorded["context_state_digests"] == list(digests)

    @pytest.mark.parametrize(
        "digest",
        ["sha256:not-a-digest", "", "8" * 64],
    )
    def test_malformed_context_state_digest_is_refused(self, ledger, digest):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        before = ledger.path.read_bytes()
        with pytest.raises(LedgerError, match="context_state_digest must be a sha256 digest"):
            record_logic_check(
                ledger,
                proposal,
                artifacts,
                context_state_digests=(digest,),
            )
        assert ledger.path.read_bytes() == before


class TestALedgerAnchoredUnderAnEarlierGrammarStillReplays:
    """Reported by an adopting project whose deploy gate this blocked, and
    reproduced here: not one ontology byte changed and the recorded hash
    stopped matching, because the payload grammar version sits inside the
    hashed payload and 0.11.0 made it conditional.

    A hash written into an accepted append-only ledger is a public contract.
    The ledger cannot be rewritten to match a new hashing rule, so the rule
    must be able to verify what the ledger already holds."""

    def _legacy_hash(self):
        from malleus.ontology import (
            LEGACY_FINGERPRINT_VERSION,
            OntologyRegistry,
            bundled_ontology_path,
        )
        registry = OntologyRegistry(bundled_ontology_path("assent.yaml"))
        return registry, f"sha256:{registry.content_hash_under(LEGACY_FINGERPRINT_VERSION)}"

    def test_the_same_bytes_hash_differently_under_the_two_grammars(self):
        """The premise. If this ever stops holding, the rest is theatre."""
        registry, legacy = self._legacy_hash()
        assert legacy != f"sha256:{registry.content_hash()}"
        assert registry.verifying_grammar(legacy) == 3
        assert registry.verifying_grammar(f"sha256:{registry.content_hash()}") == 4

    def test_a_hash_matching_no_known_grammar_still_refuses(self):
        registry, _legacy = self._legacy_hash()
        assert registry.verifying_grammar("sha256:" + "0" * 64) is None

    def test_a_ledger_written_under_the_old_grammar_replays(self, tmp_path):
        from malleus.ledger import JsonlLedger
        registry, legacy = self._legacy_hash()
        current = f"sha256:{registry.content_hash()}"

        written_then = JsonlLedger(tmp_path / "l.jsonl", legacy)
        written_then.append(
            event_id="e1", event_type="ARTIFACT_RECORDED",
            transaction_time="2026-01-01T00:00:00+00:00",
            actor_id="actor:1", payload={"artifact_type": "SourceArtifact", "artifact": {}},
            validate=lambda events: None,
        )

        read_now = JsonlLedger(tmp_path / "l.jsonl", current, (legacy,))
        events = read_now.read()
        assert len(events) == 1
        assert read_now.verified_ontology_hashes == (legacy,), (
            "the grammar that verified must be reported, not absorbed"
        )

    def test_a_ledger_that_declares_no_history_still_refuses(self, tmp_path):
        """Accepting an older grammar is a declaration, never an assumption."""
        from malleus.ledger import JsonlLedger, LedgerError
        registry, legacy = self._legacy_hash()
        written_then = JsonlLedger(tmp_path / "l.jsonl", legacy)
        written_then.append(
            event_id="e1", event_type="ARTIFACT_RECORDED",
            transaction_time="2026-01-01T00:00:00+00:00",
            actor_id="actor:1", payload={"artifact_type": "SourceArtifact", "artifact": {}},
            validate=lambda events: None,
        )
        strict = JsonlLedger(tmp_path / "l.jsonl", f"sha256:{registry.content_hash()}")
        with pytest.raises(LedgerError, match="under any payload grammar"):
            strict.read()

    def test_a_genuinely_foreign_hash_is_refused_even_with_history_declared(self, tmp_path):
        from malleus.ledger import JsonlLedger, LedgerError
        registry, legacy = self._legacy_hash()
        current = f"sha256:{registry.content_hash()}"
        foreign = JsonlLedger(tmp_path / "l.jsonl", "sha256:" + "7" * 64)
        foreign.append(
            event_id="e1", event_type="ARTIFACT_RECORDED",
            transaction_time="2026-01-01T00:00:00+00:00",
            actor_id="actor:1", payload={"artifact_type": "SourceArtifact", "artifact": {}},
            validate=lambda events: None,
        )
        reader = JsonlLedger(tmp_path / "l.jsonl", current, (legacy,))
        with pytest.raises(LedgerError, match="under any payload grammar"):
            reader.read()
